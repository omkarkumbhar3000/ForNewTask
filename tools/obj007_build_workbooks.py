#!/usr/bin/env python3
"""Build the OBJ-007 consolidated Excel deliverables from data/analysis/*.json.

Two workbooks, many worksheets - the consolidation the objective asks for:

  artifacts/workbooks/PAM-API-Validation-Analysis.xlsx   technical analysis
  artifacts/workbooks/PAM-Project-Governance.xlsx        management + tracking

Design rules
------------
* This is the ONLY thing that writes .xlsx. Analysis agents emit JSON; the
  workbook shape is decided in one place so worksheets stay consistent.
* Missing inputs are tolerated and reported. The script is meant to be re-run as
  each analysis lands, so a partial build must succeed rather than crash.
* Nothing is invented. A sheet whose source JSON is absent is written with a
  single explanatory row saying so, not silently omitted - an absent worksheet
  reads as "not applicable", which is a different claim.

Usage:  python tools/obj007_build_workbooks.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from paths import workspace_root  # OBJ-025: one resolver, marker-based
ROOT = workspace_root(__file__)
# OBJ-025 split the former single document/data/ by measured provenance: the
# authored inputs a human maintains, and the generated ones an obj007_* analyser
# writes. This builder consumes both halves, so it searches both rather than
# pinning one and silently reporting the other half as missing.
DATA_AUTHORED = ROOT / "data" / "analysis"
DATA_GENERATED = ROOT / "artifacts" / "analysis-data"
DATA_ROOTS = (DATA_AUTHORED, DATA_GENERATED)
OUT = ROOT / "artifacts" / "workbooks"

# Excel hard limits / practical caps
MAX_CELL_CHARS = 32000
MAX_COL_WIDTH = 70
MIN_COL_WIDTH = 10

HEADER_FILL = PatternFill("solid", fgColor="1F3864")
HEADER_FONT = Font(bold=True, color="FFFFFF", size=10)
TITLE_FONT = Font(bold=True, size=14, color="1F3864")
NOTE_FONT = Font(italic=True, color="606060", size=9)
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

VERDICT_FILL = {
    "PASS": PatternFill("solid", fgColor="C6EFCE"),
    "FAIL": PatternFill("solid", fgColor="FFC7CE"),
    "NOT RUN": PatternFill("solid", fgColor="FFEB9C"),
    "NOT_RUN": PatternFill("solid", fgColor="FFEB9C"),
    "NOT APPLICABLE": PatternFill("solid", fgColor="E7E6E6"),
    "NOT EXECUTED": PatternFill("solid", fgColor="FFEB9C"),
    "UNKNOWN": PatternFill("solid", fgColor="FFEB9C"),
    "CRITICAL": PatternFill("solid", fgColor="FF9999"),
    "HIGH": PatternFill("solid", fgColor="FFC7CE"),
    "MEDIUM": PatternFill("solid", fgColor="FFEB9C"),
    "LOW": PatternFill("solid", fgColor="E7E6E6"),
}

missing_inputs: list[str] = []


def load(name: str):
    """Load a JSON input by name from either analysis-data root.

    Returns None and records the miss if it is in neither."""
    for base in DATA_ROOTS:
        path = base / name
        if not path.exists():
            continue
        try:
            with path.open(encoding="utf-8") as handle:
                return json.load(handle)
        except json.JSONDecodeError as exc:
            missing_inputs.append(f"{name} (invalid JSON: {exc})")
            return None
    missing_inputs.append(name)
    return None


def as_rows(payload, prefer: tuple[str, ...] = ()) -> list[dict]:
    """Normalise a loaded payload into a list of flat dict rows.

    `prefer` names keys whose embedded row list is the real content of a summary
    object (e.g. envelope-shapes.json keeps its 31 shapes under "shapes"). Without
    it a nested summary would collapse into one metric/value row per top-level key,
    burying the detail.
    """
    if payload is None:
        return []
    if isinstance(payload, list):
        return [r for r in payload if isinstance(r, dict)]
    if not isinstance(payload, dict):
        return []

    for key in prefer + ("rows", "data", "items", "records"):
        value = payload.get(key)
        if isinstance(value, list) and value and isinstance(value[0], dict):
            return value

    # A nested summary: unpack to Section / Metric / Value so each leaf is its own
    # row and stays readable, rather than one cell holding "k=v; k=v; k=v".
    return unpack_summary(payload)


def unpack_summary(payload: dict) -> list[dict]:
    """Depth-2 unpack of a summary dict into section/metric/value rows."""
    rows: list[dict] = []
    for section, value in payload.items():
        label = humanise(section)
        if isinstance(value, dict):
            for metric, leaf in value.items():
                rows.append({"section": label, "metric": humanise(metric), "value": flatten(leaf)})
        elif isinstance(value, list):
            if value and isinstance(value[0], dict):
                # A row list under a non-preferred key: summarise, do not drop.
                rows.append({"section": label, "metric": "row count", "value": len(value)})
                for index, item in enumerate(value, start=1):
                    rows.append({"section": label, "metric": f"[{index}]", "value": flatten(item)})
            else:
                rows.append({"section": label, "metric": "count", "value": len(value)})
                rows.append({"section": label, "metric": "values", "value": flatten(value)})
        else:
            rows.append({"section": label, "metric": "", "value": flatten(value)})
    return rows


def flatten(value):
    """Render a value as a cell-safe scalar.

    Numbers pass through so Excel stores them as numbers; everything else is
    rendered to a string and capped at Excel's per-cell limit.
    """
    if value is None:
        return ""
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        text = value
    elif isinstance(value, dict):
        text = "; ".join(f"{k}={flatten(v)}" for k, v in value.items())
    elif isinstance(value, list):
        text = " | ".join(str(flatten(v)) for v in value)
    else:
        text = str(value)
    text = str(text)
    if len(text) > MAX_CELL_CHARS:
        text = text[: MAX_CELL_CHARS - 20] + f"...[{len(text)} chars]"
    return text


def humanise(key: str) -> str:
    return key.replace("_", " ").strip().title()


def write_sheet(wb: Workbook, title: str, rows: list[dict], note: str = "",
                source: str = "", freeze: str = "A4") -> Worksheet:
    """Write one worksheet: title row, provenance row, header, data."""
    ws = wb.create_sheet(title[:31])
    ws["A1"] = title
    ws["A1"].font = TITLE_FONT
    provenance = note or ""
    if source:
        provenance = (provenance + "  ").strip() + f"Source: {source}"
    ws["A2"] = provenance
    ws["A2"].font = NOTE_FONT

    if not rows:
        ws["A3"] = "NO DATA"
        ws["A3"].font = Font(bold=True, color="9C0006")
        ws["A4"] = (
            f"The input {source or 'JSON'} was not produced, so this worksheet is empty. "
            "It is present rather than omitted so the gap is visible instead of reading "
            "as 'not applicable'."
        )
        ws.column_dimensions["A"].width = 120
        return ws

    # Union of keys, preserving first-seen order - rows may be ragged.
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)

    for index, key in enumerate(columns, start=1):
        cell = ws.cell(row=3, column=index, value=humanise(key))
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        cell.border = BORDER

    for r, row in enumerate(rows, start=4):
        for c, key in enumerate(columns, start=1):
            value = flatten(row.get(key))
            cell = ws.cell(row=r, column=c, value=value)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if isinstance(value, str):
                fill = VERDICT_FILL.get(value.strip().upper())
                if fill is not None and len(value) < 40:
                    cell.fill = fill

    # Column widths from a sample - scanning every row is slow at 7k rows.
    sample = rows[:400]
    for index, key in enumerate(columns, start=1):
        longest = max([len(humanise(key))] + [len(str(flatten(r.get(key)))) for r in sample])
        width = max(MIN_COL_WIDTH, min(MAX_COL_WIDTH, longest + 2))
        ws.column_dimensions[get_column_letter(index)].width = width

    ws.freeze_panes = freeze
    ws.auto_filter.ref = (
        f"A3:{get_column_letter(len(columns))}{len(rows) + 3}"
    )
    return ws


def write_index(wb: Workbook, workbook_title: str, entries: list[tuple[str, str, int]]) -> None:
    """Front sheet listing every worksheet, what it holds, and its row count."""
    ws = wb.create_sheet("Index", 0)
    ws["A1"] = workbook_title
    ws["A1"].font = Font(bold=True, size=16, color="1F3864")
    ws["A2"] = (
        "OBJ-007 deliverable. Every figure traces to a file under artifacts/runs/, the automation repo, "
        "or the QA database; where evidence is absent the cell says so rather than carrying a guess."
    )
    ws["A2"].font = NOTE_FONT

    for index, header in enumerate(["Worksheet", "What it holds", "Rows"], start=1):
        cell = ws.cell(row=4, column=index, value=header)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.border = BORDER

    for r, (sheet, description, count) in enumerate(entries, start=5):
        ws.cell(row=r, column=1, value=sheet).font = Font(bold=True)
        ws.cell(row=r, column=2, value=description).alignment = Alignment(wrap_text=True, vertical="top")
        cell = ws.cell(row=r, column=3, value=count)
        cell.alignment = Alignment(horizontal="right")
        if count == 0:
            cell.fill = VERDICT_FILL["FAIL"]

    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 95
    ws.column_dimensions["C"].width = 10

    if missing_inputs:
        start = len(entries) + 7
        ws.cell(row=start, column=1, value="Inputs not produced").font = Font(bold=True, color="9C0006")
        for offset, name in enumerate(sorted(set(missing_inputs)), start=1):
            ws.cell(row=start + offset, column=1, value=name)


# --------------------------------------------------------------------- workbooks

def build_analysis_workbook() -> Path:
    wb = Workbook()
    default_sheet = wb.active
    if default_sheet is not None:
        wb.remove(default_sheet)
    entries: list[tuple[str, str, int]] = []

    # Keys whose embedded row list is the real content, per file.
    prefer = {
        "envelope-shapes.json": ("shapes",),
        "db-schema-map.json": ("objects",),
    }

    sheets = [
        ("Chaining Validation", "chaining-validation.json",
         "One row per hop across all flows, with every L1-L7 verdict, the parent/child "
         "dependency and the extracted identifier. The 196 MISSING ['NEW_ID'] failures live here.", "A1"),
        ("L6 Read-Back", "l6-read-back.json",
         "Every hop where a created object was read back through the API. 2 of 107 passed.", "A4"),
        ("Positive Validation", "positive-validation.json",
         "Every endpoint under positive testing: payload, expected vs actual response, what was "
         "validated and what a correct assertion would also have checked.", "A2"),
        ("Negative Validation", "negative-validation.json",
         "All 1,306 endpoints x >=5 negative scenarios. Expected outcomes are derived from the "
         "contract; actual values are measured only where the run covers them.", "A3"),
        ("Negative Coverage", "negative-coverage-summary.json",
         "Scenario counts by category and controller, and the endpoints with zero existing "
         "negative coverage.", "A3"),
        ("Envelope Shapes", "envelope-shapes.json",
         "Measured distribution of response-envelope shapes. An API with N undocumented shapes "
         "cannot be asserted generically.", "A2"),
        ("Required Fields", "required-fields.json",
         "Per-property mandatory/length/format/pattern metadata, and whether it is declared, "
         "inferred, or absent.", "A5"),
        ("Required Fields Summary", "required-fields-summary.json",
         "The counts behind the required-field finding, including per-controller and the 217 "
         "create endpoints.", "A5"),
        ("Doc Gap Coverage", "doc-gap-coverage.json",
         "Per-controller documentation coverage: endpoints, payload examples, response models, "
         "error codes, business rules.", "A7"),
        ("DB Schema Map", "db-schema-map.json",
         "API object to table to primary key to identifying columns, whether those columns are "
         "encrypted at rest, and the resulting validation approach.", "C"),
    ]

    for title, filename, note, item in sheets:
        rows = as_rows(load(filename), prefer.get(filename, ()))
        write_sheet(wb, title, rows, note=f"[{item}]", source=f"data/analysis/{filename}")
        entries.append((title[:31], note, len(rows)))

    # envelope-shapes.json and db-schema-map.json carry further sections beyond the
    # row list used above. Surface them rather than letting them go unread.
    extra = [
        ("Envelope Shape Totals", "envelope-shapes.json", "pam_envelope_shape_totals",
         "Totals per PamEnvelope.Shape class. All 8 occur in the evidence - none is speculative.", "A2"),
        ("DB Schema Detail", "db-schema-map.json", None,
         "Validation levers, referential-integrity findings and framework wiring from the schema study.", "C"),
    ]

    # The zero-coverage endpoint list is 1,289 entries. Left inside the summary it
    # collapses into one truncated cell, which would hide the very list that makes
    # the finding actionable - so it gets its own worksheet.
    summary = load("negative-coverage-summary.json") or {}
    uncovered = summary.get("endpoints_with_zero_live_negative_coverage") or []
    uncovered_rows = [
        {"#": index, "endpoint": entry} if not isinstance(entry, dict) else {"#": index, **entry}
        for index, entry in enumerate(uncovered, start=1)
    ]
    write_sheet(wb, "No Negative Coverage", uncovered_rows,
                note="[A3] Endpoints with zero runnable negative coverage today - the itemised work list.",
                source="artifacts/analysis-data/negative-coverage-summary.json")
    entries.append(("No Negative Coverage",
                    "Every endpoint with zero runnable negative coverage - 1,289 of 1,306. Itemised so it "
                    "can be handed over as a work list rather than quoted as a percentage.", len(uncovered_rows)))
    for title, filename, section, note, item in extra:
        payload = load(filename)
        if payload is None:
            rows = []
        elif section:
            rows = as_rows(payload.get(section))
        else:
            rows = unpack_summary({k: v for k, v in payload.items() if k != "objects"})
        write_sheet(wb, title, rows, note=f"[{item}] {note}", source=f"data/analysis/{filename}")
        entries.append((title[:31], note, len(rows)))

    write_index(wb, "PAM API - Validation Analysis", entries)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "PAM-API-Validation-Analysis.xlsx"
    wb.save(path)
    return path


def merge_solutions() -> list[dict]:
    """Merge every solutions-*.json into one ordered list."""
    merged: list[dict] = []
    for path in sorted(DATA.glob("solutions*.json")):
        try:
            with path.open(encoding="utf-8") as handle:
                payload = json.load(handle)
        except json.JSONDecodeError as exc:
            missing_inputs.append(f"{path.name} (invalid JSON: {exc})")
            continue
        for row in as_rows(payload):
            row.setdefault("source_file", path.name)
            merged.append(row)
    if not merged:
        missing_inputs.append("solutions-*.json (none found)")
    return merged


def build_governance_workbook() -> Path:
    wb = Workbook()
    default_sheet = wb.active
    if default_sheet is not None:
        wb.remove(default_sheet)
    entries: list[tuple[str, str, int]] = []

    observations = as_rows(load("observations.json"))
    write_sheet(wb, "Observations", observations, note="[D] Updated continuously.",
                source="data/analysis/observations.json")
    entries.append(("Observations", "Daily issues, technical blockers, missing documentation, missing APIs, "
                                   "framework and product limitations, suggestions and workarounds.",
                    len(observations)))

    findings = as_rows(load("management-findings.json"))
    write_sheet(wb, "Management Findings", findings, note="[D] Escalation view.",
                source="data/analysis/management-findings.json")
    entries.append(("Management Findings", "Missing documentation, developer dependencies, framework "
                                           "limitations, product issues, missing validations, risks, action "
                                           "items, ownership, priority and recommendations.", len(findings)))

    solutions = merge_solutions()
    write_sheet(wb, "Solutions", solutions,
                note="[A8] Two solutions per issue - recommended and alternative.",
                source="data/analysis/solutions-*.json (merged)")
    entries.append(("Solutions", "Every issue raised, each with a recommended and an alternative solution, "
                                 "advantages, disadvantages and estimated effort.", len(solutions)))

    db_observations = as_rows(load("db-observations.json"))
    write_sheet(wb, "DB Observations", db_observations, note="[C] QA read-only.",
                source="data/analysis/db-observations.json")
    entries.append(("DB Observations", "Every database observation, each carrying the query that produced it.",
                    len(db_observations)))

    write_index(wb, "PAM API - Project Governance", entries)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "PAM-Project-Governance.xlsx"
    wb.save(path)
    return path


def main() -> int:
    analysis = build_analysis_workbook()
    governance = build_governance_workbook()

    print(f"built  {analysis.relative_to(ROOT)}")
    print(f"built  {governance.relative_to(ROOT)}")
    if missing_inputs:
        print("\ninputs not yet produced (worksheets written empty, and flagged on each Index):")
        for name in sorted(set(missing_inputs)):
            print(f"  - {name}")
        print("\nRe-run this script once the analyses land; it is idempotent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
