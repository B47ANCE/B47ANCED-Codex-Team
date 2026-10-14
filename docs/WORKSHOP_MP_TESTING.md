# Workshop distribution before dedicated MP testing

Effective 2026-10-14. Workshop upload can be a test-distribution step before clients/server can run the team's dedicated tests. An explicit publish request authorizes the selected existing item's test upload when MP is not yet tested. It does not authorize a new item, visibility change, deployment or server changes. This overrides older MP-before-upload wording only.

Before uploading:

1. Verify canonical version/current mirrors, public GitHub freshness/commit, Lua-only source, server authority, sandbox configuration, IDs, staging, metadata, package integrity, provenance and all applicable offline checks. Failures or unsafe/unresolved authority block upload.
2. Keep G7 BLOCKED / NOT TESTED and stable-release G8 BLOCKED. Never claim MP verified or stable/release-ready status from an upload.
3. Label description and changenote: "MP testing build - dedicated multiplayer NOT TESTED". State known limitations and actual offline/SP evidence; preserve established formatting and attribution.
4. Preserve prior package/provenance and describe recovery limitations. Record version, commit, hashes, Mod ID, Workshop ID and exact game build; never relabel historical evidence.
5. Use established uploader/cached authentication and verify the actual SteamCMD result. This policy document itself authorizes no upload.

After upload, humans test the exact subscribed package: download/install, server startup, client join/rejoin, server validation, synchronization, duplication risks, persistence and restarts. Record exact version/commit/build and actual results. Server launch/restart/deployment requires separate authorization. G7 PASS is required before stable-release G8 approval; changed source needs appropriately scoped retesting.

Upload success proves distribution, not MP correctness. Known failures must remain explicit and evaluated; never silently mark them PASS.
