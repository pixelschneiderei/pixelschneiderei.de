# Bilder-Manifest

Vollständige Liste der Mock-Bilder, die für die Demo-Auftritte gebraucht werden.

## Allgemeine Hinweise

**Format:** JPG (für Fotos), PNG nur wenn Transparenz nötig.
**Komprimierung:** ~75-85% Qualität, optimiert für Web (max ~300 KB pro Bild).
**Farb-Profil:** sRGB.
**Dateinamen:** Kleinbuchstaben, Bindestriche statt Leerzeichen.

**Prompt-Sprache:** Englisch funktioniert bei den meisten KI-Generatoren (Midjourney, DALL-E, Flux, Stable Diffusion) am zuverlässigsten — die Prompts unten sind deshalb auf Englisch.

**Fallback:** Solange ein Bild noch fehlt, zeigt der Browser den fest eingebauten Farbverlauf an (kein Bruch in der Optik).

---

## Übersicht — was wird wo gebraucht

| Demo                | Ordner                        | Anzahl Bilder | Priorität |
|---------------------|-------------------------------|---------------|-----------|
| **Lichtblick** (Foto)    | `demos/lichtblick/img/`    | ~17 (Hero, 3 Stories, 2 Bleed, 9 Masonry, About, Contact) | **Hoch** — Demo ist bildgetrieben |
| **Atmen** (Yoga)         | `demos/atmen/img/`         | 13 (Hero, 2 Editorial, 6 Bento, 3 Lehrer, Closing) | **Hoch** — Editorial lebt von Fotos |
| **Holzgeist** (Tischlerei) | `demos/holzgeist/img/`   | 9 (Hero + 8 Galerie) | Mittel |
| **Aurora** (Café)        | `demos/aurora/img/`        | 4 (Hero, Coffee, 2 Menu)  | Mittel |
| **Kontur** (Blog)        | `demos/kontur/img/`        | 7 (Hero + 6 Posts) | Mittel |
| **Praxis Linde** (Arzt)  | `demos/arztpraxis/img/`    | 3 (Hero, 2 Doktor) | Mittel |
| **Kanzlei**              | `demos/kanzlei/img/`       | 4 (Hero, 3 Anwält:in) | Mittel |
| **Laden** (Schreibwaren) | `demos/laden/img/`         | 6 (Hero, 4 Produkte, Story) | Mittel |
| **Akademie** (Bildung)   | `demos/akademie/img/`      | 7 (1 Hero + 6 Kurs-Thumbs) | Editorial / abstrakt |
| **Atelier** (Hochglanz)  | —                          | 0 *(SVG/CSS-basiert)* | Optional |
| **Nachtschicht** (DJ)    | —                          | 0 *(SVG/CSS-basiert)* | Optional |
| **e-bikefactory.de**     | (extern, live)             | —             | — |

**Insgesamt ~63 Bilder** für „voll bestückte" Demos. Wenn du nur die wichtigsten machen willst: Lichtblick (komplett) + Atmen (komplett) sind die gr&ouml;&szlig;ten visuellen Hebel; danach reicht oft schon der jeweilige `hero.jpg` pro Demo.

---

## 1. Atmen — Yoga Studio (Editorial)

**Ordner:** `demos/atmen/img/`
**Bild-Stil:** Editorial photography, soft natural light, sage green & cream palette, calm and intimate. Photorealistic, 35mm film aesthetic, shallow depth of field. **Kein** klischeehaftes Stock-Yoga.

