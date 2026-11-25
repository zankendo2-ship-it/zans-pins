// Round ceramic bauble print files, re-made after the 25 Nov print check. Face 2.95 in = 74.93 mm, 3960 px.
// No thin ring; all key content inside a 6 mm safe zone; name 6 mm+ tall; MERRY CHRISTMAS 3.5 mm+ in dark ink; no tiny logo text.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const F = 74.93, C = F / 2, SAFE = C - 6, INK = '#1C1C1C';
const hex = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16)); const toHex = a => '#' + a.map(v => Math.round(Math.max(0, Math.min(255, v))).toString(16).padStart(2, '0')).join('').toUpperCase();
function hsl([r, g, b]) { r /= 255; g /= 255; b /= 255; const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2; let h = 0, s = 0; if (mx !== mn) { const d = mx - mn; s = l > .5 ? d / (2 - mx - mn) : d / (mx + mn); h = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; h /= 6; } return [h, s, l]; }
function rgb([h, s, l]) { const f = (p, q, t) => { t = (t + 1) % 1; return t < 1 / 6 ? p + (q - p) * 6 * t : t < .5 ? q : t < 2 / 3 ? p + (q - p) * (2 / 3 - t) * 6 : p; }; if (!s) return [l, l, l].map(v => v * 255); const q = l < .5 ? l * (1 + s) : l + s - l * s, p = 2 * l - q; return [f(p, q, h + 1 / 3), f(p, q, h), f(p, q, h - 1 / 3)].map(v => v * 255); }
const deep = (h, sat = 1.25, lig = .84) => { const [a, s, l] = hsl(hex(h)); return l > .97 || s < .04 ? h : toHex(rgb([a, Math.min(1, s * sat), l * lig])); };  // richer, darker for glazed ceramic; white and black left alone
const shade = (h, k) => toHex(hex(h).map(v => v * k));
const lum = h => { const [r, g, b] = hex(h).map(v => v / 255); return .2126 * r + .7152 * g + .0722 * b; };
const JOBS = [
  { file: 'loussiemoo-A-approved-hexes', name: ['LOUSSIEMOO'], body: '#F3B5C9', second: '#6CC24A', cap: '#F3B5C9', pattern: 'spots', note: 'Approved hexes (Alex, 21 Nov) kept exactly' },
  { file: 'loussiemoo-B-deeper-ceramic', name: ['LOUSSIEMOO'], body: deep('#F3B5C9', 1.0, .88), second: deep('#6CC24A', 1.15, .82), cap: deep('#F3B5C9', 1.0, .88), pattern: 'spots', note: 'Deeper pink and green for ceramic' },
  { file: 'rexs-romance', name: ['REXS', 'ROMANCE'], body: deep('#1C4FA0', 1.15, .8), second: null, cap: '#FFFFFF', pattern: 'plain', note: 'Deeper blue for ceramic; white cap' },
  { file: 'zoo-olympios', name: ['ZOO', 'OLYMPIOS'], body: deep('#F5D130', 1.2, .9), second: '#111111', cap: '#111111', pattern: 'diag', note: 'Deeper yellow for ceramic; black spots and cap' } ];
function pattern(j) { let o = `<rect width="${F}" height="${F}" fill="${j.body}"/>`;
  if (j.pattern === 'spots') for (let r = -1; r < 8; r++) for (let c = -1; c < 8; c++) o += `<circle cx="${c * 12.5 + (r % 2 ? 6.25 : 0)}" cy="${6.3 + r * 10.85}" r="3.95" fill="${j.second}" stroke="${shade(j.second, .62)}" stroke-width=".35"/>`;
  if (j.pattern === 'diag') for (let r = -1; r < 5; r++) for (let c = -1; c < 6; c++) o += `<circle cx="${1.8 + r * 3.5 + c * 19.5}" cy="${15 + r * 22.5}" r="3.2" fill="${j.second}"/>`;
  return o; }
