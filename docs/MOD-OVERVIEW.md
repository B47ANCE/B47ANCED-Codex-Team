# Features and connections overview

The team package includes the reviewed 26-project portfolio and 15 shared-feature
groups. Each developer gets an interactive, self-contained local overview during
explicit workspace setup. It works offline and includes projects they have not
cloned, explicitly labelled **NOT INSTALLED — shared snapshot only**.

## Open and refresh

Open your generated `B47ANCED.code-workspace` in VS Code. Under **Terminal → Run
Task**, choose **Overview: Open mod ecosystem**. The overview opens in your browser
from `<your workspace>/mod-overview/index.html`. All data and scripts are local;
no server, hosting account or additional Python package is required.

**Overview: Keep features and connections current** is the sole automatic task.
VS Code may ask you to allow automatic tasks in this trusted workspace. Make that
trust decision yourself; setup does not bypass it or change your editor settings.
If automatic tasks are disabled, run that task manually. It checks every 60
seconds; the browser reloads the generated page every 60 seconds. The task stops
when terminated or VS Code closes. It is not a Windows service or sign-in task.

**Overview: Refresh features and connections** performs one refresh. For an
existing installation, after reviewing this package:

```powershell
& .\tools\Setup-CodeWorkspace.ps1 -Workspace $teamWorkspace -RepositoryRoot $modRepositories -PythonExe $pythonExe
```

Use your existing developer-local paths. Customized generated workspaces or
runtime copies are preserved and block replacement; review/merge them manually
rather than deleting your settings. Generated overview outputs have their own
ownership hashes and backups and refuse to overwrite custom edits. No mod source,
project instructions or local settings are changed by the inventory/watch tasks.

For a direct, one-shot build from a reviewed package:

```powershell
& $pythonExe .\tools\mod_overview.py --repositories $modRepositories --output (Join-Path $teamWorkspace 'mod-overview')
# Add --watch to keep refreshing; Ctrl+C stops it.
```

## What updates automatically

- Current local root VERSION, branch and HEAD, plus required Mod IDs from
  `src/` and/or `Contents/mods/` metadata. Unresolved/external requirements remain
  visible. Parallel source trees are inspected, never reconciled or rewritten.
- Added projects appear with UNKNOWN features until described. Hidden
  infrastructure and `.worktrees` are excluded; known Mod IDs and shared Git
  common directories deduplicate alternate checkouts. The canonical folder wins;
  a newer feature worktree is not silently substituted for that build.
- Project-owned `docs/MOD_OVERVIEW.json` overrides its feature summary and optional
  incoming connections. A version or source-content change invalidates its review
  marker. The shared audit snapshot is also flagged when its source digest differs.
- Dependencies come from current loader metadata; optional adapters and shared
  feature stories remain reviewed descriptions, not speculative code inference.

No Git fetch/pull, GitHub API call, external mod execution or arbitrary project
script occurs. Local HEAD does not prove remote freshness. Developers see their
own checked-out branches; they must pull/review project updates through the normal
workflow to share the same current source. A missing local clone is never labelled
current merely because a shared snapshot exists.

## Keep features current alongside development

When features, dependencies or integration contracts change, update the project's
descriptor in the same branch/PR as its README, changelog and source. The first
adoption is an intentional project documentation change, not an automatic rewrite.
Use the stable portfolio id in `templates/overview/catalog.json`; do not invent a
replacement Mod ID or project VERSION. New unknown projects use the generated
`local-…` id until their permanent catalog record is reviewed.

Generate a **draft only** to stdout:

```powershell
& $pythonExe .\tools\mod_overview.py --describe-repository $project --project-id rooms
```

This prints current VERSION and `source_digest`. Merge those fields into
`docs/MOD_OVERVIEW.json` after reviewing the actual change; preserve existing
features, limits and relations. Do not replace an existing descriptor with the
empty draft. Review feature evidence, then set `reviewed` to true. Evidence paths
are repository-relative. Regenerate the digest after source/README/VERSION edits;
the descriptor itself is excluded, so there is no self-hash cycle.

Example structure (use your actual version/digest and feature evidence):

```json
{
  "schema": 1,
  "id": "rooms",
  "name": "Rooms",
  "version": "YOUR_EXISTING_VERSION",
  "source_digest": "SHA256_FROM_DRAFT",
  "reviewed": false,
  "features": [
    {"status": "Source", "text": "Describe the implemented behavior precisely."},
    {"status": "Planned", "text": "Describe a proposal without implying it ships."}
  ],
  "limits": "Native SP/dedicated NOT TESTED for this change.",
  "evidence": ["README.md"],
  "relations": [
    {"target": "qm", "kind": "Optional", "text": "This project consumes the named provider contract."}
  ]
}
```

