# Saved local Codex chats in VS Code

Explicit team setup now creates `B47ANCED-Saved-Chats.code-workspace` beside the normal team workspace. Open it in VS Code and choose Terminal > Run Task > Chats: Resume saved chat, then select the chat and owning project. Confirm the chat is idle in its other surface before resuming to avoid concurrent writes. No chat starts during setup or workspace opening.

The picker uses Codex CLI's supported `resume <session-id>` command with existing local history. It is not an import into Copilot, another agent's sidebar or a ChatGPT cloud-chat archive. Existing transcripts, archives and databases are never moved, copied or rewritten by the helper. Once resumed, Codex itself can continue writing its normal session history. Desktop-only integrations and monitor automations remain on their existing host.

## Setup and refresh

Normal `tools/Setup-CodexTeam.ps1` includes the saved-chat workspace after the main CLI workspace. `-SkipChatWorkspace` omits only this feature; `-SkipCLIWorkspace` omits both workspaces. Accounts with no saved sessions get refresh and browse tasks rather than a failing empty picker. After creating chats, run Chats: Refresh saved-chat picker and reopen the workspace if VS Code requests it.

For an existing installation, from your reviewed checkout:

```powershell
& .\tools\Setup-ChatWorkspace.ps1 -Workspace $teamWorkspace
code.cmd --new-window (Join-Path $teamWorkspace 'B47ANCED-Saved-Chats.code-workspace')
```

Use the same `$teamWorkspace` selected during onboarding. Supply `-PythonExe` for a nonstandard runtime. The existing `B47ANCED.code-workspace` must exist first. `CODEX_HOME`, when configured for the current user, selects that user's saved history; explicit isolated HomeDirectory tests use their own .codex. The launcher forwards the chosen history store to Codex and checks session identity before resume. Archived sessions and subagent histories are excluded. Browse all local chats is available independently of the generated list.

## Privacy, preservation and updates

Only first-record session metadata and optional local index titles are read; transcripts and tool output are not exported. Titles, identifiers and paths remain private local metadata under the selected Codex home `cli-chat-runtime`, and in the generated workspace. Do not commit these outputs or share them with teammates. Each developer discovers their own chats; the package contains no personal chat list.

Owned output hashes protect customized workspaces, scripts and metadata. Explicit refresh backs up changed owned files under `cli-chat-backups`; drift blocks replacement. The older manually generated `B47ANCED-Chats.code-workspace` is preserved independently; the package uses the new Saved-Chats name and runtime folder to avoid overwriting it. Use the new workspace going forward.

Automatic sign-in updates install new helpers inert. They never scan history, refresh private outputs, start agents or open VS Code. After reviewing an updated package, rerun explicit setup/Setup-ChatWorkspace to refresh local outputs. Team rollback restores managed package files, not private chat history or developer-local workspace/runtime copies; keep their backups if restoring those manually. Missing or incompatible sessions should be continued using a local handoff rather than editing session databases.

Source: [official Codex CLI documentation](https://learn.chatgpt.com/docs/codex/cli). Installation and metadata validation do not prove an interactive resume succeeded; verify the selected history and available tools in the new session.


Team setup automatically installs **All Existing Chats** inside the Codex sidebar,
using your own local history. See [sidebar setup, privacy and recovery](CHAT-SIDEBAR.md).
Use `-SkipChatSidebar` to omit it; settings and histories are preserved.
