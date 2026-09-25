# Phase 5 — Safety and operations

**Purpose:** run at scale without harming the environment, the accounts, or the run itself.
**Principle:** deny by default. Every capability that can cause harm is off until explicitly enabled.

Everything here was learned by something going wrong on the reference project. None of it is
precautionary theory.

---

## 1. The controls, and what each one prevents

| Control | Setting | Prevents |
|---|---|---|
| **Plan-only default** | A bare run issues **zero** HTTP calls; an explicit flag is required | An exploratory command becoming a live run against a shared environment |
| **Blocklist** | Action-name substrings, enforced at *planning* time | Calling an endpoint that takes the service down. Three sequential calls to one endpoint took the reference API to `503` with no recovery |
| **Destructive-name guard** | Name-based regex, refused unless teardown is permitted | Deleting data the run did not create. **Verb guards do not work** where deletion is a `POST` |
| **Throttle** | Fixed delay, or limit-aware backoff where limits are published | Rate-limit rejection being misread as a product failure |
| **Circuit breaker** | Pause after N consecutive `5xx`/timeouts | Hammering an environment that is already down |
| **Downtime wait + resume** | Wait, probe, resume **from the paused hop** | Restarting a multi-hour run, and losing the work already done |
| **Checkpoint after every flow** | `--resume <folder>` skips completed work | Total loss on a crash at hop 3,000 of 5,400 |
| **One credential per run** | Cached, latched on failure | Locking an account that other systems depend on |
| **Redaction before disk** | Substring match on secret-ish keys | Evidence files becoming a credential leak |
| **Body cap** | Hard byte limit per response | One unfiltered endpoint returning megabytes and exhausting memory |

---

## 2. Blocklist enforcement — where, not just whether

**Enforce at planning time, before a request is constructed.** A blocklist consulted at send time
still requires the code path to reach send, and one refactor later it will.

Three checks in sequence, all before any I/O:

1. Does the action name match a blocklist entry? → withhold, record **Blocked** with the reason.
2. Does it match the destructive-name guard, without teardown permitted? → withhold, record **Blocked**.
3. Is the verb outside the allowed set? → withhold, record **Blocked**.

⛔ **A withheld call is `Blocked` with a per-item reason. Never `Skipped`, never absent.** The
distinction matters to a reader: *skipped* implies unimportant, *blocked* implies known-and-withheld.

⚠️ **Parse the path before you trust the action name.** Splitting a path on `/` *before* stripping
its query string yields a garbage action name — and that name is exactly what feeds the blocklist and
the destructive guard. On the reference project a query containing a date produced a nonsense action;
the measured impact was one row and no changed guard decision, but the class of bug is a safety
failure, not a cosmetic one. It also crashed a four-hour run by producing an illegal filename.

---

## 3. Credential handling

**One attempt, then latch.** Resolution order:

```
environment variable  ->  valid cache  ->  ONE live attempt  ->  latch and stop
```

| Rule | Why |
|---|---|
| Never retry a failed credential call | A lockout deepens. Stop and report |
| A failure latches **persistently** | It must block later attempts in this run *and future runs* until a human clears it. Otherwise "once per run" becomes an unbounded retry loop across many runs — which is how the reference account was locked |
| Network faults latch too | A timeout is indistinguishable from a refused login, and guessing wrong costs an account |
| An out-of-band token is the safest unattended path | It bypasses the credential endpoint entirely |
| Never blank a stored credential to force a refresh | If the code path re-requests when the value is empty *and* runs per test, one blank field becomes one credential request per test across a whole suite |

The single-gate design matters more than any individual rule: **exactly one code path may reach the
credential endpoint**, and it owns the cache, the latch, and the attempt counter. Enforcement that
depends on every caller remembering the policy is not enforcement.

---

## 4. Environment instability is a first-class cost, not an exception

On the reference project's full run, **85 of 329 minutes** were spent waiting for the environment
across **17 downtime pauses** — 26% of wall-clock. The run still completed with full coverage,
because wait-and-resume was built *before* scaling up rather than after.

| Behaviour | Detail |
|---|---|
| Detect | Consecutive `5xx`/timeouts trip the breaker |
| Wait | A fixed interval, then probe with the safe health-check endpoint |
| Resume | Continue **from the paused hop**. Never restart |
| Give up | After N failed probes, abort *that flow* — and **re-queue it**, do not mark it done |
| Report | Count the pauses and the minutes lost. It is usually the largest single cost |

⛔ **A checkpoint must distinguish "completed" from "gave up".** On the reference project `--resume`
treated an aborted flow as complete because it appeared in the checkpoint, which would have silently
dropped coverage from a resumed run. Add an explicit gate — *no flow left aborted* — so the class of
error cannot recur unnoticed.

⚠️ **A resumed run lies about its own metadata.** Elapsed time, call counts and downtime events
recorded by the final process describe only that process: the reference run reported 94.9 minutes
against 329.1 actual. Reconstruct totals across segments, or every performance figure is wrong by the
size of the first segment.

**Tuning note:** most pauses recover on the first probe, so a flat long wait spends more time idle
than necessary. A short first probe with backoff is strictly better.

---

## 5. Data hygiene

| Concern | Handling |
|---|---|
| Records created by the run | Suffix every identity field with a run-scoped random seed, and **list the seeds in the report** so cleanup is possible later |
| Teardown | Disabled by default. `created-only` is the sane middle: delete what this run created, nothing else |
| Repeat runs | Without unique identity fields the second run gets "already exists" — which may score as a *pass* if success-message semantics are not asserted |
| Secrets in evidence | Redacted before the write, not after. There is no second chance on a file that already exists |

---

## 6. Exit gate

| ✅ | Condition |
|---|---|
| ☐ | A bare run makes zero HTTP calls |
| ☐ | Every blocklisted and destructive action was withheld and counted as **Blocked**, with a reason |
| ☐ | Exactly one credential request was made, or zero if a cached or out-of-band token was used |
| ☐ | The run survived at least one simulated interruption and resumed from the paused point |
| ☐ | No flow ended in an aborted state; anything aborted was re-queued and executed |
| ☐ | No secret appears in any file written to disk |
| ☐ | Created-record seeds are recorded in the report |
