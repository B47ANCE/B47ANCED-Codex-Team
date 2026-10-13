---
name: pz-mp-audit
description: Audit a Project Zomboid Lua feature for dedicated-server authority, synchronization, persistence, and failure cases.
---
Trace client requests, server validation, state ownership, server sandbox interpretation, network messages, late joins, disconnects, restarts, headless server compatibility, and duplication/exploit boundaries. Remain Lua-only using exposed vanilla APIs. Stop affected gameplay implementation if safe authority cannot be established; never downgrade to client authority. Classify static evidence separately from dedicated multiplayer runtime results. Require gameplay G7 PASS before G8; missing dedicated evidence is G7 BLOCKED / NOT TESTED and G8 BLOCKED. Provide test cases and blockers; audit does not authorize starting a server or deployment.
