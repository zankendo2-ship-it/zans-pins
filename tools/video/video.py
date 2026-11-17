"""Two-part 8.5-second video. Part 1 (0-6s): the photographed bauble with a big hook. Part 2 (6-8.5s): the branded snow end-card."""
import subprocess, numpy as np, imageio_ffmpeg
from PIL import Image, ImageFilter
FF = imageio_ffmpeg.get_ffmpeg_exe(); FPS, W, H = 30, 1080, 1920
P1, XF, TOTAL = 6.0, 0.35, 8.5
CX, CY = 725, 1164
ease = lambda x: 0 if x <= 0 else 1 if x >= 1 else x*x*(3-2*x)
def back(x):                                  # ease-out with a small overshoot: the "pop"
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    c1 = 1.70158; c3 = c1+1; return 1 + c3*(x-1)**3 + c1*(x-1)**2
def fade(img, a): return img if a >= 1 else Image.merge('RGBA', (*img.split()[:3], img.split()[3].point(lambda v: int(v*a))))
def shift(img, dy): return img.transform(img.size, Image.AFFINE, (1, 0, 0, 0, 1, -dy)) if dy else img
rng = np.random.default_rng(7)
FL = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(2.0, 6.0), rng.uniform(70, 190), rng.uniform(0, 6.28), rng.uniform(.4, .95)) for _ in range(110)]
ky, kx = np.mgrid[-14:15, -14:15].astype(np.float32)
def snow(arr, t):                             # soft, slow, slightly drifting flakes over the whole card
    for (x, y, r, sp, ph, op) in FL:
        yy = (y + sp*t) % (H+40) - 20; xx = (x + 26*np.sin(ph + t*0.9)) % W
        xi, yi = int(xx), int(yy)
        if 14 <= xi < W-14 and 14 <= yi < H-14:
            arr[yi-14:yi+15, xi-14:xi+15] += (np.exp(-(kx**2+ky**2)/(2*r*r))*255*op)[..., None]
    return arr
def render(key):
    master = Image.open(f'v/scene-{key}.png').convert('RGB'); MW, MH = master.size
    h1, h2, shade = (Image.open(f'v/{key}-{n}.png').convert('RGBA') for n in ('h1', 'h2', 'vshade'))
    card = np.asarray(Image.open('v/endcard.png').convert('RGB')).astype(np.float32)
    m = np.asarray(master).astype(np.float32)/255
    warm = np.clip((m[..., 0]-0.55)*2.2, 0, 1) * (m[..., 0] > m[..., 2]*1.25)
    yy, xx = np.mgrid[0:MH, 0:MW]
    warm *= (((xx-CX)/400.0)**2 + ((yy-CY)/450.0)**2 > 1)
    glow = np.asarray(Image.fromarray((warm*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(26))).astype(np.float32)/255
    phase = (np.sin(xx/170.0)*1.7 + np.cos(yy/210.0)*2.3).astype(np.float32); tint = np.array([1.0, 0.80, 0.42], dtype=np.float32)
    out = f'v/{key}.mp4'
    p = subprocess.Popen([FF, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
        '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '64k', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for f in range(int(FPS*TOTAL)):
        t = f/FPS
        if t < P1 + XF:
            tw = glow * (0.5+0.5*np.sin(phase + t*2.4)) * 0.55
            frame = Image.fromarray(((m + tw[..., None]*tint).clip(0, 1)*255).astype(np.uint8))
            z = 1.07 + 0.13*ease(t/P1); cw, ch = MW/z, MH/z          # slow push-in, anchored to the top so the bauble stays clear of the hook
            x0 = min(max(CX*0.5 + MW*0.25 - cw/2 + (CX-MW/2)*0.5*ease(t/P1), 0), MW-cw)
            fr = frame.resize((W, H), Image.BICUBIC, box=(x0, 0, x0+cw, ch)).convert('RGBA')
            fr = Image.alpha_composite(fr, fade(shade, ease((t-0.3)/0.5)))
            for img, t0 in ((h1, 0.5), (h2, 0.68)):                  # the hook pops in at about half a second
                k = (t-t0)/0.42
                if k > 0: fr = Image.alpha_composite(fr, shift(fade(img, min(1, k*2.2)), int((1-back(k))*90)))
            a = np.asarray(fr.convert('RGB')).astype(np.float32)
        if t >= P1:
            c = snow(card.copy(), t-P1).clip(0, 255)
            k = ease((t-P1)/XF); a = c if k >= 1 else a*(1-k) + c*k
        if f in (0, 30, 170, 235): Image.fromarray(a.astype(np.uint8)).save(f'v/{key}-frame-{f:03d}.jpg', quality=92)
        p.stdin.write(a.astype(np.uint8).tobytes())
    p.stdin.close(); p.wait(); print(out)
    feed = master.resize((1080, 1920), Image.LANCZOS).crop((0, 110, 1080, 1460)).convert('RGBA')
    Image.alpha_composite(feed, Image.open(f'v/{key}-f.png').convert('RGBA')).convert('RGB').save(f'v/{key}-feed.png')
render('ombudsman'); render('lossiemouth')
