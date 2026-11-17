"""Wide, warm scene: blurred fireplace backdrop + the designer's real bauble, cord and pine branches."""
import sys, numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageChops
W, H = 1296, 2304            # 9:16 master, bigger than 1080x1920 so the video can zoom
def build(capture, out, seed):
    rng = np.random.default_rng(seed)
    # backdrop: the Canva fireplace scene (small copy), enlarged and softened into bokeh
    bd = Image.open('t1.png').convert('RGB').resize((W, int(W*200/112)), Image.BICUBIC)
    bd = bd.crop((0, (bd.height-H)//2, W, (bd.height-H)//2+H)).filter(ImageFilter.GaussianBlur(14))
    bd = ImageEnhance.Color(bd).enhance(1.35); bd = ImageEnhance.Contrast(bd).enhance(1.12); bd = ImageEnhance.Brightness(bd).enhance(1.05)
    # foreground: the designer photo with the artwork mapped on (1176x1455), plus its bauble mask
    fg = Image.open(capture).convert('RGB'); fw, fh = fg.size
    mask = Image.open('assets/bauble-tree-moody-mask.png').convert('L').resize((fw, fh), Image.LANCZOS)
    # make the silks pop inside the bauble only
    pop = ImageEnhance.Contrast(ImageEnhance.Color(fg).enhance(1.35)).enhance(1.12)
    fg = Image.composite(pop, fg, mask.filter(ImageFilter.GaussianBlur(1.5)))
    a = np.asarray(fg).astype(np.float32)
    luma = a @ np.array([.299, .587, .114], dtype=np.float32)
    red = (a[...,0] > 110) & (a[...,0] > a[...,1]*1.7) & (a[...,0] > a[...,2]*1.7)        # the cord
    alpha = np.clip((luma-22)/46, 0, 1)                                                   # lit needles and baubles stay
    yy0, xx0 = np.mgrid[0:fh, 0:fw].astype(np.float32)
    top_cy, top_r = 648*(fh/1088), 298*(fh/1088)
    keep = ((yy0 < top_cy - top_r*0.62) & (xx0 > fw*0.12) & (xx0 < fw*0.58)).astype(np.float32)   # only the branch above the bauble
    keep = np.asarray(Image.fromarray((keep*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(30))).astype(np.float32)/255
    alpha = alpha*keep
    red &= (yy0 < top_cy - top_r*0.5) & (xx0 > fw*0.36) & (xx0 < fw*0.56)
    alpha = np.maximum(alpha, red.astype(np.float32))
    # the ceramic disc: fully opaque, slightly grown to keep the white rim
    disc = np.asarray(mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32)/255
    alpha = np.maximum(alpha, disc)
    # fade the photo's outer edges so no rectangle shows
    yy, xx = np.mgrid[0:fh, 0:fw].astype(np.float32)
    edge = np.minimum.reduce([xx/140, (fw-1-xx)/140, yy/60, (fh-1-yy)/200]).clip(0, 1)
    alpha *= edge
    A = Image.fromarray((alpha*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))
    s = 0.74; fgs = fg.resize((int(fw*s), int(fh*s)), Image.LANCZOS); As = A.resize(fgs.size, Image.LANCZOS)
    ox, oy = (W-fgs.width)//2 - 6, 480
    # soft shadow behind the disc so it sits in the scene
    sh = Image.new('L', (W, H), 0); dm = mask.resize(fgs.size, Image.LANCZOS)
    sh.paste(dm, (ox+26, oy+34)); sh = sh.filter(ImageFilter.GaussianBlur(38))
    bd = Image.composite(Image.new('RGB', (W, H), (8, 6, 4)), bd, sh.point(lambda v: int(v*0.55)))
    bd.paste(fgs, (ox, oy), As)
    # warm vignette
    vy, vx = np.mgrid[0:H, 0:W].astype(np.float32)
    v = 1 - 0.38*(((vx-W/2)/(W*0.72))**2 + ((vy-H*0.52)/(H*0.62))**2).clip(0, 1)
    out_im = Image.fromarray((np.asarray(bd).astype(np.float32)*v[..., None]).clip(0, 255).astype(np.uint8))
    out_im.save(out)
    cx, cy, r = ox + 452*(fw/880)*s, oy + 648*(fh/1088)*s, 298*(fw/880)*s
    print(out, 'bauble centre', round(cx), round(cy), 'radius', round(r))
build('assets/bauble-ombudsman.png', 'v/scene-ombudsman.png', 1)
build('assets/bauble-lossiemouth.png', 'v/scene-lossiemouth.png', 2)
