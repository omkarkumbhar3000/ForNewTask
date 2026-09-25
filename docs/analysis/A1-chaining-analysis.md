# A1 — Chaining validation: why 196 hops never published a chain key

**Scope:** OBJ-007 item A1 · **Evidence:** `artifacts/runs/2026-07-29_181439/results.json` + its 1,868
`evidence/*.json` captures · **Generator:** `tools/obj007_chain_analysis.py`
**Data emitted:** `artifacts/analysis-data/chaining-validation.json` (1,873 rows, one per executed hop)
**HTTP requests issued by this analysis:** 0 · **DB access:** none

---

## 0. The finding in one line

All **196** `resolved []; MISSING ['NEW_ID']` failures are **product-side or contract-side**, not extractor
bugs. Cause (c) — *the extractor's key pattern missed an id that was present* — is **0 of 196**. No response
among the 196 contains an id-shaped value anywhere, at any depth, under any id-ish key name.

| Cause | Hops | Share | Owner |
|---|---:|---:|---|
| **(a)** The create genuinely failed — no id ever existed | **117** | 59.7 % | Product + missing request contracts |
| **(b)** Create acknowledged, response carries no id field | **19** | 9.7 % | ⛔ **Product / API contract gap** |
| **(c)** An id *was* present and the extractor missed it | **0** | 0.0 % | — (no harness bug of this kind) |
| **(d)** No id **and** no determinate create signal — outcome `UNKNOWN` | **60** | 30.6 % | Product (silent writes) + generator misclassification |
| Total | **196** | 100 % | |

Cause (d) is reported separately rather than folded into (a) or (b) because the evidence cannot say whether
the write happened — see §5. Folding it either way would be an invented measurement.

---

## 1. Exactly which hops produced the 196

### 1.1 All 196 are the same structural position

Every one is **hop 4** of its flow — the create call that immediately follows the fixed three-hop LOB
prelude (`generate_flows.py:69-85`: `GetLOBList` → `GetUserGroupList` → `GetServerGroupList`). No prelude
hop and no read-sweep hop ever failed L5.

| Property of the 196 | Value |
|---|---|
| Hop number | `4` for all 196 |
| Distinct endpoints | **196** — each endpoint failed exactly once, so the by-endpoint distribution is flat |
| Distinct controllers | **56** |
| Detail string | identical for all 196: `resolved []; MISSING ['NEW_ID']` |
| HTTP status | `200` × 170 · `400` × 16 · `404` × 8 · `500` × 2 |
| Content-Type | `application/json` for all 196 |
| Transport errors | 0 |
| Flow outcome | **99** flows stopped here (no later hop ran) · **97** continued |
| Flow tier | the split is exact: all **99** that stopped are **tier 1** (the create had a payload literal, so `stop_on_fail: True`); all **97** that continued are **tier 3** bodyless probes (`stop_on_fail: False`) |

### 1.2 By endpoint-name prefix — the generator's create rule dominates

| Prefix | Hops | Note |
|---|---:|---|
| `Set*` | **152** | `WRITE_NEW` (`generate_flows.py:37`) treats *any* name starting `set` as a create |
| `Insert*` | 26 | genuine inserts |
| `Create*` | 10 | genuine creates |
| `Save*` | 6 | genuine saves |
| `Add*` | 2 | genuine adds |

The tier split above is worth stating separately, because it decides what each failure costs. A **tier-1**
flow is a create for which the framework *does* hold a payload literal, so it carries `expect_created: True`
and `stop_on_fail: True` (`generate_flows.py:252-254`) — its L5 failure ends the flow immediately. A
**tier-3** flow is a create for which **no request body is defined anywhere in the framework**, probed with
`{}` deliberately to record the gap (`generate_flows.py:236-243`); it carries `stop_on_fail: False`, so it
runs on into a read-back that cannot possibly work. Every one of the 97 meaningless L6 verdicts analysed in
A4 comes from this second group.

