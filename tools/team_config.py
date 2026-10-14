"""Trusted validator and transactional team installation; fetched code is never executed."""
import argparse,hashlib,json,os,pathlib,re,shutil,sys,tempfile,uuid
SKILLS=23
NAMES=set("pz-2d-asset-pipeline pz-3d-asset-pipeline pz-api-audit pz-artifact-retention pz-build42-compatibility pz-character-animation pz-ci-automation pz-clean-room-research pz-debug-root-cause pz-dedicated-server-sftp pz-deploy pz-github-versioning pz-item-and-recipe-development pz-mod-compatibility pz-mp-audit pz-persistence-and-migration pz-publish pz-release-audit pz-repository-governance pz-repository-hygiene pz-repository-startup pz-security-permissions pz-ui-ux-development".split())
def digest(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def files(src):
 out=[]
 for base,dirs,names in os.walk(src,followlinks=False):
  dirs[:]=[d for d in dirs if d not in ('.git','__pycache__')]
  for name in dirs+names:
   p=pathlib.Path(base)/name
   if p.is_symlink() or getattr(p,'is_junction',lambda:False)():raise ValueError('linked source rejected')
  out.extend(pathlib.Path(base)/n for n in names if n!='MANIFEST.sha256.json')
 return out
def validate(src):
 src=pathlib.Path(src)
 for n in ['AGENTS.md','VERSION','.codex/config.toml','README.md','MANIFEST.sha256.json']:
  if not (src/n).is_file():raise ValueError('missing '+n)
 version=(src/'VERSION').read_text(encoding='utf-8').strip()
 if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?',version):raise ValueError('invalid version')
 actual={};seen=set()
 for p in files(src):
  rel=p.relative_to(src).as_posix();lower=rel.lower()
  if lower in seen:raise ValueError('case collision')
  seen.add(lower)
  if p.stat().st_size>5000000:raise ValueError('oversized file')
  if any(x in lower for x in ('local.settings.json','.env','password','credential','.ppk','.pem','.pfx','private.key')) and not lower.endswith('.example.json'):raise ValueError('sensitive filename')
  if p.suffix.lower() not in ('.md','.json','.py','.ps1','.toml','.yml','.yaml','') and p.name not in ('.gitignore',):raise ValueError('unexpected file type '+rel)
  actual[rel]=digest(p)
 dirs={p.name for p in (src/'.agents/skills').iterdir() if p.is_dir()}
 if dirs!=NAMES:raise ValueError('skill allowlist mismatch')
 for name in NAMES:
  text=(src/'.agents/skills'/name/'SKILL.md').read_text(encoding='utf-8')
  if not text.startswith('---\n') or not re.search(r'^name: '+re.escape(name)+r'$',text,re.M) or not re.search(r'^description: .+',text,re.M):raise ValueError('invalid skill '+name)
 if json.loads((src/'MANIFEST.sha256.json').read_text(encoding='utf-8'))!=actual:raise ValueError('manifest mismatch')
 return {'skills':23,'files':len(actual),'version':version}
def state_path(home):return pathlib.Path(home)/'.codex/b47anced-team-state.json'
def managed(src):return [p.relative_to(src).as_posix() for p in files(src) if p.relative_to(src).as_posix().startswith('.agents/skills/')]
def mappings(src,home,initial,workspace=None):
 result=[(src/'AGENTS.md',home/'.codex/AGENTS.md','global/AGENTS.md')]
 for rel in managed(src):result.append((src/rel,home/rel,'global/'+rel))
 for p in files(src):
  rel=p.relative_to(src).as_posix()
  if rel.startswith(('tools/','templates/','docs/')) or rel in ('VERSION','README.md','CHANGELOG.md','AGENTS.md','TEAM-ONBOARDING.md'):
   result.append((p,home/'.codex/b47anced-team'/rel,'hub/'+rel))
 if initial and not (home/'.codex/config.toml').exists():result.append((src/'.codex/config.toml',home/'.codex/config.toml','initial-config'))
 if workspace:
  for source,dst,key in list(result):
   if key=='global/AGENTS.md':result.append((src/'templates/WORKSPACE_AGENTS.md',workspace/'AGENTS.md','workspace/AGENTS.md'))
   elif key.startswith('hub/tools/'):result.append((source,workspace/key[len('hub/'):],'workspace/'+key[len('hub/'):]))
   elif key.startswith('hub/templates/'):result.append((source,workspace/'templates/current'/key[len('hub/templates/'):],'workspace/templates/'+key[len('hub/templates/'):]))
 return result
def check_drift(home):
 st=state_path(home)
 if not st.exists():raise ValueError('missing installation state')
 old=json.loads(st.read_text(encoding='utf-8'))
 for key,r in old['managed'].items():
  p=pathlib.Path(r['path'])
  if not p.is_file() or digest(p)!=r['sha256']:raise ValueError('managed drift: '+key)
 return old
def install(src,home,backup_base,initial=False,migrate=False,workspace=None,commit=None):
 src=pathlib.Path(src);home=pathlib.Path(home);info=validate(src);st=state_path(home)
 old=json.loads(st.read_text(encoding='utf-8')) if st.exists() else {'managed':{}}
 if st.exists():check_drift(home)
 entries=mappings(src,home,initial,pathlib.Path(workspace) if workspace else None)
 for _,dst,key in entries:
  if dst.exists() and key not in old['managed'] and not (initial and migrate):raise ValueError('untracked existing file: '+key)
  for parent in [dst]+list(dst.parents):
   if parent==home or (workspace and parent==pathlib.Path(workspace)):break
   if parent.is_symlink() or getattr(parent,'is_junction',lambda:False)():raise ValueError('linked destination rejected')
 backup=pathlib.Path(backup_base)/uuid.uuid4().hex;backup.mkdir(parents=True)
 journal=[];moved=[];oldstate=st.read_bytes() if st.exists() else None
 try:
  # Remove only verified team duplicates; retain unrelated project-local skills.
  if workspace:
   for name in NAMES:
    folder=pathlib.Path(workspace)/'.agents/skills'/name
    canonical=home/'.agents/skills'/name
    if folder.exists():
     if folder.is_symlink() or getattr(folder,'is_junction',lambda:False)():raise ValueError('linked skill needs manual review')
     expected={p.relative_to(folder).as_posix():digest(p) for p in folder.rglob('*') if p.is_file()}
     installed={p.relative_to(canonical).as_posix():digest(p) for p in canonical.rglob('*') if p.is_file()} if canonical.exists() else {}
     if expected!=installed:raise ValueError('workspace skill is customized: '+name)
     archived=backup/'consolidated-skills'/name;archived.parent.mkdir(parents=True,exist_ok=True)
     shutil.move(str(folder),str(archived));moved.append((folder,archived))
  for source,dst,key in entries:
   existed=dst.exists();b=backup/key
   if existed:b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dst,b)
   journal.append((dst,key,existed));dst.parent.mkdir(parents=True,exist_ok=True)
   fd,tmp=tempfile.mkstemp(prefix='.b47-',dir=dst.parent);os.close(fd)
   try:
    shutil.copy2(source,tmp)
    if key=='global/AGENTS.md' and existed:
     existing=dst.read_text(encoding='utf-8-sig');incoming=source.read_text(encoding='utf-8')
     pattern=r'(?s)<!-- BEGIN B47ANCED TEAM -->.*?<!-- END B47ANCED TEAM -->'
     if re.search(pattern,existing):
      pathlib.Path(tmp).write_text(re.sub(pattern,lambda match:incoming.strip(),existing),encoding='utf-8')
     elif key not in old['managed']:
      pathlib.Path(tmp).write_text(existing.rstrip()+'\n\n'+incoming,encoding='utf-8')
    if key=='workspace/AGENTS.md' and existed and key not in old['managed']:
     pathlib.Path(tmp).write_text(dst.read_text(encoding='utf-8-sig').rstrip()+'\n\n'+source.read_text(encoding='utf-8'),encoding='utf-8')
    os.replace(tmp,dst)
   finally:
    if pathlib.Path(tmp).exists():pathlib.Path(tmp).unlink()
  newstate={'version':info['version'],'commit':commit,'workspace':str(workspace) if workspace else None,'backup':str(backup),'managed':{k:{'path':str(dst),'sha256':digest(dst)} for _,dst,k in entries if k!='initial-config'}}
  if oldstate:(backup/'previous-state.json').write_bytes(oldstate)
  st.parent.mkdir(parents=True,exist_ok=True);fd,tmp=tempfile.mkstemp(dir=st.parent);os.close(fd)
  pathlib.Path(tmp).write_text(json.dumps(newstate,indent=2),encoding='utf-8');os.replace(tmp,st)
 except BaseException:
  for dst,key,existed in reversed(journal):
   if existed:shutil.copy2(backup/key,dst)
   elif dst.exists():dst.unlink()
  if oldstate:st.write_bytes(oldstate)
  elif st.exists():st.unlink()
  for folder,archived in reversed(moved):
   if archived.exists():shutil.move(str(archived),str(folder))
  raise
 return newstate

def main():
 a=argparse.ArgumentParser();a.add_argument('action',choices=['validate','install','drift']);a.add_argument('--source');a.add_argument('--home',default=str(pathlib.Path.home()));a.add_argument('--backup-dir');a.add_argument('--workspace');a.add_argument('--commit');a.add_argument('--initial',action='store_true');a.add_argument('--migrate',action='store_true');v=a.parse_args()
 try:
  home=pathlib.Path(v.home).resolve()
  if v.action=='validate':result=validate(pathlib.Path(v.source).resolve())
  elif v.action=='drift':result={'status':'PASS','version':check_drift(home)['version']}
  else:result=install(pathlib.Path(v.source).resolve(),home,pathlib.Path(v.backup_dir or home/'.codex/b47anced-backups'),v.initial,v.migrate,v.workspace,v.commit);result={'status':'installed','version':result['version'],'files':len(result['managed']),'backup':result['backup']}
  print(json.dumps(result));return 0
 except Exception as e:print('ERROR: '+str(e),file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
