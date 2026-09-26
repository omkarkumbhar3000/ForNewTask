#!/usr/bin/env python3
"""Markdown → .docx / .xlsx renderer. `md_to_docx_xlsx.py` is the command-line entry point.

Every `#`/`##`/`###` heading opens a section. In Word, each section becomes a heading
with its paragraphs and first table. In Excel, the first section becomes a `Cover` sheet
(title plus bold metadata lines) and every later section that has a table becomes one
worksheet. `all_data=True` adds one sheet holding every table in order.

⛔ **The markdown is the source of truth and is never written here.** This module reads
one `.md` and writes the `.docx` and `.xlsx` beside it. It does not recalculate: every
number in the output is the number parsed out of the markdown cell. Fix the markdown,
then re-render; never hand-edit a rendered file.

⚠️ **One table per section.** A section holding two tables keeps only the first, so put
each further table under its own heading.

⚠️ **Grouped headers.** A two-level header can be written as

    | Priority | Total Count | Open |  |  | Closed |  |  | Unmapped |
    | --- | ---: | ---: | ... |
    |  |  | Client | Internal | Total | Client | Internal | Total |  |

which is valid GFM — the separator is still line 2 — with the leaf row sitting where the
first body row goes. `parse_md()` recognises that shape and lifts the leaf row into
`table_subheaders`, and both builders then merge cells so the grouping is real in Word
and Excel rather than a row of blanks. Detection requires BOTH an empty cell in the
header row AND an empty first cell in the row beneath it, so an ordinary table cannot
trip it.

⚠️ **Cells arrive as strings.** Markdown has no types, so `_coerce()` turns `1,234` into
an int and `12.3%` into a float with a percent number-format. Without it every figure
lands in Excel left-aligned as text and cannot be summed by the reader.
"""
from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

# ----------------------------------------------------------------------- appearance

ACCENT = "1F497D"
HEADER_BG = "4472C4"
SUBHEADER_BG = "8EA9DB"
TOTAL_BG = "FFF2CC"

HEADER_FONT = Font(bold=True, color="FFFFFF", size=10)
HEADER_FILL = PatternFill("solid", start_color=HEADER_BG, end_color=HEADER_BG)
SUBHEADER_FONT = Font(bold=True, color="1F3864", size=10)
SUBHEADER_FILL = PatternFill("solid", start_color=SUBHEADER_BG, end_color=SUBHEADER_BG)
TOTAL_FONT = Font(bold=True, size=10)
TOTAL_FILL = PatternFill("solid", start_color=TOTAL_BG, end_color=TOTAL_BG)
BODY_FONT = Font(size=10)

HEADER_ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)
TEXT_ALIGN = Alignment(horizontal="left", vertical="center", wrap_text=True)
NUM_ALIGN = Alignment(horizontal="right", vertical="center")
THIN = Side(style="thin", color="B4C6E7")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

INT_FMT = "#,##0"
PCT_FMT = "0.0%"

MAX_COL_WIDTH = 60
MIN_COL_WIDTH = 9

#: Sections that keep their place in the markdown and the Word report but get no
#: worksheet. Matched on the heading lower-cased, with any leading "12. " numbering
#: stripped, so renumbering a document cannot silently re-enable one. Empty by default;
#: pass `skip=` (or `--skip` on the command line) to leave sections out of the workbook.
DEFAULT_XLSX_SKIP = frozenset()

_NUM_PREFIX = re.compile(r"^\s*\d+(?:\.\d+)*[.)]?\s+")
_BOLD = re.compile(r"\*\*(.*?)\*\*")
_LINK = re.compile(r"^\[([^\]]+)\]\(([^)]+)\)$")
_INT = re.compile(r"^-?\d{1,3}(?:,\d{3})+$|^-?\d+$")
_PCT = re.compile(r"^-?\d+(?:\.\d+)?%$")
_FLOAT = re.compile(r"^-?\d+\.\d+$")


def _plain(text: str) -> str:
    """Strip markdown bold markers for display."""
    return _BOLD.sub(r"\1", text or "").strip()


def normalise_heading(heading: str) -> str:
    return _NUM_PREFIX.sub("", heading or "").strip().lower()


def _coerce(cell: str):
    """Return (value, number_format, is_bold, hyperlink) for one markdown cell."""
    raw = (cell or "").strip()
    bold = raw.startswith("**") and raw.endswith("**") and len(raw) > 4
    text = _plain(raw)

    link = _LINK.match(text)
    if link:
        return link.group(1), None, bold, link.group(2)
    if _INT.match(text):
        return int(text.replace(",", "")), INT_FMT, bold, None
    if _PCT.match(text):
        return float(text[:-1]) / 100.0, PCT_FMT, bold, None
    if _FLOAT.match(text):
        return float(text), "#,##0.0", bold, None
    return text, None, bold, None


