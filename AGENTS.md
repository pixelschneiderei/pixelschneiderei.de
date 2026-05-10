# AGENTS.md — Konventionen für KI-Agenten und neue Projekte

> Diese Datei wird von KI-Agenten (Claude, ChatGPT, Cursor etc.) **vor jeder Aufgabe gelesen**. Sie kodifiziert die Pixelschneiderei-Konventionen, damit alle künftigen Kunden-Webseiten **konsistent gebaut** werden — DSGVO-konform, eigenständig, sauber strukturiert.
>
> **Diese Datei in jedes neue Projekt kopieren.** Kunden-spezifische Anpassungen am Anfang dokumentieren.

---

## Hard Rules — niemals brechen

### 1. Keine externen Inhalte laden (DSGVO!)

Alles Externe wird **selbst gehostet**, keine Verbindungen zu Drittservern beim Aufruf der Seite:

- ❌ **Keine Google Fonts** via `https://fonts.googleapis.com/...`. Stattdessen `tools/download-fonts.mjs` ausführen → lokale `.woff2` in `assets/fonts/` + `assets/fonts.css` mit `@font-face`.
- ❌ **Kein Google Analytics**, Hotjar, Matomo (Cloud), Facebook-Pixel etc.
- ❌ **Keine CDN-eingebundenen JS-Bibliotheken** (jQuery from cdnjs, Tailwind Play CDN, etc.). JS und CSS lokal halten.
- ❌ **Keine Google Maps**. Stattdessen OpenStreetMap-Iframe (`openstreetmap.org/export/embed.html?...`) — datenschutzfreundlich, kein Cookie.
- ❌ **Keine YouTube-Embeds ohne nocookie**. Wenn Video nötig, dann `youtube-nocookie.com` mit Consent-Hinweis, oder lieber Selbst-Hosting.
- ❌ **Keine Webfonts-Loader** (Fontsource via CDN etc.) — alles lokal.

**Begründung:** LG-München-Urteil 2022 (Az. 3 O 17493/20) und folgende Abmahnwellen. IP-Übermittlung ohne Einwilligung ist DSGVO-Verstoß.

### 2. BILDER.md ist Pflicht

Jedes Bild-Platzhalter (`url('img/xyz.jpg')`, `<img src="...">`) muss in **`BILDER.md` dokumentiert** sein mit:

- Dateipfad
- Format (Aspect-Ratio + Empfehlung in Pixeln)
- Verwendung (welche Sektion / Funktion)
- Prompt für KI-Bildgeneratoren (auf Englisch — Midjourney/DALL-E/Flux funktionieren damit besser)
- Stil-Hinweis pro Demo (konsistente Bildsprache)

**Audit-Befehl** (vor jedem Push):

```bash
# Alle url('img/...')-Referenzen finden:
grep -rhoE "url\('[^']+\.(jpg|jpeg|png|webp)'\)" *.html demos/*/index.html assets/*.css | sort -u
```

Jeder Treffer muss in BILDER.md auftauchen. Sonst nachtragen.

### 3. Fallback bei jedem Bild

```css
background:
  url('img/hero.jpg') center/cover no-repeat,
  linear-gradient(135deg, #colorA, #colorB);
```

Wenn das `.jpg` fehlt (404), fällt der Browser auf den Gradient zurück. **Site bricht nicht**, sieht nur etwas „flacher" aus. Genau so wollen wir das.

### 4. Demos sind `noindex`

Jede Demo (`demos/[name]/index.html`) hat:

```html
<meta name="robots" content="noindex, nofollow" />
```

Demos sind keine echten Auftritte — sie sollen Google nicht verwirren. Sie bleiben aber crawlbar (kein `Disallow: /demos/` in `robots.txt`), damit Social-Media-Bots `og:image` abrufen können.

### 5. Demo-Banner + Demo-Exit-Button auf jeder Demo

Oben ein farbiger Banner: `Demo · Branche: X — ← zur Pixelschneiderei`. Unten links ein fixierter **Demo-Verlassen-Button** (dunkler Pill mit Pfeil-links). **Nicht versteckt machen**, das sind unsere Beispiele, nicht die Sites unserer Kunden.

```html
<a class="demo-exit" href="../../referenzen.html">
  <svg .../><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
  Demo verlassen
</a>
```

