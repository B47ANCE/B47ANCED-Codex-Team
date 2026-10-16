---
name: pz-character-animation
description: Create and retarget Project Zomboid Build 42 skeletal animations with Codex-authored Blender/local workflows; validate animal rigs, clips and game integration.
---

# Skeletal character and animal animations

Use when the task concerns this domain. Follow the shared guide at `%USERPROFILE%/.codex/AGENTS.md` and the active project AGENTS.md. Gameplay requires dedicated G7 PASS before release G8; skill instructions do not authorize game/server launch, deployment or publication.

## Procedure

1. Discover the authoritative repository files, local tools and matching installed Build 42 evidence; do not assume paths or API capabilities.
2. Define target artifacts, expected behavior, ownership and measurable acceptance criteria.
   Codex authors all rigging, skinning, retargeting and animation through Blender/local tools. Never use Meshy rigging, animation-library clips, animation generation or text-to-motion, for humanoids or animals. Approved static Meshy geometry may be an input only. If local tools or verified skeleton/export evidence are missing, document the blocker; do not substitute Meshy.
   Read [animation contracts and acceptance cases](references/animation-contracts.md) for loading, skeleton, cancellation, equipment and remote-observer research limits.
3. Audit installed B42 rigs, skeletons, animation naming and supported export path before editing. Preserve source rig/actions; check bone hierarchy, root motion, axes, scale, transitions, event timing, equipped items and multiplayer visibility. Test in Blender then in-game; one does not prove the other. No custom Java or copied third-party rigs without license.
4. Run available static/structural checks, retain evidence, and mark unavailable runtime validation NOT TESTED.
5. Report changed files, validation results, licensing/provenance, outstanding blockers, and deployment/publication status.
