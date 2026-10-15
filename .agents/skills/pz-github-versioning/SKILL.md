---
name: pz-github-versioning
description: Version, commit, push, and verify public GitHub iteration history for Lua-only Project Zomboid mods.
---

# Public GitHub versioning

Read the canonical shared guide at `%USERPROFILE%/.codex/AGENTS.md` and the selected project instructions. Runtime mods remain Lua-only; server authority, sandbox configuration and dedicated runtime gates still apply.

Trigger on `commit`, a requested version iteration, or explicit GitHub backup.

1. Inspect repository root, branch, `git status --short`, `git remote -v`, upstream, and current HEAD. Do not assume repository identity.
2. Confirm GitHub remote points to the intended PUBLIC repository; when creating a new repository, ensure public visibility and verify it. Never invent an owner or silently change an existing remote.
3. Discover canonical root VERSION, mod.info, the declared current mirrors and docs/VERSION_POLICY.md. Classify PATCH/MINOR/MAJOR compatibility impact and record the target development version before implementation. Never invent a missing version. Run existing scripts/check_versions.py before and after changes; update current mirrors and CHANGELOG.md consistently while preserving historical evidence. Keep dependency/game/schema versions separate. Do not change Workshop IDs.
4. Run focused available validation and record static/SP/MP evidence accurately. A development snapshot may be pushed with untested runtime gates if labeled clearly. Version inconsistency blocks release G8; gameplay requires dedicated G7 PASS before G8. Do not treat a pushed iteration as release-ready.
5. Inspect `git diff`, `git diff --cached`, `git status --ignored`, and relevant tracked files. Stage only intended source, tests, and documentation. Exclude generated staging, archives, secrets, SFTP profiles, server diagnostics, private player data, and local settings. Check for secrets BEFORE pushing. If exposed, stop; do not push and do not silently rewrite history.
6. Commit with a meaningful message that includes the iteration when appropriate. Push to the configured upstream (or establish upstream with explicit approval when missing). Verify `git rev-parse HEAD` matches the remote branch SHA after push.
7. Only for explicitly approved stable releases: create an annotated vX.Y.Z tag and push it after release gates pass. A GitHub push never implies Steam Workshop publication.
8. Report repository, branch, commit SHA, remote verification, version, files changed, validation status, and any blockers. Never claim success without verification.

Safety: Never force-push, delete branches, reset user changes, make repos private, or commit secrets. Respect Codex sandbox and approval prompts.

## Team branches and review

Documentation ships with each development iteration. Before commit/push, review the relevant README, CHANGELOG and existing feature/design, setup, sandbox/configuration, compatibility, API and validation docs against the implemented change. Update affected documents in the same branch/PR, including current limitations and exact offline/SP/dedicated evidence; do not wait for release. Record a reason in the PR when no documentation update is needed. Preserve project instructions and historical evidence. Only update documents affected by the change; a version mirror update does not by itself document changed behavior.

Use a named feature/fix branch for team work and open a PR before merging shared main. In B47ANCE-owned repositories, owner B47ANCE may self-merge their own PR after required CI passes without approval from another developer or a temporary protection exception; other developers require reviewer approval. An explicit merge request authorizes this owner self-merge; never bypass required CI. Preserve the intended remote/upstream and unrelated user changes. A commit request authorizes the intended iteration commit/push; it does not authorize merging shared main, changing repository visibility or settings, or creating an unverified stable release. Prefer available CI and report missing gates.

## Workshop test distribution exception
Apply the Workshop MP testing policy in global AGENTS.md and installed hub docs/WORKSHOP_MP_TESTING.md. Missing dedicated MP evidence alone does not block an explicitly authorized labelled Workshop test upload. G7 remains NOT TESTED / BLOCKED and stable-release G8 remains BLOCKED; offline/authority/security/version/package failures still block upload. This skill does not itself authorize publication.