def _is_total_row(cells) -> bool:
    if not cells:
        return False
    first = _plain(str(cells[0])).lower()
    return first.startswith("total") or first.startswith("**total")


# --------------------------------------------------------------------------- parsing

def _blank_section(heading: str, level: int) -> dict:
    return {"heading": heading, "level": level, "meta": [], "paragraphs": [],
            "table_headers": [], "table_subheaders": [], "table_rows": []}


def parse_md(text: str) -> list[dict]:
    """Parse markdown into sections.

    Each section carries `table_headers`, an optional `table_subheaders` (the leaf row
    of a grouped header) and `table_rows`. A section holding more than one table keeps
    the FIRST, so give every further table its own heading or it is dropped.
    """
    sections: list[dict] = []
    current = None
    lines = text.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        for prefix, level in (("### ", 3), ("## ", 2), ("# ", 1)):
            if line.startswith(prefix):
                if current:
                    sections.append(current)
                current = _blank_section(line[len(prefix):].strip(), level)
                break
        else:
            if current is None:
                i += 1
                continue

            if stripped == "---":
                i += 1
                continue

            if stripped.startswith("|"):
                block = []
                while i < len(lines) and lines[i].strip().startswith("|"):
                    block.append(lines[i].strip())
                    i += 1
                if len(block) >= 2 and not current["table_headers"]:
                    headers = [c.strip() for c in block[0].split("|")[1:-1]]
                    rows = [[c.strip() for c in tl.split("|")[1:-1]] for tl in block[2:]]
                    # Grouped header: the header row has an interior blank AND the row
                    # beneath it starts blank. Both conditions, so a normal table with a
                    # blank first cell is not mistaken for one.
                    if any(h == "" for h in headers) and rows and rows[0] and rows[0][0] == "":
                        current["table_subheaders"] = rows.pop(0)
                    current["table_headers"] = headers
                    current["table_rows"] = rows
                continue

            if stripped.startswith("> "):
                current["paragraphs"].append(stripped[2:].strip())
            elif stripped.startswith("**") and stripped.endswith("**"):
                current["meta"].append(stripped)
            elif stripped.startswith("**"):
                current["meta"].append(stripped)
            elif stripped:
                current["paragraphs"].append(stripped)
            i += 1
            continue

        i += 1

    if current:
        sections.append(current)
    return sections


def merge_plan(headers, subheaders):
    """Work out the merges a grouped header needs.

    Returns (vertical, horizontal): `vertical` are column indices whose header spans
    both rows; `horizontal` are (start, end) column spans in the group row.
    """
    vertical, horizontal = [], []
    if not subheaders:
        return vertical, horizontal
    n = len(headers)
    j = 0
    while j < n:
        sub = subheaders[j] if j < len(subheaders) else ""
        if sub == "":
            vertical.append(j)
            j += 1
            continue
        k = j + 1
        while k < n and headers[k] == "" and (k >= len(subheaders) or subheaders[k] != ""):
            k += 1
        if k - 1 > j:
            horizontal.append((j, k - 1))
        j = k
    return vertical, horizontal


# ------------------------------------------------------------------------------ Word

def _shade(cell, color_hex: str) -> None:
    tc_pr = cell._element.get_or_add_tcPr()
    shd = tc_pr.makeelement(qn("w:shd"), {
        qn("w:val"): "clear", qn("w:color"): "auto", qn("w:fill"): color_hex})
    tc_pr.append(shd)


def _cell_text(cell, text, *, bold=False, size=9, color=None, align=None):
    cell.text = ""
    para = cell.paragraphs[0]
    para.alignment = align or WD_ALIGN_PARAGRAPH.LEFT
    run = para.add_run(str(text))
    run.font.size = Pt(size)
    run.font.bold = bold
    if color:
        run.font.color.rgb = color
    para.paragraph_format.space_before = Pt(1)
    para.paragraph_format.space_after = Pt(1)


