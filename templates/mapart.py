"""Print the exact designer artwork onto the photographed blank ceramic bauble, keeping the real glaze, highlights, shadow, hole and cord."""
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
W, H = 1296, 2304
def build(art_path, photo, seed, out, ratio=1.02):
    ph = Image.open(photo).convert('RGB').resize((W, H), Image.LANCZOS)
    a = np.asarray(ph).astype(np.float32)/255
    mx, mn = a.max(-1), a.min(-1); lum = a @ np.array([.299, .587, .114], dtype=np.float32)
    sat = (mx-mn)/(mx+1e-4)
    white = (lum > 0.40) & (sat < 0.20)                              # the glazed ceramic face (bokeh and fire are far more saturated)
    m = Image.fromarray((white*255).astype(np.uint8)).filter(ImageFilter.MedianFilter(9))
    fl = m.copy(); ImageDraw.floodfill(fl, seed, 128, thresh=10)
    disc = (np.asarray(fl) == 128)
    ys, xs = np.nonzero(disc); y0 = ys.min()
    top = disc[y0:y0+420]; tx = np.nonzero(top.any(0))[0]             # measure the width from the upper part, where nothing else is white
    x0, x1 = tx.min(), tx.max(); r = (x1-x0)/2; cx = (x0+x1)/2; cy = y0 + r*1.03
    yy, xx = np.mgrid[0:H, 0:W]
    ry = r*ratio; cy = y0 + ry
    red = (a[..., 0] > 0.42) & (a[..., 0] > a[..., 1]*1.8) & (a[..., 0] > a[..., 2]*1.8)       # the cord stays in front
    hole = (lum < 0.16) & (yy < y0 + ry*0.4)                                                     # the hanging hole stays a hole
    disc = (((xx-cx)/(r*0.992))**2 + ((yy-cy)/(ry*0.992))**2 <= 1) & ~red & ~hole               # the whole face, even where the fire tints it
    ys, xs = np.nonzero(disc); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    print(out, 'disc box', x0, y0, x1, y1, 'w', x1-x0, 'h', y1-y0, 'fill', round(disc.sum()/((x1-x0)*(y1-y0)*0.785), 2))
    art = Image.open(art_path).convert('RGBA').resize((x1-x0+1, y1-y0+1), Image.LANCZOS)
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0)); canvas.paste(art, (x0, y0))
    A = np.asarray(canvas).astype(np.float32)/255
    dm = Image.fromarray((disc*255).astype(np.uint8)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.6))
    alpha = (np.asarray(dm).astype(np.float32)/255) * A[..., 3]
    ref = np.percentile(lum[disc], 75)
    shade = np.clip(lum/ref, 0, 1.0)[..., None]
    hi = np.clip((lum-ref)/(1-ref+1e-4), 0, 1)[..., None]
    printed = A[..., :3]*shade*0.98 + hi*0.55*(1-A[..., :3]*shade)
    res = a*(1-alpha[..., None]) + printed*alpha[..., None]
    im = Image.fromarray((res.clip(0, 1)*255).astype(np.uint8))
    im.save(out); return (x0+x1)//2, (y0+y1)//2, (x1-x0)//2
if __name__ == '__main__':
    print(build('assets/art-silks-bauble.png', 'assets/scene-candles.webp', (636, 1035), 'v/scene-silks-bauble.png'))
    print(build('assets/art-syndicate.png', 'assets/scene-gifts.webp', (627, 1357), 'v/scene-syndicate.png'))
