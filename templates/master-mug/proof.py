"""Builds every proof picture for the master mug's sign-off into templates/master-mug/proof/. python3 templates/master-mug/proof.py"""
import subprocess, json, math, os
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__)); O = H + '/proof/'; T = '/tmp/master-mug-proof/'; os.makedirs(T, exist_ok=True); os.makedirs(O, exist_ok=True)
R = lambda out, v: subprocess.run(['node', H + '/render.js', out, json.dumps(v)], check=True, capture_output=True)
B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; f, f2, f3 = ImageFont.truetype(B, 26), ImageFont.truetype(B, 40), ImageFont.truetype(B, 30); BG = (238, 236, 231); INK = (28, 28, 28)
views = [("FRONT, HANDLE LEFT", dict(az=0, el=5)), ("BACK, HANDLE RIGHT", dict(az=180, el=5)), ("HANDLE SIDE", dict(az=90, el=5)), ("OPPOSITE THE HANDLE", dict(az=-90, el=5)),
         ("THREE-QUARTER, LEFT", dict(az=30, el=30)), ("THREE-QUARTER, RIGHT", dict(az=150, el=30)), ("FROM ABOVE", dict(az=0, el=62)), ("LOW ANGLE", dict(az=20, el=1))]
C = 640; sheet = Image.new('RGB', (4*C, 3*(C + 40) + 100), BG); d = ImageDraw.Draw(sheet); d.text((30, 24), "ZANS MASTER MUG - BLANK, ALL ANGLES (no artwork)", fill=INK, font=f2)
for i, (name, v) in enumerate(views):
    p = T + f"v{i}.png"; v.update(flat=None, drink=False, fov=10, w=900, h=900, fill=0.78); R(p, v)
    a = Image.open(p).convert('RGBA').resize((C, C), Image.LANCZOS); x, y = (i % 4)*C, 90 + (i//4)*(C + 40); sheet.paste(a, (x, y), a); d.text((x + 24, y + C - 4), name, fill=INK, font=f)
Rr = 4.1
for i, (name, az, cy) in enumerate([('TOP JOINT, CLOSE', 20, 8.1), ('BOTTOM JOINT, CLOSE', 20, 3.0), ('TOP JOINT, OTHER SIDE', 160, 8.1), ('BOTTOM JOINT, OTHER SIDE', 160, 3.0)]):
    a = math.radians(az); p = T + f"c{i}.png"; R(p, dict(flat=None, drink=False, az=az, el=14, fov=10, w=900, h=900, fill=3.0, cx=-Rr*math.cos(a)*1.05, cy=cy, cz=Rr*math.sin(a)*1.05))
    a = Image.open(p).convert('RGBA').resize((C, C), Image.LANCZOS); x, y = i*C, 90 + 2*(C + 40); a = a.crop((40, 40, C - 40, C - 80)); sheet.paste(a, (x + 40, y + 20), a); d.rectangle([x + 38, y + 18, x + C - 38, y + C - 98], outline=(150, 150, 150), width=3); d.text((x + 40, y + C - 80), name, fill=INK, font=f)
sheet.save(O + 'MASTER-MUG-BLANK-all-angles.jpg', quality=92); sheet.resize((1080, int(sheet.height*1080/sheet.width)), Image.LANCZOS).save(O + 'MASTER-MUG-BLANK-all-angles-PHONE-1080.jpg', quality=90)
A = dict(az=26, el=36, fov=54, w=1400, h=1400, fill=0.75); R(T + 'plain.png', dict(A, flat=None, shadow=False)); R(T + 'print.png', dict(A, flat=H + '/../mug-flats/fact-to-file.png', shadow=False))
print(subprocess.run(['python3', H + '/overlay.py', T + 'plain.png', O + 'MASTER-MUG-overlay-on-real-photo.jpg'], capture_output=True, text=True).stdout)
subprocess.run(['python3', H + '/overlay.py', T + 'print.png', T + 'x.jpg', O + 'MASTER-MUG-half-and-half-blend-on-real-photo.jpg'], check=True)
def fit(p, h):
    a = Image.open(p).convert('RGBA'); a = a.crop(a.getbbox()); k = h/a.height; return a.resize((int(a.width*k), h), Image.LANCZOS)
real = Image.open(H + '/../../reference/real-mug-fact-to-file.jpg').convert('RGB').crop((40, 120, 860, 900)).resize((900, 856)); o = Image.new('RGB', (1800, 920), BG); o.paste(real, (0, 32)); d = ImageDraw.Draw(o)
R(T + 'nat.png', dict(flat=None, az=26, el=24, fov=10, w=1400, h=1400, fill=0.8)); a = fit(T + 'nat.png', 700); o.paste(a, (900 + (900 - a.width)//2, 110), a)
for i, t in enumerate(["ALEX'S REAL MUG (phone held close, above)", "MASTER MUG, BLANK"]): d.text((30 + i*900, 880), t, fill=INK, font=f3)
o.save(O + 'MASTER-MUG-next-to-real-photo.jpg', quality=92); o.resize((1080, 552), Image.LANCZOS).save(O + 'MASTER-MUG-next-to-real-photo-PHONE-1080.jpg', quality=90)
R(T + 'sideov.png', dict(flat=None, drink=False, shadow=False, az=0, el=3, fov=8, w=1400, h=1400, fill=0.72, cx=-1.2)); subprocess.run(['python3', H + '/overlay_side.py', T + 'sideov.png', O + 'MASTER-MUG-outline-on-supplier-11oz-photo.jpg'], check=True)
R(T + 'side.png', dict(flat=None, az=0, el=4, fov=20, drink=False, w=1400, h=1400, fill=0.72, cx=-1.2))
l = Image.open(H + '/../../reference/mug-shape-11oz-alex-2026-11-19.jpg').convert('RGB').crop((40, 560, 880, 1440)).resize((859, 900)); a = fit(T + 'side.png', 640); o2 = Image.new('RGB', (1800, 960), (240, 240, 238)); o2.paste(l, (20, 10)); o2.paste(a, (900 + (900 - a.width)//2, 150), a)
d = ImageDraw.Draw(o2); d.text((30, 920), "11oz SHAPE REFERENCE", fill=INK, font=f3); d.text((930, 920), "MASTER MUG, SIDE ON", fill=INK, font=f3); o2.save(O + 'MASTER-MUG-side-on-next-to-11oz-reference.jpg', quality=92)

# the join on the real mug beside the model's join, same close phone camera
R(T + 'join.png', dict(A, flat=None, shadow=False, w=2800, h=2800))
a = Image.open(T + 'join.png').convert('RGBA'); bb = a.getbbox(); a = a.crop(bb); k = 655/(a.height); a = a.resize((int(a.width*k*2), int(a.height*k*2)), Image.LANCZOS)   # real mug is 655 px high in the photo; x2 like the real crop
rj = Image.open(H + '/../../reference/real-mug-fact-to-file.jpg').convert('RGB').crop((89, 280, 400, 720)).resize((622, 880))
bgj = Image.new('RGB', (622, 880), BG); bgj.paste(a, (0, -(280 - 168)*2), a); o3 = Image.new('RGB', (1284, 950), BG); o3.paste(rj, (10, 10)); o3.paste(bgj.crop((0, 0, 622, 880)), (652, 10)); d = ImageDraw.Draw(o3)
d.text((20, 900), "REAL MUG: where the handle joins", fill=INK, font=f); d.text((662, 900), "MASTER MUG: same place, same camera", fill=INK, font=f); o3.save(O + 'MASTER-MUG-handle-join-real-v-model.jpg', quality=92)
