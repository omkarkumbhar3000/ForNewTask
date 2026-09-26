# Objective Records — OBJ-001 … OBJ-012

**Part of** [`../objective_original_origin.md`](../objective_original_origin.md) — the project's permanent, append-only archive. Full ten-field record for every objective. This is §0 of the archive, in detail; the summary table and the next ID live in the index.

⛔ Append-only. Never delete, reword or reorder an entry. Section numbers (`§N`) are the stable citation scheme and do not change when files are reorganised.

---

### OBJ-001 — Automation framework optimization

**Status:** ⬜ Superseded

**Summary.** The founding brief. Acting as a Senior SDET, apply the `SKILL.md` structure to the automation
code, audit `pam_automation_bootstrap` module-wise, remove dead code, fix architectural violations, move
assertions to test level, replace custom waits with Playwright's built-ins, and extend API testing beyond
status codes to Excel-driven response-content validation.

**Key Deliverables.** Planning set in `workbench/archive/approach/` — `instruction.md` (the brief itself),
`plan.md`, `dynamic-api-generation.md`, `orphans.md` (218-orphan catalogue), `Graphify.md`.

**Related Files.** `workbench/archive/approach/*`, `workbench/archive/README.md`,
`workbench/skills/*.SKILL.md`, `Automation gitlab repo/pam_automation_bootstrap/`.

**Reason for Archiving.** Superseded. Its sixth instruction grew into the entire project; the remaining
items were overtaken when measurement showed the API surface itself was the problem. The planning folder
was frozen into `workbench/archive/` when requirements were consolidated (decision D4).

**Pending Work.** Four of the ten original instructions were never carried out and remain open:
architectural violations (base-page methods called directly from test files), assertions still sitting at
page level, custom waits instead of Playwright's built-ins, and tests skipping without an explainable
reason. Dead-code removal survives as ISSUE-008 / Phase 7.

**Lessons Learned / Observations.** The single most consequential observation in the project came from
here — *"API validation today = status code only."* That proved far worse than a coverage gap: the product
answers HTTP 200 for rejected requests, so a status-only suite reports **false passes**, not merely thin
ones. Everything measured since elaborates that point.

**Dependencies.** Precedes OBJ-002 and OBJ-003. Related: ISSUE-008, `workbench/archive/README.md`,
`workbench/skills/`.

---

### OBJ-002 — Dynamic API validation, feasibility analysis

**Status:** ✅ Completed

**Summary.** First formal BLAST run. The deliverable requested was an *analysis*, not code: determine
whether the API under test can be derived by parsing the developer repository, and report a feasibility
verdict with a gap analysis and clarifying questions.

**Key Deliverables.** Feasibility verdict delivered to the owner; findings F1–F3 in `BLAST/findings.md`;
corrections fed back into `workbench/archive/approach/dynamic-api-generation.md` §2, §2.1, §9.1.

**Related Files.** `pam/PAM` (6,866 `.cs` files, measured not modified), `APIConfig.java`,
`BLAST/findings.md`, `BLAST/progress.md`, `Reports/Issues/ISSUE-005-api-coverage-gap.md`.

**Reason for Archiving.** Completed successfully — the verdict was delivered and acted upon.

**Pending Work.** None.

**Lessons Learned / Observations.** ⚠️ **The objective's premise was checkable, and it was false.** Only
**48 of 1,306** declared endpoints (3.7%) exist anywhere in `pam/PAM`; the real API sits behind
`ARCONAPIGateway`. Verifying the premise before assessing feasibility was the entire value of the run — a
plan built on Roslyn-parsing the developer source would have failed late and expensively. Also measured:
37 shared Swagger specs / 690 operations overlap the catalogue by only ~6%, and **0 of 690** declare any
4xx or 5xx, so negative expectations cannot be derived from a spec. Nothing was written to `tools/` —
Protocol 0 was correctly not cleared.

**Dependencies.** Follows OBJ-001. Precedes OBJ-003. Related: ISSUE-005.

---

### OBJ-003 — Auto-generated multi-hop API chaining, and API graph visualisation

**Status:** ✅ Completed

**Summary.** Chain APIs automatically — take a value from one endpoint's response and feed it into the
next endpoint's request, following the application's real flow, fully generated with no manual scripting
per chain. Supporting requirement: a graph of the API surface so relationships are visible.

**Key Deliverables.**
- Scripts — `workbench/scripts/chain_runner.py`, `generate_flows.py`, `run_chains.py`, `run_validation.py`,
  `run_qa_mssql.py`, and the declarative `workbench/scripts/flows/*.json`
- Graphs — `Graphify/api-graph/build_api_graph.py` and `out/api-graph.html`, `api-graph.json`,
  `chaining-report.md`; `Graphify/pam-scope/` (112,628 nodes)
- Runs — `Reports/Runs/2026-07-29_160155/` (3 flows, 15 hops, all PASS) and
  `Reports/Runs/2026-07-29_181439/` (326 flows, 1,868 calls, 870 endpoints)
- Summaries — `Reports/Summary/API-Chaining-Feasibility-Demo.md`,
  `Reports/Summary/Full-Generated-Run-2026-07-29.md`
- Defect write-ups — `Reports/Issues/ISSUE-001` … `ISSUE-011`

**Related Files.** `workbench/scripts/`, `Graphify/`, `Reports/`, `APIConfig.java`, the 66
`utils/apiPayload/*.java` helpers.

**Reason for Archiving.** Completed — the definition of done was met. One command discovers chains from
the catalogue, injects real values between calls, binds path templates, validates each hop across seven
layers, and reports every chain attempted *and* every chain declined with its reason.

**Pending Work.** Four items, carried forward: all **1,680** chain candidates remain name-*inferred*
because no business-endpoint response has been captured; write coverage is blocked at **13 of 217**
creates; teardown is disabled because generated teardown bodies are not bound to the created record's id;
the Java/TestNG port was deferred.

**Lessons Learned / Observations.** The headline measurement of the project: **90% of calls returned HTTP
200, but only 64% passed all seven layers** — a 26-point gap of 406 calls. ⛔ `Success: true` does not mean
a write happened (`SetServiceDetails` returns it with `Message: "Already Exists"`). **135 × 404** proved
the catalogue declares endpoints the deployment does not serve. Eight distinct response shapes were
observed on one API. Blind `Result[0]` chaining fails — only 19 of 34 LOBs have user groups, so flows must
select by name and discover the id. The circuit breaker and pre-flight health probe exist because an
earlier runner continued through **322 consecutive 503s** during an outage.

**Dependencies.** Follows OBJ-002. Feeds OBJ-004 and OBJ-005. Related: ISSUE-001 … ISSUE-011.

---

### OBJ-004 — Developer loophole evidence packs and Jira tickets

**Status:** 🟡 In Progress

**Summary.** Turn each finding from the API work into a self-contained, raisable Jira ticket backed by
citable evidence — one folder per finding, each generated from one dataset so the markdown, the workbook
and the machine-readable extract cannot disagree.

**Key Deliverables.** `Developer-Loopholes/LH-01` … `LH-12`, each with `JIRA-TICKET.md`, `EVIDENCE.md`,
`EVIDENCE.xlsx` and `data/`; generators `workbench/scripts/build_lh_pack.py`, `lh_common.py`,
`lh_specs_run.py`, `lh_specs_static.py`, `lh01_evidence.py`; the Jira client `jira/jira_client.py` and
`jira/create_lh01.py`; **`PAMIT-42744`** raised for LH-01; the brief
`workbench/developer-loopholes.md`.

**Related Files.** `Developer-Loopholes/`, `jira/`, `workbench/scripts/`, `workbench/developer-loopholes.md`,
`Reports/Issues/`, source run `Reports/Runs/2026-07-29_181439/`.

**Reason for Archiving.** Not archived — still open. Eleven of twelve tickets are drafted and
deliberately **held** pending the owner's validation of the evidence.

**Pending Work.** Raise LH-02 … LH-12, or fold LH-04 and LH-11 into `PAMIT-42744` as sub-tasks — they were
found inside its responses and a developer fixing LH-01 will touch the same code. Generalise the ADF
builders and attachment routine out of `create_lh01.py` when the second ticket is written.

**Lessons Learned / Observations.** LH-01 re-validated live: **289 of 289 calls still reproduce, 100%**.
🔴 The `GenericScheduler` service account is **locked** — `/arcontoken` returns HTTP 400; supply
`$env:PAM_API_TOKEN` and never retry a failed token request. ⚠️ Evidence is redacted at capture and the
redaction is over-broad (it catches booleans too), so a replayed call that fails may be a harness artefact
rather than a fixed defect — **never report such a call as "fixed"**. `replay_filter` is mandatory: 35 rows
across LH-02 and LH-09 would otherwise mutate data on every re-validation. Jira Cloud v3 needs ADF, not
wiki markup, and `createmeta` under-reports six required fields.

**Dependencies.** Follows OBJ-003. Related: `PAMIT-42744`, ISSUE-001, ISSUE-003, ISSUE-009, ISSUE-010,
OBJ-005.

---

### OBJ-005 — Data sufficiency analysis

**Status:** ✅ Completed

**Summary.** Grade every data source supplied to the effort against what is actually being asked of it,
and state precisely what must be provided to close the gaps.

**Key Deliverables.** `required-context/01-Data-Gap-Analysis.md`,
`required-context/02-Data-Access-Requests.md`, `workbench/document-gap.md`, and the merged
`workbench/scripts/source-map.json` + `SOURCE-MAP.md`, built by `workbench/scripts/build_source_map.py`.

**Related Files.** `Company Documents/` (four sources), `workbench/rag/`, `APIConfig.java`, the payload
helpers, `pam/PAM`.

**Reason for Archiving.** Completed — the analysis was delivered and its conclusion now governs planning.

**Pending Work.** The access requests in `02-Data-Access-Requests.md` are unanswered; until they are, the
write path stays blocked.

**Lessons Learned / Observations.** Reads are well covered and **writes are structurally untestable**:
870 of 1,306 endpoints were exercised in one run, but only **13 of 217** create endpoints can be driven,
because nothing supplied contains a valid request body. That single gap cascades — a failed create returns
no identifier, so a chain cannot proceed past its first hop. Only **3** properties carry `[Required]`
across 6,738, so mandatory-ness is always inferred, never asserted. The 2,470-page Confluence export is
the best payload asset available (3,194 examples, 1,654 endpoint-bound) but binds payloads to endpoints by
**page proximity**, so some bindings are wrong.

**Dependencies.** Follows OBJ-003. Informs OBJ-004 and all future write-path work.

---

### OBJ-006 — Objective management and workspace governance

**Status:** 🟡 In Progress

**Summary.** Establish how instructions enter the project and how history is preserved: a lightweight
active-objective file that loads itself, a permanent append-only archive, a defined CLI workflow, and this
objective register.

**Key Deliverables.** `BLAST/Objective.md` reduced to ~2.3 KB and auto-loaded; this file
(`objective_original_origin.md`) as the permanent archive; the `@BLAST/Objective.md` import and the
`UserPromptSubmit` hook in `.claude/settings.json`; `CLAUDE.md` §Active instructions, §Standard workflow
and §Objective lifecycle; the workspace-structure review; `pending-tasks-in-queue.md` retired into §6.

**Related Files.** `CLAUDE.md`, `BLAST/Objective.md`, `BLAST/CLAUDE.md`, `BLAST/README.md`, `BLAST/LLM.md`,
`.claude/settings.json`, root `README.md`, `Reports/README.md`, `workbench/` docs, `Graphify/README.md`,
`required-context/01-Data-Gap-Analysis.md`.

**Reason for Archiving.** Not archived — governance is ongoing. Tracked through decisions D5–D17 rather
than through `BLAST/Objective.md`, because process rules stored in that file would be erased by the next
instruction they govern.

**Pending Work.** One measured contradiction is unresolved: how many of the 70 declared controllers are
absent from `pam/PAM` — `CLAUDE.md` previously said 23, while `required-context/01-Data-Gap-Analysis.md`
and `SOURCE-MAP.md` both say 54. Re-measure before quoting either.

**Lessons Learned / Observations.** File size is functional, not cosmetic — at ~16.5 KB `Objective.md`
exceeded the hook's inline-injection limit and was spilled to a side file with only a preview reaching
context; under the limit the whole file lands every prompt. On this machine `shell: "powershell"` is
unusable (no `pwsh`, no `jq`), PowerShell 5.1 serialises `Get-Content -Raw` as `{"value":…}` rather than a
string, and its console output defaults to ANSI, which destroys em-dashes and `⛔` markers — all three were
caught only by pipe-testing the hook before trusting it.

**Dependencies.** Governs all future objectives. Related: decisions D5–D17.

---

### OBJ-007 — Validation depth, mandatory-field evidence and the `document/` deliverable set

**Status:** ✅ Completed — superseded as the active instruction by OBJ-008

**Summary.** An 18-point instruction covering three things at once: (a) build a single consolidated
documentation set under a new top-level `document/` folder, multi-worksheet Excel rather than many files;
(b) analyse in depth what the 2026-07-29 run measured but never explained — the 196 `MISSING ['NEW_ID']`
L5 chaining failures, the 105/107 L6 read-back failures, the 3-of-6,738 `[Required]` gap; (c) deepen the
framework itself — full-envelope negative validation, response-body/schema/error-code assertions, and a
`DBUtils` rewrite off its MySQL assumptions onto SQL Server, now that QA DB credentials exist.

**Key Deliverables.** `document/` (all reports, Excel workbooks, observations, findings, summaries);
consolidated workbooks carrying the Chaining / Positive / Negative / L6-read-back / Observations /
Management-Findings / DB-validation worksheets; framework changes in `pam_automation_bootstrap` on `AI`
(validation layers + `DBUtils`); refreshed `workbench/` briefs and `Reports/` docs.

**Related Files.** `Reports/Runs/2026-07-29_181439/results.json` (326 flows · 1,873 hops · every L1–L7
check verdict — the evidence base for the whole analysis), `workbench/scripts/chain_runner.py`,
`workbench/scripts/source-map.json`, `workbench/document-gap.md`, `workbench/developer-loopholes.md`,
`required-context/01-Data-Gap-Analysis.md`, `src/test/java/com/arcon/utils/DBUtils.java`,
`src/test/java/com/arcon/utils/ApiHelper.java`, `Environments/QA_MsSQL.properties`.

**Reason for Archiving.** Not archived — active. Status updated in place until complete. All 18 points have
been delivered in analysis and framework terms; what remains is owner-gated (commit approval) or
downstream (suite migration).

**Pending Work.** Nothing is committed — the `AI` branch carries the work uncommitted, awaiting approval.
**Live execution never ran:** no `PAM_API_TOKEN` was supplied, so every API-side figure derives from
`Reports/Runs/2026-07-29_181439/` rather than fresh measurement. Outstanding downstream work, all
QA-side and none blocked on a developer: migrating the 76 API suites onto `PamApiValidator`; rewiring the
negative suite (199 of 279 referenced data providers do not exist, and the 80 that resolve read the
*positive* sheets); fixing the `APIExcelReportUtil` data race and the `ApiHelper` Playwright leak before any
full-catalogue run; and the harness fix so an unresolved placeholder records `NOT RUN` rather than `FAIL`.
Enabling `L11` persistence assertions is blocked only on replacing the `sysadmin` login with a
least-privilege account.

**Lessons Learned / Observations.** The single most important lesson is methodological: **a `FAIL` is not
evidence of a defect, and a green suite is not evidence of correctness.** Both halves were demonstrated by
measurement. The prior run's headline "105 of 107 read-backs failed" turned out to be 97 checks that
searched each response for the literal string `${NEW_ID}` and could never have passed — carrying no
information about the product, while being read as product failure. In the opposite direction, the
framework's only application-envelope assertion read `success` in camelCase where the API emits `Success`
in **1,580 of 1,868** responses and lowercase in **0** — so a whole validation layer was disabled by one
letter while appearing to exist. This is why `NOT RUN` was made a first-class verdict distinct from both
`PASS` and `FAIL` (D21).

Substantive findings: **31** distinct response shapes, not 4–8, with only 6 documented. **70** responses
returned `Success:true` having written nothing, none caught. The 196 chaining failures split **117** genuine
create failures / **19** acknowledged-with-no-identifier / **0** extractor bugs / **60** indeterminate — so
the generator was sound and the contract was not. On the surface actually under test the declared-required
count is **0 of 5,175**, not 3 of 6,738, because all three `[Required]` attributes sit on a class in a
service that is not among the 70 controllers. Twelve constraint families return zero while the server
demonstrably enforces Newtonsoft's required check (123 live rejections), which reframes the developer
repository from *incomplete* to *the wrong repository*. The negative suite is largely non-functional and
partly inverted: 199 of 279 referenced data providers do not exist, and all 80 that resolve read the
**positive** sheets, so a class named `MissingParameter` submits valid data.

DB validation **is** possible and the API's writes do land in `ARCOSDB_U16SP2_WEBSM_QA` — confirmed three
independent ways. Three product security defects surfaced incidentally: deterministic at-rest encryption
(20,651 rows, 59 distinct `ss_port` ciphertexts — functionally AES-ECB), cleartext API passwords in
`sso_ApiUsers` alongside an unencrypted private key in `tbl_KeyEncryptionDecryption`, and **16,560**
authorisation rows pointing at deleted services with only **5** foreign keys across 552 tables. The `devops`
login is **`sysadmin`** over 30 databases, so read-only discipline is a safety control, not a preference.

**Corrected within this objective.** Two of my own conclusions were wrong and are recorded rather than
quietly dropped. I stated that no row on the server was newer than 2025-10-01 and inferred the QA API might
not write to the supplied database; the newest row is `2026-08-03 15:29:18`. The error was sampling one
column in the *wrong* databases and generalising to the instance — withdrawn as `OBS-012`, corrected by
`OBS-045`, `MF-07` rewritten. And `OBS-001` overstated encryption as universal; it covers three table
families, with the audit log and all keys and timestamps in plaintext. Separately, the long-standing
**23-vs-54** controller contradiction is settled at **58**: `54` was a hardcoded string literal in
`build_source_map.py:333` that no code computed, and `23` answered a narrower question. `Environments/QA_MsSQL.properties`
had shipped its `db_*` keys blank, and `AutoConfigs` read two of them from key names that existed in no
environment file — the mechanical reason no DB assertion had ever run.

**Dependencies.** Consumes OBJ-003's run artifacts and OBJ-005's gap analysis. Governed by OBJ-006.

