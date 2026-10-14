---
name: pz-publish
description: Publish an explicitly selected validated Project Zomboid mod to its existing Steam Workshop item through cached-login SteamCMD when the user says publish.
---
Follow the `publish` command contract in `%USERPROFILE%/.codex/AGENTS.md` and the selected project's instructions. Reuse established project packaging and SteamCMD upload scripts. Verify canonical version/current mirrors, existing Workshop ID, App ID 108600, VDF, exact content, changelog and required tests. Reject custom Java/JAR/native runtime components. For stable-release approval all required gates, including dedicated G7, must pass. Missing MP evidence alone does not block an explicitly authorized labelled Workshop MP test upload under the shared policy. All other applicable preflight checks must pass; refuse upload on failures. Invoke `the verified developer-local SteamCMD executable` using existing cached credentials, never store secrets, and verify the actual upload result. Do not create new items, deploy locally or guess an ambiguous target. Do not request redundant permission when an explicit publish command already authorizes the concrete operation and all gates pass.

## Release provenance (v12)
- Before SteamCMD upload create a release manifest binding exact Git commit SHA, version, Workshop ID, Mod ID, package SHA-256, target Build 42 version and validation status.
- Confirm the explicit publish request authorizes the concrete release (do not request redundant permission when all gates pass) and inspect the actual staging tree; publication must not occur as a side effect of GitHub CI.

## Workshop description governance - v12.3

## Canonical project files
- `docs/WORKSHOP_DESCRIPTION.md`: human-editable description with project-specific content, reviewed and committed. Use the standardized section order in `%USERPROFILE%/.codex/b47anced-team/templates/workshop/WORKSHOP_DESCRIPTION.template.md` for new projects.
- `docs/WORKSHOP_CHANGELOG.md`: reviewed player-facing changes; only changes approved for the selected stable release or authorized Workshop MP test upload become the Steam changenote; include testing status.
- `workshop/description.bbcode` and `workshop/changenote.txt`: generated output; never treat them as source of truth.
- For existing projects, discover and preserve established canonical description locations and scripts. Do not overwrite or migrate existing Workshop text without task authorization and review of the concrete diff; existing user authorization remains valid.

## Description sections
Title; Overview; Features (implemented only); Compatibility & Requirements (specific supported game versions and actual SP/MP validation); Configuration (if applicable); Source Code & Development; Known Issues (when applicable); Credits & Permissions. No fabricated features, promises, testing claims, or placeholders in publication.

## GitHub link
Obtain from `git remote get-url origin` and normalize supported GitHub SSH/HTTPS remote forms to `https://github.com/OWNER/REPO`. Confirm the URL belongs to the current project and is public; never invent an owner/repo. Render `[url=https://github.com/OWNER/REPO]GitHub — Source Code & Issues[/url]`. If unavailable or ambiguous, BLOCK publishing until resolved.

## Preflight and output
1. Run repository-startup freshness and verify Git commit/version/source inventory; no uncommitted release payload unless explicitly approved and recorded.
2. Resolve canonical description and changenote; compare against the existing Workshop description and show material changes for review; ask for approval only if the session does not already authorize them. Preserve custom formatting and legal attribution.
3. Convert Markdown to a *supported* Steam BBCode subset using `%USERPROFILE%/.codex/b47anced-team/tools/Build-WorkshopDescription.py` or verified existing tooling; fail closed on unsupported markup. Do not blindly replace arbitrary Markdown or silently discard HTML/images.
4. Validate all links, nonempty sections, text length (check current SteamCMD/Workshop constraints rather than inventing a universal cap), real line breaks, no literal `\n` escape sequences, no TODO markers, credits, correct item ID, and nonempty change notes.
5. Inspect actual staging tree, VDF `appid=108600`, existing `publishedfileid`, target path, version and release manifest binding Git SHA, package hash, Mod ID and validation status.
6. Use existing SteamCMD uploader and cached authentication; never store credentials in repositories or tool output. Publish only the authorized target. Confirm uploader result and inspect the public page when accessible; report any verification gap.
7. No GitHub CI auto-publishing and no SFTP server mutations.

## Mandatory status report
State canonical inputs, generated outputs, GitHub URL, release commit, Workshop ID, validations, upload result, and any untested SP/MP or live-page verification gates.

## Workshop test distribution exception
Apply the Workshop MP testing policy in global AGENTS.md and installed hub docs/WORKSHOP_MP_TESTING.md. Missing dedicated MP evidence alone does not block an explicitly authorized labelled Workshop test upload. G7 remains NOT TESTED / BLOCKED and stable-release G8 remains BLOCKED; offline/authority/security/version/package failures still block upload. This skill does not itself authorize publication.
