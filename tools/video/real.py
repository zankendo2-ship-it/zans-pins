"""The REAL designer bauble photo, kept whole. The bauble is the hero: surroundings calmed and warmed, a soft glow behind the
bauble to lift it off the background, the bauble itself brightened. No fake light discs. Never an AI-generated or cut-out bauble."""
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
W, H = 1296, 2304
def build(capture, out):
    ph = Image.open(capture).convert('RGB'); phh = int(ph.height*W/ph.width); ph = ph.resize((W, phh), Image.LANCZOS)
    top = 380; bot = H-top-phh
    canvas = Image.new('RGB', (W, H))
    canvas.paste(ph.crop((0, 0, W, 36)).resize((W, top), Image.BICUBIC).filter(ImageFilter.GaussianBlur(40)), (0, 0))
    canvas.paste(ph, (0, top))
    canvas.paste(ph.crop((0, phh-36, W, phh)).resize((W, bot), Image.BICUBIC).filter(ImageFilter.GaussianBlur(40)), (0, top+phh))
    a = np.asarray(canvas).astype(np.float32)/255
    for y0 in (top, top+phh):
        blurred = np.asarray(Image.fromarray((a[y0-140:y0+140]*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(22))).astype(np.float32)/255
        wgt = (1 - np.abs(np.linspace(-1, 1, 280)))[:, None, None]; a[y0-140:y0+140] = a[y0-140:y0+140]*(1-wgt) + blurred*wgt
    cx, cy, rad = 452*W/880, top + 648*phh/1088, 298*W/880
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); d = np.sqrt((xx-cx)**2 + (yy-cy)**2)
    off = np.clip((d-rad)/50, 0, 1)[..., None]                                   # 0 on the bauble, 1 away from it
    # surroundings: warm and a little brighter, but calm, so nothing competes with the bauble
    bg = np.power(a, 0.80) * np.array([1.10, 1.0, 0.86], dtype=np.float32)
    bgb = np.asarray(Image.fromarray((bg.clip(0, 1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(5))).astype(np.float32)/255
    far = np.clip((d-rad*1.15)/(rad*0.9), 0, 1)[..., None]; bg = bg*(1-far*0.7) + bgb*far*0.7     # background falls further out of focus
    halo = np.clip(1-(d-rad)/(rad*0.95), 0, 1)[..., None]**2.2                    # warm light glowing out from behind the bauble
    bg = bg + halo*np.array([0.62, 0.44, 0.16], dtype=np.float32)
    vig = (1 - 0.42*np.clip((np.sqrt(((xx-cx)/(W*0.62))**2 + ((yy-cy)/(H*0.52))**2) - 0.55)/0.6, 0, 1))[..., None]
    bg = bg*vig                                                                   # darker corners pull the eye to the centre
    # the bauble itself: brighter, crisper, more colour
    b = Image.fromarray((a.clip(0, 1)*255).astype(np.uint8))
    b = ImageEnhance.Contrast(ImageEnhance.Brightness(ImageEnhance.Color(b).enhance(1.28)).enhance(1.22)).enhance(1.06)
    b = b.filter(ImageFilter.UnsharpMask(radius=3, percent=60, threshold=2))
    res = (np.asarray(b).astype(np.float32)/255)*(1-off) + bg*off
    Image.fromarray((res.clip(0, 1)*255).astype(np.uint8)).save(out); print(out)
build('assets/bauble-ombudsman.png', 'v/scene-ombudsman.png'); build('assets/bauble-lossiemouth.png', 'v/scene-lossiemouth.png')
