# Waterproofing360 R5 — verification

**943 local recorded checks passed; 0 failed.** Repeated viewport tests and checks of individual routes are counted separately, not as distinct feature types. All eight test-suite processes completed successfully.

## Exact scope

R5 is patched directly from the approved R4 archive (SHA-256 `6a86535b55e8417ba498814c1c70ea1bd3fa2dfae3a82a7dbd98da7a1a87cacc`). All 18 main-page bodies match R4 after accounting for only the removed hero Pause button and selected Rain/Orbit defaults. All 29 protected content and image files remain byte-identical, including all eight articles, the original gallery mappings, service data, and architectural/project WebP assets.

The supplied logo PNG is byte-identical at `assets/logo.png` (SHA-256 `286796b3e2cf27fa57b221d9ab782ccd6dbd0a1860ad3b3870578c4461d51f66`). Its header, mobile-menu, and footer uses were verified on all 18 routes. The PNG remains 300×90 with alpha transparency; CSS preserves its aspect ratio without enlargement or color filters. The favicon isolates its original shield through an SVG clipping wrapper.

## Motion behavior exercised

- Live 3D starts with Rain and Orbit selected and actually running; timeline and camera movement are measured.
- Rain and Orbit remain independently switchable. Mouse/keyboard camera controls intentionally pause automatic orbit.
- Reset and keyboard Home restore rain/orbit defaults and synchronize button states.
- Leaving/reopening the view and navigating back home retain or reinitialize the appropriate defaults.
- The hero Pause button is absent; normal hero effects remain enabled automatically.
- Reduced-motion preferences disable automatic motion. The existing footer Motion setting remains available. A live preference change also stops effects.
- Model disposal and deferred resize callbacks are safe during navigation. No uncaught exceptions were recorded in the final runs.

## Desktop/mobile verification

The full inherited regression suite ran at widths 320, 360, 390, 430, 768, 1024, 1440, and 1920. Dedicated header/logo/gallery checks also exercised 568×320 and 844×390 landscape, 1100×900 and 1101×900 navigation breakpoints, and 1920×1080 widescreen.

Checks cover header logo/native aspect ratio and bounds, mobile dialog bounds, desktop menu, seven original gallery links, eighteen static routes, the eight articles, search, article checklist and contents links, project-guide choices/results/downloads, all 3D views, reset/rotation/zoom, reduced motion, fallback rendering, focus/scroll locks, and decoded images. Selected current screenshots are included under `verification/`.

## Packaging and production configuration

All local links, assets and referenced anchors resolve. Page titles/descriptions remain unique and structured JSON parses. Both runtime scripts pass syntax checks. The preview's 18 route records match the built page registry, and its initial runtime assets are embedded. No font binaries, credentials, new remote dependencies, or analytics were introduced.

Production configuration was exercised only in a scratch copy. All eighteen pages received the specified canonical origin and indexing setting; the sitemap had eighteen absolute URLs; invalid origins were rejected; relative asset paths remained suitable for a repository subpath. The delivered review stays noindex until the actual deployment URL is explicitly configured.

## Limits

This is local Chromium evidence, not a hosted-site or physical-device certification. The 3D tests exercised the existing compatibility renderer; hardware/WebGL, Safari, Firefox, and physical iPhone/Android rendering are not claimed. External gallery content and live inquiry submission were not re-tested. No GitHub push, domain change, or site publication was performed.

## Reproduce

`tools/verify_r5.py`, `tools/verify.py`, `tools/verify_advanced.py`, `tools/verify_r4.py` (gallery/nav regression), `tools/verify_final.py`, and `tools/verify_packaging.py` contain the current checks. Individual results are in `verification/checks-*.json`; process statuses in `suite-execution.json`; baseline hashes in `r4-baseline.json`; combined results and core hashes in `checks.json`. `MANIFEST.json` covers the complete packaged release.
