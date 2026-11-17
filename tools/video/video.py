"""8.5-second video. 0-6s: slow cinematic push-in on the pure photograph (gentle snowfall outdoors, soft light shimmer indoors),
no text at all. 6-8.5s: the animated ZANS snow end-card with all the branding and the call to action."""
import subprocess, numpy as np, imageio_ffmpeg
from PIL import Image, ImageFilter
FF = imageio_ffmpeg.get_ffmpeg_exe(); FPS, W, H = 30, 1080, 1920
P1, XF, TOTAL = 6.0, 0.35, 8.5
ease = lambda x: 0 if x <= 0 else 1 if x >= 1 else x*x*(3-2*x)
def flakes(seed, n, w, h, rmin, rmax, smin, smax):
    r = np.random.default_rng(seed)
    return [(r.uniform(0, w), r.uniform(0, h), r.uniform(rmin, rmax), r.uniform(smin, smax), r.uniform(0, 6.28), r.uniform(.45, .95)) for _ in range(n)]
ky, kx = np.mgrid[-16:17, -16:17].astype(np.float32)
def snow(arr, t, fl, drift=22):
    h, w = arr.shape[:2]
    for (x, y, r, sp, ph, op) in fl:
        yy = (y + sp*t) % (h+40) - 20; xx = (x + drift*np.sin(ph + t*0.8)) % w
        xi, yi = int(xx), int(yy)
        if 16 <= xi < w-16 and 16 <= yi < h-16: arr[yi-16:yi+17, xi-16:xi+17] += (np.exp(-(kx**2+ky**2)/(2*r*r))*255*op)[..., None]
    return arr
def render(key, centre, mode):
    master = Image.open(f'v/scene-{key}.png').convert('RGB'); MW, MH = master.size; CX, CY = centre
    m = np.asarray(master).astype(np.float32)/255
    if mode == 'shimmer':                                         # the scene's own fairy lights breathe, never on the bauble
        warm = np.clip((m[..., 0]-0.6)*2.5, 0, 1) * (m[..., 0] > m[..., 2]*1.2)
        yy, xx = np.mgrid[0:MH, 0:MW]; warm *= (((xx-CX)/360.0)**2 + ((yy-CY)/370.0)**2 > 1)
        glow = np.asarray(Image.fromarray((warm*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(20))).astype(np.float32)/255
        phase = (np.sin(xx/150.0)*1.9 + np.cos(yy/190.0)*2.1).astype(np.float32)
    scene_snow = flakes(3, 70, W, H, 1.6, 4.2, 40, 110)
    card = np.asarray(Image.open(f'v/{key}-endcard.png').convert('RGB')).astype(np.float32)
    head = Image.open(f'v/{key}-vhead.png').convert('RGBA'); card_snow = flakes(7, 110, W, H, 2.0, 6.0, 70, 190)
    out = f'v/{key}.mp4'
    p = subprocess.Popen([FF, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
        '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '64k', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for f in range(int(FPS*TOTAL)):
        t = f/FPS
        if t < P1 + XF:
            src = m if mode != 'shimmer' else (m + (glow*(0.5+0.5*np.sin(phase + t*2.2))*0.35)[..., None]*np.array([1.0, .82, .5], dtype=np.float32))
            frame = Image.fromarray((src.clip(0, 1)*255).astype(np.uint8))
            k = ease(min(t, P1)/P1); z = 1.0 + 0.14*k; cw, ch = MW/z, MH/z      # slow push-in towards the bauble
            x0 = min(max(MW/2 + (CX-MW/2)*k - cw/2, 0), MW-cw); y0 = min(max(MH/2 + (CY-260-MH/2)*k - ch/2, 0), MH-ch)
            a = np.asarray(frame.resize((W, H), Image.BICUBIC, box=(x0, y0, x0+cw, y0+ch))).astype(np.float32)
            if mode == 'snow': a = snow(a, t, scene_snow, 14)
            hk = ease((t-0.35)/0.55)                                    # the branded header slides down at about half a second
            if hk > 0:
                fr = Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA')
                L = head.transform(head.size, Image.AFFINE, (1, 0, 0, 0, 1, int((1-hk)*660)))
                a = np.asarray(Image.alpha_composite(fr, L).convert('RGB')).astype(np.float32)
        if t >= P1:
            c = snow(card.copy(), t-P1, card_snow).clip(0, 255); k = ease((t-P1)/XF)
            a = c if k >= 1 else a*(1-k) + c*k
        a = a.clip(0, 255)
        if f in (0, 90, 175, 240): Image.fromarray(a.astype(np.uint8)).save(f'v/{key}-frame-{f:03d}.jpg', quality=92)
        p.stdin.write(a.astype(np.uint8).tobytes())
    p.stdin.close(); p.wait(); print(out)
    Image.open(f'v/{key}-feed-branded.png').convert('RGB').save(f'v/{key}-feed.png')
render('ombudsman', (657, 1254), 'snow'); render('lossiemouth', (654, 1213), 'shimmer')
