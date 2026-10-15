"""Build-bound API evidence catalog; never loads game code or runs a game."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import tempfile

CURATED = Path(__file__).resolve().parents[1] / "references/api-library.json"

def local_library():
    return Path.home() / ".codex/pz-api-audit/library.local.json"

def key(record):
    return tuple(record[x] for x in ("api_library", "receiver_type", "symbol", "signature", "side", "game_version", "steam_build"))

def validate(data):
    if not isinstance(data, dict) or set(data) != {"schema", "records"} or type(data["schema"]) is not int or data["schema"] != 1 or not isinstance(data["records"], list):
        raise ValueError("expected schema 1 catalog with records list")
    seen = set()
    fields = {"api_library", "receiver_type", "symbol", "signature", "signature_scope", "game_version", "steam_build", "side", "returns", "mutation", "status", "runtime_status", "verified_on", "evidence", "notes"}
    for record in data["records"]:
        if not isinstance(record, dict) or set(record) != fields:
            raise ValueError("invalid record fields")
        for field in fields - {"evidence"}:
            if not isinstance(record[field], str) or not record[field].strip():
                raise ValueError("missing text: " + field)
        if record["steam_build"] != "UNKNOWN" and not record["steam_build"].isdigit():
            raise ValueError("invalid Steam build")
        if record["side"] not in {"client", "server", "shared", "UNKNOWN"} or record["status"] not in {"VERIFIED", "INFERRED", "UNKNOWN"}:
            raise ValueError("invalid side/status")
        if record["runtime_status"] not in {"NOT_TESTED", "SP_VERIFIED", "DEDICATED_MP_VERIFIED"}:
            raise ValueError("invalid runtime status")
        datetime.date.fromisoformat(record["verified_on"])
        if not isinstance(record["evidence"], list) or not record["evidence"]:
            raise ValueError("evidence required")
        for proof in record["evidence"]:
            if not isinstance(proof, dict) or set(proof) != {"kind", "path", "sha256", "lines", "statement"}:
                raise ValueError("invalid evidence fields")
            path = proof["path"]
            if not isinstance(path, str) or not path or PurePosixPath(path).is_absolute() or any(x in path for x in ("..", ":", "\\")):
                raise ValueError("evidence path must be portable and relative")
            if proof["kind"] not in {"vanilla_lua", "official_docs", "native_inspection", "offline_test", "sp_runtime", "dedicated_runtime"}:
                raise ValueError("invalid evidence kind")
            if not re.fullmatch(r"[0-9a-f]{64}", proof["sha256"]):
                raise ValueError("evidence SHA-256 required")
            if not isinstance(proof["lines"], list) or len(proof["lines"]) != 2 or any(type(n) is not int or n < 1 for n in proof["lines"]) or proof["lines"][0] > proof["lines"][1] or not isinstance(proof["statement"], str) or not proof["statement"].strip():
                raise ValueError("invalid evidence range/statement")
        kinds = {p["kind"] for p in record["evidence"]}
        needed = {"SP_VERIFIED": "sp_runtime", "DEDICATED_MP_VERIFIED": "dedicated_runtime"}.get(record["runtime_status"])
        if needed and needed not in kinds:
            raise ValueError("runtime claim needs matching runtime evidence")
        if record["status"] == "VERIFIED" and kinds <= {"native_inspection"}:
            raise ValueError("native signature alone does not prove Lua exposure")
        identity = key(record)
        if identity in seen:
            raise ValueError("duplicate symbol/signature/build/side")
        seen.add(identity)
    # Do not sync developer paths, credentials or copied source bodies as catalog notes.
    text = json.dumps(data)
    if re.search(r"[A-Za-z]:[\\/]|/(?:Users|home|root)/|ghp_|github_pat_|-----BEGIN .*PRIVATE KEY", text):
        raise ValueError("private path or secret-like content rejected")
    return data

def read(path):
    return validate(json.loads(Path(path).read_text(encoding="utf-8")))

def search(data, symbol, steam_build, game_version=None, game_root=None):
    result = []
    for record in validate(data)["records"]:
        if symbol.casefold() not in record["symbol"].casefold():
            continue
        match = record["steam_build"] == steam_build and steam_build != "UNKNOWN"
        if game_version and record["game_version"] not in {game_version, "UNKNOWN"}:
            match = False
        state = "RECHECK_SOURCE" if match else "STALE_BUILD"
        if match and game_root:
            root = Path(game_root).resolve()
            local_proofs = [p for p in record["evidence"] if p["kind"] in {"vanilla_lua", "native_inspection"}]
            if local_proofs:
                matches = []
                for proof in local_proofs:
                    path = (root / proof["path"]).resolve()
                    matches.append(path.is_relative_to(root) and path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == proof["sha256"])
                state = "SOURCE_HASH_MATCH" if all(matches) else "STALE_SOURCE"
        result.append({"reuse": state, "game_version_known": record["game_version"] != "UNKNOWN", "record": record})
    return result

def unlinked(path):
    for p in [path, *path.parents]:
        if p.is_symlink() or getattr(p, "is_junction", lambda: False)():
            raise ValueError("linked destination refused")

def record_entry(path, entry, replace=False):
    validate({"schema": 1, "records": [entry]})
    path = Path(path).absolute()
    unlinked(path)
    for managed in (Path.home()/".agents/skills", Path.home()/".codex/b47anced-team"):
        if path.resolve().is_relative_to(managed.resolve()):
            raise ValueError("managed install is read-only; record a local draft or edit a reviewed source checkout")
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_name(path.name + ".lock")
    # Exclusive lock protects simultaneous audit writers. Existing lock is never removed.
    with lock.open("x"):
        pass
    try:
        data = read(path) if path.exists() else {"schema": 1, "records": []}
        found = next((i for i,r in enumerate(data["records"]) if key(r) == key(entry)), None)
        if found is not None:
            if data["records"][found] == entry:
                return "UNCHANGED"
            if not replace:
                raise ValueError("conflicting record; inspect and use --replace deliberately")
            data["records"][found] = entry
        else:
            data["records"].append(entry)
        validate(data)
        fd, temporary = tempfile.mkstemp(prefix=".api-library-", dir=path.parent)
        os.close(fd)
        try:
            Path(temporary).write_text(json.dumps(data, indent=2, sort_keys=True)+"\n", encoding="utf-8")
            os.replace(temporary, path)
        finally:
            if Path(temporary).exists():
                Path(temporary).unlink()
        return "RECORDED"
    finally:
        lock.unlink()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["validate", "search", "record"])
    parser.add_argument("--library", type=Path)
    parser.add_argument("--symbol")
    parser.add_argument("--steam-build")
    parser.add_argument("--game-version")
    parser.add_argument("--game-root", type=Path)
    parser.add_argument("--entry", type=Path)
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    try:
        path = args.library or (local_library() if args.action == "record" else CURATED)
        if args.action == "validate":
            result = {"status": "PASS", "records": len(read(path)["records"])}
        elif args.action == "record":
            if not args.entry: raise ValueError("--entry required")
            result = {"status": record_entry(path, json.loads(args.entry.read_text(encoding="utf-8")), args.replace)}
        else:
            if not args.symbol or not args.steam_build or not args.steam_build.isdigit():
                raise ValueError("search requires --symbol and exact numeric --steam-build")
            catalogs = [("curated" if not args.library else "explicit", read(path))]
            if not args.library and local_library().exists():
                catalogs.append(("local_draft", read(local_library())))
            result = [{"catalog": label, **item} for label,data in catalogs for item in search(data,args.symbol,args.steam_build,args.game_version,args.game_root)]
        print(json.dumps(result, indent=2)); return 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        print("ERROR: " + str(error)); return 1
if __name__ == "__main__":
    raise SystemExit(main())
