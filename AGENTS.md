# AGENTS.md — workspace-root guidance for AI agents

> **De-identified snapshot.** This copy omits the real deployment: there are **no** git repositories
> checked out (the root is not a repo), and the nested checkouts `Automation gitlab repo/` and `pam/`
> are **absent**. Anything below that touches git, Maven, or the automation framework applies only once
> those checkouts are restored. In the current tree you can verify and run the Python tooling only.

## Restored-deployment facts (apply only when the nested checkouts exist)

When `Automation gitlab repo/` and `pam/` are present, this is really three repos with different rights —
don't run a git remote operation until you know which one you are in:

| Repo | Location | Branch | Push |
|---|---|---|---|
| **dynamic-api-validator** (this workspace) | root | `main` | Auto-allowed |
| **PAM Bootstrap Automation** | `Automation gitlab repo/pam_automation_bootstrap/` | `Dev` | Manual only — owner must ask in the same turn. Never auto-push |
| **PAM** (product source) | `pam/` | — | Never push. Pushurl mechanically disabled (`D28`) |

`pam/` embeds the bootstrap repo as an **uninitialised submodule** at `pam/Automation/` — an empty
directory until `git submodule update --init`. The gitlink pins one commit and does not follow the branch:
a commit on `Dev` is **not** visible in `pam` until the owner bumps it. Never call a fix "reached PAM"
on the strength of a bootstrap commit alone.

Develop on `Dev`, never `AI` (`AI` is a stale point behind `origin/Dev`).

**JAVA_HOME** must be overridden every session — the system value points at a nonexistent JDK and Maven
fails until you fix it. **Verify the Adoptium folder first**, it has changed before:

```powershell
Get-ChildItem "C:\Program Files\Eclipse Adoptium" | Select-Object -ExpandProperty Name
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-21.0.12.8-hotspot"
```

Run Maven from **PowerShell only** (not Bash), from `Automation gitlab repo/pam_automation_bootstrap/`:
```powershell
mvn clean test                                                    # default: Demo.xml, QA_MsSQL, chrome
mvn clean test -DsuiteFile=API_Suites/Positive_All/<Module>.xml   # one module
mvn -o clean test-compile -DskipTests                             # compile check
```

`-Dtest=X` overrides `suiteXmlFiles` entirely — listeners never register, no Excel report produced. Use a suite XML instead.

## Response envelope — the #1 assertion trap

Most PAM endpoints return **HTTP 200 with an application-level `errorCode` in the body**. A rejected request is usually 200, not 4xx.

- Never assert only `status == 200` — it passes against a fully rejected request.
- Use `com.arcon.utils.validation` for new validation code (`PamEnvelope`, `PamApiValidator`).
- `Success: true` is not evidence of a write — check `Message` semantics.

## Path resolution — one rule

`tools/paths.py` is the single root resolver. **Never count parents or hardcode depths.** Import `workspace_root()` or `ROOT` from it.

## Deny-by-default — the HTTP harness scripts

A bare `python tools\<script>.py` issues **zero HTTP calls**. `chain_runner.py`, `obj016_daily_refresh.py`
and `obj017_weekly_execution.py` each require `--execute` to do real work; a dry run prints what would
happen and stops. ⚠️ **`engage.py` is the one exception (`D31`)** — it is *safe*-by-default, not
deny-by-default, and runs without `--execute` (it has `--dry-run` instead). Don't expect `--execute` there.

**Where to run them:** run the harness from **PowerShell**. Under Bash, set `PYTHONUTF8=1` first — the
scripts print non-ASCII glyphs (`⛔`) and a console-less Python child dies on the ANSI codepage otherwise
(the scheduler forces `PYTHONUTF8=1` via `child_env()`).

## Token generation — single gate, zero retries

