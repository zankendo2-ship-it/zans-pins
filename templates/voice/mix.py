"""Mix one post's soundtrack: the London woman's clips (slides 1-2), then Santa (slide 3), over quiet music.
Voices are never sped up: the video is made as long as the voices need. Prints P2 and TOTAL for templates/video.py.
Usage: python3 templates/voice/mix.py <clips_dir> <out.m4a> <music.wav> <santa.mp3> <clip1.mp3> [clip2.mp3 ...]"""
import subprocess, sys, re, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
TRIM = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
def trimmed(src, dst):
    subprocess.run([FF, "-nostdin", "-v", "error", "-y", "-i", src, "-af", TRIM, "-ar", "44100", "-ac", "2", dst], check=True)
    out = subprocess.run([FF, "-nostdin", "-i", dst], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out); return int(m.group(2))*60 + float(m.group(3))
d, out, music, santa, clips = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:]
t = 0.3; ins = []; parts = []
for i, c in enumerate(clips):
    L = trimmed(f"{d}/{c}", f"{d}/_t{i}.wav"); ins.append((f"{d}/_t{i}.wav", t)); t += L + 0.3
p2 = max(6.5, round(t + 0.05, 2))
Ls = trimmed(f"{d}/{santa}", f"{d}/_ts.wav"); ins.append((f"{d}/_ts.wav", p2 + 0.25)); total = round(p2 + 0.25 + Ls + 0.6, 2)
cmd = [FF, "-nostdin", "-v", "error", "-y"]
for f, _ in ins: cmd += ["-i", f]
cmd += ["-i", music]
fc = "".join(f"[{i}]adelay={int(s*1000)}|{int(s*1000)}[v{i}];" for i, (_, s) in enumerate(ins))
n = len(ins)
fc += f"[{n}]volume=0.30,atrim=0:{total},afade=t=out:st={total-1.2}:d=1.2[m];" + "".join(f"[v{i}]" for i in range(n)) + f"[m]amix=inputs={n+1}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,apad=whole_dur={total},atrim=0:{total}"
subprocess.run(cmd + ["-filter_complex", fc, "-ar", "44100", "-c:a", "aac", "-b:a", "160k", out], check=True)
print(p2, total)
