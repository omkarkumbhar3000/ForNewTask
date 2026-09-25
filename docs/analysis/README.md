# docs/analysis/ — the report index

**Owner:** Sudesh Sawant · **Jira:** `PAMIT`, `CI` · **Environment:** `QA_MsSQL` only

**Twelve reports, two evidence bases** — §3 splits them, and a figure means nothing without knowing which:

| Set | Reports | Derived from |
|---|---|---|
| **API validation** (`OBJ-007`) | `A1`–`A7`, `B`, `C` | `artifacts/runs/2026-07-29_181439/` — 326 flows · 1,873 hops · 1,868 calls · 1,868 evidence files |
| **Jira ticket analysis** (`OBJ-028`/`OBJ-029` and the 2026 censuses) | `D1`, `Jira_Analysis_…`, `CI_Jira_Analysis_…` | Jira, via the read-only query layer — **no execution run involved** |

⚠️ **This README predates `OBJ-025` in places.** The `document/`, `questions/`, `reports/` and branch `AI`
names below are stale; `_AGENT-BRIEF.md` and the two `OBJ-007` workbooks are **not present in this tree**
(only `PAM-Client-Ticket-Analysis.xlsx` is). Sections 1, 2 and 6 have not been re-verified.

---

## 1. Start here

| If you want | Open |
|---|---|
| **To demo how business context is given to the AI** | ⭐ **`BUSINESS-CONTEXT-DEMO.md`** — short, walkable in 5 minutes. **Use this one live** |
| The full reference behind that demo | `BUSINESS-CONTEXT-STANDARD.md` — 27 sections, same example extended through the approval chain. §0 is a reusable checklist |
| The management view — risks, owners, priorities | `workbooks/PAM-Project-Governance.xlsx` → **Management Findings** |
| The technical analysis — every row of evidence | `workbooks/PAM-API-Validation-Analysis.xlsx` → **Index** |
| What is wrong today and what to do about it | `workbooks/PAM-Project-Governance.xlsx` → **Observations**, **Solutions** |
| What changed in the framework and why | `reports/B-framework-validation-enhancement.md` |
| Whether database validation is possible | `reports/C-database-validation.md` |

Both workbooks open on an **Index** sheet listing every worksheet, what it holds, and its row count. A row
count of zero is highlighted — it means the input was not produced, and the Index says which.

---

## 2. Workbooks

### `workbooks/PAM-API-Validation-Analysis.xlsx` — technical

| Worksheet | Item | Holds |
|---|---|---|
| `Chaining Validation` | A1 | One row per executed hop, every `L1`–`L7` verdict, parent/child dependency, extracted identifier, cause bucket |
| `L6 Read-Back` | A4 | Every hop where a created object was read back through the API |
| `Positive Validation` | A2 | Endpoint, payload, expected vs actual, what was validated, what a correct assertion would also check |
| `Negative Validation` | A3 | All 1,306 endpoints × ≥5 scenarios across 19 categories |
| `Negative Coverage` | A3 | Category and controller aggregates; endpoints with no coverage |
| `Envelope Shapes` | A2 | The measured response-shape census |
| `Required Fields` | A5 | Per-property mandatory / length / format / pattern metadata and its status |
| `Required Fields Summary` | A5 | The counts, per controller and for the 217 create endpoints |
| `Doc Gap Coverage` | A7 | Per-controller documentation coverage |
| `DB Schema Map` | C | API object → table → key → identifying columns → encrypted? → feasibility |

### `workbooks/PAM-Project-Governance.xlsx` — management and tracking

| Worksheet | Item | Holds |
|---|---|---|
| `Observations` | D | Daily issues, blockers, missing docs and APIs, framework and product limitations, suggestions, workarounds |
| `Management Findings` | D | The escalation view: risk, action item, owning team, priority, recommendation |
| `Solutions` | A8 | Every issue with a recommended **and** an alternative solution, advantages, disadvantages, effort |
| `DB Observations` | C | Every database observation, each carrying the query that produced it |

---

## 3. Reports

