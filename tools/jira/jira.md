# jira — raising PAMIT tickets from the terminal

**Status:** 🟡 draft, pending owner validation of `PAMIT-42744` · **Last updated:** 2026-07-31
**Site:** `https://arcon-tech-solution.atlassian.net` · **Project:** `PAMIT` — PAM Issue Tracker
(classic, id 10001)
**Not versioned** — sits parallel to `BLAST/`, outside both git checkouts.

---

## 1. What is here

| File | Role |
|---|---|
| `.env` | Credentials **and** environment-under-test details. ⛔ gitignored, never commit |
| `.env.sample` | Documented shape of `.env`, safe to share |
| `.gitignore` | Excludes `.env`, `.tmp/`, `*.zip`, `last-created-issue.json` |
| `jira_client.py` | Minimal REST client — auth, GET/POST, multipart attach |
| `create_lh01.py` | Ticket builder for developer loophole LH-01. The reference implementation |
| `last-created-issue.json` | Key + URL + attachment list of the most recent create |

```powershell
python tools\jira\create_lh01.py --dry-run   # build and print the payload, create nothing
python tools\jira\create_lh01.py --create    # create the issue and attach evidence
```

---

## 2. Auth

HTTP Basic: `JIRA_EMAIL` as username, `JIRA_API_TOKEN` as password, base64-encoded. Tokens are
issued at <https://id.atlassian.com/manage-profile/security/api-tokens>. Verify with:

```
GET /rest/api/3/myself   ->  200 + displayName
```

Nothing in this folder prints or persists the token. Keep it that way — if a script needs to
report which credential it used, report the *email*, never the token.

---

## 3. ⚠️ Two traps that cost a failed create

### 3.1 Description must be ADF, not wiki markup

