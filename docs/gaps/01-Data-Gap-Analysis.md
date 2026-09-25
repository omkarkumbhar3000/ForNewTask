# Data Gap Analysis — what we have, and what it cannot answer

**Purpose:** an overview of every data source supplied to the QA automation effort, what each one
actually covers when measured, and where the gaps fall against the three areas under review.
**Companion file:** `02-Data-Access-Requests.md` — what to provide to close these gaps.
**Basis:** **5,416 live API calls** (2026-08-05, `QA_MsSQL`, `OBJ-010`) plus 1,868 (2026-07-29) · static
analysis of 6,866 `.cs` files · the 1,306-endpoint catalogue · the existing negative-test workbook (§2 — row total is definition-dependent)
test data.
**Every figure below is measured.** Where a figure disagrees with an earlier document, this file
states both.
**Last updated:** 2026-08-05

---

## 0. The one-paragraph answer

We have **more than enough** to test reads and **structurally cannot** test writes. 870 of 1,306
endpoints were exercised in a single run, but only **13 of 217 create endpoints** can be driven
successfully — because the information needed to build a valid request body exists nowhere we
have been given. That single gap cascades: a create that fails returns no identifier, so a chain
cannot proceed past its first hop, so a write cannot be verified as persisted. **All three areas
under review bottleneck on the same root cause.**

---

## 1. What we have been given

| # | Source | Size | What it genuinely provides | What it does **not** |
|---:|---|---|---|---|
| 1 | **`pam/PAM`** — developer repo | 181 `.csproj`, 6,866 `.cs` | C# property names and types (2,674 mapped); prevailing code patterns | **The API under test.** Only **48 of 1,306** catalogue endpoints (3.7%) are implemented here; **58 of 70** controllers have no implementation. No Swagger, no route attributes in Framework projects |
| 2 | **`PAM API (Internal Team).pdf`** — Confluence export | 2,470 pages | **3,194 JSON payload examples**, **1,605** bound to an endpoint (this said 1,654 — see the note below). The single best asset we have | 914 of 1,306 endpoints (**70%**) undocumented; **3** error codes (this said 4 — two of them were IP-address fragments, not codes); **6** of the **31** measured response shapes; no status-code semantics |
| 3 | **Swagger specs** | 37 specs, 690 operations | The only surface with real response schemas | A **different API** — ~6% name overlap with the catalogue. **0 of 690** declare any 4xx or 5xx |
| 4 | **PAM Administrative Guide** | 702 pages | Access model, module taxonomy, product concepts | No endpoints, no schemas, no error codes |

⚠️ **Two live measurements of "payloads bound to an endpoint", and they disagree.**
`tools/build_source_map.py` reports **1,654 bound / 1,540 orphaned**;
`docs/analysis/A7-documentation-gap-analysis.md` §1 reports **1,605 bound / 1,589 orphaned / 440
unparseable**. Both partitions sum to 3,194, so this is a **methodology difference in where the line falls**,
not an arithmetic error — A7 separates unparseable examples that the generator counts as bound. Quote either
**with its basis attached**; do not quote a bare number. Reconciling the two definitions is unfinished work.
| 5 | **Client Manager Guide** | 399 pages | Client-side behaviour and configuration | Same — administrator documentation, not an API contract |
| 6 | **`APIConfig.java`** — test catalogue | 1,306 endpoints | Controller · action · verb · path for the surface we target | Not authoritative — **348 of the 1,388 endpoints exercised return 404** (25.1%) on the deployed build; 135 on the narrower N-1 run |
| 7 | **Payload helpers** | 66 files, 1,289 methods | Request bodies for 111 of 217 creates (51%) | Static literals with hardcoded foreign keys; most fail validation |
| 8 | **`QA_MsSQL` environment** | live | The only place behaviour can be observed | Shared, unversioned, unknown data state; **DB credentials blank** |
| 9 | **Run evidence** | **5,424** files (plus 1,868 from N-1) | Observed behaviour — the only source of truth we actually trust | Describes what happened, not what *should* happen |

