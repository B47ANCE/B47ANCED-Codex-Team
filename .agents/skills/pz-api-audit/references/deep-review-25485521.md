Historical 13.4.2 review. [The exposure follow-up](lua-exposure-review.md) supersedes binding uncertainty only; runtime limits remain.

# Build 25485521 API deep review — 2026-10-14

All 70 previously unresolved records were reviewed. Forty-eight have source-verified contextual receivers and observed call forms; eighteen formerly unknown native methods become INFERRED, three remain INFERRED, and one prior inferred fluid call becomes UNKNOWN. Shared totals are **71 VERIFIED, 21 INFERRED, 1 UNKNOWN**, out of 93. Every runtime status remains **NOT_TESTED**; full engine version remains **UNKNOWN**.

## What was checked

Installed Lua caller context was inspected with exact paths, line ranges and SHA-256 fingerprints. A read-only class-file parser inspected metadata in 5,095 packaged zombie classes without loading/executing game classes. Selected public method descriptors, inheritance chains, packaged class hashes and available loose-class method metadata are preserved in [the native evidence summary](native-metadata-25485521.json). No game implementation/source bodies are distributed.

VERIFIED applies only to each stated caller/receiver/source observation. It does not prove native implementation behavior, overload dispatch in a running game, side authority, nullability, persistence, transaction atomicity, synchronization or MP acceptance. Side denotes the source folder. Shipped debug/test callers are explicitly identified and were not executed. Native-only signatures remain INFERRED even when public. A native descriptor is not a Lua invocation recipe.

Initial same-name references included unrelated food age, inventory weight, fluid-panel ownership, model attachment ID, resource-input amount, debug floor helper and vehicle-part condition. Those are replaced by relevant callers or explicitly unresolved native candidates. Records retain originating project audit fingerprints; historical behavior claims are not promoted wholesale. The unchanged Git parent preserves the prior catalog.

## Conflicting fluid evidence

ISInventoryPane.lua calls item:getFluidContainer():getFluidAmount(). Packaged GameEntity.getFluidContainer returns FluidContainer. The inspected FluidContainer superclass chain has no getFluidAmount method, while packaged IsoObject defines it. Installed fluid UI uses FluidContainer.getAmount. The getFluidAmount record is UNKNOWN, not API availability proof, and no universal source substitution is authorized. Loose overrides/injected process transformations may differ; no game process was examined or launched.

## Remaining inference

AnimalData.setAge is not proved by the old food setter reference; the animal UI uses a command/setAgeDebug route. IsoZombie.getOwner is not the fluid-panel owner. SafeHouse.getId is not a model attachment ID. Other native-only leads include zombie speed/activity setters, frame-speed setter, generator power-use getter, static GameTime.getServerTimeMills, file helpers, getEquipParent, shouldUpdateInWorld, thump interfaces, XP multiplier helper, ModData.request, clothing condition chance and helmetFall. Their records identify precise native candidates while leaving Lua invocation and behavior unresolved. Commented frame-speed text is not an active call.

Metadata evidence is pinned to the whole JAR SHA-256; [1,1] is a binary sentinel, not an invented text line. The companion summary distinguishes missing loose files from differing loose bytes and records receiver ancestry. Neither packaged metadata nor matching source files certify a clean/effective runtime. Known class overrides remain untouched. No custom Java, bridge, game/server launch, deployment or Workshop publication was introduced. SP/dedicated gates are unchanged.

## Per-record disposition

