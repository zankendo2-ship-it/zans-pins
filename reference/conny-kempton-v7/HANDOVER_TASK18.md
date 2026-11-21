# Conny Kempton video: handover to the ETSY & SOCIAL chat (TASK 18), 21 Nov 2026

The master video thread is not building a v8. This file is everything that chat needs.

## 1. New images (in progress at the image hub)

Folder: /mnt/project-files/image-hub/2026-11-21/constitution-hill-kempton/ (with a CHECK note).

What the horse looks like in every image:
- Conny is a bay.
- The rider wears all-white silks and a black cap.
- The face is hidden naturally. There must be no black mask.

What the hub is making:
- A floodlit head-on opener clip, 2.5 to 3 seconds. The rail is on the viewer's left.
- A Christmas Hurdle jump at Kempton, with a grandstand and crowd. This replaces the rural hurdle.
- A close, powerful daylight shot on the Kempton all-weather for the September Stakes. That race was run in daylight on 5 Sep 2026.
- Face fixes on the 13 Nov stills B, G and H and on explainer 7.

The hub will post "done" in the notes thread.

## 2. Rejected v7 and why

Files are in /mnt/project-files/visibility/constitution-hill-who-rides/videos/v7/:
- scenes/ has the stills.
- main_A, main_B and main_C are the main cut with each music option.
- tiktok_A, tiktok_B and tiktok_C are the TikTok cut with each music option.

The coordinator failed it for these reasons:
1. In the hook, the rider's face reads as a black mask.
2. The legend scene shows a hurdle in a rural field, which looks like a point-to-point.
3. In the last-time scene the horse is tiny and seen from behind.
4. The end card is plain green with no image or motion.
5. The facts needed two sources each. That is done; see section 4.
6. Scenes 2 and 4 need checking against the same standard.

## 3. Voice (ready, brand voice, clean transcripts)

Folder: /mnt/project-files/visibility/constitution-hill-who-rides/voice_k4/. Its script.json lists the scene, file and text for each clip. Each clip is trimmed, with atempo 1.07 applied.

Main cut clips:
- k4_hook: "Can Constitution Hill win at Kempton on Wednesday?"
- k4_news: "He's heading back to Kempton for the Floodlit Stakes on Wednesday, with Oisin Murphy booked to ride." (file k4_news_murphy.mp3)
- k4_legend: "Champion Hurdle hero, Christmas Hurdle three years running and four wins from five at Kempton"
- k4_flat: "On the Flat this year, Oisin Murphy won on him at Southwell and Ryan Moore won on him at Kempton"
- k4_last: "Last time at Kempton he finished fourth, so can he bounce back?"
- k4_ask: "Can he win on Wednesday? Tell us in the comments."
- k4_end: "Come on Conny!"

TikTok cut clips (fan only):
- k4_tthook
- k4_ttlegend
- k4_ttflat
- k4_ttask
- k4_end

The TikTok cut has no race, no date and no win wording.

## 4. Verified facts (2+ sources each)

- **Oisin Murphy booked:** he is booked for the Listed Floodlit Stakes, Kempton, Wed 25 Nov. Sources: Racing Post (Scott Burton, 20 Nov) and Sporting Life (20 Nov). It is a booking, not yet a declaration; declarations are Mon 23 Nov.
- **Christmas Hurdle 3 in a row:** he won it in 2022, 2023 and 2024, each on 26 Dec at Kempton.
  - Sky Sports, 26 Dec 2024: "third Christmas Hurdle crown".
  - Racing Post, Lee Mottershead, 26 Dec 2024: "the now triple Ladbrokes Christmas Hurdle winner".
  - 2023: Jockey Club Kempton press release.
  - 2022: Sky Sports.
  - He did not run in the 2025 race. Sky Sports' result has Sir Gino winning, Golden Ace 2nd and Rubaud 3rd.
- **Kempton, 4 wins from 5:** the three Christmas Hurdles, plus two Flat runs.
  - Win on 25 Mar 2026 under Ryan Moore, on a floodlit Wednesday night. Sources: At The Races and Sky Sports.
  - 4th in the G3 September Stakes on 5 Sep 2026.
- **2026 Flat wins:** Southwell, ridden by Murphy, and Kempton, ridden by Moore.
- **Silks:** all white with a black cap. Sources: Sporting Life silk images for 25 Mar and 5 Sep 2026, plus a Sky Sports photo. Never name the owner.

## 5. Build kit

Folder: /mnt/project-files/visibility/constitution-hill-who-rides/build/
- **gen.py** writes the scenes; the k7_* scenes are the latest set. Its SMALL table places each photo above the text box using zoom, focal point and target y, over a blurred fill.
- **Render the scenes:** `python3 gen.py`, then `node shot.js $PWD <names>`.
- **Build the video:** `python3 build5.py main|tt <music.mp3> <out.mp4> ../voice_k4`. The hook uses img/copen.mp4; replace that with the hub's new opener.
- **Music:** Mixkit 1069, 1076 and 12, from /mnt/project-files/visibility/mug-reach/sounds/.

## 6. Alex's process

1. The coordinator does a strict review of the stills first.
2. Alex approves the stills scene by scene.
3. Then the video is built with 3 music options.

Keep "Come on Conny!!!!" on screen; that was Alex's request on 12 Nov.
