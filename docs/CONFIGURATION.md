# Managed and developer-local ownership

Managed: global team guide block, 23 global skills, hub tools/templates/docs, selected workspace guide and supporting resources. Custom text outside the global team block is preserved; full-file drift checking stops unattended updates after local edits. Per-project guides retain text outside their managed startup block; the connector backs up before replacing only that block.

One physical team skill store lives under the user profile `.agents/skills`. Verified byte-identical workspace copies move into a unique transaction backup. Customized copies block consolidation. Rollback restores archived directories on failure; unrelated skills are never moved.

Existing config.toml, developer settings, SSH/Steam/Git authentication and local paths are never overwritten or committed. Bootstrap source.json contains paths and approved URL only, next to the pinned validator/updater in `.codex/b47anced-team-tools`, not AppData. State is `.codex/b47anced-team-state.json`; backups are `.codex/b47anced-backups`.
