"""nozilla icons — one source, two outputs.

Every icon is defined once on a 64-unit grid with a 4-unit stroke (square caps,
miter joins) and can be rendered either as native PPTX vector shapes (sharp and
recolourable inside Google Slides) or exported as SVG for the web — so the deck
and project/assets/ can never drift apart.
"""
from pptx.util import Pt, Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

GREEN = RGBColor(0x00, 0xFF, 0x9C)
GREEN_DEEP = RGBColor(0x00, 0xC0, 0x75)
GREEN_SOFT = RGBColor(0xB7, 0xFF, 0xE0)
G = 64.0


def _emu(v):
    return Emu(int(round(v)))


# ── Renderer A: native PPTX shapes ────────────────────────────────────────
class Pen:
    def __init__(self, slide, x, y, size, color, stroke=4.0):
        self.s = slide
        self.x0, self.y0 = x * 914400.0, y * 914400.0
        self.k = size * 914400.0 / G
        self.color = color
        self.wpt = Pt(size * (stroke / G) * 72.0)

    def X(self, u): return self.x0 + u * self.k
    def Y(self, v): return self.y0 + v * self.k

    def _plain(self, sh):
        sh.shadow.inherit = False
        return sh

    def line(self, x1, y1, x2, y2):
        from pptx.enum.shapes import MSO_CONNECTOR
        c = self.s.shapes.add_connector(
            MSO_CONNECTOR.STRAIGHT, _emu(self.X(x1)), _emu(self.Y(y1)),
            _emu(self.X(x2)), _emu(self.Y(y2)))
        c.line.color.rgb = self.color
        c.line.width = self.wpt
        return self._plain(c)

    def rect(self, x, y, w, h, fill=None):
        sh = self.s.shapes.add_shape(MSO_SHAPE.RECTANGLE, _emu(self.X(x)), _emu(self.Y(y)),
                                     _emu(w * self.k), _emu(h * self.k))
        if fill is None:
            sh.fill.background()
        else:
            sh.fill.solid(); sh.fill.fore_color.rgb = fill
        sh.line.color.rgb = self.color
        sh.line.width = self.wpt
        return self._plain(sh)

    def solid(self, x, y, w, h, fill):
        sh = self.s.shapes.add_shape(MSO_SHAPE.RECTANGLE, _emu(self.X(x)), _emu(self.Y(y)),
                                     _emu(w * self.k), _emu(h * self.k))
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
        sh.line.fill.background()
        return self._plain(sh)

    def circle(self, cx, cy, r, fill=None):
        sh = self.s.shapes.add_shape(MSO_SHAPE.OVAL, _emu(self.X(cx - r)), _emu(self.Y(cy - r)),
                                     _emu(2 * r * self.k), _emu(2 * r * self.k))
        if fill is None:
            sh.fill.background()
        else:
            sh.fill.solid(); sh.fill.fore_color.rgb = fill
        sh.line.color.rgb = self.color
        sh.line.width = self.wpt
        return self._plain(sh)

    def dot(self, cx, cy, r, fill):
        sh = self.s.shapes.add_shape(MSO_SHAPE.OVAL, _emu(self.X(cx - r)), _emu(self.Y(cy - r)),
                                     _emu(2 * r * self.k), _emu(2 * r * self.k))
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
        sh.line.fill.background()
        return self._plain(sh)

    def poly(self, pts, close=False, fill=None):
        ff = self.s.shapes.build_freeform(_emu(self.X(pts[0][0])), _emu(self.Y(pts[0][1])))
        ff.add_line_segments([(_emu(self.X(x)), _emu(self.Y(y))) for x, y in pts[1:]], close=close)
        sh = ff.convert_to_shape()
        if fill is None:
            sh.fill.background()
        else:
            sh.fill.solid(); sh.fill.fore_color.rgb = fill
        sh.line.color.rgb = self.color
        sh.line.width = self.wpt
        return self._plain(sh)


# ── Renderer B: SVG ───────────────────────────────────────────────────────
def _hex(c):
    return "#%02X%02X%02X" % (c[0], c[1], c[2]) if not isinstance(c, str) else c


