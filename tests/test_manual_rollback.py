import importlib.util, json, pathlib, tempfile, unittest, os, subprocess, sys
from unittest import mock
root=pathlib.Path(__file__).resolve().parents[1]
def load(name):
 s=importlib.util.spec_from_file_location(name,root/"tools"/(name+".py"));m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
i=load("team_config");r=load("rollback_team")
class RollbackTests(unittest.TestCase):
 def fixture(self, td):
  h=pathlib.Path(td)/"home";w=pathlib.Path(td)/"workspace"
  i.install(root,h,h/".codex/b47anced-backups",True,workspace=w,commit="old")
  (h/".codex/b47anced-team-tools").mkdir()
  (h/".codex/config.toml").write_text("private settings")
  st=i.state_path(h);state=json.loads(st.read_text());v=h/".codex/b47anced-team/VERSION";v.write_text("13.1.1\n");state["version"]="13.1.1";state["managed"]["hub/VERSION"]["sha256"]=i.digest(v);st.write_text(json.dumps(state))
  old=i.check_drift(h)
  i.install(root,h,h/".codex/b47anced-backups",workspace=w,commit="new")
  return h,old
 def test_preview_restore_preserves_local_and_recovery(self):
  with tempfile.TemporaryDirectory() as td:
   h,old=self.fixture(td);before=i.state_path(h).read_bytes()
   self.assertEqual(r.rollback(h,True)["status"],"validated")
   self.assertEqual(i.state_path(h).read_bytes(),before)
   result=r.rollback(h);self.assertEqual(i.check_drift(h),old)
   self.assertEqual((h/".codex/config.toml").read_text(),"private settings")
   self.assertEqual((pathlib.Path(result["recovery"])/"previous-state.json").read_bytes(),before)
 def test_new_managed_file_archived(self):
  with tempfile.TemporaryDirectory() as td:
   h,old=self.fixture(td);st=i.state_path(h);state=json.loads(st.read_text());p=h/".codex/b47anced-team/docs/new.md";p.write_text("new owned file")
   state["managed"]["hub/docs/new.md"]={"path":str(p),"sha256":i.digest(p)};st.write_text(json.dumps(state))
   result=r.rollback(h);self.assertFalse(p.exists());self.assertEqual((pathlib.Path(result["recovery"])/"hub/docs/new.md").read_text(),"new owned file")
 def test_corrupt_backup_refused_without_writes(self):
  with tempfile.TemporaryDirectory() as td:
   h,old=self.fixture(td);state=i.check_drift(h);before=i.state_path(h).read_bytes()
   (pathlib.Path(state["backup"])/"global/AGENTS.md").write_text("corrupt")
   with self.assertRaises(ValueError):r.rollback(h)
   self.assertEqual(i.state_path(h).read_bytes(),before);i.check_drift(h)
 def test_drift_and_concurrent_update_refused(self):
  with tempfile.TemporaryDirectory() as td:
   h,old=self.fixture(td);p=h/".codex/AGENTS.md";p.write_text("local edit")
   with self.assertRaises(ValueError):r.rollback(h)
   self.assertEqual(p.read_text(),"local edit")
   lock=h/".codex/b47anced-team-tools/update.lock";lock.mkdir()
   with self.assertRaises(FileExistsError):r.rollback(h)
 def test_injected_failure_restores_current(self):
  with tempfile.TemporaryDirectory() as td:
   h,old=self.fixture(td);before=i.state_path(h).read_bytes();original=r.atomic_copy;calls=[]
   def fail(src,dst):
    calls.append(dst)
    if len(calls)==3:raise OSError("injected")
    return original(src,dst)
   with mock.patch.object(r,"atomic_copy",side_effect=fail):
    with self.assertRaises(OSError):r.rollback(h)
   self.assertEqual(i.state_path(h).read_bytes(),before);i.check_drift(h)
 def test_unowned_path_and_traversal_refused(self):
  with tempfile.TemporaryDirectory() as td:
   h,old=self.fixture(td);st=i.state_path(h);state=json.loads(st.read_text())
   state["managed"]["global/AGENTS.md"]["path"]=str(h/".codex/config.toml");st.write_text(json.dumps(state))
   with self.assertRaises(ValueError):r.rollback(h)
   with self.assertRaises(ValueError):r.destination("hub/../../config.toml",h,None)

 @unittest.skipUnless(os.name=="nt", "Windows PowerShell wrapper")
 def test_powershell_preview_and_restore(self):
  with tempfile.TemporaryDirectory() as td:
   h,old=self.fixture(td)
   (h/".codex/b47anced-team-tools/source.json").write_text(json.dumps({"python_exe":sys.executable}))
   for suffix in [["-CheckOnly"],[]]:
    result=subprocess.run(["powershell.exe","-NoProfile","-File",str(root/"tools/Restore-CodexTeam.ps1"),"-HomeDirectory",str(h),*suffix],capture_output=True,text=True)
    self.assertEqual(result.returncode,0,result.stdout+result.stderr)
   self.assertEqual(i.check_drift(h),old)
