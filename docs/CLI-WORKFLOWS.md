# Team workflow map for Codex CLI in VS Code

Open B47ANCED.code-workspace, run the Codex CLI project task and select the repository that owns the work. Its AGENTS.md and existing source/version/layout are authoritative. All 23 global team skills are reused; none are copied into project folders.

| Work | CLI prompt or task | Relevant existing skills |
|---|---|---|
| Start, freshness and organization | Start CLI; request the repository preflight and bounded audit | pz-repository-startup, pz-repository-hygiene, pz-repository-governance |
| API and game updates | Audit APIs against the installed build; record evidence through the library helper | pz-api-audit, pz-build42-compatibility |
| Workshop research | Inspect authorized downloads read-only; retain neutral findings and provenance | pz-clean-room-research |
| Multiplayer | Audit authority, synchronization, reconnects and dedicated evidence | pz-mp-audit |
| Saves and migration | Design/test disposable persistence fixtures and rollback | pz-persistence-and-migration |
| Items and inventory | Implement scoped features with sandbox configuration and verification | pz-item-and-recipe-development |
| Interfaces | Develop localized vanilla-aligned UI/context menus | pz-ui-ux-development |
| Original art and animation | Use verified Blender/Meshy integrations and original editable assets; approve paid jobs individually | pz-2d-asset-pipeline, pz-3d-asset-pipeline, pz-character-animation |
| Compatibility and bugs | Investigate symptoms and installed evidence; preserve runtime labels | pz-mod-compatibility, pz-debug-root-cause |
| GitHub and docs | `commit` after authorized changes; follow branch/docs/secrets/tests/push rules | pz-github-versioning, pz-ci-automation, pz-security-permissions |
| Release checks | Audit packages, identity, versions, translations and case safety | pz-release-audit |
| Local SP installation | Explicit `deploy` for the selected mod after checks | pz-deploy |
| Workshop upload | Explicit `publish` for the selected existing item after required gates | pz-publish |
| Dedicated diagnostics | `server-debug` or `check server logs`: verified read-only SFTP only | pz-dedicated-server-sftp |
| Retention | Propose a bounded plan; deletion needs explicit authorization | pz-artifact-retention |

Tasks expose routine checks/helpers without inventing a generic build/test command. Run the project's documented validation from its terminal or ask Codex to inspect the current commands. The version task runs only an existing scripts/check_versions.py. Do not run third-party production/gameplay code simply to discover what it does.

All Lua-only, server-authority, sandbox, SemVer, clean-room, docs and G7/G8 rules still apply. Workspace launch does not authorize game/server launch, deployment, Workshop upload, SFTP writes or paid Meshy operations. Request those actions explicitly in the selected project's CLI session. Static checks and editor previews are not dedicated MP evidence.

Updates and rollback remain the validated Windows helpers. Workspace tasks offer update check/apply and rollback preview; actual rollback uses reviewed Restore-CodexTeam.ps1 per onboarding. Sign-in updates remain an independent Windows scheduled task and need no desktop chat window.

Desktop heartbeat jobs remain hosted by the app until a separately configured and verified scheduler replaces them. Do not drop pending download audits during the editor change. Local handoffs should list IDs, report paths, completion checks and exclusion boundaries without embedding third-party code/assets or credentials.