class SvgPen:
    """Same drawing API, emits SVG — keeps web assets identical to the deck."""

    def __init__(self, color="#000000", stroke=4.0):
        self.color = color
        self.sw = stroke
        self.out = []

    def line(self, x1, y1, x2, y2):
        self.out.append(f'<path d="M{x1} {y1} L{x2} {y2}"/>')

    def rect(self, x, y, w, h, fill=None):
        f = f' fill="{_hex(fill)}"' if fill is not None else ''
        self.out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}"{f}/>')

    def solid(self, x, y, w, h, fill):
        self.out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                        f'fill="{_hex(fill)}" stroke="none"/>')

    def circle(self, cx, cy, r, fill=None):
        f = f' fill="{_hex(fill)}"' if fill is not None else ''
        self.out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}"{f}/>')

    def dot(self, cx, cy, r, fill):
        self.out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{_hex(fill)}" stroke="none"/>')

    def poly(self, pts, close=False, fill=None):
        d = "M" + " L".join(f"{x} {y}" for x, y in pts) + (" Z" if close else "")
        f = f' fill="{_hex(fill)}"' if fill is not None else ''
        self.out.append(f'<path d="{d}"{f}/>')

    def svg(self, label):
        body = "\n  ".join(self.out)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none" '
                f'stroke="{self.color}" stroke-width="{self.sw}" stroke-linecap="square" '
                f'stroke-linejoin="miter" role="img" aria-label="{label}">\n  {body}\n</svg>\n')


# ── Dialekt A — Heavy-Stroke ──────────────────────────────────────────────
def i_grid(p):
    for x, y in ((10, 10), (36, 10), (10, 36), (36, 36)):
        p.rect(x, y, 18, 18)


def i_cursor(p):
    p.poly([(18, 12), (18, 46), (27, 38), (33, 52), (39, 49), (33, 36), (44, 36)], close=True)


def i_maze(p):
    p.poly([(12, 12), (52, 12), (52, 52), (20, 52), (20, 20), (44, 20),
            (44, 44), (28, 44), (28, 28), (36, 28)])


def i_terminal(p):
    p.rect(8, 12, 48, 40); p.line(8, 23, 56, 23)
    p.poly([(16, 33), (22, 38), (16, 43)]); p.line(28, 43, 42, 43)


def i_chat(p):
    p.poly([(10, 12), (54, 12), (54, 40), (26, 40), (16, 50), (16, 40), (10, 40)], close=True)
    for cx in (24, 32, 40):
        p.dot(cx, 26, 2.4, p.color)


def i_spark(p):
    p.poly([(32, 8), (37, 27), (56, 32), (37, 37), (32, 56), (27, 37), (8, 32), (27, 27)],
           close=True, fill=GREEN)


def i_arrow(p):
    p.line(10, 32, 50, 32); p.poly([(38, 20), (52, 32), (38, 44)])


def i_user(p):
    p.circle(32, 22, 10); p.poly([(14, 52), (18, 43), (32, 39), (46, 43), (50, 52)])


def i_gear(p):
    p.circle(32, 32, 15); p.circle(32, 32, 5)
    for a, b, c, d in ((47, 32, 53, 32), (32, 47, 32, 53), (17, 32, 11, 32), (32, 17, 32, 11),
                       (42.6, 42.6, 47, 47), (21.4, 42.6, 17, 47),
                       (21.4, 21.4, 17, 17), (42.6, 21.4, 47, 17)):
        p.line(a, b, c, d)


def i_folder(p):
    p.poly([(10, 20), (26, 20), (31, 26), (54, 26), (54, 48), (10, 48)], close=True)


def i_lightbulb(p):
    p.circle(32, 26, 14, fill=GREEN); p.line(24, 44, 40, 44); p.line(26, 50, 38, 50)


def i_code(p):
    p.poly([(24, 18), (12, 32), (24, 46)]); p.poly([(40, 18), (52, 32), (40, 46)])
    p.line(36, 14, 28, 50)


def i_calendar(p):
    p.rect(9, 16, 46, 38); p.line(9, 27, 55, 27)
    p.line(21, 10, 21, 20); p.line(43, 10, 43, 20)
    for x in (18, 30, 42):
        p.solid(x, 34, 6, 6, p.color)
    p.solid(18, 44, 6, 6, GREEN)


def i_clock(p):
    p.circle(32, 32, 21); p.line(32, 32, 32, 19); p.line(32, 32, 43, 32)


def i_chart(p):
    p.line(12, 12, 12, 52); p.line(12, 52, 54, 52)
    p.solid(19, 34, 9, 18, p.color); p.solid(32, 26, 9, 26, p.color)
    p.solid(45, 16, 9, 36, GREEN)


