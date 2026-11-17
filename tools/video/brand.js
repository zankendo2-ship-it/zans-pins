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
.pill{border:3px solid #E6C766;border-radius:8px;background:#141414;color:#F2CF5B;font-family:Plex,monospace;font-weight:700;letter-spacing:.2em;box-shadow:0 0 0 1px #6B5300 inset}
.stripe{position:absolute;left:0;right:0;height:12px;background:linear-gradient(90deg,#725415 0%,#B98A36 22%,#FFF4C9 50%,#B98A36 78%,#725415 100%)}
.block{position:absolute;left:0;right:0;color:#fff}
.eyebrow{font-weight:600;letter-spacing:.24em;text-transform:uppercase;opacity:.95}
.big{font-weight:700;text-transform:uppercase;line-height:.98;letter-spacing:.005em}
.sub{font-weight:600;line-height:1.15}
.cream{position:absolute;left:0;right:0;background:#EAE2D8}
.logo{display:block;border-radius:22px}
.ink{color:#1C1C1C}.muted{color:#5E574F}
.flake{position:absolute}`;
const P = {
  ombudsman: { colour: '#1C4FA0', eyebrow: "Social showcase · any horse's name", big: 'Ombudsman retiring?', sub: 'Put him on your tree this Christmas.' },
  lossiemouth: { colour: '#C2477E', eyebrow: "Social showcase · any horse's name", big: 'Lossiemouth fans,', sub: 'would this go on your tree?' },
};
const bar = `<div class="bar"><b>ZANS · HORSE RACING GIFTS</b><span class="pill" style="font-size:19px;padding:5px 16px">CHRISTMAS 2026</span></div><div class="stripe" style="top:60px"></div>`;
(async () => {
  const b = await chromium.launch();
  const shot = async (name, w, h, html, transparent) => { const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.setContent(`<!doctype html><meta charset=utf8><style>${css}</style>${html}`); await p.evaluate(() => document.fonts.ready);
    const fit = await p.evaluate(() => [...document.querySelectorAll('.big')].map(e => { let s = parseFloat(getComputedStyle(e).fontSize);
      while (e.scrollWidth > e.clientWidth + 1 && s > 40) { s -= 2; e.style.fontSize = s + 'px'; } return s; }));
    await p.screenshot({ path: `v/${name}.png`, omitBackground: transparent }); await p.close(); return fit; };
  for (const [k, D] of Object.entries(P)) {
    // 4:5 feed photo, laid out like the guide cover
    const photo = img(`v/${k}-window.png`);
    console.log(k, 'feed', await shot(`${k}-feed-branded`, 1080, 1350, `${bar}
      <div class="block" style="top:72px;height:200px;background:${D.colour};padding:26px 48px 0">
        <div class="eyebrow" style="font-size:19px">${D.eyebrow}</div>
        <div class="big" style="font-size:82px;margin-top:10px;white-space:nowrap;overflow:hidden">${D.big}</div>
        <div class="sub" style="font-size:34px;margin-top:6px">${D.sub}</div></div>
      <img src="${photo}" style="position:absolute;left:0;top:272px;width:1080px;height:722px;object-fit:cover">
      <div class="stripe" style="top:994px"></div>
      <div class="cream" style="top:1006px;height:344px;display:flex;align-items:center;gap:36px;padding:0 48px">
        <img class="logo" src="${santa}" style="height:280px">
        <div><div class="big ink" style="font-size:62px;line-height:1.02">Wishing you a<br>Merry Christmas</div>
          <div class="muted" style="font-family:Src,sans-serif;font-size:27px;margin-top:14px">Any horse's name · zanshorseracing.co.uk</div></div></div>`, false));
    // video header (0-6s): the bar, stripe and colour block slide in over the photo; text kept below y 340 (TikTok top UI)
    console.log(k, 'vhead', await shot(`${k}-vhead`, 1080, 1920, `${bar}
      <div class="block" style="top:72px;height:560px;background:${D.colour};padding:0 56px">
        <div class="eyebrow" style="position:absolute;left:56px;top:300px;font-size:24px">${D.eyebrow}</div>
        <div class="big" style="position:absolute;left:56px;right:56px;top:350px;font-size:100px;white-space:nowrap;overflow:hidden">${D.big}</div>
        <div class="sub" style="position:absolute;left:56px;right:56px;top:468px;font-size:52px">${D.sub}</div></div>
      <div class="stripe" style="top:632px"></div>`, true));
    // end-card (6-8.5s): the post's colour, big Santa-hat logo, Merry Christmas, BUY NOW, website at y 1350
    await shot(`${k}-endcard`, 1080, 1920, `<div style="position:absolute;inset:0;background:radial-gradient(120% 70% at 50% 42%, ${D.colour}EE, ${D.colour})"></div>${bar}
      <div class="eyebrow" style="position:absolute;left:0;right:0;top:350px;text-align:center;color:#fff;font-size:26px">ZANS Racing · Tools &amp; Gifts</div>
      <img class="logo" src="${santa}" style="position:absolute;left:190px;top:410px;width:700px;box-shadow:0 22px 60px #0006">
      <div class="big" style="position:absolute;left:0;right:0;top:1000px;text-align:center;color:#fff;font-size:94px;line-height:1.0">Wishing you a<br>Merry Christmas</div>
      <div style="position:absolute;left:0;right:0;top:1222px;text-align:center"><span class="pill" style="display:inline-block;font-size:40px;padding:14px 46px;border-radius:14px">BUY NOW</span></div>
      <div style="position:absolute;left:0;right:0;top:1350px;text-align:center;color:#fff;font-weight:600;font-size:36px;letter-spacing:.12em">WWW.ZANSHORSERACING.CO.UK</div>
      <div class="stripe" style="top:1848px"></div><div style="position:absolute;left:0;right:0;top:1860px;height:60px;background:#1C1C1C"></div>`, false);
  }
  await b.close();
})();
