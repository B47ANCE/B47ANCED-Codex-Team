"""Read-only portfolio inventory. Never executes project code or fetches remotes."""
import argparse
import copy
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess
import time

STATUSES={'Source','Foundation','Planned','Blocked','Separate branch','Historical','UNKNOWN'}
KINDS={'Required','Optional','Migration','Planned'}
MAX_FILES=20000

def linked(p):
    return p.is_symlink() or getattr(p,'is_junction',lambda:False)()

def safe_path(root,relative):
    root=Path(root).resolve()
    relative=Path(relative)
    if relative.is_absolute() or '..' in relative.parts or not relative.parts:
        raise ValueError('Evidence paths must be repository-relative')
    p=root
    for part in relative.parts:
        p=p/part
        if linked(p):raise ValueError('Linked inputs are not followed')
    if not p.resolve().is_relative_to(root):raise ValueError('Path escaped root')
    return p

def read_json(p):
    if linked(p) or p.stat().st_size>2000000:raise ValueError('Unsafe/oversized JSON')
    return json.loads(p.read_text(encoding='utf-8-sig'))

def git(p,*args):
    # No shell, hooks, scripts, network, or mutating Git operations.
    r=subprocess.run(['git','-C',str(p),*args],capture_output=True,timeout=10,
                     encoding='utf-8',errors='replace')
    return r.stdout.strip() if r.returncode==0 else None

def source_roots(repo):
    roots=[]
    for name in ('src','Contents/mods'):
        p=safe_path(repo,name)
        if p.is_dir():roots.append(name)
    return roots

def walk_files(repo,roots):
    count=0
    for name in roots:
        base=safe_path(repo,name)
        if not base.exists():continue
        if base.is_file():
            yield base
            continue
        for parent,dirs,files in os.walk(base,followlinks=False):
            dirs[:]=sorted(d for d in dirs if not d.startswith('.') and not linked(Path(parent)/d))
            for name in sorted(files):
                p=Path(parent)/name
                if linked(p):continue
                count+=1
                if count>MAX_FILES:raise ValueError('Source file budget exceeded')
                yield p

def fingerprint(repo,roots):
    digest=hashlib.sha256()
    for p in sorted(set(walk_files(repo,roots)),key=lambda p:p.as_posix()):
        if p.suffix.lower() not in {'.lua','.txt','.json','.md','.info',''}:continue
        if p.stat().st_size>10000000:raise ValueError('Source file budget exceeded')
        before=p.stat()
        raw=p.read_bytes()
        after=p.stat()
        if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):
            raise ValueError('Concurrent source change; retry next refresh')
        digest.update(p.relative_to(repo).as_posix().encode());digest.update(b'\0')
        digest.update(hashlib.sha256(raw).digest())
    return digest.hexdigest()

def metadata(repo):
    result=[]
    for p in walk_files(repo,source_roots(repo)):
        if p.name!='mod.info':continue
        if p.stat().st_size>100000:raise ValueError('Oversized mod.info')
        d={'path':p.relative_to(repo).as_posix()}
        for line in p.read_text(encoding='utf-8-sig',errors='replace').splitlines():
            if '=' in line:
                k,v=line.split('=',1)
                if k.strip() in {'id','name','require','modversion'}:d[k.strip()]=v.strip()
        result.append(d)
    return result

def validate_descriptor(d,repo=None):
    if not isinstance(d,dict):raise ValueError('Descriptor must be an object')
    if d.get('schema')!=1 or not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,79}',d.get('id','')):
        raise ValueError('Invalid descriptor schema/id')
    if not isinstance(d.get('name'),str) or not d['name'].strip():raise ValueError('Missing name')
    if not isinstance(d.get('features'),list) or len(d['features'])>200:raise ValueError('Invalid features')
    for f in d['features']:
        if f.get('status') not in STATUSES or not isinstance(f.get('text'),str) or len(f['text'])>3000:
            raise ValueError('Invalid feature')
    if not isinstance(d.get('limits',''),str):raise ValueError('Invalid limits')
    if not isinstance(d.get('reviewed',False),bool):raise ValueError('Invalid review flag')
    if d.get('reviewed') and not d['features']:raise ValueError('Reviewed features must not be empty')
    for rel in d.get('evidence',[]):
        if not isinstance(rel,str):raise ValueError('Invalid evidence path')
        safe_path(repo or Path.cwd(),rel)
    for e in d.get('relations',[]):
        if e.get('kind') not in KINDS or not isinstance(e.get('target'),str) or not isinstance(e.get('text'),str):
            raise ValueError('Invalid relation')
    return d

