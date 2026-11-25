# Bauble print QA: original production files (evidence, unaltered)

These are the exact PNGs uploaded to Printify for Alex's 3 own-sample ceramic baubles. The source is a private branch of the racing repo, claude/project-thread-1htexo at fc476bdd, under etsy/orders/. They are copied here byte-for-byte; sha256 below. Nothing has been corrected.

| File | Bauble | Pixels | Mode | ICC | sha256 (first 16) |
|---|---|---|---|---|---|
| originals/own-loussiemoo.png | Lossiemouth-colours personalised "LOUSSIEMOO" | 3960x3960 | RGBA | none | b9ad959f3ae3e469 |
| originals/own-rexs-romance.png | "REXS ROMANCE" | 3960x3960 | RGBA | none | ba9c01b173e37afc |
| originals/own-zoo-olympios.png | "ZOO OLYMPIOS" | 3960x3960 | RGBA | none | 9c1e598861f799e8 |

- Product: Printify blueprint 1676 (round ceramic bauble 2.95"), provider 94 Harrier (UK), variant 115590. This is the same product as the live listings.
- Placement: one print area "front" only, image centred x 0.5 / y 0.5, scale 1, angle 0. There is no separate back file: the design is printed once.
- Effective DPI: 3960 px over 2.95 in is about 1,342 DPI.
- Source: drawn as vector and rasterised at 4x. No separate vector master file was kept in the repo (the build script draws it).
- For each file there are 100% crops (`_CROP100_top-edge`, `_centre`, `_bottom-edge`; each 1200 px wide, unscaled) and a `_PREVIEW_1200.jpg` downscale for quick viewing.
- Not included here:
  - Printify order and product IDs, and the delivery address. These are private.
  - Placement screenshots from the Printify UI. The upload was made through the API, so there was no UI step to screenshot.
  - Alex's physical sample photos. These are his; ask him before they are posted publicly.
- Measured faults: see the root-cause comment on #26 (7168896556).