| Datei              | Format     | Verwendung           | Prompt |
|--------------------|------------|----------------------|--------|
| `hero.jpg`         | 16:9, 2400×1350 | Vollbild-Hero    | *Editorial photography, woman in cross-legged seated meditation by large industrial warehouse window, golden morning light streaming in, sage green and cream tones, minimal composition, shallow depth of field, photorealistic, 35mm film aesthetic, calm intimate atmosphere* |
| `editorial-1.jpg`  | 4:5, 1200×1500 | Erste Story-Sektion | *Close-up editorial of person breathing deeply, hand resting on chest, soft natural light, sage and cream linen, intimate quiet moment, photorealistic, 35mm aesthetic* |
| `editorial-2.jpg`  | 4:5, 1200×1500 | Zweite Story-Sektion | *Person mid-vinyasa flow pose, side profile, blurred warm background, editorial photography, sage green tones, contemplative atmosphere, soft natural daylight* |
| `gallery-1.jpg`    | 3:4 portrait | Bento (groß, links) | *Quiet yoga studio interior, large industrial windows, polished wooden floor, single rolled mat, soft morning light, no people, editorial* |
| `gallery-2.jpg`    | 1:1, 1000×1000 | Bento (klein) | *Close-up of bare feet in mountain pose on wooden floor, warm natural light, sage tones, editorial detail shot* |
| `gallery-3.jpg`    | 1:1, 1000×1000 | Bento (klein) | *Hands holding warm ceramic tea cup, soft steam rising, sage linen background, still life, editorial* |
| `gallery-4.jpg`    | 16:9 wide   | Bento (breit) | *Wide interior shot of yoga studio, soft afternoon light through tall industrial windows, hanging plants, minimal furniture, editorial architecture photography* |
| `gallery-5.jpg`    | 1:1, 1000×1000 | Bento (klein) | *Person silhouette in child's pose against window light, dramatic backlight, calm editorial composition* |
| `gallery-6.jpg`    | 1:1, 1000×1000 | Bento (klein) | *Stack of folded sage linen blankets and a wooden yoga block on wood floor, neutral background, still life editorial* |
| `teacher-lina.jpg` | 3:4 portrait, 1200×1600 | Lehrer-Portrait | *Editorial portrait of woman late 30s, short dark hair, gentle expression looking slightly away from camera, sage green linen top, neutral cream background, soft natural light, shallow depth of field, 35mm aesthetic* |
| `teacher-jonas.jpg`| 3:4 portrait, 1200×1600 | Lehrer-Portrait | *Editorial portrait of man early 30s, short brown hair, calm thoughtful expression, neutral oatmeal linen shirt, soft natural light, neutral background, 35mm film aesthetic* |
| `teacher-mira.jpg` | 3:4 portrait, 1200×1600 | Lehrer-Portrait | *Editorial portrait of woman early 40s, longer hair loosely tied back, warm relaxed smile, soft sage tones, natural daylight, editorial photography* |
| `closing.jpg`      | 16:9 wide, 2400×1350 | Vollbild-Schluss | *Wide cinematic shot of empty yoga studio at golden hour, warm light streaming through tall windows, single mat unrolled in center, contemplative empty space, editorial atmosphere* |

---

## 2. Aurora — Café & Rösterei

**Ordner:** `demos/aurora/img/`
**Bild-Stil:** Warm hospitality photography, peach and coral tones with cream highlights, golden morning light, cozy and inviting.

| Datei              | Format        | Verwendung    | Prompt |
|--------------------|---------------|---------------|--------|
| `hero.jpg`         | 4:5 portrait, 1200×1500 | Hero rechts | *Top-down photo of latte art in white ceramic cup on warm peach linen tablecloth, soft morning light, croissant on side plate, hospitality photography, warm coral tones* |
| `coffee.jpg`       | 1:1 square    | Rösterei-Sektion | *Close-up of dark roasted coffee beans being poured from copper scoop, warm golden light, shallow depth of field, atmospheric* |
| `menu-pastry.jpg`  | 4:3, 1200×900 | Menu-Karte 1 | *Flat lay of fresh pastries — sourdough toast with avocado, croissants, small cake — peach linen background, hospitality editorial* |
| `menu-coffee.jpg`  | 4:3, 1200×900 | Menu-Karte 2 | *Lineup of three coffee drinks — espresso, flat white, filter — on warm marble counter, soft warm light, editorial hospitality* |

---

## 3. Holzgeist — Tischlerei

**Ordner:** `demos/holzgeist/img/`
**Bild-Stil:** Rich warm wood tones, workshop atmosphere, golden hour lighting, craft and tradition. Photorealistic.

