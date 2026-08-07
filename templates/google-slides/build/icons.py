"""nozilla icons as native PPTX vector shapes (64-unit grid, 4-unit stroke).

Every icon is drawn with real shapes — no rasters — so they stay sharp at any
size and can be recoloured directly inside Google Slides.
"""
from pptx.util import Inches as In, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

GREEN = RGBColor(0x00, 0xFF, 0x9C)
G = 64.0  # design grid


def _emu(v):
    return Emu(int(round(v)))


class Pen:
    """Maps 64-grid coordinates onto a slide box, in EMU."""

    def __init__(self, slide, x, y, size, color, stroke=4.0):
        self.s = slide
        self.x0, self.y0 = x * 914400.0, y * 914400.0
        self.k = size * 914400.0 / G          # EMU per grid unit
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
        sh = self.s.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, _emu(self.X(x)), _emu(self.Y(y)),
            _emu(w * self.k), _emu(h * self.k))
        if fill is None:
            sh.fill.background()
        else:
            sh.fill.solid(); sh.fill.fore_color.rgb = fill
        sh.line.color.rgb = self.color
        sh.line.width = self.wpt
        return self._plain(sh)

    def solid(self, x, y, w, h, fill):
        """Filled block with no outline — for pixel art."""
        sh = self.s.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, _emu(self.X(x)), _emu(self.Y(y)),
            _emu(w * self.k), _emu(h * self.k))
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
        sh.line.fill.background()
        return self._plain(sh)

    def circle(self, cx, cy, r, fill=None):
        sh = self.s.shapes.add_shape(
            MSO_SHAPE.OVAL, _emu(self.X(cx - r)), _emu(self.Y(cy - r)),
            _emu(2 * r * self.k), _emu(2 * r * self.k))
        if fill is None:
            sh.fill.background()
        else:
            sh.fill.solid(); sh.fill.fore_color.rgb = fill
        sh.line.color.rgb = self.color
        sh.line.width = self.wpt
        return self._plain(sh)

    def dot(self, cx, cy, r, fill):
        sh = self.s.shapes.add_shape(
            MSO_SHAPE.OVAL, _emu(self.X(cx - r)), _emu(self.Y(cy - r)),
            _emu(2 * r * self.k), _emu(2 * r * self.k))
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
        sh.line.fill.background()
        return self._plain(sh)

    def poly(self, pts, close=False, fill=None):
        ff = self.s.shapes.build_freeform(_emu(self.X(pts[0][0])), _emu(self.Y(pts[0][1])))
        ff.add_line_segments([(_emu(self.X(x)), _emu(self.Y(y))) for x, y in pts[1:]],
                             close=close)
        sh = ff.convert_to_shape()
        if fill is None:
            sh.fill.background()
        else:
            sh.fill.solid(); sh.fill.fore_color.rgb = fill
        sh.line.color.rgb = self.color
        sh.line.width = self.wpt
        return self._plain(sh)


# ── Icon definitions — Dialekt A: Heavy-Stroke ────────────────────────────
def i_grid(p):
    for x, y in ((10, 10), (36, 10), (10, 36), (36, 36)):
        p.rect(x, y, 18, 18)


def i_cursor(p):
    p.poly([(18, 12), (18, 46), (27, 38), (33, 52), (39, 49), (33, 36), (44, 36)], close=True)


def i_maze(p):
    p.poly([(12, 12), (52, 12), (52, 52), (20, 52), (20, 20), (44, 20),
            (44, 44), (28, 44), (28, 28), (36, 28)])


def i_terminal(p):
    p.rect(8, 12, 48, 40)
    p.line(8, 23, 56, 23)
    p.poly([(16, 33), (22, 38), (16, 43)])
    p.line(28, 43, 42, 43)


def i_chat(p):
    p.poly([(10, 12), (54, 12), (54, 40), (26, 40), (16, 50), (16, 40), (10, 40)], close=True)
    for cx in (24, 32, 40):
        p.dot(cx, 26, 2.4, p.color)


def i_spark(p):
    p.poly([(32, 8), (37, 27), (56, 32), (37, 37), (32, 56), (27, 37), (8, 32), (27, 27)],
           close=True, fill=GREEN)


