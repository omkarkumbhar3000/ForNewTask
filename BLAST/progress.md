# Progress Log

> What was done, what broke, what was learned. Updated after every meaningful task.

## 2026-07-29 (later) — full generated run: 326 flows, 1,868 calls, 870 endpoints

**Run:** `artifacts/runs/2026-07-29_181439/` · 3 h 11 m · summary in
`docs/management/summary/Full-Generated-Run-2026-07-29.md`.

Done:
- Built `tools/generate_flows.py` — derives flows from `APIConfig.java` (1,307 endpoints) and
  the 66 payload helpers. 323 of 326 flows were generated; the executor was unchanged, which was the point.
- Extended `chain_runner.py`: `extract_any_id` and `verify_value_anywhere` (so generated flows need no
  field names known in advance), verb allowlist, teardown gating, checkpoint/resume, `--wait-for-env`,
  and downtime wait-and-resume.
- Executed the whole plan. 870 distinct endpoints reached (66.6% of the catalogue), 69 of 70 controllers.

Learned:
- **90% of calls returned HTTP 200; only 64% passed all seven layers.** 289 responses carried
  `Success: false` at HTTP 200, and 115 returned a bare string body. A status-only suite would have
  reported this run as 90% green. This is the envelope trap quantified.
- **135 × 404** — `APIConfig.java` declares endpoints that do not exist on the deployment. Independent
  confirmation of ISSUE-005, from execution rather than source comparison.
- **13 of 217 creates actually inserted.** 101 create endpoints have no request body defined anywhere in
  the framework; the rest carry stale hardcoded foreign keys. Write coverage is blocked on payload data,
  not on the harness.
- **Eight distinct response shapes**, four of them new: DataTables-style `aaData`, a pipe-delimited error
  inside `{"Output": "..."}`, a bare `false` boolean body, and a bare `""` body — all at HTTP 200.
- Two more error codes outside `KNOWN_ERROR_CODES`: `206-LC_GLD`, `902-ALC-ISSML`.
- Downtime handling works: the environment went down 3 times mid-run; each time the runner waited 300 s
  and resumed from the paused hop. Zero restarts, zero lost work.

Corrected:
- The runner's own `RUN_REPORT.md` reports 1,200 passing hops; the true figure is 1,204. Four bare-array
  responses were wrongly flagged by the envelope check because generated flows do not emit
  `envelope: false`. The generator should set it for bare-array endpoints.

Open:
- Teardown stayed disabled: generated teardown bodies are not bound to the created record's id, so running
  them would remove pre-existing QA data. 5 hops excluded and reported. Needs id-binding.
- Flow-level verdicts (296 FAIL / 30 PASS) are misleading — one bad hop condemns a ten-hop read sweep.
  Hop level is the measure that should be quoted.

## 2026-07-29 — API chaining executed end to end (3 flows, all PASS)

**Run:** `artifacts/runs/2026-07-29_160155/` · `QA_MsSQL` · 15 hops · 15 evidence files · zero 5xx.

Done:
- **ISSUE-009 resolved.** Token generation never was a logic fault — `QA_MsSQL.properties` held a stale
  password (`<REDACTED>`). With the owner's updated credential: 200 in 3.50 s, bearer, 24 h.
- Built `tools/chain_runner.py` — a generic executor over **declarative flow JSON**. Flows are
  data (`tools/flows/*.json`), so generation can extend them without touching the runner and
  the hand-written flows survive unchanged.
- Three flows executed live: `lob_hierarchy`, `user_lifecycle`, `service_lifecycle` — five levels each.
  Created **UserId 1456** and **ServiceId 25339**, both verified by independent reads.
- Retention changed across all four harnesses: **auto-delete removed**, every run writes its own dated
  folder under `artifacts/runs/`. Pre-existing output archived to `artifacts/runs-archive/`.
- All scripts moved to `tools/` with search-based workspace-root resolution.
- Added `demonstrate_readme.md` (root) — how to read a report, re-execute, and how generation works.

Learned:
- **`Success: true` does not mean a write happened.** `SetServiceDetails` returns `Success: true` with
  `Message: "Already Exists"` — a no-op that a status check *and* a `Success` check both score green.
- **HTTP 200 with `Success: false` + `ErrorCode` captured live** on `GetLogDetails`. `206-LC_GLD` is not in
  the framework's `KNOWN_ERROR_CODES {201,202,203}`, so that set is incomplete.
- **Four envelope shapes on one API**, including a bare array with no envelope from
  `GET /api/DeviceOnboarding/GetLOBList`.
