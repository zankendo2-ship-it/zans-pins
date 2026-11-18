// ZANS racecourse guide carousel in the ZANS predictions-sheet look (Alex, 18 Nov 2026): cream page, gold metal strips,
// a vibrant course-colour header bar with a metal line under it, stat tiles, pills and segmented bars.
// Usage: node templates/guide_cards.js <out_dir> [post_key ...]   Data: templates/guide_posts.json   Output: <key>-<n>.png at 1080x1350.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = __dirname, FD = path.join(T, 'fonts');
const b64 = f => fs.readFileSync(f).toString('base64');
const font = (fam, file, w) => `@font-face{font-family:'${fam}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(FD, file))}) format("woff2")}`;
const FONTS = font('Jost', 'jost-600.woff2', 600) + font('Jost', 'jost-700.woff2', 700) + font('Plex', 'plex-mono-700.woff2', 700)
  + font('Sans', 'source-sans-3-400.woff2', 400) + font('Sans', 'source-sans-3-600.woff2', 600);
const LOGO = `data:image/png;base64,${b64(path.join(T, 'assets', 'zans-logo.png'))}`;
const METAL = 'linear-gradient(90deg,#725415 0%,#B98A36 22%,#FFF4C9 50%,#B98A36 78%,#725415 100%)';
const FLAG = '<svg width="62" height="40" viewBox="0 0 62 40"><rect width="62" height="40" fill="#fff" stroke="#1C1C1C" stroke-width="2"/><rect x="25" width="12" height="40" fill="#CE1124"/><rect y="14" width="62" height="12" fill="#CE1124"/></svg>';
const lum = h => { const n = parseInt(h.slice(1), 16); return (0.299*(n>>16) + 0.587*((n>>8)&255) + 0.114*(n&255))/255; };
const css = (C, ON, TXT) => `${FONTS}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;background:#EAE2D8;font-family:Sans,sans-serif;color:#1C1C1C;position:relative}
.metal{position:absolute;left:0;right:0;height:16px;background:${METAL}}
.wrap{position:absolute;left:44px;right:44px;top:44px;bottom:44px;display:flex;flex-direction:column}
.brand{border:3px solid #1C1C1C;border-radius:8px;background:#F3EDE5;padding:14px 22px;display:flex;align-items:center;justify-content:space-between}
.brand b{font-family:Jost;font-weight:700;letter-spacing:.14em;font-size:25px}
.brand span{display:block;font-family:Plex;font-weight:700;font-size:21px;margin-top:3px;color:#5E574F}
.hbar{margin-top:20px;background:${C};color:${ON};border-radius:10px 10px 0 0;padding:18px 26px;display:flex;align-items:baseline;justify-content:space-between}
.hbar .n{font-family:Plex;font-weight:700;font-size:44px}
.hbar .c{font-family:Jost;font-weight:700;letter-spacing:.16em;font-size:40px;margin-left:18px}
.hbar .r{font-size:26px;font-weight:600}
.hline{height:9px;background:${METAL}}
.panel{background:#F3EDE5;border:2px solid #C9BDAE;border-top:0;border-radius:0 0 10px 10px;padding:22px 26px 24px;flex:1;display:flex;flex-direction:column}
.eyebrow{font-family:Jost;font-weight:700;letter-spacing:.18em;font-size:23px;color:#5E574F}
h1{font-family:Jost;font-weight:700;font-size:78px;line-height:1.0;margin-top:6px;color:#1C1C1C}
h1 em{font-style:normal;color:${TXT}}
.sub{font-size:31px;color:#5E574F;margin-top:10px}
.rows{flex:1;display:flex;flex-direction:column;justify-content:space-around;margin-top:14px;border-top:3px solid #1C1C1C}
.row{display:flex;align-items:center;padding:12px 0 12px 16px;border-bottom:2px solid #C9BDAE;border-left:10px solid transparent}
.row:last-child{border-bottom:0}
.row.best{border-left-color:#2E7D32;background:#EAF3E6}
.lab{width:290px;font-family:Jost;font-weight:700;letter-spacing:.1em;font-size:29px}
.val{flex:1}
.top{display:flex;align-items:baseline;gap:18px}
.fig{font-family:Plex;font-weight:700;font-size:58px;line-height:1}
.cnt{font-size:25px;color:#5E574F}
.segs{display:flex;gap:6px;margin-top:9px}
.segs i{width:38px;height:22px;border-radius:4px;background:#DDD3C6}
.g .fig{color:#2E7D32}.g .segs i.on{background:#2E7D32}
.a .fig{color:#1C1C1C}.a .segs i.on{background:#E0A100}
.r .fig{color:#B03A2E}.r .segs i.on{background:#B03A2E}
.pill{display:inline-block;font-family:Jost;font-weight:700;letter-spacing:.1em;font-size:20px;border:2px solid;border-radius:6px;padding:3px 10px;margin-left:6px;position:relative;top:-8px}
.g .pill{color:#2E7D32}.r .pill{color:#B03A2E}
.fact{font-family:Jost;font-weight:700;font-size:46px}
.note{font-size:23px;color:#5E574F;margin-top:8px}
.strip{background:#1C1C1C;color:#F3EDE5;font-family:Jost;font-weight:600;font-size:30px;text-align:center;padding:15px 14px;margin-top:16px;border-radius:8px}
.strip b{color:#F2CF5B;font-weight:700}
.src{font-size:20px;color:#5E574F;margin-top:10px;text-align:center}
.foot{display:flex;justify-content:space-between;align-items:center;margin-top:12px;font-size:23px;color:#5E574F}
.foot b{font-family:Jost;font-weight:700;letter-spacing:.06em;color:#1C1C1C;font-size:25px}
.tiles{display:flex;gap:14px;margin-top:18px}
.tile{flex:1;background:#F3EDE5;border:2px solid #C9BDAE;border-top:9px solid ${C};border-radius:8px;text-align:center;padding:12px 6px 14px}
.tile b{display:block;font-family:Plex;font-weight:700;font-size:58px;color:${TXT};line-height:1.05}
.tile span{font-family:Jost;font-weight:600;letter-spacing:.12em;font-size:20px;color:#5E574F}
.logo{width:250px;border:4px solid #1C1C1C;border-radius:26px;display:block;margin:18px auto 0}
.course{font-family:Jost;font-weight:700;letter-spacing:.14em;font-size:104px;text-align:center;color:${TXT};line-height:1;margin-top:14px}
.csub{font-family:Jost;font-weight:700;font-size:40px;text-align:center;color:#5E574F;margin-top:6px}
.rule{height:12px;background:${METAL};margin-top:18px}
.gl{font-family:Jost;font-weight:700;letter-spacing:.12em;font-size:25px;color:${TXT};margin-top:20px;padding-bottom:6px;border-bottom:3px solid ${C}}
.list{background:#F3EDE5;border:2px solid #C9BDAE;border-radius:8px;margin-top:10px;flex:1;display:flex;flex-direction:column}
.li{flex:1;display:flex;align-items:center;padding:0 22px;border-bottom:2px solid #C9BDAE;font-family:Sans;font-weight:600;font-size:36px}
.li:last-child{border-bottom:0}
.li i{font-style:normal;font-family:Plex;font-weight:700;color:${TXT};width:70px;font-size:40px}
.li u{margin-left:auto;text-decoration:none;font-family:Jost;font-weight:700;letter-spacing:.08em;font-size:20px;border:2px solid #5E574F;color:#5E574F;border-radius:6px;padding:4px 10px}
.huge{font-family:Plex;font-weight:700;font-size:230px;line-height:.95;color:#B03A2E;text-align:center;margin-top:6px}
.hsub{font-family:Jost;font-weight:700;font-size:44px;text-align:center;letter-spacing:.06em}
.dots{display:flex;flex-wrap:wrap;gap:5px;margin:12px auto 4px;width:810px}
.dots i{width:19px;height:19px;border-radius:50%;background:#DDD3C6}.dots i.on{background:#B03A2E}
.ln{font-size:31px;text-align:center;padding:9px 0;border-top:2px solid #C9BDAE;font-weight:600}
.save{background:${C};color:${ON};font-family:Jost;font-weight:700;letter-spacing:.1em;font-size:40px;text-align:center;padding:26px 18px;border-radius:10px 10px 0 0;margin-top:26px;text-transform:uppercase;line-height:1.25}
.qbox{background:#F3EDE5;border:2px solid #C9BDAE;border-top:0;border-radius:0 0 10px 10px;padding:30px 30px;text-align:center}
.qbox small{display:block;font-family:Jost;font-weight:700;letter-spacing:.2em;font-size:24px;color:#5E574F;margin-bottom:12px}
.qbox div{font-family:Jost;font-weight:700;font-size:50px;line-height:1.18}
.soon{font-family:Jost;font-weight:700;font-size:30px;text-align:center;margin-top:26px;color:#5E574F}
.url{font-family:Jost;font-weight:700;letter-spacing:.1em;font-size:36px;text-align:center;margin-top:8px}
`;
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const brand = P => `<div class="brand"><div><b>ZANS RACING · HORSE RACING GUIDES</b><span>${esc(P.tagline)}</span></div>${P.flag === false ? '' : FLAG}</div>`;
const foot = P => `<div class="foot"><span>${esc(P.footer)}</span><b>www.zanshorseracing.co.uk</b></div>`;
function body(P, s) {
  if (s.type === 'cover') return brand(P) + `<img class="logo" src="${LOGO}"><div class="course" style="${P.courseSize ? `font-size:${P.courseSize}px;letter-spacing:.08em` : ''}">${esc(P.course)}</div><div class="csub">${esc(s.sub)}</div><div class="rule"></div>
    <div class="tiles">${s.tiles.map(t => `<div class="tile"><b>${esc(t[0])}</b><span>${esc(t[1])}</span></div>`).join('')}</div>
    <div class="gl">${esc(s.gl || 'WHAT TO LOOK OUT FOR')}</div><div class="list">${s.points.map((p, i) => `<div class="li"><i>${i + 1}</i>${esc(p[0])}<u>${esc(p[1])}</u></div>`).join('')}</div>
    <div class="strip">${s.strip}</div>`;
  if (s.type === 'end') return brand(P) + `<img class="logo" src="${LOGO}" style="width:330px;margin-top:34px"><div class="save">${esc(s.big)}</div><div class="qbox"><small>TELL US IN THE COMMENTS</small><div>${esc(s.question)}</div></div><div class="rule" style="margin-top:30px"></div><div class="soon">${esc(P.footer)}</div><div class="url">WWW.ZANSHORSERACING.CO.UK</div>`;
  const head = brand(P) + `<div class="hbar"><div><span class="n">${esc(s.num)}</span><span class="c">${esc(P.course)}</span></div><span class="r">${esc(P.code)}</span></div><div class="hline"></div>`;
  const title = `<div class="eyebrow">${esc(s.eyebrow)}</div><h1>${s.big}</h1><div class="sub">${esc(s.sub)}</div>`;
  let mid = '';
  if (s.type === 'facts') mid = `<div class="rows">${s.rows.map(r => `<div class="row"><div class="lab" style="color:#5E574F">${esc(r[0])}</div><div class="val"><div class="fact">${esc(r[1])}</div></div></div>`).join('')}</div>`;
  if (s.type === 'bars') { const mx = Math.max(...s.rows.map(r => r[2]));
    mid = `<div class="rows">${s.rows.map(r => { const on = Math.max(1, Math.round(14 * r[2] / mx)); const k = r[4];
      return `<div class="row ${k} ${k === 'g' ? 'best' : ''}"><div class="lab">${esc(r[0])}</div><div class="val"><div class="top"><span class="fig">${esc(r[3])}</span><span class="cnt">${esc(r[1])}</span>${k === 'g' ? '<span class="pill">BEST</span>' : ''}${k === 'r' ? '<span class="pill">LOWEST</span>' : ''}</div><div class="segs">${Array.from({ length: 14 }, (_, i) => `<i class="${i < on ? 'on' : ''}"></i>`).join('')}</div></div></div>`; }).join('')}</div>` + (s.note ? `<div class="note">${esc(s.note)}</div>` : ''); }
  if (s.type === 'stat') mid = `<div style="flex:1;display:flex;flex-direction:column;justify-content:center;border-top:3px solid #1C1C1C;margin-top:14px"><div class="huge">${esc(s.figure)}</div><div class="hsub">${esc(s.figsub)}</div><div class="dots">${Array.from({ length: s.dots[0] }, (_, i) => `<i class="${s.dots[1].includes(i) ? 'on' : ''}"></i>`).join('')}</div>${s.lines.map(l => `<div class="ln">${esc(l)}</div>`).join('')}</div>`;
  return head + `<div class="panel">${title}${mid}</div><div class="strip">${s.strip}</div><div class="src">${esc(P.source)}</div>` + foot(P);
}
(async () => {
  const out = process.argv[2] || 'out'; fs.mkdirSync(out, { recursive: true });
  const posts = JSON.parse(fs.readFileSync(path.join(T, 'guide_posts.json'), 'utf8')); const only = process.argv.slice(3);
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const [key, P] of Object.entries(posts)) { if (only.length && !only.includes(key)) continue;
    const ON = lum(P.colour) > 0.6 ? '#1C1C1C' : '#FFFFFF';
    for (let i = 0; i < P.slides.length; i++) {
      const html = `<html><head><meta charset="utf-8"><style>${css(P.colour, ON, P.text || P.colour)}</style></head><body><div class="metal" style="top:0"></div><div class="wrap">${body(P, P.slides[i])}</div><div class="metal" style="bottom:0"></div></body></html>`;
      await pg.setContent(html); await pg.evaluate(() => document.fonts.ready);
      const over = await pg.evaluate(() => { const w = document.querySelector('.wrap'); return w.scrollHeight - w.clientHeight; });
      const f = path.join(out, `${key}-${i + 1}.png`); await pg.screenshot({ path: f }); console.log(f, over > 0 ? `OVERFLOW ${over}px` : 'ok');
    } }
  await b.close();
})();
