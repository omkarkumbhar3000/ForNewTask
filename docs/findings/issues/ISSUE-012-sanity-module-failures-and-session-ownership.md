# ISSUE-012 — Sanity module failures and session-leak ownership

**Raised under:** `OBJ-021` · **Environment:** `QA_MsSQL` (`https://u16hf.arconnet.com:1302`) ·
**Build:** `MSSQL_Build35.8` · **Account:** `arcosadmin`, domain `ARCOSAUTH`
**Evidence runs:** `performance/reports/2026-08-18_152615` (1 VU, post-fix) ·
`performance/reports/2026-08-18_142809` (3 concurrent) · `performance/reports/2026-08-18_151943`
**Audience:** internal analysis. **Verdict: no product defect is established by this investigation.**

> ⛔ **Headline: all 10 module failures are OUR automation's fault, and the session leak was OURS
> too.** Neither warrants a Jira ticket against the development team. This document records the
> evidence for that conclusion so it can be re-checked rather than taken on trust.

---

## 1. Session leak — ownership verdict: **OURS, not the product's**

### 1.1 Correction of an earlier claim

An earlier statement in this workspace said the product has **"no usable logout in this build"**.
**That was wrong**, and it was wrong because the search was too narrow — it looked only for a
`Logout.aspx` page and a rendered logout control. A wider search of the product source found a
complete, live session-termination path.

### 1.2 What the product actually does (Observed, from source)

| Fact | Evidence |
|---|---|
| A real logout routine exists and is live | `ACMO_New.Master.cs:124` `LogoutUser(reason, domain)` |
| It removes the server-side session from the session registry | `ARCOSUserSessions.Remove(lLoginUserDetail.SessionID)` — `ACMO_New.Master.cs:135` |
| It abandons the ASP.NET session and returns to login | `Session.Abandon();` then `Response.Redirect("~/frmLoginACMO.aspx")` — lines 136, 138 |
| Idle timeout is enforced | `CheckIdleTimeout(domain, Timeout)` — `ACMO_New.Master.cs:43`; fires `LogoutUser("session timeout", …)` at line 97 |
| Idle threshold | `Timeout` defaults to **10 minutes** (`:43`, `:226`) and is overridden per user from `lLoginUserDetail.KeepSessionActive` (`:243`) |
| Authenticated ASP.NET session lifetime | **120 minutes**, set at runtime — `Session.Timeout = 120;` (`:242`), and `CalculateNewSessionTimeout()` returns a hardcoded `120` (`:156`) |

**Conclusion.** The product terminates sessions by design: an idle session is abandoned and removed
from the session registry, and the ASP.NET session expires at 120 minutes. Cleanup is
**request-driven** — `LogoutUser` runs during a page load — which is ordinary ASP.NET behaviour, not
a defect. A session belonging to a client that simply vanished persists until the 120-minute
expiry. **That is expected behaviour for a stateful web application.**

### 1.3 What we did wrong (Observed, from our own code)

| Our defect | Evidence | Status |
|---|---|---|
| `login-browser.js` created a browser context per iteration and only called `page.close()` — never `context.close()`, so contexts and cookies leaked and sequential iterations were **not independent** | the pre-fix file; this is the flow that was being demonstrated | **Fixed** — `clearCookies()` + `context.close()` teardown added |
| `login-api.js` never reset the k6 cookie jar, which is per-VU and **persists across iterations**, so iteration 2 still carried iteration 1's authenticated cookie. The file's own comment claimed the opposite | pre-fix file, `export default function` entry | **Fixed** — `resetSessionJar()` at iteration entry and exit |
| The sanity scenario never released app windows | no `context.close()`, no window close | **Fixed** — `closeAppWindow()` per module |

**We never triggered the product's logout path, never closed contexts, and repeatedly logged in on
one shared account.** The symptom was created by our harness.

### 1.4 The rejection storm — still NOT attributed

Run `2026-08-18_120004` aborted after 3 consecutive rejections classified **`unknown`**. The
classifier matches five known messages, including `account_locked` and `max_sessions`
("maximum session limit exceeds"); the responses matched **none** of them. So the storm was
**neither a lockout nor a session cap**. Grade: **`Requires further investigation`.** A diagnostic
that logs the actual rejection text has been added and costs no extra login attempt; if it recurs,
the cause will be named. ⛔ Do not attribute it to the product without that message.