⚠️ 152 of 196 are `Set*`. A large part of that population is not a create at all — `SetStatus`,
`SetRelativePath`, `SetVideoFileName`, `SetErrorLog`, `SetSessionCommandLog`, `SetServiceSessionLogout` are
status probes and telemetry writes with no entity and no key to return. Expecting `NEW_ID` from them is a
**generator classification defect**, distinct from cause (c).

### 1.3 By controller — full distribution (all 56)

| Controller | Total | (a) failed | (b) no id returned | (c) missed id | (d) unknown |
|---|---:|---:|---:|---:|---:|
| `ServiceDetails` | 16 | 9 | 3 | 0 | 4 |
| `ServiceDetailsV2` | 16 | 9 | 3 | 0 | 4 |
| `ServiceDetailsV3` | 15 | 9 | 3 | 0 | 3 |
| `UserDetailsV2` | 15 | 14 | 0 | 0 | 1 |
| `UserDetailsV4` | 14 | 13 | 0 | 0 | 1 |
| `UserDetails` | 13 | 12 | 0 | 0 | 1 |
| `UserDetailsV3` | 13 | 12 | 0 | 0 | 1 |
| `ActivityLogs` | 6 | 3 | 2 | 0 | 1 |
| `DeviceOnboarding` | 5 | 4 | 0 | 0 | 1 |
| `LobandService` | 5 | 4 | 0 | 0 | 1 |
| `ServiceCreation` | 5 | 2 | 2 | 0 | 1 |
| `UserOnboarding` | 5 | 4 | 0 | 0 | 1 |
| `UIAutomationData` | 4 | 0 | 0 | 0 | 4 |
| `UserRegistrationV2` | 4 | 3 | 0 | 0 | 1 |
| `FileServerDetail` | 3 | 0 | 2 | 0 | 1 |
| `MouseKeysActivityLogs` | 3 | 1 | 0 | 0 | 2 |
| `RAVPNSetting` | 3 | 2 | 0 | 0 | 1 |
| `UserRegistration` | 3 | 2 | 0 | 0 | 1 |
| `ADbridging` | 2 | 1 | 1 | 0 | 0 |
| `ADbridgingV2` | 2 | 1 | 1 | 0 | 0 |
| `ARCONLAMMiddleware` | 2 | 1 | 0 | 0 | 1 |
| `ATSConfiguration` | 2 | 1 | 0 | 0 | 1 |
| `ATSMapping` | 2 | 0 | 1 | 0 | 1 |
| `Logs` | 2 | 1 | 0 | 0 | 1 |
| `RDPSServiceInsert` | 2 | 1 | 0 | 0 | 1 |
| `RDPSServiceInsertV2` | 2 | 1 | 0 | 0 | 1 |
| `RTSM` | 2 | 1 | 0 | 0 | 1 |
| `ServicePasswordDependancy` | 2 | 1 | 0 | 0 | 1 |
| `AGWPlus` | 1 | 0 | 0 | 0 | 1 |
| `APEMTool` | 1 | 0 | 0 | 0 | 1 |
| `ARSIMServer` | 1 | 0 | 1 | 0 | 0 |
| `AWSKeyVault` | 1 | 0 | 0 | 0 | 1 |
| `AzureKeyVault` | 1 | 0 | 0 | 0 | 1 |
| `Base` | 1 | 0 | 0 | 0 | 1 |
| `Collaborations` | 1 | 1 | 0 | 0 | 0 |
| `Configuration` | 1 | 0 | 0 | 0 | 1 |
| `CustomErrorHandler` | 1 | 0 | 0 | 0 | 1 |
| `ErrorLogToDB` | 1 | 0 | 0 | 0 | 1 |
| `Flooding` | 1 | 0 | 0 | 0 | 1 |
| `HSMEntrust` | 1 | 0 | 0 | 0 | 1 |
| `HSMUtimaco` | 1 | 0 | 0 | 0 | 1 |
| `License` | 1 | 0 | 0 | 0 | 1 |
| `OutsideARCONPAMAccess` | 1 | 1 | 0 | 0 | 0 |
| `Policy` | 1 | 0 | 0 | 0 | 1 |
| `ProfileManagement` | 1 | 0 | 0 | 0 | 1 |
| `RASyn` | 1 | 0 | 0 | 0 | 1 |
| `SIEM` | 1 | 0 | 0 | 0 | 1 |
| `Se0rviceDetailsV3` | 1 | 1 | 0 | 0 | 0 |
| `ServicePassword` | 1 | 0 | 0 | 0 | 1 |
| `ServicePasswordV2` | 1 | 0 | 0 | 0 | 1 |
| `ServiceType` | 1 | 0 | 0 | 0 | 1 |
| `User` | 1 | 1 | 0 | 0 | 0 |
| `UserDelegation` | 1 | 1 | 0 | 0 | 0 |
| `UserLabels` | 1 | 0 | 0 | 0 | 1 |
| `UserServiceSession` | 1 | 0 | 0 | 0 | 1 |
| `VideoLog` | 1 | 0 | 0 | 0 | 1 |
| **Total** | **196** | **117** | **19** | **0** | **60** |

