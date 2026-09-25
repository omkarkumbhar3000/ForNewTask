#!/usr/bin/env python3
"""OBJ-010 - inventory every API test the framework implements, before executing anything.

Answers four questions that the execution plan depends on, all from repo assets:

  1. Which API test classes exist?                     src/test/java/com/arcon/tests/API/**
  2. Which are reachable through a live suite XML?     API_Suites/ + CICD_Suites/, comments stripped
  3. What endpoint rows does each class actually drive? dataprovider/*.java -> testdata/*.xls
  4. Which of those rows hit a blocklisted endpoint?    chain_runner.ENDPOINT_BLOCKLIST

Output: .obj010/inventory.json  plus a human summary on stdout.
Zero HTTP calls. Reads only; writes one JSON file.

  python tools/obj010_inventory.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from paths import workspace_root  # OBJ-025: one resolver, marker-based

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from chain_runner import REPO, ENDPOINT_BLOCKLIST          # noqa: E402

OUT_DIR = workspace_root(__file__) / "state" / "obj010"
TESTS = REPO / "src" / "test" / "java" / "com" / "arcon" / "tests" / "API"
DP_DIR = REPO / "src" / "test" / "java" / "com" / "arcon" / "dataprovider"
TESTDATA = REPO / "testdata"
SUITE_DIRS = ["API_Suites", "CICD_Suites"]

# Workbook name -> file, as the env file maps them (QA_MsSQL.properties).
WORKBOOKS = {
    "API_ExcelDataProviderFileName": "API_Automation_Test_Input_Data.xls",
    "Negative_API_ExcelDataProviderFileName": "Negative_API_Automation_Test_Input_Data.xls",
    "ExcelDataProviderFileName": "Automation_Test_Input_Data.xls",
}

BLOCK_RE = re.compile("|".join(re.escape(k) for k in ENDPOINT_BLOCKLIST), re.I)


def strip_block_comments(src: str) -> str:
    """Remove /* */ and //-to-EOL so a commented-out @DataProvider never counts as live."""
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    return re.sub(r"(?m)^\s*//.*$", "", src)


def parse_dataproviders() -> dict:
    """provider name -> {workbook, sheet, table, file}. Live definitions only."""
    out = {}
    for jf in sorted(DP_DIR.glob("*DataProviderUtils.java")):
        live = strip_block_comments(jf.read_text(encoding="utf-8", errors="replace"))
        # @DataProvider(name="X") ... getTableArray(... <WorkbookKey>, "Sheet", "Table")
        for m in re.finditer(
            r'@DataProvider\s*\(\s*name\s*=\s*"([^"]+)"\s*\).*?'
            r'getTableArray\s*\((.*?)\)\s*;',
            live, re.S,
        ):
            name, args = m.group(1), m.group(2)
            wb = next((k for k in WORKBOOKS if k in args), None)
            quoted = re.findall(r'"([^"]*)"', args)
            # drop the path fragments ("testdata", separators) - sheet/table are the last two
            meaningful = [q for q in quoted if q and q != "testdata"]
            sheet = meaningful[-2] if len(meaningful) >= 2 else None
            table = meaningful[-1] if len(meaningful) >= 1 else None
            out[name] = {"workbook": wb, "sheet": sheet, "table": table, "file": jf.name}
    return out


def parse_test_classes() -> list:
    """Every API test class, with the providers its live @Test methods consume."""
    rows = []
    for jf in sorted(TESTS.rglob("*.java")):
        raw = jf.read_text(encoding="utf-8", errors="replace")
        live = strip_block_comments(raw)
        fqn = (str(jf.relative_to(REPO / "src" / "test" / "java"))
               .replace("\\", ".").replace("/", ".")[:-5])
        tests = re.findall(r"@Test\s*\(([^)]*)\)", live, re.S)
        providers, enabled_flags = [], []
        for t in tests:
            pm = re.search(r'dataProvider\s*=\s*"([^"]+)"', t)
            if pm:
                providers.append(pm.group(1))
            em = re.search(r"enabled\s*=\s*(true|false)", t)
            enabled_flags.append(em.group(1) if em else "true")
        rows.append({
            "fqn": fqn,
            "folder": fqn.split(".")[4] if len(fqn.split(".")) > 4 else "",
            "simple": fqn.rsplit(".", 1)[-1],
            "test_methods": len(tests),
            "providers": sorted(set(providers)),
            "all_disabled": bool(enabled_flags) and all(f == "false" for f in enabled_flags),
        })
    return rows


def parse_suites() -> tuple[set, dict]:
    """Classes referenced by live (uncommented) <class name=...> entries."""
    referenced, by_suite = set(), {}
    for d in SUITE_DIRS:
        for xf in sorted((REPO / d).rglob("*.xml")):
            raw = xf.read_text(encoding="utf-8", errors="replace")
            live = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
            names = re.findall(r'<class\s+name="([^"]+)"', live)
            rel = str(xf.relative_to(REPO)).replace("\\", "/")
            by_suite[rel] = {
                "classes": names,
                "has_listener": "<listeners>" in live,
                "parallel": (re.search(r'parallel="([^"]+)"', live) or [None, None])[1],
            }
            referenced.update(names)
    return referenced, by_suite


