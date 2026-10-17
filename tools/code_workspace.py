"""Create a developer-local VS Code workspace without changing project/editor files."""
import argparse, hashlib, json, os, pathlib, tempfile, uuid

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def save_owned(files, state_path, backup_root, reviewed_custom=None):
    reviewed_custom=reviewed_custom or {}
    if state_path.is_symlink():
        raise ValueError('Linked state preserved')
    state=json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}
    previous={}
    for path,raw in files.items():
        if path.is_symlink():
            raise ValueError('Linked output preserved')
        old=path.read_bytes() if path.exists() else None
        previous[path]=old
        if path in reviewed_custom and (old is None or reviewed_custom[path]!=digest(old)):
            raise ValueError('Custom output changed during review')
        if old is not None and old!=raw and state.get(str(path))!=digest(old) and reviewed_custom.get(path)!=digest(old):
            raise ValueError('Customized output preserved for manual review')
    changed={path:raw for path,raw in files.items() if previous[path]!=raw}
    if changed:
        backup=backup_root/uuid.uuid4().hex
        for path in changed:
            if previous[path] is not None:
                backup.mkdir(parents=True,exist_ok=True)
                (backup/path.name).write_bytes(previous[path])
    written=[]
    try:
        for path,raw in changed.items():
            path.parent.mkdir(parents=True,exist_ok=True)
            if (path.read_bytes() if path.exists() else None)!=previous[path]:
                raise ValueError('Output changed concurrently')
            fd,temp=tempfile.mkstemp(prefix='.b47-',dir=path.parent)
            try:
                with os.fdopen(fd,'wb') as stream:
                    stream.write(raw)
                os.replace(temp,path)
                written.append(path)
            finally:
                if os.path.exists(temp):
                    os.unlink(temp)
        state_path.parent.mkdir(parents=True,exist_ok=True)
        # A narrow authorized merge never grants ownership of the whole custom file.
        state.update({str(path):digest(raw) for path,raw in files.items() if path not in reviewed_custom})
        fd,temp=tempfile.mkstemp(prefix='.b47-state-',dir=state_path.parent)
        try:
            with os.fdopen(fd,'w',encoding='utf-8') as stream:
                stream.write(json.dumps(state,indent=2)+'\n')
            os.replace(temp,state_path)
        finally:
            if os.path.exists(temp):
                os.unlink(temp)
    except Exception:
        for path in written:
            if path.read_bytes()!=files[path]:
                continue
            if previous[path] is None:
                path.unlink()
            else:
                path.write_bytes(previous[path])
        raise

