---
name: pz-mod-compatibility
description: Mod interoperability and conflict diagnosis for Project Zomboid Build 42 Lua-only mod development.
---

# Mod interoperability and conflict diagnosis

Use when the task concerns this domain. Follow the shared guide at `%USERPROFILE%/.codex/AGENTS.md` and the active project AGENTS.md. Gameplay requires dedicated G7 PASS before release G8; skill instructions do not authorize game/server launch, deployment or publication.

## Procedure

1. Discover the authoritative repository files, local tools and matching installed Build 42 evidence; do not assume paths or API capabilities.
2. Define target artifacts, expected behavior, ownership and measurable acceptance criteria.
3. Audit target mods and installed vanilla APIs, dependency declarations, load order, global overrides, namespaces and missing optional dependencies. Apply pz-clean-room-research to external authors. Do not edit third-party mods without authorization. Use opt-in adapters and nil-safe feature detection. Test standalone, with dependency, without dependency, and dedicated server; report untested combinations.
4. Run available static/structural checks, retain evidence, and mark unavailable runtime validation NOT TESTED.
5. Report changed files, validation results, licensing/provenance, outstanding blockers, and deployment/publication status.
