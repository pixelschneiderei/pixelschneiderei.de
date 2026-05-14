# new-project-agents.md — Vorlage für neue Pixelschneiderei-Kundenprojekte

> **Diese Datei ist eine Vorlage.** Beim Anlegen eines neuen Kundenprojekts wird sie nach `<kunde-projekt>/AGENTS.md` kopiert. **Teil A** bleibt wortgleich. **Teil B** wird mit den Kunden-Daten gefüllt. Diese Vorlage wird gepflegt, sobald sich universelle Patterns ändern.
>
> Letzter Stand: 2026-05-14 (Multipart-Forms, Datenschutz-Architektur, Cache-Strategie ergänzt)

## TL;DR — Do's & Don'ts auf einen Blick

| ✅ DO | ❌ DON'T |
|---|---|
| Self-hosted WOFF2-Schriften in `assets/fonts/` | Google Fonts via CDN (`fonts.googleapis.com`) |
| Lokales JS/CSS | Tailwind CDN, jQuery von cdnjs, Fontawesome-CDN |
| **Cloudflare Pages** als Hoster | WordPress/PHP/unbekannte Hoster ohne AVV |
| **Cloudflare Turnstile** für Bot-Schutz (cookie-frei) | Google reCAPTCHA (setzt Cookies, sendet an Google) |
| **Resend** für Mail-Versand (über `forms.pixelschneiderei.de`) | Direkt-SMTP, eigener PHP-Mailer, Strato-SMTP aus Worker |
| **OpenStreetMap** via Click-to-Load (Einwilligung pro Aufruf) | Google Maps, OSM direkt im Iframe, Mapbox |
| **YouTube/Vimeo** nur mit nocookie-Domain + Click-to-Load | Autoplay-Videos, eingebettete Tracker-Plattformen |
| Form-Submit an `forms.pixelschneiderei.de/<slug>/<form>` | Eigene `/api/*`-Endpoints (laufen ins Leere) |
| SPF/DKIM/DMARC für die Resend-Sending-Domain | „Aus dem Nutzer-Postfach senden" (geht technisch nicht) |
| `From: forms@pixelschneiderei.de` + `Reply-To: <user-mail>` | `From: <user-mail>` (DMARC-Violation, landet im Spam) |
| Cloudflare als Auftragsverarbeiter im Datenschutz | GitHub als „Hoster" angeben (falsch — GitHub sieht keine Endnutzer) |
| Cache-Control für CSS/JS: `must-revalidate` | CSS/JS mit `immutable` cachen ohne Hash im Dateinamen |
| Bilder mit Gradient-Fallback im CSS | Bilder ohne Fallback (404 → kahles Layout) |
| Datenschutz nach „Warum / Was / Wo / Wer ist verantwortlich"-Pattern | DSGVO-Generator-Texte 1:1 reinkopieren |
| Pixelschneiderei-Footer-Signatur „Mit Liebe geschneidert" | Footer ohne Pixelschneiderei-Hinweis |

---

## Onboarding-Fragen an den Kunden

Bevor du im Repo loslegst, klär folgende Punkte mit dem Kunden — am besten in einem strukturierten Erstgespräch oder per Fragebogen:

### 1. Identität & Rechtliches

- [ ] **Firmenname** (rechtlich korrekt, inkl. Form: GmbH, e.K., GbR, Einzelunternehmer)
- [ ] **Verantwortliche Person** (für Impressum + DSGVO Art. 4 Nr. 7)
- [ ] **Geschäftsadresse** (vollständig: Straße, PLZ, Ort, ggf. Land)
- [ ] **USt-ID** (falls vorhanden) oder Steuernummer
- [ ] **Handelsregister** (falls eingetragen: Nr. + Registergericht)
- [ ] **Berufsständische Pflichtangaben** (z.B. Handwerkskammer, Innungsmitgliedschaft, Berufshaftpflicht)
- [ ] **Mail (öffentlich)** — wird im Impressum + Datenschutz genannt
- [ ] **Telefonnummern** (mobil + Büro getrennt benennen, ob möglich)
- [ ] **Web-Domain** + ob bereits registriert (wenn nein: kümmern wir uns?)
- [ ] **Bestehende AGB / Datenschutz vorhanden?** Vom Anwalt oder selbst-generiert?

### 2. Corporate Identity (CI)

- [ ] **Logo** in welchen Formaten? (Idealfall: SVG; Notfall: hochauflösendes PNG)
- [ ] **Logo-Varianten** für hellen/dunklen Hintergrund? Für Favicon?
- [ ] **Markenfarben** als Hex/RGB — Primär, Sekundär, Akzent
- [ ] **Schriftarten** falls vorhanden — Display-Schrift + Body-Schrift
- [ ] **Tonalität** Du oder Sie? Förmlich oder locker?
- [ ] **Bilder vorhanden** — eigene Fotos? Anzahl + Qualität checken
- [ ] **Style-Vorlieben** (z.B. modern/klassisch, viel Weiß/eher dunkel, ruhig/spielerisch)

### 3. Inhalt & Struktur

