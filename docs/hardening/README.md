# Hardening review — `Jira RCA/`, 2026-09-22

**Owner:** Sudesh Sawant · **Scope:** the whole folder · **Baseline:** commit `cea4352`

> **What this is.** A review of the `Jira RCA/` workspace against industry practice, commissioned as
> "not only to fix existing issues, but also to proactively identify and implement improvements". This
> is the consolidated account. The working state behind it is [`PROGRESS.md`](PROGRESS.md).

---

## A. Overall status

**PARTIALLY COMPLETE** — and deliberately so.

Everything in the **census reporting line** — the work this copy of the workspace exists for — is
complete, validated and reproducible. Four correctness defects were found and fixed, two silent-failure
paths were closed, and the gap that let all of them ship is now covered by an independent validator that
has been demonstrated to fail on the exact defects it was written for.

Four items are **left open on purpose**. Three are outside this copy's authority (an upstream defect, an
append-only archive, an owner-owned protocol file) and one is a pre-existing broken reference I can infer
but not confirm. Each is listed in §F with the exact decision needed. None blocks anything.

Nothing is left in a half-finished state: every script runs, every document validates, and the folder is
consistent as it stands.

---

## B. Executive summary

The folder was in better shape than the defects suggest. The code is well structured, heavily commented
with the *reasons* behind decisions, and its conventions are real rather than aspirational. What it
lacked was a way to catch a particular kind of error — and it had three instances of exactly that kind
sitting in shipped client deliverables.

**The pattern.** `OBJ-030` ran eleven validation gates per project and all three defects passed every
one. Those gates test the generator against **its own rule**: re-run it, and it reproduces the report.
A rule that is *correctly implemented and wrongly named* reconciles perfectly, every time. The milestone
counter faithfully counted what it was told to count. The sub-task counter faithfully counted parents.
No amount of re-running would ever have said otherwise.

**What that cost.** PAMIT §12 published the mandated `D42` build axis as **100% `Not set`** across all
5,740 tickets, when the field is 78.8% populated — so the report asserted that Jira held no build data,
while holding 4,615 milestone assignments. CI published **4,241 sub-tasks** where 1,443 exist, and
contradicted its own §3 by 2,798 in the process. Both went out in the `21-09-2026/` client pack.

**What changed.** The defects are fixed in the generators and every document regenerated from them. More
importantly, `validate_analysis.py` now re-derives every headline figure **from the raw JSON snapshot**
and compares it with the published markdown — two independent derivations, agreeing or not. It was run
against the pre-fix reports and confirmed to name the CI defect exactly. Reports now carry a
`Source snapshot:` line with a sha256 the validator recomputes, so a report can no longer claim a source
it was not built from. And `run_census.py` sequences the six pipeline steps so that finishing with
validation is not something a person has to remember.

**Priority discipline.** Per the brief's ordering — correctness → reliability → data integrity →
validation → maintainability → usability → documentation → presentation — nothing cosmetic was changed.
No working business logic or established methodology was altered except where it was demonstrably
wrong, and every such change is named in §C with its before/after figures.

---

## C. Changes made

### C1 — PAMIT §12 `Affected Milestone` published 100% `Not set`

| | |
|---|---|
| **File** | `tools/jira/jira_analysis_2026.py` |
| **Problem** | `FIELDS` requested `customfield_10092` and §12 read `t.get("affected_milestone")`, but `normalise()` never emitted that key. The fetched field was discarded in silence and all 5,740 tickets collapsed to `Not set` |
| **Change** | `normalise()` now emits it |
| **Reason** | `D42` names this field — where the client *found* the defect — as the build axis. Publishing it as absent left `Fix versions` (27.1%, which `D42` explicitly rejects) as the only populated version table, in a shipped client deliverable |
| **Validation** | Independent recount from the raw snapshot: **4,523 of 5,740 populated (78.8%)**, 4,615 assignments, 101 distinct values. The report now publishes exactly those figures; validator check `B10` compares them every run |

### C2 — CI sub-task count was a parent-presence count

| | |
|---|---|
| **File** | `tools/jira/ci_analysis_2026.py` |
| **Problem** | Counted `parent_key` presence. In modern Jira `parent` spans the *whole* hierarchy, so Epic children carry it too |
| **Change** | Counts `issuetype.subtask`, the flag Jira sets itself, captured before `issuetype` collapses to its name |
| **Reason** | The published 4,241 swept in **2,798 Epic children** — 2,123 Bugs, 373 Stories, 266 Tasks and a tail. §15A "Top parent tickets by sub-task count" was mislabelled with it: 13 of its 15 rows were Epics with zero sub-tasks |
| **Validation** | `issuetype.subtask` and `issuetype.name` independently agree at **1,443**, which is also what the report's own §3 had been publishing all along. §1, §15 and §15A now agree with §3. Checks `B10`–`B13` |

