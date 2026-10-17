import importlib.util,json,pathlib,sys,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import chat_workspace as m
ID='11111111-2222-4333-8444-555555555555'
class ChatWorkspace(unittest.TestCase):
 def test_overview_tasks_inherited_without_starting_chats(self):
  with tempfile.TemporaryDirectory() as td:
   h,p,base,out=self.fixture(pathlib.Path(td));d=json.loads(base.read_text())
   task=dict(label='Overview: Keep features and connections current',type='process',command='powershell.exe',runOptions=dict(runOn='folderOpen'))
   d['tasks']=dict(tasks=[task]);base.write_text(json.dumps(d));before=p.read_bytes()
   m.generate(h,base,out);ws=json.loads(out.read_text())
   self.assertEqual(ws['tasks']['tasks'][-1],task);self.assertEqual(p.read_bytes(),before)
 def fixture(self,b,chat=True):
  h=b/'home/.codex';(h/'sessions').mkdir(parents=True)
  p=h/'sessions/chat.jsonl';raw=(json.dumps(dict(type='session_meta',payload=dict(id=ID,cwd='old path',source='vscode',timestamp='2026-10-12')))+'\n').encode()
  if chat:p.write_bytes(raw+b'invalid transcript not parsed\n')
  project=b/'project with spaces';project.mkdir();base=b/'base.code-workspace';base.write_text(json.dumps({'folders':[{'path':str(project),'name':'Project'}]}));out=b/'Saved-Chats.code-workspace'
  return h,p,base,out
 def test_metadata_only_and_invalid_sessions(self):
  with tempfile.TemporaryDirectory() as td:
   h,p,base,out=self.fixture(pathlib.Path(td));before=p.read_bytes();(h/'sessions/bad.jsonl').write_text('{"type":"session_meta","payload":{"id":"bad"}}')
   rows=m.scan(h);self.assertEqual(len(rows),1);self.assertEqual(rows[0]['id'],ID);self.assertEqual(before,p.read_bytes());self.assertNotIn('transcript',str(rows))
 def test_subagents_and_archives_excluded(self):
  with tempfile.TemporaryDirectory() as td:
   h,p,base,out=self.fixture(pathlib.Path(td));r=json.loads(p.read_text().splitlines()[0]);r['payload']['source']={'subagent':{}};p.write_text(json.dumps(r));(h/'archived_sessions').mkdir();(h/'archived_sessions/old.jsonl').write_text(json.dumps(r));self.assertEqual(m.scan(h),[])
 def test_empty_history_creates_refresh_and_browse(self):
  with tempfile.TemporaryDirectory() as td:
   h,p,base,out=self.fixture(pathlib.Path(td),False);result=m.generate(h,base,out);self.assertEqual(result['saved_chats'],0)
   ws=json.loads(out.read_text());self.assertEqual(len(ws['tasks']['tasks']),2);self.assertNotIn('chat',[x['id'] for x in ws['tasks']['inputs']])
 def test_repeat_refresh_and_customization_preserved(self):
  with tempfile.TemporaryDirectory() as td:
   h,p,base,out=self.fixture(pathlib.Path(td));before=p.read_bytes();m.generate(h,base,out);old=out.read_bytes();m.generate(h,base,out);self.assertEqual(old,out.read_bytes());self.assertEqual(before,p.read_bytes())
   ws=json.loads(old);self.assertEqual(len(ws['tasks']['tasks']),3);self.assertTrue(all('runOptions' not in t for t in ws['tasks']['tasks']));self.assertIn('-CodexHome',ws['tasks']['tasks'][0]['args'])
   out.write_text('custom');self.assertRaises(ValueError,m.generate,h,base,out);self.assertEqual(out.read_text(),'custom')
 def test_custom_launcher_preserved(self):
  with tempfile.TemporaryDirectory() as td:
   h,p,base,out=self.fixture(pathlib.Path(td));m.generate(h,base,out);launcher=h/'cli-chat-runtime/Resume-CodexChat.ps1';launcher.write_text('custom');self.assertRaises(ValueError,m.generate,h,base,out);self.assertEqual(launcher.read_text(),'custom')
 def test_setup_optout_and_inert_update(self):
  setup=(ROOT/'tools/Setup-CodexTeam.ps1').read_text();self.assertIn('not $SkipChatWorkspace',setup);self.assertIn('not $SkipCLIWorkspace -and',setup)
  updater=(ROOT/'tools/Update-CodexTeam.ps1').read_text();self.assertNotIn('Setup-ChatWorkspace',updater);self.assertNotIn('chat_workspace.py',updater)
