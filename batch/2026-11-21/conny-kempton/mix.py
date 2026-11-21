"""Sets each scene's length from its voice clip (voices are never cut), then mixes voice + a quiet music bed (music at 0.30, whole mix -14 LUFS).
python3 mix.py main|tiktok <music.wav> <out.m4a>   (rewrites the scene durations in scenes.json)"""
import json, os, subprocess, sys, imageio_ffmpeg
D = os.path.dirname(os.path.abspath(__file__)); cut, music, out = sys.argv[1:4]; FF = imageio_ffmpeg.get_ffmpeg_exe(); S = json.load(open(D + '/scenes.json'))
def dur(f):
    r = subprocess.run([FF, '-i', f], capture_output=True, text=True).stderr; h, m, s = r.split('Duration: ')[1].split(',')[0].split(':'); return int(h) * 3600 + int(m) * 60 + float(s)
t = 0.0; ins = []; fl = []
for i, s in enumerate(S[cut]):
    f = f"{D}/voice/ck_{s['key']}.mp3"; d = dur(f); lead = 0.25 if i == 0 else 0.18; tail = 0.9 if i == len(S[cut]) - 1 else 0.22
    s['dur'] = round(lead + d + tail, 2); ins += ['-i', f]; fl.append(f"[{i}:a]adelay={int((t + lead) * 1000)}:all=1[v{i}]"); t += s['dur']
json.dump(S, open(D + '/scenes.json', 'w'), indent=1, ensure_ascii=False); n = len(S[cut])
fc = ';'.join(fl) + ';' + ''.join(f'[v{i}]' for i in range(n)) + f"amix=inputs={n}:normalize=0[vo];[{n}:a]volume=0.30,afade=t=in:d=0.4,afade=t=out:st={t - 1.2}:d=1.2[mu];[vo][mu]amix=inputs=2:normalize=0,atrim=0:{t},loudnorm=I=-14:TP=-1.5:LRA=11[a]"
subprocess.run([FF, '-y', '-loglevel', 'error'] + ins + ['-i', music, '-filter_complex', fc, '-map', '[a]', '-c:a', 'aac', '-b:a', '192k', out], check=True); print(cut, 'total', round(t, 2))
