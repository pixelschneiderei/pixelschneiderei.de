# AGENTS.md — Konventionen für KI-Agenten und neue Projekte

> Diese Datei wird von KI-Agenten (Claude, ChatGPT, Cursor etc.) **vor jeder Aufgabe gelesen**.
>
> Sie ist in zwei Teile gegliedert:
>
> - **TEIL A — Universell:** kopierbar 1:1 in jedes neue Projekt. Diese Konventionen wechseln nicht. Sie sichern DSGVO-Konformität, Performance, SEO und Konsistenz. Niemals löschen, nur ergänzen.
> - **TEIL B — Projekt-spezifisch:** alles was sich pro Kunde ändert — CI-Farben, Schriften, Branche, Adresse, Content. Diesen Teil bei jedem neuen Projekt komplett ersetzen.

---

# TEIL A — UNIVERSELLE REGELN (1:1 für jedes Projekt)

## A1. Hard Rules — niemals brechen

### A1.1 Keine externen Inhalte laden (DSGVO!)

Alles Externe wird **selbst gehostet**, keine Verbindungen zu Drittservern beim Aufruf der Seite:

- ❌ **Keine Google Fonts** via `https://fonts.googleapis.com/...`. Stattdessen `tools/download-fonts.mjs` ausführen → lokale `.woff2` in `assets/fonts/` + `assets/fonts.css` mit `@font-face`.
- ❌ **Kein Google Analytics**, Hotjar, Matomo (Cloud), Facebook-Pixel etc.
- ❌ **Keine CDN-eingebundenen JS-Bibliotheken** (jQuery from cdnjs, Tailwind Play CDN, etc.). JS und CSS lokal halten.
- ❌ **Keine Google Maps**. Stattdessen OpenStreetMap-Iframe (`openstreetmap.org/export/embed.html?...`) — datenschutzfreundlich, kein Cookie.
- ❌ **Keine YouTube-Embeds ohne nocookie**. Wenn Video nötig, dann `youtube-nocookie.com` mit Consent-Hinweis, oder lieber Selbst-Hosting.
- ❌ **Keine Webfonts-Loader** (Fontsource via CDN etc.) — alles lokal.

**Begründung:** LG-München-Urteil 2022 (Az. 3 O 17493/20) und folgende Abmahnwellen. IP-Übermittlung ohne Einwilligung ist DSGVO-Verstoß.

### A1.2 BILDER.md ist Pflicht

Jedes Bild-Platzhalter (`url('img/xyz.jpg')`, `<img src="...">`) muss in **`BILDER.md` dokumentiert** sein mit:

- Dateipfad
- Format (Aspect-Ratio + Empfehlung in Pixeln)
- Verwendung (welche Sektion / Funktion)
- Prompt für KI-Bildgeneratoren (auf Englisch — Midjourney/DALL-E/Flux funktionieren damit besser)
- Stil-Hinweis pro Demo / Sektion (konsistente Bildsprache)

**Audit-Befehl** (vor jedem Push):

```bash
grep -rhoE "url\('[^']+\.(jpg|jpeg|png|webp)'\)" *.html demos/*/index.html assets/*.css | sort -u
```

Jeder Treffer muss in BILDER.md auftauchen. Sonst nachtragen.

### A1.3 Fallback bei jedem Bild

```css
background:
  url('img/hero.jpg') center/cover no-repeat,
  linear-gradient(135deg, #colorA, #colorB);
```

Wenn das `.jpg` fehlt (404), fällt der Browser auf den Gradient zurück. **Site bricht nicht**, sieht nur etwas „flacher" aus. Genau so wollen wir das.

### A1.4 Demos sind `noindex`

Jede Demo (`demos/[name]/index.html`) hat:

```html
<meta name="robots" content="noindex, nofollow" />
```

