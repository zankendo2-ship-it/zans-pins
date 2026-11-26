"""Mug B in the LIVE listing scene (4608193933 photo 19, fireplace): the real print PNG is wrapped onto the photo's own mug.
Geometry measured from the photo (script comments): body CX=559 R=331 in the 1215x1518 crop frame; print top = ellipse c455.1+e32.7*cz,
print bottom = c1179.7+e87.2*cz; print runs x 230..805. File mapping: Harrier 11oz, 82 mm mug, 209.55 mm print, handle at +82 deg."""
import math, os, sys, numpy as np
from PIL import Image
SRC = sys.argv[1] if len(sys.argv) > 1 else '/mnt/project-files/etsy-seo/2026-11-23/REX recolour DRAFT - not live/AFTER 4608193933_19.jpg'
HERE = os.path.dirname(os.path.abspath(__file__)); ART = os.path.join(HERE, '..', 'out'); OUT = os.path.join(HERE, 'out'); os.makedirs(OUT, exist_ok=True)
OX, OY = 810, 405                      # crop origin inside the 2700x2025 photo
CX, R = 559.0, 331.0
TOP_C, TOP_E, BOT_C, BOT_E = 455.1, 32.7, 1179.7, 87.2
XL, XR = 229.0, 805.5
C, FILE_MM = math.pi * 82.0, 209.55
PHI = math.radians(-82.0)
SS = 3
def wrap(art_png, out):
    photo = np.asarray(Image.open(SRC).convert('RGB')).astype(float)[OY:OY + 1518, OX:OX + 1215]
    art = np.asarray(Image.open(art_png).convert('RGB')).astype(float); AH, AW, _ = art.shape
    x0, x1, y0, y1 = 220, 815, 430, 1300
    gx = (np.arange((x1 - x0) * SS) + 0.5) / SS + x0; gy = (np.arange((y1 - y0) * SS) + 0.5) / SS + y0
    X, Y = np.meshgrid(gx, gy)
    u = np.clip((X - CX) / R, -0.999, 0.999); s = np.arcsin(u); cz = np.cos(s)
    top = TOP_C + TOP_E * cz; bot = BOT_C + BOT_E * cz
    inside = (Y >= top - 4.0) & (Y <= bot + 5.0) & (X >= XL - 2.2) & (X <= XR + 4.2)
    v = np.clip((Y - top) / (bot - top), 0, 1)
    theta = np.mod(s + PHI, 2 * math.pi); along = (theta - math.pi) / (2 * math.pi) * C
    fx = (along / FILE_MM + 0.5) * AW; fy = v * (AH - 1)
    ok = inside
    fxc = np.clip(fx, 0, AW - 2); x0i = fxc.astype(int); wx = (fxc - x0i)[..., None]
    y0i = np.clip(fy, 0, AH - 2).astype(int); wy = (np.clip(fy, 0, AH - 2) - y0i)[..., None]
    smp = art[y0i, x0i] * (1 - wx) * (1 - wy) + art[y0i, x0i + 1] * wx * (1 - wy) + art[y0i + 1, x0i] * (1 - wx) * wy + art[y0i + 1, x0i + 1] * wx * wy
    side = np.where(u < 0, 0.55 + 0.45 * cz ** 0.9, 0.80 + 0.20 * cz ** 0.9)       # darker to both edges (more on the shadow side)
    shade = (side * (1 - 0.10 * v ** 3))[..., None]
    streak = (0.24 * np.exp(-((u - 0.18) / 0.06) ** 2) + 0.08 * np.exp(-((u - 0.18) / 0.20) ** 2) + 0.06 * np.exp(-((u + 0.62) / 0.05) ** 2))
    streak = (streak * (1 - 0.6 * v ** 2))[..., None]
    lit = np.clip(smp * shade + 255 * streak * (0.45 + 0.55 * smp.mean(-1, keepdims=True) / 255), 0, 255)
    cov = ok.astype(float)[..., None]
    def down(a): h, w = a.shape[:2]; return a.reshape(h // SS, SS, w // SS, SS, -1).mean((1, 3))
    covd = down(cov); litd = down(lit * cov) / np.maximum(covd, 1e-6)
    reg = photo[y0:y1, x0:x1]
    photo[y0:y1, x0:x1] = reg * (1 - covd) + litd * covd
    Image.fromarray(np.clip(photo, 0, 255).astype(np.uint8)).save(out, quality=95)
if __name__ == '__main__':
    for ref, n in (('loussiemoo', 'Loussiemoo'), ('zoo-olympios', 'Zoo Olympios'), ('rexs-romance', 'Rexs Romance')):
        o = os.path.join(OUT, f'{n} bauble-style mug - scene.png'); wrap(os.path.join(ART, f'{ref}-bauble-style-mug-2475x1155.png'), o); print(o)
