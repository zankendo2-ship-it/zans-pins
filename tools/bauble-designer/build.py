"""Build docs/bauble-designer/index.html from the mug designer's head/CSS + silks engine + bauble.js.
Run from repo root: python3 tools/bauble-designer/build.py"""
import re, base64, json, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
mug = (root / 'docs/mug-designer/index.html').read_text()
here = pathlib.Path(__file__).parent
head = mug[:mug.index('<div class="strip"></div>')]
scripts = re.findall(r'<script[^>]*>(.*?)</script>', mug, flags=re.S)
engine = next(s for s in scripts if 'ZANS silks drawing engine' in s)
metricool = next(s for s in scripts if 'tracker.metricool.com' in s)
URL = 'https://www.zanshorseracing.co.uk/bauble-designer/'
TITLE = 'Personalised Horse Racing Christmas Bauble in Your Silks | ZANS'
DESC = "Design a personalised horse racing Christmas bauble in your own jockey silks with your horse's name, then see it on a Christmas tree. Printed in the UK."
head = re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', head)
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', head)
head = head.replace('https://www.zanshorseracing.co.uk/mug-designer/', URL)
head = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="Personalised Horse Racing Christmas Bauble in Your Silks">', head)
head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{DESC}">', head)
# schema: breadcrumb for this page
schema = {"@context": "https://schema.org", "@graph": [{"@type": "BreadcrumbList", "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.zanshorseracing.co.uk/"},
    {"@type": "ListItem", "position": 2, "name": "Horse racing gifts", "item": "https://www.zanshorseracing.co.uk/horse-racing-gifts/"},
    {"@type": "ListItem", "position": 3, "name": "Silks bauble designer", "item": URL}]},
    {"@type": "WebPage", "name": "Personalised Horse Racing Christmas Bauble Designer", "url": URL, "description": DESC}]}
head = re.sub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">' + json.dumps(schema) + '</script>', head, count=1, flags=re.S)
head = head.replace('<!-- Tailwind CSS is built into this page', '<!-- Bauble designer: built by tools/bauble-designer/build.py from the mug designer CSS. Only reuse Tailwind classes the mug page already has; new styles go in the bauble <style> block. Tailwind CSS is built into this page')
logo = 'data:image/png;base64,' + base64.b64encode((here / 'logo_wide_750.png').read_bytes()).decode()
css = (here / 'bauble.css').read_text()
body = (here / 'body.html').read_text()
js = (here / 'bauble.js').read_text().replace('const Z = window.ZANS;', 'const Z = window.ZANS;\nconst LOGO_WIDE = ' + json.dumps(logo) + ';', 1)
out = head + f'<style>{css}</style>\n' + body + f'\n<script>{engine}</script>\n<script>{js}</script>\n\n<!-- Metricool visit counter (same as the home page) -->\n<script>{metricool}</script>\n</body></html>\n'
p = root / 'docs/bauble-designer/index.html'; p.parent.mkdir(exist_ok=True); p.write_text(out)
print('wrote', p, len(out))