### C3 — §12 counted unpopulated tickets as "milestone assignments"

| | |
|---|---|
| **File** | `tools/jira/jira_analysis_2026.py` |
| **Problem** | Found during C1's validation. The footnote claimed **5,832 milestone assignments**; only **4,615** exist. The counter folded each of the 1,217 unpopulated tickets in as a `Not set` assignment — putting a `Not set` row at the top of a table whose every other row is a real build, and making the total incomparable with the `Fix Version` table directly above it, which excludes them |
| **Change** | Components, fix versions and milestones now share one `multi_counter()` that counts assignments only. §11 and §12 each carry a `**Coverage:**` line stating the populated subset, the assignment count and the distinct-value count |
| **Reason** | `D46` requires a figure to be quoted over its populated subset with the subset size beside it. It also puts the `D42` ruling in front of the reader: §11 reads 27.1% and §12 reads 78.8%, and the ruling rests on that gap |
| **Validation** | Full report diff against `HEAD` shows **exactly four hunks** — the two timestamps, the §11 coverage line, and §12. §6 Components is byte-identical, proving the shared-counter refactor behaviour-neutral. Checks `B10`/`B11` and lint `C4` |

### C4 — `--offline` silently performed a live Jira fetch

| | |
|---|---|
| **Files** | `tools/jira/jira_analysis_2026.py`, `tools/jira/ci_analysis_2026.py` |
| **Problem** | `if args.offline and snap_file.exists()` — when the snapshot was absent, the `else` branch fetched from production Jira **and overwrote the snapshot**. The operator asks for zero HTTP, gets network traffic, and loses the capture |
| **Change** | Both refuse with **exit 2** and name the missing path, matching `pamit_client_analysis.py`, which had always been correct |
| **Reason** | `CLAUDE.md` tells operators to always prefer `--offline`. A flag that does the opposite of what it promises, quietly, is worse than no flag |
| **Validation** | Tested by hiding each snapshot and running: both exited 2 with the correct message and issued no requests; both snapshots restored intact (29.3 MB / 70.0 MB) |

### C5 — `main()` return codes were discarded

| | |
|---|---|
| **Files** | both census generators |
| **Problem** | `if __name__ == "__main__": main()` — a bare call. Any non-zero return, including C4's deliberate refusal, was thrown away and the process reported success |
| **Change** | `sys.exit(main() or 0)` |
| **Validation** | The C4 test above returns a true exit 2; `run_census.py` stops on it |

### C6 — a dropped date vanished from the weekly trend

| | |
|---|---|
| **Files** | both census generators |
| **Problem** | A ticket with an absent or unparsable `created` date was silently skipped. Its Total would sit quietly below the population **while still exactly equalling the sum of its own rows** — invisible to any reconciliation check |
| **Change** | Drops are counted and, when non-zero, stated under the table with the arithmetic spelled out. Validator check `C5` fails a trend Total that does not account for the whole population unless the report states why |
| **Reason** | Currently latent — every ticket in both snapshots has a valid date — but this is the same shape as C1: a silent discard that looks identical to a clean result |
| **Validation** | Check `C5` demonstrated firing on a crafted report and staying quiet on the corrected one (`--self-test`) |

### C7 — dead code removed

| | |
|---|---|
| **File** | `tools/jira/jira_analysis_2026.py` |
| **Problem** | `comp_counter` was built over all 5,740 tickets and **never read** — §6 is assembled from `bif()`/`C.prepare`. Imports `adf_text` and `row` were also unused |
| **Change** | Removed, with a comment recording why there is no component counter |
| **Validation** | Confirmed unused by AST (no `Load` context anywhere) before removal; §6 output byte-identical after |

### C8 — `tools/requirements.txt` was wrong in three ways

