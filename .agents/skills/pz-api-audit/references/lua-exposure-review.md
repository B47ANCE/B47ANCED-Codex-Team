# Lua exposure follow-up — 13.4.3

All 21 previously inferred entries now have VERIFIED **source exposure routes**: 19 class-based methods and two annotated global file helpers. The 93-record catalog has 92 VERIFIED source observations/routes and one UNKNOWN. This does not mean 92 successfully invoked or safe gameplay APIs. Every runtime status remains NOT_TESTED; full game version remains UNKNOWN, Steam build 25485521.

## Evidence and scope

The [reviewed static-analysis summary](lua-exposure-25485521.json) fingerprints the packaged initializer, exposer and Kahlua method exporter, class-registration offsets, exact public/static flags and method annotations. It is original analysis, not copied game source/bytecode. The exporter registers public nonstatic instance methods and public static class functions unless HiddenFromLua, using reflected names. The two file helpers have explicit global LuaMethod annotations consumed by the global exporter. These conclusions trace binding construction, beyond native signature presence. No Java or Lua game classes were loaded or invoked.

Source binding construction is conditional on successful normal initialization and the inspected packaged implementation. Namespace collisions, modified loose classes, injected transformations, receiver existence/lifetime, argument conversion, overload selection, return usability, authority, persistence and MP behavior remain untested. Existing API-specific warnings are preserved. Class registration does not authorize activity interception, native field access, reflection, Java bridges, unsafe XP restoration or installed-mod file writes.

getServerTimeMills is a static GameTime binding; it is not a bare global. getModFileWriter and getCurrentSaveName are annotated globals. Other entries describe instance methods, except ModData.request, which is a static class binding. getOwner returns a connection candidate, not an authorization decision. Setter and thump bindings are not approved mutation designs. Existing sandbox, authority and dedicated MP gates remain unchanged.

## Fluid conflict

FluidContainer and Component declare no getFluidAmount method, implement no interfaces providing it, and have no method annotation alias supplying that name. The inspected public-method exporter uses reflected names rather than inventing that alias. Packaged FluidContainer.getAmount exists, while IsoObject.getFluidAmount is a separate surface. Shipped ISInventoryPane.lua still calls the conflicting expression. Thus the catalog entry remains UNKNOWN: no packaged binding was found for that receiver. This is not an actual runtime failure diagnosis, universal absence proof, or authorization to replace calls blindly. Computed/injected runtime table changes are outside this static audit.

## Evidence labels

The offline_test summary is a reviewed static analysis, not an executed gameplay test. Native JAR evidence is still separately fingerprinted with the documented binary line sentinel. The previous 71 VERIFIED entries retain their previous scopes; the 21 refinements use signature_scope verified_source_exposure_route. All invocation, SP and dedicated runtime evidence remains NOT_TESTED. Local historical drafts are preserved separately; select the installed curated library explicitly for current shared-only results.

## Routes

| Symbol | Export route | Source binding |
| --- | --- | --- |
| getTotalPowerUsing | instance_method | receiver:getTotalPowerUsing |
| getServerTimeMills | static_class | GameTime.getServerTimeMills |
| getModFileWriter | annotated_global | getModFileWriter |
| getCurrentSaveName | annotated_global | getCurrentSaveName |
| setAge | instance_method | receiver:setAge |
| getOwner | instance_method | receiver:getOwner |
| doSprinter | instance_method | receiver:doSprinter |
| doFastShambler | instance_method | receiver:doFastShambler |
| doShambler | instance_method | receiver:doShambler |
| getSpeedType | instance_method | receiver:getSpeedType |
| makeInactive | instance_method | receiver:makeInactive |
| setFrameSpeedPerFrame | instance_method | receiver:setFrameSpeedPerFrame |
| getEquipParent | instance_method | receiver:getEquipParent |
| getId | instance_method | receiver:getId |
| shouldUpdateInWorld | instance_method | receiver:shouldUpdateInWorld |
| getThumpableFor | instance_method | receiver:getThumpableFor |
| Thump | instance_method | receiver:Thump |
| AddXPNoMultiplier | instance_method | receiver:AddXPNoMultiplier |
| request | static_class | ModData.request |
| setConditionLowerChance | instance_method | receiver:setConditionLowerChance |
| helmetFall | instance_method | receiver:helmetFall |
