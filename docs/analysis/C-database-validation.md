# Database validation — is it possible, and does the API write here at all?

**Database:** `ARCOSDB_U16SP2_WEBSM_QA` · **Server:** `10.10.0.194,1433` · SQL Server 2019 CU32-GDR
(15.0.4455.2), Developer Edition, Linux (Ubuntu 20.04.6 LTS)
**Scope:** OBJ-007 items 4 and 13 · **Access used:** read-only `SELECT`, zero HTTP requests
**Inventory:** 552 tables · 17 views · 612 stored procedures · **5** declared foreign keys · 0 certificates · 0 symmetric keys
**Harness:** `tools/obj007_db_probe.ps1` (deny-by-default: refuses anything not `SELECT`/`WITH`) ·
`tools/obj007_encryption_survey.ps1`
**Data:** `data/analysis/db-schema-map.json` · `data/analysis/db-observations.json` (22 observations) ·
`data/analysis/solutions-DB.json` (10 issues × 2 solutions)

---

## 1. The answer, up front

| Question | Answer |
|---|---|
| **Is DB validation possible?** | ✅ **Yes.** Not merely possible — it is the only channel that can settle questions the API-side run left open |
| **Does the QA API write to this database?** | ✅ **Yes, confirmed three independent ways.** The 2026-07-29 run's writes are in this database and individually traceable |
| **Newest timestamp in the database** | **`2026-08-03 15:29:18`** (`sso_services.ss_modified_on`) — minutes old at query time |
| **Is column encryption a blocker?** | ⬜ **No.** It is real but narrow, and a plaintext audit channel routes around it entirely |
| **Can it be switched on today?** | ⛔ **No — one hard blocker.** The configured login is `sysadmin` over 31 databases. Fix that first |

Two prior conclusions are **overturned by measurement**, and both mattered:

| Prior belief | Measured reality |
|---|---|
| "No DB row is newer than 2025-10-01, so the API's writes may not land here" | **False for this database.** Newest business timestamp `2026-08-03 15:29:18`. Row counts rose *during this session* — `sso_services` 20,650 → 20,651, `ssR_Users_Services` 313,086 → 313,197 |
| "LOB names are encrypted, so matching a created object by name cannot work" | **True only for `sso_lobs`, `sso_users`, `sso_services`.** `sso_Sgroup`, `sso_Ugroup`, `sso_ApiUsers` and the entire audit log are **plaintext** |

The earlier freshness figure was almost certainly taken from a different database on this instance (it hosts
31) or from the empty AD-bridging tables. **Always name the database when quoting a freshness number.**

---

## 2. Does the API write here? — the evidence

The 2026-07-29_181439 run window is `18:14:39`–`21:26:22`. Three independent channels agree.

**2.1 The audit log names the run's writes in plaintext.** Filtering `sso_arcos_log` to the test runner's IP:

```sql
SELECT sal_id, sal_timestamp, aoo_object_operation, aot_description,
       sal_object_referance, sal_Api_user_id
FROM sso_arcos_log
WHERE sal_timestamp BETWEEN '2026-07-29 18:14:39' AND '2026-07-29 21:35:00'
  AND sal_ipaddress = '10.10.1.242';
```

| `sal_id` | Time | Operation | Object type | Reference (**plaintext**) | API user |
|---|---|---|---|---|---|
| 2313798 | 19:12:06 | Created | User Transactions | `AUTO40PC47` | 2 |
| 2313799 | 19:12:42 | Created | Service Transactions | `10.11.0.48@SVC40PC47:Windows RDP` | 2 |
| 2313801 | 19:27:20 | Deleted | Service Transactions | `10.10.0.38@arcostest12:SSHLINUX` | 2 |
| 2313852 | 19:44:00 | Created | User Transactions | `AUTO40PC47` | 2 |
| 2313853 | 19:49:46 | Created | User Transactions | `AUTO40PC47` | 2 |

**2.2 Business tables carry the rows, stamped `SYSTEM_API`.**

