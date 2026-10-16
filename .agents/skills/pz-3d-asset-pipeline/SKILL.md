---
name: pz-3d-asset-pipeline
description: Create or adapt original Project Zomboid Build 42 models using Meshy MCP and Blender; validate meshes, materials, attachments and game exports.
---

# 3D models and Blender exports

Use when the task concerns this domain. Follow the shared guide at `%USERPROFILE%/.codex/AGENTS.md` and the active project AGENTS.md. Gameplay requires dedicated G7 PASS before release G8; skill instructions do not authorize game/server launch, deployment or publication.

## Procedure

1. Discover the authoritative repository files, local tools and matching installed Build 42 evidence; do not assume paths or API capabilities.
2. Define target artifacts, expected behavior, ownership and measurable acceptance criteria.
   For requested AI generation, image/multi-view reconstruction, retexturing, remeshing or conversion, read [the shared Meshy workflow](references/meshy-workflow.md). Use the configured official MCP; approval is required before spending credits. Prefer editing existing project assets when that meets the task. Never use Meshy for rigging, skinning, animation, retargeting or text-to-motion. Route all skeletal work to Codex-authored Blender/local workflows in `pz-character-animation`; generated geometry does not establish rig or game compatibility.
3. Audit installed B42 model pipeline and existing mod assets before choosing export formats. Preserve editable .blend source, licenses and provenance. Verify dimensions, transforms, normals, UVs, textures, materials, LOD where applicable, naming, attachment positions, export format, script definitions and case-sensitive references. Inspect compatibility with game runtime; Blender preview is not game proof. Never claim actual modeling/export succeeded without artifact and tool evidence.
4. Run available static/structural checks, retain evidence, and mark unavailable runtime validation NOT TESTED.
5. Report changed files, validation results, licensing/provenance, outstanding blockers, and deployment/publication status.
