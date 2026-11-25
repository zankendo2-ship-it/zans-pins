// v3: SQUARE chrome cufflinks + slim silver BAR tie clip. Code-drawn concept previews. No supplier, no paid credits.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const METAL = 'linear-gradient(90deg,#8a6a22,#f2cf5b 18%,#fff3c8 32%,#c9a13b 50%,#fff3c8 68%,#f2cf5b 82%,#8a6a22)';
const CH = ['#5f6468', '#c9ccd0', '#ffffff', '#9a9ea3'];
const sq = { // square insert, 100 x 100
  stripes: (a, b) => `<rect width="100" height="100" fill="${a}"/>` + [0, 2, 4].map(i => `<rect x="${10 + i * 16}" width="16" height="100" fill="${b}"/>`).join(''),
  hoops: (a, b) => `<rect width="100" height="100" fill="${a}"/>` + [0, 2, 4].map(i => `<rect y="${10 + i * 16}" width="100" height="16" fill="${b}"/>`).join(''),
  spots: (a, b) => `<rect width="100" height="100" fill="${a}"/>` + [[20, 20], [50, 20], [80, 20], [35, 50], [65, 50], [20, 80], [50, 80], [80, 80], [5, 50], [95, 50]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="9" fill="${b}"/>`).join(''),
  chevrons: (a, b) => `<rect width="100" height="100" fill="${a}"/>` + [4, 36, 68].map(y => `<path d="M0 ${y + 22} L50 ${y} L100 ${y + 22} L100 ${y + 36} L50 ${y + 14} L0 ${y + 36} Z" fill="${b}"/>`).join(''),
  diamonds: (a, b) => `<rect width="100" height="100" fill="${a}"/>` + [0, 1, 2, 3, 4].flatMap(r => [0, 1, 2, 3, 4].map(c => [c * 25 + (r % 2 ? 12.5 : 0), r * 25])).map(([x, y]) => `<path d="M${x} ${y - 11} L${x + 9} ${y} L${x} ${y + 11} L${x - 9} ${y} Z" fill="${b}"/>`).join(''),
  quartered: (a, b) => `<rect width="100" height="100" fill="${a}"/><rect width="50" height="50" fill="${b}"/><rect x="50" y="50" width="50" height="50" fill="${b}"/>`,
  bigspots: (a, b) => `<rect width="100" height="100" fill="${a}"/>` + [[25, 25], [75, 25], [50, 50], [25, 75], [75, 75], [0, 50], [100, 50], [50, 0], [50, 100]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="14" fill="${b}"/>`).join(''),
  cap: (a, b) => `<rect width="100" height="100" fill="${a}"/><g transform="translate(50 54) scale(.98) translate(-50 -57)"><g fill="#fff" stroke="#8a8f94" stroke-width="2.2" stroke-linejoin="round"><path d="M34 40 L12 80 L22 86 L39 58 Z"/><path d="M66 40 L88 80 L78 86 L61 58 Z"/><path d="M34 40 L44 36 Q50 42 56 36 L66 40 L63 60 L64 92 L36 92 L37 60 Z"/><path d="M44 36 Q50 43 56 36" fill="none"/></g><path d="M38 35 A12 13 0 0 1 62 35 Z" fill="#111"/><path d="M60 30 L71 35 L60 35 Z" fill="#111"/></g>`,
  capA: (a, b) => `<rect width="100" height="100" fill="${a}"/><g transform="translate(50 54) scale(.98) translate(-50 -57)"><g fill="#fff" stroke="#8a8f94" stroke-width="2.2" stroke-linejoin="round"><path d="M34 40 L12 80 L22 86 L39 58 Z"/><path d="M66 40 L88 80 L78 86 L61 58 Z"/><path d="M34 40 L44 36 Q50 42 56 36 L66 40 L63 60 L64 92 L36 92 L37 60 Z"/><path d="M44 36 Q50 43 56 36" fill="none"/></g><path d="M38 35 A12 13 0 0 1 62 35 Z" fill="#111"/><path d="M60 30 L71 35 L60 35 Z" fill="#111"/></g>`,
  capB: (a, b) => `<rect width="100" height="100" fill="${a}"/><g transform="translate(50 54) scale(.98) translate(-50 -57)"><g fill="#fff" stroke="#8a8f94" stroke-width="2.2" stroke-linejoin="round"><path d="M34 40 L12 80 L22 86 L39 58 Z"/><path d="M66 40 L88 80 L78 86 L61 58 Z"/><path d="M34 40 L44 36 Q50 42 56 36 L66 40 L63 60 L64 92 L36 92 L37 60 Z"/><path d="M44 36 Q50 43 56 36" fill="none"/></g><path d="M38 35 A12 13 0 0 1 62 35 Z" fill="#111"/><path d="M60 30 L71 35 L60 35 Z" fill="#111"/></g>`,
  blank: () => `<rect width="100" height="100" fill="#f4f4f2"/>` };
