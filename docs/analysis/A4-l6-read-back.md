# A4 — Level-6 read-back: why 2 of 107 passed

**Scope:** OBJ-007 item A4 · **Evidence:** `artifacts/runs/2026-07-29_181439/results.json` + its 1,868
`evidence/*.json` captures · **Generator:** `tools/obj007_chain_analysis.py`
**Data emitted:** `artifacts/analysis-data/l6-read-back.json` (107 rows, one per `record-exists` check)
**HTTP requests issued by this analysis:** 0 · **DB access:** none

---

## 0. The finding in one line

Of the 107 `record-exists` checks, **97 could not have passed under any circumstances** — they searched the
read-back response for the literal string `${NEW_ID}`, because the create hop published no id and
`substitute()` left the placeholder token in place. Those 97 verdicts carry **no information about
persistence**. Only **10** checks searched for a real value, and of those 2 passed.

| Root cause | Checks | Does the verdict say anything about persistence? |
|---|---:|---|
| ⛔ **Unresolved placeholder** — searched for the literal `${NEW_ID}` | **97** | **No.** Structurally impossible to pass |
| ⚠️ **Read-back endpoint rejected the request** — the store was never queried | **4** | No. The FAIL is about the read endpoint |
| 🟡 **Zero records returned** — the object is not listed by this endpoint | **2** | Partly — see §5 |
| ⚠️ **Harness false negative** — existence confirmed in `Message`, not in a payload | **2** | Yes, and it was **positive** — recorded as FAIL anyway |
| ✅ **Verified** — the created record was found | **2** | Yes |
| Total | **107** | |

**Corrected pass rate.** Judged only on the checks that were capable of returning an answer, the read-back
layer ran on **10** hops: 2 verified, 2 falsely failed (existence was in fact confirmed), 4 never queried the
store, 2 genuinely returned nothing. Quoting "2 of 107 = 1.9 %" describes the harness, not the product.

---

## 1. Where the 107 came from

The generator attaches a read-back to every lifecycle flow whose entity it can name
(`generate_flows.py:259-270`). **218 of the 326 flows planned one. Only 107 ran.**

| Outcome | Flows | Cause |
|---|---:|---|
| Read-back executed → an L6 verdict exists | **107** | reached its hop |
| Never ran — the create hop failed **L5** (no id) and `stop_on_fail` truncated the flow | **98** | the A1 cascade |
| Never ran — the create hop failed **L4** (message semantics) while L5 passed | **9** | create rejected, id still extractable |
| Never ran — hop 1 `GetLOBList` breached its 8,000 ms **L7** SLA | **4** | the prelude died before the create |
| **Total planned** | **218** | |

Of the 107 that ran, **106 were hop 5** and **1 was hop 4** (`user_lifecycle`, a hand-written flow with a
two-hop prelude rather than three).

⛔ **The 97 unresolved-placeholder checks are not a random subset — they are exactly the tier-3 population.**
A create for which the framework holds a payload literal is emitted with `stop_on_fail: True`
(`generate_flows.py:253`), so its L5 failure ends the flow and no read-back runs. A create for which **no
request body exists anywhere in the framework** is probed with `{}` and emitted with `stop_on_fail: False`
(`generate_flows.py:236-243`), so the flow runs on. The correlation is 1:1 and exact: all **99** tier-1 L5
failures stopped at the create; all **97** tier-3 L5 failures continued into a read-back that could not
work. Upstream cause for those 97: **48** cause-(a) rejections, **48** cause-(d) unknowns, **1** cause-(b)
acknowledged insert.

---

## 2. The two assertion mechanisms — and why only one of them works

The runner supports two forms of the record-exists check, and they behave very differently.

**Form 1 — `verify_present`, used by the two hand-written flows.** The field name is pinned, so the search is
exact (`chain_runner.py:621-627`, asserted at `chain_runner.py:460-464`):

```python
if hop.get("verify_present") and doc is not None:                    # chain_runner.py:621
    v = hop["verify_present"]
    wanted = substitute(v["value"], vars)
    hit = find_in(doc, v.get("in", ""), v["match_field"], wanted)    # chain_runner.py:625
    res["_found"] = hit is not None
```

**Form 2 — `verify_value_anywhere`, used by all 216 generated flows.** The field name is unknown, so it deep
searches for the *value* (`chain_runner.py:629-637`, asserted at `chain_runner.py:465-468`):