def validate_catalog(catalog):
    ids=[]
    for m in catalog['mods']:
        validate_descriptor(dict(m,schema=1))
        safe_path(Path.cwd(),m['folder'])
        for alias in m.get('aliases',[]):safe_path(Path.cwd(),alias)
        ids.append(m['id'])
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate project ids')
    for e in catalog['edges']:
        if e['a'] not in ids or e['b'] not in ids or e['kind'] not in KINDS:raise ValueError('Invalid edge')
    for f in catalog['flows']:
        if not set(f['mods'])<=set(ids):raise ValueError('Invalid shared feature')

def snapshot(catalog,root):
    validate_catalog(catalog)
    data=copy.deepcopy(catalog)
    root=Path(root).resolve() if root else None
    if root and not root.is_dir():raise ValueError('Repository root must exist')
    found={};seen=set();unknown=[]
    if root:
        # Prefer canonical folder before duplicates; never crawl .worktrees/history.
        folders=[safe_path(root,m['folder']) for m in data['mods']]
        for m in data['mods']:folders.extend(safe_path(root,a) for a in m.get('aliases',[]))
        folders.extend(sorted((p for p in root.iterdir() if p.is_dir() and not p.name.startswith('.') and not linked(p)),key=lambda p:p.name.lower()))
        visited=set()
        for p in folders:
            if p in visited or not p.is_dir() or linked(p):continue
            visited.add(p)
            common=git(p,'rev-parse','--path-format=absolute','--git-common-dir')
            if common and common in seen:continue
            meta=metadata(p)
            modids={x.get('id') for x in meta}
            match=next((m for m in data['mods'] if p.name in [m['folder'],*m.get('aliases',[])] or modids.intersection(m.get('mod_ids',[]))),None)
            if not match and not meta:continue
            if common:seen.add(common)
            if match:
                if match['id'] in found:continue
            else:
                match=dict(id='local-'+hashlib.sha256(p.name.encode()).hexdigest()[:12],folder=p.name,name=next((x.get('name') for x in meta if x.get('name')),p.name),features=[dict(status='UNKNOWN',text='New project: add docs/MOD_OVERVIEW.json to describe its current features.')],limits='No reviewed feature inventory.',evidence=[],mod_ids=list(filter(None,modids)))
                data['mods'].append(match)
            found[match['id']]=(p,meta)
    for m in data['mods']:
        m.pop('git',None);m.pop('metadata',None)
        if m['id'] not in found:
            m['review']='NOT INSTALLED — shared snapshot only'
            m['installed']=False
            continue
        p,meta=found[m['id']]
        version=safe_path(p,'VERSION')
        m['version']=version.read_text(encoding='utf-8-sig').strip() if version.is_file() else 'No root VERSION; metadata only'
        m['installed']=True;m['local_folder']=p.name;m['metadata']=meta
        m['head']=git(p,'rev-parse','HEAD') or 'Not a verified Git checkout'
        m['branch']=git(p,'branch','--show-current') or 'UNKNOWN'
        descriptor=safe_path(p,'docs/MOD_OVERVIEW.json')
        if descriptor.is_file():
            d=validate_descriptor(read_json(descriptor),p)
            if d['id']!=m['id']:raise ValueError('Descriptor id does not match project')
            for key in ('name','features','limits','relations'):m[key]=d.get(key,m.get(key,[] if key=='relations' else ''))
            if not m['features']:m['features']=[dict(status='UNKNOWN',text='Descriptor draft has no reviewed feature list.')]
            m['evidence']=d.get('evidence',[])
            current=fingerprint(p,source_roots(p)+['README.md','VERSION'])
            m['review']='CURRENT DESCRIPTOR — source only' if d.get('reviewed') is True and d.get('version')==m['version'] and d.get('source_digest')==current else 'REVIEW — descriptor not reviewed or version/source differs'
            for rel in m['evidence']:
                if not safe_path(p,rel).is_file():m['review']='REVIEW — missing evidence'
        else:
            roots=m.get('source_roots',source_roots(p))+['README.md','VERSION']
            current=fingerprint(p,roots)
            m['review']='SNAPSHOT MATCH — source only' if current==m.get('source_digest') else 'REVIEW — source changed since feature audit'
        m['unresolved_requires']=sorted({x.strip() for row in meta for x in row.get('require','').split(',') if x.strip()})
    owners={x:m['id'] for m in data['mods'] if m.get('installed') for x in {row.get('id') for row in m.get('metadata',[])} if x}
    # Loader requirements are current metadata, not frozen curated edges.
    edges=[e for e in data['edges'] if e['kind']!='Required']
    for m in data['mods']:
        for req in m.get('unresolved_requires',[]):
            if req in owners:
                edges.append(dict(a=owners[req],b=m['id'],kind='Required',text='Current mod.info requires '+req))
        m['unresolved_requires']=[r for r in m.get('unresolved_requires',[]) if r not in owners]
        if m.get('relations') is not None:
            edges=[e for e in edges if not(e['b']==m['id'] and e['kind']!='Required')]
            for e in m['relations']:
                target=next((x['id'] for x in data['mods'] if e['target'] in [x['id'],*x.get('mod_ids',[])]),None)
                if target:edges.append(dict(a=target,b=m['id'],kind=e['kind'],text=e['text']))
    # Missing local installs retain snapshot requirements, explicitly labelled.
    for e in catalog['edges']:
        if e['kind']=='Required' and not next(m for m in data['mods'] if m['id']==e['b']).get('installed'):
            edges.append(dict(e,text='Shared snapshot (not locally checked): '+e['text']))
    data['edges']=list({(e['a'],e['b'],e['kind'],e['text']):e for e in edges}.values())
    data['scope']='Local files only; no fetch, game tests or remote freshness guarantee. Changed source is flagged for feature review. Shared features are reviewed design/source summaries, not proof of a matched runtime build.'
    return data

