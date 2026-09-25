# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## ⚡ Active instructions — read these first

**`BLAST/Objective.md` is the single source of active instruction.** The owner rewrites it whenever the
requirement changes, and a `UserPromptSubmit` hook injects its **current** contents on every prompt — so
you already have it, and an edit takes effect on the very next message.
**Where it conflicts with anything below, `Objective.md` wins** — this file is standing operating guidance,
`Objective.md` is what to do right now.

⛔ **Do not re-add an `@BLAST/Objective.md` import here.** It was removed under `OBJ-013`. An `@`-import is
resolved **once, at session start**, while the hook stays live — so the two paths delivered *two different
copies of the objective in the same context*, and the stale one was indistinguishable from the current one.
Measured directly: after `Objective.md` was rewritten mid-session, the import still served the superseded
objective while the hook served the new one. One live path beats two disagreeing ones. The drift loop
watches this (`governance.objective_single_injection`) and will report if the count ever leaves exactly 1.

Its permanent counterpart is `docs/history/README.md` (workspace root) — **append-only** history of
every instruction, decision and measurement since Day 1. Consult it when you need to know *why* something
is the way it is; append to it when a requirement changes or a run produces a durable finding. Never edit
its existing entries.

## 🔁 Standard workflow — follow this for every CLI interaction

**Established 2026-08-03. Applies to all future sessions unless the owner explicitly says otherwise.**

`BLAST/Objective.md` is the single source of truth for the current task. Record the instruction there
*before* building anything — never start implementation against a request that exists only in the chat.

| Step | Action |
|---:|---|
| 1 | Owner gives an instruction |
| 2 | **Write it into `BLAST/Objective.md` first**, replacing the `## Instruction` block. Append the outgoing objective to `docs/history/README.md` before overwriting — always, even if no work was done on it |
| 3 | Read it back and identify genuine ambiguities |
| 4 | If clarification is needed, **ask in MCQ form** (`AskUserQuestion`) before proceeding |
| 5 | Fold the answers into `BLAST/Objective.md` so the file matches what was agreed |
| 6 | Execute, using `BLAST/Objective.md` as the instruction and the workspace as context — `docs/history/README.md` for history, plus `docs/analysis/`, `artifacts/runs/`, the repo, `artifacts/graph/`, `tools/rag/` |
| 7 | On completion, update the affected documentation and reports, and **append what changed and what was learned** to `docs/history/README.md` |

**What triggers step 2.** Substantive task requests — build, analyse, fix, run, produce. **Not** questions
("is it done?"), conversational replies, or process/config changes like this workflow itself; writing those
into the file would overwrite a real objective with noise. A correction to the current task **amends** the
instruction already there rather than replacing it.

**Where a standing rule goes.** Process rules live *here*, in `CLAUDE.md` — not in `Objective.md`, which the
next instruction overwrites. If the owner states a durable way of working, record it in this file and log
the decision in `docs/history/README.md`.

**Do not** copy historical content into `Objective.md` (§Markdown conventions), and do not ask the owner to
restate anything the workspace already records — read it.

### Objective lifecycle — archive before overwriting

⛔ **Never overwrite `BLAST/Objective.md` without archiving first.** Step 2 above expands into this:

1. Read the outgoing objective out of `BLAST/Objective.md`.
2. Add a record to **§0 Objective Register** — the summary row goes in the index
   `docs/history/README.md`, the full record in `docs/history/01-objective-records.md`. Use the
   next sequential ID (the index states which). Ten fields, all mandatory — write `None`, never drop one:
   **Objective ID · Title · Status · Summary** (2–5 lines) **· Key Deliverables · Related Files · Reason
   for Archiving · Pending Work · Lessons Learned / Observations · Dependencies**.
3. Only then replace the `## Instruction` block with the new objective.

| Rule | Detail |
|---|---|
| **Status** | `Completed` · `In Progress` · `Superseded` · `Cancelled` |
| **⛔ No dates** | The sequential ID is the ordering. Never "archived on \<date\>" — say "superseded by OBJ-00N". **Exception: filesystem paths.** `artifacts/runs/2026-07-29_181439/` is an identifier; cite it exactly or traceability breaks |
| **Traceability** | Name the real artifacts — reports, workbooks, scripts, suite XMLs, graphs, Jira keys, ISSUE files, run folders. A record an auditor cannot follow has failed |
| **Unfinished work** | State what was completed, what remains, why it stopped, and whether to resume |
| **Multi-session** | An objective keeps its ID across sessions; update its **Status** in place until archived. That in-place edit is the *only* permitted exception to append-only |
| **Append-only** | Never delete, reword or reorder an existing record |

The register is the audit log; §1–§6 of that file remain the long-form narrative behind it.

## What this workspace is

This directory is the **root of the `dynamic-api-validator` repository** (`main`, push allowed — `D28`),
and it also *contains* two unrelated nested checkouts that are gitignored from it. **Three repositories are
in play; establish which one you are in before any remote operation** (§Edit scope has the rights table).

⚠️ **Restructured to `v0.3` under `OBJ-025`.** The layout is now five drawers by *kind*, not by the
objective that created a thing. If you are following an older instruction that names `workbench/`,
`Reports/`, `document/`, `questions/`, `writer/`, `Graphify/`, `jira/`, `required-context/`,
`objective-history/`, `Company Documents/` or `Developer-Loopholes/`, **it is stale** — the complete
old→new map is `docs/history/README.md` §7. The append-only history deliberately still cites the old
paths; that map is how you resolve them.

