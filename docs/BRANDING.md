# Default artwork

Use manually supplied art first, independently for icon, poster and Workshop thumbnail. Only absent roles use the provided B47 defaults. Existing custom images are not placeholders merely because they differ from the logo.

Portable exact PNG bytes and hashes are stored as data in templates/branding/B47_BRANDING.json; decode with base64, verify SHA-256 and PNG dimensions, and copy without editing. The mod icon is 64x64, poster 128x128, and Workshop thumbnail 512x512. The original files remain user-owned art sources.

Selected current projects: Eyewear, Dogmeat, Medical Checks, Helicopter Events, Buildable Fences, Active Hours and Glowsticks. UI excluded. Custom Eyewear thumbnail and Buildable Fences poster preserved. Apply this fallback to future team projects without custom artwork.

Discover mod.info fields, active source layout and existing packagers. Retain project identity; no invented production package for research-only projects. Generated placeholders may be replaced by the approved fallback, but unknown artwork is preserved until its provenance is understood. This document grants no deployment or Workshop upload permission.

B47_THUMBNAIL.png is a direct high-quality resize of the original B47.png to exactly 512x512. Use its exact bytes for fallback Workshop thumbnails; do not stretch the 128x128 poster. Custom artwork precedence remains unchanged.