| | |
|---|---|
| **Problem** | **`python-docx` was missing entirely**, while `analysis_render.py` has always imported it — so a machine provisioned purely from this file failed on *every* `.docx` render, including the whole client pack, with an ImportError naming a package the file said was not needed. It also credited `jsonschema` to `tools/onboarding/validate_profile.py`, whose own header states it is deliberately dependency-free. Import counts and the Python version (3.14.6 vs the actual 3.14.7) had drifted |
| **Change** | Re-censused by counting import lines across `tools/`, and corrected |
| **Validation** | Measured: openpyxl 34 lines / 11 files · python-docx 5 / 1 · python-pptx 7 / 2 · xlrd 5 / 5 · pypdf 1 · jsonschema 1 (in `tools/run_validation.py`). `doctor.py` now checks the file against what is actually importable |

### C9 — new: `tools/jira/validate_analysis.py` (853 lines, 57 checks)

Independent validation. It deliberately does **not** call the generators — it re-derives each figure from
the raw snapshot and compares it with the published markdown.

| Family | Checks | Covers |
|---|---:|---|
| **A** snapshot integrity | 12 | row count, duplicate keys, project prefix, date window, required fields, calendar gaps (reported as INFO — an empty day cannot be proven genuine offline) |
| **B** published vs recount | 26 | provenance digest, totals, client/internal, open/closed/unmapped, both stated identities, CI sub-tasks, PAMIT milestone and fix-version coverage |
| **C** markdown self-consistency | 10 | Totals sum their rows, `% of Total` cells divide correctly, truncation footnotes reconcile, assignment tables carry no empty-label row, trend tables partition the population |
| **D** artifact provenance | 10 | `.docx`/`.xlsx` newer than the markdown; the delivery pack byte-identical to the canonical report |
| **E** cross-report | 2 | both reports cover the same window, and the window the validator is pinned to |

`C1` is worth singling out: a multi-value axis legitimately has rows that out-sum its Total, so instead of
waving that through, the check reads the explanation the report gives and **verifies the figure in it**.

### C10 — new: `tools/jira/doctor.py` (233 lines)

Preflight. Interpreter, every third-party package with its version and what breaks without it, credential
*names* (never values, and it issues no HTTP), snapshot presence and size, report/render/pack freshness,
and a plain list of the tooling that cannot work in this copy and why. Verified to run clean under
`PYTHONIOENCODING=cp1252`.

### C11 — new: `tools/jira/run_census.py` (133 lines)

The six pipeline steps in dependency order, stopping at the first failure and **ending with
`validate_analysis.py`, whose exit code it inherits**. Every step shells out to the script that already
owns it, so there is no second copy of the logic. Offline by default; `--live`, `--project`, `--dry-run`.

The hazard it removes is specific: regenerating a report leaves the `.docx`, the `.xlsx` and the client
pack describing the previous edition. Nothing looks wrong — the files open, they are formatted, the
numbers are plausible — they simply describe a report that no longer exists. **That is the state this
workspace was found in**, and the validator caught it the moment it was written.

### C12 — provenance in every report

`pamit_fmt.snapshot_provenance()` adds a `**Source snapshot:**` header line naming the snapshot file and a
16-hex sha256 of its bytes. Validator check `B0` recomputes it and runs **first**, because if the report
was not built from that snapshot then every comparison after it is measuring two unrelated things.
Previously the only thing linking a figure to its data was a wall-clock timestamp, which says nothing
about *which* snapshot was underneath.

### C13 — documentation

| File | Change |
|---|---|
| `tools/jira/README.md` | **New.** The operator's guide: the one-command form, the step-by-step form, what writes what, modules vs entry points, which files this copy owns, and a troubleshooting table keyed by exact error text |
| `CLAUDE.md` | The two "live defects" are now recorded as fixed, with the third added. New commands, corrected `requirements.txt` note, `pamit_fmt.py` recorded as a newly-diverged tenth file, measured-facts table updated with milestone and fix-version coverage |
| `AGENTS.md` | Same corrections. Also fixed `md_to_docx_xlsx.py` being listed **without its required argument** — the exact error `CLAUDE.md` warns about |
| `docs/analysis/README.md` | Corrected the CI sub-task figure it carried (4,241 → 1,443) and documented the validation step |
| `docs/history/04-narrative-log.md` | Appended the account, per the append-only convention |

---

## D. Industry-standard improvements, by category

