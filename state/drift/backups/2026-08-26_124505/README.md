# ARCON PAM Automation — Workspace Guide

**What this is:** the working folder for ARCON PAM QA automation — the test framework, the product source
it tests against, the product documentation, and the planning material around it.
**Jira project:** `PAMIT` · **Product:** ARCON PAM (.NET) · **Framework:** Java 21 · Playwright · TestNG · Maven
**Audience:** anyone opening this project for the first time, whether to review it or to work in it.
**Last updated:** 2026-08-25 (`v0.3`, `OBJ-025`)

> **This folder IS a git repository** — `dynamic-api-validator`, branch `main`. It also *contains* two
> unrelated checkouts (`pam/` and `Automation gitlab repo/`) that are gitignored from it and keep their own
> remotes. So there are **three** repositories in play, each with different rights: §2 has the table.

> ⚠️ **Restructured to `v0.3`.** The layout is five drawers by *kind*. If you have a note, script or
> bookmark naming `workbench/`, `Reports/`, `document/`, `questions/`, `writer/`, `Graphify/`, `jira/`,
> `required-context/`, `objective-history/`, `Company Documents/` or `Developer-Loopholes/`, it is stale —
> the complete old→new map is [`docs/history/README.md`](docs/history/README.md) §7.

## 1. What is in here

Five drawers, named for **what a thing is**, not for the task that produced it. That is the whole
organising idea: if you know whether you want to *read* something, *run* something, or look at something a
tool *produced*, you know which folder to open.

| Folder | What it is | May I change it? |
|---|---|---|
| **`docs/`** | **Everything written for a human to read.** `analysis/` (nine technical reports) · `business-context/` (**start at `BUSINESS-CONTEXT-DEMO.md`** — the 5-minute walkthrough) · `briefs/` (six briefs, each for a different reader) · `findings/` (the 13 API findings, the authored issues, the repo-size investigation) · `history/` (**append-only** project record — every objective, decision and measurement since day one) · `gaps/` · `knowledge-base/` · `management/` · `specs/` | ✅ Yes |
| **`tools/`** | **Everything you can run.** The Python harness that generates and executes API flows, plus the Jira client, the documentation search (`rag/`), the new-project onboarding kit, and the two React dashboards (`dashboard/`, `dashboard-performance/` — `npm install` then `npm run dev`) | ✅ Yes |
| **`data/`** | **Hand-maintained input.** The vendor PDFs and Swagger list (`sources/`), the analysis JSON, the knowledge-base questions, the onboarding profiles. Edit these, then re-run the tool that consumes them | ✅ Yes — this is where you edit |
| **`artifacts/`** | **Everything a tool produced.** `runs/` (13 execution folders — **retained, never deleted**) · the Excel workbooks and the management deck · the 13 evidence packs · the knowledge graph · the extracted document corpus | 🔄 Generated — never hand-edit; fix the tool and re-run |
| **`state/`** | What the scheduled jobs recorded — daily refresh, weekly execution, drift, performance. Tracked **on purpose**: it is the only evidence an unattended job actually ran | 🔄 Generated |
| **`BLAST/`** | How a new requirement enters. `Objective.md` is the one file the owner edits to say what they want next | ✅ `Objective.md` is the input |
| `Automation gitlab repo/` | The QA automation framework (Java 21 · Playwright · TestNG · Maven), branch `Dev`. **Its own repository.** | ✅ Code changes go here — ⛔ but never push |
| `pam/` | The ARCON PAM product source. **Its own repository.** | ⛔ Reference only |
| `CLAUDE.md` | Operating guidance for AI assistants. Humans can skim it for detail this file summarises | ✅ |

**Two things that were true before and still are:** every execution folder under `artifacts/runs/` is kept
for ever, and nothing written outside the two nested checkouts can contaminate a product build.

## 2. ⛔ The one rule that matters

**All actual changes are made in the automation GitLab repository, in the `pam_automation_bootstrap`
project — `Automation gitlab repo/pam_automation_bootstrap/`, on branch `Dev`.**

⚠️ **The branch changed from `AI` to `Dev`** (owner decision `D25`): `AI` had no unique commits, and the
`pam` submodule gitlink tracks `Dev`, so work on `AI` could never reach the product repo.

`pam/` is reference data only. Read it freely for context; never modify it, never commit inside it, and
leave it with a clean `git status`. It is the developer's product repository — automation commits landing
there would mix test code into the product build.

