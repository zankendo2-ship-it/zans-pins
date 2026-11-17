// Section 3.7 spec: hook 95-110px bold uppercase spanning 85-90% of the width, cream with gold key words, shadow 4px offset 12px blur.
const { chromium } = require('playwright'); const fs = require('fs');
const S = __dirname, F = S + '/build/node_modules/@fontsource';
const b64 = f => fs.readFileSync(f).toString('base64');
const font = (fam, file, w) => `@font-face{font-family:${fam};font-weight:${w};src:url(data:font/woff2;base64,${b64(F + '/' + file)}) format("woff2")}`;
const santa = `data:image/png;base64,${b64(S + '/assets/zans-logo-santa.png')}`;
const GOLD = 'linear-gradient(90deg,#8A6A2A 0%,#D9B45A 14%,#F7E7A8 30%,#F2CF5B 46%,#B98A36 62%,#F4DE97 80%,#8A6A2A 100%)';
const css = `${font('Anton','anton/files/anton-latin-400-normal.woff2',400)}${font('Jost','jost/files/jost-latin-600-normal.woff2',600)}${font('Jost','jost/files/jost-latin-700-normal.woff2',700)}
*{margin:0;padding:0;box-sizing:border-box}body{background:transparent;font-family:Jost,sans-serif;overflow:hidden}
.hook{position:absolute;left:0;right:0;text-align:center;font-family:Anton,Impact,sans-serif;text-transform:uppercase;line-height:1.12;letter-spacing:.012em;white-space:nowrap;
  text-shadow:0 4px 12px rgba(0,0,0,.95),0 0 3px rgba(0,0,0,.9),0 0 34px rgba(0,0,0,.55)}
.hook span{display:block}.c{color:#EAE2D8}.g{color:#F2CF5B}
.card{position:absolute;inset:0;background:radial-gradient(130% 70% at 50% 40%,#2A7A52 0%,#1F5A3D 48%,#17462F 100%)}
.stripe{position:absolute;left:0;right:0;height:16px;background:${GOLD};box-shadow:0 0 22px rgba(242,207,91,.45)}
.hair{position:absolute;left:0;right:0;height:5px;background:${GOLD}}
.ctr{position:absolute;left:0;right:0;text-align:center}
.hdr{font-weight:700;letter-spacing:.3em;text-transform:uppercase;background:${GOLD};-webkit-background-clip:text;color:transparent}
.sub{color:#EAE2D8;font-weight:600;letter-spacing:.44em;text-transform:uppercase}
.band{position:absolute;left:0;right:0;background:#EFE8DE;display:grid;place-items:center;box-shadow:0 18px 50px #0005}
.wish{color:#EAE2D8;font-weight:700;line-height:1.05;text-shadow:0 4px 14px #0007}
.btn{position:absolute;border-radius:999px;background:linear-gradient(180deg,#FBE7A0,#F2CF5B 45%,#CFA43A);color:#1F5A3D;font-weight:700;letter-spacing:.16em;text-align:center;box-shadow:0 10px 26px #0006,inset 0 3px 0 #fff9}
.url{color:#F2CF5B;font-weight:700;letter-spacing:.1em}`;
const P = JSON.parse(fs.readFileSync(S + '/vcopy.json', 'utf8'));
const endcard = y => `<div class="card"></div><div class="stripe" style="top:0"></div><div class="stripe" style="bottom:0"></div>
  <div class="ctr hdr" style="top:${y.hdr}px;font-size:64px">ZANS Racing</div><div class="ctr sub" style="top:${y.hdr + 88}px;font-size:30px">Tools &amp; Gifts</div>
  <div class="hair" style="top:${y.band - 5}px"></div><div class="band" style="top:${y.band}px;height:${y.bandH}px"><img src="${santa}" height="${y.bandH - 50}"></div><div class="hair" style="top:${y.band + y.bandH}px"></div>
  <div class="ctr wish" style="top:${y.wish}px;font-size:${y.wishSize}px">Wishing you a<br>Merry Christmas</div>
  <div class="btn" style="left:310px;width:460px;top:${y.btn}px;font-size:46px;padding:14px 0">BUY NOW</div>
  <div class="ctr url" style="top:${y.url}px;font-size:36px">WWW.ZANSHORSERACING.CO.UK</div>`;
(async () => {
  const b = await chromium.launch(); const report = {};
  const page = async (w, h, html) => { const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.setContent(`<!doctype html><meta charset=utf8><style>${css}</style>${html}`); await p.evaluate(() => document.fonts.ready); return p; };
  for (const [k, D] of Object.entries(P)) {
    for (const [tag, w, h, top] of [['hook', 1080, 1920, 352], ['f', 1080, 1350, 54]]) {
      const p = await page(w, h, `<div class="hook" style="top:${top}px">${D.lines.map(l => `<span class="${l.c}">${l.t}</span>`).join('')}</div>`);
      // fit every line to 88% of the width, inside the 95-110px rule
      report[k + '-' + tag] = await p.evaluate(() => [...document.querySelectorAll('.hook span')].map(s => {
        s.style.display = 'inline-block'; s.style.fontSize = '100px'; const w100 = s.getBoundingClientRect().width;
        const size = Math.max(95, Math.min(110, Math.floor(100 * 950 / w100))); s.style.fontSize = size + 'px';
        let wd = s.getBoundingClientRect().width;
        if (s === s.parentNode.firstElementChild && wd < 918) { s.style.letterSpacing = ((950 - wd) / s.textContent.length / size + 0.012).toFixed(3) + 'em'; wd = s.getBoundingClientRect().width; }
        s.style.display = 'block'; return { text: s.textContent, px: size, widthPct: Math.round(wd / 10.8) }; }));
      await p.screenshot({ path: `v/${k}-${tag}.png`, omitBackground: true }); await p.close();
    }
  }
  const e = await page(1080, 1920, endcard({ hdr: 372, band: 540, bandH: 400, wish: 990, wishSize: 106, btn: 1238, url: 1350 }));
  await e.screenshot({ path: 'v/endcard.png' }); await e.close();
  const e2 = await page(1080, 1350, endcard({ hdr: 60, band: 226, bandH: 380, wish: 660, wishSize: 100, btn: 912, url: 1030 }));
  await e2.screenshot({ path: 'v/endcard-45.png' }); await e2.close();
  console.log(JSON.stringify(report, null, 1)); await b.close();
})();
