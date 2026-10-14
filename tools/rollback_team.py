"""Explicit, transactional rollback of an installed team update (never credentials)."""
import argparse, hashlib, json, os, pathlib, shutil, tempfile, uuid

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def unlinked(p):
    for q in [p, *p.parents]:
        if q.is_symlink() or getattr(q, "is_junction", lambda: False)():
            raise ValueError("linked path rejected: " + str(q))
def destination(key, home, workspace):
    rel = pathlib.PurePosixPath(key)
    if rel.is_absolute() or ".." in rel.parts or "\\" in key or ":" in key:
        raise ValueError("invalid managed key")
    if key == "global/AGENTS.md": return home / ".codex/AGENTS.md"
    if key.startswith("global/.agents/skills/pz-"): return home / key[7:]
    if key.startswith("hub/"): return home / ".codex/b47anced-team" / key[4:]
    if workspace and key == "workspace/AGENTS.md": return workspace / "AGENTS.md"
    if workspace and key.startswith("workspace/tools/"): return workspace / key[10:]
    if workspace and key.startswith("workspace/templates/"): return workspace / "templates/current" / key[20:]
    raise ValueError("unsupported managed key: " + key)

def rollback(home, check_only=False):
    home = pathlib.Path(home).absolute()
    st = home / ".codex/b47anced-team-state.json"
    lock = home / ".codex/b47anced-team-tools/update.lock"
    unlinked(st); unlinked(lock)
    lock.mkdir()  # shared with automatic updater; refuse concurrency
    try:
        current_bytes = st.read_bytes(); current = json.loads(current_bytes)
        workspace = pathlib.Path(current["workspace"]).absolute() if current.get("workspace") else None
        backup = pathlib.Path(current["backup"]).absolute()
        unlinked(backup)
        unlinked(backup / "previous-state.json")
        previous_bytes = (backup / "previous-state.json").read_bytes()
        previous = json.loads(previous_bytes)
        if previous.get("workspace") != current.get("workspace"):
            raise ValueError("workspace changed; manual review required")
        targets = {}
        for key, record in current["managed"].items():
            dst = destination(key, home, workspace); unlinked(dst)
            if pathlib.Path(record["path"]).absolute() != dst or not dst.is_file() or sha(dst) != record["sha256"]:
                raise ValueError("managed path/drift: " + key)
            targets[key] = dst
        for key, record in previous["managed"].items():
            if key not in targets or pathlib.Path(record["path"]).absolute() != targets[key]:
                raise ValueError("prior ownership differs: " + key)
            src = backup / key; unlinked(src)
            if not src.is_file() or sha(src) != record["sha256"]:
                raise ValueError("backup integrity: " + key)
        result = {"status": "validated", "version": previous["version"], "commit": previous.get("commit"), "backup": str(backup)}
        if check_only: return result
        recovery = home / ".codex/b47anced-backups" / ("manual-" + uuid.uuid4().hex)
        unlinked(recovery); recovery.mkdir(parents=True)
        for key, dst in targets.items():
            saved = recovery / key; saved.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(dst, saved)
        (recovery / "previous-state.json").write_bytes(current_bytes)
        changed = []
        try:
            for key, dst in targets.items():
                changed.append(key)
                if key in previous["managed"]:
                    atomic_copy(backup / key, dst)
                else:
                    # Archive only new managed files; never recursively delete directories.
                    dst.unlink()
            atomic_copy(backup / "previous-state.json", st)
        except BaseException:
            for key in reversed(changed): atomic_copy(recovery / key, targets[key])
            st.write_bytes(current_bytes)
            raise
        result.update(status="restored", recovery=str(recovery))
        return result
    finally:
        lock.rmdir()

def atomic_copy(src, dst):
    fd, name = tempfile.mkstemp(prefix=".b47-rollback-", dir=dst.parent); os.close(fd)
    try:
        shutil.copy2(src, name); os.replace(name, dst)
    finally:
        if pathlib.Path(name).exists(): pathlib.Path(name).unlink()
if __name__ == "__main__":
    p = argparse.ArgumentParser(); p.add_argument("--home", required=True); p.add_argument("--check-only", action="store_true")
    a = p.parse_args()
    print(json.dumps(rollback(a.home, a.check_only)))
