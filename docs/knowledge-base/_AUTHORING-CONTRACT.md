# Knowledge-base authoring contract — read before writing a single question

**Objective:** `OBJ-008` · **Output:** `artifacts/workbooks/PAM-Project-Knowledge-Base.xlsx`
**Your job:** emit JSON rows. **You never write `.xlsx`** — `tools/build_knowledge_base.py` is
the single writer, so the workbook stays consistent and rebuildable.

---

## 1. The one rule that matters

⛔ **An answer without a citation is not an answer.**

Every row's `evidence` field must name something a reader can open: a file path, a report, a run folder, a
`file.java:line`, a SQL query, a `<doc>:p<N>` page citation, or a git commit. "Measured during testing" is
not evidence. "`artifacts/runs/2026-07-29_181439/results.json` — 196 L5 checks with detail
`resolved []; MISSING ['NEW_ID']`" is.

**Where something is genuinely not established, the question still belongs in the workbook.** Set
`status = "Open"`, and write an answer that says plainly what is unknown and what would settle it. Never
invent a plausible answer — the project's single largest finding is *how much* is undocumented, and that
only holds if nothing was filled in to look complete.

## 2. Output contract

Write **one JSON file**, a flat list of row objects, to the path given in your task. Keys exactly as below —
all present on every row, `""` where genuinely not applicable.

| Key | Content |
|---|---|
| `id` | `Q-<AREA>-<NN>`, e.g. `Q-API-01`. Your task states your `<AREA>` prefix — use only that one |
| `category` | One of the categories your task assigns you. Exact string, no variants |
| `module` | The subsystem: `API` · `Framework` · `Database` · `Documentation` · `Governance` · `Tooling` · `Security` · `Reporting` · `Environment` · `Product` |
| `question` | As a stakeholder would actually phrase it. See §3 |
| `answer` | Direct, complete, self-contained. Leads with the answer, then the reasoning. Numbers with their basis |
| `evidence` | The citation(s). Multiple separated by ` · `. **Never empty** |
| `comments` | Caveats, gotchas, what a reader would get wrong, related open questions |
| `source` | Where the answer came from: `measured run` · `static analysis` · `database query` · `code read` · `product documentation` · `owner decision` · `workspace history` |
| `related_documents` | Files a reader should open next, ` · ` separated |
| `api_reference` | The endpoint(s) or Swagger reference, if the question concerns a specific API. Else `""` |
| `example` | A concrete snippet, command, payload, response or figure that makes the answer tangible. Keep under ~600 chars |
| `status` | `Answered` · `Answered - with caveats` · `Open` · `Superseded` |
| `severity_or_impact` | Why the reader should care: `Critical` · `High` · `Medium` · `Low` · `Informational` |
| `audience` | Who asks this: `Management` · `Developer` · `QA` · `Auditor` · `New joiner` — multiple ` · ` separated |
| `owner` | Team accountable for the answer staying true: `QA Automation` · `PAM Development` · `DBA` · `IT Operations` · `Documentation` · `Project owner` |
| `last_updated` | Exactly `2026-08-04` |

## 3. What makes a good question

Write the question a **real person asks**, not a heading. Compare:

| ⛔ Weak | ✅ Strong |
|---|---|
| "API endpoint count" | "How many endpoints are we actually testing, and why do I see 1,306, 1,322 and 1,336 in different documents?" |
| "Response envelope" | "If a test asserts HTTP 200 and passes, does that mean the API call succeeded?" |
| "Database validation" | "We gave you database credentials — can you now prove a record was actually created?" |

Cover the **uncomfortable** questions too, honestly:

- "Why is the pass rate 64% when 90% of calls returned HTTP 200?"
- "You reported 105 read-back failures — how many were real?"
- "Is any of this automation actually running in CI today?"
- "What did you get wrong, and how do I know you'd tell me?"
- "Why can't you just test the remaining 436 endpoints?"

A management-facing knowledge base that only contains flattering questions is useless in the meeting where
it matters.

## 4. Anti-duplication

Several agents are writing in parallel. **Stay strictly inside the categories your task assigns you.** If a
question clearly belongs to another agent's category, skip it — do not write it "just in case". Cross-refer
by putting the other area's likely question topic in `comments` instead.

## 5. Established facts — reuse, do not re-derive

These are measured and authoritative. Cite them; do not spend effort re-proving them, and do not contradict
them without stating that you are and showing why.

