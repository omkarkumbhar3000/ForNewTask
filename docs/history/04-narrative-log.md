# Narrative Running Log (§4)

**Part of** [`../objective_original_origin.md`](../objective_original_origin.md) — the project's permanent, append-only archive. Dated long-form log of what was done, broke and was learned. Predates the no-dates rule (D17), which applies to objective records only.

⛔ Append-only. Never delete, reword or reorder an entry. Section numbers (`§N`) are the stable citation scheme and do not change when files are reorganised.

---

## 4. Running log

### 2026-07-27 — knowledge graph built

**Done:** Graphify indexed the automation repo — 17,275 nodes / 46,905 edges, from commit `9b70f457`, into
`pam_automation_bootstrap/graphify-out/`, with a `graphify` MCP server registered in the repo's `.mcp.json`.
**Learned:** suite XMLs are not indexed — Graphify has no XML parser, so suite→test-class questions still
need grep.

### 2026-07-28 — BLAST Run 1: the premise was checked, and it was false

**Instructed:** first formal objective — dynamic API validation script generation. The deliverable
requested was an *analysis*, not code.

**Done:** measured the developer repo against the declared API surface — three independent measures across
all 1,306 declared endpoint pairs and 6,866 `.cs` files.

**Learned — the finding that redirected the project:**

| Fact | Value |
|---|---|
| Declared endpoints implemented anywhere in `pam/PAM` | **48 of 1,306 — 3.7%** |
| Swagger specs shared by developers | 37 specs, 690 operations |
| Swagger ↔ `APIConfig.java` name overlap | **~6%** — two disjoint surfaces |
| Swagger operations declaring any 4xx/5xx | **0 of 690** |
| Payload helper methods requiring arguments | **0 of 1,099** |

**Outcome:** ⚠️ partially feasible. The objective's *intent* was achievable; its *stated method* — parse the
developer source — was not. A plan built on Roslyn-parsing `pam/PAM` would have failed late.

**Learned (process):** verifying the premise before assessing feasibility was the entire value of the run.

**Also 2026-07-28:** workspace standardized into five top-level folders; `approach/` frozen into
`workbench/archive/`. `GenericScheduler` locked by repeated token attempts (ISSUE-009). Two GET endpoints
stopped the IIS app pool (ISSUE-010) — the earlier runner had continued through **322 consecutive 503s**,
which is why the circuit breaker and pre-flight health probe exist.

### 2026-07-29 — chaining proven end to end (3 flows, all PASS)

**Run:** `Reports/Runs/2026-07-29_160155/` — 15 hops, 15 evidence files, zero 5xx.

**Done:** built `chain_runner.py`, a generic executor over **declarative flow JSON** — flows are data, so
generation extends them without touching the runner. Three five-level flows executed live; **UserId 1456**
and **ServiceId 25339** genuinely created and verified by independent reads. ISSUE-009 resolved — the token
failure was a stale password, not a logic fault. All scripts moved to `workbench/scripts/`; auto-delete
removed so every run keeps its own dated folder.

**Learned:**
- ⛔ **`Success: true` does not mean a write happened.** `SetServiceDetails` returns `Success: true` with
  `Message: "Already Exists"` — a no-op that scores green on both status *and* the `Success` flag.
- HTTP 200 carrying `Success: false` + `ErrorCode` captured live; `206-LC_GLD` is absent from the
  framework's `KNOWN_ERROR_CODES {201,202,203}`, so that set is incomplete.
- **Four envelope shapes on one API**, including a bare array with no envelope at all.
- **Blind `Result[0]` chaining fails** — only 19 of 34 LOBs have user groups. Flows must select by name and
  discover the id.
- `ServiceId` is a string on create and an integer on read.
- Writes are slow — creates 5.5–6.5 s. The inherited 2,000 ms SLA was read-only.

**Broke, then fixed:** PowerShell `Get-Content`/`Set-Content` corrupted UTF-8 into mojibake (PS 5.1 reads as
ANSI). **Use the Edit tool for text files.**

### 2026-07-29 (later) — full generated run: 326 flows, 1,868 calls, 870 endpoints

**Run:** `Reports/Runs/2026-07-29_181439/` — 3 h 11 m.

**Done:** built `generate_flows.py`; **323 of 326 flows machine-generated**, executor unchanged — which was
the point. 870 distinct endpoints reached (66.6%), 69 of 70 controllers.

**Learned — the headline measurement of the project:**

| | Count | Share |
|---|---:|---:|
| Calls issued | 1,868 | |
| Returned HTTP 200 | 1,688 | **90%** |
| **Genuinely passed all seven layers** | **1,204** | **64%** |

**A status-only suite would have reported this run as 90% green. It was 64%.** The 26-point gap is 406
calls, each with a retained evidence file.

Also: **135 × 404** — `APIConfig.java` declares endpoints that do not exist on the deployment. **13 of 217
creates actually inserted.** Eight distinct response shapes, four of them new. Downtime handling worked —
the environment went down three times mid-run and the runner resumed from the paused hop each time.

**Corrected:** the runner's own report said 1,200 passing hops; the true figure is **1,204** — four
bare-array responses were wrongly flagged because generated flows do not emit `envelope: false`.

**Open:** teardown stayed disabled — generated teardown bodies are not bound to the created record's id, so
running them would delete pre-existing QA data. Flow-level verdicts (296 FAIL / 30 PASS) are misleading;
**hop level is the measure to quote.**

### 2026-07-30 — the four-source merge

**Done:** `build_source_map.py` merged `APIConfig.java`, the payload helpers, the 2,470-page Confluence API
reference and `pam/PAM` models into `source-map.json`.

**Learned:** 3,194 JSON payload examples parsed, **1,654 bound to an endpoint**; 2,674 property names mapped
to C# types; **only 3 properties carry `[Required]` in the entire product**, so mandatory-ness is always
inferred, never asserted. Create coverage rose to **138 of 217 (63%)** with 27 creates unlocked by
documentation alone. Documentation binds payloads to endpoints **by page proximity**, so some bindings are
wrong — `confidence: medium` is a hypothesis, not a contract.

### 2026-07-31 — twelve evidence packs, one ticket raised

**Done:** `Developer-Loopholes/` created — 12 findings, each a self-contained Jira draft plus `EVIDENCE.md`,
`EVIDENCE.xlsx` and machine-readable `data/`, all generated from one dataset by one script so the three
cannot disagree. **`PAMIT-42744` raised** for LH-01.

**Learned:** LH-01 re-validated live — **289 of 289 calls still reproduce, 100%**. Across all findings:
108 distinct error codes against 4 documented; 9 response-shape families; 135 endpoints returning 404;
`SetStatus` exposed over GET on 49 controllers; 23 responses containing credentials; 25 responses ≥100 KB,
largest **8.0 MB**.

**Also:** `GenericScheduler` **locked again**. `POST /arcontoken` now returns
`HTTP 400 {"error":"Your account has been locked..."}`. One request issued, **no retry**. Workaround
established: supply `$env:PAM_API_TOKEN`, which `get_token()` checks first.

**Learned (method):** evidence files are redacted at capture, so a replayed body can carry
`***REDACTED***` where a value was — the redaction is over-broad and also catches booleans. This is why
LH-03's single non-reproducing call was correctly identified as a harness artefact rather than a product
fix. **Never report such a call as "fixed."**

**Open:** LH-02…LH-12 are drafted but deliberately **held**, pending the owner's validation.

### 2026-08-03 — structure clarified, instruction mechanism introduced

**Instructed:** the owner set out the intended project structure folder by folder and asked for a review;
then asked for a dynamic instruction mechanism — one file for current instructions, one for permanent
history. **Corrected the same day:** the dynamic file is the *existing* `BLAST/Objective.md`, not a new
`object.md`. A new `object.md` was briefly created and then removed; `BLAST/Objective.md` was restored
byte-for-byte from its archive copy, so no requirement text was lost.

**Decided:** D5, D6, D8, D9 above (D7 reversed).

**Done:**
- Reviewed the stated structure against disk. Confirmed accurate for Dev Project, GitLab repo, Blast,
  Developer Loopholes, Jira, Reports, Workbench.
- Deleted `demonstrate_readme.md` at the owner's request and repointed the 7 links that would have
  dangled. The mention in `BLAST/progress.md` was left in place — that file is append-only history.
- Wired `@BLAST/Objective.md` into `CLAUDE.md` and added a `UserPromptSubmit` hook so edits to it apply
  mid-session. Created this file as its append-only counterpart.
- **Hook implementation note.** `shell: "powershell"` is unusable on this machine — it requires `pwsh`,
  which is not installed (only `powershell.exe`); `jq` is absent too. The hook therefore calls
  `powershell.exe` from the default bash shell, using no `$` variables so bash cannot expand them.
  Two further faults were caught by pipe-testing: PowerShell 5.1 serialises `Get-Content -Raw` as
  `{"value":"…"}` rather than a bare string (fixed with a `[string]` cast), and console output defaults
  to ANSI, which destroys the em-dashes and `⛔` markers (fixed with `[Console]::OutputEncoding`).

**Corrected — four claims in `CLAUDE.md` were stale:**

| Claim | Reality |
|---|---|
| `POST /arcontoken` works | Account **locked** since 2026-07-31 — use `PAM_API_TOKEN` |
| "All four harness scripts" | **Eleven** scripts, including the LH pack family |
| Swagger specs cached under `Reports/SpecCache/` | That folder **does not exist** |
| `workbench/rag/` holds only administrator guides with no schemas | Also holds the 2,470-page API PDF — the best payload source available |

Also documented for the first time: the **IIS app-pool blocklist**, four undocumented top-level folders
(`Developer-Loopholes/`, `jira/`, `required-context/`, `writer/`), and the fact that `Graphify/dev-scope/`
is **marker files only, not built**.

**Open — one unreconciled figure.** How many of the 70 declared controllers are absent from `pam/PAM`:
`CLAUDE.md` said **23 of 70**; `required-context/01-Data-Gap-Analysis.md` and
`workbench/scripts/SOURCE-MAP.md` both say **54 of 70**. The two newer documents agree and cite a basis;
the 23 has no locatable citation. **Not resolved — re-measure before quoting either.** The 48-of-1,306
endpoint figure is not in dispute.

### 2026-08-03 (later) — `Objective.md` slimmed to a dynamic instruction file

**Instructed:** keep `BLAST/Objective.md` lightweight — *current active instruction only*. All historical
content moves here and is never copied back. Retire `pending-tasks-in-queue.md`; there is no separate
backlog file, and whatever is in `Objective.md` is the active work. When executing an instruction, use the
whole Dev Project — docs, reports, repos, this file — as context rather than expecting it restated.

**Decided:** D10, D11 below.

**Done:** `Objective.md` cut from ~16.5 KB / 320 lines to a small template. Its outgoing body is preserved
in §5 and the backlog in §6, both below. `pending-tasks-in-queue.md` deleted after archiving.

**Learned (mechanism):** the previous 16.5 KB `Objective.md` exceeded the hook's inline-injection
threshold — the harness spilled it to a side file and injected only a ~2 KB preview. **Keeping the file
small is therefore functional, not just tidy:** under the threshold the full text lands in context on
every prompt, which is the whole point of the mechanism.

| # | Date | Decision |
|---|---|---|
| D10 | 2026-08-03 | `Objective.md` holds **active instruction only**. Historical content lives here and is never copied back |
| D11 | 2026-08-03 | **`pending-tasks-in-queue.md` retired.** No separate backlog file — see §6 for its final contents |
| D12 | 2026-08-03 | **Standard CLI workflow adopted** — record the instruction in `Objective.md` *before* implementing; ask ambiguities as MCQ; append outcomes here. Written into `CLAUDE.md` §Standard workflow |
| D13 | 2026-08-03 | Step 2 fires on **substantive task requests only** — not questions, conversational replies, or process changes. A correction **amends** the current instruction rather than replacing it |
| D14 | 2026-08-03 | On overwrite, the outgoing objective is **always appended here first** — including objectives superseded before any work was done |
| D15 | — | **Objective Register adopted** (§0). Every archived objective carries ten mandatory fields under a sequential `OBJ-NNN` ID. Enforced by `CLAUDE.md` §Objective lifecycle |
| D16 | — | **No dates in objective records.** The sequential ID is the ordering. **Filesystem paths are exempt** — run folders are identifiers, and stripping them would break the traceability the register exists for |
| D17 | — | The no-dates rule applies **going forward only**. The existing dated log (§4) and decisions D1–D14 stay as written, honouring append-only. Register backfilled as OBJ-001 … OBJ-006 |
| D18 | — | **`CLAUDE.md` split into path-scoped rules.** Detail that applies to one area moved to `.claude/rules/*.md` with `paths:` frontmatter, loading on demand. Root file cut 523 → 387 lines. **Safety rules stay unconditional** — a rule that only loads after you open a matching file is useless for preventing the first destructive call |

---

### OBJ-007 — validation depth, mandatory-field evidence, and the `document/` deliverable set