```python
if hop.get("verify_value_anywhere") and doc is not None:             # chain_runner.py:630
    v = hop["verify_value_anywhere"]
    wanted = substitute(v["value"], vars)                            # chain_runner.py:632
    hit = value_anywhere(doc, wanted)                                # chain_runner.py:633
    res["_found"] = hit is not None
```

And `value_anywhere` guards only against the empty and the string `"none"`
(`chain_runner.py:522-535`):

```python
def value_anywhere(doc, value) -> dict | None:
    want = str(value).strip().casefold()
    if want in ("", "none"):                                         # chain_runner.py:529
        return None
    for node in walk_dicts(doc):                                     # chain_runner.py:531
        for k, v in node.items():
            if isinstance(v, (str, int, float)) and str(v).strip().casefold() == want:
                return {"matched_field": k, "record": node}
    return None
```

⛔ **The defect is the interaction of three lines.** `store()` refuses to publish a `None`
(`chain_runner.py:585-587`), so `NEW_ID` never enters `vars`. `substitute()` then returns the placeholder
**unchanged** when the variable is absent (`chain_runner.py:200`):

```python
m = PLACEHOLDER.fullmatch(node)
if m:
    return vars.get(m.group(1), node)          # chain_runner.py:200 — falls back to the token
```

So `wanted` becomes the seven-character string `"${NEW_ID}"`. That is neither `""` nor `"none"`, so the
guard at `chain_runner.py:529` lets it through, and `value_anywhere` searches the response for a literal
`${NEW_ID}`. No PAM response will ever contain it. **97 of the 107 checks are that case** — visible directly
in the recorded detail strings:

```
created record id='${NEW_ID}' -> NOT FOUND        × 97
```

---

## 3. Why only 2 passed — the two that did

Both passes are **hand-written** flows using **Form 1** with a **pinned** extraction selector on the create
hop. Neither relied on `any_id()` guessing.

| Flow | Create hop | Id published | Read-back | Result |
|---|---|---|---|---|
| `user_lifecycle` | hop 3 `SetUserDetails` → HTTP 200, `Success:true`, `Message:"Inserted Successfully"` | `NEW_USER_ID = 1457` via `extract: {"NEW_USER_ID": "Result[0].UserId"}` | hop 4 `GET /api/UserDetails/GetAllActiveUserList` → `Success:true`, `"1568 Records Found"`, `Result[1568]`; asserted with `verify_present: {in: Result, match_field: UserId, value: ${NEW_USER_ID}}` | ✅ `searched Result for UserId=1457 -> found` |
| `service_lifecycle` | hop 3 `SetServiceDetails` → HTTP 200, `Success:true`, `Message:"Inserted Successfully"` | `NEW_SERVICE_ID = 25342` via `extract: {"NEW_SERVICE_ID": "Result[0].ServiceId"}` | hop 5 `POST /api/ServiceDetails/GetActiveServicesByLOBId` → `Success:true`, `"17 - Records Found"`, `Result[17]`; asserted with `verify_present: {in: Result, match_field: ServiceId, value: ${NEW_SERVICE_ID}}` | ✅ `searched Result for ServiceId=25342 -> found` |

These are also the only two flows in the whole run that achieved a genuine multi-hop chain — a value created
by this run carried into a later call and then verified. `service_lifecycle` chains three deep:
`SetServiceDetails` → `GetServiceDetails` (consuming `NEW_SERVICE_ID`, publishing `SERVICE_SESSION_ID=75293`)
→ `GetActiveServicesByLOBId`.

**What they had in common — and what the 216 generated flows lacked:**

| Property | The 2 that passed | The 105 that failed |
|---|---|---|
| Id extraction | pinned selector (`extract: {NEW_USER_ID: "Result[0].UserId"}`) | `extract_any_id` → `any_id()` guessing on `/id$/` |
| Read-back selection | chosen by hand, known to list the entity | `pick_readback()` scored on the endpoint **name** (`generate_flows.py:187-211`) |
| Read-back request body | correct for the endpoint | `payloads.get(action) or {}` (`generate_flows.py:266`) — often `{}` |
| Match | field name pinned (`match_field: UserId`) | value-anywhere deep search |

---

## 4. The 10 checks that actually searched for a real value

These are the only rows where "created but not readable back" is even testable.