Two structural readings of that table:

- **The `V`-suffixed controller families multiply every defect.** `ServiceDetails` / `V2` / `V3` contribute
  47 failures between them with near-identical cause profiles, and `UserDetails` / `V2` / `V3` / `V4`
  contribute 55. The same endpoint, re-published under a version suffix, fails the same way each time.
- **`Se0rviceDetailsV3` is a typo in the endpoint catalogue.** Its single failure is an HTTP 404
  (`Se0rviceDetailsV3/SetServiceSessionLogoutV2`, flow `se0rvicedetailsv3__setservicesessionlogoutv2`) —
  the route does not exist because the controller name carries a `0` where an `r` belongs.

---

## 2. Why `NEW_ID` resolved empty — the code path, then the evidence

### 2.1 How `NEW_ID` is defined

The generator attaches it to every create hop it emits (`generate_flows.py:250-258`):

```python
hops.append({
    "name": c["action"], "verb": c["verb"], "path": c["path"], "body": rb,
    "expect_created": not bodyless, "extract_any_id": "NEW_ID",     # generate_flows.py:252
    "sla_ms": 20000, "stop_on_fail": not bodyless,
```

and the read-back hop consumes it as a placeholder (`generate_flows.py:260-264`):

```python
hop = {"name": f"{back['action']}__verify", "verb": back["verb"],
       "path": back["path"], "sla_ms": 25000, "stop_on_fail": False,
       "verify_value_anywhere": {"value": "${NEW_ID}",              # generate_flows.py:262
                                 "label": "created record id"},
```

### 2.2 How it is extracted

The runner resolves the field name at execution time, because a generated flow cannot know whether a create
returns `UserId`, `ServiceId` or `MappingId` (`chain_runner.py:502-519`):

```python
ID_FIELD = re.compile(r"id$", re.I)                                  # chain_runner.py:502


def any_id(doc):
    """First scalar field whose name ends in 'id', from Result[0] or Result."""
    for container in ("Result[0]", "Result", ""):                    # chain_runner.py:511
        node = select(doc, container) if container else doc
        if isinstance(node, list):
            node = node[0] if node and isinstance(node[0], dict) else None
        if isinstance(node, dict):
            for k, v in node.items():                                # chain_runner.py:516
                if ID_FIELD.search(k) and isinstance(v, (str, int)) and str(v).strip():
                    return v, k
    return None, None                                                # chain_runner.py:519
```

Invoked once per create hop (`chain_runner.py:594-597`), and the store is skipped for a `None` value
(`chain_runner.py:585-587`):

```python
if hop.get("extract_any_id") and doc is not None:                    # chain_runner.py:594
    val, field = any_id(doc)
    store(hop["extract_any_id"], val)                                # chain_runner.py:596
    rec["id_field_used"] = field                                     # chain_runner.py:597
```

The L5 verdict then reads back what `store` recorded (`chain_runner.py:451-458`):

