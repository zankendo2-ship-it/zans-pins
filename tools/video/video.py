"""8-second 1080x1920 video: slow push-in on the photographed bauble, soft twinkle in the fairy lights, one headline."""
import subprocess, numpy as np, imageio_ffmpeg
from PIL import Image, ImageFilter
FF = imageio_ffmpeg.get_ffmpeg_exe(); FPS, SECS, W, H = 30, 8, 1080, 1920
CX, CY = 725, 1164                      # bauble centre in the 1296x2304 master
ease = lambda x: 0 if x <= 0 else 1 if x >= 1 else x*x*(3-2*x)
def render(key):
    master = Image.open(f'v/scene-{key}.png').convert('RGB'); MW, MH = master.size
    head = Image.open(f'v/{key}-v-head.png').convert('RGBA')
    # the scene's own fairy lights: a blurred map of its bright warm spots, used to make them breathe
    m = np.asarray(master).astype(np.float32)/255
    warm = np.clip((m[..., 0]-0.55)*2.2, 0, 1) * (m[..., 0] > m[..., 2]*1.25)
    yy, xx = np.mgrid[0:MH, 0:MW]
    warm *= (((xx-CX)/400.0)**2 + ((yy-CY)/450.0)**2 > 1)        # never on the bauble
    glow = np.asarray(Image.fromarray((warm*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(26))).astype(np.float32)/255
    phase = (np.sin(xx/170.0)*1.7 + np.cos(yy/210.0)*2.3).astype(np.float32)   # neighbouring lights twinkle out of step
    tint = np.array([1.0, 0.80, 0.42], dtype=np.float32)
    out = f'v/{key}.mp4'
    p = subprocess.Popen([FF, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
        '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p',
        '-c:a', 'aac', '-b:a', '64k', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    for f in range(FPS*SECS):
        t = f/FPS
        tw = glow * (0.5+0.5*np.sin(phase + t*2.4)) * 0.55
        frame = Image.fromarray(((m + tw[..., None]*tint).clip(0, 1)*255).astype(np.uint8))
        z = 1.0 + 0.12*ease(t/SECS); cw, ch = MW/z, MH/z
        fx, fy = MW/2 + (CX-MW/2)*ease(t/SECS)*0.7, MH/2 + (CY-150-MH/2)*ease(t/SECS)*0.7
        x0, y0 = min(max(fx-cw/2, 0), MW-cw), min(max(fy-ch/2, 0), MH-ch)
        fr = frame.resize((W, H), Image.BICUBIC, box=(x0, y0, x0+cw, y0+ch)).convert('RGBA')
        k = ease((t-1.0)/0.5)                                       # headline fades in from 1.0 to 1.5 seconds
        if k > 0:
            L = head if k >= 1 else Image.merge('RGBA', (*head.split()[:3], head.split()[3].point(lambda v: int(v*k))))
            fr = Image.alpha_composite(fr, L)
        if f in (0, 60, 235): fr.convert('RGB').save(f'v/{key}-frame-{f:03d}.jpg', quality=92)
        p.stdin.write(fr.convert('RGB').tobytes())
    p.stdin.close(); p.wait(); print(out)
    feed = master.resize((1080, 1920), Image.LANCZOS).crop((0, 140, 1080, 1490)).convert('RGBA')
    Image.alpha_composite(feed, Image.open(f'v/{key}-f.png').convert('RGBA')).convert('RGB').save(f'v/{key}-feed.png')
render('ombudsman'); render('lossiemouth')
