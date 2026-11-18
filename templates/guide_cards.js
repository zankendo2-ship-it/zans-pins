// ZANS racecourse guide cheat-sheet carousel (the Kempton draw-sheet look: black bars, gold line, racing green, cream card).
// Usage: node templates/guide_cards.js <out_dir> [post_key ...]   Data: templates/guide_posts.json   Output: <key>-<n>.png at 1080x1350.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = __dirname, FD = path.join(T, 'fonts');
const b64 = f => fs.readFileSync(f).toString('base64');
const font = (fam, file, w) => `@font-face{font-family:'${fam}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(FD, file))}) format("woff2")}`;
const FONTS = font('Jost', 'jost-600.woff2', 600) + font('Jost', 'jost-700.woff2', 700) + font('Plex', 'plex-mono-700.woff2', 700)
  + font('Sans', 'source-sans-3-400.woff2', 400) + font('Sans', 'source-sans-3-600.woff2', 600);
const LOGO = `data:image/png;base64,${b64(path.join(T, 'assets', 'zans-logo.png'))}`;
const CSS = `${FONTS}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;background:#1F5A3D;font-family:Sans,sans-serif;color:#fff;position:relative}
.top{position:absolute;left:0;right:0;top:0;height:74px;background:#141414;display:flex;align-items:center;justify-content:space-between;padding:0 56px;font-family:Jost;font-weight:600;font-size:25px;letter-spacing:.2em}
.top b{color:#F2CF5B;font-weight:600}
.line{position:absolute;left:0;right:0;top:74px;height:10px;background:#F2CF5B}
.foot{position:absolute;left:0;right:0;bottom:0;height:86px;background:#141414;display:flex;align-items:center;justify-content:space-between;padding:0 56px;font-size:25px}
.foot b{font-family:Jost;font-weight:600;color:#F2CF5B;letter-spacing:.08em;font-size:27px}
.wrap{position:absolute;left:56px;right:56px;top:112px;bottom:112px;display:flex;flex-direction:column}
.eyebrow{font-family:Jost;font-weight:600;letter-spacing:.24em;font-size:24px;color:#F3EDE5;margin-bottom:14px}
.num{display:inline-block;font-family:Plex;font-weight:700;font-size:30px;color:#141414;background:#F2CF5B;padding:4px 16px;margin-bottom:16px;align-self:flex-start}
h1{font-family:Jost;font-weight:700;color:#F2CF5B;font-size:94px;line-height:1.0;letter-spacing:-.005em}
h1.sm{font-size:84px}
.sub{font-size:36px;margin-top:20px;color:#fff}
.card{background:#F3EDE5;border:3px solid #F2CF5B;color:#1C1C1C;margin-top:34px;padding:10px 36px;flex:1;display:flex;flex-direction:column;justify-content:center}
.row{display:flex;align-items:center;padding:20px 0;border-bottom:2px solid #C9BDAE}
.row:last-of-type{border-bottom:0}
.lab{width:300px;font-family:Jost;font-weight:600;letter-spacing:.14em;font-size:28px;color:#5E574F}
.lab.hi{color:#1F5A3D}
.val{flex:1}
.fig{font-family:Plex;font-weight:700;font-size:62px;line-height:1;color:#1C1C1C}
.fig.hi{color:#1F5A3D}
.cnt{font-size:25px;color:#5E574F;margin-top:6px}
.bar{height:16px;background:#C9BDAE;margin-top:10px}
.bar.hi{background:#1F5A3D}
.fact{font-family:Jost;font-weight:600;font-size:40px;color:#1C1C1C}
.c4 .row{padding:13px 0}.c5 .row{padding:7px 0}.c5 .fig{font-size:50px}.c5 .cnt{font-size:23px;margin-top:3px}.c5 .bar{height:13px;margin-top:6px}
.note{font-size:23px;color:#5E574F;padding-top:12px;border-top:2px solid #C9BDAE}
.strip{background:#141414;color:#fff;font-family:Jost;font-weight:600;font-size:31px;text-align:center;padding:17px 16px;margin-top:22px}
.src{font-size:21px;color:#D9E4DC;margin-top:14px;text-align:center}
.huge{font-family:Plex;font-weight:700;font-size:250px;line-height:1;color:#1F5A3D;text-align:center}
.hsub{font-family:Jost;font-weight:600;font-size:44px;text-align:center;letter-spacing:.06em;color:#1C1C1C;margin-bottom:22px}
.ln{font-size:31px;text-align:center;color:#1C1C1C;padding:9px 0;border-top:2px solid #C9BDAE}
.pt{display:flex;align-items:center;padding:19px 0;border-bottom:2px solid #C9BDAE;font-family:Jost;font-weight:600;font-size:40px}
.pt:last-child{border-bottom:0}
.pt i{font-style:normal;font-family:Plex;font-weight:700;color:#1F5A3D;width:76px;font-size:44px}
.save{border:3px solid #F2CF5B;color:#F2CF5B;font-family:Jost;font-weight:600;letter-spacing:.14em;font-size:35px;text-align:center;padding:22px 16px;margin-top:40px;text-transform:uppercase;line-height:1.3}
.q{font-family:Jost;font-weight:600;font-size:46px;text-align:center;line-height:1.25;margin-top:40px}
.qbox{background:#F3EDE5;border:3px solid #F2CF5B;color:#1C1C1C;padding:30px 34px;margin-top:40px;text-align:center}
.qbox small{display:block;font-family:Jost;font-weight:600;letter-spacing:.2em;font-size:23px;color:#5E574F;margin-bottom:14px}
.qbox div{font-family:Jost;font-weight:700;font-size:46px;line-height:1.2}
.logo{width:300px;border-radius:16px;display:block;margin:0 auto 34px}
`;
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
function body(P, s) {
  const head = (s.num ? `<div class="num">${esc(s.num)} OF 4</div>` : (s.eyebrow ? `<div class="eyebrow">${esc(s.eyebrow)}</div>` : ''))
    + `<h1 class="${s.big.length > 26 ? 'sm' : ''}">${esc(s.big)}</h1>` + (s.sub ? `<div class="sub">${esc(s.sub)}</div>` : '');
  const strip = s.strip ? `<div class="strip">${esc(s.strip)}</div>` : '';
  const src = `<div class="src">${esc(P.source)}</div>`;
  if (s.type === 'cover') return head + `<div class="card">${s.points.map((p, i) => `<div class="pt"><i>${i + 1}</i>${esc(p)}</div>`).join('')}</div>` + strip + src;
  if (s.type === 'facts') return head + `<div class="card">${s.rows.map(r => `<div class="row"><div class="lab">${esc(r[0])}</div><div class="val"><div class="fact">${esc(r[1])}</div></div></div>`).join('')}</div>` + strip + src;
  if (s.type === 'bars') { const mx = Math.max(...s.rows.map(r => r[2]));
    return head + `<div class="card c${s.rows.length}">${s.rows.map(r => `<div class="row"><div class="lab ${r[4] ? 'hi' : ''}">${esc(r[0])}</div><div class="val"><div class="fig ${r[4] ? 'hi' : ''}">${esc(r[3])}</div><div class="cnt">${esc(r[1])}</div><div class="bar ${r[4] ? 'hi' : ''}" style="width:${(100 * r[2] / mx).toFixed(1)}%"></div></div></div>`).join('')}${s.note ? `<div class="note">${esc(s.note)}</div>` : ''}</div>` + strip + src; }
  if (s.type === 'stat') return head + `<div class="card"><div class="huge">${esc(s.figure)}</div><div class="hsub">${esc(s.figsub)}</div>${s.lines.map(l => `<div class="ln">${esc(l)}</div>`).join('')}</div>` + strip + src;
  if (s.type === 'end') return `<div style="flex:1;display:flex;flex-direction:column;justify-content:center"><img class="logo" src="${LOGO}"><div class="save">${esc(s.big)}</div><div class="qbox"><small>TELL US IN THE COMMENTS</small><div>${esc(s.question)}</div></div></div>`;
}
(async () => {
  const out = process.argv[2] || 'out'; fs.mkdirSync(out, { recursive: true });
  const posts = JSON.parse(fs.readFileSync(path.join(T, 'guide_posts.json'), 'utf8')); const only = process.argv.slice(3);
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const [key, P] of Object.entries(posts)) { if (only.length && !only.includes(key)) continue;
    for (let i = 0; i < P.slides.length; i++) {
      const html = `<html><head><meta charset="utf-8"><style>${CSS}</style></head><body><div class="top"><span>ZANS RACING · HORSE RACING GUIDES</span><b>${esc(P.course)}</b></div><div class="line"></div><div class="wrap">${body(P, P.slides[i])}</div><div class="foot"><span>${esc(P.footer)}</span><b>www.zanshorseracing.co.uk</b></div></body></html>`;
      await pg.setContent(html); await pg.evaluate(() => document.fonts.ready);
      const over = await pg.evaluate(() => { const w = document.querySelector('.wrap'); return w.scrollHeight - w.clientHeight; });
      const f = path.join(out, `${key}-${i + 1}.png`); await pg.screenshot({ path: f }); console.log(f, over > 0 ? `OVERFLOW ${over}px` : 'ok');
    } }
  await b.close();
})();
