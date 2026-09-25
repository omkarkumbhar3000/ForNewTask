# `tools/jira/` — the operator's guide

Everything that talks to Jira, or builds a document out of what Jira returned. This is the
only part of `tools/` that fully works in this copy of the workspace.

> **New here? Run this first.** It answers, in one screen, every environmental question that
> otherwise arrives as a traceback:
>
> ```powershell
> python tools\jira\doctor.py
> ```

---

## 1. The two rules that matter most

**⛔ Jira access is read-only, and it is enforced, not promised.** `jira_query.py::_check()`
allows `GET` to a fixed prefix list and `POST` to exactly two *search* endpoints. Anything else
raises `ReadOnlyViolation`. Nothing in this folder transitions, comments on, assigns, edits or
creates an issue. (`create_lh01.py` and `create_b01.py` are the exception and belong to the full
deployment — see §6.)

**⛔ Generated documents are never hand-edited.** The markdown is the source of truth; the
`.docx` and `.xlsx` beside it are *rendered*. A hand edit to a rendered file is silently
discarded by the next run. Fix the generator, re-run, re-render.

---

## 2. Run it

### The whole thing, one command

```powershell
python tools\jira\run_census.py            # offline, zero HTTP; ends by validating
python tools\jira\run_census.py --live     # re-fetch from Jira first (overwrites the snapshots)
python tools\jira\run_census.py --dry-run  # print the six steps without running them
```

Six steps in dependency order, stopping at the first failure, **ending with
`validate_analysis.py` and inheriting its exit code**. A green run is a claim that the published
documents and the source data agree — and there is no way to get one without that being true.
Takes about a minute offline.

Use this unless you have a reason not to. The step-by-step form below is the same pipeline, and
its hazard is that regenerating a report silently leaves the `.docx`, the `.xlsx` and the client
pack describing the *previous* edition: nothing looks wrong, the files open and carry plausible
numbers, they just describe a report that no longer exists. That is the state this workspace was
found in on 2026-09-22.

### Step by step, if you need to run one part

The same six steps, run individually. This is the `OBJ-030` line: two point-in-time censuses of
Jira, rendered to Word and Excel, and assembled into a dated client pack. Run from **PowerShell**;
under Bash set `PYTHONUTF8=1` first, or the non-ASCII console output kills a console-less Python
child.

```powershell
# 0. Is this machine ready?                                    exit 0 = yes
python tools\jira\doctor.py

# 1. Build the two census reports.  --offline reuses the snapshot and issues ZERO HTTP.
python tools\jira\jira_analysis_2026.py --offline    # PAMIT -> docs\analysis\Jira_Analysis_*.md
python tools\jira\ci_analysis_2026.py   --offline    # CI    -> docs\analysis\CI_Jira_Analysis_*.md

# 2. Render each to .docx + .xlsx, beside the markdown.
python tools\jira\convert_analysis.py                          # PAMIT (adds the All Data sheet)
python tools\jira\md_to_docx_xlsx.py docs\analysis\CI_Jira_Analysis_01Jan26-21Sep26.md

# 3. Assemble the dated client pack -> 21-09-2026\PAM\ and 21-09-2026\CI\
python tools\jira\build_delivery_pack.py

# 4. Prove it.                                                 exit 0 = every figure checks out
python tools\jira\validate_analysis.py
python tools\jira\validate_analysis.py --project CI            # one project
python tools\jira\validate_analysis.py --json                  # for a scheduled check
python tools\jira\validate_analysis.py --self-test             # prove the checks can fail
```

**Always finish with step 4.** Steps 1–3 can each succeed while producing a document that
disagrees with the data underneath it; step 4 is the only one that tests that. `run_census.py`
exists so that finishing is not optional.

### `--offline` is the default you want, and it is not universal

| Script | `--offline`? | Notes |
|---|---|---|
| `jira_analysis_2026.py` · `ci_analysis_2026.py` · `pamit_client_analysis.py` | ✅ | Byte-identical output, zero HTTP. **Refuses with exit 2** if the snapshot is absent — it will not quietly fetch instead |
| `pamit_workbook.py` · `convert_analysis.py` · `md_to_docx_xlsx.py` · `build_delivery_pack.py` · `validate_analysis.py` · `doctor.py` | n/a | No network at all, ever |
| `track_tickets.py` | ⛔ **no** | Has only `--json` and `--no-state`. **Always queries Jira live** — by design, a daily review of a stale board is worse than none |

---

## 3. What writes what

| Script | Writes | Reads |
|---|---|---|
| `jira_analysis_2026.py` | `docs/analysis/Jira_Analysis_<slug>.md` | `artifacts/client-tickets/snapshots/jira-analysis-<range>.json` |
| `ci_analysis_2026.py` | `docs/analysis/CI_Jira_Analysis_<slug>.md` | `artifacts/snapshots/ci-analysis-<range>.json` |
| `convert_analysis.py` | `.docx` + `.xlsx` beside the PAMIT markdown | that markdown |
| `md_to_docx_xlsx.py` | `.docx` + `.xlsx` beside any analysis markdown | the markdown you name (**required argument**) |
| `build_delivery_pack.py` | `21-09-2026/{PAM,CI}/*.{md,docx,xlsx}` | the two canonical markdowns |
| `pamit_client_analysis.py` | `docs/analysis/D1-client-ticket-patterns.md` **and** the workbook, in one process | `artifacts/client-tickets/snapshots/` |
| `pamit_workbook.py` | `artifacts/workbooks/PAM-Client-Ticket-Analysis.xlsx` | the newest capture |
| `validate_analysis.py` | nothing — it only reads and reports | snapshots + published markdown + renders |
| `doctor.py` | nothing | the environment |
| `run_census.py` | nothing of its own — it shells out to the six above, in order | — |
| `track_tickets.py` | nothing durable | live Jira; state in `.tracking-state.json` |

