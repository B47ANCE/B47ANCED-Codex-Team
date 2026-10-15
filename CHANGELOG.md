# Changelog

## 13.4.7 - 2026-10-15
- Require affected GitHub documentation to stay current in the same branch/PR as each mod development iteration, including behavior, setup, compatibility, limitations and actual validation evidence.
- Add the documentation review to the shared versioning skill and onboarding guidance; preserve project instructions and historical evidence.

## 13.4.6 - 2026-10-15
- Make read-only repository verification skip the .worktrees container and accept custom guides referencing the shared global AGENTS.md. Preserve missing-guide/skill failures and all project instructions/settings.
- Add six PowerShell regression fixtures covering custom references, lookalikes, exclusions and byte-preservation; document supported references.

## 13.4.5 - 2026-10-14
- Add 12 receiver/bootstrap findings from the all-mod source audit, including missing next/table.unpack dependencies and script-item versus inventory-item distinctions. All runtime evidence remains NOT_TESTED.
- Record bounded coverage, applied local fixes and user-deferred overlays. Add catalog/evidence regression checks; preserve earlier reports as historical evidence.

## 13.4.4 - 2026-10-14
- Document the supported FluidContainer.getAmount storage query and distinguish IsoObject.getFluidAmount world-source semantics; retain the conflicting component API as UNKNOWN.
- Audit local mod usage: three Quartermaster world-object callers and no confirmed invalid component caller. Preserve valid finite-source guards and all mod code.
- Add source/usage evidence and a verified world-object record. All 94 catalog records remain runtime NOT_TESTED.

## 13.4.3 - 2026-10-14
- Trace all 21 remaining candidates through packaged Lua binding construction: 19 registered class methods and two annotated globals. Verification is source exposure only; invocation and runtime remain NOT_TESTED.
- Keep FluidContainer.getFluidAmount UNKNOWN after checking the hierarchy, interfaces and annotation aliases; no packaged binding was found.
- Preserve prior behavior limits and add exposure-route regression checks. Shared catalog: 92 source observations/routes VERIFIED and one UNKNOWN; no runtime promotion.

## 13.4.2 - 2026-10-14
- Deep-review all 70 unresolved API records: 48 now have bounded source-verified receiver/call observations, 21 remain inferred and one fluid API conflict remains unknown. All 93 shared records remain runtime NOT_TESTED.
- Replace unrelated receiver/name matches, record packaged descriptors and available loose-class metadata, and document negative/conflicting evidence without claiming Lua access from native signatures alone.
- Preserve historical provenance and add regression coverage for native-only and conflicting findings.

## 13.4.1 - 2026-10-14
- Share 90 audit-derived API observations alongside the three existing catalog entries: 23 source-verified observations, 52 inferred matches and 18 unknowns; all runtime NOT_TESTED.
- Preserve build/source fingerprints and bounded verification scope; document historical provenance, modified-installation limits and teammate rechecking.
- Test that source/hash checks never promote inferred or unknown findings to verified/runtime evidence.

## 13.4.0 - 2026-10-14
- Add a build-bound API evidence catalog inside pz-api-audit with validated search/record helper and unmanaged per-user drafts.
- Seed three source-observed vanilla Mod Selector calls without claiming full version or runtime verification.

## 13.3.1 - 2026-10-14
- Use a directly resized 512x512 B47.png for fallback Workshop thumbnails; keep the 64x64 icon and 128x128 poster separate.

## 13.3.0 - 2026-10-14
- Add portable exact user-supplied fallback PNG data; manually supplied artwork takes precedence.
- Register fallback branding for seven selected projects and future team mods; UI excluded.

## 13.2.3 - 2026-10-14
- Automatically gracefully restart the verified Steam desktop client after confirmed successful Workshop publication; report restart independently and never force termination.

## 13.2.2 - 2026-10-14
- Permit explicitly authorized labelled Workshop MP test uploads before dedicated testing; retain stable G7/G8 and all other preflight requirements.

## 13.2.1 - 2026-10-14
- Permit owner self-merges after required CI, while retaining reviewer approval for other developers.
- Document review-only administrator PR bypass separate from CI/history safeguards.

## 13.2.0 - 2026-10-14
- Add explicit validated manual rollback with drift/path guards, recovery backup and update lock.
- Consolidate download, prerequisites, setup, sign-in update and rollback commands in onboarding.

## 13.1.1 - 2026-10-14
- Explicit isolated home target propagated through setup, validators, updater and scheduled runner.
- Check Git/GitHub CLI and repository-root prerequisites before managed writes.
- ZIPs inside another Git checkout no longer inherit unrelated commit identity.
- Desktop-only Codex installations no longer fail solely for absent CLI.


## 13.1.0 - 2026-10-14
- Portable setup entry point, canonical URL, Python discovery and sign-in logging.
- One global skill store; archive verified workspace duplicates with rollback.
- Lightweight workspace rule reference; preserve custom global/project instructions and settings.
- Bootstrap files under user profile instead of AppData; block downgrades.


## 13.0.1 - 2026-10-13
- Preserve exact manifest bytes across Windows/Linux Git clones.
- Install templates, docs and tools transactionally; require successful exact-main-commit CI, drift checks, unique backups and rollback.
- Preserve stronger existing PZ rules and all local configuration.


## 13.0.0 — 2026-10-13
- Complete public configuration repository with all 23 existing skills.
- Added validated main-branch updater, trusted bootstrap, backups, hash-based drift detection, rollback and scheduled sign-in updates.
- Added GitHub Actions validation and installer regression tests.
- Applied publication-triggered GitHub policy for mod projects.
- Separated shared team rules from machine-specific settings.
- Preserved SteamCMD, local deploy and read-only SFTP instructions without claiming unverified integrations.