---

### OBJ-008 — `questions/` — the project knowledge base

**Status:** ✅ Completed — *living document*; superseded as the active instruction by OBJ-009. The workbook is
delivered and validated; appends continue as new questions arise, which does not reopen the objective.

**Summary.** Build a single Excel knowledge base under a new top-level `questions/` folder capturing every
question someone might ask about this project, each with an answer, the supporting evidence, and comments.
Its purpose is threefold — demonstrations, documentation, and management discussion — so an answer without
a citation is not an answer. It is a **living** artifact: any new question arising in development or
discussion is added with its answer and evidence.

**Key Deliverables.** `questions/PAM-Project-Knowledge-Base.xlsx` — 3 sheets (`Index`, `Q&A`, `Demo Flow`),
16 columns, **241 questions**; `questions/data/questions-api.json` (76), `questions-framework.json` (75) and
`questions-project.json` (90) as its machine-readable source; `workbench/scripts/build_knowledge_base.py` as
the single writer and validator; `questions/README.md` and `questions/_AUTHORING-CONTRACT.md`.

**Related Files.** Draws its answers from the whole workspace: `document/` (the OBJ-007 reports and
workbooks), `Reports/Runs/2026-07-29_181439/`, `Reports/Issues/`, `workbench/developer-loopholes.md`,
`workbench/document-gap.md`, `required-context/`, `objective_original_origin.md` + `objective-history/`,
the root `CLAUDE.md` and `README.md`, `AGENTS.md`, and the automation repo itself.

**Reason for Archiving.** Not archived — active. Status updated in place until complete.

**Pending Work.** The workbook is delivered and validated. **By design this objective never fully closes:**
the register entry stays `In Progress` while the workbook remains a living document, and new questions are
appended as they arise. Outstanding items it surfaced rather than resolved: the **blocklist guard** in
`ApiHelper` (`MF-16`, P0, not applied — awaiting a decision); the **4 `Open` questions**, each of which names
what would settle it (error-code register · endpoint-to-role matrix · a `SELECT` confirming the 19
acknowledged creates · any response schema at all); and **one agreed counting rule** for the negative corpus,
which must live in a script rather than in prose.

**Lessons Learned / Observations.** One design decision taken at intake: the owner delegated the
single-sheet-versus-many-sheets choice, and a **single master Q&A sheet with a `Category` column** was
selected over per-topic sheets, which force a filing decision on every new question and invite the same
answer being duplicated. One sheet plus autofilter gives every per-topic view without duplicating a row.

**241 questions across 20 categories** were authored — 226 `Answered`/`with caveats`, 4 `Open`, 1
`Superseded` — with **zero uncited rows**, enforced by the builder rather than by discipline: a row missing
evidence is stamped, forced to `Open`, listed on the `Index` sheet, and **fails the build**. Average answer
length is 740 characters, and no answer is under 120.

Two things emerged that the objective did not ask for and that matter more than the workbook.

**First, a live safety gap.** The endpoint blocklist that has prevented an API outage since `ISSUE-010` is
enforced in the documentation and in the Python harness but **not in the Java framework CI runs**.
`testdata/API_Automation_Test_Input_Data.xls` holds **102 rows across 50 controllers** targeting blocklisted
action names, all expecting HTTP 200 — including rows 16–17, the two `ActivityLogs` endpoints that stop the
IIS application pool. `ActivityLogs` is the single API class activated by `CICD_Suites/APISuite.xml`, **and
by a root `testng.xml` that arrived git-tracked in the `Dev` merge** and that both `AGENTS.md` and the repo
`CLAUDE.md` asserted did not exist. IDEs pick up a root `testng.xml` by convention, so pressing *Run* is a
path to a 503. Recorded as `OBS-047`/`OBS-048`/`MF-16`; the guard was **not** applied, being outside this
objective's scope while `OBJ-007` is still awaiting review.

**Second, the exercise of writing cited answers found figure drift that reading never would.** Ten figures
across nine documents were corrected — including two of my own drafting errors in report `B`. The most
instructive is the negative-corpus row count: **five** figures were in circulation (3,167 · 3,317 · 3,652 ·
3,620 · 3,728) and **none was wrong** — they count different things. I counted it myself, got a sixth
answer, and concluded the honest resolution is that the total is **definition-dependent** and must not be
quoted bare; the stable figures (the 1,604/1,550/13 split) should be quoted instead. Declaring a sixth
"settled" number would have repeated the original error with more confidence. The equivalent applies to
payloads-bound-to-an-endpoint, where 1,654 and 1,605 differ on how unparseable examples are classified and
both are correct under their own definition.

**Dependencies.** Consumes the output of OBJ-007 and the measured evidence from OBJ-003. Governed by OBJ-006.

---

### OBJ-009 — Gold-standard business-context reference document

**Status:** ✅ Completed

**Summary.** Produce one Markdown document that answers *"How do you provide business context to the AI?"*
by being opened and walked through in front of management. The worked example is the five-level
**Service Creation → Service Password Request → Approval** validation flow. It doubles as a reusable
template: §0 is a twelve-point checklist to fill in for any new feature.

**Key Deliverables — two files, deliberately different lengths.** ⭐ `document/BUSINESS-CONTEXT-DEMO.md`
(~150 lines) is **the one used live**: seven short sections, the 5-hop service-creation chain with the
measured values from run `2026-07-29_160155` (`LobId 108` → `ServerGroupId 282` → `ServiceId 25339`
→ `ServiceSessionId 75277` → found), and a five-point management takeaway. Added on the owner's amendment
that the full document was too much for a demo. It points at, rather than duplicates,
`document/BUSINESS-CONTEXT-STANDARD.md` — 27 numbered sections, 929 lines. That one covers all
eighteen elements the owner listed, plus nine the cross-check showed were missing and that each correspond to
a failure mode actually observed in this project: glossary · preconditions and environment configuration ·
database validation points · negative scenarios distinct from edge cases · non-functional expectations ·
safety constraints · known defects affecting the flow · what is NOT known · traceability. Registered in the
root `CLAUDE.md`, root `README.md` and `document/README.md`.

**Related Files.** `workbench/scripts/flows/03_service_lifecycle.json` (the measured five-hop chain);
`src/test/java/com/arcon/tests/UI/EndToEnd/raiseRequestServicePassword/ServicePasswordRequestFiveLevelTest.java`
(the approval reference test); `workbench/scripts/source-map.json` (field provenance);
`Reports/Runs/2026-07-29_181439/results.json`; `sso_arcos_wft_details` and
`sso_arcos_workflow_request_type` in `ARCOSDB_U16SP2_WEBSM_QA`; the `document/reports/` set.

**Reason for Archiving.** Completed — the document is delivered and verified. It is a reference standard, so
it is amended when a fact it cites changes, not rewritten per objective.

**Pending Work.** None for the document. It **surfaces** rather than resolves: `SC-16` (the API-driven
approval test) is designed in §8B and not built; `SC-17` (DB validation of the approval chain) is designed in
§12 and not built; twelve `UNKNOWN`s are catalogued in §25 with what would settle each.

**Lessons Learned / Observations.** Writing this exposed how much of a "known" flow was actually
undocumented, and the exposure came from the discipline of citing every claim rather than from any new
measurement.

Three findings worth carrying forward. **The one endpoint that performs an approval has never been called by
automation** — `NotificationDetails/ServicePasswordRequestApproveReject` was not exercised in the
2026-07-29 run, while every read endpoint around it was; surrounding coverage invites exactly the wrong
inference. **The approval chain is UI-automated only** — the API variant of the reference test exists but is
commented out (lines 219–359), and in the live UI path the per-level message assertions are *also* commented
out (lines 115–116, 125–126, 135–136, 145–146, 155–156), so the approvals execute without asserting their
expected messages. And **the approval status codes are undocumented**: `wft_approver_l1_status` takes exactly
three values across 389 requests — `3` (224), `0` (98), `9` (67) — and inferring "3 = approved" from
frequency would have been a guess, so it is recorded as `UNKNOWN` instead.

Grounding that made the document credible rather than plausible: **22 genuine five-level requests** exist in
the QA database (levels 1→282, 2→63, 3→21, 4→1, 5→22), `sso_arcos_wft_details_approver` holds 96,687 rows,
and the schema carries `wft_approver_l{1..5}_status`/`_status_on`/`_comment` — so the five-level flow is a
real, exercised product path and the database assertions in §12 are constructible today.

Also confirmed and stated plainly: **no Swagger specification covers any endpoint in this flow.** The 37
specs describe a different surface (~6% name overlap, 0 of 690 declaring any 4xx/5xx), so the honest answer
to "what is the Swagger reference?" is `NOT DOCUMENTED`, with Confluence page citations as the substitute.
And **`required_hint = false` on every field** of the create payload — consistent with 0 of 5,175 declared
mandatory on the surface under test.

**Dependencies.** Consumes OBJ-003's measured run, OBJ-007's analysis and framework, and OBJ-008's Q&A
corpus. Governed by OBJ-006.

---

### OBJ-010 — Full API suite re-execution and N-1 vs N execution benchmark

**Status:** ✅ Completed — executed, validated and reported. See the completion record appended at the end of
this entry.

**Summary.** Re-execute every API test that exists in the project against `QA_MsSQL` — positive, negative,
chaining, regression and boundary scenarios, explicitly *not* limited to the scope of the previous run —
then validate the results and produce an execution summary plus a management-facing **`Execution Benchmark`**
worksheet comparing the previous run (N-1) with this one (N). A metric absent from N-1 is marked `N/A`
rather than dropped. Token is generated once and reused for its 24 h life; if the environment drops, the run
waits 5 minutes and resumes from the stopping point rather than restarting.

**Key Deliverables.** Execution summary in the existing reporting format · new `Execution Benchmark`
worksheet (total executed, pass/fail/skip/blocked, status and success-rate comparison, newly added tests,
fixed failures, new failures and regressions, performance, trend, observations, recommendations) · concise
management summary. All pending the owner's clarification round.

**Related Files.** Candidate N-1 runs `Reports/Runs/2026-07-29_181439/` (full generated run — `results.json`,
`checkpoint.json`, `RUN_REPORT.md` at 6,621 non-blank lines) and `Reports/Runs/2026-07-29_160155/` (the
three-flow chaining demo); `Reports/Summary/Full-Generated-Run-2026-07-29.md`;
`Reports/Summary/API-Chaining-Feasibility-Demo.md`; `workbench/scripts/chain_runner.py` (owns the
`--downtime-wait 300` / `--resume <folder>` / `checkpoint.json` behaviour the owner refers to as already
implemented); `workbench/scripts/token_guard.py`; `workbench/scripts/run_qa_mssql.py`;
`workbench/scripts/run_validation.py`; `Automation gitlab repo/pam_automation_bootstrap/API_Suites/`
(78 suite XMLs across `Positive_All/` 71, `Negative/` 5, `Positive/` 1) and
`src/test/java/com/arcon/tests/API/` (467 classes).

**Reason for Archiving.** Not archived — active.

**Pending Work.** All of it. Blocked at the owner's clarification round: which execution engine defines
"the entire API test suite" (Java/TestNG, the Python harness, or both), how the app-pool blocklist is to be
handled when "execute everything" collides with it, where the `Execution Benchmark` worksheet lives, and
which run is N-1.

**Lessons Learned / Observations.** Measured while scoping, before any execution:

**"Every API test" is ambiguous across two engines, and the previous run used the one that is not the Java
framework.** `Reports/Runs/2026-07-29_181439/` contains `checkpoint.json` + `results.json` + `RUN_REPORT.md`
and no `.xlsx` — the signature of `workbench/scripts/chain_runner.py`, not of a Maven/Surefire run. So a
literal like-for-like N-1 comparison is a harness comparison, while "every API test implemented in the
framework" is a Java/TestNG comparison against a baseline that does not exist.

**168 of 467 API test classes are referenced by no live suite entry** — 157 of 386 under `Negative_API`,
9 of 79 under `All_API_Positive` — counted after stripping XML comments so commented-out `<class>` entries
do not falsely count as covered. Running the 78 existing API suite XMLs therefore executes at most 299 of
467 classes and would silently satisfy neither "every API test" nor "nothing skipped unintentionally".
Closing that gap needs generated suite XMLs.

**The downtime-wait-and-resume capability is real but lives only in the Python harness.**
`chain_runner.py` implements `--downtime-wait` (default 300 s), `--resume <folder>` and `checkpoint.json`
(`chain_runner.py:259, 326-333, 867-894, 972-1004`). No equivalent exists on the Maven/TestNG path, so the
owner's environment-handling requirement is satisfiable as stated only for a harness run.

**Both token paths are already warm, so the once-only requirement costs zero `/arcontoken` calls.**
`token_guard.py status` reports a valid cache with 1,366 minutes left (`APIUserId: 2`) and no latch; the
committed `ApiToken=` in `Environments/QA_MsSQL.properties` decodes locally to an expiry of
2026-08-06 09:37 +05:30. Since `ApiHelper.getToken()` returns a non-empty `ApiToken` verbatim with no
expiry check, the Java path also performs no token request while that value holds.

**Port confusion resolved rather than assumed:** `environmentUrl` is `:1302` (app) and `environmentAPIUrl` /
`pam_BaseAPIURL` are `:6302` (API), matching `lh_common.py:61-62` (`API_BASE` / `APP_BASE`). The
`Objective.md` header previously cited only `:6302`; it now states both.

**Two known framework defects bear directly on a full-scale run** and are recorded in
`.claude/rules/automation-repo.md`: `APIExcelReportUtil` increments a `static int rowIndex` unsynchronised
while API suites run `parallel="classes"`, so rows can overwrite each other in `Api_Report.xlsx`; and
`ApiHelper` calls `Playwright.create()` per request without closing, which at full-catalogue scale is a
resource problem rather than a nuisance.

**Dependencies.** Baseline evidence from OBJ-003 (`2026-07-29_181439`) and OBJ-002; validation layers and
`document/` workbook tooling from OBJ-007; safety blocklist from OBJ-004 (`LH-08`, `ISSUE-010`).
Governed by OBJ-006.

---

---

### OBJ-010 — completion record

**Status:** ✅ Completed.

**Summary.** Executed through the dynamic framework only, as the owner's amendment required — no `mvn`, no
TestNG, no suite XML. The bootstrap repo was read purely as a generation input. **747 flows / 5,590 test
cases** generated and run against `QA_MsSQL`, **5,416 executed**, **3,459 passed (63.9%)**, reaching **1,388
distinct endpoints** versus N-1's 870. The comparable subset is stable: 858 cases, **856 unchanged**, 1 fixed,
1 regressed. Two material defects surfaced that N-1 structurally could not find.

**Key Deliverables.**
- `Reports/Runs/2026-08-05_114315/QA_MsSQL_API_Execution.xlsx` — 9 worksheets including the required
  **`Execution Benchmark`** (N-1 vs N, with `N/A` wherever N-1 captured no such metric)
- `Reports/Runs/2026-08-05_114315/RUN_REPORT.md` — existing reporting format
- `Reports/Summary/OBJ-010-Execution-Benchmark.md` — the management summary, 12 sections
- `Reports/Runs/2026-08-05_114315/validation.json` — the ten-gate checklist, all passing
- `Reports/Runs/2026-07-29_181439/rescore.json` — N-1 re-judged under the corrected validator, **0 HTTP calls**
- New scripts: `generate_data_flows.py`, `obj010_datatables.py`, `obj010_rescore.py`, `obj010_collect.py`,
  `obj010_build_workbook.py`, `obj010_admin_auth_probe.py`

**Related Files.** `workbench/scripts/chain_runner.py` (validator + guards + resume, all amended) ·
`generate_flows.py` · `.obj010/blocked-rows.json` · `.obj010/segments.json` · `BLAST/findings.md` F7–F19 ·
`Reports/Runs/2026-08-05_114315/evidence/` (5,424 files).

**Reason for Archiving.** Objective delivered in full: every module executed, results validated before
reporting, benchmark and management summary produced.

**Pending Work.**
- ⛔ **Raise the invalid-token finding as a `PAMIT` security ticket** — 19 endpoints, several writes, several
  disclosing real data. Not raised in this session; evidence is packaged and ready.
- The `/AdminAPI` question needs an owner decision: 2,104 test rows target a surface that returns 404 on both
  ports. Deployment gap, or rows that will never be runnable here?
- 348 endpoints returning 404 (25.1% of those exercised) need triage — deployment gap or stale catalogue.
- QA app-pool instability: 85 of 329 minutes were spent waiting, across 17 downtime pauses.
- Teardown remains disabled, so 146 destructive rows are still unexecuted and this run's created records
  (seeds `0I3YEV` and `EDLFK3`) remain in the environment.

**Lessons Learned / Observations.**
- **A test that cannot fail for the right reason is worse than no test.** 1,153 `*_UnauthorizedAccess` cases
  asserted 401 while sending a valid token. Making them send an invalid one turned inert assertions into a
  real security finding — the single highest-value change in this objective.
- **Status codes are not verdicts on this API.** 1,022 cases (18.9%) returned HTTP 200 while failing
  validation. A status-only assertion would have called all of them green.
- **Re-score the baseline instead of caveating it.** Because every N-1 response body was retained, the
  corrected validator could be applied offline with zero HTTP calls. It changed **nothing** — which both
  removed any caveat from the benchmark and proved the generators deterministic (1,868/1,868 hops matched a
  week later).
- **Parse order is a safety property.** Splitting a path on `/` before stripping its query string produced a
  garbage "action name" that feeds the blocklist and destructive guards. Measured impact was nil (1 row, no
  decision changed) but the class of bug is serious, and it also crashed a 4-hour run via an illegal filename.
- **A checkpoint must distinguish "done" from "gave up".** Resume skipped `ABORTED` flows because they were in
  the checkpoint, which would have silently dropped coverage. Fixed, plus a gate so it cannot recur unnoticed.
- **Resumed runs lie about their own metadata.** `meta.elapsed_s` / `calls` / `downtime_events` cover the last
  process only — 94.9 min reported against 329.1 actual. Reconstructed into `.obj010/segments.json`.
- **Substring matching on config keys is a trap.** `API_ExcelDataProviderFileName` is a substring of
  `Negative_API_ExcelDataProviderFileName`; longest-key-wins recovered ~2,450 rows the earlier inventory had
  written off.
- Flow-level pass rates mislead on long chains. Quote the **hop rate**: N-1 is 64.2%, not 9.2%.

