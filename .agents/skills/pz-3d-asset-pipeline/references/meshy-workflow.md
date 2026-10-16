# Meshy workflow for static PZ assets

Meshy is an authoring service for approved static geometry/material work, never a runtime mod dependency. All rigging, skinning, retargeting and animation must be authored by Codex through Blender/local tools in `pz-character-animation`. Never use Meshy rigging, animation, animation-library clips or text-to-motion, including humanoid and animal tasks. Tool exposure, a subscription or approval to spend on geometry does not override this rule.

## Permitted scope and authentication

Inspect the configured official MCP and current schemas before parameter selection. Reuse the developer's MESHY_API_KEY environment integration; setup is documented in the installed hub docs/MESHY.md. Never request keys in chat or put them in source/logs/arguments. Discovery and free balance checks are read-only and do not authorize jobs.

Use text-to-3D or image/multi-image-to-3D for original static geometry with authorized references. Prefer Blender edits for existing assets when sufficient; remesh, retexture or format conversion require scoped approval if they consume credits. Do topology changes before Codex-authored skinning; protect weighted sources and validate any rebind independently. Do not invoke a conversion or generation option that also rigs or animates a model.

## Paid work and recovery

Before each permitted credit-consuming job, state the operation, estimated credits (or UNKNOWN), inputs and intended outputs and obtain explicit approval. Submit once, preserve the task ID and scope, and poll with bounded waits. Reconcile an ambiguous result before another submission; never automatically retry or add paid stages. No paid job is authorized by skill/setup verification.

Confirm successful task status and actual downloaded bytes; a returned URL is not a verified local file. Verify file size/type, SHA-256 and Blender import. Preserve original service results and editable .blend sources separately from game exports. Record non-secret task/model identifiers, costs if available and rights limitations; keep keys, private inputs and signed download URLs out of public docs.

## PZ acceptance

Check scale, axes, transforms, normals, UVs, materials, attachments, export conventions and case-correct script references against installed vanilla evidence. A service result or Blender preview does not prove PZ compatibility. Use original assets only; research subscriptions do not grant reuse rights. Keep Lua-only runtime, authoritative gameplay, sandbox settings and dedicated-release gates. No game/server launch, deployment or publication is implied.

Official MCP: https://github.com/meshy-dev/meshy-mcp-server. Current team package pin remains 0.6.4; inspect installed schemas before a permitted job. Upstream generation skills are references only, not alternate integrations or permission to use their rigging/motion workflows.