def render(data,template):
    payload=json.dumps(data,ensure_ascii=False).replace('<','\\u003c')
    # Exported wrapper stores the sandbox document in an HTML attribute.
    return template['html'].replace('__B47_PORTFOLIO_DATA__',html.escape(payload,quote=True))

def write_snapshot(data,template,output):
    from code_workspace import save_owned
    output=Path(os.path.abspath(output))
    if any(linked(p) for p in [output,*output.parents]):raise ValueError('Linked output tree preserved')
    raw=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
    page=render(data,template).encode()
    save_owned({output/'portfolio.json':raw,output/'index.html':page},output/'ownership.json',output/'backups')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repositories')
    parser.add_argument('--catalog',type=Path,default=Path(__file__).resolve().parents[1]/'templates/overview/catalog.json')
    parser.add_argument('--template',type=Path,default=Path(__file__).resolve().parents[1]/'templates/overview/view.json')
    parser.add_argument('--output',type=Path)
    parser.add_argument('--describe-repository',type=Path)
    parser.add_argument('--project-id')
    parser.add_argument('--watch',action='store_true')
    parser.add_argument('--interval',type=int,default=60)
    args=parser.parse_args()
    if args.describe_repository:
        repo=args.describe_repository.resolve()
        if not repo.is_dir() or not args.project_id:parser.error('Descriptor draft needs existing repository and --project-id')
        version=safe_path(repo,'VERSION')
        draft=dict(schema=1,id=args.project_id,name=repo.name,version=version.read_text(encoding='utf-8-sig').strip() if version.is_file() else None,reviewed=False,source_digest=fingerprint(repo,source_roots(repo)+['README.md','VERSION']),features=[],limits='[UNKNOWN] Complete a source review; no new runtime proof.',evidence=['README.md'],relations=[])
        print(json.dumps(draft,ensure_ascii=False,indent=2))
        return
    if not args.output:parser.error('--output is required')
    if args.interval<10:parser.error('Minimum interval is 10 seconds')
    if args.repositories and args.output.resolve().is_relative_to(Path(args.repositories).resolve()):
        parser.error('Output must be outside mod repositories')
    while True:
        try:
            data=snapshot(read_json(args.catalog),args.repositories)
            write_snapshot(data,read_json(args.template),args.output)
        except (ValueError,OSError,KeyError,TypeError,subprocess.SubprocessError) as exc:
            if not args.watch:raise
            print('Overview refresh deferred: '+str(exc),flush=True)
            try:
                old=read_json(args.output/'portfolio.json')
                prefix='REFRESH FAILED — previous snapshot retained; inspect the watcher task. '
                old['scope']=prefix+old.get('scope','').removeprefix(prefix)
                write_snapshot(old,read_json(args.template),args.output)
            except (ValueError,OSError):pass
        if not args.watch:break
        time.sleep(args.interval)

if __name__=='__main__':main()
