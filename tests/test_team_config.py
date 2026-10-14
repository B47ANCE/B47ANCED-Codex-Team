import importlib.util, pathlib, tempfile, shutil, unittest, json
root=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('team_config',root/'tools/team_config.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class TeamConfigTests(unittest.TestCase):
 def test_package_valid(self):
  self.assertEqual(m.validate(root)['skills'],23)
 def test_install_and_modified_file_refusal(self):
  with tempfile.TemporaryDirectory() as td:
   home=pathlib.Path(td)/'home';m.install(root,home,pathlib.Path(td)/'backups',True)
   m.install(root,home,pathlib.Path(td)/'backups2',False)
   f=home/'.codex/AGENTS.md';f.write_text(f.read_text(encoding='utf-8')+'\nlocal change\n')
   with self.assertRaises(ValueError):m.install(root,home,pathlib.Path(td)/'backups3',False)
 def test_migration_backs_up_old_agents(self):
  with tempfile.TemporaryDirectory() as td:
   home=pathlib.Path(td)/"home";f=home/".codex/AGENTS.md";f.parent.mkdir(parents=True);f.write_text("old instructions")
   m.install(root,home,pathlib.Path(td)/"backups",True,True)
   self.assertTrue(f.read_text(encoding='utf-8').startswith("old instructions"));self.assertIn((root/"AGENTS.md").read_text(encoding="utf-8").strip(),f.read_text(encoding="utf-8"))
 def test_config_preserved_on_update(self):
  with tempfile.TemporaryDirectory() as td:
   home=pathlib.Path(td)/'home';m.install(root,home,pathlib.Path(td)/'backups',True)
   f=home/'.codex/config.toml';f.write_text('custom=true\n')
   m.install(root,home,pathlib.Path(td)/'backups2',False)
   self.assertEqual(f.read_text(encoding='utf-8'),'custom=true\n')
if __name__=='__main__':unittest.main()
