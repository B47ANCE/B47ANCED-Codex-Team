---
name: pz-api-audit
description: Verify Project Zomboid Build 42 Lua API assumptions against locally installed game evidence before implementation.
---
Read the canonical workspace guide at `%USERPROFILE%/.codex/AGENTS.md` and the active project's current files. Identify installed game version, locate relevant Lua/API evidence, list exact methods/events and their signatures, distinguish confirmed from inferred behavior, and document a minimal runtime validation plan for uncertain calls. Never invent API access or introduce/require custom Java, injected classes or Java/JAR mod dependencies. Native source inspection is evidence only; use exposed vanilla Lua APIs or document a Lua-only alternative. Audit alone does not authorize launching PZ/server, deployment or publishing.