**Instructed:** an 18-point requirement — create `document/` for all reports and workbooks, consolidating
into few files with many worksheets; analyse the 196 `MISSING ['NEW_ID']` chaining failures, the L6
read-back failures and the mandatory-field gap; document every API under positive and negative validation
with ≥5 negative scenarios each; deepen the framework's negative and positive validation; rewrite
`DBUtils`; establish whether DB validation is possible using newly supplied QA credentials; maintain
`Observations` and `Management Findings` worksheets; give ≥2 solutions per issue; pull the latest code
without losing work and **do not push or commit**.

**Decided:** D19–D23 below. Owner answered three intake questions: negative scope is **all 1,306
endpoints**, the owner supplies a bearer token rather than using the locked account, and the QA database is
**`ARCOSDB_U16SP2_WEBSM_QA`**.

**Done:**
- `document/` created — 2 workbooks (19 worksheets, ~22,600 data rows), 9 analysis reports, 17 JSON data
  files, and its own `README.md`. `workbench/scripts/obj007_build_workbooks.py` is the single writer of both
  `.xlsx` files.
- Framework: new `com.arcon.utils.validation` package — `PamEnvelope`, `ValidationLayer` (L1–L12),
  `ValidationOutcome`, `ValidationReport`, `ErrorCodeRegistry`, `DbPersistenceValidator`. `DBUtils` rewritten;
  `AutoConfigs` DB config fixed; `ApiHelper.validateResponseErrorCode` rewritten onto `PamEnvelope`.
  `PamValidationLayerTest` — 15 tests over **real captured responses**, all passing, zero network or DB access.
- Git: merged 15 upstream commits into `AI`, resolved 3 whitespace-only conflicts, preserved all WIP.
  **Nothing committed** — awaiting approval.
- Corrections applied across `.claude/rules/api-surface.md`, `workbench/developer-loopholes.md`,
  `workbench/document-gap.md`, `required-context/01-Data-Gap-Analysis.md`, `BLAST/findings.md`, and — at
  source, then regenerated — `build_source_map.py`/`SOURCE-MAP.md` and `lh_specs_run.py`/LH-05's pack.

**Learned (measured this objective):**
- **The framework's only envelope assertion could never pass.** It read `success` in camelCase; across all
  1,868 captured responses lowercase `success` occurs in **0** and PascalCase `Success` in **1,580**. Jackson
  is case-sensitive, so body-level validation coverage was not thin — it was **zero**. One inconsistent letter
  silently disabled an entire validation layer.
- **31 distinct response shapes**, not the 4–8 previously recorded; only **6** match a documented shape.
- **70** responses carried `Success:true` while writing nothing; the framework caught **0** of them.
- **The 196 `MISSING ['NEW_ID']` failures are not a harness bug.** Split: **117** creates genuinely failed,
  **19** were acknowledged but returned no identifier, **0** extractor misses, **60** indeterminate. Cause (c)
  = 0 was *proven* by two searches far wider than the extractor finding no identifier anywhere.
- **The "105 of 107 L6 read-backs failed" figure was largely a harness artifact.** 97 of 107 searched each
  response for the literal string `${NEW_ID}` and could never have passed. For **101 of 107** the run cannot
  separate "never created" from "created but not readable back".
- **On the surface under test the declared-required count is 0 of 5,175**, not 3 of 6,738 — all three
  `[Required]` attributes sit on one class in a service that is not among the 70 controllers.
- **The developer repository is the wrong one, not merely incomplete.** Twelve constraint families return
  zero, including Newtonsoft's `Required.Always` — yet the server demonstrably runs that check (123 live
  rejections). The enforcing models were never supplied.
- **The negative suite is largely non-functional and partly inverted.** 199 of 279 referenced data providers
  do not exist (650 tests fail at initialisation); all 80 that resolve read the **positive** sheets. The
  3,652-row negative workbook is declared in config and read by nothing.
- **73.4%** of a complete negative design (7,664 of 10,448 rows) has no documented expected outcome;
  **1,289 of 1,306** endpoints have zero runnable negative coverage.
- **DB validation is possible**, and the API's writes *do* land in `ARCOSDB_U16SP2_WEBSM_QA` — confirmed three
  ways. Encryption is narrow (3 table families) and the audit log is plaintext.
- **Three product security defects found incidentally:** at-rest encryption is deterministic (20,651 rows,
  59 distinct `ss_port` ciphertexts — functionally AES-ECB); `sso_ApiUsers` stores passwords in cleartext and
  `tbl_KeyEncryptionDecryption` holds an unencrypted private key in the database it protects; **16,560**
  authorisation rows reference deleted services, with only **5** foreign keys across 552 tables.
- **The `CallBack` background loop** logs ~240 errors/hour continuously, inflating the run window's error
  count from 194 to 1,736 — nine tenths of it not test-caused.
- The **58 of 70** controller-absence figure settled a long-standing contradiction: `54` was a **hardcoded
  string literal** in `build_source_map.py:333` that no code ever computed, and `23` answered a narrower
  question (recomputes as 22).

**Corrected (my own errors, within the session):** I claimed "no row on the server is newer than
2025-10-01" and inferred the QA API might not write to the supplied database. **Both were wrong** — the
newest row is `2026-08-03 15:29:18`, minutes old. The error was sampling one column in the *wrong*
databases and generalising to the instance. Withdrawn as `OBS-012`, corrected by `OBS-045`, and `MF-07`
rewritten. Retained rather than deleted so the reasoning error stays visible. Separately, `OBS-001`'s
severity was reduced from High once encryption proved narrow rather than universal.

**Open:** live execution never ran — no `PAM_API_TOKEN` was supplied, so every API-side figure derives from
`Reports/Runs/2026-07-29_181439/`. Nothing is committed. Suite migration onto the new validator, the negative
suite rewiring, and the two latent defects (`APIExcelReportUtil` race, `ApiHelper` Playwright leak) remain.

| # | Decision |
|---|---|
| D19 | **`document/` is the home for analysis deliverables**, parallel to `BLAST/`. `Reports/` keeps raw execution evidence; `document/` holds the analysis of it. Generator **scripts** still live in `workbench/scripts/` — only their output lands in `document/` |
| D20 | **One writer per artifact.** `obj007_build_workbooks.py` is the only thing that writes either `.xlsx`; agents emit JSON. Editing a workbook by hand is discarded on the next build |
| D21 | **`NOT RUN` is a first-class verdict, distinct from `FAIL` and from `PASS`.** A check that could not run is never counted as a pass, and never reported as a product failure. Adopted after finding that 97 of 107 `FAIL` verdicts in the prior run carried no information |
| D22 | **Absent evidence is written as `NOT EXECUTED — no evidence` or `UNKNOWN — contract undocumented`, never as a plausible value.** The objective's largest finding is *how much* is undocumented, and that figure only means something if nothing was filled in to look complete |
| D23 | **Fix a wrong figure at its generator, then regenerate** — never by hand-editing generated output. Applied to `SOURCE-MAP.md` and LH-05's pack. A hand edit is silently discarded on the next rebuild |

---

### OBJ-008 — `questions/`, the project knowledge base

**Instructed:** create `questions/` parallel to `BLAST/`, holding one Excel workbook that captures every
question someone might ask about the project — question, answer, evidence, comments, plus industry-standard
metadata — for demonstrations, documentation and management discussion. A living document: add new questions
as they arise. Sheet structure delegated to the assistant.

**Decided:** D24–D26 below.

**Done:**
- `questions/` with `PAM-Project-Knowledge-Base.xlsx` — 3 sheets (`Index`, `Q&A`, `Demo Flow`), 16 columns,
  **241 questions across 20 categories**. Source: three `data/questions-*.json` files (76 API · 75 framework ·
  90 project). Single writer `workbench/scripts/build_knowledge_base.py`, which **validates and fails the
  build** on a duplicate id, an unknown status, or a missing citation.
- `questions/README.md` and `_AUTHORING-CONTRACT.md`. Registered in the root `CLAUDE.md`, root `README.md`
  and `document/README.md`.
- Ten figures corrected across nine documents (below), two of them my own errors in report `B`.

**Learned:**
- **Writing cited answers is a stronger audit than reading.** Every drift found this objective had survived
  repeated readings of the same documents; it surfaced only when a row had to name its source.
- **A figure can be plural rather than wrong.** The negative-corpus row count had **five** values in
  circulation (3,167 · 3,317 · 3,652 · 3,620 · 3,728). I counted it myself and got a **sixth**. None is
  wrong — they count different things. The correct resolution was to declare the total
  **definition-dependent**, forbid quoting it bare, and quote the stable split (1,604 × 405 · 1,550 × 401 ·
  13 × 200) instead. Declaring a sixth "settled" number would have repeated the original error with more
  confidence. Same shape as payloads-bound-to-an-endpoint: 1,654 vs 1,605 differ only on how unparseable
  examples are classified, and both are right under their own rule.
- **`3` documented error codes, not `4`** — two of the four were fragments of IP addresses that the
  extraction matched as codes.
- **A documented safety rule does not protect the automated path.** The endpoint blocklist was honoured by
  every human and by the Python harness for months, and was absent from the one execution path that does not
  read documentation. **102 rows across 50 controllers** in the Java framework's positive test data target
  blocklisted action names at HTTP 200, including the two `ActivityLogs` endpoints that stop the IIS app
  pool — in the single class CI activates.
- **A root `testng.xml` arrived in the `Dev` merge**, git-tracked, listener-less, pointing at that same
  class. Both `AGENTS.md` and the repo `CLAUDE.md` said no such file existed; the merge made `AGENTS.md`
  accidentally correct and the repo `CLAUDE.md` newly wrong. A claim needs re-checking, not just a source.

**Corrected:** report `B` §2 named six validation classes and omitted `PamApiValidator`, the orchestrator its
own examples call (seven files, 1,568 lines); report `B` §6 still carried the pre-correction `L11` wording
that the database findings reversed — I wrote it before those landed and did not revisit. Also corrected:
database count **31** not 30 (`sys.databases`); source files **1,086** not 1,073; `1,322` → `1,306` in
`ISSUE-005` (superseding note); `101` → `79` creates without a body in `writer/writer.md` and
`workbench/self-understanding.md`; `8` → `31` response shapes and `4` → `3` error codes in
`workbench/document-gap.md`, `required-context/01-Data-Gap-Analysis.md` and `workbench/overview.md`.

**Open:** the `MF-16` blocklist guard is **not applied** — a framework change was outside this objective and
`OBJ-007` remains uncommitted awaiting review. Four questions stay `Open`, each naming what would settle it.
The negative-corpus counting rule needs agreeing in a script.

| # | Decision |
|---|---|
| D24 | **One master `Q&A` sheet, not per-topic sheets.** Per-topic sheets force a filing decision on every new question and let one answer live in two places. A `Category` column plus autofilter gives every per-topic view without duplicating a row; `Demo Flow` references question **IDs** so it cannot drift from the answers |
| D25 | **The build enforces citation; discipline does not.** A row without evidence is stamped `⚠️ NO EVIDENCE CITED`, forced to `Status = Open`, listed on the `Index` sheet, and **fails the build**. A question that cannot yet be answered is still recorded, with `Status = Open` and a statement of what would settle it — because the project's largest finding is how much is undocumented, and that only holds if nothing was filled in to look complete |
| D26 | **Where a figure is definition-dependent, say so and quote the stable derivative instead.** Do not adjudicate between measurements that answer different questions, and never publish an observation set as if it were a contract (why the error-code register question stays `Open` despite ~108 observed codes) |

---

## 2026-08-04/05 — The API service account is unlocked; `token_guard.py` becomes the only path to `/arcontoken`

**Instructed:** the owner supplied "updated" API service-account credentials (base64 `pam_APITokenUserName`
/ `pam_APITokenPassword`) and asked for the project configuration to be updated. Then: *"check whether you
are able to create token or not, with provided updated credentials."* Then, on the follow-ups: correct
`CLAUDE.md`, refresh `.token_cache.json`, update `ApiToken=` in `QA_MsSQL.properties`, and — *"also update
the logic. try to create a token after the 24 hours … but make sure while validating token generation part,
create only once. If you are not getting tokens, let me know. I don't want to face that issue again like the
user getting locked out."*

**Done:**

- **No credential change was needed.** The supplied values are **byte-identical** to
  `Environments/QA_MsSQL.properties:11-12`. Verified by exact-match grep, not by eye. No env file was edited
  for credentials, and the values were **not** propagated to the other 19 env files — those carry three
  different passwords for the same username, which is per-environment configuration, not drift.
- **One** deliberate `POST /arcontoken` → **HTTP 200**, 3,517 ms, `access_token` present, `refresh_token`
  issued. Claims: `APIUserId 2`, role `Default`, `nbf` 2026-08-04 11:20:56 UTC, `exp` 2026-08-05 11:20:56
  UTC (24 h, `expires_in=86399`). Executed via `run_qa_mssql.try_dynamic_token()` in isolation — `main()`
  was deliberately **not** invoked, so no endpoint sweep ran and nothing on the blocklist was touched.
