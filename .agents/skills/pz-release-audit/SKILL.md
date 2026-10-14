---
name: pz-release-audit
description: Check a Project Zomboid Lua mod's release packaging, metadata, translations, case sensitivity, and test evidence.
---
Inspect canonical project VERSION/current mirrors, mod.info, expected source-to-staging layout, dependencies, translations, Linux filename casing, Workshop description line breaks, release notes, unwanted development artifacts, and available source/staging/ZIP hash checks. Runtime content/dependencies must be Lua-only: reject custom Java/JAR/agent/injected-class requirements. Run the project's existing version checker; --release requires authorized existing artifacts. Version mismatch blocks G8. Gameplay requires dedicated G7 PASS before G8. Report pass/fail/untested per gate; packaging success is not gameplay verification. Auditing does not authorize packaging, deployment or publication.

## Workshop test distribution exception
Apply the Workshop MP testing policy in global AGENTS.md and installed hub docs/WORKSHOP_MP_TESTING.md. Missing dedicated MP evidence alone does not block an explicitly authorized labelled Workshop test upload. G7 remains NOT TESTED / BLOCKED and stable-release G8 remains BLOCKED; offline/authority/security/version/package failures still block upload. This skill does not itself authorize publication.