```python
want = set(hop.get("extract", {})) | set(hop.get("find_extract", {}).get("take", {}))
if hop.get("extract_any_id"):
    want.add(hop["extract_any_id"])                                  # chain_runner.py:453
missing = [k for k in want if extracted.get(k) in (None, "", [])]    # chain_runner.py:454
if want:
    add("L5", "chain-key-extracted", not missing,
        f"resolved {sorted(want - set(missing))}"
        + (f"; MISSING {missing}" if missing else ""))                # chain_runner.py:458
```

**`rec["id_field_used"]` is the decisive artifact.** It records the field `any_id()` matched. Across the 196
failures it is `null` in **195** cases and **absent** in 1 — so in 195 cases `any_id()` ran and found
nothing, and in 1 case it never ran because the body did not parse
(`mousekeysactivitylogs__insertmousekeysactivitylogs` — HTTP 200 with a **zero-byte body**, so
`json.loads("")` raised and `doc` was `None`).

### 2.3 Ruling out cause (c) — an id was present and the extractor missed it

`any_id()` is genuinely narrow: it looks only at the **top-level keys** of `Result[0]`, `Result` and the
root, and only at keys matching `/id$/`. Two searches were run over the 196 captured responses,
deliberately far wider than the runner's:

| Search | Scope | Hits |
|---|---|---:|
| Strict — any key matching `/id$/` with a non-empty scalar value | every dict at **any depth**, to 12 levels | **0** |
| Loose — any key containing `id`, `code`, `key`, `guid`, `ref`, `no`, `num`, `seq`, `sr` | every dict at any depth | **0** |

Outside the envelope fields, the 196 responses contain only these non-envelope keys in total: `Result` (49),
`LinuxServerIP`, `WindowsServerIP`, `WindowsDomainName`, `IsConfigured`, `CreatedBy`, `ModifyBy` (2 each),
and one occurrence each of `Output`, `schemas`, `Detail`, `Status`. Integer-valued fields anywhere in all
196 responses: **three** — `Status: 400` (an HTTP problem-details body, flow `user__create`) and `Result: 0`
twice (`useronboarding__addusergroup`, `useronboarding__addusertolob`, both HTTP 400
`" Input parameter cannot be null or empty."`, so `0` is a failure return, not a key).

⇒ **Cause (c) = 0 hops.** There was nothing for the extractor to miss. Widening `any_id()` would not have
recovered a single one of the 196.

### 2.4 Cause (a) — 117 hops: the create genuinely failed

| Sub-bucket | Hops | Evidence signature |
|---|---:|---|
| a1 — HTTP non-200 | **26** | `400` × 16 · `404` × 8 · `500` × 2 |
| a2 — HTTP 200 with `Success: false` | **89** | envelope rejection delivered as 200 |
| a3 — HTTP 200 with a non-standard error payload | **2** | `{"Output": "1\|Parameter error occurred …"}`; bare JSON `false` |

Named examples, each traceable to a flow id and an `evidence/` file:

| Flow · hop | Evidence |
|---|---|
| `adbridging__insertlobdetails` hop 4 `InsertLOBDetails` | HTTP 200, `Success:false`, `ErrorCode:"104-ADC-ILD"`, `"Input parameter is invalid"` |
| `userdetails__setusertousergroupmapping` hop 4 | HTTP 200, `201-UDC-UGM`, `"Required property 'UserId' not found in JSON"` |
| `userdetails__setserviceusermapping` hop 4 | HTTP **400**, `201-UDC-SUM`, `"Could not find member 'userid' on object"` |
| `deviceonboarding__setdefaultgenericidsv2` hop 4 | HTTP **500**, `"An error has occurred."` |
| `lobandservice__createpamservice` hop 4 | HTTP 200, `Success:false`, `ErrorCode` containing a full .NET stack trace with build paths (`…\ARCONPAMAPI\EntityDataAccessLayer\…LOBandServiceTypeDal.cs:line 556`) |
| `arconlammiddleware__setpamuserdetails` hop 4 | HTTP 200, `{"Output":"1\|Parameter error occurred - Parameter - Activity is Mandatory …"}` — a sixth envelope shape, not in the five the brief lists |

