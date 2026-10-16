# B47ANCE Workshop Codex Team 13.5.0

23 Lua-only Project Zomboid skills, shared rules, templates and validated Windows sign-in updates. Canonical source: https://github.com/B47ANCE/B47ANCED-Codex-Team.git, branch main.

## Quick setup

The team default is **VS Code with Codex CLI in the selected project's integrated terminal**. Setup creates a local multi-folder workspace and manual workflow tasks; the official IDE extension remains available alongside the CLI. [Daily workflow and migration boundaries](docs/VSCODE.md), [all 23 skills/workflow map](docs/CLI-WORKFLOWS.md).

Install Git, Python 3.11+, Node.js LTS, Codex CLI and GitHub CLI for the default setup. [Meshy prerequisites and exact commands](docs/MESHY.md). Authenticate GitHub CLI locally with your own account. Clone main, review the files, then run:

```powershell
& ./tools/Setup-CodexTeam.ps1 -Workspace "$env:USERPROFILE/Desktop/PZ/Codex" -RepositoryRoot "$env:USERPROFILE/Desktop/PZ/Mods" -EnableUpdates
```

Choose your own paths and an existing mod root. Omit RepositoryRoot for global-only setup. Existing untracked global/team files require reviewed `-MigrateExisting`; custom instructions/config/unrelated skills are preserved. [Complete onboarding](docs/TEAM-ONBOARDING.md).

Explicit Windows setup now installs VS Code and the official Codex extension by default. Use `-SkipVSCode` for another editor or headless setup. [Editor setup and activation](docs/VSCODE.md). Existing editor settings and credentials are preserved.

Setup also adds the official [Meshy MCP integration](docs/MESHY.md) globally for Codex, with a pinned npx package, per-developer environment authentication and all tools exposed under prompt approval. Explicit approval is required before spending credits. Requires Node.js LTS, Codex CLI and Python 3.11+; use `-SkipMeshy` to omit it. Set your own API key only through the masked local prompt, then run the free balance verifier. Automatic updates never run either provisioning helper.

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
