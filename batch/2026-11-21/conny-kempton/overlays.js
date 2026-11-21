// Card overlays (transparent PNG, 1080x1920) for the Constitution Hill at Kempton video. All wording is typeset here, never drawn by the image model.
// node overlays.js   -> ov/<key>.png
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const R = path.join(__dirname, '..', '..', '..'), FD = path.join(R, 'templates', 'fonts'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (fam, file, w) => `@font-face{font-family:'${fam}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(FD, file))}) format("woff2")}`;
const LOGO = `data:image/png;base64,${b64(path.join(R, 'templates', 'assets', 'zans-logo.png'))}`;
const S = JSON.parse(fs.readFileSync(path.join(__dirname, 'scenes.json'), 'utf8')); const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const CSS = font('Jost', 'jost-600.woff2', 600) + font('Jost', 'jost-700.woff2', 700) + `
*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1920px;background:transparent;font-family:Jost;position:relative;overflow:hidden}
.strip{position:absolute;left:0;width:1080px;height:26px;background:linear-gradient(180deg,#0d8c80,#5fe6d6 35%,#19b3a4 55%,#0a6f66);box-shadow:0 0 0 2px #caa64a}
.strip.t{top:0}.strip.b{bottom:0}
.fade{position:absolute;left:0;top:760px;width:1080px;height:1160px;background:linear-gradient(180deg,rgba(6,24,19,0),rgba(6,24,19,.82) 26%,rgba(6,24,19,.96) 60%)}
.frame{position:absolute;left:26px;top:52px;width:1028px;height:1816px;border:2px solid rgba(202,166,74,.85);border-radius:6px}
.card{position:absolute;left:70px;width:940px;bottom:330px;background:rgba(10,52,41,.90);border:2px solid #caa64a;border-radius:10px;padding:40px 44px 44px;text-align:center}
.card.tall{bottom:340px;padding:46px 44px 50px}
.brand{display:flex;align-items:center;justify-content:center;gap:14px;margin-bottom:20px}.brand img{width:54px;border-radius:9px;border:2px solid #f3ede5}.brand b{color:#f3ede5;font-weight:700;letter-spacing:.2em;font-size:27px}
.label{display:inline-block;background:linear-gradient(180deg,#22c4b4,#12a092);border-bottom:4px solid #F2CF5B;padding:14px 46px 12px;margin-bottom:26px}
.label b{display:block;color:#fff;font-weight:700;letter-spacing:.3em;font-size:31px}.label i{display:block;font-style:normal;color:#eafffb;font-weight:600;letter-spacing:.2em;font-size:19px;margin-top:5px}
.l{color:#fff;font-weight:700;font-size:96px;line-height:1.14}.l.hl span{background:#F2CF5B;color:#12261f;padding:0 20px 4px;display:inline-block;line-height:1.12}
.l.s{font-size:78px}
.sub{color:#F2CF5B;font-weight:600;font-size:42px;line-height:1.25;margin-top:16px}
.row{display:flex;justify-content:space-between;align-items:baseline;background:#f3ede5;border-left:10px solid #19b3a4;padding:16px 22px 14px 24px;margin-top:14px;text-align:left}
.row b{color:#12261f;font-weight:700;font-size:42px;letter-spacing:.03em}.row i{font-style:normal;color:#12261f;font-weight:600;font-size:31px}
.tell{color:#F2CF5B;font-weight:700;letter-spacing:.14em;font-size:36px;margin-top:22px}
.cheer{color:#F2CF5B;font-weight:700;font-size:100px;line-height:1.1;margin-top:14px}.cheer.s{font-size:70px;line-height:1.12}
.url{display:inline-block;background:linear-gradient(180deg,#22c4b4,#12a092);color:#fff;font-weight:700;font-size:38px;letter-spacing:.04em;padding:12px 34px 14px;margin-top:26px;border-radius:4px}`;
const html = (c, withCard) => { let h = '';
  if (withCard) { if (c.brand) h += `<div class="brand"><img src="${LOGO}"><b>ZANS RACING</b></div>`;
    if (c.label) h += `<div class="label"><b>${esc(c.label[0])}</b><i>${esc(c.label[1])}</i></div>`;
    for (const [t, k] of c.lines || []) h += `<div class="l ${k} ${t.length > 15 ? 's' : ''}"><span>${esc(t)}</span></div>`;
    for (const [a, b] of c.rows || []) h += `<div class="row"><b>${esc(a)}</b><i>${esc(b)}</i></div>`;
    for (const s of c.sub || []) h += `<div class="sub">${esc(s)}</div>`;
    if (c.tell) h += `<div class="tell">${esc(c.tell)}</div>`; if (c.cheer) h += `<div class="cheer ${c.cheer.length > 20 ? 's' : ''}">${esc(c.cheer)}</div>`; if (c.url) h += `<div class="url">${esc(c.url)}</div>`;
    h = `<div class="card ${c.tall ? 'tall' : ''}">${h}</div>`; }
  return `<style>${CSS}</style>` + (withCard ? '' : '<div class="fade"></div><div class="frame"></div><div class="strip t"></div><div class="strip b"></div>') + h; };
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1920 } }); fs.mkdirSync(path.join(__dirname, 'ov'), { recursive: true });
  await p.setContent(html({}, false)); await p.screenshot({ path: path.join(__dirname, 'ov', 'base.png'), omitBackground: true });   // strips, frame and the dark fade: on from frame 1
  for (const s of [...S.main, ...S.tiktok]) { await p.setContent(html(s.card, true)); await p.evaluate(() => document.fonts.ready); await p.screenshot({ path: path.join(__dirname, 'ov', s.key + '.png'), omitBackground: true });
    const box = await p.evaluate(() => { const r = document.querySelector('.card').getBoundingClientRect(); return [Math.round(r.top), Math.round(r.bottom)]; }); console.log(s.key, 'card y', box.join('-')); }
  await b.close(); })();
