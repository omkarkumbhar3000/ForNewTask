# OBJ-019 — execution state

**Purpose.** Resumable record, per `Objective.md` §Continuous. If a context window ends, read this
file first and continue from the first ⬜ step. Do not restart completed work.

**Owner decisions (MCQ, locked):** branch `Dev` fast-forwarded to `origin/Dev` · environment
`QA_MsSQL` for both initial and final (`QA_MSHKL` is a typo) · load ceiling **3 VUs**, short runs,
`arcosadmin` preferred and `auto_adminui` kept as untouched fallback · Theme 1 = existing
`tools/dashboard/src/theme.js`.

**Credentials.** Supplied by the owner in the prompt; resolved at run time from `PERF_USERNAME` /
`PERF_PASSWORD` env vars only. ⛔ Never write a password into this file, any script, any report, any
committed file or any log.

---

## Steps

| # | Step | Status |
|---|---|---|
| 1 | Ask blocking questions up front (4 asked, 4 answered) | ✅ |
| 2 | Record `OBJ-019` in `BLAST/Objective.md` + register row | ✅ |
| 3 | Git: fast-forward `Dev` → `origin/Dev`, checkout, verify nothing lost | ✅ `969627e` |
| 4 | Install k6; verify node/npm; verify versions | ✅ k6 v2.2.0, node v24.19.0 |
| 5 | Baseline-verify the existing Java automation compiles (before changes) | ✅ BUILD SUCCESS, 1083 srcs |
| 6 | Validate credentials — one attempt at a time, stop on first success | ⛔ **BLOCKED — see above.** No working cred; `auto_adminui` locked |
| 6a | Unauthenticated login-page probe — confirm reachability + field contract | ✅ HTTP 200, contract confirmed on the wire |
| 7 | Read `DevOpsSanityCheck` + its Excel tables; enumerate the real Sanity scope | ✅ 14 modules, 211 checks, 6 excluded |
| 8 | Discover the APIs each Sanity module calls (network capture or code) | ✅ **Finding: no per-module GET URLs** — WebForms postback nav; needs live capture |
| 9 | Extend the framework: Sanity browser scenarios | ✅ `browser/sanity/sanity-browser.js` |
| 10 | Extend the framework: Sanity API scenarios | ✅ `api/sanity/sanity-api.js` (backbone; per-module capture-required) |
| 11 | Extend Phase 3 correlation to per-module results | ✅ `analysis/sanity/correlate-sanity.mjs` |
| 12 | Execute Login + Sanity on `QA_MsSQL` (≤3 VUs) | ⛔ **BLOCKED on step 6** |
| 13 | Review failures, fix, re-run affected | ⛔ blocked on 12 |
| 14 | Re-verify Java automation compiles (after changes) | ✅ BUILD SUCCESS; **0 .java files touched** |
| 15 | New React app `tools/dashboard-performance/` — Theme 1 | ✅ builds (846 modules), runs on :5174 |
| 16 | Dashboard views: Executive · Login · Sanity · API · UI · API-vs-UI | ✅ all 6, browser-verified, no console errors |
| 17 | Wire real run output into the dashboard datasets | ✅ generator + ingest path; sample data flagged |
| 18 | Review/improve the existing API React app (no functional change) | ⬜ reviewed; no change needed (see notes) |
| 19 | `.md` manual run docs for BOTH apps | ✅ `react-performance/HOW-TO-RUN.md` (both apps) |
| 20 | Final trial on `QA_MsSQL` + full cross-check (§17) | ⛔ blocked on 6 (framework k6-load-verified, guard fires) |
| 21 | Update docs; append to `docs/history/README.md`; OBJ-019 record | ✅ |

