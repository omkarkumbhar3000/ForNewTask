# -*- coding: utf-8 -*-
"""
Build artifacts/deck/Prepare-1.pptx -- Dynamic API Validator, management deck.

Design system was lifted measured-for-measured from a QA Buddy reference deck that
was never committed to this repository (it lives outside it). Do not look for it:
  canvas 13.333 x 7.5in | ground gradient 115deg FFFFFF -> FFFCF7
  decorative ovals bleeding off-canvas at 7% alpha (E8722C / F2A93B / D95F3B)
  cream cards F9EEDD on EADCC3 hairline, 0.09in left accent bar
  ink 2E2620 | body 574C42 | muted 86796B | eyebrow C25318
  Segoe UI Black (hero) / Segoe UI Semibold (titles) / Segoe UI (body)

Every figure carries a traceable source -- see SOURCES at the bottom of this file.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.oxml.ns import qn

from paths import workspace_root   # OBJ-025: was a hardcoded absolute path, the only
OUT = str(workspace_root(__file__) # one in the workspace - it broke for any other
          / "artifacts" / "deck" / "Prepare-1.pptx")   # checkout, user or drive letter.

# ---------------------------------------------------------------- palette
INK      = RGBColor(0x2E, 0x26, 0x20)
BODY     = RGBColor(0x57, 0x4C, 0x42)
MUTED    = RGBColor(0x86, 0x79, 0x6B)
ORANGE   = RGBColor(0xE8, 0x72, 0x2C)
DEEP     = RGBColor(0xC2, 0x53, 0x18)
AMBER    = RGBColor(0xF2, 0xA9, 0x3B)
TERRA    = RGBColor(0xD9, 0x5F, 0x3B)
CARD     = RGBColor(0xF9, 0xEE, 0xDD)
CARDLINE = RGBColor(0xEA, 0xDC, 0xC3)
BANDFILL = RGBColor(0xFB, 0xE3, 0xCB)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)

BLACKF = "Segoe UI Black"
SEMI   = "Segoe UI Semibold"
REG    = "Segoe UI"

prs = Presentation()
prs.slide_width  = Inches(13.3333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


# ---------------------------------------------------------------- helpers
def _alpha(shape, pct):
    """Inject <a:alpha> into a solid fill -- python-pptx has no API for it."""
    clr = shape.fill._xPr.find(qn("a:solidFill")).find(qn("a:srgbClr"))
    a = clr.makeelement(qn("a:alpha"), {"val": str(int(pct * 1000))})
    clr.append(a)


def _noline(shape):
    shape.line.fill.background()


def rect(slide, x, y, w, h, kind=MSO_SHAPE.RECTANGLE):
    return slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))


def solid(slide, x, y, w, h, color, kind=MSO_SHAPE.RECTANGLE, alpha=None,
          line=None, line_w=0.01):
    s = rect(slide, x, y, w, h, kind)
    s.fill.solid()
    s.fill.fore_color.rgb = color
    if alpha is not None:
        _alpha(s, alpha)
    if line is None:
        _noline(s)
    else:
        s.line.color.rgb = line
        s.line.width = Inches(line_w)
    s.shadow.inherit = False
    return s


def ground(slide):
    """Full-bleed 115deg warm gradient."""
    s = rect(slide, 0, 0, 13.3333, 7.5)
    s.fill.gradient()
    st = s.fill.gradient_stops
    st[0].color.rgb = WHITE
    st[0].position = 0.0
    st[1].color.rgb = RGBColor(0xFF, 0xFC, 0xF7)
    st[1].position = 1.0
    s.fill.gradient_angle = 115.0
    _noline(s)
    s.shadow.inherit = False
    return s


def deco(slide, specs):
    """specs = [(x, y, size, color)] -- off-canvas washes at 7% alpha."""
    for x, y, size, color in specs:
        solid(slide, x, y, size, size, color, MSO_SHAPE.OVAL, alpha=7)


def tb(slide, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
       spacing=None, space_after=0):
    """runs = [[(text, font, size, bold, color), ...], ...] -- outer list = paragraphs."""
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, para_runs in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space_after)
        if spacing:
            p.line_spacing = spacing
        for text, font, size, bold, color in para_runs:
            r = p.add_run()
            r.text = text
            r.font.name = font
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = color
    return box


def header(slide, eyebrow, title_runs, sub=None, accent=TERRA, title_y=1.45,
           title_size=33):
    """The repeated slide grammar: dot + eyebrow, accent bar, title, deck."""
    solid(slide, 0.72, 0.6, 0.12, 0.12, ORANGE, MSO_SHAPE.OVAL)
    tb(slide, 0.98, 0.52, 8.0, 0.3, [[(eyebrow, REG, 12.5, True, DEEP)]])
    solid(slide, 0.72, 1.28, 0.55, 0.07, accent, MSO_SHAPE.ROUNDED_RECTANGLE)
    tb(slide, 0.72, title_y, 11.9, 1.0,
       [[(t, SEMI, title_size, True, c) for t, c in title_runs]])
    if sub:
        tb(slide, 0.72, title_y + 0.9, 11.6, 0.6,
           [[(sub, REG, 15.0, False, MUTED)]], spacing=1.15)


def card(slide, x, y, w, h, num, heading, body, accent=TERRA,
         num_size=20, head_size=16.5, body_size=12.5, body_h=0.9):
    """Cream card with left accent bar, numeral, heading, body."""
    solid(slide, x, y, w, h, CARD, MSO_SHAPE.ROUNDED_RECTANGLE, line=CARDLINE)
    solid(slide, x, y, 0.09, h, accent, MSO_SHAPE.ROUNDED_RECTANGLE)
    tb(slide, x + 0.42, y + 0.26, 0.8, 0.5,
       [[(num, SEMI, num_size, True, accent)]])
    tb(slide, x + 1.15, y + 0.26, w - 1.45, 0.5,
       [[(heading, SEMI, head_size, True, INK)]])
    tb(slide, x + 1.15, y + 0.75, w - 1.45, body_h,
       [[(body, REG, body_size, False, BODY)]], spacing=1.12)


def stat(slide, x, y, w, h, value, label, color, val_size=40, lab_size=12.0):
    solid(slide, x, y, w, h, CARD, MSO_SHAPE.ROUNDED_RECTANGLE, line=CARDLINE)
    tb(slide, x + 0.40, y + 0.22, w - 0.7, 0.7,
       [[(value, BLACKF, val_size, True, color)]])
    tb(slide, x + 0.42, y + 1.00, w - 0.75, 0.5,
       [[(label, REG, lab_size, False, BODY)]], spacing=1.1)


def band(slide, y, label, text, h=1.35):
    """The highlighted call-to-action strip."""
    solid(slide, 0.72, y, 11.9, h, BANDFILL, MSO_SHAPE.ROUNDED_RECTANGLE,
          line=ORANGE, line_w=0.02)
    tb(slide, 1.15, y + 0.20, 6.0, 0.4, [[(label, REG, 11.5, True, DEEP)]])
    tb(slide, 1.15, y + 0.55, 11.0, 0.55,
       [[(t, SEMI, 15.5, True, c) for t, c in text]], spacing=1.12)


def table(slide, x, y, w, rows, col_w, head_h=0.42, row_h=0.40, head_size=10.5,
          body_size=10.5):
    """Header band in ORANGE with white caps; body rows white with EADCC3 rules."""
    nr, nc = len(rows), len(rows[0])
    gt = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w),
                                Inches(head_h + row_h * (nr - 1)))
    t = gt.table
    t.first_row = True
    t.horz_banding = False
    for i, cw in enumerate(col_w):
        t.columns[i].width = Inches(cw)
    t.rows[0].height = Inches(head_h)
    for i in range(1, nr):
        t.rows[i].height = Inches(row_h)

    for ri, row in enumerate(rows):
        for ci, spec in enumerate(row):
            cell = t.cell(ri, ci)
            cell.margin_left = cell.margin_right = Inches(0.12)
            cell.margin_top = cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = ORANGE if ri == 0 else WHITE
            if ri > 0:
                tc = cell._tc.get_or_add_tcPr()
                ln = tc.makeelement(qn("a:lnB"), {"w": "12700", "cap": "flat",
                                                  "cmpd": "sng", "algn": "ctr"})
                sf = ln.makeelement(qn("a:solidFill"), {})
                cl = sf.makeelement(qn("a:srgbClr"), {"val": "EADCC3"})
                sf.append(cl)
                ln.append(sf)
                tc.insert(0, ln)

            text, kind, align = spec
            p = cell.text_frame.paragraphs[0]
            p.alignment = align
            r = p.add_run()
            r.text = text
            if ri == 0:
                r.font.name, r.font.size, r.font.bold = SEMI, Pt(head_size), True
                r.font.color.rgb = WHITE
            elif kind == "k":                       # key column
                r.font.name, r.font.size, r.font.bold = SEMI, Pt(body_size), True
                r.font.color.rgb = INK
            elif kind == "n":                       # numeric / accent
                r.font.name, r.font.size, r.font.bold = SEMI, Pt(body_size), True
                r.font.color.rgb = DEEP
            else:                                   # prose
                r.font.name, r.font.size, r.font.bold = REG, Pt(body_size), False
                r.font.color.rgb = BODY
    return gt


def chip(slide, x, y, w, dot, label):
    solid(slide, x, y, w, 0.42, CARD, MSO_SHAPE.ROUNDED_RECTANGLE, line=CARDLINE)
    solid(slide, x + 0.16, y + 0.16, 0.09, 0.09, dot, MSO_SHAPE.OVAL)
    tb(slide, x + 0.34, y, w - 0.4, 0.42, [[(label, REG, 11.5, False, BODY)]],
       anchor=MSO_ANCHOR.MIDDLE)


def wordmark(slide, right_label):
    tb(slide, 1.3, 0.66, 6.0, 0.5,
       [[("ARCON PAM", SEMI, 19, True, INK), (" | Dynamic API Validator", SEMI, 19, True, ORANGE)]],
       anchor=MSO_ANCHOR.MIDDLE)
    solid(slide, 0.72, 0.66, 0.42, 0.42, WHITE, MSO_SHAPE.OVAL, line=ORANGE, line_w=0.03)
    solid(slide, 0.85, 0.79, 0.16, 0.16, AMBER, MSO_SHAPE.OVAL)
    tb(slide, 8.0, 0.66, 4.6, 0.5, [[(right_label, REG, 11, True, MUTED)]],
       align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def new():
    s = prs.slides.add_slide(BLANK)
    ground(s)
    return s


# ================================================================ SLIDE 1
s = new()
deco(s, [(8.9, -1.8, 6.5, ORANGE), (-1.9, 4.4, 5.5, AMBER)])
wordmark(s, "MANAGEMENT OVERVIEW")

solid(s, 0.72, 2.15, 4.15, 0.44, WHITE, MSO_SHAPE.ROUNDED_RECTANGLE, line=ORANGE, line_w=0.02)
tb(s, 0.72, 2.15, 4.15, 0.44, [[("AI-DRIVEN API TEST GENERATION", REG, 11, True, DEEP)]],
   align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

tb(s, 0.7, 2.85, 11.6, 2.4,
   [[("No hand-written tests.", BLACKF, 50, True, INK)],
    [("Positive and ", BLACKF, 50, True, INK), ("negative.", BLACKF, 50, True, ORANGE)]],
   spacing=1.05)

tb(s, 0.72, 5.3, 11.0, 0.9,
   [[("The Dynamic API Validator reads our own catalogue and test data, then generates,", REG, 15.5, False, BODY)],
    [("executes, validates and reports the whole API surface -- and it found 13 product defects doing it.", REG, 15.5, False, BODY)]],
   spacing=1.2)

chip(s, 0.72, 6.55, 2.70, ORANGE, "Positive + negative testing")
chip(s, 3.54, 6.55, 2.40, AMBER,  "Zero hand-written tests")
chip(s, 6.06, 6.55, 2.55, TERRA,  "Envelope-aware validation")
chip(s, 8.73, 6.55, 2.00, ORANGE, "13 findings raised")
notes(s, "Cover. The one-line story: the tool writes the tests, runs them, judges them and reports "
         "them -- for how the product accepts a request and for how it rejects one. It surfaced 13 "
         "product defects doing it. Everything traces to run 2026-08-05_114315.")

# ================================================================ SLIDE 2
s = new()
deco(s, [(9.2, -1.6, 5.0, TERRA)])
header(s, "THE PROBLEM",
       [("Testing this API by hand ", INK), ("does not work", TERRA)],
       "1,306 declared endpoints, and a response format that makes the industry-standard assertion "
       "meaningless.")
card(s, 0.72, 3.30, 11.9, 1.55, "01", "Status codes are not verdicts on this API",
     "PAM answers a rejected request with HTTP 200 and puts the real error inside the body. An "
     "assertion that checks only the status code passes on a fully failed call.", body_h=0.6)
card(s, 0.72, 5.05, 11.9, 1.55, "02", "70% of the API is undocumented",
     "914 of 1,306 endpoints have no documentation at all, so a tester has to guess the request "
     "payload before writing a single case.", body_h=0.6)
notes(s, "Two constraints, both measured. The first is the important one: the response envelope means "
         "the assertion every other project relies on does not work here -- which is why a generic "
         "test tool would report green on failures. Sources: document-gap.md; OBJ-010 benchmark.")

# ================================================================ SLIDE 3
s = new()
deco(s, [(9.0, -1.7, 5.6, ORANGE), (-1.6, 4.8, 4.6, AMBER)])
header(s, "THE SOLUTION",
       [("Generated tests, ", INK), ("validated results", ORANGE)],
       "The tool derives tests from assets we already own, then runs, judges and reports them "
       "end to end.", accent=ORANGE)
card(s, 0.72, 3.15, 5.78, 1.72, "1", "Generates, never transcribes",
     "Endpoint catalogue plus the QA team's own Excel scenarios in, 747 executable flows and 5,590 "
     "cases out. No hand-written test code.", accent=ORANGE)
card(s, 6.86, 3.15, 5.78, 1.72, "2", "Judges the body, not the status",
     "A seven-layer validator reads the response envelope, so a green HTTP 200 that actually failed "
     "is reported as a failure.", accent=ORANGE)
card(s, 0.72, 5.17, 5.78, 1.72, "3", "Safe by default",
     "A bare run makes zero HTTP calls. Destructive endpoints are blocked by name at generation "
     "time, and credentials latch after one failure.", accent=ORANGE)
card(s, 6.86, 5.17, 5.78, 1.72, "4", "Evidence for every claim",
     "One JSON record per hop with secrets redacted -- 5,424 files -- plus a nine-worksheet workbook "
     "and a run report.", accent=ORANGE)
notes(s, "The framing that matters to management: the Dynamic API Validator produces the tests and then "
         "judges them, so it is not another suite someone has to maintain. Point 3 is worth stressing -- "
         "it is why we can run this against a live QA environment safely.")

# ================================================================ SLIDE 4
s = new()
deco(s, [(9.4, -1.9, 5.2, AMBER)])
header(s, "HOW IT WORKS",
       [("Catalogue in, ", INK), ("validated evidence out", AMBER), ("", INK)],
       "Five deterministic stages. The AI writes the flows; fixed code does every measurement, "
       "every file and every judgement.", accent=AMBER)

stages = [
    ("1", "INGEST", "1,306-endpoint catalogue\nplus the QA Excel corpus", ORANGE),
    ("2", "GENERATE", "Classify, pair and emit\n747 multi-hop flows", AMBER),
    ("3", "EXECUTE", "Chain runner carries context\nhop to hop, resumable", TERRA),
    ("4", "VALIDATE", "Seven layers read the\nenvelope, not the status", ORANGE),
    ("5", "REPORT", "Workbook, run report\nand per-hop evidence", AMBER),
]
x = 0.72
for num, name, body, col in stages:
    solid(s, x, 3.15, 2.24, 2.05, CARD, MSO_SHAPE.ROUNDED_RECTANGLE, line=CARDLINE)
    solid(s, x, 3.15, 2.24, 0.09, col, MSO_SHAPE.ROUNDED_RECTANGLE)
    solid(s, x + 0.30, 3.42, 0.46, 0.46, col, MSO_SHAPE.OVAL)
    tb(s, x + 0.30, 3.42, 0.46, 0.46, [[(num, SEMI, 15, True, WHITE)]],
       align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    tb(s, x + 0.30, 4.05, 1.85, 0.3, [[(name, SEMI, 13, True, INK)]])
    tb(s, x + 0.30, 4.38, 1.85, 0.75,
       [[(ln, REG, 10.5, False, BODY)] for ln in body.split("\n")], spacing=1.15)
    if x < 10.0:
        tb(s, x + 2.28, 4.02, 0.3, 0.4, [[(">", SEMI, 15, True, CARDLINE)]],
           align=PP_ALIGN.CENTER)
    x += 2.42

band(s, 5.55, "THE DETERMINISTIC BOUNDARY",
     [("Re-scoring the prior run offline reproduced ", INK), ("1,868 of 1,868 hops", DEEP),
      (" a week later, with zero HTTP calls -- the generators are repeatable, not lucky.", INK)],
     h=1.25)
notes(s, "Stage 4 is the differentiator. Stages 1-3 are what any generator does; reading the envelope "
         "is what makes the results trustworthy on this product. The band is the proof of "
         "determinism -- an auditor's question, answered in advance.")

# ================================================================ SLIDE 5
s = new()
deco(s, [(8.6, -1.8, 6.0, ORANGE), (-1.7, 4.7, 4.8, TERRA)])
header(s, "CAPABILITY PROGRESSION",
       [("Version 0.1 tested how the API accepts. ", INK),
        ("0.2 also tests how it rejects.", ORANGE)],
       "Both versions are fully AI-generated from the same sources. The difference is what the product "
       "is tested for.", accent=ORANGE, title_size=27)
table(s, 0.72, 2.90, 11.9,
      [[("CAPABILITY", "h", PP_ALIGN.LEFT), ("VERSION 0.1", "h", PP_ALIGN.LEFT),
        ("VERSION 0.2", "h", PP_ALIGN.LEFT)],
       [("AI-generated tests, no hand-written code", "k", PP_ALIGN.LEFT),
        ("Yes", "b", PP_ALIGN.LEFT), ("Yes", "n", PP_ALIGN.LEFT)],
       [("Positive API testing -- does it work", "k", PP_ALIGN.LEFT),
        ("Yes", "b", PP_ALIGN.LEFT), ("Yes", "n", PP_ALIGN.LEFT)],
       [("Negative API testing -- does it reject", "k", PP_ALIGN.LEFT),
        ("Not supported", "b", PP_ALIGN.LEFT), ("Yes", "n", PP_ALIGN.LEFT)],
       [("Unauthorized-access and wrong-method checks", "k", PP_ALIGN.LEFT),
        ("Not supported", "b", PP_ALIGN.LEFT), ("Yes", "n", PP_ALIGN.LEFT)],
       [("Database persistence verified after a write", "k", PP_ALIGN.LEFT),
        ("Not supported", "b", PP_ALIGN.LEFT), ("Yes", "n", PP_ALIGN.LEFT)],
       [("Envelope-aware validation, not status codes", "k", PP_ALIGN.LEFT),
        ("Yes", "b", PP_ALIGN.LEFT), ("Yes, seven layers", "n", PP_ALIGN.LEFT)]],
      col_w=[5.9, 2.7, 3.3], head_h=0.44, row_h=0.42)

band(s, 6.05, "WHY THIS IS THE RIGHT COMPARISON",
     [("Version 0.1 could only ask \"did the API do what we asked?\" Version 0.2 also asks "
       "\"does it correctly refuse what it should?\" -- ", INK),
      ("half of API quality that was previously untested.", DEEP)], h=1.15)
notes(s, "The point of this slide is capability, not volume. Both versions write every test "
         "themselves -- no engineer authored a case in either. Version 0.1 only covered the happy "
         "path. Version 0.2 adds the negative dimensions: wrong HTTP method, unauthorised access, "
         "invalid query parameters, and a database check that a write actually landed. That is the "
         "half of API quality nobody was testing before. If asked about volume: yes, it grew too, "
         "but the capability is the story.")

# ================================================================ SLIDE 6
s = new()
deco(s, [(8.8, -1.8, 5.8, TERRA), (-1.5, 4.9, 4.4, AMBER)])
header(s, "WHAT IT FOUND",
       [("13 developer findings", TERRA), (", each with attached evidence", INK)],
       "Packaged one folder per finding -- a raisable ticket plus reproducible proof. One is raised "
       "as PAMIT-42744; the rest are drafted and held.")

for x, val, lab, col in [(0.72, "4", "Critical", TERRA), (3.22, "2", "High", ORANGE),
                         (5.72, "4", "Medium", AMBER), (8.22, "3", "Low / review", MUTED)]:
    solid(s, x, 2.95, 2.30, 0.95, CARD, MSO_SHAPE.ROUNDED_RECTANGLE, line=CARDLINE)
    tb(s, x + 0.35, 3.08, 0.9, 0.6, [[(val, BLACKF, 26, True, col)]], anchor=MSO_ANCHOR.MIDDLE)
    tb(s, x + 1.05, 3.08, 1.15, 0.6, [[(lab, REG, 11.5, False, BODY)]], anchor=MSO_ANCHOR.MIDDLE)
solid(s, 10.72, 2.95, 1.92, 0.95, BANDFILL, MSO_SHAPE.ROUNDED_RECTANGLE, line=ORANGE, line_w=0.02)
tb(s, 10.90, 3.08, 1.6, 0.6, [[("1 raised", SEMI, 13, True, DEEP)], [("12 held for review", REG, 9.5, False, BODY)]],
   anchor=MSO_ANCHOR.MIDDLE, spacing=1.1)

table(s, 0.72, 4.15, 11.9,
      [[("FINDING", "h", PP_ALIGN.LEFT), ("SEVERITY", "h", PP_ALIGN.LEFT),
        ("WHY IT MATTERS", "h", PP_ALIGN.LEFT)],
       [("HTTP 200 for application-level failures", "k", PP_ALIGN.LEFT), ("Critical", "n", PP_ALIGN.LEFT),
        ("Every consumer must parse the body to know if a call worked", "b", PP_ALIGN.LEFT)],
       [("Mutation exposed over HTTP GET", "k", PP_ALIGN.LEFT), ("Medium", "n", PP_ALIGN.LEFT),
        ("A state-changing operation is reachable by a plain GET request", "b", PP_ALIGN.LEFT)],
       [("Two endpoints stop the IIS application pool", "k", PP_ALIGN.LEFT), ("Critical", "n", PP_ALIGN.LEFT),
        ("Three sequential requests took the whole API to 503", "b", PP_ALIGN.LEFT)],
       [("Authentication handling defect", "k", PP_ALIGN.LEFT), ("Critical", "n", PP_ALIGN.LEFT),
        ("Evidence packaged and ready to raise -- awaiting your decision", "b", PP_ALIGN.LEFT)],
       [("31 response shapes / error register incomplete", "k", PP_ALIGN.LEFT), ("High", "n", PP_ALIGN.LEFT),
        ("No caller can reliably tell success from failure", "b", PP_ALIGN.LEFT)],
       [("348 of 1,388 endpoints exercised return 404", "k", PP_ALIGN.LEFT), ("Medium", "n", PP_ALIGN.LEFT),
        ("Deployment gap or a stale catalogue -- needs triage", "b", PP_ALIGN.LEFT)]],
      col_w=[4.6, 1.5, 5.8], head_h=0.40, row_h=0.42)
notes(s, "Say 13, not 12 -- that is the measured count and it matches the 13 evidence packs. On the "
         "authentication finding: describe it as an authentication-handling defect, packaged and "
         "ready to raise, and do not give endpoint counts or names in this room. It is open and "
         "unraised, and raising it is the owner's call.")

# ================================================================ SLIDE 7
s = new()
deco(s, [(9.3, -1.7, 5.2, AMBER)])
header(s, "DOCUMENTATION GAP",
       [("70% of the API ", AMBER), ("is undocumented", INK)],
       "Measured by comparing the automation catalogue against the internal API reference, page "
       "by page.", accent=AMBER)

stat(s, 0.72, 3.05, 3.86, 1.55, "914", "of 1,306 endpoints have no documentation at all", TERRA)
stat(s, 4.87, 3.05, 3.86, 1.55, "392", "documented and tested -- the 30% overlap", AMBER)
stat(s, 9.02, 3.05, 3.86, 1.55, "60", "documented endpoints absent from the catalogue", ORANGE)

card(s, 0.72, 4.80, 5.78, 1.80, "A", "Payloads bind by page proximity",
     "3,194 JSON examples exist and 1,654 bind to an endpoint -- positionally, so some bind wrong. "
     "Still the best payload source we have.",
     accent=AMBER, num_size=18, body_h=1.0)
card(s, 6.86, 4.80, 5.78, 1.80, "B", "31 reply formats, only 6 written down",
     "The same API answers in 31 different formats. Everything that calls it -- our tests, the UI, "
     "any integration -- has to handle all 31, and 25 of them are nowhere in the documentation.",
     accent=AMBER, num_size=18, body_h=1.0)
tb(s, 0.72, 6.75, 11.9, 0.4,
   [[("Why that matters: an undocumented reply format is one a developer only discovers when something "
      "breaks in production. The validator was taught all 31 so our tests do not.", REG, 11.5, False, MUTED)]])
notes(s, "This slide reframes a documentation problem as a delivery risk. On the 31 formats, in plain "
         "terms: imagine ordering from 31 suppliers who each send the invoice in a different layout, "
         "and only 6 of those layouts were ever shown to you. Every new integration has to rediscover "
         "the other 25 by trial and error, and each rediscovery is a bug found late. Measured across "
         "1,868 captured responses. Source: docs/briefs/document-gap.md.")

# ================================================================ SLIDE 8
s = new()
deco(s, [(7.8, -2.0, 6.5, ORANGE), (-1.6, 4.6, 5.0, AMBER)])
header(s, "WHAT NEXT",
       [("Portable to the next project, ", INK), ("already", ORANGE)],
       "The onboarding kit is built. What is left is a decision on the findings and one data "
       "dependency.", accent=ORANGE, title_size=32)

card(s, 0.72, 3.05, 3.86, 1.75, "1", "Next project: ready",
     "Profile schema, worked example, blank template, readiness validator and a portable onboarding "
     "skill -- built and ready.", accent=ORANGE, num_size=18, head_size=14.5, body_size=11.5, body_h=0.95)
card(s, 4.87, 3.05, 3.86, 1.75, "2", "Close the payload gap",
     "204 of 217 create endpoints cannot be driven -- nothing supplies a valid request body. An "
     "OpenAPI source removes this.", accent=AMBER, num_size=18, head_size=14.5, body_size=11.5, body_h=0.95)
card(s, 9.02, 3.05, 3.86, 1.75, "3", "Triage and raise",
     "348 endpoints returning 404 need a deployment-or-catalogue decision, and 12 findings are "
     "drafted awaiting approval.", accent=TERRA, num_size=18, head_size=14.5, body_size=11.5, body_h=0.95)

band(s, 5.20, "THE ASK",
     [("Approve raising the held findings, and nominate the next project to onboard. ", INK),
      ("The tooling is done -- what it needs now is a target.", DEEP)], h=1.20)
tb(s, 0.72, 6.70, 11.9, 0.5,
   [[("Evidence: artifacts/runs/2026-08-05_114315  |  docs/management/summary/OBJ-010-Execution-Benchmark.md  |  "
      "docs/briefs/developer-loopholes.md  |  docs/briefs/document-gap.md", REG, 10, False, MUTED)]])
notes(s, "Two asks, both cheap: approve the findings for raising, and name the next project. Note "
         "that the payload-data gap is the one thing that will bite on any new project -- budget for "
         "getting an OpenAPI or Postman source, not for tooling.")

prs.save(OUT)
print("SAVED:", OUT)
print("slides:", len(prs.slides.__iter__.__self__._sldIdLst))

# ------------------------------------------------------------------ SOURCES
# 5,590 planned / 5,416 executed / 747 flows / 1,388 endpoints / 326-747 flows /
#   1,868 N-1 executed / 870 N-1 endpoints / 2,124 negative / 64.2% vs 63.9% /
#   858 comparable, 856 identical      -> docs/management/summary/OBJ-010-Execution-Benchmark.md S2, S3
# 1,022 cases HTTP 200 while failing   -> same, S1 + objective-history OBJ-010 completion record
# failures by layer 1484/1012/931/198/104/23/7 -> artifacts/runs/2026-08-05_114315/RUN_REPORT.md S1
# 5,424 evidence files                 -> OBJ-010 completion record, Related Files
# 348 of 1,388 return 404              -> docs/briefs/developer-loopholes.md S0 #5
# 13 findings, severity split          -> docs/briefs/developer-loopholes.md S0
# PAMIT-42744 = LH-01 raised           -> root CLAUDE.md, Conventions
# 914/1,306 (70%), 392, 60             -> docs/briefs/document-gap.md lines 18-20
# 31 shapes, 6 documented              -> root CLAUDE.md, Response shapes; document-gap.md S1 table
# 3,194 payload examples, 1,654 bound  -> .claude/rules/api-surface.md, Contract sources
# 204 of 217 creates undrivable        -> docs/briefs/new-project-implementation.md S9
# 1,868/1,868 reproduced, 0 HTTP calls -> OBJ-010 completion record, Lessons Learned
# 1,306 canonical endpoint count       -> .claude/rules/api-surface.md
