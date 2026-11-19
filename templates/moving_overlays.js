// Text overlays for the moving-cuts format (tester, 19 Nov 2026): transparent 1080x1920 PNGs in the brand font.
// node templates/moving_overlays.js <out_dir> '<json: {eyebrow, hook: [line, line], a: {name, bg, fg}, b: {name, bg, fg}, question}>'
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const o = JSON.parse(process.argv[3]); const T = __dirname;
const f = n => 'data:font/woff2;base64,' + fs.readFileSync(path.join(T, 'fonts', n)).toString('base64');
const css = `@font-face{font-family:J;font-weight:700;src:url(${f('jost-700.woff2')})}@font-face{font-family:J;font-weight:600;src:url(${f('jost-600.woff2')})}
*{margin:0;box-sizing:border-box}body{width:1080px;height:1920px;background:transparent;font-family:J;color:#fff;text-align:center}
.band{position:absolute;left:0;right:0;top:300px;padding:44px 60px 54px;background:linear-gradient(180deg,rgba(0,0,0,0) 0%,rgba(8,20,14,.62) 22%,rgba(8,20,14,.62) 78%,rgba(0,0,0,0) 100%)}
.eb{font-weight:600;font-size:30px;letter-spacing:6px;text-transform:uppercase;color:#F2CF5B;margin-bottom:14px}
.big{font-weight:700;font-size:86px;line-height:1.04;text-transform:uppercase;text-shadow:0 4px 18px rgba(0,0,0,.65)}
.q{position:absolute;left:0;right:0;top:1270px;padding:40px 50px 50px;background:linear-gradient(180deg,rgba(0,0,0,0) 0%,rgba(8,20,14,.66) 18%,rgba(8,20,14,.66) 82%,rgba(0,0,0,0) 100%)}
.row{display:flex;gap:22px;justify-content:center;align-items:center;margin-bottom:26px}
.pill{font-weight:700;font-size:40px;text-transform:uppercase;padding:16px 26px;border-radius:14px;border:3px solid rgba(255,255,255,.9);letter-spacing:1px}
.or{font-weight:600;font-size:36px;color:#F2CF5B}
.ask{font-weight:700;font-size:62px;line-height:1.08;text-shadow:0 4px 18px rgba(0,0,0,.65)}`;
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  const shot = async (name, html) => { await p.setContent(`<style>${css}</style>${html}`); await p.evaluate(() => document.fonts.ready); await p.screenshot({ path: path.join(process.argv[2], name), omitBackground: true }); };
  await shot('ov-hook.png', `<div class="band"><div class="eb">${o.eyebrow}</div><div class="big">${o.hook.join('<br>')}</div></div>`);
  await shot('ov-question.png', `<div class="q"><div class="row"><div class="pill" style="background:${o.a.bg};color:${o.a.fg}">${o.a.name}</div><div class="or">or</div><div class="pill" style="background:${o.b.bg};color:${o.b.fg}">${o.b.name}</div></div><div class="ask">${o.question}</div></div>`);
  await b.close(); })();
