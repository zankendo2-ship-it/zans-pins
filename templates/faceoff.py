"""Build one head-to-head (face-off) post from a small spec: the picture, the 3 slides, the voice, the video, the captions and phone stills.
Usage: python3 templates/faceoff.py <spec.json>          (run from the repo root)
spec = {"key": "h2h-<a>-<b>" (mugs) or "h2h-baubles-<a>-<b>", "product": "mug"|"bauble", "metal": "gold"|"silver",
 "a": {"name", "say" (how the voice says it, optional), "pattern", "c1", "c2", "handle" (mug), "cap" (bauble), "band": {"body","second","pattern"}},
 "b": {...}, "sub": "card sub-line", "say2": "second spoken line", "story": "caption sentence (may name the race)", "story_tiktok": "no race words",
 "scene": {"photo": "templates/scenes/pool/x.jpg", "light": "fire"|"overcast", "camY": n, "mugs": [[cx, base, h], [cx, base, h]], "crop": [x0, y0, w] (1.5x pixels),
           "discs": [[cx, cy, r], [cx, cy, r]] (1.5x pixels), "tint": [...], "cast": [...], "mode": "snow"|"shimmer"},
 "music": "batch/2026-11-17/music/<track>.m4a", "out": "batch/<date>/head-to-head"}
Nothing here posts or books anything."""
import json, os, subprocess, sys, glob, re, base64, urllib.request
from PIL import Image
sys.path.insert(0, 'templates'); import mapart2
STYLE = "a warm young woman from London with a natural everyday London accent who softens her t sounds the way Londoners do, like a friendly local chatting to a mate, upbeat and conversational, not posh, speaking at a slightly brisker pace, full of genuine excitement and enthusiasm, gripping the listener like she can't wait for this race"
WRAPPER = "Speak naturally and energetically, with short pauses, not like a robot or an advert."   # with STYLE and tempo 1.07: the voice Alex approved on 19 Nov 2026 ("Voice is perfect")
def run(cmd, env=None):
    r = subprocess.run(cmd, capture_output=True, text=True, env={**os.environ, **(env or {})})
    if r.returncode: sys.exit(f"FAILED {cmd[:3]}\n{r.stdout[-800:]}\n{r.stderr[-1500:]}")
    return r.stdout
def slug(n): return re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-')
def heard(f):
    b = base64.b64encode(open(f, 'rb').read()).decode()
    body = {"contents": [{"parts": [{"text": "Transcribe this audio exactly. Output only the words."}, {"inlineData": {"mimeType": "audio/mp3", "data": b}}]}]}
    r = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent", data=json.dumps(body).encode(),
                               headers={"Content-Type": "application/json", "x-goog-api-key": "added-by-the-environment-network-secret"})
    return json.load(urllib.request.urlopen(r, timeout=120))["candidates"][0]["content"]["parts"][0]["text"].strip()
