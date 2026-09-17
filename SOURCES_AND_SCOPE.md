# Sources and scope — R5

## Authoritative baseline

This update starts from the exact approved `WATERPROOFING360_R4_GITHUB.zip` in this conversation. Its SHA-256 is `6a86535b55e8417ba498814c1c70ea1bd3fa2dfae3a82a7dbd98da7a1a87cacc`.

The R4 archive was extracted directly. No content was reconstructed from screenshots. The current instructions authorize only the original-logo replacement, default Live-3D Rain/Orbit selection, and removal of the hero Pause effects button.

## Original artwork

The supplied `Waterproofing360 LOGO.png` is used verbatim as `assets/logo.png`. The original PNG is also embedded inside the favicon SVG; clipping selects its existing shield without drawing a replacement. The visible logo is never recolored, resampled, or upscaled.

## Carried-forward sources

The seven gallery mappings, exact external URLs, small project-photo thumbnails, business phone, inquiry destination, six service records, and all eight sourced field guides are unchanged. The galleries' prior provenance remains documented in `GALLERY_SOURCES.md`. Existing architectural images, real-project thumbnail images, article Markdown, and source data are compared byte-for-byte in `verification/r4-baseline.json`.

No new customer counts, ratings, performance claims, warranty terms, prices, service areas, or technical advice were added. This release does not research or revise the blog articles.

## Technical scope

The existing 3D geometry and shading are unchanged. The code changes initialize and reset rain/orbit to enabled, synchronize toggles with the real runtime state, and guard deferred resize callbacks against a destroyed model. Reduced-motion preferences and the footer motion setting still take precedence. The hero's existing visual effects and imagery are unchanged; only its local Pause button is removed.

## Deployment scope

No repository, external website, gallery host, live inquiry form, or DNS setting was modified. The preview is a local interactive artifact; the complete ZIP is prepared for a later, explicitly targeted deployment. Review indexing remains off until a production URL is configured.
