# REVIEW REQUEST: 21 guide thumbnails with thicker, edition-metal strips (TOP PRIORITY TASK c042493). Not uploaded.

Made 24 Nov 2026. This replaces my earlier small "layout proof" set (removed), which was built on the wrong, small website pictures.
Source: the 21 full-size 2700x2025 files in `assets/guide-thumbs-source-2026-11-23/` on `zans-social-notes` (de9af33).
Output: 21 files, same 2700x2025, named `<COURSE>-<CODE>-<Edition>-<listing id>-strip-62px-<edition>-metal.jpg`, JPEG quality 95.
The one change: the top and bottom strips are now 62 px (they measured 46 px), in the edition's metal: GOLD for Pro, SILVER for Advanced, BRONZE for Beginner. Each strip is a new metal gradient laid over the old strip and the 16 px of green beside it. Nothing else in any picture is touched.
- Phone tiles (4:5 centre crop of each): `GUIDE-THUMBNAILS-phone-tile-contact-sheet.jpg`, columns by course, rows Advanced, Beginner, Pro.
- Before and after of one strip at full size: `strip-before-46px-after-62px.jpg`.
Checked: all 21 present (7 courses x 3 editions); strip metal matches the edition word on each picture; course titles and "DIGITAL PDF DOWNLOAD" are whole in every phone tile; no text sits within 16 px of the old strip, so nothing is covered.
Notes: 62 px is about 3.1% of the 2025 px short side, which is above the 2.4% house size, as asked for these. Re-saving a JPEG costs a little quality; at quality 95 with no chroma subsampling I can see no change at full size. Ascot Flat is included as listing artwork only (its social promotion is paused).

## NEW HEADING (TOP PRIORITY TASK 440f5a4, rule 2A-13). This set replaces the strip-only set from cab43c8.
21 files, 2700x2025, JPEG quality 95: `<COURSE>-<TYPE>-<Edition>-<listing id>-heading-racecourse-guide-strip-62px-<edition>.jpg`. Phone tiles: `GUIDE-THUMBNAILS-new-heading-phone-tile-contact-sheet.jpg`. Builder: `build_heading.js`.
- Heading on every one: line 1 "<COURSE> <TYPE>" in the course's own title colour, line 2 "RACECOURSE GUIDE" in gold, e.g. AINTREE JUMPS / RACECOURSE GUIDE.
- One size for all 21: 128 px Jost bold, set by the longest, KEMPTON ALL-WEATHER, which measures 1556 px against the 1620 px phone crop.
- Cover picture reduced from 702x852 to 690x840 and moved up; edition box, "DIGITAL PDF DOWNLOAD" and the 62 px edition-metal strips kept.
How it was built: each picture is laid out afresh. The cover and the edition box are cut from the full-size source file; the green background is a new radial gradient matched to the source's centre and edge colours; the heading and the PDF line are new text.
To judge:
1. The heading is on two lines at 128 px. That is the largest that fits one line inside the phone crop, but it is SMALLER than the old course name (about 250 px). If "large" matters more than one line, a three-line heading (COURSE / TYPE / RACECOURSE GUIDE) could run at about 200 px.
2. The cover was barely shrunk, because the two-line heading takes less height than the old title did.
3. The background is rebuilt, so it is not pixel-identical to the source.