`pam/AutomationTesting/` is the easiest mistake to make: it *looks* editable, is not, and is **being
deleted**. It has no git link to the automation repo, and it is **not part of any build** — no Maven step
in `pam/jenkins-pipeline`, no reference in `pam/.gitlab-ci.yml`. Only a dependency scanner sees it, which
is why a security report can name `AutomationTesting/pom.xml` when the file that actually builds is
`pam_automation_bootstrap/pom.xml`.

---

## 3. How the automation code reaches the product repo

⚠️ **Rewritten under `OBJ-022`.** This section used to be titled "Why there are two copies of the
automation code" and described a manual file copy. **There is now one source of truth and a submodule
pointer** — the copy model was retired after it was measured reverting a security fix.

| Location | Role | Updated |
|---|---|---|
| `Automation gitlab repo/pam_automation_bootstrap/` | **The single source of truth.** All development, on `Dev`. | Daily, by whoever is working |
| `pam/Automation/` | **The submodule.** A gitlink pinning one commit of the repo above — not a copy of its files. | When the owner bumps the gitlink |
| `pam/AutomationTesting/` | ⛔ **Legacy hand-copy, being deleted.** Not part of any build. | Never again |

**Release path — only the first step is open to contributors:**

```
develop on Dev  →  owner reviews  →  owner pushes origin/Dev  →  owner bumps pam submodule gitlink
  ↑ you are here      ↑ owner only        ↑ owner only                  ↑ owner only
```

**Why the copy model was retired — measured, not theoretical.** `pam` commit `0520b6b79` fixed six
vulnerable dependencies in `AutomationTesting/pom.xml`; commit `e278fd399` then bulk-copied the bootstrap
tree over it and **reverted all six**. Fixing the delivery copy while the source of truth stayed
vulnerable guaranteed the regression would come back on the next refresh.

**Two consequences worth knowing:**

- **A commit in the bootstrap repo is not visible in `pam` until the gitlink is bumped.** The pointer does
  not follow the branch.
- **The submodule is registered but uninitialised** — `pam/Automation/` is an empty directory until
  `git submodule update --init`, and CI needs `GIT_SUBMODULE_STRATEGY` set to clone it at all.

**Develop on branch `Dev`** (owner decision `D25`). Two measured reasons: `AI` holds no unique commits, so
it had become a stale point on `Dev` rather than a working branch; and the `pam` submodule gitlink tracks
`Dev`, so anything landing on `AI` could never reach the product repo. ⛔ **Never push, never merge** here —
releasing is the owner's call, and the no-push rule is enforced mechanically (`D28`).

⚠️ Older notes say "commit to `AI` and stop there", and that `AI` is local-only with no upstream. Both are
wrong: `git branch -vv` reports `AI [origin/Dev: behind 21]`, so it *does* have an upstream, and it is
`origin/Dev`.

---

## 4. How requirements enter the project — the BLAST framework

`BLAST/` is a framework centred on two files:

| File | Role |
|---|---|
| **`Objective.md`** | Where the requirement is defined. **Edit this to change what happens.** Loaded automatically on every prompt |
| **`B.L.A.S.T.md`** | The protocol. It drives a **question-and-answer process** based on that requirement. |
| **`docs/history/README.md`** (workspace root) | **Append-only** record of every instruction, decision and measurement since Day 1 |

**The cycle:**

```
1. Define the requirement in Objective.md
2. Run it:  "Run Objective.md by referring to blast.md, and give me the output."
3. BLAST asks clarifying questions about the requirement
4. Answers are provided
5. The expected output is generated accordingly — landing in pam_automation_bootstrap on branch AI
```

`Objective.md` is a **reusable, dynamic blueprint**, not a fixed statement. It is rewritten whenever the
requirement changes and run again. Going forward this is the single entry point: update `Objective.md`,
and changes flow from there. Since 2026-08-03 it is loaded automatically on every prompt, so an edit takes
effect without pointing at the file. Its permanent counterpart is `docs/history/README.md` at the
workspace root, which is append-only and holds the full history.

The Q&A step in stage 3 is deliberate, not friction — it is what stops work starting from a guessed
requirement. `BLAST/CLAUDE.md` and `BLAST/B.L.A.S.T.md` document the protocol in full.

---

## 5. Reference material

`data/sources/` holds the source company data. `tools/rag/` makes the guides searchable.