### The pattern

Sources 1–5 were provided to answer *"what is the API and how does it behave?"* Measured against
that question:

| Question | Answered by | Coverage |
|---|---|---|
| What endpoints exist? | catalogue (7) | ⚠️ **348 of 1,388 exercised are wrong** |
| What does a request body look like? | Confluence (2) + helpers (7) | 🟡 63% of creates, partially |
| **Which fields are mandatory?** | **nothing** | ⛔ **0%** |
| What does a success response look like? | observation (9) | 🟡 9 shapes, undocumented |
| What does a failure look like? | observation (9) | ⛔ 4 of 108 codes documented |
| Which HTTP status means what? | **nothing** | ⛔ **0%** |
| Did a write actually persist? | **nothing** | ⛔ **0%** |

**The four ⛔ rows are the gap.** Everything else is workable.

---

## 2. Area 1 — Negative testing

### What already exists (and is worth knowing)

This is more built out than it may appear:

| Asset | Scale |
|---|---|
| Negative suite XMLs | 5 — `MethodNotAllowed`, `UnauthorizedAccess`, `InvalidDataType`, `InvalidValue`, `MissingParameter` |
| Test classes per suite | 75–78 |
| `Negative_API_Automation_Test_Input_Data.xls` | 76 sheets. **Row total is definition-dependent — see the note below** |

⚠️ **Do not quote a bare row total for this workbook.** Five figures are in circulation and none is simply
wrong: **3,167** (data rows excluding header blocks) · **3,317** (3,167 + 150 headers) · **3,652** (a third
parse) · **3,728** (sum of `sheet.nrows`) · **3,620** (non-blank). The spread comes entirely from whether
blank rows, repeated header blocks and trailing rows are counted, and no two analyses used the same rule.

**What is stable under every rule, and what you should quote instead:** the split is **1,604 × 405** ·
**1,550 × 401** · **13 × 200**, and only those **13 rows** target the application's own validation rather
than IIS or the auth middleware. The conclusion — that ~95% of this corpus tests the transport layer — holds
regardless. Fixing this means agreeing one definition *in the counting script*, not in prose.
| Framework support | `validateApiResponseWithResponseTime_ExcelBasedsettingnegative(...)` with an `ExpectedErrorCode` parameter, already plumbed through |

### ⛔ The problem: 95% of it tests the plumbing, not the application

| `ExpectedStatus` | Rows | What it actually exercises |
|---|---:|---|
| `405` | **1,604** | The web framework rejecting a verb — never reaches application code |
| `401` | **1,550** | The auth layer — never reaches application code |
| `200` | **13** | The application's own validation |
| **`ExpectedErrorCode` populated** | **0** | — |

So **3,154 rows — about 95% of the corpus** — confirm that IIS and the auth middleware work. Only **13 rows**
test whether the application correctly rejects bad input, and **not one row asserts an error
code**.

This matters specifically because of how PAM signals failure. A rejected request returns **HTTP
200 with an `errorCode` in the body** (LH-01, 289 confirmed instances). A negative test that
asserts only `ExpectedStatus = 200` therefore **passes whether the request was correctly rejected
or wrongly accepted**. It cannot tell the difference.

### Why the expectations cannot currently be derived

To assert "this bad request must be rejected *this way*", we need a declared expectation. There
isn't one:

| Would-be source | Reality |
|---|---|
| Swagger error responses | **0 of 690** operations declare any 4xx or 5xx |
| Confluence error-code register | **4** codes documented; **108** observed live |
| C# validation attributes | **3** `[Required]` across 6,738 properties; zero length/format constraints |
| HTTP status semantics | Undefined — a rejection is a 200 |

**Consequence:** every negative expectation today would have to be *observed first and then
frozen* — a differential baseline, not a specification. That is a legitimate technique, and it is
what we should do in the interim, but it locks in current behaviour as correct, including the
defects. It cannot catch "this should have been rejected and wasn't."

---

## 3. Area 2 — Is the current QA dataset sufficient?