| Table | Created in window | Identifying value | Stamp |
|---|---:|---|---|
| `sso_users` | 1 | `ssu_id=1457`, username ciphertext `OhjN7MeS…KUHDAk=` | `created_by='SYSTEM_API'` |
| `sso_services` | 1 | `ss_service_id=25342` | `ss_created_by='SYSTEM_API'` |
| `sso_ApiUsers` | 1 | `RowId=365`, `Username='AUTO40PC47'` (**plaintext**) | `CreatedBy='System'` |
| `sso_user_details` · `sso_lobs_users` · `sso_lobs_services` · `sso_services_param` | 1 each | — | — |
| `sso_lobs` · `sso_Sgroup` · `sso_Ugroup` | **0** | — | — |

Modified in the same window: `sso_services` 3, `sso_users` 2.

**2.3 The API's own request log records the run per-call.** `ArconPamApiLog` (41,910,875 rows) captured
**194** error rows from the runner IP `10.10.1.242` across **62 distinct methods** during the window —
including unhandled .NET exceptions the HTTP 200 envelope concealed (`InvalidCastException`,
`OverflowException`, `NullReferenceException`, `SqlTypeException`, `FormatException`). The `sso_ApiUsers`
row at `19:54:46` is corroborated by a log line at the same second:
`APA:Decrypt0001 - PlainText -auto40pc47@test.local`.

**Verdict: the API writes here.** Not ambiguously — the same object appears in the audit log by name, in the
business table by ciphertext, and in the request log by timestamp.

### 2.4 The absence is also consistent

Most creates genuinely failed, and the database agrees. Sweeping **all 177 populated tables** that carry a
creation timestamp:

| Measure | Value |
|---|---:|
| Rows created anywhere in the 3h20m window | **110** |
| …of which logging / report side-effect tables | 94 (`sso_arcos_log_details` 63, `sso_arcos_customcol_report` 22, `sso_arcos_report_download` 4, others) |
| …of which genuine business objects | **≈7** |

Against 217 create endpoints and 196 chaining failures — of which **117 genuinely failed** (HTTP non-200 or
`Success:false`), **19** were acknowledged without returning an identifier, and **60** are indeterminate —
a gain of ~7 business rows is exactly what "most creates never happened" predicts. Had the run silently
created hundreds of objects it failed to report, this sweep would have shown it. **The API-side conclusion
and the database agree.**

### 2.5 What only the database can settle

The L6 `record-exists` layer reported 2 PASS / 105 FAIL, but **97 of its 107 checks searched for the literal
unresolved string `${NEW_ID}`** and could never have passed. That figure is largely a harness artifact, not
a defect count. For **101 of 107** hops the run cannot distinguish:

- never created,
- created but not readable back through the API,
- created and readable.

A read-only `SELECT` separates all three. Two of the writes L6 missed were real and durable — which is the
whole argument for wiring `DBUtils` in. ⚠️ Wherever the "105 of 107" figure is quoted, restate it.

---

## 3. How widespread is the encryption?

**Encryption is application-side, narrow, and deterministic.** No SQL Server TDE or Always Encrypted is in
use (`sys.symmetric_keys` empty, `sys.certificates` = 0), so the catalog reports every one of these columns
as plain `varchar` and offers no hint.

⚠️ **Classification is inference, not a schema fact.** Method: sample up to 4 non-null values per text
column and classify by shape — base64 charset, length a multiple of 4, decoding to whole 16-byte AES blocks,
printable-byte fraction below 0.75. Every verdict in `db-schema-map.json` carries the sampled value.

