#!/usr/bin/env python3
"""OBJ-010 - the canonical reader for the bootstrap's Excel-driven API test data.

Why this exists as its own module
---------------------------------
`obj010_inventory.py` resolved a provider's workbook with
`next(k for k in WORKBOOKS if k in args)`. `API_ExcelDataProviderFileName` is a
SUBSTRING of `Negative_API_ExcelDataProviderFileName`, so all 376 providers declared in
`Negative_API_DataProviderUtils.java` were looked up in the positive workbook and
reported as "sheet missing". That understated the resolvable corpus by ~2,450 rows.
Longest-key-wins fixes it. Both the inventory and the flow generator now read through
here so the bug cannot come back in one place only.

The bootstrap repo is a REFERENCE ASSET. Nothing here executes anything; it turns the
QA team's hand-written Excel scenarios into data the dynamic framework can generate from.

  python tools/obj010_datatables.py            # census to stdout
  python tools/obj010_datatables.py --json     # machine-readable census
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from chain_runner import REPO                                        # noqa: E402

DP_DIR = REPO / "src" / "test" / "java" / "com" / "arcon" / "dataprovider"
TESTDATA = REPO / "testdata"

# Env-file key -> workbook. Longest matching key wins; see the module docstring.
WORKBOOKS = {
    "API_ExcelDataProviderFileName": "API_Automation_Test_Input_Data.xls",
    "Negative_API_ExcelDataProviderFileName": "Negative_API_Automation_Test_Input_Data.xls",
    "ExcelDataProviderFileName": "Automation_Test_Input_Data.xls",
}

# The two header shapes that describe an executable API call.
POS_HEADER = ("InputType", "ModuleName", "RequestType", "EndPoint", "Payload",
              "ExpectedStatus")
NEG_HEADER = ("InputType", "ModuleName", "RequestType", "EndPoint", "Payload",
              "ExpectedHTTPStatus", "ExpectedErrorCode")


def strip_block_comments(src: str) -> str:
    """A commented-out @DataProvider is not live data."""
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    return re.sub(r"(?m)^\s*//.*$", "", src)


def workbook_key(args: str) -> str | None:
    """Longest key wins, so Negative_API_... is never swallowed by API_...."""
    hits = [k for k in WORKBOOKS if k in args]
    return max(hits, key=len) if hits else None


def parse_dataproviders() -> dict:
    """(provider file, provider name) -> {workbook, sheet, table}."""
    out = {}
    for jf in sorted(DP_DIR.glob("*DataProviderUtils.java")):
        live = strip_block_comments(jf.read_text(encoding="utf-8", errors="replace"))
        for m in re.finditer(
            r'@DataProvider\s*\(\s*name\s*=\s*"([^"]+)"\s*\).*?getTableArray\s*\((.*?)\)\s*;',
            live, re.S,
        ):
            name, args = m.group(1), m.group(2)
            quoted = [q for q in re.findall(r'"([^"]*)"', args) if q and q != "testdata"]
            out[(jf.name, name)] = {
                "workbook": workbook_key(args),
                "sheet": quoted[-2] if len(quoted) >= 2 else None,
                "table": quoted[-1] if quoted else None,
            }
    return out


def read_named_table(sheet, table: str):
    """Replicate ExcelUtils.getTableArray: two diagonal cells both holding `table`.

    Header row is firstMarker.row + 1; data spans the rows below it up to the closing
    marker, columns strictly between the two marker columns.
    """
    hits = [(r, c)
            for r in range(sheet.nrows)
            for c in range(sheet.ncols)
            if isinstance(sheet.cell_value(r, c), str)
            and sheet.cell_value(r, c).strip() == table]
    if len(hits) < 2:
        return None, None, f"markers found: {len(hits)}"
    r0, c0 = hits[0]
    end = next(((r, c) for (r, c) in hits[1:] if r > r0 and c > c0), None)
    if end is None:
        return None, None, "no diagonal closing marker"
    r1, c1 = end
    cols = list(range(c0 + 1, c1))
    header = [str(sheet.cell_value(r0 + 1, c)).strip() for c in cols]
    data = [[str(sheet.cell_value(r, c)).strip() for c in cols]
            for r in range(r0 + 2, r1 + 1)]
    return header, data, None


def _norm_code(v: str) -> str:
    """Excel stores every number as a float, so '200.0' must read back as '200'."""
    v = (v or "").strip()
    if not v:
        return ""
    try:
        f = float(v)
        return str(int(f)) if f == int(f) else str(f)
    except ValueError:
        return v


def load_api_rows() -> tuple[list[dict], dict]:
    """Every executable API row across all three workbooks, plus a diagnostics dict."""
    import xlrd

    provs = parse_dataproviders()
    books = {}
    for key, fname in WORKBOOKS.items():
        p = TESTDATA / fname
        if p.is_file():
            books[key] = xlrd.open_workbook(str(p), on_demand=True)

    rows: list[dict] = []
    diag = {"providers": len(provs), "resolved": 0, "unresolved": {},
            "non_api_providers": 0, "non_api_rows": 0}

    for (pfile, pname), m in sorted(provs.items()):
        wb = books.get(m["workbook"] or "")
        if wb is None or not m["sheet"] or not m["table"]:
            diag["unresolved"][f"{pfile}:{pname}"] = f"unresolved args: {m}"
            continue
        try:
            sheet = wb.sheet_by_name(m["sheet"])
        except Exception as exc:                                     # noqa: BLE001
            diag["unresolved"][f"{pfile}:{pname}"] = (
                f"sheet '{m['sheet']}' missing from {m['workbook']}: {exc}")
            continue
        header, data, err = read_named_table(sheet, m["table"])
        if err or header is None or data is None:
            diag["unresolved"][f"{pfile}:{pname}"] = f"table '{m['table']}': {err}"
            continue
        diag["resolved"] += 1
        h = tuple(header)
        if h not in (POS_HEADER, NEG_HEADER):
            diag["non_api_providers"] += 1
            diag["non_api_rows"] += len(data)
            continue
        has_error_code = h == NEG_HEADER
        for i, r in enumerate(data):
            d = dict(zip(header, r))
            ep = (d.get("EndPoint") or "").strip()
            if not ep:
                continue
            # Classify by the InputType CELL, not by the header shape. Most tables in
            # Negative_API_Automation_Test_Input_Data.xls carry only ExpectedStatus (no
            # ExpectedErrorCode column) yet every row is InputType=Negative - they assert
            # 405 / 401 at the framework level, where there is no envelope to carry a
            # code. Keying off the header mislabelled 2,368 real negatives as positive.
            it = (d.get("InputType") or "").strip().lower()
            negative = it.startswith("neg") or (has_error_code and not it.startswith("pos"))
            rows.append({
                "provider": pname,
                "provider_file": pfile,
                "workbook": m["workbook"],
                "sheet": m["sheet"],
                "table": m["table"],
                "row_index": i + 1,
                "kind": "negative" if negative else "positive",
                "input_type": d.get("InputType", ""),
                "module": d.get("ModuleName", ""),
                "verb": (d.get("RequestType") or "POST").strip().upper(),
                "endpoint": ep,
                "payload": d.get("Payload") or "",
                "expect_status": _norm_code(d.get("ExpectedHTTPStatus")
                                            or d.get("ExpectedStatus") or ""),
                "expect_error_code": _norm_code(d.get("ExpectedErrorCode", "")),
            })
    return rows, diag


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows, diag = load_api_rows()
    kinds = collections.Counter(r["kind"] for r in rows)
    verbs = collections.Counter(r["verb"] for r in rows)
    prefix = collections.Counter("/" + r["endpoint"].lstrip("/").split("/")[0]
                                 for r in rows)
    surface = collections.Counter(
        "AdminAPI" if r["endpoint"].lstrip("/").lower().startswith("adminapi")
        else "absolute-url" if r["endpoint"].lower().startswith("http")
        else "main /api" for r in rows)
    bad = 0
    for r in rows:
        p = r["payload"].strip()
        if p and p not in ("-", "NA", "N/A"):
            try:
                json.loads(p)
            except Exception:                                        # noqa: BLE001
                bad += 1

    if args.json:
        print(json.dumps({"rows": rows, "diagnostics": diag}, indent=1))
        return 0

    print(f"providers declared      : {diag['providers']}")
    print(f"  resolved to a table   : {diag['resolved']}")
    print(f"  unresolved            : {len(diag['unresolved'])}")
    print(f"  resolved but not API  : {diag['non_api_providers']} "
          f"({diag['non_api_rows']} rows - UI/workflow shapes)")
    print()
    print(f"executable API rows     : {len(rows)}   {dict(kinds)}")
    print(f"  verbs                 : {dict(verbs)}")
    print(f"  surface               : {dict(surface)}")
    print(f"  path prefixes         : {dict(prefix.most_common(8))}")
    print(f"  unparseable payloads  : {bad}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
