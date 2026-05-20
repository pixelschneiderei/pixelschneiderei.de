#!/usr/bin/env python3
"""
Pixelschneiderei — Preisübersicht.pdf

Nutzung (aus pixelschneiderei.de/tools/):
    python3 build-preisuebersicht.py                  # baut ../Preisübersicht.pdf
    python3 build-preisuebersicht.py /pfad/file.pdf   # eigenes Ziel

Dependencies (einmalig):
    pip install reportlab pdf2image pypdf fontTools brotli

Was passiert beim ersten Lauf:
    - Liest CI-Logo aus ../assets/ci/logo_w_font_light.png
    - Konvertiert WOFF2 (Fraunces, Inter, Allura) aus ../assets/fonts/ in TTF
      und cached sie in ./_fonts_cache/  (gitignore!)
    - Baut Preisübersicht.pdf in den parent (pixelschneiderei.de/-Root)
"""

import os, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Image, HRFlowable, KeepTogether,
)

HERE = os.path.dirname(os.path.abspath(__file__))
# Erlaubt, dass Script in tools/ liegt UND der Repo-Root direkt darüber ist.
# Falls Script lokal woanders liegt, einfach SITE_ROOT setzen.
SITE_ROOT = os.environ.get("PIXEL_SITE_ROOT", os.path.dirname(HERE))
FONT_CACHE = os.path.join(HERE, "_fonts_cache")
LOGO = os.path.join(SITE_ROOT, "assets", "ci", "logo_w_font_light.png")

# ---------------------------------------------------------------------------
# WOFF2 → TTF on-demand
# ---------------------------------------------------------------------------
def ensure_ttf(woff2_basename, out_name):
    """Konvertiert eine WOFF2-Datei (relativ zu SITE_ROOT/assets/fonts/) zu TTF,
    falls noch nicht im Cache. Gibt den TTF-Pfad zurück."""
    out_path = os.path.join(FONT_CACHE, out_name)
    if os.path.exists(out_path):
        return out_path
    src = os.path.join(SITE_ROOT, "assets", "fonts", woff2_basename)
    if not os.path.exists(src):
        raise FileNotFoundError(f"Schriftdatei fehlt: {src}")
    os.makedirs(FONT_CACHE, exist_ok=True)
    from fontTools.ttLib import TTFont as FT_TTFont
    f = FT_TTFont(src)
    f.flavor = None
    f.save(out_path)
    return out_path

# ---------------------------------------------------------------------------
# Fonts registrieren (latin-Subset reicht für Deutsch)
# ---------------------------------------------------------------------------
pdfmetrics.registerFont(TTFont("Fraunces",      ensure_ttf("fraunces-03.woff2", "fraunces.ttf")))
pdfmetrics.registerFont(TTFont("Fraunces-Bold", ensure_ttf("fraunces-03.woff2", "fraunces.ttf")))
pdfmetrics.registerFont(TTFont("Inter",         ensure_ttf("inter-07.woff2",    "inter.ttf")))
pdfmetrics.registerFont(TTFont("Inter-Bold",    ensure_ttf("inter-14.woff2",    "inter-bold.ttf")))
pdfmetrics.registerFont(TTFont("Allura",        ensure_ttf("allura-03.woff2",   "allura.ttf")))

from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("Inter",    normal="Inter", bold="Inter-Bold",
                   italic="Inter", boldItalic="Inter-Bold")
registerFontFamily("Fraunces", normal="Fraunces", bold="Fraunces-Bold",
                   italic="Fraunces", boldItalic="Fraunces-Bold")

SERIF  = "Fraunces"
SERIFB = "Fraunces-Bold"
SANS   = "Inter"
SANSB  = "Inter-Bold"
SCRIPT = "Allura"

# ---------------------------------------------------------------------------
# Pixelschneiderei-CI-Farben (1:1 aus assets/style.css)
# ---------------------------------------------------------------------------
PAPER     = colors.HexColor("#f5f1ec")
PAPER_2   = colors.HexColor("#eee9e1")
PAPER_3   = colors.HexColor("#e3ddd2")
SURFACE   = colors.HexColor("#ffffff")
LINE      = colors.HexColor("#d9d9d9")
LINE_SOFT = colors.HexColor("#e6e3dd")
INK       = colors.HexColor("#1a1a1a")
INK_SOFT  = colors.HexColor("#2e2e2e")
MUTED     = colors.HexColor("#7a766f")
THREAD    = colors.HexColor("#b1383a")
THREAD_2  = colors.HexColor("#c85a5c")
THREAD_3  = colors.HexColor("#f2d8d9")
GOLD      = colors.HexColor("#a87b3c")
GOLD_SOFT = colors.HexColor("#d8c194")

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
ss = getSampleStyleSheet()
S = {
    "h1": ParagraphStyle("h1", fontName=SERIFB, fontSize=26, leading=30,
                          textColor=INK, spaceAfter=4),
    "h1c": ParagraphStyle("h1c", fontName=SERIFB, fontSize=42, leading=48,
                          textColor=INK, alignment=TA_CENTER, spaceAfter=6),
    "h2": ParagraphStyle("h2", fontName=SERIFB, fontSize=16, leading=22,
                          textColor=INK, spaceBefore=6, spaceAfter=2),
    "h3": ParagraphStyle("h3", fontName=SANSB, fontSize=11.5, leading=15,
                          textColor=INK, spaceAfter=1),
    "h3_thread": ParagraphStyle("h3_thread", fontName=SANSB, fontSize=12,
                                 leading=15, textColor=THREAD, spaceAfter=1),
    "eyebrow": ParagraphStyle("eyebrow", fontName=SANSB, fontSize=8,
                              leading=11, textColor=THREAD, spaceAfter=2),
    "body": ParagraphStyle("body", fontName=SANS, fontSize=10, leading=14,
                            textColor=INK_SOFT, spaceAfter=4),
    "body_small": ParagraphStyle("body_small", fontName=SANS, fontSize=9,
                                  leading=13, textColor=INK_SOFT, spaceAfter=3),
    "muted": ParagraphStyle("muted", fontName=SANS, fontSize=8.5,
                             leading=12, textColor=MUTED),
    "muted_i": ParagraphStyle("muted_i", fontName=SANS, fontSize=8,
                               leading=11, textColor=MUTED),
    "lede": ParagraphStyle("lede", fontName=SERIF, fontSize=14, leading=20,
                            textColor=INK_SOFT, alignment=TA_CENTER,
                            spaceAfter=8),
    "lede_left": ParagraphStyle("lede_left", fontName=SERIF, fontSize=12,
                                 leading=18, textColor=INK_SOFT,
                                 spaceAfter=4),
    "price": ParagraphStyle("price", fontName=SANSB, fontSize=12, leading=14,
                             textColor=THREAD, alignment=TA_RIGHT),
    "price_inc": ParagraphStyle("price_inc", fontName=SANSB, fontSize=11,
                                 leading=14, textColor=GOLD, alignment=TA_RIGHT),
    "price_big": ParagraphStyle("price_big", fontName=SERIFB, fontSize=26,
                                 leading=30, textColor=THREAD,
                                 alignment=TA_RIGHT),
    "tc": ParagraphStyle("tc", fontName=SANS, fontSize=9, leading=12,
                          textColor=INK_SOFT),
    "tc_b": ParagraphStyle("tc_b", fontName=SANSB, fontSize=9, leading=12,
                            textColor=INK),
    "tc_c": ParagraphStyle("tc_c", fontName=SANS, fontSize=9, leading=12,
                            textColor=INK_SOFT, alignment=TA_CENTER),
    "callout_t": ParagraphStyle("callout_t", fontName=SERIFB, fontSize=13,
                                 leading=17, textColor=INK, spaceAfter=4),
    "callout_b": ParagraphStyle("callout_b", fontName=SANS, fontSize=10,
                                 leading=14, textColor=INK_SOFT),
    "script": ParagraphStyle("script", fontName=SCRIPT, fontSize=44,
                              leading=48, textColor=THREAD,
                              alignment=TA_CENTER),
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def hr(c=LINE_SOFT, thickness=0.5, spaceBefore=4, spaceAfter=4):
    return HRFlowable(width="100%", thickness=thickness, color=c,
                      spaceBefore=spaceBefore, spaceAfter=spaceAfter)

def eyebrow(label):
    return Paragraph(label.upper(), S["eyebrow"])

def item_row(name, price_text, description, is_main=False, included=False):
    """Zeile mit Item-Name, Preis (rechts), Beschreibung darunter.
    Wird als KeepTogether zurückgegeben, damit kein Paket über einen
    Seitenumbruch hinweg geteilt wird."""
    name_style  = S["h2"] if is_main else S["h3"]
    if included:
        price_style = S["price_inc"]
    elif is_main:
        price_style = S["price_big"]
    else:
        price_style = S["price"]
    head = Table(
        [[Paragraph(name, name_style), Paragraph(price_text, price_style)]],
        colWidths=[118*mm, 52*mm],
    )
    head.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))
    return [KeepTogether([head, Paragraph(description, S["body"])])]