def build_docx(sections, out_path: Path) -> Path:
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10)

    for idx, sec in enumerate(sections):
        if sec["level"] == 1:
            head = doc.add_heading(sec["heading"], level=0)
        else:
            head = doc.add_heading(sec["heading"], level=min(sec["level"], 4))
        for run in head.runs:
            run.font.color.rgb = RGBColor.from_string(ACCENT)

        for meta in sec["meta"]:
            para = doc.add_paragraph()
            run = para.add_run(_plain(meta))
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor.from_string("555555")

        for text in sec["paragraphs"]:
            para = doc.add_paragraph(_plain(text))
            para.paragraph_format.space_after = Pt(4)

        headers = sec["table_headers"]
        if not headers:
            continue
        subs = sec["table_subheaders"]
        rows = sec["table_rows"]
        header_rows = 2 if subs else 1

        table = doc.add_table(rows=header_rows + len(rows), cols=len(headers))
        table.style = "Table Grid"
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        for c, text in enumerate(headers):
            cell = table.cell(0, c)
            _cell_text(cell, _plain(text), bold=True, size=9,
                       color=RGBColor.from_string("FFFFFF"),
                       align=WD_ALIGN_PARAGRAPH.CENTER)
            _shade(cell, HEADER_BG)
        if subs:
            for c, text in enumerate(subs):
                cell = table.cell(1, c)
                _cell_text(cell, _plain(text), bold=True, size=9,
                           align=WD_ALIGN_PARAGRAPH.CENTER)
                _shade(cell, SUBHEADER_BG)
            vertical, horizontal = merge_plan(headers, subs)
            for start, end in horizontal:
                table.cell(0, start).merge(table.cell(0, end))
            for col in vertical:
                table.cell(0, col).merge(table.cell(1, col))

        for r, row_cells in enumerate(rows, start=header_rows):
            total_row = _is_total_row(row_cells)
            for c in range(len(headers)):
                raw = row_cells[c] if c < len(row_cells) else ""
                value, fmt, bold, _link = _coerce(raw)
                if fmt == PCT_FMT:
                    shown = f"{value * 100:.1f}%"
                elif fmt == INT_FMT:
                    shown = f"{value:,}"
                else:
                    shown = value
                cell = table.cell(r, c)
                align = (WD_ALIGN_PARAGRAPH.RIGHT if fmt
                         else WD_ALIGN_PARAGRAPH.LEFT)
                _cell_text(cell, shown, bold=bold or total_row, size=9, align=align)
                if total_row:
                    _shade(cell, TOTAL_BG)

    doc.save(str(out_path))
    return out_path


# ----------------------------------------------------------------------------- Excel

def safe_sheet_name(name: str, taken) -> str:
    """Excel-legal, 31 characters, unique within the workbook."""
    clean = re.sub(r"[\\/*?\[\]:]", "", _plain(name)).strip() or "Sheet"
    clean = clean[:31].rstrip()
    if clean not in taken:
        taken.add(clean)
        return clean
    for n in range(2, 100):
        suffix = f"_{n}"
        candidate = clean[:31 - len(suffix)].rstrip() + suffix
        if candidate not in taken:
            taken.add(candidate)
            return candidate
    raise ValueError(f"cannot make a unique sheet name from {name!r}")


def _write_table(ws, sec, start_row=1):
    """Write one section's table. Returns the row after the table."""
    headers = sec["table_headers"]
    subs = sec["table_subheaders"]
    rows = sec["table_rows"]
    ncols = len(headers)

    for c, text in enumerate(headers, 1):
        cell = ws.cell(row=start_row, column=c, value=_plain(text))
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = HEADER_ALIGN
        cell.border = BORDER
    ws.row_dimensions[start_row].height = 28

    header_rows = 1
    if subs:
        header_rows = 2
        for c, text in enumerate(subs, 1):
            cell = ws.cell(row=start_row + 1, column=c, value=_plain(text))
            cell.font = SUBHEADER_FONT
            cell.fill = SUBHEADER_FILL
            cell.alignment = HEADER_ALIGN
            cell.border = BORDER
        ws.row_dimensions[start_row + 1].height = 20
        vertical, horizontal = merge_plan(headers, subs)
        for start, end in horizontal:
            ws.merge_cells(start_row=start_row, start_column=start + 1,
                           end_row=start_row, end_column=end + 1)
        for col in vertical:
            ws.merge_cells(start_row=start_row, start_column=col + 1,
                           end_row=start_row + 1, end_column=col + 1)

    first_data = start_row + header_rows
    row_num = first_data
    last_data_row = first_data - 1
    for row_cells in rows:
        total_row = _is_total_row(row_cells)
        for c in range(1, ncols + 1):
            raw = row_cells[c - 1] if c - 1 < len(row_cells) else ""
            value, fmt, bold, link = _coerce(raw)
            cell = ws.cell(row=row_num, column=c, value=value)
            cell.border = BORDER
            cell.alignment = NUM_ALIGN if fmt else TEXT_ALIGN
            if fmt:
                cell.number_format = fmt
            if link:
                cell.hyperlink = link
                cell.font = Font(size=10, color="0563C1", underline="single",
                                 bold=bold or total_row)
            elif total_row or bold:
                cell.font = TOTAL_FONT
            else:
                cell.font = BODY_FONT
            if total_row:
                cell.fill = TOTAL_FILL
        if not total_row:
            last_data_row = row_num
        row_num += 1

    # Freeze the header block, and filter the data region only — a Total row inside the
    # filter range disappears the moment anyone filters, which reads as a missing total.
    ws.freeze_panes = ws.cell(row=first_data, column=1)
    if last_data_row >= first_data:
        filter_top = start_row + header_rows - 1
        ws.auto_filter.ref = (f"{get_column_letter(1)}{filter_top}:"
                              f"{get_column_letter(ncols)}{last_data_row}")

    widths = {}
    for c in range(1, ncols + 1):
        longest = len(_plain(headers[c - 1]))
        if subs and c - 1 < len(subs):
            longest = max(longest, len(_plain(subs[c - 1])))
        for row_cells in rows:
            if c - 1 < len(row_cells):
                longest = max(longest, len(_plain(row_cells[c - 1])))
        widths[c] = max(MIN_COL_WIDTH, min(MAX_COL_WIDTH, longest + 3))
    for c, width in widths.items():
        ws.column_dimensions[get_column_letter(c)].width = width

    return row_num


