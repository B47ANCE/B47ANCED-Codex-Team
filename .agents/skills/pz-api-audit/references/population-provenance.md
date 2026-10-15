# Audit population provenance — 2026-10-14

Historical population baseline (13.4.1): 93 shared records: three original Mod Selector observations and 90 observations populated from existing team-project audits. Initial status totals: **23 VERIFIED, 52 INFERRED, 18 UNKNOWN**. These initial counts are historical; [the subsequent deep review](deep-review-25485521.md) records the current **71 VERIFIED, 21 INFERRED, 1 UNKNOWN** and the scope of those labels. All are runtime **NOT_TESTED**, Steam build **25485521**, full engine version **UNKNOWN**.

VERIFIED means only the stated source observation: the original three Mod Selector calls, fourteen named global/static call-site observations and six manually reviewed findings. It does not prove complete signatures, native overload choice, state authority or runtime correctness. INFERRED means the same method short name occurs in installed Lua but its receiver/type or historical behavior is unresolved. UNKNOWN means a bounded Lua scan did not find an executable call site; it does not prove absence or inaccessibility.

## Coverage

The local population audit inventoried 115 immediate audit-like Markdown/JSON files in docs/ and research/ across 24 repository folders, including duplicate Medical Checks companion checkouts. This is not an exhaustive engine or project-document audit. Imported names retain up to six originating audit fingerprints. External-mod reports, historical bridge proposals and templates were inventoried separately, not adopted as current API authority. No raw game/decompiled source, private logs or developer paths are included.

The six manually reviewed findings cover farming month conversion, debug day display, daysInMonth arguments, plant watering state/saveData and the crafting OnCreate/consumption call order. Historical 42.20.3 prose is not current proof; current claims cite installed Lua paths, inclusive lines and SHA-256 hashes. Fourteen other VERIFIED records establish only named global/static call presence. Placeholder signatures must not be copied as real calls.

## Installation and runtime limits

353 historical relative-path/SHA pairs were compared with loose files and JAR members. Sixteen pairs matched packaged classes but differed in loose files. Packaged and loose animal classes also differ. These observations establish modified-installation uncertainty, not clean vanilla runtime behavior. No class modification, Java runtime dependency or bridge is authorized. Historical 42.21 attribution was not independently decoded in the population pass, so game_version remains UNKNOWN.

Project audit evidence paths beginning projects/ resolve beneath the developer-selected mod repository root. The referenced audits remain in their owning repositories and are not distributed here. A fingerprint without its file is not independent evidence. Installed Lua evidence is resolved beneath --game-root by the helper. Source hash matches do not validate audit prose, authority, persistence or dedicated MP. Different builds require re-audit even when names match.

## Reuse on another developer machine

Discover the local Steam build and game root, then search only relevant symbols:

```powershell
python <skill-folder>/scripts/api_library.py search --symbol water --steam-build <installed-build-id> --game-root <verified-game-root>
```

Do not assume build 25485521 is installed elsewhere. STALE_BUILD, STALE_SOURCE and missing project evidence require investigation. Keep local research in the unmanaged local draft; identical promoted records may appear as both curated and local_draft in combined searches. Shared updates deliberately preserve that draft. Use --library <skill-folder>/references/api-library.json for shared-only results. No offline check establishes SP or dedicated MP verification; release gates remain unchanged.
