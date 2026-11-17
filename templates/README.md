# Locked ZANS gift-post templates

Exact reference: `reference/locked-style/` (Ombudsman and Lossiemouth, Alex's chosen version). See CLAUDE.md section 3.7.

1. Add the post to `posts.json` (key, metal, colour, eyebrow, big, sub, question).
2. `node templates/render.js <cards_dir> <key>`
3. `python3 templates/video.py <cards_dir> <alex_uploaded_photo.png> <key> <cx> <cy> <snow|shimmer> <out_dir>`

Writes `<key>-video.mp4` and `<key>-slide1/2/3.png`.
Slide 1 is always Alex's uploaded photo, untouched. Never composite artwork onto a photo (CLAUDE.md, Section 0, rule 14).

Designer tree photos (taller than 4:5 are not available): capture with the website's own "On the Christmas tree" view at deviceScaleFactor 5, crop to 9:16 centred on the bauble, then run video.py with `ZANS_ZOOM=0.02 ZANS_KEEP_R=680` so the whole rim stays in frame and the light shimmer never touches the bauble. Slide 1 of the carousel is the same photo, untouched.
