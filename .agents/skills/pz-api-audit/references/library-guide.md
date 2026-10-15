# API catalog and audit memory

`api-library.json` is a small curated evidence index, not an exhaustive API dump. Search only relevant symbols. Three initial records describe vanilla Mod Selector call forms from Steam build 25485521; full engine version is explicitly UNKNOWN and runtime is NOT_TESTED.

## Record contents

Each record identifies `api_library`, `receiver_type`, `symbol`, `signature`, `signature_scope`, `game_version`, `steam_build`, `side`, `returns`, `mutation`, `status`, `runtime_status`, `verified_on`, `evidence` and `notes`. Unknown facts must be written as UNKNOWN instead of guessed. A signature can be only an observed call; do not infer optional arguments or overloads.

Evidence entries contain a `kind`, portable relative `path`, source/evidence-file `sha256`, inclusive `lines` and a short original `statement`. Kinds: vanilla_lua, official_docs, native_inspection, offline_test, sp_runtime or dedicated_runtime. For official docs, cite the URL in the statement and fingerprint a portable saved evidence note; do not archive entire copyrighted manuals. For runtime, fingerprint a project-owned non-private evidence summary and state environment/scenario in its statement. Do not include source bodies or private logs.

`status` is VERIFIED, INFERRED or UNKNOWN. VERIFIED describes only the stated claim. Native inspection alone cannot be VERIFIED as Lua exposure. `runtime_status` is NOT_TESTED, SP_VERIFIED or DEDICATED_MP_VERIFIED; runtime claims need corresponding runtime evidence, not a source/offline hash. The validator checks structure/consistency; authors must still verify the truth and scope of claims.

The record identity is API library + receiver type + symbol + observed/documented signature + execution side + game version + Steam build. Preserve prior-build records. A changed build invalidates reuse until re-audited even if a method name is unchanged; matching source hashes do not verify hidden native implementation behavior. Unknown full game version is reported alongside a build match.

## Helper commands

Use the developer's Python interpreter; replace placeholders with verified local paths. No command launches or loads PZ.

```powershell
python <skill-folder>/scripts/api_library.py validate
python <skill-folder>/scripts/api_library.py search --symbol getIcon --steam-build 25485521 --game-root <game-root>
python <skill-folder>/scripts/api_library.py record --entry <new-record.json>
python <skill-folder>/scripts/api_library.py validate --library <local-draft.json>
```

Create `new-record.json` as one record using the catalog's actual field structure and your own audited facts. Default record storage is the unmanaged per-user `.codex/pz-api-audit/library.local.json`. Search reads both curated and local catalogs unless `--library` selects one explicitly. Local draft results remain labelled local_draft; conflicts are not silently promoted.

Repeat identical writes are idempotent. A different record with the same identity is refused unless deliberately inspected and written with `--replace`; new build/signature identities append without overwriting history. Writes use a lock and atomic replacement. A stale lock is not deleted automatically: check that no writer remains before manual recovery.

To share a verified finding, use `record --entry <record.json> --library <reviewed-team-checkout>/.agents/skills/pz-api-audit/references/api-library.json`, then validate and commit through the normal team workflow. The helper refuses writes inside installed managed skill/hub stores and rejects linked destinations and private absolute paths. Do not bypass the team updater's manifest/drift protections.

Source rechecking uses game-root only for vanilla/native evidence files. Document/runtime evidence stays in its owning project and requires separate inspection. This library never grants authorization to run the game/server or turns a cached entry into a runtime PASS.