The dominant a2 sub-signature is a **binding failure**: **55 of the 89** carry
`"Required property '<X>' not found in JSON"`, `"Could not convert string to integer"`,
`"Could not find member '<x>' on object of type '<Y>'"` or `"Input parameter is invalid"` — 61 across all
117 cause-(a) hops. The stale payload literal in `src/test/java/com/arcon/utils/apiPayload` does not match
the current request model. This is the same root gap the brief records as *"Create endpoints: 217, of which
only 13 can be driven"* — measured here from the opposite direction. A further **23 of the 89** answer only
`"System error has occurred"`, which names no field and therefore cannot be acted on without the endpoint's
request contract.

### 2.5 Cause (b) — 19 hops: the create was acknowledged and returned no id ⛔

These are the API contract gap. The endpoint states, in its own envelope, that it inserted a record — and
returns nothing a chain can carry forward.

| Flow · hop | Response (verbatim, redacted) |
|---|---|
| `adbridging__insertserverdomainmapping` hop 4 | `Success:true, Message:"Record Inserted successfully.", Result:{LinuxServerIP, WindowsServerIP, WindowsDomainName, IsConfigured, CreatedBy, ModifyBy}` — a full record echo with **no key field** |
| `adbridgingv2__insertserverdomainmapping` hop 4 | identical |
| `arsimserver__insertarsimserverdetails` hop 4 | `Success:true, Message:"Record Inserted successfully.", Result:false` |
| `fileserverdetail__insertfileserverconfiguration` hop 4 | `Success:true, Message:"Record Inserted successfully.", Result:false` |
| `atsmapping__insertpreferencepath` hop 4 | `Success:true, Message:"Inserted Successfully"` — no `Result` at all |
| `activitylogs__insertssmlogsnew` hop 4 | `Success:true, ErrorCode:"", ErrorMessage:"Data inserted sucessfully"` — the insert confirmation is delivered in **`ErrorMessage`** |
| `activitylogs__savessmlogs` hop 4 | same shape |
| `servicecreation__setsshlinuxvault` hop 4 | `Success:true, Message:"SSH Linux vault saved successfully.", Result:true` |
| `servicecreation__setdropservice` hop 4 | `Success:true, Message:"Disabled Successfully"` |
| `servicedetails__seterrorlog` · `V2` · `V3` hop 4 | `Success:true, Message:"Operation Successfull", Result:["Success"]` |
| `servicedetails__setservicesessionlogout` · `V2` · `V3` hop 4 | same |
| `servicedetails__setsessioncommandlog` · `V2` · `V3` hop 4 | same |
| `fileserverdetail__insertuploadedfiledetails` hop 4 | bare JSON `true` — no envelope at all |

`Result` distribution across the 19: **absent** (5), `bool` (5), `list["Success"]` (7), `dict` without a key
field (2). Not one carries a primary key.

⇒ **This is the single actionable product change in this report.** A create must return the primary key of
the record it inserted. Until it does, no generated chain can proceed past the create, and no read-back can
be verified — see A4.

### 2.6 Cause (d) — 60 hops: no id **and** no statement of the outcome

| Sub-bucket | Hops | Evidence |
|---|---:|---|
| `SetStatus` banner | **48** | HTTP 200, body is the bare JSON string `"Version 1.0: Setting up !!"` — 48 controllers publish the same status probe. Not a create. |
| `Success:true` with no `Message` at all | **11** | e.g. `servicedetails__setrelativepath` → `{Program, Version, DateTime, Success:true}`; `setvideofilename` → `Success:true, Result:[]` |
| HTTP 200 with a zero-byte body | **1** | `mousekeysactivitylogs__insertmousekeysactivitylogs` — `Content-Type: application/json`, `body_bytes: 0` |