def i_arrow(p):
    p.line(10, 32, 50, 32)
    p.poly([(38, 20), (52, 32), (38, 44)])


def i_user(p):
    p.circle(32, 22, 10)
    p.poly([(14, 52), (18, 43), (32, 39), (46, 43), (50, 52)])


def i_gear(p):
    p.circle(32, 32, 15)
    p.circle(32, 32, 5)
    for a, b, c, d in ((47, 32, 53, 32), (32, 47, 32, 53), (17, 32, 11, 32), (32, 17, 32, 11),
                       (42.6, 42.6, 47, 47), (21.4, 42.6, 17, 47),
                       (21.4, 21.4, 17, 17), (42.6, 21.4, 47, 17)):
        p.line(a, b, c, d)


def i_folder(p):
    p.poly([(10, 20), (26, 20), (31, 26), (54, 26), (54, 48), (10, 48)], close=True)


def i_lightbulb(p):
    p.circle(32, 26, 14, fill=GREEN)
    p.line(24, 44, 40, 44)
    p.line(26, 50, 38, 50)


def i_code(p):
    p.poly([(24, 18), (12, 32), (24, 46)])
    p.poly([(40, 18), (52, 32), (40, 46)])
    p.line(36, 14, 28, 50)


# ── Dialekt B: Pixel-Art ──────────────────────────────────────────────────
_CUKE_BODY = [(40, 12), (44, 12), (36, 16), (40, 16), (44, 16), (32, 20), (36, 20), (40, 20),
              (28, 24), (32, 24), (36, 24), (24, 28), (28, 28), (32, 28), (20, 32), (24, 32),
              (28, 32), (16, 36), (20, 36), (24, 36), (12, 40), (16, 40), (20, 40), (12, 44),
              (16, 44)]
_CUKE_SEED = [(40, 16), (32, 24), (24, 32), (16, 40)]
_CUKE_HI = [(44, 12), (36, 20)]


def i_cucumber(p):
    for x, y in _CUKE_BODY:
        p.solid(x, y, 4, 4, GREEN)
    for x, y in _CUKE_SEED:
        p.solid(x, y, 4, 4, RGBColor(0x00, 0xC0, 0x75))
    for x, y in _CUKE_HI:
        p.solid(x, y, 4, 4, RGBColor(0xB7, 0xFF, 0xE0))
    p.solid(12, 44, 4, 4, p.color)


_HEART_ROWS = [(8, [1, 2, 6, 7]), (14, [0, 1, 2, 3, 5, 6, 7, 8]),
               (20, [0, 1, 2, 3, 4, 5, 6, 7, 8]), (26, [0, 1, 2, 3, 4, 5, 6, 7, 8]),
               (32, [1, 2, 3, 4, 5, 6, 7]), (38, [2, 3, 4, 5, 6]), (44, [3, 4, 5]), (50, [4])]


def i_pixel_heart(p):
    for y, cols in _HEART_ROWS:
        for c in cols:
            p.solid(5 + c * 6, y, 6, 6, GREEN)


HEAVY = [("Grid", i_grid), ("Cursor", i_cursor), ("Labyrinth", i_maze),
         ("Terminal", i_terminal), ("Chat", i_chat), ("Spark", i_spark),
         ("Pfeil", i_arrow), ("Person", i_user), ("Zahnrad", i_gear),
         ("Ordner", i_folder), ("Glühbirne", i_lightbulb), ("Code", i_code)]
PIXEL = [("Pixel-Gurke", i_cucumber), ("Pixel-Herz", i_pixel_heart)]
BY_NAME = {n: f for n, f in HEAVY + PIXEL}


def draw(slide, name, x, y, size, color):
    """Draw icon `name` with its top-left at (x, y) inches, `size` inches wide."""
    BY_NAME[name](Pen(slide, x, y, size, color))


def wordmark(slide, x, y, w, color):
    """Wordmark as live text — stays selectable and recolourable in Slides."""
    from pptx.util import Inches
    from pptx.enum.text import PP_ALIGN
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(w * 0.32))
    tf = tb.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    r = tf.paragraphs[0].add_run()
    r.text = "nozilla"
    r.font.name = "Zilla Slab"
    r.font.bold = True
    r.font.size = Pt(w * 34)
    r.font.color.rgb = color
    return tb
