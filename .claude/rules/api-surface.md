---
paths:
  - "**/APIConfig.java"
  - "tools/**"
  - "artifacts/loopholes/**"
  - "artifacts/runs/**"
  - "docs/findings/**"
  - "pam/PAM/**"
---

# The API surface — counts, verbs, and where the real API lives

Loads when you touch the endpoint catalogue, the harness scripts, the evidence packs or the product
source. The **response-envelope rule, the token lockout and the app-pool blocklist are safety rules and
live unconditionally in the root `CLAUDE.md`** — they are not repeated here.

## Product under test

`pam/PAM/` is .NET: ~181 `.csproj`, of which 10 serve HTTP. Nine are .NET Framework 4.5–4.8 IIS apps; one
(`OfflineMultiTabService/OfflineAPI`) is ASP.NET Core 3.1. There is **no Swagger/OpenAPI anywhere**, and no
`[Route]` attributes in any Framework project — routes come from `App_Start/WebApiConfig.cs` templates that
differ per project.

**The API the QA suite targets is not in this snapshot, and that is measured, not suspected.** Only
**48 of 1,306** endpoint operations declared in `APIConfig.java` are implemented anywhere under `pam/PAM`
(3.7%). The real API is served by separate microservices behind `ARCONAPIGateway` — see
`docs/findings/issues/ISSUE-005-api-coverage-gap.md`. Do not try to derive the API surface from `pam/PAM`.

✅ **Settled: 58 of 70 controllers have no implementation in `pam/PAM`.** Quote **58**. The two figures that
circulated were both wrong, in different ways:

| Figure | Verdict |
|---|---|
| **54 of 70** | ⛔ **Never measured.** `build_source_map.py:333` emits the string `"54 of 70 catalogue controllers are absent from that snapshot"` as a **hardcoded literal**. No code computes it. `SOURCE-MAP.md` and `docs/gaps/01-Data-Gap-Analysis.md` both inherited it from that generated file |
| **23 of 70** | 🟡 Answered a different question — the controller name appearing *nowhere in any `.cs` text*, which recomputes as **22**. A name can appear only in a comment or an outbound call site, so that is not "absent" in any sense that matters |

The 48/1,306 endpoint figure was never in dispute. Full derivation and the list of every document corrected:
`docs/analysis/A6-developer-repo-analysis.md` §6.

## The endpoint count — four numbers, use 1,306

`APIConfig.java` is 1,481 lines and yields a different total depending on what you count. Measured:

| Basis | Count |
|---|---:|
| All `public static String` declarations | 1,336 |
| …of which are **not** endpoints (`get`, `post`, `Authorization`, `Bearer`, `x-pam-version`, …) | 15 |
| `/api/` endpoint declarations, duplicates included | 1,321 |
| Distinct `/api/` path strings | 1,308 |
| **Distinct `(controller, action)` endpoints — the canonical figure** | **1,306** |

**Quote 1,306.** All coverage percentages in `artifacts/runs/` are computed against it (e.g. 870 endpoints reached
= 66.6%). `1,336` counts header and verb constants and is not an endpoint count; `1,322` is stale.

## Verb reality — there is almost no PUT, PATCH or DELETE

| POST | GET | PUT | DELETE | PATCH |
|---:|---:|---:|---:|---:|
| 992 | 325 | 2 | 2 | 0 |

`GET` + `POST` covers **99.7%** of the surface. Deletion is expressed as `POST /api/<C>/Delete<Thing>`, not
as an HTTP DELETE — so a destructive call looks like an ordinary POST. **Name-based guards matter more than
verb-based ones.** The only four exceptions are on `/api/User` (two templated DELETEs, two PUT edits).

## Harness scripts — all of them live in `tools/`

Never in `artifacts/`, never in a pack folder. Execution scripts write to their own dated folder under
`artifacts/runs/` and **delete nothing**. All are deny-by-default: **a bare run issues zero HTTP calls**;
`--execute` (or `--revalidate`) is required. Output before 2026-07-29 is in `artifacts/runs-archive/`.