**Wichtig:** Der statische `href` zeigt auf `../../referenzen.html` (nicht auf `index.html`!). Das ist der Fallback für Direkt-Einsprünge — wenn jemand aus einem Google-Treffer oder einem Link in eine Demo kommt und keine Browser-Back-History hat, soll der „Demo verlassen"-Button auf die Referenzen-Übersicht führen, nicht auf die Startseite ganz oben.

Zusätzlich bindet **jede Demo** das Skript `assets/demo-exit.js` direkt vor `</body>` ein. Es lässt den Button per `history.back()` zur Herkunftsseite (inkl. Scroll-Position und Hash, z.&nbsp;B. zurück nach `#referenzen`) springen, wenn der Besucher von der gleichen Domain kam — sonst bleibt der statische `href` (Referenzen) als Fallback.

```html
<script src="../../assets/demo-exit.js"></script>
</body>
```

### 6. Footer-Signatur „Mit Liebe geschneidert"

Auf **jeder öffentlichen Seite** (auch und gerade auf Kundenwebseiten) gehört unten eine kleine Signatur — dezent, in Mono-Schrift, mit kleinem Nadel-und-Faden-SVG-Icon und Link auf `pixelschneiderei.de`. Nicht aufdringlich, aber sichtbar.

```html
<span class="foot-signature">
  <svg viewBox="0 0 24 24" width="14" height="14" fill="none"
       stroke="currentColor" stroke-width="1.4"
       stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <line x1="6" y1="18" x2="18" y2="6"/>
    <circle cx="17" cy="7" r="1.4"/>
    <path d="M15.5 6.5C13 5 10.5 6.5 11 9.5"/>
  </svg>
  Mit Liebe geschneidert @ <a href="https://pixelschneiderei.de/">pixelschneiderei.de</a>
</span>
```

Styling siehe `assets/style.css` → `.foot-signature` (inline-flex mit 8px gap, Icon in Schneider-Rot, Link mit gepunkteter Underline).

**Auf Demo-Seiten** ist die Signatur **nicht nötig**, weil der Footer dort ohnehin den expliziten Hinweis trägt: „Demo · X ist ein fiktiver Beispielauftritt der Pixelschneiderei". Doppelte Credits vermeiden.

---

## Soft Rules — kann angepasst werden, aber begründen

### Voice & Tonalität

- **Deutsch**, „Sie"-Anrede, ehrlich, warm, kein Marketing-Geschwätz
- Kursive Hervorhebungen mit `<em>` und Accent-Farbe (z.&nbsp;B. Schneider-Rot `#b8392a`)
- Halbsätze und kurze Pointen statt Floskel-Marathons
- **Ehrliche Disclaimer** wo nötig: „Wir sind keine Anwält:innen", „Wir sind keine Förder-Berater"
- Keine Fake-Testimonials. Wenn welche, dann anonymisiert und mit Cite

### Typografie

- **Serif-Display** (z.&nbsp;B. Fraunces, Cormorant, DM Serif) für Headlines + emotionale Akzente
- **Sans-Serif** (Inter o.&nbsp;ä.) für Fließtext + UI
- **Mono** (JetBrains Mono o.&nbsp;ä.) für Eyebrows, Labels, Tags, Code
- Variable Fonts bevorzugen (eine Datei statt vieler Gewichte)
- Italics für emotionale Akzente, fett **niemals** für „Drücken Sie hier!" — wirkt aufdringlich

### Layout

- Mobile-first, Container max ~1180&nbsp;px
- Großzügige Whitespace, klare Hierarchie
- Kein Wall-of-Cards — Sektionen mit unterschiedlichem Rhythmus
- **Gerade Reihen-Anzahlen** in Grids: 2/3/4/6 — nie eine letzte Reihe mit weniger Items als die vorherigen
- `clamp()` für fluide Typografie

### CSS

- **Vanilla CSS**, kein Tailwind, kein PostCSS-Build
- Custom Properties (`--paper`, `--ink`, `--thread` …) für Theming
- Geteiltes `assets/style.css` für Hauptseiten, demo-spezifische Styles inline in der jeweiligen Demo
- `@import url('fonts.css')` ganz oben in `style.css` — wird vom Font-Skript erzeugt

---

## SEO — Pflicht für jede öffentliche Seite

Jede Seite (außer Demos) hat:

- ✅ `<title>` mit Keyword vorne (~60 Zeichen)
- ✅ `<meta name="description">` (~155 Zeichen, mit Ziel-Keywords)
- ✅ `<meta name="keywords">` (auch wenn Google es ignoriert — andere Suchmaschinen lesen es noch)
- ✅ `<link rel="canonical">`
- ✅ Open Graph: `og:title`, `og:description`, `og:type`, `og:url`, `og:image` (1200×630), `og:image:width/height`, `og:locale`
- ✅ Twitter Card: `twitter:card="summary_large_image"`, `twitter:image`
- ✅ JSON-LD strukturierte Daten — mindestens `Organization` + `LocalBusiness` auf der Hauptseite, `Service` auf Service-Seiten, `FAQPage` falls FAQ vorhanden
- ✅ `sitemap.xml` im Root, `robots.txt` mit `Sitemap:`-Verweis
- ✅ Lokale Landingpages für Branchen + Regionen (z.&nbsp;B. `webdesign-coburg.html`, `webseite-handwerker-bayern.html`) — jede mit eigenem JSON-LD und `areaServed`

---

## Sicherheit & Hosting-Standard

- **Statisch, wo immer möglich** — kein WordPress, kein dynamisches CMS außer eigenes leichtgewichtiges
- **Auto-Backup** (z.&nbsp;B. via Cloudflare Pages Preview-Branches oder Git-Snapshots)
- **Cloudflare oder vergleichbar** für DDoS / CDN
- Eigenes CMS, falls dynamisch nötig — minimal-dynamische „Inseln", restliche Site bleibt statisch
- **Keine Wartungsverträge** mit versteckten Abos. Service-Pakete werden transparent als jährlicher Posten benannt

---

## Datei-Struktur

```
projektroot/
├── index.html                    # Startseite
├── referenzen.html               # Demos-Übersicht (falls vorhanden)
├── komponenten.html              # UI-Bausteine
├── impressum.html
├── datenschutz.html
├── webdesign-X.html              # Lokale/Branchen-Landingpages
├── sitemap.xml
├── robots.txt
├── README.md
├── BILDER.md                     # Bild-Manifest (Pflicht!)
├── AGENTS.md                     # Diese Datei
├── assets/
│   ├── style.css                 # Geteiltes Stylesheet
│   ├── site.js                   # Geteiltes JS (Nav, Reveal-Animationen)
│   ├── fonts.css                 # AUTO: von download-fonts.mjs erzeugt
│   ├── fonts/                    # AUTO: lokale .woff2-Dateien
│   │   ├── inter-01.woff2
│   │   └── ...
│   ├── og-home.jpg               # Open-Graph 1200×630
│   ├── og-referenzen.jpg
│   └── img/                      # Globale Bilder
│       └── komponenten/          # Bilder für Komponenten-Schau
└── demos/
    └── [name]/
        ├── index.html            # noindex Demo
        ├── thumb.jpg             # 1200×630 (von screenshots.mjs)
        └── img/                  # Demo-spezifische Bilder
```

---

## Pflicht-Tools im `tools/`-Ordner

Jedes Projekt bekommt drei Helper-Skripte:

### `tools/download-fonts.mjs`

Lädt Google-Fonts woff2-Dateien lokal. Pflicht-Aufruf bei Setup:

```bash
node tools/download-fonts.mjs
```

Liefert:
- `assets/fonts/*.woff2`
- `assets/fonts.css` mit `@font-face`-Deklarationen

### `tools/screenshots.mjs`

Generiert `thumb.jpg` (1200×630, Open-Graph-Standard) für jede Demo + die 3 Hauptseiten via Puppeteer. Aufruf:

```bash
npx http-server -p 8080
node tools/screenshots.mjs --base http://localhost:8080
```

Liefert:
- `demos/[name]/thumb.jpg`
- `assets/og-home.jpg`, `assets/og-referenzen.jpg`, `assets/og-komponenten.jpg`

### `package.json` Scripts (optional)

```json
{
  "scripts": {
    "fonts": "node tools/download-fonts.mjs",
    "thumbs": "node tools/screenshots.mjs --base http://localhost:8080",
    "serve": "npx http-server -p 8080"
  }
}
```

---

## Anti-Patterns — niemals tun