def i_target(p):
    p.circle(32, 32, 21); p.circle(32, 32, 11); p.dot(32, 32, 4.5, GREEN)


def i_lock(p):
    p.rect(13, 29, 38, 25)
    p.poly([(22, 29), (22, 20), (32, 13), (42, 20), (42, 29)])
    p.dot(32, 41, 3.5, GREEN)


def i_server(p):
    p.rect(9, 12, 46, 14); p.rect(9, 30, 46, 14)
    p.solid(15, 17, 5, 4, GREEN); p.solid(15, 35, 5, 4, p.color)
    p.line(9, 50, 55, 50)


def i_mobile(p):
    p.rect(20, 8, 24, 48); p.line(27, 15, 37, 15); p.line(26, 49, 38, 49)


def i_monitor(p):
    p.rect(8, 12, 48, 31); p.line(32, 43, 32, 52); p.line(22, 52, 42, 52)


def i_search(p):
    p.circle(28, 28, 14); p.line(38, 38, 53, 53)


def i_mail(p):
    p.rect(8, 16, 48, 32); p.poly([(8, 16), (32, 36), (56, 16)])


def i_warning(p):
    p.poly([(32, 9), (56, 53), (8, 53)], close=True)
    p.line(32, 26, 32, 40); p.dot(32, 47, 2.6, p.color)


def i_check(p):
    p.poly([(12, 34), (26, 48), (52, 16)])


def i_close(p):
    p.line(14, 14, 50, 50); p.line(50, 14, 14, 50)


def i_plus(p):
    p.line(32, 12, 32, 52); p.line(12, 32, 52, 32)


def i_external(p):
    p.poly([(10, 22), (10, 54), (42, 54), (42, 34)])
    p.poly([(34, 10), (54, 10), (54, 30)]); p.line(54, 10, 32, 32)


def i_rocket(p):
    p.poly([(32, 8), (42, 27), (42, 45), (22, 45), (22, 27)], close=True)
    p.poly([(22, 34), (13, 51), (22, 45)]); p.poly([(42, 34), (51, 51), (42, 45)])
    p.dot(32, 25, 4.5, GREEN)


def i_pen(p):
    p.poly([(13, 51), (17, 39), (43, 13), (51, 21), (25, 47)], close=True)
    p.line(39, 17, 47, 25)


def i_trash(p):
    p.line(9, 19, 55, 19); p.rect(16, 19, 32, 35); p.rect(26, 10, 12, 9)
    p.line(27, 28, 27, 45); p.line(37, 28, 37, 45)


def i_filter(p):
    p.poly([(9, 13), (55, 13), (38, 32), (38, 53), (26, 45), (26, 32)], close=True)


def i_book(p):
    p.rect(10, 13, 44, 38); p.line(32, 13, 32, 51)
    p.line(17, 24, 26, 24); p.line(38, 24, 47, 24)


def i_bell(p):
    p.poly([(20, 43), (20, 28), (32, 16), (44, 28), (44, 43)], close=True)
    p.line(13, 43, 51, 43); p.dot(32, 50, 3.4, GREEN)


# ── Dialekt B — Pixel-Art ─────────────────────────────────────────────────
_CUKE_BODY = [(40, 12), (44, 12), (36, 16), (40, 16), (44, 16), (32, 20), (36, 20), (40, 20),
              (28, 24), (32, 24), (36, 24), (24, 28), (28, 28), (32, 28), (20, 32), (24, 32),
              (28, 32), (16, 36), (20, 36), (24, 36), (12, 40), (16, 40), (20, 40), (12, 44),
              (16, 44)]
_CUKE_SEED = [(40, 16), (32, 24), (24, 32), (16, 40)]


def i_cucumber(p):
    for x, y in _CUKE_BODY:
        p.solid(x, y, 4, 4, GREEN)
    for x, y in _CUKE_SEED:
        p.solid(x, y, 4, 4, GREEN_DEEP)
    for x, y in ((44, 12), (36, 20)):
        p.solid(x, y, 4, 4, GREEN_SOFT)
    p.solid(12, 44, 4, 4, p.color)


