// ZANS brand frame, taken from the Track DNA guides: #1C1C1C top bar, bronze-champagne-bronze metallic stripe,
// a solid colour block (here the post's own silks colour) with big white Jost Bold capitals, cream panel, big Santa-hat logo.
const { chromium } = require('playwright'); const fs = require('fs');
const S = __dirname, F = S + '/build/node_modules/@fontsource';
const b64 = f => fs.readFileSync(f).toString('base64');
const font = (fam, file, w) => `@font-face{font-family:'${fam}';font-weight:${w};src:url(data:font/woff2;base64,${b64(F + '/' + file)}) format("woff2")}`;
const img = (f, t = 'png') => `data:image/${t};base64,${b64(S + '/' + f)}`;
const santa = img('assets/santa-2x.png');
const css = `${font('Jost','jost/files/jost-latin-500-normal.woff2',500)}${font('Jost','jost/files/jost-latin-600-normal.woff2',600)}${font('Jost','jost/files/jost-latin-700-normal.woff2',700)}
${font('Plex','ibm-plex-mono/files/ibm-plex-mono-latin-700-normal.woff2',700)}${font('Src','source-sans-3/files/source-sans-3-latin-400-normal.woff2',400)}
*{margin:0;padding:0;box-sizing:border-box}body{background:transparent;font-family:Jost,sans-serif;overflow:hidden}
.bar{position:absolute;left:0;right:0;top:0;height:60px;background:#1C1C1C;display:flex;align-items:center;justify-content:space-between;padding:0 44px}
.bar b{color:#F3EDE5;font-weight:600;font-size:21px;letter-spacing:.26em}
.pill{border:3px solid var(--edge);border-radius:8px;background:#141414;color:var(--text);font-family:Plex,monospace;font-weight:700;letter-spacing:.2em;box-shadow:0 0 0 1px var(--inset) inset}
.stripe{position:absolute;left:0;right:0;height:12px;background:var(--stripe)}
.block{position:absolute;left:0;right:0;color:#fff}
.eyebrow{font-weight:600;letter-spacing:.24em;text-transform:uppercase;opacity:.95}
.big{font-weight:700;text-transform:uppercase;line-height:.98;letter-spacing:.005em}
.sub{font-weight:600;line-height:1.15}
.cream{position:absolute;left:0;right:0;background:#EAE2D8}
.logo{display:block;border-radius:22px}
.ink{color:#1C1C1C}.muted{color:#5E574F}
.flake{position:absolute}`;
const METAL = {
  gold:   { stripe: 'linear-gradient(90deg,#725415 0%,#B98A36 22%,#FFF4C9 50%,#B98A36 78%,#725415 100%)', edge: '#E6C766', text: '#F2CF5B', inset: '#6B5300' },
  silver: { stripe: 'linear-gradient(90deg,#5E646B 0%,#A9AFB6 22%,#F7F9FB 50%,#A9AFB6 78%,#5E646B 100%)', edge: '#D3D8DD', text: '#E9EDF1', inset: '#5E646B' },
};
const P = {
  ombudsman: { metal: 'silver', colour: '#1C4FA0', eyebrow: "Social showcase · any horse's name", big: 'Ombudsman retiring?', sub: 'Put him on your tree this Christmas.', q: "Which horse's name would you put on yours?" },
  lossiemouth: { metal: 'gold', colour: '#C2477E', eyebrow: "Social showcase · any horse's name", big: 'Lossiemouth fans,', sub: 'green silks and pink spots.', q: 'Would this go on your tree?' },
};
const bar = `<div class="bar"><b>ZANS · HORSE RACING GIFTS</b><span class="pill" style="font-size:19px;padding:5px 16px">CHRISTMAS 2026</span></div><div class="stripe" style="top:60px"></div>`;
const foot = H => `<div class="stripe" style="top:${H - 72}px"></div><div style="position:absolute;left:0;right:0;top:${H - 60}px;height:60px;background:#1C1C1C"></div>`;
const bg = D => `<div style="position:absolute;inset:0;background:radial-gradient(120% 70% at 50% 42%, ${D.colour}E6, ${D.colour})"></div>`;
// clip 2: the hook and the question
const textCard = (D, H, y) => `${bg(D)}${bar}
  <div class="eyebrow" style="position:absolute;left:0;right:0;top:${y.eb}px;text-align:center;color:#fff;font-size:26px">${D.eyebrow}</div>
  <div class="big" style="position:absolute;left:60px;right:60px;top:${y.big}px;text-align:center;color:#fff;font-size:${y.bigS}px;line-height:1.0">${D.big}</div>
  <div class="sub" style="position:absolute;left:80px;right:80px;top:${y.sub}px;text-align:center;color:#fff;font-size:${y.subS}px">${D.sub}</div>
  <div style="position:absolute;left:0;right:0;top:${y.rule}px;text-align:center"><span class="stripe" style="position:static;display:inline-block;width:260px;height:6px"></span></div>
  <div style="position:absolute;left:90px;right:90px;top:${y.q}px;background:#EAE2D8;border-radius:22px;padding:34px 40px;text-align:center;box-shadow:0 18px 50px #0005">
    <div class="eyebrow muted" style="font-size:22px">Tell us in the comments</div>
    <div class="ink" style="font-weight:700;font-size:${y.qS}px;line-height:1.12;margin-top:12px">${D.q}</div></div>${foot(H)}`;
