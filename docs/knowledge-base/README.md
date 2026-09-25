# questions/ — the project knowledge base

**Objective:** `OBJ-008` · **Owner:** Sudesh Sawant · **Jira:** `PAMIT`
**Deliverable:** `PAM-Project-Knowledge-Base.xlsx` — every question someone might ask about this project,
with its answer, the supporting evidence, and comments.

Built for three uses: **demonstrations**, **documentation**, and **management discussion**. It is meant to be
readable end to end — read the questions and answers in order and you should understand what has been
implemented and why.

---

## 1. The workbook

| Sheet | What it is |
|---|---|
| **`Index`** | Counts by category, audience, status, impact and owning team · how to add a question · any validation problems |
| **`Q&A`** | **The knowledge base.** One row per question. Filter on `Category`, `Audience`, `Status` or `Impact` using the header dropdowns |
| **`Demo Flow`** | A suggested walkthrough order for a live demonstration. Names a category per step and why it comes there — it references questions rather than copying them, so it cannot fall out of step with the answers |

### Columns

`Question` · `Answer` · `Evidence` · `Comments` are the required four and lead deliberately. The rest is
metadata for filtering: `ID` · `Category` · `Module` · `Source` · `Example` · `Swagger / API Reference` ·
`Related Documents` · `Status` · `Impact` · `Audience` · `Owner` · `Last Updated`.

`ID` is stable — `Q-API-NN` (API and validation), `Q-FW-NN` (framework, database, security, environment),
`Q-PRJ-NN` (project, documentation, governance, metrics, roadmap). Cite a question by its ID; it does not
change when rows are re-sorted.

---

## 2. The rule that makes this worth reading

⛔ **An answer without a citation is not an answer.**

Every `Evidence` cell names something you can open: a file path, a report, a run folder, a `file.java:line`,
a SQL query, a `<doc>:p<N>` page reference, or a git commit. The builder **refuses to accept an uncited
answer silently** — a row missing evidence is written with `⚠️ NO EVIDENCE CITED`, forced to `Status = Open`,
and listed on the `Index` sheet.

**A question with no answer still belongs here.** Set `Status = Open` and let the answer say plainly what is
unknown and what would settle it. That matters more than it sounds: this project's largest single finding is
*how much* of the API is undocumented, and that figure only holds if nothing was filled in to look complete.

`Status` values: `Answered` · `Answered - with caveats` · `Open` · `Superseded`.

---

## 3. Adding a question

This is a **living document** — when a question comes up in development or a discussion, add it.

1. Open the right file under `data/`:
   - `questions-api.json` — API surface, envelope, positive, negative, chaining, mandatory fields
   - `questions-framework.json` — framework, execution, database, security, environment, test data
   - `questions-project.json` — project, documentation, findings, governance, tooling, risks, metrics, roadmap
2. Append a row object. Minimum: `id`, `question`, `answer`, `evidence`.
3. Rebuild:

```powershell
python tools\build_knowledge_base.py
```

The build prints the category breakdown and **exits non-zero if any row fails validation** — duplicate ID,
missing evidence, unknown status. Fix the JSON, not the workbook.

⛔ **Never edit the `.xlsx` directly.** `build_knowledge_base.py` is the only writer; the next build discards
a hand edit. Same rule as `document/` — one writer per artifact.

Full authoring rules, including how to phrase a question well: `_AUTHORING-CONTRACT.md`.

---

## 4. How this relates to the rest of the workspace

| Layer | Home |
|---|---|
| Active instruction | `BLAST/Objective.md` |
| Objective history and the `OBJ-NNN` register | `docs/history/README.md` + `docs/history/` |
| **Q&A knowledge base — what things are and why** | **`questions/`** |
| Analysis: reports and tabular workbooks | `document/` |
| Raw measured evidence from execution runs | `artifacts/runs/<timestamp>/` |
| The 12 developer findings, as one brief | `docs/briefs/developer-loopholes.md` |
| Framework code | `Automation gitlab repo/pam_automation_bootstrap/` on `AI` |

`questions/` does not duplicate `document/`. `document/` holds the analysis and the row-level evidence;
`questions/` answers "what is this and why" and **cites** `document/`. Where the two overlap the convention
is to cross-reference, never restate — so a figure has one home and one provenance.

This is the one deliberate exception to OBJ-007's "all documentation goes in `document/`" rule: the owner
asked for the knowledge base in its own folder, at the same level as `BLAST/`.