def callout(title, body, bg=PAPER_2, accent=THREAD):
    t = Table(
        [[Paragraph(title, S["callout_t"])],
         [Paragraph(body, S["callout_b"])]],
        colWidths=[170*mm],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("LEFTPADDING", (0,0), (-1,-1), 14),
        ("RIGHTPADDING", (0,0), (-1,-1), 14),
        ("TOPPADDING", (0,0), (-1,-1), 12),
        ("BOTTOMPADDING", (0,0), (-1,-1), 12),
        ("LINEBEFORE", (0,0), (0,-1), 3, accent),
    ]))
    return t

# ---------------------------------------------------------------------------
# Page Frame
# ---------------------------------------------------------------------------
def add_frame(canv, doc):
    canv.saveState()
    p = canv.getPageNumber()
    if p == 1:
        canv.restoreState()
        return
    # Subtle paper-Background
    canv.setFillColor(PAPER)
    canv.rect(0, 0, A4[0], A4[1], stroke=0, fill=1)
    # Header
    canv.setFont(SANSB, 8)
    canv.setFillColor(THREAD)
    canv.drawString(20*mm, 287*mm, "PIXELSCHNEIDEREI")
    canv.setFillColor(MUTED)
    canv.setFont(SANS, 8)
    canv.drawString(46*mm, 287*mm, "· Preisübersicht 2026")
    canv.drawRightString(190*mm, 287*mm, f"{p}")
    canv.setStrokeColor(THREAD_3)
    canv.setLineWidth(0.5)
    canv.line(20*mm, 285*mm, 190*mm, 285*mm)
    # Footer
    canv.setFont(SANS, 7.5)
    canv.setFillColor(MUTED)
    canv.drawString(20*mm, 10*mm,
        "Keine USt. ausgewiesen — Kleinunternehmer nach § 19 UStG. "
        "Stand: Mai 2026.")
    canv.drawRightString(190*mm, 10*mm, "pixelschneiderei.de · erik@weisser.dev")
    canv.restoreState()

# ---------------------------------------------------------------------------
# Cover
# ---------------------------------------------------------------------------
def cover():
    s = []
    # Background filling
    s.append(Spacer(1, 25*mm))
    if os.path.exists(LOGO):
        s.append(Image(LOGO, width=85*mm, height=58*mm, hAlign="CENTER"))
    s.append(Spacer(1, 12*mm))
    s.append(Paragraph("Preis-Übersicht", S["h1c"]))
    s.append(Paragraph("<i>maßgeschneiderte Webseiten</i>", S["lede"]))
    s.append(Spacer(1, 4*mm))
    s.append(hr(c=THREAD, thickness=1, spaceBefore=0, spaceAfter=10))
    s.append(Paragraph("Was Sie auf den folgenden Seiten finden",
                       S["h2"]))
    s.append(Spacer(1, 3*mm))
    items = [
        ("1.", "Webseite Starter — der One-Pager"),
        ("2.", "Add-On Pakete — alle Bausteine im Detail"),
        ("3.", "Webseite Standard und Webseite All-Inclusive"),
        ("4.", "Pakete im Vergleich"),
        ("5.", "Server-Setup — schon vorhanden oder von uns?"),
        ("6.", "Jährliche Services im Detail"),
        ("7.", "Service-Pakete im Vergleich"),
        ("8.", "Garantien — Sourcen, Kündigung, Datenhoheit"),
        ("9.", "Zusammenfassung — wie wir zusammenarbeiten"),
    ]
    rows = [[Paragraph(f"<b>{n}</b>", S["tc_b"]),
             Paragraph(t, S["tc"])] for n, t in items]
    toc = Table(rows, colWidths=[11*mm, 159*mm])
    toc.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LINEBELOW", (0,0), (-1,-2), 0.3, LINE_SOFT),
    ]))
    s.append(toc)
    s.append(Spacer(1, 18*mm))
    s.append(Paragraph(
        "<i>schnell · ohne Cookies · ohne Tracking · ohne Überraschungen</i>",
        S["lede"]))
    s.append(Spacer(1, 4*mm))
    s.append(Paragraph(
        "<font color='#a87b3c'>Erik Weisser · Pixelschneiderei · erik@weisser.dev · "
        "pixelschneiderei.de</font>",
        ParagraphStyle("center_small", fontName=SANS, fontSize=9,
                        textColor=GOLD, alignment=TA_CENTER)))
    s.append(PageBreak())
    return s

