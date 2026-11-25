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

## FIXES DONE - style B (racing green bauble) ported (25 Nov 2026, 21:00 UTC) - TASK 8e0e73e
In `docs/bauble-designer-v2/index.html` only; a new `designB` sits beside the style A fix. Test script `testB.js` and three sample masters (`v2B-*.svg`) are in this folder.
- [x] 1. No `<filter>`, no `<image>`, no opacity (checked on 5 names). The old gold halo filter is replaced by the jersey's own outline, thickened and drawn in gold #C9A646.
- [x] 2. Every stroke at least 20 px on the 990 px face (jersey outlines are scaled up so they land at 20 px after the jersey's own scale).
- [x] 3. MERRY CHRISTMAS 66 px Jost 700 = 3.5 mm letters. Name fitted to 720 px wide, up to 150 px font: Rex 7.9 mm, Loussiemoo 6.0 mm, Starry Night 5.6 mm, No Drama This End (two lines) 5.3 mm, Inothewayurthinkin 3.4 mm.
- [x] 4. Colours: background registry racing green #0F3B2C; gold #C9A646, cream #F6F1E7 and ink #1C1C1C from style A; plus the design-code silks hexes. #E4E2D8 is gone (it came from the 92% see-through logo tab over green).
- [x] 5. Same vector horse mark in a cream tab; key content 6.1 to 7.2 mm inside the edge on all five; top of the jersey cap at 164 px, clear of the 12 mm (158 px) hanging-hole zone; both thin gold rings near the edge removed; `printMaster()` is full bleed with no outer clip.
- [x] Style A re-tested after the change: unchanged, 0 page errors.
NOT met, flagged: the name is under 6 mm for anything longer than about 10 letters on one line (Starry Night 5.6, two-line names about 5.3, an 18-letter single word 3.4). DESIGNER_PORT.md's own floor for bauble names is 4.0 mm, which all but the 18-letter word meet. Style A has the same limit for very long single words. Someone needs to decide: cap the name length for baubles, or accept the 4.0 mm floor and block shorter.
The jersey still uses inner clip-paths to hold each pattern inside its shape (as on the mug); only the outer round clip is removed.
Not served: same as before, the two `-v2` folders need copying onto the published branch for the --strict run.

## FIXES DONE (2) - style B, ADVICE 74c6148 (25 Nov 2026, 21:40 UTC)
Fresh files in this folder: `v2B-starry-night.png/.svg`, `v2B-loussiemoo.png/.svg`, `v2B-no-drama-this-end.png/.svg`, `v2B-rex.png/.svg`, sheet `v2B-four-samples-sheet.jpg`, updated `testB.js`.
- [x] 1. Cap: the cap clip was two shapes (crown + peak) in one clipPath; it is now ONE combined path, so the cap colour stays inside the cap in any renderer. In my Chromium render the cap reads as a cap on all four samples. I could not reproduce the square block here (Chromium drew the two-shape clip correctly), so please confirm in your renderer.
- [x] 2. Gold outline is now BEHIND the jersey: a gold copy of every outline shape, filled and stroked 40 px, underneath; the silks sit on top at full size with no line over them. 20 px of gold shows outside each shape. The thin ink outlines (7 units = about 3 px on the face) are removed, because they were under the 20 px rule; sleeves and body of the same colour now meet with no line between them.
- [x] 3. Name floor for BOTH styles, fail closed: if the name would print under 4.0 mm (53 px capital height), the page shows "Name too long - please shorten" under the name box, and `ZANSBauble.printFile()` and `ZANSBauble.printMaster()` throw that error, so no file is made. `ZANSBauble.nameOK()` returns true/false. In `testB.js`: "Inothewayurthinkin" is BLOCKED in style B and in style A; the other four pass (5.3 to 7.9 mm).
- [x] Re-tested: no filter, image or opacity; key content 6.1 to 7.2 mm inside the edge; cap top 164 px; style A masters for the 3 printed baubles unchanged; 0 page errors.
To know: `fixC.js` (style A) dropped the special Cross of Lorraine layout the live designer has (one big cross with the name plate as its lower bar); on the preview that pattern now uses the standard name panel. That came with the reference file; flagging it, not changing it.
