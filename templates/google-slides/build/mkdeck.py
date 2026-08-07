#!/usr/bin/env python3
"""nozilla — Google Slides decks: master, icon library, pitch deck.

Built as PPTX (Drive converts on import). White canvas, ink lines, signal green
for action only; sharp corners and hard offset shadows throughout.
"""
import os
from pptx import Presentation
from pptx.util import Inches as In, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import icons as ICONS

S = os.environ.get("SCRATCH", ".")

WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PAPER = RGBColor(0xFF, 0xFE, 0xE5)          # palette reference only
TINT  = RGBColor(0xF2, 0xF2, 0xF0)          # neutral surface tint
INK   = RGBColor(0x00, 0x00, 0x00)
DARK  = RGBColor(0x0C, 0x0C, 0x0A)
GREEN = RGBColor(0x00, 0xFF, 0x9C)
GREY  = RGBColor(0x55, 0x55, 0x55)

DISPLAY, BODY, MONO = "Zilla Slab", "Inter", "Space Mono"
MAIL = "contact@nozilla.de"
W, H = 13.333, 7.5
M = 0.85
CW = W - 2 * M


def deck():
    p = Presentation()
    p.slide_width, p.slide_height = In(W), In(H)
    return p


def slide(prs, bg=WHITE):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    r = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, In(W), In(H))
    r.fill.solid(); r.fill.fore_color.rgb = bg
    r.line.fill.background(); r.shadow.inherit = False
    return s


def rect(s, x, y, w, h, fill=None, line=None, lw=2):
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, In(x), In(y), In(w), In(h))
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line; sh.line.width = Pt(lw)
    sh.shadow.inherit = False
    return sh


def hard_box(s, x, y, w, h, fill=WHITE, line=INK, off=0.07):
    """Hard offset shadow: a solid rectangle behind — never a blur."""
    rect(s, x + off, y + off, w, h, fill=line)
    return rect(s, x, y, w, h, fill=fill, line=line)