### 1.5 One product observation, not raised (owner's call)

`web.config:131` sets `<sessionState cookieless="false" mode="InProc" timeout="9999" />` —
**9,999 minutes ≈ 6.94 days**. The authenticated path overrides this to 120 minutes at runtime, so
it does **not** explain any behaviour we measured, and it is **not** the cause of our symptom.
It remains poor hygiene for a privileged-access product (it governs pre-authentication sessions,
and `InProc` holds them in memory). **Severity: low. Recorded, deliberately not raised** — the
evidence does not support calling it a defect, and no measured impact is attached to it.

---

## 2. The 10 failed modules — root cause, with evidence

### 2.1 The conclusive evidence

Two failure messages, captured from run `2026-08-18_152615`:

- **Mode A** (3 modules): `the tile click opened no new window`
- **Mode B** (7 modules): `waiting for "//*[@id='ctl00_MainContent_lblHeader' or @id='ctl00_MainContent_lblMenuName'] >> nth=0": timed out after 20000ms`

Mode B names the readiness signal our harness waits on. Measured presence of those control IDs in
the product source:

| Application tree | Files containing `lblHeader` / `lblMenuName` |
|---|---:|
| `ARCON_ACMO` | **76** |
| `ARCON_ACM` | **0** |
| `ARCON_Services` | **0** |
| `frmAbout.aspx` (inside ACMO) | **0** |

**The app tiles open separate ARCON applications** — the product tree contains `ARCON_ACM`,
`ARCON_ASM`, `ARCONUserDiscovery`, and others as distinct web apps. `ctl00_MainContent_lblHeader` is
an **ACMO master-page control ID**; a different application cannot have it. And `frmAbout.aspx`,
though it *is* an ACMO page, does not use that control either.

**So our readiness assertion could never succeed for those 10 modules, regardless of product
health.** This is an automation defect, conclusively.

### 2.2 What the functional Java suite does instead (the source of truth we failed to mirror)

`DevOpsSanityHelperPage.navigateToApp` (`:51-67`):
`navigateToMenuOptionOn(manager).openMyAppsOption(appName)` then **`switchToWindow(appName)`** —
with a documented special case where the tile label `Access Control Manager` opens a window titled
`Access Control`. Each module then validates its **own** element table
(`AdminConsole_Elements`, `AccessControl_Elements`, …) via per-module data providers, not one shared
heading. Our harness used a single generic heading for all 14 modules.

### 2.3 Per-module determination

| # | Module | Mode | Root cause | Owner |
|---|---|---|---|---|
| 1 | `about` | B | Waits for a heading control `frmAbout.aspx` does not contain (0 occurrences) | Automation |
| 2 | `session_monitoring` | A | New application window not captured by the k6 browser context | Automation |
| 3 | `pam_logs` | A | Same as #2 | Automation |
| 4 | `uag` | A | Same as #2 | Automation |
| 5 | `digital_vault` | B | ACMO-only heading applied to a separate application | Automation |
| 6 | `settings` | B | Same as #5 | Automation |
| 7 | `admin_console` | B | Same as #5 | Automation |
| 8 | `password_vault` | B | Same as #5 | Automation |
| 9 | `access_control` | B | Same as #5, plus the tile-label / window-title mismatch | Automation |
| 10 | `user_discovery` | B | Same as #5 — `ARCONUserDiscovery` is its own application tree | Automation |

⚠️ **Product health for these 10 modules is NOT established by this run, in either direction.** Our
harness failed before it could observe them. We have **not** executed the Java functional suite
against this build, so "the modules work" is an inference from the existence of working functional
navigation code, not a measurement. Grade: **Likely healthy, not verified.**

### 2.4 What must be fixed in our harness

1. **Per-module readiness signals** sourced from each module's own element table, replacing the
   single ACMO heading. `sanity-modules.json` already carries a `heading` and `table` per module —
   the k6 scenario ignores both.
