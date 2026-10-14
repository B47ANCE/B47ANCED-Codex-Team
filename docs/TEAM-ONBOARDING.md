# Set up the second and third developer

1. Install Codex, Git, Python 3.10+ and GitHub CLI. Authenticate locally with your own identity; never share credentials.
2. Clone the canonical repository:

```powershell
git clone --branch main https://github.com/B47ANCE/B47ANCED-Codex-Team.git
cd B47ANCED-Codex-Team
```

3. Review README, AGENTS and docs/SECURITY.md, then run:

```powershell
& ./tools/Setup-CodexTeam.ps1 -Workspace "$env:USERPROFILE/Desktop/PZ/Codex" -RepositoryRoot "$env:USERPROFILE/Desktop/PZ/Mods" -EnableUpdates
```

Choose your own paths. RepositoryRoot must exist and contain only intended mod folders; omit it for global-only setup. Python is discovered automatically; use `-PythonExe` for a nonstandard runtime. Existing untracked global/team files require explicit reviewed `-MigrateExisting`; custom global guide text and unrelated skills/config are preserved. Managed-file drift blocks updates.

Alternatively download the main-branch ZIP from GitHub, extract it and run the same setup command inside the extracted folder. The installer validates every file and requires the ZIP manifest to match canonical main before assigning its commit SHA. A feature-branch or stale ZIP is rejected; cloning remains the preferred workflow.

Windows may mark ZIP-extracted scripts as downloaded. Review before running; prefer the clone workflow. If unblocking is necessary, unblock only the reviewed package scripts, never relax the machine policy globally.

4. Open a new Codex chat and confirm 23 global skills are visible. Workspace guides reference global policy; team skills are not copied into every project. Custom project rules and unrelated project-local skills remain.
5. Inspect `.codex/b47anced-team-state.json` and `.codex/b47anced-team-tools/last-update.log` under your user profile. The sign-in task uses least privilege, exact-main-commit CI, manifest/drift checks and backups. Bootstrap updates require manual reviewed setup; newly downloaded scripts are not run during updates.

Local SteamCMD/game/mod paths, SSH profiles and developer settings remain private. Existing config is not overwritten. No mod publication, game launch or dedicated-server modification occurs. Offline checks do not prove app activation or PZ runtime. Main requires reviewer approval and CI before changes ship.

## Isolated validation

Setup and validators accept -HomeDirectory for a disposable installation target; omit it for your normal Windows profile. Scheduled tasks pass the chosen target explicitly. Do not change USERPROFILE or reuse another developer's credentials to test. Desktop-only Codex activation is a separate manual gate, not a required CLI check.