| Resource | Where | Notes |
|---|---|---|
| PAM Administrative Guide | `data/sources/PAM Administrative Guide.pdf` | 702 pages |
| Client Manager Guide | `data/sources/Client Manager Guide.pdf` | 399 pages |
| Conference material | `data/sources/` | Add conference files here alongside the guides |
| **Conference link** | *`<paste the URL here>`* | 📌 **Placeholder — awaiting the link.** This row is its home; add it here and it stays discoverable from the front page. |

**Searching the guides** — run from this folder:

```powershell
python tools\rag\query.py find "web api registration"
python tools\rag\query.py page pam-admin 447-455
```

Every fact taken from the guides is cited as `<doc>:p<N>` (e.g. `pam-admin:p455`) so a reviewer can verify
it against the printed page. Note the limit: these are **administrator guides**, so they describe the
access model and module taxonomy but contain **no API endpoints, schemas, or error codes**.

---

## 6. Running the tests

Two things to know before the first run.

**1. `JAVA_HOME` must be overridden every session.** The system value points at a JDK that is not
installed; the build needs Java 21. ⚠️ **Verify the path before trusting it** — this line used to name
`21.0.11.10`, a directory that does not exist, so following it produced the very failure it was written
to prevent. List what is actually installed with
`Get-ChildItem "C:\Program Files\Eclipse Adoptium" | Select-Object -ExpandProperty Name`:

```powershell
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-21.0.12.8-hotspot"
```

**2. Run Maven from the framework folder,** `Automation gitlab repo/pam_automation_bootstrap/`:

```powershell
mvn clean test                                                    # default suite, QA_MsSQL, chrome
mvn clean test -Denv=CICD -DsuiteFile=CICD_Suites/APISuite.xml    # a specific suite
mvn clean test -DsuiteFile=API_Suites/Positive_All/<Module>.xml   # one API module
mvn -o clean test-compile -DskipTests                             # compile check only
```

| Flag | Overrides |
|---|---|
| `-Denv` | Which `Environments/<env>.properties` loads (20 available) |
| `-DsuiteFile` | The TestNG suite XML |
| `-DbrowserType` | `chrome` · `chromium` · `firefox` · `safari` · `edge` |

⚠️ **One trap worth knowing:** most PAM endpoints return **HTTP 200 with an application-level `errorCode`
in the body** — a *rejected* request is usually a 200, not a 4xx. An assertion that checks only the status
code will pass against a fully rejected request. Never write one.

---

## 7. Where to read next

| You want to | Read |
|---|---|
| Run or explain the API chaining demo | **`docs/briefs/overview.md`** — start here; run commands in `docs/runs.md` |
| Work in the framework | `Automation gitlab repo/pam_automation_bootstrap/AGENTS.md` — layout, commands, conventions |
| See what has been tested and found | `docs/management/summary/API-Chaining-Feasibility-Demo.md`, then the newest `artifacts/runs/*/RUN_REPORT.md` |
| **Demo how business context is given to the AI** | ⭐ **`docs/business-context/BUSINESS-CONTEXT-DEMO.md`** — short, 5 minutes. The full reference is `BUSINESS-CONTEXT-STANDARD.md` |
| **Understand the whole project, or run a demo** | **`artifacts/workbooks/PAM-Project-Knowledge-Base.xlsx`** — read the `Q&A` sheet, or follow `Demo Flow` |
| **Brief management on risk and next actions** | **`artifacts/workbooks/PAM-Project-Governance.xlsx`** → *Management Findings* |
| **See every validation gap, row by row** | **`artifacts/workbooks/PAM-API-Validation-Analysis.xlsx`** → *Index*; reasoning in `docs/analysis/` |
| Know what changed in the framework's validation | `docs/analysis/B-framework-validation-enhancement.md` |
| Know whether database validation is possible | `docs/analysis/C-database-validation.md` |
| Review the defects raised | `docs/findings/issues/` — 11 issues, each citing raw evidence (ISSUE-009 now closed) |
| Know what is queued next | `docs/history/README.md` §6 — the backlog file was retired 2026-08-03 |
| Know the target architecture | `docs/specs/playwright-advance-e2e.SKILL.md` (the governing spec) |
| Cite the product documentation | `tools/rag/README.md` |
| Submit a requirement | §4 above, then `BLAST/Objective.md` |
| Set an AI assistant to work here | `CLAUDE.md` |
