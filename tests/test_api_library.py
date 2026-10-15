import copy
import importlib.util
import json
import hashlib
import pathlib
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/pz-api-audit/scripts/api_library.py"
spec = importlib.util.spec_from_file_location("api_library", SCRIPT)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class ApiLibrary(unittest.TestCase):
    def entry(self):
        return copy.deepcopy(m.read(m.CURATED)["records"][0])

    def test_curated_catalog_valid(self):
        data = m.read(m.CURATED)
        self.assertEqual(len(data["records"]), 3)
        self.assertTrue(all(r["runtime_status"] == "NOT_TESTED" for r in data["records"]))

    def test_build_and_hash_rechecks_never_promote_runtime(self):
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td); entry = self.entry()
            p = root / entry["evidence"][0]["path"]; p.parent.mkdir(parents=True); p.write_bytes(b"fixture source")
            entry["evidence"][0]["sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
            data = {"schema": 1, "records": [entry]}
            result = m.search(data, entry["symbol"], entry["steam_build"], game_root=root)[0]
            self.assertEqual(result["reuse"], "SOURCE_HASH_MATCH")
            self.assertEqual(result["record"]["runtime_status"], "NOT_TESTED")
            self.assertEqual(m.search(data, entry["symbol"], "999", game_root=root)[0]["reuse"], "STALE_BUILD")
            p.write_bytes(b"changed")
            self.assertEqual(m.search(data, entry["symbol"], entry["steam_build"], game_root=root)[0]["reuse"], "STALE_SOURCE")

    def test_version_mismatch_and_missing_source_require_reaudit(self):
        entry = self.entry(); entry["game_version"] = "42.21"
        data = {"schema": 1, "records": [entry]}
        self.assertEqual(m.search(data, entry["symbol"], entry["steam_build"], "42.22")[0]["reuse"], "STALE_BUILD")
        with tempfile.TemporaryDirectory() as td:
            self.assertEqual(m.search(data, entry["symbol"], entry["steam_build"], game_root=td)[0]["reuse"], "STALE_SOURCE")

    def test_record_conflict_history_and_idempotency(self):
        with tempfile.TemporaryDirectory() as td:
            p = pathlib.Path(td)/"draft.json"; e = self.entry()
            self.assertEqual(m.record_entry(p, e), "RECORDED")
            original = p.read_bytes()
            self.assertEqual(m.record_entry(p, e), "UNCHANGED")
            changed = copy.deepcopy(e); changed["notes"] = "New claim requiring deliberate review."
            with self.assertRaises(ValueError): m.record_entry(p, changed)
            self.assertEqual(p.read_bytes(), original)
            m.record_entry(p, changed, replace=True)
            later = copy.deepcopy(e); later["steam_build"] = "999"
            m.record_entry(p, later)
            self.assertEqual(len(m.read(p)["records"]), 2)

    def test_installed_managed_store_is_not_writable(self):
        with tempfile.TemporaryDirectory() as td, mock.patch.object(m.Path, "home", return_value=pathlib.Path(td)):
            for rel in [".agents/skills/pz-api-audit/references/api-library.json", ".codex/b47anced-team/library.json"]:
                p = pathlib.Path(td)/rel
                with self.assertRaises(ValueError): m.record_entry(p, self.entry())
                self.assertFalse(p.exists())

    def test_invalid_and_private_evidence_refused(self):
        for path in ["../escape", "/absolute", "C:/private/game.lua", "folder\\escape.lua"]:
            e = self.entry(); e["evidence"][0]["path"] = path
            with self.subTest(path=path), self.assertRaises(ValueError): m.validate({"schema": 1, "records": [e]})
        e = self.entry(); e["notes"] = "Private path C:/Users/example/private"
        with self.assertRaises(ValueError): m.validate({"schema": 1, "records": [e]})
        e = self.entry(); e["evidence"][0]["sha256"] = "missing"
        with self.assertRaises(ValueError): m.validate({"schema": 1, "records": [e]})

    def test_native_only_and_offline_runtime_claim_refused(self):
        e = self.entry(); e["evidence"][0]["kind"] = "native_inspection"
        with self.assertRaises(ValueError): m.validate({"schema": 1, "records": [e]})
        for status in ["SP_VERIFIED", "DEDICATED_MP_VERIFIED"]:
            e = self.entry(); e["runtime_status"] = status
            with self.assertRaises(ValueError): m.validate({"schema": 1, "records": [e]})
        e["evidence"][0]["kind"] = "sp_runtime"
        with self.assertRaises(ValueError): m.validate({"schema": 1, "records": [e]})

    def test_atomic_failure_preserves_old_file_and_lock_refusal(self):
        with tempfile.TemporaryDirectory() as td:
            p = pathlib.Path(td)/"draft.json"; e = self.entry(); m.record_entry(p, e); original=p.read_bytes()
            e["steam_build"] = "999"
            with mock.patch.object(m.os, "replace", side_effect=OSError("injected")):
                with self.assertRaises(OSError): m.record_entry(p, e)
            self.assertEqual(p.read_bytes(), original)
            self.assertFalse(list(p.parent.glob(".api-library-*")))
            lock = p.with_name(p.name+".lock"); lock.write_text("another writer")
            with self.assertRaises(FileExistsError): m.record_entry(p, e)
            self.assertEqual(lock.read_text(), "another writer")

    def test_duplicate_identity_rejected(self):
        e = self.entry()
        with self.assertRaises(ValueError): m.validate({"schema": 1, "records": [e,e]})

    def test_local_draft_survives_managed_install_updates(self):
        installer_spec = importlib.util.spec_from_file_location("installer", ROOT/"tools/team_config.py")
        installer = importlib.util.module_from_spec(installer_spec); installer_spec.loader.exec_module(installer)
        with tempfile.TemporaryDirectory() as td:
            home=pathlib.Path(td)/"home"
            installer.install(ROOT, home, home/".codex/backups", True)
            draft=home/".codex/pz-api-audit/library.local.json"
            m.record_entry(draft, self.entry()); before=draft.read_bytes()
            installer.install(ROOT, home, home/".codex/backups")
            self.assertEqual(draft.read_bytes(), before)
            self.assertTrue((home/".agents/skills/pz-api-audit/references/api-library.json").is_file())
