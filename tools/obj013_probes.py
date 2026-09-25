"""obj013_probes.py — reality measurement library for the closed loop (OBJ-013 v0.1).

Every probe RE-DERIVES a fact from source. Nothing here reads a document to learn
what is true; documents are the thing being checked, never the source of truth.

⛔ SAFETY — this module is read-only and offline by contract:
   - zero HTTP to the PAM API, ever (no /arcontoken, no endpoint calls)
   - git is invoked local-only: rev-parse / rev-list / status. Never fetch here
     (obj013_gitcheck.py owns the throttled fetch), never pull/push/merge/checkout.
   - no file is written by this module.

A probe returns a Measurement: the value, the unit, and the derivation string that
says exactly how it was obtained, so a reader can re-run it by hand. A probe that
cannot measure returns error=... rather than guessing — an unmeasurable fact is
never auto-fixed.

Usage:
    python obj013_probes.py            # run all probes, human-readable
    python obj013_probes.py --json     # machine-readable, for obj013_scan.py
    python obj013_probes.py graph_nodes suite_counts    # named probes only
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Callable

# OBJ-025: root by marker, not by hops. tools/ sits one level below the root.
from paths import workspace_root  # OBJ-025: one resolver, marker-based
ROOT = workspace_root(__file__)
REPO = ROOT / "Automation gitlab repo" / "pam_automation_bootstrap"
# OBJ-027: the workspace's own graph output, which is where the viewer HTML lives.
GRAPHIFY_OUT = ROOT / "artifacts" / "graph" / "pam-scope" / "graphify-out"
PAM = ROOT / "pam"
SRC = REPO / "src" / "test" / "java" / "com" / "arcon"


@dataclass
class Measurement:
    probe: str
    value: Any = None
    unit: str = ""
    derivation: str = ""
    error: str | None = None
    detail: dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return self.error is None


_REGISTRY: dict[str, Callable[[], Measurement]] = {}


def probe(name: str):
    def deco(fn):
        _REGISTRY[name] = fn
        fn.probe_name = name
        return fn
    return deco


def _text(p: Path) -> str:
    """Read a text file defensively. Never raises on encoding."""
    return p.read_text(encoding="utf-8", errors="replace")


def _lines(p: Path) -> list[str]:
    return _text(p).splitlines()


def _git(repo: Path, *args: str) -> str:
    """Local-only git. Raises on non-zero so callers can degrade gracefully."""
    banned = {"fetch", "pull", "push", "merge", "checkout", "stash",
              "reset", "clean", "rebase", "commit", "cherry-pick"}
    # `stash list` is read-only; `stash` with any other (or no) sub-command is not.
    read_only_exception = args[:2] == ("stash", "list")
    if args and args[0] in banned and not read_only_exception:
        raise RuntimeError(f"obj013_probes refuses state-changing git: {args[0]}")
    out = subprocess.run(["git", "-C", str(repo), *args],
                         capture_output=True, text=True, timeout=60)
    if out.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} -> rc={out.returncode}: {out.stderr.strip()[:200]}")
    return out.stdout.strip()


# ---------------------------------------------------------------- knowledge graph

_GRAPH_SUMMARY_RE = re.compile(
    r"^-\s*(?P<nodes>[\d,]+)\s*nodes\s*[·.]\s*(?P<edges>[\d,]+)\s*edges"
    r"\s*[·.]\s*(?P<comm>[\d,]+)\s*communities"
    r"(?:\s*\(\s*(?P<shown>[\d,]+)\s*shown\s*,\s*(?P<thin>[\d,]+)\s*thin)?", re.M)


def _graph_summary(report: Path) -> dict:
    if not report.exists():
        raise FileNotFoundError(f"{report} does not exist")
    m = _GRAPH_SUMMARY_RE.search(_text(report))
    if not m:
        raise ValueError(f"no '- N nodes · N edges · N communities' line in {report.name}")
    return {k: int(v.replace(",", ""))
            for k, v in m.groupdict().items() if v is not None}


@probe("graph_automation_summary")
def graph_automation_summary() -> Measurement:
    rpt = REPO / "graphify-out" / "GRAPH_REPORT.md"
    try:
        g = _graph_summary(rpt)
    except Exception as e:
        return Measurement("graph_automation_summary", error=str(e))
    return Measurement(
        "graph_automation_summary",
        value=g, unit="nodes/edges/communities",
        derivation="regex '- N nodes · N edges · N communities' over "
                   "Automation gitlab repo/pam_automation_bootstrap/graphify-out/GRAPH_REPORT.md",
        detail=g)


@probe("graph_root_marker")
def graph_root_marker() -> Measurement:
    """CRITICAL: .graphify_root may name a foreign checkout, in which case any
    hook-triggered rebuild writes the WRONG tree. Detect, never rebuild."""
    marker = REPO / "graphify-out" / ".graphify_root"
    if not marker.exists():
        return Measurement("graph_root_marker", error=f"{marker} does not exist")
    declared = _text(marker).lstrip("﻿").strip()   # the marker is written with a BOM
    try:
        same = Path(declared).resolve() == REPO.resolve() if declared else False
    except OSError:
        same = False
    return Measurement(
        "graph_root_marker",
        value=declared, unit="path",
        derivation="content of graphify-out/.graphify_root vs this checkout's real path",
        detail={"declared_root": declared, "actual_repo": str(REPO),
                "points_at_this_checkout": same,
                "REFUSE_REBUILD": not same})


@probe("graph_hooks_installed")
def graph_hooks_installed() -> Measurement:
    hooks = REPO / ".git" / "hooks"
    found = {n: (hooks / n).exists() for n in ("post-commit", "post-checkout")}
    return Measurement(
        "graph_hooks_installed",
        value=found, unit="bool per hook",
        derivation="existence of .git/hooks/post-commit and post-checkout in the automation repo",
        detail=found)


@probe("graph_indexes_validation_pkg")
def graph_indexes_validation_pkg() -> Measurement:
    """The OBJ-007 validation package is what root CLAUDE.md tells agents to use.
    If the graph predates it, every query_graph call returns 'not found'."""
    manifest = REPO / "graphify-out" / "manifest.json"
    pkg = SRC / "utils" / "validation"
    on_disk = sorted(p.name for p in pkg.glob("*.java")) if pkg.exists() else []
    if not manifest.exists():
        return Measurement("graph_indexes_validation_pkg",
                           error=f"{manifest} does not exist", detail={"on_disk": on_disk})
    blob = _text(manifest)
    indexed = [n for n in on_disk if n.replace(".java", "") in blob]
    return Measurement(
        "graph_indexes_validation_pkg",
        value=len(indexed), unit="classes indexed",
        derivation="count of utils/validation/*.java class names appearing in graphify-out/manifest.json",
        detail={"on_disk": on_disk, "on_disk_count": len(on_disk),
                "indexed": indexed, "indexed_count": len(indexed),
                "graph_is_stale": len(indexed) < len(on_disk)})


# ---------------------------------------------------------------- java source facts

@probe("apihelper_gettoken_line")
def apihelper_gettoken_line() -> Measurement:
    """Root CLAUDE.md pins this line number. It moves whenever ApiHelper is edited,
    which is exactly why it must be re-derived rather than trusted."""
    f = SRC / "utils" / "ApiHelper.java"
    if not f.exists():
        return Measurement("apihelper_gettoken_line", error=f"{f} does not exist")
    hits = [i for i, ln in enumerate(_lines(f), 1)
            if re.match(r"\s*public\s+String\s+getToken\s*\(", ln)]
    if len(hits) != 1:
        return Measurement("apihelper_gettoken_line",
                           error=f"expected exactly 1 live getToken declaration, found {len(hits)}: {hits}")
    return Measurement(
        "apihelper_gettoken_line",
        value=hits[0], unit="line number",
        derivation=r"first line matching /^\s*public\s+String\s+getToken\s*\(/ in "
                   "src/test/java/com/arcon/utils/ApiHelper.java (commented twins excluded)",
        detail={"file_lines": len(_lines(f))})


@probe("apihelper_envelope_pins")
def apihelper_envelope_pins() -> Measurement:
    """The dead-block / live-method line pins quoted in root CLAUDE.md §response envelope."""
    f = SRC / "utils" / "ApiHelper.java"
    if not f.exists():
        return Measurement("apihelper_envelope_pins", error=f"{f} does not exist")
    dead_vrc = live_vrc = live_neg = None
    for i, ln in enumerate(_lines(f), 1):
        s = ln.strip()
        if s.startswith("//") and "private String validateResponseErrorCode(" in s and dead_vrc is None:
            dead_vrc = i
        elif not s.startswith("//") and s.startswith("private String validateResponseErrorCode("):
            live_vrc = i
        elif not s.startswith("//") and "public void validateApiResponseWithResponseTime_ExcelBasedsettingnegative(" in s:
            live_neg = i
    return Measurement(
        "apihelper_envelope_pins",
        value={"dead_block_start": dead_vrc, "live_negative_method": live_neg,
               "live_validateResponseErrorCode": live_vrc},
        unit="line numbers",
        derivation="scan of ApiHelper.java distinguishing commented (//) from live declarations",
        detail={"file_lines": len(_lines(f))})


_ENDPOINT_RE = re.compile(r'"(/api/([A-Za-z0-9_]+)/([A-Za-z0-9_]+))')


@probe("endpoint_count")
def endpoint_count() -> Measurement:
    """MULTI-BASIS, and deliberately REPORT-ONLY.

    ⛔ This probe must never drive an auto-fix. The workspace canon is 1,306 distinct
    (controller, action) pairs, but that figure was produced by a script whose exact
    rule is not recorded, and this derivation does not reproduce it: the strict pattern
    yields 1,302 because it cannot match `/api/User` (two segments, no action),
    `/api/User/{id}` (templated) or the three `/api/v1.0/*` forms (the dot breaks the
    character class). 1,302 + those 4 `/api/User` exceptions == 1,306, which is
    consistent with `.claude/rules/api-surface.md` ("the only four exceptions are on
    /api/User"), but consistency is not proof of the original rule.

    Reporting several bases and letting a human settle it is correct. Silently
    rewriting 1,306 -> 1,302 across a dozen documents would be the exact
    "propagate a wrong canonical" failure this loop exists to prevent.
    """
    f = SRC / "autoconfigs" / "APIConfig.java"
    if not f.exists():
        return Measurement("endpoint_count", error=f"{f} does not exist")
    txt = _text(f)

    strict_pairs, strict_paths = set(), set()
    for m in _ENDPOINT_RE.finditer(txt):
        strict_paths.add(m.group(1))
        strict_pairs.add((m.group(2), m.group(3)))

    # Widest basis: every /api/... literal, query string and template stripped.
    loose_paths = set()
    for lit in re.findall(r'"(/api/[^"]*)"', txt):
        loose_paths.add(lit.split("?")[0].rstrip("/"))

    decls = len(re.findall(r"public\s+static\s+String\s+", txt))
    bases = {
        "distinct_controller_action_strict": len(strict_pairs),
        "distinct_api_paths_strict": len(strict_paths),
        "distinct_api_literals_loose": len(loose_paths),
        "public_static_String_declarations": decls,
        "documented_canonical": 1306,
    }
    return Measurement(
        "endpoint_count",
        value=bases, unit="MULTI-BASIS — no single value",
        derivation='strict: distinct (controller, action) from /"(\\/api\\/(\\w+)\\/(\\w+))/; '
                   'loose: every "/api/..." literal with query/template stripped; '
                   "both over APIConfig.java",
        detail=bases | {
            "file_lines": len(_lines(f)),
            "reproduces_documented_canonical": len(strict_pairs) == 1306,
            "policy": "report-only — derivation disagrees with the documented canonical",
            "note": "1,336 counts header and verb constants and is not an endpoint count",
        })


# ---------------------------------------------------------------- inventories

def _count_glob(base: Path, pattern: str) -> int:
    """Count matches under `base`.

    OBJ-025: this used to return 0 for a missing base. A silent 0 is
    indistinguishable from a real measurement of zero, so a folder that moved
    out from under a probe reported a confident, wrong number instead of an
    error. Now it raises — 'I could not measure this' and 'I measured none' are
    different facts and the drift loop is built to tell them apart."""
    if not base.exists():
        raise FileNotFoundError(f"cannot measure {pattern!r}: {base} does not exist")
    return len(list(base.glob(pattern)))


@probe("suite_counts")
def suite_counts() -> Measurement:
    dirs = {
        "CICD_Suites": "*.xml", "CRUD_Suites": "*.xml", "E2E_Suites": "*.xml",
        "API_Suites/Positive_All": "*.xml", "API_Suites/Negative": "*.xml",
        "API_Suites/Positive": "*.xml", "Temp": "*.xml",
    }
    counts = {d: _count_glob(REPO / d, g) for d, g in dirs.items()}
    total = len(list((REPO).glob("**/*_Suites/**/*.xml"))) if REPO.exists() else 0
    counts["_total_suite_xml"] = total
    return Measurement("suite_counts", value=counts, unit="XML files per suite dir",
                       derivation="glob *.xml under each suite directory of the automation repo",
                       detail=counts)


@probe("workspace_inventory")
def workspace_inventory() -> Measurement:
    inv = {
        "harness_scripts_py": _count_glob(ROOT / "tools", "*.py"),
        "issue_files": _count_glob(ROOT / "docs" / "findings" / "issues", "ISSUE-*.md"),
        # OBJ-025: no ".exists() else 0" fallback. A silent 0 here reads as "the packs
        # were deleted" rather than "I looked in the wrong place".
        "lh_packs": len([p for p in (ROOT / "artifacts" / "loopholes").glob("LH-*")
                         if p.is_dir()]),
        "document_reports": _count_glob(ROOT / "docs" / "analysis", "A*.md"),
        "skill_specs": _count_glob(ROOT / "docs" / "specs", "*.SKILL.md"),
        "env_property_files": _count_glob(REPO / "Environments", "*.properties"),
        "run_folders": len([p for p in (ROOT / "artifacts" / "runs").iterdir() if p.is_dir()])
                       if (ROOT / "artifacts" / "runs").exists() else 0,
        "objective_history_parts": _count_glob(ROOT / "docs" / "history", "0*.md"),
        # OBJ-025: pattern narrowed from *.md to 0*.md. The index moved INTO this
        # directory as README.md, so *.md would now measure 6 and read as a real
        # change in the number of history parts. 0*.md counts the numbered parts.
        "java_sources": len(list(SRC.rglob("*.java"))) if SRC.exists() else 0,
    }
    return Measurement("workspace_inventory", value=inv, unit="file counts",
                       derivation="glob counts over the named directories",
                       detail=inv)


@probe("declared_paths_exist")
def declared_paths_exist() -> Measurement:
    """Paths the guidance documents instruct a reader to open. A dead pointer is a
    finding: the doc sends you somewhere that is not there."""
    targets = {
        # OBJ-027: three of these were measured wrong, not dead. GRAPH_TREE.html and
        # the callflow DO exist - in the WORKSPACE graph, not the bootstrap repo's
        # graphify-out - and the callflow's real name is graphify-pam-callflow.html,
        # not pam_automation_bootstrap-callflow.html. The probe was checking the wrong
        # tree under the wrong name, so it reported two live files as dead pointers.
        "artifacts/graph/.../GRAPH_TREE.html": GRAPHIFY_OUT / "GRAPH_TREE.html",
        "artifacts/graph/.../graphify-pam-callflow.html": GRAPHIFY_OUT / "graphify-pam-callflow.html",
        "artifacts/graph/.../graph.html": GRAPHIFY_OUT / "graph.html",
        # graphify-out/wiki/ is a graphify feature this workspace has never generated,
        # and QABuddy_AI_Test_Automation.pptx (the deck's style reference) was never
        # committed - it lives outside the repository. Both are absent BY DESIGN, so
        # counting them as dead pointers buried the two that genuinely misled a reader.
        "graphify-out/wiki/": GRAPHIFY_OUT / "wiki",
        "artifacts/deck/Prepare-1.pptx": ROOT / "artifacts" / "deck" / "Prepare-1.pptx",
        "artifacts/spec-cache": ROOT / "artifacts" / "spec-cache",
        "docs/findings/issues/Evidence": ROOT / "docs" / "findings" / "issues" / "Evidence",
        "repo .mcp.json": REPO / ".mcp.json",
        "workspace .mcp.json": ROOT / ".mcp.json",
    }
    # Absent-by-design paths are not defects: SpecCache is created on demand, the
    # workspace has no .mcp.json (the graphify server is repo-scoped), and
    # docs/findings/issues/Evidence is an empty stub whose content was archived. Counting
    # them as dead pointers buries the three that genuinely mislead a reader.
    BY_DESIGN = {"artifacts/spec-cache", "workspace .mcp.json",
                 "docs/findings/issues/Evidence", "graphify-out/wiki/"}
    res = {}
    for label, p in targets.items():
        exists = p.exists()
        empty = exists and p.is_dir() and not any(p.iterdir())
        res[label] = {"exists": exists, "empty_dir": empty,
                      "absent_by_design": label in BY_DESIGN}
    dead = [k for k, v in res.items()
            if (not v["exists"] or v["empty_dir"]) and not v["absent_by_design"]]
    informational = [k for k, v in res.items()
                     if (not v["exists"] or v["empty_dir"]) and v["absent_by_design"]]
    return Measurement("declared_paths_exist", value=len(dead), unit="dead pointers",
                       derivation="Path.exists() for each path the guidance tells a reader to open, "
                                  "excluding paths that are absent by design",
                       detail={"results": res, "dead": dead, "absent_by_design": informational})


@probe("large_files")
def large_files() -> Measurement:
    """The read-truncation trap: a plain Read returns the first 2,000 lines silently.
    Any file over that must be paged, and the guidance table must name the right ones."""
    cands = [
        ROOT / "artifacts" / "rag-corpus" / "pam-api.md",
        ROOT / "artifacts" / "rag-corpus" / "pam-admin.md",
        ROOT / "artifacts" / "rag-corpus" / "client-manager.md",
        ROOT / "artifacts" / "graph" / "pam-scope" / "graphify-out" / "GRAPH_REPORT.md",
        REPO / "graphify-out" / "GRAPH_REPORT.md",
        ROOT / "CLAUDE.md",
    ]
    runs = ROOT / "artifacts" / "runs"
    if runs.exists():
        cands += sorted(runs.glob("*/RUN_REPORT.md"))
    out = {}
    for p in cands:
        if not p.exists():
            continue
        ls = _lines(p)
        sec5 = next((i for i, ln in enumerate(ls, 1) if ln.startswith("## 5.")), None)
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        out[rel] = {"lines": len(ls), "truncates_on_plain_read": len(ls) > 2000,
                    "section_5_at": sec5}
    return Measurement("large_files", value=len(out), unit="files measured",
                       derivation="line count per file, plus the line of '## 5.' where present",
                       detail=out)


@probe("newest_run")
def newest_run() -> Measurement:
    runs = ROOT / "artifacts" / "runs"
    if not runs.exists():
        return Measurement("newest_run", error="artifacts/runs does not exist")
    folders = sorted([p.name for p in runs.iterdir() if p.is_dir()])
    if not folders:
        return Measurement("newest_run", error="artifacts/runs holds no run folders")
    newest = folders[-1]
    rpt = runs / newest / "RUN_REPORT.md"
    ln = len(_lines(rpt)) if rpt.exists() else None
    return Measurement("newest_run", value=newest, unit="run folder id",
                       derivation="lexicographic max of artifacts/runs/* (timestamps sort correctly)",
                       detail={"all_runs": folders, "count": len(folders),
                               "report_lines": ln, "has_report": rpt.exists()})


@probe("pptx_slides")
def pptx_slides() -> Measurement:
    deck = ROOT / "artifacts" / "deck" / "Prepare-1.pptx"
    if not deck.exists():
        return Measurement("pptx_slides", error=f"{deck} does not exist")
    try:
        from pptx import Presentation  # noqa: PLC0415
        n = len(Presentation(str(deck)).slides)
    except Exception as e:  # dependency missing or file unreadable
        return Measurement("pptx_slides", error=f"{type(e).__name__}: {e}")
    return Measurement("pptx_slides", value=n, unit="slides",
                       derivation="len(Presentation('artifacts/deck/Prepare-1.pptx').slides) via python-pptx",
                       detail={"deck": "Prepare-1.pptx"})


# ---------------------------------------------------------------- safety invariants

@probe("harness_safety_gates")
def harness_safety_gates() -> Measurement:
    """Root CLAUDE.md and .claude/rules/api-surface.md both assert every harness
    script is deny-by-default and a bare run issues zero HTTP calls. Verify it."""
    scripts = ROOT / "tools"
    res = {}
    for name in ("chain_runner.py", "run_qa_mssql.py", "run_validation.py", "run_chains.py"):
        p = scripts / name
        if not p.exists():
            res[name] = {"error": "missing"}
            continue
        txt = _text(p)
        res[name] = {
            "has_execute_flag": bool(re.search(r'add_argument\(\s*["\']--execute', txt)),
            "has_revalidate_flag": bool(re.search(r'add_argument\(\s*["\']--revalidate', txt)),
            "has_dry_run_flag": bool(re.search(r'add_argument\(\s*["\']--dry-run', txt)),
            "urlopen_sites": len(re.findall(r"urlopen\(", txt)),
        }
        gated = res[name]["has_execute_flag"] or res[name]["has_revalidate_flag"]
        res[name]["deny_by_default"] = gated
    violators = [n for n, v in res.items()
                 if "error" not in v and not v["deny_by_default"] and v["urlopen_sites"] > 0]
    return Measurement("harness_safety_gates", value=len(violators), unit="scripts violating deny-by-default",
                       derivation="argparse flag census per script; a script with urlopen but no "
                                  "--execute/--revalidate gate executes live on a bare run",
                       detail={"scripts": res, "violators": violators})


_BLOCK_KEYS = ("GetLogs", "GetErrorLogs", "GetAllActiveUserDetails")


@probe("blocklist_consistency")
def blocklist_consistency() -> Measurement:
    """The app-pool blocklist is defined independently in several scripts. Any copy
    missing an entry is a live hazard — three sequential calls took the API to 503."""
    scripts = ROOT / "tools"
    defs = {}
    for p in sorted(scripts.glob("*.py")):
        txt = _text(p)
        m = re.search(r"^\s*(ENDPOINT_)?BLOCKLIST\s*=\s*\{", txt, re.M)
        if m is None:
            continue
        body = txt[m.start():][:1200]
        defs[p.name] = {k: (k in body) for k in _BLOCK_KEYS}
    incomplete = {n: [k for k, v in d.items() if not v] for n, d in defs.items()
                  if not all(d.values())}
    return Measurement("blocklist_consistency", value=len(defs), unit="independent blocklist definitions",
                       derivation="locate each `BLOCKLIST = {` / `ENDPOINT_BLOCKLIST = {` literal and "
                                  "test membership of the three app-pool endpoints",
                       detail={"definitions": defs, "incomplete": incomplete,
                               "single_source_of_truth": len(defs) <= 1})


@probe("objective_injection")
def objective_injection() -> Measurement:
    """BLAST/Objective.md must reach context exactly once. It is currently both
    imported by CLAUDE.md (session-start snapshot, goes stale) and injected live by
    a UserPromptSubmit hook — two copies that disagree mid-session."""
    claude = ROOT / "CLAUDE.md"
    settings = ROOT / ".claude" / "settings.json"
    imported = bool(re.search(r"^@BLAST/Objective\.md\s*$", _text(claude), re.M)) if claude.exists() else False
    hooked = False
    if settings.exists():
        try:
            cfg = json.loads(_text(settings))
            hooked = "Objective.md" in json.dumps(cfg.get("hooks", {}))
        except Exception:
            hooked = "Objective.md" in _text(settings)
    return Measurement("objective_injection",
                       value=int(imported) + int(hooked), unit="injection paths",
                       derivation="@BLAST/Objective.md import line in CLAUDE.md, plus any hook in "
                                  ".claude/settings.json referencing Objective.md",
                       detail={"claude_md_import": imported, "settings_hook": hooked,
                               "double_injected": imported and hooked})


@probe("permission_guardrails")
def permission_guardrails() -> Measurement:
    """The never-push rule is prose only if the harness permits git push."""
    out = {}
    for label, p in (("settings", ROOT / ".claude" / "settings.json"),
                     ("settings.local", ROOT / ".claude" / "settings.local.json")):
        if not p.exists():
            out[label] = {"exists": False}
            continue
        try:
            cfg = json.loads(_text(p))
        except Exception as e:
            out[label] = {"exists": True, "parse_error": str(e)}
            continue
        perms = cfg.get("permissions", {}) or {}
        allow = perms.get("allow", []) or []
        deny = perms.get("deny", []) or []
        out[label] = {
            "exists": True, "allow": allow, "deny": deny,
            "wildcard_git_allow": [a for a in allow if re.search(r"git\s*\*", a)],
            "has_push_deny": any("push" in d for d in deny),
        }
    # Permissions merge ACROSS the two files — a deny in settings.json covers an allow
    # in settings.local.json. Evaluating each file in isolation reports a phantom
    # violation, so the union is what matters.
    any_wildcard = any(v.get("wildcard_git_allow") for v in out.values() if v.get("exists"))
    any_push_deny = any(v.get("has_push_deny") for v in out.values() if v.get("exists"))
    risky = any_wildcard and not any_push_deny
    return Measurement("permission_guardrails", value=risky, unit="push reachable via wildcard allow",
                       derivation="union of permissions.allow / permissions.deny across "
                                  "settings.json and settings.local.json (they merge)",
                       detail=out | {"_union": {"wildcard_git_allow_present": any_wildcard,
                                                "push_deny_present": any_push_deny,
                                                "push_reachable": risky}})


# ---------------------------------------------------------------- git provenance (local only)

@probe("repo_state")
def repo_state() -> Measurement:
    """Local-only. The throttled fetch lives in obj013_gitcheck.py, never here."""
    out = {}
    for label, repo in (("automation", REPO), ("pam", PAM)):
        if not (repo / ".git").exists():
            out[label] = {"error": "not a git checkout"}
            continue
        try:
            branch = _git(repo, "rev-parse", "--abbrev-ref", "HEAD")
            head = _git(repo, "rev-parse", "--short", "HEAD")
            dirty = len([ln for ln in _git(repo, "status", "--porcelain").splitlines() if ln.strip()])
            stashes = len([ln for ln in _git(repo, "stash", "list").splitlines() if ln.strip()])
            info = {"branch": branch, "head": head, "dirty_files": dirty, "stashes": stashes}
            try:
                upstream = _git(repo, "rev-parse", "--abbrev-ref", f"{branch}@{{upstream}}")
                ab = _git(repo, "rev-list", "--left-right", "--count", f"{branch}...{upstream}")
                ahead, behind = (int(x) for x in ab.split())
                info |= {"upstream": upstream, "ahead": ahead, "behind": behind}
            except Exception:
                info["upstream"] = None
            out[label] = info
        except Exception as e:
            out[label] = {"error": str(e)}
    return Measurement("repo_state", value=out, unit="git state per checkout",
                       derivation="git rev-parse / status --porcelain / stash list / rev-list "
                                  "(local refs only — no network)",
                       detail=out)


# ---------------------------------------------------------------- runner

def run(names: list[str] | None = None) -> dict[str, Measurement]:
    chosen = names or list(_REGISTRY)
    results: dict[str, Measurement] = {}
    for n in chosen:
        fn = _REGISTRY.get(n)
        if fn is None:
            results[n] = Measurement(n, error=f"no such probe; known: {', '.join(sorted(_REGISTRY))}")
            continue
        try:
            results[n] = fn()
        except Exception as e:  # a probe must never take the loop down
            results[n] = Measurement(n, error=f"{type(e).__name__}: {e}")
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description="Re-derive workspace facts from source. Read-only, offline.")
    ap.add_argument("probes", nargs="*", help="probe names; default all")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--list", action="store_true", help="list probe names and exit")
    a = ap.parse_args()

    if a.list:
        for n in sorted(_REGISTRY):
            print(n)
        return 0

    res = run(a.probes or None)
    if a.json:
        print(json.dumps({k: asdict(v) for k, v in res.items()}, indent=1, ensure_ascii=False))
        return 0

    failed = 0
    for n, m in res.items():
        if not m.ok:
            failed += 1
            print(f"[ERROR] {n}: {m.error}")
            continue
        v = m.value if not isinstance(m.value, (dict, list)) else json.dumps(m.value, ensure_ascii=False)
        print(f"[ok]    {n} = {v}  ({m.unit})")
    print(f"\n{len(res) - failed}/{len(res)} probes measured, {failed} error(s).")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
