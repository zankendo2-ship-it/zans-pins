"""Print the exact designer artwork onto the photographed blank ceramic bauble, keeping the real glaze, highlights, shadow, hole and cord."""
import numpy as np
from PIL import Image, ImageFilter
def build(art_path, out, W=1296, H=2304):
    ph = Image.open('assets/blank-bauble.webp').convert('RGB').resize((W, H), Image.LANCZOS)
    a = np.asarray(ph).astype(np.float32)/255
    mx, mn = a.max(-1), a.min(-1); lum = a @ np.array([.299, .587, .114], dtype=np.float32)
    sat = (mx-mn)/(mx+1e-4)
    white = (lum > 0.42) & (sat < 0.22)                          # the glazed ceramic face
    m = Image.fromarray((white*255).astype(np.uint8)).filter(ImageFilter.MedianFilter(9))
    # keep only the big blob in the middle (drops fairy lights and the window edge)
    from PIL import ImageDraw
    mm = np.asarray(m) > 127
    ys, xs = np.nonzero(mm[:, :int(W*0.9)])
    seed = (int(W*0.55), int(H*0.5))
    fl = m.copy(); ImageDraw.floodfill(fl, seed, 128, thresh=10)
    disc = (np.asarray(fl) == 128)
    ys, xs = np.nonzero(disc); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    print('disc box', x0, y0, x1, y1, 'w', x1-x0, 'h', y1-y0)
    art = Image.open(art_path).convert('RGBA').resize((x1-x0+1, y1-y0+1), Image.LANCZOS)   # ellipse fit: the disc is turned slightly
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0)); canvas.paste(art, (x0, y0))
    A = np.asarray(canvas).astype(np.float32)/255
    dm = Image.fromarray((disc*255).astype(np.uint8)).filter(ImageFilter.MinFilter(5)).filter(ImageFilter.GaussianBlur(1.6))
    alpha = (np.asarray(dm).astype(np.float32)/255) * A[..., 3]
    ref = np.percentile(lum[disc], 60)                           # the glaze's typical brightness
    shade = np.clip(lum/ref, 0, 1.0)[..., None]                  # real shading multiplies the print
    hi = np.clip((lum-ref)/(1-ref+1e-4), 0, 1)[..., None]        # real highlights sit on top
    printed = A[..., :3]*shade*0.97 + hi*0.55*(1-A[..., :3]*shade)
    res = a*(1-alpha[..., None]) + printed*alpha[..., None]
    Image.fromarray((res.clip(0, 1)*255).astype(np.uint8)).save(out)
    return (x0+x1)//2, (y0+y1)//2
for k in ('ombudsman', 'lossiemouth'):
    print(k, build(f'assets/art-{k}.png', f'v/scene-{k}.png'))
