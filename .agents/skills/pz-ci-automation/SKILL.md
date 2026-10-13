---
name: pz-ci-automation
description: CI automation — GitHub Actions
---

# CI automation — GitHub Actions
Use for new repositories, pull requests, and changes to checks.
- Keep CI read-only with respect to Steam Workshop, live servers, and local installs. Never expose Steam/SFTP credentials to PR workflows.
- Run offline checks: version/inventory, Lua syntax if a compatible interpreter is available, secret scanning, case/path safety, translation keys, package validation and focused tests.
- Missing dependencies or absent tests must be reported as NOT TESTED, not silently passed. Never claim a Lua syntax checker proves game API correctness.
- Pin third-party actions to reviewed commit SHAs before production use; minimize GITHUB_TOKEN permissions and prevent untrusted PR code from receiving secrets.
- Require green checks and human review before protected main merges. Configure branch protection in GitHub separately; a workflow file does not enforce it.
- Record commit SHA, check results and artifacts. CI must not publish, deploy or delete automatically.

## Shared workspace policy
Read `C:/Users/willi/Desktop/Work/Project Zomboid/Codex/AGENTS.md` and the active project instructions. Preserve Lua-only runtime, server authority, sandbox configuration and canonical version policy. Dedicated gameplay G7 must PASS before release G8; do not adopt alternate gate numbering or relabel historical evidence. This skill does not authorize live deployment, publication, game/server launch or external access by itself. Existing user authorization and explicit changes to repository grouping or visibility take precedence.