// clip 3: the Santa-hat end-card
const endCard = (D, H, y) => `${bg(D)}${bar}
  <div class="eyebrow" style="position:absolute;left:0;right:0;top:${y.eb}px;text-align:center;color:#fff;font-size:26px">ZANS Racing · Tools &amp; Gifts</div>
  <img class="logo" src="${santa}" style="position:absolute;left:${(1080 - y.logoW) / 2}px;top:${y.logo}px;width:${y.logoW}px;box-shadow:0 22px 60px #0006">
  <div class="big" style="position:absolute;left:0;right:0;top:${y.wish}px;text-align:center;color:#fff;font-size:${y.wishS}px;line-height:1.0">Wishing you a<br>Merry Christmas</div>
  <div style="position:absolute;left:0;right:0;top:${y.btn}px;text-align:center"><span class="pill" style="display:inline-block;font-size:40px;padding:14px 46px;border-radius:14px">BUY NOW</span></div>
  <div style="position:absolute;left:0;right:0;top:${y.url}px;text-align:center;color:#fff;font-weight:600;font-size:34px;letter-spacing:.12em">WWW.ZANSHORSERACING.CO.UK</div>${foot(H)}`;
const strips = H => `<div class="stripe" style="top:0"></div><div class="stripe" style="top:${H - 12}px"></div>`;
(async () => {
  const b = await chromium.launch();
  const shot = async (name, w, h, html, transparent, metal) => { const M = METAL[metal || 'gold']; const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.setContent(`<!doctype html><meta charset=utf8><style>:root{--stripe:${M.stripe};--edge:${M.edge};--text:${M.text};--inset:${M.inset}}${css}</style>${html}`); await p.evaluate(() => document.fonts.ready);
    const fit = await p.evaluate(() => [...document.querySelectorAll('.big')].map(e => { let s = parseFloat(getComputedStyle(e).fontSize);
      while (e.scrollWidth > e.clientWidth + 1 && s > 40) { s -= 2; e.style.fontSize = s + 'px'; } return s; }));
    await p.screenshot({ path: `v/${name}.png`, omitBackground: transparent }); await p.close(); return fit; };
  for (const [k, D] of Object.entries(P)) {
    // video (1080x1920): text kept between y 340 and 1440, clear of the TikTok and Reels interface
    await shot(`${k}-v-strips`, 1080, 1920, strips(1920), true, D.metal);
    console.log(k, 'text', await shot(`${k}-v-text`, 1080, 1920, textCard(D, 1920, { eb: 470, big: 520, bigS: 112, sub: 770, subS: 50, rule: 880, q: 930, qS: 60 }), false, D.metal));
    await shot(`${k}-endcard`, 1080, 1920, endCard(D, 1920, { eb: 350, logo: 410, logoW: 700, wish: 1000, wishS: 94, btn: 1222, url: 1350 }), false, D.metal);
    // feed carousel (1080x1350): slide 1 the photo with strips, slide 2 the hook and question, slide 3 the Santa-hat card
    await shot(`${k}-s1-strips`, 1080, 1350, strips(1350), true, D.metal);
    await shot(`${k}-s2`, 1080, 1350, textCard(D, 1350, { eb: 330, big: 380, bigS: 104, sub: 610, subS: 46, rule: 710, q: 760, qS: 56 }), false, D.metal);
    await shot(`${k}-s3`, 1080, 1350, endCard(D, 1350, { eb: 214, logo: 262, logoW: 560, wish: 752, wishS: 84, btn: 958, url: 1060 }), false, D.metal);
  }
  await b.close();
})();