- **New `workbench/scripts/token_guard.py`** — the single gate in front of `/arcontoken`. Resolution order
  `$PAM_API_TOKEN` → valid cache → **one** attempt. A failed attempt writes `.token_attempt_block.json`,
  which blocks every later attempt *in this run and all future runs* until `clear-latch` is run by a human.
  A separate per-process flag means one process cannot attempt twice even if the latch write fails. Network
  and TLS faults latch too. CLI: `status` (zero HTTP) · `refresh` · `clear-latch`.
- **`chain_runner.get_token()` and `run_qa_mssql.try_dynamic_token()` both now delegate to it**, so the
  harness has exactly one code path to the token endpoint. `run_qa_mssql`'s latch check sits *inside*
  `try_dynamic_token`, not only behind the `--try-token-gen` flag — the flag records intent, the latch
  records that an attempt already failed.
- Verified with `urlopen` monkeypatched to raise: valid cache reused, latch blocks, latch survives an
  expired cache, `clear-latch` restores permission, per-process guard holds. **0 network calls across all
  five cases.** Both harness scripts import cleanly.
- `.token_cache.json` rewritten from the token already obtained rather than by calling the endpoint again.
  `refresh_token` deliberately omitted — `try_dynamic_token` caps the recorded body at 600 bytes so the
  captured value is truncated, and nothing in the harness reads it.
- `QA_MsSQL.properties` `ApiToken=` refreshed (the previous value expired 2026-07-31 10:39 UTC) with a
  comment block recording both consequences of `ApiHelper`'s behaviour.

**Learned:**

- **The blocker was always the lock, never the password.** `ISSUE-009` is marked **RESOLVED 2026-07-29** —
  the credential was refreshed then and `chain_runner.py` generated a token successfully on run
  `2026-07-29_160155`. The value in the properties file has been correct since. The 2026-07-31 lockout
  recorded in `CLAUDE.md` was a separate, later event.
- **`ApiToken=` being populated is the only thing protecting the account from the Java suite.**
  `ApiHelper.getToken()` (`ApiHelper.java:967-993`) returns `AutoConfigs.ApiToken` verbatim when non-empty
  and only falls through to `/arcontoken` when it is blank. `getToken()` runs **per test**, so a blank value
  means **one token request per test** across a suite — the exact lockout pattern. Never blank it.
- **`ApiHelper.getToken()` never checks expiry.** An expired `ApiToken=` is returned as-is, so API tests
  fail on auth instead of regenerating — a failure that reads as a product defect.
- **The framework sends both fields base64-encoded and the server accepts that.** `password` is the 16-char
  base64 string as-is; `username` is decoded only for logging. Do not "fix" either.
- **`sso_ApiUsers` can answer the lock question with zero auth attempts** — `Is_Locked`,
  `Allowed_Login_Attempt`, `Crnt_Login_Attempt`, and a **plaintext** `Password` column
  (`document/data/db-schema-map.json`, `objects[2]`, 34 rows, `GenericScheduler` is RowId 2). DB reachable
  at `10.10.0.194:1433`. This is the right first move next time; the attempt is the fallback, not the probe.
- **The host was up throughout the lockout** — unauthenticated `GET /arcontoken` returns 405 in ~40 ms.
  Reachability proves nothing about account state; the two were conflated in the earlier write-up.

**Corrected:** root `CLAUDE.md` §"🔴 Token generation: the service account is LOCKED" stated `/arcontoken`
"no longer works" and instructed every session to avoid it. **That is now wrong** and, being auto-loaded, it
would have misdirected every future session. Rewritten as §"🟢 Token generation WORKS again", keeping the
lockout history and every safety rule — the mechanism changed from "don't touch it" to "one gate enforces
one attempt". `ISSUE-009`'s own `Reports\Scripts\run_qa_mssql.py` path is also stale; the script lives in
`workbench/scripts/`.

**Open:**

- **Not yet tested past expiry.** The owner asked for a post-24 h attempt. At the time of writing the cached
  token still had **441 min** of life (expiry 2026-08-05 11:20:56 UTC), so **no attempt was made** — calling
  the endpoint while a valid token exists is precisely what the guard prevents. The first `refresh` after
  11:20:56 UTC is the real test of the expiry path.
- **`ApiToken=` will expire and does not self-renew.** A 24 h static token in a git-tracked file needs
  refreshing before any Java API suite run. No automation was added for this deliberately — a scheduled
  refresh is a token-generation loop, which is the thing that locked the account.
- **The Java side was not changed.** `ApiHelper.getToken()` has no latch and no expiry check. `OBJ-009`
  forbids framework code changes and `OBJ-007`'s work on `AI` is still uncommitted awaiting review, so the
  Java path is protected only by `ApiToken=` staying populated. Worth a decision of its own.
- A live 24 h bearer token now sits in a **git-tracked** file (`QA_MsSQL.properties`). Consistent with the
  20 env files already holding plaintext credentials, but it is a secret entering version control.

## 2026-08-05 — Addendum: Postman parity confirmed, `refresh --force` added, expiry path exercised

Follows the entry above; corrects nothing in it.

**Instructed:** the owner generated a token by hand in Postman and shared the screenshot — *"i am able to
create token in postman manually, i hope same you are able to create without any issues."*

**Done / Learned:**

- **Method parity confirmed against the owner's Postman call.** Same URL, same `x-www-form-urlencoded` body
  with the same three keys (`username` / `password` / `grant_type`), same base64 values, same result:
  **200 OK**, `expires_in` 86399. Owner measured 3.38 s, the harness 3.517 s. There was never a discrepancy
  in method or credentials.
- **`token_guard.py refresh --force` added.** Legitimate need: generate while the current token is still
  valid, so a long run does not straddle an expiry. **`--force` overrides the CACHE, never the SAFETY** — it
  still checks the latch and still allows one attempt per process. Exercised once: **HTTP 200**, new token
  valid 2026-08-05 04:07:55 → 2026-08-06 04:07:55 UTC.
- **The generation path is now proven twice, on two different days, by two different clients.** Running total
  of live `/arcontoken` calls made by the harness across this whole exercise: **two**, both successful, no
  retry, no latch ever written by a real failure.
- **Token proven to authenticate, not merely to be issued.** `GET /api/DeviceOnboarding/GetLOBList` (read-only,
  not blocklisted) returns **HTTP 200** with a bare array of **34** LOBs, first item `{"LobId": 1, "LobName":
  "O11"}` — and **401 without the token**. The 401/200 pair is what makes it an auth test rather than a
  reachability test. It also re-confirms the documented "bare array, no envelope" shape for that endpoint.
- `ApiToken=` in `Environments/QA_MsSQL.properties` re-synced to the new token and verified byte-equal to the
  cache. Still **uncommitted on `AI`**.