const bar = { // long bar face, 900 x 100: the same silks idea scaled to read on a slim bar
  stripes: (a, b) => `<rect width="900" height="100" fill="${a}"/><rect y="20" width="900" height="20" fill="${b}"/><rect y="60" width="900" height="20" fill="${b}"/>`,
  hoops: (a, b) => `<rect width="900" height="100" fill="${a}"/>` + [...Array(9)].map((_, i) => `<rect x="${50 + i * 100}" width="50" height="100" fill="${b}"/>`).join(''),
  spots: (a, b) => `<rect width="900" height="100" fill="${a}"/>` + [...Array(18)].map((_, i) => `<circle cx="${25 + i * 50}" cy="${i % 2 ? 72 : 28}" r="15" fill="${b}"/>`).join(''),
  chevrons: (a, b) => `<rect width="900" height="100" fill="${a}"/>` + [...Array(11)].map((_, i) => `<path d="M${i * 90 - 30} 0 L${i * 90 + 20} 50 L${i * 90 - 30} 100 L${i * 90 + 10} 100 L${i * 90 + 60} 50 L${i * 90 + 10} 0 Z" fill="${b}"/>`).join(''),
  diamonds: (a, b) => `<rect width="900" height="100" fill="${a}"/>` + [...Array(13)].map((_, i) => `<path d="M${i * 75} 12 L${i * 75 + 28} 50 L${i * 75} 88 L${i * 75 - 28} 50 Z" fill="${b}"/>`).join(''),
  quartered: (a, b) => `<rect width="900" height="100" fill="${a}"/><rect width="450" height="50" fill="${b}"/><rect x="450" y="50" width="450" height="50" fill="${b}"/>`,
  bigspots: (a, b) => `<rect width="900" height="100" fill="${a}"/>` + [...Array(10)].map((_, i) => `<circle cx="${45 + i * 90}" cy="50" r="27" fill="${b}"/>`).join(''),
  cap: (a, b) => `<rect width="900" height="100" fill="${a}"/><g transform="translate(250 -4) scale(1.08 1.08) translate(-50 0)"><g fill="#fff" stroke="#8a8f94" stroke-width="2.2" stroke-linejoin="round"><path d="M34 40 L12 80 L22 86 L39 58 Z"/><path d="M66 40 L88 80 L78 86 L61 58 Z"/><path d="M34 40 L44 36 Q50 42 56 36 L66 40 L63 60 L64 92 L36 92 L37 60 Z"/><path d="M44 36 Q50 43 56 36" fill="none"/></g><path d="M38 35 A12 13 0 0 1 62 35 Z" fill="#111"/><path d="M60 30 L71 35 L60 35 Z" fill="#111"/></g>`,
  capA: (a, b) => `<rect width="900" height="100" fill="${a}"/><rect width="170" height="100" fill="${b}"/>`,
  capB: (a, b) => `<rect width="900" height="100" fill="${a}"/><g transform="translate(150 -34) scale(1.75) translate(-50 0)"><g fill="#fff" stroke="#8a8f94" stroke-width="2.2" stroke-linejoin="round"><path d="M34 40 L12 80 L22 86 L39 58 Z"/><path d="M66 40 L88 80 L78 86 L61 58 Z"/><path d="M34 40 L44 36 Q50 42 56 36 L66 40 L63 60 L64 92 L36 92 L37 60 Z"/><path d="M44 36 Q50 43 56 36" fill="none"/></g><path d="M38 35 A12 13 0 0 1 62 35 Z" fill="#111"/><path d="M60 30 L71 35 L60 35 Z" fill="#111"/></g>`,
  blank: () => `<rect width="900" height="100" fill="#f4f4f2"/>` };