| Symbol | Previous | Current | Receiver/call scope |
| --- | --- | --- | --- |
| getMonth | INFERRED | VERIFIED | zombie.GameTime |
| getYear | INFERRED | VERIFIED | zombie.GameTime |
| getDay | INFERRED | VERIFIED | zombie.GameTime |
| daysInMonth | INFERRED | VERIFIED | zombie.GameTime |
| getWorldAgeHours | INFERRED | VERIFIED | zombie.GameTime |
| getTotalPowerUsing | UNKNOWN | INFERRED | zombie.iso.objects.IsoGenerator |
| getServerTimeMills | UNKNOWN | INFERRED | zombie.GameTime |
| getModFileWriter | UNKNOWN | INFERRED | zombie.Lua.LuaManager$GlobalObject |
| getCurrentSaveName | UNKNOWN | INFERRED | zombie.Lua.LuaManager$GlobalObject |
| getAge | INFERRED | VERIFIED | zombie.characters.animals.datas.AnimalData |
| setAge | INFERRED | INFERRED | zombie.characters.animals.datas.AnimalData |
| getWeight | INFERRED | VERIFIED | zombie.characters.animals.datas.AnimalData |
| setWeight | INFERRED | VERIFIED | zombie.characters.animals.datas.AnimalData |
| setAttachedPlayer | INFERRED | VERIFIED | zombie.characters.animals.datas.AnimalData |
| getUsername | INFERRED | VERIFIED | zombie.characters.IsoPlayer |
| getOnlineID | INFERRED | VERIFIED | zombie.characters.animals.IsoAnimal |
| getOwner | INFERRED | INFERRED | zombie.characters.IsoZombie |
| doSprinter | UNKNOWN | INFERRED | zombie.characters.IsoZombie |
| doFastShambler | UNKNOWN | INFERRED | zombie.characters.IsoZombie |
| doShambler | UNKNOWN | INFERRED | zombie.characters.IsoZombie |
| getSpeedType | UNKNOWN | INFERRED | zombie.characters.IsoZombie |
| makeInactive | UNKNOWN | INFERRED | zombie.characters.IsoZombie |
| getSpriteDef | INFERRED | VERIFIED | zombie.characters.IsoGameCharacter |
| getFrame | INFERRED | VERIFIED | zombie.iso.sprite.IsoSpriteInstance |
| setFrameSpeedPerFrame | UNKNOWN | INFERRED | zombie.iso.sprite.IsoSpriteInstance |
| isCrawling | INFERRED | VERIFIED | zombie.characters.IsoZombie |
| isDead | INFERRED | VERIFIED | zombie.characters.IsoPlayer |
| UseAndSync | INFERRED | VERIFIED | zombie.inventory.InventoryItem |
| syncItemModData | INFERRED | VERIFIED | zombie.Lua.LuaManager$GlobalObject |
| syncItemFields | INFERRED | VERIFIED | zombie.inventory.InventoryItem |
| getEquipParent | UNKNOWN | INFERRED | zombie.inventory.InventoryItem |
| getAllInputItems | INFERRED | VERIFIED | zombie.entity.components.crafting.recipe.CraftRecipeData |
| luaCallOnCreate | INFERRED | VERIFIED | zombie.entity.components.crafting.recipe.CraftRecipeData |
| processDestroyAndUsedItems | INFERRED | VERIFIED | zombie.entity.components.crafting.recipe.CraftRecipeData |
| getId | INFERRED | INFERRED | zombie.iso.areas.SafeHouse |
| getPlayers | INFERRED | VERIFIED | zombie.iso.areas.SafeHouse |
| getModData | INFERRED | VERIFIED | zombie.characters.animals.IsoAnimal |
| getDeadBodyObject | INFERRED | VERIFIED | zombie.inventory.InventoryItem |
| getStaticMovingObjectIndex | INFERRED | VERIFIED | zombie.iso.objects.IsoDeadBody |
| pickUpCorpse | INFERRED | VERIFIED | zombie.characters.IsoGameCharacter |
| shouldUpdateInWorld | UNKNOWN | INFERRED | zombie.inventory.InventoryItem |
| getThumpableFor | UNKNOWN | INFERRED | zombie.iso.IsoObject |
| Thump | UNKNOWN | INFERRED | zombie.iso.IsoObject |
| getXP | INFERRED | VERIFIED | zombie.characters.IsoGameCharacter$XP |
| AddXP | INFERRED | VERIFIED | zombie.characters.IsoGameCharacter$XP |
| AddXPNoMultiplier | UNKNOWN | INFERRED | zombie.characters.IsoGameCharacter$XP |
| setXPToLevel | INFERRED | VERIFIED | zombie.characters.IsoGameCharacter$XP |
| hasRoomFor | INFERRED | VERIFIED | zombie.inventory.ItemContainer |
| isItemAllowed | INFERRED | VERIFIED | zombie.inventory.ItemContainer |
| getMediaData | INFERRED | VERIFIED | zombie.inventory.InventoryItem |
| isKnownMediaLine | INFERRED | VERIFIED | zombie.characters.IsoGameCharacter |
| setAttachedSlot | INFERRED | VERIFIED | zombie.inventory.InventoryItem |
| addFloor | INFERRED | VERIFIED | zombie.iso.IsoGridSquare |
| RemoveTileObject | INFERRED | VERIFIED | zombie.iso.IsoGridSquare |
| RecalcProperties | INFERRED | VERIFIED | zombie.iso.IsoGridSquare |
| disableErosion | INFERRED | VERIFIED | zombie.iso.IsoGridSquare |
| setSprite | INFERRED | VERIFIED | zombie.iso.IsoObject |
| transmitUpdatedSpriteToClients | INFERRED | VERIFIED | zombie.iso.IsoObject |
| transmitUpdatedSpriteToServer | INFERRED | VERIFIED | zombie.iso.IsoObject |
| transmitCompleteItemToClients | INFERRED | VERIFIED | zombie.iso.IsoObject |
| getFloor | INFERRED | VERIFIED | zombie.iso.IsoGridSquare |
| getFluidContainer | INFERRED | VERIFIED | zombie.inventory.InventoryItem |
| getCapacity | INFERRED | VERIFIED | zombie.entity.components.fluids.FluidContainer |
| getAmount | INFERRED | VERIFIED | zombie.entity.components.fluids.FluidContainer |
| getFluidAmount | INFERRED | UNKNOWN | zombie.entity.components.fluids.FluidContainer |
| addFluid | INFERRED | VERIFIED | zombie.entity.components.fluids.FluidContainer |
| request | UNKNOWN | INFERRED | zombie.world.moddata.ModData |
| setCondition | INFERRED | VERIFIED | zombie.inventory.InventoryItem |
| setConditionLowerChance | UNKNOWN | INFERRED | zombie.inventory.types.Clothing |
| helmetFall | UNKNOWN | INFERRED | zombie.characters.IsoGameCharacter |