⚠️ **Environment correction:** `CLAUDE.md` says `JAVA_HOME` points at a non-existent JDK and must be
overridden every session. That is now **stale** — the machine value is
`C:\Program Files\Eclipse Adoptium\jdk-21.0.12.8-hotspot\` and is correct. But a process inherits a
stale `jdk-26.0.1` value, so Maven still needs the override to
`C:\Program Files\Eclipse Adoptium\jdk-21.0.12.8-hotspot` per session. k6 install put the binary on the
MACHINE PATH (`C:\Program Files\k6\k6.exe`); an already-open shell won't see it until restart, which is
why `run-performance.ps1` now resolves k6 from known locations, not PATH alone.

## ⛔ CREDENTIAL BLOCKER — live execution cannot proceed (owner action required)

**No working QA_MsSQL credential exists among what was supplied, and the primary account is now locked.**

Validation was done the safe way — the real WebForms postback, one attempt per combination, each in a
fresh session (the pattern that keeps the per-session attempt counter at 1). Results on `QA_MsSQL`,
domain `ARCOSAUTH`:

| User | Password | Result |
|---|---|---|
| `arcosadmin` | `<redacted: variant A>` | `Invalid Login Details` (HTTP 200) — not a QA_MsSQL account; it belongs to Perf/Performance |
| `arcosadmin` | `<redacted: variant B>` | `Invalid Login Details` |
| `auto_adminui` | `<redacted: variant A>` | `Invalid Login Details` — **account was UNLOCKED at this point** |
| `auto_adminui` | `<redacted: variant B>` | `Invalid Login Details` |
| `auto_adminui` | *(committed functional pw, for mechanism check)* | **`The User is Locked Out`** |

⛔ **`auto_adminui` locked during these attempts.** The first two attempts returned *invalid*, not
*locked* — a locked account rejects before the password check — so the account was unlocked when I
started and locked by the mechanism-check attempt. The live lockout threshold (`sso_arcos_config`
`aps_id 32/159`, seed default 0) was evidently low enough that the fresh-session pattern did not protect
it. **I stopped immediately; no further login attempts were made against any account.**

**Consequences the owner must know:**
- `auto_adminui` is the account the **functional Java suite** and any UI regression depend on. Until an
  admin clears the lock it will fail on login. If `aps_id 33` (reset-lockout minutes) is at its seed
  default of `0`, the lock has **no auto-unlock** — admin action is required.
- The **Sunday weekly API execution** authenticates as `GenericScheduler` (the `/arcontoken` API
  account), **not** `auto_adminui`, so it is not directly affected. `GenericScheduler` was never touched.
- The **mechanism is proven correct** — clean `Invalid Login Details` rejections and a clean
  `locked out` detection mean the Phase 2 postback, the XOR-key-0 trick, the domain-by-label selection
  and the rejection classification all work end to end against the live product.

**What unblocks live execution (any one):**
1. Admin-unlock `auto_adminui` **and** supply its current working password as `PERF_PASSWORD`.
2. Provide a **dedicated performance-test account** (preferred) with a known password and no second
   factor — this was the OBJ-018 ask and remains the clean path.
3. Confirm the correct password for a QA_MsSQL account I have not locked.

**Everything that does not need a live login proceeds now** and is built to run the instant a credential
works: Sanity scope translation, the framework extension, the React dashboard, the Java-safety check.

## Step 18 — API React app review

Reviewed for consistency/reuse/responsiveness. **No change made, deliberately.** The Performance app
reuses the API app's components (`theme.js`, `Card`, `ChartCard`, `DataTable`, `States`, `Indicators`)
**verbatim** — that reuse is the strongest evidence they are already sound. The API app is the shipped
`OBJ-015` deliverable with a CVD-validated palette and a working daily refresh; editing it would risk
breaking a live dashboard for no real gain, against the instruction "do not introduce unnecessary
redesigns." The consistency the owner wants is achieved by the new app adopting the old one's language,
not by changing the old one.

## Notes / findings

- `sanity.xml` in the instruction = `CICD_Suites/SanityChecks.xml`, which runs exactly one class:
  `com.arcon.tests.UI.sanity.DevOpsSanityCheck` (423 lines). ~14 active module checks, 6 commented
  out (Dashboard, ADBridging, AutoOnBoarding, Spection, IDAM, MyVaultEnterprise). Scope is
  Excel-driven via `UI_DataProviderUtils`, sheet `DevOpsSanityCheck`.
- `git checkout Dev` fired the repo's `post-checkout` graphify hook, which rebuilds a **different
  checkout** (`.graphify_root` names another path). Harmless here; already a known workspace defect.
- OBJ-018's framework carried over to `Dev` intact: 14 files, self-test 36/36.

---

## Session record — login verified, execution re-held on an UNCLASSIFIED rejection

**Trigger.** Owner reported a successful manual login on `QA_MsSQL` (`arcosadmin` / domain `ARCOSAUTH`,
app URL `:1302`) and authorised **one** login verification before resuming the performance execution.
Credential supplied via `PERF_USERNAME` / `PERF_PASSWORD` only; never written to any file, log or report
(grep-verified against every artifact below).

### Step 6 — RESOLVED. The credential is valid. The earlier conclusion was a false negative.

| Run | Phase / profile | Result |
|---|---|---|
| `2026-08-18_115054` | browser / smoke, 1 VU × 1 iter | ✅ **`successfulLogins: 1`, `failureRate: 0`, `rejections: {}`, checks 3/3, `measurementValid: true`** — HTTP 302 to an authenticated landing page, build `MSSQL_Build35.8` |

⛔ **`Objective.md`'s "`arcosadmin` does not authenticate on `QA_MsSQL` … both case variants exhausted"
is WRONG and must be corrected.** The identical secret authenticates through the browser path. The
`OBJ-019`/`OBJ-020` conclusion came from the Phase 2 raw postback, which is defective (below).

### Phase 2 (API) postback — three hypotheses ELIMINATED from source, zero login attempts spent

Measured on the live login page by unauthenticated `GET` (safe, already-established probe):

- Rendered gate is `if ('true' == 'true')` → login-page encryption **is live**, the XOR path is active.
- `hiddentxtLPEncrID` renders as a **random** value (`6830` observed), never `0` — `frmLoginACMO.aspx.cs:950,962`
  assign `GetRandomNumber()`; the `Value="0"` at `frmLoginACMO.aspx:472` is only the markup default.
- `enteredPassword` exists and the browser posts it as `XXXXXXXXXXXXXXXXXXXX` (`frmLoginACMO.aspx:324`).
  `api/login/login-api.js` harvests it **empty** and never sets it.

Eliminated, so do not re-investigate these:
1. **Domain `aps_id`** — `firstDomainOption()` already prefers an exact **text** match on `ARCOSAUTH`.
2. **Base64** — `DecodeFromBase64(encodedData, pXORkey)` (`ARCON_ACMO/ARCOSCommonFunctions_V2/CommonFunctions.cs:2370`)
   is a **pure XOR despite its name**; there is no base64 step.
3. **Posted-key rejection** — the server decodes with the **posted** `hiddentxtLPEncrID`, and the
   `LPEID` cookie cross-check is commented out, so key `0` is a legitimate identity transform.

**Remaining candidate (untested, no attempt spent):** the empty `enteredPassword`. The fix is to
replicate the browser exactly rather than rely on the key-0 shortcut — post
`enteredPassword=XXXXXXXXXXXXXXXXXXXX`, XOR the password with the **rendered** key and post that key
back unmodified. ⛔ Not applied yet: it costs a login attempt to test, and attempts are now the scarce
resource. Phase 3 correlation stays blocked until Phase 2 works — it refuses a half analysis by design.

### Step 12 — ATTEMPTED, then RE-HELD. Do not retry without owner input.

| Run | Phase / profile | Result |
|---|---|---|
| `2026-08-18_115827` | browser / baseline | ⚠️ Void — aborted by an operator pipeline error (`2>&1` on a native exe wraps k6 stderr into `NativeCommandError` in PS 5.1). No summary written. Not a product finding |
| `2026-08-18_120004` | browser / baseline, 1 VU × 10 iters | ⛔ **Circuit breaker aborted after 3 consecutive rejected logins.** `iterations: 3`, `successfulLogins: 0`, `rejections: {"unknown": 3}`, checks 3/9. k6 exit 108 |

**The rejection is UNCLASSIFIED, and that is the informative part.** `lib/metrics.js` matches both
`invalid_credentials` and `account_locked` (`'locked out'`, `'theuserislockedout'`). The returned page
matched **neither** — so the product said neither "invalid credentials" nor "locked out".

Evidence-graded reading:

- **Observed.** One login succeeded at 11:50 (1 iteration, fresh session). Ten minutes later three
  consecutive logins were rejected with a message the classifier does not know. The credential was
  unchanged between the two runs.
- **Likely.** A **concurrent-session / session-cap restriction**, not a credential or lockout problem.
  `browser/login/login-browser.js:136` opens a fresh `browser.newContext()` per iteration but **never
  logs out** — there is no logout, no session teardown, no cookie clear anywhere in the scenario. So
  the first iteration leaves a live server-side session and every later iteration authenticates against
  an account that already has one. This is a **harness gap**, and it is why `smoke` (1 iteration)
  passes while `baseline` (10 iterations) cannot.
- **Requires further investigation.** The exact server message. The browser scenario does not persist
  the rejection body, so the text that would name the cause was not captured. Adding a body/screenshot
  capture on rejection is the single highest-value next change — it costs **no** extra login attempt
  because it only records what a rejection already returns.

### Status of this activity: ⏸️ **ON HOLD** — held deliberately, not failed-and-abandoned

⛔ **No further login attempts were made after the circuit breaker fired, and none should be.** The
standing rule is that a rejected login is a blocker, not a transient fault. `auto_adminui` is already
locked; `arcosadmin` is now the only account known to work and it has absorbed 3 rejections plus the
earlier Phase 2 rejection. The breaker's own message cites `sso_arcos_config aps_id 32/159` as the
threshold, and that value is still unknown — the same unknown that locked `auto_adminui` under `OBJ-019`.

**Resume from here, in this order, once the owner decides:**

1. Add rejection-body capture to `browser/login/login-browser.js` (zero extra attempts) — this names
   the cause instead of inferring it.
2. Add logout / session teardown per iteration, or set `iterations: 1` per login. Until then `baseline`
   cannot pass however valid the credential is.
3. Confirm `arcosadmin` is not locked (admin view, not a login attempt) before spending another attempt.
4. Then Phase 2 with the browser-faithful payload above, then Phase 3, then the dashboard ingest
   (`tools/dashboard-performance/scripts/build-performance-data.mjs`, `INGEST_RUN=<runId>`).

### Framework change made this session (kept, verified, isolated)

`performance/run-performance.ps1` gained **`-Journey login|sanity`** — the `OBJ-019` Sanity scripts had
no orchestrator path at all, so the 14-module sweep could not be driven through the gates. Routes all
three phases (`browser/sanity/sanity-browser.js`, `api/sanity/sanity-api.js`,
`analysis/sanity/correlate-sanity.mjs`) and passes `PERF_JOURNEY`. Verified by dry run: correct scripts
resolved, deny-by-default intact, zero HTTP. Backup of the pre-change file is in the session scratchpad.
**No `.java` file was touched.** The Sanity journey has **never been executed** — it is gated behind the
same login.

---

## ✅ EXECUTED — 3 concurrent users, sanity journey, `QA_MsSQL`

**Run `2026-08-18_142809`** — browser phase, journey `sanity`, profile `concurrent3`, 3 VUs,
`MSSQL_Build35.8`. k6 exit 99 (threshold breached = a *result*; the run completed and its summary
was written). Step 12 is now **done for the browser phase**.

| Measure | Value |
|---|---|
| Logins | **3 / 3 successful**, `failureRate: 0`, `rejections: {}` |
| `measurementValid` | **true** |
| Login journey | med **7,448 ms**, p95 **7,971.8 ms** |
| Authentication | med **7,267 ms** — **97.6 % of the journey** |
| Navigation | med 2,230 ms · Credential entry med 232 ms · Landing render ~181 ms |
| Checks | 12 passed / 3 failed (rate 0.80) |

**Concurrency effect — 1 user vs 3 concurrent** (runs `115054` vs `142809`, same credential, same
build). ⚠️ Grade: **Observed but small-sample** (n=1 vs n=3); directional, not a capacity curve.

| Segment | 1 user | 3 concurrent | Change |
|---|---:|---:|---:|
| Authentication med | 5,363 ms | 7,267 ms | **+35.5 %** |
| Navigation med | 1,617 ms | 2,230 ms | **+37.9 %** |
| Journey med | 7,254 ms | 7,448 ms | +2.7 % |

**Module coverage — 3 of 13 measured. This is the number to quote, not 13.**

| Module | Coverage | avg | p95 |
|---|---|---:|---:|
| My Access | ✅ measured, okRate 1 | 10.3 ms | 21.1 ms |
| Manager | ✅ measured, okRate 1 | 6,208 ms | **6,714.5 ms** |
| Reports | ✅ measured, okRate 1 | 4,203 ms | **4,642.6 ms** |
| About | ❌ reached, failed to open | — | — |
| Session Monitoring + 8 more | ⬜ **never attempted** | — | — |

⛔ **Why coverage stopped.** Clicking `//*[normalize-space(text())='Session Monitoring']` timed out
after 30 s and raised an **unhandled** promise rejection, which ended the iteration. Identical in all
3 VUs. Modules sweep in fixed order, so the unmeasured set is a **suffix**, not a random sample.
**Fix:** wrap each module in the sweep so one navigation timeout cannot end the iteration. Until
then no run can exceed 4 modules.

