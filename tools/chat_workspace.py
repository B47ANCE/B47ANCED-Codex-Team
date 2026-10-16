"""Local metadata-only chat picker. Never rewrites Codex history or databases."""
import argparse,datetime,hashlib,json,os,pathlib,tempfile,uuid
from code_workspace import save_owned

def scan(home):
    home=pathlib.Path(home);titles={};chats=[]
    index=home/'session_index.jsonl'
    if index.is_file():
        for line in index.read_text(encoding='utf-8-sig',errors='replace').splitlines():
            try:r=json.loads(line)
            except ValueError:continue
            if r.get('id'):titles[r['id']]=r.get('thread_name') or r.get('title')
    session_root=home/'sessions'
    if session_root.is_symlink() or getattr(session_root,'is_junction',lambda:False)():raise ValueError('Linked history store preserved')
    paths=[]
    for folder,dirs,names in os.walk(session_root,followlinks=False):
        dirs[:]=[d for d in dirs if not (pathlib.Path(folder)/d).is_symlink() and not getattr(pathlib.Path(folder)/d,'is_junction',lambda:False)()]
        paths.extend(pathlib.Path(folder)/n for n in names if n.endswith('.jsonl'))
    for path in paths:
        if path.is_symlink():continue
        try:
            with path.open(encoding='utf-8') as stream:r=json.loads(stream.readline(1048576))
            if r.get('type')!='session_meta':continue
            d=r['payload'];ident=str(uuid.UUID(d['id']))
            if isinstance(d.get('source'),dict):continue # sub-agent sessions are not independent chats
            chats.append(dict(id=ident,title=str(titles.get(ident) or ident),cwd=d.get('cwd'),
                              created=d.get('timestamp'),session_file=str(path.resolve())))
        except (OSError,ValueError,KeyError,TypeError):continue
    return sorted({c['id']:c for c in chats}.values(),key=lambda c:c.get('created') or '',reverse=True)

def generate(home,base_workspace,output,source_tools=None):
    home=pathlib.Path(home).resolve();output=pathlib.Path(output).resolve();base_workspace=pathlib.Path(base_workspace).resolve()
    source_tools=pathlib.Path(source_tools or pathlib.Path(__file__).parent)
    runtime=home/'cli-chat-runtime'
    base=json.loads(base_workspace.read_text(encoding='utf-8-sig'));chats=scan(home)
    projects=[]
    for folder in base['folders']:
        p=pathlib.Path(folder['path'])
        if not p.is_absolute():p=base_workspace.parent/p
        if not p.is_dir():continue
        projects.append(dict(label=folder.get('name',p.name),value=str(p.resolve())))
        if folder.get('name')=='Mod Repositories':
            projects.extend(dict(label=d.name,value=str(d.resolve())) for d in sorted(p.iterdir()) if d.is_dir() and not d.name.startswith('.'))
    if not projects:raise ValueError('No existing project directories')
    workspace=dict(folders=base['folders'],settings={},tasks=dict(version='2.0.0',tasks=[
        dict(label='Chats: Resume saved chat',type='process',command='powershell.exe',
             args=['-NoLogo','-NoProfile','-File',str(runtime/'Resume-CodexChat.ps1'),'-SessionId','${input:chat}','-Target','${input:project}','-CodexHome',str(home)],problemMatcher=[],presentation=dict(reveal='always',panel='new')),
        dict(label='Chats: Refresh saved-chat picker',type='process',command=os.sys.executable,
             args=[str(runtime/'chat_workspace.py'),'--home',str(home),'--base',str(base_workspace),'--output',str(output)],problemMatcher=[]),
        dict(label='Chats: Browse all local chats in Codex',type='process',command='powershell.exe',
             args=['-NoLogo','-NoProfile','-File',str(runtime/'Resume-CodexChat.ps1'),'-BrowseAll','-CodexHome',str(home)],problemMatcher=[])
    ],inputs=[dict(id='chat',type='pickString',description='Choose a saved local Codex chat; stop its other active surface first',
                   options=[dict(label=c['title']+' | '+str(c.get('created') or '')[:10]+' | '+c['id'][:8],value=c['id']) for c in chats]),
              dict(id='project',type='pickString',description='Choose the owning project for this chat',options=projects)]))
    if not chats:
        workspace['tasks']['tasks']=workspace['tasks']['tasks'][1:]
        workspace['tasks']['inputs']=workspace['tasks']['inputs'][1:]
    ledger=runtime/'chats.local.json'
    values={output:(json.dumps(workspace,indent=2)+'\n').encode(),ledger:(json.dumps(dict(chats=chats,archived='Excluded; original archives preserved'),indent=2)+'\n').encode()}
    for name in ('Resume-CodexChat.ps1','chat_workspace.py','code_workspace.py'):
        values[runtime/name]=(source_tools/name).read_bytes()
    for path in values:
        for parent in (path,*path.parents):
            if parent.is_symlink() or getattr(parent,'is_junction',lambda:False)():raise ValueError('Linked output preserved')
    save_owned(values,runtime/'outputs.local.json',home/'cli-chat-backups')
    return dict(saved_chats=len(chats),project_choices=len(projects),workspace=str(output),history_modified=False,automatic_agent_runs=0)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--home',default=os.environ.get('CODEX_HOME',str(pathlib.Path.home()/'.codex')));p.add_argument('--base',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    print(json.dumps(generate(a.home,a.base,a.output)))
