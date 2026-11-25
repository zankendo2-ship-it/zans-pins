# REVIEW REQUEST - v3 print fix ported into designer PREVIEW pages (25 Nov 2026, 20:15 UTC) - TASKS 4a88568 + 5feb977

## Where it is, and the catch
On branch `claude/friendly-curie-wcq9xc` (the only branch I can push to):
- `docs/bauble-designer-v2/index.html`
- `docs/mug-designer-v2/index.html`
- `docs/print-fix-v3-test/` (the SVG masters these pages produced in my test, and the two test scripts)

**There is no preview URL.** My branch is not the published one, so these pages are not served at www.zanshorseracing.co.uk. To get URLs, whoever owns the published branch copies the two folders into its `docs/`. They then appear at `/bauble-designer-v2/` and `/mug-designer-v2/`. The live `/bauble-designer/` and `/mug-designer/` are not touched by that copy.

Base used: the designer pages as they stand on `claude/project-thread-xwwh7g` (newest `docs/`, commit of 25 Nov 17:46 UTC). If the published branch is a different one, tell me and I will rebase onto its pages. Both preview pages carry `noindex,nofollow`. The mug preview loads three.js from `/mug-designer/three.min.js` (the live copy) instead of duplicating it.

## What was ported (follows DESIGNER_PORT.md)
Bauble (silks bauble, style A): `reference/fixC.js` added unchanged as a script after the page's own code, plus the traced horse path taken from `qa-v3-loussiemoo.svg`. New: `ZANSBauble.printMaster()` = the 990 x 990 print SVG with no clip-path. `ZANSBauble.printFile(1)` gives 990 x 990.
Mug: the steps of `reference/gen_mug.py` re-written in the page as a wrapper round `ZANS.printFile` (cap-band line at least 24 px; bitmap logo replaced by the traced horse + "ZANS RACING TOOLS" Jost 700 62 px; logo tab centred on width/2 and widened to fit; name plates held 6 mm inside top and bottom; opacity removed). New: `ZANS.printMaster(d, spec, font, LOGO)` = the same SVG with no `<style>`.

## Test results (local copy of the site, headless Chromium; scripts in `docs/print-fix-v3-test/`)
| Check | Bauble x3 (Loussiemoo, Zoo Olympios, Rexs Romance) | Mug (2475x1155 and 2582x1120) |
|---|---|---|
| `<image>` in master | none | none |
| `<style>` in master | none | none |
| opacity / filter | none | none |
| clip-path | none | n/a |
| thinnest stroke | 20 px | 14 px on the name-plate border (x1.05 scale = 14.7 px, 1.25 mm) - SAME as the v3 reference file; under the 1.5 mm rule, flagged, not changed |
| colours | design-code hexes + cap shading + brand cream/gold/ink only; nothing deepened | unchanged |
| size | PNG 990 x 990 from printFile(1) | SVG at both template sizes |
| v the v3 reference masters | every `<rect>` and `<circle>` identical; text is live `<text>` here, outlined paths in the reference (outlining is the render step's job) | every `<rect>` and `<g transform>` identical at both sizes (only "132.0" v "132" formatting differs) |
| page errors | 0 | 0 |

## Not done / to know
1. I could NOT run `print_selftest.py --strict`: it lives in the racing repo and needs a served URL. That is the products thread's step.
2. The racing green bauble (style B) is NOT covered: `fixC.js` only replaces `designA`. Style B still has its old lettering and filter.
3. `ZANS.printFile` on the mug page keeps its embedded font `<style>` so the on-screen mug still draws; only `printMaster` strips it. Say if the print pipeline should call `printFile` and I will flip that.
4. The traced horse logo is still "pending Alex's approval" in the port doc; both pages use it.
5. Mug text width is measured with the browser's own Jost; it matched the reference tab width (874.2 px) in my test once Jost had loaded.
6. CLAUDE.md is unchanged; the print rule waits for Alex's own yes.
No order, no spend, live pages untouched, racing repo not opened.
