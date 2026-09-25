# ISSUE-009 — Dynamic token generation fails for QA_MsSQL: `400 Invalid User Credentials`

**Status:** ✅ **RESOLVED 2026-07-29** — the credential in the properties file was stale, not the logic
**Severity:** 🟠 Medium (was: blocks unattended automation) · **Raised:** 2026-07-28
**Type:** Configuration / credential defect
**Environment:** `QA_MsSQL` · **Endpoint:** `POST https://u16hf.arconnet.com:6302/arcontoken`
**Evidence:** `../_archive-pre-2026-07-29/Execution/qa_mssql_token_check.json` (original failure)
**Reproduce:** `python tools\run_qa_mssql.py` — attempted and recorded on every run

---

## 0. Resolution

`ApiHelper.getToken(...)` was never at fault. `Environments/QA_MsSQL.properties` held a **superseded
password** for the `GenericScheduler` account:

| Key | Was | Now |
|---|---|---|
| `pam_APITokenUserName` | `R2VuZXJpY1NjaGVkdWxlcg==` | unchanged — always correct |
| `pam_APITokenPassword` | `<REDACTED>` ❌ | `<REDACTED>` ✅ |

With the owner-supplied credential in place the endpoint returns **HTTP 200 in 3.50 s**: `token_type:
bearer`, `expires_in: 86399` (~24 h), a 445-character HS256 JWT and a 427-character refresh token. Claims:
`role=Default`, `APIUserId=2`, `iss=http://localhost:8890/`.

Verified again by `tools/chain_runner.py` on run `2026-07-29_160155`, which generated a token
and executed 15 authenticated calls with zero auth failures.

⚠️ **The lockout risk in §5 still stands and is now enforced in code.** `chain_runner.py` generates a token
**once per run** and caches it to `tools/.token_cache.json` for its 24-hour life. Never call
`/arcontoken` in a loop: repeated attempts on 2026-07-28 moved the response from `Invalid User Credentials`
to `Your account has been locked`, and `GenericScheduler` is also the data-warehouse ETL service account.

The paragraphs below are retained as the original diagnosis.

---

## 1. Statement

`ApiHelper.getToken(...)` cannot obtain a token for QA_MsSQL using the credentials in
`Environments/QA_MsSQL.properties`. The token endpoint rejects them:

```
POST https://u16hf.arconnet.com:6302/arcontoken
Content-Type: application/x-www-form-urlencoded
grant_type=password&username=R2VuZXJpY1NjaGVkdWxlcg%3D%3D&password=<16 chars>

HTTP 400
{"error":"Invalid User Credentials"}
```

Every API test that calls `getToken(...)` in `@BeforeMethod` therefore cannot authenticate on this
environment.

## 2. What was verified

| Check | Result |
|---|---|
| Endpoint reachable | ✅ Yes — responds in ~170–460 ms |
| Request shape matches `ApiHelper.getToken()` | ✅ Form-encoded `grant_type` / `username` / `password`, credentials sent **as stored** (not decoded) — `ApiHelper.java:945-963` |
| `pam_grantType` | ✅ `password` |
| `pam_APITokenUserName` | `R2VuZXJpY1NjaGVkdWxlcg==` → base64-decodes to **`GenericScheduler`** |
| `pam_APITokenPassword` | `<REDACTED>` → decodes to a 12-character string |
| **Result with stored values** | ⛔ **400 Invalid User Credentials** |
| Sent raw instead of base64 | ⛔ Also rejected — so this is **not** an encoding problem |
| A separately supplied token | ✅ **Works** — HTTP 200 against `/api/ActivityLogs/GetDatabaseStatus` |

Three credential-encoding variants were tried and no more, deliberately, to avoid any account-lockout risk
on a shared environment. No password guessing was performed.

## 3. 🔗 Correlation with the developer repository

This is the part that makes the issue easy to acknowledge. The API user store **is** in the developer repo:

**`pam/PAM/Database/ReportingDb/ReportingDb/CustomScripts/MetaData/dbo.sso_ApiUsers.Table.sql`**

Row 2 of `[dbo].[sso_ApiUsers]`:

| Column | Value |
|---|---|
| `RowId` | **2** |
| `Username` | `TsLOCq2egav9DCLMMU8FXHu7qnA/iifmv4PcikR/mG0fvTmtt0Xl21U4W7cJZ9Cp` |
| `Password` | `TsLOCq2egav9DCLMMU8FXHu7qnA/iifmv4PcikR/mG2IkDr13YUYPFTJ0X755qi6` |
| `EmailId` | `GenericScheduler@arconnet.com` |
| `IsDefault` / `Active` | 1 / 1 |

The working token's JWT claims match this row **exactly**:

```
"APIUserId" : "2"                                                     -> sso_ApiUsers.RowId = 2
"APIUser"   : "TsLOCq2egav9DCLMMU8FXHu7qnA/iifmv4PcikR/mG0fvTmtt0Xl21U4W7cJZ9Cp"
                                                                      -> sso_ApiUsers.Username, byte for byte
```

**What this establishes:**

