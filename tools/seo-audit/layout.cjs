// Live layout check of www.zanshorseracing.co.uk in real Chrome (runs on GitHub; the Claude sandbox cannot reach the site).
//  1. Gift pages: is the top photo BESIDE the text on computer screens (1024px and wider) and BELOW it on a phone?
//     (4 Nov 2026: PR #1 put the photo under the text on screens 1280px+; PR #2 fixed it. This catches it if it comes back.)
//     Also: does any page scroll sideways?
//  2. Mug designer (phone size): built-in CSS, no Tailwind CDN script, the 3D library fetched once, the 3D mug drawn,
//     no errors, and no 3D redraws while nobody touches the page.
// Usage: NODE_PATH=<dir with playwright-core> node tools/seo-audit/layout.cjs <out dir>
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright-core');

const out = process.argv[2] || 'layout-out';
fs.mkdirSync(out, { recursive: true });
const BASE = process.env.SITE_BASE || 'https://www.zanshorseracing.co.uk'; // SITE_BASE = a local copy, for testing this script
const PAGES = ['/horse-racing-gifts/', '/gifts-for-racehorse-owners/', '/racing-syndicate-gifts/'];
const WIDTHS = [390, 1024, 1280, 1440, 1920];
const chromePath = ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', process.env.CHROME_PATH].find(p => p && fs.existsSync(p));

const COUNT_DRAWS = () => {
  window.__draws = 0;
  for (const C of [window.WebGLRenderingContext, window.WebGL2RenderingContext]) {
    if (!C) continue;
    for (const f of ['drawElements', 'drawArrays']) { const o = C.prototype[f]; C.prototype[f] = function () { window.__draws++; return o.apply(this, arguments); }; }
  }
};

(async () => {
  const browser = await chromium.launch({ executablePath: chromePath, headless: true,
    args: ['--no-sandbox', '--enable-unsafe-swiftshader', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] });
  const R = { chrome: browser.version(), run_utc: new Date().toISOString(), hero: [], designer: {} };
  const L = [`# Live layout check ${R.run_utc}`, '', `Chrome ${R.chrome}`, '', '## Top photo on the gift pages', ''];

  for (const p of PAGES) {
    for (const w of WIDTHS) {
      const phone = w < 600;
      const ctx = await browser.newContext({ viewport: { width: w, height: 900 }, deviceScaleFactor: 1, isMobile: phone, hasTouch: phone });
      const page = await ctx.newPage();
      let row = { page: p, width: w };
      try {
        await page.goto(BASE + p + '?layoutcheck=' + Date.now(), { waitUntil: 'load', timeout: 60000 });
        await page.waitForTimeout(800);
        const b = await page.evaluate(() => {
          const grid = document.querySelector('.hero .in');
          if (!grid) return null;
          const text = [...grid.children].find(k => k.querySelector('h1'));
          const img = grid.querySelector('img');
          const r = e => { const x = e.getBoundingClientRect(); return { left: Math.round(x.left), top: Math.round(x.top + scrollY), right: Math.round(x.right), bottom: Math.round(x.bottom + scrollY), width: Math.round(x.width) }; };
          return { text: text ? r(text) : null, img: img ? r(img) : null, img_src: img ? img.currentSrc : null, page_width: document.documentElement.scrollWidth };
        });
        let layout = 'not found';
        if (b && b.text && b.img) {
          if (b.img.left >= b.text.right - 2 && b.img.top < b.text.bottom && b.img.bottom > b.text.top) layout = 'beside';
          else if (b.img.top >= b.text.bottom - 2) layout = 'below';
          else layout = 'other';
        }
        const expect = w >= 1024 ? 'beside' : 'below';
        const sideways = b ? b.page_width > w : null;
        row = { ...row, layout, expect, ok: layout === expect && !sideways, sideways_scroll: sideways, ...b };
        if (w === 1440) await page.screenshot({ path: path.join(out, `hero${p.replace(/\//g, '_')}1440.jpg`), type: 'jpeg', quality: 60 });
      } catch (e) {
        row = { ...row, ok: false, error: String(e).slice(0, 300) };
      }
      R.hero.push(row);
      L.push(`- ${p} at ${w}px: photo ${row.layout || 'ERROR'} the text (expected ${row.expect || '?'})${row.sideways_scroll ? ', PAGE SCROLLS SIDEWAYS' : ''} -> ${row.ok ? 'OK' : 'PROBLEM'}${row.error ? ' ' + row.error : ''}`);
      await ctx.close();
    }
  }

  // Mug designer at phone size
  const D = R.designer;
  try {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true });
    await ctx.addInitScript(COUNT_DRAWS);
    const page = await ctx.newPage();
    const errors = [], three = [];
    page.on('pageerror', e => errors.push(String(e).slice(0, 200)));
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text().slice(0, 200)); });
    page.on('request', q => { if (q.url().includes('three.min.js')) three.push(q.url()); });
    const resp = await page.goto(BASE + '/mug-designer/?layoutcheck=' + Date.now(), { waitUntil: 'load', timeout: 60000 });
    const raw = await resp.text();
    D.tailwind_cdn_script = raw.includes('cdn.tailwindcss.com');
    D.built_in_css = raw.includes('<style id="zans-tw">');
    await page.waitForTimeout(10000);
    D.canvas = await page.evaluate(() => !!document.querySelector('canvas'));
    D.fallback_message_shown = await page.evaluate(() => /3D preview could not load/.test(document.body.innerText));
    const d0 = await page.evaluate(() => window.__draws);
    await page.waitForTimeout(5000);
    D.draws_while_idle_5s = (await page.evaluate(() => window.__draws)) - d0;
    D.three_requests = three.length;
    D.errors = errors;
    await page.screenshot({ path: path.join(out, 'designer_phone.jpg'), type: 'jpeg', quality: 60 });
    D.ok = !D.tailwind_cdn_script && D.built_in_css && D.canvas && !D.fallback_message_shown && D.three_requests === 1 && D.draws_while_idle_5s === 0 && errors.length === 0;
    await ctx.close();
  } catch (e) {
    D.ok = false; D.error = String(e).slice(0, 300);
  }
  L.push('', '## Mug designer (phone size)', '',
    `- Tailwind CDN script on the page: ${D.tailwind_cdn_script ? 'YES (old page)' : 'no'}; built-in CSS: ${D.built_in_css ? 'yes' : 'NO'}`,
    `- 3D library requests: ${D.three_requests}; 3D mug drawn: ${D.canvas ? 'yes' : 'NO'}; flat-print fallback shown: ${D.fallback_message_shown ? 'YES' : 'no'}`,
    `- 3D redraws in 5 s with nobody touching the page: ${D.draws_while_idle_5s}`,
    `- Errors: ${D.errors && D.errors.length ? D.errors.join(' | ') : 'none'}${D.error ? ' ' + D.error : ''}`,
    `- Result: ${D.ok ? 'OK' : 'PROBLEM'}`);
  R.all_ok = R.hero.every(h => h.ok) && !!D.ok;
  L.push('', `ALL OK: ${R.all_ok ? 'yes' : 'NO'}`);
  fs.writeFileSync(path.join(out, 'layout.json'), JSON.stringify(R, null, 1));
  fs.writeFileSync(path.join(out, 'layout.md'), L.join('\n') + '\n');
  console.log(L.join('\n'));
  await browser.close();
})();
