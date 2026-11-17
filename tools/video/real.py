"""The REAL designer bauble photo, kept whole (genuine ribbon, pine sprig, studio lighting; artwork mapped by the designer itself).
Only the surroundings are brightened and warmed, and soft golden lights are added around it. The bauble is never AI-generated or cut out."""
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
W, H = 1296, 2304
def bokeh(shape, seed, avoid, n=34):
    h, w = shape; rng = np.random.default_rng(seed); layer = np.zeros((h, w), np.float32); pts = []
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); cx, cy, rad = avoid
    while len(pts) < n:
        x, y, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(34, 104)
        if (x-cx)**2 + (y-cy)**2 < (rad+r+30)**2: continue                      # never over the bauble
        if 430 < y < 760 and abs(x-cx) < 430: continue                          # keep the headline area calmer
        pts.append((x, y, r, rng.uniform(.22, .6)))
    for (x, y, r, op) in pts:
        d = np.sqrt((xx-x)**2 + (yy-y)**2); layer = np.maximum(layer, np.clip((r-d)/7, 0, 1)*op)   # crisp-edged discs, like real lens bokeh
    return np.asarray(Image.fromarray((layer*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))).astype(np.float32)/255, pts
def build(capture, out, seed):
    ph = Image.open(capture).convert('RGB'); pw = W; phh = int(ph.height*W/ph.width); ph = ph.resize((pw, phh), Image.LANCZOS)
    top = 380; bot = H-top-phh
    canvas = Image.new('RGB', (W, H))
    canvas.paste(ph.crop((0, 0, pw, 36)).resize((pw, top), Image.BICUBIC).filter(ImageFilter.GaussianBlur(40)), (0, 0))       # the photo's own tones continue upwards, soft
    canvas.paste(ph, (0, top))
    canvas.paste(ph.crop((0, phh-36, pw, phh)).resize((pw, bot), Image.BICUBIC).filter(ImageFilter.GaussianBlur(40)), (0, top+phh))
    seam = Image.new('L', (W, H), 0); px = seam.load()
    a = np.asarray(canvas).astype(np.float32)/255
    # soften the two joins
    for y0 in (top, top+phh):
        blurred = np.asarray(Image.fromarray((a[y0-140:y0+140]*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(22))).astype(np.float32)/255
        wgt = (1 - np.abs(np.linspace(-1, 1, 280)))[:, None, None]                 # full blur on the join, fading out either side
        a[y0-140:y0+140] = a[y0-140:y0+140]*(1-wgt) + blurred*wgt
    cx, cy, rad = 452*W/880, top + 648*phh/1088, 298*W/880
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    off = np.clip((np.sqrt((xx-cx)**2 + (yy-cy)**2) - rad)/60, 0, 1)[..., None]   # 0 on the bauble, 1 away from it
    # brighten and warm the surroundings only: lift the shadows, push gold
    lifted = np.power(a, 0.62) * np.array([1.18, 1.02, 0.80], dtype=np.float32) + np.array([0.06, 0.035, 0.0], dtype=np.float32)
    a = a*(1-off) + lifted*off
    b, pts = bokeh((H, W), seed, (cx, cy, rad))
    a = a + (b[..., None]*np.array([1.0, 0.80, 0.40], dtype=np.float32))*off*0.9   # added golden fairy-light bokeh
    glow = np.clip(1 - np.sqrt((xx-cx)**2 + (yy-(cy+rad*1.5))**2)/(rad*2.6), 0, 1)[..., None]**2
    a = a + glow*np.array([0.42, 0.20, 0.03], dtype=np.float32)*off                 # amber fire glow rising from below
    a_b = np.clip(a*1.06, 0, 1)                                                     # a touch more light on the product itself
    im = Image.fromarray((a_b*255).astype(np.uint8)); im.save(out)
    print(out, 'bauble centre', int(cx), int(cy), 'radius', int(rad)); return pts
build('assets/bauble-ombudsman.png', 'v/scene-ombudsman.png', 11); build('assets/bauble-lossiemouth.png', 'v/scene-lossiemouth.png', 12)