- [ ] **Welche Seiten/Sektionen** braucht der Kunde? (One-Pager vs. Mehrseiter)
- [ ] **Leistungen / Produkte** — Liste mit Kurzbeschreibung
- [ ] **Über uns / Team** — Kurzgeschichte, Mitarbeiterzahl, Gründungsjahr
- [ ] **Referenzen / Bewertungen** vorhanden? (z.B. Google-Reviews, Trustpilot)
- [ ] **Karriere** — Stellen aktiv zu besetzen?
- [ ] **Pakete / Preise** — soll Pricing öffentlich sein?
- [ ] **Häufige Fragen** — was wird oft gefragt? (für FAQ)
- [ ] **Öffnungszeiten** (falls relevant) inkl. Feiertags-Regel

### 4. Funktionen

- [ ] **Kontaktformular?** (90 %: ja → Pixel-Form-Mailer)
- [ ] **Bewerbungsformular?** (mit CV-Upload)
- [ ] **Kartendarstellung?** (OpenStreetMap, Click-to-Load)
- [ ] **WhatsApp-Button?**
- [ ] **Newsletter-Anmeldung?** (kommt später, P3-Feature)
- [ ] **Service-Konfigurator / Online-Bestellung?** (kommt später)
- [ ] **Mehrsprachig?** (oft DE+EN; Stand 2026 noch nicht im Standard-Setup)

### 5. Hosting & Mail

- [ ] **Mail-Provider** des Kunden — wo liegt das Postfach? (Strato/IONOS/Google Workspace/Microsoft 365)
- [ ] **Empfänger-Adresse** für Form-Submissions (z.B. `info@kunde-name.de`)
- [ ] **DNS-Zugang** — können wir bei Bedarf DKIM/SPF-Records eintragen?
- [ ] **Bestehender Web-Vertrag**? Falls ja: Umzug oder parallel?
- [ ] **Cloudflare-Account beim Kunden vorhanden?** Sonst läuft alles auf Pixelschneiderei.

### 6. Branche / Spezifisches

- [ ] **Branche** und besondere DSGVO-Pflichten? (Arzt, Anwalt, Therapeut, Finanzen → strenger)
- [ ] **Saisonalität?** (z.B. Steuerberater hat Hochzeit im Frühling)
- [ ] **Lokal/Regional/National?** Beeinflusst SEO + JSON-LD
- [ ] **Vergleichbare Mitbewerber** zur Inspiration / Abgrenzung

### 7. Zeitplan & Budget

- [ ] **Gewünschter Go-Live**?
- [ ] **Anfragen-Volumen erwartet?** (beeinflusst Rate-Limit-Setup)
- [ ] **Service-Paket nach Go-Live?** (Budget / Basis / All-Inc)
- [ ] **Sonderwünsche** außerhalb des Standard-Setups?

---

## Was ist `forms.pixelschneiderei.de`?

Pixelschneiderei betreibt ein **Multi-Tenant-Mail-Backend** auf Cloudflare Workers für alle Kundenwebsites. Das spart pro Kunde Zeit + Geld und bietet einheitliche Qualität für Bot-Schutz, Mail-Versand und DSGVO-Compliance.

### Funktionsweise (Vereinfacht)

```
[Kunde-Website: kontaktformular]
        │
        │ POST forms.pixelschneiderei.de/<KUNDE-SLUG>/contact
        │ Header: Turnstile-Token
        │ Body:   Form-Daten (JSON oder Multipart)
        │
        ▼
[Cloudflare Worker: pixel-form-mailer]
        │
        ├─ 1. Origin-Check (CORS) → nur erlaubte Kunden-Domains
        ├─ 2. Honeypot-Check
        ├─ 3. Turnstile-Verify (Bot-Schutz)
        ├─ 4. Rate-Limit (optional, IP-gehasht)
        ├─ 5. Feld-Validierung (gegen Site-Config-Schema)
        ├─ 6. Attachment-Validierung (MIME, Größe)
        └─ 7. Resend-Versand
                │
                ▼
        [Mail-Postfach beim Kunden, z.B. Strato]
```

### Was du im Kunden-Projekt brauchst

1. **Site-Config** in `pixel-form-mailer/sites/<kunde-slug>.json` (Import in `src/lib/config.ts`)
2. **HTML-Pattern** auf der Kunden-Website (siehe A2.2 weiter unten)
3. **JS-Handler** in `assets/site.js` (siehe A2.3)
4. **CSP-Erweiterung** in `_headers` (siehe A7)
5. **Datenschutz-Sektionen** für Cloudflare + Resend in `datenschutz.html` (siehe A5)

### Vorteile

- **Bot-Schutz** via Cloudflare Turnstile (cookie-frei!)
- **Keine eigenen Server** beim Kunden — alles serverless auf Cloudflare
- **DSGVO-konform**: AVV mit Cloudflare + Resend, IP-Hashing, kein Tracking
- **Multipart-Support** für CV-Uploads, Foto-Anhänge, etc.
- **Test-Modus** pro Site (`mode: "test"`) für sicheren Aufbau ohne Live-Mails
- **Pro Kunde 0–10 Min Setup** nach dem Initial-Onboarding

### Wichtige Limits

| Limit | Wert |
|---|---|
| JSON-Body | 1 MB |
| Multipart-Body | 25 MB |
| Pro Datei-Anhang | 10 MB (per Site-Config) |
| Mail-Gesamt-Größe (Resend) | ≤ 40 MB |
| Resend Free-Tier | 3.000 Mails/Monat, 100/Tag |
| Cloudflare Workers Free | 100.000 Requests/Tag |