| Object | Table | Identifying column | Verdict | Sample / basis |
|---|---|---|---|---|
| LOB | `sso_lobs` | `sls_name` | ⛔ Encrypted | `6riBmF0+uM8LEZjpHV4a2Q==` — 16 B, 1 AES block, printable frac 0.19 |
| User | `sso_users` | `ssu_username` | ⛔ Encrypted | `+0PSggY5XiWZuQ1lBoTdWQ==` — 16 B, frac 0.38 |
| Service | `sso_services` | `ss_username`, `ss_server_ip`, `ss_server_host`, `ss_port` | ⛔ Encrypted | `PQmEJ+q9r5IOT//Z06Ar1A==` — 16 B, frac 0.25 |
| **Service group** | `sso_Sgroup` | `srv_group_name` | ✅ **Plaintext** | non-base64 characters present |
| **User group** | `sso_Ugroup` | `usr_group_name` | ✅ **Plaintext** | non-base64 characters present |
| **API user** | `sso_ApiUsers` | `Username` | ✅ **Plaintext** | `AUTO40PC47` |
| **Audit log** | `sso_arcos_log` | `sal_object_referance` | ✅ **Plaintext** | `AUTO40PC47` — verified across 14 operation/object-type groupings |

Encrypted-column counts: `sso_lobs` 5 of 7 text columns · `sso_users` 4 · `sso_services` 12 ·
`sso_user_details` 2 · `sso_Sgroup` **0** · `sso_Ugroup` **0** · `sso_ApiUsers` **0** · `sso_arcos_log` **0**.

**Plaintext in every table:** the surrogate PK, `created_by`/`modified_by`, and `created_on`/`modified_on`.
Those four alone make ID-based and provenance-based validation possible everywhere.

### 3.1 The encryption is deterministic — which cuts both ways

| Evidence | Measurement |
|---|---|
| `sso_services` has 20,651 rows but only **59 distinct** `ss_port` ciphertexts | one ciphertext `/QJnyC6c+u1e5VeF0EyvPA==` covers **18,848** rows (91%) |
| Ciphertext `4QVsqJbF6MWeAvmlLMC+Kg==` appears in **3 columns across 2 tables** | `sso_lobs.sls_address2` (67), `sso_lobs.sls_report_header` (123), `sso_services.ss_instance` (18,865) |
| The run-created user row | `ssu_username` and `ssu_displayname` held the **identical** ciphertext |

Same plaintext → same ciphertext, everywhere, under one key with no per-row IV or salt. Functionally
**AES-ECB**.

- 🔴 **Security:** plaintext distribution leaks without the key. 91% of services sharing one port ciphertext
  tells a reader with `SELECT` access that they all use the default port. Frequency analysis recovers common
  values. Raised as `SOL-DB-003`.
- 🟡 **Testing:** determinism is *why* ciphertext-equality lookups work. Verified —
  `WHERE ssu_username = 'OhjN7MeS…KUHDAk='` returned exactly 1 row. But this lever **dies the day the
  security fix lands**, so it must not be the primary design.

---

## 4. The five validation levers

| # | Lever | Encryption-proof? | Strength |
|---|---|---|---|
| **1** | **`sso_arcos_log` audit log** — plaintext `sal_object_referance`, `sal_old_value`/`sal_new_value`, `sal_Api_user_id` isolates API writes | ✅ Yes | **Primary.** Covers create/update/delete. Over-reports creates 6:1 |
| 2 | **Ciphertext equality** — read the ciphertext back once, reuse as a fixture | ✅ Yes (no key needed) | Only validates "the row I created still exists". Breaks on the security fix |
| 3 | **`created_by = 'SYSTEM_API'`** — plaintext provenance stamp (11 `sso_users`, 395 `sso_services`) | ✅ Yes | Scopes to API-created rows; needs a timestamp window to be run-specific |
| 4 | **Row-count delta** | ✅ Yes | ⚠️ Unsafe unscoped — see §4.1 |
| 5 | **`ArconPamApiLog`** — per-call error codes and unhandled exceptions | ✅ Yes | Surfaces defects invisible to black-box tests. Must bound by `LogId` range |

### 4.1 Two traps that will produce false passes

**⛔ The audit log over-reports creation.** It records the *attempt*, not the durable insert:

```sql
SELECT COUNT(*) FROM sso_arcos_log
WHERE sal_object_referance='AUTO40PC47' AND aoo_object_operation='Created'
  AND aot_description='User Transactions';                                  -- → 6
SELECT COUNT(*) FROM sso_users
WHERE ssu_username='OhjN7MeS4xe7sCksQFhyTMUAKRTy1ZbFzZu+2KUHDAk=';          -- → 1
```

Six "Created" audit rows, one actual row. This is the **DB-side mirror** of the known API trap where
`Success: true` carries `Message: "Already Exists"`. Neither channel is sufficient alone.

**⛔ The environment is shared and concurrently written.** In the run window, audit rows came from at least
five sources: the runner (`10.10.1.242`, 5 rows), `10.10.6.88`, `10.10.0.203`, `10.10.1.123` (created a
Server Type at 18:37:11 — which explains the `sso_server_type` row in the §2.4 sweep), `10.10.8.215`, plus
52 auto-revocations at 19:32:00–19:32:01. Operation mix: Revoked 52, **Created 6**, Modified 5, Assigned 2,
Deleted 2 — **only 2 of the 6 creates were the test's.** A bare `COUNT(*)` delta would steal credit for
other people's writes. Every count must carry an attribution predicate.

---

## 5. Feasibility per validation type — the core answer

| Validation type | Verdict | Why |
|---|---|---|
| **Record creation** | ✅ **Possible** | Audit log gives the plaintext name; business table confirms durability. Must be **two-part** (§4.1) |
| **Update** | ✅ **Possible** | `sal_old_value` → `sal_new_value` is a genuine before/after pair — the only channel that has one. Confirm with `modified_on` |
| **Deletion** | 🟡 **Possible with caveats** | Hard deletes, no tombstone on the main tables. Must assert **absence + audit row + captured PK** — never absence alone |
| **Consistency** | ✅ **Possible** | Denormalized copies are a real target. `sso_lobs_users.lug_sls_name` vs `sso_lobs.sls_name`: 1,147 links, 472 matching, **5 drifted** |
| **Persistence** | ✅ **Possible** | Confirmed end-to-end: the run's rows are still present days later, with `created_on` intact |
| **Integrity** | ✅ **Possible — and immediately productive** | Only **5** FKs exist in 552 tables, so orphans accumulate. Measured below |
| Access-control profiles | ⛔ **Not possible** | `sso_users_accesscontrol` unmodified since 2026-06-11; all four companion profile tables have **0 rows** |
| AD-bridging / data warehouse | ⛔ **Not possible** | ~35 tables at 0 rows, incl. `tblLOBDetail`, all `sso_AD_*`, `sso_ob_*`, `DWH_*`/`Dwh_*` |

### 5.1 Integrity — real defects, found on the first query

| Check | Orphans | Of total |
|---|---:|---:|
| `ssR_Users_Services` → missing service | **16,560** | 313,197 (**5.3%**) |
| `sso_users` → no `sso_user_details` row | 17 | 1,439 |
| `sso_lobs_users` → missing user | 9 | 1,147 |
| `sso_lobs_users` → missing LOB | 1 | 1,147 |
| `lug_sls_name` drifted from `sso_lobs.sls_name` | **5** | 1,147 |

**16,560 user-to-service authorisation mappings point at services that no longer exist.** Deletion does not
cascade. In a privileged-access product, dangling access rows are security-relevant — not untidy data.
Raised as `SOL-DB-005`.

---

## 6. Required permissions — the blocker

The configured account is **`sysadmin`**:

```sql
SELECT r.name FROM sys.server_role_members m
JOIN sys.server_principals r ON r.principal_id = m.role_principal_id
JOIN sys.server_principals p ON p.principal_id = m.member_principal_id
WHERE p.name = 'devops';                                    -- → sysadmin
SELECT IS_SRVROLEMEMBER('sysadmin'), IS_SRVROLEMEMBER('dbcreator'), USER_NAME(),
       (SELECT COUNT(*) FROM fn_my_permissions(NULL,'SERVER'));   -- → 1, 1, dbo, 34
SELECT COUNT(*) FROM fn_my_permissions(NULL,'DATABASE');    -- → 82
SELECT COUNT(*) FROM sys.databases;                         -- → 31
```