# ---------------------------------------------------------------------------
# 1. Webseite Starter (OnePager) + Add-Ons
# ---------------------------------------------------------------------------
def section_starter():
    s = []
    s.append(eyebrow("1 · Einstieg"))
    s.append(Paragraph("Webseite Starter — der One-Pager", S["h1"]))
    s.append(Spacer(1, 3*mm))
    s += item_row(
        "Webseite Starter",
        "ab 900&nbsp;€",
        "Eine scrollbare Seite — Hero, Über-uns, Leistungen und ein "
        "Kontaktblock mit Mail- und Telefon-Link. <b>Keine Unterseiten.</b> "
        "Perfekt als digitale Visitenkarte, für Solo-Selbständige oder "
        "kleine Betriebe, die online präsent sein wollen, aber keinen "
        "Mehrseiter brauchen.",
        is_main=True,
    )
    s.append(Spacer(1, 6*mm))
    s.append(callout(
        "Impressum &amp; Datenschutz sind separat",
        "Als Unternehmen oder Selbständige sind Sie <b>gesetzlich zur Veröffentlichung "
        "von Impressum und Datenschutzerklärung verpflichtet</b> (§ 5 DDG / Art. 13 DSGVO). "
        "Das ist nicht im Starter-Preis enthalten — wir bieten es als Paket dazu an "
        "(<b>75&nbsp;€ einmalig</b>). Damit landen Sie für einen kompletten, "
        "rechtssicheren Web-Einstieg bei <b>975&nbsp;€</b>."))
    s.append(Spacer(1, 8*mm))
    s.append(Paragraph(
        "<b>Alle Add-On Pakete</b> (Kontaktformular Premium, Karriereseite, "
        "Bewertungs-Slider, KI-Content, Premium Design u.&nbsp;v.&nbsp;m.) finden Sie "
        "auf der nächsten Seite. Jedes ist beliebig mit dem Starter kombinierbar.",
        S["body"]))
    s.append(PageBreak())
    return s

# ---------------------------------------------------------------------------
# 2. Add-On Pakete (Katalog)
# ---------------------------------------------------------------------------
def section_addons():
    s = []
    s.append(eyebrow("2 · Bausteine"))
    s.append(Paragraph("Add-On Pakete", S["h1"]))
    s.append(Spacer(1, 3*mm))
    s.append(Paragraph(
        "Jedes Paket ist ein einmaliger Festpreis und kombinierbar mit jedem "
        "Webseiten-Tier. Wer das Premium-Bundle bucht, bekommt fast alle "
        "Bausteine in einem Festpreis — siehe Sektion&nbsp;3.",
        S["body"]))
    s.append(Spacer(1, 5*mm))

    # Erste Hälfte — Rechtliches, Kontakt, Inhalt
    addons_page_a = [
        ("Paket: Impressum &amp; Datenschutz", "75 €",
         "Impressum und Datenschutzerklärung werden in die Webseite eingebunden — "
         "Texte aus einem etablierten Rechtstexte-Generator (z.&nbsp;B. eRecht24 oder "
         "Datenschutz-Generator.de), die jeweils relevanten Dienst-Sektionen werden "
         "von uns sauber eingearbeitet. <i>Keine juristische Beratung.</i>"),
        ("Paket: Kontaktformular (Basis)", "(im Starter inkl.)",
         "Schön gestalteter Kontaktblock mit Mail- und Telefon-Link. "
         "Direkter Klick öffnet den Mail-Client des Besuchers — kein Server, "
         "kein Auftragsverarbeiter nötig.", False, True),
        ("Paket: Kontaktformular (Premium)", "150 €",
         "Echtes server-basiertes Formular mit Bot-Schutz (Cloudflare Turnstile, "
         "cookie-frei) und Vorqualifizierungsoptionen (Kategorie, Angebotsart), "
         "die direkt im E-Mail-Betreff erscheinen. Der Empfänger sieht auf einen "
         "Blick, worum es geht."),
        ("Paket: WhatsApp Call-to-Action", "50 €",
         "Click-to-Chat-Button mit vordefinierter Nachricht — wird häufig direkt "
         "neben dem Kontaktformular eingebaut, damit Besucher den Kommunikations-"
         "Weg wählen können. Mit DSGVO-konformem Hinweistext (Datenübertragung "
         "an Meta erst nach Klick)."),
        ("Paket: Bild (Basis)", "50 €",
         "Bearbeitung und Optimierung der von Ihnen gelieferten Bilder: Zuschnitt, "
         "Komprimierung, WebP-Konvertierung für schnelles Laden auf Mobilgeräten, "
         "Alt-Texte für Barrierefreiheit + SEO."),
        ("Paket: Premium Design", "ab 250 €",
         "Sie möchten keine simple Standard-Seite, sondern etwas <b>aufwändigeres, "
         "glänzendes</b> — eine Produkt-Vorschau wie im "
         "<a color='#b1383a' href='https://pixelschneiderei.de/demos/atelier/'>"
         "Atelier-Demo</a>? Hier helfen wir gerne. Aufwändigere Animationen, "
         "Hero-Inszenierungen, Scroll-Sequenzen, Custom-Typografie. Je nach "
         "Seiten-Paket, Wünschen und Vorstellung wird ein Aufpreis fällig — "
         "<i>konkrete Zahl erst nach Absprache</i>."),
        ("Paket: KI-Content (Bilder &amp; Texte)", "150 €",
         "Sie haben keine eigenen Bilder? Wollen nicht viel Geld für Stockfoto-"
         "Bibliotheken ausgeben? Wir generieren passgenaue Bilder und Texte "
         "<b>mit KI</b>, abgestimmt auf Ihre Branche, Ihren Auftritt und Ihre "
         "Tonalität. Bis zu 10 individuell erstellte Bilder + bis zu 4 fertig "
         "ausformulierte Sektionen-Texte."),
    ]
    # Zweite Hälfte — SEO, Erweiterungen, Extra-Seiten
    addons_page_b = [
        ("Paket: SEO-Optimierung (Basis)", "200 €",
         "Titles, Meta-Descriptions, JSON-LD Schema.org (LocalBusiness / Service), "
         "sitemap.xml, robots.txt mit KI-Crawler-Freigabe, llms.txt-Wegweiser — "
         "alles auf bessere regionale Google-Sichtbarkeit optimiert."),
        ("Paket: Bewertungs-Slider", "100 €",
         "Karussell mit Auto-Advance, Pagination-Dots und Touch-Swipe. "
         "Inkl. Schema.org Review &amp; AggregateRating für Sterne-Bewertung "
         "direkt in den Google-Suchergebnissen."),
        ("Paket: Click-to-Load (Privacy-Embed)", "50 € / Embed",
         "DSGVO-konformer 2-Klick-Wrapper für OpenStreetMap, YouTube-nocookie, "
         "Calendly, Trustpilot &amp; Co. Erst nach explizitem Klick wird das "
         "Iframe geladen — IP-Adresse bleibt bis dahin beim Besucher."),
        ("Paket: Content-Modal (Lightbox)", "50 €",
         "Wiederverwendbare Datenschutz-Quickinfo-Modal-Komponente — taucht z.&nbsp;B. "
         "über Form-Labels auf, statt Besucher auf eine andere Seite zu schicken."),
        ("Paket: Karriereseite inkl. Formular", "250 €",
         "Dedizierte Karriereseite mit Stellenanzeigen, Schema.org-JobPosting "
         "(damit Google die Stelle in der Suche prominent zeigt) und Bewerbungs-"
         "Formular inkl. CV-Upload."),
        ("Paket: Extraseite", "50 € / Seite",
         "Zusätzliche Unterseite mit eigenen Inhalten "
         "(z.&nbsp;B. eigene Über-uns-Seite, Team-Seite, Anfahrts-Seite)."),
        ("Paket: Produktseite", "50 € / Produkt",
         "Produkt-Übersichtsseite + pro Produkt eine eigene Detail-Seite "
         "mit Bildern, Beschreibung und Anfrage-CTA."),
    ]

    def render(addons_list, out):
        for row in addons_list:
            if len(row) == 5:
                n, p, d, _, inc = row
            else:
                n, p, d = row
                inc = False
            out += item_row(n, p, d, included=inc)
            out.append(hr())
        return out

    s = render(addons_page_a, s)
    s.append(PageBreak())
    s.append(eyebrow("2 · Bausteine (Fortsetzung)"))
    s.append(Paragraph("Add-On Pakete", S["h1"]))
    s.append(Spacer(1, 3*mm))
    s.append(Paragraph(
        "SEO, Erweiterungen und zusätzliche Seiten — alle ebenfalls einmalige "
        "Festpreise und beliebig mit jeder Tier-Stufe kombinierbar.",
        S["body"]))
    s.append(Spacer(1, 5*mm))
    s = render(addons_page_b, s)
    s.append(PageBreak())
    return s