2. **Window handling** — mirror `switchToWindow(appName)`; the current `waitForEvent('page')`
   approach captured no window for 3 modules. Verify whether k6's browser module surfaces a
   target opened by a tile at all before investing further.
3. **`access_control`** — tile label `Access Control Manager`, window title `Access Control`. The
   registry now records both (`nav.label`, `nav.windowTitle`); the scenario must use the right one
   for each purpose.

---

## 3. Summary

| Question | Answer |
|---|---|
| Is the session leak ours or the developer's? | **Ours.** The product has a working logout path, a 10-minute idle timeout and a 120-minute session expiry. Our harness never closed contexts, never reset the cookie jar, and never triggered logout. All three fixed |
| Jira ticket raised? | **No.** The evidence does not establish a product defect. Raising one would be unsupported |
| Root cause of the 10 module failures | **All 10 are automation defects** — a readiness selector that does not exist outside ACMO (7) and uncaptured application windows (3) |
| Which failures need development action? | **None** |
| Which are automation / environment / test data? | **All 10 automation.** No environment or test-data cause found |
| Unresolved | The `unknown` rejection storm of run `120004` — `Requires further investigation`; diagnostic now in place |

---

## 4. Addendum — re-execution after the fixes, and two findings that invalidate today's timings

### 4.1 The fixes worked: coverage went 3 → 12 of 13 modules

Root causes from §2 were fixed in `browser/sanity/sanity-browser.js`: per-module readiness signals
(ACMO heading → the module's own `heading` text → window title, with the matched signal logged), the
`data-bs-original-title` tile selector, async polling for the new application window, and a
main-page close guard. Run `2026-08-18_165358` (3 concurrent) measured **12 of 13** modules.

### 4.2 ⛔ Finding A — coverage is NOT reproducible

| Run | VUs | Modules measured | Check rate |
|---|---:|---:|---:|
| `2026-08-18_165358` | 3 | **12 / 13** | 0.691 |
| `2026-08-18_170008` | 1 | **10 / 13** | 0.786 |
| `2026-08-18_170645` | 1 | **5 / 13** | 0.429 |

Three runs inside 15 minutes, same scope, same credential. Causes identified per run:
`165358` — **two of three Chromium processes died** (`process with PID … unexpectedly ended: exit
status 1`, `category=browser`), so later modules lost samples; `170008` — a self-inflicted defect,
`waitForNewPage` returned `pages[length-1]` which was the **main page**, and closing it killed the
next two modules (since fixed by identity matching plus a close guard); `170645` — repeated
`recovery-failed` on the landing page followed by total context collapse in under 2 seconds.

⚠️ **No run today is a valid performance baseline.** Coverage of 12/13 proves the *capability*; the
*timings* are not trustworthy — see Finding B.

### 4.3 ⛔ Finding B — every timing today is contaminated by concurrent API load

The `OBJ-020` API execution (`chain_runner`, pid 8724) has been running **continuously since
11:30:32**, ~5.6 h, against the **same `QA_MsSQL` environment**, for the whole period in which these
web-tier measurements were taken. The degradation is visible in the data:

| Measurement | 14:28 (`142809`) | 17:00 (`170008`) | 17:06 (`170645`) |
|---|---:|---:|---:|
| `session_monitoring` load | 15,980 ms | 28,205 ms | — |
| `pam_logs` load | 16,646 ms | 33,661 ms | — |
| Landing-page recovery | fine | fine | **timing out** |

**Grade: `Likely` — the correlation is strong and the mechanism is plausible, but no isolated control
run exists.** Confirming it requires one sanity run with the API execution stopped. Until then, no
latency figure from today should be quoted as a PAM performance characteristic.

### 4.4 Remaining module failure

`uag` — tile `//*[@data-bs-original-title='User Access Governance']` **not clickable after 20 s in
both runs that reached it**. The label matches `PAMSpecifcConfigs.uag` exactly, so it is not a naming
error. Most likely the tile is absent for `arcosadmin` on this build (provisioning/licensing) rather
than broken. **Grade: `Requires further investigation`** — settled by one look at the Manager page
for this user. Still **not** a product defect on current evidence.
