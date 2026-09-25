#!/usr/bin/env python3
"""Build artifacts/workbooks/PAM-Project-Knowledge-Base.xlsx from data/questions/questions-*.json.

OBJ-008. This is the ONLY thing that writes the workbook - edit the JSON and re-run.
A hand edit to the .xlsx is discarded on the next build.

Design decisions worth knowing before changing anything:

* ONE master Q&A sheet with a Category column, not per-topic sheets. Per-topic
  sheets force a filing decision on every new question and invite the same answer
  living in two places, which is how a knowledge base goes stale. Autofilter gives
  every per-topic view without duplicating a row.
* Rows are VALIDATED, not trusted. A row with no evidence, a duplicate id or an
  unknown status is reported loudly and marked in the sheet rather than silently
  written - the whole value of this artifact is that a cited answer can be checked.
* Demo Flow references question IDs; it never copies answer text.

Usage:  python tools/build_knowledge_base.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from paths import workspace_root  # OBJ-025: one resolver, marker-based
ROOT = workspace_root(__file__)
DATA = ROOT / "data" / "questions"
OUT = ROOT / "artifacts" / "workbooks" / "PAM-Project-Knowledge-Base.xlsx"

MAX_CELL_CHARS = 32000

# Column order for the master sheet. Question / Answer / Evidence / Comments are the
# owner's required minimum and lead deliberately; the rest are metadata.
COLUMNS: list[tuple[str, str, int]] = [
    ("id", "ID", 12),
    ("question", "Question", 58),
    ("answer", "Answer", 95),
    ("evidence", "Evidence", 55),
    ("comments", "Comments", 55),
    ("category", "Category", 26),
    ("module", "Module", 14),
    ("source", "Source", 20),
    ("example", "Example", 55),
    ("api_reference", "Swagger / API Reference", 30),
    ("related_documents", "Related Documents", 42),
    ("status", "Status", 20),
    ("severity_or_impact", "Impact", 14),
    ("audience", "Audience", 24),
    ("owner", "Owner", 18),
    ("last_updated", "Last Updated", 14),
]

REQUIRED = ("id", "question", "answer", "evidence")
VALID_STATUS = {"Answered", "Answered - with caveats", "Open", "Superseded"}

HEADER_FILL = PatternFill("solid", fgColor="1F3864")
HEADER_FONT = Font(bold=True, color="FFFFFF", size=10)
TITLE_FONT = Font(bold=True, size=16, color="1F3864")
SUB_FONT = Font(italic=True, color="606060", size=9)
THIN = Side(style="thin", color="D0D0D0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

STATUS_FILL = {
    "Answered": PatternFill("solid", fgColor="C6EFCE"),
    "Answered - with caveats": PatternFill("solid", fgColor="FFEB9C"),
    "Open": PatternFill("solid", fgColor="FFC7CE"),
    "Superseded": PatternFill("solid", fgColor="E7E6E6"),
}
IMPACT_FILL = {
    "Critical": PatternFill("solid", fgColor="FF9999"),
    "High": PatternFill("solid", fgColor="FFC7CE"),
    "Medium": PatternFill("solid", fgColor="FFEB9C"),
    "Low": PatternFill("solid", fgColor="E7E6E6"),
    "Informational": PatternFill("solid", fgColor="DDEBF7"),
}

problems: list[str] = []


def cell_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        text = " · ".join(str(v) for v in value)
    elif isinstance(value, dict):
        text = "; ".join(f"{k}={v}" for k, v in value.items())
    else:
        text = str(value)
    if len(text) > MAX_CELL_CHARS:
        text = text[: MAX_CELL_CHARS - 20] + f"...[{len(text)} chars]"
    return text.strip()


def load_rows() -> list[dict]:
    """Load and merge every questions-*.json, validating as we go."""
    files = sorted(DATA.glob("questions*.json"))
    if not files:
        problems.append(f"no questions*.json found under {DATA}")
        return []

    rows: list[dict] = []
    seen_ids: dict[str, str] = {}
    for path in files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            problems.append(f"{path.name}: invalid JSON - {exc}")
            continue
        if not isinstance(payload, list):
            problems.append(f"{path.name}: expected a JSON list, got {type(payload).__name__}")
            continue

        for index, raw in enumerate(payload, start=1):
            if not isinstance(raw, dict):
                problems.append(f"{path.name}[{index}]: not an object")
                continue
            row = {key: cell_text(raw.get(key)) for key, _, _ in COLUMNS}
            row["_file"] = path.name

            missing = [k for k in REQUIRED if not row.get(k)]
            if missing:
                problems.append(f"{path.name} {row.get('id') or f'[{index}]'}: missing {', '.join(missing)}")
                # An uncited answer is flagged in the sheet, not silently accepted.
                if "evidence" in missing:
                    row["evidence"] = "⚠️ NO EVIDENCE CITED - answer unverified"
                    row["status"] = "Open"

            if row["id"] in seen_ids:
                problems.append(f"duplicate id {row['id']} in {path.name} (first seen in {seen_ids[row['id']]})")
            else:
                seen_ids[row["id"]] = path.name

            if row["status"] and row["status"] not in VALID_STATUS:
                problems.append(f"{row['id']}: unknown status {row['status']!r}")
            if not row["status"]:
                row["status"] = "Answered"
            if not row["last_updated"]:
                row["last_updated"] = "2026-08-04"

            rows.append(row)

    # Category, then ID - so a reader scrolling sees a coherent narrative per topic.
    rows.sort(key=lambda r: (r["category"], r["id"]))
    return rows


def write_qa_sheet(wb: Workbook, rows: list[dict]) -> None:
    ws = wb.create_sheet("Q&A")
    ws["A1"] = "PAM API Automation — Project Knowledge Base"
    ws["A1"].font = TITLE_FONT
    ws["A2"] = (
        f"{len(rows)} questions. Filter on Category, Audience, Status or Impact using the header "
        "dropdowns. Every Evidence cell names something you can open — if it does not, the row is "
        "flagged. Source of truth: data/questions/questions-*.json — never edit this workbook by hand."
    )
    ws["A2"].font = SUB_FONT

    header_row = 4
    for col, (_, label, width) in enumerate(COLUMNS, start=1):
        cell = ws.cell(row=header_row, column=col, value=label)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        cell.border = BORDER
        ws.column_dimensions[get_column_letter(col)].width = width
    ws.row_dimensions[header_row].height = 28

    status_col = next(i for i, (k, _, _) in enumerate(COLUMNS, start=1) if k == "status")
    impact_col = next(i for i, (k, _, _) in enumerate(COLUMNS, start=1) if k == "severity_or_impact")

    for offset, row in enumerate(rows):
        r = header_row + 1 + offset
        for col, (key, _, _) in enumerate(COLUMNS, start=1):
            cell = ws.cell(row=r, column=col, value=row.get(key, ""))
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = BORDER
        ws.cell(row=r, column=1).font = Font(bold=True, size=9)
        ws.cell(row=r, column=2).font = Font(bold=True)
        fill = STATUS_FILL.get(row.get("status", ""))
        if fill:
            ws.cell(row=r, column=status_col).fill = fill
        fill = IMPACT_FILL.get(row.get("severity_or_impact", ""))
        if fill:
            ws.cell(row=r, column=impact_col).fill = fill

    last = header_row + len(rows)
    ws.auto_filter.ref = f"A{header_row}:{get_column_letter(len(COLUMNS))}{last}"
    ws.freeze_panes = f"C{header_row + 1}"   # keep ID + Question visible while scrolling

    # Dropdown on Status so a maintainer editing the JSON knows the allowed values.
    if rows:
        validation = DataValidation(
            type="list", formula1='"' + ",".join(sorted(VALID_STATUS)) + '"', allow_blank=True
        )
        ws.add_data_validation(validation)
        validation.add(f"{get_column_letter(status_col)}{header_row + 1}:{get_column_letter(status_col)}{last}")


def write_index_sheet(wb: Workbook, rows: list[dict]) -> None:
    ws = wb.create_sheet("Index", 0)
    ws["A1"] = "Knowledge Base — Index"
    ws["A1"].font = TITLE_FONT
    ws["A2"] = (
        "OBJ-008. Read the Q&A sheet end to end to understand the project, or filter it by Category. "
        "Demo Flow gives a suggested walkthrough order for a live demonstration."
    )
    ws["A2"].font = SUB_FONT

    line = 4

    def block(title: str, counts: Counter, note: str = "") -> None:
        nonlocal line
        ws.cell(row=line, column=1, value=title).font = Font(bold=True, size=12, color="1F3864")
        if note:
            ws.cell(row=line, column=3, value=note).font = SUB_FONT
        line += 1
        for header_col, header in ((1, "Value"), (2, "Questions")):
            cell = ws.cell(row=line, column=header_col, value=header)
            cell.fill = HEADER_FILL
            cell.font = HEADER_FONT
        line += 1
        for key, count in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
            ws.cell(row=line, column=1, value=key)
            c = ws.cell(row=line, column=2, value=count)
            c.alignment = Alignment(horizontal="right")
            line += 1
        line += 1

    block("By category", Counter(r["category"] for r in rows), "the main organising axis - filter Q&A on this")
    block("By audience", Counter(a.strip() for r in rows for a in r["audience"].split("·") if a.strip()))
    block("By status", Counter(r["status"] for r in rows), "Open = not yet answerable from evidence")
    block("By impact", Counter(r["severity_or_impact"] for r in rows))
    block("By owning team", Counter(r["owner"] for r in rows))

    ws.cell(row=line, column=1, value="How to add a question").font = Font(bold=True, size=12, color="1F3864")
    line += 1
    for step in (
        "1. Add a row object to the appropriate data/questions/questions-*.json.",
        "2. Every row needs at minimum: id, question, answer, evidence.",
        "3. Evidence must name something openable — a file, report, run folder, file.java:line, SQL query or <doc>:p<N>.",
        "4. If the answer is not yet known, still add the question with status = Open and say what would settle it.",
        "5. Re-run: python tools/build_knowledge_base.py",
        "Never edit this workbook directly — the next build discards it.",
    ):
        ws.cell(row=line, column=1, value=step)
        line += 1

    ws.column_dimensions["A"].width = 46
    ws.column_dimensions["B"].width = 12
    ws.column_dimensions["C"].width = 60

    if problems:
        line += 1
        ws.cell(row=line, column=1, value=f"⚠️ {len(problems)} validation problem(s)").font = Font(
            bold=True, color="9C0006"
        )
        line += 1
        for problem in problems[:60]:
            ws.cell(row=line, column=1, value=problem)
            line += 1


def write_demo_sheet(wb: Workbook, rows: list[dict]) -> None:
    """An ordered walkthrough. References IDs only - never copies answer text."""
    ws = wb.create_sheet("Demo Flow")
    ws["A1"] = "Suggested demonstration order"
    ws["A1"].font = TITLE_FONT
    ws["A2"] = (
        "Each step names a Category to filter the Q&A sheet on, and why that step comes where it does. "
        "It references questions rather than copying them, so it can never fall out of step with the answers."
    )
    ws["A2"].font = SUB_FONT

    steps = [
        ("1", "Project & Scope", "Start with what the project is for and what has been delivered. "
         "Sets the frame before any number is quoted."),
        ("2", "Metrics & Measured Figures", "Establish that every figure has a provenance — and that "
         "several previously circulated figures were wrong and are now settled. Credibility first."),
        ("3", "API Surface & Contract", "How large the surface is and what is actually being tested."),
        ("4", "Response Envelope & Shapes", "THE pivotal section. A rejected request returns HTTP 200, "
         "so a status-only assertion passes against failure. Everything downstream follows from this."),
        ("5", "Positive Validation", "What was validated, and the gap between 'validated' and "
         "'should be validated'."),
        ("6", "API Chaining & Multi-hop", "Walk the one flow that works end to end, then explain why "
         "only 2 of 326 did."),
        ("7", "Mandatory Fields & Schema", "Why creates cannot be driven — the root cause behind the "
         "chaining failures."),
        ("8", "Negative Validation", "The 10,448-scenario design, and the honest state of what runs today."),
        ("9", "Framework & Architecture", "What was built to fix the validation depth, and how it is verified."),
        ("10", "Database Validation", "The new capability: proving a record actually landed."),
        ("11", "Security & Credentials", "The incidental product security findings. Expect questions."),
        ("12", "Developer Findings & Defects", "The 12 findings and their Jira state."),
        ("13", "Documentation & Knowledge Sources", "What documentation can and cannot answer."),
        ("14", "Risks, Blockers & Escalations", "What is blocked, on whom, and at what priority."),
        ("15", "Roadmap & Next Steps", "Close on sequence and ownership — what starts today with no "
         "developer dependency."),
    ]

    header_row = 4
    for col, label in enumerate(("Step", "Filter Q&A Category on", "Why here", "Questions"), start=1):
        cell = ws.cell(row=header_row, column=col, value=label)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.border = BORDER

    by_category: defaultdict[str, list[str]] = defaultdict(list)
    for row in rows:
        by_category[row["category"]].append(row["id"])

    for offset, (step, category, why) in enumerate(steps):
        r = header_row + 1 + offset
        ws.cell(row=r, column=1, value=step).font = Font(bold=True)
        ws.cell(row=r, column=2, value=category).font = Font(bold=True)
        ws.cell(row=r, column=3, value=why).alignment = Alignment(wrap_text=True, vertical="top")
        count = len(by_category.get(category, []))
        cell = ws.cell(row=r, column=4, value=count)
        cell.alignment = Alignment(horizontal="right")
        if count == 0:
            cell.fill = STATUS_FILL["Open"]

    covered = {c for _, c, _ in steps}
    orphans = sorted(set(by_category) - covered)
    if orphans:
        r = header_row + len(steps) + 2
        ws.cell(row=r, column=1, value="Categories not in the demo order (still in Q&A):").font = Font(bold=True)
        for offset, category in enumerate(orphans, start=1):
            ws.cell(row=r + offset, column=2, value=category)
            ws.cell(row=r + offset, column=4, value=len(by_category[category]))

    ws.column_dimensions["A"].width = 8
    ws.column_dimensions["B"].width = 32
    ws.column_dimensions["C"].width = 88
    ws.column_dimensions["D"].width = 12


def main() -> int:
    rows = load_rows()

    wb = Workbook()
    default = wb.active
    if default is not None:
        wb.remove(default)

    write_qa_sheet(wb, rows)
    write_demo_sheet(wb, rows)
    write_index_sheet(wb, rows)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)

    print(f"built  {OUT.relative_to(ROOT)}")
    print(f"       {len(rows)} questions across {len({r['category'] for r in rows})} categories")
    for category, count in sorted(Counter(r["category"] for r in rows).items()):
        print(f"         {count:>4}  {category}")
    if problems:
        # ASCII only from here: this console is cp1252 and an em-dash or an emoji in a
        # print() raises UnicodeEncodeError, which would mask the very problems being
        # reported. Cell values keep their Unicode - only stdout is constrained.
        print(f"\n!! {len(problems)} validation problem(s) - also listed on the Index sheet:")
        for problem in problems[:40]:
            print(f"   - {problem.encode('ascii', 'replace').decode('ascii')}")
        if len(problems) > 40:
            print(f"   ... and {len(problems) - 40} more")
        return 1
    print("\nall rows validated: ids unique, evidence present, statuses known")
    return 0


if __name__ == "__main__":
    sys.exit(main())