_HEART_ROWS = [(8, [1, 2, 6, 7]), (14, [0, 1, 2, 3, 5, 6, 7, 8]),
               (20, [0, 1, 2, 3, 4, 5, 6, 7, 8]), (26, [0, 1, 2, 3, 4, 5, 6, 7, 8]),
               (32, [1, 2, 3, 4, 5, 6, 7]), (38, [2, 3, 4, 5, 6]), (44, [3, 4, 5]), (50, [4])]


def i_pixel_heart(p):
    for y, cols in _HEART_ROWS:
        for c in cols:
            p.solid(5 + c * 6, y, 6, 6, GREEN)


_STAR_ROWS = [(8, [4]), (14, [3, 4, 5]), (20, [0, 1, 2, 3, 4, 5, 6, 7, 8]),
              (26, [1, 2, 3, 4, 5, 6, 7]), (32, [2, 3, 4, 5, 6]), (38, [1, 2, 3, 5, 6, 7]),
              (44, [0, 1, 7, 8])]


def i_pixel_star(p):
    for y, cols in _STAR_ROWS:
        for c in cols:
            p.solid(5 + c * 6, y, 6, 6, GREEN)


def i_pixel_disk(p):
    """Pixel-Diskette — retro save."""
    for y in range(10, 52, 6):
        for c in range(0, 8):
            p.solid(8 + c * 6, y, 6, 6, GREEN)
    for c in range(2, 6):                      # label window
        p.solid(8 + c * 6, 34, 6, 6, GREEN_SOFT)
        p.solid(8 + c * 6, 40, 6, 6, GREEN_SOFT)
    for c in range(2, 6):                      # shutter
        p.solid(8 + c * 6, 10, 6, 6, GREEN_DEEP)
        p.solid(8 + c * 6, 16, 6, 6, GREEN_DEEP)


# ── Registry: slug · label · draw ─────────────────────────────────────────
HEAVY = [
    ("grid", "Grid", i_grid), ("cursor", "Cursor", i_cursor), ("maze", "Labyrinth", i_maze),
    ("terminal", "Terminal", i_terminal), ("chat", "Chat", i_chat), ("spark", "Spark", i_spark),
    ("arrow", "Pfeil", i_arrow), ("user", "Person", i_user), ("gear", "Zahnrad", i_gear),
    ("folder", "Ordner", i_folder), ("lightbulb", "Glühbirne", i_lightbulb),
    ("code", "Code", i_code), ("calendar", "Kalender", i_calendar), ("clock", "Uhr", i_clock),
    ("chart", "Diagramm", i_chart), ("target", "Ziel", i_target), ("lock", "Schloss", i_lock),
    ("server", "Server", i_server), ("mobile", "Mobil", i_mobile), ("monitor", "Monitor", i_monitor),
    ("search", "Suche", i_search), ("mail", "Mail", i_mail), ("warning", "Warnung", i_warning),
    ("check", "Haken", i_check), ("close", "Kreuz", i_close), ("plus", "Plus", i_plus),
    ("external", "Extern", i_external), ("rocket", "Rakete", i_rocket), ("pen", "Stift", i_pen),
    ("trash", "Papierkorb", i_trash), ("filter", "Filter", i_filter), ("book", "Buch", i_book),
    ("bell", "Glocke", i_bell),
]
PIXEL = [
    ("cucumber", "Pixel-Gurke", i_cucumber), ("pixel-heart", "Pixel-Herz", i_pixel_heart),
    ("pixel-star", "Pixel-Stern", i_pixel_star), ("pixel-disk", "Pixel-Diskette", i_pixel_disk),
]
ALL = HEAVY + PIXEL
BY_SLUG = {s: (lbl, fn) for s, lbl, fn in ALL}


def draw(slide, slug, x, y, size, color):
    BY_SLUG[slug][1](Pen(slide, x, y, size, color))


def to_svg(slug, color="#000000"):
    lbl, fn = BY_SLUG[slug]
    pen = SvgPen(color)
    fn(pen)
    return pen.svg(lbl)


def wordmark(slide, x, y, w, color, green=GREEN):
    """Wordmark as live text: lowercase 'nozilla' plus the green period."""
    from pptx.util import Inches
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w * 1.25), Inches(w * 0.34))
    tf = tb.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    para = tf.paragraphs[0]
    for txt, col in (("nozilla", color), (".", green)):
        r = para.add_run()
        r.text = txt
        r.font.name = "Zilla Slab"
        r.font.bold = True
        r.font.size = Pt(w * 34)
        r.font.color.rgb = col
    return tb
