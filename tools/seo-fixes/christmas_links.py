"""Add the Christmas mug listing (Etsy 4609859882) to the gifts hub page.

Usage: python3 christmas_links.py <docs dir> <christmas photo png> <santa logo png>
- Secret Santa card: link to the Christmas listing.
- Christmas section: photo of three Christmas silks mugs, button to the Christmas
  listing, then the Santa-hat ZANS logo with "Wishing you a Merry Christmas"
  (Alex's rule for all Christmas content, 4 Nov 2026).
- Sitemap: the new photo is listed for the gifts page.
The Product schema stays on the main listing 4608193933.
"""
import sys
from pathlib import Path
from PIL import Image

docs, photo, logo = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
img = docs / "img"
XMAS = "https://www.etsy.com/uk/listing/4609859882"

im = Image.open(photo).convert("RGB")
for w in (600, 940, 1448):
    r = im.resize((w, round(im.size[1] * w / im.size[0])), Image.LANCZOS)
    r.save(img / f"christmas-mug-trio-{w}.webp", "WEBP", quality=80, method=6)
    if w == 940:
        r.save(img / "christmas-mug-trio-940.jpg", "JPEG", quality=82, optimize=True, progressive=True)
lg = Image.open(logo).convert("RGB").crop((357, 55, 1355, 884))  # the logo's own frame + a cream margin
for w in (260, 520):
    r = lg.resize((w, round(lg.size[1] * w / lg.size[0])), Image.LANCZOS)
    r.save(img / f"zans-christmas-logo-{w}.webp", "WEBP", quality=85, method=6)
    r.save(img / f"zans-christmas-logo-{w}.jpg", "JPEG", quality=85, optimize=True, progressive=True)

page = docs / "horse-racing-gifts" / "index.html"
s = page.read_text(encoding="utf-8")


def sub(old, new):
    global s
    assert s.count(old) == 1, (old[:70], s.count(old))
    s = s.replace(old, new)


sub('<p>£14.99 plus postage, ideal for the racing fan at work. Our racecourse guide PDFs are an instant-download stocking filler for racegoers too.</p><a href="/#guides">',
    '<p>£14.99 plus postage, ideal for the racing fan at work. Our racecourse guide PDFs are an instant-download stocking filler for racegoers too.</p>'
    f'<p><a href="{XMAS}" target="_blank" rel="noopener">See the Christmas mug on Etsy →</a></p><a href="/#guides">')

sub('''<section id="christmas"><div class="in">
<p class="eyebrow">Christmas delivery</p><h2>Order in time for Christmas</h2>
<p><b>We recommend ordering by Monday 7 December</b> for UK delivery before Christmas. Each mug is made to order in 3 to 5 working days, then posted from the UK. Etsy shows the delivery estimate for your order at checkout.</p>
</div></section>''',
    f'''<section id="christmas"><div class="in xmas">
<div>
<p class="eyebrow">Christmas delivery</p><h2>Order in time for Christmas</h2>
<p><b>We recommend ordering by Monday 7 December</b> for UK delivery before Christmas. Each mug is made to order in 3 to 5 working days, then posted from the UK. Etsy shows the delivery estimate for your order at checkout.</p>
<p>Shopping for Christmas? Our Christmas listing on Etsy is the same personalised silks mug.</p>
<a class="btn" href="{XMAS}" target="_blank" rel="noopener">See the Christmas mug on Etsy</a><a class="btn line" href="/mug-designer/">Design yours first</a>
</div>
<picture><source type="image/webp" srcset="/img/christmas-mug-trio-600.webp 600w, /img/christmas-mug-trio-940.webp 940w, /img/christmas-mug-trio-1448.webp 1448w" sizes="(max-width: 900px) calc(100vw - 32px), 500px"><img src="/img/christmas-mug-trio-940.jpg" alt="Horse racing Christmas gift: three personalised jockey silks mugs named ZEUS, MIKEL and SEA HORSE by a Christmas tree and a gift box" width="940" height="705" loading="lazy"></picture>
<div class="merry"><picture><source type="image/webp" srcset="/img/zans-christmas-logo-260.webp 1x, /img/zans-christmas-logo-520.webp 2x"><img src="/img/zans-christmas-logo-260.jpg" srcset="/img/zans-christmas-logo-520.jpg 2x" alt="ZANS Horse Racing logo in a Santa hat" width="260" height="216" loading="lazy"></picture><p>Wishing you a Merry Christmas</p></div>
</div></section>''')

sub('footer{background:#0c241a;',
    '.xmas{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:32px;align-items:center}\n'
    '.xmas>picture>img{width:100%;height:auto;border:1px solid var(--gold)}\n'
    '.merry{grid-column:1/-1;text-align:center}\n'
    '.merry img{width:220px;height:auto;border-radius:6px;background:var(--cream)}\n'
    '.merry p{font:600 15px var(--display);letter-spacing:.24em;text-transform:uppercase;color:var(--gold);margin:12px 0 0}\n'
    'footer{background:#0c241a;')
page.write_text(s, encoding="utf-8")

sm = docs / "sitemap.xml"
t = sm.read_text(encoding="utf-8")
old = '<image:loc>https://www.zanshorseracing.co.uk/img/silks-mugs-trio-1553.jpg</image:loc></image:image></url>\n  <url><loc>https://www.zanshorseracing.co.uk/mug-designer/</loc>'
assert t.count(old) == 1
t = t.replace(old, '<image:loc>https://www.zanshorseracing.co.uk/img/silks-mugs-trio-1553.jpg</image:loc></image:image>'
              '<image:image><image:loc>https://www.zanshorseracing.co.uk/img/christmas-mug-trio-940.jpg</image:loc></image:image></url>\n'
              '  <url><loc>https://www.zanshorseracing.co.uk/mug-designer/</loc>')
sm.write_text(t, encoding="utf-8")
print("ok")
