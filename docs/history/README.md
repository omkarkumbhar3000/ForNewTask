# History — Append-only record of objectives, decisions and what was learned

**Starts at:** `OBJ-031` · **Next objective ID:** `OBJ-032` · **Next decision ID:** `D52`
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
| OBJ-031 | Make the workspace a clean, reusable BLAST framework, and prepare `New Task/` for the next development project | 🟡 In Progress — stage 1 (preparation) done: Jira/PAM/CI material removed (661 files, recoverable from `2a3298d`), objective hook repaired, `New Task/Current Project/` and `New Task/Updated Project/` created. Stage 2 (analyse and build the updated project) waits for the owner's upload. Narrative: `03-narrative-log.md` §OBJ-031 |