**Dependencies.** Baseline `Reports/Runs/2026-07-29_181439` (OBJ-003); validation layering and workbook style
from OBJ-007; safety blocklist from OBJ-004 (`LH-08`, `ISSUE-010`); token latch policy from `ISSUE-009`.
Governed by OBJ-006. The standing rule that *"Execute everything" means the dynamic framework, never the
bootstrap suite* was recorded in the root `CLAUDE.md` during this objective.

---

### OBJ-011 — Portable onboarding kit: replicating the solution on a new project (`IDEV`)

**Status:** ✅ Completed — guide rewritten, kit built, recommendation given. See the completion record at the
end of this entry.

**Summary.** The dynamic API generation solution proved itself on PAM under OBJ-010 and is PAM-hardcoded.
This objective makes it portable: rewrite `workbench/new-project-implementation.md` as a generic onboarding
guide covering prerequisites, dependencies, configuration, implementation steps, assumptions and the
project-specific questions to answer before starting; then recommend how the solution becomes reusable
across projects rather than PAM-specific. Two architectures are to be compared — reusable **AI Skills**
versus a **standard instruction/template document** consumed by the AI — with a single final recommendation
suited to a management audience. First target project is `IDEV`, about which the workspace holds nothing.

**Key Deliverables.** Rewritten `workbench/new-project-implementation.md` (generic onboarding guide) ·
two architecture approaches with advantages and disadvantages · a comparison on scalability, maintainability,
ease of adoption and long-term support · one final recommendation.

**Related Files.** `workbench/new-project-implementation.md` (the artifact under revision, previously
132 lines, last updated 2026-07-30 and carrying the superseded 326-flow / 1,868-call figures) ·
`workbench/scripts/chain_runner.py` (the generic executor, and where the PAM-specific constants live:
`REPO`, `ENV_FILE`, `ENV_NAME`, `ENDPOINT_BLOCKLIST`, `DESTRUCTIVE`, the `/api/ADbridging/GetLOBList`
health probe, `CREATED_MESSAGES`) · `generate_flows.py` (the `${LOB_ID}` alias map and the LOB prelude) ·
`generate_data_flows.py` · `token_guard.py` · `workbench/skills/*.SKILL.md` (six existing specs, PAM-bound
and aimed at the Java bootstrap rather than the dynamic framework) ·
`document/BUSINESS-CONTEXT-STANDARD.md` §0 (the twelve-item context checklist) ·
`Reports/Summary/OBJ-010-Execution-Benchmark.md` (the current measured figures).

**Reason for Archiving.** Not archived — active.

**Pending Work.** All of it. Objective recorded; owner's clarification round outstanding on four points:
what is known about `IDEV`, whether the deliverables are one file or several, whether this objective builds
the reusable scaffolding or only recommends it, and what management-facing asset is wanted.

**Lessons Learned / Observations.** Established while scoping, before writing:

**The executor is already generic; the couplings are few, named and local.** `chain_runner.py`'s
domain-specific surface is a short list — the workspace-root probe, the properties file and env name, the
blocklist, the destructive-name regex, the health-probe endpoint, the envelope field names (`Success` /
`errorCode`), and `CREATED_MESSAGES`. `generate_flows.py` adds two more: the `${LOB_ID}` alias map and the
hardcoded LOB prelude. That is what makes a profile-driven adapter design credible rather than aspirational.

**The six existing `workbench/skills/*.SKILL.md` files are not reusable as they stand, for two separate
reasons.** They are PAM-hardcoded (the envelope, `APIConfig`, `PAMIT`), and they target the **Java/TestNG
bootstrap** rather than the dynamic Python framework that actually produced OBJ-010's result — so they
encode the architecture the owner's standing rule says not to execute.

**The guide's own figures were stale before this objective started.** It cited 326 flows / 1,868 calls /
870 endpoints from `2026-07-29`; OBJ-010 superseded that with 747 flows / 5,590 cases / 5,416 executed /
1,388 endpoints. A guide that under-states the reference implementation understates the case for reuse.

**Dependencies.** Measured figures from OBJ-010; the validation layering from OBJ-007
(`com.arcon.utils.validation`, L1–L12); the safety blocklist from OBJ-004 (`LH-08`, `ISSUE-010`); the
token-latch policy from `ISSUE-009`; the context checklist from OBJ-009. Governed by OBJ-006.

---

### OBJ-011 — completion record

**Status:** ✅ Completed. Zero HTTP calls; no environment contact; no framework code changed.

**Summary.** `workbench/new-project-implementation.md` rewritten from 132 to 505 lines as a project-agnostic
onboarding guide, and the executable half of it built as `workbench/onboarding/` — a profile schema, PAM as
the worked example, a blank template, a readiness gate and a portable onboarding skill. Two architectures were
compared and one recommended: **the AI Skill as the delivery vehicle, with the document retained as its
human-facing specification and one of its inputs rather than as the mechanism.**

**Key Deliverables.**
- `workbench/new-project-implementation.md` — 505 lines, 18 sections: what transfers · the five hard-gate
  inputs · technical / operational / human prerequisites · the seven-phase workflow · configuration · 15
  project-specific considerations · what to skip · design decisions · **the coupling inventory (§8)** ·
  effort-reduction opportunities (§9) · **both approaches (§10)** · **the comparison (§11)** · **the
  recommendation with a read-aloud management passage (§12)** · 15 pitfalls · effort reference · the `IDEV`
  readiness table (all `UNKNOWN`) · assumptions · a provenance table for every claim class
- `workbench/onboarding/profile.schema.json` (285) — the contract; every field is a place the harness
  currently hardcodes a PAM fact, annotated `x-blocker` / `x-degrades`
- `workbench/onboarding/profiles/pam.json` (182) — the worked example, authored from the working scripts
- `workbench/onboarding/profiles/_template.json` (140) — what a new project copies; every `UNKNOWN` is a real
  question with an owner
- `workbench/onboarding/validate_profile.py` (315) — the readiness gate; stdlib only, ASCII output, zero HTTP
- `workbench/onboarding/skills/api-onboarding/SKILL.md` (107) + six phase references (566) — the portable
  skill, holding no project facts
- `workbench/onboarding/README.md` (44)

**Related Files.** Root `CLAUDE.md` (workbench row now lists six subfolders; the briefs line points at the
kit) · `workbench/README.md` (rewritten subfolder table — it had been omitting `scripts/` entirely) ·
`objective-history/04-narrative-log.md` (the full narrative entry) · `Reports/Summary/OBJ-010-Execution-Benchmark.md`
and `workbench/developer-loopholes.md` §13 / `LH-13` (the sources for every measured figure quoted).

**Reason for Archiving.** Delivered in full: guide rewritten, both approaches specified with advantages and
disadvantages, comparison on all four requested axes, one final recommendation, and the scaffolding built.

**Pending Work.**
- **The scripts do not yet read the profile.** It documents the couplings rather than driving them. The
  refactor is scoped in `new-project-implementation.md` §8 as four steps; step 2 is a PAM parity re-run diffed
  against `results.json`, provable offline from retained evidence.
- **`probe_to_profile.py`** — the highest-value remaining build, and small: emit a profile's `envelope` section
  directly from a probe run, removing the last hand-transcription step.
- **Every `IDEV` fact.** All ten rows of the readiness table are `UNKNOWN`; the day-one questionnaire has not
  been sent. No `IDEV` duration estimate is defensible yet — only the shape of one: materially less work than
  PAM required, concentrated in a single risk (payload availability). Phase 0–1 produces the costed go/no-go.
- Running the validator in CI so a profile cannot silently decay.
- The four prerequisites in §12's sequenced ask need owner approval before `IDEV` Phase 0 can start.

**Lessons Learned / Observations.**
- **The couplings are few, named and local.** PAM-specific facts in 1,806 lines of harness code reduce to
  eleven places, listed with line references in §8. That is what makes a profile boundary credible rather than
  aspirational — and it was not obvious before it was inventoried.
- **A schema without a gate is a suggestion.** The measurable gap between the two profiles *is* the onboarding
  worklist: `pam.json` exits `0` (0 blockers, 0 warnings, 5 declared unknowns), `_template.json` exits `1` with
  13 blockers and 6 warnings, each naming its owner.
- **Neither architecture can enforce anything by itself.** The validator and the deny-by-default machinery are
  what enforce; the prose and the skill both merely instruct. Identifying the gate as the load-bearing
  component is what makes the recommendation defensible rather than a matter of taste.
- **The recurring cost is procedure, and the recurring failure is ordering.** Every expensive PAM mistake was a
  step taken before the step that would have informed it. Phase gates address that; a document cannot.
- **The existing `workbench/skills/*.SKILL.md` set is not reusable for two independent reasons** — PAM-hardcoded
  *and* aimed at the Java/TestNG bootstrap rather than the dynamic framework. Worth stating before anyone
  proposes reusing them for `IDEV`.
- **One adapter is not an abstraction.** Expect the second onboarding to modify the machinery a little; expect
  the third not to.
- **The guide's own figures had gone stale by a full objective** and nothing flagged it — which is itself the
  strongest argument in §11 against a document as the primary mechanism.

**Dependencies.** Measured figures from OBJ-010 (`Reports/Runs/2026-08-05_114315`) and OBJ-003
(`2026-07-29_181439`); the L1–L12 layering from OBJ-007; the safety blocklist from OBJ-004 (`LH-08`,
`ISSUE-010`); the token-latch policy from `ISSUE-009`; the auth-bypass finding from `LH-13`; the
context-checklist standard from OBJ-009. Governed by OBJ-006. **Blocks nothing; blocked on the owner's
approval of the §12 prerequisites for `IDEV`.**

---

### OBJ-010 — follow-on record: LH-13, the §5 correction, and a documentation sweep

**Status:** ✅ Completed. Closes the "raise/record the security finding" item from the OBJ-010 completion
record's Pending Work. **No Jira ticket was raised** — the owner explicitly withheld that.

**Summary.** The OBJ-010 findings had not propagated into the findings pipeline. Added **LH-13** as the
thirteenth finding, re-measured LH-05/§5 against the newer run, and swept every affected document.

**Key Deliverables.**
- **`Developer-Loopholes/LH-13-endpoints-accept-invalid-auth-token/`** — `EVIDENCE.md`, `EVIDENCE.xlsx`,
  `JIRA-TICKET.md`, `data/`. 57 endpoints answered HTTP 200 to an invalid bearer; **19 in scope** after
  excluding 34 health probes and 4 client-bootstrap endpoints; **6 writes**, **8 disclosing data**
- **`workbench/scripts/lh_specs_obj010.py`** — the LH-13 spec, in its own module
- **`LoopholeSpec.run_id`** in `lh_common.py` — lets a pack pin its own source run. LH-13 reads
  `2026-08-05_114315`; LH-02…12 stay pinned to `2026-07-29_181439`. Verified: rebuilding all packs reproduces
  every previously published figure unchanged
- **`workbench/developer-loopholes.md`** — new §13; §5 re-measured **135 → 348 of 1,388 (25.1%)** with the
  older figure retained and attributed; §15 re-ranked (LH-13 displaces `[Required]` at rank 1); §16 evidence
  paths updated for both runs
- Swept: `Developer-Loopholes/README.md` + `PLAN.md`, root `CLAUDE.md`, `.claude/rules/api-surface.md` +
  `markdown-docs.md`, `Reports/README.md`, `writer/writer.md`, `workbench/overview.md`,
  `self-understanding.md`, `document-gap.md`, `required-context/01-Data-Gap-Analysis.md`, and the
  `JIRA-TICKET.md` boilerplate (the hardcoded "all 12 findings" is now count-agnostic)

**Related Files.** All of the above, plus `BLAST/findings.md` F14–F20.

**Reason for Archiving.** Delivered. The findings pipeline is consistent again: brief → pack → (held) ticket.

**Pending Work.**
- ⛔ **`LH-13` is not raised in Jira.** Owner's decision, deliberately withheld. Evidence pack complete.
- ⛔ **`required-context/02-Data-Access-Requests.md` needs rebuilding** — see Lessons below. §0–§10 were
  destroyed during this work. The file carries a loss notice, the recovered skeleton and a rebuild guide.
  **Untried recovery path: VS Code Timeline / Local History**, which only the owner can check.
- The `/AdminAPI` ruling and the route-dump ask are now recorded as owner decisions 6 and 7.

**Lessons Learned / Observations.**
- ⛔ **I destroyed an authored document, and the rule that would have prevented it already existed.**
  `Path.write_text()` truncates in `w` mode *before* encoding, so a `UnicodeEncodeError` mid-write leaves the
  file destroyed rather than unchanged. The error came from writing an emoji as two lone surrogate escapes
  instead of `\U0001F534`. ~12.7 KB was unrecoverable: the folder is unversioned, no shadow copies, not in the
  Recycle Bin. `.claude/rules/markdown-docs.md` already said *"Use the Edit tool for text files"* and is now
  hardened with three explicit rules. **In a workspace where most folders are unversioned, a destructive edit
  is permanent — use `Edit`, never a whole-file write.**
- **The lost content was not reconstructed from memory, deliberately.** Inventing eight plausible access
  requests would breach the evidence-or-`UNKNOWN` standard more seriously than the loss itself.
- **A finding can outrank the list it joins.** LH-13 arrived thirteenth and displaced the long-standing rank-1
  recommendation. A priority summary is not append-only; re-rank it when the evidence says so.
- **Pin a pack's source run rather than repointing the shared one.** `run_id` let LH-13 use the new run while
  LH-02…12 stayed byte-reproducible against the old one — the alternative would have silently restated eleven
  published figures.
- **Hardcoded counts in generated output go stale silently.** The ticket boilerplate read "all 12 findings"
  and was wrong the moment LH-13 existed. It is now count-agnostic; the brief states its own count.
- **Superseding a measurement means keeping both.** §5 now carries 135 (N-1) *and* 348/1,388 (N) with the
  basis for each, because the packs still legitimately measure 135 against their pinned run.

**Dependencies.** Follows the OBJ-010 completion record. Feeds OBJ-004 (the loophole/Jira track), which stays
🟡 In Progress with 12 of 13 packs held. Unblocks nothing in OBJ-011.

---

### OBJ-012 — Management presentation for the API Dynamic Data Generation Tool

**Objective ID.** `OBJ-012`

**Title.** Management presentation for the API Dynamic Data Generation Tool (`Prepare-1.pptx`), styled on the
QA Buddy deck.

**Status.** ✅ Completed.

**Summary.** The owner supplied `writer/PPT/QABuddy_AI_Test_Automation.pptx` as a style reference and asked for
a management-ready deck of at most 10 slides covering the PAM dynamic API generation work — achievements,
technical capability, business value, the developer findings, the documentation gap and future enhancements.
The reference deck's design system was measured out of the file rather than approximated, and a 10-slide deck
was generated programmatically so it stays reproducible. Every figure traces to `OBJ-010` evidence,
`workbench/developer-loopholes.md` or `workbench/document-gap.md`.

**Key Deliverables.**
- `writer/PPT/Prepare-1.pptx` — 10 slides, 13.333×7.5in, speaker notes on all 10
- `workbench/scripts/obj012_build_ppt.py` — the generator, with a `SOURCES` block mapping every figure on
  every slide to its evidence file. **The deck is generated, never hand-edited** — edit the script and re-run

**Related Files.** Reference: `writer/PPT/QABuddy_AI_Test_Automation.pptx` (unmodified, verified by byte
length). Evidence consumed: `Reports/Summary/OBJ-010-Execution-Benchmark.md` §1–§3 ·
`Reports/Runs/2026-08-05_114315/RUN_REPORT.md` §1 · `workbench/developer-loopholes.md` §0 ·
`workbench/document-gap.md` · `workbench/new-project-implementation.md` §9 · `.claude/rules/api-surface.md`.

**Reason for Archiving.** Delivered in full: the deck exists, matches the reference style, holds no invented
figure, and its generator is installed alongside the other `objNNN_*` scripts.

**Pending Work.**
- The deck states an authentication-handling defect without specifics, per the owner's decision. **`LH-13`
  itself remains unraised** — that decision is still open and is tracked under OBJ-004.
- No measured effort baseline exists, so the impact slide carries capability facts only. If management wants
  an hours figure, it has to be **measured deliberately** — it must not be back-filled by estimate.

**Lessons Learned / Observations.**
- **A style reference should be measured, not eyeballed.** Reading the reference `.pptx` through `python-pptx`
  yielded the exact grammar — 115° `FFFFFF`→`FFFCF7` ground, decorative ovals at **`<a:alpha val="7000"/>`
  (7%)**, cream cards `F9EEDD` on `EADCC3` with a `0.09in` accent bar, header dot + eyebrow in `C25318` +
  accent bar + title, and an `E8722C` table header band with white caps. The 7% alpha is the detail that makes
  the big off-canvas circles work as a wash instead of a block of colour, and `python-pptx` has no API for it —
  it needs direct XML injection.
- **Without a renderer, geometry has to be audited arithmetically.** Neither LibreOffice nor PowerPoint COM was
  available, so a script checked every text box against the canvas and estimated wraps from glyph advance
  (~0.50×pt regular, 0.56×pt bold display). It caught four collisions the layout maths had hidden — a card body
  needing 4 lines in a 0.8in box, and a band overrunning the canvas by 0.03in.
- **The owner's recalled figure was wrong, and asking was correct.** The request said "12 developer loopholes";
  the measured count is **13** (`workbench/developer-loopholes.md` §0, 13 packs in `Developer-Loopholes/`).
  The owner confirmed 13. The "12" is still true of a *different* quantity — packs held rather than found —
  which is exactly how the confusion arises, and the deck now states both without contradiction.
- ⛔ **Two live figure conflicts were found while sourcing the deck, and both need settling.**
  **(a)** Invalid-token endpoints: `LH-13`'s own derivation gives **19** (57 responded 200, less 34 health
  probes and 4 client-bootstrap), but `Reports/Summary/OBJ-010-Execution-Benchmark.md` §1 and §5 say **23**.
  19 is the derivable figure; §5's headline should be corrected or its basis stated.
  **(b)** Documented ARCON error codes: root `CLAUDE.md` says **3**, `.claude/rules/api-surface.md` and
  `workbench/document-gap.md` say **4**. Neither figure went on a slide.
- **`/init` is not a substantive task.** The same session ran `/init` first; per `CLAUDE.md` §Standard workflow
  that is a process request, so `BLAST/Objective.md` was **not** overwritten with it — which mattered, because
  the file still held `OBJ-011`.

