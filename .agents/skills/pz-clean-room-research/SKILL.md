---
name: pz-clean-room-research
description: Research mods authored outside the B47ANCE'd Workshop team for interoperability, behavior, or feasibility while preserving independent implementation and licensing boundaries.
---

# Third-party mod clean-room research

Read the shared guide at `%USERPROFILE%/.codex/AGENTS.md` and project instructions. Preserve Lua-only runtime, authority and existing evidence/gate definitions. Read-only research does not authorize copying, edits to external mods or publication.

Use this skill whenever examining, comparing, integrating with, or implementing behavior inspired by a mod authored outside the development team. Applies equally to Steam Workshop, GitHub, ZIPs, decompiled material, and locally installed third-party mods. Do not assume public availability means open-source permission.

## 1. Establish purpose and provenance
- Identify mod title, author, source URL, Workshop ID if available, exact version/date, applicable license and any explicit permissions; record unknowns as UNKNOWN.
- Define a narrow research question: compatibility surface, interoperability contract, observed behavior, limitation, or reproduction of a failure. Prefer vanilla game source, public documentation, and published API contracts first.
- Do not access private, paywalled, encrypted, or restricted material without authorization. Respect applicable licenses and terms.

## 2. Allowed observations and boundaries
- May inspect behavior, metadata, exposed public APIs, documented interfaces, event names, compatibility requirements, error signatures, and high-level capability/failure evidence where access is legitimate.
- Do not transplant or closely paraphrase third-party implementation code, nontrivial algorithms, distinctive architecture, scripts, UI text, textures, sprites, models, animations, sounds, translations, or documentation into team projects without license/permission that authorizes that use.
- Do not treat renaming identifiers, translating languages, formatting changes, or AI rewriting as independent implementation.
- Similar game mechanics and interoperability are not inherently prohibited; implement independently from requirements and verified vanilla APIs.
- If a license affirmatively permits reuse, record exact license, notices, attribution and redistribution obligations and obtain project-owner approval before importing anything. When unclear, do not reuse protected expression; ask for permission or design independently.

## 3. Separate research from implementation
- Produce a neutral *behavioral specification* with inputs, outputs, observable states, constraints, and compatibility contract. Do not embed third-party code or close pseudocode.
- Maintain a provenance ledger (`docs/THIRD_PARTY_RESEARCH.md` or project-approved equivalent) with references, version, license status, observed facts, uncertainties, and resulting original design decisions. Never include credentials or private server data.
- Where feasible, have a different developer implement from the neutral specification without seeing third-party implementation source; require independent review for sensitive overlaps.
- Implement using verified Build 42 Lua-exposed vanilla APIs, original assets, original naming and architecture. Do not edit or redistribute the third-party mod without permission.
- Public API compatibility adapters may call documented interfaces under applicable permissions. Check optional dependency presence and fail gracefully when absent. Avoid shipping third-party source or assets.

## 4. Review and evidence
- Review changed files for suspiciously similar code, assets, naming, structure, or copied documentation. A superficial similarity scan is not a legal clearance.
- Review license obligations, attribution, bundled dependencies, Workshop redistribution, and any required permission evidence.
- Record technical source evidence separately from SP/MP runtime validation. Mark uncertain or blocked claims explicitly.
- PRs touching third-party compatibility/research require a clean-room checklist and reviewer signoff; flag unresolved licensing questions for owner review, not automated assumptions.

## Required output
Report: purpose; third-party mod/author/version/URL; license/permission status; factual findings; clean-room design boundary; assets/code imported (normally NONE); attribution obligations; review result; unresolved questions; validation performed/not performed.

## Stop conditions
Stop and request approval if asked to copy an unlicensed implementation or asset, remove attribution, bypass license restrictions, or ship a third-party component whose rights are unclear. This workflow is an engineering safeguard, not legal advice.
