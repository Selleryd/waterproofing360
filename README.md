# Waterproofing360 R5 — original logo & final motion defaults

This complete release is a targeted update of the approved `WATERPROOFING360_R4_GITHUB.zip`. It is not a reconstruction or a different site design.

## Review

Open `OPEN_PREVIEW.html` in Chrome. The single-file interactive preview includes the same 18 page routes, assets, scripts, original galleries, eight articles, and guide as the deployable files. No server, installation, or Terminal command is required to review it.

In the house explorer, select **Live 3D**. Rain and Orbit start selected and running. Reset (including the keyboard Home key) restores those defaults. Manual camera dragging or rotation still stops automatic orbit so the visitor can examine a detail. Rain remains independently switchable.

The hero starts with its existing rain/image animations on. Its **Pause effects** button is removed; both image-scene buttons remain. The separate footer Motion setting and operating-system reduced-motion preferences are preserved. They can disable motion for accessibility; an explicit footer Motion-on selection can re-enable it. Hidden/offscreen animation suspension is retained.

## Your actual logo

`assets/logo.png` is the user-uploaded `Waterproofing360 LOGO.png`, byte for byte. It is used in the header, mobile navigation, and footer on all 18 routes. It is displayed at its original aspect ratio, below its 300-pixel native width, without recoloring, filtering, upscaling, or an AI redraw. A light backing keeps its blue artwork visible against dark surfaces. The favicon clips the original shield pixels in an SVG wrapper rather than retaining the previous placeholder shield.

## GitHub deployment

The deployable entry is **`index.html`**, next to **`assets/`**, **`gallery/`**, **`services/`**, **`blog/`**, and **`contact/`**. Upload the **contents of this release folder** to the intended repository root; do not nest the folder one level inside an older website. `.nojekyll` is included. The site is static: no install or build step is required to serve these files.

No repository name, domain, PAT, or hosting setting has been invented or configured. Nothing has been pushed. Preserve the existing repository's history, custom-domain file, and unrelated deployment configuration when preparing the eventual push. Preview/build tooling and source content are included for ownership and reproducibility; they are not required at runtime.

### Production indexing

This review stays `noindex` until the actual public URL is confirmed. To configure production URLs and indexing, run from the release folder:

```bash
python3 tools/configure_site.py --url https://YOUR-ACTUAL-PUBLIC-ADDRESS.example --index
```

Replace the example with the site's real HTTPS address, including a repository subpath when applicable. This rebuilds canonical URLs, the sitemap, and indexing settings. The downloadable offline preview remains noindex. Do not configure a production origin using a sandbox/download link.

## Editable source

- `tools/build.py`: shared templates, navigation, logo placement, service pages, galleries, and homepage.
- `assets/styles.css`: responsive layout and original-logo presentation.
- `assets/app.js`: navigation, hero effects, guides, search, and page interactions.
- `assets/house3d.js`: existing model/renderer with the updated default motion and synchronized controls.
- `content/`: unchanged article, service, gallery, and source data; site settings are in `settings.json`.

Rebuild and package with Python's standard library:

```bash
python3 tools/build.py
python3 tools/make_preview.py
python3 tools/package.py
```

## Preserved and verified

All 18 page bodies are compared with R4: the only page-body changes are removal of the hero Pause button and initially selected Rain/Orbit controls. All 29 protected content and WebP image files remain byte-identical to R4, including eight article sources and seven gallery records. The three brand placements are changed globally to the uploaded PNG. `verification/r4-baseline.json` and `verification/checks-scope.json` record those comparisons.

See `VERIFICATION.md` for the current local test scope and results, and `MANIFEST.json` for the package's file-by-file hashes. No font binaries, credentials, analytics, new external scripts, or automatic form submissions have been added.

## Limits

There is no newly hosted URL and no GitHub push in this release. External gallery URLs and the existing inquiry provider are preserved, not migrated or submitted to. Browser checks use local Chromium with embedded source/assets; physical-device, Safari/Firefox, hardware-WebGL, and deployed-network acceptance are not implied. Architectural scenes and the model are conceptual, not engineering specifications.
