"""Three subtle Christmas backing tracks (public-domain carols), synthesised here, 9 seconds each, soft and low."""
import numpy as np, wave, subprocess, imageio_ffmpeg
SR = 44100; DUR = 9.0
def hz(n):  # note name like 'G4'
    names = {'C':-9,'C#':-8,'D':-7,'D#':-6,'E':-5,'F':-4,'F#':-3,'G':-2,'G#':-1,'A':0,'A#':1,'B':2}
    return 440*2**((names[n[:-1]] + 12*(int(n[-1])-4))/12)
def env(n, a, d):
    t = np.arange(n)/SR; return np.minimum(t/a, 1)*np.exp(-t/d)
def musicbox(f, n):   # bright, gentle, quick decay
    t = np.arange(n)/SR; e = env(n, 0.004, 0.55)
    return e*(np.sin(2*np.pi*f*t) + 0.35*np.sin(2*np.pi*2*f*t) + 0.12*np.sin(2*np.pi*4.01*f*t))
def bell(f, n):       # soft church-bell partials
    t = np.arange(n)/SR; e = env(n, 0.003, 0.9)
    return e*sum(a*np.sin(2*np.pi*f*r*t) for r, a in ((1, 1), (2.0, .45), (2.76, .3), (5.4, .12)))
def piano(f, n):      # warm, rounded
    t = np.arange(n)/SR; e = env(n, 0.01, 0.8)
    return e*(np.sin(2*np.pi*f*t) + 0.5*np.sin(2*np.pi*2*f*t)*np.exp(-t/0.3) + 0.2*np.sin(2*np.pi*3*f*t)*np.exp(-t/0.2))
def pad(fs, n):       # very quiet held chord under the tune
    t = np.arange(n)/SR; e = np.minimum(t/0.6, 1)*np.minimum((n/SR - t)/0.6, 1)
    return e*sum(np.sin(2*np.pi*f*t)*0.5 + np.sin(2*np.pi*f*1.003*t)*0.5 for f in fs)/len(fs)
def render(name, voice, notes, beat, chords, sleigh=False):
    out = np.zeros(int(SR*(DUR+1)))
    t0 = 0.35
    for n, b in notes:
        if n != '-':
            k = int(SR*t0); L = int(SR*min(2.5, DUR+1-t0)); out[k:k+L] += 0.32*voice(hz(n), L)[:len(out)-k]
        t0 += b*beat
        if t0 > DUR - 0.6: break
    for i, (ch, start, length) in enumerate(chords):
        k = int(SR*start); L = int(SR*length); out[k:k+L] += 0.10*pad([hz(c) for c in ch], L)[:len(out)-k]
    if sleigh:   # faint sleigh-bell shimmer on the beat
        rng = np.random.default_rng(1)
        for s in np.arange(0.35, DUR-0.5, beat):
            k = int(SR*s); L = int(SR*0.12); out[k:k+L] += 0.035*rng.standard_normal(L)*env(L, 0.001, 0.03)
    out = out[:int(SR*DUR)]
    fade = np.ones_like(out); fl = int(SR*1.2); fade[-fl:] = np.linspace(1, 0, fl); fade[:int(SR*0.2)] = np.linspace(0, 1, int(SR*0.2))
    out = out*fade; out = 0.5*out/np.max(np.abs(out))          # quiet: peaks at half volume, under any voiceover
    # simple room reverb
    rev = out.copy()
    for d, g in ((0.031, .25), (0.047, .2), (0.083, .15), (0.121, .1)):
        k = int(SR*d); rev[k:] += g*out[:-k]
    rev = 0.5*rev/np.max(np.abs(rev))
    pcm = (np.stack([rev, np.roll(rev, 90)], 1)*32767).astype(np.int16)
    with wave.open(f'music/{name}.wav', 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-loglevel', 'error', '-i', f'music/{name}.wav', '-c:a', 'aac', '-b:a', '160k', f'music/{name}.m4a'], check=True)
    print(name)
# 1: We Wish You a Merry Christmas, music box, 3/4
w = [('D5',1),('G5',1),('G5',.5),('A5',.5),('G5',.5),('F#5',.5),('E5',1),('E5',1),('E5',1),('A5',1),('A5',.5),('B5',.5),('A5',.5),('G5',.5),('F#5',1),('D5',1),('D5',1),('B5',1),('B5',.5),('C6',.5),('B5',.5),('A5',.5),('G5',1),('E5',1)]
render('1-music-box-we-wish-you', musicbox, w, 0.5, [(('G3','B3','D4'), .3, 1.6), (('C4','E4','G4'), 1.8, 1.5), (('A3','C4','E4'), 3.3, 1.5), (('D4','F#4','A4'), 4.8, 1.5), (('G3','B3','D4'), 6.3, 2.7)], sleigh=True)
# 2: Deck the Halls, soft bells, 4/4
d = [('G5',1.5),('F5',.5),('E5',1),('D5',1),('C5',1),('D5',1),('E5',1),('C5',1),('D5',.5),('E5',.5),('F5',.5),('D5',.5),('E5',1.5),('D5',.5),('C5',1),('B4',1),('C5',2)]
render('2-soft-bells-deck-the-halls', bell, d, 0.42, [(('C4','E4','G4'), .3, 2.0), (('G3','B3','D4'), 2.3, 1.6), (('F3','A3','C4'), 3.9, 1.7), (('G3','B3','D4'), 5.6, 1.4), (('C4','E4','G4'), 7.0, 2.0)])
# 3: Silent Night, warm piano, slow
s = [('G4',1.5),('A4',.5),('G4',1),('E4',3),('G4',1.5),('A4',.5),('G4',1),('E4',3),('D5',2),('D5',1),('B4',3)]
render('3-warm-piano-silent-night', piano, s, 0.5, [(('C3','E3','G3'), .3, 3.0), (('C3','E3','G3'), 3.3, 3.0), (('G2','B2','D3'), 6.3, 2.7)])