**No — and the shortfall is measurable rather than a matter of opinion.**

### 3.1 Writes essentially do not work

| Measure | Value |
|---|---:|
| Create endpoints in the catalogue | 217 |
| …with a request body available from any source | 138 (63%) |
| …**that successfully insert a record** | **13 (6%)** |
| …with no request body derivable anywhere | **79** |

⚠️ **The last row read `101` and was wrong** — 138 + 101 = 239, which exceeds the 217 total. Recomputed from
`source-map.json`: **138** creates have fields from at least one source and **79** have none. The same `101`
is repeated in `docs/briefs/document-gap.md` §5. Corrected under `OBJ-007`; see
`docs/analysis/A6-developer-repo-analysis.md`.

The failures are almost entirely *missing mandatory field* and *wrong type* —
`Validation error occurred - Port is Mandatory`, `Could not convert string to integer`. Those
requirements exist **only in server-side procedural code**. When two payloads were corrected by
hand after reading the error text, both inserted successfully the same day on the same
environment. **This is a metadata problem, not a tooling problem.**

### 3.2 The cascade — one root cause, three symptoms

Measured across the run's seven validation layers:

| Layer | Pass | Fail | What the failure means |
|---|---:|---:|---|
| L5 `chain-key-extracted` | 982 | **196** | **All 196 identical:** `resolved []; MISSING ['NEW_ID']` |
| L6 `record-exists` | **2** | **105** | 97 are `created record id='${NEW_ID}' -> NOT FOUND` |

Read those together and the causal chain is unambiguous:

```
create fails (no mandatory-field metadata)
   → no identifier is returned          → L5 fails, 196 times
      → the chain cannot proceed         → depth stays at 1
         → nothing exists to read back   → L6 fails, 105 times
            → persistence is unverified  → 2 confirmed writes out of 107 attempts
```

**Only 2 writes in the entire run were proven to have persisted.** Not because the product
failed — because we could not create the record in the first place.

### 3.3 The environment's own seed data is stale and unverifiable

| Configured in `QA_MsSQL.properties` | Actually found at runtime |
|---|---|
| `LOBId = 24` | `LobId 108` (`AUTOMATION_TEST_LOB`) |
| `serverGroupId = 220` | `ServerGroupId 282` |

The harness discovers these at runtime rather than trusting configuration, which works — but it
means **no test has a known starting state**. The environment is shared, its data changes without
notice, and we have no way to assert a precondition or restore one.

### 3.4 DB access is configured for, but not provisioned

```properties
db_host_name =        # empty
db_port      =        # empty
db_name      =        # empty
db_user_name =        # empty
db_type      =        # empty
```

`DBUtils.java` exists and is wired to `AutoConfigs`, so the intent was clearly there. Two things
would need attention if credentials arrive:

1. **It is blank for every environment we use.** No DB verification has ever run.
2. ⚠️ **`DBUtils.getConnection()` hardcodes `jdbc:mysql://` and loads
   `com.mysql.cj.jdbc.Driver`** — even inside the branch labelled `mssql`. Against `QA_MsSQL`
   (SQL Server) it would fail on connect. This is a latent defect in our own framework and is
   ours to fix, not the developers'.

---

## 4. Area 3 — Payload chaining

### Current state

| Measure | Value |
|---|---:|
| Chain candidates derived from field-name matching | 1,680 |
| …**observed** (producer response actually seen) | **0** — all name-inferred |
| Flows executed in the last run | 326 |
| Chains that reached depth ≥ 2 | limited by L5 above |
| Deepest chain proven end to end | **5 hops** |

The 5-hop chain works and is the proof the approach is sound:

```
GetLOBList          → LobId 108
GetServerGroupList  → ServerGroupId 282
SetServiceDetails   → ServiceId 25339   "Inserted Successfully"
GetServiceDetails   → ServiceSessionId 75277
GetActiveServicesByLOBId → ServiceId 25339 FOUND
```

Not one of those five values is hardcoded. **The mechanism is not the problem.**

