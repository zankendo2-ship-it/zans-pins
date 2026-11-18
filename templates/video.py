"""Locked ZANS 3-part video (Alex, 17 Nov 2026), 9 seconds at 1080x1920:
  0.0-4.0s  slide 1: slow push-in on the product photo, thin metal strip top and bottom only, no text (as the locked reference)
  4.0-6.5s  slide 2: the hook card (carousel_hook.html), gentle snow
  6.5-10.8s slide 3: the end-card (carousel_endcard.html), falling snow
The footer sits in the same place in all three clips, so nothing at the bottom ever moves.
Usage: python3 templates/video.py <cards_dir> <scene.png> <key> <cx> <cy> <snow|shimmer> <out_dir> [music.m4a]"""
import os, sys, subprocess, numpy as np, imageio_ffmpeg
from PIL import Image, ImageFilter
FF = imageio_ffmpeg.get_ffmpeg_exe(); FPS, W, H = 30, 1080, 1920
P1, XF = 4.0, 0.35
P2 = float(os.environ.get('ZANS_P2', 6.5))        # slide 3 starts once the woman's lines have finished (never earlier than 6.5s)
TOTAL = float(os.environ.get('ZANS_TOTAL', 10.8)) # runs until Santa has finished; voices are never sped up to fit
ZOOM = float(os.environ.get('ZANS_ZOOM', 0.16))      # push-in amount; 0.16 = the locked reference
KEEP = float(os.environ.get('ZANS_KEEP_R', 380))     # radius around the product the light shimmer never touches
ease = lambda x: 0 if x <= 0 else 1 if x >= 1 else x*x*(3-2*x)
def flakes(seed, n, rmin, rmax, smin, smax):
    r = np.random.default_rng(seed)
    return [(r.uniform(0, W), r.uniform(0, H), r.uniform(rmin, rmax), r.uniform(smin, smax), r.uniform(0, 6.28), r.uniform(.45, .95)) for _ in range(n)]
ky, kx = np.mgrid[-16:17, -16:17].astype(np.float32)
def snow(arr, t, fl, drift=22):
    for (x, y, r, sp, ph, op) in fl:
        yy = (y + sp*t) % (H+40) - 20; xx = (x + drift*np.sin(ph + t*0.8)) % W; xi, yi = int(xx), int(yy)
        if 16 <= xi < W-16 and 16 <= yi < H-16: arr[yi-16:yi+17, xi-16:xi+17] += (np.exp(-(kx**2+ky**2)/(2*r*r))*255*op)[..., None]
    return arr
def main(cards, scene, key, CX, CY, mode, out_dir, music=None):
    master = Image.open(scene).convert('RGB'); MW, MH = master.size
    m = np.asarray(master).astype(np.float32)/255
    if mode == 'shimmer':
        warm = np.clip((m[..., 0]-0.6)*2.5, 0, 1) * (m[..., 0] > m[..., 2]*1.2)
        yy, xx = np.mgrid[0:MH, 0:MW]; warm *= (((xx-CX)/KEEP)**2 + ((yy-CY)/(KEEP*1.03))**2 > 1)
        glow = np.asarray(Image.fromarray((warm*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(20))).astype(np.float32)/255
        phase = (np.sin(xx/150.0)*1.9 + np.cos(yy/190.0)*2.1).astype(np.float32)
    frame = Image.open(f'{cards}/{key}-9x16-frame.png').convert('RGBA')
    hook = np.asarray(Image.open(f'{cards}/{key}-9x16-hook.png').convert('RGB')).astype(np.float32)
    end = np.asarray(Image.open(f'{cards}/{key}-9x16-end.png').convert('RGB')).astype(np.float32)
    scene_snow, card_snow = flakes(3, 70, 1.6, 4.2, 40, 110), flakes(7, 110, 2.0, 6.0, 70, 190)
    out = f'{out_dir}/{key}-video.mp4'
    audio = ['-i', music] if music else ['-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo']
    p = subprocess.Popen([FF, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', *audio,
        '-shortest', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for f in range(int(FPS*TOTAL)):
        t = f/FPS
        if t < P1 + XF:
            src = m if mode != 'shimmer' else (m + (glow*(0.5+0.5*np.sin(phase + t*2.2))*0.35)[..., None]*np.array([1.0, .82, .5], dtype=np.float32))
            img = Image.fromarray((src.clip(0, 1)*255).astype(np.uint8))
            k = ease(min(t, P1+XF)/(P1+XF)); z = 1.0 + ZOOM*k; cw, ch = MW/z, MH/z
            x0 = min(max(MW/2 + (CX-MW/2)*k - cw/2, 0), MW-cw); y0 = min(max(MH/2 + (CY-MH/2)*k - ch/2, 0), MH-ch)
            a = np.asarray(img.resize((W, H), Image.BICUBIC, box=(x0, y0, x0+cw, y0+ch))).astype(np.float32)
            if mode == 'snow': a = snow(a, t, scene_snow, 14)
            a = np.asarray(Image.alpha_composite(Image.fromarray(a.clip(0, 255).astype(np.uint8)).convert('RGBA'), frame).convert('RGB')).astype(np.float32)
        if P1 <= t:
            c = snow(hook.copy(), t-P1, card_snow).clip(0, 255); k = ease((t-P1)/XF); a = c if k >= 1 else a*(1-k) + c*k
        if P2 <= t:
            c = snow(end.copy(), t-P2, card_snow).clip(0, 255); k = ease((t-P2)/XF); a = c if k >= 1 else a*(1-k) + c*k
        a = a.clip(0, 255)
        if f in (0, 60, 165, 250): Image.fromarray(a.astype(np.uint8)).save(f'{out_dir}/{key}-frame-{f:03d}.jpg', quality=92)
        p.stdin.write(a.astype(np.uint8).tobytes())
    p.stdin.close(); p.wait()
    # feed carousel: slide 1 = the photo with its metal strips, slides 2 and 3 = the cards
    fh = int(MW*1350/1080); y0 = int(min(max(CY - fh*0.52, 0), MH-fh))
    s1 = master.crop((0, y0, MW, y0+fh)).resize((1080, 1350), Image.LANCZOS).convert('RGBA')
    Image.alpha_composite(s1, Image.open(f'{cards}/{key}-4x5-frame.png').convert('RGBA')).convert('RGB').save(f'{out_dir}/{key}-slide1.png')
    Image.open(f'{cards}/{key}-4x5-hook.png').convert('RGB').save(f'{out_dir}/{key}-slide2.png')
    Image.open(f'{cards}/{key}-4x5-end.png').convert('RGB').save(f'{out_dir}/{key}-slide3.png')
    print(out)
if __name__ == '__main__':
    a = sys.argv[1:]; main(a[0], a[1], a[2], int(a[3]), int(a[4]), a[5], a[6], a[7] if len(a) > 7 else None)