`tools/token_guard.py` is the only path to `/arcontoken`. It is **subcommand-based, not `--execute`**:
`status` (report only) · `refresh` (ONE attempt if the cache is expired) · `flash`-free `clear-latch`.
Resolution order: `$PAM_API_TOKEN` env var → valid cache → **one** live attempt. A failed attempt latches
forever (`tools/.token_attempt_block.json`) until a human runs `clear-latch`. Never retry — the account is
shared with production ETL.

## Three blocklisted endpoints — never call

`GET /api/ActivityLogs/GetErrorLogs`, `GET /api/ActivityLogs/GetLogs`, `GET /api/ActivityLogs/GetAllActiveUserDetails` hang for 30s and **crash the IIS app pool**. Three requests were enough to take the API down to 503. Enforce at planning time, before a request is built.

## "Execute everything" means the dynamic framework

When told to run the APIs or execute everything, that means: generate flows → `chain_runner.py --execute` → validate → report. The Java/TestNG suite in the bootstrap repo is a **reference asset only** — read it for scenarios and payloads, never run it as the deliverable.

## Jira analysis — the half of this tree that actually runs

Two projects on `https://arcon-tech-solution.atlassian.net`: **`PAMIT`** (PAM product) and **`CI`**
(Converged Identity). Credentials in `tools/jira/.env` (gitignored; copy `.env.sample`).

```powershell
python tools\jira\pamit_client_analysis.py --offline   # D1 report + workbook, zero HTTP
python tools\jira\pamit_workbook.py                    # rebuild the workbook from that capture
python tools\jira\jira_analysis_2026.py --offline      # PAMIT census 01Jan-21Sep26, 5,740 tickets
python tools\jira\ci_analysis_2026.py --offline        # CI census,    same range, 5,994 tickets
python tools\jira\md_to_docx_xlsx.py <report.md>       # render an analysis markdown; REQUIRES the path
python tools\jira\convert_analysis.py                  # the PAMIT render; path derived, takes no argument
python tools\jira\build_delivery_pack.py               # the dated client pack -> 21-09-2026\{PAM,CI}\
python tools\jira\track_tickets.py                     # daily "what needs us"; exit 1 = action items

python tools\jira\doctor.py                            # preflight: env, packages, creds, freshness
python tools\jira\validate_analysis.py                 # 55 checks vs the snapshots; exit 1 = a figure is wrong
```

⚠️ **`md_to_docx_xlsx.py` takes a path and fails without one** — an earlier revision of this file listed it
bare. `convert_analysis.py` is the one that derives its own.

✅ **Three report defects were fixed on 2026-09-22** — PAMIT §12 `Affected Milestone` (published 100%
`Not set`; really 78.8% populated), the CI sub-task count (published 4,241; really **1,443**), and the
milestone assignment total (published 5,832; really 4,615). All three reconciled cleanly through every
`OBJ-030` gate, because those gates check the generator against its own rule. `validate_analysis.py` exists
to close that gap — it re-derives each figure from the raw snapshot instead. See
`docs/hardening/README.md` and `tools/jira/README.md`.

Every one has a cached snapshot on disk, so **prefer `--offline`** — identical output, no requests.
The `.docx`/`.xlsx` beside each report are rendered, not authored: edit the markdown and re-render.

⛔ **Read-only is structural, not conventional.** `jira_query.py::_check()` permits `GET` to a fixed
prefix list and `POST` to the two *search* endpoints only; anything else raises `ReadOnlyViolation`.
`GET /rest/api/3/search` is gone (HTTP 410) — only `/search/jql` remains. `/search/approximate-count`
was measured wrong here, so any figure in a report must come from `search()`, which enumerates.

⚠️ **Build axis is `Affected Milestone` (`cf 10092`, 97.3%)**, never `Fix versions`, never a
`Milestone`-named field (`D42`). Several Jira fields share a concept and only one is live — measure
every same-named candidate, because a 0% field returns an empty result that reads exactly like a clean
one. `RCA` (`cf 10245`) is 80.7% populated and carries most of the analytical weight; `Phase` and
`ReopenCount` exist and are **0%**, so defect-injection phase is not answerable.

