# History — Append-only record of objectives, decisions and what was learned

**Starts at:** `OBJ-031` · **Next objective ID:** `OBJ-035` · **Next decision ID:** `D76`
**Earlier history:** `OBJ-001`–`OBJ-030` and `D1`–`D47` belong to the retired Jira/PAM/CI project. They are
kept in git, not in this tree: `git show 2a3298d:docs/history/README.md` (index),
`git show 2a3298d:docs/history/01-objective-records.md` (records), `git show 2a3298d:docs/history/03-decisions.md`.
IDs continue from them so no ID is ever reused.

---

## 1. Files

| File | Holds |
|---|---|
| `README.md` | This index and the objective register table (§3) |
| `01-objective-records.md` | The full ten-field record of every archived objective |
| `02-decisions.md` | Owner decisions, `D-NN`, each with its basis and consequence |
| `03-narrative-log.md` | What changed and what was learned, per objective, in order |

## 2. How to append

- ⛔ **Append-only.** Never delete, reword or reorder an entry. Fix a mistake by appending a correction. The
  one permitted in-place edit is the **Status** of a live objective in §3.
- **No dates in records.** The sequential ID is the ordering ("superseded by `OBJ-032`", never "archived on
  <date>"). Filesystem paths and commit hashes are identifiers; cite them exactly.
- **Traceability.** Name the real artifacts: files, folders, commits. A figure is quoted with its basis.
- **Archiving an objective** (before `BLAST/Objective.md` is overwritten): add its full record to
  `01-objective-records.md` under its ID with all ten fields, writing `None` rather than dropping one —
  Objective ID · Title · Status · Summary · Key Deliverables · Related Files · Reason for Archiving ·
  Pending Work · Lessons Learned / Observations · Dependencies — and update its row in §3.
- **When an owner states a durable way of working**, record it in the root `CLAUDE.md` **and** as a
  decision in `02-decisions.md`.
- Split a file into sequential parts once it passes about 600 lines, and list each part in §1.

## 3. Objective register

| ID | Title | Status |
|---|---|---|
| OBJ-031 | Make the workspace a clean, reusable BLAST framework, and prepare `New Task/` for the next development project | Superseded by `OBJ-032` — stage 1 (preparation) ✅ completed: Jira/PAM/CI material removed (661 files, recoverable from `2a3298d`), objective hook repaired, `New Task/Current Project/` and `New Task/Updated Project/` created. Stage 2 (analyse and build the updated project) never started; carried forward as Pending Work. Record: `01-objective-records.md`. Narrative: `03-narrative-log.md` §OBJ-031 |
| OBJ-032 | Correct the repository documentation, and extract the reusable framework into the new `NewProject_Framework` repository | Superseded by `OBJ-033` — ✅ completed: the folder-level `CLAUDE.md` corrected (this repository is a git repository, and eight further statements the restructure made wrong), one sentence of the global `~/.claude/CLAUDE.md` updated; `NewProject_Framework` 1.0.0 built, validated (15-check gate, negative tests, fresh-clone run), first commit `4bd37b0` pushed and verified. Decisions `D52`–`D54`. Record: `01-objective-records.md`. Narrative: `03-narrative-log.md` §OBJ-032 |
| OBJ-033 | Identify, document and address the security issues of the uploaded current project (`Kids_learn_project`), stored locally with no git push or pull | Superseded by `OBJ-034` at intake — nothing built; the security scope is folded into `OBJ-034` §20. Record: `01-objective-records.md` |
| OBJ-034 | Enhance the Kids Learn / CleverCubs project into a secure, child-friendly application with a Java backend, in `New Task/Updated Project/` (stage 2 of `OBJ-031`) | 🟡 Active — **B0–B8 built and verified**, first published in `3651d3b` (`D72`). Completion run: 219 JUnit tests pass on MySQL 8.4 **and** PostgreSQL 17 (`D73`), 6 Playwright journeys green locally, media lightened (`FUN-E29`, `FUN-E32`); review summary `Updated Project/docs/06-review-summary.md`. Remaining: the Vercel production deployment (`Updated Project/docs/07-deployment.md`). Decisions `D69`–`D75`. Narrative: `03-narrative-log.md` §OBJ-034 |