⚠️ `RANGE_SLUG` is **derived** from the date constants, never hardcoded. The 03 Sep edition was
renamed by hand after generation, so re-running wrote a *different* file and left the intended
deliverable stale. Moving the window means editing `DATE_FROM` / `DATE_TO` and nothing else —
then update `DATE_FROM` / `DATE_TO` in `validate_analysis.py` too, which check `E2` will tell you
about rather than silently validating the wrong window.

---

## 4. Modules, not entry points

Import these; do not run them. A change to a shared definition belongs here, never in one report.

| Module | Owns |
|---|---|
| `analysis_classify.py` | Open/Closed and Client/Internal for **both** censuses, so the two cannot drift. Carries the union of the internal-client markers — PAMIT uses `Internal (ARCON)` and variants, CI uses `Internal Arcon`, and applying PAMIT's set to CI once misclassified 3,713 internal tickets as client |
| `analysis_render.py` | markdown → `.docx`/`.xlsx`. Lifts grouped headers into merged cells and coerces `1,234` / `12.3%` to typed cells. ⛔ **Never recalculates** — every figure is the one parsed out of a markdown cell |
| `pamit_fmt.py` | `pct`, `tally`, `table`, `row`, and `snapshot_provenance` (the `Source snapshot:` header line) |
| `jira_query.py` | The read-only enforcement layer, paging, and `field_value` field-shape normalisation |
| `jira_client.py` | Transport and `load_env`. The only place credentials are read |
| `pamit_analysis_rules.py` | Classification and grouping for the `D1` client-ticket analysis |
| `pamit_report.py` | Rendering for `D1` |

⛔ **`jira_query.py`, `track_tickets.py`, `pamit_*.py` and `create_b01.py` are maintained in
`E:\Omkar\AI Projects\Dev Project`, not here** — this copy is 5–12 days behind on those seven
files and has no git history to catch an edit. Check which side owns a file before changing it.
The census line (`jira_analysis_2026.py`, `ci_analysis_2026.py`, `analysis_classify.py`,
`analysis_render.py`, `convert_analysis.py`, `md_to_docx_xlsx.py`, `build_delivery_pack.py`) plus
`validate_analysis.py`, `doctor.py` and `run_census.py` are owned **here** and safe to edit.

⚠️ **`pamit_fmt.py` is the one file in neither camp.** It was byte-identical on both sides until
`snapshot_provenance()` was added here on 2026-09-22 — an additive change, so porting it upstream is
a clean append, but this copy is now ahead on a file the divergence table lists nowhere.

---

## 5. Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `UnicodeEncodeError: 'charmap' codec can't encode character` | A console-less Python child on the Windows ANSI codepage. Run from PowerShell, or `set PYTHONUTF8=1` first. `doctor.py` and `validate_analysis.py` reconfigure their own streams and are verified to run clean under `PYTHONIOENCODING=cp1252` |
| `--offline requested, but there is no snapshot at: …` (exit 2) | Deliberate. Run the same script **once without `--offline`** to capture it. It will not silently fetch instead — that would hit production Jira and overwrite the snapshot you meant to reuse |
| `ImportError: No module named docx` | `python -m pip install -r tools/requirements.txt`. `python-docx` was missing from that file until 2026-09-22, so a machine provisioned from an older copy fails on every `.docx` render |
| `missing tools/jira/.env` | Copy `.env.sample` and fill in the four `JIRA_*` keys. Only needed for a live fetch; everything offline works without it |
| `Jira auth failed: HTTP 401` | The token in `.env` expired. Re-issue at id.atlassian.com → Security → API tokens |
| `SystemExit` from `paths.py` | It finds the root by searching upward for a directory holding **both** `CLAUDE.md` and `.claude/`. It refuses rather than guessing, because every historical failure here was a script that carried on with a wrong root. Never count parent directories — import `workspace_root()` |
| `validate_analysis.py` says a `.docx` is OLDER than the markdown | You regenerated a report and did not re-render. Re-run step 2, then step 3 |
| `validate_analysis.py` says the pack DIFFERS from the canonical report | The client pack is shipping a different analysis. Re-run `build_delivery_pack.py` |
| A figure looks wrong | Fix the **generator** and re-run it. Never hand-edit the markdown to make a check pass — the next run discards it and the check passes on a lie |

---

## 6. Present here, but not for this copy

| File | Why |
|---|---|
| `create_lh01.py` · `create_b01.py` | Ticket *creation*. Belongs to the full deployment; nothing in this copy raises a ticket. `jira.md` documents the field map and the ADF requirement |
| `register_client_analysis_task.ps1` | Registers a Windows scheduled task for the daily client analysis |
| `.tracking-state.json` · `tracked-tickets.json` | State and registry for `track_tickets.py`; see `TRACKING.md` |

---

## 7. Further reading

| For | Read |
|---|---|
| The field rulings (`D42`, `D43`, `D44`, `D46`) and why each was paid for | `../../CLAUDE.md` |
| Ticket creation: ADF, the field map, `createmeta` under-reporting 6 required fields | `jira.md` |
| The daily review format and its registry | `TRACKING.md` |
| What the 2026-09-22 hardening review changed, and why | `../../docs/hardening/README.md` |
| Report index and how to read a figure | `../../docs/analysis/README.md` |
