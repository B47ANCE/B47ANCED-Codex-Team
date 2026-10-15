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
        self.assertEqual(len(data["records"]), 93)
        self.assertEqual({r["status"] for r in data["records"]}, {"VERIFIED", "INFERRED", "UNKNOWN"})
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

class SharedUncertainty(unittest.TestCase):
    def test_hash_match_does_not_promote_inferred_or_unknown(self):
        for status in ("INFERRED", "UNKNOWN"):
            entry = copy.deepcopy(next(r for r in m.read(m.CURATED)["records"] if r["status"] == status))
            with tempfile.TemporaryDirectory() as td:
                root = pathlib.Path(td)
                entry["evidence"] = [copy.deepcopy(m.read(m.CURATED)["records"][0]["evidence"][0])]
                proof = entry["evidence"][0]
                path = root / proof["path"]; path.parent.mkdir(parents=True); path.write_bytes(b"source fixture")
                proof["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
                result = m.search({"schema": 1, "records": [entry]}, entry["symbol"], entry["steam_build"], game_root=root)[0]
                self.assertEqual(result["reuse"], "SOURCE_HASH_MATCH")
                self.assertEqual(result["record"]["status"], status)
                self.assertEqual(result["record"]["runtime_status"], "NOT_TESTED")

class DeepAuditEvidence(unittest.TestCase):
    def test_native_only_refinements_remain_inferred(self):
        data = m.read(m.CURATED)
        records = [r for r in data["records"] if r["signature_scope"].startswith("native_descriptor_only")]
        self.assertTrue(records)
        for entry in records:
            self.assertEqual(entry["status"], "INFERRED")
            self.assertEqual(entry["runtime_status"], "NOT_TESTED")
            self.assertFalse(any(p["kind"] == "vanilla_lua" for p in entry["evidence"]))
            self.assertTrue(any(p["kind"] == "native_inspection" for p in entry["evidence"]))

    def test_conflicting_receiver_is_not_verified_from_name_match(self):
        record = next(r for r in m.read(m.CURATED)["records"] if r["symbol"] == "getFluidAmount")
        self.assertEqual(record["status"], "UNKNOWN")
        self.assertEqual(record["runtime_status"], "NOT_TESTED")
        report = json.loads((m.CURATED.parent / "native-metadata-25485521.json").read_text())
        metadata = next(r for r in report["findings"] if r["symbol"] == "getFluidAmount")
        self.assertEqual(metadata["methods"], [])
        self.assertIsNone(metadata["declaring_class"])
        self.assertTrue(metadata["alternative_IsoObject_methods"])

    def test_observed_refinements_have_source_and_public_native_correspondence(self):
        report = json.loads((m.CURATED.parent / "native-metadata-25485521.json").read_text())
        metadata = {r["symbol"]: r for r in report["findings"]}
        for record in m.read(m.CURATED)["records"]:
            if not record["signature_scope"].startswith("observed_vanilla_call; contextual"):
                continue
            self.assertEqual(record["status"], "VERIFIED")
            self.assertEqual(record["runtime_status"], "NOT_TESTED")
            kinds = {p["kind"] for p in record["evidence"]}
            self.assertIn("vanilla_lua", kinds)
            self.assertIn("native_inspection", kinds)
            self.assertTrue(any(r["public"] for r in metadata[record["symbol"]]["methods"]))
