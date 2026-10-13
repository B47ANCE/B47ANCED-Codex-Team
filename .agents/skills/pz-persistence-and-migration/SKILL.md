---
name: pz-persistence-and-migration
description: Save ownership, persistence and migrations for Project Zomboid Build 42 Lua-only mod development.
---

# Save ownership, persistence and migrations

Use when the task concerns this domain. Follow the shared guide at `C:/Users/willi/Desktop/Work/Project Zomboid/Codex/AGENTS.md` and the active project AGENTS.md. Gameplay requires dedicated G7 PASS before release G8; skill instructions do not authorize game/server launch, deployment or publication.

## Procedure

1. Discover the authoritative repository files, local tools and matching installed Build 42 evidence; do not assume paths or API capabilities.
2. Define target artifacts, expected behavior, ownership and measurable acceptance criteria.
3. Document where state lives, who writes it, serialization schema, version and migration behavior. Server owns shared state; handle disconnect/reconnect, restart, stale requests, duplicate events, corrupted/missing data and backward compatibility. Never silently reset user saves. Add offline tests and explicitly require live dedicated restart/reconnect tests.
4. Run available static/structural checks, retain evidence, and mark unavailable runtime validation NOT TESTED.
5. Report changed files, validation results, licensing/provenance, outstanding blockers, and deployment/publication status.

## Save migration validation (v12)
- Build disposable fixtures from prior version saves where legally and technically available; record schema and exact versions.
- Test forward migration, idempotent reload, missing/corrupt fields, older clients where relevant, reconnect and dedicated-server restart.
- Preserve save backups and document whether downgrade/rollback is supported; do not mutate actual player saves during automated tests.
- Static simulation is not native save compatibility proof.