⚠️ For all 60, the run cannot state whether a write occurred. `Success:true` with no message is not evidence
of a write — the brief's own rule (`SetServiceDetails` returns `Success:true` / `"Already Exists"` having
inserted nothing) applies with more force where there is no message to read. **What would settle it:** a
read-only `SELECT` against `ARCOSDB_U16SP2_WEBSM_QA` for the 11 silent writes; for the 48 `SetStatus` hops
nothing needs settling — they must be removed from the create population
(`generate_flows.py:37`, `WRITE_NEW = re.compile(r"^(set|insert|create|add|save)", re.I)`).

---

## 3. The cascade — what the missing ids cost downstream

### 3.1 Planned vs executed

| Measure | Value | Source |
|---|---:|---|
| Hops planned across the 326 flows | **2,067** | `tools/flows/**/*.json` |
| Hops executed and recorded | **1,873** | `results.json` |
| Hops never executed | **194** | difference |
| Flows truncated before their last planned hop | **115** | per-flow comparison |
| Of the 194 lost hops, lost in a flow whose create failed L5 | **118** across **98 flows** | join on the L5 verdict |
| Hops transmitted **with an unresolved `${…}` placeholder** | **103** | placeholder set of the hop definition vs the run seed plus everything published upstream |

Truncation is the runner honouring `stop_on_fail` (`chain_runner.py:656-658`): a create hop emitted with a
parseable body carries `stop_on_fail: True` (`generate_flows.py:253`), so the flow ends at the first failing
check.

### 3.2 Starved read-backs

218 of the 326 flows planned a read-back hop. Only **107** ever ran:

| Outcome | Flows | Why |
|---|---:|---|
| Read-back executed (L6 verdict recorded) | **107** | reached hop 5 |
| Never ran — create hop failed **L5** and truncated the flow | **98** | ⛔ the starvation this report is about |
| Never ran — create hop failed **L4** (message semantics) with L5 passing | **9** | create rejected, but an id was still extractable |
| Never ran — hop 1 `GetLOBList` breached its 8,000 ms **L7** SLA | **4** | the prelude itself died (8 flows died this way in total; 4 of them had planned a read-back) |

### 3.3 Unresolved placeholders, by variable

`substitute()` leaves an unmatched placeholder **as the literal token** (`chain_runner.py:200`,
`return vars.get(m.group(1), node)`), so a starved hop is still transmitted — carrying the string
`${NEW_ID}` where a value belonged.

Only two variables were ever starved. The nine per-run identity variables (`NEW_USERNAME`,
`NEW_USER_EMAIL`, `NEW_SERVICE_HOST`, …) are handed to every flow as the run seed
(`chain_runner.py:177-191`, `chain_runner.py:539`), so they always resolved and are excluded here.

| Variable | Hops sent with it unresolved | Why it was missing |
|---|---:|---|
| `${NEW_ID}` | **97** | the create published nothing — these are exactly the read-backs analysed in A4 |
| `${SERVICE_GROUP_ID}` | **6** | ⛔ **unsatisfiable by construction** — `CONTEXT` (`generate_flows.py:46`) rewrites any `servicegroupid` field to this placeholder, but the three-hop prelude publishes only `LOB_ID`, `LOB_NAME`, `USER_GROUP_ID`, `USER_GROUP_NAME` and `SERVER_GROUP_ID`. Nothing ever sets it |

⛔ **This is a harness defect in its own right, independent of cause (c).** A hop whose input did not resolve
should be reported as `NOT VERIFIABLE` and not sent. Transmitting `"${NEW_ID}"` as a request value means the
196 create failures produced 97 further meaningless assertions downstream (A4 §3).

### 3.4 Achieved chain depth

Hops actually executed per flow (a skipped teardown does not count):

| Hops executed | Flows | Reading |
|---:|---:|---|
| 1 | 8 | died in the prelude at `GetLOBList` — **all 8 on the L7 latency SLA** (8,240–10,034 ms vs 8,000 ms); the call itself returned HTTP 200 |
| 4 | **131** | prelude + create, then stopped — the modal outcome |
| 5 | **116** | prelude + create + read-back |
| 6 | 11 | + update or teardown |
| 7 | 5 | |
| 8 | 5 | |
| 9 | 4 | |
| 10 | 4 | |
| 11 | 2 | |
| 12 | 3 | |
| 13 | **37** | full read-sweep flows (prelude + 10 reads) |