# ---------------------------------------------------------------------------
# 3.  Standard UND Premium kombiniert auf EINER Seite
# ---------------------------------------------------------------------------
def section_standard_and_premium():
    s = []

    # --- 3 · STANDARD ---
    s.append(eyebrow("3 · Webseiten-Pakete"))
    s.append(Paragraph("Webseite Standard — der Mehrseiter", S["h1"]))
    s.append(Spacer(1, 2*mm))
    s += item_row(
        "Webseite Standard (Multi-Page)",
        "ab 1.400&nbsp;€",
        "Startseite + 2–4 Detail-Seiten + Kontaktseite mit echtem Formular. "
        "Wenn Sie mehr als eine scrollbare Seite brauchen — eigene "
        "Leistungs-Seiten, &bdquo;Über uns&ldquo;, &bdquo;Referenzen&ldquo;.",
        is_main=True,
    )
    s.append(Spacer(1, 4*mm))
    s.append(callout(
        "Was im Standard schon drin ist",
        "Impressum &amp; Datenschutz · Premium-Kontaktformular mit Bot-Schutz · "
        "SEO-Optimierung (Basis) · WhatsApp Call-to-Action · 1× Click-to-Load "
        "(OSM-Karte). <b>→ Sie sparen ~15 %</b> gegenüber Starter + Einzel-Paketen."))

    # Trennlinie zwischen den beiden Paketen
    s.append(Spacer(1, 8*mm))
    s.append(hr(c=THREAD_3, thickness=1, spaceBefore=0, spaceAfter=8))

    # --- PREMIUM (Teil von Sektion 3) ---
    s.append(eyebrow("Komplettpaket"))
    s.append(Paragraph("Webseite All-Inclusive", S["h1"]))
    s.append(Spacer(1, 2*mm))
    s += item_row(
        "Webseite Premium (All-in)",
        "2.000&nbsp;€",
        "<b>Ein fester Preis — keine Einzelkalkulation, keine Überraschungen.</b> "
        "Multi-Page-Auftritt (4–6 Detailseiten) mit Karriereseite inkl. Bewerbungs-"
        "formular, Reviews-Slider, Galerie, KI-Content-Boost, vollständigem "
        "SEO-Tuning, Click-to-Load und allen wesentlichen Pixelschneiderei-Modulen.",
        is_main=True,
    )
    s.append(Spacer(1, 4*mm))
    s.append(callout(
        "Was bedeutet &bdquo;All-In&ldquo;?",
        "Sie bekommen, was sonst aus 10–14 einzelnen Paketen zusammengestellt würde "
        "— als ein einziger Festpreis. <b>→ Sie sparen ~20 %</b> gegenüber dem "
        "komplett-individuellen Aufbau aus dem Starter."))

    s.append(PageBreak())
    return s

