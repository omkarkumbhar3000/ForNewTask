# Developer-Loopholes — Evidence Packs and Jira Drafts

**Purpose:** turn each finding in `docs/briefs/developer-loopholes.md` into a self-contained, raisable
Jira ticket backed by citable evidence.
**Scope:** 13 findings · **Evidence packs complete:** 13 · **Raised in Jira:** 1 (`PAMIT-42744`)
**Source of truth for the findings list:** `docs/briefs/developer-loopholes.md`
**Not versioned** — this folder sits outside both git checkouts, parallel to `BLAST/`, so nothing
written here can reach a product build.
**Last updated:** 2026-08-05 — **LH-13 added** from the OBJ-010 run; LH-05's scope re-measured.

---

## 1. Why this folder exists

`docs/briefs/developer-loopholes.md` states every finding in one brief for the development team.
That brief is the right shape for a conversation and the wrong shape for a defect tracker: a Jira
ticket needs one finding, its own evidence, its own reproduction steps and its own severity
justification, and it needs them as attachments a developer can open without access to this
workspace.

This folder holds one subfolder per finding, each producing that ticket.

`docs/findings/issues/` is **not** superseded by this. The distinction:

| | `docs/findings/issues/` | `artifacts/loopholes/` |
|---|---|---|
| Audience | Internal QA and management | The development team, via Jira |
| Form | Analytical write-up | Ticket draft + attachable evidence |
| Granularity | Whatever the analysis found | Exactly one finding per folder |
| Regenerated | Authored by hand, retained | **Rebuilt from run data by script** |

Where an issue and a loophole cover the same defect, cross-reference rather than restate — see
`LH-01` §9, which points back at ISSUE-001, ISSUE-003 and ISSUE-009.

---

## 2. Status

| # | Finding | Severity | Measured scope | Live re-validation | Jira |
|---:|---|---|---|---|---|
| 1 | HTTP 200 for application-level failures | 🔴 Critical | 289 calls · 276 endpoints | ✅ **289/289 reproduce** | ✅ **PAMIT-42744** |
| 2 | `Success: true` when nothing was created | 🔴 Critical | **2** write no-ops · 8 success-message variants | ✅ 49/49 (+503 withheld) | ⬜ Need to create a ticket |
| 3 | Multiple incompatible response shapes | 🔴 High | **9** families · 16 variants · 872 endpoints | ✅ 39/40 | ⬜ Need to create a ticket |
| 4 | Error-code register incomplete | 🔴 High | **108** codes vs 4 documented | ✅ 40/40 | ⬜ Need to create a ticket |
| 5 | Declared endpoints return 404 | 🟠 Medium | **135** endpoints *(pack)* · **348 of 1,388** on the newer run | ✅ **135/135** | ⬜ Need to create a ticket |
| 6 | Mutation exposed over HTTP GET | 🟠 Medium | `SetStatus` GET on **49** controllers | ⚠️ all 49 withheld — mutating | ⬜ Need to create a ticket |
| 7 | Field naming and types inconsistent | 🟠 Medium | **61** concepts · 7 spellings of `ServiceId` | n/a — static | ⬜ Need to create a ticket |
| 8 | Two endpoints stop the IIS app pool | 🔴 Critical | **98** endpoints at risk | ⛔ **FORBIDDEN** | ⬜ Need to create a ticket |
| 9 | Credentials returned in responses | 🟠 Review | 23 responses · 21 endpoints | ✅ 16/16 (+7 withheld) | ⬜ Need to create a ticket |
| 10 | No validation attributes on request models | 🟠 Medium | **3** `[Required]` in 6,738 properties | n/a — static | ⬜ Need to create a ticket |
| 11 | Internal detail leaked in errors | 🟡 Low | **16** responses w/ stack traces | ✅ 16/16 | ⬜ Need to create a ticket |
| 12 | Unfiltered full datasets | 🟡 Low | 25 responses ≥100 KB · largest **8.0 MB** | ✅ 25/25 | ⬜ Need to create a ticket |
| **13** | **Invalid auth token accepted — HTTP 200** | 🔴 **Critical** | **19** in scope of 57 · **6 writes** · **8 disclose data** | ⛔ **not replayed — writes** | ⬜ Need to create a ticket |

