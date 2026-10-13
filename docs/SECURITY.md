# Security and trust

This is a public repository. Never commit SFTP/Steam passwords, WinSCP exported sessions, GitHub tokens, private keys, or raw server logs. Rotate exposed credentials.

**Auto-update trust:** Each workstation trusts maintainers allowed to merge to `main`. A passing CI check does not make malicious changes impossible. Require PR review, restricted write access, and branch protection/rulesets on GitHub. No updater should run scripts from the newly fetched checkout.

**Validation:** `tools/team_config.py validate` rejects symlinks, unexpected file types, secret-like filenames, malformed skills, missing required files, and integrity mismatches. It does not replace a full secrets scanner. CI additionally runs Gitleaks using a pinned release in a reviewed workflow, or equivalent.

**Credentials:** Machine-specific configuration remains local and is excluded from Git. Do not configure SFTP write access for diagnostics.

**Rollbacks:** Backups are made before applying updates; restore from a known good backup if a local failure occurs.