# ---------------------------------------------------------------------------
# 3.5  Webseiten-Pakete im Vergleich
# ---------------------------------------------------------------------------
def section_websites_compare():
    s = []
    s.append(eyebrow("4 · Auf einen Blick"))
    s.append(Paragraph("Die drei Webseiten-Pakete im Vergleich", S["h1"]))
    s.append(Paragraph(
        "Was ist drin, was kostet's, wie viel sparen Sie gegenüber Einzelkauf:",
        S["lede_left"]))
    s.append(Spacer(1, 4*mm))

    header = ["", "Starter", "Standard", "Premium"]
    sub    = ["Festpreis", "<b>900 €</b>", "<b>1.400 €</b>", "<b>2.000 €</b>"]

    rows = [
        ("Layout",                                "One-Pager", "2–4 Detailseiten", "4–6 Detail + Karriere"),
        ("Impressum &amp; Datenschutz",                  "—", "✓", "✓"),
        ("Kontaktformular (Basis, mailto)",              "✓", "—", "—"),
        ("Kontaktformular (Premium, Bot-Schutz)",        "",  "✓", "✓"),
        ("SEO-Optimierung (Basis)",                      "",  "✓", "✓"),
        ("WhatsApp Call-to-Action",                      "",  "✓", "✓"),
        ("Click-to-Load (1× OSM-Karte)",                 "",  "✓", "✓"),
        ("Bewertungs-Slider",                            "",  "",  "✓"),
        ("Karriereseite + Bewerbungsformular",           "",  "",  "✓"),
        ("Galerie / Bilder-Optimierung (bis 20)",        "",  "",  "✓"),
        ("KI-Content-Boost (10 Bilder + 4 Texte)",       "",  "",  "✓"),
        ("Content-Modal (Datenschutz-Quickinfo)",        "",  "",  "✓"),
        ("Volles Schema.org / Rich Snippets",            "",  "",  "✓"),
    ]

    def cell(t, bold=False, center=True):
        style = S["tc_b"] if bold else S["tc"]
        if center:
            style = ParagraphStyle("c", parent=style, alignment=TA_CENTER)
        return Paragraph(t, style)

    check_style = ParagraphStyle(
        "check", fontName="Helvetica-Bold", fontSize=14,
        textColor=THREAD, alignment=TA_CENTER)

    data = []
    data.append([cell(h, bold=True) for h in header])
    data.append([cell(c, bold=True) for c in sub])
    for r in rows:
        row = [cell(r[0], bold=True, center=False)]
        for col in r[1:]:
            if col == "✓":
                row.append(Paragraph("✓", check_style))
            elif col == "—":
                row.append(cell("—"))
            elif col == "":
                row.append(cell(""))
            else:
                row.append(cell(col))
        data.append(row)

    # Ersparnis-Zeilen (Prozentual, 5er-%, ab 10%)
    # Standard 1400 vs. einzeln: Starter 900 + Impressum 75 + KF Premium 150
    #   + SEO 200 + 4× Extra 200 + WhatsApp 50 + Click-to-Load 50 = 1.625 €
    #   → Save 225 € = 13.8 % → rund 15 %
    # Premium 2000 vs. einzeln: Starter 900 + Impressum 75 + KF Premium 150
    #   + SEO 200 + 5× Extra 250 + WhatsApp 50 + 3× CTL 150 + Karriere 250
    #   + Slider 100 + KI 150 + Bilder 50 + Modal 50 + 2× Produkt 100 = 2.475 €
    #   → Save 475 € = 19.2 % → rund 20 %
    data.append([
        cell("Wert bei Einzelkauf der enthaltenen Module", bold=True, center=False),
        cell("≈ 900 €"),
        cell("≈ 1.625 €"),
        cell("≈ 2.475 €"),
    ])
    data.append([
        Paragraph("<b>Ihre Ersparnis gegenüber Einzelkauf</b>",
                  ParagraphStyle("save_lbl", fontName=SANSB, fontSize=10,
                                  textColor=THREAD)),
        Paragraph("—", ParagraphStyle("save_v", fontName=SANSB, fontSize=11,
                                       textColor=THREAD, alignment=TA_CENTER)),
        Paragraph("<b>~15 %</b>", ParagraphStyle("save_v", fontName=SANSB,
                                                      fontSize=12, textColor=THREAD,
                                                      alignment=TA_CENTER)),
        Paragraph("<b>~20 %</b>", ParagraphStyle("save_v", fontName=SANSB,
                                                      fontSize=13, textColor=THREAD,
                                                      alignment=TA_CENTER)),
    ])

    tbl = Table(data, colWidths=[68*mm, 32*mm, 34*mm, 36*mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,1), PAPER_2),
        ("BACKGROUND", (0,-1), (-1,-1), THREAD_3),
        ("LINEBELOW",  (0,1), (-1,1), 1.2, THREAD),
        ("LINEBELOW",  (0,-2), (-1,-2), 0.6, THREAD),
        ("LINEBELOW",  (0,0), (-1,0), 0.3, LINE_SOFT),
        ("LINEBELOW",  (0,2), (-1,-3), 0.3, LINE_SOFT),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN",      (1,0), (-1,-1), "CENTER"),
        ("ALIGN",      (0,0), (0,-1), "LEFT"),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    s.append(tbl)
    s.append(Spacer(1, 4*mm))

    # Lesart + Premium-Design-Note kombiniert in einer Callout-Box
    s.append(callout(
        "Lesart &amp; Premium-Design",
        "Wir haben die Module der jeweiligen Stufe einzeln aus dem Add-on-Katalog "
        "zusammengezählt und dem Festpreis gegenübergestellt. Die Ersparnis ist real — "
        "wir verdienen am gebündelten Verkauf weniger Stundenkosten und geben die "
        "Differenz an Sie weiter."
        "<br/><br/>"
        "<b>Premium-Design</b> ist in keinem der drei Pakete enthalten — kommt bei "
        "Bedarf als Aufpreis <b>ab 250 €</b> dazu. "
        "<a color='#b1383a' href='https://pixelschneiderei.de/demos/atelier/'>"
        "Beispiel-Seite mit Premium-Design hier als Demo ansehen →</a>"))
    s.append(PageBreak())
    return s

# ---------------------------------------------------------------------------
# 4. Server-Entscheidung
# ---------------------------------------------------------------------------
def section_server():
    s = []
    s.append(eyebrow("5 · Hosting &amp; Inbetriebnahme"))
    s.append(Paragraph("Brauchen Sie einen Server?", S["h1"]))
    s.append(Spacer(1, 3*mm))
    s.append(Paragraph(
        "Eine fertige Webseite muss irgendwo &bdquo;leben&ldquo;. Zwei Wege — "
        "abhängig davon, ob Sie bereits einen Webspace bei einem Anbieter "
        "(Strato, IONOS, All-Inkl., Mittwald, …) haben oder nicht.",
        S["body"]))
    s.append(Spacer(1, 8*mm))

    # A
    s.append(Paragraph(
        "<font color='#b1383a'><b>A · Sie haben bereits einen Server / Webspace</b></font>",
        S["h2"]))
    s.append(Spacer(1, 2*mm))
    s += item_row(
        "Paket: Initiale Einrichtung (Basic)",
        "50 € einmalig",
        "Domain-Verknüpfung, DNS, SSL, Mail-Weiterleitung auf Ihrem bestehenden "
        "Webspace einrichten. Danach läuft die Seite bei Ihrem Anbieter — "
        "wir sind raus aus dem laufenden Betrieb.",
    )
    s.append(Spacer(1, 8*mm))

    # B
    s.append(Paragraph(
        "<font color='#b1383a'><b>B · Sie haben keinen Server</b></font>",
        S["h2"]))
    s.append(Spacer(1, 2*mm))
    s.append(Paragraph(
        "Dann hosten wir Ihre Seite auf Cloudflare Pages — schnell, "
        "DSGVO-konform, mit globalem CDN und automatischer DDoS-Abwehr. "
        "Zwei Posten:",
        S["body"]))
    s.append(Spacer(1, 2*mm))
    s += item_row(
        "Paket: Initiale Einrichtung (Premium)",
        "100 € einmalig",
        "Wie Basic + Cloudflare-Pages-Projekt, Custom-DNS-Records, automatischer "
        "Deploy-Pipeline. <i>Erfordert das jährliche Hosting-Service-Paket "
        "(unten), damit sauberer Betrieb sichergestellt ist.</i>",
    )
    s.append(Spacer(1, 4*mm))
    s += item_row(
        "Service-Paket: SSL, Hosting &amp; Kontaktformular",
        "50 € / Jahr",
        "Betrieb der Seite inkl. SSL-Zertifikat (Auto-Renewal), Cloudflare-Pages-"
        "Hosting und Kontaktformular-Endpunkt über <b>forms.pixelschneiderei.de</b>. "
        "Weitere Aufwände werden über die Stundenpauschale (80&nbsp;€/h) oder ein "
        "höherwertiges Service-Paket abgerechnet.",
    )
    s.append(Spacer(1, 8*mm))
    s.append(callout(
        "Warum Cloudflare?",
        "Cloudflare ist einer der weltweit größten Internet-Infrastruktur-Anbieter "
        "— <b>rund jede fünfte Webseite weltweit</b> wird über Cloudflare ausgeliefert. "
        "Großer Versandhandel, Banken, Vergleichsportale, öffentliche Verwaltung "
        "nutzen es. Sicherheit, Verfügbarkeit und Performance auf Konzern-Niveau, "
        "ohne dass Sie selbst Server-Infrastruktur unterhalten müssen.",
        bg=PAPER_2))
    s.append(PageBreak())
    return s

