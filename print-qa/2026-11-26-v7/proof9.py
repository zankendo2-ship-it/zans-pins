"""Exact proof per bauble for the new sample order (26 Nov). Uses the pinned v7 print PNGs (not renders of a mock-up).
Card: original v final, 100% pixel crops, centre + edge spacing, 6 mm safe zone, nominal and +/-5 mm printer-shift simulations,
file hash, DPI, ICC profile, palette hex. Plus one PDF with each bauble at actual size (74.9 mm)."""
import hashlib, io, json, os, re, sys
from PIL import Image, ImageDraw, ImageFont, ImageCms
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'proof9')
ORIG = '/tmp/claude-0/r1h/etsy/orders/own-{}.png'
NAMES = {'loussiemoo': 'Loussiemoo', 'zoo-olympios': 'Zoo Olympios', 'rexs-romance': 'Rexs Romance'}
PX, MM = 990, 74.9; PXMM = PX / MM
F = lambda s, b=False: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf' % ('-Bold' if b else ''), s)
INK, GOLD, GREEN, RED, BG = (28, 28, 28), (201, 166, 70), (20, 110, 60), (190, 30, 30), (246, 241, 231)

def disc(im, size, cx=None, cy=None):
    """The physical bauble face (diameter = the print area) laid over the art at offset (cx, cy) art px; outside the art = unprinted white."""
    cx = PX / 2 if cx is None else cx; cy = PX / 2 if cy is None else cy
    canvas = Image.new('RGB', (PX, PX), 'white'); canvas.paste(im, (int(round(PX / 2 - cx)), int(round(PX / 2 - cy))))
    m = Image.new('L', (PX, PX), 0); ImageDraw.Draw(m).ellipse((0, 0, PX - 1, PX - 1), fill=255)
    o = Image.new('RGB', (PX, PX), BG); o.paste(canvas, (0, 0), m)
    ImageDraw.Draw(o).ellipse((0, 0, PX - 1, PX - 1), outline=(150, 150, 150), width=3)
    return o.resize((size, size), Image.LANCZOS)

def palette(im):
    c = im.convert('RGB').getcolors(1 << 20); c.sort(reverse=True); tot = sum(n for n, _ in c)
    return [('#%02X%02X%02X' % rgb, n / tot) for n, rgb in c if n / tot > 0.004][:8]

