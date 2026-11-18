"""Original, copyright-free 'race day' music bed, made note by note in code (no samples, no existing tune).
A driving but subtle pulse: soft kick, plucked bass, warm pad and a light arpeggio in A minor at 112 bpm.
Usage: python3 templates/music_race.py <out.wav> [seconds]"""
import sys, wave, numpy as np
out = sys.argv[1]; dur = float(sys.argv[2]) if len(sys.argv) > 2 else 30.0
SR = 44100; bpm = 112; beat = 60 / bpm; n = int(SR * dur); t = np.arange(n) / SR; mix = np.zeros(n)
f = lambda m: 440 * 2 ** ((m - 69) / 12)
def add(start, sig):
    i = int(start * SR)
    if i >= n: return
    sig = sig[: n - i]; mix[i:i + len(sig)] += sig
def pluck(m, L, a):
    x = np.arange(int(L * SR)) / SR; return a * (np.sin(2*np.pi*f(m)*x) + 0.35*np.sin(4*np.pi*f(m)*x)) * np.exp(-x * 5)
def kick(a):
    x = np.arange(int(0.22 * SR)) / SR; return a * np.sin(2*np.pi*(95*np.exp(-x*22) + 45)*x) * np.exp(-x * 14)
def pad(ms, L, a):
    x = np.arange(int(L * SR)) / SR; env = np.minimum(1, x / 0.5) * np.minimum(1, (L - x) / 0.5)
    return a * env * sum(np.sin(2*np.pi*f(m)*x) + 0.5*np.sin(2*np.pi*f(m)*1.004*x) for m in ms) / len(ms)
CH = [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (43, [55, 59, 62])]   # Am F C G
bars = int(dur / (4 * beat)) + 1
for b in range(bars):
    root, tri = CH[b % 4]; t0 = b * 4 * beat
    add(t0, pad(tri, 4 * beat, 0.16))
    for k in range(4):
        add(t0 + k * beat, kick(0.5)); add(t0 + k * beat, pluck(root, beat * .9, 0.3)); add(t0 + (k + .5) * beat, pluck(root + 12, beat * .45, 0.16))
    for k in range(8):
        add(t0 + k * beat / 2, pluck(tri[k % 3] + 12, beat * .5, 0.11))
mix *= np.minimum(1, t / 0.8) * np.minimum(1, (dur - t) / 1.5); mix = np.tanh(mix * 1.2) * 0.7
st = (np.stack([mix, mix], 1) * 32767).astype('<i2')
w = wave.open(out, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes()); w.close()