1. The account the framework is trying to use is `sso_ApiUsers` **RowId 2**, confirmed by the token itself.
2. Credentials are stored under a **proprietary encryption**, not base64 — the stored `Username` is not
   base64 of `GenericScheduler`. Note that `Username` and `Password` share a **41-character prefix**
   (`TsLOCq2egav9DCLMMU8FXHu7qnA/iifmv4PcikR/mG`), which indicates a deterministic, non-salted scheme.
3. On success the API copies the stored `Username` into the `APIUser` claim.

So the value in `pam_APITokenPassword` is simply **not the current password for RowId 2** — consistent with
the note that these credentials changed recently.

## 4. ⚠️ Secondary finding — the account itself is the wrong choice

`GenericScheduler` (`GenericScheduler@arconnet.com`) is the **data-warehouse ETL service account**, not a
test account. Corroborated in the repo by `GenericSchedulerSettings` tables and
`usp_GenericSchedulerSettings` stored procedures under both `ArconPamDatabase` and `ReportingDb`, and in the
product guides at `pam-admin:p320-321`.

Using an ETL service account for test automation means:

- test traffic is indistinguishable from scheduler traffic in audit logs;
- the token carries role `Default`, whose privileges are whatever the scheduler needs — not what tests need;
- rotating the scheduler's password silently breaks the whole QA suite, which is exactly what happened.

**Recommendation:** provision a dedicated `automation`/`qa` API user in `sso_ApiUsers` and point
`pam_APITokenUserName` at it.

## 4a. 🔴 ESCALATION — the account is now LOCKED

**2026-07-28, later the same day.** The token endpoint's response changed:

| Attempt | Response |
|---|---|
| Earlier | `HTTP 400 {"error":"Invalid User Credentials"}` |
| **Now** | `HTTP 400 {"error":"Your account has been locked. Please contact your supervisor"}` |

**Cause: this harness.** It re-attempted `getToken()` on **every run** by design, so that the issue would
close itself with evidence once credentials were fixed. Combined with three one-off encoding-diagnostic
attempts, that accumulated enough consecutive failures to trip the account lockout policy.

**This is a defect in the harness, not in the product.** It has been corrected — see §7a.

### Why this matters more than a test-account lockout

The locked account is `GenericScheduler` (`sso_ApiUsers` RowId 2), the **data-warehouse ETL service
account** (§4). A lockout is therefore not confined to test automation:

| At risk | Because |
|---|---|
| QA data-warehouse ETL / scheduler jobs | They authenticate as this same account |
| Any other consumer using the default API user | `IsDefault = 1` on this row |
| Reporting built on `ReportingDb` | Fed by the scheduler |

**Immediate action: unlock the account, and check whether QA scheduler jobs failed while it was locked.**
This is the strongest possible argument for §6 item 3 — automation must not share the ETL identity.

## 5. Consequence

| Area | Impact |
|---|---|
| **Unattended runs** | ⛔ Not possible — every run needs a hand-supplied token, which expires in 24 h |
| **CI** | ⛔ A Jenkins job cannot authenticate; the API suite would fail at `@BeforeMethod` |
| **Existing API tests** | ⛔ Any test calling `getToken(...)` on QA_MsSQL fails before its first assertion |
| **Audit trail** | 🟠 Test traffic attributed to the ETL scheduler account |

## 6. Required action

| # | Action | Owner |
|---|---|---|
| 1 | Supply the **current password** for the API user, and confirm whether it must be sent base64-encoded or raw | Owner / Development |
| 2 | Update `pam_APITokenPassword` in `Environments/QA_MsSQL.properties` — and the other 19 environment files if they share the credential | QA |
| 3 | **Provision a dedicated automation API user** rather than reusing `GenericScheduler` | Development / DBA |
| 4 | Document the credential-encryption scheme, or expose an admin action to set an API user password, so QA can rotate without a DBA | Development |

## 7a. Harness correction made in response

Dynamic token generation is now **opt-in only**:

```powershell
python Reports\Scripts\run_qa_mssql.py                    # does NOT touch /arcontoken
python Reports\Scripts\run_qa_mssql.py --try-token-gen    # attempts once, deliberately
```

Default runs no longer call the token endpoint at all, so no run can contribute to a lockout. Use
`--try-token-gen` **once**, only after the account is unlocked and correct credentials are in place — never
on a schedule, never in a loop, never in CI until it is confirmed working.

**Lesson recorded:** a "verify on every run so the issue self-closes" behaviour is unsafe against any
endpoint with a lockout policy. Retry-on-failure and account lockout are incompatible; the check must be
manual and deliberate.

## 7. Current workaround, and its limit

A supplied bearer token is read from `$PAM_API_TOKEN` or `Reports/Scripts/.token`. It works — this run
authenticated successfully with it.

**Limits:** it expires (the current one has a **24-hour** lifetime, not 12), it must be replaced by hand,
and it cannot be used for unattended CI. The harness re-attempts dynamic generation on **every** run and
records the outcome in `../Execution/qa_mssql_token_check.json`, so the moment the credentials are fixed
this issue closes itself with evidence.

> ⚠️ `Reports/Scripts/.token` holds a live bearer credential in plaintext. It is short-lived, but delete it
> when the trial period ends, and do not copy it into any repository.
