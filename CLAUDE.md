# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## ⚠️ What this folder is — read before anything else

This is a **partial, de-identified copy** of the `dynamic-api-validator` workspace, pared down to the
**Jira ticket-analysis work**. It is not the full deployment, and the difference is load-bearing:

| | Here |
|---|---|
| Git | ✅ **Its own repository since 2026-09-25**: branch `main`, remote `github.com/omkarkumbhar3000/ForNewTask`, root commit `8d8b841`. A committed file can be restored with `git restore <path>`; an uncommitted edit or an ignored file cannot. ⚠️ `.gitignore` excludes `artifacts/workbooks/PAM-Client-Ticket-Analysis.xlsx` because it embeds a customer login pasted into a ticket, so that workbook is local-only and a clone must rebuild it. The vendor PDFs and `graph.json` are Git LFS objects (`.gitattributes`); a clone made without `git lfs` gets pointer files |
| Nested checkouts | ⛔ `Automation gitlab repo/` and `pam/` are **absent**. No Java, no Maven, no TestNG, no product source |
| Live API | ⛔ No `artifacts/runs/`. Nothing here executes against the PAM API, and `/arcontoken` is never called |
| What runs | ✅ **The Python tooling only** — Jira analysis, the RAG corpus query, the workbook/report builders |

**The full-workspace guidance is preserved verbatim as `CLAUDE.full-workspace.md`** (854 lines). Consult
it for *why* a rule exists — it is the append-only reasoning behind the three-repo rights model, the
response envelope, the endpoint blocklist and the token guard. ⛔ **Do not follow its commands here**;
most of them address paths this copy does not contain. The maintained deployment is
`E:\Omkar\AI Projects\Dev Project`, whose copy on the D: machine is `..\dynamic-api-validator\` (see §Divergence).

`AGENTS.md` beside this file carries the same scope note and is the OpenCode-facing equivalent. The root
`README.md` is the **full-workspace** guide: it opens by calling this folder the `dynamic-api-validator`
repository and documents Maven/TestNG, and neither applies here. For this copy, read `tools/jira/README.md`.

### Do not act on these — they cannot succeed here

`python tools\obj013_loop.py check` exits **255** with 15 `[ERR] high` probes, every one pointing at an
absent `Automation gitlab repo/…` path or `artifacts/runs`. The same applies to `engage.py`,
`chain_runner.py`, `obj016_daily_refresh.py`, `obj017_weekly_execution.py`, `obj020_execution_supervisor.py`,
`token_guard.py` and `control_center.py`. They are present, they import, and they have nothing to work on.
**Their presence is not evidence they apply.**

⛔ **Both hooks in `.claude/settings.json` are dead.** They hard-code
`E:\Omkar\Automation\Dev Project\…`, which does not exist: the sibling moved to
`E:\Omkar\AI Projects\Dev Project`, and the D: machine has no `E:` drive at all. Two consequences:

- **`BLAST/Objective.md` is NOT auto-injected.** `CLAUDE.full-workspace.md` opens by asserting it is, and
  forbids re-adding the `@import` on that basis. That reasoning inverts once the hook is dead — **read
  `BLAST/Objective.md` explicitly at the start of a session.** It currently holds `OBJ-030`, marked
  complete and retained as the active record.
- The `SessionStart` drift headline never fires, and it points at a pre-`OBJ-025` path
  (`workbench\scripts\obj013_loop.py`) that no longer exists in any copy.

The same `settings.json` also carries a live `permissions.deny` for `git merge` and `git remote set-url`
(both shells). That half **does** work. Now that this folder is a repository the deny has teeth: in a
session started here, `git merge` is refused even when the owner has authorised merging, until the owner
edits the list. The assistant cannot edit `.claude/settings.json`; that fix is the owner's.

## The work this copy exists for — Jira analysis

Two Jira projects, both on `https://arcon-tech-solution.atlassian.net`: **`PAMIT`** (PAM product) and
**`CI`** (Converged Identity). Credentials live in `tools/jira/.env` (gitignored; copy `.env.sample`).

