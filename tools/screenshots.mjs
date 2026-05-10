#!/usr/bin/env node
/**
 * Generiert thumb.jpg pro Demo + assets/og-*.jpg für die Hauptseiten.
 *
 * Nutzung — eine einzige Zeile:
 *   npm install puppeteer        (einmalig)
 *   node tools/screenshots.mjs   (startet eigenen Server + macht alle Bilder)
 *
 * Das Skript:
 *   1. startet einen lokalen Mini-HTTP-Server (Port wird auto-gewählt),
 *   2. lädt jede Seite mit Puppeteer und macht 1200×630-Screenshots,
 *   3. fährt den Server wieder runter und beendet sich sauber.
 *
 * Optional: --base http://localhost:8080 — überspringt den eigenen Server
 *           und nutzt einen schon laufenden.
 */

import puppeteer from 'puppeteer';
import { fileURLToPath } from 'url';
import { dirname, resolve, join, extname } from 'path';
import { existsSync, mkdirSync, createReadStream, statSync } from 'fs';
import { createServer } from 'http';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, '..');

const args = process.argv.slice(2);
const baseFlag = args.indexOf('--base');
const externalBase = baseFlag >= 0 ? args[baseFlag + 1] : null;

const demos = [
  'atelier', 'holzgeist', 'aurora', 'atmen', 'arztpraxis',
  'laden', 'akademie', 'kanzlei', 'lichtblick', 'nachtschicht', 'kontur', 'dashboard',
];

// Hauptseiten — OG-Standard 1200×630 (Facebook/LinkedIn/Twitter erwarten dieses Format).
const mainOg = { viewport: { width: 1200, height: 630 }, clip: { width: 1200, height: 630 } };
const mainPages = [
  { url: '/index.html',                       out: 'assets/og-home.jpg',                             ...mainOg },
  { url: '/referenzen.html',                  out: 'assets/og-referenzen.jpg',                       ...mainOg },
  { url: '/komponenten.html',                 out: 'assets/og-komponenten.jpg',                      ...mainOg },
  { url: '/premium-webdesign.html',           out: 'assets/og-premium-webdesign.jpg',                ...mainOg },
  { url: '/webdesign-coburg.html',            out: 'assets/og-webdesign-coburg.jpg',                 ...mainOg },
  { url: '/webdesign-oberfranken.html',       out: 'assets/og-webdesign-oberfranken.jpg',            ...mainOg },
  { url: '/webdesign-bayern.html',            out: 'assets/og-webdesign-bayern.jpg',                 ...mainOg },
  { url: '/webseite-handwerker-bayern.html',  out: 'assets/og-webseite-handwerker-bayern.jpg',       ...mainOg },
];

// Bilder für die Responsive-Sektion auf der Startseite —
// Startseite in drei Viewport-Grössen geschossen.
// Tablet/Mobile bekommen extra-hohe Clip-Höhe (ca. 1.5× Viewport),
// damit der gestapelte Hero-Bereich (Text + Nadel-Illustration) komplett
// im Bild liegt. Die Device-Frames im CSS croppen mit `background-size: cover`
// von oben aus, sodass Logo + Hero erkennbar bleiben.
const responsiveShots = [
  { url: '/index.html', out: 'assets/responsive-desktop.jpg', viewport: { width: 1440, height: 900  }, clip: { width: 1440, height: 900  }, settle: 2500 },
  { url: '/index.html', out: 'assets/responsive-tablet.jpg',  viewport: { width: 820,  height: 1500 }, clip: { width: 820,  height: 1500 }, settle: 2500 },
  { url: '/index.html', out: 'assets/responsive-mobile.jpg',  viewport: { width: 390,  height: 1200 }, clip: { width: 390,  height: 1200 }, settle: 2500 },
];

const wait = {
  default: 1500,
  atelier: 2500,
  atmen: 2000,
  lichtblick: 2000,
  nachtschicht: 1500,
};

// ---------------------------------------------------------------
// Mini-HTTP-Server
// ---------------------------------------------------------------
const mime = {
  '.html': 'text/html; charset=utf-8',
  '.css':  'text/css; charset=utf-8',
  '.js':   'application/javascript; charset=utf-8',
  '.mjs':  'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg':  'image/svg+xml',
  '.png':  'image/png',
  '.jpg':  'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif':  'image/gif',
  '.webp': 'image/webp',
  '.woff': 'font/woff',
  '.woff2':'font/woff2',
  '.ico':  'image/x-icon',
  '.txt':  'text/plain; charset=utf-8',
  '.xml':  'application/xml; charset=utf-8',
};

