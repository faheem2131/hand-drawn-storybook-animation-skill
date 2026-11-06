// Render the animation frame by frame with headless Chromium.
//   node render.cjs frames <outdir> [fps]       → PNG sequence (deterministic: renderAt(t))
//   node render.cjs stills <outdir> t1 t2 ...   → individual stills
const { chromium } = require('playwright');
const { mkdirSync, writeFileSync } = require('node:fs');
const { pathToFileURL } = require('node:url');
const path = require('node:path');
(async () => {

const [mode, out, ...rest] = process.argv.slice(2);
mkdirSync(out, { recursive: true });
const here = __dirname;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
page.on('pageerror', e => { console.error('PAGE ERROR', e); process.exit(1); });
await page.goto(pathToFileURL(path.join(here, 'index.html')).href + '#capture');
await page.waitForFunction(() => typeof window.renderAt === 'function');
await page.evaluate(() => document.fonts.ready);

async function grab(t) {
  const url = await page.evaluate(t => { window.renderAt(t); return document.getElementById('c').toDataURL('image/png'); }, t);
  return Buffer.from(url.split(',')[1], 'base64');
}
if (mode === 'frames') {
  const fps = +(rest[0] || 30), dur = await page.evaluate(() => window.DURATION), N = Math.round(dur * fps);
  for (let i = 0; i < N; i++) {
    writeFileSync(path.join(out, `f${String(i).padStart(5, '0')}.png`), await grab(i / fps));
    if (i % 60 === 0) console.log(`frame ${i}/${N}`);
  }
} else {
  for (const t of rest) writeFileSync(path.join(out, `t${(+t).toFixed(2).padStart(6, '0')}.png`), await grab(+t));
}
await browser.close();
})();
