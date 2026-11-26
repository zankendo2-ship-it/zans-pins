"""Mug photo from the REAL print file (2475x1155 Harrier 11oz), wrapped at true scale on a straight 82 mm x 95 mm cylinder.
Name panel faces the camera, handle behind-left, no labels. Not a print file. Usage: python mockup.py"""
import math, os, numpy as np
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); OUTD = os.path.join(HERE, 'out'); os.makedirs(OUTD, exist_ok=True)
SS = 2; OW, OH = 1200, 1500; W, H = OW * SS, OH * SS
D_MM, H_MM, FILE_MM = 82.0, 95.0, 209.55
BG = np.array([234, 226, 216], float)
PXMM = 8.6 * SS; R = D_MM / 2 * PXMM; BH = H_MM * PXMM; ELL = R * 0.15
CX = W / 2 + 17 * PXMM; TY = H / 2 - BH / 2 - ELL * 0.2; BY = TY + BH
C = math.pi * D_MM
PHI = math.pi - (FILE_MM / 4) / C * 2 * math.pi        # name panel at file x = W/4 faces the camera

def lerp(a, b, t): return a + (b - a) * t

def render(png, out, handle=(24, 24, 26)):
    art = np.asarray(Image.open(png).convert('RGB')).astype(float); SH, SW, _ = art.shape
    bg = np.ones((H, W, 3)) * BG
    yy = np.linspace(0, 1, H)[:, None, None]; bg = bg * (1.03 - 0.07 * yy)
    img = Image.fromarray(bg.astype(np.uint8)).convert('RGB')
    # soft contact shadow
    sh = Image.new('L', (W, H), 0); d = ImageDraw.Draw(sh)
    d.ellipse((CX - R * 1.02, BY - ELL * 0.2, CX + R * 1.02, BY + ELL * 1.9), fill=150)
    d.ellipse((CX - R * 1.5, BY - ELL * 0.5, CX + R * 0.6, BY + ELL * 2.6), fill=70)
    sh = sh.filter(ImageFilter.GaussianBlur(26 * SS))
    img = Image.composite(Image.new('RGB', (W, H), (92, 84, 76)), img, sh.point(lambda v: int(v * 0.55)))
    # handle (behind the body: its attachment is buried under the body edge)
    from scipy import ndimage as ndi
    hx_side = math.sin(-PHI); side = -1 if hx_side < 0 else 1
    edge = CX + side * R * abs(hx_side) * 0.97
    y0 = TY + ELL + 16 * PXMM; y1 = TY + ELL + 72 * PXMM; reach = 28 * PXMM
    rad = 5.2 * PXMM
    pts = []
    for i in range(0, 1201):
        t = i / 1200; pts.append((edge + side * reach * math.sqrt(max(0.0, 1 - abs(2 * t - 1) ** 3.0)), y0 + (y1 - y0) * t))
    pts = [(edge - side * (40 - 40 * k / 40) * SS, y0) for k in range(40)] + pts + [(edge - side * (40 * k / 40) * SS, y1) for k in range(40)]
    m = Image.new('L', (W, H), 0); md = ImageDraw.Draw(m)
    for x, y in pts: md.ellipse((x - rad, y - rad, x + rad, y + rad), fill=255)
    mk = np.asarray(m) > 127
    dist = ndi.distance_transform_edt(mk); h = np.sqrt(np.clip(1 - (1 - np.clip(dist / rad, 0, 1)) ** 2, 0, 1))
    hs = ndi.gaussian_filter(np.clip(dist, 0, rad) / rad, 0.12 * rad); gy, gx = np.gradient(hs)
    Lx, Ly = -0.55, -0.83
    lam = np.clip(0.40 + (-(gx * Lx + gy * Ly)) * 0.30 * rad, 0.12, 1.0) * (0.45 + 0.55 * h)
    spec = np.clip((-(gx * Lx + gy * Ly)) * 0.45 * rad - 0.22, 0, 1) ** 1.3 * 1.0 * h
    hc = np.array(handle, float)
    col = np.clip(hc[None, None, :] * lam[..., None] * 1.6 + 70 * (lam[..., None] ** 3) + 255 * spec[..., None], 0, 255)
    cov = ndi.gaussian_filter(mk.astype(float), 0.7 * SS)[..., None]
    arr0 = np.asarray(img).astype(float); arr0 = arr0 * (1 - cov) + col * cov
    img = Image.fromarray(np.clip(arr0, 0, 255).astype(np.uint8))
    # body, per pixel
    arr = np.asarray(img).astype(float)
    xs = np.arange(int(CX - R) - 1, int(CX + R) + 2)
    u = (xs + 0.5 - CX) / R; ok = np.abs(u) < 1; xs = xs[ok]; u = u[ok]
    s = np.arcsin(u); cz = np.cos(s); theta = PHI + s
    t = np.mod(theta, 2 * math.pi); along = (t - math.pi) / (2 * math.pi) * C          # mm from print centre
    fx = (along / FILE_MM + 0.5) * SW
    top = TY + ELL * cz; bot = BY + ELL * cz
    rows = np.arange(int(TY), int(BY + ELL) + 3)
    Y = rows[:, None]; Xc = xs[None, :]
    inside = (Y >= top[None, :]) & (Y < bot[None, :])
    py = (Y - top[None, :]) / PXMM - (97.8 - H_MM) / 2                  # mm down the file, file centred on the body
    fy = (py + 0.0) / 97.8 * SH + SH * 0 + (97.8 - H_MM) / 2 / 97.8 * SH * 0
    fy = (py + (97.8 - H_MM) / 2) / 97.8 * SH
    fxx = np.broadcast_to(fx[None, :], inside.shape)
    has = inside & (fxx >= 0) & (fxx < SW - 1) & (fy >= 0) & (fy < SH - 1)
    ix = np.clip(fxx, 0, SW - 2); iy = np.clip(fy, 0, SH - 2)
    x0 = ix.astype(int); y0i = iy.astype(int); wx = (ix - x0)[..., None]; wy = (iy - y0i)[..., None]
    smp = (art[y0i, x0] * (1 - wx) * (1 - wy) + art[y0i, x0 + 1] * wx * (1 - wy) + art[y0i + 1, x0] * (1 - wx) * wy + art[y0i + 1, x0 + 1] * wx * wy)
    base = np.where(has[..., None], smp, np.array([250, 249, 247.]))
    czb = cz[None, :, None] * np.ones_like(base[..., :1])
    shade = (0.62 + 0.38 * czb ** 0.9) * (0.95 + 0.05 * (1 - (u[None, :, None] + 1) / 2))
    ub = u[None, :, None]
    spec = 0.16 * np.exp(-((ub + 0.52) / 0.035) ** 2) + 0.05 * np.exp(-((ub + 0.52) / 0.15) ** 2) + 0.06 * np.exp(-((ub - 0.64) / 0.04) ** 2)
    vgrad = np.clip((Y - top[None, :]) / BH, 0, 1)[..., None]
    shade = shade * (1 - 0.10 * np.clip((vgrad - 0.9) / 0.1, 0, 1))
    lit = base * shade + 255 * spec * (0.55 + 0.45 * (base.mean(-1, keepdims=True) / 255))
    lit = np.clip(lit, 0, 255)
    reg = arr[int(TY):int(TY) + len(rows), :]
    sub = reg[:, xs[0]:xs[-1] + 1]
    # anti-alias the silhouette: coverage from distance to top/bottom curves
    cov = np.clip(np.minimum(Y - top[None, :], bot[None, :] - Y) + 0.5, 0, 1)[..., None]
    sub[...] = np.where(inside[..., None], sub * (1 - cov) + lit * cov, sub)
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    # glazed interior + lip
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.ellipse((CX - R, TY - ELL, CX + R, TY + ELL), fill=tuple(int(v * 0.35) for v in handle) + (255,))
    inner = Image.new('L', (W, H), 0); ImageDraw.Draw(inner).ellipse((CX - R * 0.955, TY - ELL * 0.93, CX + R * 0.955, TY + ELL * 0.93), fill=255)
    g = np.zeros((H, W, 4), np.uint8); yy2 = np.clip((np.arange(H) - (TY - ELL)) / (2 * ELL), 0, 1)
    for c in range(3): g[..., c] = (np.array(handle[c]) * 0.30 + 40 * (1 - yy2) ** 1.5)[:, None].astype(np.uint8)
    g[..., 3] = 255
    ov.paste(Image.fromarray(g, 'RGBA'), (0, 0), inner.filter(ImageFilter.GaussianBlur(1.2)))
    od.arc((CX - R, TY - ELL, CX + R, TY + ELL), 195, 285, fill=(190, 190, 195, 255), width=int(2.4 * SS))
    od.arc((CX - R * 0.955, TY - ELL * 0.93, CX + R * 0.955, TY + ELL * 0.93), 200, 280, fill=(255, 255, 255, 90), width=int(1.6 * SS))
    img = Image.alpha_composite(img.convert('RGBA'), ov).convert('RGB')
    # soft lip highlight
    img.resize((OW, OH), Image.LANCZOS).save(out)

if __name__ == '__main__':
    P = os.path.join(HERE, '..', 'out')
    for ref, n in (('loussiemoo', 'Loussiemoo'), ('zoo-olympios', 'Zoo Olympios'), ('rexs-romance', 'Rexs Romance')):
        o = os.path.join(OUTD, f'{n} bauble-style mug.png'); render(os.path.join(P, f'{ref}-bauble-style-mug-2475x1155.png'), o); print(o)