**Hinweis:** Der Vorher/Nachher-Slider („&Uuml;berarbeitung von Bestandsseiten") ist rein CSS &mdash; **keine zus&auml;tzlichen Bilder n&ouml;tig**. Auf der „Nachher"-Seite wird das `hero.jpg` automatisch als Hintergrund mitverwendet.

| Datei              | Format        | Verwendung    | Prompt |
|--------------------|---------------|---------------|--------|
| `hero.jpg`         | 4:5 portrait, 1200×1500 | Hero rechts | *Detailed close-up of beautiful oak wood grain on a finished tabletop, warm golden hour light raking across surface, photorealistic, rich amber tones* |
| `gallery-1.jpg`    | 4:5 portrait  | Galerie · Küche Eiche | *Custom oak kitchen, warm natural lighting, minimalist craftsman style, photorealistic* |
| `gallery-2.jpg`    | 4:5 portrait  | Galerie · Esstisch Nussbaum | *Solid walnut dining table in warm interior, golden hour light, photorealistic* |
| `gallery-3.jpg`    | 4:5 portrait  | Galerie · Garderobe Esche | *Custom ash wood wardrobe in entryway, warm natural light, simple craftsman design* |
| `gallery-4.jpg`    | 4:5 portrait  | Galerie · Sideboard Kirsche | *Cherry wood sideboard, mid-century-influenced craftsmanship, warm interior* |
| `gallery-5.jpg`    | 4:5 portrait  | Galerie · Treppe Buche | *Wooden beech staircase, modern minimalist craftsmanship, soft daylight* |
| `gallery-6.jpg`    | 4:5 portrait  | Galerie · Bett Eiche | *Oak bed frame in calm bedroom, soft morning light, craftsman quality* |
| `gallery-7.jpg`    | 4:5 portrait  | Galerie · Schreibtisch Lärche | *Larch wood desk in home office, warm light, minimalist* |
| `gallery-8.jpg`    | 4:5 portrait  | Galerie · Vitrine Ahorn | *Maple wood display cabinet, glass doors, simple craftsman design* |

---

## 4. Praxis Linde — Hausarztpraxis

**Ordner:** `demos/arztpraxis/img/`
**Bild-Stil:** Clean, professional, trustworthy. Soft blue-grey palette, white surfaces, warm but clinical. **Keine** Stock-„Doctor with stethoscope smiling at camera"-Klischees — eher architektonisch / atmosphärisch.

| Datei              | Format        | Verwendung    | Prompt |
|--------------------|---------------|---------------|--------|
| `hero.jpg`         | 4:5 portrait, 1200×1500 | Hero rechts | *Modern minimalist medical practice waiting room, soft blue-grey walls, single comfortable chair, plant in corner, soft daylight from window, calm and reassuring atmosphere, architectural photography* |
| `doctor-anna.jpg`  | 1:1 square, 1000×1000 | Dr. Anna Linde | *Editorial portrait of woman late 40s, doctor, white coat over light shirt, gentle confident expression, neutral background, soft daylight, professional but approachable* |
| `doctor-johannes.jpg` | 1:1 square, 1000×1000 | Dr. Johannes Bender | *Editorial portrait of man early 50s, doctor, white coat, slight smile, glasses, neutral background, soft daylight, professional and warm* |

---

## 5. Das gute Büro — Schreibwaren-Geschäft

**Ordner:** `demos/laden/img/`
**Bild-Stil:** Cozy small business, warm rust and cream tones, traditional craft, intimate. Like a beloved corner shop.

| Datei              | Format        | Verwendung    | Prompt |
|--------------------|---------------|---------------|--------|
| `hero.jpg`         | 4:5 portrait  | Hero rechts | *Vintage stationery shop interior, wooden shelves filled with notebooks and pens, warm afternoon light through shop window, cozy and inviting, editorial* |
| `prod-fueller.jpg` | 1:1 square    | Produkt: Füller | *Close-up of fountain pens and ink bottle on warm wood surface, soft natural light, editorial product photography* |
| `prod-notiz.jpg`   | 1:1 square    | Produkt: Notizbücher | *Stack of leather-bound notebooks in earthy tones, top-down view, warm wood surface, editorial product still life* |
| `prod-buero.jpg`   | 1:1 square    | Produkt: Bürobedarf | *Beautiful arrangement of vintage-style office supplies — wooden ruler, scissors, paper clips — on cream linen, editorial flat lay* |
| `prod-geschenk.jpg`| 1:1 square    | Produkt: Geschenke | *Curated still life of stamps, sealing wax, twine and writing paper, warm rust palette, editorial* |
| `story.jpg`        | 1:1 square    | Geschichte-Sektion | *Black and white style portrait of small shop window from outside, warm reflection of street, nostalgic editorial photography* |

---

## 6. Pixelakademie — Online-Kurse

**Ordner:** `demos/akademie/img/`
**Bild-Stil:** Editorial / abstrakt. Jedes Kurs-Thumbnail hat einen eigenen Farbton (passend zur Kursfarbe) und greift die Kurs-Thematik visuell auf. Hochwertige Fotografie oder abstrakte Komposition &mdash; **keine** Stock-„Person mit Laptop"-Klischees.

| Datei              | Format        | Verwendung    | Prompt |
|--------------------|---------------|---------------|--------|
| `hero.jpg`         | landscape     | Hintergrund Hero (optional) | *Soft editorial composition of an open notebook with sketches, color swatches and a coffee cup, warm natural light, calm focused mood* |
| `course-1.jpg`     | 16:10         | Webdesign-Grundlagen | *Editorial flat lay: typography sample card, color swatch fan and a draft paper with grid lines, blue palette, soft natural light* |
| `course-2.jpg`     | 16:10         | Farb- &amp; Typo-Systeme | *Three overlapping circles in warm orange/amber tones on neutral paper, abstract design composition, editorial photography* |
| `course-3.jpg`     | 16:10         | Modernes CSS &amp; Layout | *Abstract layout grid with rectangles in green palette, paper-like texture, editorial design composition* |
| `course-4.jpg`     | 16:10         | Animation &amp; Bewegung | *Abstract motion-blur composition with curved light streaks in copper/brown palette, dynamic editorial photo* |
| `course-5.jpg`     | 16:10         | SEO ohne Hokuspokus | *Stack of clean structured paper documents with horizontal text lines, purple/lavender color, editorial flat lay* |
| `course-6.jpg`     | 16:10         | Barrierefreiheit | *Connected dots forming a chart on cream background, blue/navy palette, abstract editorial composition representing connection and clarity* |

---

## 7. Kanzlei Mahler — Rechtsanwälte

**Ordner:** `demos/kanzlei/img/`
**Bild-Stil:** Klassisch, professionell, vertraulich. Navy + gold Akzente, dunkle Holztöne, gediegene Atmosphäre. **Keine** Stock-„Lawyer pointing at document"-Klischees — eher architektonisch / Detail-Aufnahmen.

| Datei              | Format        | Verwendung    | Prompt |
|--------------------|---------------|---------------|--------|
| `hero.jpg`         | 3:4 portrait  | Hero rechts | *Atmospheric photo of antique bronze statue of Lady Justice on dark wooden desk, soft window light, warm gold reflections on dark navy background, editorial detail shot* |
| `lawyer-lena.jpg`  | 1:1 square    | Dr. Lena Mahler | *Editorial portrait of woman late 40s, dark blazer, confident calm expression, neutral background, soft natural light, professional photography, slightly looking away* |
| `lawyer-tobias.jpg`| 1:1 square    | Tobias Weber | *Editorial portrait of man early 50s, navy suit, glasses, thoughtful expression, neutral background, soft natural light, professional* |
| `lawyer-selma.jpg` | 1:1 square    | Selma Roth | *Editorial portrait of woman late 30s, dark blouse, calm professional expression, neutral background, soft natural light* |

---

## 8. Lichtblick — Fotografie (Hochzeit/Editorial)

**Ordner:** `demos/lichtblick/img/`
**Bild-Stil:** Editorial wedding photography, warm earth tones (champagne, ochre, deep umber), natural light, intimate documentary feel. **Keine** posierten Stockbilder — eher quiet candid moments. 35mm aesthetic, shallow depth of field.

**Wichtig:** Da die Demo bildgetrieben ist, lebt sie wirklich von guten Bildern. Falls möglich: konsistenter Look über alle Bilder hinweg (z. B. alle warm-toned, alle in derselben „Saison").

| Datei              | Format            | Verwendung    | Prompt |
|--------------------|-------------------|---------------|--------|
| `hero.jpg`         | 16:9, 2400×1350   | Vollbild-Hero | *Editorial wedding photo, bride and groom walking away from camera in soft golden hour light, warm champagne tones, candid intimate moment, 35mm film aesthetic, shallow depth of field, photorealistic* |
| `feature-1.jpg`    | 4:5, 1200×1500    | Story 01 (Marlene & Aaron) | *Editorial wedding photo, close-up detail of bride's hands holding wildflower bouquet, soft natural light, champagne and sage tones, intimate documentary style, 35mm aesthetic* |
| `feature-2.jpg`    | 4:5, 1200×1500    | Story 02 (Friederike & Tom) | *Editorial wedding photo, mountain wedding scene, couple in alpine setting, warm earthy tones, golden hour light, candid documentary, photorealistic* |
| `feature-3.jpg`    | 4:5, 1200×1500    | Story 03 (Sina & Lukas) | *Editorial wedding photo, intimate small wedding in courtyard with string lights, warm evening light, candid documentary moment, 35mm aesthetic* |
| `bleed-1.jpg`      | 16:9 wide, 2400×1350 | Vollbild-Sektion 1 | *Sweeping wide editorial wedding shot, couple silhouetted against landscape, golden hour, warm earth tones, cinematic composition, photorealistic* |
| `bleed-2.jpg`      | 16:9 wide, 2400×1350 | Vollbild-Sektion 2 | *Editorial wedding shot, dance floor moment, warm golden lights, candid joyful expression, motion blur, atmospheric, 35mm film aesthetic* |
| `m1.jpg`–`m9.jpg`  | gemischt (3:4, 1:1, 4:5) | Masonry-Galerie (9 Bilder) | *Various editorial wedding photos: details (rings, shoes, flowers), candid portraits, ceremony moments, reception scenes, all warm earth tones, consistent style, 35mm aesthetic* |
| `about.jpg`        | 4:5, 1200×1500    | Über uns (Helene & Jakob) | *Editorial portrait of photographer couple in their 30s with cameras, casual relaxed pose, warm natural light, intimate behind-the-scenes feel, neutral background* |
| `contact.jpg`      | 16:9 wide, 2400×1350 | Kontakt-Hintergrund (mit Overlay) | *Soft atmospheric wedding-related still life — flowers, light, fabric — warm tones, blurred, used as faded background image* |

---

## 9. Nachtschicht — DJ &amp; Producer

**Ordner:** `demos/nachtschicht/img/` *(optional — die Demo lebt von CSS-Effekten und braucht keine Bilder zwingend)*

| Datei              | Format        | Verwendung    | Prompt |
|--------------------|---------------|---------------|--------|
| `set-1.jpg`        | 1:1 square    | optional Set-Cover | *Abstract synthwave artwork, vibrant magenta and cyan gradients, dark background, geometric shapes, retro-futuristic, perfect square cover art* |
| `set-2.jpg`–`set-4.jpg` | 1:1 square | optional Set-Covers | *Various abstract music cover art in synthwave aesthetic, magenta/cyan/dark, geometric, premium club artwork* |
| `hero.jpg`         | 16:9 wide     | optional Hero-Hintergrund | *Atmospheric DJ booth photography from behind, neon lights in pink and cyan, warehouse club setting, motion blur, cinematic, photorealistic* |

---

## 10. Kontur — Magazin / Blog

**Ordner:** `demos/kontur/img/`
**Bild-Stil:** Editorial magazine photography, varied subjects matching the article topics. Documentary feel, natural light, neutral tones with occasional warm accents.

| Datei              | Format        | Verwendung    | Prompt |
|--------------------|---------------|---------------|--------|
| `hero.jpg`         | 4:3, 1600×1200 | Hero-Artikel | *Editorial photo of an old well-worn coat hanging in a wardrobe, warm natural light, intimate documentary style, neutral background* |
| `post-1.jpg`       | 4:3           | „Vom Schnittmuster zum Browser" | *Close-up of measuring tape on dark fabric, warm lighting, editorial detail shot* |
| `post-2.jpg`       | 4:3           | „Die Kunst, ‚nein' zu sagen" | *Editorial photo of empty notepad with pencil, soft window light, neutral palette* |
| `post-3.jpg`       | 4:3           | „Drei Tage in einer Werkstatt" | *Bavarian carpenter's workshop interior, wood shavings on floor, golden afternoon light, documentary photography* |
| `post-4.jpg`       | 4:3           | „Wir sind keine Bastelbude" | *Editorial portrait of woman web designer at desk, soft window light, candid working moment* |
| `post-5.jpg`       | 4:3           | „Warum jede Webseite mit einer Frage anfangen sollte" | *Editorial photo of hand writing in notebook, warm natural light, neutral tones* |
| `post-6.jpg`       | 4:3           | „Sechs Schriften" | *Editorial close-up of variable font specimens printed on paper, warm light, design context* |

---

## 11. Atelier — Pixelschneiderei Hochglanz

**Ordner:** `demos/atelier/img/`
**Bild-Stil:** Dunkel, abstrakt, premium. Nicht photorealistisch — eher Renderings / Abstraktionen. Deep blacks mit Schneider-Rot-Akzenten.

| Datei              | Format        | Verwendung    | Prompt |
|--------------------|---------------|---------------|--------|
| `hero-device.jpg`  | 16:10         | (optional) ersetzt SVG-Mockup | *Abstract minimal product render, dark background with deep red glow, single object floating in space, premium product photography aesthetic, cinematic lighting* |

(Das Atelier-Demo lebt vor allem von SVG/CSS-Effekten — Bilder sind hier nur optional.)

---

## Hauptseiten — og:image (Screenshots)

Jede öffentliche Hauptseite bekommt ein eigenes Open-Graph-Bild (1200×630), damit Social-Sharing-Vorschauen den richtigen Inhalt zeigen:

| Datei                                          | Verwendung                                                |
|------------------------------------------------|------------------------------------------------------------|
| `assets/og-home.jpg`                           | Startseite (`/`) sowie Impressum / Datenschutz             |
| `assets/og-referenzen.jpg`                     | Referenzen-Übersicht (`/referenzen.html`)                  |
| `assets/og-komponenten.jpg`                    | Komponenten-Schau (`/komponenten.html`)                    |
| `assets/og-premium-webdesign.jpg`              | Premium-Landingpage (`/premium-webdesign.html`)            |
| `assets/og-webdesign-coburg.jpg`               | Lokale Landingpage Coburg                                  |
| `assets/og-webdesign-oberfranken.jpg`          | Lokale Landingpage Oberfranken                             |
| `assets/og-webdesign-bayern.jpg`               | Lokale Landingpage Bayern                                  |
| `assets/og-webseite-handwerker-bayern.jpg`     | Branchen-Landingpage Handwerker (Bayern)                   |

Diese Bilder werden beim Teilen in WhatsApp, Slack, LinkedIn, Twitter etc. als Vorschau gezeigt. Sie werden — genau wie die Demo-Thumbnails — vom selben Puppeteer-Skript automatisch generiert. **Impressum und Datenschutz** bleiben bewusst beim allgemeinen `og-home.jpg` (sie werden nicht als Marketing-Inhalt geteilt).

### Responsive-Sektion auf der Startseite

Drei zusätzliche Screenshots in passenden Viewport-Grössen, die in den CSS-Device-Frames der „Web · Tab · Mob"-Sektion eingeblendet werden:

| Datei                            | Viewport     | Inhalt              |
|----------------------------------|--------------|---------------------|
| `assets/responsive-desktop.jpg`  | 1440×900     | Atelier-Demo (Desktop) |
| `assets/responsive-tablet.jpg`   | 820×1093     | Atelier-Demo (Tablet, 3:4) |
| `assets/responsive-mobile.jpg`   | 390×845      | Atelier-Demo (Mobile, ≈9:19.5) |

Werden vom selben `tools/screenshots.mjs`-Skript automatisch erzeugt — kein Extra-Schritt.

---

## Demo-Thumbnails (Screenshots)

Jede Demo bekommt ein `thumb.jpg` als **echten Seiten-Screenshot** (1200×630, Open-Graph-Standard).

**Wofür:**
- og:image-Vorschau beim Teilen (WhatsApp, Slack, LinkedIn, Twitter)
- Bild-Overlay über der SVG-Vorschau in der Referenzen-Übersicht
- Portfolio-Material

**Pfade:**
| Datei                          | Demo                |
|--------------------------------|---------------------|
| `demos/atelier/thumb.jpg`      | Atelier             |
| `demos/holzgeist/thumb.jpg`    | Holzgeist           |
| `demos/aurora/thumb.jpg`       | Aurora              |
| `demos/atmen/thumb.jpg`        | Atmen               |
| `demos/arztpraxis/thumb.jpg`   | Praxis Linde        |
| `demos/laden/thumb.jpg`        | Das gute Büro       |
| `demos/akademie/thumb.jpg`     | Pixelakademie       |
| `demos/kanzlei/thumb.jpg`      | Kanzlei Mahler      |
| `demos/lichtblick/thumb.jpg`   | Lichtblick          |
| `demos/nachtschicht/thumb.jpg` | Nachtschicht        |
| `demos/kontur/thumb.jpg`       | Kontur              |
| `demos/_external/e-bikefactory.jpg` | e-bikefactory.de (manuell screenshoten) |

**Erzeugung — vollautomatisch mit Puppeteer:**

```bash
# Einmalig:
npm install puppeteer

# Lokalen Server starten (empfohlen, damit Google Fonts korrekt laden):
npx http-server -p 8080
# oder: python3 -m http.server 8080

# In zweitem Terminal: alle 11 Thumbnails generieren
node tools/screenshots.mjs --base http://localhost:8080
```

Das Skript steht bereits unter `tools/screenshots.mjs` und blendet vor dem Screenshot automatisch das Demo-Banner und den „Demo verlassen"-Button aus. Anpassungen pro Demo (Wartezeit für Animationen) sind im Skript konfigurierbar.

**Manuelles Screenshoten** (z.B. mit „GoFullPage"-Browser-Extension oder OS-Screenshot bei 1200px-Breite):
1. Demo öffnen
2. Demo-Banner oben + „Demo verlassen"-Button im DevTools temporär ausblenden
3. Hero/oberer Bereich auf 1200×630 zuschneiden
4. JPEG ~85 % Qualität, max ~200 KB
5. Als `demos/[name]/thumb.jpg` speichern

**Fallback:** Wenn `thumb.jpg` fehlt, zeigt die Referenzen-Karte automatisch die handgebaute SVG-Vorschau. Kein Bruch im Layout.

---

## Komponenten-Bilder (für `komponenten.html`)

**Ordner:** `assets/img/komponenten/`

Damit die Galerie-Komponente und der Audio-Player auf der Komponenten-Seite plausibel aussehen:

| Datei              | Format        | Verwendung    | Prompt |
|--------------------|---------------|---------------|--------|
| `gallery-1.jpg`    | 4:5 portrait  | Galerie-Tile (groß) | *Top-down photo of design tools — measuring tape on dark fabric, pencil, color swatches — warm light, editorial workspace photography, neutral palette* |
| `gallery-2.jpg`    | 1:1 square    | Galerie-Tile | *Close-up macro of red thread being pulled through fabric, soft natural light, detail shot, photorealistic* |
| `gallery-3.jpg`    | 1:1 square    | Galerie-Tile | *Modern computer screen showing a clean design grid in CSS, soft window light, editorial workspace photography* |
| `gallery-4.jpg`    | 4:5 portrait  | Galerie-Tile | *Hand sketching on paper with fountain pen, warm light, intimate detail shot, design process editorial* |
| `gallery-5.jpg`    | 1:1 square    | Galerie-Tile | *Pinned color swatches and typography specimens on linen pinboard, warm afternoon light, design office editorial* |
| `track-cover.jpg`  | 1:1 square    | Audio-Player Cover | *Abstract minimalist artwork in deep red and black, geometric shapes, premium music cover art, square format* |

(Optional — ohne diese Bilder zeigt die Galerie ihre Gradient-Fallbacks und der Player das Brand-Logo als Cover.)

---

## Workflow-Empfehlung

1. **Pro Demo zuerst Hero + Story-Bilder generieren** — die haben die größte visuelle Wirkung.
2. **Galerie- und Sekundär-Bilder erst danach** — wenn die Hero-Stimmung sitzt, lassen sich die kleineren konsistent passend zum Stil weiter generieren.
3. **Stil-Konsistenz pro Demo wichtiger als perfektes Einzelbild.** Lieber alle Bilder einer Demo in einem Sitting / mit ähnlichen Prompts erzeugen.
4. **Optimieren vor dem Hochladen:** [Squoosh](https://squoosh.app) oder `cwebp -q 80` reicht.
5. **Alt-Text:** Falls du bei einer späteren Optimierung möchtest, dass die Bilder als `<img>` mit Alt-Text statt als CSS-Background verwendet werden — sag Bescheid, baue ich um.

## Falls Bilder fehlen

Solange ein Bild noch nicht im `img/`-Ordner liegt, fällt der Browser automatisch auf den fest eingebauten Farbverlauf zurück. Die Demo sieht dann etwas „flacher" aus, aber bricht **nicht**. Du kannst also Bild für Bild nachreichen.
