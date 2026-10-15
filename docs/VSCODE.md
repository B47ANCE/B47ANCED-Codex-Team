# VS Code with Codex

Explicit Windows team setup installs Microsoft VS Code for the current user when absent, then the official OpenAI Codex extension `openai.chatgpt`. Windows App Installer supplies winget. If winget is unavailable, install VS Code from https://code.visualstudio.com/Download and rerun setup. Existing installations are reused. Settings, keybindings, credentials and unrelated extensions are preserved. Use `-SkipVSCode` with Setup-CodexTeam.ps1 for headless/disposable setup or another editor.

For an already installed team configuration, run only the editor helper from a reviewed repository checkout:

```powershell
& .\tools\Setup-VSCode.ps1
& .\tools\Setup-VSCode.ps1 -CheckOnly
```

Open VS Code, use File > Open Folder to open the actual mod repository, then select the Codex icon (or Command Palette > Codex: Open Codex Sidebar). Sign in with your own ChatGPT account if prompted. Review Workspace Trust yourself. Start a new Codex chat and confirm global instructions and all 23 team skills are discovered. Preserve project AGENTS.md and use the existing user-profile skill store.

Use Explorer, source control, diffs, search and the integrated terminal alongside Codex. Open files and selections can supply editor context. Other extensions do not automatically become Codex tools; desktop-only integrations may differ. Installation verification does not prove authentication or agent activation.

Automatic team updates and rollback install this helper inert and never execute editor provisioning. VS Code and extension updates follow existing editor preferences. Team rollback restores team-managed files, not editor versions. The helper does not change update preferences or launch an editor.

Official references: [Codex IDE](https://developers.openai.com/codex/ide), [official extension](https://marketplace.visualstudio.com/items?itemName=openai.chatgpt), [Windows setup](https://code.visualstudio.com/docs/setup/windows), [VS Code CLI](https://code.visualstudio.com/docs/configure/command-line).