| Path | What it is | Versioned |
|---|---|---|
| `tools/` | **Everything executable.** The flat Python harness (`chain_runner.py`, the `obj0NN_*` pipeline, `engage.py`, `token_guard.py`, `paths.py`) plus `jira/` (Jira client) · `rag/` (`extract.py`, `query.py`) · `onboarding/` (the portable new-project kit, `OBJ-011`) · `analysis/` (one-shot regenerators) · `dashboard/` + `dashboard-performance/` + `control-center/` (React + Vite; `npm run dev`) · `control_center.py` (the Control Center's local decision server, `OBJ-027` — see §`engage`). **`paths.py` is the single re-point site** — every script gets the workspace root from it, by marker, never by counting parents | ✅ |
| `docs/` | **Everything a human reads.** `analysis/` (**10** reports — `A1`–`A7`, `B`, `C`, plus `D1-client-ticket-patterns.md` from `OBJ-028`/`OBJ-029` — and `README.md` + `summary.md`) · `business-context/` (`BUSINESS-CONTEXT-DEMO.md` ⭐ for a live demo, and the full `-STANDARD.md`) · `findings/` (the 13 loophole write-ups, `issues/` = the 12 authored `ISSUE-*.md`, `repository/` = the `pam` repo-size investigation) · `briefs/` (six reader-specific briefs, one per reader; `developer-loopholes.md` is the findings brief) · `history/` (**append-only** register + narrative; its `README.md` is the index and holds the `OBJ-025` path map) · `gaps/` · `knowledge-base/` · `management/` (`writeup.md` + `summary/`) · `specs/` (`*.SKILL.md`) · `graph.md` · `runs.md` | ✅ |
| `data/` | **Authored machine-readable input.** `sources/` (the 3 vendor PDFs via LFS + the Swagger link CSV) · `analysis/` (the 8 hand-maintained analysis JSON) · `questions/` (the knowledge-base source) · `profiles/` (onboarding profiles) | ✅ |
| `artifacts/` | **Everything a tool produced.** `runs/` (13 execution folders, `YYYY-MM-DD_HHMMSS`, **direct children, retained, never deleted**) · `runs-archive/` · `analysis-data/` (the 10 generated analysis JSON) · `workbooks/` + `deck/` (the two Excel workbooks and (the 8-slide management deck, `OBJ-012`)) · `loopholes/` (`LH-01`…`LH-13` packs — **generated, never hand-edited**) · `repo-issues/` · `client-tickets/` (the dated PAMIT capture series, `OBJ-028`) · `graph/` (`pam-scope/`, `api-graph/`, `dev-scope/`) · `rag-corpus/` · `flows/` | ✅ |
| `state/` | Job state and audit logs — `daily/` `weekly/` `drift/` `perf/` `obj010/` `client-analysis/` `control-center/` tracked **on purpose** (they are the only evidence an unattended job ran); `engage/` gitignored (per-invocation, regenerable) | ✅ mostly |
| `BLAST/` | The requirement intake framework — `Objective.md` (**auto-loaded every prompt**) + `B.L.A.S.T.md`. **Has its own `CLAUDE.md` and protocol** — read them before touching it | ✅ |
| `Automation gitlab repo/pam_automation_bootstrap/` | QA automation framework — Playwright + Java 21 + TestNG + Maven. **The only editable product code**, branch `Dev` (`D25`) | ⛔ own repo, gitignored here |
| `pam/` | ARCON PAM product source (.NET) under `pam/PAM/`, plus `pam/Automation/` (the automation repo as an **uninitialised submodule**) and ⛔ `pam/AutomationTesting/` (legacy hand-copy, part of no build) | ⛔ own repo, gitignored here |

⚠️ **The `Versioned` column used to read "not versioned" for twelve of these rows. Every one of them was
measured tracked** — the claim predated `OBJ-024` and was never corrected. `git restore <path>` recovers a
bad write anywhere except the gitignored token files.


`docs/briefs/` holds six briefs, each written for a different reader: `overview.md` (the demo
document) · `developer-loopholes.md` (**source of truth for the 13 findings**) · `document-gap.md` (for the
documentation team) · `new-project-implementation.md` (**how to onboard a new project** — `OBJ-011`: the
onboarding workflow, both architecture approaches, the comparison and the recommendation. Its executable
half is `tools/onboarding/`) · `self-understanding.md` (plain-language personal reference) · `README.md`.

**The findings pipeline runs across three folders — know which stage you are in.** A finding is stated once
in `docs/briefs/developer-loopholes.md`, packaged per-finding into `artifacts/loopholes/LH-NN-*/`, and raised
from `tools/jira/`. `docs/findings/issues/` is a parallel track, not a predecessor: same defects, internal-analysis
audience. Where a loophole and an issue overlap, **cross-reference rather than restate**.

**Path convention:** documents inside a drawer refer to their siblings by short path because they are
siblings (`docs/briefs/README.md` → `overview.md`). Documents *outside* it — this file, the root
`README.md`, the automation repo's `AGENTS.md` — use the full path from the workspace root
(`docs/briefs/overview.md`).

Two nested guidance files own detail this one deliberately does not repeat:

- **`pam_automation_bootstrap/AGENTS.md`** — the repo's own reference: Graphify commands and automation,
  suite inventory, package layout, listeners, Jenkins pipeline. It defers workspace-level topics (edit
  scope, `JAVA_HOME`, the response envelope, the `docs/` document set) back up to this file. Keep
  that split when editing either. **It is imported by `pam_automation_bootstrap/CLAUDE.md` (`@AGENTS.md`),
  so it loads automatically once you open a file in that repo** — Claude Code does not read `AGENTS.md` on
  its own. `.claude/rules/automation-repo.md` carries only the handful of things `AGENTS.md` omits.
- **`BLAST/CLAUDE.md`** — a different protocol entirely, including a hard "Protocol 0 HALT" that forbids
  writing code before a discovery checkpoint.

## ⛔ Edit scope

### 🔑 Three repositories, three different rights — owner decisions `D28` and `D47`

There are now **three** git repositories in play, and the push rule is neither uniform nor even
two-valued. Establish which one you are in before any remote operation.

| Repository | Location | Pull | Automatic push | Manual push |
|---|---|:--:|:--:|:--:|
| **`dynamic-api-validator`** — this workspace, `OBJ-024` | workspace **root** (`main`) | ✅ | ✅ **allowed** | ✅ **allowed** |
| **PAM Bootstrap Automation** — QA automation | `Automation gitlab repo/pam_automation_bootstrap/` (`Dev`) | ✅ | ⛔ **never** | ✅ **explicit instruction only** (`D47`) |
| **PAM** — developer/product repo | `pam/` (`35.8.29_Hotfix`) | ✅ | ⛔ **never** | ⛔ **never** |

Pull the latest code from the two nested repos freely — that is explicitly permitted, and it is the
supported way to pick up upstream changes.

⚠️ **`D47` narrowed the bootstrap rule from "never push" to "never push *automatically*" — read the
distinction precisely, because the two halves are enforced by different things.**

| | Means |
|---|---|
| **Manual push — permitted** | You may run `git push` against `pam_automation_bootstrap` on branch `Dev` **when the owner tells you to in that turn**. `/go-go-go` is usable there when the owner points it at that repo. |
| **Automatic push — never** | ⛔ Never on your own initiative, never as the closing step of a task, never from a scheduled job or harness script, never because a run "looks finished". A commit on `Dev` is still where your work ends unless a push was asked for. |

⛔ **A push you were not asked for is the failure mode this rule exists to prevent.** "The task is done
and there are unpushed commits" is **not** an instruction to push. Ask, or leave it committed and say so.

✅ **`pam/` remains blocked mechanically, not merely by instruction.** It carries
`remote.origin.pushurl = DISABLED-push-blocked-per-D28` in its **local** `.git/config`, so any push to it
fails before touching the network — for anyone: an agent, a script, or a scheduled job. The bootstrap
repo's block was **removed under `D47`** (`git config --unset remote.origin.pushurl`); verified after the
change that its fetch URL was untouched, `ls-remote` still resolves, and the tree was clean. Re-apply the
block with `git -C <repo> config remote.origin.pushurl DISABLED-push-blocked-per-D28`.

✅ **Automatic push stays impossible structurally, and that is what makes `D47` safe.** `push` is in
`obj016_daily_refresh.FORBIDDEN` and absent from `engage_core.ALLOWED`, so **no** scheduled job, harness
script, `engage` run or Control Center action can emit a `git push` for **any** repository — including
the workspace one. Removing a pushurl does not change that; the ban sits upstream of it, and
`engage_selftest.py` asserts it (`guard: git push refused`).

⚠️ **A `git push` failure in `pam/` is therefore expected, not a fault.** The error reads
*"'DISABLED-push-blocked-per-D28' does not appear to be a git repository"*. Do not "fix" it by restoring
the push URL — that is the guard doing its job. And do not attempt to re-point it: changing a remote URL
is denied in `.claude/settings.json` and blocked by the classifier.

⚠️ **"Never push, never merge" below now refers to `pam/` only, and to *merging* everywhere.** It
predates both the workspace repository and `D47`, and must not be read as forbidding a push to
`dynamic-api-validator`, nor an instructed manual push to the bootstrap repo. **`merge` is unchanged and
still never yours** — in any of the three.

⛔ **`.claude/settings.json` enforces this and the assistant cannot edit it.** The classifier blocks an
agent from widening its own permissions, by design — so if a push is denied, the fix is an owner edit to
that file, never a workaround. Do not attempt one. Note `deny` beats `allow`, and rules match **command
text, not the target repository**: a prefix rule such as `Bash(git push:*)` only matches when the command
*starts* with `git`, so `cd pam && git push` is not covered by it. That is a side effect of prefix
matching, not a guarantee — the working directory persists between tool calls, so **confirm your cwd
before any push.**

**Write only inside `Automation gitlab repo/pam_automation_bootstrap/`, on branch `Dev`.**

⚠️ **The branch changed from `AI` to `Dev` — owner decision `D25`.** Two measured reasons: `AI` holds **no
unique commits** (`git rev-list --left-right --count AI...Dev` returns `0 2`), so it had become a stale
point on `Dev` rather than a working branch; and the PAM submodule gitlink tracks `Dev`, so anything
landing on `AI` could never reach the submodule pointer. Ignore the older "develop on `AI`" wording
wherever it still appears — including `docs/history/archive/workbench-archive/approach/instruction.md` item 8, which is frozen
and must not be edited.

`pam/` is reference-only. Read it freely for context; never modify it, never commit there, and leave it
with a clean `git status`. It is the developer's product repo — automation commits landing there mix test
code into the product build.

⛔ **`pam/AutomationTesting/` is being deleted — never edit it, and never treat it as the active build.**
It is a hand-copy with no git link to the bootstrap repo, and it is **not part of any build**: there is no
Maven step in `pam/jenkins-pipeline` and no reference in `pam/.gitlab-ci.yml`. Only a dependency scanner
sees it, which is why an SCA report can name `AutomationTesting/pom.xml` while the file that actually
builds is `pam_automation_bootstrap/pom.xml`. **Measured proof that editing the copy does not work:**
`pam` commit `0520b6b79` remediated six vulnerable dependencies there, and commit `e278fd399` ("added
automation code") bulk-copied the bootstrap tree over it and reverted every one, line for line. Fix the
source of truth, never the copy.

**The release path is: develop on `Dev` → owner reviews → push → owner bumps the submodule gitlink in
`pam`.** ⚠️ **`D47` changed who may perform step 3, and nothing else.** The push may now be run
manually, by you, on the owner's explicit instruction — it is no longer owner-only. The review still
precedes the push, the gitlink bump is still the owner's, and **`merge` is still never yours**.

⚠️ **Committing on `Dev` needs one check first.** Local `Dev` can sit behind `origin/Dev`
(`git rev-list --left-right --count Dev...origin/Dev`). ✅ **A `--ff-only` pull to fix that is now
permitted (`D30`)** — this line previously said "do **not** pull", which contradicted `D28` and §Edit
scope's own **Pull ✅** column. The permission is bounded: fast-forward only, and only when the tree is
clean, so it can neither create a merge commit nor run against uncommitted work. **A diverged branch is
still never reconciled automatically** — that needs a rebase or a merge, and both are the owner's call.
If you would rather not pull, the old route still works: confirm the incoming commits do not touch the
files you are about to change (`git diff --stat Dev origin/Dev -- <path>`), commit, and tell the owner.

⚠️ **`AI` is no longer local-only — this file said otherwise until `OBJ-026`.** Measured:
`git branch -vv` reports `AI  7be00b3 [origin/Dev: behind 31]` — a count that grows with every commit on
`Dev`, so re-measure rather than quoting this line — so it *does* have an upstream, and it is
`origin/Dev` rather than a branch of its own. There is still **no `origin/AI`**; the only remote branch is
`origin/Dev`. Develop on `Dev` (`D25`) and treat `AI` as the stale point it is.

### The PAM submodule — the architecture that makes this repo the source of truth

`pam` embeds this repo as a git submodule at **`pam/Automation/`** (not `pam-automation-bootstrap-submodule/`).
`.gitmodules` is committed and pushed. Three things to know:

| Fact | Consequence |
|---|---|
| The submodule is **registered but uninitialised** — `git submodule status` returns a leading `-`, `pam/Automation/` is an **empty directory** | A plain `git clone` of `pam` gets no automation code. `git submodule update --init` is required, and CI needs `GIT_SUBMODULE_STRATEGY` |
| The gitlink **pins one commit** and does not follow the branch | A commit on `Dev` is **not** visible in `pam` until the owner bumps the gitlink. Never say a fix "reached PAM" on the strength of a bootstrap commit alone |
| `pam/.gitlab-ci.yml` is a one-line include of `Dhruvin.Chawda/claude_code_pipeline` → `base_pipeline.yml`, **unreadable from this workspace**, and this repo has **no `.gitlab-ci.yml` of its own** | Where the SCA scan actually looks is **unverified**. If submodules are not cloned, deleting `AutomationTesting/` yields a **false all-clear** rather than a fix. Report this; do not guess it |

Full rules: `BLAST/Objective.md` (§Constraints). The original standing instruction is archived at
`docs/history/archive/workbench-archive/approach/instruction.md` — frozen. ⚠️ **Its item 8 names branch `AI` and is now
superseded by `D25`; the archive is append-only, so it stays as written. This section is authoritative.**

## The BLAST workflow — how requirements enter this workspace

`BLAST/` is how the owner states new requirements. **`BLAST/Objective.md` is a dynamic blueprint, not a
fixed spec:** the owner rewrites it whenever the requirement changes. Expect its contents to differ
completely between sessions. Since 2026-08-03 it is **auto-loaded** (§Active instructions above), so you
already have its current contents at the top of every turn.

⚠️ **It is deliberately small — keep it that way.** It holds the active instruction and nothing else.
Do not write history, findings, run results, or a task backlog into it; do not restate context that
already exists elsewhere in the workspace. Two consequences that matter:

- **Fill the gaps yourself.** The owner will not repeat what the project already records. Read the rest of
  the workspace — this file, `docs/history/README.md`, `docs/analysis/`, the repo — before asking.
- **Append, never copy back.** When the instruction changes or a run produces a durable finding, append it
  to `docs/history/README.md`. Never move historical content into `Objective.md`.

Size is functional, not cosmetic: at ~16 KB the file exceeded the hook's inline-injection limit and was
spilled to a side file with only a preview in context. Under that limit the whole thing lands every turn.

**Trigger.** A run is invoked with a prompt of the form:

> Run `Objective.md` by referring to `blast.md`, and give me the output.

`blast.md` means `BLAST/B.L.A.S.T.md`. That is a request to execute the whole protocol — Blueprint → Link →
Architect → Stylize → Trigger, starting at Protocol 0. Read both files in full before acting;
`B.L.A.S.T.md` assigns you the "System Pilot" role and constrains what you may do and when.

**Protocol 0 still halts, and the dynamic objective makes it matter more.** You are forbidden from writing
tools until the five Discovery questions are answered by the owner, the JSON data schema is in `LLM.md`, and
`task_plan.md` holds an approved Blueprint. Confirming your reading of an objective that already answers a
question is fine; skipping the checkpoint is not. Because the objective is rewritten between runs, a new one
can silently contradict the previous run's schema — the checkpoint is what catches that.

**Where output goes.** The objective changes, so the target is confirmed during Blueprint rather than fixed
here. The boundaries are fixed:

| Destination | Rule |
|---|---|
| `pam_automation_bootstrap/` on `Dev` | **The deliverable.** Java 21 / Playwright / TestNG code, suite XMLs, Excel test data. |
| `BLAST/` | **Working space.** Protocol memory (`LLM.md`, `task_plan.md`, `findings.md`, `progress.md`), `architecture/` SOPs, `tools/` generators, `.tmp/` intermediates. Not a git repo — writes here touch no history. |
| `pam/` | **Never.** Reference data only; leave `git status` clean. |

**Per-run state.** Since `Objective.md` is overwritten, BLAST's memory files can carry state belonging to a
previous, unrelated objective. At Protocol 0, establish whether the run is a new objective or a continuation
of the last one. If new: treat the `LLM.md` schema and `task_plan.md` phases as stale and re-derive them;
keep `progress.md` append-only so the history of past runs survives.

**Precedence.** BLAST calls `LLM.md` "law". Within this workspace, this file outranks it:

| Where they conflict | Resolution |
|---|---|
| Phase 5 wants a cloud deploy plus cron/webhook triggers, and calls a project incomplete until the payload lands there | You never merge, and a run **ends committed on `Dev`** (`D25`) — finishing a run is never itself a reason to push (`D47`). A manual push is a separate, explicitly instructed act; the owner bumps the `pam` submodule gitlink. The "trigger" here is the Jenkins pipeline (`jenkins.properties`) plus a suite XML, not a cloud cron. Say plainly that the run is complete at that boundary. |
| Phase 3 lets Layer 3 pick any language | Anything landing in the automation repo is Java 21 + Playwright + TestNG. Only generators kept in `BLAST/tools/` may be JS or Python. |
| Any generated assertion | The response-envelope rule below is absolute — never a status-only check. |

Record any such deviation in `LLM.md` so the next run inherits it.

## Build and test

### Fix `JAVA_HOME` first — every session

System `JAVA_HOME` points at `C:\Program Files\Java\jdk-26.0.1`, **which does not exist** (the installed
Java 26 is now `jdk-26.0.2`, so the stale path did not self-heal). `pom.xml` requires Java 21. Maven fails
with *"The JAVA_HOME environment variable is not defined correctly"* until you override it:

```powershell
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-21.0.12.8-hotspot"
```

⚠️ **The path is `21.0.12.8`, not `21.0.11.10`.** This file said `21.0.11.10` until `OBJ-022`; that
directory does not exist, so following the old instruction produced the *same* failure it was written to
prevent. Verify before trusting either value:

```powershell
Get-ChildItem "C:\Program Files\Eclipse Adoptium" | Select-Object -ExpandProperty Name
```

`java` on `PATH` is now the Adoptium **21** build, not 26 — so a bare `java` works while `mvn` still
fails, because Maven reads `JAVA_HOME` rather than `PATH`.

`mvn` resolves on the **PowerShell** `PATH` only, not in Bash. Use the PowerShell tool for Maven.

### Running suites

Execution is entirely Surefire + TestNG XML — there are no Maven profiles, no runner classes, and no
shell scripts.

```powershell
mvn clean test                                              # default: CICD_Suites/Demo.xml, env QA_MsSQL, chrome
mvn clean test -Denv=CICD -DsuiteFile=CICD_Suites/APISuite.xml
mvn clean test -DsuiteFile=API_Suites/Positive_All/<Module>.xml   # one API module (71 such files)
mvn -o clean test-compile -DskipTests                       # compile-only check
```

Add `-Dmaven.test.failure.ignore=true` when you need the reports written even though tests fail — that is
what Jenkins passes.

| Flag | Overrides |
|---|---|
| `-Denv` | Which `Environments/<env>.properties` loads (20 available) |
| `-DsuiteFile` | TestNG suite XML — default `CICD_Suites/Demo.xml` |
| `-DbrowserType` | `chrome` · `chromium` · `firefox` · `safari` · `edge` |
| `-DurlFromCmd` | `environmentUrl` from the env properties |

### Running a single test

```powershell
mvn clean test -Dtest=ActivityLogs
mvn clean test -Dtest=ActivityLogs#activityLogs
```

⚠️ `-Dtest` **overrides `suiteXmlFiles` entirely**, so the suite's `<listeners>` never register. For API
tests that means `TestListener` does not run, so `APIExcelReportUtil` is never initialised or saved and no
Excel report is produced. Use a suite XML when you need the report.

### Config resolution order

`Env_configs/Automation.Properties` (master switches) → `Environments/<env>.properties` (URLs,
credentials, DB, timeouts) → `-D` flags win over both. Surfaced as `public static` fields on
`com.arcon.autoconfigs.AutoConfigs`. Credentials are committed in plaintext across all 20 env files.

## Architecture

Detail is path-scoped so it loads only where it applies — see `.claude/rules/`:

| Rule file | Loads when you open | Covers |
|---|---|---|
| `automation-repo.md` | `Automation gitlab repo/**` · `**/pam_automation_bootstrap/**` · `pam/AutomationTesting/**` | `BaseTest`/`ApiHelper`, the Excel→report API data flow, two known defects, suite layout, config detail, code conventions, Graphify usage |
| `api-surface.md` | `**/APIConfig.java` · `tools/**` · `artifacts/loopholes/**` · `artifacts/runs/**` · `docs/findings/**` · `pam/PAM/**` | The 1,306 count and its basis, verb distribution, why the API is not in `pam/PAM`, the harness scripts, Swagger and payload sources |
| `markdown-docs.md` | `**/*.md` | "Update MD files", the one-fact-one-home layer table, house style |

Three things you need **before** opening any of those files, so they stay here:

- **`pam/PAM` is not the API under test** — only 48 of 1,306 endpoints (3.7%) exist there. Do not plan
  around parsing it.
- **Quote 1,306** as the endpoint count. `1,336` and `1,322` are wrong or stale.
- **`GET` + `POST` is 99.7% of the surface.** Deletion is `POST /api/<C>/Delete<Thing>`, so a destructive
  call looks like an ordinary POST — **guard on names, not verbs.**

## ⚠️ The response envelope

Most PAM endpoints return **HTTP 200 with an application-level `errorCode` in the body**. A rejected
request is usually a 200, not a 4xx.

Never write or generate an assertion that checks only `response.status() == 200` — it passes against a
fully rejected request. `ApiHelper.validateResponseErrorCode(...)` handles the envelope; negative cases
need both an `ExpectedStatus` (often `200`) and an `ExpectedErrorCode`.

Two traps when you go looking for it in `ApiHelper`:

- It is **`private`**, so tests never call it directly. The public entry point is
  `validateApiResponseWithResponseTime_ExcelBasedsettingnegative(...)`, which invokes it only when
  `expectedStatusCode == 200` — framework-level rejections (401/405) carry no envelope.
- A **superseded copy of both methods sits commented out immediately above the live ones**, so a grep for
  `validateResponseErrorCode` hits the dead block first. Check for a leading `//` before concluding
  anything about the behaviour. ⛔ **Never quote a line number here — measure it:**
  `grep -n "validateResponseErrorCode\|ExcelBasedsettingnegative" <ApiHelper.java>`. Last measured, the
  dead pair is at **1391**/**1426** and the live pair at **1500**/**1601** in a **1,794**-line file. Every
  previous version of this file quoted numbers that had already moved — 1282–1394/1397/1464, then
  1319/1432/1533, which was ~70 lines out by the time anyone read it. The **structure** is the durable
  fact: dead copy first, live copy below it. `obj013_loop.py check` re-derives this
  (`code.apihelper.dead_block_start`).

**Use `com.arcon.utils.validation` for anything new.** Since OBJ-007 the envelope logic lives there:
`PamEnvelope` normalises the shapes, `PamApiValidator` runs twelve layers, `ValidationReport` collects
them, `ErrorCodeRegistry` holds the codes, `DbPersistenceValidator` checks the database. `ApiHelper`'s
`validateResponseErrorCode` now delegates field access to `PamEnvelope`.

⛔ **Two measured facts about the old implementation, both worth knowing before trusting any green run
that predates OBJ-007:**

- It read **`node.has("success")` in camelCase, and Jackson is case-sensitive.** Across all 1,868
  captured responses, lowercase `success` appears in **0** and PascalCase `Success` in **1,580** — so the
  method's first assertion failed on every response this API can produce. Every negative case reaching it
  failed for the wrong reason.
- Recognised codes were hardcoded as `KNOWN_ERROR_CODES = {"201","202","203"}` and asserted hard, so the
  real, measured `ErrorCode: "206-LC_GLD"` (HTTP 200, `POST /api/Logs/GetLogDetails`) would have been
  reported as a broken test. `ErrorCodeRegistry` now matches on the numeric prefix and records an
  unrecognised code as an observation — the defect is the missing product registry, not the response.

### Response shapes — **31 distinct**, measured across all 1,868 captured calls

⚠️ **This section used to say "four". A full census under OBJ-007 counted 31 distinct top-level shapes,
of which only 6 match a documented one.** The exemplars below are the ones worth memorising, but treat the
list as illustrative, not exhaustive — the whole census is `artifacts/analysis-data/envelope-shapes.json`.

What breaks a fixed-shape assertion, with counts: **127** calls are not JSON objects at all · **288**
carry no `Success` field · **139** of 1,291 `Result` values are not arrays (object, string, bool, int) ·
**2** bodies are a naked `true`/`false` · **291** lack the `Program`/`Version`/`DateTime` frame.

`PamEnvelope` exists to absorb all of this — all 8 of its `Shape` classes occur in the evidence, none is
speculative. The exemplars:

| Shape | Seen on |
|---|---|
| `{Program, Version, DateTime, Success, Message, Result[]}` | `GetAllActiveUserList`, most business endpoints |
| Same, but **no `Message` field** | `GetLOBList` |
| Same, but `Result` is an **object**, not an array | `GetServiceDetails` |
| **Bare array, no envelope at all** | `GET /api/DeviceOnboarding/GetLOBList` |
| Error form: `Success: false` + `ErrorCode` + `ErrorMessage`, still **HTTP 200** | `GetLogDetails` (missing param) |

⛔ **`Success: true` is not evidence of a write.** `POST /api/ServiceCreation/SetServiceDetails` returns
`Success: true` with `Message: "Already Exists"` when the record already exists — nothing was inserted, and
both the status code and the `Success` flag are green. A create assertion must check **`Message`
semantics**: `"Inserted Successfully"` means inserted, `"Already Exists"` means no-op.

### 🟢 Token generation WORKS again — `token_guard.py` owns the only call to it

⚠️ **This section previously said the account was locked and `/arcontoken` "no longer works". That is no
longer true, and the correction matters:** the account has been unlocked. Verified 2026-08-04 by a single
deliberate attempt — `POST /arcontoken` returned **HTTP 200** in 3,517 ms with an `access_token`
(`APIUserId: 2`, role `Default`, 24 h lifetime). The credentials in `Environments/QA_MsSQL.properties`
(`pam_APITokenUserName` / `pam_APITokenPassword`) are correct and unchanged — **the blocker was always the
lock, never the password.**

⛔ **The lockout risk has not gone away, and the rule that prevents it is unchanged.** `GenericScheduler`
is also the data-warehouse ETL service account, so a lockout reaches past testing. The 2026-07-28 lockout
was **not** caused by a wrong credential: the harness re-attempted `getToken()` **on every run by design**,
and accumulated failures tripped the lockout policy (`ISSUE-009` §4a). Retry-on-failure and account lockout
are fundamentally incompatible.

**`tools/token_guard.py` is now the single gate.** `chain_runner.get_token()` and
`run_qa_mssql.try_dynamic_token()` both delegate to it, so there is exactly one code path to `/arcontoken`:

```powershell
python tools\token_guard.py status        # report only, zero HTTP calls
python tools\token_guard.py refresh       # ONE attempt, only if the cache is expired
python tools\token_guard.py clear-latch   # human unblock, after fixing the cause
```

Resolution order is `$PAM_API_TOKEN` → valid cache → **one** live attempt. Setting the env var still
bypasses the endpoint entirely and is the safest option for an unattended run:

```powershell
$env:PAM_API_TOKEN = "<bearer token>"
```

| Rule | Why |
|---|---|
| **Never retry a failed token request** | A lockout deepens. Stop and report. `token_guard` enforces this — it does not rely on you remembering |
| **A failed attempt latches** | `.token_attempt_block.json` blocks every later attempt, in this run *and all future runs*, until a human clears it. Without this, "once per run" silently becomes "every run" — the original lockout |
| **Network faults latch too** | A timeout cannot be distinguished from a refused login, and guessing wrong costs an account |
| One token per run, cached to `tools/.token_cache.json` | Never schedule or loop token generation. No cron, no backoff |
| Do not blank `ApiToken=` in an env file | `ApiHelper.getToken()` (**two overloads** — last measured `ApiHelper.java:1006` 3-arg and `:1034` 2-arg; re-grep rather than trusting either) returns it verbatim **with no expiry check** and only calls `/arcontoken` when it is empty. Since `getToken()` runs per test, a blank value means **one token request per test** across a whole suite |

⚠️ **`ApiToken=` is not auto-renewed.** Once it expires, Java API tests fail on auth rather than
regenerating — a confusing failure mode that reads as a product defect. Refresh it from `token_guard`.

Full account history and the re-validation workflow: `docs/findings/README.md` §6, `ISSUE-009`.

### ⛔ Three endpoints take the whole API down — never call them

`GET /api/ActivityLogs/GetErrorLogs` and `GET /api/ActivityLogs/GetLogs` hang for 30 s and **stop the IIS
application pool**. Three sequential requests were enough to take the entire API to `503` with no recovery
without intervention — this was not a load test. `GetAllActiveUserDetails` is blocklisted for the same
reason. `ISSUE-010` has the decisive capture; `LH-08` puts **98 endpoints** at risk and its live
re-validation is **forbidden**, not merely skipped.

Enforce the blocklist **at planning time**, before a request is built. Two related traps:

- **Verb guards do not work on this API.** Deletion is `POST /api/<C>/Delete<Thing>` — guard on *names*.
- **Never replay a call that would mutate.** The harness expresses this as `replay_filter`; 35 rows across
  LH-02 and LH-09 are withheld for exactly this reason.

## Markdown conventions

Path-scoped to `**/*.md` — see `.claude/rules/markdown-docs.md` for "Update MD files", the
one-fact-one-home layer table, the frozen-archive rule and house style.

## 📄 Large files — never let size hide information

Reading a large file returns the **first 2,000 lines and no error**. Nothing tells you the rest exists, so
a truncated read looks exactly like a complete one. **Treat any file over ~1,500 lines as truncated until
proven otherwise** — check with `wc -l` before reading something unfamiliar.

| Lines | Approach |
|---:|---|
| < 1,500 | Read normally |
| 1,500 – 5,000 | Page with explicit `offset`/`limit`, or Grep straight to the section |
| > 5,000 | Never read linearly. `grep -n "^## "` for the section map, then read only those ranges |

**Never read these directly — a query layer already exists and reading the file is the wrong access path:**

| File | Lines | Use instead |
|---|---:|---|
| `artifacts/rag-corpus/pam-api.md` | 101,803 | `python tools\rag\query.py find "<terms>"` · `page <doc> <N>` |
| `artifacts/rag-corpus/pam-admin.md` · `client-manager.md` | 18,560 · 9,611 | same |
| `artifacts/graph/pam-scope/graphify-out/GRAPH_REPORT.md` | 13,313 | the `graphify` MCP tools |

⚠️ **`artifacts/runs/*/RUN_REPORT.md` is the live trap.** The `2026-07-29_181439` report is 8,566 lines and
its section **"5. Exclusions — nothing is silently skipped" begins at line 8,544.** A plain read stops
6,500 lines short of it and silently omits the one section recording what the run left out — the exact
failure this rule exists to prevent. Get the section map first, then read ranges.

**When authoring.** An archive that grows without bound gets an **index plus sequential parts**:
`docs/history/README.md` + `docs/history/NN-slug.md` is the working example. Rules for that
pattern — the index must list **every** part and what it holds, so nothing becomes undiscoverable; split a
part once it passes ~600 lines; and keep a **stable citation scheme** (`§N`) that survives reorganisation,
so existing cross-references never break. Auto-loaded files (`CLAUDE.md`, `BLAST/Objective.md`,
`.claude/rules/*`) are held to a stricter budget, because they are paid for on **every** turn rather than
when something is opened. The measured limits: `BLAST/Objective.md` spills to a side file above **~16 KB**
(only a preview then reaches context), and this file is **65 KB / 836 lines** — by far the largest of
them, and a ceiling rather than a target. ⚠️ Re-measure before quoting either number; this line has
already gone stale once inside the edit that added it. Anything not needed on every turn belongs in a
path-scoped `.claude/rules/*` file instead — that is the pressure valve, and this file is overdue for it.

## 🚀 `engage` — the one-word way to start a session (`OBJ-026`)

**Say `engage` and the workspace is made ready.** It is the front door to the automation described in
the two sections below: it discovers every repository, fetches, fast-forwards what is safe, re-derives
stale data, then reports what changed, what needs attention and what to do next.

```powershell
python tools\engage.py              # the full sequence (~10 s, ~35 s if data is stale)
python tools\engage.py --dry-run    # decide everything, change nothing
python tools\engage.py --offline    # no fetch; classify against local refs
python tools\engage_selftest.py     # 57 assertions, throwaway git fixtures
```

| Piece | What it is |
|---|---|
| `~/.claude/skills/engage/SKILL.md` | The user-invocable skill. Detects the workspace, runs the engine, **narrates the conclusion rather than pasting the output** |
| `engage_core.py` | Discovery, the per-repo policy table, and the ordered decision table. **Pure** — no writes, no printing, so it can be tested |
| `engage.py` | Orchestration, analysis and rendering. Every workspace path it binds to is in one `PATHS` block, so `OBJ-025` re-points it in a single edit |
| `engage_selftest.py` | 13 real git fixtures · 13 synthetic table rows · 11 safety-guard checks |
| `state/engage/` | `context.json` + `briefing.md` + append-only `engage.log`. **Gitignored** — unlike `.daily/`, this is per-invocation and regenerable |
| `control_center.py` + `control-center/` | **The Control Center (`OBJ-027`)** — the third arrow: `engage` measures and presents decisions, the owner approves, `engage` executes. React + Vite over a **127.0.0.1-only** server with a random per-process token on every request, never written to disk. The browser sends an action *type* plus a target, both looked up in `ACTIONS`; **no request data ever reaches a shell string**. Every git action still goes through `engage_core.run_git`'s allow-list and `policy_for`'s `D28` rights — the UI **cannot widen either**. ⛔ A decision interface, never a security boundary. State in `state/control-center/` |

⛔ **A pull happens only when all five hold:** policy allows it · tree clean · upstream exists · strictly
behind (never diverged) · no merge or rebase in progress. Everything else is reported, never forced.
An **unclassified** repository is fetched and reported but **never pulled** — that default is what makes
leaving discovery switched on safe. Bans are imported from `obj016_daily_refresh.FORBIDDEN`, so the
workspace has exactly one list of forbidden git subcommands.

⚠️ **It is safe-by-default, not deny-by-default (`D31`)** — the one script here that acts without
`--execute`. It is human-invoked, issues **zero** product HTTP, and `--ff-only` cannot lose work. When it
triggers `obj016_daily_refresh.py` it passes *that* script's `--execute`; it will never invoke
`obj017_weekly_execution.py`, `chain_runner.py` or `token_guard refresh`.

⚠️ **Run it from PowerShell, or set `PYTHONUTF8=1` under Bash** — same encoding trap as the scheduler.

## 🔁 Drift control — the closed loop (`OBJ-013`, v0.1)

Facts in this workspace are measured once and then quoted in a dozen documents, where they go stale
silently. The loop re-derives them from source and reports what no longer matches.

```powershell
python tools\obj013_loop.py check          # read-only drift check
python tools\obj013_loop.py check --json   # machine-readable
python tools\obj013_fix.py                 # dry run — what would be corrected
python tools\obj013_fix.py --apply         # write, with backups
python tools\obj013_rag_ingest.py --apply  # rebuild the workspace evidence index
```

A `SessionStart` hook runs `check --brief` and injects a capped (~1.5 KB) headline, so drift surfaces
without being asked. Full detail goes to `state/drift/drift-report.json`, never to context.

| Piece | What it is |
|---|---|
| `obj013_probes.py` | Re-derives each fact from source. **Read-only and offline** — refuses state-changing git, never calls the API |
| `state/drift/facts.json` | The registry: canonical value, unit, basis, derivation, and every document site that quotes it |
| `obj013_scan.py` | Diffs claims against measurements. Separates `mismatch` (fixable) from `anchor-not-found` / `anchor-ambiguous` (**report, never guess**) |
| `obj013_fix.py` | The only writer. Dry-run by default; `--apply` mandatory |
| `obj013_rag_ingest.py` | Indexes authored evidence into `corpus/workspace.jsonl`, a **sibling** to the PDF corpus |
| `state/drift/waivers.json` | Closes a deliberate item. Keyed to the evidence hash, so a waiver **expires when the measurement moves** |

**Rules the loop obeys, and you should too:**

- ⛔ **Auto-fix is confined to six files** — root `CLAUDE.md`, root `README.md`, the three `.claude/rules/*`,
  and the repo's `CLAUDE.md` + `AGENTS.md`. Everything else is report-only. Nine folders here have no git
  history; a bad automated write there is permanent.
- ⛔ **A multi-basis number is never auto-fixed.** "Endpoints" legitimately has five values that differ by
  unit. `api.endpoint_count` is deliberately `report-only`: the derivation yields 1,302 strict / 1,308 loose,
  and the canonical **1,306** comes from a rule nobody recorded. Rewriting 1,306 → 1,302 everywhere would be
  worse than the drift. **Keep quoting 1,306**, and settle the rule before changing that policy.
- ⛔ **The loop never rebuilds the graph.** `graphify-out/.graphify_root` names a *different checkout*
  (`C:\Users\…\git\pam_automation_bootstrap`), so the installed `post-commit`/`post-checkout` hooks refresh
  the wrong tree. The loop raises `REFUSE_REBUILD` and stops.
- ⛔ **Pull only.** `check` uses local refs; it never fetches, pulls, pushes or merges.

### 🕗 The daily refresh job (`OBJ-016`)

A Windows scheduled task, **`PAM-Dashboard-Daily-Refresh`**, runs `obj016_daily_refresh.py --execute`
at 08:30 daily. It is what keeps the drift loop, the RAG index and the dashboard current — so **the
drift check above now runs daily whether or not a session opens.**

```powershell
python tools\obj016_daily_refresh.py             # DRY RUN — deny-by-default
python tools\obj016_daily_refresh.py --execute    # pull, fetch, re-derive
Start-ScheduledTask -TaskName PAM-Dashboard-Daily-Refresh
```

| Rule | Detail |
|---|---|
| **`pam/` is fast-forward only** | `--ff-only`, so it can never create a merge commit, and **skipped entirely if its tree is dirty**. It will not stash, reset or checkout to get its work done |
| ⛔ **The automation repo is fetch-and-report** | `AI` has **no upstream**; the job fetches `origin` and reports how far behind `origin/Dev` it is. Merging is the owner's call, and uncommitted work is never touched. ⚠️ This row used to name "the 98 uncommitted files"; that work was committed long ago and the tree now measures **clean** (0 dirty, 1 stash) |
| ⛔ **It never executes the API suite** | Decided explicitly: fresh source changes no KPI, and a daily 5.5 h run against this environment would produce a daily false alarm. Zero HTTP to PAM, `/arcontoken` untouched |
| ⛔ **It never applies drift auto-fixes** | Drift is reported daily; `obj013_fix.py --apply` stays a human action, because it writes to the auto-loaded governance files |
| **Guarded structurally** | `run_git()` holds an allow-list — push · merge · rebase · reset · checkout · clean · gc · branch surgery are refused before reaching a subprocess |
| **State** | `state/daily/last-run.json` + append-only `daily.log`. `public/data/refresh.json` puts the result on the dashboard, so a failed job is visible rather than silently serving yesterday's figures |

⛔ **Two encoding traps that only bite under the scheduler — both fixed, do not undo:** a child Python
gets **no console**, so it picks the ANSI codepage and dies printing `⛔`
(`child_env()` forces `PYTHONUTF8=1`); and **the `*_register_*.ps1` scripts must stay 7-bit ASCII**, because
PS 5.1 reads UTF-8 as ANSI and an em-dash decodes into a smart quote that opens an unterminated string.

### 📅 The weekly execution (`OBJ-017`)

A second task, **`PAM-Weekly-API-Execution`**, runs `obj017_weekly_execution.py --execute` **Sundays at
10:00**. This is the only thing that moves the headline KPIs — the daily job refreshes what is *derived*.

```powershell
python tools\obj017_weekly_execution.py            # DRY RUN — zero HTTP, not even the probe
python tools\obj017_weekly_execution.py --execute   # the full chain, ~5.5 h
python tools\obj017_weekly_execution.py --execute --resume-only <run>
Start-ScheduledTask -TaskName PAM-Weekly-API-Execution
```

Chain: token-latch check → **unauthenticated** env probe → generate flows → `chain_runner --execute`
(6 h budget, `GET,POST,PUT,PATCH`) → **one** resume if any flow aborted → `obj010_collect` →
`obj010_build_workbook --baseline <resolved previous run>` → dashboard datasets → `execution.json`.

| Rule | Detail |
|---|---|
| ⛔ **Never `--allow-teardown`, `--allow-preexisting-teardown` or `--include-unsafe`** | Asserted absent in `run_script()`, not merely omitted. `--include-unsafe` re-enables the three endpoints that stop the IIS app pool |
| ⛔ **One token attempt, latched** | **D24 knowingly relaxes the "no scheduled token generation" rule for this job only.** Mitigations: the host is probed **unauthenticated and first**, so no token is spent against a dead host; exactly one attempt; a failure latches for ever until a human clears it. `token_guard.py` itself must never gain a scheduled refresh. If `GenericScheduler` locks again, **disable this task first** |
| ⛔ **`chain_runner` takes the token BEFORE its own `--wait-for-env`** | Which is why the pre-flight probe lives in the weekly job instead. Do not "simplify" it away |
| **One resume, then stop** | A partial run is kept and flagged incomplete — never promoted to current |

⛔ **N and N-1 are resolved at run time, never hardcoded.** `obj015_build_dashboard_data.py` picks the
newest substantive run as N. **But authored analysis is pinned**: the benchmark narrative, the trend line
and the three headline findings belong to `AUTHORED_ANALYSIS_RUN` and are **withheld** when N moves —
attaching them to a run that never produced them would be fabrication. After a weekly run, author an
analysis and update that constant, or the dashboard will keep saying "analysis pending".

### 🗂️ The daily client-ticket analysis (`OBJ-028`, `OBJ-029`)

A **third** scheduled task, **`PAM-Client-Ticket-Analysis`**, runs `tools/jira/pamit_client_analysis.py`
at **09:00 daily**. It is the only job that reads Jira, and it touches the PAM API not at all.

```powershell
python tools\jira\pamit_client_analysis.py    # fetch, analyse, write the report and the workbook
python tools\jira\pamit_workbook.py           # rebuild the workbook from the last capture
powershell -ExecutionPolicy Bypass -File tools\jira\register_client_analysis_task.ps1
```

| Rule | Detail |
|---|---|
| ⛔ **Read-only against Jira** | `GET` plus `POST` to the two Jira *search* endpoints and nothing else — the guard in `jira_query.py` refuses any other method or path. It never touches a ticket, field, comment or workflow, and issues **zero** requests to the PAM product API |
| **The build axis is `Affected Milestone`** | `customfield_10092`, 97.3% populated (`D42`). **Not** `Fix versions` — that is where a fix *ships*, not where the client *found* it — and **not** any field named `Milestone` (0–9%, or 63% populated with the literal string `None`) |
| ⛔ **Three fields are named `Affected Milestone`-something and two are 0% on PAMIT** | Picking one returns an empty build line that reads exactly like a clean result. Full audit: `docs/analysis/D1-client-ticket-patterns.md` §0.2 + workbook sheet `10 Field Audit` |
| ⛔ **No count without its tickets** (`D43`) | Sheet `04 Ticket Details` is the source data; sheet `09 Count Reconciliation` restates every headline count as a live `COUNTIFS` with `PASS`/`FAIL`, and `pamit_workbook.verify()` exits non-zero if anything fails to reconcile |
| ⛔ **One workbook, many worksheets** (`D44`) | `artifacts/workbooks/PAM-Client-Ticket-Analysis.xlsx` — **13 sheets**, 2,169 tickets × **71 columns**. A new analysis is a new `sheet_*` builder in `build()` plus its manifest row, **never a second `.xlsx`** |
| **Quote a regression figure over its populated subset** | The three client-facing fields (`cf 10780` reopen-from-customer · `cf 11253` working-in-previous-version · `cf 11254` previous-working-version) sit at ~25%. `unstated` is an **unfilled field, never evidence of "no regression"**; the sentinel is `Info not available in JIRA` (`D46`) |
| **`RCA` (`cf 10245`) is the live root-cause field** | 80.7% populated, 33 values in 15 families — the most populated analytical field in the project. `cf 10113` (0.2%) and `cf 10199` (0.1%) are the decoys that made an earlier version of the analysis claim Jira held no root-cause categorisation at all |
| ⛔ **`Phase` and `ReopenCount` exist and are 0%** | Defect-injection phase is **not answerable**, and is **not** derivable from `RCA` — `Code - Logic Issue` says where a defect was *found in code*, not where it was *introduced* |
| **315 tickets are "not a product defect"** | Classified so by the product team. A weak spot attributed to one of them is a **false finding** — reported, never silently applied to a denominator (`D38`) |

**Where its output lives:** the report is `docs/analysis/D1-client-ticket-patterns.md`, the workbook is
`artifacts/workbooks/PAM-Client-Ticket-Analysis.xlsx`, the dated captures are `artifacts/client-tickets/`
(never deleted — sheet `12 Daily History` is derived from them), and its state is `state/client-analysis/`
(`last-run.json` + append-only `analysis.log`).

⚠️ **The lesson `D42` and `D46` share, recorded twice because it cost twice:** several Jira fields share a
concept and **only one is live**. Measure *every* same-named candidate before picking one — choosing a 0%
field returns an empty result that is indistinguishable from a clean one. Using `fixVersion` moved the
build line from 2,010 to 1,384 and made the current build `HF13` look 13× worse than it is.

⛔ **All three scheduled tasks store absolute paths — moving the workspace kills every one of them
silently.** They are user-level tasks whose `Execute`, `Arguments` and `WorkingDirectory` are literal
strings. A dead `WorkingDirectory` fails with **`0x8007010B`** ("the directory name is invalid") *before*
Python starts, so nothing reaches any log and the only symptom is a `LastRunTime` that stops advancing.
`paths.py` cannot help — it is only reached once the process runs. Measured: after the workspace moved to
`E:\Omkar\AI Projects\Dev Project`, all three tasks were dead for two days while `engage` (human-invoked,
and therefore correctly rooted) kept the derived data current and masked it. **The fix is to re-run the
registrars** — each re-derives the root by marker, so none needs editing:

```powershell
powershell -ExecutionPolicy Bypass -File tools\obj016_register_task.ps1
powershell -ExecutionPolicy Bypass -File tools\obj017_register_weekly_task.ps1
powershell -ExecutionPolicy Bypass -File tools\jira\register_client_analysis_task.ps1
```

⚠️ The same applies to the two hooks in `.claude/settings.json`, which hold the same literal path and which
**the assistant cannot edit** — an owner fix, and until it lands neither `Objective.md` injection nor the
`SessionStart` drift headline actually fires. ⛔ `obj013_loop`'s
`governance.objective_single_injection` probe cannot catch this: it substring-matches the config text
rather than resolving the path, so it reports `1` while the true count is `0`.

## 🔁 Interrupted executions — resume, never abandon (`OBJ-020`)

**Standing rule, set by the owner.** A scheduled or long-running execution that stops because of a
**timeout, a temporary deployment, or a backend issue is not a failed execution.** It is resumed.

| Rule | Detail |
|---|---|
| **Wait 30 minutes, then resume** | Repeat the cycle. **At least five** intervals before the window may close |
| **12 h ceiling** | Give up only after 12 h of *continuous* failure. A run taking 20–24 h is acceptable — completing matters more than finishing quickly |
| **Report at the end only** | Do not report each transient failure. Report on completion, or when the ceiling is hit |
| ⛔ **One token, pinned for the whole cycle** | Resolve the bearer token **once**, pin it to `$PAM_API_TOKEN`, and let every retry reuse it. `token_guard` resolves that env var first, so **no retry reaches `/arcontoken`**. Retry-on-failure against that endpoint is exactly what locked `GenericScheduler` in July — an unattended retry loop is only safe *because* of the pin |
| ⛔ **A rejected login is NOT transient** | Stop at the first rejection and report it. Every attempt increments a lockout counter on a shared functional account, and `auto_adminui` is already locked |

`tools/obj020_execution_supervisor.py` implements this. It runs **detached**, so completion
never depends on an interactive session surviving; state is in `state/weekly/obj020-supervisor.json`
and `obj020-supervisor.log`.

⛔ **An interrupted run must never be invisible.** Declining to *promote* a partial run to N is correct —
its figures are not comparable. Declining to *show* it is not: "no run happened" and "a run was
interrupted at 43%" are different facts. `reliability.json` (API dashboard, **Execution reliability**
view) and `executions.json` (performance dashboard) carry every run's terminal state.

⚠️ **`--budget-seconds` paces the run, it does not just cap it.** `chain_runner` recomputes the
inter-call delay each hop to land inside the window (floor 0.25 s, ceiling 30 s), so a larger budget
makes a run *slower*, not faster. Raise it to let a run finish, not to speed one up.

⛔ **Three path-convention bugs in `obj017_weekly_execution.py` were fixed under `OBJ-020` — do not
reintroduce them.** `chain_runner --resume` takes a **bare run id** (it prepends `artifacts/runs/`
itself), while `obj010_collect.py` and `obj010_build_workbook.py` take the **path**. `obj017` had both
backwards, so its resume searched `artifacts/runs/artifacts/runs/<id>`, exited 2, and **that resume path
had never once succeeded** — which is why Sunday's "one resume" policy never salvaged anything.

## Consult these before grepping

- **Knowledge graph** — `pam_automation_bootstrap/graphify-out/` indexes the Java sources as 17,293 nodes
  / 49,193 edges. The repo's `.mcp.json` registers a **`graphify` MCP server**, so prefer its native tools
  (`query_graph`, `get_neighbors`, `shortest_path`, `god_nodes`, …) over shelling out; the CLI equivalents
  are `graphify query "<question>"`, `graphify explain "<class>"`, `graphify affected "<class>" --depth 1`.
  ⛔ **Check freshness with `python tools\obj013_loop.py check`, not by reading the report.**
  `GRAPH_REPORT.md` does **not** record a `Built from commit:` line — that instruction was wrong and is
  removed. Its header carries a build *date* and the *source path*, and the path is the thing that matters:
  it names `C:\Users\omkar.kumbhar_pam\git\pam_automation_bootstrap`, **a different checkout**. The
  `post-commit` / `post-checkout` hooks in this repo therefore rebuild that tree, not this one, which is why
  the graph is stale here and has never refreshed. It predates the whole `com.arcon.utils.validation`
  package, so `query_graph` returns "not found" for exactly the code this file tells you to use.
  Suite XMLs are **not** indexed — Graphify has no XML parser, so suite→test-class questions still need grep.
  ⚠️ **Three viewers exist, and this file previously said they did not.** Measured under `OBJ-027` in `artifacts/graph/pam-scope/graphify-out/`: **`graph.html`, `GRAPH_TREE.html` and `graphify-pam-callflow.html` are all present.** The old claim was wrong twice over — it looked in the bootstrap repo's `graphify-out/` rather than the workspace's, and it used the wrong callflow filename (`pam_automation_bootstrap-callflow.html`, which exists nowhere). ⛔ Genuinely absent: **`graphify-out/wiki/`** — a graphify feature this workspace has never generated. The drift probe now checks the right tree under the right names, and `docs.declared_paths_exist` is clean as a result.
  Full command reference: `AGENTS.md`.
- **Manual test cases** — a user-global `pamit-testcases` MCP server (`search_test_cases`, `get_test_case`,
  `test_case_stats`) serves the hand-written PAMIT test-case corpus. It is **small and partial** — 63 cases,
  Login (50) and Dashboard (13) only — so absence there proves nothing about coverage. The server lives
  outside this workspace, at `E:\Omkar\AI\MCP\Custom_MCP_Vibe\Test_Case_Creator`.
- **Product documentation** — `tools/rag/` is the extracted, page-cited corpus.
  `python tools\rag\query.py find "<terms>"` or `page <doc> <N>`. Cite as `<doc>:p<N>`. Two different
  kinds of document live there, and conflating them wastes a search:
  - The **two administrator guides** (1,101 pp) cover the access model and product concepts. They contain
    **no endpoints, schemas, or error codes** — do not look for an API contract in them.
  - **`PAM API (Internal Team).pdf`** (2,470 pp, Confluence export → `rag/corpus/pam-api.md`) is a different
    asset entirely: **3,194 JSON payload examples**, of which **1,605–1,654 are bound to an endpoint** — the
    best request-body source available. *(The range is real: `build_source_map.py` counts 1,654 bound / 1,540
    orphaned; `docs/analysis/A7-…` §1 counts 1,605 / 1,589 / 440 unparseable. Both sum to 3,194 — the two
    definitions differ on unparseable examples. **Quote a figure with its basis, never bare.**)*
    Limits: 70% of the 1,306 endpoints are undocumented, only **3** error codes (two previously counted were
    IP-address fragments), **6 of the 31** measured response shapes, and payloads bind to endpoints **by page
    proximity**, so a binding can be wrong. The owner has confirmed it is **not up to date**. Gap analysis:
    `docs/briefs/document-gap.md`; full correction list: `docs/analysis/A7-documentation-gap-analysis.md` §9.
- **Current state of the API validation work** — `docs/management/summary/API-Chaining-Feasibility-Demo.md` first
  (the executed three-flow demo), then the newest `artifacts/runs/<timestamp>/RUN_REPORT.md`, then
  `docs/findings/issues/` for defects. `docs/runs.md` explains how to read a run report and how to
  re-execute; `docs/briefs/overview.md` explains how dynamic generation works. Active requirement and backlog:
  `BLAST/Objective.md` (active instruction), `docs/history/README.md` (history and former backlog).
- **Harness scripts** — every one lives in `tools/`, never in `Reports/`. All are
  deny-by-default: **a bare run issues zero HTTP calls**, `--execute` is required. Script inventory,
  the Swagger split, and the create-endpoint data gap: `.claude/rules/api-surface.md`.

## ⛔ "Execute everything" = the dynamic framework, never the bootstrap suite

**Standing rule, set by the owner (recorded under `OBJ-010`).** When the owner says *execute everything*,
*run the APIs*, or *run the suite*, that means the **AI-based dynamic API framework in
`tools/`** — generate flows → `chain_runner.py --execute` → validate → report.

`pam_automation_bootstrap/` is a **reference asset only**: read it to learn scenarios, payloads, expected
statuses and error codes, and to *generate* flow JSON from. **Never run its Java/TestNG API tests as the
deliverable** — no `mvn test`, no suite XMLs, no runner classes. This does not change §Edit scope; it
narrows what "execute" means. If a request genuinely needs Maven, say so and get it confirmed first.

✅ **One standing exception — dependency remediation (`D26`).** A `pom.xml` change can only be validated by
resolving and compiling against the real dependency graph, which no Python harness can do. So
`dependency:tree`, `test-compile`, and targeted suite runs for Excel / DB / logging / Playwright / API
regression are permitted **when the work is a dependency change**. The blocklist and the one-token rule
still bind, and a run that needs a report still needs a **suite XML** — `-Dtest` overrides
`suiteXmlFiles`, so the listeners never register.

⚠️ **Since `OBJ-018` there is a third executable thing, and it is neither of those two.**
`pam_automation_bootstrap/performance/` is a k6 performance framework for the login journey — browser,
HTTP and correlation. It is deny-by-default like everything in `tools/` (a bare `k6 run`
issues zero requests; `PERF_EXECUTE=true` is required, checked in `setup()` **and** on the request path
so `--no-setup` cannot bypass it). It is **not** covered by "execute everything": running it generates
load against an authentication endpoint and is a separate, named decision. It has never been executed.
Two things to know before touching it: it authenticates against the **web tier** (`POST
/frmLoginACMO.aspx` on `:1302`), never `/arcontoken` — those are independent mechanisms against separate
identity stores — and its credentials come from `PERF_USERNAME`/`PERF_PASSWORD` only. Start at
`performance/README.md`.

## Conventions

- Jira project is `PAMIT`. Unresolvable items are marked `PAMIT-TODO` in place. Raising a real ticket has
  its own traps (v3 needs **ADF**, not wiki markup; `createmeta` under-reports 6 required fields and
  paginates at 50) — read `tools/jira/jira.md` before composing one, and never attach `JIRA-TICKET.md` to its own
  ticket. One ticket exists so far: `PAMIT-42744` (LH-01); LH-02…13 are **drafted but deliberately held**.
  ⛔ **`LH-13` is a security finding** — 19 endpoints accept an invalid bearer token, 6 of them writes. Raising
  it is the owner's call and it has not been raised.
- Five user-invocable skills are installed globally, and three encode workspace rules you would
  otherwise have to reconstruct: **`/engage`** (§`engage` above — the session-start entry point), **`/raise-the-jira-ticket`** (the `tools/jira/` workflow above) and **`/go-go-go`** (the
  git sync/commit/push activity — it targets the automation repo, where a **manual** push is permitted
  since `D47`, so invoke it there only on an explicit instruction; develop on `Dev`, never `AI`). Also `/graphify` and `/give-me-a-prompt`.
- Code-level conventions (test IDs, `@BeforeMethod`/`@AfterMethod` pairs, logging, tabs, CI) are
  path-scoped — see `.claude/rules/automation-repo.md`.
