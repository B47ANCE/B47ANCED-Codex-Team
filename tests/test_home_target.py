import pathlib,tempfile,subprocess,os,unittest
root=pathlib.Path(__file__).resolve().parents[1]
class HomeTarget(unittest.TestCase):
 @unittest.skipUnless(os.name=='nt','Windows PowerShell validator')
 def test_verifier_does_not_inspect_real_profile(self):
  with tempfile.TemporaryDirectory() as td:
   env=dict(os.environ,PSModulePath=r'C:\Windows\System32\WindowsPowerShell\v1.0\Modules;C:\Program Files\WindowsPowerShell\Modules')
   p=subprocess.run(['powershell','-NoProfile','-File',str(root/'tools/Test-CodexTeamInstall.ps1'),'-PackageRoot',str(root),'-Installed','-HomeDirectory',td],env=env,capture_output=True,text=True)
   self.assertNotEqual(p.returncode,0);self.assertIn('FAIL: Installed global AGENTS.md',p.stdout)