**Corrected (in this session's own work, not in a prior entry):** `token_guard.py` printed `✅` / `⛔` to
stdout and the console codepage is **cp1252**, so `refresh` raised `UnicodeEncodeError` **after** successfully
writing the token — a crash with a misleading exit code on a successful operation. All operator-facing
`print()` output is now ASCII-only and asserted so. Lesson: a tool whose whole purpose is to be trusted about
a risky operation must not be able to fail while reporting success.

**Open:**

- **The genuine post-expiry path is still not exercised.** Both attempts so far ran against a healthy account
  with a valid or absent cache. What remains untested is the *failure* path — a real rejection writing
  `.token_attempt_block.json`. It has only ever been triggered synthetically (`record_failure()` in the
  monkeypatched test), never by the endpoint.
- **Possible API instability, unresolved.** One authenticated call failed with `ConnectionRefused`
  (WinError 10061) and the identical call succeeded seconds later. The unauthenticated 405 probe took
  **12.5 s** where it took **0.07 s** the previous day, and a later `GetLOBList` took 626 ms against 270 ms
  minutes earlier. TCP is open on 6302 and 1302, no proxy is set, DNS resolves to `10.10.0.120` — so this is
  server-side, not client-side. Consistent with the IIS app-pool fragility of `ISSUE-010` / `LH-08` but
  **not evidence of it**: the endpoints that would confirm it are blocklisted and were not called.

## 2026-08-05 — `OBJ-011`: the solution is made portable, and the onboarding question gets an answer

**Instructed:** the owner asked how the API dynamic-generation tooling built for PAM would be replicated on
another project — `IDEV` was named as the first target — and asked for `workbench/new-project-implementation.md`
to be reviewed and turned into a generic onboarding guide covering prerequisites, dependencies, configuration,
implementation steps, assumptions and project-specific considerations. Plus two architecture approaches with
advantages and disadvantages (**AI Skills** versus a **standard instruction document**), a comparison on
scalability / maintainability / ease of adoption / long-term support, and one final recommendation fit for
management.

**Decided (owner, clarification round):** the guide stays **project-agnostic** — nothing is known about `IDEV`
and nothing about it may be invented, so it appears as a table of `UNKNOWN`s each naming what would settle it.
**One file** carries the workflow, both approaches, the comparison and the recommendation. The scaffolding is
**built, additively** — no edits to `chain_runner.py` or `generate_flows.py`, which produced OBJ-010's
5,416-case run and stay as verified. The management asset is a **section inside the guide**, not a separate
brief or a published page.

**Done:**

- **`workbench/onboarding/` created** — 12 files. `profile.schema.json` (285 lines) is the contract;
  `profiles/pam.json` (182) is the worked example; `profiles/_template.json` (140) is what a new project
  copies; `validate_profile.py` (315) is the readiness gate; `skills/api-onboarding/SKILL.md` (107) plus six
  phase references (566) is the portable skill.
- **`workbench/new-project-implementation.md` rewritten** — 132 → 505 lines, 18 sections. Its figures were
  stale by a whole objective (it quoted the retired 326-flow / 1,868-call / 870-endpoint set); it now carries
  OBJ-010's measured numbers with a provenance table for every claim class.
- **Recommendation:** adopt the **AI Skill** as the delivery vehicle, with the document retained as its
  human-facing specification and one of its inputs — not as the mechanism. The decisive argument is that the
  recurring cost is *procedure*, and every expensive PAM mistake was an ordering failure (assertions before
  the probe, generation before one hand-written chain, a credential retry before the lockout policy was
  known), which phase gates address and prose cannot.
- Root `CLAUDE.md`, `workbench/README.md` updated: `workbench/` now has six subfolders, and
  `workbench/README.md` had been omitting `scripts/` entirely.

**Learned:**

- **The couplings are few, named and local — which is what makes the profile boundary credible.** PAM-specific
  facts in 1,806 lines of harness code reduce to eleven places: `chain_runner.py:70-76` (paths, env name),
  `:77-82` (SLA, timeout, throttle, caps), `:85-91` (blocklist, destructive regex), `:373` (health probe),
  `:398` (created-messages), `:458-480` (envelope field names); `generate_flows.py:37-40` (classification),
  `:43-66` (context/identity/keep maps), `:69-85` (the LOB prelude); `token_guard.py:170-175` (credential
  keys); and `generate_data_flows.py`'s Java parsing. Everything else is HTTP, JSON, assertion and safety
  logic that transfers untouched.
- **The whole execution path is Python standard library only.** `openpyxl` is needed for the optional workbook
  and nothing else — so the thing being onboarded has no install step, and the kit was deliberately built to
  the same standard (a hand-rolled schema check rather than a `jsonschema` dependency).
- **A schema without a gate is a suggestion.** The measurable difference between the two profiles is the
  onboarding worklist: `pam.json` exits `0` with 0 blockers, 0 warnings and 5 declared open unknowns;
  `_template.json` exits `1` with **13 blockers and 6 warnings**, each naming the question and who settles it.
  That converts "are we ready?" from a judgement call into a command.
- **The six existing `workbench/skills/*.SKILL.md` files are not reusable, for two independent reasons** —
  they are PAM-hardcoded, *and* they target the Java/TestNG bootstrap rather than the dynamic framework that
  actually produced the result. Worth knowing before anyone proposes reusing them for `IDEV`.
- **One adapter is not an abstraction.** The catalogue-adapter interface is only validated when a second
  project uses it, so the second onboarding should be expected to modify the machinery a little and the third
  should not.
- **ASCII-only operator output, applied pre-emptively.** `validate_profile.py` prints `[BLOCK]` / `[WARN]` /
  `[NOTE]` rather than status emoji, because the console codepage is cp1252 and the `token_guard.py` lesson in
  the entry above is that a tool whose purpose is to be trusted must not be able to crash while reporting
  success.

**Corrected:** `Reports/Summary/OBJ-010-Execution-Benchmark.md` states **23** endpoints accepting an invalid
token in its §1 and its §5 heading, while the classification table in that same §5 sums 34 + 4 + 19 = **57**,
of which **19** require review. `workbench/developer-loopholes.md` §13 and `LH-13` both say 57 → 19 (6 writes,
8 returning business data), so **57 → 19 is the figure to quote**. The summary itself was left unedited — it
is a completed objective's artifact and correcting it is the owner's call; the discrepancy is recorded in
`new-project-implementation.md` §17.

**Open:**

- **The scripts do not yet read the profile.** It currently *documents* the couplings rather than driving
  them. The refactor is scoped in `new-project-implementation.md` §8 as four steps, the second of which is a
  PAM parity re-run diffed against `results.json` — provable from retained evidence, zero product risk.
- **`probe_to_profile.py` is the highest-value remaining build** and is small: it would emit the `envelope`
  section of a profile directly from a probe run, removing the last hand-transcription step in onboarding.
- **Every `IDEV` fact.** All ten rows of the readiness table are `UNKNOWN`. Nothing can be estimated for
  `IDEV` beyond its *shape* — materially less work than PAM required, concentrated in one risk (payload
  availability) rather than many — until the day-one questionnaire comes back. Deliberately no date is quoted:
  Phase 0–1 exists to produce a costed go/no-go, and quoting ahead of it would be a guess wearing a number.

---

## OBJ-013 — the closed loop: rescan, pull, ingest, and keep it that way

**Instructed.** "Build a robust, closed-loop system in which every file stays configured and updated
automatically." Four action items: rescan every file and script for pending updates; pull the latest code
from both repos, **pull only, never push**; ingest anything new into the RAG; close the loop so it keeps
doing this unasked. Ship as `v0.1`.

**Decided (owner, two clarification rounds).** Q1 trigger: a Claude Code `SessionStart` hook, no scheduler.
Q2: **fetch only** — do not touch `AI`. Q3 RAG scope: the three PDFs plus workspace evidence, **not** the
Java source (Graphify indexes it) and **not** `pam/`. Q4: auto-fix mechanical facts only, prose reported.
D1: auto-fix confined to six guidance files, widen later. D2: `facts.json` with explicit multi-basis facts.
D3: **`pam_automation_bootstrap/CLAUDE.md` is authoritative**, importing `AGENTS.md` as its appendix.
D4: waivers keyed to the evidence hash so they expire when the measurement moves.

**Done — pulls.** `pam/` fast-forwarded `e278fd399` → `12234f037` (106 commits, 142 files, tree left clean,
**0 changes to `AutomationTesting/`**). The automation repo's local `Dev` was fast-forwarded `9b70f45` →
`365050d` **via `git fetch origin Dev:Dev`, without a checkout**, so `AI`'s 98 uncommitted files and its one
stash were never at risk. Nothing was pushed or merged.

**Done — rescan.** Eight parallel domain audits, every finding then adversarially verified by a skeptic
instructed to refute it. 192 raw → **180 confirmed, 12 refuted** (7 double-counts, 4 auditor errors, 1 out
of Q3 scope). 19 critical · 61 high · 74 medium · 26 low; 82 fully machine-fixable.

**Done — built.** `obj013_probes.py` (18 probes, read-only, refuses state-changing git) ·
`workbench/.drift/facts.json` (registry + 7 invariants) · `obj013_scan.py` · `obj013_fix.py` ·
`obj013_loop.py` · `obj013_rag_ingest.py` (45 sources → 576 sections in `corpus/workspace.jsonl`) ·
`requirements.txt` · `SessionStart` hook · `permissions.deny` for push/merge.
Drift went **13 open → 3 open, 23 clean**; 8 mechanical corrections applied with backups.

**Corrected — five documented facts were wrong and are now fixed by measurement:** graph
17,275→**17,293** nodes and 46,905→**49,193** edges; `AGENTS.md` communities 865/808/57→**848/773/75**;
`ApiHelper.java:971`→**967**; `Prepare-1.pptx` "10-slide"→**8**; pam-scope report 13,312→**13,313**.

**Learned — four things measurement found that no document recorded.**

- **`BLAST/Objective.md` was reaching context twice and the copies disagreed.** The `@`-import in
  `CLAUDE.md` resolves once at session start; the `UserPromptSubmit` hook stays live. Observed directly:
  after the objective was rewritten mid-session the import still served the superseded one. The import is
  removed; the hook is the single live path, and `governance.objective_single_injection` now watches it.
- **The graphify git hooks rebuild a different repository.** `graphify-out/.graphify_root` names
  `C:\Users\omkar.kumbhar_pam\git\pam_automation_bootstrap`. `post-commit`/`post-checkout` are installed and
  executable, so every triggered rebuild scans that tree — which is why the graph here has never refreshed
  and predates the entire `com.arcon.utils.validation` package it tells agents to use. `v0.1` has no code
  path that rebuilds; it raises `REFUSE_REBUILD`.
- ⛔ **Two harness scripts broke the deny-by-default invariant both files assert.** `run_qa_mssql.py` had
  **no `--execute` gate** — a bare run swept the live GET surface — *and* was the only one of four blocklist
  copies missing `GetAllActiveUserDetails`. `run_validation.py`'s `--dry-run` did not suppress network at
  all: `fetch_specs()` ran before the dry-run branch and opened sockets to 38 spec URLs across four live
  hosts. Both fixed; a socket-interception test now proves a bare run issues **zero** HTTP calls.
- **The `jira` package was never a dependency.** `jira_client.py` is hand-rolled on `urllib`. The real set
  is five: `openpyxl`, `python-pptx`, `xlrd`, `pypdf`, `jsonschema`.

**Learned — two design lessons from building the writer.**

- **Applying several edits to one file must go highest-offset-first.** Ascending order shifts every later
  span; the hash precondition then refuses them — safe, but it silently halves the work. Caught because the
  7th of 8 edits refused rather than corrupting `CLAUDE.md`.
- **A partial fix can be worse than none.** Correcting `865 communities` while leaving `(808 named, 57 thin)`
  on the same line would have made a wrong line *look* verified. A fact must own every number in the claim
  it governs.

**Open.**

- **`api.endpoint_count` is deliberately `report-only` and must stay that way until the rule is settled.**
  The derivation gives 1,302 strict / **1,308 loose** — and the loose basis reproduces the documented 1,308
  exactly — but the canonical **1,306** comes from a rule nobody wrote down. **Keep quoting 1,306.**
- **3 invariants remain open by design:** the graph is stale and cannot be rebuilt from here
  (`.graphify_root` points elsewhere — owner's call), and 4 dead viewer/deck pointers remain in `AGENTS.md`
  and on disk.
- **177 of the 180 confirmed findings are not yet fixed.** `v0.1` mechanised the 8 that were registered
  facts; the rest are in `workbench/.drift/register.json` awaiting either registry entries or a human.
- **`AI` is untouched** — 98 uncommitted files, 1 stash, 11 commits behind `origin/Dev`, still awaiting the
  owner's merge decision. The only conflicting file is `Environments/QA_MsSQL.properties` (keys `ApiToken`,
  `password`).

---

## 2026-08-12 — `OBJ-015`: the management dashboard, and three numbers that were wrong

**Instructed.** Build a small, lightweight React app giving a graphical view of everything completed —
execution results, benchmarks, previous-vs-current comparison, trends, findings, improvements, project
information, execution history, and a report per execution date. Management-facing, white theme, no fake
numbers, `N/A` where data is absent, and inspect the workspace first rather than asking for data again.

**Decided.**

- **`workbench/react/` is the home**, not a new top-level folder. It had been reserved for exactly this
  since the 2026-07-28 standardization and had asked, in its own README, for commands to be recorded there.
- **A build-time JSON snapshot, generated by a script.** A Vite dev server cannot read outside its root and
  a backend was excluded, so `obj015_build_dashboard_data.py` reads the artifacts and emits
  `src/data/*.json`. Presentation never touches a source file; `services/dataService.js` is the only module
  importing the data.
- **No `react-router`.** Six views and one parameterised route do not pay for a dependency, and hash
  routing is what lets the built `dist/index.html` open from disk during a demo.
- **The run workbook is the source of truth, not `results.json`.** Where both could answer, the authored
  workbook wins — re-deriving a figure that already exists just invents a second answer.

**Done.** Six views (dashboard, benchmark, history, projects, findings, per-run report), 14 datasets, a
generator that verifies itself against the workbook's own `Summary` sheet on ten figures and exits non-zero
on mismatch. `npm install` → `npm run dev` verified; production bundle builds at ~57 KB gzipped for the app
plus ~156 KB for Recharts. All six views were opened in a browser and inspected.

**Learned — three numbers that were wrong, and how each was caught.**

- ⛔ **Endpoints reached ÷ endpoints declared is not coverage.** The Projects page rendered
  **"1,388 of 1,306 — 106.3%"**. Measured the overlap rather than papering over it: of the 1,388 endpoints
  run N reached, only **1,140** are declared in `APIConfig.java`; **248** exist only in the QA team's Excel
  corpus. True catalogue coverage is **1,140/1,306 = 87.3%**. N-1 was a clean subset (870 of 870), which is
  why this never surfaced before. **Caught only by looking at the rendered page.**
- ⛔ **A resumed run's own metadata undercounts it by 234 minutes.** `meta.elapsed_s` covers the last
  process only — 94.9 min against a true 329.1. `segments.json` exists precisely for this; every duration
  now carries a `durationBasis` naming its source.
- ⛔ **`results.json` has no hop verdict field.** The verdict is the AND of the check layers, and a hop with
  no checks was *withheld* — never a pass, never a fail. The derivation was accepted only once it
  reproduced the published 3,459/1,957/14 and 1,200/668/5 exactly.

**Learned — two more worth keeping.**

- **The scenario dimensions cannot be re-derived from the expected status code.** A plausible attempt missed
  the published split by up to 54 cases. `Hop Results.Scenario` in the workbook is authoritative.
- **Colour is computable, so it was computed.** Two intuitive schemes failed the validator: green-vs-red for
  pass/fail (ΔE 4.1 under deuteranopia — the classic red/green trap) and red/amber/yellow as three adjacent
  severity fills (yellow leaves the lightness band; yellow↔amber normal-vision ΔE 13.6, under the 15 floor).
  Hence **passed is blue**, and severity is a single-series bar with the tier named on the axis. Status
  colour survives only as a small dot beside ink text.

**Open.**

- **The "trend" line is a comparison.** Two full executions are retained, so the success-rate line over time
  is thin by construction. It earns its name as more executions land.
- **Per-module and performance breakdowns exist for run N only** — `obj010_build_workbook.py` never ran
  against N-1. Running it there would backfill them and make the benchmark's module view two-sided.
- **One project.** Only `workbench/onboarding/profiles/pam.json` exists; the selector and per-project shape
  are built so a second is a data change, not a redesign.
- **The sub-900 px layout was verified by container constraint, not visually** — the browser window would
  not resize below 1920 px in that session. Clean to 760 px; a single-column fallback was added below 620 px.
- **8 data gaps are listed in `src/data/gaps.json`** and shown on the dashboard under *Data coverage*, each
  with why it is missing and what would close it. *(Path superseded by `OBJ-016`: the datasets moved to
  `public/data/` so they can be fetched at runtime.)*

---

## 2026-08-12 — `OBJ-016`: the automation that was believed to exist

**Instructed.** The owner asked, as a statement of fact, whether the system already polled both repos
daily, updated everything, and fed the React app in real time. It did not. Asked to build it: daily code
pulling, update everything, dynamic data for the React application.

**Corrected — three claims, all false, all checked rather than argued.**

- **No daily polling.** No Windows scheduled task referenced the workspace, a git pull, or any `obj0*`
  script; the only tasks on the machine were WPS Office's. `CronList` returned "No scheduled jobs".
- **No recent pulls.** `FETCH_HEAD` on both repos was dated **10 Aug ~12:56** — the manual `OBJ-013`
  pull, two days earlier. The drift loop is explicitly *pull only* in the sense of reading local refs.
- **No real-time anything.** Zero `fetch` / `XMLHttpRequest` / `WebSocket` / `EventSource` in `src/`.
  Every dataset was bundled into the JS at build time.

**Decided (owner, by MCQ).** Pull and refresh daily but **do not execute the API suite** — fresh source
changes no KPI, and a daily 5.5 h run against an environment that lost 85 of 329 minutes to app-pool
downtime would generate a daily false alarm. Dashboard data **fetched at runtime**, refresh-to-update.
Refresh scope left to the assistant: drift **check** yes, RAG index yes, dashboard data yes; drift
**auto-fix no** (it writes the auto-loaded governance files, in folders with no git history) and
knowledge-base/workbooks no (neither depends on a pull, and the KB build fails hard on an uncited answer).

**Done.** `obj016_daily_refresh.py` (six steps, deny-by-default, per-step status, structural git
allow-list), `obj016_register_task.ps1`, the `PAM-Dashboard-Daily-Refresh` task at 08:30 with
`StartWhenAvailable`, datasets moved to `public/data/`, `dataService.js` rewritten as an async bootstrap
keeping selectors synchronous, and a freshness stamp plus failure banner so a broken job is visible on
screen. `pam/` fast-forwarded `12234f037` → `a6a7620b1` (+6.4 MB of packfile); the automation repo was
fetched only and reported `AI` 0 ahead / **15 behind** `origin/Dev`, untouched.

**Learned — the scheduler is a different environment, and that is where it broke.**

- ⛔ **The first scheduled run exited 1 while the same command by hand exited 0.** Task Scheduler gives a
  child Python **no console**, so it takes the ANSI codepage for stdout and dies on the `⛔` these scripts
  print: `UnicodeEncodeError: 'charmap' codec can't encode character '⛔'`. Fixed by forcing
  `PYTHONUTF8=1` / `PYTHONIOENCODING=utf-8` on every child. **A scheduled job verified only by hand is
  not verified.**
- ⛔ **PS 5.1 reading BOM-less UTF-8 as ANSI is a *parse* failure, not mojibake.** An em-dash becomes three
  cp1252 characters ending in `U+201D`, which PowerShell accepts as a string delimiter — an unterminated
  string that killed the whole registration script. `obj016_register_task.ps1` is now 7-bit ASCII by rule.
  Same trap `markdown-docs.md` records for `Set-Content`, on the reading side.
- **A step reported "ok" when its output could not be parsed.** That is the job lying to itself; it now
  fails, because not learning the drift state is not success.
- **`cache: 'no-store'` is the mechanism, not a detail.** A cached `runs.json` after a regenerate is
  indistinguishable from nothing having changed.

**Open.**

- **Execution is still manual** by explicit decision, so the headline KPIs move only when someone runs the
  suite. A weekly execution was offered and declined; revisit if the benchmark needs to roll forward.
- **The task fires only while this user is logged on** (`LogonType Interactive`, to avoid storing a
  password). A machine off for several days catches up in one run, not one per missed day.
- **`AI` is 15 behind `origin/Dev` and unmerged.** The job reports the number daily and will never act on
  it — 98 uncommitted files and 1 stash still await the owner's merge decision.

---

## 2026-08-12 — `OBJ-017`: the weekly execution, and the hardcoded constant that would have made it pointless

**Instructed.** Implement a weekly execution schedule, every Sunday at 10:00.

**Decided (owner, by MCQ).** One token attempt after a health probe, latched (**D24**). Full suite
inside a 6-hour budget (**D23**). One automatic resume on abort, then stop (**D23**).

**Done.** `obj017_weekly_execution.py` — nine steps, deny-by-default with **no HTTP at all** in a dry
run — plus `obj017_register_weekly_task.ps1` and the `PAM-Weekly-API-Execution` task, next firing
16 Aug 10:00. Rewrote the dashboard generator's run resolution. Added a *Weekly execution* panel and
`execution.json`.

**Learned — the fix nobody asked for was the one that mattered.**

- ⛔ **`RUN_N` and `RUN_N1` were hardcoded string literals in `obj015_build_dashboard_data.py`.** A
  weekly execution would have written a new run folder every Sunday while the dashboard went on
  reporting `2026-08-05_114315` as current — a system that runs forever and never changes a number.
  Now resolved from disk: newest substantive run is N, the one before it is N-1. **Automating a step
  means checking what downstream consumes it.**
- ⛔ **Authored analysis is not a property of the API.** The trend line and the three headline findings
  (1,022 · 19 · 85 min) were measured in one execution. Once N can move, reattaching them to a new run
  would assert measurements that run never produced — so they are pinned to `AUTHORED_ANALYSIS_RUN`
  and withheld, with the UI saying "analysis pending", when N is a run nobody has analysed. Proved by
  test: with N pointed at an unanalysed run, headlines drop to 0 and trend to `''` while every measured
  KPI stays intact.
- ⛔ **`chain_runner` acquires the token BEFORE its own `--wait-for-env` probe**, and that probe needs
  the token — so its wait cannot protect the credential. The agreed "probe first" policy therefore
  needed a separate unauthenticated pre-flight in the weekly job. **Reading the order of operations
  mattered more than reading the flag list.**
- **The pre-flight hits `/`, not an API action** — no credential, nothing on the blocklist, and a dead
  application pool still shows up, because it answers 503 for the whole site.
- **A monkeypatched test beat a real one.** Proving the latch guard with the real
  `.token_attempt_block.json` risked leaving it behind and blocking every future run. Pointing the path
  at a temp file proved the same thing with no blast radius — and exposed a real fragility,
  `Path.relative_to` raising inside the error-reporting path.
- **The scheduler path was validated without executing anything**, by registering a temporary task that
  ran the dry run: exit 0. That is the check `OBJ-016` learned to do the hard way.

**Open.**

- ⛔ **The weekly execution has never actually run.** A 5.5 h live run was not launched, because it was
  not asked for. First real proof is Sunday 16 Aug: watch that it finishes inside the 6-hour budget,
  that the resume path behaves if it aborts, and that the new run becomes N with the previous as N-1.
- **`AUTHORED_ANALYSIS_RUN` is a manual pointer.** After each weekly run someone must author an analysis
  and update it, or the dashboard will correctly — but permanently — say "analysis pending".
- **Both tasks fire only while this user is logged on** (`LogonType Interactive`, to avoid storing a
  password).
- **Token exposure is now once a week rather than never.** D24 records the trade and its three
  mitigations. If `GenericScheduler` ever locks again, the weekly task is the first thing to disable.

## 2026-08-14 — `OBJ-018`: performance testing arrives, and the endpoint everyone would have picked was wrong

**Instructed.** Build an industry-standard k6 performance capability for the login journey in three
integrated phases — browser/UI, HTTP/API, and correlation that locates the bottleneck. One framework,
not three scripts. Reuse what exists; invent no load figures; never hardcode a credential.

**Decided (owner, by MCQ, before any implementation).** `performance/` lives in the automation repo on
`AI` — the only versioned option and the only editable code location. **Build only, zero HTTP** this
pass. Dedicated performance credentials to be supplied later as environment variables; until then the
framework fails fast and the effective ceiling is 1 VU.

**Done.** A 14-file `performance/` tree: two k6 phases, a Node correlation engine with its own
mutation-tested self-test, a shared workload/threshold/identifier core, and a dry-run-by-default
PowerShell orchestrator. `.gitignore` was updated *before* the tree existed. The repo `CLAUDE.md` and
the root `CLAUDE.md` both record what it is and that running it is a separate decision.

**Learned — the finding that shaped the whole design.** The two authentication mechanisms are
independent. `:1302` validates a human against Active Directory and mints its own JWT into the
HttpOnly `_AT` cookie (`frmLoginACMO.aspx.cs:6398-6426`); `:6302` `/arcontoken` is a password grant for
a registered API client in `sso_ApiUsers`. The web app is a *consumer* of the second, server-side, with
its own APP001 account — the browser never sees it. So Phase 2 targets `POST /frmLoginACMO.aspx`, not
`/arcontoken`. Had it targeted the obvious endpoint, Phase 3 would have subtracted a machine token
grant from a human login and reported the difference as browser overhead. It also means this objective
carries **no `GenericScheduler` lockout exposure at all**.

**Learned — three product facts that decide whether this can ever run.** `sso_arcos_config aps_id 55`
("Use Secured ARCOS Login Validation"): if enabled, the server reads machine details from an in-process
registry only the local PAM agent populates, and **no headless client can log in** — Phase 2 becomes
impossible as designed. `aps_id 33` at its shipped default of `0` means a lockout has **no duration and
no auto-unlock**. `aps_id 49` rejects the (N+1)th concurrent login for one account, so a multi-VU run
above the cap measures the cap. All three are `IF NOT EXISTS`-seeded, so the live values are genuinely
unknown and one read-only `SELECT` settles them.

**Learned — the login form discards `fill()`.** The visible password box never holds the real password;
a `keydown` handler accumulates it into a hidden field. Any driver that sets `.value` directly posts an
empty password and every login fails with "Invalid Login Details" regardless of the credential. The
Java suite is correct only by accident of style.

**Learned — a self-test that cannot fail is worse than none.** The first version passed all 14
assertions with **7 of 8 rules deliberately broken**: every fixture sat above the sample threshold, one
of four joinability rules was covered, and a grade assertion accepted a two-element set. Rebuilt to 36
assertions and mutation-tested — 12 of 12 mutations now caught. **Mutation survival is the measurement;
assertion count is not.**

**Learned — a PowerShell safety gate that only worked with two failures.** An unwrapped pipeline
returning a single `[pscustomobject]` has no `.Count`, so `$blocked.Count -gt 0` evaluated `$null -gt 0`
= `False` and the refusal went inert on exactly one failed prerequisite — including the case where the
operator had set `PERF_USERNAME=GenericScheduler`. Reproduced on PS 5.1.26100.8894, fixed with `@()`,
and re-measured.

**Learned — adversarial review paid for itself.** Six lenses raised 33 defects. Two would have made
Phase 1 fail on *every* iteration: no TLS suppression against the self-signed QA certificate, and the
domain dropdown selected by value when the product binds the name as the option *text*. One meant a
locked account would never be detected — the matcher used the resource **key** (`TheUserisLockedOut`)
rather than any string the product renders. The same review independently confirmed the WebForms
postback contract — field naming, `__EVENTTARGET`, the omitted `__EVENTVALIDATION`, and the
XOR-with-key-0 identity trick — as correct.

**Open.** Never executed. Blocked on: dedicated credentials confirmed free of any second factor, k6
installed, the five `sso_arcos_config` values, and an environment decision (`Objective.md` says
QA_MsSQL, but two dedicated perf environments already exist in the repo and the k6 skill says never to
load-test a shared functional environment). Per-VU accounts are deliberately unimplemented.

## 2026-08-14 — `OBJ-019`: Login + Sanity, the dashboard ships, and the credential validation locks an account

Full record in `01-objective-records.md` (OBJ-019); resumable state and the credential blocker in
full in `workbench/.perf/OBJ-019-STATE.md`. The short version:

**Decided (owner, by MCQ).** Branch `Dev` (fast-forwarded to `origin/Dev`, which already contains all of
`AI` — local `Dev` was 11 commits stale). Environment `QA_MsSQL` for both (`QA_MSHKL` in §16/§17 is a
typo). Load ceiling **3 VUs** on the shared accounts. "Theme 1" = the existing `react/src/theme.js`.

**Done.** Extended the k6 framework from login to Login + Sanity: the 14-module / 211-check Sanity scope
generated from `DevOpsSanityCheck` (not guessed), a browser sweep, an API backbone scenario, and a
per-module UI-vs-backend correlation. Installed k6 v2.2.0 and verified the whole framework loads in it
with the guard firing (zero HTTP). Built the second React dashboard (`workbench/react-performance/`, six
views, browser-verified on :5174) in the same Theme 1 language, with run docs for both apps. Java still
compiles; zero `.java` touched.

**Learned — the hard one.** Validating the owner's credentials the safe way (real postback, one attempt
per combo, fresh session each time) still **locked `auto_adminui`** — the account the functional suite
depends on. The first attempts returned *invalid* (so it was unlocked); a later one returned *locked
out*. The live lockout threshold was low enough that the fresh-session protection discovery had promised
did not hold. The unknown `aps_id` lockout values were not a footnote — they were the thing that bit.
Stopped immediately; `GenericScheduler` untouched. None of the four supplied combinations authenticated
anyway (`arcosadmin` is a Perf-environment account, not QA_MsSQL).

