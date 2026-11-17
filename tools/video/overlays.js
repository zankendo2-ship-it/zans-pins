const { chromium } = require('playwright'); const fs = require('fs');
const S = __dirname, F = S + '/build/node_modules/@fontsource';
const b64 = f => fs.readFileSync(f).toString('base64');
const font = (file, w) => `@font-face{font-family:Jost;font-weight:${w};src:url(data:font/woff2;base64,${b64(F + '/jost/files/' + file)}) format("woff2")}`;
const css = `${font('jost-latin-700-normal.woff2',700)}${font('jost-latin-600-normal.woff2',600)}${font('jost-latin-500-normal.woff2',500)}
*{margin:0;padding:0;box-sizing:border-box}body{background:transparent;font-family:Jost,'Noto Color Emoji',sans-serif;color:#EAE2D8;overflow:hidden}
.h{position:absolute;left:40px;right:40px;white-space:nowrap;text-align:center;font-weight:700;line-height:1.02;letter-spacing:-.005em;text-shadow:0 4px 0 #000a,0 0 34px #000,0 0 70px #000c}
.h b{display:block;color:#EAE2D8}.h i{display:block;font-style:normal;color:#F2CF5B}
.pill{position:absolute;text-align:center;border:4px solid #F2CF5B;background:#0d2619e6;color:#F2CF5B;font-weight:600;letter-spacing:.08em;text-transform:uppercase}
.q{position:absolute;text-align:center;font-weight:500;text-shadow:0 0 22px #000,0 0 44px #000}
.end{position:absolute;display:flex;align-items:center;gap:26px;background:#0d2619f2;border-top:3px solid #F2CF5B;border-bottom:3px solid #F2CF5B}
.end img{border-radius:12px}.end em{display:block;font-style:normal;color:#F2CF5B;font-weight:500}.end strong{display:block;font-weight:600}`;
const logo = `data:image/png;base64,${b64(S + '/assets/zans-logo-santa.png')}`;
const P = JSON.parse(fs.readFileSync(S + '/vcopy.json', 'utf8'));
(async () => {
  const b = await chromium.launch();
  const shot = async (name, w, h, html) => { const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.setContent(`<!doctype html><meta charset=utf8><style>${css}</style>${html}`); await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: `v/${name}.png`, omitBackground: true }); await p.close(); };
  for (const [k, D] of Object.entries(P)) {
    // video layers, 1080x1920, all inside the TikTok safe zone (y 340-1600; nothing right of x 950 below y 1240)
    await shot(`${k}-v-head`, 1080, 1920, `<div class="h" style="top:352px;font-size:${D.vsize}px"><b>${D.l1}</b><i>${D.l2}</i></div>`);
    await shot(`${k}-v-cta`, 1080, 1920, `<div class="pill" style="left:90px;width:840px;top:1262px;font-size:33px;padding:16px 8px">${D.cta}</div>
      <div class="q" style="left:90px;width:840px;top:1362px;font-size:38px">${D.q}</div>`);
    await shot(`${k}-v-end`, 1080, 1920, `<div class="end" style="left:90px;width:840px;top:1452px;padding:16px 24px"><img src="${logo}" height="96">
      <div><em style="font-size:30px">Wishing you a Merry Christmas</em><strong style="font-size:33px">www.zanshorseracing.co.uk</strong></div></div>`);
    // feed photo layer, 1080x1350
    await shot(`${k}-f`, 1080, 1350, `<div class="h" style="top:54px;font-size:${D.fsize}px"><b>${D.l1}</b><i>${D.l2}</i></div>
      <div class="pill" style="left:70px;width:940px;top:1020px;font-size:33px;padding:15px 8px">${D.cta}</div>
      <div class="q" style="left:70px;width:940px;top:1112px;font-size:38px">${D.q}</div>
      <div class="end" style="left:70px;width:940px;top:1196px;padding:14px 24px"><img src="${logo}" height="92">
      <div><em style="font-size:30px">Wishing you a Merry Christmas</em><strong style="font-size:33px">www.zanshorseracing.co.uk</strong></div></div>`);
  }
  await b.close();
})();
