---
name: pz-repository-governance
description: Audit and govern PZ Build 42 Lua-only repositories, canonical versions, source provenance, packages, localization, Linux case safety, and retention.
---
# PZ repository governance

Read the canonical shared guide at `C:/Users/willi/Desktop/Work/Project Zomboid/Codex/AGENTS.md` and the active project instructions. Preserve their gate nomenclature: dedicated gameplay G7 must PASS before G8. Never renumber historical validation.

1. Inventory repository, branches, remote visibility, tracked/untracked files, mod.info files, version files, src/Contents trees, build scripts, staging, ZIPs and docs. Do not assume a standard layout for existing projects.
2. Establish authoritative sources using scripts and recorded provenance. Identify mirrors and differences. Never overwrite ambiguous trees.
3. For new projects, initialize VERSION, README, CHANGELOG, project AGENTS.md, source/package inventory, .gitignore, validation entry point, and public GitHub remote. Do not invent an existing Workshop ID.
4. For legacy projects, propose canonical version based on evidence and require review before changing it; do not infer approval from modversion.
5. Audit Lua-only active dependencies, translation key coverage, case-correct requires, duplicate/unsafe ZIP paths, CRC, hashes and generated artifacts. Classify each check by evidence and scope.
6. Report gates separately: offline source/static, local SP, dedicated MP, publication. Historical results remain tied to historical versions.
7. Before any cleanup: dry-run, generate plan and protected-file ledger, preserve current/newest/stable/ambiguous builds and provenance, confirm explicit deletion authorization in the current session (do not ask again when already authorized); after cleanup verify hashes and produce a deletion ledger.
8. For an authorized version iteration, commit and push on a feature branch, open PR for review; never rewrite history or force-push. If not possible, state blocker.
9. Output concise findings, exact commands run, changed files, hashes/commit, verified GitHub visibility, and all untested gates.