34 server-level permissions including `ALTER ANY DATABASE`, `ALTER ANY LOGIN`, `ALTER ANY CREDENTIAL`,
`ALTER ANY LINKED SERVER`, `ADMINISTER BULK OPERATIONS`. `Environments/QA_MsSQL.properties` (lines 77–82)
now ships `db_user=devops` with the password in plaintext, in version control.

⛔ **Do not enable DB validation in CI until this is replaced.** A generated or mistyped statement would
execute with full destructive authority over 31 databases, several non-QA.

### 6.1 What a correct least-privilege account needs

```sql
-- Run by a DBA. Read-only, one database, explicit table whitelist.
CREATE LOGIN pam_qa_validator WITH PASSWORD = '<generated>';
USE ARCOSDB_U16SP2_WEBSM_QA;
CREATE USER pam_qa_validator FOR LOGIN pam_qa_validator;

-- No server roles. No db_datareader (it would grant every table, incl. the two below).
GRANT SELECT ON dbo.sso_arcos_log      TO pam_qa_validator;   -- primary validation channel
GRANT SELECT ON dbo.sso_users          TO pam_qa_validator;
GRANT SELECT ON dbo.sso_user_details   TO pam_qa_validator;
GRANT SELECT ON dbo.sso_services       TO pam_qa_validator;
GRANT SELECT ON dbo.sso_services_param TO pam_qa_validator;
GRANT SELECT ON dbo.sso_lobs           TO pam_qa_validator;
GRANT SELECT ON dbo.sso_lobs_users     TO pam_qa_validator;
GRANT SELECT ON dbo.sso_lobs_services  TO pam_qa_validator;
GRANT SELECT ON dbo.sso_Sgroup         TO pam_qa_validator;
GRANT SELECT ON dbo.sso_Ugroup         TO pam_qa_validator;
GRANT SELECT ON dbo.ssR_Users_Services TO pam_qa_validator;
GRANT SELECT ON dbo.ssR_Ugroup_users   TO pam_qa_validator;
GRANT SELECT ON dbo.ssR_Sgroup_services TO pam_qa_validator;
GRANT SELECT ON dbo.ArconPamApiLog     TO pam_qa_validator;   -- error-log assertions

-- Explicitly withhold the secret-bearing tables.
DENY SELECT ON dbo.sso_ApiUsers               TO pam_qa_validator;  -- cleartext passwords
DENY SELECT ON dbo.tbl_KeyEncryptionDecryption TO pam_qa_validator; -- private key material
```

| Control | Rule |
|---|---|
| Server roles | **None.** Never `sysadmin`, `dbcreator`, `securityadmin` |
| Database roles | **None.** Not even `db_datareader` — it would grant the two `DENY`d tables |
| Statement guard | `DBUtils` refuses any SQL not beginning with `SELECT`/`WITH`, and rejects mutating keywords. Same control as `obj007_db_probe.ps1` |
| Startup guard | Abort if `IS_SRVROLEMEMBER('sysadmin') = 1` — makes the rule self-enforcing |
| Row caps | `TOP`/`OFFSET` on every data query; explicit command timeout |
| Credentials | Rotate the exposed `devops` password; keep the new one out of version control |

⚠️ The `DENY` pair is not optional. `sso_ApiUsers` stores `Password`, `UsersSecret` and `UsersKey` in
**cleartext** for 34 API users (`Username='AUTO40PC47'`, `Password='<REDACTED>'`), and
`tbl_KeyEncryptionDecryption` holds an unencrypted private key (1,702 chars) in the same database as the
data it protects. A test account has no business reading either.

---

## 7. The SQL to embed in the framework