⚠️ **The `reports/` prefix below is stale** — `OBJ-025` flattened these into `docs/analysis/`, so every
file named here is a **sibling of this README**. Read `A1-chaining-analysis.md`, not `reports/A1-…`.

### The `OBJ-007` API validation set

| File | Item | Answers |
|---|---|---|
| `A1-chaining-analysis.md` | A1 | Why 196 hops resolved no identifier, and how the cascade propagated |
| `A2-positive-validation.md` | A2 | What positive testing covers, and the gap between "validated" and "should be validated" |
| `A3-negative-validation.md` | A3 | What a correct negative assertion looks like on this API, and how little exists |
| `A4-l6-read-back.md` | A4 | Why only 2 of 107 read-backs passed — and why most of the rest prove nothing |
| `A5-mandatory-field-analysis.md` | A5 | The mandatory-field gap and its downstream consequences |
| `A6-developer-repo-analysis.md` | A6 | Why the developer repository is insufficient |
| `A7-documentation-gap-analysis.md` | A7 | What the documentation is missing and how to make it robust |
| `B-framework-validation-enhancement.md` | 7, 8, 10 | What changed in the framework, verified, and what it does **not** fix |
| `C-database-validation.md` | 4, 13 | Whether DB validation is possible, the approach, limits and permissions |

### The Jira ticket-analysis set

A separate evidence base: **Jira**, not an execution run. Nothing here derives from `artifacts/runs/`.

| File | Objective | Covers | Regenerate |
|---|---|---|---|
| `D1-client-ticket-patterns.md` | `OBJ-028`/`OBJ-029` | Client-raised PAMIT defects — testing weak spots, build-wise escape, regression signal, RCA families. Its tabular half is `artifacts/workbooks/PAM-Client-Ticket-Analysis.xlsx` (13 sheets) | `python tools\jira\pamit_client_analysis.py --offline` |
| `Jira_Analysis_01Jan26-21Sep26.md` | `OBJ-030` | **PAMIT census, 01 Jan – 21 Sep 2026**: 5,740 tickets (3,705 client · 2,035 internal). Status, priority, type, components, assignees, reporters, creation trends | `python tools\jira\jira_analysis_2026.py --offline` |
| `CI_Jira_Analysis_01Jan26-21Sep26.md` | `OBJ-030` | **CI (Converged Identity) census, same range**: 5,994 tickets, **1,443 of them sub-tasks**. The only report here covering a project other than `PAMIT` | `python tools\jira\ci_analysis_2026.py --offline` |

⛔ **The sub-task figure was 4,241 in every edition before 2026-09-22 and that number was wrong.**
`ci_analysis_2026.py` counted *parent-presence*, and in modern Jira `parent` spans the whole hierarchy, so
2,798 Epic children (2,123 Bugs, 373 Stories, 266 Tasks, plus a tail) were counted as sub-tasks. The real
count is 1,443, which `issuetype.subtask` and `issuetype.name` agree on exactly — and which §3 of that same
report had been publishing all along, contradicting its own §1 and §15. If you are holding an older edition,
its §1/§15 sub-task rows and §15A parent table are wrong; nothing else in it is affected.

The `.docx` and `.xlsx` beside these three are **rendered from the markdown, not authored** — change the
markdown and re-render with `python tools\jira\md_to_docx_xlsx.py`. Editing a `.docx` directly is lost on
the next render. ⚠️ **Build-wise figures use `Affected Milestone` (`cf 10092`), never `Fix versions`**
(`D42`); regression figures are quoted over their ~25% populated subset with the subset size beside them
(`D46`). `Product Stack Dependency Matrix_CI(…).docx` is vendor-supplied input, not a generated report.

### Checking a census report before you circulate it

```powershell
python tools\jira\validate_analysis.py      # 55 checks; exit 0 = every figure matches the source
```