### What blocks it from scaling

| Blocker | Evidence | Nature |
|---|---|---|
| Creates fail, so no id is produced | 196 × `MISSING ['NEW_ID']` | **Data/metadata** |
| Candidates are name-inferred, not observed | 0 of 1,680 observed | Resolvable by running more creates |
| Field naming is inconsistent | `ServiceId` in **7** spellings | Compensated by case-insensitive matching |
| Ids change type between operations | string on create, int on read | Compensated by explicit casts |
| No known starting state | seed config stale (§3.3) | **Data/access** |
| Teardown not bound to created records | 5 steps excluded from the run | Safety — cannot delete what we cannot identify |

Two of these are ours to absorb and already are. The two marked **Data/access** are not.

---

## 5. Adequacy verdict per source

Directly answering *"is the developer repo and the conference document enough?"*

| Source | Verdict | Reasoning |
|---|---|---|
| **`pam/PAM` developer repo** | ⛔ **Not adequate for its intended purpose** | It was provided so we could derive the API surface. It contains **3.7%** of it. The real API is served by separate microservices behind `ARCONAPIGateway`, which are not in this snapshot. Still valuable for C# type names — keep it, but stop treating it as the contract |
| **Confluence API export (2,470 pp)** | 🟡 **Partially adequate — and the best asset available** | Its 3,194 payload examples are exactly what we need for the create problem. Its weakness is everything needed to determine *success*: **3** error codes, **6 of 31** response shapes, no status semantics. Detail: `docs/briefs/document-gap.md` |
| **Swagger specs (37 / 690 ops)** | 🟡 **Adequate for a surface we are not testing** | Real schemas, but ~6% name overlap with the catalogue. Worth running as its own programme; does not help the legacy surface |
| **Admin + Client Manager guides (1,101 pp)** | ✅ **Adequate for what they are** | Administrator documentation. Correctly used for the access model and module taxonomy. Never expected to contain API detail |
| **`QA_MsSQL` environment** | 🟡 **Adequate for reads, not for writes** | Reachable and stable enough for 1,868 calls. Shared, no known state, no DB access, and the service account is currently locked |
| **Existing negative test data** | 🟡 **Adequate in volume, misdirected in aim** | ~3,200–3,700 rows depending on the counting rule (§2 note), **95% of which test IIS and auth rather than the application**. Only 13 rows target application validation |

---

## 6. What is **not** a gap

Stated so the asks in `02-Data-Access-Requests.md` stay narrow and credible:

- **Read coverage.** **1,388 endpoints across 122 of 122 modules** in one run, with zero per-endpoint
  test code. This works.
- **The chaining mechanism.** Proven to 5 hops with no hardcoded values.
- **The validation approach.** Seven layers caught 406 body-level failures a status-only suite
  scored as passing.
- **Execution reliability.** Survived three environment outages by pausing and resuming; one
  token for 5,416 calls — zero `/arcontoken` requests, even across a resume; every run retained and diffable.
- **Evidence discipline.** One redacted JSON file per call, **5,424** of them, all retained.

We are not asking for tooling. We are asking for **information the product already has and has
not published**, and for **access to verify what we cannot currently see**.

---

## 7. Where the detail lives

| Topic | Document |
|---|---|
| Confluence documentation gaps, all 8 | `docs/briefs/document-gap.md` |
| The 12 developer findings, with evidence packs | `docs/findings/README.md` |
| Missing validation metadata — the create blocker | `artifacts/loopholes/LH-10-no-validation-attributes-on-models/` |
| Error-code register — the negative-testing blocker | `artifacts/loopholes/LH-04-error-code-register-incomplete/` |
| Catalogue vs deployment drift | `artifacts/loopholes/LH-05-declared-endpoints-return-404/` |
| Full run results | `docs/management/summary/Full-Generated-Run-2026-07-29.md` |
| Merged 4-source field map | `tools/SOURCE-MAP.md` |
| Backlog and open questions | `docs/history/README.md` §6 (the retired backlog, archived in full) |
