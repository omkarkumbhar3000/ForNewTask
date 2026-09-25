# objective_original_origin.md — Master Instruction History

> **Append-only. Nothing in this file is ever deleted, reworded, or reordered.**
> It is the complete record of what was instructed, decided, observed and learned since Day 1.
> Active instructions live in [`BLAST/Objective.md`](BLAST/Objective.md) — this file is where they go to
> be remembered.

**Companion:** `BLAST/Objective.md` (current, dynamic) · **This file:** historical, permanent
**Started:** 2026-08-03, reconstructed from `workbench/archive/approach/instruction.md`,
`BLAST/progress.md`, `Reports/`, and the dated artefacts in the workspace
**Owner:** Sudesh Sawant · **Jira:** `PAMIT`

---

## How to append

Add a new `## <YYYY-MM-DD> — <title>` section at the **bottom**, under `§4 Running log`. Never edit an
existing entry; if something recorded here turns out to be wrong, add a new entry that says so and cite
the entry it corrects. Each entry carries whichever of these apply:

| Field | Meaning |
|---|---|
| **Instructed** | What the owner asked for, in their framing |
| **Decided** | A choice made, and by whom |
| **Done** | What was actually built or changed |
| **Learned** | Measured findings — figures, with where the evidence lives |
| **Corrected** | A previously stated fact that turned out to be wrong |
| **Open** | Left unresolved, and why |

When `BLAST/Objective.md` is rewritten, append its outgoing content here first. That is the only rule that
keeps the two files synchronised.

### Archiving an objective

Before `BLAST/Objective.md` is overwritten, add a record to **§0 Objective Register** using the next
sequential ID. Every record carries all ten fields — write `None` rather than omitting one:

`Objective ID` · `Title` · `Status` · `Summary` (2–5 lines) · `Key Deliverables` · `Related Files` ·
`Reason for Archiving` · `Pending Work` · `Lessons Learned / Observations` · `Dependencies`

**Status** is one of: `Completed` · `In Progress` · `Superseded` · `Cancelled`.

⛔ **No dates, timestamps or times in the narrative fields.** The sequential ID is the only ordering
needed — "archived after OBJ-003", never "archived on <date>". **Filesystem paths are exempt**: run
folders such as `Reports/Runs/2026-07-29_181439/` are identifiers, and stripping them would break the
traceability the register exists to provide. Cite them exactly.

If an objective was not finished, its record must state what was completed, what remains, why it stopped,
and whether it should be resumed. An objective spanning several sessions keeps its ID and has its
**Status** updated in place until it is archived — that in-place status edit is the one permitted
exception to the append-only rule.

---

## 0. Objective Register — audit log

Sequential, oldest first. **Next ID to assign: `OBJ-031`.**
✅ `OBJ-027` is now registered below, out of numerical order relative to `OBJ-028` because it ran concurrently and was archived later. It is recorded **`Superseded`, not `Completed`**: the Control Center half shipped, and three cleanup items — the `obj0NN_` script renames, the root `CLAUDE.md` auto-load budget (still 770 lines / 58 KB), and the `workbench/`+`Reports/` path audit — were measured outstanding when `OBJ-029` displaced it.
Backfilled from the narrative history in §1–§6; those sections remain the long-form record.