It re-derives each headline figure straight from the JSON snapshot and compares it with the published
markdown, so it can catch what re-running the generator cannot: a rule that is correctly implemented and
wrongly named. It also verifies that the `.docx`/`.xlsx` and the `21-09-2026/` delivery pack really were
built from the current markdown. Each census report now carries a **`Source snapshot:`** line naming its
snapshot and a sha256 of its bytes; the validator recomputes that digest, so a report cannot claim a source
it was not built from. Full rationale: `docs/hardening/README.md`.

---

## 4. How to read a figure in here

Three conventions, applied throughout, so a number can always be traced or discounted:

| Value | Means |
|---|---|
| A number | Traceable to a named file — `results.json`, a `.java` line, or a SQL query recorded alongside it |
| `NOT EXECUTED — no evidence` | The scenario is designed but was never run. **Not** a pass and not a failure |
| `UNKNOWN — contract undocumented` | No documented expected outcome exists. This is a finding in its own right, and it is counted |

⛔ **Nothing here is a plausible guess.** Where evidence is absent the cell says so. This matters because
the objective's largest single finding is *how much* is undocumented — 73.4% of negative scenarios have no
documented expected outcome — and that figure only means something if nothing was filled in to look complete.

⚠️ **A `FAIL` is not automatically a product defect.** The clearest example: 105 of 107 `L6` read-backs were
recorded `FAIL` in the source run, but **97 of them could never have passed** — the harness searched each
response for the literal string `${NEW_ID}`. Those verdicts carry no information about the product.
`reports/A4-l6-read-back.md` separates harness artifact from product behaviour, and the new framework models
`NOT RUN` as distinct from `FAIL` precisely so this cannot recur.

---

## 5. Regenerating

Generator scripts live in `tools/` — the standing workspace rule is that every harness script
lives there and only its **output** lands here.

```powershell
python tools\obj007_chain_analysis.py       # A1, A4  -> data/analysis/
python tools\obj007_positive_analysis.py    # A2
python tools\obj007_negative_matrix.py      # A3
python tools\obj007_required_fields.py      # A5
python tools\measure_doc_gap.py             # A7
python tools\obj007_db_probe.ps1            # C   (read-only SELECTs)
python tools\obj007_build_workbooks.py      # both .xlsx from data/analysis/*.json
```

`obj007_build_workbooks.py` is **the only thing that writes `.xlsx`**, so worksheet shape is decided in one
place. It is idempotent and tolerates missing inputs — a worksheet whose source is absent is written with an
explanatory row rather than omitted, because an absent worksheet reads as "not applicable", which is a
different claim.

`data/analysis/*.json` is the machine-readable layer and the input to the workbooks. Edit the JSON, re-run
the builder — never edit the `.xlsx` by hand, or the next build discards it.

---

## 6. Where this sits in the workspace

| Layer | Home |
|---|---|
| Active instruction | `BLAST/Objective.md` |
| Objective history and the `OBJ-NNN` register | `docs/history/README.md` + `docs/history/` |
| **This objective's analysis, workbooks and reports** | **`document/`** |
| Q&A knowledge base — "what is this and why", for demos and management | `artifacts/workbooks/PAM-Project-Knowledge-Base.xlsx` |
| Raw measured evidence from execution runs | `artifacts/runs/<timestamp>/` |
| The 12 developer findings, as one brief | `docs/briefs/developer-loopholes.md` |
| Per-finding raisable ticket packs | `artifacts/loopholes/LH-NN-*/` |
| Framework code | `Automation gitlab repo/pam_automation_bootstrap/` on `AI` |

`document/` does not replace `Reports/` — `Reports/` holds the raw evidence from execution, `document/` holds
the analysis of it. Where a finding here overlaps `docs/briefs/developer-loopholes.md` or `docs/findings/issues/`,
the convention is to **cross-reference rather than restate**.

`questions/` is a third, distinct layer: it answers *"what is this and why"* in question-and-answer form and
**cites** the reports here. So a figure keeps one home and one provenance — if a number appears in both, the
knowledge base points at `document/` rather than restating the derivation.

`_AGENT-BRIEF.md` is the working brief the analysis was run against: hard safety rules, the authoritative
tallies, and the output contract. It is kept because it records the constraints every figure was produced
under.