Every statement is read-only and row-capped. `?` marks a bound parameter — never string concatenation.

**7.1 Record creation** — two-part, and report the parts separately:

```sql
-- (a) Did the API log the operation, by plaintext name?
SELECT COUNT(*) AS audit_hits
FROM   sso_arcos_log
WHERE  sal_object_referance   = ?      -- plaintext name, e.g. 'AUTO40PC47'
  AND  aot_description        = ?      -- 'User Transactions' | 'Service Transactions'
  AND  aoo_object_operation   = 'Created'
  AND  sal_Api_user_id IS NOT NULL     -- API-originated only, not UI
  AND  sal_timestamp          >= ?;    -- run start

-- (b) Is the row durably there? (Scoped — never a bare COUNT.)
SELECT COUNT(*) AS row_hits
FROM   sso_users
WHERE  created_by = 'SYSTEM_API'
  AND  created_on >= ?;                -- run start
```

Fail if either is 0. Surface `audit_hits > row_hits` explicitly — that divergence **is** the defect.

**7.2 Update** — the only channel with a true before/after pair:

```sql
SELECT TOP 10 sal_old_value, sal_new_value, sal_timestamp
FROM   sso_arcos_log
WHERE  sal_object_referance = ?
  AND  aoo_object_operation = 'Modified'
  AND  sal_Api_user_id IS NOT NULL
  AND  sal_timestamp >= ?
ORDER BY sal_id DESC;
```

**7.3 Deletion** — three-part; capture the PK *before* deleting:

```sql
SELECT COUNT(*) AS audit_deletes            -- audit records the delete
FROM   sso_arcos_log
WHERE  sal_object_referance = ? AND aoo_object_operation = 'Deleted'
  AND  sal_Api_user_id IS NOT NULL AND sal_timestamp >= ?;

SELECT COUNT(*) AS still_present            -- expect 0; PK captured pre-delete
FROM   sso_services WHERE ss_service_id = ?;
```

**7.4 Consistency** — denormalized copy vs authoritative value (ciphertext-to-ciphertext works because
encryption is deterministic):

```sql
SELECT COUNT(*) AS drifted
FROM   sso_lobs_users lu
JOIN   sso_lobs l ON l.sls_id = lu.lug_sls_id
WHERE  lu.lug_sls_name <> l.sls_name;       -- current baseline: 5
```

**7.5 Persistence** — ciphertext-equality on the row the API created (lever 2; read the ciphertext back once
and hold it as a fixture):

```sql
SELECT COUNT(*) AS persisted
FROM   sso_users WHERE ssu_username = ?;    -- bound ciphertext fixture
```

**7.6 Integrity** — nightly, not per-test; these scan large tables:

```sql
SELECT COUNT(*) AS orphan_services          -- baseline 16,560
FROM   ssR_Users_Services rs
LEFT   JOIN sso_services s ON s.ss_service_id = rs.sus_service_id
WHERE  s.ss_service_id IS NULL;

SELECT COUNT(*) AS users_without_details    -- baseline 17
FROM   sso_users u
LEFT   JOIN sso_user_details d ON d.sud_user_id = u.ssu_id
WHERE  d.sud_user_id IS NULL;
```

**7.7 Server-side error check** — one assertion covering all 62 methods. ⚠️ `LoggedOnDate` is **unindexed**
on 41.9 M rows; bound by `LogId` first or this scans the whole table:

```sql
-- Step 1: binary-search the clustered PK to the run start (cheap seek).
SELECT TOP 1 LogId FROM ArconPamApiLog WHERE LogId >= ? ORDER BY LogId;

-- Step 2: bounded by that LogId, exclude the known-broken background loop.
SELECT TOP 200 Method, Message, LoggedOnDate
FROM   ArconPamApiLog
WHERE  LogId >= ?                       -- from step 1
  AND  ApplicationName = 'ARCONPAMAPI'
  AND  Level = 'ERROR'
  AND  IpAddress = ?                    -- the runner's IP
  AND  Method NOT IN ('CallBack','UpdateTargetUserCreationStatus')  -- see §8
ORDER BY LogId;
```