Relations describe incoming providers: `target → this project`. Required edges
normally come from `mod.info`; do not invent them in prose. Statuses are Source,
Foundation, Planned, Blocked, Separate branch, Historical and UNKNOWN. Connection
kinds are Required, Optional, Migration and Planned. A source review flag never
establishes SP or dedicated runtime correctness. Preserve exact runtime version,
environment and evidence references in project validation docs.

Until a project adopts a descriptor, maintain its reviewed entry in the shared
catalog through a team-package PR. For a new multi-mod feature, update the shared
`flows` record and each affected project's contract documentation; never merge
evidence from different branches into a claim about one installed build. The
catalog retains the original audit date and explicitly separate branch work.

## Security, updates and rollback

The watcher reads bounded text/data files only, rejects unsafe evidence paths,
skips linked trees, and writes only its owned output directory outside mod roots.
Descriptions render as text, not executable markup. Do not add credentials,
private paths, player records or diagnostic logs to public descriptors/catalogs.

Reviewed explicit setup pins the generator, view and catalog under
`.codex/cli-workflow-runtime/overview`. Validated team updates install new helpers
inert and never run them. After reviewing a new package, rerun workspace setup to
activate its new overview code/catalog; stop the old watcher first. Project
descriptors and metadata are refreshed without reinstalling. Team rollback does
not change your mod branches or automatically replace this pinned runtime; review
the restored package and rerun workspace setup if you want that runtime version.
Prior owned outputs/runtime files are backed up. Preserve custom outputs and all
existing update/rollback safeguards.

This is a feature/contract map, not a release gate, dependency installer, workshop
publisher, live server monitor or proof that every vanilla-system interaction has
been identified. G7/G8 requirements remain unchanged.


## Merged source snapshot update — 2026-10-17

Package 13.9.1 refreshes Quartermaster **0.18.0-dev.1** at merged commit
`bec375b0483ec8d9d4bbf1565cd897c50d6fb887` and Rooms **0.2.0-dev.6** at
`e9d3b0965155ef6bb5ae067eb42d50e96d2de7b2`. Ledger, physical Shopping Lists,
computer/CD and carry features are Source; advisory room allocation is Foundation.
Rooms supplies designated UUID geometry/metadata and independent action permissions;
Quartermaster owns profiles and shadow accounting. Enforcement and live role routing
remain disabled. Native SP/dedicated NOT TESTED; G7/stable G8 BLOCKED.

The original catalog date remains the broader portfolio audit date. Only these two
entries and affected flows/connections were refreshed; other projects are not claimed
re-audited. Missing clones show the shared versions labelled NOT INSTALLED. Existing
clones use their own version/source review state and normal Git update workflow.
Package updates do not pull mod repositories, activate a new pinned watcher or change
local settings. After a validated-main update, review and rerun workspace setup as
described above to activate the refreshed catalog, then refresh the overview.


## Preserve a customized VS Code workspace

If normal setup preserves a customized workspace, explicitly merge only overview
tasks using the reviewed 13.9.2 helper:

```powershell
& .\tools\Setup-CodeWorkspace.ps1 -Workspace $teamWorkspace -RepositoryRoot $modRepositories -PythonExe $pythonExe -MergeOverviewTasks
```

This opt-in mode requires an existing strict JSON workspace (JSONC comments,
duplicate keys and unsupported task schemas are refused unchanged). It adds only
Open/Refresh/Keep-current overview tasks, retaining settings, folders, launch and
extension fields, existing tasks/inputs and unknown fields. Existing identical
overview tasks are retained; conflicting labels are refused for manual review.
The original bytes are backed up under the developer-local cli-workflow-backups
directory. All writes are checked for concurrent changes and rolled back on write
failure. The customized workspace stays outside whole-file team ownership, so a
later default setup cannot silently replace it. Other customized runtime outputs
still block replacement. VS Code retains control of workspace trust and automatic
task consent; adding the read-only watcher does not start it or grant approval.

Repository verification also accepts literal USERPROFILE/.codex/AGENTS.md, as used
by Earthworks, with bounded exact-path matching. No project guide is rewritten.
