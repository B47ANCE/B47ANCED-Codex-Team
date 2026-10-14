---
name: pz-deploy
description: Deploy the latest Project Zomboid mod development build to the verified local single-player mods folder when the user says deploy.
---
Follow the `deploy` command contract in `%USERPROFILE%/.codex/AGENTS.md` and the target project's instructions. Prefer established project scripts, build from authoritative working source, verify target identity and folder structure, copy only owned files to `the verified developer-local SP mods directory`, verify resulting files, and report the result. Include intended uncommitted changes. Do not create/require custom Java/JAR/native runtime components. Never upload to Steam or launch the game. If the target mod is ambiguous, ask which one before copying.
