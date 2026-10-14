---
name: pz-debug-root-cause
description: Diagnose Project Zomboid Build 42 Lua mod bugs from console logs, reproducible symptoms, source and runtime evidence; implement root-cause fixes with regression coverage.
---

# Project Zomboid root-cause debugging

Use this skill when the user reports a crash, stack trace, missing UI action, desync, broken persistence, performance regression, or other mod defect; or asks to debug, investigate, or fix a failure.

## Evidence intake
1. Identify the exact target mod, Build 42 game version, mod version, SP/client/dedicated-server context, reproduction steps, and expected versus actual behavior. Read project `AGENTS.md`, `README.md`, current `mod.info`, tests and relevant source before editing.
2. Check the most recent relevant `the verified developer-local console.txt` when available, but do not assume it covers the failure. For MP, use `pz-dedicated-server-sftp` to retrieve remote server logs when configured, and inspect affected client logs as appropriate. Never silently treat old logs as current evidence.
3. Capture timestamp, exception, full stack trace, affected file and line, call chain, and any preceding warnings. Separate primary failure from secondary cascading errors. Redact credentials, identifiers, and personal information in shared diagnostics.
4. Correlate logs with authoritative source, installed runtime APIs, initialization/load order, mod conflicts, nil handling, event registration, state transitions and multiplayer authority. Check Linux case sensitivity when relevant.

## Diagnose before changing code
5. State at least one falsifiable root-cause hypothesis and the evidence supporting or contradicting it. Distinguish confirmed root cause from plausible inference. If evidence is insufficient, propose the smallest instrumented reproduction or runtime probe.
6. Prefer the smallest architectural fix that restores intended behavior; do not hide exceptions with broad `pcall`, silently skip failures, add arbitrary delays, or patch symptoms without understanding the cause.
7. Remain Lua-only; never introduce custom Java, injected classes, bytecode patches, or native extensions. Validate Lua APIs against the locally installed Build 42 runtime/source rather than guessing.

## Regression and validation
8. Add a focused regression test or deterministic repro harness that fails before the fix and passes afterward where feasible. Include nil, duplicate event, stale network message, and restart/reconnect cases when relevant.
9. Run targeted syntax/static tests, then relevant broader regression tests. For multiplayer defects, separately examine server authority, client synchronization, persistence and headless behavior; do not call MP verified without a real dedicated-server test.
10. If runtime validation is unavailable, label the result STATIC PASS / RUNTIME UNVERIFIED. Never infer in-game success from code inspection, mocked tests or log silence.
11. Do not `deploy`, `publish`, launch the game/server, or edit unrelated mods unless the user separately authorizes that action.

## Required handoff
Report: symptom and reproduction; evidence/log references; confirmed root cause or remaining hypotheses; exact changed files and rationale; tests run and outcomes; unresolved risks; precise SP/MP reproduction steps needed to validate. If blocked, explain the missing evidence and next diagnostic step rather than inventing success.
