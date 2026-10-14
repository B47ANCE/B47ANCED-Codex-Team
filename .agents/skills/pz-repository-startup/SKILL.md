---
name: pz-repository-startup
description: Mandatory read-only GitHub freshness and working-tree preflight before any repository edits, commits, deploys, or publishes.
---
# Repository startup and latest-version gate

Before modifying any repository, run `%USERPROFILE%/.codex/b47anced-team/tools/Test-PZRepositoryFreshness.ps1 -Repository <path>` or equivalent checks. A fresh check is required for each new work session and again immediately before commit, deploy, or publish. Do not rely on stale cached results.

- Identify Git root, current branch, remotes, upstream and HEAD. Fail closed on detached HEAD, missing remote/upstream, unresolved merge/rebase, or ambiguous target unless user resolves it.
- Fetch remote references without changing the worktree. Compare HEAD with its tracking branch using `git rev-list --left-right --count HEAD...@{upstream}`. Compare the remote default branch as well; a feature branch can be up to date with its upstream while missing changes from main.
- Inspect `git status --porcelain=v1` for dirty and untracked files. Preserve all work. Never auto-stash, reset, clean, pull, merge, rebase, or force-push.
- Report local/remote commit SHAs, ahead/behind counts, default-branch divergence, and freshness. Local VERSION and mod.info are metadata, not a substitute for commit ancestry.
- If remote fetch fails, status is UNKNOWN, not CURRENT; do not edit until user explicitly authorizes offline work. Block commit/deploy/publish on unverified freshness by default.
- Behind or diverged branch: stop before editing and ask for safe reconciliation. Ahead-only feature branch can proceed with its upstream verified, subject to project branch policy. Dirty working tree: disclose and only proceed when changes are understood and do not conflict with the task.
- Never automatically check out or update the branch. Never modify other developers' files or credentials.
- If the target is not yet a Git repository, follow repository-governance onboarding rather than pretending a freshness check passed.
- For release actions, verify the release source commit and upstream relationship immediately before packaging/upload. `publish` must never be performed from a stale or ambiguous checkout.

Read the canonical shared AGENTS.md and project instructions. Preserve Lua-only, sandbox, canonical version and G7 dedicated MP / G8 release policies. Non-Git legacy repositories remain onboarding blockers, not permission to create a remote or invent VERSION. Fetch updates tracking refs but never the working tree; the helper does not prune refs. A missing remote-default reference or dirty state is REVIEW, not PASS. Offline authorization already given explicitly in the session remains valid.