⛔ **LH-02 … LH-13 are drafted but NOT raised.** They are held pending the owner's validation of
the evidence. `PAMIT-42744` (LH-01) is the only ticket in Jira.

⚠️ **LH-13 sources a different run.** LH-01…12 are pinned to `2026-07-29_181439`, so their published
figures stay reproducible. LH-13 could only be found in **`2026-08-05_114315`** (OBJ-010) — the first run in
which the framework sent a deliberately **invalid** credential. `LoopholeSpec.run_id` carries that per-pack;
unset means the pinned run.

⛔ **LH-13 is never replayed, and that is a deliberate refusal rather than an omission.** Six of its
in-scope endpoints are writes (`UpdateMobileOTPRegistrationDetails`,
`InsertFileServerConfiguration`, `UpdateFileUploadConfiguration`,
`UpdateDatabaseAfterDeletionOfFilesOnFileServer(ByUser)`). Re-issuing them unauthenticated to prove the
finding would itself write to QA with no credential.

Everything above was **recomputed from the source run**, not copied from
`docs/briefs/developer-loopholes.md`. Where the two disagree the pack states both and explains —
see `PLAN.md` §1. LH-05 is the live example: the pack measures **135** against its pinned run, while the
brief now quotes **348 of 1,388** from the newer one. Both are correct for their basis; cite the basis.

### Overlaps — cross-referenced, not restated

| Pair | Relationship |
|---|---|
| LH-01 ↔ LH-04 | LH-01 measured 104 codes inside its 289; LH-04 covers all **108** across every response |
| LH-01 ↔ LH-11 | LH-01 found 11 leaks inside its 289; LH-11 covers all **16** |
| LH-01 ↔ LH-02 | Both are "the status line does not reflect the outcome"; LH-02 is the `Success:true` half |
| LH-03 ↔ LH-04 | Shape 5 (`Success:false` envelope) is the carrier for the error codes |
| LH-08 ↔ LH-12 | Both are unbounded-query defects; **LH-08 is the fatal case of LH-12** |
| LH-06 ↔ LH-08 | The same 49-controller diagnostic scaffold (`GetLogs`/`GetStatus`/`SetStatus`) |
| LH-04 ↔ LH-10 | Validation errors surface as prose because no declarative rule exists to reference |
| LH-13 ↔ LH-01 | LH-13's bypass is delivered at HTTP 200, so status-code monitoring sees nothing — LH-01 is why it stayed invisible |
| LH-13 ↔ LH-09 | Same trust boundary: LH-09 returns credentials to an authenticated caller, LH-13 returns data to an unauthenticated one |
| LH-13 ↔ LH-10 | Authorization is undeclared for the same reason validation is — nothing is expressed declaratively on the controller |

Decide at triage whether LH-04 and LH-11 are separate tickets or sub-tasks of `PAMIT-42744` —
they were found inside its responses, and a developer fixing LH-01 will touch the same code.

---

## 3. Folder contract

Every `LH-NN-<slug>/` folder contains exactly this. Nothing else, so a reviewer opening any one
of them knows where to look.

| File | Required | What it is |
|---|---|---|
| `JIRA-TICKET.md` | ✅ | The ticket draft. Fenced blocks paste directly into Jira fields; prose outside them is guidance for whoever raises it |
| `EVIDENCE.md` | ✅ | Full write-up — the defect, measured scope, secondary findings, and the complete per-occurrence register |
| `EVIDENCE.xlsx` | ✅ | The same evidence as a filterable workbook, for developers who want to sort and slice |
| `data/<slug>-*.json` | ✅ | Machine-readable extract. The workbook and the markdown are both rendered from this, so the three cannot disagree |
| `data/revalidation-attempt.json` | when live re-check attempted | Outcome of the live replay, including a blocked attempt and why |

