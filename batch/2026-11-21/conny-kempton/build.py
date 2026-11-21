"""Builds the Constitution Hill at Kempton video from scenes.json: a moving picture (push/track + drifting kickback dust) under the card overlays.
python3 build.py main|tiktok <out.mp4> [audio.m4a] [--stills DIR]   Card text fades in at 1.0 s on the opener and 0.35 s on later scenes."""
import json, os, subprocess, sys, numpy as np, cv2, imageio_ffmpeg
D = os.path.dirname(os.path.abspath(__file__)); S = json.load(open(D + '/scenes.json')); cut = sys.argv[1]; out = sys.argv[2]
audio = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith('--') else None; stills = sys.argv[sys.argv.index('--stills') + 1] if '--stills' in sys.argv else None
FPS, W, H = 30, 1080, 1920; rng = np.random.default_rng(7)
rgba = lambda f: cv2.imread(f, cv2.IMREAD_UNCHANGED).astype(np.float32)
base = rgba(D + '/ov/base.png'); P = rng.random((150, 5))                     # dust: x, y, size, speed, phase
def over(fr, ov, a=1.0):
    al = ov[..., 3:4] / 255.0 * a; return fr * (1 - al) + ov[..., :3] * al
def view(pic, c, dark):
    cx, cy, z = c; h, w = pic.shape[:2]; vw = w / z * (W / H) / (w / h) if w / h > W / H else w / z; vh = vw * H / W
    vw, vh = min(vw, w), min(vw * H / W, h); x0 = np.clip(cx - vw / 2, 0, w - vw); y0 = np.clip(cy - vh * 0.36, 0, h - vh)   # the subject sits in the top half
    M = np.float32([[W / vw, 0, -x0 * W / vw], [0, H / vh, -y0 * H / vh]]); return cv2.warpAffine(pic, M, (W, H), flags=cv2.INTER_LANCZOS4) * dark
def dust(fr, t):
    for x, y, s, v, ph in P:
        px = int((x + 0.03 * np.sin(t * 0.7 + ph * 6)) * W) % W; py = int(((y - t * (0.02 + 0.05 * v)) % 1) * 1150); r = 1 + int(s * 2.4)
        a = 0.10 + 0.22 * s * (0.5 + 0.5 * np.sin(t * 2 + ph * 9)); cv2.circle(fr, (px, py), r, (200 * a + fr[py, px, 0] * (1 - a), 215 * a + fr[py, px, 1] * (1 - a), 235 * a + fr[py, px, 2] * (1 - a)), -1, cv2.LINE_AA)
    return fr
cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-'] + (['-i', audio] if audio else []) + \
      ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium'] + (['-c:a', 'aac', '-b:a', '192k', '-shortest'] if audio else []) + ['-movflags', '+faststart', out]
ff = subprocess.Popen(cmd, stdin=subprocess.PIPE); T = 0.0
for i, s in enumerate(S[cut]):
    sf = s.get('sf', 2); n = int(round(s['dur'] * FPS)); clip = None
    if s.get('clip'):                                    # a real moving clip, slowed to fill the scene (frames blended, so no jumps)
        src = D + '/' + s['clip']; cd = float(subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-i', src], capture_output=True, text=True).stderr.split('Duration: ')[1].split(',')[0].split(':')[2])
        raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-loglevel', 'error', '-i', src, '-vf', f"setpts={s['dur'] / cd:.4f}*PTS,minterpolate=fps={FPS}:mi_mode=blend", '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], capture_output=True).stdout
        clip = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    else:
        pic = cv2.imread(f"{D}/pics/{s['pic']}.png").astype(np.float32)
        if sf != 1: pic = cv2.resize(pic, None, fx=sf, fy=sf, interpolation=cv2.INTER_CUBIC)
        pad = cv2.copyMakeBorder(pic, 0, 1200, 0, 0, cv2.BORDER_REFLECT); pad[pic.shape[0]:] *= 0.3; pic = pad   # dark room below the picture, so low subjects can be framed above the card
    card = rgba(f"{D}/ov/{s['key']}.png")
    t_in = 1.0 if i == 0 else 0.35
    for k in range(n):
        u = k / max(1, n - 1); e = u * u * (3 - 2 * u) * 0.35 + u * 0.65; c = [sf * (a + (b - a) * e) if j < 2 else a + (b - a) * e for j, (a, b) in enumerate(zip(s['from'], s['to']))]
        if clip is not None: pic = clip[min(k, len(clip) - 1)].astype(np.float32)
        fr = dust(view(pic, c, s.get('dark', 1.0)), T + k / FPS); fr = over(fr, base); fr = over(fr, card, float(np.clip((k / FPS - t_in) / 0.3, 0, 1)))
        if k < 4 and i > 0: fr = fr * (0.55 + 0.15 * k)                        # a quick dip between scenes
        fr8 = np.clip(fr, 0, 255).astype(np.uint8); ff.stdin.write(fr8.tobytes())
        if stills and k == int(n * 0.72): os.makedirs(stills, exist_ok=True); cv2.imwrite(f"{stills}/{s['key']}.jpg", fr8, [cv2.IMWRITE_JPEG_QUALITY, 90])
    T += s['dur']
ff.stdin.close(); ff.wait(); print('done', out, round(T, 2))
