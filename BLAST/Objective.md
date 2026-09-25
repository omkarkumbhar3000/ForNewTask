# Objective.md — Active Instruction

> **This file holds one thing: what I want done right now.** Rewrite the §Instruction block below and
> save. It is imported by the root `CLAUDE.md` and re-injected on every prompt, so the change takes
> effect immediately — no need to restate context, point at the file, or start a new session.
>
> **Keep it small.** Nothing historical belongs here. Everything already known about this project —
> decisions, prior requirements, measured findings, the backlog — lives in
> [`../docs/history/README.md`](../docs/history/README.md) and in the workspace docs. The
> assistant reads those when it needs them and must **never copy them back into this file.**

**Owner:** Sudesh Sawant · **Jira:** `PAMIT` · **Updated:** 2026-08-26
**Environment:** `QA_MsSQL` only — API `https://u16hf.arconnet.com:6302` (app URL is `:1302`)

---

## Instruction

<!-- ▼▼▼ WRITE THE CURRENT REQUIREMENT HERE — replace everything between the markers ▼▼▼ -->

**`OBJ-030` — Extend both 2026 Jira census reports from 03 Sep to 21 Sep 2026.** ✅ **Complete.**
PAMIT **5,431 → 5,740**, CI **5,588 → 5,994**. Kept here as the active record until the owner issues the
next instruction. ⛔ **A pre-existing defect was found and fixed:** JQL `created <= 'YYYY-MM-DD'` excludes
that whole day, so every prior edition of both reports omitted its own final date (24 PAMIT / 31 CI tickets
in the 03 Sep edition). See §Validation results below and `../docs/history/04-narrative-log.md`.

Update `Jira_Analysis_*` (PAMIT) and `CI_Jira_Analysis_*` (CI) to cover **2026-01-01 → 2026-09-21**,
processed separately. ⛔ **Update the analysis, do not change the methodology.**

### Method — regenerate, never hand-edit

Both reports were measured **100% generated**: regenerating each from its own 03 Sep snapshot reproduced
the on-disk file with **2 differing lines out of 469 / 433**, both the `Generated:` timestamp. Nothing is
hand-authored. So the requirement "preserve the format, headings, tables, calculations and analysis logic"
is met **by construction** — bump `DATE_TO` in the generator and re-run. Hand-editing the markdown would
be the one approach that *could* break it.

### Owner decisions taken at intake

| | Decision |
|---|---|
| **Filenames** | Rename to `01Jan26-21Sep26`; **retire the `03Sep26` set** (`.md` + `.docx` + `.xlsx`). One current report per project. The 03 Sep JSON snapshots are retained, so the old report stays reproducible |
| **Historical window** | **Full re-fetch.** The report is a point-in-time census; it is now taken on 21 Sep instead of 03 Sep, so Jan–Sep tickets carry their *current* status/resolution. Same methodology, later evaluation date. The historical drift is to be **quantified and reported**, never silent |

⚠️ **`jira_analysis_2026.py` writes a filename computed from its date constants**
(`Jira_Analysis_20260101-20260903.md`) which **does not match the file on disk** (`…01Jan26-03Sep26.md`) —
it was renamed by hand after generation. Re-running it unchanged writes a *new* file and leaves the
intended one stale. `ci_analysis_2026.py` hardcodes its output name instead. Both must be fixed to emit
the agreed name, or the deliverable silently misses.

### Validation gates — all must pass before the work is called done

1. No missing dates and no duplicate issue keys across the full range.
2. Old-window ticket **set** is unchanged (JQL filters on `created`); only field *values* may move.
3. Every headline count reconciles against the enumerated ticket list — ⛔ **never**
   `/search/approximate-count`, which `jira_query.py` records as measured-wrong here.
4. Report body, summary section and the `.docx`/`.xlsx` renders agree with each other.

### Deliverables

| What | Where |
|---|---|
| PAMIT census | `docs/analysis/Jira_Analysis_01Jan26-21Sep26.md` + `.docx` + `.xlsx` |
| CI census | `docs/analysis/CI_Jira_Analysis_01Jan26-21Sep26.md` + `.docx` + `.xlsx` |
| Snapshots | `artifacts/client-tickets/snapshots/jira-analysis-2026-01-01-to-2026-09-21.json` · `artifacts/snapshots/ci-analysis-2026-01-01-to-2026-09-21.json` |
| Changed | `tools/jira/jira_analysis_2026.py` · `ci_analysis_2026.py` · `convert_analysis.py` (date range + output naming) |

```powershell
python tools\jira\jira_analysis_2026.py     # PAMIT, fetch + report
python tools\jira\ci_analysis_2026.py       # CI, fetch + report
```

### Validation results — 11 gates per project

| Gate | PAMIT | CI |
|---|---|---|
| No duplicate issue keys | ✅ 5,740 / 5,740 unique | ✅ 5,994 / 5,994 unique |
| Every 03 Sep ticket still present | ✅ 5,431 → 5,455 | ⛔ **1 missing — `CI-25546`** |
| End date 21 Sep present | ✅ 44 tickets | ✅ 38 tickets |
| Every empty date confirmed zero at source | ✅ 06, 14, 20 Sep | ✅ 06, 13 Sep |
| Header / §1 / client+internal / §2 / §10 all reconcile to the enumerated population | ✅ | ✅ |
| `.md` ≡ `.docx` ≡ `.xlsx` | ✅ 23 §§, 26 sheets | ✅ 18 §§, 21 sheets |

⛔ **`CI-25546` — a Jira search-index inconsistency, not a tooling defect.** Readable by `key =`
(`2026-08-31T21:57:29`, project `CI`, Story, Closed) and invisible to every bulk search. Not paging: a
one-day window returns **56 rows in a single page**, the server's own count agrees at 56, neighbours
`CI-25545`/`CI-25547` are present, and it is still absent with no `ORDER BY`. 1 in 5,994 (**0.017%**);
no aggregate is affected. The gate is left **failing on purpose** — a characterised exception beats a
suppressed one.

⚠️ **Historical drift is real and was quantified, not assumed.** Among the 5,431 pre-04-Sep PAMIT
tickets: status moved on **478 (8.8%)**, assignee 328 (6.0%), priority 3, resolution 0. CI: 350 (6.3%),
291 (5.2%), 6, 0. The ticket **set** is unchanged — JQL filters on `created` — only field values moved.

⚠️ **21 Sep was the current date**, so its final-day counts are a partial day and will grow on a later
re-run of the same range. That is not drift.

<!-- ▲▲▲ WRITE THE CURRENT REQUIREMENT HERE ▲▲▲ -->

---

## How this gets executed

The assistant runs the instruction above using the whole workspace as context, without being told twice:

| Needs | Reads |
|---|---|
| Standing rules — edit scope, never push, response envelope, safety blocklist, `JAVA_HOME` | root `CLAUDE.md` |
| Why something is the way it is — decisions, prior requirements, findings, the old backlog | `../docs/history/README.md` |
| The protocol and its phases | `B.L.A.S.T.md`; memory in `LLM.md`, `task_plan.md`, `findings.md`, `progress.md` |
| Measured evidence | `../artifacts/runs/` (runs) · `../docs/analysis/` (reports) · `../docs/findings/issues/` |
| Code and its structure | `Automation gitlab repo/pam_automation_bootstrap/` + `graphify-out/`, `AGENTS.md` |
| Product docs and payloads | `tools/rag/` |

**On completion:** append what changed and what was learned to `../docs/history/README.md`.
When this file is rewritten, its outgoing instruction is appended there first.