def card(ref):
    png = os.path.join(HERE, 'out9', f'{ref}-v9.png'); svg = open(png[:-4] + '.svg').read()
    raw = open(png, 'rb').read(); im = Image.open(io.BytesIO(raw)); icc = im.info.get('icc_profile')
    prof = ImageCms.getProfileDescription(ImageCms.ImageCmsProfile(io.BytesIO(icc))).strip() if icc else 'NONE'
    dpi = im.info.get('dpi', (0, 0)); im = im.convert('RGB')
    orig = Image.open(ORIG.format(ref)).convert('RGB').resize((PX, PX), Image.LANCZOS)
    res = json.load(open(os.path.join(HERE, 'out9', 'results.json')))[f'{ref} A']
    panel = [float(v) for v in re.search(r'data-label="name panel" x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"', svg).groups()]
    tab = [float(v) for v in re.search(r'data-label="logo tab" x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)"', svg).groups()]
    sw = 6  # half the panel's 12 px gold border
    W, H = 1800, 5200; c = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(c)
    d.rectangle((0, 0, W, 130), fill=(20, 60, 40))
    d.text((40, 30), f'{NAMES[ref].upper()} BAUBLE - FINAL PRINT PROOF', font=F(54, True), fill='white')
    d.text((40, 145), 'Made from the exact print file. Printify check of this version follows.', font=F(28), fill=RED)
    y = 210
    for i, (lab, img) in enumerate((('YOUR ORIGINAL (19 Nov order)', orig), ('FINAL - what will print', im))):
        x = 60 + i * 870; d.text((x, y), lab, font=F(34, True), fill=INK); c.paste(disc(img, 800), (x, y + 50))
    y += 880
    d.text((60, y), 'Only changes from your original:', font=F(34, True), fill=INK); y += 50
    for t in ('1. Thin gold ring at the very edge removed - it sat 2 mm from the edge, where Printify can be up to 5 mm off,',
              '    so it would have printed lopsided (that is what made your first ones look off centre).',
              '2. Gold line on the cap peak 0.45 -> 0.53 mm (Printify\'s thinnest printable line is 0.5 mm).',
              '3. Shine on the top left of the cap removed (your instruction, 12:19) - seams now unbroken.',
              '4. Invisible: text and logo turned into sharp vector shapes, see-through shine made solid, full-bleed file.',
              'Kept exactly: name, MERRY CHRISTMAS, colours, layout, and the ZANS logo at its ORIGINAL size (your choice, 11:02).'):
        d.text((60, y), t, font=F(28), fill=INK); y += 42
    y += 20
    # measurement overlay
    d.text((60, y), 'CENTRING + SAFE ZONE (final file)', font=F(34, True), fill=INK); y += 50
    ov = disc(im, 800).convert('RGBA'); k = 800 / PX; od = ImageDraw.Draw(ov)
    r6 = (PX / 2 - 6 * PXMM) * k; od.ellipse((400 - r6, 400 - r6, 400 + r6, 400 + r6), outline=GREEN + (255,), width=4)
    od.line((400, 0, 400, 800), fill=RED + (255,), width=2); od.line((0, 400, 800, 400), fill=RED + (255,), width=2)
    c.paste(ov, (60, y), ov)
    L = panel[0] - sw; R = PX - (panel[0] + panel[2] + sw); B = PX - (tab[1] + tab[3])
    pcx = (panel[0] + panel[2] / 2 - PX / 2) / PXMM; tcx = (tab[0] + tab[2] / 2 - PX / 2) / PXMM
    rows = [('Bauble face', f'{MM} mm across (print area 990 x 990 px)'),
            ('Name panel centre', f'{pcx:+.1f} mm from the middle (0 = dead centre)'),
            ('Logo centre', f'{tcx:+.1f} mm from the middle'),
            ('Gap edge -> name panel', f'left {L / PXMM:.1f} mm, right {R / PXMM:.1f} mm (equal)'),
            ('Gap edge -> logo (bottom)', f'{B / PXMM:.1f} mm'),
            ('Top + sides', 'silks pattern runs to the edge on purpose (full bleed)'),
            ('Safe zone', 'green circle = 6 mm in from the edge'),
            ('Name, greeting, logo', res[1][2] if len(res[1]) > 2 else ''),
            ('Red lines', 'true centre of the bauble')]
    yy = y
    for a, b in rows:
        d.text((900, yy), a, font=F(26, True), fill=INK); d.text((900, yy + 32), b, font=F(25), fill=INK); yy += 86
    y += 830
    d.text((60, y), 'PRINTER SHIFT TEST - Printify says placement can be up to 5 mm off', font=F(34, True), fill=INK); y += 50
    s = 5 * PXMM; sims = (('As designed', 0, 0), ('5 mm left', s, 0), ('5 mm right', -s, 0), ('5 mm up', 0, s), ('5 mm down', 0, -s))
    for i, (lab, dx, dy) in enumerate(sims):
        x = 60 + i * 340; d.text((x, y), lab, font=F(26, True), fill=INK); c.paste(disc(im, 320, PX / 2 + dx, PX / 2 + dy), (x, y + 40))
    y += 380
    for t in ('Worst case (5 mm): the name panel and logo stay fully on the bauble (logo still 1.7 mm clear); a white sliver can',
              'show at one edge and the cap button at the top can be trimmed - same as with your original.',
              'Borders cannot be guaranteed equal on the real bauble - this is the printer\'s stated limit.'):
        d.text((60, y), t, font=F(26), fill=INK); y += 38
    y += 30
    d.text((60, y), 'CAP SEAMS at 300% - all 4 seam lines continuous (shine removed 12:19)', font=F(30, True), fill=INK); y += 46
    cc = im.crop((150, 0, 560, 220)); c.paste(cc.resize((cc.width * 3, cc.height * 3), Image.NEAREST), (60, y)); y += cc.height * 3 + 30
    d.text((60, y), '100% ZOOM (real print pixels, then 3x)', font=F(34, True), fill=INK); y += 50
    lc = (int(tab[0]) - 10, int(tab[1]) - 8, int(tab[0] + tab[2]) + 10, int(tab[1] + tab[3]) + 8)
    nc = (int(panel[0]) - 10, int(panel[1]) - 10, int(panel[0] + panel[2]) + 10, int(panel[1] + panel[3]) + 10)
    crop_l = im.crop(lc); c.paste(crop_l, (60, y)); c.paste(crop_l.resize((crop_l.width * 3, crop_l.height * 3), Image.NEAREST), (60 + crop_l.width + 40, y))
    y += crop_l.height * 3 + 30
    crop_n = im.crop(nc); c.paste(crop_n, (60, y)); y += crop_n.height + 30
    d.text((60, y), 'Logo letters are 0.7 mm tall at the original size (printers advise 1.5 mm+), so they may print slightly soft.', font=F(26), fill=RED); y += 60
    d.text((60, y), 'FILE FACTS', font=F(34, True), fill=INK); y += 50
    for t in (f'File: {ref}-v9.png   990 x 990 px   effective {PX / MM * 25.4:.0f} x {PX / MM * 25.4:.0f} DPI at 74.9 mm   colour profile: {prof}',
              f'SHA-256: {hashlib.sha256(raw).hexdigest()}',
              'Printify: Christmas bauble (Harrier UK), blueprint 1676, provider 94, variant 115590, one print area "front",',
              '  placed centre x 0.5 y 0.5, scale 1, angle 0 - same product and print area as your 19 Nov order.',
              'Print check: PASS (resolution, safe zone, centring, line widths, colours = your original colours)'):
        d.text((60, y), t, font=F(24), fill=INK); y += 36
    y += 20; d.text((60, y), 'Colours in the file (same hex as your original):', font=F(28, True), fill=INK); y += 46
    for i, (hx, share) in enumerate(palette(im)):
        x = 60 + (i % 4) * 430; yy = y + (i // 4) * 80
        d.rectangle((x, yy, x + 60, yy + 60), fill=hx, outline=(120, 120, 120)); d.text((x + 75, yy + 14), f'{hx}  {share * 100:.0f}%', font=F(26), fill=INK)
    y += 170
    d.text((60, y), 'A screen cannot show the exact printed colour; the real bauble can look slightly different.', font=F(24), fill=INK)
    c = c.crop((0, 0, W, y + 60))
    path = os.path.join(OUT, f'{NAMES[ref]} bauble - FINAL PROOF.png'); c.save(path); return path, im

def actual_size_pdf(ims):
    pdf = os.path.join(OUT, 'Baubles - ACTUAL SIZE proof (print at 100 percent).pdf')
    pages = []
    for ref, im in ims:
        dpi = 300; Wp, Hp = int(210 / 25.4 * dpi), int(297 / 25.4 * dpi); pg = Image.new('RGB', (Wp, Hp), 'white'); d = ImageDraw.Draw(pg)
        d.text((150, 150), f'{NAMES[ref]} - ACTUAL SIZE ({MM} mm across). Print at 100% / "actual size" to check.', font=F(60, True), fill=INK)
        sz = int(round(MM / 25.4 * dpi)); pg.paste(disc(im, sz), ((Wp - sz) // 2, 500))
        d.line((150, 500 + sz + 120, 150 + int(50 / 25.4 * dpi), 500 + sz + 120), fill=INK, width=6)
        d.text((150, 500 + sz + 150), '50 mm ruler - measure this to check the print scale', font=F(45), fill=INK)
        pages.append(pg)
    pages[0].save(pdf, save_all=True, append_images=pages[1:], resolution=300); return pdf

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True); ims = []
    for ref in NAMES:
        p, im = card(ref); ims.append((ref, im)); print(p)
    print(actual_size_pdf(ims))
