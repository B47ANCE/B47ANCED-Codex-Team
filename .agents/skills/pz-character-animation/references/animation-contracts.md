# Animation contracts and independent acceptance tests

Research provenance: 12 installed Workshop animation leads, inspected without executing third-party scripts or copying code, rigs, clips, XML graphs, assets or documentation. Permission/license defaults are UNKNOWN; this reference grants no reuse rights. Declared versions/authors below are metadata, not identity or rights certification. Relevant vanilla source fingerprints are in the API skill's `workshop-source-evidence.json` and `api-library.json` for Steam build 25485521. Full engine version UNKNOWN. SP/dedicated runtime NOT_TESTED.

## Authoring policy

Codex authors rigs, skinning, retargeting, clips and animation logic through Blender/local tools for humanoids and animals. Never use Meshy rigging, animation-library clips, animation or text-to-motion. Approved static Meshy geometry may be a starting mesh only; do not import a Meshy-generated rig or motion as a shortcut. If no verified skeleton/export route or local authoring tool exists, record the blocker and keep the task pending.

## Evidence and contracts

| Concern | Evidence level and consequence | Independent acceptance work |
|---|---|---|
| Animation selection and hand presentation | VERIFIED source declarations: ISBaseTimedAction setActionAnim, setOverrideHandModels, setOverrideHandModelsString, setAnimVariable, overrideWeaponType and restoreWeaponType. Only formal wrapper arguments are recorded. | Inspect valid action lifetime/receiver and native forwarding; arbitrary clip names, null/clear semantics and side effects remain UNKNOWN until investigated. |
| Loading and registration | OBSERVED source locations/markers and installed vanilla XML field names; complete loader order, branch selection and arbitrary action-group registration UNKNOWN. | Verify the exact installed loader and case-correct references for an original minimal clip. File placement alone is not a loading test. |
| Skeleton and clips | UNKNOWN binary rig compatibility, bind pose, bone hierarchy, root-motion and export support. | Compare our own source rig with installed-game evidence, test axes/scale/bone mapping, and retain editable .blend/actions. Do not reuse third-party rigs or measured poses. |
| Equipment and transitions | Hook/call presence does not establish cancellation or cleanup. | Exercise equip/unequip, movement, interruption, queued-action replacement, death and repeated start/stop. Restore our presentation state on each exit path. |
| Synchronization and authority | UNKNOWN engine replication and server visibility for arbitrary presentation changes. A shared Lua path or command count is not authority evidence. | Identify gameplay owner, keep intent validation server-side, and test remote observers, late join/rejoin and dedicated restart. Cosmetic local changes must not own shared gameplay state. |
| Linux paths | Static case-collision scans are not exact reference or Linux runtime proof. | Resolve case-correct clip/action-group/script paths and test the dedicated Linux target separately. |

Callback registration, wrapper existence and Blender playback never establish G7 PASS. Choose gameplay sandbox configuration and authority under the current global policy; keep G7/G8 blocked when required dedicated evidence is absent. No game/server launch, deployment or publication is implied.

## Provenance ledger (historical research snapshot)

| Workshop lead | Declared author/credit | Declared versions | Unresolved declared Mod IDs |
|---|---|---|---|
| [Fancy Handwork B42.20](https://steamcommunity.com/sharedfiles/filedetails/?id=3771638611) | sunrunner; original dhert; B42 update credit klitoris mahpus | 2.5.1 | None identified; undeclared requirements UNKNOWN |
| [True Action Dancing B42](https://steamcommunity.com/sharedfiles/filedetails/?id=3650071729) | Tchernobill; original iBrRus credited | 2.14 | None identified; undeclared requirements UNKNOWN |
| [Knox Wildlife [B42.21 Beta]](https://steamcommunity.com/sharedfiles/filedetails/?id=3818096743) | UNKNOWN in captured description | 0.1.6 | None identified; undeclared requirements UNKNOWN |
| [Lever-Action Animations [B42.19]](https://steamcommunity.com/sharedfiles/filedetails/?id=3682076457) | Salty Oreos; animation origin credit Nik | UNKNOWN | None identified; undeclared requirements UNKNOWN |
| [Authentic Animations](https://steamcommunity.com/sharedfiles/filedetails/?id=2207282444) | Ravenim and Authentic Peach | UNKNOWN | None identified; undeclared requirements UNKNOWN |
| [Vanilla vehicles animated](https://steamcommunity.com/sharedfiles/filedetails/?id=3281755175) | Hilvon | UNKNOWN | FancyHandwork |
| [Lethal Stealth](https://steamcommunity.com/sharedfiles/filedetails/?id=3531611692) | retbenwin | 1.1 | None identified; undeclared requirements UNKNOWN |
| [Tactical Hold Complete](https://steamcommunity.com/sharedfiles/filedetails/?id=3693258802) | Swalma | UNKNOWN | modoptions |
| [Lifestyle: Hobbies](https://steamcommunity.com/sharedfiles/filedetails/?id=3403870858) | Angry and Mopop | 0.4.0.3 | None identified; undeclared requirements UNKNOWN |
| [Brutal Handwork Build 42 Patch](https://steamcommunity.com/sharedfiles/filedetails/?id=3778038193) | dracarsy2; original DHERT credited | 1.4 | FancyHandwork |
| [[B42] Vehicle Animations Orphanage](https://steamcommunity.com/sharedfiles/filedetails/?id=3684603401) | Hilvon | UNKNOWN | None identified; undeclared requirements UNKNOWN |
| [Sync smooth car animations 42.20](https://steamcommunity.com/sharedfiles/filedetails/?id=3670959466) | БОСС НИКИТОС | UNKNOWN | None identified; undeclared requirements UNKNOWN |

No unresolved dependency is silently satisfied by a similarly named installed mod. No confirmed Java/ZombieBuddy requirement was found in this 12-item snapshot; dynamic/undeclared dependencies remain UNKNOWN and current projects must recheck eligibility. Coverage describes bounded static triage, not exhaustive semantic/security review. Preserve originating local audit ledgers separately; do not bundle raw scans or third-party implementation details in a skill.
