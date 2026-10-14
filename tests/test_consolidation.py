import pathlib,tempfile,shutil,unittest,importlib.util,unittest.mock as mock
root=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('team',root/'tools/team_config.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Consolidation(unittest.TestCase):
 def test_custom_global_survives_repeated_updates(self):
  with tempfile.TemporaryDirectory() as td:
   h=pathlib.Path(td)/'home';b=pathlib.Path(td)/'backups';p=h/'.codex/AGENTS.md';p.parent.mkdir(parents=True);p.write_text('Unrelated custom workflow')
   m.install(root,h,b,True,True);first=p.read_text(encoding='utf-8');m.install(root,h,b)
   self.assertEqual(first,p.read_text(encoding='utf-8'));self.assertEqual(first.count('BEGIN B47ANCED TEAM'),1);self.assertTrue(first.startswith('Unrelated custom workflow'))
 def test_duplicate_archive_and_unrelated_preservation(self):
  with tempfile.TemporaryDirectory() as td:
   h=pathlib.Path(td)/'home';b=pathlib.Path(td)/'backups';ws=pathlib.Path(td)/'Workspace';m.install(root,h,b,True)
   shutil.copytree(h/'.agents/skills',ws/'.agents/skills');custom=ws/'.agents/skills/custom/SKILL.md';custom.parent.mkdir();custom.write_text('custom');guide=ws/'AGENTS.md';guide.write_text('Custom workspace instructions')
   state=m.install(root,h,b,True,True,ws)
   self.assertTrue(guide.read_text(encoding='utf-8').startswith('Custom workspace instructions'));self.assertEqual(custom.read_text(),'custom')
   self.assertEqual(len(list((pathlib.Path(state['backup'])/'consolidated-skills').iterdir())),23)
   self.assertEqual(len(list((ws/'.agents/skills').iterdir())),1);m.check_drift(h)
   first=guide.read_text(encoding='utf-8');m.install(root,h,b,False,False,ws)
   self.assertEqual(first,guide.read_text(encoding='utf-8'))
 def test_custom_duplicate_blocks_without_loss(self):
  with tempfile.TemporaryDirectory() as td:
   h=pathlib.Path(td)/'home';b=pathlib.Path(td)/'backups';ws=pathlib.Path(td)/'Workspace';m.install(root,h,b,True);shutil.copytree(h/'.agents/skills',ws/'.agents/skills')
   target=ws/'.agents/skills/pz-api-audit/SKILL.md';target.write_text('custom implementation')
   with self.assertRaises(ValueError):m.install(root,h,b,False,False,ws)
   self.assertEqual(target.read_text(),'custom implementation');self.assertEqual(len(list((ws/'.agents/skills').iterdir())),23)