- **Blind `Result[0]` chaining fails.** `GetLOBList[0]` is LOB 1 (`O11`) which has no user groups; only 19
  of 34 LOBs do. Flows select the LOB by name and discover its id.
- Type drift: `ServiceId` is a string on create, an integer on read. Explicit casts needed.
- Writes are slow — creates 5.5–6.5 s, full user list 7.4 s. The inherited 2,000 ms SLA was read-only.

Broke, then fixed:
- Rewriting two files through PowerShell `Get-Content`/`Set-Content` corrupted UTF-8 into mojibake (PS 5.1
  reads as ANSI). Repaired by reversing the codepage round-trip. **Use the Edit tool for text files.**

Open:
- The transaction-log hop (`GetLogDetails`) needs filter parameters beyond `LogTypeId` — returns
  `No Records Found`. Needs the Confluence API reference or a developer answer.
- `baseline-qa_mssql.json` still records `503` from the outage; re-promote from a healthy run.
- Java/TestNG port not started. Created records are not cleaned up (deletion is refused by the gate).

## Phase 0 — Initialization
- Framework skeleton in place: `B.L.A.S.T.md` (protocol), `Objective.md` (requirement).
- Memory files created: `task_plan.md`, `findings.md`, `progress.md`.
- `LLM.md` initialized as the Project Constitution — schema section still empty.
- Jira MCP configuration prepared but **not activated** (`.mcp.json.template`, see `MCP-SETUP.md`).
- `GROQ_KEY` set in `.env` and **link verified live**.
- **HALT in effect** — no Layer 3 tools until Discovery + Schema are confirmed.

## Framework validation (trial run, completed)
A throwaway smoke test exercised all five phases end-to-end before this reset:
Discovery → schema → live GROQ handshake → 3-layer build → run → teardown.
The self-annealing loop fired on a real defect and resolved it. All three failure
paths (missing key, missing input, empty input) exited 1 with clear messages.
Durable learnings kept in `findings.md`; trial code removed.

## Run 1 — 2026-07-28 · Dynamic API validation script generation (PAM)

**Objective received.** First real objective. Deliverable requested was an *analysis*, not code:
feasibility verdict, gap analysis, user-side requirements, enhancements, clarifying questions.

**Done**
- Read `B.L.A.S.T.md` and `Objective.md`; loaded the workspace's existing decision-layer doc on this exact
  topic, `docs/history/archive/workbench-archive/approach/dynamic-api-generation.md` (workstream `D`), rather than re-deriving it.
- Measured the developer repo against the declared API surface — 3 independent measures over all 1,306
  declared endpoint pairs and 6,866 `.cs` files. See `findings.md` F1.
- Reproduced the automation repo's executability numbers independently (1,160 / 1,322 · 87.7 %) and found
  two refinements the existing doc lacked: **0 payload methods require arguments**, and the negative-case
  taxonomy already exists as 386 hand-written classes. See `findings.md` F2, F3.
- Fed the new measurements back into `docs/history/archive/workbench-archive/approach/dynamic-api-generation.md` §2, §2.1, §9.1 —
  correcting its `ActivityLogs` figure (was "6 declared, 1 implemented"; actually 17 and 1).

**Outcome:** ⚠️ **Partially feasible.** The objective's *intent* is achievable today; its *stated method*
(parse the developer source) is not — that source holds under 8 % of the API under test. Full verdict
delivered to the owner.

**Learned**
- The objective's premise was checkable and false. Verifying the premise before assessing feasibility was
  the whole value of this run — a plan built on Roslyn-parsing `pam/PAM` would have failed late.
- The existing workspace docs had the right conclusion from a single spot-check; measuring it turned a
  claim into evidence and corrected a number.

**Not done, deliberately**
- Nothing written to `tools/`. Protocol 0 is **not** cleared: Discovery answers are outstanding and
  `LLM.md` §3 has no data schema yet. Measurement scripts stayed in the session scratchpad.

## Errors / learnings
- See `findings.md` → *Platform gotcha: Windows + Node + fetch*.
- Run 1: a background measurement script timed out at 420 s because a per-endpoint loop re-read all 6,866
  `.cs` files. Fixed by tokenising the corpus once into a set and testing membership. Applies to any future
  pass over `pam/PAM` — build one corpus, query it many times.

## Status
Run 1 analysis delivered. **Blocked on the owner's answers** to the clarifying questions before any
implementation begins — chiefly the input-source decision (Q1) and the pass/fail semantics (Q3).