Demos sind keine echten Auftritte — sie sollen Google nicht verwirren. Sie bleiben aber crawlbar (kein `Disallow: /demos/` in `robots.txt`), damit Social-Media-Bots `og:image` abrufen können.

### A1.5 Demo-Banner + Demo-Exit-Button auf jeder Demo

Oben ein farbiger Banner: `Demo · Branche: X — ← zur Pixelschneiderei`. Unten links ein fixierter **Demo-Verlassen-Button** (dunkler Pill mit Pfeil-links).

```html
<a class="demo-exit" href="../../referenzen.html">
  <svg .../><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
  Demo verlassen
</a>
```

**Wichtig:** Der statische `href` zeigt auf `../../referenzen.html` (nicht `index.html`!). Fallback für Direkt-Einsprünge — ohne Browser-Back-History soll der Klick auf die Referenzen-Übersicht führen, nicht auf die Startseite ganz oben.

Zusätzlich bindet **jede Demo** das Skript `assets/demo-exit.js` direkt vor `</body>` ein. Es ruft `history.back()` zur Herkunftsseite (inkl. Scroll-Position und Hash) auf, wenn der Besucher von der gleichen Domain kam — sonst greift der statische `href`.

```html
<script src="../../assets/demo-exit.js"></script>
</body>
```

### A1.6 Footer-Signatur „Mit Liebe geschneidert"

Auf **jeder öffentlichen Seite** (auch und gerade auf Kundenwebseiten) eine kleine Signatur — dezent, in Mono-Schrift, mit kleinem Nadel-und-Faden-SVG-Icon und Link auf `pixelschneiderei.de`:

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

**Auf Demo-Seiten** ist die Signatur **nicht nötig**, weil der Footer dort ohnehin „Demo · X ist ein fiktiver Beispielauftritt der Pixelschneiderei" trägt.

---

## A2. SEO + Social-Sharing — Pflicht für jede öffentliche Seite

### A2.1 Was muss rein, und warum

| Tag | Wirkung |
|---|---|
| `<title>` (~60 Zeichen, Keyword vorne) | Browser-Tab + Suchergebnis-Headline |
| `<meta name="description">` (~155 Zeichen) | Snippet unter dem Suchergebnis |
| `<meta name="keywords">` | Bonus-Signal für Bing, Yandex, DuckDuckGo (Google ignoriert) |
| `<link rel="canonical">` | verhindert Duplicate-Content-Probleme |
| `<meta name="robots">` mit `max-image-preview:large` | Google darf große OG-Bilder im Suchergebnis zeigen |
| `og:title` / `og:description` | wird in **WhatsApp, LinkedIn, Slack, Telegram, Signal, Discord** als Headline + Untertext gezeigt |
| `og:image` (1200×630, < 1 MB) | das große Vorschaubild beim Teilen |
| `og:image:width/height/alt` | Crawler kennen Layout sofort, Alt-Text für Accessibility |
| `og:type`, `og:url`, `og:locale` | Pflicht-Begleiter für vollständigen OG-Block |
| `twitter:card=summary_large_image` + `twitter:image` | Twitter/X braucht eigene Tags, sonst kleines Quadrat-Bild |
| JSON-LD strukturierte Daten | Rich Snippets in Google: Sterne, Breadcrumbs, FAQ-Akkordeon, LocalBusiness-Karte |

**Warum das alles?** Wenn jemand deine Seite in WhatsApp teilt, soll dort eine fette Vorschaukarte mit Bild + Headline + Beschreibung erscheinen — kein nackter Link. Genauso in LinkedIn, Slack-Channels, Discord-Servern. Ohne OG-Tags zeigen all diese Plattformen einen kahlen Link, das wirkt unprofessionell.

### A2.2 Copy-Paste-Template für jede neue öffentliche Seite

Folgenden Block am Anfang von `<head>` einfügen und die `{{Platzhalter}}` ersetzen:

