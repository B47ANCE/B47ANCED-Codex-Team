import pathlib,tempfile,unittest,importlib.util,unittest.mock as mock
root=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('team',root/'tools/team_config.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Safeguards(unittest.TestCase):
 def test_unrelated_and_config(self):
  with tempfile.TemporaryDirectory() as td:
   h=pathlib.Path(td)/'home';other=h/'.agents/skills/unrelated/SKILL.md';other.parent.mkdir(parents=True);other.write_text('custom')
   config=h/'.codex/config.toml';config.parent.mkdir(parents=True);config.write_text('custom=true')
   m.install(root,h,pathlib.Path(td)/'backups',True)
   self.assertEqual(other.read_text(),'custom');self.assertEqual(config.read_text(),'custom=true');self.assertTrue((h/'.codex/b47anced-team/tools/team_config.py').is_file())
 def test_rollback_and_state(self):
  with tempfile.TemporaryDirectory() as td:
   h=pathlib.Path(td)/'home';b=pathlib.Path(td)/'backups';m.install(root,h,b,True)
   old=m.state_path(h).read_bytes();guide=(h/'.codex/AGENTS.md').read_bytes();real=m.shutil.copy2;count=[0]
   def fail_once(*args,**kwargs):
    count[0]+=1
    if count[0]==4:raise OSError('injected copy failure')
    return real(*args,**kwargs)
   with mock.patch.object(m.shutil,'copy2',side_effect=fail_once):
    with self.assertRaises(OSError):m.install(root,h,b)
   self.assertEqual(old,m.state_path(h).read_bytes());self.assertEqual(guide,(h/'.codex/AGENTS.md').read_bytes());m.check_drift(h)
 def test_manifest_required(self):
  with tempfile.TemporaryDirectory() as td:
   with self.assertRaises(ValueError):m.validate(pathlib.Path(td))
