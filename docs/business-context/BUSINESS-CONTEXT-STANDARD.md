# Business Context Standard — the reference example

**Purpose:** the answer to *"How do you provide business context to the AI?"* — open this file and walk it.
**Worked example:** five-level **Service Creation → Service Password Request → Approval** validation.
**Status:** ✅ Gold standard. Copy §0's checklist for any new feature. · **Objective:** `OBJ-009`
**Owner:** Sudesh Sawant · **Jira:** `PAMIT` · **Environment:** `QA_MsSQL` — `https://u16hf.arconnet.com:6302`

---

## How to read this document

| § | Section | Why an AI needs it |
|---:|---|---|
| **0** | [The context checklist](#0-the-context-checklist) | The reusable template. **Start here in a demo** |
| **1** | [Business objective](#1-business-objective) | What the business is trying to achieve |
| **2** | [Glossary](#2-glossary) | Domain vocabulary — without it every other section is ambiguous |
| **3** | [Actors](#3-actors) | Who acts, with which identity |
| **4** | [Business workflow](#4-business-workflow) | The end-to-end story |
| **5** | [Approval chain](#5-approval-chain) | The five levels, and how state advances |
| **6** | [Preconditions](#6-preconditions-and-environment-configuration) | Configuration that must be true first |
| **7** | [APIs involved](#7-apis-involved) | The endpoint inventory with roles |
| **8** | [API sequence](#8-api-sequence) | Order, and what each hop passes forward |
| **9** | [Request payloads](#9-request-payloads) | Real fields, real types, real provenance |
| **10** | [Response expectations](#10-response-expectations) | What "success" actually looks like here |
| **11** | [Validation points](#11-validation-points) | The twelve layers, per hop |
| **12** | [Database validation](#12-database-validation-points) | Proving the row landed |
| **13** | [Business rules](#13-business-rules) | Rules that must hold, and their status |
| **14** | [Edge cases](#14-edge-cases) | Boundaries and awkward states |
| **15** | [Negative scenarios](#15-negative-scenarios) | Rejection behaviour |
| **16** | [Test scenarios](#16-test-scenarios) | The suite, with IDs |
| **17** | [Expected outcomes](#17-expected-outcomes) | Pass criteria per scenario |
| **18** | [Non-functional expectations](#18-non-functional-expectations) | Latency, concurrency |
| **19** | [Required datasets](#19-required-datasets) | Data that must exist or be generated |
| **20** | [Safety constraints](#20-safety-constraints-absolute) | ⛔ What must never be called |
| **21** | [Known defects](#21-known-defects-affecting-this-flow) | So a product bug isn't chased as a test bug |
| **22** | [Documentation references](#22-documentation-references) | Every citable source |
| **23** | [Assumptions](#23-assumptions) | Stated, so they can be challenged |
| **24** | [Dependencies](#24-dependencies) | What this needs, and who owns it |
| **25** | [What is NOT known](#25-what-is-not-known) | The honest gaps |
| **26** | [Traceability](#26-traceability) | Evidence and ticket links |

⚠️ **Every figure in this document is traceable.** Where something is not established it says
`UNKNOWN` or `NOT DOCUMENTED` and names what would settle it. That is the single most important property of
a context document: an AI given a plausible-sounding invention will build confidently on sand.

---

## 0. The context checklist

This is the transferable part. For any new feature, supply these twelve things — the rest of this document
is that checklist, filled in.

| # | Supply | Failure if you omit it |
|---:|---|---|
| 1 | **Business objective** — the outcome, in business terms | The AI optimises the wrong thing (e.g. maximises endpoints called, not risk covered) |
| 2 | **Glossary** of domain terms | `LOB`, `SLS`, `WFT`, `ACMO` get guessed at; wrong tables queried |
| 3 | **Actors and identities** — who acts, with which credential | Chains fail at the first authorisation boundary with an unexplained rejection |
| 4 | **Workflow and state machine** — steps and how state advances | Steps get run in a valid-looking but impossible order |
| 5 | **Preconditions** — configuration and data that must pre-exist | Failures look like product defects and get escalated |
| 6 | **API inventory with roles** — read / create / update / delete | The AI cannot tell a safe probe from a destructive write |
| 7 | **Payload contracts** — field, type, mandatory, example, **provenance** | Generated payloads are rejected; nobody can tell whether the test or the API is wrong |
| 8 | **Response contract** — including how failure is expressed | ⚠️ **The biggest trap here.** See §10 |
| 9 | **Validation points** — what to assert at each step, and what *cannot* be asserted | Status-only assertions pass against rejected requests |
| 10 | **Business rules and edge cases** | Only the happy path is covered |
| 11 | **Safety constraints** — what must never be called | ⛔ An outage. See §20 |
| 12 | **Explicit unknowns** | The AI invents the missing piece rather than flagging it |

---

## 1. Business objective

**Business outcome.** A privileged user must be able to obtain the password for a specific service **only
after an approval chain of up to five approvers has consented**, with a complete, non-repudiable record of
who approved what and when.

**Why it matters commercially.** This is the core control ARCON PAM sells. If a password can be obtained
without the full approval chain, the product has failed at its primary purpose. If an approved request
*cannot* be fulfilled, the product blocks legitimate operational work.

**QA objective.** Prove both directions:

| Must hold | Meaning |
|---|---|
| **No premature release** | The password is not obtainable until level 5 has approved |
| **No lost approval** | Each approval is recorded against the right level, approver and timestamp |
| **No silent failure** | A rejection at any level stops the chain and is visible |
| **Fulfilment on approval** | After the final approval the password is delivered and the record closes |

**Scope of this document.** The composite flow: **create a service** (5-hop chain, ✅ measured end to end)
→ **raise a password request against it** → **five sequential approvals** → **fulfilment and audit**.

---

## 2. Glossary

Domain vocabulary. An AI without this queries the wrong tables and misreads field names.

| Term | Meaning | Where it appears |
|---|---|---|
| **LOB** | Line of Business — the top-level tenant/grouping. Every service and user belongs to one | `sso_lobs`, `LOBID`, `sls_id` |
| **SLS** | The database prefix for LOB columns (`sls_id`, `sls_name`) | `sso_lobs` |
| **Service** | A managed target: a server, database or device a privileged user connects to | `sso_services`, `ss_service_id` |
| **Server Group** | A grouping of services within a LOB. A service is created **into** one | `sso_Sgroup`, `ServerGroupId` |
| **Service Type** | The connection protocol. `1` = Windows RDP in this environment | `ServiceTypeId` |
| **ACMO** | The end-user web portal — where a user raises a request and reads their mailbox | `PAMSpecifcConfigs.acmo` |
| **AdminUI / Settings** | The administrative console — where the workflow is *defined* | `PAMSpecifcConfigs.settings` |
| **WFT** | Workflow Transaction — one approval request instance | `sso_arcos_wft_details`, `wft_*` |
| **TransID** | The business handle for a request, used by the approval APIs | `wft_trans_id`, `TransID` |
| **Approval Level** | 1–5. Configured per workflow, stored per request | `wft_approval_levels` |
| **GC** | Global Configuration — a product-wide switch in the admin console | `sso_arcos_lob_global_config` |
| **Vault** | Where service passwords are stored; delivery is via the ACMO mailbox | `NotificationDetails/VaultPasswordMailBox` |
| **Envelope** | The application-level `{Success, Message, ErrorCode, Result}` wrapper | §10 |

---

## 3. Actors

Six distinct identities. Credentials are in `Environments/QA_MsSQL.properties` (⚠️ plaintext, git-tracked —
see §21).

| Actor | Identity | Property key | Role in this flow |
|---|---|---|---|
| **Administrator** | `auto_adminui` | `user_name` / `password` | Defines the workflow in AdminUI; also raises the request in this test |
| **Approver L1** | `auto_admin1` | `Admin_user1_name` | First approval |
| **Approver L2** | `auto_admin2` | `Admin_user2_name` | Second |
| **Approver L3** | `auto_admin3` | `Admin_user3_name` | Third |
| **Approver L4** | `auto_admin4` | `Admin_user4_name` | Fourth |
| **Approver L5** | `auto_admin5` | `Admin_user5_name` | **Final** — fulfilment triggers here |
| **API principal** | `GenericScheduler` | `pam_APITokenUserName` | The identity all API calls run as. ⛔ **Currently locked** — §24 |

**Domain:** `ARCOSAUTH` (`Domain` property).

⚠️ **The API principal is not any of the six humans.** Every API call in §7 executes as `GenericScheduler`
via a bearer token, *not* as the approver whose approval it records — the approver is identified by the
`UserID` field in the payload. This is why authorisation cannot currently be negative-tested: one token,
one identity. See §25.

---

## 4. Business workflow

```
ADMIN (AdminUI)                    REQUESTER (ACMO)              APPROVERS L1..L5 (ACMO/Manager)
      |                                   |                                   |
 1. Enable GC switches                    |                                   |
 2. Define workflow:                      |                                   |
    RequestType = Service Password        |                                   |
    AccessType  = One Time                |                                   |
    ApprovalLevels = 5                    |                                   |
    Approver1..5 = admin1..admin5         |                                   |
      |                                   |                                   |
 3. Create the target service ------------+                                   |
    (the 5-hop chain, §8A)                |                                   |
      |                                   |                                   |
      |                          4. Raise password request                     |
      |                             -> TransID issued, status Pending         |
      |                                   |                                   |
      |                          5. Appears in Pending Requests               |
      |                                   |                                   |
      |                                   +--------> 6. L1 approves ----------+
      |                                   |          7. L2 approves          |
      |                                   |          8. L3 approves          |
      |                                   |          9. L4 approves          |
      |                                   |         10. L5 approves (FINAL)  |
      |                                   |                                   |
      |                         11. Password delivered to ACMO mailbox        |
      |                         12. Request Log shows Approved                |
      |                                   |         13. Approval Log per level|
      |                                   |                                   |
 14. Workflow deleted (teardown)          |                                   |
```

**Reference implementation:** `src/test/java/com/arcon/tests/UI/EndToEnd/raiseRequestServicePassword/ServicePasswordRequestFiveLevelTest.java`

⚠️ **Automated via the UI, not the API.** An API variant exists in that same file but is **entirely
commented out** (lines 219–359). So the approval chain is exercised through Playwright UI driving today;
the API path in §8B is **designed and grounded but not yet automated**. Stating this plainly is the point —
an AI told "we test the approval chain" would otherwise assume API coverage that does not exist.

---

## 5. Approval chain

### 5.1 Definition

Configured per LOB in AdminUI → Workflow. Fields set by the reference test:

| Field | Value | Page-object constant |
|---|---|---|
| Description | *(data-driven)* | `WorkflowPage.description` |
| Request Type | **Service Password** | `WorkflowPage.requestType` |
| Access Type | **One Time** | `WorkflowPage.accessType` |
| Priority | *(data-driven)* | `WorkflowPage.priority` |
| LOB / Profile | *(data-driven)* | `WorkflowPage.lobOrProfile` |
| **Approval Levels** | **5** | `WorkflowPage.approvalLevels` |
| Enabled | Yes | `WorkflowPage.enabled` |
| Approver 1–5 | `auto_admin1` … `auto_admin5` | `WorkflowPage.approver1..approver5` |

**Request types available** — measured from `sso_arcos_workflow_request_type` (5 rows):

| `wfr_id` | Type | Active |
|---:|---|---|
| 1 | **Service Password** ← *this flow* | ✅ |
| 2 | Service Access | ✅ |
| 3 | Service Ticket | ⬜ inactive |
| 4 | Critical Command | ✅ |
| 5 | New User Creation | ✅ |

### 5.2 State advance

Approval is **strictly sequential**: level *N+1* becomes actionable only after level *N* approves. The
request carries `CurrentApprovalLevel` and `LastApprovalLevel`
(`NotificationDetails/ViewServicePasswordRequest`), and the database records each level independently:

```
wft_approver_l{1..5}_id          -- who
wft_approver_l{1..5}_user        -- username (plaintext)
wft_approver_l{1..5}_status      -- 0 | 3 | 9   (see the warning below)
wft_approver_l{1..5}_status_on   -- when
wft_approver_l{1..5}_comment     -- why
wft_current_status_sas_id        -- overall request status
```

⚠️ **The status codes are undocumented.** Measured in `sso_arcos_wft_details` (389 requests):
`wft_approver_l1_status` takes exactly three values — **`3`** (224 rows), **`0`** (98), **`9`** (67). Their
meanings are **`UNKNOWN`**. No status-lookup table for `sas_id` exists in the schema. Inferring
"3 = approved" from frequency would be a guess, so **it is not asserted**. Settled by: a status-code
lookup from Development. Recorded in §25.

### 5.3 Five-level requests are real

Approval-level distribution in `sso_arcos_wft_details`:

| Levels | Requests |
|---:|---:|
| 1 | 282 |
| 2 | 63 |
| 3 | 21 |
| 4 | 1 |
| **5** | **22** |

**22 genuine five-level requests exist in the QA database**, so this is a real, exercised product path —
not a theoretical configuration. `sso_arcos_wft_details_approver` holds **96,687** rows, and
`sso_arcos_wft_config_details` **1,353** — the workflow subsystem carries real volume.

---

## 6. Preconditions and environment configuration

⚠️ **The most commonly omitted section, and the most expensive.** Omit it and the flow fails in a way that
looks like a product defect. Every item below is set by `pre_requisites()` in the reference test.

| Precondition | Setting | Constant |
|---|---|---|
| Service access allowed for the LOB | **Enabled** | `LobPage.allowServiceAccess` |
| LOB-wise workflow configuration | **Enabled** | `GeneralPage.lobwiseWorkflowConf` |
| Service display fields | `IPADDRESS,USERNAME,DOMAIN,DBINSTANCE,HOSTNAME` | `ServicePage.serviceDisplayConfiguration` |
| Captcha in ACMO | **Disabled** | `WorkflowPage.captchaValidationInAcmo` |
| Existing workflows for the LOB | **Disabled** before adding a new one | `disableAllEntries(...)` |

Data preconditions:

| Must exist | Value in QA | Source |
|---|---|---|
| A LOB | `AUTOMATION_TEST_LOB`, `LOB_ID = 108` | measured, run `2026-07-29_181439` |
| A server group in that LOB | `SERVER_GROUP_ID = 282` | measured |
| Six user accounts | `auto_adminui`, `auto_admin1..5` | `Environments/QA_MsSQL.properties` |
| Service type | `ServiceTypeId = 1` (Windows RDP) | flow definition |
| A bearer token | `$env:PAM_API_TOKEN` | ⛔ §20 — must be supplied by the owner |

⚠️ **`sso_arcos_wft_lob_details`, `sso_arcos_wft_lob_user_details` and `sso_arcos_wft_usr_details` all hold
0 rows** in QA. If a test depends on LOB-scoped or user-scoped workflow mappings, that data does not exist
and must be created first.

---

## 7. APIs involved

Roles come from `tools/source-map.json`. **"Exercised"** = called in run
`artifacts/runs/2026-07-29_181439/`.

### 7A. Service creation (the validated spine)

| # | Endpoint | Verb | Role | Exercised |
|---:|---|---|---|---|
| 1 | `/api/ADbridging/GetLOBList` | POST | read | ✅ 326× · all 200 |
| 2 | `/api/ADbridging/GetServerGroupList` | POST | read | ✅ 317× · all 200 |
| 3 | `/api/ServiceCreation/SetServiceDetails` | POST | **create** | ✅ 2× · all 200 |
| 4 | `/api/ServiceDetails/GetServiceDetails` | POST | read | ✅ 2× · all 200 |
| 5 | `/api/ServiceDetails/GetActiveServicesByLOBId` | POST | read | ✅ 3× · all 200 |

### 7B. Password request and approval

| Endpoint | Verb | Role | Exercised |
|---|---|---|---|
| `/api/NotificationDetails/GetPendingNotificationsCount` | POST | read | ✅ 1× · 200 |
| `/api/NotificationDetails/GetServicePasswordRequestNotification` | POST | read | ✅ 1× · 200 |
| `/api/NotificationDetails/ViewServicePasswordRequest` | POST | read | ✅ 1× · 200 |
| **`/api/NotificationDetails/ServicePasswordRequestApproveReject`** | POST | **other (mutating)** | ⛔ **NOT EXERCISED** |
| `/api/ServicePassword/GetServicePwdReqWorkflowLogs` | POST | read | ✅ 1× · 200 |
| `/api/ServicePasswordV2/GetServicePwdReqWorkflowLogs` | POST | read | not in this run |
| `/api/NotificationDetails/GetMailBoxNotification` | POST | read | ✅ 1× · 200 |
| `/api/NotificationDetails/VaultPasswordMailBox` | POST | read | ⛔ **NOT EXERCISED** |

⚠️ **The one endpoint that performs the approval has never been called by automation.** Everything around
it is exercised; the mutation itself is not. That is the honest state, and it is exactly the kind of fact an
AI must be told rather than left to assume from the surrounding coverage.

### 7C. Swagger references

⛔ **None of the endpoints above appear in any Swagger specification.**

| Fact | Value |
|---|---|
| Swagger specs available | **37**, listed in `data/sources/Automation PAM Endpoints Details_Shared(Swagger_JSON Links).csv` |
| Operations they describe | **690** |
| Name overlap with the 1,306-endpoint catalogue | **~6%** |
| Specs declaring any `4xx`/`5xx` response | **0 of 690** |
| Specs covering §7A / §7B | **0** |

The Swagger set describes a **different surface** — the microservices behind `ARCONAPIGateway`, not the
legacy `/api/<Controller>/<Action>` surface this flow uses. So for this flow the answer to "what is the
Swagger reference?" is **`NOT DOCUMENTED — no spec covers these endpoints`**. The substitute is the
Confluence page citations in §9. Detail: `docs/findings/issues/ISSUE-005-api-coverage-gap.md`,
`.claude/rules/api-surface.md`.

---

## 8. API sequence

### 8A. Service creation — five levels, ✅ measured end to end

Definition: `tools/flows/03_service_lifecycle.json`. Values are **actually measured** from run
`2026-07-29_181439`, flow `service_lifecycle`, verdict **PASS**.

| Level | Endpoint | Consumes | Publishes | Measured |
|---:|---|---|---|---|
| 1 | `ADbridging/GetLOBList` | — | `LOB_ID`, `LOB_NAME` | `108`, `AUTOMATION_TEST_LOB` · 58 ms |
| 2 | `ADbridging/GetServerGroupList` | `${LOB_ID}` | `SERVER_GROUP_ID` | `282` · 58 ms |
| 3 | `ServiceCreation/SetServiceDetails` | `${LOB_ID}`, `${SERVER_GROUP_ID}` | **`NEW_SERVICE_ID`** | `25342`, `Message='Inserted Successfully'` · 4,589 ms |
| 4 | `ServiceDetails/GetServiceDetails` | `${NEW_SERVICE_ID}` | `SERVICE_SESSION_ID`, `FETCHED_HOSTNAME` | `75293`, `10.11.0.48` · 1,672 ms |
| 5 | `ServiceDetails/GetActiveServicesByLOBId` | `${LOB_ID}` | — asserts presence | `ServiceId=25342` **found** · `'17 - Records Found'` · 815 ms |

**Level 5 is the point.** It returns to the LOB the chain started from and proves the service was
*registered against it* — not merely that a POST was accepted.

Three mechanics that make it work, each a workaround for a contract defect:

```jsonc
// 1. Find the row; never assume Result[0]
"find_extract": { "in": "Result", "where": {"LobName": "AUTOMATION_TEST_LOB"},
                  "take": {"LOB_ID": "LobId", "LOB_NAME": "LobName"} }

// 2. ServiceId returns as a STRING; hop 4 requires a NUMBER
"extract": { "NEW_SERVICE_ID": "Result[0].ServiceId" },
"cast":    { "NEW_SERVICE_ID": "int" }

// 3. Independent proof, not a status check
"verify_present": { "in": "Result", "match_field": "ServiceId", "value": "${NEW_SERVICE_ID}" }
```

⚠️ `Result` is an **array** at level 3 and an **object** at level 4 — same chain, same run. Any extractor
must handle both (§10).

### 8B. Password request and approval — designed, not yet automated via API

| Step | Endpoint | Consumes | Publishes |
|---:|---|---|---|
| 6 | *raise request* | `${NEW_SERVICE_ID}`, `${LOB_ID}`, requester `UserID` | **`TransID`**, `CurrentStatusID` |
| 7 | `NotificationDetails/GetPendingNotificationsCount` | approver `UserID` | pending count |
| 8 | `NotificationDetails/GetServicePasswordRequestNotification` | approver `UserID` | request list incl. `TransID` |
| 9 | `NotificationDetails/ViewServicePasswordRequest` | `UserID`, `${TransID}`, `CurrentStatusID` | `CurrentApprovalLevel`, `LastApprovalLevel` |
| 10 | **`NotificationDetails/ServicePasswordRequestApproveReject`** | `UserID`, `LstSPPR[{TransID, CurrentStatusID}]`, `Type='Approve'`, `Comment` | advances the level |
| 11 | *repeat 7–10 as L2, L3, L4, L5* | each approver's own `UserID` | — |
| 12 | `ServicePassword/GetServicePwdReqWorkflowLogs` | `${TransID}` | per-level audit trail |
| 13 | `NotificationDetails/GetMailBoxNotification` | requester `UserID` | password delivery entry |

⛔ **Step 6 has no confirmed endpoint.** The raise-request API is not identified in `APIConfig.java`; the
reference test raises the request **through the UI**
(`getservicePasswordPage().raiseServicePasswordRequest_New(...)`). Marked `UNKNOWN` in §25 rather than
guessed — inventing an endpoint name here would be the worst possible failure of a context document.

---

## 9. Request payloads

Field metadata from `tools/source-map.json`. **`Provenance`** matters as much as the value:
`payload-helper` = a hand-written literal in the framework; `confluence` = the 2,470-page export;
`pam-model` = a C# class in `pam/PAM`.

### 9.1 `POST /api/ServiceCreation/SetServiceDetails` — the create

**Confluence:** `pam-api.md:p2122`, `p2125`

| Field | C# type | Provenance | Chainable | Mandatory? |
|---|---|---|---|---|
| `LOBID` | `Int64` | payload-helper · pam-model | ✅ | ⚠️ **not declared** |
| `ServerGroupId` | `List<int>` | payload-helper · pam-model | ✅ | ⚠️ not declared |
| `Hostname` | `String` | payload-helper · pam-model | — | ⚠️ not declared |
| `IPAddress` | `IPAddress` | payload-helper · pam-model | — | ⚠️ not declared |
| `Domain` | `String` | payload-helper · pam-model | — | ⚠️ not declared |
| `ServiceTypeId` | `int` | payload-helper · pam-model | ✅ | ⚠️ not declared |
| `DBInstanceName` | *unknown* | payload-helper only | — | ⚠️ not declared |
| `ServiceUserName` | `string` | payload-helper · pam-model | — | ⚠️ not declared |
| `ServicePassword` | `string` | payload-helper · pam-model | — | ⚠️ not declared |
| `Description1/2/3` | `string` | payload-helper · pam-model | — | ⚠️ not declared |
| `Parameter` | *unknown* | payload-helper only | — | ⚠️ not declared |
| `ServiceID` *(response)* | `long` | confluence · pam-model | ✅ | — |

⛔ **`required_hint = false` on every single field.** Not one field in this payload is declared mandatory
anywhere. Project-wide: **3** of ~6,738 properties carry `[Required]`, and all three sit on a class in a
service that is not among the 70 controllers — so **on the surface under test the declared-mandatory count
is 0 of 5,175**. There is also **no** max-length, format, pattern or enum metadata: 12 constraint families
return zero across `pam/PAM`. Consequence: the payload below is **inferred**, and a "missing mandatory
field" negative test cannot be authored honestly. Detail: `docs/analysis/A5-mandatory-field-analysis.md`.

Actual body used by the working flow — randomised fields marked:

```jsonc
{
  "LOBID":            "${LOB_ID}",             // 108, from level 1
  "ServerGroupId":    "${SERVER_GROUP_ID}",    // 282, from level 2
  "Hostname":         "${NEW_SERVICE_HOST}",   // randomised per run  <-- see below
  "IPAddress":        "${NEW_SERVICE_HOST}",   // randomised per run
  "Domain":           "2",
  "ServiceTypeId":    1,                       // Windows RDP
  "DBInstanceName":   "",
  "ServiceUserName":  "${NEW_SERVICE_USER}",   // randomised per run
  "ServicePassword":  "${NEW_SERVICE_PASSWORD}",
  "Description1":     "", "Description2": "", "Description3": "",
  "Parameter":        "1",
  "Port":             "${NEW_SERVICE_PORT}",   // randomised per run
  "AllowPasswordChange": 1,
  "Vault_Password_Immediately": 1
}
```

⚠️ **Randomisation is mandatory, not hygiene.** The owner's originally verified payload returned
`Success: true` with `Message: "Already Exists"` — it created **nothing**, while HTTP status and the
`Success` flag were both green. Randomising host, IP, user and port is what makes this a genuine insert.

### 9.2 `POST /api/NotificationDetails/ServicePasswordRequestApproveReject` — the approval

**Confluence:** `pam-api.md:p1868`

| Field | C# type | Provenance | Notes |
|---|---|---|---|
| `UserID` | `long` | payload-helper · pam-model | The **approver's** id, not the requester's |
| `LstSPPR` | list | payload-helper | Array of `{TransID, CurrentStatusID}` — batch-capable |
| `Type` | `string` | payload-helper · pam-model | `"Approve"` / `"Reject"` — ⚠️ enum values **not documented**, taken from the example |
| `Comment` | *unknown* | payload-helper | Free text |

```jsonc
{
  "UserID": 36,                                     // approver identity for this level
  "LstSPPR": [ { "TransID": "${TRANS_ID}", "CurrentStatusID": "1" } ],
  "Type":    "Approve",
  "Comment": "Approving"
}
```

### 9.3 Supporting payloads

```jsonc
// GetServicePasswordRequestNotification    p1866
{ "UserID": 36 }

// ViewServicePasswordRequest               p1871, p1872
{ "UserID": 36, "TransID": "972f911", "CurrentStatusID": "1" }
//   -> returns CurrentApprovalLevel, LastApprovalLevel

// GetServicePwdReqWorkflowLogs
{ }   // ⛔ fields = {} and sources = [] in source-map: NO payload metadata exists at all
```

---

## 10. Response expectations

### ⛔ The single most important fact about this API

**A rejected request normally returns HTTP 200 with the rejection in the body.** An assertion that checks
only the status code **passes against a fully rejected request**.

Measured: **1,688 of 1,868** calls returned HTTP 200; **289** of those carried an application-level failure.
A status-only suite scored the run **90% green** against a true **64%**.

### 10.1 The envelope

```jsonc
{ "Program": "ARCON PAM API", "Version": "1.0", "DateTime": "27/Oct/2020 07:17:59",
  "Success": true, "Message": null, "ErrorCode": null, "ErrorMessage": null,
  "Result": [ /* ... */ ] }
```

Error form — **still HTTP 200**:

```jsonc
{ "Success": false, "ErrorCode": "206-LC_GLD",
  "ErrorMessage": "Parameter error occurred - Required property 'LogTypeId' not found" }
```

### 10.2 Shape variance — 31 measured, 6 documented

| What breaks a fixed-shape client | Count |
|---|---:|
| Responses that are not JSON objects at all | 127 |
| Responses with **no `Success` field** | 288 |
| `Result` values that are not arrays (object, string, bool, int) | 139 of 1,291 |
| Bodies that are a naked `true`/`false` | 2 |
| Responses lacking the `Program`/`Version`/`DateTime` frame | 291 |

⚠️ **Field casing varies too, and it is not cosmetic.** The framework's own envelope assertion read
`success` in camelCase; across all 1,868 responses lowercase appears in **0** and PascalCase `Success` in
**1,580**. Jackson is case-sensitive, so that assertion **could never pass** — one letter silently disabled
an entire validation layer. Fixed under `OBJ-007` by routing all access through
`com.arcon.utils.validation.PamEnvelope`.

### 10.3 ⛔ `Success: true` is not evidence of a write

`POST /api/ServiceCreation/SetServiceDetails` returns `Success: true` with `Message: "Already Exists"` when
the record exists — nothing inserted, status and flag both green. **70** such responses were measured; the
framework caught **0** of them.

**So a create must be judged on `Message` semantics:**

| `Message` | Means |
|---|---|
| `"Inserted Successfully"` | ✅ a row was written |
| `"Already Exists"` / `"Record Already Exists."` | ⛔ **no-op** — must fail an insert assertion |
| absent | cannot be judged from the response; needs read-back or DB (§12) |

⚠️ The wording **varies** (`"Already Exists"` vs `"Record Already Exists."`), so match on patterns, never
literals or a per-endpoint allowlist.

### 10.4 Expected responses for this flow

| Hop | Expected |
|---|---|
| `GetLOBList` | 200 · `Success:true` · `Result[]` containing `LobName = AUTOMATION_TEST_LOB` · **no `Message` field** |
| `GetServerGroupList` | 200 · `Success:true` · `Result[]` non-empty |
| `SetServiceDetails` | 200 · `Success:true` · **`Message = 'Inserted Successfully'`** · `Result[0].ServiceId` present, non-empty, castable to int |
| `GetServiceDetails` | 200 · `Success:true` · `Message = 'Operation Successfull'` · **`Result` is an OBJECT** |
| `GetActiveServicesByLOBId` | 200 · `Success:true` · `Message = 'N - Records Found'` · `Result[]` contains the new `ServiceId` |
| `ServicePasswordRequestApproveReject` | `NOT DOCUMENTED` — never exercised. Envelope shape from `p1868` shows `Success`/`ErrorCode`/`Result`; the **success `Message` is unknown** |

---

## 11. Validation points

Twelve layers, from `com.arcon.utils.validation.ValidationLayer`. `L1`–`L7` match the Python harness so
results compare directly; `L8`–`L12` were added under `OBJ-007`.

| Layer | Check | Applied to this flow |
|---|---|---|
| `L1` | http-status | 200 at every hop — **weakest signal here** |
| `L2` | content-type | `application/json` |
| `L3` | envelope | `Success:true`; on a bare-array endpoint → `NOT_APPLICABLE`, not `FAIL` |
| `L4` | message-semantics | **`'Inserted Successfully'` at the create; `'Already Exists'` must FAIL** |
| `L5` | chain-key-extracted | `ServiceId` present and non-empty — the hop that gates everything downstream |
| `L6` | record-exists | `ServiceId` found in `GetActiveServicesByLOBId` |
| `L7` | latency | per-hop SLA (§18) |
| `L8` | schema | expected fields present and correctly typed |
| `L9` | mandatory-fields | ⚠️ mostly `NOT_RUN` — nothing is declared mandatory (§9.1) |
| `L10` | business-rule | §13 — mostly `NOT_RUN`, no documented rules |
| `L11` | db-persistence | §12 |
| `L12` | security | no leaked stack traces, SQL exceptions or connection strings |

### ⚠️ `NOT_RUN` is a first-class verdict, distinct from `PASS` and `FAIL`

A check that could not run is **never** reported as a pass, and never as a product failure. This is not
pedantry — it is the lesson from the most misleading number this project produced: **105 of 107** `L6`
read-backs were recorded `FAIL` when **97** of them had searched each response for the literal string
`${NEW_ID}` and could never have passed. Those verdicts carried no information about the product and were
being read as product defects.

```java
new PamApiValidator("POST", APIConfig.setServiceDetails, response, elapsedMs)
    .expectStatus(200).expectJson().expectSuccess()
    .expectInserted()                                   // L4 - fails on "Already Exists"
    .expectFields("ServiceId").expectFieldType("ServiceId", Integer.class)
    .expectMandatory("ServiceId")                       // L9
    .expectChainKey("ServiceId")                        // L5
    .expectPersisted(DbPersistenceValidator.recordExistsById(
        "sso_services", "ss_service_id", "ServiceId"))  // L11
    .expectNoServerInternals()                          // L12
    .withinMs(8000)                                     // L7
    .validate().assertAll();
```

---

## 12. Database validation points

Read-only, `ARCOSDB_U16SP2_WEBSM_QA` on `10.10.0.194,1433`. The API's writes **do** land there — confirmed
three ways (audit log naming the objects in plaintext, business rows stamped `created_by='SYSTEM_API'`, and
194 `ArconPamApiLog` rows from the runner).

| # | Assertion | SQL |
|---:|---|---|
| 1 | The service row exists | `SELECT COUNT(*) FROM dbo.sso_services WHERE ss_service_id = ?` |
| 2 | It is linked to the LOB | `SELECT COUNT(*) FROM dbo.sso_lobs_services WHERE lsg_sls_id = ? AND lsg_ss_service_id = ?` |
| 3 | The request record exists | `SELECT COUNT(*) FROM dbo.sso_arcos_wft_details WHERE wft_trans_id = ?` |
| 4 | It is configured for 5 levels | `SELECT wft_approval_levels FROM dbo.sso_arcos_wft_details WHERE wft_trans_id = ?` → `5` |
| 5 | The right approvers are assigned | `SELECT wft_approver_l1_user, …, wft_approver_l5_user FROM dbo.sso_arcos_wft_details WHERE wft_trans_id = ?` — **plaintext** |
| 6 | Each level recorded a decision, timestamp, comment | `SELECT wft_approver_l1_status, wft_approver_l1_status_on, wft_approver_l1_comment, … WHERE wft_trans_id = ?` |
| 7 | Levels advanced **in order** | `wft_approver_l1_status_on <= l2_status_on <= … <= l5_status_on` |
| 8 | The audit trail is complete | `SELECT COUNT(*) FROM dbo.sso_arcos_wft_details_approver WHERE …` |

### Constraints on DB validation — real, and they shape the design

| Constraint | Consequence |
|---|---|
| **Some columns are encrypted at rest** | `sso_lobs.sls_name`, `sso_users.ssu_username`, `sso_services.ss_username`/`ss_server_ip`/`ss_server_host`/`ss_port` hold base64 ciphertext. **Validate by integer key, never by business name.** `recordExistsByName` returns `INCONCLUSIVE` — not `FAIL` — when it detects ciphertext |
| **Encryption is narrow** | Approver usernames, all keys, and all `created_on`/`modified_on` are **plaintext** — which is what makes assertions 5–7 possible |
| **Status codes undocumented** | Assertion 6 can prove a decision was *recorded*; it cannot prove *what* was decided (§5.2) |
| **Audit over-reports creates 6:1** | An audit row is **not** evidence of a write. Pair every audit check with a business-row check |
| **Concurrent activity** | Only 2 of 6 creations in the run window were the test's. **Never assert on a bare `COUNT(*)` delta** — add `created_by = 'SYSTEM_API'` or the runner IP |
| **Deterministic encryption** | One key, no IV — functionally AES-ECB (20,651 rows → 59 distinct `ss_port` ciphertexts). Ciphertext-equality lookups *work*, but do not build on it: it is a security defect that should be fixed |

⛔ **`SELECT` only.** The supplied `devops` login is `sysadmin` over **31** databases, several not QA.
`DBUtils` refuses any non-`SELECT` unless `allowMutations()` is called explicitly, and requests driver-level
read-only (accepted, verified). A least-privilege account should replace it before CI use — `MF-08`.

---

## 13. Business rules

| # | Rule | Documented? | Testable now? |
|---:|---|---|---|
| BR-1 | The password is not obtainable until **all 5** levels approve | ⛔ inferred from behaviour | 🟡 via DB (§12 #6–7) |
| BR-2 | Approvals are **strictly sequential** | ⛔ inferred from `CurrentApprovalLevel` | 🟡 via DB timestamp ordering |
| BR-3 | An approver may act **only at their own level** | ⛔ not documented | ⬜ needs the authorisation matrix (§25) |
| BR-4 | A **rejection at any level** terminates the chain | ⛔ not documented | 🟡 UI test asserts a rejection message |
| BR-5 | `AccessType = One Time` means the grant is single-use | ⛔ not documented | ⬜ no test |
| BR-6 | A workflow must be **Enabled** to take effect | ✅ AdminUI field | ✅ |
| BR-7 | Only **one** workflow per LOB + request type is active | 🟡 implied by `disableAllEntries` | 🟡 |
| BR-8 | A service must belong to a server group within the LOB | ✅ enforced by the create payload | ✅ |
| BR-9 | Duplicate service → `Already Exists`, **not** an error | ✅ measured | ✅ |
| BR-10 | The requester must have service access in that LOB | ✅ GC `allowServiceAccess` | ✅ |

⚠️ **Eight of ten rules are inferred from observed behaviour, not documented.** A test built on an inferred
rule freezes today's behaviour — including any defect in it. This is why `L10` reports `NOT_RUN` rather than
inventing an assertion. The fix is a published business-rule specification — `MF-01`.

---

## 14. Edge cases

| # | Case | Expected | Status |
|---:|---|---|---|
| EC-1 | Approver 3 rejects after 1 and 2 approved | Chain terminates; levels 4–5 never actionable | 🟡 UI only |
| EC-2 | The same user is set as approver at two levels | `UNKNOWN` — does level 2 auto-satisfy? | ⬜ untested |
| EC-3 | An approver is deleted mid-chain | `UNKNOWN` | ⬜ untested |
| EC-4 | Workflow disabled while a request is pending | `UNKNOWN` | ⬜ untested |
| EC-5 | `ApprovalLevels` reduced 5 → 3 mid-chain | `UNKNOWN` | ⬜ untested |
| EC-6 | Two requests for the same service by the same user | `UNKNOWN` — dedupe or two `TransID`s? | ⬜ untested |
| EC-7 | Request raised against a **deleted** service | Should fail — **16,560 dangling authorisation rows exist**, so referential integrity is not enforced | ⬜ untested |
| EC-8 | `openForHours` boundary (0, max, negative) | `UNKNOWN` — no length/range metadata | ⬜ untested |
| EC-9 | Access window expires before final approval | `UNKNOWN` | ⬜ untested |
| EC-10 | Approval delegation active (`sso_arcos_wft_delegation_master`, 26 rows) | Delegate may approve | ⬜ untested |
| EC-11 | Service created into a server group in a **different** LOB | Should be rejected | ⬜ untested |
| EC-12 | Duplicate create — the `Already Exists` path | `Success:true`, no insert | ✅ measured |

⚠️ **Ten of twelve are `UNKNOWN`,** because the behaviour is undocumented and the flow has no API automation.
Listing them as unknown is the correct output — an AI asked to "test the edge cases" without this section
would invent expected results for all ten.

---

## 15. Negative scenarios

⚠️ **The expected status is usually `200`, not `4xx`** — the rejection is in the body (§10).

| # | Scenario | Expected | Status |
|---:|---|---|---|
| NS-1 | Missing mandatory field on the create | `UNKNOWN` — no field is declared mandatory (§9.1) | ⬜ unassertable |
| NS-2 | `LOBID` as a string where `Int64` expected | 200 + `Success:false` + an error code | ⬜ |
| NS-3 | Non-existent `LOBID` (e.g. `999999`) | 200 + `Success:false` | ⬜ |
| NS-4 | `ServerGroupId` from another LOB | Should reject (EC-11) | ⬜ |
| NS-5 | Malformed `IPAddress` | `UNKNOWN` — no format metadata | ⬜ |
| NS-6 | Oversized `Hostname` | `UNKNOWN` — no max-length metadata | ⬜ |
| NS-7 | No / invalid bearer token | **401** — framework-level, no envelope | ✅ asserted today |
| NS-8 | Wrong HTTP verb (GET on a POST endpoint) | **405** | ✅ asserted today |
| NS-9 | Approve with a `TransID` that does not exist | `ErrorMessage: "No Record Found"` (per `p1868`) | ⬜ |
| NS-10 | Approve at a level that is not current | Should reject (BR-3) | ⬜ |
| NS-11 | Approve as a user who is not an approver | Should reject | ⬜ needs a second identity |
| NS-12 | Approve an already-approved request | `UNKNOWN` | ⬜ |
| NS-13 | `Type` value outside `Approve`/`Reject` | `UNKNOWN` — enum not documented | ⬜ |
| NS-14 | SQL-injection string in `Comment` | Rejected or safely escaped; **no SQL error leaked** (`L12`) | ⬜ |
| NS-15 | Malformed JSON body | 400 or 200 + error | ⬜ |

**Project-wide context:** 10,448 negative scenarios were designed across all 1,306 endpoints. **7,664
(73.4%) have no documented expected outcome**, and **1,289 of 1,306 endpoints (98.7%)** have zero runnable
negative coverage today. The existing suite asserts little beyond 401/404/405 — and **199 of 279** of its
referenced data providers do not exist, while the 80 that resolve read the **positive** sheets. Detail:
`docs/analysis/A3-negative-validation.md`, `MF-12`.

---

## 16. Test scenarios

| ID | Scenario | Level | Automation | State |
|---|---|---|---|---|
| `SC-01` | Service creation, 5-hop chain | API | `tools/flows/03_service_lifecycle.json` | ✅ **PASS**, measured |
| `SC-02` | Zero-level request (no approval) | UI | `ServicePasswordRequestZeroLevelTest` | ✅ exists |
| `SC-03` | One-level approval | UI | `ServicePasswordRequestOneLevelTest` | ✅ exists |
| `SC-04` | Two-level approval | UI | `ServicePasswordRequestTwoLevelTest` | ✅ exists |
| `SC-05` | Three-level approval | UI | `ServicePasswordRequestThreeLevelTest` | ✅ exists |
| `SC-06` | Four-level approval | UI | `ServicePasswordRequestFourLevelTest` | ✅ exists |
| `SC-07` | **Five-level approval** | UI | `ServicePasswordRequestFiveLevelTest` | ✅ exists |
| `SC-08` | One-level, negative | UI | `ServicePasswordRequestOneLevelTest_Negative` | ✅ exists |
| `SC-09`…`SC-12` | Two/Three/Four/Five-level, negative | UI | `…LevelTest_N` | ✅ exist |
| `SC-13` | Request-log verification | UI | `ServicePasswordRequestLogTest` | ✅ exists |
| `SC-14` | PAM-logs verification | UI | `ServicePasswordRequestLogsTest` | ✅ exists |
| `SC-15` | Workflow teardown | UI | `…WorkflowDeleteTest` (priority 2) | ✅ exists |
| `SC-16` | **Five-level approval via API** | API | `fiveLevelServicePasswordRequestTestWithAPI` | ⛔ **commented out** (lines 219–359) |
| `SC-17` | DB validation of the approval chain | DB | — | ⬜ **not built** (§12 is the design) |

⚠️ **Two caveats on the "✅ exists" rows.** (a) In the live five-level path the message assertions are
**commented out** — `requestStatus(approverStatus, expectedMessageAfterApproved, expectedMessageAfterReject)`
at lines 115–116, 125–126, 135–136, 145–146, 155–156 — replaced by
`approveSRPRequest(approverStatus, "Approving")`. So the approvals execute but their expected messages are
**not asserted**. (b) The reset-configuration teardown is also commented out (lines 189–196), so the
environment is left mutated.

---

## 17. Expected outcomes

| Scenario | Pass criteria |
|---|---|
| `SC-01` | All 5 hops HTTP 200 · `Success:true` · create returns `'Inserted Successfully'` **and** a non-empty `ServiceId` · `ServiceId` present in the LOB's active list · every hop within SLA. **Measured: PASS** |
| `SC-07` | Workflow created (`workflowCreationMessage`) · request raised (`raisedRequestSuccessMessage`) · visible in Pending Requests · **each of 5 approvals recorded** · L1–L4 show `expectedMessageAfterApproved`, L5 shows `expectedMessageAfterLastApproved` · Approval Log per level · Request Log = Approved · report renders · **password present in the ACMO mailbox** |
| `SC-08`…`SC-12` | Rejection at the configured level yields `expectedMessageAfterReject`; the chain does **not** advance; **no password is delivered** |
| `SC-15` | Workflow deleted (`workflowDeletionMessage`); environment returns to baseline |
| `SC-16` | *(when built)* Same as `SC-07`, asserted through §8B with `L1`–`L12` |
| `SC-17` | *(when built)* §12 assertions 1–8 all pass |

**The decisive assertion for the whole flow:** after the **fourth** approval, no password exists in the
requester's mailbox; after the **fifth**, it does. That single before/after pair is what proves the business
control works — everything else is supporting evidence.

---

## 18. Non-functional expectations

| Aspect | Expectation | Measured |
|---|---|---|
| Read-hop latency | ≤ 5,000 ms | 58–815 ms ✅ |
| Create latency | ≤ 8,000 ms | **4,589 ms** — over half the budget ⚠️ |
| Read-back latency | ≤ 8,000 ms | 1,672 ms ✅ |
| SLA breaches, whole run | — | **13 of 1,868** |
| Concurrency | Framework runs `parallel="classes"` | ⚠️ `APIExcelReportUtil` has an unsynchronised static row index — report rows can overwrite. Fix before scaling (`MF-10`) |
| Approval chain duration | Human-paced; no SLA defined | `UNKNOWN` |

---

## 19. Required datasets

| Dataset | Where | State |
|---|---|---|
| Run-seed variables | `chain_runner.py` seed: `NEW_SERVICE_HOST`, `NEW_SERVICE_USER`, `NEW_SERVICE_PASSWORD`, `NEW_SERVICE_PORT`, `RUN_SUFFIX` | ✅ generated per run |
| Flow definition | `tools/flows/03_service_lifecycle.json` | ✅ |
| UI data provider | `raiseFiveLevelServicePasswordRequest` (32 columns) in `UI_DataProviderUtils` | ✅ |
| API positive data | `testdata/API_Automation_Test_Input_Data.xls` → `AllApiPositiveScenarios` (1,865 rows) | ⚠️ contains 102 blocklisted rows — §20 |
| API negative data | `testdata/Negative_API_Automation_Test_Input_Data.xls` (76 sheets) | ⛔ **read by no data provider** — `MF-12` |
| Approval-chain API data | — | ⬜ **does not exist**; needed for `SC-16` |
| Six user accounts | `Environments/QA_MsSQL.properties` | ✅ (plaintext) |
| Bearer token | `$env:PAM_API_TOKEN` | ⛔ must be supplied per run — §24 |

⚠️ **The negative workbook's row total is definition-dependent** — five figures circulate (3,167 · 3,317 ·
3,652 · 3,620 · 3,728) and none is wrong; they count different things. Quote the **stable** split instead:
`1,604 × 405` · `1,550 × 401` · `13 × 200`, with only **13 rows** testing application validation.

---

## 20. Safety constraints (absolute)

| ⛔ Rule | Why |
|---|---|
| **Never call `ActivityLogs/GetErrorLogs`, `ActivityLogs/GetLogs`, `GetAllActiveUserDetails`** | Three sequential calls stopped the IIS application pool and took the whole API to **503** with no self-recovery. **98** endpoints share these action names (`LH-08`); live re-validation is **forbidden** |
| **Guard on endpoint *names*, not verbs** | Deletion is `POST /api/<C>/Delete<Thing>` — a destructive call looks like an ordinary POST. In this flow: `SetDropService`, `SetDeleteService` |
| **Never retry a failed token request** | `GenericScheduler` is locked, and it is **also the data-warehouse ETL account** — a test-side lockout is a production-side outage |
| **Never replay a mutating call** | Approvals and creates are not idempotent. `SC-16` must generate fresh data, never replay captured requests |
| **Database: `SELECT` only, QA only** | The `devops` login is `sysadmin` over 31 databases |
| **Enforce at planning time** | Check the blocklist *before* a request is built, not after |

### 🔴 Live gap you must know about

The blocklist is enforced in this documentation and in the Python harness — **but not in the Java
framework's test data.** `AllApiPositiveScenarios` holds **102 rows across 50 controllers** targeting
blocklisted action names, all expecting HTTP 200, including rows 16–17 for `ActivityLogs`. `ActivityLogs` is
the single API class activated by `CICD_Suites/APISuite.xml` **and by a root `testng.xml`** that IDEs pick up
by convention. Recorded as `OBS-047` / `MF-16` (P0). **A documented safety rule does not protect the
automated path** — that is the lesson.

---

## 21. Known defects affecting this flow

So an AI does not chase a product defect as a test defect.

| ID | Defect | Effect here |
|---|---|---|
| `LH-01`/§1 | HTTP 200 for application-level failures | Status assertions are worthless (§10) |
| `LH-02`/§2 | `Success: true` when nothing was created | Create assertions must read `Message` |
| `LH-03`/§3 | 31 response shapes, 6 documented | Needs `PamEnvelope` normalisation |
| `LH-04`/§4 | Error-code register incomplete (**3** documented for 1,306 endpoints) | Negative expectations cannot be derived |
| `LH-05`/§5 | 135 declared endpoints return 404 | A 404 may be a catalogue defect, not a product one |
| `LH-09`/§9 | **Service passwords returned in cleartext** | `GetServiceDetails` returns the password; evidence writers must redact |
| `LH-10`/§10 | No validation attributes on request models | §9.1, §15 |
| `MF-15` | Deterministic encryption · cleartext API passwords · 16,560 dangling authorisation rows | §12, EC-7 |
| `OBS-043` | `CallBack` background loop logs ~240 errors/hour continuously | Inflated the run window 194 → 1,736. **Exclude it** before quoting any error rate |
| `OBS-049` | Test-data corruption — e.g. `ck/api/Us/nv/gg/bnerLabels/GetErrorLogs` | A 404 may be a mangled path |

---

## 22. Documentation references

| Source | What it gives this flow | Limits |
|---|---|---|
| `pam-api.md:p2122`, `p2125` | `SetServiceDetails` payload | Bound **by page proximity** — a binding can be wrong |
| `pam-api.md:p1866`, `p1868`, `p1871`, `p1872` | Notification / approval payloads | Same caveat |
| `pam-api.md:p1802`, `p1804-1807` | `GetLOBList`, `GetServerGroupList` | Same |
| `pam-api.md:p653`, `p655`, `p790`, `p792`, `p924`, `p925`, `p930`, `p969`, `p971`, `p1073` | Service-detail reads | Same |
| **Confluence export overall** | 3,194 payload examples, **1,605–1,654** endpoint-bound | 70% of endpoints undocumented · **3** error codes · **6 of 31** shapes · owner confirms **not up to date** |
| Two administrator guides (1,101 pp) | Access model, product concepts | ⛔ **no endpoints, schemas or error codes** |
| Swagger (37 specs / 690 ops) | ⛔ nothing for this flow | Different surface, ~6% overlap, **0** declare 4xx/5xx |
| `pam/PAM` | C# property names and types | **48 of 1,306** endpoints (3.7%); **58 of 70** controllers absent |
| `docs/analysis/A1`…`A7`, `B`, `C` | The measured analysis behind every figure here | — |
| `artifacts/workbooks/PAM-Project-Knowledge-Base.xlsx` | 241 Q&A rows, all cited | — |

**Access method — mandatory.** ⛔ Never read `artifacts/rag-corpus/pam-api.md` directly (101,803 lines).
Use `python tools\rag\query.py find "<terms>"` or `page <doc> <N>`, and cite as `<doc>:p<N>`.

---

## 23. Assumptions

Stated so they can be challenged. Each is a candidate defect if wrong.

| # | Assumption | Basis | Risk if wrong |
|---:|---|---|---|
| A-1 | `ServiceTypeId = 1` is Windows RDP | flow definition + observed `ServiceWindowTitle` | Wrong service type created |
| A-2 | `Domain = "2"` is a valid domain id in QA | working payload | Create fails |
| A-3 | `UserId = 35` / `UserSessionId = 1` are a valid session context | owner's verified call | Read-back fails |
| A-4 | `Type` accepts exactly `Approve`/`Reject` | payload-helper example only | Approval silently ignored |
| A-5 | `CurrentStatusID = "1"` means "pending" | example only | Wrong request targeted |
| A-6 | Approver `UserID` is the PAM user id | field naming + type | Approval recorded against the wrong user |
| A-7 | `wft_trans_id` is the same value as the API's `TransID` | naming | DB assertions target the wrong row |
| A-8 | Approvals must be sequential | `CurrentApprovalLevel`/`LastApprovalLevel` exist | BR-2 test invalid |
| A-9 | The QA API writes to `ARCOSDB_U16SP2_WEBSM_QA` | ✅ **verified three ways** | *(no longer an assumption)* |
| A-10 | The 5 approver accounts have approver permission in the LOB | UI test passes | Approvals rejected |

---

## 24. Dependencies

| Dependency | Owner | State | Blocks |
|---|---|---|---|
| **A working bearer token** | Project owner | ⛔ locked account; last committed token **expired 2026-07-31** | All API execution |
| A dedicated non-shared API service account | IT Operations | ⛔ not provisioned | Unattended CI (`MF-04`) |
| Least-privilege QA DB login | DBA | ⛔ only `sysadmin` supplied | `L11` in CI (`MF-08`) |
| **Error-code register** | PAM Development | ⛔ 3 of ~108 observed codes documented | All negative expectations (`MF-01`) |
| **Approval status-code lookup** (0/3/9) | PAM Development | ⛔ undocumented | BR-1, BR-2 assertions |
| **Business-rule specification** | PAM Development | ⛔ 8 of 10 rules inferred | `L10` |
| **Endpoint-to-role/LOB matrix** | PAM Development | ⛔ does not exist | BR-3, NS-10, NS-11 |
| The **raise-request endpoint** | PAM Development | ⛔ not identified | `SC-16` step 6 |
| Source of the enforcing request models | PAM Development / Architecture | ⛔ not in `pam/PAM` — 12 constraint families return zero yet the server runs the checks (**123** live rejections) | §9.1, `MF-13` |
| `JAVA_HOME` override each session | QA Automation | 🟡 manual: `C:\Program Files\Eclipse Adoptium\jdk-21.0.11.10-hotspot` | Any Maven run |
| Workflow LOB/user mapping data | QA Automation | ⛔ 3 tables hold 0 rows | Scoped-workflow tests |

---

## 25. What is NOT known

The section most context documents omit, and the one that prevents the most wasted work.

| # | Unknown | What would settle it |
|---:|---|---|
| U-1 | Meaning of approver status `0` / `3` / `9` | A status-code lookup from Development |
| U-2 | The raise-request API endpoint | The endpoint name, or confirmation it is UI-only |
| U-3 | Which fields are genuinely mandatory | `[Required]` on the models, or a published spec |
| U-4 | Field lengths, formats, patterns, enums | Same |
| U-5 | Complete error-code register | Development (`~108` observed ≠ a contract) |
| U-6 | Success `Message` for `ServicePasswordRequestApproveReject` | One live call, or documentation |
| U-7 | Whether an approver can act out of turn | Authorisation matrix + a second identity |
| U-8 | Behaviour of EC-2…EC-11 (ten edge cases) | Business-rule specification |
| U-9 | Whether `AccessType = One Time` is enforced | Specification + a test |
| U-10 | Response schema for any endpoint in this flow | An OpenAPI document |
| U-11 | Whether the 19 acknowledged-but-idless creates inserted a row | A read-only `SELECT` on submitted business fields |
| U-12 | Whether the Jenkins API job is enabled | Jenkins configuration — **material**, because of §20's live gap |

⛔ **None of the above is guessed anywhere in this document.** An AI given a plausible invention builds on
it confidently and the error surfaces late, disguised as a product defect.

---

## 26. Traceability

| Artifact | Location |
|---|---|
| Measured run | `artifacts/runs/2026-07-29_181439/` — `results.json`, `evidence/` (1,868 files) |
| The passing flow | `results.json` → flow `service_lifecycle`, verdict `PASS`, 5 hops |
| Flow definition | `tools/flows/03_service_lifecycle.json` |
| UI reference test | `…/UI/EndToEnd/raiseRequestServicePassword/ServicePasswordRequestFiveLevelTest.java` |
| Validation framework | `src/test/java/com/arcon/utils/validation/` (7 classes, 1,568 lines) |
| Framework verification | `…/tests/API/Validation/PamValidationLayerTest.java` — 15 tests, all passing |
| Analysis reports | `docs/analysis/A1`…`A7`, `B`, `C` |
| Row-level evidence | `artifacts/workbooks/PAM-API-Validation-Analysis.xlsx` |
| Risks and owners | `artifacts/workbooks/PAM-Project-Governance.xlsx` → `Management Findings` |
| Q&A knowledge base | `artifacts/workbooks/PAM-Project-Knowledge-Base.xlsx` — 241 rows |
| Developer findings | `docs/briefs/developer-loopholes.md` → `artifacts/loopholes/LH-NN-*/` |
| Jira | `PAMIT-42744` (LH-01) raised · LH-02…12 drafted, **held** |

---

## Closing note — what makes this a gold standard

Not its length. Three properties:

1. **Every figure is traceable**, and every gap is labelled `UNKNOWN` with what would settle it. The
   document is as useful for what it refuses to claim as for what it states.
2. **It distinguishes what is validated from what is validatable.** `SC-07` exists; its message assertions
   are commented out. `SC-16` is designed and not built. Both are said plainly.
3. **It carries the traps, not just the happy path.** HTTP 200 on failure · `Success: true` with no write ·
   31 response shapes · a casing mismatch that disabled a whole layer · a blocklist absent from the one path
   that runs unattended. An AI given only the happy path will reproduce the happy path — and report success.
