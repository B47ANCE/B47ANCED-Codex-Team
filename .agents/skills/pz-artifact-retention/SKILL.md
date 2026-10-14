---
name: pz-artifact-retention
description: Plan and verify conservative cleanup of generated Project Zomboid release ZIPs, Workshop staging, build artifacts, and archives without risking source or historical evidence.
---
# Artifact retention and safe cleanup
This is a destructive-workflow gate. Planning is always read-only unless the user explicitly authorizes a precise cleanup scope.

1. Inventory each artifact stream separately (dist, release ZIP, staging, candidate, stable, archives) and inspect version evidence from filenames, embedded mod.info, VERSION, build manifests and known scripts. Never invent a canonical version from filenames alone.
2. Compute SHA-256 for every candidate and protected file, capture file size, timestamps, relative path, archive entries, and ambiguous metadata. Avoid opening archives with unsafe traversal paths.
3. Protect authoritative source, VERSION, README, tests, scripts, research, native/toolchains, editable asset masters, backups, runtime logs, historical evidence and release ledgers. Also protect current-version, newest, newest-stable, dist/current, candidates, ambiguous versions, mismatched metadata and collision cases by default.
4. Classify each artifact KEEP, REVIEW, or PROPOSE_DELETE with reasons and hashes. Treat historical published artifacts conservatively even when superseded.
5. Produce a human-readable plan and machine-readable proposed-deletions ledger; do not execute deletions in the same step as a generic audit request.
6. Confirm explicit session authorization for the exact deletion scope and retention rule; ask only if authorization is absent or unclear. If unanswered, do not expand deletion scope. An approved cleanup must not imply permission to remove source or staging backups.
7. Before execution recheck paths, hashes and current version; abort on drift, symlink escapes, path traversal, unexpected changes, or mismatched approval. Prefer reversible quarantine if authorized and feasible.
8. After execution verify every remaining protected file hash and retained archive integrity (including ZIP CRC), record deleted paths and pre-deletion hashes, and report reclaimed bytes accurately.
9. Never replay a prior cleanup ledger as executable instructions. Preserve audit provenance and do not rewrite historical validation claims.

Return exact status: PLANNED, APPROVED, EXECUTED, VERIFIED, or BLOCKED. Keep offline integrity distinct from SP, dedicated MP, and Workshop publication gates.

## Shared workspace policy
Read `%USERPROFILE%/.codex/AGENTS.md` and the active project instructions. Preserve Lua-only runtime, server authority, sandbox configuration and canonical version policy. Dedicated gameplay G7 must PASS before release G8; do not adopt alternate gate numbering or relabel historical evidence. This skill does not authorize live deployment, publication, game/server launch or external access by itself. Existing user authorization and explicit changes to repository grouping or visibility take precedence.
