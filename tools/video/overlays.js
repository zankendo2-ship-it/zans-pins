// One understated headline, brand cream, nothing else on the picture.
const { chromium } = require('playwright'); const fs = require('fs');
const S = __dirname, F = S + '/build/node_modules/@fontsource';
const b64 = f => fs.readFileSync(f).toString('base64');
const font = (file, w) => `@font-face{font-family:Jost;font-weight:${w};src:url(data:font/woff2;base64,${b64(F + '/jost/files/' + file)}) format("woff2")}`;
const css = `${font('jost-latin-500-normal.woff2',500)}${font('jost-latin-600-normal.woff2',600)}
*{margin:0;padding:0;box-sizing:border-box}body{background:transparent;font-family:Jost,sans-serif;overflow:hidden}
.shade{position:absolute;left:0;right:0;top:0}
.h{position:absolute;left:80px;right:80px;text-align:center;font-weight:500;line-height:1.14;letter-spacing:.005em;color:#EAE2D8;text-shadow:0 1px 14px #0009}
.h span{display:block}`;
const P = JSON.parse(fs.readFileSync(S + '/vcopy.json', 'utf8'));
(async () => {
  const b = await chromium.launch();
  const shot = async (name, w, h, html) => { const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.setContent(`<!doctype html><meta charset=utf8><style>${css}</style>${html}`); await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: `v/${name}.png`, omitBackground: true }); await p.close(); };
  for (const [k, D] of Object.entries(P)) {
    const lines = `<span>${D.l1}</span><span>${D.l2}</span>`;
    await shot(`${k}-v-head`, 1080, 1920, `<div class="shade" style="height:700px;background:linear-gradient(#05080699,#05080666 60%,#05080600)"></div>
      <div class="h" style="top:356px;font-size:${D.vsize}px">${lines}</div>`);   // inside the TikTok safe zone
    await shot(`${k}-f`, 1080, 1350, `<div class="shade" style="height:420px;background:linear-gradient(#050806a6,#05080666 60%,#05080600)"></div>
      <div class="h" style="top:70px;font-size:${D.fsize}px">${lines}</div>`);
  }
  await b.close();
})();
