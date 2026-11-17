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
    for _ in range(5):                                       # least-squares rotated ellipse, drop outliers
        x, y = P[:, 0]-c0[0], P[:, 1]-c0[1]
        A = np.c_[x*x, x*y, y*y, x, y]; a, b, c, d, e = np.linalg.lstsq(A, np.ones(len(x)), rcond=None)[0]
        M = np.array([[a, b/2], [b/2, c]]); ctr = np.linalg.solve(2*M, [-d, -e])
        k = 1 + ctr @ M @ ctr
        w, v = np.linalg.eigh(M/k); ax = 1/np.sqrt(w)
        ang = np.arctan2(v[1, 0], v[0, 0])
        R = np.array([[np.cos(ang), np.sin(ang)], [-np.sin(ang), np.cos(ang)]])
        q = (np.c_[x, y]-ctr) @ R.T
        res = np.abs(np.hypot(q[:, 0]/ax[0], q[:, 1]/ax[1]) - 1)
        P = P[res < max(0.02, np.percentile(res, 80))]
    # report as (cx, cy, semi-axis along u, semi-axis along v, angle of u); choose u nearest horizontal
    if abs(np.cos(ang)) < abs(np.sin(ang)): ang += np.pi/2; ax = ax[::-1]
    return ctr[0]+c0[0], ctr[1]+c0[1], ax[0], ax[1], ang, len(pts)
def build(art_path, photo, c0, r0, out, skip=(), base=None, up=None):
    ph = Image.open(base or photo).convert('RGB').resize((W, H), Image.LANCZOS)
    src = np.asarray(Image.open(photo).convert('RGB').resize((W, H), Image.LANCZOS)).astype(np.float32)/255
    a = np.asarray(ph).astype(np.float32)/255
    lum = src @ np.array([.299, .587, .114], dtype=np.float32)
    cx, cy, rx, ry, ang, n = fit(lum, c0, r0, skip)
    yy, xx = np.mgrid[0:H, 0:W]
    ca, sa = np.cos(ang), np.sin(ang)
    U = (xx-cx)*ca + (yy-cy)*sa; V = -(xx-cx)*sa + (yy-cy)*ca
    mx, mn = src.max(-1), src.min(-1); sat = (mx-mn)/(mx+1e-4)
    red = (src[..., 0] > 0.30) & (src[..., 0] > src[..., 1]*1.6) & (src[..., 0] > src[..., 2]*1.6)
    inside = (U/rx)**2 + (V/ry)**2 <= 0.985**2
    skin = (sat > np.percentile(sat[inside], 50) + 0.24) & ~red   # fingers, tissue, glass: anything far more coloured than the glaze
    ref = np.percentile(lum[inside & ~red & ~skin], 75)
    hole = (lum < ref*0.45) & (V < -ry*0.6)
    disc = inside & ~red & ~skin & ~hole
    art = Image.open(art_path).convert('RGBA'); aw, ah = art.size
    # forward map: image = c + Rg . diag(rx, ry) . Rphi . p, p in the unit disc; Rphi turns the art so its top points at the hanging hole
    Rg = np.array([[ca, -sa], [sa, ca]]); D = np.diag([rx, ry])
    upv = np.array(up if up else (cx, cy - ry), float) - [cx, cy]
    t = np.linalg.inv(D) @ Rg.T @ upv; phi = np.arctan2(t[0], -t[1])
    Rp = np.array([[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]])
    Finv = np.linalg.inv(Rg @ D @ Rp)
    # art pixel = (p + 1) * size/2, p = Finv (x - c)
    m = Finv * np.array([[aw/2], [ah/2]]); off = -m @ [cx, cy] + [aw/2, ah/2]
    canvas = art.transform((W, H), Image.AFFINE, (m[0, 0], m[0, 1], off[0], m[1, 0], m[1, 1], off[1]), resample=Image.BICUBIC)
    A = np.asarray(canvas).astype(np.float32)/255
    dm = Image.fromarray((disc*255).astype(np.uint8)).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.4))
    alpha = (np.asarray(dm).astype(np.float32)/255)*A[..., 3]
    shade = np.clip(lum/ref, 0, 1.0)[..., None]; hi = np.clip((lum-ref)/(1-ref+1e-4), 0, 1)[..., None]
    printed = A[..., :3]*shade*0.98 + hi*0.55*(1-A[..., :3]*shade)
    res = a*(1-alpha[..., None]) + printed*alpha[..., None]
    Image.fromarray((res.clip(0, 1)*255).astype(np.uint8)).save(out)
    print(out, 'edge pts', n, 'ellipse', round(cx), round(cy), round(rx), round(ry), 'tilt', round(np.degrees(ang), 1))
    return round(cx), round(cy)