| ID | Title | Status |
|---|---|---|
| OBJ-001 | Automation framework optimization | ⬜ Superseded |
| OBJ-002 | Dynamic API validation — feasibility analysis | ✅ Completed |
| OBJ-003 | Auto-generated multi-hop API chaining + API graph | ✅ Completed |
| OBJ-004 | Developer loophole evidence packs and Jira tickets | 🟡 In Progress — 13 packs, 1 raised |
| OBJ-005 | Data sufficiency analysis | ✅ Completed |
| OBJ-006 | Objective management and workspace governance | 🟡 In Progress |
| OBJ-007 | Validation depth, mandatory-field evidence and the `document/` deliverable set | ✅ Completed |
| OBJ-008 | `questions/` — the project knowledge base | ✅ Completed *(living)* |
| OBJ-009 | Gold-standard business-context reference document | ✅ Completed |
| OBJ-010 | Full API suite re-execution and N-1 vs N execution benchmark | ✅ Completed |
| OBJ-011 | Portable onboarding kit — replicating the solution on a new project (`IDEV`) | ✅ Completed |
| OBJ-012 | Management presentation for the API Dynamic Data Generation Tool (`Prepare-1.pptx`) — tool since renamed **Dynamic API Validator**, see the amendment in `01-objective-records.md` | ✅ Completed |
| OBJ-013 | Closed-loop system keeping every file configured and current automatically (`v0.1`) | ✅ Completed |
| OBJ-014 | Developer repository (`pam/`) size investigation — 35.57 GB, evidence pack | ✅ Completed |
| OBJ-015 | Management Execution & Benchmark Dashboard — React app in `workbench/react/` | ✅ Completed |
| OBJ-016 | Daily pull-and-refresh job + runtime data for the dashboard | ✅ Completed |
| OBJ-017 | Weekly API execution, Sundays 10:00, + run-time N/N-1 resolution | ✅ Completed |
| OBJ-018 | k6 performance capability for the login journey — browser, API, and correlated bottleneck analysis | ✅ Completed *(built, never executed)* |
| OBJ-019 | Login + Sanity performance scope, live execution on `QA_MsSQL`, and the Performance React dashboard | 🟡 In Progress |
| OBJ-020 | Resume of the terminated Sunday API execution, the standing retry policy, and execution-reliability visibility on both dashboards | ✅ Completed — run `2026-08-16_100005` finished on the 6th supervised attempt: **747/747 flows, 5,382 executed, 3,422 passed (63.6%), 10/10 gates**, 840.8 min across 7 segments. Promoted to N. Three defects fixed en route: `obj017`'s three path-convention bugs (its resume had **never** worked), `obj010_build_workbook` applying a pinned run's elapsed to every later run, and the supervisor judging exit code instead of run artefacts |
| OBJ-021 | Professional performance-engineering capability: full 211-check sanity scope, correct session lifecycle, evidence-graded load model, baseline-relative gates, living documentation and detect-and-propose daily sync | 🟡 In Progress |
| OBJ-022 | Dependency-vulnerability remediation in the active automation `pom.xml`, and confirmation of the PAM submodule architecture that makes it the single source of truth | 🟡 In Progress — **remediation done and committed on `Dev` as `4d2d567`; 25 advisories → 1** (the survivor has no upstream fix). Open on owner actions only: push + submodule gitlink bump, `AutomationTesting/` deletion, the unverified CI scan target, and a suite run gated on a working credential. Narrative: §4 |
| OBJ-023 | Failure-reproducibility re-run — separate confirmed application failures from transient/environment-related ones by executing the full suite a second time and comparing hop-by-hop against `2026-08-16_100005` | ✅ Completed — scope agreed (all 747 flows, once, no regeneration), mechanics built and dry-run verified (`--no-generate`, supervisor `--fresh`). ⛔ **Execution blocked: `GenericScheduler` is locked** (`HTTP 400 "Your account has been locked"`, 2026-08-19 11:53). One attempt made, latched, not retried. This workspace issued only two `/arcontoken` calls in 48 h — 08-18 11:24 (success) and the locked one — every retry in between used a pinned token, so the lock did not originate from a retry loop here. Unblocks on an account unlock **or** a bearer token supplied as `$PAM_API_TOKEN`. **Unblocked** — the account was unlocked (the password was never rotated; the value the owner supplied is the one already committed in `QA_MsSQL.properties`), token minted on one attempt. Re-run `2026-08-19_133400` launched 13:33 and **stopped by the owner at 15:35 with 178 of 747 flows checkpointed** — a deliberate pause, not a failure; remaining 569 flows to be executed later. Resume point: `workbench/.weekly/OBJ-023-RESUME.md`. Comparison tool `obj023_reproducibility.py` is built and self-tested (run N vs itself → 100% reproducible, 5,396 hops, zero spurious drift) ⛔ **The pinned-token window has since elapsed** — the token's 24 h lifetime ran out during the pause, so resuming the remaining 569 flows now requires a fresh `/arcontoken` attempt on the shared `GenericScheduler` account. Full ten-field record: [`01-objective-records.md`](objective-history/01-objective-records.md) ⛔ **Closed by owner instruction under `OBJ-025`, not by executing the remaining 569 flows.** The paused re-run is explicitly **not** being resumed manually (`D29`): the standing `PAM-Weekly-API-Execution` schedule (Sundays 10:00) performs the next full execution, and reproducibility is to be assessed from that run against baseline `2026-08-16_100005` instead. This avoids the one thing that made the resume unsafe — a fresh `/arcontoken` attempt on the twice-locked shared `GenericScheduler` account outside the guarded weekly path. The partial run `Reports/Runs/2026-08-19_133400/` and its `checkpoint.json` are **retained as evidence**, and `obj023_reproducibility.py` remains built and self-tested for use against the scheduled run. |
| OBJ-024 | Consolidate the workspace into the `dynamic-api-validator` GitLab repository — version-control the unversioned work without duplicating the two repositories that already have remotes | ✅ Completed — Phase 1 inventory complete and Phase 2 snapshot verified (25,964 files, exact count match, zero `pam/` leakage). Approach agreed: **`git init` at the existing root** with `/pam/` and `/Automation gitlab repo/` ignored — zero file movement, so all 227 path references, 8 `parents[2]` resolutions, 3 rule globs and both scheduled tasks keep resolving. **Pushed.** Initial commit `736392e` (14,722 files) + `63bbff7` on `main` at `repo.arconnet.com/Omkar.Kumbhar/dynamic-api-validator.git`; LFS confirmed enabled server-side (4 objects, 294 MB) and the git pack compressed to 22.88 MiB. `v0.2` tagged locally on `63bbff7`. Owner decided to commit the AWS credential material as-is rather than redact. Remaining: push `63bbff7` + the `v0.2` tag, then clone-verify — `git push` is blocked inside the assistant session, so the owner runs it. Validation that the in-place approach worked: the `PAM-Dashboard-Daily-Refresh` task ran on schedule after `git init` and resolved every path ✅ **Now fully complete.** `main` verified 0 ahead / 0 behind `origin/main` at `3e295f2`, and the annotated `v0.2` tag is on the remote (`9833206` → `63bbff7`). The owner-run push and tag that this record listed as outstanding have both landed. |
| OBJ-025 | Workspace restructure to a compact, industry-standard architecture (`v0.3`) | 🟡 In Progress *(paused)* — owner asked for an end-to-end review of the whole implementation and granted explicit freedom to change, merge, rename and realign folders, targeting "robust, compact, simple, industry-standard" and "minimal, clean, easy to understand" while **maintaining all existing functionality and important data**. Starting point measured: 14,722 tracked files / 828.6 MB across 15 top-level entries, of which `Reports/` alone is 14,035 files (95% of the file count) and three directory names contain spaces. Constraints carried forward: `/pam/` and `/Automation gitlab repo/` are gitignored nested repos that cannot move (`D28`); Git-LFS pins `Graphify/pam-scope/graphify-out/graph.json` by literal path; `obj013_scan.py` `WRITE_ALLOWLIST` and `workbench/.drift/facts.json` bind documents by path; two Windows scheduled tasks invoke scripts by absolute path | ✅ **Completed — `v0.3` delivered.** 21 top-level entries → 12, in nine commits on `main` (`962af5d`…`912518c`), each independently revertible. Structure: `tools/` `docs/` `data/` `artifacts/` `state/` + root-pinned `CLAUDE.md`/`README.md`/`.claude/`/`BLAST/` + the two immovable checkouts. Both removable space-bearing names gone. **Zero data loss**: 14,727 tracked files against a 14,725 baseline, the difference being the two tools this objective added; 4 LFS objects with the 201 MB `graph.json` still a pointer; 13 run folders retained as direct children; longest path *down* from 171 to 162 chars. The measured basis for the sequencing (`D34`) held: 103 path bindings, 75 silent-breaking, and Phase 0 converted the 25 root resolvers to one marker-based `paths.py` **before** anything moved — at step 9 every script's depth changed from 2 to 1, and the old `parents[2]` would have resolved to `E:\Omkar\Automation`, above the workspace, writing 15 dashboard datasets outside the repository while printing success. Acceptance caught four further silent breaks that greps had missed (the drift loop measuring *nothing*; `obj015` computing 112.5 min instead of 840.8; a stale `.claude/rules` glob; 37 segmented path forms) and one four-week-old pre-existing break was repaired en route — `build_api_graph.py` had silently ignored 280 evidence files since the 2026-07-29 reorganisation. ⛔ **One owner action outstanding:** the `.claude/settings.json` `SessionStart` hook still names the old `obj013_loop.py` path and the assistant cannot edit that file. Previously: 🟡 In Progress — resumed. The owner reissued the restructure as the active instruction after `OBJ-026` completed, restating the same mandate (change / merge / rename / realign; robust, compact, simple, industry-standard) and reconfirming that the weekly PAM execution is closed and needs no manual resume (`D29`, `D32`). Nothing had been moved during the pause, so the resume starts from the preserved design rather than from an unwind. ⚠ Previously: ⏸ paused before any file moved — displaced in the active-instruction slot by `OBJ-026` under `D14`. Design work is preserved in the ten-field record; nothing is half-moved, so a resume starts from sign-off rather than from an unwind. Full record: [`01-objective-records.md`](objective-history/01-objective-records.md) |
| OBJ-026 | `engage` — one-word workspace readiness for DevProjects | ✅ Completed — a single entry point that inspects, synchronizes, analyses and prepares the workspace, then reports what changed, what needs attention and what to do next. Built as three modules plus a user-global skill: `engage_core.py` (pure discovery + policy + ordered decision table), `engage.py` (six-phase orchestrator), `engage_selftest.py` (**57 assertions, 0 failures** across 13 real git fixtures, 13 synthetic table rows and 11 safety guards), and `~/.claude/skills/engage/SKILL.md`. Reuse was real: `Journal`, `child_env()`, `make_output_safe()` and `FORBIDDEN` are imported from `obj016_daily_refresh.py`, whose refresh is **called** with `--skip-git` rather than reimplemented. Owner decisions `D30` (fast-forward pull permitted on both nested repos when clean — resolving a live `CLAUDE.md` contradiction) and `D31` (safe-by-default, the one departure from the deny-by-default convention). First real run fast-forwarded `Dev` +10 and `pam/` +12, re-derived 3-day-stale data, and surfaced that **the `2026-08-23` weekly execution never fired** — leaving the assumption behind `D29` unmet. Full ten-field record: [`01-objective-records.md`](objective-history/01-objective-records.md) |
| OBJ-028 | Client-raised PAMIT ticket analysis — build/release trend, current-window blind spots, open/unversioned defects and testing weak spots | ✅ Completed — a read-only Jira analysis engine producing five non-overlapping views and a dated daily summary, scheduled at 09:00. **Read-only is structural, not a promise**: `jira_query.ReadOnlyJira` whitelists GET on a fixed path list plus POST to the two search endpoints and refuses everything else, including `GET /transitions` — 16 guard assertions, 0 failures. Measured scope: **1,377** client tickets across **20** `35.8.29` versions; focus builds HF12/HF13(current)/HF14/HF15 hold **185** client / **120** defects; **429** client tickets in the last 30 days of which **334 (77.9%) carry no fix version**; Query C = **183** open unversioned client defects. Six defects were found and fixed in the analysis itself, each of which had produced a wrong answer: `_get` coerced a **list** body to `{}` so `/versions` reported 0 of 122 releases; ADF `description` read as `.get("value")` looked 0% populated across 201 issues; categorising on title+description put an SSH/MySQL/Mac defect in *Session Recording* because its description mentioned video; substring matching tagged "Login with SAML" as *Logging* (`log` ⊂ `login`) and then a word-boundary fix silently dropped plurals (`cipher` misses "ciphers"); a priority rule keyed on absolute counts, then on absolute ShowStopper counts, marked **every** testing area High — ShowStopper is not rare here (one area carries 45), so density replaced volume; and the scheduled task exited 1 in under a second, writing nothing, because `set PYTHONUTF8=1 && ...` captures the trailing space and Python rejects `"1 "` outright (*preconfig_init_utf8_mode: invalid PYTHONUTF8*). The taxonomy was **re-derived against the real corpus rather than the sample**: built from 82 HF12/HF13 tickets it left 33.3% of the build line uncategorised, so seven categories the data demanded were appended — first-match ordering means an append cannot re-label anything already classified — taking the current window to 8.6%. ⛔ **A clone edge is not recurrence**: cloning is how a fix is carried into a hotfix here, so 43 of 55 defects have clone ancestry by construction; only **23** whose clone family spans 2+ hotfixes are reported as cross-release. Owner decisions `D38`–`D41`. Deliverables: `tools/jira/jira_query.py`, `pamit_analysis_rules.py`, `pamit_client_analysis.py`, `pamit_report.py`, `pamit_fmt.py`, `register_client_analysis_task.ps1`; `docs/analysis/summary/summary_<date>.md` + `D1-client-ticket-patterns.md`; `artifacts/client-tickets/`; `state/client-analysis/`. Scheduled task **`PAM-Client-Ticket-Analysis`**, 09:00 daily, verified exit 0 |
| OBJ-027 | Close out the `v0.3` restructure, then build the DevProjects Control Center | 🟡 **Superseded** by `OBJ-029` — the build half delivered, three cleanup items measurably outstanding. **Delivered:** `tools/control_center.py` (the local decision server — `127.0.0.1` only, per-process in-memory token, a server-side `ACTIONS` table so the browser sends an action *type* and never a command string, three action types with anything else refused **by name**, zero product HTTP and no HTTP client at all) plus `tools/control-center/` (the third React + Vite app: four substantive views on real `engage` data and three honest stubs that state what data they need). Append-only `state/control-center/decisions.jsonl` + `executions.jsonl`, both tracked. Owner decisions `D36` (decision interface, never a security boundary) and `D37` (`not_interested` expires by itself — suppression keyed to a state fingerprint, reusing the drift loop's waiver mechanism). Four commits: `74d48ce`/`04a8217`/`3a8f37d`/`2a7fb69`. ⛔ **Outstanding, each measured against disk rather than inferred from the objective's own progress notes:** (1) the `obj0NN_` → role-based script renames never ran — `tools/` still holds `obj007_*` through `obj025_*`; (2) the auto-load budget was not reduced — root `CLAUDE.md` is **770 lines / 58,072 bytes** injected every prompt, against 15,925 bytes across the three path-scoped rule files, with the three largest sections still inline; (3) the path audit left **live wrong instructions** — `CLAUDE.md` still describes `workbench/` in the present tense and still sends the reader to `Reports/` from *step 6 of the standard workflow*, and neither directory exists, while the `.claude/rules` glob table advertises `Reports/**` (a trigger that can never fire) and omits the two real globs. ⚠️ The drift probe reports `docs.declared_paths_exist` **clean** across all of that, so the probe needs the fix as much as the prose does. Full ten-field record: [`01-objective-records.md`](01-objective-records.md) |
| OBJ-029 | Build-wise methodology correction (`Affected Milestone`), the three client-facing regression fields, and one consolidated ticket-level workbook | ✅ **Completed.** The owner asked which Jira field the build-wise analysis keyed on and whether the methodology was correct; it was **not**. Every build-wise count used `fixVersion` — where a fix *ships* — and was read as where a defect was *found*. Corrected to **`Affected Milestone` (`customfield_10092`, 97.3% populated)** and the conclusions move, not the decimals: build line **1,384 → 2,010** client tickets (+45%), **1,369** tickets carry the axis and *no fix version at all* (structurally invisible to the old query) against 38 the other way, heaviest build moves from `base` (262) to **`HF6` (399)** and **`HF1` (388)** with `base` only 69, and current build `HF13` falls from an apparent **27** client tickets to **2** — the 27 were *fixes scheduled into* HF13. Escape latency was the visible cost: `§7` reported **9** escapes recovered from build tokens clients typed into ticket titles; the field census measures **367** distinct defects escaping (**439** over all client tickets), and where both methods fire they agree exactly (`PAMIT-41274`, found HF1 / fixed HF12, +11 on each) — the heuristic was accurate, just blind. ⛔ **Root cause recorded so it cannot recur:** the previous revision checked the *native* `affectedVersion`, measured it 0% project-wide, concluded no field records the build a client was on, and built a title-parsing fallback — while a custom field held the fact on 97.3% of the population. ⚠️ **Three fields in this Jira are named `Affected Milestone`-something and two are 0% on PAMIT**, so selecting one returns an *empty build line that reads as a clean result*; the full audit of all ten milestone-shaped fields is `§0.2` and workbook sheet `10 Field Audit`. **All three owner-named fields verified present:** `Is reopen from customer` (`cf 10780`, 25.5%, already captured but never used in a view), `Functionality working in previous version` (`cf 11253`, 24.8% — **new**), `Previous working version` (`cf 11254`, 24.4% — **new**, of which **130 carry the literal string `None`**, a real option value that is not an empty field and must never be ordered as a version). Regression view: **506 of 2,010 (25.2%)** state any signal, **252 confirmed regressions** with a named previous working version, **47** customer re-opens — every figure quoted over the *populated subset*, because an `unstated` ticket is an unfilled field and not evidence of 'no regression'. ⛔ **`Milestone` is not a usable axis in PAMIT at all**: `Release Milestone.` is 9% and legacy, `Forward Merge Milestone` is 63% populated with **344 of 388 values the literal `None`**, and four more are 0%. Deliverables: `D1-client-ticket-patterns.md` regenerated **307 → 544 lines** with a new `§0` methodology, `§7.1`/`§7.2`, and `§15`–`§17` defining traceability, the workbook manifest and the derivation of every weak spot and scenario gap; **one** workbook `artifacts/workbooks/PAM-Client-Ticket-Analysis.xlsx` with **11 worksheets** (1.02 MB) — `01 Testing Weak Spots` at **693 ticket-level rows × 20 JIRA-oriented columns** each carrying a PAM-specific recommendation, `04 Ticket Details` at **2,169 tickets × 57 columns** as the source data, and `09 Count Reconciliation` restating every headline count as a **live `COUNTIFS` over sheet 04 with a `PASS`/`FAIL`**, so the workbook proves its own totals in Excel rather than asserting them; new `tools/jira/pamit_workbook.py` whose `verify()` gate exits non-zero if any pool or area count fails to reconcile. Verified: 693 weak-spot rows = the sum of the 15 area counts with **zero** per-area mismatch, pool columns reproduce 2,010 / 190 / 401 / 171 exactly, zero orphan tickets, zero cells over Excel's 32,767 limit. **Extended in the same session with owner items #8–#11.** ⛔ **#9 uncovered a second, larger instance of the `D42` error class:** the report claimed *"Jira holds no [root-cause] categorisation to cross-check against"* after measuring `cf 10113` (*Root Cause*, **0.2%**) and `cf 10199` (*Root cause*, **0.1%**) — while **`cf 10245` (*RCA*) is 80.7% populated (1,622 / 2,010) with 33 values in 15 families**, the most populated analytical field in the project, never once used. A 276-field sweep brought in **15 populated regression fields** in total (`RCA`, `RCA Details` 79.2%, `Fixed Date` 51.0%, `Reopen RCA` 7.3%, plus the reopen trail) and identified **`Phase` and `ReopenCount` as existing-but-0%**, making defect-injection phase and reopen count **not answerable** — refused rather than derived from the RCA family, because `Code - Logic Issue` says where a defect was *found in code*, not where it was *introduced*. **315 tickets are classified by the product team as not a product defect**, so a weak spot attributed to one is a false finding — reported, never silently applied (`D38` denominators stand). **#8**: the workbook now refreshes **in place inside the daily analysis run**, so the existing 09:00 task needed **no registration change**; history lives in the never-deleted dated snapshots with new sheet `12 Daily History` as a derived view showing day-over-day deltas and the 2026-08-30 gap. **#10**: the report carries **`Generated`** (when the data was captured) and **`Updated`** (when the file was written) as separate timestamps, which differ on any `--offline` re-render. Workbook now **13 sheets** (+`11 RCA Analysis`, +`12 Daily History`), ticket sheet **71 columns**. Two self-inflicted defects found and fixed on inspection: the Excel escape guard over-escaped `+`/`-`/`@` (openpyxl only promotes a leading `=`), putting a visible apostrophe on every negative delta; and a history column labelled *Build line* actually held the per-build sum (2,025) rather than the de-duplicated total (2,010). Owner decisions `D45`, `D46`. Full ten-field record: [`01-objective-records.md`](01-objective-records.md) |
| OBJ-030 | Extend both 2026 Jira census reports from 03 Sep to 21 Sep 2026 — PAMIT and CI, processed separately | ✅ **Completed.** PAMIT **5,431 → 5,740**, CI **5,588 → 5,994**; both `.md` + `.docx` + `.xlsx` delivered at `01Jan26-21Sep26`, section structure and sheet counts (26 / 21) identical to the editions they replace. ⛔ **One defect found and fixed that predates this objective:** JQL `created <= 'YYYY-MM-DD'` reads as `00:00` and excludes that entire day, so **every edition of both reports had silently omitted its own final date** — 24 PAMIT / 31 CI tickets missing from the 03 Sep edition, 44 / 38 recovered here. Both scripts now query the half-open `created < DATE_TO_EXCLUSIVE`, derive the output name from one `RANGE_SLUG` constant, sort with a stable `key ASC` tie-break, and raise `max_pages` to 200 (**CI had completed on page 60 of a 60-page runaway stop**). Historical drift quantified, not assumed: among the 5,431 pre-04-Sep PAMIT tickets status moved on **478 (8.8%)**, assignee 328, priority 3, resolution 0; CI 350 / 291 / 6 / 0 — the ticket *set* is unchanged, only field values. 11 validation gates per project pass, with one deliberate exception: **`CI-25546` is readable by `key =` and invisible to every bulk search** (one-day window returns 56 rows in a single page, server count agrees, neighbours present, absent even with no `ORDER BY`) — a **Jira search-index inconsistency**, 1 in 5,994 (0.017%), unrecoverable by any change here and recorded rather than suppressed. ⚠️ 21 Sep was the current date, so its final-day counts are a partial day and will grow on a later re-run — not drift. Narrative: §4. Previously: 🟡 In Progress — scope: update the analysis, **not** the methodology. Both reports measured **100% generated** (regenerating each from its own 03 Sep snapshot reproduced the on-disk file with 2 differing lines of 469 / 433, both the `Generated:` timestamp), so the extension is a `DATE_TO` bump and a re-run rather than a markdown edit. Owner decisions at intake: filenames move to `01Jan26-21Sep26` and the `03Sep26` set is **retired** (its JSON snapshots are retained, so it stays reproducible); the historical window is **fully re-fetched** — the report is a point-in-time census now taken on 21 Sep, so Jan–Sep tickets carry current status, and that drift is quantified rather than silent. ⚠️ Found at intake: `jira_analysis_2026.py` computes its output name from its date constants (`Jira_Analysis_20260101-20260903.md`) and **does not match the file on disk**, which had been renamed by hand — re-running it unchanged would have written a new file and left the intended deliverable stale |

---

### Where each section lives

The archive is split across files so no single file grows past the point where it can be read reliably in
one pass. **`§N` is the stable citation scheme** — it does not change when files are reorganised, so an
existing reference like "§6" stays valid; look it up here.

| § | Contents | File |
|---|---|---|
| §0 (summary) | Register table and next ID | **this file, above** |
| §0 (detail) | Full ten-field record per objective | [`objective-history/01-objective-records.md`](objective-history/01-objective-records.md) |
| §1–§2 | Founding instruction · standing constraints and when each was set | [`objective-history/02-origin-and-constraints.md`](objective-history/02-origin-and-constraints.md) |
| §3 | Owner decisions, D1 onward | [`objective-history/03-decisions.md`](objective-history/03-decisions.md) |
| §4 | Narrative running log — what was done, broke, learned | [`objective-history/04-narrative-log.md`](objective-history/04-narrative-log.md) |
| §5–§6 | Retired requirement detail · retired backlog | [`objective-history/05-archived-requirements.md`](objective-history/05-archived-requirements.md) |

**Adding content.** A new objective record goes in `01-objective-records.md` and its row in the table
above. A new decision goes in `03-decisions.md`. A narrative entry goes at the bottom of
`04-narrative-log.md`. **When any part passes ~600 lines, split it** — add `06-…`, `07-…` and list it here.
Nothing is ever deleted or moved out of the archive; only redistributed within it, and always recorded here.

---

## 7. Path translation — `OBJ-025` old → new

**Why this section exists.** The `OBJ-025` restructure moved most top-level folders. §0–§6 above and the
five numbered parts in this directory are **append-only**, so their existing citations were deliberately
**not rewritten** — rewriting history so it agrees with a later layout would falsify the audit log.

Use this map to resolve any path cited in an older record. A citation is correct *as written* for the
state of the workspace at the time it was made.

| Cited as (pre-`v0.3`) | Now at |
|---|---|
| `required-context/` | `docs/gaps/` |
| `objective-history/` | `docs/history/` |
| `objective_original_origin.md` | `docs/history/README.md` |
| `Company Documents/` | `data/sources/` |
| `document/reports/` | `docs/analysis/` |
| `document/BUSINESS-CONTEXT-*.md` | `docs/business-context/` |
| `document/README.md` | `docs/analysis/README.md` |
| `document/_AGENT-BRIEF.md` | `docs/history/archive/document-agent-brief.md` (retired) |
| `document/workbooks/` | `artifacts/workbooks/` |
| `document/data/` (8 authored) | `data/analysis/` |
| `document/data/` (10 generated) | `artifacts/analysis-data/` |
| `questions/data/` | `data/questions/` |
| `questions/*.xlsx` | `artifacts/workbooks/` |
| `questions/README.md`, `_AUTHORING-CONTRACT.md` | `docs/knowledge-base/` |
| `writer/writer.md` | `docs/management/writeup.md` |
| `writer/PPT/` | `artifacts/deck/` |
| `Developer-Loopholes/LH-*/`, `_TEMPLATE` | `artifacts/loopholes/` |
| `Developer-Loopholes/{README,PLAN,FINDINGS-SUMMARY-AND-PRIORITY}.md` | `docs/findings/` |
| `Developer Repository Issues/{README.md,findings.csv}` | `docs/findings/repository/` |
| `Developer Repository Issues/evidence/` | `artifacts/repo-issues/evidence/` |
| `Developer Repository Issues/regenerate-*.py` | `tools/analysis/` |
| `jira/` | `tools/jira/` |
| `Graphify/` | `artifacts/graph/` |
| `Graphify/README.md` | `docs/graph.md` |
| `Graphify/api-graph/build_api_graph.py` | `tools/build_api_graph.py` |
| `Reports/Runs/` | `artifacts/runs/` |
| `Reports/_archive-pre-2026-07-29/` | `artifacts/runs-archive/` |
| `Reports/Issues/` | `docs/findings/issues/` |
| `Reports/Summary/` | `docs/management/summary/` |
| `Reports/README.md` | `docs/runs.md` |
| `workbench/scripts/` | `tools/` (flat) |
| `workbench/scripts/flows/` | `artifacts/flows/` |
| `workbench/scripts/.obj010/` | `state/obj010/` |
| `workbench/rag/` | `tools/rag/` |
| `workbench/rag/corpus/` | `artifacts/rag-corpus/` |
| `workbench/react/` | `tools/dashboard/` |
| `workbench/react-performance/` | `tools/dashboard-performance/` |
| `workbench/onboarding/` | `tools/onboarding/` |
| `workbench/onboarding/profiles/` | `data/profiles/` |
| `workbench/skills/` | `docs/specs/` |
| `workbench/archive/` | `docs/history/archive/workbench-archive/` |
| `workbench/*.md` (6 briefs) | `docs/briefs/` |
| `workbench/.daily/` `.weekly/` `.drift/` `.perf/` `.engage/` | `state/daily/` `weekly/` `drift/` `perf/` `engage/` |

⚠️ This table is appended to as each step lands. It is the only sanctioned way to reconcile an
append-only citation with the current tree.
