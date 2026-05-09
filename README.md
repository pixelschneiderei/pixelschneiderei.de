# pixelschneiderei.de

Quellcode der Webseite [pixelschneiderei.de](https://pixelschneiderei.de) – maßgeschneiderte Webseiten.

## Aufbau

Statische Webseite, kein Build-Prozess nötig. Direkt deploybar auf GitHub Pages, Cloudflare Pages, Netlify oder jedem statischen Hoster.

```
.
├── index.html              # Hauptseite
├── referenzen.html         # Übersicht aller Demos
├── komponenten.html        # Komponenten-Schau (Formulare, CTAs, WhatsApp etc.)
├── impressum.html
├── datenschutz.html
├── assets/
│   ├── style.css           # geteiltes Stylesheet
│   └── site.js             # geteiltes JS (Nav, Reveal-Animationen)
└── demos/
    ├── atelier/            # Hochglanz-Showcase im Apple-Stil
    ├── holzgeist/          # Tischlerei (Branche: Handwerk)
    ├── aurora/             # Café (Branche: Essen)
    ├── atmen/              # Yoga-Studio (Branche: Fitness)
    ├── arztpraxis/         # Hausarztpraxis (Branche: Arzt)
    └── laden/              # Schreibwaren-Geschäft (Branche: Geschäft)
```

## Lokal ansehen

Einfach in einem Browser öffnen oder einen kleinen Webserver starten:

```bash
python3 -m http.server 8000
# oder
npx serve .
```

## Tech

- Plain HTML, CSS, JS (kein Framework)
- Schriftarten via Google Fonts (Fraunces, Inter, JetBrains Mono)
- Keine Cookies, keine Tracker, kein Analytics
- DSGVO-konform

## Lizenz

Inhalte © Pixelschneiderei. Code MIT-lizenziert (siehe `LICENSE`).
