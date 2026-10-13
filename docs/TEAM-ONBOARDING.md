# Three-desktop onboarding

1. Review `docs/SECURITY.md`, protect the public GitHub `main` branch and restrict merge permissions.
2. Install Git, Python 3.10+ and Codex on each Windows desktop; verify `git --version` and `py -3 --version`.
3. Clone this configuration repository from the approved public URL. Never use an unverified URL.
4. Back up existing `%USERPROFILE%\.codex\AGENTS.md`, `config.toml`, and shared skills.
5. Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Install-CodexTeam.ps1 -RepositoryPath . -RepositoryUrl https://github.com/OWNER/B47ANCED-Codex-Team.git` after replacing OWNER.
6. Check `%LOCALAPPDATA%\B47ANCED-Codex-Team\state.json` and run `tools\Test-CodexTeamInstall.ps1`.
7. Configure developer-specific paths and credentials manually in ignored local files. No secrets in public GitHub.
8. Register the scheduled updater only after a dry run: `tools\Register-CodexTeamUpdater.ps1 -TaskName B47ANCED-Codex-Update`.
9. Verify startup update behavior on one desktop, then repeat on the other two.
10. Confirm `deploy`, `publish` and SFTP workflows independently; these are not validated by installing configuration.

**Auto-update policy:** validated `main` commits install at user logon via Task Scheduler; the task invokes the previously installed trusted updater. A local manifest check and backup precede installation. Dirty managed files cause a safe stop.