Beide Free-Tiers reichen für 10+ aktive Kundenwebsites locker.

---

# TEIL A — UNIVERSELL (1:1 für jedes Projekt)

> Dieser Teil ändert sich pro Kunde nicht. Diese Konventionen sichern DSGVO-Konformität, Performance, SEO und Konsistenz. Niemals löschen, nur ergänzen.

## A1. Hard Rules — niemals brechen

### A1.1 Keine externen Inhalte beim Seitenaufruf (DSGVO!)

Alles Externe wird **selbst gehostet**, keine Verbindungen zu Drittservern beim Aufruf der Seite:

- ❌ **Keine Google Fonts** via `https://fonts.googleapis.com/...`. Stattdessen WOFF2 lokal in `assets/fonts/`.
- ❌ **Kein Google Analytics**, Hotjar, Matomo (Cloud), Facebook-Pixel.
- ❌ **Keine CDN-eingebundenen JS-Libs** (jQuery from cdnjs, Tailwind Play CDN). JS und CSS lokal halten.
- ❌ **Keine Google Maps**. Stattdessen OpenStreetMap mit Click-to-Load.
- ❌ **Keine YouTube-Embeds ohne nocookie + Consent**.
- ❌ **Keine Webfonts-Loader**.

**Erlaubte Ausnahmen** (mit Begründung):
- ✅ `https://challenges.cloudflare.com/turnstile/v0/api.js` für Bot-Schutz (cookie-frei, Art. 32 DSGVO als Sicherheitsmaßnahme)
- ✅ `https://forms.pixelschneiderei.de/` als Form-Backend (eigener Dienst, AVV-geregelt)

**Rechtsgrundlage:** LG-München-Urteil 2022 (Az. 3 O 17493/20) — IP-Übermittlung ohne Einwilligung ist DSGVO-Verstoß.

### A1.2 Click-to-Load für jedes Drittanbieter-Iframe

Sobald ein `<iframe>` zu einer fremden Domain auflöst (OpenStreetMap, YouTube, Vimeo, Calendly, etc.), darf es **nicht** beim Laden der Seite automatisch geladen werden. Stattdessen Platzhalter mit:

1. **Erklärung**, dass beim Laden Daten an Drittanbieter übertragen werden
2. **Name + Sitz** des Drittanbieters
3. **Link zur Datenschutzerklärung** mit Anker
4. **Klick-Button** zur expliziten Einwilligung
5. **Alternativ-Link** zum direkten Öffnen beim Anbieter

Pattern siehe vollständige `AGENTS.md` der Pixelschneiderei, Sektion A1.1b.

### A1.3 BILDER.md ist Pflicht

Jedes Bild im Projekt muss in `BILDER.md` dokumentiert sein mit Pfad, Format, Verwendung, KI-Prompt.

```bash
grep -rhoE "url\('[^']+\.(jpg|jpeg|png|webp)'\)" *.html assets/*.css | sort -u
```

Jeder Treffer muss in BILDER.md auftauchen.

### A1.4 Fallback bei jedem Bild

```css
background:
  url('img/hero.jpg') center/cover no-repeat,
  linear-gradient(135deg, #colorA, #colorB);
```

Wenn das `.jpg` 404'd, fällt der Browser auf den Gradient zurück. Site bricht nicht.

### A1.5 Footer-Signatur „Mit Liebe geschneidert"

Auf jeder öffentlichen Seite eine dezente Signatur mit Link auf `pixelschneiderei.de`:

```html
<span class="foot-signature">
  <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <line x1="6" y1="18" x2="18" y2="6"/>
    <circle cx="17" cy="7" r="1.4"/>
    <path d="M15.5 6.5C13 5 10.5 6.5 11 9.5"/>
  </svg>
  Mit Liebe geschneidert @ <a href="https://pixelschneiderei.de/">pixelschneiderei.de</a>
</span>
```

---

## A2. Forms-Architektur (Pixel-Form-Mailer)

Jedes Kontakt-/Bewerbungs-/Anfrage-Formular läuft über **`forms.pixelschneiderei.de`** — den Multi-Tenant-Worker, der im Repo [`pixel-form-mailer`](../pixel-form-mailer/) lebt.

### A2.1 Onboarding-Schritte pro neuem Kunden

1. **Resend-Sending-Domain** verifizieren — nur einmalig nötig, wenn `from_address` auf Kunden-Domain zeigen soll. Im Standard-Setup nutzen wir `forms@pixelschneiderei.de` als Absender → kein zusätzlicher Resend-Setup nötig.
2. **Turnstile-Hostname** zur Allow-List des gemeinsamen Widgets hinzufügen (im Cloudflare-Turnstile-Dashboard).
3. **Site-Config** im `pixel-form-mailer`-Repo anlegen: `sites/<kunde-slug>.json` (kopiert von `sites/_example.json`).
4. **Site-Import** in `pixel-form-mailer/src/lib/config.ts` ergänzen.
5. **Deploy** des `pixel-form-mailer` via `wrangler deploy` oder Git-Push.
6. **HTML-Snippet** auf der Kunden-Site einbauen (siehe A2.2).

### A2.2 HTML-Pattern für ein Kontaktformular

