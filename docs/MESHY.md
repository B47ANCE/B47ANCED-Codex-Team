# Meshy MCP for Codex CLI and VS Code

Explicit Windows team setup configures the official Meshy server globally, alongside VS Code and the official Codex extension. Each developer uses their own credentials. This integration is a development tool, not a dependency shipped with a Project Zomboid mod.

## Prerequisites and install

Install a supported [Node.js LTS](https://nodejs.org/en/download) release (Meshy requires Node 18+), Python 3.11+ for the additive TOML validator, and the official Codex CLI:

```powershell
npm.cmd install -g @openai/codex
node --version
npm.cmd --version
npx.cmd --version
codex.cmd --version
```

Review the team checkout, then use normal Setup-CodexTeam.ps1. It includes both integrations by default. Use `-SkipMeshy` and/or `-SkipVSCode` for headless setup or developers who do not want those integrations. The base team installer still supports Python 3.10; Meshy provisioning requires 3.11+.

For an existing team installation, run only:

```powershell
& .\tools\Setup-Meshy.ps1
& .\tools\Set-MeshyApiKey.ps1
& .\tools\Setup-Meshy.ps1 -CheckOnly
python .\tools\test_meshy_connection.py --balance
```

Supply `-PythonExe` to Setup-Meshy.ps1 when Python is not on PATH. Use that same interpreter instead of `python` in the probe command. Setup verifies Node, npm, npx and Codex before changing the config. The official documented npx method installs `@meshy-ai/meshy-mcp-server@0.6.4` into npm cache on first MCP start. Explicit setup runs the probe to warm that cache and discover tools, without API calls. Internet access is required on that first start. CheckOnly validates prerequisites and configuration without downloading or calling the API; run the separate probe with --balance for live API verification.

## Authentication and scope

Create a Meshy API key in your own [Meshy developer account](https://www.meshy.ai/developers/keys). The masked local PowerShell prompt stores it in the Windows user environment as MESHY_API_KEY. This environment store is accessible to processes running as your account; it is not an encrypted secret vault. No key is placed in command arguments, chat, team files or Codex TOML. Existing user keys are preserved. Do not run the key prompt in a recorded screen-sharing session.

The per-user PowerShell launcher loads MESHY_API_KEY from the Windows user environment when the parent process has not inherited it. Restart the Meshy MCP server or start a new Codex session after first setting a key. Existing process-level keys take precedence. The MCP entry forwards only the variable name through `env_vars`. It is appended to the existing user config (`CODEX_HOME` when explicitly set, otherwise the selected user's .codex directory). Existing config bytes are retained, parsed values are checked, and a local backup precedes the atomic write. An existing differing Meshy entry or customized local launcher blocks changes instead of being replaced. Unrelated integrations and project files are preserved. Avoid committing your global config or integration backups.

Open a new Codex CLI or Codex VS Code extension session and inspect `/mcp`. Codex's extension uses the global Codex MCP configuration; VS Code's separate built-in MCP feature is not configured here. The server runs through PowerShell/npx on Windows, with a neutral per-user working directory so repository .env files are not loaded. The reviewed launcher is copied locally during explicit setup; automatic team updates do not replace it. Node must remain on the environment PATH inherited by Codex.

## Paid operations and supported tools

The server supports text-to-3D, image-to-3D, multi-image-to-3D, task status, model downloads, remeshing, format conversion, rigging and animation. The verifier checks discovery; it does not submit generation, remesh, conversion, rigging or animation jobs. Those operations can consume credits, including conversion.

All 28 tools are exposed. The global server entry sets `default_tools_approval_mode = "prompt"`, and team policy requires explicit user approval before each credit-consuming job. Tool access is not spending authorization. Balance/discovery tests do not authorize any generation. Do not switch paid tools to automatic approval or interpret a previous job approval as unlimited spending. Customized Meshy settings are preserved and require manual review rather than being reset.

`test_meshy_connection.py --balance` performs MCP initialization, tools/list and only meshy_check_balance (a free GET). It prints tool names and balance fields, suppressing raw errors and key material. A missing key, network failure or API rejection is a failed live check. Tool discovery can pass without authentication; it does not prove API connectivity. Usage listing can require a Studio/Enterprise team; it is not called during setup. No model is generated, downloaded or converted during verification.

## Asset skills

Use `pz-3d-asset-pipeline` for geometry/materials/export and `pz-character-animation` for skeletons, retargeting and clips. Both use [one shared Meshy MCP reference](../.agents/skills/pz-3d-asset-pipeline/references/meshy-workflow.md), preserving the existing 23-skill set. It covers paid-job approval, task recovery, verified downloads and Blender/PZ validation. API humanoid rigging and web-app quadruped rigging are distinct; animal MCP compatibility is not assumed. Official vendor generation skills currently use a separate CLI and are references, not automatically installed competing integrations.

## Updates and removal

Automatic team updates install these helpers inert and never execute provisioning or prompts. The server version is pinned; package upgrades require an explicit reviewed setup change. Team rollback restores managed team files, not local MCP config, npm cache, software or environment keys. If you need to remove only Meshy, use `codex.cmd mcp remove meshy` and verify other integrations remain. Review local integration backups before any restore; do not overwrite newer unrelated settings with an old whole-file backup. Keep or remove your user environment key yourself as appropriate for other Meshy clients.

Sources: [official Meshy repository](https://github.com/meshy-dev/meshy-mcp-server), [official Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp), [Codex CLI](https://developers.openai.com/codex/cli).
