---
name: pz-ui-ux-development
description: Vanilla-aligned interfaces and context menus for Project Zomboid Build 42 Lua-only mod development.
---

# Vanilla-aligned interfaces and context menus

Use when the task concerns this domain. Follow the shared guide at `%USERPROFILE%/.codex/AGENTS.md` and the active project AGENTS.md. Gameplay requires dedicated G7 PASS before release G8; skill instructions do not authorize game/server launch, deployment or publication.

## Procedure

1. Discover the authoritative repository files, local tools and matching installed Build 42 evidence; do not assume paths or API capabilities.
2. Define target artifacts, expected behavior, ownership and measurable acceptance criteria.
3. Inspect vanilla UI and input patterns. Show only meaningful state-applicable context actions, never opposite-state redundant commands. Support keyboard/mouse/controller, resizing, clipping, scale, focus, localization and accessibility. Separate client presentation from server-authoritative mutations. Validate in-game; static layout inspection is insufficient.
4. Run available static/structural checks, retain evidence, and mark unavailable runtime validation NOT TESTED.
5. Report changed files, validation results, licensing/provenance, outstanding blockers, and deployment/publication status.