```html
<!-- Im <head>: Turnstile-Script (cookie-frei) -->
<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>

<!-- Im <body>: Form -->
<form data-form="kontakt"
      action="https://forms.pixelschneiderei.de/<KUNDE-SLUG>/contact"
      method="post"
      autocomplete="on"
      novalidate>

  <!-- Felder -->
  <div class="field">
    <label for="kf-name">Name *</label>
    <input id="kf-name" name="name" type="text" required maxlength="100" autocomplete="name">
  </div>
  <div class="field">
    <label for="kf-email">E-Mail *</label>
    <input id="kf-email" name="email" type="email" required maxlength="200" autocomplete="email">
  </div>
  <!-- weitere Felder (phone, message, category, ...) -->

  <!-- Datenschutz-Checkbox -->
  <div class="field field--check">
    <input id="kf-datenschutz" name="datenschutz" type="checkbox" required>
    <label for="kf-datenschutz">Ich habe die <a href="/datenschutz.html">Datenschutzhinweise</a> gelesen ...</label>
  </div>

  <!-- Cloudflare Turnstile -->
  <div class="cf-turnstile"
       data-sitekey="<SHARED_SITEKEY>"
       data-theme="light"
       data-action="<KUNDE-SLUG>-contact"
       data-callback="onContactTurnstileSuccess"
       data-error-callback="onContactTurnstileError"
       data-expired-callback="onContactTurnstileExpired"></div>

  <!-- Honeypot (versteckt) -->
  <div class="honeypot" aria-hidden="true">
    <input name="hp_company" type="text" tabindex="-1" autocomplete="off">
    <input name="hp_url" type="text" tabindex="-1" autocomplete="off">
  </div>

  <!-- Submit + Status -->
  <button type="submit" class="cta cta--primary" data-submit disabled>Anfrage senden</button>
  <p data-form-status role="status" aria-live="polite" style="min-height: 1.2em;"></p>

  <!-- Provider-Hint (immer am Form-Ende, dezent grau) -->
  <p class="muted" style="font-size: var(--fs-xs); margin-top: var(--sp-2);">
    Felder mit * sind Pflicht. Kein Tracking, keine Cookies, keine dauerhafte Speicherung.
  </p>
  <p class="muted" style="font-size: var(--fs-xs); display: flex; align-items: center; gap: 6px;">
    <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0;" aria-hidden="true">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    </svg>
    <span>Bot-Schutz via <strong>Cloudflare Turnstile</strong> · cookie-frei · Versand via <strong>Resend</strong> · <a href="/datenschutz.html#turnstile">Details</a></span>
  </p>
</form>
```

### A2.3 JS-Pattern für die Form-Logik

In `assets/site.js` für jede Form-ID einmal:

- **Turnstile-Callbacks** als `window.on<Form>TurnstileSuccess/Error/Expired` registrieren
- **Submit-Button** disabled lassen bis Turnstile-Token vorliegt UND Datenschutz-Checkbox aktiv
- **Inline-Validierung** auf `blur` pro Feld (required, max_length, email, tel-format)
- **Submit-Handler:**
  - `e.preventDefault()` zuerst
  - Client-Validation laufen lassen → bei Fehler: erstes ungültiges Feld fokussieren, scrollen, kein POST
  - Body bauen: `FormData(form)` (multipart) ODER JSON
  - POST an Endpoint
  - Response-Status mappen: `validation` → Felder markieren, `rate_limit` → Status-Text, `captcha` → Turnstile reset, `send_failed` → Mail-Fallback anbieten

**Pattern in voller Länge:** Siehe `stuck-fuerl.de/assets/site.js`, Sektionen 7 (Kontakt) und 8 (Bewerbung).

### A2.4 Multipart vs JSON

| Form-Typ | Content-Type | Use Case |
|---|---|---|
| Kontakt (nur Text) | `application/json` | Einfacher Fall, kleinerer Body (max 1 MB Worker-Limit) |
| Kontakt mit Foto-Upload | `multipart/form-data` | Wenn Bild-Anhänge erlaubt sind |
| Bewerbung mit CV | `multipart/form-data` | Immer mit Dateien |

Der `pixel-form-mailer`-Worker erkennt den Content-Type automatisch und parst entsprechend. Limits:
- JSON: 1 MB Body
- Multipart: 25 MB total (Resend-Mail-Limit ≤ 40 MB; Datei-Anhänge werden base64-codiert ~33 % größer)
- Pro Datei: 10 MB (per Site-Config konfigurierbar)

### A2.5 Site-Config-Schema (Auszug)

```jsonc
{
  "site_id": "kunde-slug",
  "display_name": "Kunde GmbH",
  "allowed_origins": ["https://kunde-name.de", "https://www.kunde-name.de"],
  "turnstile_sitekey": "0x...",
  "turnstile_secret_env": "TURNSTILE_SECRET_SHARED",
  "mode": "test",                                   // → "production" beim Go-Live
  "forms": {
    "contact": {
      "recipient": ["info@kunde-name.de"],           // String oder Array
      "recipient_test": ["erikweisser@gmail.com"],   // greift bei mode: test
      "cc": [],                                       // optional, sichtbare CC
      "bcc": [],                                      // optional, versteckte BCC
      "from_name": "Web Form",
      "from_address": "forms@pixelschneiderei.de",
      "reply_to_field": "email",                      // → Reply-To auf User-Mail
      "subject_template": "[Kunde] {category} – Anfrage von {name}",
      "fields": {
        "name":     { "required": true,  "max_length": 100 },
        "email":    { "required": true,  "type": "email", "max_length": 200 },
        "phone":    { "required": false, "max_length": 30 },
        "message":  { "required": true,  "max_length": 5000 },
        "category": { "required": false, "max_length": 100 }
      },
      "attachments": {                                 // optional, wenn File-Upload
        "field": "anhang",
        "required": false,
        "max_size_bytes": 10485760,
        "allowed_mime": ["image/jpeg", "image/png", "image/webp"]
      }
    }
  }
}
```