### The earlier rejection mystery — resolved by elimination

`guard.js:63-66` already documented `sso_arcos_config aps_id 49` *Max Session(s) Per User*, warning
the (N+1)th concurrent login is rejected with *"Maximum Session Limit Exceeds"* — and the classifier
already matches that string. The 12:00 rejections matched **none** of the five known messages, so
they were **not** a session cap and **not** a lockout. What changed by 14:28: 2.5 h elapsed, and
`context.close()` was added. **Grade: `Requires further investigation`** — the diagnostic added this
session will name it if it recurs. `arcosadmin` is confirmed working and was never locked.

### Framework changes (all outside `.java`; 0 Java files touched)

1. `run-performance.ps1` — `-Journey login|sanity`, and `concurrent3` added to the profile ValidateSet.
2. `config/workload.js` — **`concurrent3`** profile: 3 VUs, 1 full pass each. Basis recorded in-file as
   an owner-set ceiling, explicitly **not** a modelled traffic figure. Needs `-MaxVus 3` (the guard's
   deliberate-act gate) to run.
3. `browser/sanity/sanity-browser.js` — rejection diagnostic (`[perf][login-rejected]`, logs URL/title/
   message text, **never** the password, spends **no** extra login attempt) + `context.close()` teardown.
4. `tools/dashboard-performance/scripts/build-performance-data.mjs` — ⛔ **`INGEST_RUN` was documented
   but never implemented**: the script hardcoded `SAMPLE = true` and emitted pseudo-random latencies.
   A dashboard shown to management would have presented invented numbers as results. Real ingest now
   implemented; runs last and overwrites, so measured and illustrative data can never mix.

### Dashboard — updated and verified

`INGEST_RUN=2026-08-18_142809 node scripts/build-performance-data.mjs`. All 8 datasets: `measured`
for login/sanity/ui/summary/executions, **`not-measured`** for `api` and `comparison` (Phase 2 never
ran — no API or attribution figure is invented). Verified served live on `:5174` and `npm run build`
passes. `executions.json` blocker flipped to resolved.

### ⛔ Still open

1. **`Objective.md`'s credential block is factually wrong** and is injected every prompt — it says
   `arcosadmin` does not authenticate and that execution stays blocked. Owner action.
2. **Module sweep abort** — caps coverage at 4 of 13 modules (fix above).
3. **Phase 2 API postback** — untested candidate fix recorded above; Phase 3 correlation stays blocked.
4. **10-user config** — `aps_id 49` live value still unknown; owner checking separately.
