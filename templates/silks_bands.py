"""Version B of the hook card (slide 2): the cap colour as a band directly under the top metal strip, and the silks
colours (with their pattern) as a band directly above the bottom metal strip.  Usage: python3 templates/silks_bands.py <cards_dir> <key ...>
Rewrites <key>-4x5-hook.png and <key>-9x16-hook.png in place; silks come from posts.json ("silks": body, second, pattern, cap)."""
import sys, json, os, math
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); POSTS = json.load(open(f'{HERE}/posts.json'))
EDGE = {'gold': '#B98A36', 'silver': '#A9AFB6'}
def silks_band(w, h, s):
    k = 3; im = Image.new('RGB', (w*k, h*k), s['body']); d = ImageDraw.Draw(im); H = h*k
    if s['pattern'] == 'hoops':
        n = 5
        for i in range(n):
            if i % 2: d.rectangle([0, round(i*H/n), w*k, round((i+1)*H/n)], fill=s['second'])
    elif s['pattern'] == 'quartered':
        n = 12
        for i in range(n):
            for j in range(2):
                if (i + j) % 2: d.rectangle([round(i*w*k/n), round(j*H/2), round((i+1)*w*k/n), round((j+1)*H/2)], fill=s['second'])
    elif s['pattern'] == 'sash':
        n = 3; sw = w*k/n
        for i in range(-1, n+1): d.polygon([(i*sw, H), (i*sw+sw*0.42, H), (i*sw+sw*1.02, 0), (i*sw+sw*0.60, 0)], fill=s['second'])
    elif s['pattern'] in ('discs', 'stars'):
        n = 9; r = H*0.27
        for i in range(n):
            cx = (i+0.5)*w*k/n; cy = H/2
            if s['pattern'] == 'discs': d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=s['second'])
            else:
                R = r*1.25; pts = [(cx + (R if j % 2 == 0 else R*0.42)*math.sin(j*math.pi/5), cy - (R if j % 2 == 0 else R*0.42)*math.cos(j*math.pi/5)) for j in range(10)]
                d.polygon(pts, fill=s['second'])
    return im.resize((w, h), Image.LANCZOS)
def apply(cards, key):
    P = POSTS[key]; s = P['silks']; edge = EDGE[P.get('metal', 'gold')]
    for fmt, bh in (('4x5', 96), ('9x16', 120)):
        f = f'{cards}/{key}-{fmt}-hook.png'; im = Image.open(f).convert('RGB'); W, H = im.size; d = ImageDraw.Draw(im)
        top0 = 72; bot1 = H - 72                       # under the top metal strip / above the bottom metal strip
        s2 = P.get('silks2')                            # head-to-head: first horse's silks on top, second horse's at the bottom
        if s2: im.paste(silks_band(W, bh, s), (0, top0))
        else: d.rectangle([0, top0, W, top0+bh], fill=s['cap'])
        d.rectangle([0, top0+bh, W, top0+bh+5], fill=edge)
        im.paste(silks_band(W, bh, s2 or s), (0, bot1-bh)); d.rectangle([0, bot1-bh-6, W, bot1-bh-1], fill=edge)
        im.save(f)
def apply_end(src, out, key):
    """Face-off end card (Alex, 19 Nov 2026): both horses' silks as bands just inside the metal strips. python3 templates/silks_bands.py --end <end.png> <out.png> <key>"""
    P = POSTS[key]; s = P['silks']; s2 = P.get('silks2') or s; edge = EDGE[P.get('metal', 'gold')]
    im = Image.open(src).convert('RGB'); W, H = im.size; d = ImageDraw.Draw(im); bh = 120 if H > 1500 else 96; top0 = 72; bot1 = H - 72
    im.paste(silks_band(W, bh, s), (0, top0)); d.rectangle([0, top0+bh, W, top0+bh+5], fill=edge)
    im.paste(silks_band(W, bh, s2), (0, bot1-bh)); d.rectangle([0, bot1-bh-6, W, bot1-bh-1], fill=edge); im.save(out)
if __name__ == '__main__':
    if sys.argv[1] == '--end': apply_end(*sys.argv[2:5]); sys.exit()
    for k in sys.argv[2:]: apply(sys.argv[1], k)