### A2.6 Test-Modus pro Site

Während des Aufbaus (vor Go-Live):

```json
"mode": "test",
"recipient_test": ["erikweisser@gmail.com"]
```

Beim Go-Live:

```diff
- "mode": "test",
+ "mode": "production",
```

`recipient_test` darf stehen bleiben (wird ignoriert, falls `mode: "production"`).

---

## A3. SEO + Social-Sharing — Pflicht für jede öffentliche Seite

Vollständiges Pattern siehe `pixelschneiderei.de/AGENTS.md` Sektion A2.

**Minimum pro Seite:**
- `<title>` (~60 Zeichen, Keyword vorne)
- `<meta name="description">` (~155 Zeichen)
- `<link rel="canonical">`
- Open Graph: `og:title`, `og:description`, `og:type`, `og:url`, `og:image` (1200×630 JPEG), `og:image:width/height/alt`, `og:locale`
- Twitter: `twitter:card="summary_large_image"`, `twitter:image`
- JSON-LD strukturierte Daten (Schema.org) passend zum Seiten-Typ
- `robots.txt` mit KI-Crawler-Allowlist (GPTBot, ClaudeBot, PerplexityBot, etc.)
- `sitemap.xml` mit allen indexierbaren Seiten
- `llms.txt` als KI-Wegweiser

**OG-Image:** 1200×630 JPEG, < 300 KB, Logo zentriert auf gebrandetem Hintergrund. Generierung via `tools/`-Script (vgl. Stuck-Fürl `og-index.jpg` als Referenz: cremfarbener Hintergrund + Logo + Tagline darunter).

---

## A4. Hosting + Cloudflare-Setup

### A4.1 Cloudflare Pages als Default-Hoster

Vorteile:
- Kostenlos im Free-Tier (unbegrenzte Bandbreite, 500 Builds/Monat)
- Globales CDN
- HTTPS automatisch
- Git-Integration → automatischer Deploy
- Preview-Branches für Feature-Tests

### A4.2 `_headers`-Datei — Pflicht

Im Repo-Root:

```
/*
  Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
  Content-Security-Policy: default-src 'self'; img-src 'self' data: https://www.openstreetmap.org; style-src 'self' 'unsafe-inline'; script-src 'self' https://challenges.cloudflare.com; font-src 'self'; frame-src 'self' https://challenges.cloudflare.com https://www.openstreetmap.org; connect-src 'self' https://challenges.cloudflare.com https://forms.pixelschneiderei.de; form-action 'self' https://forms.pixelschneiderei.de; base-uri 'self'; object-src 'none';

# HTML — kurz cachen, immer revalidieren
/*.html
  Cache-Control: public, max-age=300, must-revalidate

/
  Cache-Control: public, max-age=300, must-revalidate

# Schriften — 1 Jahr immutable
/assets/fonts/*
  Cache-Control: public, max-age=31536000, immutable

# CSS / JS — KEIN Hash im Dateinamen → MUSS revalidieren, sonst kommen Updates nie an
/assets/style.css
  Cache-Control: public, max-age=300, must-revalidate
/assets/site.js
  Cache-Control: public, max-age=300, must-revalidate

# Bilder — 1 Jahr immutable (Dateinamen sind versioniert via Pfad)
/assets/img/*
  Cache-Control: public, max-age=31536000, immutable
/assets/ci/*
  Cache-Control: public, max-age=31536000, immutable
/assets/og-*.jpg
  Cache-Control: public, max-age=31536000, immutable
```

**Wichtig:** CSS/JS dürfen NICHT `immutable` sein, sonst sieht der Nutzer Updates nie. 5 Min Cache + Revalidate ist der Kompromiss.

### A4.3 `_redirects`-Datei — bei Bedarf

Für saubere URLs / Legacy-Redirects:

```
# Beispiel
/altseite.html  /neue-seite.html  301
/api/*  https://forms.pixelschneiderei.de/<KUNDE-SLUG>/:splat  200
```

### A4.4 Custom Domain konfigurieren

In Cloudflare Pages → Project → Custom domains → `kunde-name.de` + `www.kunde-name.de` hinzufügen.

Bei externer DNS-Konfiguration: CNAME-Record auf `<projektname>.pages.dev`.

---

## A5. Datenschutzerklärung — Architektur-Pattern

Die `datenschutz.html` folgt einer **vierteiligen Struktur** pro Drittanbieter-Sektion:

### A5.1 Pflicht-Sektionen

