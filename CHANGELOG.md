# Changelog

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