| Group | Scripts |
|---|---|
| Execution | `chain_runner.py` (declarative multi-hop chains) · `run_qa_mssql.py` (legacy sweep) · `run_validation.py` (Swagger surface; the others import its 7-layer validator) · `run_chains.py` (graph-derived) |
| Generation | `generate_flows.py` → `flows/generated/` (positive chains) · **`generate_data_flows.py` → `flows/generated-data/`** (negative / boundary / positive-parity, from the Excel corpus) · `build_source_map.py` → `source-map.json` + `SOURCE-MAP.md` |
| OBJ-010 pipeline | **`obj010_datatables.py`** (the one reader for all three test-data workbooks) · `obj010_inventory.py` · `obj010_collect.py` (validation gate) · `obj010_build_workbook.py` (execution + benchmark workbook) · `obj010_rescore.py` (re-judge a stored run, zero HTTP) · `obj010_admin_auth_probe.py` |
| Workspace readiness | **`engage.py`** (`OBJ-026`, the `engage` entry point) · `engage_core.py` (discovery + policy + decision table, pure) · `engage_selftest.py`. ⚠️ Safe-by-default rather than deny-by-default (`D31`) — the one exception in this directory, justified by zero product HTTP and `--ff-only`-only git |
| Evidence packs | `build_lh_pack.py` (CLI/registry) · `lh_common.py` (engine) · `lh_specs_run.py` · `lh_specs_static.py` · `lh_specs_obj010.py` (LH-13) · `lh01_evidence.py` (LH-01's bespoke original) |

⚠️ **`generate_flows.py` emits positive flows only** — lifecycle and read sweeps. It has no concept of an
expected rejection. Negative, boundary, input-validation and error-handling coverage comes from
`generate_data_flows.py`, which reads the QA team's authored Excel scenarios. Together they produced OBJ-010's
**747 flows / 5,590 cases**.

⛔ **Do not resolve a workbook by substring.** `API_ExcelDataProviderFileName` is a substring of
`Negative_API_ExcelDataProviderFileName`, and matching on the former first silently read 376 negative
providers from the wrong workbook — understating the corpus by ~2,450 rows. `obj010_datatables.py` uses
longest-key-wins and is the single reader; do not re-derive this elsewhere.

`python tools\build_lh_pack.py --all` rebuilds **LH-02…13** with zero HTTP calls. ⛔ **It does
not rebuild LH-01** — that pack is attached to `PAMIT-42744` and is left exactly as raised. A spec may pin its
own source run via `LoopholeSpec.run_id`: **LH-13** reads `2026-08-05_114315` while LH-02…12 stay pinned to
`2026-07-29_181439`, so their published figures remain reproducible.

⛔ **Generated output is never hand-edited.** `artifacts/loopholes/LH-*/EVIDENCE.md`, `EVIDENCE.xlsx` and
`data/` are rebuilt from run data — a hand edit is silently discarded on the next rebuild. Fix the script.

## Contract sources

- **Swagger** — 37 specs, 690 operations, listed in `data/sources/Automation PAM Endpoints
  Details_Shared(Swagger_JSON Links).csv`, fetched on demand (`artifacts/spec-cache/` does not exist). They
  describe a **different surface**: ~6% name overlap with `APIConfig.java`, and **0 of 690** declare any
  4xx or 5xx.
- **`PAM API (Internal Team).pdf`** — 2,470 pp, extracted to `artifacts/rag-corpus/pam-api.md`. **3,194
  JSON payload examples, 1,654 endpoint-bound** — the best request-body source available. 70% of endpoints
  undocumented, 4 error codes, payloads bound by **page proximity** so some bindings are wrong.
- **What the data cannot answer** — `docs/gaps/01-Data-Gap-Analysis.md`. Reads are covered; **only
  13 of 217 create endpoints** can be driven, because nothing supplies a valid request body.
