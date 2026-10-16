# Shared Meshy MCP workflow for PZ assets

Use this reference from the 3D and skeletal-animation skills when Meshy contributes to the requested asset task. It centralizes service-specific guidance; each skill retains its own PZ acceptance checks. Meshy is an authoring service, never a shipped mod dependency.

## Select tools and scope

Inspect the configured official Meshy MCP tools and their current schemas before choosing parameters. Setup/authentication lives in `%USERPROFILE%/.codex/b47anced-team/docs/MESHY.md`; use the existing `MESHY_API_KEY` integration. Never request keys in chat, print them, or install another client to work around missing authentication. Discovery and balance checks are read-only; discovery alone does not prove authentication.

The official [Meshy agent skills](https://github.com/meshy-dev/meshy-3d-agent) are useful upstream references for generation workflows. Their current generation skill targets a separate Meshy CLI. Adapt relevant concepts to the configured MCP rather than automatically installing its CLI, OAuth flow, printing skill or OpenClaw integration. Keep one team workflow and the existing 23 skill names. If an upstream skill is separately requested, review its instructions and dependencies before installation.

| Requested outcome | Preferred route |
| --- | --- |
| Original prop or character geometry | Text-to-3D, or image/multi-image-to-3D with user-owned or licensed references; inspect a preview before any separately charged refinement. |
| Existing asset adjustment | Blender edits first where sufficient; Meshy remesh/retexture/convert only when useful and approved. |
| Humanoid rig and motion | Check rig eligibility, then rig; reuse included walk/run results if suitable. Discover library action IDs before animation, or use text-to-motion for original requested motion. |
| Dog, cat, rat or other non-humanoid animation | Blender rigging/retargeting against verified PZ skeleton evidence. Meshy-generated geometry may be an input; API animal auto-rig compatibility remains unsupported by current documentation. |

Define silhouette, dimensions, polygon/texture budget, required views, output files and acceptance criteria before generation. Upload only authorized references; research subscriptions do not grant asset reuse rights. Preserve manually supplied artwork and editable sources.

## Spending and task lifecycle

All exposed tools remain subject to explicit approval before each credit-consuming job, including generation, refinement, remesh, retexture, conversion, rigging and animation. Check current tool documentation/pricing and describe the proposed operation, estimated credits (or UNKNOWN) and outputs before requesting approval. An already explicit, scoped job approval is sufficient; tool availability, balance or a subscription alone is not approval. Skill/setup verification submits no paid jobs.

Submit once and retain the task ID, actual task type, parameters and approval scope. Poll status with bounded waits, respecting rate limits; report pending tasks rather than polling indefinitely. After a timeout or ambiguous submission, reconcile existing tasks/status before any new paid submission. Do not automatically retry failed paid jobs or silently add paid pipeline stages.

Choose only required output formats. Preserve original service outputs and editable `.blend` sources separately from game exports. Confirm a succeeded task and real local file bytes before claiming a download: the MCP download helper returns URLs for rigging/animation results, requiring a separate authorized file transfer. Verify file size/type, importability and SHA-256. Record provenance, task/model identifiers, parameters, costs if available and rights limitations, but keep keys, private inputs and signed download URLs out of public documentation.

## Rigging and motion limits

[VERIFIED - official API documentation, reviewed 2026-10-15] Programmatic auto-rigging supports textured, clearly structured humanoid/biped assets. The API excludes non-humanoids; input-task meshes above 300,000 faces are unsupported, and a supplied GLB must face +Z. Recheck current schemas before submission. The web app's humanoid/quadruped Animate feature is a separate capability, not evidence for MCP animal rigging.

For library animation, discover actual action IDs through `meshy_list_animations`. `meshy_animate` selects exactly one of `action_id`, `action_ids` or `motion_task_id`; validate current limits instead of inventing IDs. Text-to-motion produces motion rather than a character model: current prime outputs FBX, swift outputs BVH, and motion clips expire after three days. Download approved results promptly and preserve provenance. Check current retention and output schemas at execution time.

Do topology-changing operations before rigging where practical. Remeshing a weighted model can invalidate skin weights and bindings; preserve the original and validate/rebind explicitly. A Meshy humanoid skeleton or motion clip still needs Blender retargeting and comparison with the installed PZ skeleton, bone names/hierarchy, bind pose, scale, axes, root motion and clip/event conventions. Never assume FBX/GLB/BLEND interchange files are game-ready exports.

## Evidence and acceptance

Inspect normals, UVs, textures/materials, skin weights, deformation, attachment points, transitions and animation timing in Blender, then validate the exact installed-game import/script pipeline. Preserve Lua-only runtime, authoritative gameplay and sandbox rules from the global guide. No custom Java bridges or copied third-party rigs/clips.

Label service output, Blender checks, offline checks, SP and dedicated MP separately. Neither a completed Meshy job nor a Blender preview proves PZ runtime compatibility. Report runtime gates honestly; no game/server launch, deployment or publication is authorized by asset creation alone.

## Primary references

Reviewed 2026-10-15; vendor capabilities and pricing may change. Consult current documentation and installed tool schemas before execution.

- [Official MCP server](https://github.com/meshy-dev/meshy-mcp-server), reviewed upstream commit `fad086d1dc4e4492244d4fe006802c501b6b37de`; team package pin 0.6.4.
- [Official agent skills](https://github.com/meshy-dev/meshy-3d-agent), reviewed upstream commit `92ffd747638284f6ccdf419d764e6f14753ec298`; reference only, no additional client installed.
- [Rigging API](https://docs.meshy.ai/en/api/rigging), [Animation API](https://docs.meshy.ai/en/api/animation), [Text-to-Motion API](https://docs.meshy.ai/en/api/text-to-motion).
- [Web-app Animate](https://docs.meshy.ai/en/webapp/guides/animate): distinguish web-app capabilities from API exposure.