1. **Auf einen Blick** — Kurzer Klartext-Überblick (keine Cookies, kein Tracking, etc.)
2. **Verantwortlicher** — Name, Adresse, Mail, Telefon des Kunden (DSGVO Art. 4 Nr. 7)
3. **Was wir NICHT tun** — explizit auflisten: keine Cookies, kein Tracking, keine Google Fonts, etc.
4. **Architektur-Übersicht** — Verantwortlichkeitskette + Tabelle „Wer sieht welche Daten?"
5. **Pro Dienst eine Sektion** mit Anker (`#cloudflare-pages`, `#turnstile`, `#resend`, etc.) im Pattern unten

### A5.2 Pattern pro Drittanbieter-Sektion

Jede Service-Sektion folgt diesem Aufbau:

```markdown
<h2 id="dienst-slug">N. Dienstname (Kurz-Funktion)</h2>

<h3>Wer ist [Anbieter]?</h3>
<!-- Glaubwürdigkeit: Größe, Verbreitung, Reputation -->
<!-- Beispiel für Cloudflare: „Rund jede fünfte Webseite weltweit..." -->

<h3>Warum nutzen wir das?</h3>
<!-- Wertversprechen: was leistet der Dienst, warum brauchen wir ihn -->

<h3>Welche Daten werden verarbeitet?</h3>
<!-- Liste der Datenkategorien -->

<h3>Wo werden die Daten gespeichert?</h3>
<!-- Standort + Speicherdauer -->

<h3>Wer ist verantwortlich?</h3>
<!-- Verantwortlicher / Auftragsverarbeiter / Unterauftragsverarbeiter -->

<p>
  <strong>Rechtsgrundlage:</strong> Art. X Abs. Y DSGVO.<br/>
  <strong>Drittlandstransfer:</strong> ... SCC nach Art. 46 ...<br/>
  Datenschutzhinweise: <a href="...">...</a><br/>
  AVV: <a href="...">...</a>
</p>
```

### A5.3 Architektur-Tabelle — Pflicht-Bestandteil

In der Architektur-Übersicht eine Tabelle „Wer sieht welche Daten und wie lange?":

```html
<table>
  <thead>
    <tr><th>Dienst</th><th>Sieht</th><th>Speichert wie lange?</th></tr>
  </thead>
  <tbody>
    <tr><td>Cloudflare Pages</td><td>IP, User-Agent, URL</td><td>~7 Tage</td></tr>
    <tr><td>Cloudflare Turnstile</td><td>IP, Browser-Signale</td><td>Wenige Minuten</td></tr>
    <tr><td>Cloudflare Workers</td><td>Formularinhalte (in transit)</td><td>Wird nicht gespeichert</td></tr>
    <tr><td>Resend</td><td>Inhalt der Mail</td><td>Bis zu 30 Tage in Logs</td></tr>
    <tr><td>Strato (Mail-Postfach)</td><td>Empfangene Mail</td><td>Bis Anliegen erledigt</td></tr>
    <!-- weitere Dienste je nach Setup -->
  </tbody>
</table>
```

### A5.4 Verantwortlichkeitskette — bei Form-Backend

Wenn der Kunde Pixel-Form-Mailer nutzt, lautet die Kette:

1. **Verantwortlicher** (Art. 4 Nr. 7 DSGVO): der Kunde
2. **Auftragsverarbeiter** (Art. 28 DSGVO): Pixelschneiderei (technischer Dienstleister)
3. **Unterauftragsverarbeiter**: Cloudflare (Pages, Workers, Turnstile, DNS) und Resend (Mail-Versand)

Bei Pixelschneiderei selbst entfällt Stufe 2 — Pixelschneiderei ist direkt Verantwortlicher.

### A5.5 Glaubwürdigkeits-Bausteine

Für die „Wer ist [Anbieter]?"-Sektionen sind Glaubwürdigkeits-Hinweise hilfreich, um den Nutzer zu beruhigen:

> Cloudflare ist einer der weltweit größten Internet-Infrastruktur-Anbieter. **Rund jede fünfte Webseite weltweit** wird über Cloudflare-Dienste ausgeliefert oder abgesichert — von kleinen Handwerksbetrieben bis zu DAX-Konzernen und öffentlichen Stellen. Damit gehört Cloudflare zu den am besten überprüften und regulierten Anbietern weltweit.

Vergleichbarer Baustein für STRATO als deutscher Anbieter mit deutschem Rechenzentrum, oder Resend als spezialisierter Transactional-Mail-Anbieter.

### A5.6 Anti-Patterns in Datenschutz

- ❌ **GitHub als „Hoster" nennen.** Code liegt auf GitHub, ausgeliefert wird aber von Cloudflare Pages. GitHub sieht keine Endnutzer-Daten.
- ❌ Generische DSGVO-Generator-Texte 1:1 kopieren ohne Anpassung an die tatsächliche Verarbeitung.
- ❌ „Wir nutzen Google Analytics ..." reinkopieren, obwohl wir es gar nicht verwenden.
- ❌ Speicherdauer „unbestimmt" ohne Gesetzes-Bezug.

---

## A6. Mobile-First Forms — UX-Standards

### A6.1 Input-Anforderungen

- `width: 100%; max-width: 100%; min-width: 0;` auf allen Form-Inputs (verhindert horizontales Scrollen)
- `box-sizing: border-box` global
- `body { overflow-x: clip }` als Safety-Net gegen seitliches Überlaufen von fixed Elementen
- Grid-Items in `.field-row` brauchen `min-width: 0`, damit sie unter ihre intrinsische Min-Width schrumpfen dürfen
- `html` darf **NICHT** `overflow: hidden` haben (bricht position: fixed auf iOS Safari)

