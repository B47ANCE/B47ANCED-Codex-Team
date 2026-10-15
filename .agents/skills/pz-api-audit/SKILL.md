---
name: pz-api-audit
description: Verify Project Zomboid Build 42 Lua APIs against installed evidence and record build-specific findings for reuse.
---
Read the current global guide and active project instructions. Identify the installed game version and Steam build before auditing relevant Lua/API evidence. Never introduce custom Java/JAR code or assume native signatures prove Lua exposure. Audit alone does not authorize game/server launch, deployment or publication.

## Consult the library first

Use [the API catalog](references/api-library.json) for relevant symbols, not as a complete engine API reference. [Catalog guidance](references/library-guide.md) explains the entry fields and recording workflow. The helper searches the curated catalog plus the developer's local draft by default:

```powershell
python <skill-folder>/scripts/api_library.py search --symbol getModInfo --steam-build <installed-build-id> --game-root <verified-game-root>
```

A different build is `STALE_BUILD`; changed/missing source evidence is `STALE_SOURCE`. Even `SOURCE_HASH_MATCH` confirms only the recorded evidence bytes, not an unrecorded overload, execution side, authority model or runtime behavior. UNKNOWN version/signature/return details stay UNKNOWN. Record observed call forms separately from complete documented signatures.

## Audit and record

Inspect only relevant current sources. State exact methods/events, argument/return observations, execution side, state ownership, mutation/synchronization/persistence limits, and uncertain runtime gates. Prefer an exposed vanilla Lua route; document a Lua-only alternative when access is unsupported. Keep source verification, offline tests, SP and dedicated MP evidence distinct.

After each audit, record reusable findings using the helper's `record` action and a structured entry, including negative/uncertain findings. Its default destination is `%USERPROFILE%/.codex/pz-api-audit/library.local.json`; this unmanaged local draft survives team updates. Do not edit the installed managed catalog or this skill during ordinary audits. Drafts are searchable but are not approved shared facts.

Promote useful findings into this skill's `references/api-library.json` in a reviewed source checkout, validate, regenerate the team manifest and use the normal version/PR/update workflow. This keeps the API knowledge inside the shared skill without creating local drift. No raw game/decompiled source, diagnostic logs, credentials or developer paths belong in the shared catalog. Keep detailed project/runtime evidence in its owning project and cite portable evidence fingerprints.
