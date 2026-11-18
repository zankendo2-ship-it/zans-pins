// Renders the locked ZANS 3-part post for every entry in posts.json:
//   slide 1 = the product photo with metal strips (no text), slide 2 = carousel_hook.html, slide 3 = carousel_endcard.html,
// at 1080x1350 (feed carousel) and 1080x1920 (Reels/TikTok clips). Usage: node templates/render.js <out_dir> [post_key ...]
// text goes dark on light post colours (yellow, white) so it stays readable
const lum = h => { const n = parseInt(h.slice(1), 16); return (0.299*(n>>16) + 0.587*((n>>8)&255) + 0.114*(n&255))/255; };
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const T = __dirname, FONTDIR = path.join(T, 'fonts'), ASSETS = path.join(T, 'assets');
const b64 = f => fs.readFileSync(f).toString('base64');
const font = (fam, file, w) => `@font-face{font-family:'${fam}';font-weight:${w};src:url(data:font/woff2;base64,${b64(path.join(FONTDIR, file))}) format("woff2")}`;
const FONTS = font('Jost', 'jost-600.woff2', 600) + font('Jost', 'jost-700.woff2', 700) + font('Plex', 'plex-mono-700.woff2', 700);
const METAL = {
  gold:   { STRIPE: 'linear-gradient(90deg,#725415 0%,#B98A36 22%,#FFF4C9 50%,#B98A36 78%,#725415 100%)', EDGE: '#E6C766', TEXT: '#F2CF5B', INSET: '#6B5300' },
  silver: { STRIPE: 'linear-gradient(90deg,#5E646B 0%,#A9AFB6 22%,#F7F9FB 50%,#A9AFB6 78%,#5E646B 100%)', EDGE: '#D3D8DD', TEXT: '#E9EDF1', INSET: '#5E646B' },
};
// Exact positions from the approved post2-ombudsman slides. 9x16 keeps all text between y 340 and 1440.
const LAYOUT = {
  '4x5':  { W: 1080, H: 1350, hook: { Y_EB: 330, Y_BIG: 380, BIG_SIZE: 104, Y_SUB: 610, SUB_SIZE: 46, Y_RULE: 710, Y_Q: 760, Q_SIZE: 56 },
            end: { Y_EB: 214, Y_LOGO: 262, LOGO_W: 560, Y_WISH: 752, WISH_SIZE: 84, Y_BTN: 958, Y_URL: 1060 } },
  '9x16': { W: 1080, H: 1920, hook: { Y_EB: 470, Y_BIG: 520, BIG_SIZE: 112, Y_SUB: 770, SUB_SIZE: 50, Y_RULE: 880, Y_Q: 930, Q_SIZE: 60 },
            end: { Y_EB: 350, Y_LOGO: 410, LOGO_W: 700, Y_WISH: 1000, WISH_SIZE: 94, Y_BTN: 1222, Y_URL: 1350 } },
};
const fill = (tpl, v) => tpl.replace(/\{\{(\w+)\}\}/g, (_, k) => (k in v ? v[k] : `{{${k}}}`));
const CSS = fs.readFileSync(path.join(T, '_brand.css'), 'utf8');
(async () => {
  const out = process.argv[2] || 'out'; fs.mkdirSync(out, { recursive: true });
  const posts = JSON.parse(fs.readFileSync(path.join(T, 'posts.json'), 'utf8'));
  const only = process.argv.slice(3);
  const b = await chromium.launch();
  for (const [key, P] of Object.entries(posts)) {
    if (only.length && !only.includes(key)) continue;
    const christmas = (P.season || 'christmas') === 'christmas';
    const logo = `data:image/png;base64,${b64(path.join(ASSETS, christmas ? 'zans-logo-santa-2x.png' : 'zans-logo.png'))}`;
    for (const [fmt, L] of Object.entries(LAYOUT)) {
      const base = { ...METAL[P.metal || 'gold'], W: L.W, H: L.H, COLOUR: P.colour || '#1F5A3D', INK: P.ink || (lum(P.colour || '#1F5A3D') > 0.55 ? '#1C1C1C' : '#FFFFFF'), BADGE: P.badge || (christmas ? 'CHRISTMAS 2026' : 'ZANS RACING'),
        FOOT_STRIPE: L.H - 72, FOOT_BAR: L.H - 60, FONTS };
      base.CSS = fill(CSS, base);
      const pages = {
        hook: fill(fs.readFileSync(path.join(T, 'carousel_hook.html'), 'utf8'), { ...base, ...L.hook, BIG_SIZE: Math.round(L.hook.BIG_SIZE * (P.bigSize || 1)), EYEBROW: P.eyebrow, BIG: P.big, SUB: P.sub, QUESTION: P.question }),
        end: fill(fs.readFileSync(path.join(T, 'carousel_endcard.html'), 'utf8'), { ...base, ...L.end, LOGO: logo, LOGO_X: (L.W - L.end.LOGO_W) / 2,
          GREETING: P.greeting || (christmas ? 'Wishing you a<br>Merry Christmas' : 'Personalised<br>racing gifts') }),
        // slide 1 frame, exactly as Alex's locked reference (05e640f): thin metal strip at the very top and very bottom only
        frame: fill(`<!doctype html><meta charset="utf-8"><style>{{CSS}}</style><div class="stripe" style="top:0"></div><div class="stripe" style="top:{{H12}}px"></div>`, { ...base, H12: L.H - 12 }),
      };
      for (const [name, html] of Object.entries(pages)) {
        const p = await b.newPage({ viewport: { width: L.W, height: L.H } });
        await p.setContent(html); await p.evaluate(() => document.fonts.ready);
        const left = await p.evaluate(() => document.body.innerHTML.match(/\{\{\w+\}\}/g));
        if (left) throw new Error(`${key} ${fmt} ${name}: unfilled ${left}`);
        await p.screenshot({ path: path.join(out, `${key}-${fmt}-${name}.png`), omitBackground: name === 'frame' }); await p.close();
      }
      console.log(key, fmt, 'done');
    }
  }
  await b.close();
})();