const D = [['C-clip-option-A', 'capA', 'Constitution Hill colours: tie clip option A, bold black band', '#FFFFFF', '#111111'], ['C-clip-option-B', 'capB', 'Constitution Hill colours: tie clip option B, larger motif', '#FFFFFF', '#111111']];
let uid = 0; const defs = id => `<linearGradient id="${id}m" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="${CH[2]}"/><stop offset=".3" stop-color="${CH[1]}"/><stop offset=".62" stop-color="${CH[0]}"/><stop offset="1" stop-color="${CH[3]}"/></linearGradient>
<linearGradient id="${id}v" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${CH[0]}"/><stop offset=".35" stop-color="${CH[2]}"/><stop offset=".65" stop-color="${CH[1]}"/><stop offset="1" stop-color="${CH[0]}"/></linearGradient>
<linearGradient id="${id}g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".12"/><stop offset=".4" stop-color="#fff" stop-opacity=".04"/><stop offset="1" stop-color="#000" stop-opacity=".06"/></linearGradient>
<filter id="${id}s" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="10" stdDeviation="9" flood-opacity=".38"/></filter>`;
// square cufflink, front-on. s = side in px
function cuffFront(s, kind, a, b) { const id = 'q' + (uid++), r = s * .075;
  return `<svg width="${s + 40}" height="${s + 50}" viewBox="-20 -15 ${s + 40} ${s + 50}"><defs>${defs(id)}</defs>
<rect width="${s}" height="${s}" rx="${s * .05}" fill="url(#${id}m)" filter="url(#${id}s)"/><g transform="translate(${r} ${r}) scale(${(s - 2 * r) / 100})"><clipPath id="${id}q"><rect width="100" height="100"/></clipPath><g clip-path="url(#${id}q)">${sq[kind](a, b)}</g></g>
<rect x="${r}" y="${r}" width="${s - 2 * r}" height="${s - 2 * r}" fill="url(#${id}g)"/><rect x="${r}" y="${r}" width="${s - 2 * r}" height="${s - 2 * r}" fill="none" stroke="rgba(0,0,0,.3)" stroke-width="2"/></svg>`; }
// square cufflink at a 3/4 angle: face skewed, chrome side for depth, post and bullet toggle behind
function cuff34(s, kind, a, b) { const id = 'q' + (uid++), r = s * .075, kx = .8, sk = .2, dp = s * .2, w = s * kx, rise = s * kx * sk;
  return `<svg width="${w + dp + s * .95 + 40}" height="${s + rise + 60}" viewBox="-20 ${-rise - 20} ${w + dp + s * .95 + 40} ${s + rise + 60}"><defs>${defs(id)}</defs>
<g filter="url(#${id}s)"><rect x="${w + dp - 4}" y="${s / 2 - rise + dp * .15 - s * .065}" width="${s * .4}" height="${s * .13}" fill="url(#${id}v)"/>
<rect x="${w + dp + s * .36}" y="${s / 2 - rise + dp * .15 - s * .4}" width="${s * .22}" height="${s * .8}" rx="${s * .11}" fill="url(#${id}m)"/>
<path d="M${w} ${-rise} L${w + dp} ${-rise + dp * .3} L${w + dp} ${s - rise + dp * .3} L${w} ${s - rise} Z" fill="url(#${id}v)"/>
<path d="M0 ${s} L${w} ${s - rise} L${w + dp} ${s - rise + dp * .3} L${dp} ${s + dp * .3} Z" fill="${CH[0]}"/>
<g transform="matrix(${kx} ${-kx * sk} 0 1 0 0)"><rect width="${s}" height="${s}" rx="${s * .05}" fill="url(#${id}m)"/><g transform="translate(${r} ${r}) scale(${(s - 2 * r) / 100})"><clipPath id="${id}q"><rect width="100" height="100"/></clipPath><g clip-path="url(#${id}q)">${sq[kind](a, b)}</g></g>
<rect x="${r}" y="${r}" width="${s - 2 * r}" height="${s - 2 * r}" fill="url(#${id}g)"/><rect x="${r}" y="${r}" width="${s - 2 * r}" height="${s - 2 * r}" fill="none" stroke="rgba(0,0,0,.3)" stroke-width="2"/></g></g></svg>`; }
// bar tie clip, front-on. L x H in px
function clipFront(L, H, kind, a, b) { const id = 'b' + (uid++), r = H * .1;
  return `<svg width="${L + 40}" height="${H + 50}" viewBox="-20 -15 ${L + 40} ${H + 50}"><defs>${defs(id)}<clipPath id="${id}c"><rect x="${r}" y="${r}" width="${L - 2 * r}" height="${H - 2 * r}" rx="${H * .08}"/></clipPath></defs>
<rect width="${L}" height="${H}" rx="${H * .16}" fill="url(#${id}v)" filter="url(#${id}s)"/><g clip-path="url(#${id}c)"><g transform="translate(${r} ${r}) scale(${(L - 2 * r) / 900} ${(H - 2 * r) / 100})">${bar[kind](a, b)}</g>
<rect width="${L}" height="${H * .45}" fill="#fff" opacity=".06"/></g>
<rect x="${r}" y="${r}" width="${L - 2 * r}" height="${H - 2 * r}" rx="${H * .08}" fill="none" stroke="rgba(0,0,0,.3)" stroke-width="2"/></svg>`; }
// bar tie clip at a 3/4 angle with the back arm and the spring hinge at the left end
function clip34(L, H, kind, a, b) { const id = 'b' + (uid++), r = H * .1, kx = .86, sk = .16, w = L * kx, rise = w * sk, off = H * .55;
  return `<svg width="${w + off + 60}" height="${H + rise + off + 70}" viewBox="-30 ${-rise - off - 20} ${w + off + 60} ${H + rise + off + 70}"><defs>${defs(id)}<clipPath id="${id}c"><rect x="${r}" y="${r}" width="${L - 2 * r}" height="${H - 2 * r}" rx="${H * .08}"/></clipPath></defs>
<g filter="url(#${id}s)"><g transform="translate(${off} ${-off}) matrix(${kx} ${-kx * sk} 0 1 0 0)"><rect x="${L * .04}" y="${H * .2}" width="${L * .9}" height="${H * .6}" rx="${H * .2}" fill="url(#${id}v)" stroke="${CH[0]}" stroke-width="2"/></g>
<path d="M0 0 L${off} ${-off} L${off} ${H - off} L0 ${H} Z" fill="url(#${id}m)" stroke="${CH[0]}" stroke-width="2"/><ellipse cx="${off * .5}" cy="${H * .5 - off * .5}" rx="${H * .2}" ry="${H * .26}" fill="${CH[0]}"/><ellipse cx="${off * .5}" cy="${H * .5 - off * .5}" rx="${H * .09}" ry="${H * .12}" fill="${CH[2]}"/>
<path d="M0 0 L${w} ${-rise} L${w + off * .25} ${-rise - off * .25} L${off * .25} ${-off * .25} Z" fill="${CH[2]}"/>
<g transform="matrix(${kx} ${-kx * sk} 0 1 0 0)"><rect width="${L}" height="${H}" rx="${H * .16}" fill="url(#${id}v)"/><g clip-path="url(#${id}c)"><g transform="translate(${r} ${r}) scale(${(L - 2 * r) / 900} ${(H - 2 * r) / 100})">${bar[kind](a, b)}</g><rect width="${L}" height="${H * .45}" fill="#fff" opacity=".06"/></g>
<rect x="${r}" y="${r}" width="${L - 2 * r}" height="${H - 2 * r}" rx="${H * .08}" fill="none" stroke="rgba(0,0,0,.3)" stroke-width="2"/></g></g></svg>`; }
const head = (t, sub) => `<html><head><style>${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}*{box-sizing:border-box;margin:0}
body{width:2000px;height:1500px;position:relative;overflow:hidden;font-family:Jost;background:radial-gradient(ellipse at 50% 40%,#24684a,#143524)}
.s{position:absolute;left:0;right:0;height:38px;background:${METAL}}.card{position:absolute;left:110px;width:1780px;background:#F3EDE5;border:3px solid #C9BDAE;border-radius:26px;box-shadow:0 22px 50px rgba(0,0,0,.45)}
.ct{position:absolute;left:44px;top:26px;font:700 44px Jost;letter-spacing:7px;color:#1F5A3D}.zm{position:absolute;right:44px;top:34px;font:700 28px Jost;letter-spacing:6px;color:#1F5A3D}
.lab{font:700 30px Jost;letter-spacing:4px;color:#5E574F;text-align:center}.mm{font:700 34px Jost;color:#1C1C1C;text-align:center}
.pane{position:absolute;top:300px;width:850px;height:1040px;border-radius:26px;overflow:hidden;box-shadow:0 22px 50px rgba(0,0,0,.45);border:3px solid #C9BDAE}
.cap{position:absolute;left:0;right:0;bottom:0;padding:16px 0 18px;background:rgba(243,237,229,.96);text-align:center;font:700 38px Jost;letter-spacing:2px;color:#1C1C1C}</style></head><body><div class="s" style="top:0"></div><div class="s" style="bottom:0"></div>
<div style="position:absolute;left:0;right:0;top:66px;text-align:center;font:700 86px Jost;letter-spacing:5px;color:#fff">${t}</div>
<div style="position:absolute;left:0;right:0;top:178px;text-align:center;font:700 40px Jost;letter-spacing:2px;color:#F2CF5B">${sub}</div>`;
const foot = t => `<div style="position:absolute;left:0;right:0;bottom:58px;text-align:center;font:600 32px Jost;letter-spacing:4px;color:#EAE2D8">${t}</div></body></html>`;
const rule = (px, t) => `<div style="width:${px}px;margin:2px auto 0;border-top:3px solid #1C1C1C;position:relative;height:12px"><i style="position:absolute;left:0;top:-9px;height:16px;border-left:3px solid #1C1C1C"></i><i style="position:absolute;right:0;top:-9px;height:16px;border-left:3px solid #1C1C1C"></i></div><div class="mm">${t}</div>`;
const sub = ([, , name]) => name.toUpperCase();
function page(d) { const [n, kind, , a, b] = d, PX = 22, L = 55 * PX, H = 6 * PX, S = 17 * PX;
  return head('SILKS TIE CLIP &amp; SQUARE CUFFLINKS', sub(d)) + `
<div class="card" style="top:286px;height:410px"><div class="ct">BAR TIE CLIP</div><div class="zm">ZANS · RACING</div>
<div style="position:absolute;left:60px;top:104px;width:${L + 40}px"><div class="lab">FRONT</div>${clipFront(L, H, kind, a, b)}<div style="margin-top:-30px">${rule(L, 'about 55 mm long, 6 mm tall')}</div></div>
<div style="position:absolute;left:1330px;top:92px;width:420px"><div class="lab">ANGLE: HINGE END</div><div style="width:420px;height:200px;margin-top:12px;overflow:hidden;position:relative"><div style="position:absolute;left:0;bottom:-6px">${clip34(L * .6, H * .7, kind, a, b)}</div></div><div class="mm" style="font-size:28px">spring clip at the back</div></div></div>
<div class="card" style="top:716px;height:640px"><div class="ct">SQUARE CUFFLINKS</div><div class="zm">ZANS · RACING</div>
<div style="position:absolute;left:70px;top:92px;width:880px"><div class="lab">FRONT (SOLD AS A PAIR)</div><div style="display:flex;justify-content:center;gap:36px">${cuffFront(S, kind, a, b)}${cuffFront(S, kind, a, b)}</div><div style="margin:-30px ${S + 76}px 0 0">${rule(S, 'about 17 mm')}</div></div>
<div style="position:absolute;left:1000px;top:92px;width:730px"><div class="lab">ANGLE: FACE, POST, BULLET BAR</div><div style="display:flex;justify-content:center;margin-top:20px">${cuff34(S * .88, kind, a, b)}</div></div></div>` + foot('SHOWCASE CONCEPT · NO NAME ON THE PRODUCT · NOT A PRODUCT PHOTO'); }
function worn(d) { const [, kind, , a, b] = d, S = 11;
  return head('HOW BIG IS IT WHEN WORN?', sub(d)) + `
<div class="pane" style="left:120px;background:linear-gradient(100deg,#fbfbf9,#e9e9e4)"><div style="position:absolute;left:50%;top:0;width:6px;height:100%;margin-left:-3px;background:rgba(0,0,0,.06)"></div>
<svg style="position:absolute;left:0;top:0" width="850" height="1040"><defs><pattern id="w" width="18" height="18" patternTransform="rotate(45)" patternUnits="userSpaceOnUse"><rect width="18" height="18" fill="#2c2f36"/><rect width="18" height="5" fill="#363a43"/></pattern></defs>
<path d="M${425 - 300} -10 L${425 + 300} -10 L${425 + 80 * S / 2} 1040 L${425 - 80 * S / 2} 1040 Z" fill="url(#w)"/><path d="M${425 - 300} -10 L${425 - 80 * S / 2} 1040" stroke="rgba(0,0,0,.35)" stroke-width="6"/></svg>
<div style="position:absolute;left:${425 - 55 * S / 2 - 20}px;top:420px">${clipFront(55 * S, 6 * S, kind, a, b)}</div><div class="cap">55 mm tie clip on an 8 cm tie</div></div>
<div class="pane" style="left:1030px;background:linear-gradient(160deg,#3a3f4a,#22252c)"><div style="position:absolute;left:-40px;top:300px;width:900px;height:${62 * S}px;transform:rotate(-7deg)">
<div style="position:absolute;left:0;top:${6 * S}px;width:330px;height:${50 * S}px;background:linear-gradient(180deg,#30343d,#1d2026)"></div>
<div style="position:absolute;left:300px;top:0;width:${68 * S / 1.6}px;height:${62 * S}px;background:linear-gradient(180deg,#ffffff,#e4e4df);border-radius:10px 26px 26px 10px;box-shadow:0 14px 30px rgba(0,0,0,.45)">
<div style="position:absolute;inset:16px;border:3px dashed rgba(0,0,0,.14);border-radius:6px 18px 18px 6px"></div><div style="position:absolute;right:${6 * S}px;top:50%;transform:translateY(-50%)">${cuffFront(17 * S, kind, a, b)}</div></div>
<div style="position:absolute;left:${300 + 68 * S / 1.6 - 6}px;top:${14 * S}px;width:260px;height:${34 * S}px;background:linear-gradient(180deg,#e7c2a0,#cfa27c);border-radius:0 90px 90px 0"></div></div><div class="cap">17 mm cufflink on a shirt cuff</div></div>` + foot('CONCEPT PREVIEW · TIE AND CUFF DRAWN TO THE SAME SCALE · NOT A PRODUCT PHOTO'); }
(async () => { const b = await chromium.launch(); for (const d of D) { const slug = d[2].toLowerCase().replace(/ colours:.*/, '').replace(/[^a-z]+/g, '-').replace(/-$/, '');
  for (const [fn, tag] of [[page, 'CONCEPT'], [worn, 'WORN-SCALE']]) { const p = await b.newPage({ viewport: { width: 2000, height: 1500 } }); await p.setContent(fn(d)); await p.waitForTimeout(250);
    const out = `ZANS-silks-bar-tie-clip-square-cufflinks-${d[0]}-${slug}-${tag}-SHOWCASE-DRAFT-v4.jpg`; await p.screenshot({ path: path.join(__dirname, out), type: 'jpeg', quality: 93 }); await p.close(); console.log(out); } } await b.close(); })();
