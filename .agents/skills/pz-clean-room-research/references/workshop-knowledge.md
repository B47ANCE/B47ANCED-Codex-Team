# Portable Workshop research knowledge map

## Provenance and boundaries

Historical local research snapshot: 585 installed folders, 573 included for bounded static knowledge triage, 12 excluded for Java/custom-native components or direct/transitive ZombieBuddy requirements. The original 182 pending downloads and 12 animation leads were complete; two late items and six changed included items were reviewed separately. An excluded metadata update remained excluded. These are snapshot counts, not a claim that another developer has the same subscriptions or files.

Useful observations prompted independent checks of vanilla build 25485521. Shared API evidence records portable source paths, inclusive lines, SHA-256 and narrow claim scopes; no raw game or mod bodies are included. Full engine version UNKNOWN; SP and dedicated runtime NOT_TESTED. Source hashes do not prove semantic correctness, performance, authority or security. Unknown licenses block copying, not independent research. Code, assets, UI text, distinctive algorithms/architecture and documentation imported: NONE.

## UI

Research themes: state-aware context menus, input handling, localization and layout. Start from verified vanilla ISContextMenu declarations, not another mod's menu structures. Specify eligibility and disabled reasons independently; test focus, controller/keyboard, resizing, stale selections and display categories. Keep category presentation distinct from authoritative inventory transfer logic. Late research lead: [Extended Categories - Better Hoarding!](https://steamcommunity.com/sharedfiles/filedetails/?id=3650035249), declared author Kechna, version 1.9.0, permissions UNKNOWN; taxonomy, labels and item lists are not imported.

## Authority

Command/event occurrence only identifies a possible boundary. Trace actor identity, execution side, request validation, state owner, rate/duplicate handling, synchronization and permissions against vanilla evidence. A file in shared/ or OnServerStarted registration is not an authority or headless-safety guarantee. Test remote observers, malicious/stale requests, reconnect and dedicated restart before gameplay acceptance.

## Persistence

Research themes: object lifecycle, mod data, world objects and migrations. Select ownership and serialization from the owning project's requirements. Verify nil/absent state, initialization order, bounded writes, load/unload and repeated reload/migration, using disposable fixtures. A save-related symbol or S/CGlobalObjectSystem declaration does not establish replication, global availability or save durability.

## Items

Research themes: sandbox configuration, item/recipe definitions, loot lifecycle, fluids, vehicles, animals and localization. Separate Mod ID, item identity, display categories, script definitions and actual instances. Verify recipe consumption/output callbacks and fluid receiver types before implementation. preAddCatDefs is a foraging category hook, not an animal-cat event. Build independent recipes, values and tables; do not reuse another mod's balancing data.

## Compatibility

Treat require as a dependency; ordering and incompatibility metadata are separate constraints. Traverse required dependencies conservatively; reject confirmed Java/native or ZombieBuddy dependencies and flag dynamic/ambiguous cases UNKNOWN. Verify current manifests and stable files, not merely installed folders. Preserve old research when source fingerprints change and refresh changed items instead of relabelling history.

Late research lead: [Item Arrange Extension](https://steamcommunity.com/sharedfiles/filedetails/?id=3813943783), declared author Kechna, version 1.13.0, permissions UNKNOWN. Its required ItemArrange ID resolved in the local snapshot; custom methods are not vanilla APIs. Independent model-presentation work must verify native APIs, measure our own original assets and test scale, rotation, collision and state ownership. No geometry profiles, transforms or support tables are imported.

## Animation, rendering and scheduling

For the 12 animation leads, use [animation contracts](../../pz-character-animation/references/animation-contracts.md). For scheduled/scanning work, define bounded event-driven updates and invalidation from our own requirements; source counts are not benchmark evidence. Rendering visibility does not prove network state. Models/rigs/clips must be original, with Codex authoring all rigging/animation through Blender/local tools; Meshy is limited to approved static assets.

## Promotion checklist

Keep only neutral requirements, vanilla extension-point evidence and independent acceptance questions in shared skills. Each promoted API needs a scoped receiver/signature/side/build, portable fingerprint and preserved UNKNOWN/INFERRED/NOT_TESTED fields. Recheck evidence on the teammate's installation. Do not sync local drafts wholesale, private reports, logs, absolute paths or third-party implementations. Clean-room reviewer signoff remains required before merging research-related PRs; a successful CI run is not that signoff or runtime proof.
