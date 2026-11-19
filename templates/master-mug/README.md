# The ZANS master mug (locked 19 Nov 2026)

Alex, 19 Nov 2026: "Why can you not get the mugs right!!!" From now on there is ONE mug. Every mug picture and video wraps the print onto this model. No more generated or redrawn mugs.

- `mug.json`: the mug in centimetres (8.2 wide, 9.5 high, flat base with a small rounded edge, black rim and inside, one smooth black D handle). Locked: never changed per video.
- `render.js`: `node templates/master-mug/render.js <out.png> '<json>'` renders it with a clear background, plain or with a flat print from `templates/mug-flats/` (made by `node templates/mug_flat.js` from the website designer).
- `overlay.py`: the pass/fail picture. It draws the model's outline over Alex's real mug photo (`reference/real-mug-fact-to-file.jpg`). Photo angle: `{"az":26,"el":36,"fov":54,"fill":0.75}`.
- `build_handle.py`: builds `handle_mesh.json`, the handle and its joins as ONE blended surface (the strap melts into the wall with a moulded fillet, as glazed ceramic does; no cut ends; as on Alex's real mug the first half-centimetre of each join is body-white and the handle colour starts after it). Run only if the handle in `mug.json` changes, then get a new all-angles sign-off.
- `proof.py`: rebuilds every picture in `proof/`.
- `handle_path.py`: how the handle path in `mug.json` was made (one oval D: top 8.45 cm, bottom 2.3 cm, reach 3.05 cm, arms 0.4 cm).
- `proof/`: the stills shown to the reviewer and to Alex.
- `three.min.js`: the 3D library (three.js 0.150.1, MIT licence, see THREE-LICENSE.txt), kept here so the render never depends on the network.