**Dependencies.** Consumes OBJ-010's measured run and OBJ-004's finding set; reports OBJ-011's onboarding kit
as the portability story on the final slide. Blocks nothing. The `LH-13` disclosure decision stays with the
owner under OBJ-004.

---

### OBJ-012 — amendment: the tool is named **Dynamic API Validator**

**Amends** the OBJ-012 record above, which is left as written per the append-only rule. The record's title and
its register row still read *API Dynamic Data Generation Tool*; that was the name in the instruction at the
time, and this entry is the correction.

**Decided.** The owner rejected *API Dynamic Data Generation Tool* and renamed the tool to **Dynamic API
Validator**. `writer/PPT/Prepare-1.pptx` is the authority for the name.

**Done.** Renamed in five places in `workbench/scripts/obj012_build_ppt.py` and the deck regenerated —
cover wordmark (`ARCON PAM | Dynamic API Validator`), the cover deck line, the module docstring, and the
slide-3 solution title, which changed from *"A test factory, not a test suite"* to *"Generated tests,
validated results"* so the headline reinforces the name rather than competing with it. Slide 3's speaker note
was reworded off the "factory" metaphor. Geometry re-audited: 10 slides, zero problems. `BLAST/Objective.md`
carries the amendment inline.

**Open.** The rename is **not** propagated across the wider document set. The literal string *API Dynamic Data
Generation Tool* only ever existed in the governance files; everywhere else the tool is called *the dynamic
framework* or *the AI dynamic API framework* — including a **standing rule** in the root `CLAUDE.md`
(§"Execute everything" = the dynamic framework, never the bootstrap suite), plus `workbench/overview.md`,
`writer/writer.md` and `Reports/Summary/`. Standardising those onto *Dynamic API Validator* is a deliberate
sweep the owner has not asked for, and it would touch a standing rule — do not do it incidentally.

**Lessons Learned / Observations.**
- **A coined name will spread further than the deck.** *API Test Factory* was invented for the cover wordmark
  and had already reached a slide title and a speaker note by the time it was rejected. Name the thing before
  writing copy around it, or the rename is a content edit rather than a find-and-replace.
- **An append-only archive handles a rename by amendment, not by rewrite.** Editing the record title would have
  been the intuitive fix and would have broken the rule; the register row is deliberately left stale and this
  entry carries the truth.

---

### OBJ-012 — amendment: owner review round, deck cut to 8 slides

**Amends** the OBJ-012 record and its rename amendment above, both left as written.

**Instructed.** The owner reviewed `Prepare-1.pptx` and gave seven changes: drop the cover's *"5,590 cases
anyway"*; drop the problem-slide cards *"Coverage is capped by typing speed"* and *"Negative testing was
absent"*; reframe the N-1 vs N slide as **Version 0.1 (positive API testing only) vs Version 0.2 (positive
and negative)** and stop leading on coverage numbers; exclude the *"Already Exists"* validation pending
clarification; explain *"31 response shapes"* in plain English for management; remove the slide titled *"1,022
tests would have passed anywhere else"*; remove the *"What changed, measured"* impact slide. Theme, formatting
and flow to stay unchanged.

**Done.** All seven applied; the deck is now **8 slides** (cover · problem · solution · how it works · version
progression · 13 findings · documentation gap · what next). Theme verified unchanged — same three Segoe UI
weights, same nine text colours, 13 decorative ovals still at 7% alpha, speaker notes on all 8, geometry audit
zero problems.

- **Cover.** Hero is now *"No hand-written tests. / Positive and negative."* The four chips were reworked off
  raw coverage figures (`1,388 endpoints reached`, `2.9x prior coverage` removed) onto capability statements,
  because keeping numeric coverage chips on the cover would have contradicted the owner's §3 direction.
- **Problem slide.** Two cards survive, relaid out as **full-width stacked** rather than left as a 2×2 grid
  with two holes. The deck line lost the phrase *"two people"* — an unevidenced staffing claim that should not
  have been there.
- **Version progression.** Replaced the metric table with a capability table: AI-generated / positive /
  negative / unauthorised-access and wrong-method / database persistence / envelope-aware, each marked
  `Yes` or `Not supported` per version. Basis for the split is `Reports/Summary/OBJ-010-Execution-Benchmark.md`
  §3, which lists the four dimensions that did not exist in N-1.
- **Findings table.** The *"Success: true when nothing was created"* row was removed with the Already-Exists
  content and replaced by *"Mutation exposed over HTTP GET"* (Medium) to keep six rows. **The headline count of
  13 is unaffected** — the table always showed a subset.

**Pending Work.**
- ⛔ **The Already-Exists finding (`LH-02`) is now absent from the deck entirely**, both as a validation
  capability and as a listed finding. The owner wants clarification before it is presented. It remains in
  `workbench/developer-loopholes.md` §2 and its evidence pack is untouched.
- The 1,022-cases-green-but-failing evidence and the failures-by-layer breakdown are no longer anywhere in the
  deck. They remain in `RUN_REPORT.md` §1 and the benchmark summary.

**Lessons Learned / Observations.**
- ⛔ **Corrected: the Dynamic API Validator asserts SEVEN layers, not twelve.** `chain_runner.py` registers
  exactly `L1 http-status · L2 content-type · L3 envelope · L4 message-semantics · L5 chain-key-extracted ·
  L6 record-exists · L7 latency`, which is also why `RUN_REPORT.md` §1 breaks failures down by seven layer
  names. **Twelve** belongs to `com.arcon.utils.validation.PamApiValidator` — the *Java* framework's validator
  from OBJ-007, a different component that this tool does not call. The first cut of the deck said
  "twelve-layer validator" on two slides and in a speaker note; all three are corrected to seven.
- ⛔ **Consequently, `writer/writer.md` §3 "seven-layer validation" was right, and the previous session's advice
  to "fix" it was wrong.** Only `writer.md`'s *"Eight response shapes"* is genuinely stale against the measured
  **31**; `workbench/overview.md` has the same eight-shapes drift plus three correct seven-layer references.
  **Do not "correct" the layer count in either file.**
- **Two of the owner's seven instructions conflicted, and the resolution was to preserve intent, not
  sequence.** Item 5 asked for a better explanation of the 31 response shapes; item 6 asked to delete the slide
  that carried it. The point was relocated onto the documentation-gap slide, where a *"6 of 31 documented"* card
  already lived, and rewritten in plain language. Deleting the slide and silently losing the item-5 content
  would have satisfied the letter of both and the intent of neither.
- **Removing cards from a grid is a layout change, not a deletion.** Two of four cards left a 2×2 grid visibly
  broken; the fix was a different arrangement, which is why "keep the formatting unchanged" and "remove this
  content" are not always simultaneously satisfiable without a judgement call.

**Dependencies.** Unchanged from the OBJ-012 record. The Already-Exists clarification is now a prerequisite for
restoring `LH-02` to any management-facing asset.

---

### OBJ-013 — Closed-loop system keeping every file configured and current (`v0.1`)

**Objective ID.** `OBJ-013`

**Title.** Closed-loop system keeping every file in the workspace configured and current automatically,
shipped as `v0.1`.

**Status.** ✅ Completed *(v0.1 scope; the register it produced is deliberately larger than v0.1 fixes)*

**Summary.** The project reached ~90% and the remaining cost was drift: facts measured once, quoted in a
dozen documents, then quietly going stale as the repos moved. Both repos were pulled (pull-only), the whole
workspace was rescanned by eight parallel domain audits with every finding adversarially verified, and a
detection-plus-repair loop was built and wired to a `SessionStart` hook. 192 raw findings became 180
confirmed; drift fell from 13 open to 3 open / 23 clean, with 8 mechanical corrections applied under backup.

**Key Deliverables.**
- `workbench/scripts/obj013_probes.py` — 18 probes re-deriving facts from source; read-only, offline,
  refuses state-changing git
- `workbench/.drift/facts.json` — fact registry (canonical value, unit, basis, derivation, quoting sites)
  plus 7 safety/governance invariants
- `workbench/scripts/obj013_scan.py` · `obj013_fix.py` · `obj013_loop.py`
- `workbench/scripts/obj013_rag_ingest.py` — 45 sources → 576 sections in `corpus/workspace.jsonl`
- `workbench/.drift/register.json` (180 confirmed + 12 refuted, reasons retained), `waivers.json`,
  `drift-report.json`, `backups/`, `fix-log.jsonl`
- `workbench/scripts/requirements.txt` — five real dependencies, measured
- `.claude/settings.json` — `SessionStart` hook + `permissions.deny` for push/merge
- Safety-gate repairs to `run_qa_mssql.py` and `run_validation.py`

**Related Files.** Modified: root `CLAUDE.md` (drift-control section, `@`-import removed, graph guidance
corrected, 5 measured figures), `.claude/rules/automation-repo.md` (D3 authority), automation repo
`CLAUDE.md` (real `@AGENTS.md` import) and `AGENTS.md` (community figures). Evidence:
`workbench/.drift/register.json`.

**Reason for Archiving.** `v0.1` delivered: the loop detects, reports, and repairs within the authorised
blast radius, and runs unasked via the hook.

**Pending Work.**
- **177 of 180 confirmed findings are unfixed** — `v0.1` mechanised only those promoted into `facts.json`.
- ⛔ **`api.endpoint_count` stays `report-only`.** Derivation gives 1,302 strict / 1,308 loose; the loose
  basis reproduces the documented 1,308 exactly, but the canonical **1,306** rule was never recorded.
  **Keep quoting 1,306** until a human settles it.
- **The graph cannot be rebuilt from here** — `.graphify_root` names a foreign checkout. Owner's call.
- **`AI` untouched**: 98 uncommitted files, 1 stash, 11 commits behind `origin/Dev`; the sole conflicting
  file is `Environments/QA_MsSQL.properties` (keys `ApiToken`, `password`).

**Lessons Learned / Observations.**
- **Adversarial verification paid for itself:** 12 of 192 findings died, 7 as double-counts. An unverified
  register would have sent the loop chasing the same defect three times.
- **The tool that reports on the workspace found the workspace reporting on itself twice** — `Objective.md`
  reached context via both a stale `@`-import and a live hook, disagreeing. Auto-loading is not idempotent.
- **A documented safety invariant is worth nothing unmeasured.** Two scripts violated "a bare run issues
  zero HTTP calls" while both governance files asserted it. Invariants now execute every session.
- **Ordering matters when a writer touches one file repeatedly** — edits must apply highest-offset-first,
  or every edit after the first is refused by its own hash check.
- **Partial correction can be worse than none:** fixing one number on a line and leaving two stale makes the
  line look verified.

**Dependencies.** Consumes OBJ-004's findings, OBJ-007's validation package (as the staleness signal for the
graph), OBJ-010's run evidence and OBJ-012's deck. Blocks nothing; the register is the input to `v0.2`.

---

### OBJ-014 — Developer repository (`pam/`) size investigation

**Objective ID.** `OBJ-014`

**Title.** Investigate and document why the developer repository (`pam/`) is ~28 GB, packaged as a
raisable issue set.

**Status.** ✅ Completed

**Summary.** The owner observed that `pam/` occupies ~28 GB and asked for a documented investigation with
a summary, a detailed table and evidence per finding. The figure was confirmed and corrected: the folder
is **35.57 GB**, and the 28 GB observed is almost exactly `.git` (27.88 GB). The cause is not source
code — it is third-party binary archives committed and re-committed dozens of times. **`ARCONDbeaver.zip`
alone is 11.45 GiB across 50 versions: 41.1% of the entire repository.** All C# source across 30,888
versions is 0.204 GiB — 0.8%.

**Key Deliverables.**
- `Developer Repository Issues/README.md` — summary, on-disk attribution tables, 16 findings, per-finding
  evidence, remediation with risk, stated limits, reproduction commands
- `Developer Repository Issues/findings.csv` — 19 machine-readable rows, each with `basis` and
  `evidence_command`
- `Developer Repository Issues/evidence/` — 7 raw captures (`E1`–`E8`)
- Three regeneration scripts: `regenerate-pack-attribution.py`, `regenerate-head-analysis.py`,
  `regenerate-history-analysis.py`

**Related Files.** Subject: `pam/` at `12234f037`. Comparator: `Automation gitlab repo/pam_automation_bootstrap`
(131 MB). Registered in `objective_original_origin.md` §0.

**Reason for Archiving.** Delivered in full: the number is confirmed, attributed to on-disk packfile bytes,
and every finding carries a reproducible command.

**Pending Work.** ⛔ **Nothing was remediated and nothing should be without the product team.** `pam/` is
not our repository. The blobless-clone recommendation (§5.2) is available to any developer immediately;
the `.gitignore` fix (§5.3) needs the repo owner; the history rewrite (§5.4) needs an org-wide freeze.
Per-branch unique content was not measured — 3,326 refs makes it expensive.

**Lessons Learned / Observations.**
- ⛔ **`git ls-tree -l` separates the path with a TAB, and this repo's paths contain spaces.** An early
  pass split on whitespace, truncating `ARCON PAM.msi` to `ARCON` — which fabricated a phantom "251 copies
  of ARCON" finding and skewed the whole extension table. Caught by trying to verify a claim not measured
  directly. **Parse git plumbing on its declared separator, never on whitespace.**
- **`git verify-pack -v` is the only honest basis for "what is big".** Logical (`cat-file`) sizes said
  `.cs` was 12.38 GiB of history; on disk it is 0.204 GiB, because text deltas ~60×. Ranking by logical
  size would have pointed remediation at exactly the wrong files.
- **The delta-base column is the proof, not the theory.** 44 of 47 `ARCONDbeaver.zip` versions are stored
  whole with no delta base — which is simultaneously why the repo is huge and why `gc` cannot help.
- **A partial workflow is still useful if you refuse to trust it.** Six investigation agents produced 77
  findings but all verifiers died on a session limit, leaving them unverified. They were used only as a
  checklist against independently-measured work; the handful that were material (pack-2 attribution, the
  delta-base test, absent LFS, the 1-byte `chromedriver.exe`) were each re-measured before publication.
- **The observed number can be right and still mislead.** "28 GB" was accurate for `.git` but the folder
  is 35.57 GB, and the instinctive fix — deleting large files — reclaims nothing.

**Dependencies.** Consumes the `pam/` pull performed under `OBJ-013`. Blocks nothing.

---

### OBJ-015 — Management Execution & Benchmark Dashboard (React)

**Objective ID.** `OBJ-015`

**Title.** A lightweight React dashboard making the completed API execution, benchmark, findings and
automation work visible graphically instead of as raw files and logs.

**Status.** ✅ Completed

**Summary.** Management had no way to see this programme's results without reading run folders, workbooks
and markdown. Built a React + Vite app in `workbench/react/` — previously a declared-but-empty placeholder
— with six views: dashboard, previous-vs-current benchmark, execution history with per-run drill-down,
project rollup, findings by severity, and a per-execution management report. Every figure is generated from
measured artifacts by a script that cross-checks itself against the run workbook's own authored summary;
nothing is estimated, and anything unmeasured renders as `N/A` with the gap named.

**Key Deliverables.**
- `workbench/react/` — the app. 4 runtime dependencies, no backend, light theme, hash-routed so `dist/`
  opens from the filesystem. `npm install` → `npm run dev`
- `workbench/scripts/obj015_build_dashboard_data.py` — the data layer generator. Read-only on the
  workspace, zero HTTP calls, writes only `src/data/`. `--verify` mode writes nothing
- 14 datasets under `src/data/`, incl. `manifest.json` (provenance per source file) and `gaps.json`
  (8 named gaps, surfaced in the UI)
- `workbench/react/README.md` — commands, architecture, the colour-validation constraints, the two
  measurement traps

**Related Files.** Sources: `Reports/Runs/2026-08-05_114315/QA_MsSQL_API_Execution.xlsx` (9 sheets) ·
`validation.json` · both runs' `results.json` · `Reports/Summary/OBJ-010-Execution-Benchmark.md` ·
`Developer-Loopholes/FINDINGS-SUMMARY-AND-PRIORITY.md` §3 · `Developer Repository Issues/findings.csv` ·
`document/data/management-findings.json` · `observations.json` · `workbench/scripts/.obj010/segments.json` ·
`workbench/onboarding/profiles/pam.json` · `APIConfig.java`. Root `README.md` and `CLAUDE.md` folder tables
updated.

**Reason for Archiving.** Delivered in full and verified in a browser: all six views render, the ten
self-checks pass, and the production bundle builds.

**Pending Work.** The success-rate line on the history page is honest but thin — with two full executions
retained it is a comparison, not a trend, and it earns its name only as more executions land. Per-module and
performance breakdowns exist for run N only, because `obj010_build_workbook.py` never ran against N-1;
running it there would backfill them. Could not force the browser window below 1920 px, so the sub-900 px
nav layout was verified by constraining the container (clean to 760 px) rather than visually.

**Lessons Learned / Observations.**
- ⛔ **`results.json` has no hop verdict field.** A test case's verdict is the AND of its check layers, and
  a hop with **no** checks was withheld — never a pass, never a fail. Getting this wrong would have shifted
  every headline number. The derivation reproduces the published 3,459/1,957/14 and 1,200/668/5 exactly.
- ⛔ **A resumed run's own metadata undercounts it.** `meta.elapsed_s` covers the *last* process only, so
  run N reads 94.9 min against a true 329.1 — a **234-minute** understatement. `segments.json` exists for
  this; every duration in the dashboard carries a `durationBasis` naming its source.
- ⛔ **Endpoints reached ÷ endpoints declared is not coverage, and the raw ratio reads 106%.** Newly
  measured: of the **1,388** endpoints run N reached, only **1,140** are declared in `APIConfig.java` —
  **248** exist only in the QA team's Excel corpus. True catalogue coverage is **1,140/1,306 = 87.3%**.
  This is the multi-basis trap the root `CLAUDE.md` warns about, caught only by looking at the rendered page.
- **The workbook, not `results.json`, is the source of truth for the scenario dimensions.** A plausible
  re-derivation from the expected-status code missed the published split by up to 54 cases. The authored
  `Hop Results.Scenario` column is authoritative; re-deriving a figure that already exists invents a
  second answer.
- **Colour was computed, not chosen, and two intuitive schemes failed.** green-vs-red for pass/fail fails
  colourblind separation (ΔE 4.1, deuteranopia), and red/amber/yellow as three adjacent severity fills
  fails twice over. Hence: **passed is blue**, and severity is a single-series bar with the tier on the axis.