| Category | What landed |
|---|---|
| **Correctness** | Four defects fixed (C1, C2, C3, C6), each verified by an independent recount rather than by re-running the code that produced it |
| **Reliability** | `--offline` can no longer become a live fetch (C4); exit codes propagate (C5); the pipeline stops at the first failure and says which outputs are now mixed |
| **Data integrity** | Snapshot integrity checks; both stated identities (`Total = Open + Closed + Unmapped`, `Client + Internal = Total`) asserted every run; unmapped never guessed into a bucket |
| **Validation** | An independent validator that does not share code with what it validates; **proven to fail** against the pre-fix reports and against six crafted defects via `--self-test` |
| **Reproducibility** | Determinism measured — two consecutive runs are byte-identical outside the two timestamp lines. Source-snapshot digest in every report, recomputed on validation. `.docx`/`.xlsx`/pack freshness enforced rather than assumed |
| **Code quality** | One shared `multi_counter()` where three near-identical loops had drifted apart; dead code removed after AST proof; unused imports dropped |
| **Maintainability** | Per-project config in one `PROJECTS` table — a third project is a row, not a branch; every new module documents *why* it exists, matching the house style |
| **Usability** | One command for the whole pipeline; a preflight that answers environmental questions in one screen; error messages that name the path and the next action; ASCII-safe output on legacy codepages |
| **Operational readiness** | `--json` on both new tools for a scheduled check; documented exit codes (0/1/2); `--dry-run`; a troubleshooting table keyed by exact error text |
| **Documentation** | An operator's guide that did not exist; three authoritative files corrected where they now misdescribe reality |

---

## E. Validation results

| What | Method | Result |
|---|---|---|
| PAMIT milestone fix | Independent recount from raw snapshot | ✅ 4,523/5,740 (78.8%), 4,615 assignments, 101 values — report matches exactly |
| CI sub-task fix | `issuetype.subtask` vs `issuetype.name`, independently | ✅ both give 1,443; 2,798 Epic children identified by type |
| §12 assignment unit | Recount excluding unpopulated | ✅ 4,615, and 4,138 shown + 477 hidden reconciles |
| Refactor is behaviour-neutral | Full report diff vs `HEAD` | ✅ exactly four hunks; §6 Components byte-identical |
| `--offline` guard | Hid each snapshot, ran both generators | ✅ exit 2, correct message, zero HTTP, snapshots restored |
| Pipeline failure path | Hid the CI snapshot, ran `run_census.py` | ✅ stopped at step 2, exit 1, stated that outputs are now mixed |
| Pipeline success path | `run_census.py`, full chain | ✅ 6 steps, ~47s, exit 0 |
| Determinism | Two consecutive runs, diffed | ✅ byte-identical outside the two timestamp lines, both projects |
| Validator catches real defects | Ran it against the pre-fix reports from `cea4352` | ✅ named the CI defect exactly (`+2798` / `-2798`) and the missing PAMIT coverage lines |
| Validator checks can fail | `--self-test`, six crafted cases | ✅ each fires on its defect, each stays quiet on the corrected version |
| Console safety | `PYTHONIOENCODING=cp1252` | ✅ both new tools run clean |
| Full validation | `validate_analysis.py` | ✅ **57 PASS · 0 FAIL · 3 INFO** |
| Environment | `doctor.py` | ✅ READY |
| Every script compiles | `python -m py_compile tools/jira/*.py` | ✅ clean |
| Unused imports | AST audit of every touched file | ✅ none remain |
| Secrets still untracked | `git check-ignore` | ✅ `tools/jira/.env` still ignored |
| Relative links resolve | Link check across touched markdown | ✅ except one pre-existing, see §F4 |

**The three INFO rows are not failures and should not be made into any.** Two report calendar days with
zero tickets (36 CI, 14 PAMIT) — whether a given day is a genuine zero cannot be proven offline, and
`OBJ-030` confirmed several at source. The third records that 4,241 CI issues carry a parent while only
1,443 are sub-tasks, so the gap that caused C2 stays measured rather than forgotten.

---

## F. Remaining items

### F1 — `tools/rag/query.py` is broken, and the fix belongs upstream 🔒 *blocked by ownership*

`query.py:22` hardcodes `Path(__file__).parent / "corpus"` while `extract.py` writes to
`artifacts/rag-corpus/`, so the documented command raises `FileNotFoundError`. `OBJ-025` re-pointed the
writer and not the reader, and this is the one script that does not import `paths.py`. The fix is one
line — `from paths import RAG_CORPUS as CORPUS` — but `CLAUDE.md` records it as present in
`E:\Omkar\AI Projects\Dev Project` too and says to **raise it rather than patch this copy silently**.

**Decision needed:** may I apply the one-line fix here as well, accepting that the two copies then differ
until it is ported upstream — or should it stay broken here until you fix it in Dev Project?

