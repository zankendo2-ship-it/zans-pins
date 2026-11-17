# Locked ZANS gift-post templates

Exact reference: `reference/locked-style/` (Ombudsman and Lossiemouth, Alex's chosen version). See CLAUDE.md section 3.7.

1. Add the post to `posts.json` (key, metal, colour, eyebrow, big, sub, question).
2. `node templates/render.js <cards_dir> <key>`
3. `python3 templates/video.py <cards_dir> templates/scenes/<key>.png <key> <cx> <cy> <snow|shimmer> <out_dir>`

Writes `<key>-video.mp4` and `<key>-slide1/2/3.png`.
