"""Exercise the read-only PowerShell verifier with disposable developer homes."""
import hashlib
import json
import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SHELL = shutil.which('pwsh') or shutil.which('powershell')

@unittest.skipUnless(SHELL, 'PowerShell required for verifier integration fixtures')
class RepositoryVerification(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = pathlib.Path(self.temp.name)
        self.home = self.base / 'home [custom]'
        self.mods = self.base / 'mods'
        self.mods.mkdir()
        (self.home / '.codex').mkdir(parents=True)
        (self.home / '.codex/AGENTS.md').write_text('shared instructions')
        managed = {}
        for folder in (ROOT / '.agents/skills').iterdir():
            if not folder.is_dir():
                continue
            rel = '.agents/skills/' + folder.name + '/SKILL.md'
            p = self.home / rel
            p.parent.mkdir(parents=True)
            p.write_text('fixture skill')
            managed['global/' + rel] = {}
        (self.home / '.codex/b47anced-team-state.json').write_text(json.dumps({'managed': managed}))

    def project(self, name, guide):
        p = self.mods / name
        p.mkdir()
        if guide is not None:
            (p / 'AGENTS.md').write_text(guide)
        (p / 'local.settings.json').write_text('private fixture settings')
        return p

    def verify(self, success=True):
        before = {p.relative_to(self.base).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in self.base.rglob('*') if p.is_file()}
        result = subprocess.run([SHELL, '-NoProfile', '-NonInteractive', '-File',
            str(ROOT / 'tools/Test-ModRepositories.ps1'), '-HomeDirectory', str(self.home),
            '-RepositoryRoot', str(self.mods)], capture_output=True, text=True)
        after = {p.relative_to(self.base).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in self.base.rglob('*') if p.is_file()}
        self.assertEqual(before, after, 'Verifier changed project or developer files')
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report['Status'], 'PASS')
            self.assertEqual(report['GlobalSkills'], 23)
            return report
        self.assertNotEqual(result.returncode, 0)
        return result.stderr

    def test_worktree_container_ignored_and_custom_rooms_guide_preserved(self):
        self.project('.worktrees', None)
        self.project('Rooms', 'Read `%USERPROFILE%/.codex/AGENTS.md`.\nCustom server-owned room rules.')
        self.assertEqual(self.verify()['Projects'], 1)

    def test_portable_and_absolute_custom_references(self):
        variants = ['%USERPROFILE%\\.codex\\AGENTS.md', '$env:USERPROFILE/.codex/AGENTS.md',
                    '~/.codex/AGENTS.md', 'USERPROFILE/.codex/AGENTS.md', 'USERPROFILE\\.codex\\AGENTS.md', str(self.home / '.codex/AGENTS.md'),
                    str(self.home / '.codex/AGENTS.md').replace('\\', '/').upper()]
        for index, reference in enumerate(variants):
            self.project('Custom' + str(index), 'Read `' + reference + '` before work.')
        self.project('Sentence', 'Read %USERPROFILE%/.codex/AGENTS.md.')
        self.assertEqual(self.verify()['Projects'], len(variants) + 1)

    def test_existing_managed_startup_accepted(self):
        self.project('Managed', '<!-- PZ-CODEX-MANAGED-STARTUP -->\nExisting instructions')
        self.assertEqual(self.verify()['Projects'], 1)

    def test_real_project_without_guide_still_fails(self):
        self.project('Missing', None)
        self.assertIn('Missing project guide', self.verify(False))

    def test_unrelated_or_lookalike_references_fail(self):
        p = self.project('Invalid', '')
        for text in ['Custom project rules only', 'Read .codex/config.toml',
                     'Read NOTUSERPROFILE/.codex/AGENTS.md', 'Read /wrong/USERPROFILE/.codex/AGENTS.md',
                     'Read USERPROFILE/.codex/AGENTS.md.bak', 'Read USERPROFILE/.codex/AGENTS.md/subfolder',
                     'Read %USERPROFILE%/.codex/AGENTS.md.bak', 'Read /other/.codex/AGENTS.md',
                     'Read /wrong' + str(self.home / '.codex/AGENTS.md'),
                     'Read %USERPROFILE%/.codex/AGENTS.md/subfolder']:
            with self.subTest(text=text):
                (p / 'AGENTS.md').write_text(text)
                self.assertIn('Missing startup reference', self.verify(False))

    def test_missing_installed_skill_still_fails(self):
        self.project('Rooms', 'Read ~/.codex/AGENTS.md')
        next((self.home / '.agents/skills').glob('*/SKILL.md')).unlink()
        self.assertIn('Missing global skill', self.verify(False))