## BLAST workflow — the active instruction

**Read `BLAST/Objective.md` at the start of every session.** Under Claude Code a hook injected it automatically; OpenCode does not run that hook, so you must read it explicitly. It is the current task — before implementing anything, write the instruction there first. Archive the outgoing objective to `docs/history/README.md` before overwriting. The full workflow is in `CLAUDE.md` §Standard workflow. `BLAST/` is **not a git repo** — edits there are unrecoverable, so archive before overwriting `Objective.md`.

## Large files — do not read linearly

Files over ~1,500 lines are likely truncated on read. Use `grep -n` to find sections first. Never read `artifacts/rag-corpus/pam-api.md` (101K lines) directly — use `python tools\rag\query.py find "<terms>"`. Run reports under `artifacts/runs/*/RUN_REPORT.md` can be 8K+ lines; get the section map first.

## Scheduled tasks

Three Windows scheduled tasks store absolute paths. If the workspace moves, re-run the registrars:
```powershell
powershell -ExecutionPolicy Bypass -File tools\obj016_register_task.ps1
powershell -ExecutionPolicy Bypass -File tools\obj017_register_weekly_task.ps1
powershell -ExecutionPolicy Bypass -File tools\jira\register_client_analysis_task.ps1
```

## Key reference files

| What you need | Read |
|---|---|
| Current task / requirement | `BLAST/Objective.md` (read explicitly — the injection hook is dead, see below) |
| Project history | `docs/history/README.md` |
| Jira analysis — the live work | `docs/analysis/D1-client-ticket-patterns.md`, then the two 2026 census reports |
| Jira ticket-raising traps | `tools/jira/jira.md` · daily review: `tools/jira/TRACKING.md` |
| Findings / defects | `docs/briefs/developer-loopholes.md`, `docs/findings/issues/` |
| Full-deployment guidance | `CLAUDE.full-workspace.md` — the reasoning behind every rule; ⛔ not its commands |
| API validation state | `docs/briefs/overview.md` ⚠️ `artifacts/runs/*/RUN_REPORT.md` is **absent** in this tree |
| Session start | ⚠️ `engage.py` needs the nested checkouts — it has nothing to do here |

⛔ **Both hooks in `.claude/settings.json` are dead** — they hard-code `E:\Omkar\Automation\Dev Project\…`,
which does not exist (the maintained workspace is `E:\Omkar\AI Projects\Dev Project`). So `Objective.md`
is not auto-injected even under Claude Code, and the `SessionStart` drift headline never fires.

🔴 **`python tools\rag\query.py find "<terms>"` is broken** — it hardcodes `tools/rag/corpus/` while
`extract.py` writes to `artifacts/rag-corpus/`. Broken upstream too, so raise it rather than patching this
copy. Until then, grep the corpus files directly (`pam-api` 2,470 pp · `pam-admin` 702 · `client-manager` 399).

⚠️ **`tools/jira/` has diverged in both directions** from `E:\Omkar\AI Projects\Dev Project`: the four
`pamit_*` modules are ~12 days newer there, while the four 2026 analysis scripts exist only here. Neither
is a superset, and there is no git to catch a stale edit — check which side owns a file before changing it.

## Conventions

- Jira project: `PAMIT`. The security finding `LH-13` (19 endpoints accept invalid tokens) is drafted but not raised — owner's call.
- `artifacts/runs/` folders are **retained forever**, never deleted.
- `docs/history/README.md` is **append-only** — never edit existing entries.
- `.claude/rules/` has path-scoped rules for automation-repo, API surface, and markdown docs.
- `pam/AutomationTesting/` **looks editable but is not** — it is a legacy hand-copy with no git link, not part of any build, and is being deleted. Never treat it as the active codebase.