def main(spec):
    K, P, A, B, SC, O = spec['key'], spec['product'], spec['a'], spec['b'], spec['scene'], spec['out']
    W = f'/tmp/zans-faceoff/{K}'; os.makedirs(W, exist_ok=True); os.makedirs(f'{O}/phone', exist_ok=True)
    scene = f"templates/scenes/{spec.get('scene_key', K)}.png"
    # 1. the picture
    if SC.get('reuse'):                                # copy-only redo: keep the approved picture, aim the zoom at the middle of the pair
        cx, cy = SC['focus']
        env = {"ZANS_STEAM": ";".join(f"{x},{y}" for x, y in SC['steam']), "ZANS_ZOOM": "0.08", "ZANS_KEEP_R": "640"} if P == 'mug' else {"ZANS_KEEP_R": "560"}
    elif P == 'mug':
        jobs = [[f'{s}.png', h['pattern'], h['c1'], h['c2'], h['handle'], h['name'], side, {"light": SC['light'], "turn": h.get('turn', 0.5), "camY": SC.get('camY', 3.6), "teaDrop": 0.34, **({"ring": h['ring']} if 'ring' in h else {})}]
                for s, h, side in (('ma', A, 'left'), ('mb', B, 'right'))]
        print(run(['node', 'templates/mug3d.js', W, json.dumps(jobs)]).strip())
        ps = {"tint": SC.get('tint', [1, 0.97, 0.93] if SC['light'] == 'fire' else [0.97, 0.98, 1.0]), "glint": [1, 0.87, 0.62] if SC['light'] == 'fire' else [0.9, 0.92, 0.95],
              "cast": SC.get('cast', [0, 0.45] if SC['light'] == 'fire' else [0, 0]), "bounce": 0.32,
              "mugs": [{"png": f'{W}/ma.png', "cx": SC['mugs'][0][0], "base": SC['mugs'][0][1], "h": SC['mugs'][0][2]}, {"png": f'{W}/mb.png', "cx": SC['mugs'][1][0], "base": SC['mugs'][1][1], "h": SC['mugs'][1][2]}]}
        json.dump(ps, open(f'{W}/place.json', 'w')); run(['python3', 'templates/place_mugs.py', SC['photo'], f'{W}/placed.png', f'{W}/place.json'])
        x0, y0, w = SC['crop']; h = round(w*16/9); k = 1296/w
        Image.open(f'{W}/placed.png').crop((x0, y0, x0+w, y0+h)).resize((1296, 2304), Image.LANCZOS).save(scene)
        mouths = [(round((m[0]*1.5-x0)*k), round(((m[1]-m[2])*1.5+0.19*m[2]*1.5-y0)*k)) for m in SC['mugs']]
        cx = round(sum(p[0] for p in mouths)/2); cy = round(((SC['mugs'][0][1]-SC['mugs'][0][2]/2)*1.5-y0)*k)
        env = {"ZANS_STEAM": ";".join(f"{x},{y}" for x, y in mouths), "ZANS_ZOOM": str(SC.get('zoom', 0.08)), "ZANS_KEEP_R": "640"}
        if 'focus' in SC: cx, cy = SC['focus']
    else:
        js = open('templates/cap_baubles.js').read()
        jl = "const jobs=[\n" + "".join(f" ['{s}.png',0,'{h['pattern']}','{h['c1']}','{h['c2']}','{h['cap']}',{json.dumps(h['name'])},'ZBA'],\n" for s, h in (('ba', A), ('bb', B))) + "];"
        open(f'{W}/cap.js', 'w').write(re.sub(r"const jobs=\[.*?\];", lambda m: jl, js, flags=re.S).replace("codes.includes(exp)?'MATCH':'MISMATCH'", "codes.length?'CODE':'NO CODE'"))
        print(run(['node', f'{W}/cap.js', W]).strip())
        Image.open(SC['photo']).convert('RGB').save(f'{W}/blank.png')
        (ax, ay, ar), (bx, by, br) = SC['discs']
        mapart2.build(f'{W}/ba.png', f'{W}/blank.png', (ax, ay), ar, f'{W}/one.png', skip=tuple(map(tuple, SC.get('skip_a', []))))
        mapart2.build(f'{W}/bb.png', f'{W}/blank.png', (bx, by), br, scene, base=f'{W}/one.png', skip=tuple(map(tuple, SC.get('skip_b', []))))
        cx, cy = round((ax+bx)/2), round(min((ay+by)/2 - 150, 1250)); env = {"ZANS_KEEP_R": "560"}
    # 2. the cards
    posts = json.load(open('templates/posts.json'))
    big = spec.get('big', f"{A['name']} or<br>{B['name']}?"); longest = max(len(x) for x in big.split('<br>')) + 1
    posts[K] = {"metal": spec.get('metal', 'gold'), "colour": "#1F5A3D", "eyebrow": spec.get('eyebrow', f"Head to head · {'mugs' if P == 'mug' else 'baubles'} in their colours"), "big": big,
                "bigSize": round(min(0.74, 11.4/longest), 2), "sub": spec['sub'], "question": spec.get('question', "Which one are you cheering?"),
                "silks": {**A['band'], "cap": A.get('cap', A['band']['body'])}, "silks2": {**B['band'], "cap": B.get('cap', B['band']['body'])}}
    json.dump(posts, open('templates/posts.json', 'w'), indent=1, ensure_ascii=False)
    run(['node', 'templates/render.js', W, K]); run(['python3', 'templates/silks_bands.py', W, K])
    # 3. the voice (brand voice, each clip transcribed and compared)
    V = 'templates/voice/clips'; pair = f"{slug(A['name'])}-{slug(B['name'])}"
    lines = spec.get('lines') or [{"file": f"zp_fo_{pair}_1.mp3", "text": f"{A.get('say', A['name'])} or {B.get('say', B['name'])}?"}, {"file": f"zp_fo_{slug(spec['say2'])[:40]}.mp3", "text": spec['say2']}]
    G = {"voice": "Aoede", "style": spec.get('style', STYLE), "wrapper": spec.get('wrapper', WRAPPER), "tempo": spec.get('tempo', 1.07)}
    json.dump({"gemini": G, "lines": lines}, open(f'{W}/voice.json', 'w'))
    run(['python3', 'templates/voice/gemini_tts.py', V, f'{W}/voice.json'])
    for l in lines: print('  voice:', l['text'], '| heard:', heard(f"{V}/{l['file']}"))
    after = spec.get('after', [])                      # extra spoken lines after "Tell us in the comments!" (e.g. "Come on Conny!")
    if after:
        json.dump({"gemini": G, "lines": after}, open(f'{W}/voice2.json', 'w')); run(['python3', 'templates/voice/gemini_tts.py', V, f'{W}/voice2.json'])
        for l in after: print('  voice:', l['text'], '| heard:', heard(f"{V}/{l['file']}"))
    out = run(['python3', 'templates/voice/mix.py', V, f'{W}/audio.m4a', spec['music'], 'zp_santa_a.mp3', *[l['file'] for l in lines], *spec.get('closers', ['zp_cheer.mp3', 'zp_ask_2.mp3'])] + [l['file'] for l in after]).split()
    p2, total = float(out[-2]), float(out[-1])
    for f in glob.glob(f'{V}/_t*.wav'): os.remove(f)
    # 4. the video and slides
    run(['python3', 'templates/video.py', W, scene, K, str(cx), str(cy), SC['mode'], O, f'{W}/audio.m4a'], {**env, "ZANS_P1": str(max(4.0, round(min(p2-5.6, p2*0.4), 2))), "ZANS_P2": str(p2), "ZANS_TOTAL": str(total)})
    sheet = Image.new('RGB', (1080*4, 1920))
    for i, n in enumerate(('000', '060', '165', '250')): sheet.paste(Image.open(f'{O}/{K}-frame-{n}.jpg'), (i*1080, 0))
    sheet.thumbnail((1900, 900)); sheet.save(f'{W}/check.png')
    for f in glob.glob(f'{O}/{K}-frame-*.jpg'): os.remove(f)
    v = spec.get('version', 1); os.replace(f'{O}/{K}-video.mp4', f'{O}/{K}-video-v{v}.mp4')
    ph = Image.new('RGB', (1200, 500), 'white')
    for i in (1, 2, 3): ph.paste(Image.open(f'{O}/{K}-slide{i}.png').resize((400, 500)), ((i-1)*400, 0))
    ph.save(f'{O}/phone/{K}-phone-3-slides.jpg', quality=88); Image.open(scene).resize((400, 711)).save(f'{O}/phone/{K}-phone-tall-scene.jpg', quality=88)
    # 5. captions (from the approved head-to-head wording)
    mug = P == 'mug'; thing, things = ('mug', 'mugs') if mug else ('Christmas bauble', 'Christmas baubles')
    designer = 'mug-designer' if mug else 'bauble-designer'; etsy = '4608193933' if mug else '4611232428'; tag = '#personalisedmug' if mug else '#personalisedbauble'
    pick = "the pattern, the colours, the handle and the name" if mug else "the pattern, the colours and the name"
    a, b, q = A['name'], B['name'], spec.get('q', "Which one are you cheering?") + " 👇"; hook = spec.get('hook', f"{A['name']} or {B['name']}? 🏇"); hook_t = spec.get('hook_tiktok', hook); web = "Visit www.zanshorseracing.co.uk for horse racing gifts, the perfect present for Christmas 🎄"; xmas = "Wishing you a Merry Christmas 🎅"
    spec_txt = "with a coloured handle and inside. 330 ml ceramic." if mug else "Round ceramic, about 7.5 cm, with a ribbon."
    cap = f"""# Head to head {things}: {a} v {b}. Social showcase only: sells "design your own", never these two {things}. Facts and silks: see the review request and research files. Not booked.
Alt text: {spec['alt']}

## Instagram
{hook} Two personalised horse racing {things}, each in famous colours.

{spec['story']} Design a {thing.split()[-1]} in any colours, with any name, at www.zanshorseracing.co.uk. These two are showcases, not ready-made {things.split()[-1]}. You pick {pick}. We print yours.

Send this to the mate who'll be cheering the other one.

{q}

Search ZANSRacingTools on Etsy.

{web}

{xmas}

#horseracinggifts {tag} #racingsilks #horseracing #christmasgifts

Link in bio 👉 www.zanshorseracing.co.uk

## Facebook
{hook} Two personalised horse racing {things}, each in famous colours.

{spec['story']} Design a {thing.split()[-1]} in any colours, with any name, on our website. These two are showcases, not ready-made {things.split()[-1]}. You pick {pick}. We print yours.

{q}

{xmas}

#horseracinggifts {tag} #horseracing

First comment: Design yours: https://www.zanshorseracing.co.uk/{designer}/

## X
{spec.get('x', f'{a} or {b}? 🏇 Two {things} in famous racing colours. Which one are you cheering?')} #HorseRacing #HorseRacingGifts

Reply: Design yours in any colours, with any name: https://www.zanshorseracing.co.uk/{designer}/ {xmas}

## LinkedIn
{hook} Two personalised horse racing {things}, each in famous colours.

{spec['story']} A {thing.split()[-1]} in the syndicate's own colours, with each member's name, makes an easy Christmas gift for owners and clients. Design one at www.zanshorseracing.co.uk.

{q}

{xmas}

#horseracinggifts {tag} #horseracing

## YouTube
Title: {spec.get('yt_title', f"Horse Racing {'Mugs' if mug else 'Christmas Baubles'}: {a} or {b}? 🎄")}
{hook} Two personalised horse racing {things} in famous colours. Design yours in any colours, with any name, at www.zanshorseracing.co.uk. Search ZANSRacingTools on Etsy.

{q}

{xmas}

#Shorts #HorseRacing #ChristmasGifts

## Pinterest
Title: Personalised Horse Racing {'Mug' if mug else 'Christmas Bauble'} - Racing Silks in Any Colours, Any Name
A personalised horse racing {thing} in racing silks, with any name. These showcase designs carry {a} and {b}; yours can carry any name, in any of 25 silks patterns and any colours, {spec_txt} A Christmas gift for racing fans, owners and syndicates. Wishing you a Merry Christmas 🎅
Link: https://www.etsy.com/uk/listing/{etsy}

## TikTok
Title: {spec.get('tt_title', f"{a} or {b}? {'Mugs' if mug else 'Baubles'} in their colours 🎄")}
{hook_t} Two personalised horse racing {things}, each in famous colours.

{spec['story_tiktok']} Design a {thing.split()[-1]} in any colours, with any name. You pick {pick}.

{q}

{xmas}

#horseracinggifts {tag} #racingsilks #horseracing #christmasgifts

Link in bio 👉 www.zanshorseracing.co.uk
"""
    open(f'{O}/CAPTIONS-{K}.md', 'w').write(cap)
    tt = cap.split('## TikTok')[1].lower(); bad = [w for w in ['odds', 'stalls', 'draw', 'going', 'winner', 'winning', ' win', 'bet', 'price', 'guide', '£', '18+'] if w in tt]
    yt = re.search(r'Title: (.*)', cap.split('## YouTube')[1]).group(1); ttt = re.search(r'Title: (.*)', cap.split('## TikTok')[1]).group(1)
    print(f"DONE {K}: video v{v}, total {total}s, check sheet {W}/check.png | TikTok flags {bad} | titles yt {len(yt)} tiktok {len(ttt)}")
if __name__ == '__main__':
    main(json.load(open(sys.argv[1])))
