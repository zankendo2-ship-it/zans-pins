// Part 1: big two-colour hook, nothing else over the bauble. Part 2: the branded snow end-card.
const { chromium } = require('playwright'); const fs = require('fs');
const S = __dirname, F = S + '/build/node_modules/@fontsource';
const b64 = f => fs.readFileSync(f).toString('base64');
const font = (file, w) => `@font-face{font-family:Jost;font-weight:${w};src:url(data:font/woff2;base64,${b64(F + '/jost/files/' + file)}) format("woff2")}`;
const santa = `data:image/png;base64,${b64(S + '/assets/zans-logo-santa.png')}`;
const GOLD = 'linear-gradient(90deg,#8A6A2A 0%,#D9B45A 14%,#F7E7A8 30%,#F2CF5B 46%,#B98A36 62%,#F4DE97 80%,#8A6A2A 100%)';
const css = `${font('jost-latin-500-normal.woff2',500)}${font('jost-latin-600-normal.woff2',600)}${font('jost-latin-700-normal.woff2',700)}
*{margin:0;padding:0;box-sizing:border-box}body{background:transparent;font-family:Jost,sans-serif;overflow:hidden}
.shade{position:absolute;left:0;right:0;top:0}
.hook{position:absolute;left:36px;right:36px;text-align:center;font-weight:700;line-height:1.04;text-transform:uppercase;letter-spacing:.01em;text-shadow:0 3px 18px #000b,0 1px 2px #0008;white-space:nowrap}
.c{color:#EAE2D8}.g{color:#F2CF5B}
.card{position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 38%,#27704C 0%,#1F5A3D 45%,#163F2B 100%)}
.stripe{position:absolute;left:0;right:0;height:12px;background:${GOLD};box-shadow:0 0 18px rgba(242,207,91,.35)}
.ctr{position:absolute;left:0;right:0;text-align:center}
.hdr{font-weight:600;letter-spacing:.34em;text-transform:uppercase;background:${GOLD};-webkit-background-clip:text;color:transparent}
.sub{color:#EAE2D8;font-weight:500;letter-spacing:.42em;text-transform:uppercase}
.logo{position:absolute;background:#EAE2D8;border:6px solid #E3C266;border-radius:20px;box-shadow:0 0 0 1px #8A6A2A,0 14px 40px #0006;display:grid;place-items:center}
.wish{color:#EAE2D8;font-weight:700;line-height:1.06}
.any{color:#F2CF5B;font-weight:500;letter-spacing:.06em}
.btn{position:absolute;border-radius:999px;background:linear-gradient(180deg,#F8E08A,#F2CF5B 45%,#D2A93C);color:#1F5A3D;font-weight:700;letter-spacing:.14em;text-align:center;box-shadow:0 8px 24px #0005,inset 0 2px 0 #fff8}
.url{color:#EAE2D8;font-weight:600;letter-spacing:.12em}`;
const P = JSON.parse(fs.readFileSync(S + '/vcopy.json', 'utf8'));
// k = scale: 1 for the 1080x1920 video card, smaller offsets for the 4:5 slide
const endcard = (H, y) => `<div class="card"></div>
  <div class="stripe" style="top:${y.s1}px"></div><div class="stripe" style="top:${y.s2}px"></div>
  <div class="ctr hdr" style="top:${y.hdr}px;font-size:54px">ZANS Racing</div>
  <div class="ctr sub" style="top:${y.hdr + 76}px;font-size:26px">Tools &amp; Gifts</div>
  <div class="logo" style="left:270px;width:540px;top:${y.logo}px;height:${y.logoH}px"><img src="${santa}" height="${y.logoH - 44}"></div>
  <div class="ctr wish" style="top:${y.wish}px;font-size:86px">Wishing you a<br>Merry Christmas</div>
  <div class="ctr any" style="top:${y.wish + 208}px;font-size:36px">Any horse's name · Custom keepsake</div>
  <div class="btn" style="left:340px;width:400px;top:${y.btn}px;font-size:40px;padding:17px 0">BUY NOW</div>
  <div class="ctr url" style="top:${y.btn + 104}px;font-size:32px">WWW.ZANSHORSERACING.CO.UK</div>`;
(async () => {
  const b = await chromium.launch();
  const shot = async (name, w, h, html, opaque) => { const p = await b.newPage({ viewport: { width: w, height: h } });
    await p.setContent(`<!doctype html><meta charset=utf8><style>${css}</style>${html}`); await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: `v/${name}.png`, omitBackground: !opaque }); await p.close(); };
  for (const [k, D] of Object.entries(P)) {
    await shot(`${k}-h1`, 1080, 1920, `<div class="hook c" style="top:${D.vy}px;font-size:${D.v1}px">${D.l1}</div>`);
    await shot(`${k}-h2`, 1080, 1920, `<div class="hook g" style="top:${D.vy + D.v1 * 1.1}px;font-size:${D.v2}px;line-height:1.08;white-space:normal">${D.l2}</div>`);
    await shot(`${k}-vshade`, 1080, 1920, `<div class="shade" style="height:820px;background:linear-gradient(#050806b3,#05080680 60%,#05080600)"></div>`);
    await shot(`${k}-f`, 1080, 1350, `<div class="shade" style="height:520px;background:linear-gradient(#050806b3,#05080680 60%,#05080600)"></div>
      <div class="hook c" style="top:56px;font-size:${D.f1}px">${D.l1}</div><div class="hook g" style="top:${56 + D.f1 * 1.1}px;font-size:${D.f2}px;line-height:1.08;white-space:normal">${D.l2}</div>`);
  }
  // everything on the end-card sits in the upper and middle 70% (above y 1344), clear of the TikTok and Reels caption bar
  await shot('endcard', 1080, 1920, endcard(1920, { s1: 300, s2: 1372, hdr: 344, logo: 484, logoH: 400, wish: 912, btn: 1186 }), true);
  await shot('endcard-45', 1080, 1350, endcard(1350, { s1: 22, s2: 1316, hdr: 62, logo: 206, logoH: 380, wish: 612, btn: 1010 }), true);
  await b.close();
})();
