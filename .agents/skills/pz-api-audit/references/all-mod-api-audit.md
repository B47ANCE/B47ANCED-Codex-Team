# All-mod API audit — Steam build 25485521

Game version: UNKNOWN (not independently decoded). Runtime: NOT_TESTED.
The installation has loose class overrides; packaged metadata does not establish
the effective running environment. No game/server was launched.

The companion [original evidence summary](all-mod-api-audit-25485521.json) records
coverage and fingerprints. No game source, raw bytecode, logs or private settings
are distributed here. Native binary evidence uses the existing [1,1] sentinel.

## Coverage and limits

Read-only triage covered 27 project folders, 1,028 non-test Lua files and 11,380
direct-colon/literal-dispatch call sites. This includes source, packaged mirrors
and prototypes, so it is not a count of unique production contracts. The name scan
flagged 141 sites. A narrower native-return-chain scan observed 100 calls and found
no additional missing named methods. These scans cannot prove receiver type,
overload selection, effective exposure, authority, persistence or runtime success.
Dynamic names, generated code and unsupported argument combinations can be missed.
Existing library entries remain build-bound; source matches never upgrade runtime.

The triage resolved custom callbacks (canRun, serialize, deserialize, onCollision,
onDamaged, onNativeStateChanged, onTrip), domain/dependency dispatch (Authority,
UV, ZombieHunger), custom diagnostic core and updateLight aliases, and standard
Lua string methods (byte, gmatch, gsub, upper). They are not missing vanilla APIs.
Quartermaster getPreCookItems is a Project Cook dependency interface, not a vanilla
contract; dependency availability remains UNVERIFIED and no upstream code was copied.

Guarded compatibility probes getActivated, getDeadBodies, getTeachedRecipes,
getWaterAmount, getWaterMax and setTaintedWater have supported primary paths or
context-dependent legacy use; this scan did not establish a current failure.
PropertyContainer.Is is a legacy guarded probe; has is present but behavior was
not mechanically substituted. setLx/setLy/setLz remain unresolved guarded probes:
setLastX/Y/Z names are not enough to prove equivalent movement/interpolation state.
These unresolved paths require owning-project receiver and runtime investigation.

## Confirmed offline corrections

- lightWorks: InventoryItem has a packaged getTorchDot descriptor but no inspected
  public setTorchDot. Preserve bulb dot overrides in its existing Lua renderer
  cache instead of silently attempting the setter. ScriptManager item definitions
  are scripting.objects.Item, not InventoryItem; absent light getters now yield
  UNKNOWN diagnostic metadata instead of fabricated zero/false. Script getItemType
  is a native candidate, not runtime-verified exposure.
- groundWorks: use the inspected haveRoofFull candidate in the guarded shelter
  probe. Outside/exterior does not imply unroofed. Roofed/open/explicit shelter
  host fixtures pass; actual weather behavior remains NOT_TESTED.
- Medical Checks cooperative 0.3.0-dev.3: replace only the fresh-store next check
  with a local pairs loop. Original fails and corrected module passes when next
  is absent under host Lua 5.1. Fresh-slot seeding, populated stores, failed writes,
  recovered and incomplete-store rejection have focused regression coverage.
  Full project suite: 83 PASS, one historical-fixture SKIP; two optional research
  selector fixtures PASS. Native medical privacy remains BLOCKED.

lightWorks/groundWorks changes are user-authorized local-only exceptions before
Git/version onboarding. Existing version metadata and historical Contents trees
were preserved. They are not GitHub-backed mod iterations. Medical Checks uses
its own versioned feature-branch/PR workflow. Shared library publication does not
apply these patches to another developer's mod checkout.

## Kahlua bootstrap findings and pending fixes

The reviewed J2SEPlatform setup registers BaseLib and TableLib before loading root
stdlib.lua. BaseLib registers global unpack; TableLib registers pairs and ipairs;
the root Lua aliases pairs=table.pairs. These bounded inspected sources register
neither global next nor table.unpack. Other mods/runtime code may add them; actual
global availability remains UNKNOWN. Standard host Lua tests can mask this difference.

Use a local pairs-based emptiness check where that is the intended operation.
Use a local `(unpack or table.unpack)` fallback for cross-host return unpacking.
Do not install global shims or replace unrelated iterator/ordering operations.

The user explicitly left tested overlays pending for itjustWorks recipe result
unpacking, weatherWorks empty-store initialization, powerWorks identity-set
registration and Last Known Address world-identity initialization. Each original
failed and overlay passed under Windows host Lua 5.1 with next/table.unpack absent.
No source patch was applied to those four projects.

experienceWorks claim migration has another guarded next dependency; its general
journal fixture did not exercise that branch, so it is not labeled reproduced.
Dogmeat has three development-source next emptiness checks; concurrent development
was preserved, with no fix applied during this audit. These remain pending.

All offline tests use host Lupa, not the game Kahlua runtime. Recheck on the exact
developer installation and test SP/headless startup, store initialization/restart,
reconnect and dedicated synchronization as appropriate. Gameplay G7 remains
BLOCKED / NOT TESTED and stable G8 BLOCKED. No deployment/publication is authorized
by this evidence library.