- **Rendering it is part of building it.** The 106% coverage figure, literal `**` markers surviving a
  multi-line bold span, and a `−0%` delta were all invisible in the data and obvious on screen.

**Dependencies.** Consumes `OBJ-010` (both runs, the workbook, the benchmark), `OBJ-004`/`OBJ-014` (finding
sets), `OBJ-007` (management findings, observations), `OBJ-011` (the project profile). Blocks nothing.

---

### OBJ-016 — Daily pull-and-refresh job, and runtime data for the dashboard

**Objective ID.** `OBJ-016`

**Title.** Pull both repositories daily, refresh everything derived from them, and have the React
dashboard serve live data instead of a build-time snapshot.

**Status.** ✅ Completed

**Summary.** The owner believed daily polling and real-time dashboard updates were already configured.
They were not: no scheduled task existed, both repos had last been fetched under `OBJ-013` two days
earlier, and the app had no `fetch` of any kind — every dataset was bundled into the JS at build time.
This objective built what had been assumed. A guarded daily job now pulls, re-derives and reports; the
dashboard fetches its datasets at runtime and shows on screen when they were last refreshed and whether
the attempt succeeded.

**Key Deliverables.**
- `workbench/scripts/obj016_daily_refresh.py` — six steps, deny-by-default (`--execute` required),
  per-step status, `--skip-git` for a derive-only run. State in `workbench/.daily/last-run.json`,
  append-only `daily.log`
- `workbench/scripts/obj016_register_task.ps1` — registers/removes the `PAM-Dashboard-Daily-Refresh`
  scheduled task; user-level, no admin, no stored password, `StartWhenAvailable`
- Runtime data: datasets moved to `workbench/react/public/data/`; `dataService.js` rewritten as an
  async bootstrap with synchronous selectors; `src/components/Freshness.jsx` for the sidebar stamp and
  the stale/failed banner; an *Automatic refresh* panel showing the job's per-step result
- `refresh.json`, written by the job, is what makes a failed refresh visible instead of silent

**Related Files.** `pam/` (fast-forwarded `12234f037` → `a6a7620b1`) ·
`Automation gitlab repo/pam_automation_bootstrap` (fetched only; `AI` 0 ahead / 15 behind `origin/Dev`) ·
calls `obj013_loop.py`, `obj013_rag_ingest.py`, `obj015_build_dashboard_data.py`. Root `CLAUDE.md`
(§Drift control gained a daily-refresh subsection), root `README.md` and `workbench/react/README.md` §2,
§4, §10 updated.

**Reason for Archiving.** Delivered and verified through the scheduler, not just by hand: the task ran
to `LastTaskResult 0` with all six steps `ok`, and a live re-fetch in the browser moved the refresh
stamp from 16:55:42 to 16:57:33 with no rebuild and no page reload.

**Pending Work.** Execution stays manual by explicit decision, so the headline KPIs still only move when
someone runs the suite — a weekly execution was offered and not taken. The task only fires while this
user is logged on (`LogonType Interactive`, chosen to avoid storing a password); a machine left off for
days catches up on one run rather than back-filling each day. `AI` is now 15 behind `origin/Dev` and
still unmerged — the job reports that number and will not act on it.

**Lessons Learned / Observations.**
- ⛔ **A job that works interactively can fail under the scheduler for encoding reasons alone.** The
  first scheduled run exited 1: Task Scheduler gives a child Python **no console**, so it picks the ANSI
  codepage and dies with `UnicodeEncodeError: 'charmap' codec can't encode character '⛔'` — the ⛔
  this workspace prints everywhere. `child_env()` now forces `PYTHONUTF8=1` / `PYTHONIOENCODING=utf-8`.
  **Never certify a scheduled job by running it by hand.**
- ⛔ **PowerShell 5.1 reads a BOM-less UTF-8 script as ANSI, and that is a parse error, not mojibake.**
  An em-dash decodes to three cp1252 characters ending in `U+201D`, which PowerShell accepts as a string
  delimiter — opening an unterminated string and failing the whole file. `obj016_register_task.ps1` is
  deliberately 7-bit ASCII. This is the same trap `markdown-docs.md` records for `Set-Content`, biting on
  script *reading* instead of writing.
- **Reporting a step as "ok" when its output could not be parsed is a lie the job tells itself.** The
  drift step originally did exactly that; it now fails, because a job that did not learn the drift state
  has not done its work.
- **`cache: 'no-store'` is the whole mechanism.** Without it the browser serves a cached `runs.json`
  after a regenerate — indistinguishable from "nothing changed".
- **"Real-time" was assumed, not built.** Worth noting as a pattern: the gap between what a system is
  believed to do and what it does is only closed by checking. `performance.getEntriesByType('resource')`
  settled it in one call, and the app chunk dropping 214 KB → 70 KB confirmed the data really left the
  bundle.
- **One copy of the data, enforced.** `src/data/` was deleted rather than left beside `public/data/`; two
  copies of a generated dataset is the same failure mode as the duplicated objective import under
  `OBJ-013`.

**Dependencies.** Consumes `OBJ-015` (the dashboard and its generator) and `OBJ-013` (the drift loop and
RAG index it calls). Blocks nothing.

---

### OBJ-017 — Weekly API execution, and run-time resolution of N / N-1

**Objective ID.** `OBJ-017`

**Title.** Execute the full API suite every Sunday at 10:00 so the benchmark rolls forward on its own,
and make the dashboard promote a new run automatically.

**Status.** ✅ Completed

**Summary.** `OBJ-016` automated everything *derived*; the headline KPIs still moved only on a manual
execution. This adds that execution weekly, and — critically — fixes what would have made it pointless:
the dashboard generator had `RUN_N` and `RUN_N1` **hardcoded**, so a new run would have landed on disk
while the dashboard went on reporting August's as current. N and N-1 are now resolved from disk each
build. Authored analysis, by contrast, is now explicitly pinned to the run it was measured in and
withheld when N moves.

**Key Deliverables.**
- `workbench/scripts/obj017_weekly_execution.py` — nine steps, deny-by-default (a bare run issues
  **no HTTP at all**): token-latch check → unauthenticated env probe → generate → execute → one
  resume → validation gate → workbook against the resolved baseline → dashboard → execution stamp.
  `--resume-only` finishes a partial run
- `workbench/scripts/obj017_register_weekly_task.ps1` — registers/removes `PAM-Weekly-API-Execution`,
  Sundays 10:00, 14 h limit, `StartWhenAvailable`, ASCII-only
- `obj015_build_dashboard_data.py`: `resolve_runs()`, `FINDINGS_BY_RUN` as a pinned id map,
  `AUTHORED_ANALYSIS_RUN` gating, derived N-1 latency and a computed performance-trend sentence
- Dashboard: a *Weekly execution* panel, plus empty states wherever authored narrative is withheld
- `public/data/execution.json` — the weekly outcome, read at runtime

**Related Files.** `workbench/.weekly/last-run.json` + `weekly.log` · calls `generate_flows.py`,
`generate_data_flows.py`, `chain_runner.py`, `obj010_collect.py`, `obj010_build_workbook.py`,
`obj015_build_dashboard_data.py`, `token_guard.py` (indirectly) · decisions **D21–D24** in
`03-decisions.md` · root `CLAUDE.md`, root `README.md`, `workbench/react/README.md`.

**Reason for Archiving.** Built, registered for 16 Aug 2026 10:00, and verified as far as it can be
without spending 5.5 hours of live QA time: the token-latch guard was proved to abort (against a
temp latch, so the real one was never created), the unauthenticated probe returned HTTP 200 from the
live host, the full nine-step dry run reports every step, the authored-analysis gating was proved to
withhold headlines and trend when N is an unanalysed run, and a temporary scheduled task confirmed
the script runs cleanly **under Task Scheduler** — the environment that broke `OBJ-016` on its first
attempt.

**Pending Work.** ⛔ **The actual weekly execution has never run.** A 5.5-hour live run was not
launched, because it was not asked for; the first real proof arrives Sunday 16 Aug. What that run must
be checked for: that `chain_runner` completes under the 6-hour budget, that the resume path behaves
if it aborts, and that the new run correctly becomes N with the previous as N-1. The task fires only
while this user is logged on. `AUTHORED_ANALYSIS_RUN` is a manual pointer — after a weekly run, someone
must author an analysis and update it, or the dashboard will keep saying "analysis pending".

**Lessons Learned / Observations.**
- ⛔ **The feature would have been inert without a fix nobody asked for.** `RUN_N`/`RUN_N1` were
  hardcoded string literals. Scheduling an execution while the dashboard pins its current run to a
  fixed stamp produces a system that runs every week and shows the same numbers for ever. **When
  automating a step, check what downstream consumes it.**
- ⛔ **`chain_runner` takes the token BEFORE its own `--wait-for-env` probe** (lines ~993 vs ~1019),
  and that probe needs the token. So its wait cannot protect the credential, and the agreed
  "probe first, then one attempt" policy required a separate unauthenticated pre-flight in the job.
  Reading the order of operations mattered more than reading the flag list.
- **The pre-flight probes `/` and not an API action** — no credential, nothing on the safety
  blocklist, and it still catches the failure mode that matters: a dead application pool answers 503
  for the whole site.
- **Last month's findings are not this week's findings.** The headline numbers are results of one
  execution. Gating them behind `AUTHORED_ANALYSIS_RUN` is the difference between a dashboard that
  reports and one that quietly fabricates.
- **A monkeypatched test beat a real one.** Proving the latch guard by creating the real
  `.token_attempt_block.json` would have risked leaving it behind and blocking every future run;
  pointing the path at a temp file proved the same thing with no blast radius. It also surfaced a
  genuine fragility — `Path.relative_to` raising inside the error-reporting path.

**Dependencies.** Consumes `OBJ-010` (the execution pipeline and its workbook builder), `OBJ-015`
(the dashboard generator it rewrites) and `OBJ-016` (the scheduling pattern and the runtime data
path). Blocks nothing.

---

### OBJ-018 — k6 performance capability for the login journey: browser, API, and correlated bottleneck analysis

**Objective ID.** `OBJ-018`

**Title.** Build an industry-standard k6 performance-testing capability for the PAM login journey as
one framework in three integrated phases — browser/UI, HTTP/API, and correlation.

**Status.** ✅ Completed *(built and verified; deliberately never executed against the product)*

**Summary.** Functional API coverage was ~90%; nothing in the workspace measured performance. This
adds it as one framework rather than three scripts: a real browser login journey, the same
authentication exercised at the HTTP layer, and an analysis step that joins the two on shared
identifiers and attributes the latency. The agreed scope was **build only, zero HTTP** — execution is
a separate, named owner decision, because concurrency against an authentication endpoint is an
account-lockout event rather than a test.

**Key Deliverables.**
- `pam_automation_bootstrap/performance/` — 14 files, git-tracked on `AI`. The repo's only non-Java
  asset, a documented exception: k6 runs ES modules on its own Go runtime, adds no npm dependency and
  nothing to the Maven build
- Phase 1 `browser/login/login-browser.js` · Phase 2 `api/login/login-api.js` ·
  Phase 3 `analysis/login/correlate.mjs` + `selftest.mjs`
- Shared core: `config/{run-context,environments,workload}.js`, `lib/{guard,metrics,summary}.js`,
  `thresholds/login-thresholds.js`
- `run-performance.ps1` — dry-run by default, mints one run id for both phases, 7-bit ASCII
- `.gitignore` updated **before** the tree existed, so no run output can ever be staged

**Related Files.** `performance/README.md` (the safety preconditions) · repo `CLAUDE.md` §`performance/`
· root `CLAUDE.md` §"Execute everything" · supersedes the layout proposed in
`workbench/skills/k6-performance.SKILL.md` (which is API-only and has no browser coverage).

**Reason for Archiving.** The three-phase foundation is complete and everything that can be verified
without k6 or a credential has been. Remaining work is gated on owner inputs, not on engineering.

**Pending Work.** ⛔ **Never executed.** Needed before a first live run: (1) dedicated
performance-test credentials as `PERF_USERNAME`/`PERF_PASSWORD`, confirmed free of any second factor —
PAM supports ten plus FIDO2/SAML/ADFS/Azure AD, and **any of them makes an HTTP-level login impossible**;
(2) `k6` installed (absent; `winget install --id GrafanaLabs.k6 --exact`, 2.2.0 confirmed available);
(3) the live values of `sso_arcos_config` `aps_id` 32/159/33/49/50/55 — **`aps_id 55` would invalidate
Phase 2 outright**, and `aps_id 33 = 0` means a lockout never auto-unlocks; (4) an environment decision —
`Objective.md` says QA_MsSQL only, but `Environments/Perf.properties` and `Performance.properties`
already exist and point at other hosts. Also unimplemented by design: per-VU accounts
(`data/login-users.sample.json` is shape only). Expect the first smoke run to need selector or
field-name corrections.

**Lessons Learned / Observations.**
- ⛔ **The obvious target would have been the wrong one.** `/arcontoken` on `:6302` and the UI login on
  `:1302` are independent mechanisms against separate identity stores (`sso_ApiUsers` vs `sso_users`);
  the web app consumes the former server-side with its own APP001 account and the browser never sees
  it. Correlating Phase 1 against `/arcontoken` would have compared a human login to a machine token
  grant and called the difference "browser overhead" — a fabricated result. Discovering the auth path
  instead of assuming it also removed the GenericScheduler lockout risk from this objective entirely.
- ⛔ **`fill()` silently produces an empty password on this login form.** The real password is captured
  only from `keydown` into a hidden field. Any driver setting `.value` directly posts nothing and every
  login fails with "Invalid Login Details" regardless of the credential. The Java suite is correct only
  by accident of style (`safe_type_text` uses `.type()`).
- ⛔ **A self-test that cannot fail is worse than none.** The first version passed all 14 assertions with
  **7 of 8 rules deliberately broken** — every fixture sat above the sample threshold, only one of four
  joinability rules was covered, and a grade assertion accepted a two-element set. Rebuilt to 36
  assertions and then mutation-tested: 12 of 12 mutations now caught. **Assertion count measures nothing;
  mutation survival measures everything.**
- ⛔ **A PowerShell safety gate went inert on exactly one failure.** An unwrapped pipeline returning a
  single `[pscustomobject]` has **no `.Count`** — the one type lacking the scalar auto-property — so
  `$blocked.Count -gt 0` evaluated `$null -gt 0` = `False`. The gate worked with two failures and not
  with one. Always `@()`-wrap a `Where-Object` result before counting it.
- **Grading must be structural, not editorial.** Hardcoded `Observed` grades let one report carry a
  small-sample warning and an "Observed" claim simultaneously, and let section 2 disagree with section 3
  about the same figure. Grades are now computed once and capped by the phase they came from.
- **Percentiles are not additive.** p95-of-part over p95-of-whole gave shares summing to 100.7% under a
  row labelled 100%. Shares are computed from the mean.
- **k6 tags are invisible to `handleSummary`.** A tagged counter only materialises as a sub-metric when
  a threshold names it, so every per-reason rejection tally reported "unclassified" — losing exactly the
  distinction that decides whether a run must be stopped. Named counters cross the runtime boundary;
  tags and module-level arrays do not.
- **The adversarial review earned its cost.** Six lenses found 33 defects across safety, k6 API fidelity,
  WebForms fidelity, correlation logic, wiring and documentation — including two that would have made
  Phase 1 fail on every iteration (no TLS suppression, domain selected by value instead of label) and
  one that meant a locked account would never be detected (matching a resource *key* rather than the
  rendered text). It also independently confirmed the WebForms postback contract as correct.

**Dependencies.** Consumes the discovery in `pam/PAM` (login mechanism, lockout policy, session cap) and
the existing `Environments/` config surface. Reuses `workbench/skills/k6-performance.SKILL.md` as prior
art. Blocks nothing; its own live run is blocked on the owner inputs listed under Pending Work.

---

### OBJ-019 — Login + Sanity performance scope, live execution on QA_MsSQL, and the Performance React dashboard

**Objective ID.** `OBJ-019`

**Title.** Expand performance testing from Login-only to Login + the full Sanity scope, execute it on
`QA_MsSQL`, and add a dedicated Performance React dashboard beside the API one.

**Status.** 🟡 In Progress — **live execution ACHIEVED.** Run `2026-08-18_142809` (sanity journey,
3 concurrent users, `QA_MsSQL`) authenticated 3/3 and produced the project's first valid performance
measurement; the dashboard is updated from it. The credential blocker recorded below was a **false
negative from the defective Phase 2 postback** — `arcosadmin` authenticates through the browser path.
Two items remain: the module sweep aborts after 4 of 13 modules (unhandled navigation timeout), and
Phase 2 API + Phase 3 correlation are still blocked. Full detail in `workbench/.perf/OBJ-019-STATE.md`.

**Summary.** `OBJ-018` built the three-phase k6 framework for login and never ran it. This extends the
scope to the 14 active module checks of `CICD_Suites/SanityChecks.xml` → `DevOpsSanityCheck` (browser +
API + per-module correlation), installs k6, verifies the framework loads against the live product, and
builds a second React dashboard (`workbench/react-performance/`) in the same Theme 1 language. The live
execution could not run: none of the four owner-supplied credential combinations authenticate on
QA_MsSQL, and the shared `auto_adminui` account locked during safe validation.

**Key Deliverables.**
- Sanity scope, generated not guessed: `performance/data/build-sanity-registry.mjs` →
  `sanity-modules.json` (14 modules, 211 checks, 6 excluded), from the real Excel-driven suite
- `performance/browser/sanity/sanity-browser.js` — login + per-module load timing across the sweep
- `performance/api/sanity/sanity-api.js` — the authenticated auth+landing backbone; per-module API
  timing honestly marked capture-required (no invented URLs)
- `performance/analysis/sanity/correlate-sanity.mjs` — per-module UI-vs-backend attribution, graded
- k6 **v2.2.0 installed**; the whole framework verified to load in k6 with the guard firing (zero HTTP)
- An **unauthenticated login-page probe** confirming the Phase 2 WebForms contract on the wire
- `workbench/react-performance/` — a 6-view React+Vite dashboard (Executive · Login · Sanity · API ·
  UI · API-vs-UI), builds (846 modules) and browser-verified on :5174, with `HOW-TO-RUN.md` for both apps
