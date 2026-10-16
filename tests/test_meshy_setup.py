import importlib.util
import pathlib
import tempfile
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('meshy_setup',ROOT/'tools/meshy_setup.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class MeshyConfig(unittest.TestCase):
    def test_preserves_bytes_and_unrelated_integrations(self):
        with tempfile.TemporaryDirectory() as td:
            home=pathlib.Path(td)
            old=b'# custom comments\r\nmodel_reasoning_effort="high"\r\n[mcp_servers.other]\r\ncommand="keep-me"\r\n'
            cfg=home/'config.toml'
            cfg.write_bytes(old)
            result=module.configure(home,'C:/Program Files/nodejs/npx.cmd','cmd.exe')
            self.assertTrue(cfg.read_bytes().startswith(old))
            self.assertTrue(result['backup_created'])
            backups=list((home/'integration-backups').rglob('config.toml'))
            self.assertEqual(len(backups),1)
            self.assertEqual(backups[0].read_bytes(),old)
            self.assertEqual(module.tomllib.loads(cfg.read_text())['mcp_servers']['other']['command'],'keep-me')

    def test_repeated_setup_is_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            module.configure(td,'npx.cmd','cmd.exe')
            path=pathlib.Path(td)/'config.toml'
            old=path.read_bytes()
            self.assertEqual(module.configure(td,'npx.cmd','cmd.exe')['status'],'CURRENT')
            self.assertEqual(path.read_bytes(),old)
            self.assertFalse((path.parent/'integration-backups').exists())

    def test_custom_meshy_is_preserved(self):
        with tempfile.TemporaryDirectory() as td:
            path=pathlib.Path(td)/'config.toml'
            old=b'[mcp_servers."meshy"]\ncommand="custom"\n'
            path.write_bytes(old)
            with self.assertRaises(ValueError):
                module.configure(td,'npx.cmd','cmd.exe')
            self.assertEqual(path.read_bytes(),old)

    def test_invalid_toml_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as td:
            path=pathlib.Path(td)/'config.toml'
            path.write_bytes(b'invalid [')
            with self.assertRaises(ValueError):
                module.configure(td,'npx.cmd','cmd.exe')
            self.assertEqual(path.read_bytes(),b'invalid [')

    def test_check_only_does_not_create_files(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                module.configure(td,'npx.cmd','cmd.exe',check=True)
            self.assertEqual(list(pathlib.Path(td).iterdir()),[])

    def test_no_key_and_all_tools_require_approval(self):
        with tempfile.TemporaryDirectory() as td:
            module.configure(td,'npx.cmd','cmd.exe')
            cfg=module.tomllib.loads((pathlib.Path(td)/'config.toml').read_text())['mcp_servers']['meshy']
            self.assertEqual(cfg['env_vars'],['MESHY_API_KEY'])
            self.assertNotIn('enabled_tools',cfg)
            self.assertNotIn('disabled_tools',cfg)
            self.assertEqual(cfg['default_tools_approval_mode'],'prompt')
            self.assertNotIn('env',cfg)

    def test_automatic_update_does_not_provision_integrations(self):
        for name in ['Update-CodexTeam.ps1','rollback_team.py']:
            text=(ROOT/'tools'/name).read_text()
            self.assertNotIn('Setup-Meshy.ps1',text)
            self.assertNotIn('Set-MeshyApiKey.ps1',text)
        setup=(ROOT/'tools/Setup-CodexTeam.ps1').read_text()
        self.assertIn('if(-not $SkipMeshy)',setup)

    def test_custom_launcher_is_preserved(self):
        with tempfile.TemporaryDirectory() as td:
            module.configure(td,'npx.cmd','powershell.exe')
            home=pathlib.Path(td)
            config=(home/'config.toml').read_bytes()
            launcher=home/'meshy-runtime/Start-Meshy.ps1'
            launcher.write_bytes(b'custom launcher')
            with self.assertRaises(ValueError):
                module.configure(td,'npx.cmd','powershell.exe')
            self.assertEqual(launcher.read_bytes(),b'custom launcher')
            self.assertEqual((home/'config.toml').read_bytes(),config)

    def test_missing_launcher_check_fails_and_setup_repairs(self):
        with tempfile.TemporaryDirectory() as td:
            module.configure(td,'npx.cmd','powershell.exe')
            home=pathlib.Path(td)
            config=(home/'config.toml').read_bytes()
            launcher=home/'meshy-runtime/Start-Meshy.ps1'
            launcher.unlink()
            with self.assertRaises(ValueError):
                module.configure(td,'npx.cmd','powershell.exe',check=True)
            module.configure(td,'npx.cmd','powershell.exe')
            self.assertEqual(launcher.read_bytes(),(ROOT/'tools/Start-Meshy.ps1').read_bytes())
            self.assertEqual((home/'config.toml').read_bytes(),config)