**Also learned.** k6 doesn't create its output directory (a run does all its work then fails to save —
fixed in the orchestrator). The live product probe turned OBJ-018's last unverified assumptions into
measured facts (field names, `__EVENTVALIDATION` absent, `ARCOSAUTH` as option text). Recharts needs
`isAnimationActive={false}` under StrictMode. And the API dashboard was "reviewed" by reusing its
components verbatim — the strongest statement that they are sound.

**Open.** Live execution, gated on an owner action: unlock `auto_adminui` or provide a dedicated perf
account, then run and ingest. The dashboard shows clearly-flagged SAMPLE data until then; the Sanity
scope in it is real.

## 2026-08-18 — `OBJ-019`: the 3-user sanity execution lands, and the dashboard was about to show invented numbers

**The credential was never the problem.** `Objective.md` recorded `arcosadmin` as non-authenticating on
`QA_MsSQL` with "both case variants exhausted". The owner reported a successful manual login, authorised
one verification, and run `2026-08-18_115054` (browser, 1 VU, 1 iteration) returned
`successfulLogins: 1`, `rejections: {}`, 3/3 checks, HTTP 302 to an authenticated landing page. The
recorded conclusion was a **false negative produced by the Phase 2 raw postback**, which is defective.
Lesson: a negative result from one code path is evidence about that path, not about the credential —
and the archived credential table had been read as if it were about the account.

**Three Phase 2 hypotheses were eliminated from source with zero login attempts spent**, which matters
because failed attempts are the scarce resource on a shared account: the domain scrape already prefers
an exact text match on `ARCOSAUTH`; `DecodeFromBase64(data, key)` is a **pure XOR despite its name**,
with no base64 step; and the server decodes with the **posted** key, so `0` is a legitimate identity
transform. The surviving candidate is that the harness posts `enteredPassword` **empty** where the real
browser posts `XXXXXXXXXXXXXXXXXXXX`. Untested — it costs an attempt.

