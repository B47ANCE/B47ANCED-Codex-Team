# B47ANCE Workshop Codex Team 13.2.2

23 Lua-only Project Zomboid skills, shared rules, templates and validated Windows sign-in updates. Canonical source: https://github.com/B47ANCE/B47ANCED-Codex-Team.git, branch main.

## Quick setup

Install Git, Python 3.10+, Codex and GitHub CLI. Authenticate GitHub CLI locally with your own account. Clone main, review the files, then run:

```powershell
& ./tools/Setup-CodexTeam.ps1 -Workspace "$env:USERPROFILE/Desktop/PZ/Codex" -RepositoryRoot "$env:USERPROFILE/Desktop/PZ/Mods" -EnableUpdates
```

Choose your own paths and an existing mod root. Omit RepositoryRoot for global-only setup. Existing untracked global/team files require reviewed `-MigrateExisting`; custom instructions/config/unrelated skills are preserved. [Complete onboarding](docs/TEAM-ONBOARDING.md).

## One policy and skill store

Global `.codex/AGENTS.md` supplies team policy. Workspace AGENTS is a lightweight reference. `.agents/skills` in the user profile owns the 23 team skills. Verified identical workspace duplicates are archived, never deleted; customized copies block consolidation. Local settings and custom project instructions remain independent. Tools/templates/docs live under `.codex/b47anced-team`.

Updates require successful CI for the exact main SHA, a full manifest, unchanged managed files, unique backups and rollback. Downgrades and changed commits reusing VERSION are blocked. The pinned local bootstrap validates downloaded data without executing downloaded code; manually review bootstrap upgrades. Sign-in uses the user-profile bootstrap directory and logs results, avoiding AppData visibility problems.

## Validate

```powershell
python tools/team_config.py validate --source .
python -m unittest discover -s tests -v
& ./tools/Test-CodexTeamInstall.ps1 -PackageRoot . -Installed
```

[Security](docs/SECURITY.md), [ownership/configuration](docs/CONFIGURATION.md), [changelog](CHANGELOG.md). CI remains offline; no deployment, Workshop upload or dedicated-server access is implied. G7 dedicated MP and G8 release gates remain unchanged.
