"""Official ZANS brand voices (CLAUDE.md 3.7): Google Gemini text-to-speech, copied EXACTLY from video_media/gemini_voice.py in the
HORSE-RACING-EXTRACTION- repo. Voices a script json ({"gemini": {"voice", "style"}, "lines": [{"file", "text"}]}), skipping clips that exist.
The key is never in this repo: the environment's network secret adds it to requests for generativelanguage.googleapis.com.
Usage: python3 templates/voice/gemini_tts.py <out_dir> <script.json> [<script.json> ...]"""
import base64, json, re, subprocess, sys, time, urllib.error, urllib.request
from pathlib import Path
import imageio_ffmpeg
API = "https://generativelanguage.googleapis.com/v1beta/models"
MODEL = "gemini-2.5-pro-preview-tts"
KEY = "added-by-the-environment-network-secret"     # placeholder: the proxy swaps in the real key
WRAP = "Speak naturally, with normal pauses, not like a robot or an advert."    # the locked wrapper; a script may carry its own under gemini.wrapper (Alex's 19 Nov trial)
def speak(text, voice, style, out_mp3, wrap=WRAP):
    prompt = f"Say ONLY the words between the <line> tags, once, then stop. Voice: {style}. {wrap}\n<line>{text}</line>"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    last = None
    for attempt in range(3):
        req = urllib.request.Request(f"{API}/{MODEL}:generateContent", data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
        try:
            with urllib.request.urlopen(req, timeout=180) as f:
                data = json.load(f)
            part = data["candidates"][0]["content"]["parts"][0]["inlineData"]
            pcm = base64.b64decode(part["data"])
            rate = int(re.search(r"rate=(\d+)", part.get("mimeType", "")).group(1)) if "rate=" in part.get("mimeType", "") else 24000
            subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(rate), "-ac", "1",
                            "-i", "-", "-b:a", "128k", str(out_mp3)], input=pcm, check=True)
            return
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read()[:300].decode(errors='replace')}"
            if e.code in (400, 402, 403, 404, 429): break          # billing / credit / access: stop and ask Alex, never swap voices
        except Exception as e:  # noqa: BLE001
            last = f"{type(e).__name__}: {e}"
        time.sleep(4 * (attempt + 1))
    raise RuntimeError(last)
def clip_len(f):
    out = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-i", str(f)], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out)
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
if __name__ == "__main__":
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    for p in map(Path, sys.argv[2:]):
        s = json.loads(p.read_text()); g = s["gemini"]
        for x in s["lines"]:
            f = out / x["file"]
            if f.exists(): continue
            limit = len(x["text"].split()) * 0.55 + 4
            for attempt in range(4):
                speak(x["text"], g["voice"], g["style"], f, g.get("wrapper", WRAP))
                if g.get("tempo"):                               # Alex's approved pace (19 Nov 2026): a small speed-up that keeps her pitch
                    t = f.with_suffix(".t.mp3"); subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-i", str(f), "-af", f"atempo={g['tempo']}", "-b:a", "128k", str(t)], check=True); t.replace(f)
                d = clip_len(f)
                print(f"{x['file']}: {d:.1f}s (limit {limit:.1f})", flush=True)
                if d <= limit: break
                f.unlink()
            else:
                print(f"GAVE UP {x['file']}")