# ---------------------------------------------------------------------------
# 5. Einzelne Services
# ---------------------------------------------------------------------------
def section_services_single():
    s = []
    s.append(eyebrow("6 · Jährliche Pflege"))
    s.append(Paragraph("Einzelne Services à 25&nbsp;€ / Jahr", S["h1"]))
    s.append(Spacer(1, 3*mm))
    s.append(Paragraph(
        "Hier können Sie genau die jährlichen Services auswählen, die Sie "
        "wirklich brauchen — alle zum Einheitspreis von <b>25&nbsp;€ pro Jahr</b>. "
        "Wenn Ihnen die Auswahl zu unübersichtlich wird, schauen Sie auf der "
        "nächsten Seite die <b>Service-Pakete im Vergleich</b> an — die bündeln "
        "sinnvolle Kombinationen.",
        S["body"]))
    s.append(Spacer(1, 3*mm))
    s.append(Paragraph(
        "<i>Wer die Technik gerne an den Dienstleister abgibt, kann mit unseren "
        "Service-Paketen nur gewinnen. Sie beherrschen Ihr Handwerk — wir das "
        "unsere.</i>",
        S["lede_left"]))
    s.append(Spacer(1, 4*mm))

    services = [
        ("Service: SSL- &amp; Uptime-Monitoring",
         "Laufende Überwachung der Erreichbarkeit und Zertifikats-Gültigkeit, "
         "automatischer Alarm bei Ausfall."),
        ("Service: Security-Header-Review (technisch)",
         "Jährliche technische Aktualisierung von Content-Security-Policy, HSTS, "
         "Permissions-Policy &amp; Co. nach aktuellen OWASP-Empfehlungen."),
        ("Service: Google-Bewertungen",
         "Quartalsweises Einpflegen neuer Kundenstimmen in den Reviews-Slider "
         "inkl. Schema.org-Aktualisierung — aktiver Beleg, dass Ihr Betrieb "
         "läuft und beliebt ist."),
        ("Service: Inhaltsupdate klein (2 / Jahr)",
         "2 kleine Content-Anpassungen pro Jahr, je bis 30&nbsp;Min Arbeit: "
         "Telefonnummer, Öffnungszeit, Absatz tauschen, Bild wechseln. "
         "Mehr Bedarf? → höherwertiges Service-Paket."),
        ("Service: Bewerbungs-Formular-Pflege",
         "Funktionsprüfung des Bewerbungsformulars, JobPosting-validThrough-Datum-"
         "Update, Stellenanzeigen-Anpassung bei Bedarf."),
        ("Service: Bildpflege / Vorher-Nachher",
         "Bis zu 5 vom Kunden gelieferte Bilder pro Jahr werden eingebaut "
         "(Optimierung, Zuschnitt, WebP-Variante, Alt-Text)."),
        ("Service: Karriere-Anzeige-Pflege",
         "Stellenanzeigen aktualisieren, validThrough-Datum prüfen, "
         "Schema.org-JobPosting nach Google-Indexing-Tool validieren."),
    ]
    for n, d in services:
        s += item_row(n, "25 € / Jahr", d)
        s.append(hr())

    s.append(Spacer(1, 4*mm))
    s.append(Paragraph("Stundenpauschale für alles weitere", S["h2"]))
    s += item_row(
        "Entwicklung- &amp; Beratungspauschale",
        "80 € / Stunde",
        "Stundensatz für allgemeine Beratung, Entwicklung und Einrichtung von "
        "IT-Komponenten, die außerhalb der oben gelisteten Pakete liegen. "
        "Transparente Zeiterfassung, vorab abgestimmter Aufwand.")
    s.append(PageBreak())
    return s

# ---------------------------------------------------------------------------
# 6. Service-Pakete im Vergleich
# ---------------------------------------------------------------------------
def section_services_compare():
    s = []
    s.append(eyebrow("7 · Bequemer Weg"))
    s.append(Paragraph("Zu viel Auswahl?", S["h1"]))
    s.append(Paragraph(
        "Service-Pakete im Vergleich — eines davon passt zu fast jedem Kunden:",
        S["lede_left"]))
    s.append(Spacer(1, 4*mm))

    header = ["", "Hosting", "Budget", "Basis", "All-Inc"]
    sub = ["Preis pro Jahr", "<b>50 €</b>", "<b>100 €</b>", "<b>150 €</b>", "<b>200 €</b>"]
    rows = [
        ("SSL + Cloudflare-Hosting + Form-Endpoint",      "✓", "✓", "✓", "✓"),
        ("Impressum-Check (technisch)",                    "", "✓", "✓", "✓"),
        ("Security-Header-Review",                          "", "✓", "✓", "✓"),
        ("Content-Änderungen (klein)",                  "—", "2 / J", "5 / J", "8 / J"),
        ("Google-Bewertungen (quartalsweise)",             "",  "", "✓", "✓"),
        ("Feiertage- &amp; Urlaubs-Refresh",               "",  "", "✓", "✓"),
        ("SEO-Check (jährlich)",                           "",  "",  "", "✓"),
        ("Bewerbungs-Formular-Pflege",                     "",  "",  "", "✓"),
        ("Bildpflege (bis 5 Bilder / Jahr)",               "",  "",  "", "✓"),
        ("Karriere-Anzeige-Pflege",                        "",  "",  "", "✓"),
        ("DNS/Hosting-Wartung",                            "",  "",  "", "✓"),
    ]

    def cell(t, bold=False, center=True):
        style = S["tc_b"] if bold else S["tc"]
        if center:
            style = ParagraphStyle("c", parent=style, alignment=TA_CENTER)
        return Paragraph(t, style)

    check_style2 = ParagraphStyle(
        "check2", fontName="Helvetica-Bold", fontSize=14,
        textColor=THREAD, alignment=TA_CENTER)

    data = []
    data.append([cell(h, bold=True) for h in header])
    data.append([cell(c, bold=True) for c in sub])
    for r in rows:
        row = [cell(r[0], bold=True, center=False)]
        for col in r[1:]:
            if col == "✓":
                row.append(Paragraph("✓", check_style2))
            else:
                row.append(cell(col))
        data.append(row)

    # Ersparnis-Zeilen (% statt €)
    # Budget 100 vs. 125 (Hosting50 + Header25 + Impressum25 + 2 Updates25) → 20%
    # Basis  150 vs. 225 (Budget + Bewertungen25 + Feiertage25 + 3 extra Updates50) → ~30%
    # All-Inc 200 vs. ~375 → ~45-50%
    data.append([
        Paragraph("<b>Wert bei Einzelkauf (à 25 €/Service)</b>",
                  ParagraphStyle("val_lbl", fontName=SANSB, fontSize=9,
                                  textColor=INK_SOFT)),
        cell("≈ 50 €"),  cell("≈ 125 €"),  cell("≈ 225 €"),  cell("≈ 375 €"),
    ])
    data.append([
        Paragraph("<b>Ihre Ersparnis pro Jahr</b>",
                  ParagraphStyle("save_lbl", fontName=SANSB, fontSize=10,
                                  textColor=THREAD)),
        Paragraph("—", ParagraphStyle("save_v", fontName=SANSB, fontSize=11,
                                       textColor=THREAD, alignment=TA_CENTER)),
        Paragraph("<b>~20 %</b>", ParagraphStyle("save_v", fontName=SANSB,
                                                      fontSize=11, textColor=THREAD,
                                                      alignment=TA_CENTER)),
        Paragraph("<b>~30 %</b>", ParagraphStyle("save_v", fontName=SANSB,
                                                      fontSize=12, textColor=THREAD,
                                                      alignment=TA_CENTER)),
        Paragraph("<b>~45 %</b>", ParagraphStyle("save_v", fontName=SANSB,
                                                      fontSize=13, textColor=THREAD,
                                                      alignment=TA_CENTER)),
    ])

    tbl = Table(data, colWidths=[68*mm, 25*mm, 25*mm, 25*mm, 25*mm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,1), PAPER_2),
        ("BACKGROUND", (0,-1), (-1,-1), THREAD_3),
        ("LINEBELOW",  (0,1), (-1,1), 1.2, THREAD),
        ("LINEBELOW",  (0,-2), (-1,-2), 0.6, THREAD),
        ("LINEBELOW",  (0,0), (-1,0), 0.3, LINE_SOFT),
        ("LINEBELOW",  (0,2), (-1,-3), 0.3, LINE_SOFT),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN",      (1,0), (-1,-1), "CENTER"),
        ("ALIGN",      (0,0), (0,-1), "LEFT"),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    s.append(tbl)
    s.append(Spacer(1, 8*mm))

    # „Welches Paket passt zu wem?" — alle 4 Empfehlungen müssen zusammen bleiben.
    recs = [
        ("Hosting · 50 € / Jahr",
         "Sie wollen, dass die Seite läuft. Mehr nicht. Ideal, wenn Sie selbst "
         "Inhalte pflegen oder einen anderen Dienstleister haben."),
        ("Budget · 100 € / Jahr",
         "Sie wollen, dass die Seite läuft <i>und</i> jährlich grundsätzlich "
         "geprüft wird. 2 kleine Content-Änderungen sind inklusive."),
        ("Basis · 150 € / Jahr",
         "<b>Empfehlung für die meisten Kunden.</b> Bewertungen aktuell, "
         "Inhalte gepflegt, kleine Anpassungen drin, Sicherheits-Check inklusive."),
        ("All-Inc · 200 € / Jahr",
         "Sie wollen sich um <i>nichts</i> kümmern. Bewerbungen, Bilder, "
         "SEO-Pflege, Karriere-Anzeigen — alles inklusive. "
         "Bundle-Ersparnis von 50&nbsp;€ gegenüber Einzel-Buchung."),
    ]
    rec_block = [
        Paragraph("Welches Paket passt zu wem?", S["h2"]),
        Spacer(1, 2*mm),
    ]
    for n, d in recs:
        # item_row gibt eine Liste mit einem KeepTogether zurück → flatten
        rec_block += item_row(n, "", d)
        rec_block.append(hr())
    s.append(KeepTogether(rec_block))
    s.append(PageBreak())
    return s

