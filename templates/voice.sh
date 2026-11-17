#!/bin/bash
# Brand voiceover (slides 1-2) + Santa (slide 3) for one post, mixed to 9.5 s.  Usage: templates/voice.sh <key> <out.m4a> [music.m4a]
# The line for <key> comes from templates/voice_lines.txt ("key|text"). Needs edge-tts and the environment to allow speech.platform.bing.com.
set -e; K=$1; OUT=$2; MUS=$3; T=$(mktemp -d); FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
LINE=$(grep "^$K|" "$(dirname "$0")/voice_lines.txt" | cut -d'|' -f2-)
edge-tts --proxy "$HTTPS_PROXY" --voice en-GB-LibbyNeural --rate=+6% --text "$LINE" --write-media $T/v.mp3 >/dev/null
edge-tts --proxy "$HTTPS_PROXY" --voice en-GB-RyanNeural --pitch=-14Hz --rate=+30% --text "Ho, ho, ho! Merry Christmas from Zans Racing!" --write-media $T/s.mp3 >/dev/null
TRIM="silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"
$FF -v error -y -i $T/v.mp3 -af $TRIM -ar 44100 -ac 2 $T/v.wav; $FF -v error -y -i $T/s.mp3 -af $TRIM -ar 44100 -ac 2 $T/s.wav
D=$($FF -i $T/v.wav 2>&1 | grep -o "Duration: [0-9:.]*" | cut -d: -f4); TEMPO=$(python3 -c "print(max(1.0, min(1.15, $D/6.05)))")
if [ -n "$MUS" ]; then   # subtle background music, well under the voices
  $FF -v error -y -i $T/v.wav -i $T/s.wav -i "$MUS" -filter_complex "[0]atempo=$TEMPO,adelay=200|200[a];[1]adelay=6380|6380[b];[2]volume=0.22[m];[a][b][m]amix=inputs=3:normalize=0,alimiter=limit=0.95,apad=whole_dur=9.5,atrim=0:9.5" -c:a aac -b:a 160k "$OUT"
else
  $FF -v error -y -i $T/v.wav -i $T/s.wav -filter_complex "[0]atempo=$TEMPO,adelay=200|200[a];[1]adelay=6380|6380[b];[a][b]amix=inputs=2:normalize=0,apad=whole_dur=9.5,atrim=0:9.5" -c:a aac -b:a 160k "$OUT"
fi
echo "$OUT (voice ${D}s, tempo $TEMPO)"
