# Fluid API resolution — 13.4.4

For an InventoryItem's attached FluidContainer, the source-supported Lua query is **getAmount()**, after checking that the component exists:

```lua
local fluid = item and item:getFluidContainer()
local storedAmount = fluid and fluid:getAmount() or nil
```

This is a read example for a known item receiver. Zero means an empty component; nil means no component. Preserve that distinction. The packaged getter refreshes caches then returns amountCache; shipped UI formats amount times 1000 as mL. This is component storage, not an external supply, permission decision, fluid transfer transaction or runtime guarantee.

**IsoObject:getFluidAmount() is a different supported API.** The packaged source checks sprite/source conditions, infinite water (10000.0 sentinel), external-source delegation, component storage, reserve water and puddles. Do not replace it with component getAmount when source availability matters. Queries can involve cache/discovery side effects. The available loose IsoObject class has different instructions; this audit does not prove equivalence or effective process behavior.

## The original conflict

Installed ISInventoryPane.lua and ISInventoryPaneContextMenu.lua call getFluidAmount on a value returned by getFluidContainer. The packaged FluidContainer/Component hierarchy has no such method/interface/default method/annotation alias, whereas its getAmount is a public exposed source route and IsoObject has getFluidAmount. The component getFluidAmount record stays UNKNOWN. This is a confirmed source/API mismatch, not a reproduced runtime failure. The game/third-party files were not changed and no shim, reflection, Java code or metatable monkey patch was introduced.

## Local mod scan

The [source/usage evidence](fluid-resolution-25485521.json) inventories local Lua paths and fingerprints. Only Quartermaster had production getFluidAmount references: NativePort.lua once and BuildingNative.lua twice. Their receivers are selected world objects with getSquare/getFluidContainer and world-source checks, not fluid components. Those comparisons intentionally reject indirect/infinite sources when finite component storage is required. One matching test fixture models the world-object method. No confirmed invalid FluidContainer caller was found; no mod code was changed. waterWorks, groundWorks, CATConstruction and Quartermaster already use component getAmount in inspected adapters/actions. A broad getAmount name match elsewhere can refer to recipe/resource quantities and is not proof of fluid usage.

The scan covers the selected local mod root, including source/mirrors, prototypes and tests; it excludes research, docs, archived/generated trees and hidden worktrees. Dynamic concatenated method names, remote code and unscanned copies are not exhaustively proved absent. Quartermaster is dirty on an upstream-current feature branch; the three legacy component consumers lack Git metadata. These are local snapshots, not claims about remote main. No unsafe edits were needed or performed.

## Evidence status

Current library: 94 records, 93 VERIFIED source observations/routes and one UNKNOWN component conflict. Steam build 25485521; full engine version UNKNOWN. All runtime statuses remain NOT_TESTED. Source method semantics, Lua exposure and observed callers are separate evidence layers. No transfer/consumption, synchronization, authority, persistence, SP or dedicated MP guarantee was promoted. Gameplay configuration/release gates remain unchanged.
