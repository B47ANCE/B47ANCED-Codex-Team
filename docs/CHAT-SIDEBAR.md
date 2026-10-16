# Existing chats in the Codex sidebar

Normal `Setup-CodexTeam.ps1` now installs `b47ance.codex-chat-sidebar` alongside
`openai.chatgpt`. Open the Codex sidebar and expand **All Existing Chats**.
Each developer sees their own local primary chats, including original names and
history references. No export from another developer or terminal picker is needed.
Selecting a row asks the official extension to open that existing conversation;
it does not send a prompt. Setup does not launch VS Code or resume chats.

## Existing installations

After downloading and reviewing the latest team package, run:

```powershell
& ./tools/Setup-ChatSidebar.ps1
& ./tools/Setup-ChatSidebar.ps1 -CheckOnly
```

Python is discovered from your own installed team bootstrap. Fresh clone/ZIP
users simply follow [team onboarding](TEAM-ONBOARDING.md); no additional step is
needed. `-SkipChatSidebar` opts out of main setup; `-SkipVSCode` also skips it.
The saved-chat terminal workspace remains a separate optional fallback.
Background/sign-in updates install helpers inert; they never install extensions,
scan histories or launch an editor. After such an update, explicitly run the
reviewed setup above to upgrade the companion.

## Privacy and compatibility

The companion reads `state_5.sqlite` in inherited `CODEX_HOME`, otherwise the
current user's `.codex`. SQLite is opened read-only with query-only enforcement.
Archived/subagent chats and missing history files are excluded. Transcript
contents, credentials and environment secrets are never read or packaged.
An empty profile shows an empty list. A schema/read error is shown in the view
and Output > Codex Existing Chats; it never triggers a database migration.
Remote, WSL and different-user histories are separate and are not imported.
Use the same local Windows user/profile in VS Code as in the desktop app.

Requires Python 3.11+, VS Code 1.106+ and the official extension. Its view container
IDs and existing-chat URI route are compatibility dependencies and may change.
The live predecessor was verified with VS Code 1.142.0 / openai.chatgpt
26.1007.21434 and 18 existing chats. This is a companion Tree View, not a
replacement for the official extension's internal recent-chat widget. Native
conversation rendering after clicking a row still needs developer confirmation;
list visibility is independently verified by local runtime-status.json.

The original JavaScript source is an embedded template in
`tools/build_chat_sidebar.py`, allowing existing trusted validators to accept
updates without expanding executable file-type policy. Explicit setup builds a
VSIX offline using Python's standard library; npm/Marketplace publishing is not
involved. Only a developer-local Python path enters generated runtime.json.
Generated packages stay in `.codex/chat-sidebar-build` and must not be committed.
Existing VS Code settings, official extension files and chat stores are untouched.
Disable or uninstall only `b47ance.codex-chat-sidebar` to remove the list; chat
history is preserved. Older generated VSIX files remain available for recovery.