**Plaintext-name shortcut** — for service groups, user groups and API users, none of this is needed:

```sql
SELECT COUNT(*) FROM sso_Sgroup   WHERE srv_group_name = ?;   -- plaintext
SELECT COUNT(*) FROM sso_Ugroup   WHERE usr_group_name = ?;   -- plaintext
SELECT COUNT(*) FROM sso_ApiUsers WHERE Username      = ?;    -- plaintext
```

Start the pilot here — no encryption, no audit-log semantics, no key.

---

## 8. Limitations — read before relying on any of the above

| # | Limitation | Consequence |
|---|---|---|
| 1 | **Audit log over-reports creates 6:1** | Never assert on it alone (§4.1) |
| 2 | **Encryption classification is inference** | Shape-based, not a schema fact. `db-schema-map.json` carries every sample so a human can overrule |
| 3 | **`aot_description` values are known for only 2 object types** | 'User Transactions', 'Service Transactions'. Catalogue the rest before relying on them. No LOB create was observed |
| 4 | **Ciphertext equality dies on the security fix** | Lever 2 is temporary by construction. Keep lever 1 primary |
| 5 | **Shared environment, concurrent writes** | Only 2 of 6 creates in the run window were the test's. Always scope by attribution |
| 6 | **`ArconPamApiLog` date filters are full scans** | 41.9 M rows, one clustered PK on `LogId`, nothing else indexed. Bound by `LogId` |
| 7 | **A broken background job floods the error log** | 240 errors/hour, constant before/during/after the run — `CallBack` (`APA:DOC0010`) + `UpdateTargetUserCreationStatus` (`APA:DL0046`), `IndexOutOfRangeException`, from `10.10.0.120`. It inflated the window's error count from **194 → 1,736**. Filter it out; raise it as a defect (`SOL-DB-007`) |
| 8 | **~35 tables are empty** | No AD-bridging, DWH or access-control-profile validation is possible. Report NOT-APPLICABLE, not FAIL |
| 9 | **Only 5 FKs exist** | The database will not reject bad references; the framework must check them |
| 10 | **`KNOWN_ERROR_CODES = {201,202,203}` is far too small** | Real codes are structured: `903- SDC-SFS`, `902-UDC-ULN`, `902SPB-GSP`, `APA:DL0046`, `APA:Decrypt0001`. A numeric set can never match them (`SOL-DB-009`) |

---

## 9. Recommended sequence

| Step | Action | Blocked on |
|---:|---|---|
| 1 | **Provision the least-privilege login** (§6.1) and repoint `db_user`. Add the `sysadmin` startup guard | DBA — start now |
| 2 | Pilot on `sso_Sgroup` / `sso_Ugroup` / `sso_ApiUsers` — plaintext names, no key, no audit semantics | — |
| 3 | Catalogue `aot_description` per object type; build the two-part create assertion (§7.1) | Step 2 |
| 4 | Replace L6 for the 13 drivable create endpoints; report NOT-APPLICABLE where no DB channel exists | Step 3 |
| 5 | Add the nightly integrity job (§7.6), baselined at 16,560 / 17 / 9 / 1 / 5, with a burn-down owner | Step 1 |
| 6 | Add the server-side error assertion (§7.7) with the background-loop filter | Step 1 |
| 7 | Raise the product findings: `SOL-DB-003` (deterministic encryption), `SOL-DB-004` (cleartext secrets), `SOL-DB-005` (16,560 orphans), `SOL-DB-007` (broken job) | — |

**Bottom line.** DB validation is possible, the API demonstrably writes to
`ARCOSDB_U16SP2_WEBSM_QA`, and encryption is a narrow obstacle that a plaintext audit channel routes
around. The one thing standing in the way is a `sysadmin` credential that must not be used by an
automated test.