### A6.2 Nav: Desktop-First CSS

Mobile-Nav-Slide-In: alle Mobile-spezifischen Rules in `@media (max-width: 919.98px)`, damit Desktop nicht ständig Overrides braucht:

```css
/* Default: Desktop — Navi inline im Header */
.primary-nav { display: block; }
.primary-nav ul { display: flex; flex-direction: row; ... }

/* Mobile (< 920px): Slide-in von rechts */
@media (max-width: 919.98px) {
  .primary-nav {
    position: fixed; top: var(--header-h); right: 0; bottom: 0; left: 0;
    height: calc(100dvh - var(--header-h));
    transform: translateX(100%);
    visibility: hidden;
    ...
  }
  .primary-nav[data-open="true"] { transform: translateX(0); visibility: visible; }
}

@media (min-width: 920px) {
  .nav-toggle { display: none; }
}
```

### A6.3 Bilder — Responsive + Performance

Für jedes Hero-/Section-Bild:

```html
<picture>
  <source
    type="image/webp"
    srcset="/assets/img/foo-800.webp 800w,
            /assets/img/foo.webp 1600w"
    sizes="(max-width: 720px) 100vw, (max-width: 1100px) 50vw, 580px">
  <img src="/assets/img/foo.jpg" alt="..." loading="lazy" decoding="async" width="1600" height="1200">
</picture>
```

Pflicht:
- WebP-Quelle + JPG-Fallback
- 800w-Mobile-Variante (separater Build-Schritt)
- `loading="lazy"` (außer Above-the-Fold)
- `width`/`height` Attribute (gegen Layout-Shift)
- `decoding="async"`

---

## A7. Sicherheits-Header (CSP-Pflicht-Bausteine)

Für Sites mit Pixel-Form-Mailer-Forms MUSS die CSP enthalten:

```
script-src 'self' https://challenges.cloudflare.com;
frame-src  'self' https://challenges.cloudflare.com https://www.openstreetmap.org;
connect-src 'self' https://challenges.cloudflare.com https://forms.pixelschneiderei.de;
form-action 'self' https://forms.pixelschneiderei.de;
```

Falls weitere Drittdienste (z.B. Buchungs-Widget): CSP entsprechend erweitern.

**Häufige CSP-Fehler:**
- ❌ Turnstile-Script vergessen → Form wird nie aktiv
- ❌ `connect-src` zu strikt → POST an Worker scheitert
- ❌ `form-action` zu strikt → Browser cancelt Submit ohne Fehler-Indikator

---

## A8. Anti-Patterns — niemals tun

- ❌ Google Fonts via CDN einbinden
- ❌ Cookie-Banner für Funktionen, die wir gar nicht brauchen
- ❌ DSGVO-Generator-Texte 1:1 reinkopieren
- ❌ Stockfotos von „diverse business team"-Klischees
- ❌ Versprechen wie „100 % rechtssicher", „garantierte Top-1-Platzierung"
- ❌ Auto-Play-Videos mit Sound
- ❌ Pop-Ups beim Verlassen, Newsletter-Modals
- ❌ Karussells als Hero
- ❌ Datei-Upload-Forms ohne Multipart-Backend → CSP-Fehler
- ❌ Form-Action auf nicht-existente `/api/*`-URLs lassen

---

## A9. Verifikation vor Live-Schaltung — Checkliste

### A9.1 Technische Basics
- [ ] Lighthouse > 95 (Performance, Accessibility, Best Practices, SEO)
- [ ] HTTPS erzwungen (HSTS-Header)
- [ ] `_headers` mit CSP + Cache-Strategie
- [ ] OG-Image für jede Seite vorhanden, 1200×630 JPEG, < 300 KB
- [ ] WhatsApp-Sharing-Test: Link an sich selbst senden, Bild + Titel + Beschreibung kommen?
- [ ] Twitter-Card-Validator: card-validator.twitter.com
- [ ] Google Rich Results Test: search.google.com/test/rich-results
- [ ] Schema.org Validator: validator.schema.org

### A9.2 Forms
- [ ] Pixel-Form-Mailer Custom Domain `forms.pixelschneiderei.de` aktiv
- [ ] Secrets im Worker als **Secret** (nicht Plaintext) hinterlegt
- [ ] Turnstile-Hostname zur Allow-List hinzugefügt
- [ ] Site-Config committed und deployed
- [ ] End-to-End-Test: echte Submission → Mail kommt an
- [ ] Site-Config noch in `mode: "test"`? Beim Go-Live auf `production` umschalten

### A9.3 DSGVO
- [ ] `datenschutz.html` mit Architektur-Tabelle und allen Dienst-Sektionen
- [ ] Verantwortlicher korrekt benannt
- [ ] AVV mit Pixelschneiderei und Resend liegt vor (sofern Endkunden-Daten verarbeitet werden)
- [ ] OSM via Click-to-Load, nicht direkt eingebettet
- [ ] Kontaktdaten in Impressum + Datenschutz konsistent

### A9.4 Inhaltlich
- [ ] BILDER.md vollständig (grep-Audit grün)
- [ ] Alle Bilder gradient-fallback-fähig
- [ ] Footer-Signatur „Mit Liebe geschneidert" eingebaut
- [ ] Datenschutz an die *tatsächliche* Verarbeitung angepasst
- [ ] Kontakt-Mailadresse + Impressum-Daten korrekt