| Fact | Value |
|---|---|
| Endpoints under test | **1,306** distinct `(controller, action)`. `1,322` = raw route constants in `APIConfig.java`; `1,336` = all `public static String` including headers/verbs. Both are answers to different questions |
| Verb split | `GET` + `POST` = **99.7%**. Deletion is `POST /api/<C>/Delete<Thing>` — guard on **names**, never verbs |
| Executed run | `artifacts/runs/2026-07-29_181439/` — 326 flows · **1,873 hops** · 1,868 HTTP calls · 11,503 s · **870 of 1,306** endpoints |
| Status-only vs true pass rate | **90%** HTTP-200 green vs **64%** true across all layers |
| L1–L7 check tallies | L1 1,688/180 · L2 1,864/4 · L3 1,278/590 · L4 1,410/458 · L5 982/**196** · L6 **2**/105 · L7 1,855/13 (PASS/FAIL) |
| The 196 `MISSING ['NEW_ID']` split | **117** creates genuinely failed · **19** acknowledged but returned no identifier · **0** extractor bugs · **60** indeterminate |
| L6 read-back truth | **97 of 107** could never have passed — the check searched each response for the literal string `${NEW_ID}`. For **101 of 107** the run cannot separate "never created" from "created but not readable back" |
| Response shapes | **31** distinct, only **6** documented. 127 responses are not JSON objects; 288 carry no `Success` field |
| False success | **70** responses returned `Success: true` having written nothing. The framework caught **0** |
| The casing defect | `ApiHelper.validateResponseErrorCode` read `success` (camelCase); lowercase occurs in **0** of 1,868 responses, PascalCase `Success` in **1,580** — so the assertion could never pass. Fixed under OBJ-007 |
| Error codes | Framework had `{201,202,203}` hardcoded; the real measured `206-LC_GLD` arrives on HTTP 200. Product documents **4** error codes for 1,306 endpoints |
| Mandatory fields | `3` of `~6,738` properties carry `[Required]` across the whole product — but all 3 sit on a class in a service not among the 70 controllers, so **on the surface under test it is 0 of 5,175** |
| Constraint metadata | **12** families return zero, including `[StringLength]`, `[MaxLength]`, `[Range]`, `[RegularExpression]` and Newtonsoft `Required.Always` — yet the server demonstrably runs the Newtonsoft check (**123** live rejections), so the enforcing models were never supplied |
| Create endpoints | **217** total · only **13** can be driven successfully · **185 (85.3%)** have no mandatory-field signal at all · **0 of 1,245** create body properties carry a max-length, format or pattern |
| Developer repo | **48 of 1,306** endpoints (3.7%) exist in `pam/PAM`; **58 of 70** controllers have no implementation there (settled — `54` was a hardcoded literal never computed, `23` answered a narrower question) |
| Negative design | **10,448** scenarios generated across all 1,306 endpoints in 19 categories. **7,664 (73.4%)** have no documented expected outcome. **1,289 of 1,306 (98.7%)** endpoints have zero runnable negative coverage |
| Negative suite state | **199 of 279** referenced `@DataProvider` names do not exist (650 tests fail at TestNG init); all **80** that resolve read the **positive** sheets. The 3,652-row negative workbook is declared in config and read by nothing |
| Database | Validation **is** possible. QA target `ARCOSDB_U16SP2_WEBSM_QA` on `10.10.0.194,1433`; the API's writes land there, confirmed three ways. Encryption is **narrow** (3 table families); audit log, keys and timestamps are plaintext |
| DB security defects | Deterministic at-rest encryption (20,651 rows → **59** distinct `ss_port` ciphertexts — functionally AES-ECB) · cleartext API passwords in `sso_ApiUsers` plus an unencrypted private key in `tbl_KeyEncryptionDecryption` · **16,560** authorisation rows referencing deleted services, with only **5** foreign keys across 552 tables |
| Blocklist | `GetErrorLogs`, `GetLogs`, `GetAllActiveUserDetails` stop the IIS app pool — 3 sequential calls took the API to 503. **98** endpoints at risk (LH-08); 110 blocked as app-pool-killers, 50 more as mutating |
| Token | `GenericScheduler` is **locked** and is also the data-warehouse ETL account. The token committed in `QA_MsSQL.properties` **expired 2026-07-31**. Never retry `/arcontoken` |
| Chaining that works | **2 of 326** flows achieved a real multi-hop chain — `user_lifecycle` and `service_lifecycle`, both with pinned extract selectors. Depth cliff at hop 4→5: 131 flows (40%) died at the create hop |

## 6. Where to look for answers

| Need | Path |
|---|---|
| OBJ-007 analysis reports (9) | `docs/analysis/A1…A7`, `B-framework-validation-enhancement.md`, `C-database-validation.md` |
| The tabular evidence | `artifacts/workbooks/*.xlsx`, sourced from `data/analysis/*.json` |
| Raw run evidence | `artifacts/runs/2026-07-29_181439/` — `results.json`, `RUN_REPORT.md` (**6,621 lines — get the section map first**), `evidence/` (1,868 files) |
| Authored defect write-ups | `docs/findings/issues/` (11) |
| The 12 developer findings | `docs/briefs/developer-loopholes.md` — source of truth; packaged in `artifacts/loopholes/LH-NN-*/` |
| Documentation gap | `docs/briefs/document-gap.md`, `docs/gaps/01-Data-Gap-Analysis.md`, `02-Data-Access-Requests.md` |
| Project history and decisions | `docs/history/README.md` + `docs/history/01…05` |
| Operating rules | root `CLAUDE.md`, `.claude/rules/*.md`, root `README.md` |
| Framework reference | `Automation gitlab repo/pam_automation_bootstrap/AGENTS.md` |
| Product docs — **never read the corpus directly** | `python tools\rag\query.py find "<terms>"` · `page <doc> <N>`; cite `<doc>:p<N>` |

⚠️ **Large-file rule.** Anything over ~1,500 lines is truncated silently on read. `grep -n "^## "` for a
section map first, then read ranges. Never read `artifacts/rag-corpus/pam-api.md` (101,803 lines) directly.

⛔ **Issue zero HTTP requests. Issue no database writes.** Everything you need is already on disk.
