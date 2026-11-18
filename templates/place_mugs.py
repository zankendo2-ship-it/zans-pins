"""Stand the exact ZANS mug renders (templates/mug3d.js: the website designer's own 3D model with the real print) on an empty table in a FLUX photo.
Usage: python3 templates/place_mugs.py <photo> <out.png> <spec.json>
spec: {"tint": [r,g,b], "mugs": [{"png": "...", "cx": x, "base": y, "h": height}, ...]}  (cx/base/h in the photo's own pixels; photo enlarged 1.5x)."""
import json, sys, numpy as np
from PIL import Image, ImageFilter, ImageDraw
UP = 1.5
def build(photo, out, spec):
    bg = Image.open(photo).convert('RGB'); bg = bg.resize((round(bg.width*UP), round(bg.height*UP)), Image.LANCZOS)
    tint = np.array(spec.get('tint', [1, 1, 1]), np.float32)
    for m in spec['mugs']:
        mug = Image.open(m['png']).convert('RGBA'); mug = mug.crop(mug.getbbox())
        a = np.asarray(mug)[..., 3]; body = np.where(a.sum(axis=1) > a.sum(axis=1).max()*0.5)[0]       # rows where the body (not just the handle) is
        H = round(m['h']*UP); k = H/mug.height; mug = mug.resize((round(mug.width*k), H), Image.LANCZOS)
        a = np.asarray(mug)[..., 3]; cols = np.where(a[int(H*0.5)] > 128)[0]
        rows = np.where(a[:, a.shape[1]//2] > 128)[0]; bot = rows.max()
        # body centre: handle sticks out one side, so use the body's own columns near the bottom
        bc = np.where(a[int(H*0.10)] > 128)[0]; bcx = (bc.min()+bc.max())/2; bw = float(bc.max()-bc.min()); bcx = float(bcx); bot = int(bot)
        x0 = round(m['cx']*UP - bcx); y0 = round(m['base']*UP - bot)
        # contact shadow: a soft dark ellipse under the base, plus a wider faint one
        sh = Image.new('L', bg.size, 0); d = ImageDraw.Draw(sh); cx, by = m['cx']*UP, m['base']*UP - bw*0.06
        d.ellipse([cx-bw*0.53, by-bw*0.10, cx+bw*0.53, by+bw*0.115], fill=255); sh1 = sh.filter(ImageFilter.GaussianBlur(bw*0.022))
        dx, dy = spec.get('cast', [0.0, 0.0])                                                  # a longer soft shadow thrown away from the light (in body widths)
        if dx or dy:
            sc = Image.new('L', bg.size, 0); dc = ImageDraw.Draw(sc)
            for i in range(12):
                k = i/11; dc.ellipse([cx-bw*0.5+dx*bw*k, by-bw*0.09+dy*bw*k, cx+bw*0.5+dx*bw*k, by+bw*0.12+dy*bw*k], fill=int(150*(1-k*0.75)))
            sh1 = Image.fromarray(np.maximum(np.asarray(sh1), np.asarray(sc.filter(ImageFilter.GaussianBlur(bw*0.06)))))
        sh2 = Image.new('L', bg.size, 0); d = ImageDraw.Draw(sh2); d.ellipse([cx-bw*0.75, by-bw*0.12, cx+bw*0.85, by+bw*0.22], fill=150); sh2 = sh2.filter(ImageFilter.GaussianBlur(bw*0.12))
        b = np.asarray(bg).astype(np.float32); s = np.maximum(np.asarray(sh1), np.asarray(sh2)).astype(np.float32)[..., None]/255
        bg = Image.fromarray((b*(1-0.88*s)).clip(0, 255).astype(np.uint8))
        g = np.asarray(mug).astype(np.float32); rgb = g[..., :3]/255
        yy = np.linspace(0, 1, H)[:, None, None]; rgb = rgb*tint*(1.0 - 0.10*yy)                           # scene light, a touch darker towards the table
        xs = (np.arange(mug.width) - bcx)/(bw/2); inb = (np.abs(xs) <= 1)                                    # round the body: darker towards its edges, a soft glaze streak
        cyl = np.where(inb, 0.74 + 0.26*np.sqrt(np.clip(1 - xs*xs, 0, 1)), 1.0)[None, :, None]
        streak = (np.exp(-((xs + 0.42)/0.10)**2)*0.16 + np.exp(-((xs - 0.62)/0.05)**2)*0.07)*inb
        rgb = rgb*cyl + streak[None, :, None]*np.array(spec.get('glint', [1, 1, 1]), np.float32)
        tb = np.asarray(bg).astype(np.float32)[int(min(m['base']*UP + 20, bg.height-1)), max(0, int(cx - bw/2)):int(cx + bw/2)].mean(axis=0)/255   # table colour just in front of the mug
        bounce = np.clip((yy - 0.62)/0.38, 0, 1)**1.6 * spec.get('bounce', 0.30)                                                                         # the table reflecting in the glaze near the base
        rgb = rgb*(1 - bounce) + (rgb*0.35 + tb*0.65)*bounce
        rgb = rgb + np.random.default_rng(5).normal(0, 0.012, rgb.shape[:2])[..., None]                                                                  # the photo's grain
        mug = Image.fromarray(np.dstack([(rgb.clip(0, 1)*255), g[..., 3:]]).astype(np.uint8), 'RGBA').filter(ImageFilter.GaussianBlur(spec.get('soft', 0.8)))
        bg.paste(mug, (x0, y0), mug)
    bg.save(out)
if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2], json.load(open(sys.argv[3])))