- ❌ Google Fonts via CDN einbinden
- ❌ Cookie-Banner für Funktionen, die wir gar nicht brauchen (kein Tracking = kein Banner nötig)
- ❌ „Akzeptiere alle Cookies"-Modal über die ganze Seite legen
- ❌ DSGVO-Generator-Texte 1:1 reinkopieren ohne Anpassung an die *tatsächliche* Datenverarbeitung
- ❌ Stockfotos von „diverse business team"-Klischees
- ❌ Versprechen, die wir nicht halten können („100 % rechtssicher", „garantierte Top-1-Platzierung in Google")
- ❌ Bullet-Listen, die mit „Bei uns ist Qualität immer..." anfangen
- ❌ Karussells als Hero (User scrollt eh durch)
- ❌ „Geheim­tipps" oder „Hot Right Now"-Sticker
- ❌ Pop-Ups beim Verlassen, Newsletter-Modals nach 5 Sekunden
- ❌ Auto-Play-Videos mit Sound

---

## Häufige Aufgaben — Quick Reference

### Neue Demo hinzufügen

1. Ordner `demos/[name]/` anlegen
2. `index.html` aus existierender Demo kopieren, anpassen
3. **`<meta name="robots" content="noindex, nofollow" />`** sicherstellen
4. **Demo-Banner + Demo-Exit-Button** einbauen
5. Bild-Hooks mit Gradient-Fallback verwenden
6. In `BILDER.md` neuen Abschnitt anlegen (Pfade + Prompts)
7. In `referenzen.html` neue Karte einfügen
8. In `index.html` Industries-Strip ggf. erweitern (immer **gerade Anzahl** behalten)
9. `tools/screenshots.mjs` um neue Demo erweitern, einmal laufen lassen → `thumb.jpg`

### Neue lokale/Branchen-Landingpage

1. `webdesign-[stadt].html` oder `webseite-[branche]-[region].html`
2. Vom Template `webdesign-coburg.html` kopieren
3. Anpassen: Title, Description, Keywords, Hero-Text, JSON-LD `areaServed`
4. **`<meta name="robots" content="index, follow" />`** (im Gegensatz zu Demos)
5. In `sitemap.xml` eintragen
6. Cross-Links zu anderen Landingpages am Ende

### Neue FAQ-Frage

1. In `index.html` als `<details><summary>…</summary><div class="faq-body">…</div></details>` einbauen
2. **Auch in das `FAQPage`-JSON-LD-Schema** als `Question`/`Answer`-Paar einfügen — sonst kein Rich Snippet bei Google

### Neue Schrift verwenden

1. In `tools/download-fonts.mjs` die `fonts`-Liste erweitern
2. `node tools/download-fonts.mjs` neu laufen lassen
3. `font-family` in `style.css` (Variable) referenzieren

### Bild ergänzt werden soll

1. Pfad in HTML/CSS einfügen mit Gradient-Fallback
2. **`BILDER.md` aktualisieren** (Datei, Format, Verwendung, Prompt)
3. Bild physisch nach `assets/img/...` oder `demos/[name]/img/` legen

---

## Beim Übergeben an Kunden

Checkliste:
- [ ] `node tools/download-fonts.mjs` einmal gelaufen, `assets/fonts/` befüllt
- [ ] `node tools/screenshots.mjs` einmal gelaufen, alle `thumb.jpg` + `og-*.jpg` vorhanden
- [ ] BILDER.md vollständig (Audit via grep)
- [ ] Alle Bilder, die der Kunde wollte, eingebaut
- [ ] `sitemap.xml` mit allen Pages
- [ ] `robots.txt` korrekt
- [ ] DSGVO im `datenschutz.html` zur **tatsächlichen** Datenverarbeitung passend (nicht generisch)
- [ ] Kontakt-Mailadresse + Impressum-Daten korrekt
- [ ] og:image Pfade absolut auf der Live-Domain (nicht relativ — viele Social-Crawler verstehen relativ schlecht)
- [ ] Cache-Header für `.woff2` und Bilder (1 Jahr) auf dem Hoster eingerichtet
- [ ] DNS sauber: A/AAAA, MX falls Mail dazu, TXT (SPF/DKIM/DMARC) falls Versand
- [ ] HTTPS erzwungen (HSTS-Header)
- [ ] Test: lighthouse > 95, PageSpeed > 90, Datenschutz-Scanner gibt grünes Licht

---

## Ende

Für **Kunden-spezifische Abweichungen** dieser Konventionen: am Anfang dieser Datei in einem neuen Abschnitt `## Projekt-spezifische Abweichungen` dokumentieren — **mit Begründung**, sodass auch der Kunde versteht, warum wir hier von der Norm abgewichen sind.