def read_named_table(sheet, table: str):
    """Replicate ExcelUtils.getTableArray: two diagonal marker cells named `table`.

    startRow = firstMarker.row + 1 (header row); data rows are startRow+1..endRow.
    Columns are startCol+1 .. endCol-1.
    """
    hits = []
    for r in range(sheet.nrows):
        for c in range(sheet.ncols):
            v = sheet.cell_value(r, c)
            if isinstance(v, str) and v.strip() == table:
                hits.append((r, c))
    if len(hits) < 2:
        return None, None, f"markers found: {len(hits)}"
    (r0, c0) = hits[0]
    end = next(((r, c) for (r, c) in hits[1:] if r > r0 and c > c0), None)
    if end is None:
        return None, None, "no diagonal closing marker"
    r1, c1 = end
    hdr_row = r0 + 1
    cols = list(range(c0 + 1, c1))
    header = [str(sheet.cell_value(hdr_row, c)).strip() for c in cols]
    data = []
    for r in range(hdr_row + 1, r1 + 1):
        data.append([str(sheet.cell_value(r, c)).strip() for c in cols])
    return header, data, None


def main() -> int:
    try:
        import xlrd
    except ImportError:
        print("xlrd is required: pip install xlrd", file=sys.stderr)
        return 2

    providers = parse_dataproviders()
    classes = parse_test_classes()
    referenced, by_suite = parse_suites()

    books = {}
    for key, fname in WORKBOOKS.items():
        p = TESTDATA / fname
        if p.is_file():
            books[key] = xlrd.open_workbook(str(p), on_demand=True)

    # provider -> rows + blocklist hits
    prov_rows, prov_err = {}, {}
    for name, meta in providers.items():
        wb = books.get(meta["workbook"] or "")
        if wb is None or not meta["sheet"] or not meta["table"]:
            prov_err[name] = f"unresolved workbook/sheet/table: {meta}"
            continue
        try:
            sheet = wb.sheet_by_name(meta["sheet"])
        except Exception as exc:
            prov_err[name] = f"sheet '{meta['sheet']}' missing: {exc}"
            continue
        header, data, err = read_named_table(sheet, meta["table"])
        if err:
            prov_err[name] = f"table '{meta['table']}': {err}"
            continue
        low = [h.lower() for h in header]
        ep_i = next((i for i, h in enumerate(low) if "endpoint" in h), None)
        vb_i = next((i for i, h in enumerate(low) if "requesttype" in h or h == "method"), None)
        eps = []
        for row in data:
            ep = row[ep_i] if ep_i is not None and ep_i < len(row) else ""
            vb = row[vb_i] if vb_i is not None and vb_i < len(row) else ""
            if ep:
                eps.append({"endpoint": ep, "verb": vb,
                            "blocked": bool(BLOCK_RE.search(ep))})
        prov_rows[name] = {"header": header, "row_count": len(data), "endpoints": eps,
                           "blocked_count": sum(1 for e in eps if e["blocked"])}

    # roll up onto classes
    for c in classes:
        c["referenced_by_live_suite"] = c["fqn"] in referenced
        rows = blocked = 0
        unresolved = []
        for p in c["providers"]:
            if p in prov_rows:
                rows += prov_rows[p]["row_count"]
                blocked += prov_rows[p]["blocked_count"]
            else:
                unresolved.append(p)
        c["data_rows"] = rows
        c["blocked_rows"] = blocked
        c["unresolved_providers"] = unresolved
        c["touches_blocklist"] = blocked > 0

    OUT_DIR.mkdir(exist_ok=True)
    payload = {
        "blocklist": ENDPOINT_BLOCKLIST,
        "providers": providers,
        "provider_rows": {k: {"row_count": v["row_count"],
                              "blocked_count": v["blocked_count"],
                              "header": v["header"]} for k, v in prov_rows.items()},
        "provider_errors": prov_err,
        "classes": classes,
        "suites": by_suite,
    }
    (OUT_DIR / "inventory.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    # ---- summary
    tot = len(classes)
    ref = sum(1 for c in classes if c["referenced_by_live_suite"])
    blk = [c for c in classes if c["touches_blocklist"]]
    dis = [c for c in classes if c["all_disabled"]]
    unres = [c for c in classes if c["unresolved_providers"]]
    print(f"API test classes            : {tot}")
    print(f"  reachable via live suite  : {ref}")
    print(f"  NOT in any live suite     : {tot - ref}")
    print(f"  every @Test disabled      : {len(dis)}")
    print(f"providers (live)            : {len(providers)}")
    print(f"  resolved to Excel rows    : {len(prov_rows)}")
    print(f"  unresolved                : {len(prov_err)}")
    print(f"total data rows addressed    : {sum(c['data_rows'] for c in classes)}")
    print(f"rows hitting blocklist       : {sum(c['blocked_rows'] for c in classes)}")
    print()
    print(f"CLASSES TOUCHING BLOCKLIST ({len(blk)}) - these must be reported Blocked, not skipped:")
    for c in sorted(blk, key=lambda x: -x["blocked_rows"]):
        print(f"  {c['fqn']}  blocked_rows={c['blocked_rows']}/{c['data_rows']}")
    if prov_err:
        print(f"\nUNRESOLVED PROVIDERS ({len(prov_err)}) - first 15:")
        for k, v in list(prov_err.items())[:15]:
            print(f"  {k}: {v}")
    by_folder = defaultdict(lambda: [0, 0])
    for c in classes:
        by_folder[c["folder"]][0] += 1
        if c["referenced_by_live_suite"]:
            by_folder[c["folder"]][1] += 1
    print("\nby folder (total / in a live suite):")
    for f, (t, r) in sorted(by_folder.items()):
        print(f"  {f:<22} {t:>4} / {r:>4}")
    print(f"\nwrote {OUT_DIR / 'inventory.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
