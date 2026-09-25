# OBJ-007 — Shared agent brief

**Read this before starting.** It exists so each agent does not re-derive the same facts. Everything here
was measured this session unless marked *(prior)*.

---

## 1. Hard rules — these are safety controls, not preferences

| ⛔ Rule | Why |
|---|---|
| **Never call `GET /api/ActivityLogs/GetErrorLogs`, `GET /api/ActivityLogs/GetLogs`, `GetAllActiveUserDetails`** | Three sequential calls stopped the IIS app pool and took the whole API to `503` with no self-recovery. Enforce at *planning* time, before a request is built |
| **Never retry a failed token request** | The `GenericScheduler` account is locked. Retrying deepens the lockout, and it is also the data-warehouse ETL account |
| **Guard on endpoint *names*, not verbs** | Deletion is `POST /api/<Controller>/Delete<Thing>`. A destructive call looks like an ordinary POST |
| **Never replay a mutating call** | No re-execution of creates/updates/deletes captured in prior runs |
| **DB: read-only, `ARCOSDB_U16SP2_WEBSM_QA` only** | The `devops` login is **`sysadmin`** over 30 databases, several non-QA. `SELECT` only — no `INSERT`/`UPDATE`/`DELETE`/DDL, ever |
| **Write only inside `Automation gitlab repo/pam_automation_bootstrap/` on branch `AI`** | `pam/` is the developer's product repo — reference only, leave `git status` clean |
| **Never push, never commit** | Owner approves first. `AI` is local-only with no upstream |

## 2. The response envelope — no status-only assertions

Most PAM endpoints return **HTTP 200 with an application-level error in the body**. A rejected request is
usually a 200, not a 4xx. Any assertion that checks only `status == 200` passes against a fully rejected
request.

Five observed envelope shapes *(prior, measured 2026-07-29)* — no generated assertion may assume one:

| Shape | Seen on |
|---|---|
| `{Program, Version, DateTime, Success, Message, Result[]}` | most business endpoints |
| same, but **no `Message`** | `GetLOBList` |
| same, but `Result` is an **object** not an array | `GetServiceDetails` |
| **bare array, no envelope** | `GET /api/DeviceOnboarding/GetLOBList` |
| `Success:false` + `ErrorCode` + `ErrorMessage`, still **HTTP 200** | `GetLogDetails` (missing param) |

⛔ **`Success: true` is not evidence of a write.** `POST /api/ServiceCreation/SetServiceDetails` returns
`Success: true` with `Message: "Already Exists"` when nothing was inserted. A create assertion must read
**`Message` semantics**: `"Inserted Successfully"` = inserted, `"Already Exists"` = no-op.

`KNOWN_ERROR_CODES = {"201","202","203"}` in `ApiHelper` is **incomplete** — a live run captured
`ErrorCode: "206-LC_GLD"` on HTTP 200.

## 3. The evidence base

`Reports/Runs/2026-07-29_181439/results.json` — **the single source for every API-side figure.** Structure:

```
{ meta{...}, seed{...}, flows[326] }
flows[i]  = { id, title, verdict('PASS'|'FAIL'), note, vars{}, hops[] }
hops[j]   = { n, name, verb, path, extracted{}, checks[], status, latency_ms,
              body_bytes, error, content_type, ... }
checks[k] = { layer('L1'..'L7'), check, verdict('PASS'|'FAIL'), detail }
```

326 flows · **1,873 hops** · 1,868 HTTP calls · 11,503 s elapsed. Flow verdicts: 30 PASS / 296 FAIL.

**Check tallies measured this session — quote these, do not re-count differently:**

| Layer | Check | PASS | FAIL |
|---|---|---:|---:|
| L1 | `http-status` | 1,688 | 180 |
| L2 | `content-type` | 1,864 | 4 |
| L3 | `envelope` | 1,278 | 590 |
| L4 | `message-semantics` | 1,410 | 458 |
| L5 | `chain-key-extracted` | 982 | **196** |
| L6 | `record-exists` | **2** | **105** |
| L7 | `latency` | 1,855 | 13 |

All **196** L5 failures carry the identical detail string `resolved []; MISSING ['NEW_ID']`. L6 ran on only
107 hops and passed **2**.

Also available: `checkpoint.json`, and `evidence/` with **1,868 per-call files**.

## 4. Facts established this session