# ---------------------------------------------------------------------------
# 7. Garantien
# ---------------------------------------------------------------------------
def section_guarantees():
    s = []
    s.append(eyebrow("8 · Garantien"))
    s.append(Paragraph("Sourcen, Kündigung, Datenhoheit", S["h1"]))
    s.append(Spacer(1, 4*mm))

    s.append(callout(
        "Die Seite gehört Ihnen — immer.",
        "Alle Inhalte, alle Texte, alle Bilder, der gesamte Quellcode "
        "Ihrer Webseite gehören <b>Ihnen</b>. Sie erhalten zur Abnahme bzw. "
        "Schlussrechnung ein vollständiges <b>.zip-Archiv</b> mit:<br/><br/>"
        "• Den Webseiten-Sourcen (HTML, CSS, JavaScript, Bilder, Schriften)<br/>"
        "• Allen Konfigurationsdateien (DNS-Records, Hosting-Konfig, Mail-Setup)<br/>"
        "• Einer <b>Betriebsanleitung</b> — wie Sie die Seite selbst hosten, "
        "deployen, aktualisieren und um neue Inhalte ergänzen<br/>"
        "• Den Lizenz-Belegen aller verwendeten Schriftarten und Open-Source-Komponenten<br/><br/>"
        "Sie sind <b>nicht abhängig</b> von uns — Sie könnten die Seite jederzeit "
        "selbst weiterführen oder zu einem anderen Dienstleister mitnehmen."))
    s.append(Spacer(1, 6*mm))

    s.append(callout(
        "Service-Pakete: 12 Monate Mindestlaufzeit, danach kündbar.*",
        "Service-Pakete laufen 12&nbsp;Monate und verlängern sich automatisch um "
        "weitere 12&nbsp;Monate, sofern nicht spätestens 1&nbsp;Monat vor Ablauf "
        "gekündigt wird. <b>Beidseitige Kündigung jederzeit zum Monatsende</b> ist "
        "möglich — vorzeitig nicht in Anspruch genommene Folgemonate werden "
        "anteilig erstattet. Volle Details in den "
        "<a color='#b1383a' href='https://pixelschneiderei.de/agb'>AGB §&nbsp;8</a>."))
    s.append(Spacer(1, 6*mm))

    s.append(callout(
        "* Kündigung des Hosting-Service-Pakets — und dann?",
        "Wenn Ihre Seite durch uns auf Cloudflare gehostet wird "
        "(50&nbsp;€/Jahr-Paket) und Sie kündigen, erhalten Sie <b>sofort</b>:"
        "<br/><br/>"
        "• Das vollständige .zip-Archiv (siehe oben)<br/>"
        "• Eine Schritt-für-Schritt-Anleitung, wie Sie die Seite selbst auf "
        "Cloudflare, GitHub Pages, Netlify, Vercel, Strato, IONOS oder einem "
        "beliebigen statischen Hoster wieder ans Laufen bekommen<br/>"
        "• Mindestens <b>30 Tage Übergangsfrist</b> mit Parallel-Betrieb auf "
        "Cloudflare, damit der Wechsel ohne Ausfallzeit erfolgt<br/><br/>"
        "Auf Wunsch richten wir Ihre Seite auch beim Anbieter Ihrer Wahl ein — "
        "über das <b>Paket: Initiale Einrichtung (Basic)</b> für 50&nbsp;€ "
        "einmalig. Damit ist Ihre Webseite spätestens am Folgetag wieder live, "
        "dieses Mal in Ihrer eigenen Verantwortung. "
        "Details siehe <a color='#b1383a' href='https://pixelschneiderei.de/agb'>AGB §&nbsp;9</a>."))
    s.append(Spacer(1, 6*mm))

    s.append(callout(
        "Datenschutz ist nicht aufgesetzt — er ist gebaut.",
        "Pixelschneiderei-Webseiten werden von Grund auf <b>cookie-frei</b>, "
        "<b>tracker-frei</b> und <b>DSGVO-konform</b> gebaut. Keine Google "
        "Fonts über externe CDN, keine Analytics, keine Third-Party-Tracker, "
        "kein &bdquo;akzeptiere alle&ldquo;-Modal. Wenn Drittanbieter-Inhalte "
        "(Karten, Videos) eingebunden werden, dann nur per <b>Click-to-Load</b> "
        "mit ausdrücklicher Einwilligung des Besuchers."))

    s.append(Spacer(1, 10*mm))
    s.append(hr(c=THREAD, thickness=1, spaceBefore=0, spaceAfter=6))
    s.append(Paragraph(
        "<b>Sie wollen Beispiele sehen?</b> Unsere bisherigen Auftritte und "
        "Branchen-Demos finden Sie unter "
        "<font color='#b1383a'><a color='#b1383a' href='https://pixelschneiderei.de/referenzen'>pixelschneiderei.de/referenzen</a></font>.",
        S["body"]))
    s.append(Spacer(1, 3*mm))
    s.append(Paragraph(
        "<b>Vollständige Geschäftsbedingungen</b> unter "
        "<font color='#b1383a'><a color='#b1383a' href='https://pixelschneiderei.de/agb'>pixelschneiderei.de/agb</a></font>.",
        S["body"]))
    s.append(Spacer(1, 6*mm))
    s.append(Paragraph(
        "<b>Fragen?</b> Schreiben Sie uns gerne unter "
        "<font color='#a87b3c'>erik@weisser.dev</font>. Wir nehmen uns Zeit für "
        "die richtige Empfehlung — auch wenn am Ende kleinere Pakete dabei rauskommen.",
        S["body"]))
    s.append(Spacer(1, 4*mm))
    s.append(Paragraph(
        "<i>Mit Liebe geschneidert · pixelschneiderei.de</i>",
        S["muted_i"]))
    return s

