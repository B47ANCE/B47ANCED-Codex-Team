import os
import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

@unittest.skipUnless(os.name == 'nt', 'Windows CLI fixture')
class VSCodeSetup(unittest.TestCase):
    def run_fixture(self, mode, check=False):
        with tempfile.TemporaryDirectory() as td:
            base = pathlib.Path(td)
            cli = base / 'code.cmd'
            cli.write_text('@echo off\nif "%1"=="--version" (echo fixture-version & exit /b 0)\n'
                           'if "%1"=="--install-extension" (echo installed>"%VSCODE_TEST_STATE%" & exit /b 0)\n'
                           'if "%VSCODE_TEST_MODE%"=="failure" exit /b 7\n'
                           'if "%VSCODE_TEST_MODE%"=="present" (echo openai.chatgpt@1.0 & exit /b 0)\n'
                           'if exist "%VSCODE_TEST_STATE%" echo openai.chatgpt@1.0\nexit /b 0\n')
            # Plain --list-extensions must omit versions, as the real CLI does.
            text = cli.read_text().replace('echo openai.chatgpt@1.0',
                'if "%2"=="--show-versions" (echo openai.chatgpt@1.0) else (echo openai.chatgpt)')
            cli.write_text(text)
            settings = base / 'settings.json'
            settings.write_bytes(b'custom editor preferences')
            env = dict(os.environ, PATH=str(base)+os.pathsep+os.environ['PATH'],
                       VSCODE_TEST_MODE=mode, VSCODE_TEST_STATE=str(base/'installed'))
            args = ['powershell', '-NoProfile', '-File', str(ROOT/'tools/Setup-VSCode.ps1')]
            if check:
                args.append('-CheckOnly')
            result = subprocess.run(args, env=env, capture_output=True, text=True)
            self.assertEqual(settings.read_bytes(), b'custom editor preferences')
            return result, (base/'installed').exists()

    def test_existing_extension_reused(self):
        result, installed = self.run_fixture('present', True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(installed)

    def test_missing_extension_installed(self):
        result, installed = self.run_fixture('missing')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(installed)

    def test_check_only_does_not_install(self):
        result, installed = self.run_fixture('missing', True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(installed)

    def test_enumeration_failure_stops_setup(self):
        result, installed = self.run_fixture('failure')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(installed)

    def test_default_setup_and_updater_boundary(self):
        setup = (ROOT/'tools/Setup-CodexTeam.ps1').read_text()
        self.assertIn('if(-not $SkipVSCode)', setup)
        for name in ['Update-CodexTeam.ps1', 'rollback_team.py']:
            self.assertNotIn('Setup-VSCode.ps1', (ROOT/'tools'/name).read_text())
