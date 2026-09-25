# Findings — what the product guides tell us

**Corpus:** `data/sources/` — 1,101 pages, PAM version U10, ARCON © 2025. Usage: [`README.md`](./README.md).
**Role:** this file is the **documentary evidence layer** — what the guides say, page-cited. Decisions built
on it live in `BLAST/Objective.md`; measured evidence (execution results, defects) lives in `Reports/`.
Both cite this file rather than restating it.
**Verify any claim with** `python tools\rag\query.py page <doc> <N>` (from the workspace root).

---

## 1. Summary

The guides contain **no API contract** — no endpoints, no schemas, no error codes (§6). They do not reduce
the need to discover the API surface elsewhere. What they supply is the access model, the module taxonomy,
and the domain vocabulary:

| Question source alone could not answer | Guide answer | Section |
|---|---|---|
| Who may call the API, and how is that granted? | An **API User** account type with a three-way **Access Type** scope | §2 |
| Why would a valid-looking request still be refused? | **Web API Registration** — an IP/MAC allow-list on password endpoints | §3 |
| What do the 69 `APIConfig` module blocks correspond to? | 16 Admin + 8 ACMO product modules | §7 |
| Which modules matter most? | Purpose statements per module | §9 |

---

## 2. 🔑 The API surface is partitioned by Access Type

An API User is created at **Manager → Application Settings → API User List → + New User** with fields
`User Name`, `Password`, `Confirm Password`, `Email ID`, and **`Access Type`** — `client-manager:p101–102`.

`Access Type` takes three values — `client-manager:p102`: **ARCON PAM User Details** ·
**ARCON PAM Service Details** · **ARCON Service Creation**.

Stated purpose — `client-manager:p100`:

> "Allow granular control over who can interact with which API endpoints"

**Consequence.** A harness authenticating as a single API User will be refused across whole module groups —
and because PAM answers rejections as **HTTP 200 with an `errorCode`**, those refusals look like successes
unless the envelope is checked. Provision all three scopes and bind the right credential per module.

### Access Type → `APIConfig` module blocks

⚠️ *Name-based inference — verify against a live environment. Only the three Access Type values themselves
are documented.*

| Access Type | Module blocks it plausibly governs |
|---|---|
| **ARCON PAM User Details** | `User` · `UserDetails` · `UserDetailsV2/V3/V4` · `UserRegistration` · `UserRegistrationV2` · `UserDelegation` · `UserFavourites` · `UserLabels` · `UserOnboarding` · `UserRestrictCommand` · `UserServiceSession` |
| **ARCON PAM Service Details** | `ServiceDetails` · `ServiceDetailsV2/V3` · `ServiceType` · `ServicePassword` · `ServicePasswordV2` · `ServicePasswordDependancy` · `LobandService` · `Lob` |
| **ARCON Service Creation** | `ServiceCreation` · `RDPSServiceInsert` · `RDPSServiceInsertV2` · `DeviceOnboarding` · `RDPS` |
| **outside all three** | `Configuration` · `Logs` · `ActivityLogs` · `Policy` · `License` · `SIEM` · `HSMEntrust` · `HSMUtimaco` · `AWSKeyVault` · `AzureKeyVault` · `Encryption` · `DualFactor` · `Flooding` · `ATSConfiguration` · `ATSMapping` · `AGWPlus` · `NotificationDetails` · `Collaborations` · `ARSIMServer` · `ARCONLAMMiddleware` · `APEMTool` · `RAVPNSetting` · `RTSM` · `ProfileManagement` |

The last row is the significant one: **roughly a third of the module blocks fall outside all three
documented Access Types**, so they are presumably reachable only through the regular PAM token path.

## 3. 🔑 Web API Registration is an IP/MAC allow-list

> "Web API Registration helps you to register the user's machine IP address, where the user can view the
> password from the registered machine or laptop." — `pam-admin:p455`

**Settings → API → Registered Machines.** Fields: `Description`, `Requestor IP`, `Requestor MAC` —
`pam-admin:p456`. Requires the *ARCON PAM Web API Registration* privilege.

**Consequence.** `ServicePassword*` endpoints fail from an unregistered host regardless of credentials. The
CI agent's IP **and MAC** must be registered — a standing prerequisite on recycled or containerised agents.
This is a *second, independent* IP gate, additional to `ARCONProvisioningWebAPI`'s `enableWhiteList` handler.

## 4. Environment preconditions

| Precondition | Source |
|---|---|
| PAM and PAM API both on **HTTPS with a valid certificate**, or both on **HTTP without** — mixed mode unsupported | `client-manager:p104` |
| Each API registered in the in-product **Application List** as `Application Name` + `URL (with port)` + `Is Active`; one entry per name | `client-manager:p103–105` |
| Privileges: *API User Registration*; client users also need *Manager Menu Display* | `client-manager:p104` |

`pam_BaseAPIURL` in `Environments/<env>.properties` must agree with the Application List entry — a mismatch
produces environment-specific failures that look like code faults.

The transport rule retroactively explains `setIgnoreHTTPSErrors(true)` in `ApiHelper` — QA environments are
presumably on self-signed certificates.