| Flow | Create hop → what it returned | Searched for | Read-back response | Root cause |
|---|---|---|---|---|
| `user_lifecycle` | `SetUserDetails` → `NEW_USER_ID=1457` | `UserId=1457` | `Result[1568]` | ✅ **VERIFIED** |
| `service_lifecycle` | `SetServiceDetails` → `NEW_SERVICE_ID=25342` | `ServiceId=25342` | `Result[17]` | ✅ **VERIFIED** |
| `adbridging__addserverinformationaddomain` | `AddServerInformationAdDomain` → `Success:true`, `"Record Added successfully."`, `NEW_ID=53` from `ServerDetailID` | `53` | `GET /api/ADbridging/GetServerList` → `Success:false`, `103-ADB-SGL`, `"Input parameter is null"` | ⚠️ read-back rejected |
| `adbridgingv2__addserverinformationaddomain` | identical | `53` | identical | ⚠️ read-back rejected |
| `adbridging__insertaddomain` | `InsertAdDomain` → `Success:true`, `"Record Inserted successfully."`, `NEW_ID=0` from `DomainId` | `0` | same `103-ADB-SGL` rejection | ⚠️ read-back rejected |
| `adbridgingv2__insertaddomain` | identical | `0` | identical | ⚠️ read-back rejected |
| `adbridging__insertuserdetails` | `InsertUserDetails` → `Success:true`, `"Record Inserted successfully."`, `NEW_ID='auto40pc47@test.local'` from `EmailID` | `'auto40pc47@test.local'` | `POST /api/ADbridging/GetAllADUserDetails` → `Success:true`, `"No Record Found"`, `Result[0]` | 🟡 zero records |
| `adbridgingv2__insertuserdetails` | identical | same | identical | 🟡 zero records |
| `adbridging__saveuserrolemappingdetails` | `SaveUserRoleMappingDetails` → `Success:true`, `"Record Inserted successfully."`, `NEW_ID=10` from `RuleID` | `10` | `POST /api/ADbridging/validateUserRoleMappingDetails` → `Success:true`, **`"Record Already Exists."`**, no `Result` | ⚠️ **harness false negative** |
| `adbridgingv2__saveuserrolemappingdetails` | same, `NEW_ID=11` | `11` | identical | ⚠️ **harness false negative** |

Three findings sit inside that table, and none of them is "the record was not persisted":

- ⛔ **Two of the four "ids" are not ids.** `NEW_ID='auto40pc47@test.local'` came from the field `EmailID` —
  `ID_FIELD = re.compile(r"id$", re.I)` (`chain_runner.py:502`) matches `EmailID`, so `any_id()` took an
  email address as the record key. And `NEW_ID=0` from `DomainId` is a create acknowledging an insert while
  returning key `0`.
- ⛔ **`NEW_ID=53` is a request echo, not a generated key.** The request body for
  `AddServerInformationAdDomain` already carried `"ServerDetailID": "53"` (from the stale payload literal),
  and the response echoed it back. Chaining on it proves nothing about what was written.
- ⚠️ **The two `"Record Already Exists."` rows are the harness reporting a FAIL against positive
  evidence.** The read-back explicitly confirms the record is present; it just returns no record body, so
  `value_anywhere()` had nothing to match. `RuleID` also incremented `10 → 11` between the two flows, which
  is consistent with two real inserts.

---

## 5. "Never created" vs "created but not readable back"

This is the question A4 exists to answer, so the answer is given per population rather than in aggregate.

| Population | Checks | Can the evidence separate the two? |
|---|---:|---|
| Unresolved placeholder (`${NEW_ID}`) | **97** | ⛔ **No — and not even in principle.** The read-back never looked for the object. Measured against the upstream create: **48** were rejected outright (A1 cause a), so probably nothing exists; **48** returned no determinate outcome at all (A1 cause d), so nothing is known; **1** claimed an insert (A1 cause b). The L6 verdict adds nothing to any of the three |
| Read-back endpoint rejected the request | **4** | ⛔ **No.** `GetServerList` answered `103-ADB-SGL "Input parameter is null"` — the store was never interrogated. The create said `"Record Added successfully."` / `"Record Inserted successfully."`, so this is an untested claim, not a refuted one |
| Zero records returned | **2** | 🟡 **Partly.** The read-back succeeded and returned `Result[0]` with `"No Record Found"`, so the object is **not visible through `GetAllADUserDetails`**. Whether it was never written, or written to a store this endpoint does not read, cannot be told from the API alone |
| Existence confirmed in `Message` | **2** | ✅ **Yes — and it says created.** `"Record Already Exists."` is a positive existence statement from the product |
| Verified | **2** | ✅ **Yes — created and readable back** |