Cumulative reach:

| Reached at least hop | Flows | Share of 326 |
|---:|---:|---:|
| 1 | 326 | 100 % |
| 2 | 318 | 97.5 % |
| 3 | 318 | 97.5 % |
| 4 | 318 | 97.5 % |
| **5** | **187** | **57.4 %** |
| **6 or deeper** | **71** | **21.8 %** |
| 7 | 60 | 18.4 % |
| 8 | 55 | 16.9 % |

**The cliff is between hop 4 and hop 5** — 318 flows reached the create, 187 got past it. 131 flows
(40 % of the run) ended at the create hop. True multi-hop depth, in the sense of *a value created by this run
being carried into a later call*, was achieved by 2 flows only: `user_lifecycle` (`NEW_USER_ID=1457` →
`GetAllActiveUserList`) and `service_lifecycle` (`NEW_SERVICE_ID=25342` → `GetServiceDetails` →
`GetActiveServicesByLOBId`). Both are **hand-written** flows with a **pinned** extraction selector.

---

## 4. Per level — what was validated, and what a failure means

| Layer | Check | What passing proves | PASS | FAIL | What the failures were |
|---|---|---|---:|---:|---|
| **L1** | `http-status` | the transport agreed with the expectation | 1,688 | **180** | 176 wrong status (`400`/`404`/`500`), 4 no response at all (timeout / transport error) |
| **L2** | `content-type` | the response declared `application/json` | 1,864 | **4** | Content-Type absent entirely — an assertion cannot even parse the body |
| **L3** | `envelope` | the standard envelope is present **and** `Success=true` (or a known `errorCode`) | 1,278 | **590** | 303 `Success=False` (⚠️ **289 of them on HTTP 200** — a status-only assertion passes against every one; 14 on HTTP 400), 161 neither `Success` nor `errorCode` present, 113 bare string, 7 unparseable body (`NoneType`), 4 bare array, 2 bare boolean |
| **L4** | `message-semantics` | the `Message` text asserts the outcome the hop expected — the brief's `"Inserted Successfully"` vs `"Already Exists"` rule | 1,410 | **458** | 243 `ErrorMessage` set (of those: 101 name a binding/parameter problem, 64 say only `"System error has occurred"`, 15 carry .NET exception text), 126 no envelope to read at all, 83 `Message` present but **empty**, 4 `Message` present but not a create confirmation, 2 explicit no-ops (`"Already Exists"`) |
| **L5** | `chain-key-extracted` | every chain key this hop must publish resolved to a non-empty value — **the only layer that proves a chain is possible** | 982 | **196** | one signature: `resolved []; MISSING ['NEW_ID']`. §2 splits it a/b/c/d |
| **L6** | `record-exists` | the record this flow created is readable back through a list endpoint — **the only layer that proves a write persisted** | **2** | **105** | 97 searched for the literal `${NEW_ID}`. Full analysis in A4 |
| **L7** | `latency` | the hop finished inside its SLA (5,000 ms default; 20,000 ms create; 25,000 ms read) | 1,855 | **13** | **8 of the 13 were hop 1** (`GetLOBList`, 8,240–10,034 ms against an 8,000 ms SLA) and each one killed its flow outright; the other 5 were at hops 3, 4 and 13 |

Two cross-layer readings that matter more than any single count:

- **L1 passing is worth almost nothing on this API.** 1,688 hops passed L1 while 590 failed L3 and 458
  failed L4. 303 rejections were delivered as HTTP 200. This is the brief's response-envelope rule measured:
  a status-only assertion would have reported a 90 % pass rate against a 64 % true pass rate.
- **L5 and L6 are the only layers that test *chaining*.** L1–L4 test one call in isolation. L5 answers
  "can this call feed the next one?" (196 times: no) and L6 answers "did the write actually land?"
  (105 times: unproven). Those two layers are where the automation value is, and they are the two the
  product currently cannot support.