## 5. ⚠️ The suite authenticates as the data-warehouse ETL account

`pam_APITokenUserName` / `pam_APITokenPassword` decode from Base64 to **`GenericScheduler`** /
`GenericScheduler123`. The guide identifies that account — `pam-admin:p320–321`:

> "**ARCOS Generic Scheduler:** This is responsible for transferring the data from ARCON PAM DB to the Data
> warehouse DB via ARCON PAM API."

`ApplicationName = GenericScheduler` is listed as a **Generic Scheduler service setting**, not a test account.

**Implications:** the suite runs with whatever privileges the ETL job holds — a scope nobody chose for
testing, and a plausible explanation for coverage gaps; test traffic is indistinguishable from production
ETL traffic in PAM's audit logs; and an administrator rotating those credentials breaks every API suite at
once. Provision a dedicated automation API User instead.

## 6. What the guides do *not* contain

Searched across all 1,101 pages:

| Sought | Hits | Consequence |
|---|---:|---|
| `error code` · `errorCode` · `status code` · `response code` | **0** | ⛔ `ExpectedErrorCode` cannot be populated from documentation — it must be baselined from live responses |
| Endpoint or route reference | 0 | ⛔ The API surface must be discovered from code, not docs |
| Request/response schemas | 0 | ⛔ Schemas must come from payload helpers or DTOs |
| `Swagger` · `OpenAPI` | 0 | Consistent with the source scan |

The `Success Tag` / `Error Tag` fields at `pam-admin:p450` belong to **outbound** Web API Configuration —
PAM calling third-party APIs — not to PAM's own inbound envelope. They confirm the pattern is idiomatic at
ARCON but document none of PAM's own codes.

## 7. Product module taxonomy — `pam-admin:p9–13`

**Admin (16):** Server Manager · Session Monitoring · AD Bridging · Digital Vault / Password Vault ·
Auto Onboarding · PAM Logs · My Vault (Admin) · Spection · Settings · IDAM · User Access Governance ·
Administrator Console · My Vault Enterprise · Access Control · User Discovery · Reports.

**ACMO (8):** Script Manager · Dashboard · My Services · My Preferences · Raise Request · Pending Request ·
Request Logs · My Activity.

## 8. Domain vocabulary for seed data

| Entity | Where | Note |
|---|---|---|
| LOB / Profile | `pam-admin:p455` | Already in `Environments/*.properties` as `LOBId` |
| Service · Service Type · Service Username · Service Reference Number | `client-manager:p99` | Access Logs column set |
| Session ID | `client-manager:p99` | "A unique session ID associated with each session" |
| Server Group | `pam-admin:p9` | Already present as `serverGroupId` |
| Critical Command | `pam-admin:p636` | Feeds `Command`, `UserRestrictCommand` |
| Workflow / Approval level | `pam-admin:p224`, `p379` | Feeds `Pending_LogRequests`, `TicketRequestDetails` |
| API User + Access Type | `client-manager:p102` | §2 |
| Registered Machine (IP + MAC) | `pam-admin:p456` | §3 |

**Cheapest fixture build:** the Access Logs grid at `client-manager:p99` exposes `Session ID`, `User ID`,
`User Machine`, `Service IP`, `Service Username`, `DB Instance`, `Service Type` and
`Service Reference Number` as columns. Harvesting one real access-log row yields most of a valid seed set
in a single step.

## 9. Suggested coverage priority

From each module's stated purpose, plus the safety constraints in the approach doc.

| Tier | Modules | Why |
|---|---|---|
| **1** | `ServiceDetails*`, `UserDetails*`, `ServicePassword*`, `Configuration` | Core access paths; heaviest existing test investment; read-dominant, so safe |
| **2** | `ActivityLogs`, `Logs`, `VideoLog`, `Command`, `UserServiceSession` | Audit and compliance evidence — silent breakage is costliest to find late |
| **3** | `Lob`, `LobandService`, `ServiceType`, `ProfileManagement`, `Policy` | Reference data; stable; cheap smoke coverage |
| **4** | `ADbridging*`, `DualFactor`, `HSM*`, `AWSKeyVault`, `AzureKeyVault`, `SIEM` | Integration modules — need external systems |
| **5 — defer** | `ServiceCreation`, `RDPSServiceInsert*`, `DeviceOnboarding`, `UserOnboarding`, `OfflineSync` | Mutating; require explicit allowlisting |
| **excluded** | Provisioning API, `ARCOSWebDT.ReturnDataTable`, `CallInlineQuery` | Destructive, or unauthenticated SQL execution |

## 10. Actions arising

| # | Action |
|---|---|
| F1 | Provision API Users covering all three Access Types; add `Access Type` to the run configuration |
| F2 | Register the CI agent IP + MAC before testing password modules |
| F3 | Assert `pam_BaseAPIURL` matches the in-product Application List entry at suite start |
| F4 | Record both-HTTPS / both-HTTP as an environment precondition |
| F5 | Stop authenticating as `GenericScheduler`; provision a dedicated automation API User |
| F6 | Build the seed fixture from the Access Logs column set |
| F7 | Rank generated coverage by §9 |
| F8 | Do not expect error codes from documentation — baseline them |
