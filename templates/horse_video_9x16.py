"""Racehorse post video: the guide-look slides with a slow zoom, the London woman's voice (Gemini Aoede) and a quiet music bed.
Voices are never sped up: each slide stays up as long as its clips need. Output 1080x1920 (TikTok, native 9:16), 30 fps.
Usage: python3 templates/horse_video.py <out.mp4> <music.wav> <clips_dir> <slide1.png>=<clipA,clipB> <slide2.png>=<clipC> ..."""
import subprocess, sys, re, os, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
TRIM = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
out, music, cd, segs = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
def trimmed(src, dst):
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", src, "-af", TRIM, "-ar", "44100", "-ac", "2", dst], check=True)
    e = subprocess.run([FF, "-nostdin", "-i", dst], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", e); return int(m.group(2)) * 60 + float(m.group(3))
XF, GAP, FPS = 0.4, 0.35, 30
t = 0.0; voice = []; slides = []; k = 0
for s in segs:
    png, clips = s.split("="); start = t; t += 0.45
    for c in clips.split(","):
        w = f"{cd}/_t{k}.wav"; k += 1; L = trimmed(f"{cd}/{c}", w); voice.append((w, t)); t += L + GAP
    t += 0.35; slides.append((png, start, t))
total = round(t + 0.8, 2)
cmd = [FF, "-nostdin", "-v", "error", "-y"]; fc = ""
for i, (png, a, b) in enumerate(slides):
    d = (b - a) + XF + (0.8 if i == len(slides) - 1 else 0); cmd += ["-loop", "1", "-t", f"{d:.2f}", "-i", png]
    fr = int(d * FPS) + 2
    fc += f"[{i}]scale=2160:3840,zoompan=z='1+0.10*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps={FPS},trim=0:{d:.2f},setpts=PTS-STARTPTS,format=yuv420p[s{i}];"
prev = "s0"
for i in range(1, len(slides)):
    fc += f"[{prev}][s{i}]xfade=transition=fade:duration={XF}:offset={slides[i][1]:.2f}[x{i}];"; prev = f"x{i}"
n = len(slides)
for j, (w, s) in enumerate(voice): cmd += ["-i", w]; fc += f"[{n+j}]adelay={int(s*1000)}|{int(s*1000)}[v{j}];"
cmd += ["-i", music]
fc += f"[{n+len(voice)}]volume=0.30,atrim=0:{total},afade=t=out:st={total-1.2}:d=1.2[m];" + "".join(f"[v{j}]" for j in range(len(voice))) + f"[m]amix=inputs={len(voice)+1}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,apad=whole_dur={total},atrim=0:{total}[a]"
subprocess.run(cmd + ["-filter_complex", fc, "-map", f"[{prev}]", "-map", "[a]", "-t", str(total), "-r", str(FPS), "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out], check=True)
print("total", total, [(os.path.basename(p), round(a, 2), round(b, 2)) for p, a, b in slides])