- `run-performance.ps1` hardened: creates the report dir k6 won't, resolves k6 off PATH, normalises the
  banned-account check

**Related Files.** `workbench/.perf/OBJ-019-STATE.md` (resumable state + the credential blocker in full)
· `performance/README.md`, `workbench/react-performance/README.md` + `HOW-TO-RUN.md` · repo `CLAUDE.md`
§`performance/` · git branch **`Dev`** (fast-forwarded to `origin/Dev`).

**Reason for Archiving.** Not archived — In Progress. Recorded here because a natural checkpoint was
reached: all build/verify work is done and the only remaining work is gated on an owner action
(credential/unlock).

**Pending Work.** ⛔ **Live execution never ran.** Unblocks on any one of: admin-unlock `auto_adminui`
plus its current password; a dedicated perf account; or a confirmed working QA_MsSQL password — supplied
as `PERF_USERNAME`/`PERF_PASSWORD`. Then: `run-performance.ps1 -Execute` for Login and Sanity (≤3 VUs),
point the dashboard generator's `INGEST_RUN` at the run folder, author the analysis. Also open: the
per-module Sanity API capture (one authenticated network trace) and the §16 final `QA_MsSQL` trial.

**Lessons Learned / Observations.**
- ⛔ **Safe-looking credential validation locked a shared account.** Validation used the real postback,
  one attempt per combination, each in a fresh session — the pattern discovery said keeps the
  per-session lockout counter at 1. The first two `auto_adminui` attempts returned *invalid* (proving it
  was unlocked); a later attempt returned *locked out*. So the live lockout threshold was low enough that
  the fresh-session protection did not hold. **The unknown `aps_id 32/159/33` values were not a
  theoretical caveat — they were the thing that bit.** Stopped at once; `GenericScheduler` never touched.
- **The obvious credentials were the wrong environment.** `arcosadmin` belongs to Perf/Performance, not
  QA_MsSQL (whose user is `auto_adminui`); it cleanly returned *invalid* on QA. Worth checking which
  env a given account is provisioned for before spending an attempt.
- ⛔ **k6 does not create output directories.** A run does all its work and then fails to write its
  summary with "path not found", losing everything. The orchestrator now `mkdir`s the report dir first.
- **`CLAUDE.md`'s `JAVA_HOME` rule is stale but still needed.** The documented JDK path
  (`jdk-21.0.11.10`) no longer exists; the machine now has `jdk-21.0.12.8` and the machine `JAVA_HOME` is
  correct — but a process still inherits a stale `jdk-26.0.1`, so Maven needs the per-session override,
  now to the `.12.8` path.
- **The framework held up against the live product.** k6 v2.2.0 parsed all 15 modules, `open()`
  resolved, the guard refused with zero HTTP, and the unauthenticated probe confirmed the exact rendered
  field names (`ctl00$MainContent$…`, `__EVENTVALIDATION` absent, `ARCOSAUTH` as option *text*) — turning
  the last unverified OBJ-018 assumptions into measured facts. Folded in a 62-field harvest.
- **Recharts + StrictMode needs `isAnimationActive={false}`.** Line charts drew only a stub at the first
  point until animation was disabled — the same fix the API dashboard already uses on every series.
- **Reuse is the review.** The API dashboard was "reviewed" by adopting its components verbatim into the
  new app; that is stronger evidence they are sound than any edit, and editing a shipped dashboard for
  polish would risk breaking it for nothing.

**Dependencies.** Consumes `OBJ-018` (the framework it extends), the `DevOpsSanityCheck` suite and its
Excel data (Sanity scope), and `OBJ-015`'s React app (component/theme reuse). Blocked on an owner
credential for its live half.

---

### OBJ-021 — Professional performance-engineering capability for the login and sanity journeys

**Objective ID.** `OBJ-021`

**Title.** Turn the login performance script into a professional performance-engineering capability:
full 211-check sanity scope, correct session lifecycle, evidence-graded load model, baseline-relative
gates, living documentation and a detect-and-propose daily sync.

**Status.** 🟡 In Progress — **no work started.** Recorded here because the active instruction slot was
needed for `OBJ-022` (dependency-vulnerability remediation), which the owner raised while this objective
was still queued. Nothing was built against it; it resumes exactly where it was stated.

**Summary.** Extends `OBJ-019`'s framework, dashboard and first real run from Login-plus-partial-sweep
to the whole measured scope: 211 checks across 14 modules of `CICD_Suites/SanityChecks.xml` →
`DevOpsSanityCheck`. Requires fixing the module-sweep abort first (an unhandled 30 s navigation timeout
on `Session Monitoring` ends the iteration, capping coverage at 4 of 13 modules), then correcting the
session lifecycle, publishing A/B/C scope classification, and driving PASS/WARN/FAIL from
baseline-relative regression gates rather than an invented SLO.

**Key Deliverables.** None produced — the objective was displaced before implementation began. As
stated, the six were: full 211-check coverage across 14 modules · a correct documented session lifecycle
(`Login → Authenticated Session → Test Activity → Logout/Termination → Cleanup`) with three measured
defects fixed · A/B/C scope classification on the dashboard as
`Total scope → Performance-relevant → Executed → Validations → Results` · baseline-relative regression
gates with build-to-build and execution-to-execution comparison · living documentation with one source of
truth per fact · a daily repo sync that detects and proposes but never auto-writes.

**Related Files.** `Automation gitlab repo/pam_automation_bootstrap/performance/` (the framework, still
untracked at `?? performance/`) · `performance/data/sanity-modules.json` (owns the scope counts) ·
`performance/browser/login/login-browser.js`, `performance/api/login/login-api.js` (two of the three
lifecycle defects) · `workbench/react-performance/` (the dashboard) ·
`workbench/.perf/OBJ-019-STATE.md` (resumable state) · runs `Reports/Runs/2026-08-18_115054` and
`Reports/Runs/2026-08-18_142809`.

**Reason for Archiving.** Not archived — In Progress, and not superseded. Displaced from the active
instruction slot by `OBJ-022` when the owner brought forward the developer's SCA findings on the
automation `pom.xml`. The two objectives are unrelated and do not conflict; this one resumes on request.

**Pending Work.** ⛔ **All of it.** In the order stated: fix the `Session Monitoring` navigation-timeout
abort that caps the sweep at 4 of 13 modules; fix the three measured session-lifecycle defects — the
missing `context.close()`/logout in `login-browser.js`, the absent cookie-jar reset in `login-api.js`,
and the logout mechanism itself (no usable logout exists in this build: `/Logout.aspx` navigation is
commented out in `ACMO_New.Master`, so either a real termination step is found via `btnLogout` or its
absence is recorded as a product finding); then scope classification, the regression gates, the
documentation reconciliation and the daily detect-and-propose sync. Phase 2 API remains an open defect
from `OBJ-019` — its untested candidate fix is a non-empty `enteredPassword` plus XOR with the
page-rendered key rather than forcing key `0`.

**Lessons Learned / Observations.**
- **The "211 = Sign-In" premise was a conflation, and measurement caught it.** Sign-In is **10** of the
  211 checks; the 211 spans 14 modules. Measured from `performance/data/sanity-modules.json`, which the
  objective then made the single source of truth for scope counts.
- **A displaced objective must still be recorded.** The `CLAUDE.md` lifecycle rule requires a register
  record before the instruction slot is reused, whether or not any work was done — otherwise the queued
  work becomes indistinguishable from work that was cancelled. `D14` already anticipated this case.
- **Negative-credential load was excluded on evidence, not caution.** Every invalid-credential iteration
  increments the PAM lockout counter, which is exactly how `auto_adminui` was locked under `OBJ-019`.
  Excluding them keeps those scenarios functional-only (Category C) with the reason published.

**Dependencies.** Builds directly on `OBJ-019` (framework, dashboard, first valid run) and `OBJ-018`
(the three-phase k6 capability). Runs alongside `OBJ-020`. Consumes the `DevOpsSanityCheck` suite and its
Excel data for scope. Now sequenced after `OBJ-022`, which touches the same repository (`pom.xml`) but
no performance file.

---

### OBJ-022 — Dependency-vulnerability remediation in the active automation pom.xml

**Objective ID.** `OBJ-022`

**Title.** Remediate the developer's SCA findings in the active automation `pom.xml`
(`pam_automation_bootstrap`), not the legacy `pam/AutomationTesting/` copy the scan named, and confirm
the submodule architecture that makes the bootstrap repo the single source of truth.

**Status.** 🟡 In Progress — remediation complete and committed on `Dev` as `4d2d567`; **25 advisories
reduced to 1**, the survivor having no upstream fix at any version. Everything remaining is an owner
action outside this workspace.

**Summary.** The developer's scan named a `pom.xml` that is part of no build — a stale hand-copy only the
scanner sees. The two poms being functionally identical, every finding applied to the active one. A
measured baseline (`mvn dependency:tree` queried against OSV.dev) found 25 advisories across 12 of 85
resolved artifacts — 3 CRITICAL, 10 HIGH, 12 MODERATE — against the 6 the developer reported, two of
which were not Maven CVEs at all and six real ones missed, including all three CRITICALs.

**Key Deliverables.**
- `pom.xml` remediated on `Dev` (`4d2d567`), no `.java` change
- `log4j:log4j:1.2.14` excluded from the `jxl` path — verified safe: `jxl/common/Logger` falls back to
  its bundled `SimpleLogger`, and 0 of 1,084 sources import `org.apache.log4j`
- `poi` 5.5.1 with `commons-io` 2.21.0 raised in the same change (nearest-definition would otherwise
  have produced a runtime `NoSuchMethodError`, not a compile error); `jackson` 2.22.2, never 2.22.0
- `org.json`, `influxdb-client-java`, `pdfbox` removed after verified zero usage
- `jdom 1.1.3` documented as unfixable rather than silently dropped
- Playwright's finding stated as what it is — the embedded Node `v20.14.0` in the driver-bundle, not a
  Maven CVE

**Related Files.** `Automation gitlab repo/pam_automation_bootstrap/pom.xml` · that repo's `AGENTS.md`
and `README.md` (submodule architecture correction) · the remediation report distinguishing
fixed · not-reachable · unfixable.

**Reason for Archiving.** Not archived — In Progress. Displaced from the active slot by `OBJ-023`, a
different activity touching no common file. Recorded here because remediation reached a natural
checkpoint and everything left is an owner action.

**Pending Work.** Owner actions only: push `Dev`; bump the submodule gitlink (pinned at `365050d5`,
11 commits behind); delete the legacy `AutomationTesting/`; resolve the **unverified CI scan target** —
after deletion the scanner either sees no `pom.xml` and reports a false all-clear, or reads the stale
gitlink and keeps reporting old versions; and a suite run still gated on a working credential.

**Lessons Learned / Observations.**
- ⛔ **The same fix was already applied once and silently reverted.** `pam` commit `0520b6b79`
  remediated all six dependencies in the legacy copy; `e278fd399` bulk-copied the bootstrap tree over it
  and reverted every one line for line. Fixing the delivery copy instead of the source of truth is the
  root cause, and it is why the submodule architecture had to be confirmed as part of this objective.
- ⚠️ **An import-only search does not prove a dependency is unused.** Two of five planned zero-usage
  removals were wrong: `AcmoHelperPage.java:2343` uses `org.apache.poi.hwpf` **fully qualified inline**,
  so removing `poi-scratchpad` broke the build; and `Environments/demo.properties` targets MySQL, so
  `mysql-connector-j` was upgraded 9.0.0 → 9.7.0 rather than dropped.
- A scan finding is a claim about a *file*, not about a *build*. Establish which artifact actually ships
  before acting on the path a report names.

**Dependencies.** Shares the `pam_automation_bootstrap` repository with `OBJ-021` but no file. Its
verification is constrained by the same credential blocker recorded under `OBJ-019`.

---

### OBJ-023 — Failure-reproducibility re-run: confirmed application failures vs transient ones

**Objective ID.** `OBJ-023`

**Title.** Establish which of the 1,960 failing test cases in `Reports/Runs/2026-08-16_100005/` are real,
reproducible application failures and which were transient or environment-related, by executing the full
suite a second time against the identical flow set and comparing hop-by-hop.

**Status.** ✅ Completed — closed by owner instruction (`D29`); see **Closure** at the end of this record. Mechanics built, dry-run verified and comparison tool self-tested; execution
**paused by the owner at 178 of 747 flows** with 569 remaining. Displaced from the active slot by
`OBJ-024`. The two touch no common file.

**Summary.** Run N recorded 63.6% of test cases passing (3,422 of 5,382 executed across 747/747 flows),
leaving 1,960 failures attributed to no cause — so the pass rate could not be read as a statement about
the product. The agreed method was a second full execution of the same corpus, then a verdict-transition
analysis keyed on `(flow, hop, name)` splitting every case into PASS→PASS, FAIL→FAIL (confirmed
reproducible), FAIL→PASS (non-reproducible) and PASS→FAIL (newly failing — the class a failed-only re-run
would be blind to). Scope was resolved with the owner before execution: all 747 flows rather than the
failing subset, because a failed-only re-run costs 4,449 of 5,396 hops anyway and a chain must be replayed
whole for a failing hop to carry its context; once; and ⛔ no flow regeneration, since a regenerated corpus
invalidates the comparison.

**Key Deliverables.**
- `workbench/scripts/obj023_reproducibility.py` — the verdict-transition comparator, built and self-tested
  against run N versus itself: 5,396 hops, 100% reproducible, zero spurious drift
- Re-run `Reports/Runs/2026-08-19_133400/` — 178 flows checkpointed (24 passed, 154 failed), 945 evidence
  files retained, `checkpoint.json` at 1,365,439 B carrying the resume state
- `workbench/.weekly/OBJ-023-RESUME.md` — the resume brief, and the only record of how to continue
- A **prediction recorded before execution so it could be judged**: of the failing hops in N, 778 are 404
  (`LH-05`, endpoint absent), 1,008 are HTTP 200 whose envelope or message-semantics checks failed
  (`LH-01/02/03` contract findings), 100 are 400, and only ~67 carry a transient signature — expectation
  ~95% reproduce. Materially fewer would put the contract findings themselves in question.

**Related Files.** `workbench/scripts/obj023_reproducibility.py` · `workbench/.weekly/OBJ-023-RESUME.md` ·
`workbench/.weekly/obj020-supervisor.json` (the supervisor state names this objective) ·
`Reports/Runs/2026-08-19_133400/checkpoint.json` · baseline `Reports/Runs/2026-08-16_100005/` ·
`workbench/scripts/obj020_execution_supervisor.py` · `workbench/scripts/token_guard.py`.

**Reason for Archiving.** Not archived — In Progress. Displaced from the active slot by `OBJ-024`
(consolidation of the workspace into the `dynamic-api-validator` GitLab repository), which touches no file
this objective depends on. Recorded here because execution reached a deliberate owner-initiated pause and
the resume state needed capturing before the objective slot was reused.

**Pending Work.** 569 of 747 flows remain. Resume via `chain_runner --resume` with the **bare run id**
`2026-08-19_133400`, per `workbench/.weekly/OBJ-023-RESUME.md`. ⛔ **The resume can no longer use the
pinned token**: its 24-hour lifetime has elapsed, so continuing now requires a fresh `/arcontoken` call on
the shared `GenericScheduler` account — a one-attempt-then-latch path on an account that has locked twice
recently. That is an owner decision, not a mechanical step. After the run completes, the comparator
produces the transition analysis and both the raw and the confirmed-reproducible failure rates go to the
dashboard, distinguished from one another.

**Lessons Learned / Observations.**
- ⛔ **A deliberate pause must not be observable as a failure.** The supervisor was killed *before* the run
  so it could not interpret the stop as a transient fault and relaunch under the `OBJ-020` retry policy.
  A retry policy and an owner-initiated stop are in direct conflict unless the supervisor dies first.
- ⚠️ **A pinned token converts an availability problem into a deadline.** Pinning `$PAM_API_TOKEN` is what
  makes unattended retries safe, but it also means a paused run inherits the token's remaining lifetime as
  a hard resume window. The pause outlasted the window.
- The account lock that first blocked this objective did **not** originate from a retry loop here: only two
  `/arcontoken` calls were issued from this workspace in the surrounding 48 hours, every retry between them
  reusing the pinned value. The lock was external, and the password was never rotated — the credential the
  owner supplied is the one already committed in `Environments/QA_MsSQL.properties`.
- A partial run is neither a success nor a failure and must be represented as its own state. Declining to
  *promote* it to N is correct; declining to *show* it would not be.

**Dependencies.** Baseline `Reports/Runs/2026-08-16_100005/` from `OBJ-020` — the comparison is only valid
against it. Shares `token_guard.py` and the supervisor with `OBJ-017` and `OBJ-020`. Blocked on the same
shared-credential constraint recorded under `OBJ-019` and `OBJ-022`.

---

**Closure (owner instruction, `D29`).** ⛔ **This objective is closed without executing the remaining
569 flows.** The owner's instruction under `OBJ-025` is explicit: the paused activity is on hold, the standing
`PAM-Weekly-API-Execution` trigger runs every Sunday at 10:00 and will cover the next full execution
automatically, and it is **not** to be resumed manually.

What this changes, stated plainly so a later reader is not misled:

- **The reproducibility question is not answered by this objective.** It is deferred to a comparison of the
  next scheduled run against baseline `Reports/Runs/2026-08-16_100005/`. `obj023_reproducibility.py` is built
  and self-tested (run N vs itself → 100% reproducible, 5,396 hops, zero spurious drift), so the tooling is
  ready; only the second data set is outstanding.
- **The 178 completed flows are retained, not promoted.** `Reports/Runs/2026-08-19_133400/` and its
  `checkpoint.json` stay on disk under the never-delete-a-run rule. The run is **not** comparable to N and must
  never be presented as a benchmark — 178 of 747 flows is not a suite result.
- **Closing it removes a real hazard rather than papering over one.** Resuming required a fresh `/arcontoken`
  call on `GenericScheduler` — a shared functional account that also serves the data-warehouse ETL and has
  locked twice recently — outside the three mitigations `D24` grants the weekly job. Letting the guarded
  scheduled path produce the second data set is the safer route to the same answer.

### OBJ-024 — Consolidate the workspace into the `dynamic-api-validator` GitLab repository

**Objective ID.** `OBJ-024`

**Title.** Put the workspace's previously unversioned work under version control in a new GitLab
repository, without duplicating the two repositories that already have their own remotes.

