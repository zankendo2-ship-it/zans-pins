"""Moving-cuts video (tester for Alex, 19 Nov 2026): several quick shots cut from ONE approved product scene, each shot moving, the hook on screen from 1.0 s,
an A-or-B question with both choices on screen, then a short end card. Usage: python3 templates/moving.py <spec.json>
spec: {"scene": png (1296x2304), "out": mp4, "audio": m4a, "end_card": png (1080x1920), "ov_hook": png, "ov_question": png, "snow": bool, "end": seconds of end card,
       "shots": [{"dur": s, "from": [cx, cy, zoom], "to": [cx, cy, zoom]}], "hook_at": 1.0, "question_at": seconds}  zoom 1.0 = whole scene."""
import json, subprocess, sys, numpy as np, imageio_ffmpeg
from PIL import Image
FF = imageio_ffmpeg.get_ffmpeg_exe(); FPS, W, H = 30, 1080, 1920
ease = lambda x: 0 if x <= 0 else 1 if x >= 1 else x*x*(3-2*x)
def flakes(seed, n):
    r = np.random.default_rng(seed); return [(r.uniform(0, W), r.uniform(0, H), r.uniform(1.6, 4.6), r.uniform(60, 170), r.uniform(0, 6.28), r.uniform(.45, .95)) for _ in range(n)]
ky, kx = np.mgrid[-14:15, -14:15].astype(np.float32)
def snow(a, t, fl):
    for (x, y, r, sp, ph, op) in fl:
        yy = int((y + sp*t) % (H+40) - 20); xx = int((x + 20*np.sin(ph + t*0.8)) % W)
        if 14 <= xx < W-14 and 14 <= yy < H-14: a[yy-14:yy+15, xx-14:xx+15] += (np.exp(-(kx**2+ky**2)/(2*r*r))*255*op)[..., None]
    return a
def over(a, ov, k):
    if k <= 0: return a
    al = ov[..., 3:]/255.0*k; return a*(1-al) + ov[..., :3]*al
def main(s):
    sc = Image.open(s['scene']).convert('RGB'); MW, MH = sc.size
    hook = np.asarray(Image.open(s['ov_hook']).convert('RGBA')).astype(np.float32); ques = np.asarray(Image.open(s['ov_question']).convert('RGBA')).astype(np.float32)
    end = np.asarray(Image.open(s['end_card']).convert('RGB')).astype(np.float32); fl = flakes(5, 80)
    body = sum(x['dur'] for x in s['shots']); total = body + s.get('end', 2.0); XF = 0.3
    p = subprocess.Popen([FF, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', s['audio'], '-t', str(total),
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', s['out']], stdin=subprocess.PIPE)
    for f in range(int(FPS*total)):
        t = f/FPS
        if t < body + XF:
            tt = min(t, body - 1e-3); acc = 0
            for sh in s['shots']:
                if tt < acc + sh['dur']: break
                acc += sh['dur']
            k = (tt - acc)/sh['dur']; k = 0.15*k + 0.85*ease(k) if sh.get('ease', True) else k
            cx, cy, z = [a + (b - a)*k for a, b in zip(sh['from'], sh['to'])]; cw, ch = MW/z, MH/z
            x0 = min(max(cx - cw/2, 0), MW - cw); y0 = min(max(cy - ch/2, 0), MH - ch)
            a = np.asarray(sc.resize((W, H), Image.BICUBIC, box=(x0, y0, x0+cw, y0+ch))).astype(np.float32)
            if s.get('snow'): a = snow(a, t, fl)
            qa = s['question_at']
            a = over(a, hook, ease((t - s.get('hook_at', 1.0))/0.25)*(1 - ease((t - (qa - 0.25))/0.25)))
            a = over(a, ques, ease((t - qa)/0.25))
            if t > body: kk = ease((t - body)/XF); a = a*(1-kk) + (snow(end.copy(), t, fl) if s.get('snow_end', True) else end)*kk
        else: a = snow(end.copy(), t, fl) if s.get('snow_end', True) else end
        p.stdin.write(a.clip(0, 255).astype(np.uint8).tobytes())
    p.stdin.close(); p.wait(); print('done', s['out'], round(total, 2))
if __name__ == '__main__': main(json.load(open(sys.argv[1])))