**A rejection storm, then a clean run.** A 10-iteration baseline hit the circuit breaker after 3
consecutive rejections classified `unknown`. `guard.js` already documented `sso_arcos_config aps_id 49`
(*Max Session(s) Per User*) and the classifier already matched "Maximum Session Limit Exceeds" — and the
rejections matched **none** of the five known messages, so it was neither a session cap nor a lockout.
Graded `Requires further investigation`; a diagnostic that logs the actual message was added, costing no
extra attempt. 2.5 h later, with `context.close()` teardown added, 3 concurrent users authenticated 3/3.

**Run `2026-08-18_142809` — the first real performance measurement this project has produced.** Sanity
journey, `concurrent3` profile, 3 VUs, `MSSQL_Build35.8`. Authentication is **97.6 % of the login
journey** (med 7,267 ms of 7,448 ms). Against the 1-user run, authentication degraded **+35.5 %** and
navigation **+37.9 %** at 3 concurrent users — `Observed`, but n=1 vs n=3, so directional only.
`Manager` (p95 6,714 ms) and `Reports` (p95 4,643 ms) are genuinely slow module loads.

⛔ **Coverage is 3 of 13 modules, and that must be quoted rather than "the sanity suite".** An unhandled
30 s navigation timeout on `Session Monitoring` ended the iteration in all three VUs. Because modules
sweep in a fixed order the unmeasured set is a **suffix, not a sample**, and no run can currently exceed
4 modules. The dashboard therefore reports three distinct states — measured · failed · never-attempted —
because collapsing "never attempted" into either pass or fail is what would misrepresent the run.

⛔ **The dashboard was one command away from showing management fabricated latencies.**
`build-performance-data.mjs` documented `INGEST_RUN` in its header, and **nothing in the file read it**:
it hardcoded `SAMPLE = true` and emitted seeded pseudo-random numbers. The `OBJ-019` record had logged
step 17 as complete ("generator + ingest path"), so the gap was invisible from the audit trail. Real
ingest is now implemented and runs last, overwriting, so measured and illustrative figures cannot
coexist. `api` and `comparison` are written `not-measured` rather than filled, because Phase 2 never ran.
**Lesson: a documented mechanism is not an implemented one — grep for the env var, do not trust the
header comment or the completed-step record.**

**Also fixed:** a pre-existing credential leak — two passwords in cleartext across 6 occurrences in
`workbench/.perf/OBJ-019-STATE.md`, in the file whose own header forbids exactly that. Redacted,
preserving which variant was tried.

---

## 2026-08-18 — OBJ-022: the SCA report named the wrong file, and the fix had already been reverted once

**Instructed.** Remediate the developer's dependency-vulnerability findings — but verify the submodule
architecture first and **do not assume `AutomationTesting/pom.xml` is the active source.** Full
remediation approved after review, branch `Dev` from now on, Maven permitted.

**Decided.** `D25` branch `AI` → `Dev` · `D26` Maven permitted for dependency validation · `D27` full
remediation over the three-item minimum-risk subset.

**Learned — the owner's instinct was right, and the reason is stronger than "the path is stale".**

- `pam/AutomationTesting/pom.xml` is **part of no build**: no Maven step in `pam/jenkins-pipeline`, no
  reference in `pam/.gitlab-ci.yml`. Only a dependency scanner sees it. It is a stale hand-copy — 1,064
  `.java` against 1,084 active — and **functionally identical** to the active pom: a full diff yields one
  addition (`jakarta.mail`). So every finding applied, to a different file than the one reported.
