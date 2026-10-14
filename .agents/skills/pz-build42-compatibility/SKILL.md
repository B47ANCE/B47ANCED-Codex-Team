---
name: pz-build42-compatibility
description: Compare Project Zomboid Build 42 updates against exact API, asset, networking and save evidence.
---

# Build 42 compatibility tracking
Use when the game updates, a mod targets a new Build 42 version, or APIs/assets change.
- Record exact installed game build, source file locations and hashes, and target mod version/commit.
- Compare relevant Lua APIs, script definitions, animation/model hooks, asset formats, networking, and save contracts against the previous evidence baseline.
- Do not infer compatibility from matching filenames or successful static scans. Test changes in SP and dedicated MP separately; mark unrun gates NOT TESTED.
- Create a compatibility matrix: feature, previous evidence, current evidence, risk, required migration, tests, and outcome.
- Preserve historical evidence unchanged and never automatically bump supported versions or rewrite releases.
- Lua-only remains mandatory; report engine API blockers and viable Lua-only alternatives.

## Shared workspace policy
Read `%USERPROFILE%/.codex/AGENTS.md` and the active project instructions. Preserve Lua-only runtime, server authority, sandbox configuration and canonical version policy. Dedicated gameplay G7 must PASS before release G8; do not adopt alternate gate numbering or relabel historical evidence. This skill does not authorize live deployment, publication, game/server launch or external access by itself. Existing user authorization and explicit changes to repository grouping or visibility take precedence.
