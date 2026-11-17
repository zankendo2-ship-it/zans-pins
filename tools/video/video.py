import subprocess, numpy as np, imageio_ffmpeg
from PIL import Image
FF = imageio_ffmpeg.get_ffmpeg_exe(); FPS, SECS, W, H = 30, 8, 1080, 1920
CX, CY, R = 654, 1121, 295           # bauble in the 1296x2304 master
ease = lambda x: 0 if x <= 0 else 1 if x >= 1 else x*x*(3-2*x)
def layer(img, a, dy=0):
    if a <= 0: return None
    im = img if a >= 1 else Image.merge('RGBA', (*img.split()[:3], img.split()[3].point(lambda v: int(v*a))))
    return im if dy == 0 else im.transform(im.size, Image.AFFINE, (1, 0, 0, 0, 1, -dy))
def render(key, seed):
    master = Image.open(f'v/scene-{key}.png').convert('RGB'); MW, MH = master.size
    head, cta, end = (Image.open(f'v/{key}-v-{n}.png').convert('RGBA') for n in ('head', 'cta', 'end'))
    rng = np.random.default_rng(seed); sp = []
    while len(sp) < 34:                                   # twinkling warm lights, kept off the bauble
        x, y = rng.uniform(40, W-40), rng.uniform(120, H-120)
        if (x-W/2)**2 + (y-940)**2 > 330**2: sp.append((x, y, rng.uniform(5, 13), rng.uniform(0, 6.28), rng.uniform(1.2, 3.2)))
    yy, xx = np.mgrid[-40:41, -40:41].astype(np.float32)
    out = f'v/{key}.mp4'
    p = subprocess.Popen([FF, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
        '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '64k', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for f in range(FPS*SECS):
        t = f/FPS
        z = 1.0 + 0.16*ease(t/SECS)                       # slow cinematic push in towards the bauble
        cw, ch = MW/z, MH/z
        fx, fy = MW/2 + (CX-MW/2)*ease(t/SECS)*0.6, MH/2 + (CY-80-MH/2)*ease(t/SECS)*0.6
        x0, y0 = min(max(fx-cw/2, 0), MW-cw), min(max(fy-ch/2, 0), MH-ch)
        fr = master.resize((W, H), Image.BICUBIC, box=(x0, y0, x0+cw, y0+ch))
        a = np.asarray(fr).astype(np.float32)
        for (x, y, r, ph, sp_) in sp:                     # shimmer
            k = (0.5+0.5*np.sin(ph + t*sp_*2))**3
            if k < 0.03: continue
            g = np.exp(-(xx**2+yy**2)/(2*r*r)) * 150*k
            xi, yi = int(x), int(y); a[yi-40:yi+41, xi-40:xi+41] += g[..., None]*np.array([1.0, 0.82, 0.45], dtype=np.float32)
        fr = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')
        for img, t0, slide in ((head, 1.0, 46), (cta, 4.0, 30), (end, 5.6, 30)):   # hook lands between 1.0 and 1.4 seconds
            k = ease((t-t0)/0.4); L = layer(img, k, int((1-k)*slide))
            if L is not None: fr = Image.alpha_composite(fr, L)
        if f in (0, 45, 150, 235): fr.convert('RGB').save(f'v/{key}-frame-{f:03d}.jpg', quality=90)
        p.stdin.write(fr.convert('RGB').tobytes())
    p.stdin.close(); p.wait(); print(out)
    # 4:5 feed photo from the same scene
    feed = master.resize((1080, 1920), Image.LANCZOS).crop((0, 330, 1080, 1680)).convert('RGBA')
    feed = Image.alpha_composite(feed, Image.open(f'v/{key}-f.png').convert('RGBA')).convert('RGB'); feed.save(f'v/{key}-feed.png')
render('ombudsman', 3); render('lossiemouth', 4)