| Fact | Detail |
|---|---|
| **QA DB is `ARCOSDB_U16SP2_WEBSM_QA`** | `10.10.0.194,1433`, SQL Server 2019 CU32 (15.0.4455.2) on **Linux/Ubuntu 20.04**, Developer Edition. Owner-confirmed |
| **`devops` is `sysadmin` + `dbcreator`** | Full destructive authority over all 30 databases. Read-only discipline is mandatory |
| **LOB names are encrypted at rest** | `sso_lobs.sls_name` holds base64 AES ciphertext, e.g. `ff/5iyC63//aqUrPI13Zkw==`. Matching a created object by plaintext name **cannot work** |
| **`tblLOBDetail` is empty in every database** | 0 rows — the ADbridging LOB table the API reads/writes |
| **No DB row newer than 2025-10-01** | Yet the API run was 2026-07-29 — reconcile before asserting persistence |
| **`Environments/QA_MsSQL.properties` ships `db_*` blank** | `db_host_name`, `db_port`, `db_name`, `db_user_name`, `db_password`, `db_type` all empty. This is why no DB assertion has ever run |
| **`AutoConfigs.db_type` is hardcoded `"mysql"`** | `AutoConfigs.java:140` — a literal, not read from properties |
| **`DBUtils` has zero callers** | Nothing in the framework performs any DB validation. It only `System.out.println`s — it returns no data an assertion could use |
| **`DBUtils` was migrated to SQL Server upstream** | Now `jdbc:sqlserver://...;encrypt=true;trustServerCertificate=true`. `mssql-jdbc 12.8.0.jre11` **and** `mysql-connector-j 9.0.0` are both in `pom.xml` |
| **The committed `ApiToken` is expired** | `Environments/QA_MsSQL.properties` carries a hardcoded JWT with `exp` = **2026-07-31 10:39 UTC** — dead |
| **`/arcontoken` is locked** | HTTP 400 `"Your account has been locked..."`. Owner supplies a token via `$env:PAM_API_TOKEN` |

## 5. Prior measured figures — reuse, do not re-derive

| Figure | Value |
|---|---|
| Endpoints in `APIConfig.java` | **1,306** (`1,336` / `1,322` are stale — do not quote) |
| Verb split | `GET` + `POST` = **99.7%** of the surface |
| Endpoints exercised 2026-07-29 | **870** of 1,306 |
| Endpoints present in `pam/PAM` | **48** of 1,306 = **3.7%** |
| Create endpoints | **217**, of which only **13** can be driven — nothing supplied has a valid request body |
| `[Required]` properties | **3** of **~6,738**. No length, format or pattern validation anywhere |
| Confluence payload export | 3,194 JSON examples, **1,654** endpoint-bound, binding by **page proximity** (so some bindings are wrong). 70% of endpoints undocumented, 4 error codes, 1 of 9 response shapes |
| Admin guides | 1,101 pp — access model and concepts only, **no endpoints, schemas or error codes** |

## 6. Where things live

| Need | Path |
|---|---|
| Endpoint catalogue | `Automation gitlab repo/pam_automation_bootstrap/src/test/java/com/arcon/autoconfigs/APIConfig.java` |
| Merged source map | `workbench/scripts/source-map.json` (1.7 MB) + `SOURCE-MAP.md` |
| Run evidence | `Reports/Runs/2026-07-29_181439/` |
| Product docs (**never read the corpus directly**) | `python workbench\rag\query.py find "<terms>"` · `page <doc> <N>`; cite `<doc>:p<N>` |
| The findings — **13** as of `OBJ-010` | `workbench/developer-loopholes.md` (source of truth, states its own count) → packaged in `Developer-Loopholes/LH-NN-*/` |
| Documentation gap *(prior)* | `workbench/document-gap.md` |
| Data sufficiency *(prior)* | `docs/gaps/01-Data-Gap-Analysis.md`, `02-Data-Access-Requests.md` |
| Existing defect write-ups | `Reports/Issues/` (11 files) |

## 7. Output contract — follow exactly

| Rule | Detail |
|---|---|
| **Deliverables go in `document/` only** | `document/data/*.json` (structured), `document/reports/*.md` (prose), `document/workbooks/*.xlsx` (built centrally — do **not** write .xlsx yourself) |
| **Generator scripts go in `workbench/scripts/`** | Standing workspace rule: every harness script lives there. Only their *output* lands in `document/` |
| **Emit JSON, not Excel** | Write `document/data/<your-area>.json` as a list of row objects with stable snake_case keys. The workbook build reads these. One agent writing .xlsx would break consolidation |
| **Never invent a measurement** | If a value is not in the evidence, write `NOT EXECUTED — no evidence` or `UNKNOWN`, never a plausible guess. Every number must be traceable to a file |
| **Cite** | Reports cite `results.json` flow/hop ids, `<doc>:p<N>` for product docs, `file.java:line` for code |
| **No dates in narrative** | Filesystem paths are exempt — `Reports/Runs/2026-07-29_181439/` is an identifier, cite it exactly |

House style for markdown: `# Subject — Purpose`, a bold `**Key:** value` block, `---`, then numbered
`## N.` sections. Tables over prose. Status as `✅ 🟡 ⬜ ⛔ ⚠️` in cells, never checkboxes.