**Setup, once per machine.** The Jira line needs only `openpyxl` and `python-docx`. `doctor.py`,
`validate_analysis.py` and `run_census.py --dry-run` use the stdlib alone. Install into a venv, because a
distribution-managed Python refuses a global `pip install`:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r tools\requirements.txt
```

On the D: machine, `python` and `py` do not work. The one interpreter there is `python3.11` (uv-managed
3.11.9, with no packages), and `..\CLAUDE.md` records the rest of that machine's quirks.

```powershell
# The whole census line in one command: generate -> render -> pack -> validate, inheriting the
# validator's exit code (0 = every step ran and every figure validated). Prefer this to the steps below.
python tools\jira\run_census.py                          # offline, zero HTTP
python tools\jira\run_census.py --project CI             # one project; the pack is still rebuilt from both
python tools\jira\run_census.py --dry-run                # print the six steps, run nothing
python tools\jira\run_census.py --live                   # re-fetch first: production Jira, overwrites snapshots

# Daily PAMIT client-ticket analysis -> report + the master workbook
python tools\jira\pamit_client_analysis.py              # fetch, analyse, write
python tools\jira\pamit_client_analysis.py --offline     # reuse last capture, zero HTTP
python tools\jira\pamit_workbook.py                      # rebuild the workbook from that capture

# The 2026 census reports (01 Jan - 21 Sep 2026, OBJ-030), step by step; run_census.py runs these
python tools\jira\jira_analysis_2026.py --offline        # PAMIT, 5,740 tickets
python tools\jira\ci_analysis_2026.py --offline          # CI,    5,994 tickets

# Markdown -> Word + Excel. Both are thin entry points over analysis_render.render().
python tools\jira\convert_analysis.py                    # PAMIT; path derived, takes no argument
python tools\jira\md_to_docx_xlsx.py <report.md>         # CI + general; REQUIRES the path

# The dated client delivery pack -> 21-09-2026/PAM/ and 21-09-2026/CI/
python tools\jira\build_delivery_pack.py

# The daily "what needs us" review
python tools\jira\track_tickets.py                       # exit 0 = clear, 1 = action items, 2 = lookup failed