**MD and Excel are generated, never hand-edited.** Both come from one script, from one dataset.
Editing either by hand breaks that guarantee and the next rebuild silently discards the edit.
Fix the script instead.

### Required sections in `JIRA-TICKET.md`

The four the user asked for, plus the three that make a ticket survive triage:

1. **Field values** — project, type, severity, priority, component, environment, labels, attachments
2. **Summary** — the title, one line, in a fenced block
3. **Description** — in Jira wiki markup (`h2.`, `||` tables, `{code}`), fenced
4. **Steps to reproduce** — numbered, with a preconditions block; the first case should be the
   simplest that reproduces, ideally read-only and body-free
5. **Expected vs actual** — one short block, quotable in triage
6. **Severity justification** — a table, so the rating survives someone disagreeing with it
7. **Proposed fix + acceptance criteria** — including how QA will verify the fix

---

## 4. The generator

Every pack except LH-01 is produced by one command. Scripts live in `tools/` per the
workspace convention; the pack folders hold output only, and **nothing in them is hand-edited**.

```powershell
python tools\build_lh_pack.py --list          # the registry
python tools\build_lh_pack.py --lh 02         # one pack, zero HTTP
python tools\build_lh_pack.py --all           # LH-02…13, zero HTTP
$env:PAM_API_TOKEN = "<bearer>"
python tools\build_lh_pack.py --all --revalidate
```

| File | Role |
|---|---|
| `lh_common.py` | The engine — run loading, safety, replay, MD/XLSX writers, ticket writer |
| `lh_specs_run.py` | LH-02/03/04/05/09/11/12 — selected from run responses |
| `lh_specs_static.py` | LH-06/07/10 (catalogue and source) and LH-08 (incident) |
| `lh_specs_obj010.py` | **LH-13** — sources the OBJ-010 run via `run_id`, so the pinned run stays untouched |
| `build_lh_pack.py` | CLI and registry |
| `lh01_evidence.py` | LH-01's original bespoke script, kept as-is — its pack is attached to a live ticket and is **not** rebuilt by `--all` |

⚠️ **`--all` does not include LH-01.** It covers LH-02…13. LH-01's pack is attached to `PAMIT-42744` and is
left exactly as raised.

A spec may pin its own source run with `run_id`. Verified after LH-13 was added: rebuilding all packs
reproduces every previously published figure unchanged (LH-02 552/220, LH-03 1868/872, LH-04 297/284,
LH-05 135/135, LH-06 49/49, LH-07 147/147, LH-08 98/98, LH-09 23/21, LH-10 10/10, LH-11 16/16,
LH-12 25/13).

A loophole supplies only what is genuinely specific:

```
select(hop, response) -> bool      the selector
rows_static()         -> rows      alternative to select, when the pack builds its own rows
run_id                -> str       pin a different source run (LH-13); unset = the pinned run
classify(row)         -> class     the classification
TAXONOMY                           class -> (meaning, expected behaviour)
narrative(payload, md)             the prose
sheets(payload, xl)                the workbook
TICKET                             repro steps, severity argument, fix table, acceptance
replay_filter(row)    -> bool      ⛔ excludes rows whose replay would MUTATE data
reproduces(row, res)  -> bool      what "still reproduces" means for this finding
```

**`replay_filter` is not optional bookkeeping.** LH-02 selects 552 responses of which **28 are
successful inserts** — replaying those would create records on every re-validation. LH-09 has 7
of the same. Both specs filter them out, and the filter runs before anything is called.

---

## 5. ⛔ Safety rules when re-validating live

These are not optional and they are the reason LH-01's live re-check is currently blocked rather
than retried.