function art(j, m) { const capLine = lum(j.cap) > .5 ? shade(j.cap === '#FFFFFF' ? '#B9BDC2' : j.cap, .62) : '#6E7378', visor = lum(j.cap) > .5 ? shade(j.cap === '#FFFFFF' ? '#D5D8DB' : j.cap, .8) : '#3A3D41';
  const nameCol = [j.body, j.second].filter(Boolean).find(c => lum(c) < .16) || INK;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${F}mm" height="${F}mm" viewBox="0 0 ${F} ${F}" style="display:block">
${pattern(j)}
<path d="M0 0 H${F} V12 Q${C} 16.5 0 12 Z" fill="${j.cap}"/><path d="M0 12 Q${C} 16.5 ${F} 12" fill="none" stroke="${INK}" stroke-width=".55"/>
${[[13, 13.3], [27.5, 14], [47.4, 14], [62, 13.3]].map(([x, y]) => `<line x1="${C}" y1="7.8" x2="${x}" y2="${y}" stroke="${capLine}" stroke-width=".7" stroke-linecap="round"/>`).join('')}<circle cx="${C}" cy="7.8" r="1.4" fill="${capLine}"/>
<path d="M17.5 15.2 Q${C} 17.1 ${F - 17.5} 15.2 Q${C} 26 17.5 15.2 Z" fill="${visor}" stroke="${INK}" stroke-width=".55" stroke-linejoin="round"/>
<rect x="${C - m.pw / 2}" y="${m.py}" width="${m.pw}" height="${m.ph}" rx="5" fill="#FFFDF7" stroke="${INK}" stroke-width=".7"/>
${j.name.map((t, i) => `<text x="${C}" y="${m.py + m.pad + m.capN + i * m.lineN}" text-anchor="middle" font-family="Jost" font-weight="700" font-size="${m.fsN}" fill="${nameCol}">${t}</text>`).join('')}
<text x="${C}" y="${m.py + m.ph - m.pad}" text-anchor="middle" font-family="Jost" font-weight="700" font-size="${m.fsM}" letter-spacing="${m.lsM}" fill="${INK}">MERRY CHRISTMAS</text></svg>`; }
(async () => { const b = await chromium.launch(); const css = `${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}*{margin:0;box-sizing:border-box}`; const report = [];
  const pm = await b.newPage(); await pm.setContent(`<html><head><style>${css}</style></head><body><canvas id="c"></canvas></body></html>`); await pm.waitForTimeout(300);
  const measure = (txt, fs, ls = 0) => pm.evaluate(([txt, fs, ls]) => { const x = document.getElementById('c').getContext('2d'); x.font = `700 ${fs * 100}px Jost`; const m = x.measureText(txt), h = x.measureText('H'); return { w: m.width / 100 + ls * (txt.length - 1), cap: h.actualBoundingBoxAscent / 100 }; }, [txt, fs, ls]);
  for (const j of JOBS) { const pad = 3.1, gap = 3.0;
    const cy = j.name.length > 1 ? 39.6 : 38.5, long = j.name.reduce((a, t) => t.length > a.length ? t : a);
    let fsN = 9.4, fsM = 5.2, lsM, mN, mM, lineN, ph, pw, py, far;
    for (; ; fsN -= .05) { mN = await measure(long, fsN); lsM = .45; for (; ; lsM -= .05) { mM = await measure('MERRY CHRISTMAS', fsM, lsM); if (mM.w <= Math.max(mN.w, 46) || lsM <= .06) break; }
      lineN = fsN * .98; ph = pad + mN.cap + (j.name.length - 1) * lineN + gap + mM.cap + pad; pw = Math.max(mN.w, mM.w) + 5; py = cy - ph / 2;
      far = Math.max(...[[C - pw / 2 + 1.5, py + 1.5], [C + pw / 2 - 1.5, py + 1.5], [C - pw / 2 + 1.5, py + ph - 1.5], [C + pw / 2 - 1.5, py + ph - 1.5]].map(([x, y]) => Math.hypot(x - C, y - C)));
      if (far <= SAFE - .3 || fsN < 6) break; }
    const m = { pad, fsN, fsM, lsM, capN: mN.cap, lineN, ph, pw, py };
    const corner = far;
    const ok = corner <= SAFE && mN.cap >= 6 && mM.cap >= 3.5;
    report.push({ file: j.file, note: j.note, body: j.body, second: j.second, cap: j.cap, name_cap_mm: +mN.cap.toFixed(2), merry_christmas_cap_mm: +mM.cap.toFixed(2), panel_mm: [+pw.toFixed(1), +ph.toFixed(1)], furthest_key_content_from_centre_mm: +corner.toFixed(1), safe_radius_mm: +SAFE.toFixed(1), pass: ok });
    const svg = art(j, m);
    const p = await b.newPage({ viewport: { width: 990, height: 990 }, deviceScaleFactor: 4 }); await p.setContent(`<html><head><style>${css}svg{width:990px;height:990px}</style></head><body>${svg}</body></html>`); await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(__dirname, `ZANS-bauble-PRINT-FILE-${j.file}-3960px-DRAFT.png`) }); await p.close();
    // flat real-size proof at 300 dpi (1 mm = 11.811 px): disc 885 px on a 1400 x 1560 sheet
    const k = 300 / 25.4, d = F * k, ox = (1400 - d) / 2, oy = 150;
    const q = await b.newPage({ viewport: { width: 1400, height: 1560 }, deviceScaleFactor: 1 });
    await q.setContent(`<html><head><style>${css}body{width:1400px;height:1560px;background:#fff;font-family:Jost;color:#1C1C1C;position:relative}
.d{position:absolute;left:${ox}px;top:${oy}px;width:${d}px;height:${d}px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 2px #1C1C1C}.d svg{width:${d}px;height:${d}px}
.sz{position:absolute;left:${ox + 6 * k}px;top:${oy + 6 * k}px;width:${d - 12 * k}px;height:${d - 12 * k}px;border-radius:50%;border:3px dashed #E0115F}
.t{position:absolute;left:0;right:0;text-align:center}</style></head><body>
<div class="t" style="top:26px;font:700 44px Jost">FLAT REAL-SIZE PROOF · ${j.name.join(' ')}</div><div class="t" style="top:84px;font:600 26px Jost">${j.note}. Print at 100% (300 dpi): the disc is 74.9 mm across.</div>
<div class="d">${svg}</div><div class="sz"></div>
<div class="t" style="top:${oy + d + 26}px;font:600 30px Jost"><span style="color:#E0115F;font-weight:700">- - -</span> 6 mm safe zone: cap button, peak, name panel and all text sit inside it. Colour bleeds to the edge. No ring.</div>
<div class="t" style="top:${oy + d + 78}px;font:700 32px Jost">Name ${mN.cap.toFixed(1)} mm tall · MERRY CHRISTMAS ${mM.cap.toFixed(1)} mm tall, dark ink · panel ${pw.toFixed(0)} x ${ph.toFixed(0)} mm</div>
<div class="t" style="top:${oy + d + 132}px;font:600 28px Jost">Colours: body ${j.body}${j.second ? ' · spots ' + j.second : ''} · cap ${j.cap} · text ${INK}</div>
<div class="t" style="top:${oy + d + 180}px;font:700 30px Jost;color:${ok ? '#1F5A3D' : '#C8102E'}">${ok ? 'FILE CHECK: PASS' : 'FILE CHECK: FAIL'} (furthest key content ${corner.toFixed(1)} mm from centre; safe radius ${SAFE.toFixed(1)} mm)</div>
<div style="position:absolute;left:${ox}px;top:${oy + d + 240}px;width:${50 * k}px;border-top:4px solid #1C1C1C"></div><div style="position:absolute;left:${ox}px;top:${oy + d + 248}px;font:600 26px Jost">50 mm check line: measure it after printing</div>
</body></html>`); await q.waitForTimeout(300); await q.screenshot({ path: path.join(__dirname, `ZANS-bauble-FLAT-PROOF-${j.file}-300dpi-DRAFT.png`) }); await q.close(); }
  fs.writeFileSync(path.join(__dirname, 'print-check.json'), JSON.stringify(report, null, 1)); console.log(JSON.stringify(report)); await b.close(); })();