# Preflight and proof — run the first on a new machine, the second before circulating anything
python tools\jira\doctor.py                              # env, packages, credentials, snapshots; 0 = ready
python tools\jira\validate_analysis.py                   # 57 checks vs the snapshots; 0 = every figure agrees
python tools\jira\validate_analysis.py --project CI      # one project: PAMIT | CI
python tools\jira\validate_analysis.py --self-test       # proves each markdown check fires on its defect
```

There is no pytest suite. `validate_analysis.py` is the test: `--project` narrows it to one project, and
`--self-test` tests the checks themselves without touching project data. The three React apps have only
`dev`, `build` and `preview` scripts, with no lint or test script.

`tools/jira/README.md` is the operator's guide for this folder — the pipeline in order, what writes
what, and a troubleshooting table keyed by the exact error text.

⚠️ **Run from PowerShell, or set `PYTHONUTF8=1` under Bash** — these scripts print `⛔`/`⚠` and a
console-less Python child dies on the ANSI codepage.

⚠️ **`--offline` is not universal.** `pamit_client_analysis.py`, `jira_analysis_2026.py` and
`ci_analysis_2026.py` take it — prefer it, the output is byte-identical and issues no requests.
`pamit_workbook.py` and the two renderers need no network at all. **`track_tickets.py` has only `--json`
and `--no-state`, and always queries Jira live.**

✅ **`tools/requirements.txt` was corrected 2026-09-22.** It had omitted `python-docx`, which
`analysis_render.py` imports (`from docx import Document`), so a machine provisioned purely from that file
failed on every `.docx` render — the two census reports and the whole client pack — with an ImportError
naming a package the file said was not needed. It also credited `jsonschema` to
`tools/onboarding/validate_profile.py`, which is deliberately dependency-free; the one real import is in
`tools/run_validation.py`. Import counts and the Python version (3.14.7, not 3.14.6) are now re-censused.
`python tools\jira\doctor.py` checks the file against what is actually importable.

### Which script owns which output

| Script | Writes | Snapshot drawer |
|---|---|---|
| `pamit_client_analysis.py` | `docs/analysis/D1-client-ticket-patterns.md` **and the workbook** (built in-process — `D45`, deliberately not a second job, so the two cannot describe different days) | `artifacts/client-tickets/snapshots/` (dated, **never deleted** — sheet `12 Daily History` is derived from them) |
| `pamit_workbook.py` | `artifacts/workbooks/PAM-Client-Ticket-Analysis.xlsx` | reads the newest capture |
| `jira_analysis_2026.py` | `docs/analysis/Jira_Analysis_01Jan26-21Sep26.md` | `artifacts/client-tickets/snapshots/jira-analysis-*.json` |
| `ci_analysis_2026.py` | `docs/analysis/CI_Jira_Analysis_01Jan26-21Sep26.md` | `artifacts/snapshots/ci-analysis-*.json` |
| `build_delivery_pack.py` | `21-09-2026/{PAM,CI}/*.{md,docx,xlsx}` | — |
| `track_tickets.py` | nothing durable | `tools/jira/.tracking-state.json` (registry: `tracked-tickets.json`) |

The `.docx`/`.xlsx` beside each report are **rendered, not authored** — edit the markdown and re-render.

### The 2026 census line — three shared modules sit under the two reports

`jira_analysis_2026.py` (PAMIT) and `ci_analysis_2026.py` (CI) are **not** standalone. A change to a
shared definition belongs in the module, never in one report:

- **`analysis_classify.py`** — the Open/Closed and Client/Internal classification both reports import, so
  the two cannot drift on the definitions driving every bifurcated table.
- **`analysis_render.py`** — the markdown → `.docx`/`.xlsx` renderer both entry points call. It lifts
  grouped headers into merged cells and coerces `1,234`/`12.3%` to typed cells (without which every figure
  lands as left-aligned text that the reader cannot sum). ⛔ **It never recalculates** — every figure is
  the one parsed out of a markdown cell. `convert_analysis.py` differs from `md_to_docx_xlsx.py` only by
  the PAMIT-only consolidated `All Data` sheet.
- **`build_delivery_pack.py`** — copies the canonical markdown into the dated pack, then renders Word and
  Excel **from the copy that ships beside them**, so the three files in each folder are provably one
  analysis. The folder name derives from `DATE_TO`, so it regenerates rather than being maintained.

⛔ **The internal-client marker differs per project and only one value is live in each.** PAMIT uses
`Internal (ARCON)` / `Internal` / `Internal(ARCON)`; CI uses **`Internal Arcon`**, which matches none of
PAMIT's variants. Applying PAMIT's set to CI classified **3,713** internal tickets as *Client* — the
`D42` error class exactly. `analysis_classify` carries the union, and reproduces both published splits.

⛔ **An unmapped status is never guessed into a bucket.** `classify_status()` returns `UNMAPPED` and the
caller carries it as its own column (137 PAMIT / 262 CI). "Identify unmapped separately" and "counts
reconcile" are only simultaneously satisfiable if Unmapped is visible, so the identity is:

    Total Count  = Open Total + Closed Total + Unmapped
    Open Total   = Open Client + Open Internal
    Closed Total = Closed Client + Closed Internal

### ✅ Three defects, all fixed 2026-09-22 — and the reason they survived

All three pre-date `OBJ-030` (which was scoped "update the analysis, do not change the methodology"), so
they were generator defects, not extension-task defects. Each was fixed **in the generator and re-run** —
never by hand-editing the markdown. The reports, the `.docx`/`.xlsx` renders and the `21-09-2026/` pack
were all regenerated from the fixes and now agree.

| Defect | Detail | Fix |
|---|---|---|
| **PAMIT §12 Affected Milestone read 100% `Not set`** | `jira_analysis_2026.py` listed `customfield_10092` in `FIELDS` and §12 read `t.get("affected_milestone")`, but **`normalise()` never emitted that key** — the fetched field was silently discarded and all 5,740 tickets collapsed to `Not set`. The field is **78.8% populated (4,523/5,740)**. A `D42` violation in the shipped deliverable: the mandated build axis published as absent, leaving `Fix versions` (27.1%, which `D42` rejects) as the only populated version table. **PAMIT only** — CI never requests the field | `normalise()` now emits it; §12 publishes 101 distinct milestones |
| **CI "Sub-tasks 4241 (70.8%)" was not a sub-task count** | `ci_analysis_2026.py` counted `parent_key` presence, and in modern Jira `parent` spans the whole hierarchy. Real count **1,443** (`issuetype.subtask` and `issuetype.name` agree exactly); the published figure swept in **2,798 Epic children** — 2,123 Bugs, 373 Stories, 266 Tasks. The same report published 1,443 in §3, so §1/§15 contradicted §3 by 2,798 | counts `issuetype.subtask`; §1/§15/§15A now agree with §3 |
| **PAMIT §12 called 5,832 figures "milestone assignments"** | Only **4,615** exist. The counter folded each of the 1,217 unpopulated tickets in as a `Not set` assignment, putting a `Not set` row at the top of a table whose every other row is a real build — and making the total incomparable with the `Fix Version` table beside it, which excludes them | components, fix versions and milestones now share one `multi_counter()`; §11 and §12 each state coverage |

⚠️ **All three reconciled cleanly through every `OBJ-030` gate**, because those gates test **reproducibility
against the generator's own rule** — they cannot detect a rule that is correctly implemented and wrongly
named. **Reconciliation is not validation.** That gap is what `tools/jira/validate_analysis.py` now closes:
it re-derives every headline figure from the raw snapshot and compares it with the published markdown, so
a figure passes only when the report and the source agree. Run it before circulating anything:

```powershell
python tools\jira\doctor.py              # environment + freshness preflight; exit 0 = ready
python tools\jira\validate_analysis.py   # 57 checks; exit 0 = every figure matches the source
```

⚠️ **A validator that has never failed proves nothing**, so this one was run against the pre-fix reports
from `cea4352` and confirmed to catch the CI sub-task defect by name (`+2798`) and the missing PAMIT
coverage line. Each census report now also carries a **`Source snapshot:`** header line naming its snapshot
and a sha256 of its bytes, which the validator recomputes — a report can no longer claim a source it was
not built from. Full account: `docs/hardening/README.md`.

⛔ **That hash is taken over the snapshot's bytes as checked out, so line endings count.** The snapshots
were CRLF when they were hashed. Git stores them as LF, and `core.autocrlf=true` restores CRLF on checkout.
A clone with `autocrlf` off gets LF and fails `B0-provenance` against a correct report. Check
`git config core.autocrlf` before you believe a provenance failure.

⚠️ **One provenance failure is real and has been in the history since the first commit.** Both
`artifacts/snapshots/ci-analysis-*.json` files were rewritten at 19:33 on 2026-09-25, 15 minutes before
`8d8b841`. `.gitignore` records a redaction made before the first commit; whether this rewrite was part of
it is unverified. The committed 21 Sep CI snapshot now hashes to `650b1e8e…`, while the CI report's header
claims `5e12f6be…`. Run against a `git archive` of HEAD, the validator gives **PASS 56 · FAIL 1**, and that
failure is this one. Which way to fix it is the owner's call: regenerate the CI report from the committed
snapshot (`run_census.py --project CI`) and check whether any figure moved, or restore the pre-rewrite
snapshot. **Never edit the hash in the markdown.**

⛔ **JQL `created <= 'YYYY-MM-DD'` means `<= YYYY-MM-DD 00:00` — it silently excludes the whole end day.**
Every edition of both reports before `OBJ-030` omitted its own final date (24 PAMIT / 31 CI tickets in the
03 Sep edition). Both generators now compute `DATE_TO_EXCLUSIVE` and emit `created < …`. **Any new JQL
written here uses the exclusive form.** Both also derive their output filename from `RANGE_SLUG`, which
exists because the 03 Sep edition was renamed by hand and the generator then wrote a *different* file,
leaving the intended deliverable stale.

### ⛔ Jira access is structurally read-only

`jira_query.py` enforces it in `_check()`, not by convention: `GET` only to a fixed prefix list, and
`POST` only to the two **search** endpoints (`/rest/api/3/search/jql`, `/search/approximate-count`).
Anything else raises `ReadOnlyViolation`. It never transitions, comments on, assigns, edits or creates an
issue. Three API facts baked into that layer:

- `GET /rest/api/3/search` is **gone** — HTTP 410. Only `/search/jql` remains, paged by opaque token.
- `/search/approximate-count` **was measured wrong here.** Any figure reaching a report must come from
  `search()`, which enumerates.
- Array-returning endpoints (`/project/{k}/versions`, `/field`) go through `_get_list`, never `_get`.
  Coercing a list body to `{}` once reported HTTP 200 and "no versions" for a project with 122 of them —
  a silent failure that reads exactly like a clean result.

`tools/jira/jira.md` covers ticket *creation* (ADF not wiki markup; `createmeta` under-reports 6 required
fields). Creation belongs to the full deployment — nothing in this copy raises a ticket.

### The field rulings — these still bind, and each one was paid for

| Ruling | Rule |
|---|---|
| `D42` | Build axis is **`Affected Milestone` (`customfield_10092`, 97.3% — 1,346/1,384)** — where the client *found* it. **Not** `Fix versions` (where a fix *ships*), and **not** any field named `Milestone` (0–9%, or 63% populated with the literal `None`) |
| `D43` | **No count without its tickets.** Sheet `04 Ticket Details` is the source; `09 Count Reconciliation` restates every headline as a live `COUNTIFS` with `PASS`/`FAIL`; `pamit_workbook.verify()` exits non-zero if anything fails |
| `D44` | **One workbook, many worksheets.** A new analysis is a new `sheet_*` builder in `build()` **plus its manifest row** in `sheet_readme()` — never a second `.xlsx`. The two are hand-kept in step |
| `D46` | Quote a regression figure **over its populated subset, with the subset size beside it.** The three client-facing fields (`cf 10780`, `cf 11253`, `cf 11254`) sit at ~25%. An unfilled field is **never** evidence of "no regression"; the sentinel is `Info not available in JIRA` |

⚠️ **The lesson `D42` and `D46` share, recorded twice because it cost twice: several Jira fields share a
concept and only one is live. Measure every same-named candidate before picking one** — a 0% field returns
an empty result indistinguishable from a clean one. Using `fixVersion` moved the build line 1,384 → 2,010
and made the current build `HF13` look 13× worse than it is. The same error class then hid `RCA`
(`cf 10245`, **80.7% — 1,622 tickets**, 33 values in 15 families — the most populated analytical field in
the project) behind two decoys at 0.2% and 0.1%, producing a report that claimed
Jira held no root-cause data at all. Full audit: `docs/analysis/D1-client-ticket-patterns.md` §0.2 + workbook sheet `10 Field Audit`.

⛔ **`Phase` and `ReopenCount` exist and are 0%.** Defect-injection phase is **not answerable** and is
**not** derivable from `RCA` — `Code - Logic Issue` says where a defect was *found in code*, not where it
was *introduced*. ⛔ **315 tickets are classified by the product team as "not a product defect"** — a weak
spot attributed to one is a false finding, reported but never silently applied to a denominator (`D38`).

## Layout — five drawers by kind, plus one dated deliverable

| Path | Holds |
|---|---|
| `tools/` | Everything executable. `jira/` is the live half here; `rag/`, `analysis/`, `onboarding/` and the three React apps also work. The flat `obj0NN_*` harness does not (§What this folder is) |
| `docs/` | Everything a human reads. `analysis/` (**12** reports, plus `README.md`, `summary.md` and a dated `summary/` series) · `history/` (**append-only** register + narrative) · `hardening/` (the 2026-09-22 review — what was wrong, what changed, what is still open) · `briefs/` · `findings/` · `business-context/` · `gaps/` · `knowledge-base/` · loose `graph.md` and `runs.md`. ⚠️ `management/` and `specs/` are **absent**, although the root `README.md` still lists them |
| `data/` | Authored input. `sources/` (3 vendor PDFs, ~83 MB, stored in Git LFS) · `analysis/` (8 hand-maintained JSON) · `profiles/` |
| `artifacts/` | Everything a tool produced — **never hand-edit; fix the tool and re-run.** `workbooks/` · `client-tickets/` · `snapshots/` · `rag-corpus/` · `analysis-data/` · `graph/` · `flows/` · `deck/` |
| `state/` | Job state and audit logs — `client-analysis/` `daily/` `drift/` `obj010/` `perf/` |
| `BLAST/` | Requirement intake. `Objective.md` is the active instruction; `B.L.A.S.T.md` is the protocol. **Has its own `CLAUDE.md`** with a hard "Protocol 0 HALT" — read it before touching `BLAST/` |
| `21-09-2026/` | ⚠️ The **only** generated output living outside `artifacts/` — the owner's explicit layout for the client delivery pack. Still generated: re-run `build_delivery_pack.py`, never hand-edit |

⛔ **`tools/paths.py` is the single root resolver.** It finds the root by searching upward for a directory
holding **both** `CLAUDE.md` and `.claude/` — which is why renaming this file would break every script.
**Never count parent directories**; import `workspace_root()` or `ROOT`. It raises `SystemExit` loudly
rather than guessing, because every historical failure here was a script that carried on with a wrong root
and wrote to the wrong place. The docstring records the 25 sites this replaced.

⚠️ `paths.py` still defines `PAM`, `AUTOMATION_REPO`, `BOOTSTRAP`, `RUNS`, `LOOPHOLES` and others that
resolve to **non-existent directories here**. A `Path` object is not a promise; `.exists()` before use.

## Product documentation — the RAG corpus

`artifacts/rag-corpus/` holds three extracted, page-cited documents, all present in `corpus.jsonl`:

| Doc id | Pages | Contains |
|---|---:|---|
| `pam-api` | 2,470 | 3,194 JSON payload examples — the best request-body source available |
| `pam-admin` | 702 | Access model and product concepts. ⛔ **No endpoints, schemas or error codes** |
| `client-manager` | 399 | Same kind — administrator guide, not an API contract |

Cite every fact as `<doc>:p<N>` (e.g. `pam-admin:p455`) so a reviewer can check it against the printed page.

⛔ **Never read `artifacts/rag-corpus/pam-api.md` directly — it is 101,803 lines** (`pam-admin.md` 18,560,
`client-manager.md` 9,611). A read returns the first 2,000 lines *with no error*, so a truncated read looks
exactly like a complete one. Treat anything over ~1,500 lines as truncated until proven otherwise: `wc -l`
first, then `grep -n "^## "` for a section map, then read only those ranges. A `.headings.tsv` sits beside
each `.md` and is the cheap way in.

🔴 **The documented query command is broken in this copy and upstream.**
`python tools\rag\query.py find "<terms>"` raises `FileNotFoundError`: `query.py:22` hardcodes
`CORPUS = Path(__file__).parent / "corpus"`, but `extract.py` writes to `artifacts/rag-corpus/`.
`OBJ-025` re-pointed the writer and not the reader, and `query.py` is the one script that does not import
`paths.py`. Verified broken in `E:\Omkar\AI Projects\Dev Project` too, so it is a real defect, not a copy
artifact. The fix is one line — `from paths import RAG_CORPUS as CORPUS` — but it belongs upstream, so
**raise it rather than patching this copy silently.** Until then, grep the corpus files directly.

## ⚠️ Divergence — this is not the only copy

`tools/jira/` has drifted **in both directions** against `E:\Omkar\AI Projects\Dev Project`. Measured
2026-09-22, then re-measured on 2026-09-26 against its D: copy `..\dynamic-api-validator\tools\jira\`.
Every size below still holds, and the only correction was adding `run_census.py`, which the earlier table
had left out. Re-measure before relying on it, because both sides move:

| | Files | Evidence |
|---|---|---|
| **Dev Project ahead — 7** | `pamit_analysis_rules.py` · `pamit_client_analysis.py` · `pamit_report.py` · `pamit_workbook.py` · **`jira_query.py`** · **`track_tickets.py`** · `create_b01.py` | `pamit_analysis_rules.py` 86,440 B (15 Sep) vs **77,662 B here** (3 Sep); `jira_query.py` 13,665 B (8 Sep) vs **13,441 B here** |
| **Here ahead — 10** | the whole 2026 census line: `jira_analysis_2026.py` · `ci_analysis_2026.py` · `analysis_classify.py` · `analysis_render.py` · `convert_analysis.py` · `md_to_docx_xlsx.py` · `build_delivery_pack.py`, plus `validate_analysis.py`, `doctor.py` and `run_census.py` (added 2026-09-22) | **absent on Dev Project** |

⛔ **Neither copy is a superset, and the behind-set is wider than the `pamit_*` four** — it includes
**`jira_query.py`, the read-only enforcement layer itself.** Editing any of those seven here silently
edits a copy 5–12 days behind the maintained one. This folder's own history starts at `8d8b841` and
cannot show what changed on the other side. **Before changing anything under `tools/jira/`, check which
side owns the file** and say which copy you are in. The ten here-only modules are owned here and are safe
to edit. `register_client_analysis_task.ps1` also differs from the D: copy: same size, 4 bytes, not yet
examined.

⚠️ **`tools/jira/pamit_fmt.py` is a tenth, newly-diverged file.** It was **byte-identical on both sides**
(measured 2026-09-22: `HEAD:tools/jira/pamit_fmt.py` vs `Dev Project\tools\jira\pamit_fmt.py`, no
difference) until `snapshot_provenance()` was added here on 2026-09-22. Both census generators import it.
It is an **additive** change — nothing existing was altered — so porting it upstream is a clean append, but
this copy is now ahead on a file the divergence table above had listed on neither side.

## Conventions that still bind

- **`docs/history/README.md` is append-only** — the index; `docs/history/01-objective-records.md` holds the
  `OBJ-NNN` register. Never delete, reword or reorder an existing entry. Updating a live objective's
  **Status** in place is the only permitted exception. No dates in narrative fields — the sequential ID is
  the ordering ("superseded by `OBJ-00N`", never "archived on `<date>`"). **Filesystem paths are exempt:**
  `artifacts/runs/2026-07-29_181439/` is an identifier, cite it exactly.
- ⚠️ **The register stops at `OBJ-029` while `BLAST/Objective.md` holds `OBJ-030`.** OBJ-030 is complete
  but **not yet archived** — archive it to `01-objective-records.md` *before* overwriting `Objective.md`
  with the next instruction, or the record of it is lost.
- **`BLAST/Objective.md` stays small** and holds the active instruction only. Never copy history into it.
  Archive the outgoing objective to the register *before* overwriting. `BLAST/` has been tracked since
  `8d8b841`, but only a committed version can be restored, so commit before you overwrite.
- **Traceability over tidiness.** Name the real artifact — report, workbook sheet, script, snapshot file,
  Jira key. A figure quoted without its basis is a defect; several counts here legitimately differ by unit.
- `.claude/rules/` holds three path-scoped rules. `markdown-docs.md` (`**/*.md`) applies; `api-surface.md`
  partly applies via `tools/**` and `docs/findings/**`; **`automation-repo.md` is dead** — every glob it
  matches on is an absent directory.

## Running the dashboards

`tools/dashboard/`, `tools/dashboard-performance/` and `tools/control-center/` are React + Vite.
`node_modules/` is absent in all three, so `npm install` comes first, then `npm run dev`. The first two
read committed JSON from their own `public/data/` and render correctly offline. **`control-center/` is
inert here** — its server (`tools/control_center.py`) exists to approve git actions against repositories
this copy does not contain.

## Measured facts worth not re-deriving

Re-measured 2026-09-22. The validator and runtime rows were re-measured 2026-09-26.

| Fact | Value | Where |
|---|---:|---|
| Client-ticket workbook | **13 sheets**; `04 Ticket Details` = **2,201 tickets × 71 columns** | `artifacts/workbooks/PAM-Client-Ticket-Analysis.xlsx` (gitignored; local-only) |
| …its row geometry | 5-line title block, blank row 6, header row **7**, data rows **8–2208** (`max_row` 2208) | ⚠️ quote the unit — the prior "2,206 rows" matched neither |
| PAMIT tickets, 2026-01-01 → 2026-09-21 | **5,740** = 3,705 client + 2,035 internal | `docs/analysis/Jira_Analysis_01Jan26-21Sep26.md` |
| CI tickets, same range | **5,994** = 1,456 client + 4,538 internal | `docs/analysis/CI_Jira_Analysis_01Jan26-21Sep26.md` |
| CI sub-tasks | **1,443** (`issuetype.subtask`, agreeing with `issuetype.name`) — the report published 4,241 until 2026-09-22, counting parent-presence and sweeping in 2,798 Epic children (2,123 Bugs, 373 Stories, 266 Tasks) | `ci_analysis_2026.py`; §1/§15/§15A now agree with §3 |
| PAMIT Affected Milestone | **4,523 of 5,740 tickets (78.8%)** populated → **4,615** assignments over **101** distinct values | `docs/analysis/Jira_Analysis_01Jan26-21Sep26.md` §12; published as 100% `Not set` until 2026-09-22 |
| PAMIT Fix versions | **1,558 of 5,740 tickets (27.1%)** populated → **1,607** assignments over **68** values — the gap against 78.8% above is exactly why `D42` names Affected Milestone as the build axis | same report, §11 |
| Daily client-analysis captures | stop at **2026-09-03** — that line is paused; the census line is the active work | `artifacts/client-tickets/snapshots/` |
| `validate_analysis.py` on commit `8d8b841` | **57 checks: PASS 56 · FAIL 1** (CI `B0-provenance`, §Three defects). `--self-test` passes | run on a `git archive` of HEAD |
| Runtime, original machine | Python **3.14.7** · Node **v24.19.0** · everything in `tools/requirements.txt` | measured 2026-09-22 |
| Runtime, D: machine | only `python3.11` (3.11.9, no packages) · Node **v24.16.0**. `doctor.py`, `validate_analysis.py` and `run_census.py --dry-run` run there; nothing that renders does | measured 2026-09-26 |

⛔ **Re-measure before quoting any number in this file.** This is not decorative — it keeps catching this
document. The revision two back described itself as "65 KB / 836 lines" while measuring 68,498 bytes /
854 lines, and claimed `docs/analysis/` held 10 reports when it holds 12. The revision before this one
carried a workbook ticket count off by five and an active objective ID off by one, listed a renderer
command without its required argument, and understated the `tools/jira/` divergence by three files —
every one of them inside a section warning against exactly that.
