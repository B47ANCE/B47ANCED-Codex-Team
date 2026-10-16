# Default team workspace: VS Code with Codex CLI

Daily development uses Codex CLI in VS Code's integrated terminal, at the selected project's root. The official extension remains available alongside the CLI. Global Codex config, authentication, MCP servers and all 23 team skills are reused, never copied into each repository.

Explicit Windows team setup installs Microsoft VS Code for the current user when absent, then the official OpenAI Codex extension `openai.chatgpt`. Windows App Installer supplies winget. If winget is unavailable, install VS Code from https://code.visualstudio.com/Download and rerun setup. Existing installations are reused. Settings, keybindings, credentials and unrelated extensions are preserved. Use `-SkipVSCode` with Setup-CodexTeam.ps1 for headless/disposable setup or another editor.

For an already installed team configuration, run only the editor helper from a reviewed repository checkout:

```powershell
& .\tools\Setup-VSCode.ps1
& .\tools\Setup-VSCode.ps1 -CheckOnly
& .\tools\Setup-CodexCLI.ps1
& .\tools\Setup-CodeWorkspace.ps1 -Workspace $teamWorkspace -RepositoryRoot $modRepositories -Open
```

Use the paths selected during onboarding. Open B47ANCED.code-workspace, then Terminal > Run Task > Codex CLI: Start in project. Choose the actual mod repository for development; choose the research/setup workspace only for that work. The resume task opens the CLI session picker. Sign in locally with codex login if needed. Review Workspace Trust yourself and confirm global instructions, skills and MCP tools in the new session. For optional IDE-extension use, select the Codex icon or run Codex: Open Codex Sidebar.

Use Explorer, source control, diffs, search and the integrated terminal alongside Codex. Open files and selections can supply editor context. Other extensions do not automatically become Codex tools; desktop-only integrations may differ. Installation verification does not prove authentication or agent activation.

Automatic team updates and rollback install this helper inert and never execute editor provisioning. VS Code and extension updates follow existing editor preferences. Team rollback restores team-managed files, not editor versions. The helper does not change update preferences or launch an editor.

Official references: [Codex IDE](https://developers.openai.com/codex/ide), [official extension](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt), [Windows setup](https://code.visualstudio.com/docs/setup/windows), [VS Code CLI](https://code.visualstudio.com/docs/configure/command-line).

## CLI tasks and preserved ownership

Explicit Setup-CodexTeam.ps1 verifies/installs Codex CLI, provisions the integrations and generates the workspace. Use -SkipCLIWorkspace to omit CLI/workspace provisioning intentionally; base-only disposable setup uses -SkipCLIWorkspace -SkipVSCode -SkipMeshy. CLI setup preserves an existing CLI version and installs official @openai/codex only when absent.

The generated multi-folder workspace shows the research/setup folder and selected mod root. Its project picker excludes hidden infrastructure folders such as .worktrees. Each CLI starts in the selected repository with workspace-write sandbox, on-request approvals and live web search. Model and reasoning preferences remain yours. No task runs automatically when opening the workspace. Opening multiple folders does not authorize Codex to edit all of them.

Manual tasks cover CLI start/resume, freshness, an existing scripts/check_versions.py, team/repository verification, update check/apply, rollback preview, MCP connection names, masked Meshy key entry and a free balance check. Project-specific build/test/deploy/publish workflows remain governed by their existing instructions and [the workflow map](CLI-WORKFLOWS.md). Missing version checkers are reported, never invented.

No .vscode files are written into mod repositories. A developer-local launcher and hash state live in .codex/cli-workflow-runtime. Explicit refresh updates only outputs matching their last recorded hashes, backing up old files in .codex/cli-workflow-backups. Customized workspaces/launchers block regeneration for manual review. Generated paths remain local, not shared on GitHub. Automatic updates do not refresh these outputs or launch tasks; regenerate explicitly from reviewed tools after a setup change.

For direct terminal use:

```powershell
Set-Location -LiteralPath 'YOUR ACTUAL MOD REPOSITORY'
codex.cmd login status
codex.cmd --cd . --sandbox workspace-write --ask-for-approval on-request --search --no-alt-screen
```

## Desktop handoff limits

Explicit team setup now adds a separate [saved-chat workspace](SAVED-CHATS.md) using supported CLI resume, with private local metadata, refresh and browse tasks. It does not import history into another agent's sidebar or move desktop monitors. Use -SkipChatWorkspace to omit it.

Skills, shell tools, Git/GitHub CLI, vanilla API research and configured MCP servers are portable. Desktop-only browser/UI bridges, Pages/side panels, app thread-management tools and heartbeat scheduling are not assumed available in the CLI. Inspect actual capabilities. Native web research uses --search; account-changing browser work needs a separately verified browser integration.

Preserve private chat/session history. Resume compatible sessions offered by codex resume, or use a concise local handoff describing files, pending work and evidence. Keep an active desktop monitor running until an equivalent CLI-compatible scheduler has been configured and tested. Changing the default editor does not migrate an automation host. This remains a stated migration gap, not a claim that the monitor runs inside VS Code.

Further official references: [Codex CLI reference](https://learn.chatgpt.com/docs/cli/reference), [Codex IDE settings](https://learn.chatgpt.com/docs/ide/settings), [VS Code tasks](https://code.visualstudio.com/docs/debugtest/tasks).


Team setup automatically installs **All Existing Chats** inside the Codex sidebar,
using your own local history. See [sidebar setup, privacy and recovery](CHAT-SIDEBAR.md).
Use `-SkipChatSidebar` to omit it; settings and histories are preserved.
