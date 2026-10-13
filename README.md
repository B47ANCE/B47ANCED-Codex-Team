# B47ANCE'd Workshop Codex Team — v13.0.0

Complete standalone, public GitHub-ready configuration repository with **23 skills**, shared Lua-only Project Zomboid development rules, templates, validation, and three-desktop automatic main-branch updates. No previous package is required.

## Important policy

Mod projects are not required to use GitHub until their **first confirmed Steam Workshop publication**. The team configuration repository itself is public on GitHub from inception. See `AGENTS.md`.

## First installation on each Windows desktop

1. Install Git, Python 3.10+ and Codex. Verify commands are on PATH.
2. Create the public GitHub repository `B47ANCED-Codex-Team` under your chosen owner. Upload these repository files, excluding credentials. **This ZIP does not create or push a GitHub repository by itself.**
3. Review repository contents and GitHub branch protections. Clone the approved URL.
4. Back up your current global Codex configuration and shared skills. `-MigrateExisting` explicitly authorizes replacing existing global AGENTS.md and matching skill folders after automatic backup; it never deletes unrelated skills.
5. From the reviewed checkout, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Install-CodexTeam.ps1 -RepositoryPath . -RepositoryUrl 'https://github.com/OWNER/B47ANCED-Codex-Team.git' -Initial -MigrateExisting
```

6. Check the installation with `powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Test-CodexTeamInstall.ps1 -PackageRoot .`.
7. Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Update-CodexTeam.ps1 -CheckOnly` from the reviewed checkout (requires installed trusted bootstrap).
8. Enable automatic updates at Windows sign-in:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\Register-CodexTeamUpdater.ps1
```

## Update behavior

The task runs the **previously installed trusted updater**. It clones `main` to temporary staging, validates with the previously installed validator, checks managed files against recorded hashes, backs up existing managed files, and installs only the known global `AGENTS.md` and 23 skill folders. Unmanaged skills and per-project instructions are untouched. Existing `config.toml` is preserved on subsequent updates.

Unexpected local modifications block an update; nothing is reset or discarded. A backup is created before changes and an attempted rollback occurs if copying fails. Updates occur at next Windows sign-in, not continuously. Version `VERSION` must change for each approved main update.

**Security:** This is a trusted-main auto-update system, not a sandbox for untrusted contributions. Protect main with required PR reviews and CI. Never commit credentials. See `docs/SECURITY.md`. The installer/updater bootstrap is updated only by manually running a reviewed installer again.

## Scope and limitations

Configuration installation and updates do not establish SteamCMD publication, SFTP log retrieval, Blender exports, or Project Zomboid runtime compatibility. Those require separate per-machine testing. See `docs/TEAM-ONBOARDING.md` and `docs/CONFIGURATION.md`.

## Owner-reviewed integration
Read docs/LOCAL-INTEGRATION.md for local corrections and preserved stricter policy. Installer requires explicit -PythonExe and optionally -Workspace. All original archive files and initial validation are preserved separately in the owner audit. No package script publishes a mod.
