# Managed versus local files

Managed globally: `%USERPROFILE%\.codex\AGENTS.md`, 23 `pz-*` skill folders in `%USERPROFILE%\.agents\skills`, and `%USERPROFILE%\.codex\config.toml` only on initial install. On subsequent updates config.toml is preserved as developer-local.

Local: `local.settings.json`, saved WinSCP session, SSH host key, SteamCMD cached credentials, Git authentication, custom Codex configuration overrides, and installed game paths. These are never included in GitHub.

The updater manages only the named 23 skills. It does not delete unrelated skills or project-specific AGENTS.md. It will stop if a managed file has changed unexpectedly rather than clobber local edits.