### F2 — `OBJ-030`'s full ten-field record is still unwritten 🔒 *owner-governed*

`docs/history/README.md` §0 carries OBJ-030's summary row, but `01-objective-records.md` stops at
`OBJ-029`. `BLAST/Objective.md` still holds OBJ-030 as the active instruction. `CLAUDE.md` warns the
record is lost if `Objective.md` is overwritten before it is archived.

I did **not** write it, and did not touch `BLAST/Objective.md`. That file is the owner's active
instruction and `BLAST/CLAUDE.md` puts a Protocol 0 HALT in front of anything that treats it as an
intake. This review was a direct instruction, not a BLAST objective, so no `OBJ-NNN` was assigned; the
account went to the append-only narrative log instead.

**Decision needed:** should this review be registered as `OBJ-031` (the register's next ID), and would
you like me to draft OBJ-030's ten-field record for your review before it is appended?

### F3 — the seven files this copy does not own ⚠️ *left unchanged on purpose*

`pamit_analysis_rules.py`, `pamit_client_analysis.py`, `pamit_report.py`, `pamit_workbook.py`,
`jira_query.py`, `track_tickets.py` and `create_b01.py` are maintained in Dev Project and are 5–12 days
ahead there. I reviewed them and changed nothing. One observation worth passing upstream: the
`--offline` guard from C4 is the pattern `pamit_client_analysis.py` already uses correctly, so nothing is
owed in that direction.

⚠️ **One file did newly diverge:** `pamit_fmt.py` was byte-identical on both sides (measured) until
`snapshot_provenance()` was added here. It is a pure addition, so porting it upstream is a clean append.

### F4 — a broken link in six append-only history files ⚠️ *inference, not fact*

All six files under `docs/history/` open with **Part of [`../objective_original_origin.md`]**, and that
file does not exist anywhere in the tree. The intended target is almost certainly
`docs/history/README.md` — the index those files are sections of — but that is an inference, and these
files are append-only with an explicit "never reword" rule.

**Decision needed:** confirm the target and I will correct all six, or tell me to leave them.

### F5 — things intentionally left alone

| Item | Why |
|---|---|
| `docs/analysis/README.md` §1, §2, §6 | Self-documented as predating `OBJ-025` and unverified; referencing folders (`document/`, `questions/`, `Reports/`) that no longer exist. Rewriting it is a separate piece of work with its own scope. I corrected only the figure my own change invalidated |
| The `obj0NN_*` harness, `engage.py`, `control_center.py` | Cannot work in this copy by design. `doctor.py` now says so plainly instead of leaving it to be discovered |
| `CI-25546` | A characterised Jira search-index exception, 1 in 5,994. `OBJ-030` left its gate failing on purpose; I did not suppress it |
| The 315 "not a product defect" tickets and the `D38` denominators | Established methodology, deliberately not touched |
| `.claude/settings.json` | The assistant cannot edit it; both its hooks remain dead (hard-coded to a path that does not exist on this machine) |
| `21-09-2026/` living at the workspace root | The owner's explicit layout |

---

## G. Recommended next steps

1. **Review the two regenerated client deliverables before they go anywhere.** `21-09-2026/PAM/` and
   `21-09-2026/CI/` now carry materially different numbers — CI sub-tasks 4,241 → 1,443, and PAMIT gains
   a populated §12 where it previously read 100% `Not set`. **If the earlier pack was already sent to a
   client, those two figures were wrong in it** and that is worth a note to whoever received it.
2. **Commit.** The working tree holds 20 modified and 5 new paths, all verified. Nothing is staged.
3. **Answer F1, F2 and F4** — three short decisions, each unblocking a small piece of work.
4. **Run `validate_analysis.py` before circulating any future edition.** Better: run `run_census.py`,
   which cannot finish green without it.
5. **Port `snapshot_provenance()` and, if you want them, `validate_analysis.py` / `doctor.py` /
   `run_census.py` to Dev Project.** The validator is written against the census line, which does not
   exist there yet, but `doctor.py` and the provenance helper apply to both.
6. **Consider asking the product team to populate `Phase`.** Unchanged from `OBJ-029`, and still the
   highest-value single field-hygiene change available: it is the only thing standing between this
   analysis and defect-injection-phase reporting. `ReopenCount` is the same story.
7. **If this folder ever gains CI**, `run_census.py` and `validate_analysis.py --json` are the two
   commands to wire up. Both are offline, deterministic and exit non-zero on failure.
