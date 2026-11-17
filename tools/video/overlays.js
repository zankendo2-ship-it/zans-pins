const { chromium } = require('playwright'); const fs = require('fs');
const S = __dirname, F = S + '/build/node_modules/@fontsource';
const b64 = f => fs.readFileSync(f).toString('base64');
const font = (file, w) => `@font-face{font-family:Jost;font-weight:${w};src:url(data:font/woff2;base64,${b64(F + '/jost/files/' + file)}) format("woff2")}`;
const css = `${font('jost-latin-700-normal.woff2',700)}${font('jost-latin-600-normal.woff2',600)}${font('jost-latin-500-normal.woff2',500)}
*{margin:0;padding:0;box-sizing:border-box}body{background:transparent;font-family:Jost,sans-serif;color:#EAE2D8;overflow:hidden}
.shade{position:absolute;left:0;right:0}
.eyebrow{position:absolute;left:0;right:0;text-align:center;font-weight:600;letter-spacing:.32em;text-transform:uppercase;color:#F2CF5B;text-shadow:0 0 18px #000}
.h{position:absolute;left:70px;right:70px;text-align:center;font-weight:600;line-height:1.08;letter-spacing:-.005em;text-shadow:0 2px 24px #000,0 0 60px #000a}
.h b{display:block;font-weight:600;color:#EAE2D8}.h i{display:block;font-style:normal;color:#F2CF5B}
.q{position:absolute;text-align:center;font-weight:500;color:#EAE2D8;text-shadow:0 0 22px #000,0 0 44px #000}
.rule{position:absolute;height:2px;background:#F2CF5B}
.sig{position:absolute;text-align:center;text-shadow:0 0 20px #000}
.sig em{display:block;font-style:normal;font-weight:500;color:#F2CF5B;letter-spacing:.04em}.sig strong{display:block;font-weight:600;color:#EAE2D8;letter-spacing:.03em}`;
const logo = `data:image/png;base64,${b64(S + '/assets/zans-logo-santa.png')}`;
const P = JSON.parse(fs.readFileSync(S + '/vcopy.json', 'utf8'));
(async () => {
  const b = await chromium.launch();
  const shot = async (name, w, h, html) => { const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.setContent(`<!doctype html><meta charset=utf8><style>${css}</style>${html}`); await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: `v/${name}.png`, omitBackground: true }); await p.close(); };
  for (const [k, D] of Object.entries(P)) {
    // video layers, 1080x1920, all inside the TikTok safe zone (y 340-1600; nothing right of x 950 below y 1240)
    await shot(`${k}-v-head`, 1080, 1920, `<div class="shade" style="top:0;height:760px;background:linear-gradient(#07120ccc,#07120c99 55%,#07120c00)"></div>
      <div class="eyebrow" style="top:352px;font-size:24px">ZANS Racing</div>
      <div class="h" style="top:398px;font-size:${D.vsize}px"><b>${D.l1}</b><i>${D.l2}</i></div>`);
    await shot(`${k}-v-cta`, 1080, 1920, `<div class="shade" style="bottom:0;height:820px;background:linear-gradient(#07120c00,#07120c85 45%,#07120cc4)"></div>
      <div class="q" style="left:80px;width:860px;top:1356px;font-size:36px;white-space:nowrap">${D.q}</div>`);
    await shot(`${k}-v-end`, 1080, 1920, `<div class="rule" style="left:390px;width:240px;top:1428px"></div>
      <div class="sig" style="left:110px;width:800px;top:1450px"><em style="font-size:30px">Wishing you a Merry Christmas</em><strong style="font-size:34px;margin-top:6px">www.zanshorseracing.co.uk</strong></div>`);
    // feed photo layer, 1080x1350
    await shot(`${k}-f`, 1080, 1350, `<div class="shade" style="top:0;height:420px;background:linear-gradient(#07120ce0,#07120c99 60%,#07120c00)"></div>
      <div class="shade" style="bottom:0;height:400px;background:linear-gradient(#07120c00,#07120cbf 45%,#07120cf0)"></div>
      <div class="eyebrow" style="top:52px;font-size:22px">ZANS Racing</div>
      <div class="h" style="top:92px;font-size:${D.fsize}px"><b>${D.l1}</b><i>${D.l2}</i></div>
      <div class="q" style="left:90px;width:900px;top:1112px;font-size:38px">${D.q}</div>
      <div class="rule" style="left:420px;width:240px;top:1182px"></div>
      <div class="sig" style="left:90px;width:900px;top:1204px"><em style="font-size:28px">Wishing you a Merry Christmas</em><strong style="font-size:32px;margin-top:4px">www.zanshorseracing.co.uk</strong></div>`);
  }
  await b.close();
})();