Jira Cloud REST **v3** requires the description as [Atlassian Document
Format](https://developer.atlassian.com/cloud/tools/jira/platform/apis/document/structure/) — a JSON
node tree. Pasting `h2.` / `||` / `{code}` wiki markup into a v3 `description` renders it as
literal text.

`artifacts/loopholes/LH-01-.../JIRA-TICKET.md` holds the human-readable draft in wiki markup;
`create_lh01.py` composes the *same content* as ADF nodes. Those two are maintained together —
if you edit one, edit the other.

ADF builders provided in `create_lh01.py`: `heading` · `para` · `txt` (with `strong`/`code`
marks) · `codeblock` · `table` · `bullets` · `panel` · `rule`.

### 3.2 `createmeta` under-reports required fields

`GET /rest/api/3/issue/createmeta/PAMIT/issuetypes/10009` lists **7** required fields. A create
with exactly those returns **HTTP 400** — a project validator enforces **7 more** that
createmeta marks optional:

| Field | ID | Value used |
|---|---|---|
| Affected Milestone. | `customfield_10092` | `35.8.29 HF12` (id 21486) — array |
| End-User OS | `customfield_10115` | `All` (12766) |
| Functionality working in previous version | `customfield_11253` | `No` (22131) |
| Previous working version | `customfield_11254` | `None` (22194) |
| Is reopen from customer | `customfield_10780` | `No` (18854) |
| Reopen Original Ticket ID | `customfield_10781` | `NA` (string) |
| **Database Type** | **`customfield_10156`** | **`MSSQL` (11188)** |

⚠️ **`Database Type` was added to this list by `PAMIT-43050`.** This file previously said six.
`create_lh01.py` set `Database Type` anyway, so the gap never surfaced until a ticket deliberately
omitted it as not-applicable — a source-control defect has no database. The create failed with
`"Field Database Type is required."` and nothing was created. **It is mandatory regardless of
relevance**; set it to `MSSQL` and note in the ticket that it carries no meaning.

The lesson generalises: **the validator list is discovered only by a failed create.** Treat every
"optional per createmeta" field that `create_lh01.py` sets as probably mandatory.

Also note `createmeta` paginates at **50 fields** by default — pass `?maxResults=200` or you
will silently miss `summary`, `priority`, `fixVersions` and the rest.

---

## 4. PAMIT field map — Bug (issue type `10009`)

### Required by createmeta

| Field | ID | Notes |
|---|---|---|
| Project | `project` | `{"key": "PAMIT"}` |
| Issue Type | `issuetype` | `{"id": "10009"}` |
| Summary | `summary` | string |
| Description | `description` | **ADF document** |
| Priority | `priority` | `High` · `Medium` · `Low` · `ShowStopper` — **no "Critical"** |
| Primary Client | `customfield_10112` | 1,011 options. Internal defects → `Internal (ARCON)` (11183) |
| Department Of Created By | `customfield_10114` | → `Automation Team` (13273) |

### Set for LH-01, worth setting on any QA-raised bug

| Field | ID | Value |
|---|---|---|
| Severity | `customfield_10190` | `Sev-0` … `Sev-3`. Critical-but-not-release-blocking → `Sev-1` |
| Components | `components` | 51 options; API defects → `PAM API` |
| Fix versions | `fixVersions` | `35.8.29 HF12` = id `17321` |
| Labels | `labels` | free-form array |
| Database Type | `customfield_10156` | `MSSQL` · `MySQL` · `MySql & MSSql` |
| Hosting Environment | `customfield_11220` | `Windows` · `RHEL` · `Ubuntu` · `Kubernetes` |
| Task Complexity | `customfield_10251` | `Small` · `Medium` · `Large` · `Very Large` |

### Absent from the create screen — do not try to set

`reporter` (defaults to the token owner) · `environment` · `versions` (Affects Version).
There is **no "Steps to Reproduce" field** — steps go in the description. Environment details
go in a description table, populated from `.env`.

---

## 5. Severity vs Priority

PAMIT separates them and the vocabularies do not line up. `Priority` has no "Critical", so a
🔴 Critical finding maps to:

| | Value | Reasoning |
|---|---|---|
| `Severity` | **Sev-1** | Sev-0 is reserved for production-down |
| `Priority` | **High** | `ShowStopper` implies release-blocking; a contract defect that has shipped for many releases is not |

Raise to `ShowStopper` only if the owner says the release is gated on it.

---

## 6. Attachments

`POST /rest/api/3/issue/{key}/attachments`, `multipart/form-data`, field name `file`, and the
header **`X-Atlassian-Token: no-check`** — without it Jira rejects the upload as XSRF. One file
per request.

**Exclusion rule:** `JIRA-TICKET.md` is never attached. It is the internal draft *of the ticket
itself*, so attaching it to that ticket is circular. `create_lh01.py` enforces this twice — the
zip builder skips it by name, and the attach loop refuses any file in
`EXCLUDED_FROM_ATTACHMENTS`. The zip is asserted clean before upload.

---

## 7. Environment details live in `.env`

`TEST_ENVIRONMENT` · `APPLICATION_URL` · `API_URL` · `BUILD_NUMBER` · `FIX_VERSION` ·
`AFFECTS_VERSION` are read from `.env` and rendered into the ticket's Environment table and the
reproduction steps. Switching target environment — `QA_Indus`, `MS_Scale`, `Preprod_MsSQL` — is
an `.env` edit, not a code edit.

Keep `TEST_ENVIRONMENT` matching a real `Environments/<env>.properties` in the automation repo,
so a reader can reproduce the run.

---

## 8. Raised so far

| Ticket | Finding | Summary | Attachments |
|---|---|---|---|
| [PAMIT-42744](https://arcon-tech-solution.atlassian.net/browse/PAMIT-42744) | LH-01 | HTTP 200 for application-level failures — 289 calls / 276 endpoints | `EVIDENCE.xlsx` · `EVIDENCE.md` · evidence `.zip` |
| [PAMIT-43050](https://arcon-tech-solution.atlassian.net/browse/PAMIT-43050) | **B1** (repo-size F01/F02/F03/F07/F13) | Binary artifacts committed to version control — `pam` is 35.57 GB, 73.3% of history from three third-party ZIP files | `findings.csv` · `README.md` · evidence `.zip` |

**`create_b01.py`** is the builder for the second one. It differs from `create_lh01.py` in three
ways worth copying for the next ticket: it imports the ADF helpers rather than duplicating them,
its component is **`SCM` (10376)** rather than `PAM API` — the right home for a source-control
defect — and its evidence pack is `artifacts/repo-issues/`, not an `LH-NN` folder.

---

## 9. To generalise for LH-02…12

`create_lh01.py` is deliberately one file per loophole rather than a parameterised generator —
the description is bespoke prose and forcing it into a template would flatten it. What *should*
be lifted into a shared module when the second one is written:

- the ADF builders (`heading`, `para`, `table`, `codeblock`, `panel`, …)
- `build_payload()`'s field block, minus `summary`/`description`
- the zip-and-exclude attachment routine

Leave the description composition per-ticket. Confirm the field map in §4 still holds by
re-running the createmeta discovery — options lists (versions, milestones) change every release.