def build_xlsx(sections, out_path: Path, *, all_data=False, skip=DEFAULT_XLSX_SKIP) -> Path:
    wb = Workbook()
    wb.remove(wb.active)

    # Cover sheet: the document title plus its bold metadata lines and paragraphs. It
    # deliberately does not restate any later section, which gets its own sheet.
    cover = wb.create_sheet("Cover")
    cover.sheet_properties.tabColor = ACCENT
    taken = {"Cover"}
    title_sec = sections[0] if sections else None
    if title_sec:
        cover.merge_cells("A1:D1")
        cell = cover["A1"]
        cell.value = _plain(title_sec["heading"])
        cell.font = Font(bold=True, size=15, color=ACCENT)
        cell.alignment = Alignment(horizontal="left", vertical="center")
        cover.row_dimensions[1].height = 26
        row_num = 3
        for meta in title_sec["meta"]:
            cover.merge_cells(f"A{row_num}:D{row_num}")
            mcell = cover.cell(row=row_num, column=1, value=_plain(meta))
            mcell.font = Font(size=10, color="555555")
            mcell.alignment = Alignment(vertical="center", wrap_text=True)
            row_num += 1
        for para in title_sec["paragraphs"]:
            row_num += 1
            cover.merge_cells(f"A{row_num}:D{row_num}")
            pcell = cover.cell(row=row_num, column=1, value=_plain(para))
            pcell.font = Font(size=9, color="555555")
            pcell.alignment = Alignment(vertical="top", wrap_text=True)
            cover.row_dimensions[row_num].height = 46
    for col in range(1, 5):
        cover.column_dimensions[get_column_letter(col)].width = 32

    for sec in sections[1:]:
        if not sec["table_headers"]:
            continue
        if normalise_heading(sec["heading"]) in skip:
            continue
        ws = wb.create_sheet(safe_sheet_name(sec["heading"], taken))
        _write_table(ws, sec)

    if all_data:
        ws = wb.create_sheet(safe_sheet_name("All Data", taken))
        ws.sheet_properties.tabColor = "E26B0A"
        row_num = 1
        for sec in sections:
            if not sec["table_headers"]:
                continue
            if normalise_heading(sec["heading"]) in skip:
                continue
            ncols = max(1, len(sec["table_headers"]))
            ws.merge_cells(start_row=row_num, start_column=1,
                           end_row=row_num, end_column=ncols)
            cell = ws.cell(row=row_num, column=1, value=_plain(sec["heading"]))
            cell.font = Font(bold=True, size=11, color=ACCENT)
            row_num += 1
            row_num = _write_table(ws, sec, start_row=row_num) + 1
        ws.freeze_panes = "A1"
        ws.auto_filter.ref = None

    wb.save(str(out_path))
    return out_path


# ------------------------------------------------------------------------------ entry

def render(md_path, *, all_data=False, skip=DEFAULT_XLSX_SKIP, stem=None):
    """Render `md_path` to .docx and .xlsx beside it. Returns (docx_path, xlsx_path)."""
    md_path = Path(md_path)
    if not md_path.exists():
        raise SystemExit(f"markdown not found: {md_path}")
    sections = parse_md(md_path.read_text(encoding="utf-8"))
    base = md_path.with_name(stem) if stem else md_path
    docx_path = base.with_suffix(".docx")
    xlsx_path = base.with_suffix(".xlsx")
    build_docx(sections, docx_path)
    build_xlsx(sections, xlsx_path, all_data=all_data, skip=skip)
    return docx_path, xlsx_path
