# The ZANS master mug (locked 19 Nov 2026)

Alex, 19 Nov 2026: "Why can you not get the mugs right!!!" From now on there is ONE mug. Every mug picture and video wraps the print onto this model. No more generated or redrawn mugs.

- `mug.json`: the mug in centimetres (8.2 wide, 9.5 high, flat base with a small rounded edge, black rim and inside, one smooth black D handle). Locked: never changed per video.
- `render.js`: `node templates/master-mug/render.js <out.png> '<json>'` renders it with a clear background, plain or with a flat print from `templates/mug-flats/` (made by `node templates/mug_flat.js` from the website designer).
- `overlay.py`: the pass/fail picture. It draws the model's outline over Alex's real mug photo (`reference/real-mug-fact-to-file.jpg`). Photo angle: `{"az":26,"el":36,"fov":54,"fill":0.75}`.
- `handle_path.py`: how the handle path in `mug.json` was made (top 8.1 cm, bottom 3.0 cm, reach 2.95 cm, corner radius 2.35 cm, with a 2.4 mm moulded fillet at each joint).
- `proof/`: the stills shown to the reviewer and to Alex.
- `three.min.js`: the 3D library (three.js 0.150.1, MIT licence, see THREE-LICENSE.txt), kept here so the render never depends on the network.