# ---------------------------------------------------------------------------
# 9. Zusammenfassung + Prozess (letzte Seite)
# ---------------------------------------------------------------------------
def section_summary():
    s = []
    s.append(PageBreak())
    s.append(eyebrow("9 · Zusammenfassung"))
    s.append(Paragraph("Auf einen Blick", S["h1"]))
    s.append(Spacer(1, 4*mm))

    s.append(callout(
        "Was Sie ab ~975 € bekommen",
        "Eine einfache, responsive Webseite mit Impressum, Datenschutz und "
        "Hosting ist ab <b>~975&nbsp;€</b> möglich (Starter + DSGVO-Paket + "
        "Initiale Einrichtung auf Ihrem Webspace). Mit Cloudflare-Hosting kommen "
        "50&nbsp;€/Jahr Service-Paket hinzu. <br/><br/>"
        "Durch unsere <b>transparente Preisübersicht</b> gibt es keine "
        "unerwarteten Kosten — jeder Baustein hat einen Festpreis, jedes Bundle "
        "eine ausgewiesene Ersparnis."))

    s.append(Spacer(1, 8*mm))
    s.append(Paragraph("So läuft die Zusammenarbeit", S["h2"]))
    s.append(Spacer(1, 2*mm))

    steps = [
        ("1", "Unverbindliches Erstgespräch",
         "Schreiben Sie uns kurz an "
         "<font color='#b1383a'>erik@weisser.dev</font> — wir vereinbaren ein "
         "<b>kostenloses, unverbindliches Beratungsgespräch</b>, entweder "
         "telefonisch oder vor Ort. Sie schildern, was Sie brauchen; wir hören zu, "
         "stellen die richtigen Fragen und beraten Sie ehrlich."),
        ("2", "Bestandsaufnahme &amp; Angebot",
         "Wir nehmen alle Bestandteile auf — gewünschte Pakete, Inhalte, "
         "Sonderwünsche, Zielgruppe, Branche — und erstellen Ihnen ein "
         "<b>schriftliches Angebot</b> mit Festpreis und Liefertermin."),
        ("3", "Bau bis zum ersten Design-Review",
         "Nach Auftragsbestätigung bauen wir Ihre Seite. <b>Innerhalb von ca. "
         "zwei Wochen</b> erhalten Sie das erste Design-Review — eine "
         "live-Vorschau der Seite mit Ihren Inhalten."),
        ("4", "Feedback einarbeiten",
         "Sie geben Feedback, liefern eigene Texte oder Bilder, wünschen "
         "Anpassungen. Wir arbeiten Ihre Rückmeldungen ein und übergeben Ihnen "
         "die <b>finale Version</b>."),
        ("5", "Abnahme &amp; Zahlung",
         "<b>Erst nach Abnahme der finalen Version wird die volle Summe fällig.</b> "
         "Sie zahlen für ein Ergebnis, das Sie gesehen und für gut befunden haben."),
        ("6", "Danach",
         "<b>Nacharbeiten</b> nach Abnahme erfolgen auf Stundenbasis (80&nbsp;€/h). "
         "<b>Inhaltsänderungen</b> sind je nach gebuchtem Service-Paket "
         "jährlich inklusive oder können jederzeit auf Stundenbasis angefragt "
         "werden."),
    ]

    step_rows = []
    for num, title, body in steps:
        step_rows.append([
            Paragraph(num, ParagraphStyle("step_num", fontName=SERIFB,
                                           fontSize=28, leading=32,
                                           textColor=THREAD,
                                           alignment=TA_CENTER)),
            [
                Paragraph(title, ParagraphStyle("step_t", fontName=SERIFB,
                                                 fontSize=13, leading=16,
                                                 textColor=INK,
                                                 spaceAfter=2)),
                Paragraph(body, ParagraphStyle("step_b", fontName=SANS,
                                                 fontSize=9.5, leading=13,
                                                 textColor=INK_SOFT)),
            ],
        ])
    step_tbl = Table(step_rows, colWidths=[14*mm, 156*mm])
    step_tbl.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 2),
        ("RIGHTPADDING", (0,0), (-1,-1), 2),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LINEBELOW", (0,0), (-1,-2), 0.3, LINE_SOFT),
    ]))
    s.append(step_tbl)

    s.append(Spacer(1, 8*mm))
    s.append(hr(c=THREAD, thickness=1, spaceBefore=0, spaceAfter=6))
    s.append(Paragraph(
        "<b>Demos &amp; Referenzen:</b> "
        "<a color='#b1383a' href='https://pixelschneiderei.de'>pixelschneiderei.de</a> · "
        "<b>Kontakt:</b> "
        "<a color='#b1383a' href='mailto:erik@weisser.dev'>erik@weisser.dev</a>",
        S["body"]))
    s.append(Spacer(1, 2*mm))
    s.append(Paragraph(
        "<i>Mit Liebe geschneidert · Pixelschneiderei · Mai 2026</i>",
        S["muted_i"]))
    return s

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def build(out_path):
    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=22*mm, bottomMargin=16*mm,
        title="Pixelschneiderei Preisübersicht 2026",
        author="Pixelschneiderei (Erik Weisser)",
        subject="Preisübersicht",
    )
    story = []
    story += cover()
    story += section_starter()
    story += section_addons()
    story += section_standard_and_premium()
    story += section_websites_compare()
    story += section_server()
    story += section_services_single()
    story += section_services_compare()
    story += section_guarantees()
    story += section_summary()
    doc.build(story, onFirstPage=add_frame, onLaterPages=add_frame)
    print(f"OK: {out_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        out = sys.argv[1]
    else:
        out = os.path.join(SITE_ROOT, "Preisübersicht.pdf")
    build(out)
