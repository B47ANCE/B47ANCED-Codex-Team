import unittest,tempfile,pathlib,subprocess,os
root=pathlib.Path(__file__).resolve().parents[1]
class Connector(unittest.TestCase):
 @unittest.skipUnless(os.name=='nt','Windows PowerShell fixture')
 def test_custom_project_and_config_preserved(self):
  with tempfile.TemporaryDirectory() as td:
   base=pathlib.Path(td);home=base/'home';guide=home/'.codex/AGENTS.md';guide.parent.mkdir(parents=True);guide.write_text('shared')
   project=base/'mods'/'Example';project.mkdir(parents=True);p=project/'AGENTS.md';p.write_text('Custom rules\n<!-- PZ-CODEX-MANAGED-STARTUP -->stale<!-- /PZ-CODEX-MANAGED-STARTUP -->\nCustom suffix')
   config=project/'local.settings.json';config.write_text('local settings');env=dict(os.environ,USERPROFILE=str(home))
   args=['powershell','-NoProfile','-File',str(root/'tools/Connect-ModRepositories.ps1'),'-RepositoryRoot',str(project.parent)]
   for _ in range(2):
    result=subprocess.run(args,env=env,capture_output=True,text=True);self.assertEqual(result.returncode,0,result.stderr)
   text=p.read_text(encoding='utf-8-sig');self.assertTrue(text.startswith('Custom rules'));self.assertTrue(text.endswith('Custom suffix'));self.assertEqual(text.count('PZ-CODEX-MANAGED-STARTUP -->'),2);self.assertEqual(config.read_text(),'local settings')
