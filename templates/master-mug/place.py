"""Stands master mugs (render.js, artwork wrapped) on an EMPTY table photo, with contact shadows and the room's light.
python3 templates/master-mug/place.py <table photo> <out.png> '<json>'
json: {"w":1296,"h":2304,"el":24,"tint":[1.0,0.965,0.91],"dim":0.9,"mugs":[{"flat":"templates/mug-flats/x.png","az":20,"x":430,"base":1560,"height":560}, ...]}  back mug first.
x = centre of the mug BODY, base = y of the bottom of the mug, height = mug height in pixels (bigger = nearer the camera)."""
import json, subprocess, sys, os, tempfile, numpy as np
from PIL import Image, ImageFilter, ImageDraw
H = os.path.dirname(os.path.abspath(__file__)); table, out, sp = sys.argv[1], sys.argv[2], json.loads(sys.argv[3]); W, HH = sp.get('w', 1296), sp.get('h', 2304)
bg = Image.open(table).convert('RGB').resize((W, HH), Image.LANCZOS); tint = np.array(sp.get('tint', [1.0, 0.965, 0.91]), np.float32)*sp.get('dim', 0.9); tmp = tempfile.mkdtemp()
for i, m in enumerate(sp['mugs']):
    o = dict(flat=m.get('flat'), az=m['az'], el=sp.get('el', 24), fov=m.get('fov', 16), w=1600, h=1600, light='fire', shadow=False, fill=0.8, exposure=1.2)
    f = '%s/m%d.png' % (tmp, i); subprocess.run(['node', H + '/render.js', f, json.dumps(o)], check=True, stdout=subprocess.DEVNULL)
    a = np.asarray(Image.open(f)).astype(np.float32); al = a[..., 3] > 40; ys, xs = np.where(al)
    # the body (not the handle) sets the scale and the centre: use the widest run of rows near the base
    row = al[int(ys.max() - (ys.max() - ys.min())*0.06)]; bx = np.where(row)[0]; k = m['height']/(ys.max() - ys.min() + 1)
    rgb = a[..., :3]*tint; yy = (np.arange(a.shape[0])[:, None] - ys.min())/(ys.max() - ys.min()); xx = (np.arange(a.shape[1])[None, :] - bx.min())/(bx.max() - bx.min())
    rgb = rgb*(1.0 - 0.16*np.clip(yy, 0, 1))[..., None] * (0.86 + 0.2*np.clip(xx, 0, 1))[..., None] * (1 + np.array([0.16, 0.05, -0.05], np.float32)*np.clip(xx - 0.6, 0, 1)[..., None]*2.2)     # darker towards the table, lit from the fire side
    body = ((xx > 0.02) & (xx < 0.98))[..., None] * ((yy > 0.24) & (yy < 0.97))[..., None] * (a[..., :3].max(2) > 70)[..., None]; rgb = rgb + body*(np.exp(-((xx - 0.3)/0.035)**2)*46 + np.exp(-((xx - 0.86)/0.03)**2)*np.array([40, 22, 6], np.float32)[None, None, :].mean()*0.9)[..., None]   # the glaze: a soft strip of light down the body, and the fire on the other side
    im = Image.fromarray(np.dstack([np.clip(rgb, 0, 255), a[..., 3]]).astype(np.uint8), 'RGBA'); k = k*im.width/1600*1600/im.width; im = im.resize((round(im.width*k), round(im.height*k)), Image.LANCZOS)
    ox, oy = round(m['x'] - (bx.min() + bx.max())/2*k), round(m['base'] - ys.max()*k); bw = float((bx.max() - bx.min())*k)
    sh = Image.new('L', (W, HH), 0); d = ImageDraw.Draw(sh); ry = bw*0.20                                              # soft shadow thrown away from the fire, and a tight dark one right under the base
    d.ellipse([m['x'] - bw*1.75, m['base'] - ry*1.25, m['x'] + bw*0.5, m['base'] + ry*1.15], fill=175); sh = sh.filter(ImageFilter.GaussianBlur(bw*0.11))
    c = Image.new('L', (W, HH), 0); ImageDraw.Draw(c).ellipse([m['x'] - bw*0.53, m['base'] - ry*0.9, m['x'] + bw*0.53, m['base'] + ry*0.28], fill=215); c = c.filter(ImageFilter.GaussianBlur(bw*0.03))
    s = np.maximum(np.asarray(sh), np.asarray(c)).astype(np.float32)/255.0; b = np.asarray(bg).astype(np.float32)*(1 - 0.9*s[..., None]); bg = Image.fromarray(b.astype(np.uint8))
    bg.paste(im, (ox, oy), im)
bg.save(out); print('scene ->', out)
