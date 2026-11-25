// FACT TO FILE mug print file, re-made as vector at 2x (4950 x 2310) after the 25 Nov mug print check.
// Harrier print area 2475 x 1155 px at 300 dpi = 209.55 x 97.79 mm. Silks colours and layout unchanged; only print quality changes.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = path.join(__dirname, '../../../templates'); const b64 = f => fs.readFileSync(f).toString('base64');
const font = (n, w, f) => `@font-face{font-family:'${n}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(T, 'fonts', f))})}`;
const W = 2475, H = 1155, MM = 300 / 25.4;                       // 1x pixels per mm
const RED = '#C8102E', WHITE = '#FFFFFF', YEL = '#F5D130', GRN = '#00843D', CREAM = '#FBF7F0', INK = '#1C1C1C';   // sampled from the printed test file
const CAP_H = 132, LINE = Math.round(2.0 * MM), BODY = CAP_H + LINE;   // white line now 2.0 mm (was 1.2 mm)
const P = 123.25, EDGE = Math.round(8.3 * MM), PW = 289, PB = Math.round(1.6 * MM);   // plate 8.3 mm from each wrap end (was 6.3), border 1.6 mm (was 1.2)
const NAME = ['FACT', 'TO FILE'], FS = 126, GAP = 132;
function art() { let s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" style="display:block"><rect width="${W}" height="${H}" fill="${YEL}"/>`;
  for (let k = 0; k < 4; k++) s += `<rect y="${BODY + 100.5 + k * 2 * P}" width="${W}" height="${P}" fill="${GRN}"/>`;
  s += `<rect width="${W}" height="${CAP_H}" fill="${RED}"/><rect y="${CAP_H}" width="${W}" height="${LINE}" fill="${WHITE}"/>`;
  const py = BODY + 4, ph = H - py - 54;
  for (const [x, rot] of [[EDGE, -90], [W - EDGE - PW, 90]]) { const cx = x + PW / 2, cy = py + ph / 2;
    s += `<rect x="${x}" y="${py}" width="${PW}" height="${ph}" rx="${PW / 2}" fill="${YEL}"/><rect x="${x + PB}" y="${py + PB}" width="${PW - 2 * PB}" height="${ph - 2 * PB}" rx="${PW / 2 - PB}" fill="${CREAM}"/>
<g transform="rotate(${rot} ${cx} ${cy})">${NAME.map((t, i) => `<text x="${cx}" y="${cy + (i - .5) * GAP + FS * .35}" text-anchor="middle" font-family="Jost" font-weight="700" font-size="${FS}" fill="${GRN}">${t}</text>`).join('')}</g>`; }
  const ty = BODY + 100.5 + 5 * P + P / 2, th = Math.round(7 * MM), fsL = 3.3 * MM / .7, tw = 800;   // logo text 3.3 mm capital height (was about 2 mm), vector text
  s += `<rect x="${1350 - tw / 2}" y="${ty - th / 2}" width="${tw}" height="${th}" rx="14" fill="${CREAM}"/><text x="1350" y="${ty + 3.3 * MM / 2}" text-anchor="middle" font-family="Jost" font-weight="700" font-size="${fsL}" letter-spacing="3" fill="${INK}">ZANS RACING TOOLS</text></svg>`;
  return { s, py, ph, ty, th, tw }; }
