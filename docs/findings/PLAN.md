# Developer-Loopholes — build plan for LH-02 … LH-13

**Status:** in progress · **Owner gate:** ⛔ no Jira ticket is raised for any of these until the
owner has validated the evidence and approved. LH-01 (`PAMIT-42744`) is the only one raised.
**Last updated:** 2026-08-05 — LH-13 added from the `OBJ-010` run.

---

## 1. Measured scope — profiled from the source run before any pack was written

Every figure below was recomputed from `artifacts/runs/2026-07-29_181439/` (1,873 hops, 1,868
calls) or from static analysis, **not** copied from `docs/briefs/developer-loopholes.md`. Where
the two disagree, the difference is explained in the pack.

⚠️ **LH-13 is the exception, deliberately.** It is recomputed from
`artifacts/runs/2026-08-05_114315/` (5,430 hops, 5,416 executed) because it *could not exist* in
the pinned run — that run never sent an invalid credential. `LoopholeSpec.run_id` pins the
source per pack, so LH-02…11 remain byte-reproducible against the older run.

| # | Finding | Measured scope | Basis |
|---:|---|---|---|
| 2 | `Success: true` when nothing created | 49 responses; **6** are true create no-ops (`Already Exists`), 43 are empty reads | run |
| 3 | Multiple response shapes on one API | **16** distinct shapes measured; brief's "8" is the coarser family grouping | run |
| 4 | Error-code register incomplete | **108** distinct codes across all responses; register documents 4; framework knows 3 | run |
| 5 | Declared endpoints return 404 | **135** calls, 135 distinct endpoints | run |
| **13** | **Invalid auth token accepted** | **57** endpoints answered HTTP 200 to an invalid bearer; **19** in scope after excluding 34 health probes and 4 bootstrap endpoints; **6 writes**, **8 disclose data** | run (`2026-08-05_114315`) |
| 6 | Mutation exposed over HTTP GET | `SetStatus` declared **GET on 49 controllers**; 321 GET / 982 POST / 2 DELETE / 1 PUT | catalogue |
| 7 | Field naming and types inconsistent | 951 distinct field names, **61 variant groups**; `ServiceId` has **7** spellings | catalogue + payloads |
| 8 | Two endpoints stop the IIS app pool | 2 actions × **49 controllers** = 98 endpoints; 3 requests took the environment down for a day | ISSUE-010 |
| 9 | Service passwords returned in cleartext | **23** responses, **21** distinct endpoints carry a password-shaped key | run |
| 10 | No validation attributes on request models | 6,866 `.cs`, 6,738 auto-properties, **3** `[Required]`, **0** `[Range]`/`[StringLength]`/`[MaxLength]`/`[RegularExpression]` | static |
| 11 | Internal errors leaked in messages | **16** responses, 16 distinct endpoints, incl. build-server paths | run |
| 12 | Unfiltered full datasets | **25** responses >100 KB, 19 >500 KB, largest **8.0 MB** | run |

## 2. ⛔ Re-validation policy — per loophole

`QA_MsSQL`, token supplied via `PAM_API_TOKEN` (never `/arcontoken` — the `GenericScheduler`
account is locked, ISSUE-009).

| # | Live replay | Why |
|---:|---|---|
| 2 | ✅ safe | The creates are no-ops — they already fail or report "Already Exists" |
| 3 | ✅ safe | Shape classification needs only the response body; reads |
| 4 | ✅ safe | Same call set as LH-01, already replayed 289/289 |
| 5 | ✅ safe | The routes do not exist; a 404 mutates nothing |
| 6 | ⚠️ **partial** | `GetStatus` may be read. **`SetStatus` is never called** — it mutates, and that is the entire point of the finding |
| 7 | ✅ safe | Reads only, to confirm the field spellings in live responses |
| 8 | ⛔ **FORBIDDEN** | `GetLogs`/`GetErrorLogs` stop the IIS application pool. Three requests took QA down for a day. Evidence comes from ISSUE-010; the blocklist stays enforced |
| 9 | ✅ safe | Reads. Responses are redacted before anything is written to disk |
| 10 | n/a static | Source analysis of `pam/PAM`; nothing to call |
| 11 | ✅ safe | Same responses as LH-01's leak subset |
| 12 | ✅ safe | Reads, but body capped — one response is 8 MB |

## 3. Deliverables per pack

Identical contract to LH-01 (`docs/findings/README.md` §3):
`JIRA-TICKET.md` · `EVIDENCE.md` · `EVIDENCE.xlsx` · `data/*.json`.
MD and Excel are generated from one dataset by one script, never hand-edited.

## 4. Build order

Grouped so related evidence is derived once and reused:

1. **Run-derived, response-shape family** — LH-03, LH-04, LH-02 (all read the same envelopes)
2. **Run-derived, failure family** — LH-05, LH-11, LH-12
3. **Security family** — LH-09, **LH-13**
4. **Catalogue/static family** — LH-06, LH-07, LH-10
5. **Incident** — LH-08 (documentary; no execution)

## 5. Known overlaps to cross-reference, not restate

| Pair | Relationship |
|---|---|
| LH-01 ↔ LH-04 | LH-01 measured 104 codes inside its 289; LH-04 covers all 108 across every response |
| LH-01 ↔ LH-11 | LH-01 found 11 leaks inside its 289; LH-11 covers all 16 |
| LH-03 ↔ LH-04 | Shape 5 (`Success:false` envelope) is the carrier for the error codes |
| LH-08 ↔ LH-12 | Both are unbounded-query defects; LH-08 is the fatal case of LH-12 |
| LH-06 ↔ LH-08 | The same 49-controller diagnostic scaffold (`GetLogs`/`GetStatus`/`SetStatus`) |
| LH-02 ↔ LH-01 | Both are "the status line does not reflect the outcome"; LH-02 is the `Success:true` half |
| LH-13 ↔ LH-01 | LH-13's bypass arrives at HTTP 200, so status-code monitoring never sees it |
| LH-13 ↔ LH-09 | Same trust boundary — LH-09 leaks credentials to an authenticated caller, LH-13 leaks data to an unauthenticated one |
| LH-13 ↔ LH-10 | Authorization is undeclared for the same reason validation is: nothing is expressed declaratively on the controller |