- ⛔ **The fix had already been applied and silently reverted.** `pam` commit `0520b6b79` ("Fix remaining
  SCA findings: AutomationTesting deps") remediated all six dependencies; `e278fd399` ("added automation
  code") bulk-copied the bootstrap tree over it and **reverted all six line for line**, additionally
  introducing `poi-scratchpad 5.2.5` and `pdfbox 2.0.30`. **Root cause: the fix went to the delivery copy
  while the source of truth stayed vulnerable.** This is the measured argument for the submodule model,
  and it also handed us five of six target versions already chosen and accepted by the developer.
- **The developer's report was wrong in both directions.** Of 6 reported findings, **2 are not Maven CVEs
  at all** — OSV returns zero advisories for `playwright:1.45.1` and `poi:5.3.0` (the POI one is
  misattributed from `poi-ooxml`). And **6 real findings were missed, including all three CRITICALs**.
  Full census: **85 resolved artifacts, 12 vulnerable, 25 advisories — 3 CRITICAL, 10 HIGH, 12 MODERATE.**
- ⛔ **The worst item on the classpath was absent from the report entirely.** `jxl:2.6.12` drags in
  `log4j:log4j:1.2.14` — EOL, **6 advisories, `fixed_in: NONE` on all of them** (CVE-2019-17571,
  CVE-2022-23305, CVE-2022-23307 CRITICAL; CVE-2021-4104, CVE-2023-26464, CVE-2022-23302 HIGH). One
  `<exclusion>` removed it. Verified safe *before* excluding, not after: `jxl/common/Logger` resolves its
  impl by `Class.forName` on a `logger` system property, catches `ClassNotFoundException`, and falls back
  to `jxl.common.log.SimpleLogger` **shipped inside the jxl jar** — and 0 of 1,084 sources import
  `org.apache.log4j`. Confirmed at runtime: the fallback logger is what loads.
- **Playwright's MEDIUM is an embedded Node runtime, not a Maven CVE.** `driver-bundle-1.45.1.jar` holds
  1,710 entries including **five complete Node.js binaries** (~456 MB uncompressed) plus
  `playwright-core 1.45.3`; version strings in `driver/linux/node` resolve to **`node-v20.14.0`**. That is
  why the scanner offered no fixed version — there is no Maven advisory to fix, only a newer bundle.
- ⛔ **`commons-io` was a trap that compiles clean and fails at runtime.** POI 5.4.1 requires commons-io
  2.18.0 and POI 5.5.1 requires 2.21.0, but the pom **pinned commons-io 2.16.1 directly**, so
  nearest-definition would have won and POI would have run against 2.16.1 → `NoSuchMethodError` at
  runtime, invisible to `test-compile`. Both had to move in the same change.
- **One bump fixed two findings.** POI 5.5.1 → commons-compress 1.28.0 → **commons-lang3 3.18.0**, exactly
  the CVE-2025-48924 fix version.
- ⛔ **The developer's own earlier choice was still vulnerable.** `jackson-databind` **2.22.0** carries
  GHSA-5gvw-p9qm-jgwh and GHSA-5jmj-h7xm-6q6v. Used **2.22.2**. Also worth noting no 2.19.x or 2.20.x fix
  exists at all — the minimum forward fix from 2.19.1 is 2.21.4, so a patch-level-only policy would have
  failed here.
- **Removal beat upgrading for three dependencies with zero usages** — `org.json` (HIGH CVE-2023-5072; all
  JSON goes through Jackson), `influxdb-client-java` (dropped 14 artifacts including kotlin-stdlib
  1.6.20), `pdfbox` (only a commented-out block at `AcmoHelperPage.java:2105`).
- ⚠️ **Reachability and severity are different questions, and conflating them would have mis-ranked the
  work.** None of the five log4j advisories are reachable through `src/test/resources/log4j2.xml` — it is
  Console + PatternLayout only, with no XmlLayout, Rfc5424Layout, SocketAppender or MapMessage JSON. The
  jackson CVEs concern polymorphic typing, records and `InetSocketAddress`; the code uses plain
  `ObjectMapper`/`ObjectNode`. Upgraded anyway because the cost was near zero — but the *scan's* severity
  ordering was not the *real* risk ordering, and the CRITICALs it missed were.

**Corrected — two of my own errors, both worth recording because both were method failures.**

- ⛔ **`poi-scratchpad` is used, and I removed it.** My search looked for `import org.apache.poi.hslf|hwpf`
  and the string "scratchpad" and found nothing. `AcmoHelperPage.java:2343` uses
  `org.apache.poi.hwpf.HWPFDocument`, `usermodel.Range`, `usermodel.TableIterator` and `usermodel.Table`
  **fully qualified inline**, with no import. The build failed with "package org.apache.poi.hwpf does not
  exist". **Lesson: an import-only search does not prove a dependency is unused — search for
  fully-qualified references too.** Restored on `${poi.version}`, which also fixed the pre-existing
  version mismatch (scratchpad 5.2.5 against poi 5.3.0). The same corrected search then found
  `com.mysql.cj.jdbc.Driver` at `DBUtils.java:88` — a string literal, so no compile dependency.
- ⛔ **`mysql-connector-j` should not have been removed either, and evidence found mid-task changed the
  plan.** `Environments/demo.properties` is configured for **MySQL** — `db_port = 3306`,
  `databaseName=myvaultdb` — and is the one env file with **no `db_type` key**, so `buildJdbcUrl` defaults
  it to mssql and builds `jdbc:sqlserver://…:3306` against a MySQL server. That is a **pre-existing
  defect** (recorded, not fixed here), but it means the capability is intended and removal would make it
  unfixable by config. **Upgraded 9.0.0 → 9.7.0 instead**, which pulls protobuf-java 4.31.1 and clears
  CVE-2024-7254 without dropping the driver. Better outcome than the approved plan; deviation flagged.
- ⚠️ **I broke the markdown whole-file-write rule.** `.claude/rules/markdown-docs.md` forbids rewriting a
  markdown file via a whole-file write or Python, after that pattern destroyed ~12.7 KB of
  `required-context/02-Data-Access-Requests.md`. I used a Python whole-file write on five markdown files
  before the rule surfaced. **No loss occurred** — all five verified valid UTF-8, zero replacement
  characters, zero mojibake, all grew as expected — but the check was after the fact, which is exactly
  what the rule exists to prevent. Switched to `Edit` for the remainder.

**Done.**

- `pom.xml` remediated and committed on `Dev` as **`4d2d567`** — 172 changed lines, **no `.java` file
  touched**. Every change carries an in-pom comment naming the advisory and, where one exists, the
  coupling or the reason it was kept.
- **Result: 85 artifacts / 25 advisories → 63 artifacts / 1 advisory.** All 3 CRITICAL and 9 of 10 HIGH
  cleared; all 12 MODERATE cleared.
- **The survivor is documented, not hidden:** `org.jdom:jdom:1.1.3` via `zap-clientapi` — CVE-2021-33813
  (XXE, HIGH) with **no fix at any version**. Checked `zap-clientapi 1.17.0` (latest): still depends on
  jdom 1.1.3, and `jdom2` lives under `org.jdom2`, so excluding it would break ZAP at runtime. ZAP is off
  by default (`enableZapProxy=false`), so the parser is never reached on a normal run. Left in place with
  the exposure and both exit routes recorded in the pom. **Owner decision — a security-testing capability
  is not removed to tidy a scan report.**
- **Validated 21/21** by a scratchpad harness compiled against the real project classpath (nothing added
  to the repo): log4j2 2.26.1 binding · log4j 1.x absent + jxl SimpleLogger fallback ·
  `ExcelUtils.getTableArray` reading the real `.xls` · POI xlsx write/read/DataFormatter roundtrip ·
  HWPF resolution · jackson `has("Success")=true` / `has("success")=false` (the envelope's case
  sensitivity, unchanged) · SQLServerDriver + `DBUtils.buildJdbcUrl` emitting
  `encrypt=true;trustServerCertificate=true` · MySQL driver retained · `APIExcelReportUtil` write path ·
  both TestNG listeners · `ApiHelper` static initialiser · **all five `-DbrowserType` launch paths**.
  Plus `test-compile` exit 0 on 1,083 sources (30 s against a 26 s baseline).
- Docs corrected off the retired copy model and onto the submodule architecture: root `CLAUDE.md`
  (§Edit scope rewritten, new §PAM submodule, folder table, BLAST output boundaries), root `README.md`
  (§2 and §3), and the repo's `AGENTS.md` and `README.md`.

**Learned — Playwright's upgrade has a side effect worth knowing before a CI rollout.** Creating
Playwright 1.61.0 made its driver **prune the browser revisions belonging to 1.45.1** —
`chromium-1124`, `firefox-1454`, `webkit-2035`, `ffmpeg-1009` were deleted automatically. This machine
was unaffected because a newer set (`chromium-1228`, `firefox-1532`, `webkit-2311`) was already present,
and all five browser paths launch. **A fresh CI agent is a different story:** the `driver-bundle` is
~193 MB per version, and the `chromium`/`firefox`/`safari` paths need `playwright install`. The default
`-DbrowserType=chrome` is insulated — `BaseTest` sets `LaunchOptions.setChannel("chrome")`, i.e. the
system-installed Chrome.

**Corrected — the `JAVA_HOME` path in `CLAUDE.md` was wrong and blocked Maven.** The documented
`jdk-21.0.11.10-hotspot` does not exist; the installed JDK is **`jdk-21.0.12.8-hotspot`**. Following the
documented instruction produced the exact failure it was written to prevent. Fixed, with the verification
command added. Also: `java` on `PATH` is now Adoptium 21, so a bare `java` works while `mvn` still fails
— Maven reads `JAVA_HOME`, not `PATH`. And the installed Java 26 is now `26.0.2`, so the broken system
`JAVA_HOME` pointing at `26.0.1` did not self-heal.

**Open — and this decides whether any of the remediation shows up as fixed.**

- ⚠️ **Where the SCA scan actually runs is unverified.** `pam/.gitlab-ci.yml` is a one-line include of
  `Dhruvin.Chawda/claude_code_pipeline` → `base_pipeline.yml`, not readable from this workspace; nothing
  sets `GIT_SUBMODULE_STRATEGY`; and **the bootstrap repo has no `.gitlab-ci.yml` of its own.** So after
  `AutomationTesting/` is deleted either the scanner finds no `pom.xml` and reports **zero** findings — a
  **false all-clear**, not a fix — or it reads `Automation/pom.xml` at the pinned gitlink and keeps
  reporting the old versions. **Two follow-ups: give the bootstrap repo its own scan job, and add a
  gitlink bump to the release path.**
- ⚠️ **The submodule is registered but uninitialised.** `git submodule status` returns `-365050d5…`;
  `pam/Automation/` is an **empty directory**, and the gitlink is **11 commits behind** local `Dev` — so
  `4d2d567` is not visible in `pam` until the owner pushes and bumps it.
- ⛔ **No UI or API suite was run, and the reason is a safety rule, not a permission gap.**
  `Environments/QA_MsSQL.properties` resolves `user_name` to the **locked `auto_adminui`** account (12
  chars, matches), and every login attempt increments the lockout counter on a shared functional account.
  `pam_APITokenUserName` decodes toward `GenericScheduler`, the data-warehouse ETL account. Unblocks on a
  working credential supplied as an override — then `CICD_Suites/Demo.xml` for UI and one
  `API_Suites/Positive_All/<Module>.xml` for API, **via suite XML, never `-Dtest`**, or the listeners do
  not register and no Excel report is written.
- `pam/AutomationTesting/` deletion is still the owner's action — **1,211 files remain tracked**, and
  `pam/` was left clean at 0 changes.
- Not pulled: local `Dev` is **3 commits behind `origin/Dev`**. Verified those 3 commits touch none of
  `pom.xml`, `AGENTS.md` or `README.md`, so `4d2d567` will merge without conflict. **Merging is the
  owner's call.**
- ➖ Noted, not fixed, all pre-existing: `ExtentReportListener.java:181` has a hardcoded placeholder JDBC
  URL with no `encrypt` option, which mssql-jdbc ≥10.2 would reject; `xml-apis 2.0.2` resolves to
  `1.0.b2` through an upstream relocation; a dead `logback.xml` sits at the repo root with no Logback on
  the classpath; and the `graphify` `post-commit` hook fired on this commit and **failed against a
  different checkout** (`C:\Users\…\git\pam_automation_bootstrap`, with a BOM in the stored path) — the
  known stale-graph cause, unchanged by this work.

## 2026-08-18 (later) — `OBJ-021`: the board becomes demo-ready, and three metrics were being measured then thrown away

**The fixes that mattered were reporting fixes, not instrumentation.** Web Vitals were absent from every
sanity run, and the cause was not that k6 could not collect them: k6 emits `browser_web_vital_*`
**automatically** for any browser scenario, `login-browser.js` already harvested them, and
`sanity-browser.js` simply never read them. The same was true of `min`/`med`/`p90`/`p99`/`max` on every
per-module trend — `summaryTrendStats` already asked k6 for them and the summary exported only `avg` and
`p95`. **Lesson: before concluding a metric "cannot be captured", check whether it is being captured and
discarded at report time.** Four real vitals and five extra statistics per module appeared with no new
instrumentation and no estimated values.

**The `INGEST_RUN` mechanism was documented but never implemented.** The generator's header described it;
nothing in the file read the variable, and `SAMPLE = true` was hardcoded, so the dashboard emitted
seeded pseudo-random latencies. One command away from showing management invented numbers. Implemented,
then extended to a two-run ingest (N-1 vs N) with the owner's baseline-relative gates — WARN above 15 %
of N-1, FAIL above 30 %, hard FAIL on a login failure or a check-rate drop. No SLO was invented.

⛔ **`pct()` was wrong by 100× across the whole dashboard.** It appended `%` without multiplying while
all six call sites passed fractions, so the Login page displayed **`SUCCESS RATE 1.0%`** for a run where
every login succeeded, and "checks pass 0.998" rendered as `1.0%`. Fixed in the formatter after
confirming no caller passed a pre-scaled value. **A dashboard bug that understates success is as
dangerous as one that overstates it.**

**Two more display defects with the same shape — a plausible-looking wrong value.** `c.muted` and
`c.danger` do not exist in `theme.js` (they are `inkMuted` and `critical`), so Recharts received
`undefined` and painted the baseline series **black**; the palette's purpose-built `c.baseline` was
there all along. And the Scenarios tile reported only passed and failed out of 14, leaving **six
degraded modules invisible** — a module that opens on some concurrent samples and not others is neither.
Four buckets now reconcile to the total.

**Retention: archived, never deleted.** Seventeen older k6 runs were **moved** to
`performance/reports-archive/` with a restore note, because `performance/` is gitignored and a delete
would have been unrecoverable — and those runs are the evidence behind `ISSUE-012`. `Reports/Runs/`
(the 12 API executions) was left untouched: the standing "retained, never deleted" rule holds, the API
dashboard resolves N/N-1 from those folders, and the `OBJ-020` execution was still writing into one.

**The remaining module failures were never product defects.** The crash that cost coverage was ours:
closing an app window **mid-sweep** raced k6's browser-target tracking and killed Chromium — 2 of 3
browsers, then 3 of 3, while host memory stayed at 73 % free. Deferring those closes to iteration
teardown produced two clean 12/13 runs with zero crashes. Earlier, `waitForNewPage` returned
`pages[length-1]`, which was the **main page**; closing it poisoned every module after it. **Identify a
browser target by identity, never by index.**

⚠️ **Both retained executions ran while the `OBJ-020` API execution loaded the same environment** — the
owner's explicit decision. The N-1 vs N comparison is valid because both sides share the condition, but
the absolute latencies are inflated against an idle environment. That caveat is rendered on the board
itself rather than left to the presenter. Graded `Likely`; one control run with the API execution paused
would settle it. Board state: N-1 `2026-08-18_180719`, N `2026-08-18_181323`, gate **WARN** (check pass
rate −3 %), login p95 **improved 19.9 %**, coverage 92.3 %, `uag` the single outstanding failure.

## 2026-08-21 — `OBJ-024` lands, `OBJ-023` is closed on purpose, and `OBJ-025` opens on structure

**Instructed.** Two things, in one message. First: the paused API re-execution is on hold and is **not** to be
resumed manually — the Sunday trigger covers it — so mark it completed and move on. Second, the substantive
request: revisit the entire structure end-to-end and make it "more robust, compact, simple, and aligned with
industry standards", with explicit permission to *change, merge, rename, or realign* any folder, provided all
existing functionality and important data survive.

**Done — `OBJ-024` is finished, not just mostly finished.** Its record had listed the push and the tag as
outstanding owner actions. Both have landed and are now verified rather than assumed: `main` is 0 ahead / 0
behind `origin/main` at `3e295f2`, and the annotated `v0.2` tag is on the remote (`9833206` → `63bbff7`). The
in-place `git init` approach is also now validated by something other than argument — `PAM-Dashboard-Daily-Refresh`
ran on schedule afterwards and resolved every path.

**Decided (`D29`).** `OBJ-023` closes without executing the remaining 569 flows. The reasoning worth keeping is
that this is the *safer* option, not merely the cheaper one: the pinned token's 24 h lifetime elapsed during the
pause, so a manual resume needed a fresh `/arcontoken` call on `GenericScheduler` — a shared functional account
that also serves the data-warehouse ETL and has locked twice recently — while `D24` grants scheduled token
generation **only** to the weekly job, and only because of three mitigations a manual resume would not have had.
Routing the second data set through the guarded Sunday path reaches the same answer without taking that risk.
`Reports/Runs/2026-08-19_133400/` (178 of 747) is retained as evidence and must never be promoted to N.

**Learned — the structural picture, measured before proposing anything.** 14,722 tracked files / 828.6 MB across
15 top-level entries, and the distribution is far more lopsided than the folder list suggests:

| Fact | Figure |
|---|---|
| `Reports/` share of all tracked files | **14,035 of 14,722 — 95.3%** |
| Three folders holding most of the bytes | `Reports/` 279.1 MB · `Graphify/` 215.1 MB (17 files) · `Developer-Loopholes/` 185.0 MB (69 files) |
| `Company Documents/` | 78.7 MB in **4** files, all Git-LFS |
| Directory names containing spaces | **3** — `Company Documents/`, `Developer Repository Issues/`, `Automation gitlab repo/` |
| Folders at or under 12 tracked files | `questions/` 6 · `objective-history/` 5 · `writer/` 2 · `jira/` 10 · `BLAST/` 14 · `Developer Repository Issues/` 12 · `required-context/` 2 · `.claude/` 5 |

So "the repository is large" is really two separate claims: one folder dominates the *file count*, and three
binaries dominate the *bytes*. Those need different remedies, and conflating them would produce the wrong plan.

**Observed — an archive-hygiene issue this objective should fix.** `CLAUDE.md` §Large files says to split an
archive part once it passes ~600 lines. Two parts are well past it: `01-objective-records.md` at 1,771 lines and
`04-narrative-log.md` at 1,154. The rule is being cited while not being followed.

**Open.** The target architecture itself. Three candidate designs are being scored against three lenses
(breakage risk, the owner's stated request, one-year maintainability) on top of a *measured* path-dependency map
rather than an assumed one — because the things that break a rename here are mostly not in the Python: the two
Windows scheduled tasks invoke absolute paths, `.gitattributes` pins Git-LFS to the literal path
`Graphify/pam-scope/graphify-out/graph.json`, `.gitignore` names both nested repos literally,
`obj013_scan.py`'s `WRITE_ALLOWLIST` hardcodes seven relative paths, and `workbench/.drift/facts.json` binds
tracked facts to the documents that quote them by path. No file moves until that map is complete and signed off.

## 2026-08-24 — `engage`: one-word workspace readiness (`OBJ-026`)

**Instructed.** Build a single entry point — the owner types `engage` and the workspace becomes safe,
synchronized, understood and ready to work in. Explicitly *not* a shell-script wrapper: inspect before
acting, reuse what exists, avoid unnecessary operations, protect local work, ask only when necessary. The
owner also said not to assume a monolithic skill was the right architecture, and to inspect the existing
system before choosing one.

**Decided.** Four MCQ answers, two of which changed the safety model — recorded as `D30` and `D31`.
Fast-forward pulls are permitted on **both** nested repos when their trees are clean, resolving a live
contradiction in `CLAUDE.md`. The derived-data refresh auto-runs when stale. The skill is installed
**user-global** alongside the other four, with the engine versioned in `workbench/scripts/`. `OBJ-025` is
paused rather than closed, so `engage` binds its workspace paths through a single `PATHS` block that the
restructure can re-point in one edit.

**Done.** Three modules and a skill. `engage_core.py` is pure — discovery, a per-repository policy table
and an ordered decision table, no writes and no printing, which is what makes it testable.
`engage.py` orchestrates the six phases and renders. `engage_selftest.py` runs 57 assertions.
`~/.claude/skills/engage/SKILL.md` detects the workspace and narrates the result rather than pasting it.
Reuse was real rather than nominal: `Journal`, `child_env()`, `make_output_safe()` and the `FORBIDDEN`
list are imported from `obj016_daily_refresh.py`, and the derived-data refresh **calls** that script with
`--skip-git` instead of reimplementing it.

**Learned — the missed-occurrence heuristic that does not work, and the one that does.** The obvious way
to detect a skipped scheduled run is to compare the time since the last run against the gap between
`LastRunTime` and `NextRunTime`. It cannot work, because a skipped firing is exactly what stretches that
gap. Measured here: `PAM-Weekly-API-Execution` last ran `2026-08-16` with next set to `2026-08-30`, so the
inferred period was 14 days and the missed Sunday looked perfectly on schedule. Reading `DaysInterval` /
`WeeksInterval` off the trigger gives the real period and the miss becomes obvious.

**Learned — two scheduled runs did not fire, and one of them matters to `D29`.** On first execution
`engage` found `PAM-Dashboard-Daily-Refresh` last ran `2026-08-21` (3 missed daily occurrences) and
`PAM-Weekly-API-Execution` last ran `2026-08-16`, meaning **the `2026-08-23` Sunday execution never ran**
and its previous attempt exited `1`. ⚠️ `D29` closed `OBJ-023` on the explicit reasoning that the standing
Sunday trigger would produce the second data set for the reproducibility comparison. It has not, and the
next scheduled firing is `2026-08-30`. This is not a new decision, but the assumption behind `D29` is
currently unmet and the owner should know.

**Learned — the first real run pulled far more than the workspace thought.** `Dev` was reported 6 behind
before the fetch and was actually **10** behind after it; `pam/` took **12** commits. Both fast-forwarded
clean. This is the concrete argument for fetching *before* classifying: ahead/behind come from
remote-tracking refs, so a decision made pre-fetch is a decision about yesterday.

**Learned — the self-test earned its place immediately.** It caught two defects on first execution. One
was a Windows-specific fixture bug (git marks `.git/objects` read-only, so `shutil.rmtree` silently leaves
the directory and the next clone fails). The other looked like a core bug and was not: a fixture
classified under an unclassified path correctly refused to pull, which is the `UNKNOWN_POLICY` default
working exactly as intended. The harness was asking the wrong question, not the code answering wrongly.

**Corrected.** Two statements in `CLAUDE.md` §Edit scope. *"Do **not** pull to fix it — merging is the
owner's call"* contradicted `D28` and the **Pull ✅** column three paragraphs above it; superseded by `D30`
for the fast-forward case only. And *"`AI` remains **local-only** — no `origin/AI`, no upstream"* is
false: `git branch -vv` reports `AI 7be00b3 [origin/Dev: behind 21]`. There is still no `origin/AI`, but
`AI` does track an upstream, and it is `origin/Dev`.

**Open.** `engage` reports; it does not commit or push — `/go-go-go` still owns that. The `PATHS` block in
`engage.py` and the `POLICIES` table in `engage_core.py` are both on the `OBJ-025` path-fix checklist.
`workbench/.engage/` is gitignored deliberately: unlike `.daily/`, it is per-invocation and regenerable,
so tracking it would churn every commit and record nothing the repositories do not already say.

## 2026-09-01 — `D47`: manual push for the bootstrap repo, and the guard that was never doing the job

**Instruction.** One scoped amendment to `D28`: keep pull for all three repositories, keep automatic push
for the workspace repo, **enable manual push for `pam_automation_bootstrap`**, keep `pam` blocked. The
owner was explicit that nothing else should move.

**The finding that made it a one-line change.** The obvious reading was that removing the bootstrap's
`remote.origin.pushurl` block would also re-enable *automatic* pushes, and that something new would be
needed to hold those back. Measured, that was wrong: the pushurl was never what stopped an automated push.
`push` sits in `obj016_daily_refresh.FORBIDDEN` and is absent from `engage_core.ALLOWED`, so no scheduled
task, harness script, `engage` run or Control Center action can emit a `git push` for **any** repository —
including the workspace repo, which has never carried a pushurl block at all. The ban sits upstream of the
remote configuration entirely. So the requested split — automatic ⛔, manual ✅ — needed **no new
mechanism**, only the removal of a blanket block that was doing a different job from the one its name
suggested. `engage_selftest.py` already asserted the real guard (`guard: git push refused`); it ran
**57 passed, 0 failed** after the change, unmodified.

**What was encoded rather than merely written down.** `engage_core.Policy` carried a single `push: bool`,
which conflated *may this be pushed* with *may this be pushed unasked* — a distinction that did not exist
before and now does. It gained `push_auto`, plus a module-level assertion that no policy grants
`push_auto` without `push`. The comment above `POLICIES` says why the two must not be flattened back:
doing so would silently re-grant automatic push to the bootstrap repo, which is exactly what the decision
withholds. `classify()` and `engage.recommend()` now distinguish *"manual push only, on an explicit
instruction"* from *"ready to push"*.

**Verified.** `pam`'s block re-measured present immediately after the change; bootstrap's fetch URL
untouched and `ls-remote` resolving (`refs/heads/Dev` at `7d34e1c`, still the only remote branch — there is
no `origin/AI`); local `Dev` level with `origin/Dev`; tree clean. **Nothing was pushed in the course of
making the change.**

**Left alone on purpose.** `.claude/settings.json` holds no push rule — only `git merge` and
`git remote set-url` denies — the assistant cannot edit it by design, and the change was scoped to push
rights. ⛔ `merge` is unchanged and still never the assistant's, in any of the three repositories.

**The trap now stated in three places** (`CLAUDE.md`, `README.md`, `D47`): *"the task is done and there
are unpushed commits"* is not an instruction to push. Finishing work is never itself the trigger.

## 2026-09-21 — `OBJ-030`: extending the two 2026 censuses, and the off-by-one that had been there all along

**Instructed.** Extend the PAMIT and CI census reports from 03 Sep to 21 Sep 2026, processed separately.
Explicitly: update the analysis, **not** the methodology — preserve format, headings, tables, calculations
and categorisation, keep the historical window unchanged, and validate for missing dates, duplicates and
summary/detail inconsistency before finalising.

**Decided first, measured second — the order that made the rest cheap.** Rather than editing two markdown
files by hand, both were tested for regenerability: each was rebuilt from its own retained 03 Sep snapshot
and diffed against the file on disk. **PAMIT 2 differing lines of 469; CI 2 of 433** — in both cases the
`Generated:` timestamp and nothing else. The reports are **100% generated**, so "preserve the format" is
satisfied *by construction* by bumping `DATE_TO` and re-running. Hand-editing would have been the only
approach that could have broken it.

**⚠️ Found at intake, before any fetch.** `jira_analysis_2026.py` computed its output name from its date
constants — `Jira_Analysis_20260101-20260903.md` — while the file on disk was `Jira_Analysis_01Jan26-03Sep26.md`,
renamed by hand after generation. **Re-running it unchanged would have written a new file and left the
intended deliverable stale**, reporting success. Both scripts now derive the name from one `RANGE_SLUG`
constant, so the name cannot drift from the range again.

**⛔ The finding that mattered: `created <= 'YYYY-MM-DD'` excludes that whole day.** JQL reads a bare date
as `00:00`, so the half-open interval was never closed. Measured: `created <= '2026-09-21'` returned **0**
tickets for 21 Sep, while `>= '2026-09-21' AND < '2026-09-22'` returned **44 (PAMIT) / 38 (CI)**. The 03 Sep
edition carried the identical defect and silently omitted its own final day — **24 PAMIT / 31 CI tickets**
that were never in the report it was named after. Every edition of this report since its creation has been
short by one day. Both scripts now query `created < DATE_TO_EXCLUSIVE`.

**Corrected.** PAMIT **5,431 → 5,740**; CI **5,588 → 5,994**. Of the growth, 241/339 are genuinely new
tickets and 44/38 are the recovered end date. The per-day counts were verified independently against Jira
one day at a time and match the snapshots exactly.

**Learned — a re-fetch is not a no-op on history.** The report is a point-in-time census, so re-taking it
moves the old window too. Quantified rather than left implicit: among the 5,431 pre-04-Sep PAMIT tickets,
**status changed on 478 (8.8%)**, assignee on 328 (6.0%), priority on 3 (0.1%), resolution on **0**. CI:
status 350 (6.3%), assignee 291 (5.2%), priority 6 (0.1%), resolution 0. The ticket *set* is unchanged —
JQL filters on `created` — only the field values moved.

**Two anomalies characterised rather than waved through.**

- **24 PAMIT / 30 CI tickets created on or before 03 Sep are present now and were absent from the 03 Sep
  capture.** Consistent with late indexing: those captures ran at 21:44 and 22:29 on 03 Sep.
- ⛔ **`CI-25546` is readable by key and invisible to every bulk search.** Created `2026-08-31T21:57:29`,
  project `CI`, type `Story`, status `Closed`. It was in the 03 Sep snapshot and is not in the 21 Sep one.
  Proven not to be a paging artefact: a **one-day window returns 56 rows in a single page**, the server's
  own `approximate-count` agrees at 56, neighbours `CI-25545` and `CI-25547` are both present, and the row
  is still absent with no `ORDER BY` at all — yet `... AND key = CI-25546` returns it. This is a **Jira
  search-index inconsistency**, not a tooling defect, and no change here can recover it. One ticket in
  5,994 (**0.017%**); every aggregate is unaffected. Recorded so the count is explained rather than noticed
  later as drift.

**Hardened while in there.** A stable tie-break (`ORDER BY created ASC, key ASC`) so token paging is
deterministic across ties, and `max_pages` raised to 200 at the two call sites — **CI completed on page 60
of a 60-page runaway stop**, one page from failing the whole fetch. Both changes are local to the two 2026
scripts; `jira_query.py` was deliberately left untouched because the `E:` copy is ahead of this one on that
file and editing it here would deepen a known divergence.

**Validated.** Eleven gates per project: no duplicate keys, old-window set preserved, end date present,
every empty date confirmed zero at source (PAMIT Mon 14 Sep really is zero; the rest are weekends), header
total, §1 summary total, client+internal, §2 status distribution and §10 monthly trend each summing to the
enumerated population, and markdown/`.docx`/`.xlsx` agreement. All pass except the `CI-25546` gate above,
which is left failing on purpose — a characterised exception is worth more than a suppressed one.

**Delivered.** `docs/analysis/Jira_Analysis_01Jan26-21Sep26.{md,docx,xlsx}` (26 xlsx sheets, as before) and
`CI_Jira_Analysis_01Jan26-21Sep26.{md,docx,xlsx}` (21, as before). Section structure identical: PAMIT 23
sections, CI 18. The `03Sep26` set was retired on the owner's instruction; **its JSON snapshots are retained**,
so reproducing it needs only `DATE_TO = "2026-09-03"` and the old `created <= ` form — the data was never
the thing at risk.

**Open.** The 21 Sep run is a *snapshot of a day still in progress* — 21 Sep was the current date, so its 44
and 38 tickets are a partial day and will grow. Anyone re-running this range later will get a higher final-day
count; that is not drift.

## 2026-09-22 — the hardening review: three defects that every gate had passed

Not a BLAST objective — a direct owner instruction to bring the folder to an industry-standard level. No
`OBJ-NNN` was assigned and `BLAST/Objective.md` was left holding `OBJ-030` untouched. The full account,
with before/after figures and the validation evidence, is
[`../hardening/README.md`](../hardening/README.md); what belongs in the project's memory is the lesson.

**Three defects, all in shipped deliverables, all invisible to `OBJ-030`'s eleven gates per project.**
PAMIT §12 `Affected Milestone` published **100% `Not set`** across all 5,740 tickets — `normalise()` never
emitted `customfield_10092`, although `FIELDS` requested it and §12 read it, so the fetched field was
discarded in silence. The field is **78.8% populated (4,523/5,740)**. CI published **4,241 sub-tasks** where
**1,443** exist, because it counted *parent-presence* and `parent` spans the whole hierarchy in modern Jira;
2,798 Epic children were swept in, and the same report published 1,443 in its own §3. And §12's footnote
called **5,832** figures "milestone assignments" when only **4,615** are — the 1,217 unpopulated tickets
were folded in as `Not set` assignments, which also put a `Not set` row at the top of a table whose every
other row is a real build.

**Why the gates missed all three, which is the part worth keeping.** Every `OBJ-030` gate tests the
generator against **its own rule**: re-run it, and it reproduces the report. A rule that is correctly
implemented and wrongly *named* reconciles perfectly, every time. The milestone counter faithfully counted
what it was told to count; the sub-task counter faithfully counted parents. **Reconciliation is not
validation**, and no amount of re-running would ever have said otherwise.

**What now closes it.** `tools/jira/validate_analysis.py` — 55 checks that deliberately do **not** call the
generators. It re-derives every headline figure from the raw JSON snapshot and compares it with the
published markdown, so a figure passes only when two independent derivations agree. It also verifies that
the `.docx`/`.xlsx` and the `21-09-2026/` pack were built from the *current* markdown, which caught a real
staleness the moment it was written. ⚠️ A validator that has never failed proves nothing, so it was run
against the pre-fix reports from `cea4352` and confirmed to name the CI defect exactly (`+2798`).

**Provenance, so a report can be traced rather than trusted.** Each census report now carries a
`Source snapshot:` header line naming its snapshot file and a sha256 of its bytes, and the validator
recomputes that digest. A report can no longer claim a source it was not built from — previously the only
thing linking a figure to its data was a wall-clock timestamp, which says nothing about *which* snapshot
was underneath.

**One silent failure worth naming separately.** `--offline` fell through to a **live Jira fetch** whenever
the snapshot was absent, and then overwrote it — the operator asks for zero HTTP, gets production traffic,
and loses the capture. `pamit_client_analysis.py` had always refused correctly; the two census generators
had not. Both now exit `2` and name the missing path. Their `main()` return codes were also being discarded
by a bare `main()` call, so even a deliberate refusal would have reported success.

**Also corrected.** `tools/requirements.txt` omitted `python-docx`, which `analysis_render.py` has always
imported — a machine provisioned purely from that file failed on every `.docx` render, including the whole
client pack, with an ImportError naming a package the file said was not needed. It also credited
`jsonschema` to a script whose own header states it is deliberately dependency-free.
