"""Rebuild the mug designer's built-in Tailwind CSS from the page's own classes.

Since 4 Nov 2026 the designer page no longer loads the Tailwind Play CDN script (it compiled the CSS on every
visitor's phone before anything showed). The same CSS is prebuilt with Tailwind CLI 3.4.17 and sits inside
<style id="zans-tw">...</style> in docs/mug-designer/index.html.

If you add or change Tailwind classes on that page, the CSS has to be rebuilt:

    python3 tools/designer-speed/swap_css.py docs/mug-designer/index.html

Needs Node (npx downloads tailwindcss@3.4.17). The GitHub workflow .github/workflows/designer-css.yml runs this
automatically on every push to the live branch that touches the designer page, commits the result and asks
GitHub Pages to rebuild, so a forgotten rebuild is fixed within about a minute.

Classes written inside JavaScript strings are picked up too (Tailwind reads the whole file as text).
"""
import os
import re
import subprocess
import sys
import tempfile

BANNER = "/*! tailwindcss v3.4.17 | MIT License | https://tailwindcss.com */"
# Plain words in the page (ids, SVG attributes, comments) that are not classes on any element. Left out of the CSS
# so it matches what the CDN made; a word is kept in the CSS again as soon as the page uses it as a class.
BLOCK = ["ring", "!ring", "filter", "transform", "hidden", "sticky"]
OPEN = '<style id="zans-tw">'


def class_tokens(html):
    toks = set()
    for m in re.finditer(r'class(?:Name)?\s*=\s*["\']([^"\']*)["\']', html):
        toks.update(m.group(1).split())
    for m in re.finditer(r'classList\.(?:add|toggle|remove|replace)\(([^)]*)\)', html):
        toks.update(re.findall(r'["\']([^"\']+)["\']', m.group(1)))
    return toks


def main(path):
    html = open(path, encoding="utf-8").read()
    if html.count(OPEN) != 1:
        sys.exit("swap_css: expected exactly one %s block in %s" % (OPEN, path))
    a = html.index(OPEN) + len(OPEN)
    b = html.index("</style>", a)
    old_css = html[a:b]
    scan = html[:a] + html[b:]  # the page without its own CSS, so CSS text is not read as classes
    used = class_tokens(scan)
    block = [w for w in BLOCK if w not in used]
    with tempfile.TemporaryDirectory() as d:
        open(os.path.join(d, "page.html"), "w", encoding="utf-8").write(scan)
        open(os.path.join(d, "in.css"), "w").write("@tailwind base;\n@tailwind components;\n@tailwind utilities;\n")
        open(os.path.join(d, "tailwind.config.js"), "w").write(
            "module.exports = { content: ['./page.html'], theme: { extend: {} }, plugins: [], blocklist: %r }\n" % block)
        subprocess.run(["npx", "-y", "tailwindcss@3.4.17", "-c", "tailwind.config.js", "-i", "in.css",
                        "-o", "out.css", "--minify"], cwd=d, check=True, capture_output=True)
        css = open(os.path.join(d, "out.css"), encoding="utf-8").read().strip()
    if not css.startswith("/*!"):
        css = BANNER + css
    if len(css) < 2000 or "--tw-" not in css:
        sys.exit("swap_css: the rebuilt CSS looks wrong (%d chars) - page not changed" % len(css))
    if css == old_css:
        print("swap_css: CSS already up to date (%d chars)" % len(css))
        return
    open(path, "w", encoding="utf-8").write(html[:a] + css + html[b:])
    print("swap_css: CSS rebuilt, %d -> %d chars" % (len(old_css), len(css)))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "docs/mug-designer/index.html")
