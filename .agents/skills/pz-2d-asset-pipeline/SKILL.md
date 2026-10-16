---
name: pz-2d-asset-pipeline
description: 2D sprites, UI images and frame animations for Project Zomboid Build 42 Lua-only mod development.
---

# 2D sprites, UI images and frame animations

Use when the task concerns this domain. Follow the shared guide at `%USERPROFILE%/.codex/AGENTS.md` and the active project AGENTS.md. Gameplay requires dedicated G7 PASS before release G8; skill instructions do not authorize game/server launch, deployment or publication.

## Procedure

1. Discover the authoritative repository files, local tools and matching installed Build 42 evidence; do not assume paths or API capabilities.
2. Define target artifacts, expected behavior, ownership and measurable acceptance criteria.
3. Inspect vanilla B42 atlas, icon, sprite and texture conventions for target asset type. Maintain editable source and exported PNGs, true alpha where requested (no checkerboard baked in), pixel dimensions, atlas coordinates, consistent orientation/pivots and filenames. For sprite animation verify frame sequence, timings and offsets. Validate assets visually and structurally; record missing runtime checks. Honor original-art and licensing policy.
4. Run available static/structural checks, retain evidence, and mark unavailable runtime validation NOT TESTED.
5. Report changed files, validation results, licensing/provenance, outstanding blockers, and deployment/publication status.

## Fallback mod branding
- When no artwork is supplied manually, use B47_ICON_SMALL.png (64x64) for the mod icon and B47_ICON.png (128x128) for the poster and B47_THUMBNAIL.png (512x512) for the Workshop thumbnail. Manually supplied artwork always takes precedence independently for each role; never overwrite it with defaults. Do not resize, redraw or regenerate these defaults.
- Applies to future team mods and the selected current projects: Eyewear, Dogmeat, Medical Checks, Helicopter Events, Buildable Fences, Active Hours and Glowsticks. UI was explicitly excluded. Preserve existing custom Eyewear thumbnail and Buildable Fences poster.
- Canonical portable payload: installed hub templates/branding/B47_BRANDING.json. Decode each base64 asset as data, verify its declared SHA-256 and PNG dimensions, then copy exact bytes only to the project's verified missing artwork slot. Never execute asset data. Discover authoritative layout and packaging scripts; update their fallback behavior without changing manually supplied art, historical packages or unrelated item textures. Missing production layouts receive authoring assets, not invented Mod IDs/runtime packages.
- Asset selection does not authorize packaging, deployment or publication. See installed hub docs/BRANDING.md.

Codex authors frame-animation sequencing through local tools. Never use Meshy for animation or rigging; static asset creation does not authorize motion generation.