| Rule | Why |
|---|---|
| **One token per run, cached** | Repeated `/arcontoken` requests locked the `GenericScheduler` account (ISSUE-009). It is also the data-warehouse ETL service account, so a lockout reaches past testing |
| **Never retry a failed token request** | A lockout deepens. Stop and report |
| **Blocklist enforced at planning** | `GetLogs`, `GetErrorLogs`, `GetAllActiveUserDetails` hang 30 s and stop the IIS app pool (ISSUE-010). Never build them into a request |
| **Refuse destructive action names** | Deletion is `POST /api/<C>/Delete<Thing>`, not HTTP DELETE — verb guards do not work on this API. Guard on names |
| **Cap the replay** | LH-01 caps at 24 calls with a 1 s throttle. A re-check is a freshness probe, not a second full run |
| **Redact before writing** | Passwords and tokens are stripped before anything reaches disk |
| **Never replay a call that would mutate** | Use `replay_filter`. 35 rows across LH-02 and LH-09 are withheld for this reason |
| **Re-validation is never the basis of a claim** | Evidence comes from retained run data. A blocked re-check weakens freshness, not the finding |

### ⚠️ Replay fidelity

Evidence files are redacted at capture, so a replayed request body can carry `***REDACTED***`
where the original had a value. The redaction is deliberately over-broad — it also catches
booleans such as `AllowPasswordChange` and `Vault_Password_Immediately`, which then fail type
conversion server-side.

This is disclosed automatically: `EVIDENCE.md` §6 reports how many replayed requests carried a
redacted body. It is how LH-03's single non-reproducing call was correctly identified as a
harness artefact rather than a product change. **Never report such a call as "fixed".**

---

## 6. Token situation — use `PAM_API_TOKEN`, not `/arcontoken`

🔴 **The `GenericScheduler` API service account is locked.**

```
POST https://u16hf.arconnet.com:6302/arcontoken
-> HTTP 400 {"error":"Your account has been locked. Please contact your supervisor"}
```

Attempted 2026-07-31. One request issued, **no retry** — see §5. The host itself is up; an
unauthenticated probe returned HTTP 405 in 517 ms. `Environments/QA_MsSQL.properties` has not
changed since 2026-07-29 12:36, so no refreshed credentials have reached the workspace.

**The workaround, and the way to run every re-validation until this is resolved:** supply a
manually generated bearer token through the `PAM_API_TOKEN` environment variable.
`chain_runner.get_token()` checks that variable **first**, so `/arcontoken` is never called and
the locked account is never touched.

```powershell
$env:PAM_API_TOKEN = "<bearer token>"
python tools\lh01_evidence.py --revalidate --full
```

This is how LH-01 was re-validated on 2026-07-31: 289 of 289 calls replayed live, **100% still
reproduce**. A manually issued token lasts 24 h, so plan a re-validation pass to finish inside
that window.

⚠️ **Do not remove the guard.** `--revalidate` without `PAM_API_TOKEN` set will still attempt
`/arcontoken` once and fail cleanly against the locked account. That is intended behaviour —
it fails loudly rather than silently skipping the check.

---

## 7. Rebuilding

Zero HTTP calls; safe to run any time.

```powershell
python workbench\scriptsuild_lh_pack.py --all                # all twelve, zero HTTP
$env:PAM_API_TOKEN = "<bearer token>"
python workbench\scriptsuild_lh_pack.py --all --revalidate    # + live re-check

# LH-01 keeps its original script - its pack is attached to a live ticket
python tools\lh01_evidence.py --revalidate --full
```

`--full` is safe for LH-01 specifically because every one of those requests already *failed* —
they are rejected on validation or fault before touching state, so replaying reproduces the
rejection rather than mutating anything. **Confirm the same holds before assuming it elsewhere**;
for LH-02 and LH-09 it does not, which is why they carry a `replay_filter`.

Source run for all current packs: `artifacts/runs/2026-07-29_181439/` — 1,868 calls, one retained
evidence file each. That folder is never deleted, so every figure in every pack stays reproducible.