def text(s, txt, x, y, w, h, font=BODY, size=17, color=INK, bold=False,
         align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.0, caps=False, wrap=True):
    tb = s.shapes.add_textbox(In(x), In(y), In(w), In(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    for i, line in enumerate(str(txt).split("\n")):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        para.line_spacing = spacing
        run = para.add_run()
        run.text = line.upper() if caps else line
        f = run.font
        f.name, f.size, f.bold = font, Pt(size), bold
        f.color.rgb = color
    return tb


def label(s, txt, x, y, w=6.0, color=GREY):
    return text(s, txt, x, y, w, 0.3, font=MONO, size=11, color=color, caps=True)


NARROW = set("iljtfr.,:;'!|()[]")


def text_w(txt, size):
    """Estimated Zilla Slab Bold width in inches — caps run far wider than lowercase."""
    em = size / 72.0
    w = 0.0
    for ch in txt:
        if ch in "IJ":                     w += 0.40
        elif ch in NARROW:                 w += 0.34
        elif ch == " ":                    w += 0.26
        elif ch.isupper() or ch.isdigit(): w += 0.62
        else:                              w += 0.52
    return w * em * 1.03


def marker(s, txt, x, y, size=54, pad=0.12):
    """Green marker block behind a word — the signature highlight."""
    w = text_w(txt, size) + pad * 2
    h = size / 72.0 * 1.30 + pad * 0.5
    rect(s, x, y, w, h, fill=GREEN)
    text(s, txt, x + pad, y + pad * 0.6, w, h, font=DISPLAY, size=size, bold=True,
         color=INK, wrap=False)
    return x + w


def rule(s, x, y, w, color=INK, pt=2):
    ln = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, In(x), In(y), In(w), Pt(pt))
    ln.fill.solid(); ln.fill.fore_color.rgb = color
    ln.line.fill.background(); ln.shadow.inherit = False


def chrome(s, left, right="// GUTE DIGITALE DIENSTE.", color=GREY, ln=INK):
    label(s, left, M, 0.42, 7.0, color)
    text(s, right, W - M - 5.0, 0.42, 5.0, 0.3, font=MONO, size=11,
         color=color, align=PP_ALIGN.RIGHT, caps=True)
    rule(s, M, 0.78, CW, ln)


def footer(s, page, color=GREY):
    """Footer wordmark stays lowercase and keeps its green period."""
    rule(s, M, H - 0.72, CW, color, 1)
    ICONS.wordmark(s, M, H - 0.60, 0.42, color)
    text(s, str(page), W - M - 2.0, H - 0.58, 2.0, 0.3, font=MONO, size=11,
         color=color, align=PP_ALIGN.RIGHT)


def icon(s, slug, x, y, size=0.9, dark=False):
    ICONS.draw(s, slug, x, y, size, PAPER if dark else INK)


def logo(s, x, y, w=2.2, dark=False):
    ICONS.wordmark(s, x, y, w, PAPER if dark else INK)


# ═══════════════════════════════════════════════════════════════════
# DECK A — Präsentations-Master
# ═══════════════════════════════════════════════════════════════════
prs = deck()

# 1 · Titel (hell)
s = slide(prs)
label(s, "PRÄSENTATION · [KUNDE] · [TT.MM.JJJJ]", M, 0.6)
rule(s, M, 0.95, CW)
text(s, "[TITEL DER", M, 1.9, CW, 1.1, font=DISPLAY, size=64, bold=True, spacing=0.92)
end = marker(s, "PRÄSENTATION", M, 3.05, 64)
text(s, "]", end + 0.06, 3.12, 1.0, 1.0, font=DISPLAY, size=64, bold=True)
text(s, "[Untertitel in einem Satz — was ist die Kernaussage?]", M, 4.45, 8.5, 0.6,
     font=DISPLAY, size=22, color=GREY, spacing=1.2)
rule(s, M, 5.6, CW)
logo(s, M, 5.85, 2.0)
text(s, "[NAME]\n[ROLLE]", W - M - 4.0, 5.85, 4.0, 0.9, font=MONO, size=11,
     color=GREY, align=PP_ALIGN.RIGHT, spacing=1.5, caps=True)

# 2 · Titel (dunkel)
s = slide(prs, DARK)
label(s, "PRÄSENTATION · [KUNDE] · [TT.MM.JJJJ]", M, 0.6, 7.0, PAPER)
rule(s, M, 0.95, CW, PAPER)
text(s, "[TITEL —", M, 1.9, CW, 1.1, font=DISPLAY, size=64, bold=True, color=PAPER, spacing=0.92)
end = marker(s, "DUNKEL", M, 3.05, 64)
text(s, "]", end + 0.06, 3.12, 1.0, 1.0, font=DISPLAY, size=64, bold=True, color=PAPER)
text(s, "[Untertitel — für Bühne und dunkle Räume.]", M, 4.45, 8.5, 0.6,
     font=DISPLAY, size=22, color=PAPER, spacing=1.2)
rule(s, M, 5.6, CW, PAPER)
logo(s, M, 5.85, 2.0, dark=True)

# 3 · Agenda
s = slide(prs); chrome(s, "AGENDA")
text(s, "Agenda.", M, 1.25, 6.0, 0.9, font=DISPLAY, size=46, bold=True)
y = 2.5
for num, t in [("01", "[Ausgangslage]"), ("02", "[Ziel]"), ("03", "[Lösungsansatz]"),
               ("04", "[Vorgehen]"), ("05", "[Nächste Schritte]")]:
    rule(s, M, y - 0.12, CW, GREY, 1)
    text(s, num, M, y, 1.0, 0.4, font=MONO, size=13, color=GREEN, bold=True)
    text(s, t, M + 1.2, y - 0.06, 9.0, 0.5, font=DISPLAY, size=24, bold=True)
    y += 0.82
footer(s, 3)

# 4 · Kapiteltrenner (grün)
s = slide(prs, GREEN)
label(s, "KAPITEL [N]", M, 0.6, 7.0, INK)
rule(s, M, 0.95, CW)
text(s, "[KAPITEL-\nTITEL.]", M, 2.6, CW, 2.2, font=DISPLAY, size=70, bold=True, spacing=0.92)
text(s, "[Ein Satz, worum es in diesem Kapitel geht.]", M, 5.3, 8.0, 0.5,
     font=DISPLAY, size=20, spacing=1.2)

# 5 · Kapiteltrenner (Tinte)
s = slide(prs, DARK)
label(s, "KAPITEL [N]", M, 0.6, 7.0, GREEN)
rule(s, M, 0.95, CW, PAPER)
text(s, "[KAPITEL-\nTITEL.]", M, 2.6, CW, 2.2, font=DISPLAY, size=70, bold=True,
     color=PAPER, spacing=0.92)
text(s, "[Ein Satz, worum es in diesem Kapitel geht.]", M, 5.3, 8.0, 0.5,
     font=DISPLAY, size=20, color=PAPER, spacing=1.2)

# 6 · Fließtext
s = slide(prs); chrome(s, "INHALT")
text(s, "[Überschrift in einem Satz.]", M, 1.25, 9.5, 1.0, font=DISPLAY, size=42,
     bold=True, spacing=1.02)
text(s, "[Fließtext. Direkt, ehrlich, deutsch. Kurze Verben statt langer Substantivketten.\n"
        "Eine Behauptung, die man prüfen kann — mit Beleg, Zahl oder Beispiel.\n\n"
        "[Zweiter Absatz: Kontext und Einordnung.]", M, 2.75, 8.8, 2.5,
     font=BODY, size=17, spacing=1.5)
footer(s, 6)

# 7 · Zwei Spalten
s = slide(prs); chrome(s, "ZWEI SPALTEN")
text(s, "[Überschrift.]", M, 1.25, 9.0, 0.9, font=DISPLAY, size=42, bold=True)
cw2 = (CW - 0.7) / 2
for i, (h, b) in enumerate([("[Links.]", "[Inhalt der linken Spalte. Ein Gedanke pro Spalte.]"),
                            ("[Rechts.]", "[Inhalt der rechten Spalte. Symmetrie hilft beim Lesen.]")]):
    x = M + i * (cw2 + 0.7)
    rect(s, x, 2.6, 0.28, 0.05, fill=GREEN)
    text(s, h, x, 2.85, cw2, 0.5, font=DISPLAY, size=26, bold=True)
    text(s, b, x, 3.5, cw2, 2.0, font=BODY, size=16, spacing=1.5)
footer(s, 7)

# 8 · Drei Karten
cw3 = (CW - 1.0) / 3
s = slide(prs); chrome(s, "DREI KARTEN")
text(s, "[Drei Bausteine.]", M, 1.25, 9.0, 0.9, font=DISPLAY, size=42, bold=True)
for i, (ic, h, b) in enumerate([("grid", "[Struktur]", "[Kurzer Text zur Karte.]"),
                                ("code", "[Technik]", "[Kurzer Text zur Karte.]"),
                                ("spark", "[Wirkung]", "[Kurzer Text zur Karte.]")]):
    x = M + i * (cw3 + 0.5)
    hard_box(s, x, 2.6, cw3, 2.9)
    icon(s, ic, x + 0.35, 2.95, 0.8)
    text(s, h, x + 0.35, 4.05, cw3 - 0.7, 0.4, font=DISPLAY, size=24, bold=True)
    text(s, b, x + 0.35, 4.6, cw3 - 0.7, 0.8, font=BODY, size=15, color=GREY, spacing=1.4)
footer(s, 8)

# 9 · Statement
s = slide(prs)
label(s, "STATEMENT", M, 0.6)
rule(s, M, 0.95, CW)
text(s, "[Ein Satz, der\nfür sich steht.]", M, 2.3, CW, 2.4, font=DISPLAY, size=62,
     bold=True, spacing=0.95)
rect(s, M, 5.2, 1.6, 0.06, fill=GREEN)
text(s, "[Optionale Einordnung in einer Zeile.]", M, 5.5, 8.0, 0.5, font=MONO, size=12,
     color=GREY, caps=True)
footer(s, 9)

# 10 · Zitat
s = slide(prs); chrome(s, "ZITAT")
rect(s, M, 1.7, 0.06, 3.2, fill=GREEN)
text(s, "„[Zitat — eine Aussage, die jemand\nwirklich so sagen würde.]“", M + 0.45, 1.9, 9.5, 2.2,
     font=DISPLAY, size=34, spacing=1.25)
text(s, "[NAME], [ROLLE], [FIRMA]", M + 0.45, 4.5, 8.0, 0.4, font=MONO, size=12,
     color=GREY, caps=True)
footer(s, 10)

# 11 · Kennzahlen
s = slide(prs); chrome(s, "KENNZAHLEN")
text(s, "[Zahlen, die zählen.]", M, 1.25, 9.0, 0.9, font=DISPLAY, size=42, bold=True)
for i, (v, l, d) in enumerate([("[XX] %", "[KENNZAHL]", "[Erläuterung]"),
                               ("[NN]", "[KENNZAHL]", "[Erläuterung]"),
                               ("[X,X]", "[KENNZAHL]", "[Erläuterung]")]):
    x = M + i * (cw3 + 0.5)
    hard_box(s, x, 2.7, cw3, 2.3)
    label(s, l, x + 0.35, 3.05, cw3 - 0.7)
    text(s, v, x + 0.35, 3.45, cw3 - 0.7, 0.9, font=DISPLAY, size=46, bold=True)
    text(s, d, x + 0.35, 4.45, cw3 - 0.7, 0.4, font=BODY, size=14, color=GREY)
footer(s, 11)

# 12 · Vorgehen
s = slide(prs); chrome(s, "VORGEHEN")
text(s, "[Vorgehen in vier Schritten.]", M, 1.25, 10.0, 0.9, font=DISPLAY, size=42, bold=True)
sw = (CW - 1.05) / 4
for i, (n, t, d) in enumerate([("1", "[Analyse]", "[X Wochen]"), ("2", "[Prototyp]", "[X Wochen]"),
                               ("3", "[Bau]", "[X Wochen]"), ("4", "[Launch]", "[X Wochen]")]):
    x = M + i * (sw + 0.35)
    if i < 3:
        rule(s, x + 0.62, 3.05, sw + 0.35 - 0.62, INK)
    rect(s, x, 2.75, 0.62, 0.62, fill=GREEN if i < 2 else WHITE, line=INK)
    text(s, n, x, 2.88, 0.62, 0.4, font=MONO, size=16, bold=True, align=PP_ALIGN.CENTER)
    text(s, t, x, 3.6, sw, 0.4, font=DISPLAY, size=22, bold=True)
    label(s, d, x, 4.05, sw)
footer(s, 12)

# 13 · Tabelle
s = slide(prs); chrome(s, "TABELLE")
text(s, "[Übersicht.]", M, 1.25, 9.0, 0.9, font=DISPLAY, size=42, bold=True)
rows = [("PHASE", "INHALT", "ERGEBNIS", "DAUER"),
        ("1 · Analyse", "[…]", "[…]", "[X W.]"), ("2 · Prototyp", "[…]", "[…]", "[X W.]"),
        ("3 · Bau", "[…]", "[…]", "[X W.]"), ("4 · Launch", "[…]", "[…]", "[X W.]")]
colx, colw = [M, M + 3.4, M + 6.8, M + 9.9], [3.3, 3.3, 3.0, 1.7]
y = 2.6
for ri, row in enumerate(rows):
    head = ri == 0
    for ci, cell in enumerate(row):
        text(s, cell, colx[ci], y, colw[ci], 0.4, font=MONO if head else BODY,
             size=11 if head else 15, bold=head,
             color=INK if head else GREY if ci else INK, caps=head)
    y += 0.32 if head else 0.62
    rule(s, M, y - 0.16, CW, INK if head else RGBColor(0xCC, 0xCC, 0xCC), 2 if head else 1)
footer(s, 13)

# 14 · Bild
s = slide(prs); chrome(s, "BILD")
hard_box(s, M, 1.25, 7.4, 4.9, fill=TINT)
text(s, "[ BILD ERSETZEN ]", M, 3.5, 7.4, 0.5, font=MONO, size=13, color=GREY,
     align=PP_ALIGN.CENTER, caps=True)
text(s, "[Bildunterschrift\nin zwei Zeilen.]", M + 7.9, 1.35, 3.6, 1.4, font=DISPLAY,
     size=28, bold=True, spacing=1.05)
text(s, "[Kontext zum Bild. Wenn Fotografie, dann schwarzweiß mit Korn — nie Stock.]",
     M + 7.9, 3.1, 3.6, 2.0, font=BODY, size=15, color=GREY, spacing=1.45)
footer(s, 14)

# 15 · Leistungen
s = slide(prs); chrome(s, "LEISTUNGEN")
text(s, "[Was wir tun.]", M, 1.25, 9.0, 0.9, font=DISPLAY, size=42, bold=True)
for i, (ic, t) in enumerate([("cursor", "[Interface]"), ("terminal", "[Plattform]"),
                             ("maze", "[Architektur]"), ("chat", "[Beratung]"),
                             ("gear", "[Betrieb]"), ("lightbulb", "[Prototyp]")]):
    x = M + (i % 3) * (cw3 + 0.5)
    y = 2.6 + (i // 3) * 1.75
    icon(s, ic, x, y, 0.75)
    text(s, t, x, y + 0.95, cw3, 0.4, font=DISPLAY, size=21, bold=True)
    text(s, "[Ein Satz dazu.]", x, y + 1.35, cw3, 0.3, font=BODY, size=14, color=GREY)
footer(s, 15)

# 16 · Team
cw4 = (CW - 1.05) / 4
s = slide(prs); chrome(s, "TEAM")
text(s, "[Wer arbeitet daran.]", M, 1.25, 9.0, 0.9, font=DISPLAY, size=42, bold=True)
for i in range(4):
    x = M + i * (cw4 + 0.35)
    hard_box(s, x, 2.6, cw4, 1.6, fill=TINT)
    icon(s, "user", x + cw4 / 2 - 0.4, 2.9, 0.9)
    text(s, "[NAME]", x, 4.4, cw4, 0.4, font=DISPLAY, size=21, bold=True)
    label(s, "[ROLLE]", x, 4.82, cw4)
footer(s, 16)

# 17 · Nächste Schritte
s = slide(prs); chrome(s, "NÄCHSTE SCHRITTE")
text(s, "[Nächste Schritte.]", M, 1.25, 9.0, 0.9, font=DISPLAY, size=42, bold=True)
for i, (w_, who, when) in enumerate([("[Was passiert als Nächstes?]", "[WER]", "[BIS WANN]"),
                                     ("[Zweiter Schritt.]", "[WER]", "[BIS WANN]"),
                                     ("[Dritter Schritt.]", "[WER]", "[BIS WANN]")]):
    y = 2.6 + i * 1.05
    hard_box(s, M, y, CW, 0.85)
    text(s, w_, M + 0.3, y + 0.24, 7.5, 0.4, font=DISPLAY, size=22, bold=True)
    text(s, who, M + 8.4, y + 0.3, 1.6, 0.3, font=MONO, size=12, caps=True)
    text(s, when, M + 10.0, y + 0.3, 1.5, 0.3, font=MONO, size=12, color=GREY,
         align=PP_ALIGN.RIGHT, caps=True)
footer(s, 17)

# 18 · Kontakt
s = slide(prs, DARK)
label(s, "KONTAKT", M, 0.6, 7.0, GREEN)
rule(s, M, 0.95, CW, PAPER)
text(s, "Gute", M, 2.2, CW, 1.1, font=DISPLAY, size=68, bold=True, color=PAPER)
marker(s, "digitale", M + text_w("Gute", 68) + 0.20, 2.16, 68)
text(s, "Dienste.", M, 3.5, CW, 1.1, font=DISPLAY, size=68, bold=True, color=PAPER)
rule(s, M, 5.15, CW, PAPER)
text(s, "[NAME] · [ROLLE]\n" + MAIL + " · nozilla.de", M, 5.4, 6.0, 1.0, font=MONO,
     size=13, color=PAPER, spacing=1.6)
logo(s, W - M - 2.4, 5.5, 2.0, dark=True)

# 19 · Stil-Referenz
s = slide(prs); chrome(s, "STIL-REFERENZ")
text(s, "Farbe & Typo.", M, 1.25, 9.0, 0.9, font=DISPLAY, size=42, bold=True)
for i, (c, n, hexv) in enumerate([(GREEN, "SIGNAL", "#00FF9C"), (PAPER, "PAPIER", "#FFFEE5"),
                                  (INK, "TINTE", "#000000"), (DARK, "INK 900", "#0C0C0A")]):
    x = M + i * (cw4 + 0.35)
    rect(s, x, 2.6, cw4, 1.15, fill=c, line=INK)
    label(s, n, x, 3.85, cw4, INK)
    text(s, hexv, x, 4.12, cw4, 0.3, font=MONO, size=12, color=GREY)
rule(s, M, 4.85, CW, GREY, 1)
text(s, "Zilla Slab Bold — Display", M, 5.05, 6.0, 0.5, font=DISPLAY, size=26, bold=True)
text(s, "Inter Regular — Fließtext, 17 pt", M, 5.65, 6.0, 0.4, font=BODY, size=17)
text(s, "SPACE MONO — LABELS", M, 6.1, 6.0, 0.4, font=MONO, size=12, caps=True)
text(s, "Radius 0 · harte Schatten (6px Offset) ·\nkeine Verläufe, kein Blur, kein Glas.",
     M + 7.0, 5.05, 4.5, 1.2, font=BODY, size=15, color=GREY, spacing=1.45)
footer(s, 19)

prs.save(f"{S}/nozilla-slides-master.pptx")
print("master:", len(prs.slides._sldIdLst), "slides")


# ═══════════════════════════════════════════════════════════════════
# DECK B — Icon-Bibliothek
# ═══════════════════════════════════════════════════════════════════
lib = deck()
HEAVY = [(s_, l_) for s_, l_, _ in ICONS.HEAVY]
PIXEL = [(s_, l_) for s_, l_, _ in ICONS.PIXEL]

s = slide(lib)
label(s, "DESIGN SYSTEM · BIBLIOTHEK", M, 0.6)
rule(s, M, 0.95, CW)
text(s, "Icon-", M, 2.2, CW, 1.2, font=DISPLAY, size=68, bold=True)
marker(s, "Bibliothek", M, 3.35, 68)
text(s, f"{len(HEAVY) + len(PIXEL)} Icons · zwei Dialekte · hell und dunkel.\n"
        "Zum Kopieren und Einsetzen.", M, 4.9, 8.0, 1.0, font=DISPLAY, size=22,
     color=GREY, spacing=1.25)
rule(s, M, 6.2, CW)
logo(s, M, 6.45, 2.0)

PER = 18          # 6 columns × 3 rows
COLS = 6
GAP = 0.18
CELLW = (CW - (COLS - 1) * GAP) / COLS
TILEH = 1.28      # sized so row 3 + its label clears the footer rule
PITCH = 1.70
TOP = 1.62


def icon_page(items, dark, title, page):
    sl = slide(lib, DARK if dark else WHITE)
    fg = PAPER if dark else INK
    if dark:
        label(sl, "DIALEKT A · INVERTIERT", M, 0.42, 7.0, PAPER)
        text(sl, "// AUF TINTE-SCHWARZ", W - M - 5.0, 0.42, 5.0, 0.3, font=MONO, size=11,
             color=PAPER, align=PP_ALIGN.RIGHT, caps=True)
        rule(sl, M, 0.78, CW, PAPER)
    else:
        chrome(sl, "DIALEKT A · HEAVY-STROKE")
    text(sl, title, M, 1.02, 9.0, 0.6, font=DISPLAY, size=30, bold=True, color=fg)
    for i, (slug, nm) in enumerate(items):
        x = M + (i % COLS) * (CELLW + GAP)
        y = TOP + (i // COLS) * PITCH
        rect(sl, x, y, CELLW, TILEH, fill=None, line=fg)
        icon(sl, slug, x + CELLW / 2 - 0.37, y + (TILEH - 0.74) / 2, 0.74, dark=dark)
        text(sl, nm, x, y + TILEH + 0.07, CELLW, 0.28, font=MONO, size=10,
             color=PAPER if dark else GREY, align=PP_ALIGN.CENTER, caps=True)
    if dark:
        rule(sl, M, H - 0.72, CW, PAPER, 1)
        ICONS.wordmark(sl, M, H - 0.60, 0.42, PAPER)
    else:
        footer(sl, page)
    return sl


pages = [HEAVY[i:i + PER] for i in range(0, len(HEAVY), PER)]
pg = 2
for n, chunk in enumerate(pages, 1):
    icon_page(chunk, False, f"Heavy-Stroke {n}/{len(pages)}.", pg); pg += 1
for n, chunk in enumerate(pages, 1):
    icon_page(chunk, True, f"Heavy-Stroke {n}/{len(pages)}, invertiert.", pg); pg += 1

# Pixel + Wortmarke
s = slide(lib); chrome(s, "DIALEKT B · PIXEL-ART & WORTMARKE")
text(s, "Pixel-Art.", M, 1.02, 9.0, 0.6, font=DISPLAY, size=30, bold=True)
for i, (slug, nm) in enumerate(PIXEL):
    x = M + i * 2.3
    rect(s, x, 1.7, 2.0, 1.95, fill=None, line=INK)
    icon(s, slug, x + 0.5, 1.9, 1.25)
    text(s, nm, x, 3.32, 2.0, 0.3, font=MONO, size=10, color=GREY,
         align=PP_ALIGN.CENTER, caps=True)
text(s, "8-Bit-Reminiszenzen — sparsam,\nals retro-digitale Interpunktion.",
     M + 9.6, 1.95, 2.6, 1.0, font=BODY, size=15, color=GREY, spacing=1.45)
text(s, "Wortmarke.", M, 4.05, 9.0, 0.6, font=DISPLAY, size=30, bold=True)
for i, (bg, dark_) in enumerate([(WHITE, False), (GREEN, False), (INK, True)]):
    x = M + i * 3.7
    rect(s, x, 4.75, 3.4, 1.35, fill=bg, line=INK)
    ICONS.wordmark(s, x + 0.45, 5.1, 2.3, PAPER if dark_ else INK)
text(s, "WEISS · SIGNAL-GRÜN · TINTE-SCHWARZ", M, 6.25, 9.0, 0.3, font=MONO,
     size=10, color=GREY, caps=True)
footer(s, pg); pg += 1

# Verwendung
s = slide(lib); chrome(s, "VERWENDUNG")
text(s, "So verwendest du die Icons.", M, 1.15, 10.0, 0.7, font=DISPLAY, size=34, bold=True)
y = 2.3
for h, b in [("Kopieren", "Icon anklicken, Strg/Cmd + C — und in deine Folie einfügen."),
             ("Skalieren", "Immer proportional. Zielgröße 48–160 px, nie verzerren."),
             ("Farbe", "Echte Vektoren: Form anklicken und umfärben. Grün nur als Akzent."),
             ("Verboten", "Keine Emoji, keine Icon-Fonts, keine fremden Icon-Sets.")]:
    rect(s, M, y + 0.06, 0.28, 0.05, fill=GREEN)
    text(s, h, M + 0.45, y, 3.0, 0.4, font=DISPLAY, size=22, bold=True)
    text(s, b, M + 3.7, y + 0.04, 7.8, 0.5, font=BODY, size=16, color=GREY)
    y += 0.95
footer(s, pg)

lib.save(f"{S}/nozilla-slides-icons.pptx")
print("icons:", len(lib.slides._sldIdLst), "slides")


# ═══════════════════════════════════════════════════════════════════
# DECK C — Pitch Deck
# ═══════════════════════════════════════════════════════════════════
p = deck()

# 1 · Titel
s = slide(p)
label(s, "PITCH · [KUNDE] · [TT.MM.JJJJ]", M, 0.6)
rule(s, M, 0.95, CW)
text(s, "[Wir lösen", M, 1.9, CW, 1.1, font=DISPLAY, size=62, bold=True, spacing=0.92)
end = marker(s, "ein Problem", M, 3.0, 62)
text(s, ",]", end + 0.06, 3.06, 1.4, 1.0, font=DISPLAY, size=62, bold=True)
text(s, "[das Sie täglich Geld kostet.]", M, 4.15, CW, 1.0, font=DISPLAY, size=62,
     bold=True, spacing=0.92)
rule(s, M, 5.7, CW)
logo(s, M, 5.95, 2.0)
text(s, "[NAME] · [ROLLE]\n" + MAIL, W - M - 4.0, 5.95, 4.0, 0.9, font=MONO, size=11,
     color=GREY, align=PP_ALIGN.RIGHT, spacing=1.5)

# 2 · Problem
s = slide(p); chrome(s, "01 · PROBLEM")
text(s, "[Das Problem.]", M, 1.25, 9.0, 0.9, font=DISPLAY, size=44, bold=True)
for i, (ic, t, b) in enumerate([("warning", "[Symptom 1]", "[Was passiert heute — messbar.]"),
                                ("clock", "[Symptom 2]", "[Was es kostet — in Zeit oder Geld.]"),
                                ("close", "[Symptom 3]", "[Was dadurch nicht geht.]")]):
    x = M + i * (cw3 + 0.5)
    icon(s, ic, x, 2.6, 0.8)
    text(s, t, x, 3.6, cw3, 0.4, font=DISPLAY, size=24, bold=True)
    text(s, b, x, 4.1, cw3, 1.0, font=BODY, size=15, color=GREY, spacing=1.45)
footer(s, 2)

# 3 · Warum jetzt
s = slide(p); chrome(s, "02 · WARUM JETZT")
text(s, "[Warum jetzt?]", M, 1.25, 9.0, 0.9, font=DISPLAY, size=44, bold=True)
text(s, "[Ein Satz, der den Zeitdruck begründet — Markt, Technik, Regulierung oder\n"
        "schlicht: die Altlast wird teurer als der Umbau.]", M, 2.6, 9.5, 1.4,
     font=DISPLAY, size=26, spacing=1.25)
rect(s, M, 4.4, 2.0, 0.06, fill=GREEN)
text(s, "[Beleg: Zahl, Studie oder eigene Messung.]", M, 4.7, 9.0, 0.5, font=MONO,
     size=12, color=GREY, caps=True)
footer(s, 3)

# 4 · Lösung
s = slide(p); chrome(s, "03 · LÖSUNG")
text(s, "[Unsere Lösung.]", M, 1.25, 9.0, 0.9, font=DISPLAY, size=44, bold=True)
hard_box(s, M, 2.5, CW, 2.5, fill=WHITE)
icon(s, "target", M + 0.5, 2.95, 1.0)
text(s, "[In einem Satz: was wir bauen und was danach anders ist.]",
     M + 2.0, 3.05, 9.0, 1.4, font=DISPLAY, size=28, bold=True, spacing=1.15)
text(s, "[Zweite Zeile: die Einschränkung, ehrlich benannt.]", M + 2.0, 4.35, 9.0, 0.4,
     font=BODY, size=15, color=GREY)
footer(s, 4)

# 5 · Wie es funktioniert
s = slide(p); chrome(s, "04 · SO FUNKTIONIERT ES")
text(s, "[So funktioniert es.]", M, 1.25, 10.0, 0.9, font=DISPLAY, size=44, bold=True)
for i, (n, t, d) in enumerate([("1", "[Erfassen]", "[Was rein geht.]"),
                               ("2", "[Verarbeiten]", "[Was passiert.]"),
                               ("3", "[Ausliefern]", "[Was raus kommt.]"),
                               ("4", "[Messen]", "[Woran wir es prüfen.]")]):
    x = M + i * (sw + 0.35)
    if i < 3:
        rule(s, x + 0.62, 3.05, sw + 0.35 - 0.62, INK)
    rect(s, x, 2.75, 0.62, 0.62, fill=GREEN, line=INK)
    text(s, n, x, 2.88, 0.62, 0.4, font=MONO, size=16, bold=True, align=PP_ALIGN.CENTER)
    text(s, t, x, 3.6, sw, 0.4, font=DISPLAY, size=22, bold=True)
    text(s, d, x, 4.05, sw, 0.6, font=BODY, size=14, color=GREY, spacing=1.4)
footer(s, 5)

# 6 · Produkt
s = slide(p); chrome(s, "05 · PRODUKT")
hard_box(s, M, 1.25, 7.4, 4.9, fill=TINT)
text(s, "[ SCREENSHOT ERSETZEN ]", M, 3.5, 7.4, 0.5, font=MONO, size=13, color=GREY,
     align=PP_ALIGN.CENTER, caps=True)
text(s, "[Was man hier sieht.]", M + 7.9, 1.35, 3.6, 1.0, font=DISPLAY, size=28,
     bold=True, spacing=1.05)
text(s, "[Drei Sätze zum Screen: was der Nutzer tut, was das System tut,\n"
        "warum es schneller ist als vorher.]", M + 7.9, 2.6, 3.6, 2.2, font=BODY,
     size=15, color=GREY, spacing=1.45)
footer(s, 6)

# 7 · Nutzen
s = slide(p); chrome(s, "06 · NUTZEN")
text(s, "[Was es bringt.]", M, 1.25, 9.0, 0.9, font=DISPLAY, size=44, bold=True)
for i, (v, l, d) in enumerate([("[−XX] %", "[AUFWAND]", "[Womit gemessen?]"),
                               ("[+XX] %", "[DURCHSATZ]", "[Womit gemessen?]"),
                               ("[X] Wo.", "[TIME TO VALUE]", "[Ab wann spürbar?]")]):
    x = M + i * (cw3 + 0.5)
    hard_box(s, x, 2.7, cw3, 2.3)
    label(s, l, x + 0.35, 3.05, cw3 - 0.7)
    text(s, v, x + 0.35, 3.45, cw3 - 0.7, 0.9, font=DISPLAY, size=44, bold=True)
    text(s, d, x + 0.35, 4.45, cw3 - 0.7, 0.4, font=BODY, size=14, color=GREY)
footer(s, 7)

# 8 · Warum nozilla
s = slide(p); chrome(s, "07 · WARUM NOZILLA")
text(s, "Warum nozilla.", M, 1.25, 9.0, 0.9, font=DISPLAY, size=44, bold=True)
for i, (ic, t, b) in enumerate([("check", "Direkt", "Wir sagen, was geht — und was nicht."),
                                ("gear", "Handwerklich", "Linien werden gezogen, nicht gefiltert."),
                                ("rocket", "Inkrementell", "Ablösen ohne Stillstand, mit Messpunkten.")]):
    x = M + i * (cw3 + 0.5)
    hard_box(s, x, 2.6, cw3, 2.7)
    icon(s, ic, x + 0.35, 2.95, 0.8)
    text(s, t, x + 0.35, 4.0, cw3 - 0.7, 0.4, font=DISPLAY, size=24, bold=True)
    text(s, b, x + 0.35, 4.5, cw3 - 0.7, 0.8, font=BODY, size=15, color=GREY, spacing=1.4)
footer(s, 8)

# 9 · Referenz
s = slide(p); chrome(s, "08 · REFERENZ")
text(s, "[Referenz: [PROJEKT].]", M, 1.25, 10.0, 0.9, font=DISPLAY, size=40, bold=True)
rect(s, M, 2.5, 0.06, 2.0, fill=GREEN)
text(s, "„[Kundenzitat — konkret, ohne Superlative.]“", M + 0.45, 2.6, 8.5, 1.2,
     font=DISPLAY, size=28, spacing=1.25)
text(s, "[NAME], [ROLLE], [FIRMA]", M + 0.45, 4.0, 8.0, 0.4, font=MONO, size=12,
     color=GREY, caps=True)
for i, (v, l) in enumerate([("[XX] %", "[ERGEBNIS]"), ("[NN]", "[ERGEBNIS]")]):
    x = M + 8.4 + i * 1.7
    text(s, v, x, 2.6, 1.6, 0.6, font=DISPLAY, size=32, bold=True)
    label(s, l, x, 3.25, 1.6)
footer(s, 9)

# 10 · Team
s = slide(p); chrome(s, "09 · TEAM")
text(s, "[Wer es baut.]", M, 1.25, 9.0, 0.9, font=DISPLAY, size=44, bold=True)
for i in range(4):
    x = M + i * (cw4 + 0.35)
    hard_box(s, x, 2.6, cw4, 1.6, fill=TINT)
    icon(s, "user", x + cw4 / 2 - 0.4, 2.9, 0.9)
    text(s, "[NAME]", x, 4.4, cw4, 0.4, font=DISPLAY, size=21, bold=True)
    label(s, "[ROLLE]", x, 4.82, cw4)
footer(s, 10)

# 11 · Investition
s = slide(p); chrome(s, "10 · INVESTITION")
text(s, "[Investition.]", M, 1.25, 9.0, 0.9, font=DISPLAY, size=44, bold=True)
for i, (t, d, price) in enumerate([("[Phase 1 · Analyse]", "[Was drin ist.]", "[€ …]"),
                                   ("[Phase 2 · Bau]", "[Was drin ist.]", "[€ …]"),
                                   ("[Phase 3 · Betrieb]", "[Was drin ist.]", "[€ … / Monat]")]):
    y = 2.6 + i * 1.05
    hard_box(s, M, y, CW, 0.85)
    text(s, t, M + 0.3, y + 0.24, 5.5, 0.4, font=DISPLAY, size=22, bold=True)
    text(s, d, M + 6.0, y + 0.3, 3.5, 0.3, font=BODY, size=14, color=GREY)
    text(s, price, M + 9.6, y + 0.24, 1.9, 0.4, font=MONO, size=15, bold=True,
         align=PP_ALIGN.RIGHT)
text(s, "[Festpreis oder Aufwand — und was ausdrücklich nicht enthalten ist.]",
     M, 5.95, 10.0, 0.4, font=BODY, size=14, color=GREY)
footer(s, 11)

# 12 · Nächster Schritt
s = slide(p, DARK)
label(s, "NÄCHSTER SCHRITT", M, 0.6, 7.0, GREEN)
rule(s, M, 0.95, CW, PAPER)
text(s, "[Lassen Sie uns", M, 2.1, CW, 1.1, font=DISPLAY, size=58, bold=True, color=PAPER)
end = marker(s, "anfangen", M, 3.2, 58)
text(s, ".]", end + 0.06, 3.26, 1.0, 1.0, font=DISPLAY, size=58, bold=True, color=PAPER)
text(s, "[Konkret: WER macht WAS bis WANN.]", M, 4.5, 9.0, 0.5, font=DISPLAY,
     size=22, color=PAPER)
rule(s, M, 5.3, CW, PAPER)
text(s, "[NAME] · [ROLLE]\n" + MAIL + " · nozilla.de", M, 5.55, 6.0, 1.0, font=MONO,
     size=13, color=PAPER, spacing=1.6)
logo(s, W - M - 2.4, 5.65, 2.0, dark=True)

p.save(f"{S}/nozilla-slides-pitch.pptx")
print("pitch:", len(p.slides._sldIdLst), "slides")
