"""Print designer artwork onto a photographed blank disc: trace the rim by radial edge scan, fit an ellipse, multiply-shade the art."""
import numpy as np
from PIL import Image, ImageFilter
W, H = 1296, 2304
def fit(lum, c0, r0, skip=()):
    g = np.asarray(Image.fromarray((lum*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))).astype(np.float32)/255
    pts = []
    for th in np.linspace(0, 2*np.pi, 360, endpoint=False):
        deg = np.degrees(th) % 360
        if any(a <= deg <= b for a, b in skip): continue
        rs = np.arange(0.6*r0, 1.35*r0, 1.0)
        xs = np.clip((c0[0]+rs*np.cos(th)).astype(int), 0, W-1); ys = np.clip((c0[1]+rs*np.sin(th)).astype(int), 0, H-1)
        v = g[ys, xs]; d = v[:-4]-v[4:]                      # bright disc -> darker outside
        i = int(np.argmax(np.abs(d))) + 2
        if abs(d[i-2]) > 0.04: pts.append((xs[i], ys[i]))
    P = np.array(pts, float)
    for _ in range(4):                                       # least-squares axis-aligned ellipse, drop outliers
        x, y = P[:, 0], P[:, 1]
        A = np.c_[x*x, y*y, x, y]; s = np.linalg.lstsq(A, np.ones(len(x)), rcond=None)[0]
        a_, b_, c_, d_ = s; cx = -c_/(2*a_); cy = -d_/(2*b_); k = 1 + a_*cx*cx + b_*cy*cy
        rx, ry = np.sqrt(k/a_), np.sqrt(k/b_)
        res = np.abs(np.hypot((x-cx)/rx, (y-cy)/ry) - 1)
        P = P[res < max(0.02, np.percentile(res, 80))]
    return cx, cy, rx, ry, len(pts)
def build(art_path, photo, c0, r0, out, skip=(), base=None):
    ph = Image.open(base or photo).convert('RGB').resize((W, H), Image.LANCZOS)
    src = np.asarray(Image.open(photo).convert('RGB').resize((W, H), Image.LANCZOS)).astype(np.float32)/255
    a = np.asarray(ph).astype(np.float32)/255
    lum = src @ np.array([.299, .587, .114], dtype=np.float32)
    cx, cy, rx, ry, n = fit(lum, c0, r0, skip)
    yy, xx = np.mgrid[0:H, 0:W]
    mx, mn = src.max(-1), src.min(-1); sat = (mx-mn)/(mx+1e-4)
    red = (src[..., 0] > 0.30) & (src[..., 0] > src[..., 1]*1.6) & (src[..., 0] > src[..., 2]*1.6)
    inside = ((xx-cx)/rx)**2 + ((yy-cy)/ry)**2 <= 0.985**2
    skin = (sat > np.percentile(sat[inside], 50) + 0.24) & ~red   # fingers, tissue, glass: anything far more coloured than the glaze
    ref = np.percentile(lum[inside & ~red & ~skin], 75)
    hole = (lum < ref*0.45) & (yy < cy - ry*0.6)
    disc = inside & ~red & ~skin & ~hole
    x0, x1, y0, y1 = int(cx-rx), int(cx+rx), int(cy-ry), int(cy+ry)
    art = Image.open(art_path).convert('RGBA').resize((x1-x0+1, y1-y0+1), Image.LANCZOS)
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0)); canvas.paste(art, (x0, y0))
    A = np.asarray(canvas).astype(np.float32)/255
    dm = Image.fromarray((disc*255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.4))
    alpha = (np.asarray(dm).astype(np.float32)/255)*A[..., 3]
    shade = np.clip(lum/ref, 0, 1.0)[..., None]; hi = np.clip((lum-ref)/(1-ref+1e-4), 0, 1)[..., None]
    printed = A[..., :3]*shade*0.98 + hi*0.55*(1-A[..., :3]*shade)
    res = a*(1-alpha[..., None]) + printed*alpha[..., None]
    Image.fromarray((res.clip(0, 1)*255).astype(np.uint8)).save(out)
    print(out, 'edge pts', n, 'ellipse', round(cx), round(cy), round(rx), round(ry))
    return round(cx), round(cy)
