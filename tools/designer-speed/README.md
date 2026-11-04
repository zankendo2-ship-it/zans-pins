# Mug designer speed-up (4 Nov 2026)

The live designer page (docs/mug-designer/index.html) used to load the Tailwind Play CDN script, which compiles the
page's CSS on every visitor's phone before anything shows, and it redrew the 3D mug 60 times a second forever.

What changed (nothing visible; checked in real Chrome on phone, tablet and computer, every step, pixel for pixel):

1. CSS built in: the same Tailwind rules, prebuilt with Tailwind CLI 3.4.17 from the page's own classes, sit in
   `<style id="zans-tw">` after the page's main style block (exactly where the CDN put its CSS, so the cascade is the same).
2. three.min.js no longer holds up the first paint: `<link rel="preload" ... fetchpriority="low">` downloads it early,
   and `load3D()` runs it just after the page's first paint, then sets up the 3D mug (`start3D`). If it fails to load,
   the page shows the flat-print message as before.
3. The mug is drawn only while something changes (drag, turn, new design, resize), plus 3 frames after the last change.
   Anything that changes the mug calls `wake()`. Never call `loop()` directly (two drawing chains would draw every frame
   twice).

## Added a Tailwind class to the designer page?

Run `python3 tools/designer-speed/swap_css.py docs/mug-designer/index.html` before pushing (needs Node; npx fetches
tailwindcss@3.4.17). If you forget, `.github/workflows/designer-css.yml` does it on the live branch after your push,
commits the rebuilt CSS and asks GitHub Pages to rebuild (about a minute).

## Files

- `make_after.py` - one-off converter from the CDN version of the page (A = CSS where the CDN script was, B = after the
  main style block, the one published).
- `tw.min.css` - the first build of the CSS (7,130 characters).
- `swap_css.py` - rebuilds the CSS block from the page itself.
- `compare.cjs` + `.github/workflows/designer-compare.yml` - real-Chrome old v new comparison and Lighthouse runs
  (trigger: add a line to `request.txt` on branch claude/project-thread-oy3858). Reports in reports/designer-compare/.