---

## 5. What is `UNKNOWN`, and what would settle it

| Question | Status | What would settle it |
|---|---|---|
| Did the 19 cause-(b) creates actually insert a row? | 🟡 `UNKNOWN` — the API says `Success:true` + `"Record Inserted successfully."`, which the brief establishes is not evidence of a write | Read-only `SELECT` on `ARCOSDB_U16SP2_WEBSM_QA` for the specific records (`10.10.2.42`/`10.10.0.71` server-domain mapping; the ARSIM server row; the file-server configuration) |
| Did the 11 silent `Success:true` writes insert anything? | 🟡 `UNKNOWN` — no `Message`, no `Result`, no id | Same — a read-only `SELECT`, per endpoint |
| Did the 48 `SetStatus` calls write anything? | ⬜ Not applicable — they are status probes returning a fixed banner | Remove them from the create population; no product action needed |
| Did the zero-byte-body create write anything? | 🟡 `UNKNOWN` | Read-only `SELECT`; and raise the empty 200 as a defect regardless |
| Are the 117 cause-(a) endpoints reachable at all with a correct body? | 🟡 Partly answerable — **61 of 117** returned an error naming the offending field, so the contract gap is evidenced for those; **23 of the 89** HTTP-200 rejections answered only `"System error has occurred"`, which evidences nothing | The published request contract per endpoint (the Confluence export binds payloads by page proximity and leaves 70 % of the surface undocumented, so it cannot answer this) |

⛔ **What must not be inferred:** that the 196 are a harness problem. Cause (c) is 0. The extractor found
nothing because there was nothing to find.

---

## 6. Fixes, in the order that unblocks the most

| # | Owner | Change | Unblocks |
|---:|---|---|---|
| 1 | **Product** | A create must return the primary key of the row it inserted, inside `Result` | 19 hops directly; every generated lifecycle chain structurally |
| 2 | **Product / API docs** | Publish the request contract for the create endpoints | up to 91 cause-(a2) hops whose bodies fail to bind |
| 3 | **Product** | Never return a rejection as HTTP 200; populate `Message` on every write | 303 L3 and 86 empty-`Message` L4 failures; removes the need for envelope guesswork |
| 4 | **Harness** | Do not send a hop whose input placeholder is unresolved — record `NOT VERIFIABLE`; and stop emitting `${SERVICE_GROUP_ID}`, which nothing publishes | 103 hops, of which 97 produced meaningless L6 verdicts |
| 5 | **Harness** | Narrow `WRITE_NEW` (`generate_flows.py:37`) so `SetStatus`, `SetRelativePath`, `SetVideoFileName` and the session/telemetry writers are not treated as creates | 60 cause-(d) hops leave the create population entirely |
| 6 | **Harness** | Pin the id field per endpoint instead of `any_id()`'s `/id$/` guess — it took an **email address** from `EmailID` and a request **echo** from `ServerDetailID` (see A4 §4) | id quality on the hops that do publish one |
| 7 | **Catalogue** | Fix `Se0rviceDetailsV3` in `APIConfig.java`; reconcile the `V2`/`V3`/`V4` controller duplicates | 1 hard 404 plus the ×3–×4 multiplication of every finding |

---

## 7. Reproducing this

```powershell
python tools\obj007_chain_analysis.py --stats   # counts only, writes nothing
python tools\obj007_chain_analysis.py           # rewrites both JSON deliverables
```

The script re-derives every figure above from `results.json` and `evidence/`, and asserts the seven check
tallies against the values the shared brief declares authoritative. It issues **zero HTTP requests** and
touches no database. All seven tallies, the flow verdicts (30 PASS / 296 FAIL), the hop count (1,873) and
the L6 population (107 = 2 PASS + 105 FAIL) reproduce exactly.

Per-hop detail — dependency, resolved inputs, all seven layer verdicts, cause bucket, and the
`evidence/` filename for every row — is in `artifacts/analysis-data/chaining-validation.json` (1,873 rows).