### 5.1 Stated plainly

**For 101 of the 107 checks (97 + 4), the run cannot distinguish "never created" from "created but not
readable back", and no amount of re-reading `results.json` will change that** — the distinguishing
observation was never made. The read-back either searched for a placeholder token or hit an endpoint that
rejected the request.

That is not a gap in the evidence base. It is a **design gap in the assertion**: a record-exists check whose
input is unresolved must report `NOT VERIFIABLE`, not `FAIL`. As recorded, 97 rows of a 107-row report look
like persistence failures and are not evidence of anything.

### 5.2 What would settle it

| To settle | Requirement |
|---|---|
| The 19 cause-(b) creates that claimed `"Record Inserted successfully."` — only **1** of which even reached a read-back | ⛔ **Product change first:** the create must return the primary key. Until then, a read-only `SELECT` on `ARCOSDB_U16SP2_WEBSM_QA` matched on the submitted business fields (server IPs, domain name, file-server path) is the only route |
| The 4 rejected read-backs | The correct request body for `GetServerList` — the generator supplied `{}` because it had no payload literal for it (`generate_flows.py:266`) |
| The 2 zero-record read-backs | Confirmation from the API owner that `GetAllADUserDetails` is the endpoint that lists what `ADbridging/InsertUserDetails` writes. If it is, this is a persistence defect worth raising |
| Any claim that a write persisted at all | A read-only `SELECT`. Two prior findings make this mandatory rather than optional: `sso_lobs.sls_name` holds **base64 AES ciphertext**, so matching a created object by plaintext name cannot work; and **no row in any database is newer than 2025-10-01** while this run executed under `artifacts/runs/2026-07-29_181439/` — that contradiction must be resolved before any persistence claim is made in either direction |
| Whether the framework could ever assert this today | Already answered and it cannot: `Environments/QA_MsSQL.properties` ships every `db_*` key blank, `AutoConfigs.db_type` is the hardcoded literal `"mysql"` (`AutoConfigs.java:140`), and `DBUtils` has **zero callers** and only `System.out.println`s |

⚠️ Note the second row of that table interacts with the safety rules: re-running the four `AddServerInformationAdDomain` / `InsertAdDomain` flows would replay a **mutating** call. Under the standing
rule "never replay a mutating call", the read-back must be fixed and re-validated on **fresh** objects, not
by re-executing the captured hops.

---

## 6. Fixes

| # | Owner | Change | Effect |
|---:|---|---|---|
| 1 | **Harness** | When a `verify_*` hop's value placeholder is unresolved, skip the call and record `NOT VERIFIABLE` — do not send the hop and do not emit a FAIL | 97 of 107 rows stop being noise; the read-back report becomes readable |
| 2 | **Product** | A create must return the primary key of the row it inserted | removes the root cause of all 97 |
| 3 | **Harness** | Accept a `Message`-level existence confirmation (`"Record Already Exists."`, `"Record Found"`) as a PASS signal in `assess()` | 2 false negatives corrected |
| 4 | **Harness** | Pin the id field per endpoint rather than `any_id()`'s `/id$/` guess, and reject a candidate that equals a value already present in the request body, or that is `0`, or that is not key-shaped | stops taking an **email address** and a **request echo** as record keys |
| 5 | **Harness** | Give `pick_readback()` a body source, or restrict it to read endpoints that need no body (`generate_flows.py:187-211`, `:266`) | 4 rejected read-backs become real tests |
| 6 | **Framework** | Populate the `db_*` keys in `Environments/QA_MsSQL.properties`, fix `AutoConfigs.java:140`, and give `DBUtils` a return value an assertion can read | the only way L6 can ever answer "created but not readable back" |

---

## 7. Reproducing this

```powershell
python tools\obj007_chain_analysis.py --stats   # counts only, writes nothing
python tools\obj007_chain_analysis.py           # rewrites both JSON deliverables
```

The L6 population reproduces exactly as the brief states: **107 checks, 2 PASS, 105 FAIL**. Per-check detail
— the upstream create and what it returned, the value searched for, the full read-back response, the root
cause and the suggested fix — is in `artifacts/analysis-data/l6-read-back.json` (107 rows). The upstream cause analysis
for the missing ids is in `docs/analysis/A1-chaining-analysis.md`.