function startServer() {
  return new Promise((resolveStart) => {
    const server = createServer((req, res) => {
      try {
        let path = decodeURIComponent(req.url.split('?')[0]);
        if (path.endsWith('/')) path += 'index.html';
        const filePath = join(root, path);
        if (!filePath.startsWith(root)) { res.writeHead(403); res.end(); return; }
        if (!existsSync(filePath) || !statSync(filePath).isFile()) {
          res.writeHead(404, { 'Content-Type': 'text/plain' });
          res.end('Not found: ' + path);
          return;
        }
        const ext = extname(filePath).toLowerCase();
        res.writeHead(200, { 'Content-Type': mime[ext] || 'application/octet-stream' });
        createReadStream(filePath).pipe(res);
      } catch (e) {
        res.writeHead(500); res.end(String(e));
      }
    });
    server.listen(0, '127.0.0.1', () => {
      const port = server.address().port;
      resolveStart({ server, base: `http://127.0.0.1:${port}` });
    });
  });
}

// ---------------------------------------------------------------
// Screenshot-Logik
// ---------------------------------------------------------------
const hideCss = `
  .demo-banner, .demo-exit, .scroll-bar { display: none !important; }
  html { scroll-behavior: auto !important; }
`;

async function shoot(page, url, outPath, label, settleMs, opts = {}) {
  const viewport = opts.viewport || { width: 1200, height: 750 };
  const clip = opts.clip || { width: 1200, height: 750 };
  const fullPage = !!opts.fullPage;
  await page.setViewport(viewport);
  try {
    await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });
  } catch (e) {
    console.warn(`  ⚠ ${label}: ${e.message}`);
    return false;
  }
  await page.addStyleTag({ content: hideCss });
  await page.evaluate(() => window.scrollTo(0, 0));
  await new Promise(r => setTimeout(r, settleMs));

  const screenshotOpts = {
    path: outPath,
    type: 'jpeg',
    quality: 88,
  };
  if (fullPage) {
    // Vollseite: capture top-down, scroll-Höhe variabel
    screenshotOpts.fullPage = true;
  } else {
    screenshotOpts.clip = { x: 0, y: 0, width: clip.width, height: clip.height };
  }
  await page.screenshot(screenshotOpts);
  console.log(`  ✓ ${label} → ${outPath.replace(root + '/', '')}`);
  return true;
}

// ---------------------------------------------------------------
// Main
// ---------------------------------------------------------------
let serverHandle = null;
let base = externalBase;

if (!base) {
  console.log('🌐 Starting local server…');
  serverHandle = await startServer();
  base = serverHandle.base;
  console.log(`   ${base}\n`);
}

const assetsDir = join(root, 'assets');
if (!existsSync(assetsDir)) mkdirSync(assetsDir, { recursive: true });

console.log(`📸 ${demos.length} demos + ${mainPages.length} main pages\n`);

const browser = await puppeteer.launch({
  headless: 'new',
  defaultViewport: { width: 1200, height: 630 },
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
});
const page = await browser.newPage();

console.log('Hauptseiten:');
for (const p of mainPages) {
  await shoot(page, `${base}${p.url}`, join(root, p.out), p.url, 2000, {
    viewport: p.viewport,
    clip: p.clip,
  });
}

console.log('\nDemos:');
for (const demo of demos) {
  const dir = join(root, 'demos', demo);
  if (!existsSync(dir)) {
    console.warn(`  ⚠ ${demo}: demo folder not found`);
    continue;
  }
  const ms = wait[demo] || wait.default;
  await shoot(page, `${base}/demos/${demo}/index.html`, join(dir, 'thumb.jpg'), demo, ms);
}

console.log('\nResponsive-Sektion (Desktop / Tablet / Mobile):');
for (const r of responsiveShots) {
  await shoot(page, `${base}${r.url}`, join(root, r.out), r.out, r.settle, {
    viewport: r.viewport,
    clip: r.clip,
    fullPage: r.fullPage,
  });
}

await browser.close();
if (serverHandle) serverHandle.server.close();

console.log('\n✅ Fertig. Du kannst die generierten JPGs jetzt committen.');