### A9.5 Deployment
- [ ] DNS sauber: A/AAAA, MX falls Mail, TXT (SPF/DKIM/DMARC) für Resend-Domain
- [ ] Cache-Header korrekt (CSS/JS revalidate, Bilder/Fonts immutable)
- [ ] Cloudflare Pages Build erfolgreich
- [ ] Custom Domain HTTPS-Zertifikat aktiv

---

# TEIL B — PROJEKT-SPEZIFISCH (pro Kunde anpassen)

> Folgender Block wird **pro Kunde** mit echten Werten gefüllt. Platzhalter sind `{{...}}`.

## B1. Kunde

- **Firmenname:** `{{Firmenname}}`
- **Verantwortlicher:** `{{Name}}`
- **Adresse:** `{{Straße, PLZ Stadt}}`
- **Branche:** `{{Branche, Spezialisierung}}`
- **Mail (öffentlich):** `{{info@kunde-name.de}}`
- **Telefon:** `{{+49 ...}}`
- **Website-Domain:** `{{kunde-name.de}}`
- **USt-ID / Steuernummer:** `{{...}}`

## B2. CI / Brand

- **Primärfarbe:** `{{#xxxxxx}}` (Verwendung: ...)
- **Sekundärfarbe:** `{{#xxxxxx}}`
- **Akzent:** `{{#xxxxxx}}`
- **Display-Schrift:** `{{Schriftname}}` (Selfhosted in `assets/fonts/`)
- **Body-Schrift:** `{{Schriftname}}`
- **Logo:** `{{Pfad zu Logo-Dateien}}`
- **Tonalität:** `{{Du/Sie + Sprachstil}}`

## B3. Site-Architektur (Sitemap)

- `/` (Startseite)
- `/kontakt.html`
- `/leistungen/...` *(falls Mehrseiter)*
- `/impressum.html`
- `/datenschutz.html`
- `/agb.html` *(falls relevant)*
- *(weitere)*

## B4. Pixel-Form-Mailer-Setup

- **Site-Slug:** `{{kunde-slug}}` (verwendet in `forms.pixelschneiderei.de/{{kunde-slug}}/contact`)
- **Form-Endpunkte:** `contact` *(weitere optional: karriere, services-order, ...)*
- **Empfänger:** `{{info@kunde-name.de}}`
- **Test-Modus aktiv?** `ja / nein` (für Go-Live auf production umstellen)

## B5. Hosting

- **Hoster:** Cloudflare Pages
- **Build-Branch:** `main`
- **Custom Domain:** `{{kunde-name.de}}`, `www.{{kunde-name.de}}`
- **DNS-Provider:** `{{Cloudflare / extern}}`
- **Mail-Provider (Empfang):** `{{Strato / IONOS / ...}}`

## B6. Besonderheiten / Notizen

`{{Hier kommen kundenspezifische Quirks, Wünsche, technische Sonderfälle, geplante Features etc.}}`

---

## Anhang: Datei-Struktur eines Pixelschneiderei-Kundenprojekts

```
projektroot/
├── AGENTS.md                       # Diese Datei (umbenannt, mit Teil B gefüllt)
├── README.md                       # Quickstart
├── BILDER.md                       # Bild-Manifest
├── DOCS.md                         # Self-Hosting-Anleitung für Kunden
├── TASKS.md                        # Phasenplan
├── TODO.md                         # Atomare Schritte
├── index.html
├── kontakt.html
├── impressum.html
├── datenschutz.html
├── agb.html                        # falls relevant
├── 404.html
├── leistungen/*.html               # falls Mehrseiter
├── _headers                        # Cloudflare Pages Header-Konfig
├── _redirects                      # Cloudflare Pages Redirects
├── sitemap.xml
├── robots.txt
├── llms.txt
├── site.webmanifest
├── assets/
│   ├── style.css                   # Komplettes Design-System
│   ├── site.js                     # Mobile-Nav, Forms, Reveal-Animationen
│   ├── fonts.css
│   ├── fonts/*.woff2               # Self-hosted WOFF2
│   ├── ci/*                        # Logo, Favicons, Brand-Assets
│   ├── og-*.jpg                    # OG-Images pro Seite
│   └── img/*                       # Inhalts-Bilder
└── tools/                          # Build-/Convert-Scripts
    ├── download-fonts.mjs
    ├── screenshots.mjs
    └── convert-fonts.mjs
```

---

## Anhang: Hilfreiche Pixelschneiderei-Referenzen

- **Pixel-Form-Mailer:** https://github.com/pixelschneiderei/pixel-form-mailer — Multi-Tenant Mail-Backend, dieser Worker bedient alle Pixelschneiderei-Kunden-Formulare
- **Pixelschneiderei.de:** https://pixelschneiderei.de — eigene Webseite, Komponenten-Showcase, Demos
- **AGENTS.md vollständig:** `pixelschneiderei.de/AGENTS.md` — die ausführliche Version dieser Vorlage (mit Pixelschneiderei-eigenem Teil B)

---

<!-- Versionsstand der Vorlage. Bei Updates dieses Templates Datum erhöhen. -->
**Stand der Vorlage: 2026-05-14**