```html
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />
<meta name="theme-color" content="#f5f1ec" />

<title>{{Titel mit Keyword vorne}} | Pixelschneiderei</title>
<meta name="description" content="{{~155 Zeichen, mit Ziel-Keywords}}" />
<meta name="keywords" content="{{komma-separierte Keywords}}" />
<meta name="author" content="Pixelschneiderei" />
<link rel="canonical" href="https://pixelschneiderei.de/{{seite}}.html" />
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1" />

<!-- Open Graph (WhatsApp / LinkedIn / Slack / Telegram / Discord / Signal) -->
<meta property="og:title" content="{{Titel}}" />
<meta property="og:description" content="{{~155 Zeichen Beschreibung}}" />
<meta property="og:type" content="website" />
<meta property="og:url" content="https://pixelschneiderei.de/{{seite}}.html" />
<meta property="og:image" content="https://pixelschneiderei.de/assets/og-{{seite}}.jpg" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta property="og:image:alt" content="{{kurze Bild-Beschreibung für Screenreader}}" />
<meta property="og:site_name" content="Pixelschneiderei" />
<meta property="og:locale" content="de_DE" />

<!-- Twitter / X -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{{Titel}}" />
<meta name="twitter:description" content="{{Beschreibung}}" />
<meta name="twitter:image" content="https://pixelschneiderei.de/assets/og-{{seite}}.jpg" />

<!-- Favicon + Apple Touch Icon -->
<link rel="icon" type="image/png" sizes="any" href="assets/ci/logo_light.png" />
<link rel="apple-touch-icon" href="assets/ci/logo_light.png" />

<link rel="stylesheet" href="assets/style.css" />
```

### A2.3 OG-Image-Spezifikation

| Spec | Wert |
|---|---|
| Format | JPEG (kleinere Dateigrösse als PNG) |
| Auflösung | **1200 × 630 px** (Facebook/LinkedIn/Twitter Standard) |
| Aspect-Ratio | 1.91:1 |
| Dateigrösse | < 1 MB (besser < 300 KB) |
| Farbraum | sRGB |
| URL | absolut (`https://...`), nicht relativ |
| Generator | `node tools/screenshots.mjs` automatisch |

WhatsApp, Apple Messages, Slack zeigen das Bild bei korrekten Tags fett über dem Text. Twitter/X braucht zwingend `twitter:card="summary_large_image"`.

### A2.4 JSON-LD strukturierte Daten — pro Seitentyp

| Seiten-Typ | Schema-Typ |
|---|---|
| Startseite | `Organization` + `LocalBusiness` + `WebSite` + ggf. `Service` |
| Service-/Premium-Seite | `Service` mit `provider` + `areaServed` |
| Lokale Landingpage | `LocalBusiness` mit `address`, `geo`, `areaServed` |
| Branchen-Landingpage | `Service` mit `audience` (`Audience.audienceType`) |
| Übersichtsseite (Referenzen, Komponenten) | `CollectionPage` + `BreadcrumbList` |
| FAQ-Sektion | `FAQPage` mit `mainEntity[]` (jede Frage als `Question`/`Answer`-Paar) — **WICHTIG**: Frage muss sowohl im DOM (`<details>`) als auch im JSON-LD vorhanden sein, sonst kein Rich Snippet |
| Legal-Seiten (Impressum, Datenschutz) | `WebPage` mit `about`-Property |
| Blog-Artikel (falls Blog) | `Article` oder `BlogPosting` mit `author`, `datePublished` |

### A2.5 Crawler-Konfiguration

**`robots.txt`** explicit `User-agent`-Blöcke für:
- Suchmaschinen: `Googlebot`, `Bingbot`, `DuckDuckBot`, `Slurp`
- KI-Crawler (alle erlaubt!): `GPTBot`, `ChatGPT-User`, `OAI-SearchBot`, `ClaudeBot`, `anthropic-ai`, `Claude-Web`, `PerplexityBot`, `Perplexity-User`, `Google-Extended`, `Applebot-Extended`, `CCBot`, `Bytespider`, `Amazonbot`, `Meta-ExternalAgent`, `cohere-ai`, `Diffbot`, `YouBot`, `MistralAI-User`

