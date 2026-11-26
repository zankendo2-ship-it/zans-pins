"""Offline placement proof: each v5 print file on the Printify placeholder (size from Printify's own records), with guides."""
import json, sys
from PIL import Image, ImageDraw, ImageFont
F = lambda n: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', n)
N = lambda n: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', n)
def dashed_circle(d, c, r, col, w=3, n=120):
    import math
    for i in range(0, n, 2):
        a0, a1 = 2*math.pi*i/n, 2*math.pi*(i+1)/n
        d.arc((c-r, c-r, c+r, c+r), math.degrees(a0), math.degrees(a1), fill=col, width=w)
# ---- baubles
S = 990; pxmm = 990 / 74.93   # catalog: variant 115590 2.95'' x 2.95'' round, placeholder front 990 x 990, dye-sublimation
cells = []
for nm, ref in [('Loussiemoo', 'loussiemoo'), ('Zoo Olympios', 'zoo-olympios'), ('Rexs Romance', 'rexs-romance')]:
    im = Image.open(f'out5/{ref}-v5C.png').convert('RGB'); ov = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    c = S / 2
    d.rectangle((0, 0, S-1, S-1), outline=(0, 120, 255, 255), width=4)                     # placeholder = print area
    sh = 5 * pxmm; d.ellipse((c-c, c-c, S, S), outline=(255, 0, 0, 255), width=3)          # finished face edge
    d.ellipse((sh, sh, S-sh, S-sh), outline=(255, 120, 0, 255), width=3)                    # 5 mm shift band inner edge
    sf = 6 * pxmm; dashed_circle(d, c, c - sf, (0, 160, 0, 255), 4)                         # 6 mm safe zone
    d.line((c, 0, c, S), fill=(255, 0, 255, 200), width=2); d.line((0, c, S, c), fill=(255, 0, 255, 200), width=2)
    ko = 12 * pxmm; d.ellipse((c-ko, -ko, c+ko, ko), outline=(120, 0, 200, 255), width=3)  # hole / cap keep-out (estimate)
    out = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB'); cells.append((nm, out))
W = 3 * 520 + 40; H = 640 + 200
sheet = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(sheet)
d.text((20, 15), 'Baubles v5 - offline placement proof on the Printify placeholder (not a Printify mock-up)', fill='black', font=F(22))
for i, (nm, img) in enumerate(cells):
    x = 20 + i * 520; sheet.paste(img.resize((500, 500), Image.LANCZOS), (x, 60)); d.text((x, 565), nm + ' - x .5, y .5, scale 1', fill='black', font=N(16))
leg = ['BLUE square = Printify print area: blueprint 1676 / provider 94 / variant 115590, front placeholder 990 x 990 px, 2.95 in round, dye-sublimation (Printify catalog record).',
       'RED circle = finished round face (74.9 mm). ORANGE = 5 mm in from the edge (band a printer shift can move into). GREEN dashed = 6 mm safe zone (all key content inside).',
       'PINK lines = centre. PURPLE = 12 mm hole/cap keep-out at the top (OUR estimate - Harrier hole size not published).',
       'Full bleed: the artwork fills the whole square, so a shift shows more artwork, not a white strip, unless it exceeds the bleed past the circle.']
for j, t in enumerate(leg): d.text((20, 600 + j * 26), t, fill='#222', font=N(14))
sheet.save('pack5/Baubles v5 placement proof.png')
# ---- mugs
for w, h, mm, bp, pp, var, label in ((2475, 1155, 209.55, 635, 94, 72180, 'Harrier 11oz (bp 635 / pp 94)'), (2582, 1120, 218.6, 535, 6, 69010, 'T Shirt and Sons white 11oz (bp 535 / pp 6)')):
    im = Image.open(f'out5/fact-to-file-mug-{w}x{h}-v5.png').convert('RGBA'); ov = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    pxmm = w / mm
    d.rectangle((0, 0, w-1, h-1), outline=(0, 120, 255, 255), width=6)
    s6 = 6 * pxmm; d.rectangle((s6, s6, w-s6, h-s6), outline=(0, 160, 0, 255), width=5)
    d.line((w/2, 0, w/2, h), fill=(255, 0, 255, 220), width=4); d.line((0, h/2, w, h/2), fill=(255, 0, 255, 220), width=4)
    out = Image.alpha_composite(im, ov).convert('RGB')
    S2 = 1600 / w; sheet = Image.new('RGB', (1640, int(h * S2) + 230), 'white'); dd = ImageDraw.Draw(sheet)
    dd.text((20, 12), f'FACT TO FILE mug v5 - {label} - offline placement proof (not a Printify mock-up)', fill='black', font=F(20))
    sheet.paste(out.resize((1600, int(h * S2)), Image.LANCZOS), (20, 50)); y = 60 + int(h * S2)
    for j, t in enumerate([f'BLUE = Printify front placeholder {w} x {h} px, image at x .5, y .5, scale 1 (from our live Printify product record for this blueprint/provider).',
                           f'GREEN = 6 mm safe zone ({mm} mm wide print). PINK = centre lines. Name plates sit at the left/right ends (as in the original), all key content >= 6.2 mm inside every edge (preflight).',
                           'Where the handle falls is NOT in Printify\'s data we hold; the wrap seam is at the left/right edges. Handle position must be confirmed on the Printify mock-up / sample.']):
        dd.text((20, y + j * 26), t, fill='#222', font=N(15))
    sheet.save(f'pack5/FACT TO FILE mug v5 placement proof {w}x{h}.png')
print('ok')