**Status.** ✅ Completed — `main` at `63bbff7` and annotated tag `v0.2` pushed to ✅ **Fully complete** — the push and tag this record listed as outstanding have landed: `main` is 0 ahead / 0 behind `origin/main` at `3e295f2`, and the annotated `v0.2` tag is on the remote (`9833206` → `63bbff7`).
`repo.arconnet.com/Omkar.Kumbhar/dynamic-api-validator.git`, verified by clone.

**Summary.** Before this objective, everything outside the two nested git checkouts had no version
history at all: 25,964 files / 1,086 MB, in nine folders, with a documented precedent of permanent
content loss (`required-context/02-Data-Access-Requests.md`). The owner's original plan was a folder
restructure into `automation-repository/` · `developer-repository/` · `dynamic-api-validator/`. A read-only
inventory measured that restructure as a 227-site code migration rather than a rename, so the approach
chosen instead was `git init` at the existing root with the two repositories gitignored — same outcome,
zero file movement.

**Key Deliverables.**
- Repository initialised at the workspace root, `main` branch, 14,722 files tracked
- `.gitignore` excluding `/pam/` and `/Automation gitlab repo/`, plus the live token cache, `.token`,
  every `.env` (with `.env.sample` negated), and 107.57 MB of regenerable build output
- `.gitattributes` routing 4 objects to Git-LFS: three source PDFs and the 201.53 MB pam-scope
  `graph.json`, the only file over GitLab's default 100 MB per-blob limit
- Verified safety snapshot taken **before** any write: 25,964 archive entries against 25,964 source
  files, zero paths from either excluded repository
- Tag `v0.2` on `63bbff7`; clone verification confirming 14,722 files, both excluded repos absent, and
  all 4 LFS objects resolving to real content

**Related Files.** `.gitignore` · `.gitattributes` · `BLAST/Objective.md` · this register ·
the snapshot `dev-project-unversioned-2026-08-20.tar.gz` held outside the workspace.

**Reason for Archiving.** Completed. Push, tag and post-push clone verification all succeeded, and both
excluded repositories were confirmed intact and clean afterwards.

**Pending Work.** Four owner items, none blocking: revoke the GitLab token, which was pasted into a chat
transcript three times; decide whether to re-author the initial commit `736392e`, which carries a
different author than the standing rule and would need a force-push over published history; confirm
`omkar.kumbhar@arconnet.com` is the address GitLab attributes to, since it was inferred; and decide the
handling of `Automation gitlab repo/graphify-out.local-backup-OBJ007/` (150 MB, 1,092 files), which
belongs to no repository and stays unversioned, though it is inside the snapshot.

**Lessons Learned / Observations.**
- ⛔ **A folder rename here is a code migration.** `"Automation gitlab repo"` is a load-bearing sentinel,
  not just a path: six harness scripts locate the workspace root by testing that directory's existence
  and `SystemExit` when it is absent. 227 references, 8 `parents[2]` root resolutions, 3 `.claude/rules`
  globs and two absolute-path scheduled tasks all depended on the current layout.
- ⚠️ **Three of four watchdogs fail silently on a bad move.** `obj016_daily_refresh` marks a missing repo
  "skipped" rather than "failed", exits 0 and writes `"ok": true`; and both `.claude/settings.json` hooks
  end in `|| true`, so the `BLAST/Objective.md` injection would stop arriving with no error at all. The
  in-place approach was validated empirically instead: the daily task ran on its normal schedule *after*
  `git init` and resolved every path, fast-forwarding `pam/` under its `--ff-only` guard.
- **Compression, not raw size, decides what belongs in git.** 830 MB of payload became a 22.88 MiB pack
  because 717 MB of it is pretty-printed JSON compressing to 3-6%. The real weight was three
  incompressible PDFs. Sizing a repository by raw bytes would have driven the wrong exclusions.
- ⚠️ **Clone requires a short target path on Windows.** The longest tracked path is 171 characters, so a
  clone into a deep directory exceeds the 260-character limit and the checkout fails *after* a successful
  object fetch — an error that reads like corruption but is not. Clone near a drive root, or set
  `core.longpaths=true`.
- ⛔ **Two credentials were burned in the course of this work**, both by being pasted or printed into a
  transcript rather than by any repository operation: the GitLab token, and a fragment of an AWS secret
  key exposed by an over-greedy masking pattern in a diagnostic command. Redact by structure, never by
  regex, when the value's position is not known in advance.
- The owner elected to commit the captured credential material rather than redact it, so it is permanent
  in history from `736392e` onward. Recorded as a decision, not an oversight.

**Dependencies.** None on other objectives. Displaced `OBJ-023` from the active slot without touching any
file it depends on; `OBJ-023`'s paused run and its `checkpoint.json` were preserved and are inside the
snapshot.

---

### OBJ-025 — Workspace restructure to a compact, industry-standard architecture (`v0.3`)

**Objective ID.** `OBJ-025`

**Title.** Review the entire implementation end-to-end and redesign the workspace into a robust, compact,
simple, industry-standard structure — with explicit owner permission to change, merge, rename and realign
folders — while maintaining every piece of existing functionality and important data.

**Status.** ✅ **Completed** — `v0.3` structure delivered and verified; one owner action outstanding (the `settings.json` hook path). Was: 🟡 In Progress — resumed. Analysis and target-architecture design were under way when this was displaced in the active-instruction slot by `OBJ-026` before sign-off was reached; **no file had been moved**, so the workspace was exactly as `v0.2` left it and there was nothing to unwind. The owner has now reissued the restructure as the active instruction with the same mandate, so work continues from the design preserved in this record. The sign-off gate below is still the next milestone — it has not been passed.

**Summary.** `v0.2` achieved its goal: the previously unversioned workspace is under version control, pushed
and tagged. The owner's next requirement is structural rather than functional. The current layout grew one
objective at a time and now has 15 top-level entries, several of which are single-purpose or near-empty, three
of which contain **spaces in the directory name**, and one of which (`Reports/`) holds 14,035 of the 14,722
tracked files. The brief is to make the structure minimal, obvious and conventional without losing anything.
Explicitly *not* a functional change: every script, dashboard, scheduled job and deliverable must still work.

**Key Deliverables.**
1. An end-to-end review of all 15 top-level entries — what is authored versus generated, what is duplicated,
   what is stale.
2. A **measured** path-dependency map: every workspace-root resolver, every hardcoded path in executable code,
   and every external binding (scheduled tasks, Git-LFS patterns, `.gitignore` literals, the drift-loop write
   allowlist, `facts.json` document sites, `.claude/rules` globs, React dataset paths).
