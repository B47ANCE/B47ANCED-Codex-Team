---
name: pz-security-permissions
description: Audit Project Zomboid repository secrets, workflow permissions and publishing or diagnostic access.
---

# Security and permissions
Use for credentials, workflows, external connectivity, release permissions and repository audits.
- Repositories are always PUBLIC; never commit secrets, local settings, passwords, SteamCMD login data, SFTP credentials, player information, server logs or private key material.
- Run a pre-commit secret scan and review staged diff. If secrets have been committed, stop, revoke/rotate and coordinate history remediation; deleting in a later commit is insufficient.
- Assign least privilege by developer. Only explicitly authorized release maintainers may publish Workshop updates. The command `publish` authorizes the intended existing Workshop item but does not override actual account permissions.
- SFTP diagnostics are GET/LIST only, restricted to allowlisted logs. Prefer host-enforced read-only access; download-only scripts do not guarantee read-only permissions.
- Verify SSH host fingerprints; do not disable host key checks. Do not put passwords in scripts, config, arguments, or console output.
- No destructive git, filesystem or remote actions without a scoped approval; no force push.
- Document what was inspected and remaining security gaps without leaking sensitive data.

## Shared workspace policy
Read `C:/Users/willi/Desktop/Work/Project Zomboid/Codex/AGENTS.md` and the active project instructions. Preserve Lua-only runtime, server authority, sandbox configuration and canonical version policy. Dedicated gameplay G7 must PASS before release G8; do not adopt alternate gate numbering or relabel historical evidence. This skill does not authorize live deployment, publication, game/server launch or external access by itself. Existing user authorization and explicit changes to repository grouping or visibility take precedence.