**`sitemap.xml`** mit allen indexierbaren Seiten + `<changefreq>` + `<priority>`. Demos NICHT in die Sitemap aufnehmen (sind noindex).

**`llms.txt`** im Root als markdown-Wegweiser für KI-Assistenten (neuer offener Standard, z. B. von Anthropic dokumentiert). Inhalt: kurzer Site-Kontext, was die Firma macht, wichtigste Seiten als Liste.

### A2.6 Verifikation vor Live-Schaltung

- [ ] Lighthouse > 95 (Performance, Accessibility, Best Practices, SEO)
- [ ] Test in [opengraph.xyz](https://www.opengraph.xyz/) — wie sehen Vorschauen aus?
- [ ] Twitter-Card-Validator: card-validator.twitter.com
- [ ] Google Rich Results Test: search.google.com/test/rich-results
- [ ] Schema.org Validator: validator.schema.org
- [ ] WhatsApp Sharing-Test: Link an sich selbst senden, prüfen ob Bild + Titel + Beschreibung gezogen werden

---

## A3. Soft Rules — kann angepasst werden, aber begründen

### Voice & Tonalität (Baseline)

- Sprache und Anrede projekt-spezifisch (Teil B), aber generell: ehrlich, warm, kein Marketing-Geschwätz
- Kursive Hervorhebungen mit `<em>` und Accent-Farbe
- Halbsätze und kurze Pointen statt Floskel-Marathons
- Ehrliche Disclaimer wo nötig („wir sind keine Anwält:innen")
- Keine Fake-Testimonials. Wenn welche, dann anonymisiert mit Cite

### Typografie-Prinzipien

- **Serif-Display** für Headlines + emotionale Akzente
- **Sans-Serif** für Fließtext + UI
- **Mono** für Eyebrows, Labels, Tags, Code
- Variable Fonts bevorzugen (eine Datei statt vieler Gewichte)
- Italics für emotionale Akzente, fett **niemals** für „Drücken Sie hier!"

### Layout

- Mobile-first, Container max ~1180&nbsp;px
- Großzügiger Whitespace, klare Hierarchie
- Kein Wall-of-Cards — Sektionen mit unterschiedlichem Rhythmus
- **Gerade Reihen-Anzahlen** in Grids: 2/3/4/6 — nie eine letzte Reihe mit weniger Items als die vorherigen
- `clamp()` für fluide Typografie

### CSS

- **Vanilla CSS**, kein Tailwind, kein PostCSS-Build
- Custom Properties (`--paper`, `--ink`, `--thread` …) für Theming
- Geteiltes `assets/style.css` für Hauptseiten, demo-spezifische Styles inline in der jeweiligen Demo
- `@import url('fonts.css')` ganz oben in `style.css` — wird vom Font-Skript erzeugt

---

## A4. Sicherheit & Hosting-Standard

- **Statisch, wo immer möglich** — kein WordPress, kein dynamisches CMS
- **Auto-Backup** (Cloudflare Pages Preview-Branches oder Git-Snapshots)
- **Cloudflare** o.&nbsp;ä. für DDoS / CDN
- Eigenes CMS, falls dynamisch nötig — minimal-dynamische „Inseln", restliche Site bleibt statisch
- HTTPS erzwungen (HSTS-Header)
- Cache-Header: `.woff2` und Bilder = 1 Jahr

---

## A5. Datei-Struktur

```
projektroot/
├── index.html                    # Startseite
├── referenzen.html               # Demos-Übersicht (falls vorhanden)
├── komponenten.html              # UI-Bausteine (falls Showcase)
├── impressum.html
├── datenschutz.html
├── webdesign-X.html              # Lokale/Branchen-Landingpages
├── sitemap.xml
├── robots.txt
├── llms.txt                      # KI-Crawler-Wegweiser
├── README.md
├── BILDER.md                     # Bild-Manifest (Pflicht!)
├── AGENTS.md                     # Diese Datei
├── assets/
│   ├── style.css                 # Geteiltes Stylesheet
│   ├── site.js                   # Geteiltes JS (Nav, Reveal-Animationen)
│   ├── demo-exit.js              # JS für Demo-Verlassen-Button
│   ├── fonts.css                 # AUTO: von download-fonts.mjs erzeugt
│   ├── fonts/                    # AUTO: lokale .woff2-Dateien
│   ├── ci/                       # CI-Logos und Brand-Assets
│   ├── og-*.jpg                  # Open-Graph 1200×630
│   └── img/                      # Globale Bilder
└── demos/
    └── [name]/
        ├── index.html            # noindex Demo
        ├── thumb.jpg             # 1200×750 (von screenshots.mjs)
        └── img/                  # Demo-spezifische Bilder
```

---

## A6. Pflicht-Tools im `tools/`-Ordner

### `tools/download-fonts.mjs`

Lädt Google-Fonts woff2-Dateien lokal. Pflicht-Aufruf bei Setup oder neuer Schrift:

```bash
node tools/download-fonts.mjs
```

Liefert `assets/fonts/*.woff2` und `assets/fonts.css` mit `@font-face`-Deklarationen.

### `tools/screenshots.mjs`

Generiert `thumb.jpg` (1200×750 für Demo-Cards), `og-*.jpg` (1200×630 für Social-Sharing) und `responsive-{desktop,tablet,mobile}.jpg` für die Device-Frames. Self-hosted Server, einzeiliger Aufruf:

```bash
node tools/screenshots.mjs
```

### `package.json` Scripts (optional)

```json
{
  "scripts": {
    "fonts": "node tools/download-fonts.mjs",
    "thumbs": "node tools/screenshots.mjs",
    "serve": "npx http-server -p 8080"
  }
}
```

---

## A7. Anti-Patterns — niemals tun

- ❌ Google Fonts via CDN einbinden
- ❌ Cookie-Banner für Funktionen, die wir gar nicht brauchen
- ❌ „Akzeptiere alle Cookies"-Modal über die ganze Seite
- ❌ DSGVO-Generator-Texte 1:1 reinkopieren ohne Anpassung an die *tatsächliche* Datenverarbeitung
- ❌ Stockfotos von „diverse business team"-Klischees
- ❌ Versprechen, die wir nicht halten können („100&nbsp;% rechtssicher", „garantierte Top-1-Platzierung")
- ❌ Bullet-Listen, die mit „Bei uns ist Qualität immer..." anfangen
- ❌ Karussells als Hero
- ❌ „Geheim­tipps" oder „Hot Right Now"-Sticker
- ❌ Pop-Ups beim Verlassen, Newsletter-Modals nach 5&nbsp;Sekunden
- ❌ Auto-Play-Videos mit Sound

---

## A8. Häufige Aufgaben — Quick Reference

### Neue Demo hinzufügen

1. Ordner `demos/[name]/` anlegen
2. `index.html` aus existierender Demo kopieren, anpassen
3. `<meta name="robots" content="noindex, nofollow" />` sicherstellen
4. Demo-Banner + Demo-Exit-Button + `assets/demo-exit.js`-Script einbauen
5. Bild-Hooks mit Gradient-Fallback verwenden
6. In `BILDER.md` neuen Abschnitt anlegen
7. In `referenzen.html` neue Karte einfügen
8. In `index.html` Industries-Strip ggf. erweitern (gerade Anzahl behalten!)
9. `tools/screenshots.mjs` um neue Demo erweitern, einmal laufen lassen

### Neue lokale/Branchen-Landingpage

1. `webdesign-[stadt].html` oder `webseite-[branche]-[region].html`
2. Vom Template kopieren, anpassen: Title, Description, Keywords, Hero-Text, JSON-LD `areaServed`
3. `<meta name="robots" content="index, follow" />` (im Gegensatz zu Demos)
4. In `sitemap.xml` eintragen
5. Cross-Links zu anderen Landingpages am Ende
6. Eigenes `og-*.jpg` in `tools/screenshots.mjs` ergänzen

### Neue FAQ-Frage

1. In Hauptseite als `<details><summary>…</summary><div class="faq-body">…</div></details>` einbauen
2. **Auch in das `FAQPage`-JSON-LD-Schema** als `Question`/`Answer`-Paar einfügen — sonst kein Rich Snippet bei Google

### Neue Schrift verwenden

1. In `tools/download-fonts.mjs` die `fonts`-Liste erweitern
2. `node tools/download-fonts.mjs` neu laufen lassen
3. `font-family` in `style.css` (Variable) referenzieren
4. `datenschutz.html` Schriftarten-Liste aktualisieren

### Bild ergänzt werden soll

1. Pfad in HTML/CSS einfügen mit Gradient-Fallback
2. **`BILDER.md` aktualisieren** (Datei, Format, Verwendung, Prompt)
3. Bild physisch nach `assets/img/...` oder `demos/[name]/img/` legen

---

## A9. Beim Übergeben an Kunden

- [ ] `node tools/download-fonts.mjs` einmal gelaufen, `assets/fonts/` befüllt
- [ ] `node tools/screenshots.mjs` einmal gelaufen, alle `thumb.jpg` + `og-*.jpg` vorhanden
- [ ] BILDER.md vollständig (Audit via grep)
- [ ] Alle Bilder, die der Kunde wollte, eingebaut
- [ ] `sitemap.xml` mit allen Pages
- [ ] `robots.txt` und `llms.txt` korrekt
- [ ] DSGVO im `datenschutz.html` zur **tatsächlichen** Datenverarbeitung passend
- [ ] Kontakt-Mailadresse + Impressum-Daten korrekt
- [ ] og:image-Pfade absolut auf Live-Domain (nicht relativ)
- [ ] Cache-Header für `.woff2` und Bilder (1 Jahr) auf Hoster eingerichtet
- [ ] DNS sauber: A/AAAA, MX falls Mail dazu, TXT (SPF/DKIM/DMARC) falls Versand
- [ ] HTTPS erzwungen (HSTS-Header)
- [ ] Footer-Signatur „Mit Liebe geschneidert @ pixelschneiderei.de" steht drin
- [ ] Test: Lighthouse > 95, PageSpeed > 90, Datenschutz-Scanner grün

---

# TEIL B — PROJEKT-SPEZIFISCH (pro Kunde anpassen)

> Dieser Teil beschreibt die Pixelschneiderei selbst und dient als ausgefülltes Beispiel.
> Bei einem neuen Kunden-Projekt: kompletten Teil B durch die jeweiligen Werte ersetzen.

## B1. Marken-Identität

### CI-Farben

```css
--paper:     #f5f1ec   /* Cream-Hintergrund */
--ink:       #1a1a1a   /* Schwarz */
--thread:    #b1383a   /* Pixelschneider-Rot (RGB 177, 56, 58) */
--muted:     #a0a0a0   /* Mid-Grey, Sekundär-Text */
--line:      #d9d9d9   /* Trennlinien */
--thread-2:  #c85a5c   /* Hover-Akzent (heller Rot) */
--thread-3:  #f2d8d9   /* Tinted Background */
```

Quelle: Brand-Board und Logo-Sample. Demo-Pages haben **eigene Farb-Systeme** (Holzgeist=Holzbraun, Aurora=Korallrot etc.) — bewusst Diversität, weil Demos fiktive Kunden zeigen.

### Schriften

- **Serif Display:** Fraunces (variable, opsz 9–144, weight 300–700, SOFT 30–100)
- **Sans:** Inter (300/400/500/600/700)
- **Mono:** JetBrains Mono (400/500)
- **Script:** Allura — *nur* für die Wortmark „schneiderei" im Logo-Schriftzug

### Voice

- Deutsch, „Sie"-Anrede
- Schneider-Metaphorik: „maßgeschneidert", „Schnitt", „Naht", „Stoff", „verarbeitet"
- Schneider-Rot als emotionaler Italic-Akzent (`color: var(--thread); font-style: italic;`)
- Tagline: **„Mit Liebe geschneidert @ pixelschneiderei.de"** im Footer

### Logo

- Volle Wortmarke + Icon: `assets/logo.svg`
- Icon-only (Laptop+Nadel+Faden) als Header- und Footer-Brand: `assets/ci/logo_light.png`
- Wortmarke neben Icon: CSS-Text in Fraunces („pixel" schwarz) + Allura-Italic („schneiderei" rot)
- Schreibweise im Brand-Mark **lowercase**: `pixelschneiderei` (matcht Domain)
- Schreibweise im Body-Text und SEO: `Pixelschneiderei` (Eigenname)

---

## B2. Auftraggeber-Daten

```
Erik Weisser
Pixelschneiderei (Einzelunternehmen)
Am Hang 1
96486 Lautertal
Deutschland

E-Mail:  erik@weisser.dev
Web:     https://pixelschneiderei.de/
USt-Id:  Kleinunternehmer (§ 19 UStG)

Geo:     50.2935° N, 10.9925° E
Region:  Bayern, Oberfranken, Landkreis Coburg
```

Erscheint in: Impressum, Datenschutz, JSON-LD `LocalBusiness` aller Hauptseiten, Footer-Kontakt.

---

## B3. Service-Modell

**Drei Webseiten-Pakete** (Preis-Anker auf `leistungen.html`, konkretes Angebot im Erstgespräch):

- **Starter** (One-Pager, kein Formular, mailto/tel) — ab 875 € + ab 75 €/Jahr Service → Jahr 1 ab 1.000 €
- **Standard** (Multi-Page, 2-4 Detail-Seiten, Formular) — ab 1.875 € + ab 175 €/Jahr Service → Jahr 1 ab 2.100 €
- **Premium** (alles + Karriere/Galerie/SEO/Karte) — ab 2.700 € + ab 250 €/Jahr Service → Jahr 1 ab 3.000 €

**Drei Service-Pakete** (jährlich, beidseitig kündbar, Teilerstattung bei vorzeitigem Ende):

- **Budget** — 75 €/Jahr (3 Module: Rechtstexte-Check + SSL/Uptime + Sicherheits-Header)
- **Basis** — 175 €/Jahr (7 Module + Bewertungen, Feiertage, Formular-Pflege, 2× Inhaltsupdate)
- **All-Inc** — 250 €/Jahr (alle 12 Module + SEO, Bewerbungsformular, Bildpflege, Karriere-Anzeigen, DNS-Wartung, 4× Inhaltsupdate). Bundle-Ersparnis 50 € vs. à-la-carte.

**12 Service-Module einzeln zubuchbar** à 25 €/Jahr — Liste vollständig auf `leistungen.html`.

**13 Bausteine zubuchbar** (einmalig, je 25-150 €): Kontaktformular, Bewertungs-Slider, Click-to-Load, Content-Modal, Bild-Optimierung, Extraseite, Produktseite, Karriereseite, WhatsApp-CTA, „Heute geöffnet"-Logik, Initiale Einrichtung Basic/Premium, SEO-Tuning.

**Förderprogramme** (für Bayern explizit erwähnt):
- Bayerischer Digitalbonus
- KfW-Programme
- IHK-Förderung
- Wir sind keine Förder-Berater — wir nennen passende Programme, ausfüllen muss der Kunde selbst.

---

## B4. Content-Struktur

### Hauptseiten (alle `index, follow`)

| Datei | Zweck |
|---|---|
| `index.html` | Startseite — Hero, Leistungen, Pakete, Bausteine, Vorteile, Responsive-Showcase, Referenzen, Prozess, FAQ, Kontakt |
| `leistungen.html` | Vergleichstabellen aller Web-/Service-Pakete + Bausteine-Galerie + Empfehlungs-FAQ + Preis-Anker |
| `referenzen.html` | 12 Branchen-Demos mit Filter |
| `komponenten.html` | UI-Bausteine: Forms, CTAs, Galerien, Audio, Karten, FAQ |
| `premium-webdesign.html` | Hochglanz-Landingpage (dunkler Hero) |
| `webdesign-coburg.html` | Lokal Coburg + Umgebung |
| `webdesign-oberfranken.html` | Regional Oberfranken |
| `webdesign-bayern.html` | Bayern + Förderung |
| `webseite-handwerker-bayern.html` | Branchen-Landingpage Handwerk |
| `impressum.html`, `datenschutz.html`, `agb.html` | Rechtliches |

### Demos (alle `noindex, nofollow`)

12 fiktive Branchen-Beispiele unter `demos/[name]/`:

| Demo | Branche | Stil |
|---|---|---|
| `atelier` | Pixelschneiderei selbst (Hochglanz) | Apple-style dunkel |
| `holzgeist` | Tischlerei | Warm, Holz, Cormorant |
| `aurora` | Café | Coral, DM Serif |
| `atmen` | Yoga | Editorial Moss-Green |
| `arztpraxis` | Hausarzt | Klinisch Blau |
| `laden` | Schreibwarengeschäft | Rust + Fraunces |
| `akademie` | Online-Kurse | Royal Blue Editorial |
| `kanzlei` | Rechtsanwälte | Navy + Gold |
| `lichtblick` | Fotografie (Hochzeit) | Champagne Editorial |
| `nachtschicht` | DJ & Producer | Synthwave Pink/Cyan |
| `kontur` | Magazin / Blog | Newspaper Style |

### Pflicht-Sektionen auf Startseite

1. Hero (Headline + Lede + CTAs + Pixel-Stitching-Animation)
2. Industries-Strip (Branchen-Chips, **gerade Anzahl** halten — aktuell 12)
3. Why-Pull (Schneider-Metapher, Pull-Quote)
4. Leistungen
5. Pakete (Hobby/Standard/Premium ohne Preise)
6. Bausteine (Add-ons)
7. Vorteile (3-Karten-Grid + „Ein ehrliches Wort zum Schluss"-Block)
8. FAQ (mind. 10 Einträge, alle mit JSON-LD-Pendant — inkl. „Nutzen Sie KI?")
9. Responsive-Showcase (Desktop / Tablet / Mobile Device-Frames)
10. Referenzen-Strip (3 Highlights mit „Alle Referenzen ansehen"-Link)
11. Prozess (Schritte vom Erstgespräch zur Live-Schaltung)
12. Kontakt (E-Mail, OpenStreetMap-Iframe)

---

## B5. KI-Position

Wir nutzen KI als Werkzeug, nicht als Ersatz. Eigene FAQ-Frage „Nutzen Sie KI beim Bauen?" mit Werkzeug-Analogie (stärkster Akkuschrauber, schärfste Säge, modernste Kamera, fähigste KI — ohne Können kein Meisterstück). Wichtig: ehrlich kommunizieren, nicht verstecken, aber auch nicht überbetonen.

---

## Ende

Für **kunden-spezifische Abweichungen** von Teil A: am Anfang dieses Teil-B-Blocks einen Abschnitt `## B0. Abweichungen von Universal-Konventionen` einfügen — **mit Begründung**, sodass auch der Kunde versteht, warum hier von der Norm abgewichen wurde.