3. Three independent candidate architectures, scored by three separate judging lenses (breakage risk, the
   owner's stated request, one-year maintainability).
4. A single recommended target structure with a complete current-path to new-path mapping leaving nothing
   unmapped, plus the exact `git mv` sequence and every path fix required.
5. Owner sign-off before any file moves; then execution, verification and a `v0.3` tag.

**Related Files.** Root `CLAUDE.md` · root `README.md` · `.gitignore` · `.gitattributes` ·
`.claude/rules/{automation-repo,api-surface,markdown-docs}.md` · `workbench/scripts/obj013_scan.py`
(`WRITE_ALLOWLIST`) · `workbench/.drift/facts.json` · `workbench/scripts/obj016_daily_refresh.py` ·
`workbench/scripts/obj017_weekly_execution.py` · `workbench/react/` and `workbench/react-performance/`
(`public/data/`) · every top-level folder named in the mapping table.

**Reason for Archiving.** Not archived — In Progress, paused. Recorded on opening so that the pre-restructure state is
captured before anything moves, which is the only way a mapping table can later be audited. The owner then issued a
new requirement (`OBJ-026`, the `engage` workspace-readiness entry point), which takes the active-instruction slot
under `D14`. Because the restructure had reached design and **not** execution, nothing is half-moved: the pause costs
the design work only, and that design is preserved in this record and in the deliverable list above.

**Pending Work.** ⛔ **Owner:** one line in `.claude/settings.json` — the `SessionStart` hook must name `tools\obj013_loop.py` instead of `workbench\scripts\obj013_loop.py`. It fails *silently* (a `Test-Path` guard), so the drift headline simply stops appearing. Nothing else is blocked. **Deferred by design, as separate objectives:** (a) renaming the 24 `obj0NN_` scripts by role — worth doing, but it touches the same import sites and `CLAUDE.md` quotes as the move, and moving and renaming must never share a commit; (b) hoisting the 8 byte-identical React components into a shared package — **blocked** until the `pct()` contract is reconciled, because `Indicators.jsx` is byte-identical in both apps while `format.js` multiplies by 100 in one and not the other, so naive deduplication breaks one dashboard silently in the safe-looking direction; (c) moving the ~319 path-specific lines out of the auto-loaded `CLAUDE.md` into `.claude/rules/` — a *content* objective that must not share a commit with a path restructure, since moving a section can orphan a `facts.json` anchor. Also still open and unrelated: the `2026-08-16` weekly-execution exit-1 diagnosis (`D32` set *when* it runs, not whether it works). ~~Superseded:~~ the original list read: Everything after the design: owner sign-off on the target structure, the `git mv` execution,
the path-fix checklist, re-registration of both Windows scheduled tasks if their script paths move,
verification (drift loop, daily-refresh dry run, both dashboard builds, a clone test), documentation rewrite
across `CLAUDE.md` / `README.md` / the three rule files, and the `v0.3` tag.

**Lessons Learned / Observations.**
- The `OBJ-024` decision to `git init` **in place** rather than restructure first is what makes this objective
  safe: every move can now be a `git mv` with history, and a bad restructure is revertible. Doing it in the
  other order would have meant restructuring with no history to fall back on.
- Three directory names contain spaces — `Company Documents/`, `Developer Repository Issues/`,
  `Automation gitlab repo/`. The last is inside a gitignored nested repo and cannot be renamed here.
- The governance layer is dense on purpose. A previous attempt to trust a stale instruction (`JAVA_HOME`
  pointing at a non-existent JDK) produced exactly the failure the instruction existed to prevent, so
  "simplify" must not become "delete the safety rules".
- `Reports/` being 95% of the file count is the single largest structural fact about this repository, and any
  claim that the repo is "large" is really a claim about that one folder plus three big binaries.

**Dependencies.** Depends on `OBJ-024` having completed (the repository must exist and be pushed before moves
can be made safely). Closes `OBJ-023` as a side effect of the same owner instruction — see `D29`. Touches no
file that `OBJ-021` or `OBJ-022` depend on for their outstanding work, but **will** move paths that their
future work references, so both must be re-pointed if the mapping affects them.

### OBJ-026 — `engage`: one-word workspace readiness for DevProjects

**Objective ID.** `OBJ-026`

**Title.** A single entry point that inspects, synchronizes, analyses, validates and prepares the DevProjects
workspace, then reports what changed, what needs attention and what to do next — invoked by one word.

**Status.** ✅ Completed — built, executed against the live workspace, and self-tested 57/57.

**Summary.** The owner's Monday routine was manual: remember what to pull, visit each repository, fetch,
inspect what changed, work out what was left unfinished. `engage` takes ownership of that preparation while
leaving every potentially destructive decision with the owner. It is an orchestrator, not a script wrapper:
it discovers repositories rather than reading a hard-coded list, applies a per-repository policy, and skips
work that is already done. Six phases — Inspect, Synchronize, Analyze, Validate, Prepare, Summarize.

**Key Deliverables.**
1. `workbench/scripts/engage_core.py` — discovery, the `POLICIES` table and an ordered decision table.
   **Pure**: no writes, no printing, so the table is testable in isolation.
2. `workbench/scripts/engage.py` — the six-phase orchestrator, analysis and rendering. All workspace path
   bindings live in one `PATHS` block.
3. `workbench/scripts/engage_selftest.py` — 13 real git fixtures, 13 synthetic decision-table rows, 11
   safety-guard assertions. **57 passed, 0 failed.**
4. `~/.claude/skills/engage/SKILL.md` — the user-invocable skill: workspace detection, the confirmation
   protocol, and the instruction to narrate the conclusion rather than paste the report.
5. Governance: `D30` (fast-forward pull policy), `D31` (safe-by-default), the `CLAUDE.md` §`engage`
   section, the `.claude/rules/api-surface.md` inventory row, and the `workbench/.engage/` gitignore rule.

**Related Files.** `workbench/scripts/engage.py` · `engage_core.py` · `engage_selftest.py` ·
`~/.claude/skills/engage/SKILL.md` · `workbench/.engage/{context.json,briefing.md,engage.log}` (gitignored) ·
root `CLAUDE.md` §`engage` and §Edit scope · `.claude/rules/api-surface.md` · `.gitignore` ·
`objective-history/03-decisions.md` (`D30`, `D31`) · reused from `workbench/scripts/obj016_daily_refresh.py`.

**Reason for Archiving.** Completed. The deliverable works end to end and is proven by execution, not by
inspection: the first real run fast-forwarded `Dev` by 10 commits and `pam/` by 12, re-derived the stale
dashboards, and a second run correctly did nothing.

**Pending Work.** None for this objective. Two items belong to others: the `PATHS` block and the `POLICIES`
table go on the `OBJ-025` path-fix checklist, and the missed `2026-08-23` weekly execution that `engage`
surfaced is an owner decision under `D29`, not work owned here.

**Lessons Learned / Observations.**
- **A missed scheduled run cannot be detected by comparing `LastRunTime` to `NextRunTime`.** The skipped
  firing is what stretches that gap, so the miss disguises itself. `PAM-Weekly-API-Execution` last ran
  `2026-08-16` with next `2026-08-30`: an inferred 14-day period, and a perfectly healthy-looking task that
  had in fact skipped `2026-08-23`. Reading `DaysInterval`/`WeeksInterval` off the trigger is the fix.
- ⚠️ **The assumption behind `D29` is currently unmet.** `OBJ-023` was closed without resuming because the
  Sunday trigger would supply the second reproducibility data set. That run did not fire, and the previous
  attempt exited `1`. Next scheduled firing `2026-08-30`.
- **Fetch before classifying, always.** `Dev` read 6 behind pre-fetch and 10 behind after. Ahead/behind come
  from remote-tracking refs, so any decision taken before the fetch is a decision about yesterday's state.
- **The safe default for an unclassified repository is the feature, not a limitation.** Discovery can be left
  switched on precisely because an unknown repository is fetched and reported but never pulled.
- **Purity paid for itself.** Splitting the decision table into a module that neither writes nor prints is
  what made 13 synthetic rows testable — including rows real git cannot produce in isolation, such as an
  unmerged path with no `MERGE_HEAD` beside it.
- **Two `CLAUDE.md` statements were wrong and are now corrected** — the do-not-pull sentence that contradicted
  `D28`, and the claim that `AI` has no upstream when it tracks `origin/Dev`.

**Dependencies.** Reuses `obj016_daily_refresh.py` (`Journal`, `child_env`, `make_output_safe`, `FORBIDDEN`,
and the `--execute --skip-git` refresh) and reads the state produced by `OBJ-013`, `OBJ-016`, `OBJ-017` and
`OBJ-020`. Complements `/go-go-go`, which still owns commit-and-push. Feeds the `OBJ-025` path-fix checklist.


### OBJ-027 — Close out the `v0.3` restructure, then build the DevProjects Control Center

**Objective ID.** `OBJ-027`

**Title.** Two halves: finish the cleanup `OBJ-025` started (path audit, drift, script renames,
auto-load budget, dashboard reconciliation) and build the DevProjects Control Center — the interactive
frontend for `engage`.

**Status.** 🟡 **Superseded** — displaced from the active-instruction slot by `OBJ-029`. The Control Center
half is delivered; **three cleanup items are measurably unfinished** and are listed under Pending Work.
Registered here late: it ran concurrently with `OBJ-028` and the register carried a warning that whoever
closed it should insert this row.

**Summary.** The build half succeeded and is in use. The cleanup half was partly done and partly not, and
the gap was only established when a later session audited the workspace against disk rather than against
the objective's own progress notes. Recording it as Superseded-with-pending-work rather than Completed is
deliberate: three of its five cleanup items can be shown to be outstanding by measurement, and marking the
objective done would have buried them.

**Key Deliverables.**
1. `tools/control_center.py` — the local decision server. `127.0.0.1` only, random per-process token held
   in memory and never written to disk, a server-side `ACTIONS` table so the browser sends an action *type*
   plus a target and never a command string. Three action types (`repo.pull_ff_only`, `data.refresh`,
   `decision.note`); anything else is refused **by name**, producing an audit line rather than a silent
   no-op. Zero product HTTP — it has no HTTP client at all.
2. `tools/control-center/` — the third React + Vite app. Four substantive views built on real `engage`
   data plus three honest stubs that state what data they still need.
3. `state/control-center/decisions.jsonl` + `executions.jsonl` — append-only, tracked.
4. Governance: `D36` (decision interface, never a security boundary), `D37` (`not_interested` expires by
   itself — suppression keyed to a state fingerprint, reusing the drift loop's waiver mechanism).
5. Commits `74d48ce` (drift closed to its two real blockers) · `04a8217` (stale user-facing paths, the
   `pct()` contract named) · `3a8f37d` (the Control Center) · `2a7fb69` (the drift report was stale and was
   hiding three defects introduced by the objective itself).

**Related Files.** `tools/control_center.py` · `tools/control-center/` · `state/control-center/` ·
`docs/history/03-decisions.md` (`D36`, `D37`) · `tools/engage.py` + `engage_core.py` (unchanged, consumed).

**Reason for Archiving.** The owner issued `OBJ-029` (build-wise methodology correction, the three
regression fields, and the consolidated workbook) as the active instruction. `Objective.md` holds one
objective, so this one is archived to make room.

**Pending Work.** Three items, each measured against disk rather than inferred:
1. ⛔ **Script renames not done.** The objective called for renaming the `obj0NN_`-prefixed scripts in
   `tools/` to role-based names. `tools/` still holds `obj007_*`, `obj010_*`, `obj012_*`, `obj013_*`,
   `obj015_*`, `obj016_*`, `obj017_*`, `obj020_*`, `obj023_*`, `obj025_*` — the rename pass never ran.
2. ⛔ **Auto-load budget not reduced.** The objective called for moving path-specific bulk out of root
   `CLAUDE.md` into `.claude/rules/`. Measured: root `CLAUDE.md` is **770 lines / 58,072 bytes**, injected
   on every prompt, against three path-scoped rule files totalling 15,925 bytes. The largest sections
   remain inline — response envelope 8.2 KB, edit scope 7.3 KB, drift control 7.2 KB.
3. ⛔ **Path audit incomplete, and it left live wrong instructions.** Root `CLAUDE.md` still describes
   `workbench/` in the present tense (line ~106, including a "Path convention" rule for documents *inside*
   a directory that does not exist) and still directs the reader to `Reports/` at line 39 — inside the
   standard workflow that governs *every* interaction — and again at line 240. Neither directory exists.
   The `.claude/rules` glob table also lists `Reports/**` for `api-surface.md`, a trigger that can never
   fire, while omitting the two real globs `artifacts/runs/**` and `docs/findings/**`.
   ⚠️ The drift loop reports `docs.declared_paths_exist` **clean**, so its path probe does not see these —
   worth fixing in the probe, not only in the prose.

Additionally outstanding and already known: the two `critical` drift invariants `graph.rebuild_target` and
`graph.indexes_validation_package` remain `violated` (the graph marker names a different checkout, so the
graph predates `com.arcon.utils.validation`), and `governance.no_push_permission` remains waived because
re-specifying it needs a per-repository expression in `.claude/settings.json`, which an agent cannot edit.

**Lessons Learned / Observations.**
- **A progress note is not a measurement.** Three cleanup items read as done from the objective's own
  narrative and were shown outstanding by one `wc -l` and two `ls`. Verify a cleanup claim against disk.
- **A stale drift report hides the defects the objective itself introduces** — the lesson `2aa7bf9`
  (part 4) recorded, and the reason the drift probe's blind spot above matters.
- **A path probe that reports clean while the prose names two dead directories is worse than no probe**,
  because it converts an unchecked area into a checked one.

**Dependencies.** `OBJ-025` (the `v0.3` structure it was cleaning up) · `OBJ-026` (`engage`, whose
`engage_core` policy table and `run_git` allow-list the Control Center server is downstream of) ·
`D28`/`D30`/`D31` (per-repository rights and safe-by-default, which the server may not widen).


### OBJ-029 — Build-wise methodology correction, the three regression fields, and one consolidated workbook

**Objective ID.** `OBJ-029`

**Title.** Establish which Jira field the build-wise analysis is keyed on and correct it to `Affected
Milestone`; bring three client-facing custom fields into the analysis; and deliver every ticket-level
detail behind every reported count in a single consolidated Excel workbook.

**Status.** ✅ Completed — methodology corrected, both deliverables regenerated from the pipeline, and
every reported count reconciled against its tickets in Python **and** as live Excel formulas.

**Summary.** The owner asked which field the build-wise analysis used — Milestone, Affected Milestone or
Fixed Version — and whether the methodology was correct. It was **not**. Every build-wise count keyed on
`fixVersion`, which records where a fix *shipped*, and was being read as where a defect was *found*. The
correction changes conclusions, not decimals: the build line grows from 1,384 to **2,010** client tickets,
the heaviest build moves from `base` (262) to `HF6` (399) and `HF1` (388), and the current build `HF13`
drops from an apparent 27 client tickets to **2**. The root cause is recorded: the previous revision
checked the *native* `affectedVersion` field, measured it at 0% project-wide, concluded that no field
records the build a client was on, and fell back to parsing build tokens out of ticket titles — while
`customfield_10092` carried the fact on 97.3% of the population all along.

**Key Deliverables.**
1. **`docs/analysis/D1-client-ticket-patterns.md`** — regenerated, 307 → 544 lines. New `§0` states the
   build axis, why the previous methodology was wrong, and every milestone-shaped field measured and
   rejected. `§7.1` replaces the 9-row title heuristic with a **367-defect field census**. `§7.2` is the
   regression view. `§15`–`§17` define the traceability contract, the workbook manifest, and the
   derivation method for weak spots and scenario gaps including the source of every gap.
2. **`artifacts/workbooks/PAM-Client-Ticket-Analysis.xlsx`** — one workbook, **11 worksheets**, 1.02 MB.
   `01 Testing Weak Spots` (693 ticket-level rows × 20 JIRA-oriented columns, each with a PAM-specific
   recommendation) · `02 Weak Spot Summary` · `03 Test Scenario Gaps` (with provenance) ·
   `04 Ticket Details` (**2,169 tickets × 57 columns** — the source data) · `05 Build-wise` ·
   `06 Escape Latency` · `07 Regression Signal` · `08 Module & Category` ·
   `09 Count Reconciliation` (**live `COUNTIFS` + `PASS`/`FAIL` per figure**) · `10 Field Audit`.
3. **`tools/jira/pamit_workbook.py`** — the workbook builder, with a `verify()` gate that reconciles every
   pool and area count against the ticket universe and **exits non-zero on any mismatch**.
4. `tools/jira/pamit_analysis_rules.py` — `AFFECTED_MILESTONE`, `MILESTONE_FIELDS_REJECTED`,
   `NULL_SENTINELS`, `REGRESSION_FIELDS`, `REGRESSION_CLASSES`, `REGRESSION_CONFIDENCE`, the
   `milestone_builds`/`earliest_build`/`regression_class` helpers, and **`AREA_DETAIL`** — seven authored
   fields per testing area (root cause, existing/missing coverage, precaution, PAM-specific
   recommendation, suggested coverage, automation), every one naming a real file, flag or measured fact.
5. `tools/jira/pamit_client_analysis.py` — trend query re-keyed to `cf[10092]`, `escape_analysis_am()`,
   `analyse_regression()`, `load_capture()` extracted and shared, capture format bumped to **v3**.
6. Governance: `D42` (the build axis), `D43` (no count without its tickets), `D44` (one workbook).

**Related Files.** `docs/analysis/D1-client-ticket-patterns.md` ·
`artifacts/workbooks/PAM-Client-Ticket-Analysis.xlsx` · `tools/jira/pamit_workbook.py` ·
`pamit_analysis_rules.py` · `pamit_client_analysis.py` · `pamit_report.py` ·
`artifacts/client-tickets/snapshots/2026-08-31.json` · `docs/history/03-decisions.md` (`D42`–`D44`).

**Reason for Archiving.** Completed within the session it was raised in.

**Pending Work.**
1. The scheduled task `PAM-Client-Ticket-Analysis` (09:00 daily) runs `pamit_client_analysis.py` only. It
   does **not** yet build the workbook, so the `.xlsx` refreshes on demand rather than daily. Adding
   `pamit_workbook.py` to that task is a one-line change and a deliberate non-decision here.
2. The three regression fields sit at ~25% population. Every figure is correctly quoted over the populated
   subset, but the analysis cannot answer "what share of defects are regressions" until the fields are
   filled. That is a **process** ask for whoever triages PAMIT, not a tooling gap.
3. `«unmapped»` is the largest row in the confirmed-regressions-by-area table because the build line is
   fetched with light records and the area axis needs the description. Either fetch descriptions for the
   build line (2,010 full records, materially slower) or leave the area figures to `§11`, which is what
   the report currently instructs.

**Lessons Learned / Observations.**
- ⛔ **Two fields can both be populated and still answer different questions.** `fixVersion` at 100% and
  `Affected Milestone` at 97% are both "the build", and picking the wrong one inverts the ranking. Ask
  what a field *means* before keying an analysis on it.
- ⛔ **Three fields in this Jira share the name `Affected Milestone` and two are empty on PAMIT.**
  Selecting one of those returns an **empty build line, which reads as a clean result rather than a wrong
  query.** The whole audit is recorded in `§0.2` and on sheet `10 Field Audit` so nobody re-measures it.
- ⛔ **A select field can be populated with the literal string `None`.** `Previous working version` carries
  130 of them and `Forward Merge Milestone` is 63% populated with 344 of 388 values being `None` —
  population without information. `NULL_SENTINELS` exists for exactly this.
- ⛔ **Finding a native field empty is not evidence that the fact is unrecorded.** That single inference
  cost this analysis 626 tickets of population and 358 escaped defects, and it looked like diligence: the
  previous revision measured `affectedVersion` at 0%, said so honestly, and built a title-parsing fallback.
- **A reconciliation the reader can recompute beats one the generator asserts.** Sheet `09` restates every
  count as a live `COUNTIFS` over sheet `04`, so the workbook proves its own totals in Excel.
- **The title heuristic was accurate, just blind.** Where both methods fire they agree exactly
  (`PAMIT-41274`: found HF1, fixed HF12, +11). The defect was coverage, not correctness — worth
  remembering before discarding a heuristic's *results* along with its method.

**Amendment — owner items #8–#11, same session.**

The owner extended the objective after the first delivery. Per `CLAUDE.md` this **amends** the active
instruction rather than replacing it, so `OBJ-029` keeps its ID.

| # | Requirement | Outcome |
|---|---|---|
| 8 | Refresh the master workbook daily, in place; keep history | ✅ Build moved **inside** `pamit_client_analysis.py`, so the existing 09:00 task needed **no change**. New sheet `12 Daily History`, derived from the never-deleted dated snapshots |
| 9 | Use **all** available regression fields; mark gaps `Info not available in JIRA` | ✅ 276-field sweep → **22 regression-shaped fields, 15 populated**. Found `RCA` (`cf 10245`) at **80.7%** — previously declared absent |
| 10 | `Generated` **and** `Updated` timestamps | ✅ Both rendered; they diverge on any `--offline` re-render, which is when it matters |
| 11 | Apply consistently across report and workbook | ✅ Report `§18`; workbook `00 README` rules block, `10 Field Audit`, and the sentinel in every regression cell |

**The second instance of the `D42` error class — the most important finding of the amendment.** §13 read
*"`Module`, `Category`, `Sub-Category`, `Root Cause` … all unpopulated (0 / 376). The whole taxonomy is
derived from ticket text. Jira holds no categorisation to cross-check it against."* It had measured
`customfield_10113` (*Root Cause*, 0.2%) and `customfield_10199` (*Root cause*, 0.1%). Neither is live.
**`customfield_10245` (*RCA*) is 80.7% populated — 1,622 of 2,010 tickets — with 33 values in 15
families**, and `RCA Details (Impact Analysis)` sits beside it at 79.2%. Two decoy fields were measured,
the live one never was, and the conclusion drawn was that the data did not exist. ⛔ **The lesson is now
recorded twice for the same reason: in this Jira instance several fields share a concept and only one is
live. Measure every same-named candidate before concluding a fact is unrecorded.**

**What the RCA field makes possible that was previously impossible.**
1. **A cross-check on the derived taxonomy.** The report's category axis is inferred from ticket text; RCA
   is authored by the product team. Where they disagree, that is a finding about the derivation — and
   `uncat_but_rca` counts the tickets where an authored answer exists and the derivation found none.
2. ⛔ **Separating non-defects on Jira's own say-so.** **315 tickets** are `Requests - Enhancement`,
   `Requests - Information Request`, `Requests - APEM Tool`, `Requests - Script Request`,
   `Others - Working as expected`, `Not a bug` or `Miscommunication`. A testing weak spot attributed to one
   of those is a **false finding**. ⚠️ Reported, **never silently applied**: the defect population stays
   keyed on issue type (`D38`), because re-cutting a denominator on a field that is 19% empty would be a
   worse error than the one it corrects. The workbook flags them so a reader excludes them deliberately.
3. ✅ **Jira's own admission of testing gaps.** `Analysis - Inadequate Test Coverage`,
   `Insufficient Unit Test case`, `Analysis - Incomplete Requirement`,
   `Analysis - Inadequate Technical Design` and `Environment - Non replicated` are the **strongest evidence
   in the whole analysis** for a testing weak spot, because the product team recorded the cause rather than
   this report inferring it.
4. **Why delivered fixes failed.** `Reopen RCA` — Code Fix (48), Dependency failure (29), Audit (23),
   Hosting Issue (22), **Tester Understanding (17 — a QA misunderstanding, not a product failure)**, Data
   Issue (8) — plus `ReOpen Date`, `ReOpen Time Spent` and the reopen trail.

**What Jira cannot answer, stated rather than estimated.** `Phase` (`cf 10164`) and `ReopenCount`
(`cf 11018`) **exist in the schema and are 0% populated**; regression-test-executed, requirement link and
detected-by stage **do not exist at all**. ⛔ Defect-injection phase is therefore **not answerable**, and
the temptation to derive it from the RCA family is refused explicitly: `Code - Logic Issue` records where a
defect was *found in code*, not the phase in which it was *introduced*, and mapping one onto the other
would yield a phase-containment metric that reads as measured and would drive real test-strategy
decisions. An unavailable field gets an **explicit workbook column reading `Info not available in JIRA`
all the way down** — a *missing* column would read as "not analysed".

**Two self-inflicted defects, found by inspecting the generated output rather than by trusting the code.**
1. `_cell()` escaped `=`, `+`, `-` and `@`, on the reasoning that Excel parses all four as formulas. It
   does — when a **human types** them. **openpyxl only promotes a leading `=`**, writing the rest as
   strings, so the guard put a visible apostrophe in front of every negative delta and every ticket title
   starting with a dash. Narrowed to `=`.
2. Sheet `12 Daily History` labelled a column *Build line* while it actually held the **per-build sum**
   (2,025) rather than the de-duplicated population (2,010) — a snapshot stores per-build counts, not the
   total. Relabelled, with the 15-ticket difference explained on the sheet.

**Pending after the amendment.**
1. The three original regression fields remain ~25% populated; `RCA` at 80.7% now carries most of the
   analytical weight. Raising `Functionality working in previous version` and `Previous working version`
   is still a **triage process** ask, not a tooling one.
2. `Phase` is 0% populated. If the product team began filling it, defect-injection-phase and
   phase-containment analysis become possible for the first time — worth asking for, and the highest-value
   single field-hygiene change available.
3. `RCA` is 19.3% empty. The RCA-based views quote their populated subset, as the regression views do.

**Dependencies.** `OBJ-028` (the analysis engine, its read-only Jira layer and the `D38`–`D41` population
rules, all retained) · `D38` (the defect denominator, which is why the escape census reports 367 defects
rather than 439 client tickets) · `D39` (linked tickets are evidence, never population).


### OBJ-030 — Extend both 2026 Jira census reports from 03 Sep to 21 Sep 2026

**Objective ID.** `OBJ-030`

**Title.** Extend the PAMIT and CI 2026 Jira census reports to cover 2026-01-01 → 2026-09-21, processed
separately; update the analysis, not the methodology.

**Status.** ✅ Completed.

**Summary.** Both reports were measured 100% generated, so the extension was a `DATE_TO` bump and a
re-run, never a markdown edit. PAMIT **5,431 → 5,740**, CI **5,588 → 5,994**, delivered as
`01Jan26-21Sep26` with the `03Sep26` set retired. A defect older than this objective was found and fixed:
JQL `created <= 'YYYY-MM-DD'` excludes that whole day, so every prior edition had omitted its own final
date. A later hardening review in the same line found and fixed three further generator defects (PAMIT
§12 `Affected Milestone` published 100% `Not set`; the CI sub-task count of 4,241 was a parent-presence
count, real figure 1,443; §12 counted unpopulated tickets as milestone assignments, 5,832 → 4,615) and
added an independent validator, a preflight and a one-command pipeline.

**Key Deliverables.**
1. `docs/analysis/Jira_Analysis_01Jan26-21Sep26.md` + `.docx` + `.xlsx` (PAMIT).
2. `docs/analysis/CI_Jira_Analysis_01Jan26-21Sep26.md` + `.docx` + `.xlsx` (CI).
3. Snapshots `artifacts/client-tickets/snapshots/jira-analysis-2026-01-01-to-2026-09-21.json` and
   `artifacts/snapshots/ci-analysis-2026-01-01-to-2026-09-21.json`.
4. The dated client pack `21-09-2026/{PAM,CI}/`, built by `tools/jira/build_delivery_pack.py`.
5. `tools/jira/validate_analysis.py` (57 checks, `--self-test`), `doctor.py`, `run_census.py`, and a
   `Source snapshot:` provenance line with a sha256 in each report (`pamit_fmt.snapshot_provenance()`).

**Related Files.** `tools/jira/jira_analysis_2026.py` · `ci_analysis_2026.py` · `analysis_classify.py` ·
`analysis_render.py` · `convert_analysis.py` · `md_to_docx_xlsx.py` · `build_delivery_pack.py` ·
`validate_analysis.py` · `doctor.py` · `run_census.py` · `pamit_fmt.py` · `docs/hardening/README.md` ·
`docs/history/04-narrative-log.md` §4. All of it is recoverable from commit `8d8b841`.

**Reason for Archiving.** Completed, then displaced from the active-instruction slot by `OBJ-031`, which
retires the Jira/PAM/CI line from this workspace and turns it into a clean BLAST framework plus a
`New Task/` working area.

**Pending Work.** None will be resumed here; the line is retired by `OBJ-031`. Recorded for whoever
restores it from `8d8b841`:
1. `CI-25546` is readable by `key =` and invisible to every bulk search, a Jira search-index
   inconsistency (1 in 5,994). Its gate was left failing on purpose.
2. On the committed tree the validator reports **PASS 56 · FAIL 1**. Both CI snapshots were rewritten
   before the first commit, so the CI report's `Source snapshot:` hash no longer matches its snapshot.
   Fix by regenerating from the committed snapshot, never by editing the hash.
3. The 21 Sep final-day counts are a partial day and grow on any later re-run of the same range.
4. `tools/rag/query.py` read a directory `extract.py` never wrote (hardening review F1).

**Lessons Learned / Observations.**
- ⛔ **JQL `created <= 'YYYY-MM-DD'` means `<= YYYY-MM-DD 00:00`.** New JQL uses the half-open
  `created < DATE_TO_EXCLUSIVE`.
- ⛔ **Reconciliation is not validation.** All three hardening defects passed every `OBJ-030` gate, because
  those gates re-ran the generator's own rule. Only an independent re-derivation from the raw snapshot
  caught them.
- **A file renamed by hand after generation turns the next run into a stale deliverable**, which is why
  output names derive from one `RANGE_SLUG` constant.
- **A provenance hash over file bytes depends on line endings.** Git stores the snapshots LF;
  `core.autocrlf=true` restores the CRLF they were hashed with.
- **A validator that has never failed proves nothing.** It was run against the pre-fix reports and caught
  the CI sub-task defect by name before it was trusted.

**Dependencies.** `OBJ-028` (the read-only Jira layer) · `OBJ-029` (`D42` build axis, `D46` populated-subset
rule) · `D38`–`D46`.
