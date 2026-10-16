# Developer setup, updates and rollback

Canonical source: [GitHub repository](https://github.com/B47ANCE/B47ANCED-Codex-Team), branch `main`.
[Download main ZIP](https://github.com/B47ANCE/B47ANCED-Codex-Team/archive/refs/heads/main.zip).
Links follow main and may advance beyond this document's configuration version, 13.6.0.

## Prerequisites

Install [Git for Windows](https://git-scm.com/downloads/win), [Python 3.11+](https://www.python.org/downloads/windows/), [Node.js LTS](https://nodejs.org/en/download) and [GitHub CLI](https://cli.github.com/). Enable Python's PATH option. Open a new PowerShell window and install the official Codex CLI for the default Meshy integration:

```powershell
git --version
npm.cmd install -g @openai/codex
node --version
npm.cmd --version
npx.cmd --version
codex.cmd --version
py -3 --version
gh --version
gh auth login --hostname github.com --git-protocol https --web
gh auth status
```

Use your own Codex/GitHub identities, credentials and private machine settings.

## Download: choose clone or ZIP

Clone is preferred:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\Desktop\PZ" | Out-Null
Set-Location "$env:USERPROFILE\Desktop\PZ"
git clone --branch main https://github.com/B47ANCE/B47ANCED-Codex-Team.git
Set-Location .\B47ANCED-Codex-Team
git rev-parse HEAD
Get-Content .\VERSION
```

Alternatively, use a fresh extraction directory:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\Desktop\PZ" | Out-Null
Invoke-WebRequest -Uri "https://github.com/B47ANCE/B47ANCED-Codex-Team/archive/refs/heads/main.zip" -OutFile "$env:USERPROFILE\Desktop\PZ\B47ANCED-Codex-Team-main.zip"
Expand-Archive -LiteralPath "$env:USERPROFILE\Desktop\PZ\B47ANCED-Codex-Team-main.zip" -DestinationPath "$env:USERPROFILE\Desktop\PZ"
Set-Location "$env:USERPROFILE\Desktop\PZ\B47ANCED-Codex-Team-main"
Get-Content .\VERSION
```

Review README.md, AGENTS.md and docs/SECURITY.md. Windows may block downloaded ZIP scripts. If necessary, after reviewing the package, unblock only its scripts:

```powershell
Get-ChildItem .\tools -File -Filter *.ps1 | Unblock-File
```

Never relax machine-wide execution policy. ZIP setup verifies its manifest against canonical main; stale or feature-branch ZIPs are rejected. Download again if main moved.

## Install and enable automatic sign-in updates

Choose your own actual paths. The mod root must exist and contain only intended project folders. Omit RepositoryRoot for global-only setup.

```powershell
$teamWorkspace = "$env:USERPROFILE\Desktop\PZ\Codex"
$modRepositories = "$env:USERPROFILE\Desktop\PZ\Mods"
New-Item -ItemType Directory -Force $modRepositories | Out-Null
& .\tools\Setup-CodexTeam.ps1 -Workspace $teamWorkspace -RepositoryRoot $modRepositories -EnableUpdates
```

Python is discovered automatically; supply `-PythonExe` for a nonstandard runtime. Existing unmanaged team files require reviewed `-MigrateExisting`; rerun setup with that switch only after inspection. Customized managed files block updates. Custom guide text, project instructions, unrelated skills and local config remain independent. Never edit managed team files to store machine-specific settings.

## Default editor

Setup also creates B47ANCED-Saved-Chats.code-workspace for existing local Codex conversations. Open it and run Chats: Resume saved chat, then choose a chat and owning project. No sessions start automatically. Empty histories are supported; each developer supplies their own history. Use -SkipChatWorkspace to omit it. See [saved-chat setup, privacy and refresh](SAVED-CHATS.md).

Daily work uses Codex CLI inside VS Code. Setup creates B47ANCED.code-workspace in $teamWorkspace. Open it, run Terminal > Run Task > Codex CLI: Start in project, and choose the owning mod repository. The official extension is optional alongside this terminal workflow. See [daily use and workspace setup](VSCODE.md) and [the workflow map](CLI-WORKFLOWS.md). Use -SkipCLIWorkspace only to omit CLI/workspace provisioning intentionally. Existing desktop monitors remain active until a tested replacement exists.

Setup installs VS Code and the official Codex extension by default. If VS Code is absent, Windows App Installer/winget is required; alternatively install VS Code manually first. Pass `-SkipVSCode` for another editor or disposable test setup. Follow [VS Code setup and activation](VSCODE.md), including sign-in and the read-only editor verification command. Editor provisioning runs only during explicit setup, never automatic updates or rollback.

## Verify

Meshy MCP is also configured by default for Codex CLI and the Codex VS Code extension. Install Node.js LTS, Codex CLI and Python 3.11+ first; follow [Meshy setup](MESHY.md) for exact prerequisites, masked local API-key entry and the free balance verification command. Use `-SkipMeshy` to omit this optional service. No shared keys or paid generation are part of team setup.

```powershell
& .\tools\Test-CodexTeamInstall.ps1 -PackageRoot . -Installed
& .\tools\Test-ModRepositories.ps1 -RepositoryRoot $modRepositories
Get-ScheduledTask -TaskName B47ANCED-Codex-Update
Get-Content "$env:USERPROFILE\.codex\b47anced-team-state.json"
```

Open a new Codex chat and confirm 23 global team skills. Desktop activation is a separate manual check; absence of the Codex CLI is not a failure.

Repository verification is read-only. It skips the `.worktrees` container and
accepts either the managed startup marker or a custom guide referencing the global
`.codex/AGENTS.md`: `%USERPROFILE%`, `$env:USERPROFILE`, `~`, or the absolute path
under the selected `-HomeDirectory`, with either path separator. Missing guides
and unrelated references still fail. Keep existing custom project instructions;
no guide rewrite or connector run is needed just to satisfy verification.

## Updates

For mod development, update relevant GitHub documentation in the same branch/PR as each code iteration, rather than waiting for release. Keep behavior, setup, configuration, compatibility, limitations and test evidence current. Review affected docs before pushing and explain in the PR if none need changes. Preserve historical validation and project-specific instructions.


The least-privilege sign-in task applies validated main updates. Updates check the full manifest, exact-commit CI, local drift and version progression; create a backup and roll back failed transactions. Downloaded executable code is installed inert. Bootstrap changes need manual review/setup.

```powershell
# Check only:
& "$env:USERPROFILE\.codex\b47anced-team-tools\Update-CodexTeam.ps1" -CheckOnly
# Apply:
& "$env:USERPROFILE\.codex\b47anced-team-tools\Update-CodexTeam.ps1"
# Inspect scheduled results:
Get-ScheduledTaskInfo -TaskName B47ANCED-Codex-Update
Get-Content "$env:USERPROFILE\.codex\b47anced-team-tools\last-update.log"
```

## Manual rollback of a completed update

Run the new rollback command from a **manually reviewed checkout/extracted package** containing tools/Restore-CodexTeam.ps1. Do not run automatically downloaded hub tools without review. This command can restore an earlier 13.1.x update backup; a first installation with no previous-state.json cannot be rolled back this way.

From that reviewed repository directory:

```powershell
# Preview checks without restoring:
& .\tools\Restore-CodexTeam.ps1 -CheckOnly
# Pause sign-in updates so they do not immediately reapply main:
Disable-ScheduledTask -TaskName B47ANCED-Codex-Update
# Validate again, create a recovery backup and restore:
& .\tools\Restore-CodexTeam.ps1
```

Rollback shares the update lock and refuses current managed drift, corrupt/missing backup files, linked paths, unsafe ownership or workspace changes. It restores the previous state and owned files only. New managed files are archived in a recovery backup before removal; directories are never recursively deleted. Local config, credentials, unrelated skills, project rules and trusted bootstrap remain untouched. It does not restore historical duplicate workspace skills. Backups missing prior ownership evidence need manual review. Keep every backup: integrity checks verify saved files against prior recorded hashes, not an independent signature against deliberate local tampering.

If restoration fails, it attempts to restore the current transaction from the recovery backup and returns an error. Keep error output and backups; do not retry blindly. After resolving the cause and deciding to resume main updates:

```powershell
Enable-ScheduledTask -TaskName B47ANCED-Codex-Update
```

Re-enabling permits the next sign-in to install newer validated main again. Restore-CodexTeam.ps1 accepts -HomeDirectory only for deliberate isolated testing; normal users omit it. Do not change USERPROFILE.

No setup/update/rollback command publishes mods, launches PZ or modifies a dedicated server. Offline setup tests do not prove PZ runtime correctness.

## Owner merges

B47ANCE may self-merge their own PR after required CI passes without another developer approval. Other developers require reviewer approval. Keep feature branches and PRs; never bypass CI or force-push. The review bypass uses repository administrator role and applies through PRs only. Current settings cover all five existing B47ANCE-owned repositories; new repositories need equivalent setup.