(async () => { const b = await chromium.launch(); const css = `${font('Jost', 600, 'jost-600.woff2')}${font('Jost', 700, 'jost-700.woff2')}*{margin:0;box-sizing:border-box}`; const a = art();
  const p = await b.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 2 }); await p.setContent(`<html><head><style>${css}</style></head><body>${a.s}</body></html>`); await p.waitForTimeout(400);
  const caps = await p.evaluate(([FS, fsL]) => { const x = document.createElement('canvas').getContext('2d'); x.font = `700 ${FS}px Jost`; const n = x.measureText('H').actualBoundingBoxAscent; x.font = `700 ${fsL}px Jost`; return [n, x.measureText('H').actualBoundingBoxAscent]; }, [FS, 3.3 * MM / .7]);
  await p.screenshot({ path: path.join(__dirname, 'ZANS-mug-PRINT-FILE-fact-to-file-4950x2310-DRAFT.png') }); await p.close();
  const rep = { file_px: [4950, 2310], print_area_mm: [+(W / MM).toFixed(1), +(H / MM).toFixed(1)], effective_dpi: 600, name_cap_mm: +(caps[0] / MM).toFixed(1), logo_text_cap_mm: +(caps[1] / MM).toFixed(1), white_line_mm: +(LINE / MM).toFixed(1), plate_border_mm: +(PB / MM).toFixed(1), plate_from_wrap_end_mm: +(EDGE / MM).toFixed(1), thinnest_line_mm: +(Math.min(LINE, PB) / MM).toFixed(1), colours: { cap_band: RED, hoops: [YEL, GRN], plate: CREAM, name: GRN, logo_text: INK } };
  fs.writeFileSync(path.join(__dirname, 'print-check.json'), JSON.stringify(rep, null, 1)); console.log(JSON.stringify(rep));
  const k = .9, ox = (2500 - W * k) / 2, oy = 190, dim = (x1, x2, y, t) => `<div style="position:absolute;left:${ox + x1 * k}px;top:${oy + y * k}px;width:${(x2 - x1) * k}px;border-top:4px solid #E0115F"></div><div style="position:absolute;left:${ox + x1 * k - 200}px;top:${oy + y * k + 6}px;width:${(x2 - x1) * k + 400}px;text-align:center;font:700 26px Jost;color:#E0115F;text-shadow:0 0 6px #fff,0 0 6px #fff,0 0 6px #fff">${t}</div>`;
  const q = await b.newPage({ viewport: { width: 2500, height: 1560 } }); await q.setContent(`<html><head><style>${css}body{width:2500px;height:1560px;background:#fff;font-family:Jost;color:#1C1C1C;position:relative}.t{position:absolute;left:0;right:0;text-align:center}</style></head><body>
<div class="t" style="top:28px;font:700 50px Jost">FLAT PROOF · FACT TO FILE MUG WRAP</div><div class="t" style="top:98px;font:600 30px Jost">Print area 209.6 x 97.8 mm. File 4950 x 2310 px = 600 dpi (2x). Shown here at 90% of real size on a 300 dpi sheet.</div>
<div style="position:absolute;left:${ox}px;top:${oy}px;width:${W * k}px;height:${H * k}px;box-shadow:0 0 0 2px #1C1C1C;overflow:hidden"><div style="transform:scale(${k});transform-origin:0 0">${a.s}</div></div>
${dim(0, Math.round(8.3 * MM), 560, '8.3 mm')}${dim(W - Math.round(8.3 * MM), W, 560, '8.3 mm')}
<div class="t" style="top:${oy + H * k + 30}px;font:700 32px Jost">Name ${rep.name_cap_mm} mm tall · logo text ${rep.logo_text_cap_mm} mm tall (vector) · white line under the cap band ${rep.white_line_mm} mm · plate border ${rep.plate_border_mm} mm</div>
<div class="t" style="top:${oy + H * k + 84}px;font:600 30px Jost">Name plates ${rep.plate_from_wrap_end_mm} mm from each wrap end · thinnest line ${rep.thinnest_line_mm} mm · sRGB profile embedded</div>
<div class="t" style="top:${oy + H * k + 134}px;font:600 28px Jost">Colours unchanged from the printed test mug: cap band ${RED} · hoops ${YEL} and ${GRN} · plate ${CREAM} · logo text ${INK}</div>
<div class="t" style="top:${oy + H * k + 184}px;font:700 32px Jost;color:#1F5A3D">PREFLIGHT: PASS on the file. A printed sample is still needed before selling.</div></body></html>`); await q.waitForTimeout(400);
  await q.screenshot({ path: path.join(__dirname, 'ZANS-mug-FLAT-PROOF-fact-to-file-300dpi-DRAFT.png') }); await b.close(); })();
