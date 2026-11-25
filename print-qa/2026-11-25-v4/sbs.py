from PIL import Image, ImageDraw, ImageFont
F = lambda n: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', n)
N = lambda n: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', n)
S = 560
rows = [('Loussiemoo', 'loussiemoo'), ('Zoo Olympios', 'zoo-olympios'), ('Rexs Romance', 'rexs-romance')]
cols = [('ORIGINAL - as approved and printed 19 Nov', '/tmp/claude-0/r1h/etsy/orders/own-{}.png'),
        ('CORRECTED A - same look, invisible fixes only', 'out/{}-v4A.png'),
        ('CORRECTED B - A + two legibility fixes', 'out/{}-v4B.png')]
W = 30 + 3 * (S + 30); H = 110 + 3 * (S + 60)
sh = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(sh)
d.text((30, 20), 'Baubles v4 - original approved artwork v corrected, same scale (full 990 px print square; the face is the circle)', fill='black', font=F(24))
d.text((30, 58), 'A: vector logo, flat colours, outlined text, edge ring removed.  B: A + MERRY CHRISTMAS 1.7 -> 3.5 mm letters + logo strip letters 0.7 -> 1.5 mm.', fill='#333', font=N(18))
for r, (nm, ref) in enumerate(rows):
    y = 110 + r * (S + 60)
    for c, (lab, pat) in enumerate(cols):
        im = Image.open(pat.format(ref)).convert('RGB').resize((S, S), Image.LANCZOS); x = 30 + c * (S + 30)
        m = Image.new('L', (S, S), 0); ImageDraw.Draw(m).ellipse((0, 0, S - 1, S - 1), fill=255)
        bg = Image.new('RGB', (S, S), '#EEEEEE'); bg.paste(im, (0, 0), m); sh.paste(bg, (x, y))
        ImageDraw.Draw(sh).ellipse((x, y, x + S - 1, y + S - 1), outline='#999999', width=2)
        d.text((x, y + S + 6), f'{nm} - {lab}', fill='black', font=N(15))
sh.save('pack/Baubles v4 original v corrected side by side.png'); print(sh.size)
