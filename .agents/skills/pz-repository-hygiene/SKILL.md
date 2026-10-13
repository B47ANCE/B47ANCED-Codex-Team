---
name: pz-repository-hygiene
description: Read-only-first audits of Project Zomboid mod repository organization, tracked files, stale references, source integrity, and unwanted generated content.
---
# Repository hygiene
Use when asked to audit, organize, tidy, or clean repositories. Read repository-specific AGENTS.md, README, source inventory, build scripts, and git status before acting. Never assume src/ is authoritative or Contents/ is disposable.

## Read-only inventory
1. Identify repo root, branch, remote, dirty state, submodules, tracked/untracked/ignored files and symlinks; inspect git status without changing it.
2. Identify source of truth, generated build outputs, workshop staging, mirrors, backup folders, logs, caches, artifacts, editable 2D/3D assets and historical evidence. Trace build scripts before classifying files.
3. Flag orphan candidates, duplicate hashes, broken links, missing README targets, incorrect .gitignore patterns, accidentally tracked secrets, unexpectedly large binaries, case-only collisions, case-mismatched Lua requires, inconsistent line endings and metadata. A matching hash does not prove a file is safe to delete.
4. Identify version drift among VERSION, mod.info, changelog, packaging metadata and Workshop VDF. Report, never silently choose a version.
5. Check public-GitHub exposure of credentials, private SFTP profiles, player data and server logs; do not print secret values or publish them in reports. If a secret is tracked, stop publication and recommend rotation and controlled remediation.
6. For each finding, record exact relative paths, why flagged, confidence, impact, safe proposed action and whether source or history would be affected.

## Changes and approvals
- Default output is a report and proposed change plan only. No deletes, moves, rewrites, renames, git clean, git reset, force pushes, or history rewriting without explicit scoped authorization.
- Do not edit generated files as if they are authoritative. Keep public APIs, saves, project layout and build entry points intact.
- For approved non-destructive fixes, make bounded changes on a feature branch, run existing validation and inspect diff. Do not automatically combine hygiene work with feature changes.
- For deletions, invoke pz-artifact-retention if generated packages are involved; require an explicit path-level approved deletion plan and a recoverable backup where feasible.
- Never treat a dry-run as proof of actual deletion or a static check as gameplay verification.

## Deliverables
Produce inventory summary, findings by severity, proposed operations, protected-file list, tests run, changes made (if authorized), before/after hashes when applicable, Git status, and untested checks.

## Shared workspace policy
Read `C:/Users/willi/Desktop/Work/Project Zomboid/Codex/AGENTS.md` and the active project instructions. Preserve Lua-only runtime, server authority, sandbox configuration and canonical version policy. Dedicated gameplay G7 must PASS before release G8; do not adopt alternate gate numbering or relabel historical evidence. This skill does not authorize live deployment, publication, game/server launch or external access by itself. Existing user authorization and explicit changes to repository grouping or visibility take precedence.
