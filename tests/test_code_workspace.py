import importlib.util,json,os,pathlib,subprocess,tempfile,unittest
from unittest import mock
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('code_workspace',ROOT/'tools/code_workspace.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class CodeWorkspace(unittest.TestCase):
    def custom(self,args):
        args[0].mkdir(parents=True,exist_ok=True)
        path=args[0]/'B47ANCED.code-workspace'
        data=dict(folders=[dict(path='../my-own-project')],settings={'editor.fontSize':19},launch={'custom':True},
                  extensions={'recommendations':['custom.extension']},tasks={'version':'2.0.0','tasks':[{'label':'My custom task','command':'keep'}],'inputs':[{'id':'mine','type':'promptString'}]})
        path.write_text(json.dumps(data))
        return path,data

    def test_explicit_overview_merge_preserves_custom_fields_and_ownership(self):
        with tempfile.TemporaryDirectory() as td:
            args,_=self.fixture(pathlib.Path(td));path,original=self.custom(args);raw=path.read_bytes()
            m.create(*args,merge_overview=True);merged=json.loads(path.read_text())
            for key in ['folders','settings','launch','extensions']:self.assertEqual(merged[key],original[key])
            self.assertEqual(merged['tasks']['inputs'],original['tasks']['inputs'])
            self.assertEqual(merged['tasks']['tasks'][0],original['tasks']['tasks'][0])
            self.assertEqual(len(merged['tasks']['tasks']),4)
            backups=list((args[2]/'.codex/cli-workflow-backups').rglob('B47ANCED.code-workspace'))
            self.assertEqual([p.read_bytes() for p in backups],[raw])
            after=path.read_bytes();m.create(*args,merge_overview=True);self.assertEqual(path.read_bytes(),after)
            state=json.loads((args[2]/'.codex/cli-workflow-runtime/workspace-state.json').read_text())
            self.assertNotIn(str(path),state)
            with self.assertRaises(ValueError):m.create(*args)
            self.assertEqual(path.read_bytes(),after)

    def test_overview_merge_conflict_or_non_json_preserves_all_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            args,_=self.fixture(pathlib.Path(td));path,data=self.custom(args)
            data['tasks']['tasks'].append({'label':'Overview: Refresh features and connections','command':'custom'})
            for raw in [json.dumps(data).encode(),b'{/* custom comment */}',b'{"settings":{},"settings":{"x":1}}',b'{"settings":{"x":NaN}}']:
                path.write_bytes(raw)
                with self.assertRaises(ValueError):m.create(*args,merge_overview=True)
                self.assertEqual(path.read_bytes(),raw)
                self.assertFalse((args[2]/'.codex/cli-workflow-runtime/Invoke-TeamWorkflow.ps1').exists())

    def test_custom_merge_write_failure_restores_original(self):
        with tempfile.TemporaryDirectory() as td:
            args,_=self.fixture(pathlib.Path(td));path,_=self.custom(args);raw=path.read_bytes()
            replace=m.os.replace;calls=[]
            def fail(source,dest):
                calls.append(dest)
                if len(calls)==2:raise OSError('injected')
                return replace(source,dest)
            with mock.patch.object(m.os,'replace',side_effect=fail):
                with self.assertRaises(OSError):m.create(*args,merge_overview=True)
            self.assertEqual(path.read_bytes(),raw)
            self.assertFalse((args[2]/'.codex/cli-workflow-runtime/Invoke-TeamWorkflow.ps1').exists())

    def test_custom_merge_concurrent_edit_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/'workspace';old=b'original';p.write_bytes(b'concurrent edit')
            with self.assertRaises(ValueError):
                m.save_owned({p:b'merged'},pathlib.Path(td)/'state.json',pathlib.Path(td)/'backups',{p:m.digest(old)})
            self.assertEqual(p.read_bytes(),b'concurrent edit')

    def fixture(self,base):
        home=base/'home';workspace=base/'Workspace with spaces';repos=base/'Mods'
        project=repos/'Custom project';project.mkdir(parents=True)
        (project/'AGENTS.md').write_bytes(b'custom instructions')
        (project/'local.settings.json').write_bytes(b'local settings')
        (repos/'.worktrees'/'hidden').mkdir(parents=True)
        args=(workspace,repos,home,'python.exe','powershell.exe',ROOT/'tools',ROOT/'tools')
        return args,project

    def test_tasks_and_project_files_preserved(self):
        with tempfile.TemporaryDirectory() as td:
            args,project=self.fixture(pathlib.Path(td));result=m.create(*args)
            data=json.loads(pathlib.Path(result['workspace']).read_text())
            self.assertEqual(result['tasks'],14)
            self.assertEqual(result['automatic_tasks'],1)
            self.assertEqual(result['project_choices'],2)
            self.assertEqual(data['settings'],{})
            self.assertEqual((project/'AGENTS.md').read_bytes(),b'custom instructions')
            self.assertEqual((project/'local.settings.json').read_bytes(),b'local settings')
            self.assertFalse((project/'.vscode').exists())
            for task in data['tasks']['tasks']:
                self.assertEqual(task['type'],'process')
                if 'overview-watch' in task['args']:
                    self.assertEqual(task['runOptions'],{'runOn':'folderOpen'})
                    self.assertTrue(task['isBackground'])
                else:self.assertNotIn('runOptions',task)
                self.assertFalse(any(x in task['label'].lower() for x in ['deploy','publish']))
            self.assertNotIn('.worktrees',json.dumps(data))

    def test_idempotent_and_owned_refresh_backed_up(self):
        with tempfile.TemporaryDirectory() as td:
            args,_=self.fixture(pathlib.Path(td));result=m.create(*args)
            path=pathlib.Path(result['workspace']);old=path.read_bytes()
            m.create(*args);self.assertEqual(path.read_bytes(),old)
            (args[1]/'Second project').mkdir()
            result=m.create(*args)
            self.assertEqual(result['project_choices'],3)
            backups=list((args[2]/'.codex/cli-workflow-backups').rglob('B47ANCED.code-workspace'))
            self.assertEqual(len(backups),1);self.assertEqual(backups[0].read_bytes(),old)

    def test_custom_workspace_stops_all_updates(self):
        with tempfile.TemporaryDirectory() as td:
            args,_=self.fixture(pathlib.Path(td));result=m.create(*args)
            path=pathlib.Path(result['workspace']);path.write_bytes(b'custom workspace')
            launcher=args[2]/'.codex/cli-workflow-runtime/Invoke-TeamWorkflow.ps1';old=launcher.read_bytes()
            with self.assertRaises(ValueError):m.create(*args)
            self.assertEqual(path.read_bytes(),b'custom workspace')
            self.assertEqual(launcher.read_bytes(),old)

    def test_unowned_workspace_never_overwritten(self):
        with tempfile.TemporaryDirectory() as td:
            args,_=self.fixture(pathlib.Path(td));args[0].mkdir()
            p=args[0]/'B47ANCED.code-workspace';p.write_bytes(b'pre-existing')
            with self.assertRaises(ValueError):m.create(*args)
            self.assertEqual(p.read_bytes(),b'pre-existing')
            self.assertFalse((args[2]/'.codex/cli-workflow-runtime/Invoke-TeamWorkflow.ps1').exists())

    def test_injected_write_failure_rolls_back_created_output(self):
        with tempfile.TemporaryDirectory() as td:
            args,_=self.fixture(pathlib.Path(td));replace=m.os.replace;calls=[]
            def fail_second(source,dest):
                calls.append(dest)
                if len(calls)==2:raise OSError('injected failure')
                return replace(source,dest)
            with mock.patch.object(m.os,'replace',side_effect=fail_second):
                with self.assertRaises(OSError):m.create(*args)
            self.assertFalse((args[2]/'.codex/cli-workflow-runtime/Invoke-TeamWorkflow.ps1').exists())
            self.assertFalse((args[0]/'B47ANCED.code-workspace').exists())

    def test_missing_repository_root_fails_without_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            base=pathlib.Path(td)
            with self.assertRaises(ValueError):m.create(base/'workspace',base/'missing',base/'home','python','powershell',ROOT/'tools',ROOT/'tools')
            self.assertFalse((base/'workspace').exists())

    @unittest.skipUnless(os.name=='nt','Windows terminal fixture')
    def test_cli_launch_args_and_cwd(self):
        with tempfile.TemporaryDirectory() as td:
            base=pathlib.Path(td);project=base/'project with spaces';project.mkdir();record=base/'args.txt'
            (base/'codex.cmd').write_text('@echo off\necho %*>"%B47_TEST_ARGS%"\ncd>"%B47_TEST_CWD%"\nexit /b 0\n')
            env=dict(os.environ,PATH=str(base)+os.pathsep+os.environ['PATH'],B47_TEST_ARGS=str(record),B47_TEST_CWD=str(base/'cwd.txt'))
            result=subprocess.run(['powershell','-NoProfile','-File',str(ROOT/'tools/Invoke-TeamWorkflow.ps1'),'-Action','codex','-Target',str(project),'-TeamTools',str(ROOT/'tools'),'-HomeDirectory',str(base/'home')],env=env,capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            command=record.read_text()
            self.assertIn('--sandbox workspace-write',command)
            self.assertIn('--ask-for-approval on-request',command)
            self.assertIn('--search',command)
            self.assertNotIn('dangerously',command)
            self.assertEqual(pathlib.Path((base/'cwd.txt').read_text().strip()),project)

    @unittest.skipUnless(os.name=='nt','Windows terminal fixture')
    def test_missing_project_version_script_fails(self):
        with tempfile.TemporaryDirectory() as td:
            base=pathlib.Path(td)
            result=subprocess.run(['powershell','-NoProfile','-File',str(ROOT/'tools/Invoke-TeamWorkflow.ps1'),'-Action','versions','-Target',str(base),'-TeamTools',str(ROOT/'tools'),'-HomeDirectory',str(base)],capture_output=True,text=True)
            self.assertNotEqual(result.returncode,0)
            self.assertFalse((base/'scripts').exists())