def create(workspace, repositories, home, python, powershell, team_tools, source_tools, merge_overview=False):
    workspace=pathlib.Path(workspace).resolve()
    home=pathlib.Path(home).resolve()
    root=pathlib.Path(repositories).resolve() if repositories else None
    if root and not root.is_dir():
        raise ValueError('Repository root must exist')
    runtime=home/'.codex/cli-workflow-runtime'
    launcher=runtime/'Invoke-TeamWorkflow.ps1'
    payload=(pathlib.Path(source_tools)/'Invoke-TeamWorkflow.ps1').read_bytes()
    folders=[dict(name='Codex Workspace',path=str(workspace))]
    targets=[dict(label='Codex Workspace (research/setup)',value=str(workspace))]
    if root:
        folders.append(dict(name='Mod Repositories',path=str(root)))
        targets += [dict(label=p.name,value=str(p)) for p in sorted(root.iterdir(),key=lambda p:p.name.lower())
                    if p.is_dir() and not p.name.startswith('.')]
    base=['-NoLogo','-NoProfile','-File',str(launcher),'-HomeDirectory',str(home),'-TeamTools',str(team_tools)]
    if python:
        base+=['-PythonExe',str(python)]
    if root:
        base+=['-RepositoryRoot',str(root)]
    actions=[('codex','Codex CLI: Start in project'),('resume','Codex CLI: Resume in project'),
             ('freshness','PZ: Check repository freshness'),('versions','PZ: Check project versions'),
             ('mcp-list','Codex: List MCP connections'),('update-check','Team: Check for updates'),
             ('update','Team: Apply validated update'),('rollback-preview','Team: Preview rollback'),
             ('meshy-balance','Meshy: Check connection and credits (free)'),('meshy-key','Meshy: Set key locally (masked)')]
    if root:
        actions.append(('verify-team','Team: Verify mod repositories and 23 skills'))
        actions += [('overview-refresh','Overview: Refresh features and connections'),
                    ('overview-open','Overview: Open mod ecosystem'),
                    ('overview-watch','Overview: Keep features and connections current')]
    tasks=[]
    for action,label in actions:
        args=base+['-Action',action]
        if action.startswith('overview-'):
            args+=['-Workspace',str(workspace)]
        if action in {'codex','resume','freshness','versions'}:
            args+=['-Target','${input:pzProject}']
        tasks.append(dict(label=label,type='process',command=str(powershell),args=args,
                          options=dict(cwd=str(workspace)),problemMatcher=[],
                          presentation=dict(reveal='always',panel='dedicated',focus=True)))
        if action=='overview-watch':
            tasks[-1].update(isBackground=True,runOptions=dict(runOn='folderOpen'))
            tasks[-1]['presentation']=dict(reveal='silent',panel='dedicated',focus=False)
    data=dict(folders=folders,settings={},
              extensions=dict(recommendations=['openai.chatgpt']),
              tasks=dict(version='2.0.0',tasks=tasks,inputs=[dict(id='pzProject',type='pickString',
                    description='Choose the project that owns this workflow',options=targets)]))
    dest=workspace/'B47ANCED.code-workspace'
    reviewed_custom={}
    original=None
    if merge_overview:
        if not root or not dest.is_file() or dest.is_symlink():
            raise ValueError('Overview merge requires an existing regular JSON workspace and repository root')
        original=dest.read_bytes()
        # Strict JSON: comments/duplicate keys are refused rather than silently lost.
        def unique(pairs):
            out={}
            for key,value in pairs:
                if key in out:raise ValueError('Duplicate workspace key')
                out[key]=value
            return out
        def invalid_constant(value):raise ValueError('Non-JSON workspace constant')
        existing=json.loads(original.decode('utf-8-sig'),object_pairs_hook=unique,parse_constant=invalid_constant)
        if not isinstance(existing,dict):raise ValueError('Invalid workspace object')
        block=existing.setdefault('tasks',dict(version='2.0.0',tasks=[]))
        if not isinstance(block,dict) or block.get('version')!='2.0.0' or not isinstance(block.get('tasks'),list):
            raise ValueError('Unsupported custom task schema')
        overview_tasks=[t for t in tasks if t['label'].startswith('Overview:')]
        for task in overview_tasks:
            matches=[t for t in block['tasks'] if isinstance(t,dict) and t.get('label')==task['label']]
            if len(matches)>1 or matches and matches[0]!=task:
                raise ValueError('Conflicting custom overview task preserved')
            if not matches:block['tasks'].append(task)
        data=existing
        reviewed_custom[dest]=digest(original)
    encoded=(json.dumps(data,indent=2)+'\n').encode('utf-8')
    if original is not None and json.loads(original.decode('utf-8-sig'))==data:encoded=original
    files={launcher:payload,dest:encoded}
    if root:
        # Explicit setup pins executable overview code and view. Validated updates
        # still install new code inert; the watcher never imports fetched helpers.
        overview=runtime/'overview'
        for name in ('mod_overview.py','code_workspace.py'):
            files[overview/name]=(pathlib.Path(source_tools)/name).read_bytes()
        for name in ('catalog.json','view.json'):
            files[overview/name]=(pathlib.Path(source_tools).parent/'templates/overview'/name).read_bytes()
    save_owned(files,runtime/'workspace-state.json',home/'.codex/cli-workflow-backups',reviewed_custom)
    return dict(workspace=str(dest),tasks=len(tasks),project_choices=len(targets),automatic_tasks=1 if root else 0)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    for name in ['workspace','home','powershell','team-tools','source-tools']:
        parser.add_argument('--'+name,required=True)
    parser.add_argument('--repositories')
    parser.add_argument('--python')
    parser.add_argument('--merge-overview-tasks',action='store_true')
    args=parser.parse_args()
    try:
        result=create(args.workspace,args.repositories,args.home,args.python,args.powershell,args.team_tools,args.source_tools,args.merge_overview_tasks)
    except Exception:
        raise SystemExit('VS Code workspace setup refused: verify paths and preserve/review existing workspace or launcher customization.')
    print(json.dumps(result))
