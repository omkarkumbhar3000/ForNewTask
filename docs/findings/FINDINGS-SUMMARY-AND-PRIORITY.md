# PAM API — Findings Summary and Fix Priority

**From:** QA Automation · **For:** Management and the PAM development team
**Basis:** two measured runs — **1,868 live API calls** across 870 endpoints, and **5,416 calls**
across **1,388 endpoints** — plus static analysis of the endpoint catalogue, 6,866 `.cs` product
files and the 2,470-page API reference. **Every figure below is measured, with an evidence file
per call.**
**Findings:** 13 · **Raised in Jira:** 1 (`PAMIT-42744`) · **Prioritisation:** requested by the
development team

> ✅ **This document is cleared for sharing.** It contains no credentials, no user identities, no
> internal hostnames and no exploit detail. See §7 for what was deliberately left out and why.

> 🤝 **Tone.** These are engineering observations, not criticism. Several are historical accretion
> rather than anyone's decision. They are listed because each one costs test reliability today.

---

## 1. Executive summary

Automated testing of the PAM API surfaced **13 implementation findings**. They are not a list of
broken features — the product works. They are places where the API's *contract* is ambiguous
enough that automated verification cannot reliably tell success from failure.

**Three things matter most:**

1. **The HTTP status code does not indicate success.** A rejected request usually returns
   **HTTP 200** with the failure carried inside the response body. Measured: **1,688 of 1,868 calls
   returned 200, and 289 of those carried `Success: false`.** Any monitoring or test that checks
   the status code alone reports these as passing.
2. **Two endpoints take the entire API offline.** Three sequential requests were enough to stop the
   IIS application pool and return `503` for everything until manual intervention. This is an
   availability risk in a live environment, not merely a test problem.
3. **An authentication-handling defect was found**, is fully evidenced, and is packaged ready to
   raise. ⛔ Details are deliberately withheld from this document — see §7.

**The business impact is testability.** Until the contract is unambiguous, every automated check
against this API needs bespoke logic to interpret each response, which is why coverage is expensive
to build and fragile to maintain. Fixing the top four findings would let standard tooling verify
the API the way it verifies any other.

**Effort is modest for the highest-value items.** Four of the six highest-priority findings are
rated **Low or Medium** effort. The two largest efforts sit at the bottom of the priority list.

---

## 2. How to read this

| Term | Meaning |
|---|---|
| **Severity** | How badly it affects correctness, availability or trust — independent of effort |
| **Impact** | Who or what is affected in practice |
| **Effort** | Development effort to fix, as estimated from the code |
| **Priority** | **Severity × impact, with effort as the tiebreak.** This is the recommended fix order |

Priority was assigned by putting safety and security first, then correctness defects that make the
API untestable, then everything reachable by a quick win, then the rest.

---

## 3. Prioritised findings — all 13

| Priority | ID | Finding | Severity | Effort | Measured scope | Jira |
|---|---|---|---|---|---|---|
| **P1** | LH-08 | Two endpoints stop the IIS application pool | 🔴 Critical | Medium | **98** endpoints at risk; 3 requests caused a full outage | ⬜ Need to create a ticket |
| **P1** | LH-13 | Authentication-handling defect *(details withheld — §7)* | 🔴 Critical | Medium | Evidenced and packaged, ready to raise | ⬜ Owner decision pending |
| **P1** | LH-02 | `Success: true` returned when nothing was created | 🔴 Critical | **Low** | **2** write no-ops · 8 success-message variants | ⬜ Need to create a ticket |
| **P1** | LH-01 | HTTP 200 returned for application-level failures | 🔴 Critical | Medium | **289** calls · **276** endpoints | ✅ **PAMIT-42744** |
| **P2** | LH-04 | Error-code register incomplete and undocumented | 🔴 High | **Low** | **108** codes in use vs **4** documented | ⬜ Need to create a ticket |
| **P2** | LH-09 | Service passwords returned in responses | 🟠 Review | **Low** | 23 responses · 21 endpoints | ⬜ Need to create a ticket |
| **P2** | LH-03 | Multiple incompatible response shapes | 🔴 High | Medium | **9** families · 16 variants · 872 endpoints | ⬜ Need to create a ticket |
| **P3** | LH-05 | Declared endpoints return 404 | 🟠 Medium | **Low** | **348 of 1,388** endpoints exercised | ⬜ Need to create a ticket |
| **P3** | LH-06 | Mutation exposed over HTTP GET | 🟠 Medium | Medium | `SetStatus` as GET on **49** controllers | ⬜ Need to create a ticket |
| **P3** | LH-10 | No validation attributes on request models | 🟠 Medium | High | **3** `[Required]` in **6,738** properties | ⬜ Need to create a ticket |
| **P3** | LH-07 | Field naming and types inconsistent | 🟠 Medium | High | **61** concepts · 7 spellings of one ID field | ⬜ Need to create a ticket |
| **P4** | LH-11 | Internal detail leaked in error messages | 🟡 Low | **Low** | **16** responses carrying stack traces | ⬜ Need to create a ticket |
| **P4** | LH-12 | Endpoints return unfiltered full datasets | 🟡 Low | Medium | 25 responses ≥100 KB; largest **8.0 MB** | ⬜ Need to create a ticket |

---

## 4. Why each priority tier is grouped that way

### P1 — Fix first (4 findings)

**LH-08 — availability.** Two read-only diagnostic endpoints hang for 30 seconds and stop the
application pool. **Three sequential requests took the whole API to `503` with no recovery without
intervention.** This is first because it is the only finding that can remove the service entirely,
and because it is reachable by an ordinary GET. Our own harness permanently blocklists these
endpoints, which means they are also permanently **untested**.

**LH-13 — security.** An authentication-handling defect, fully evidenced. ⛔ Withheld here (§7).

**LH-02 — `Success: true` when nothing was created.** A create that silently does nothing while
reporting success is the worst case for automation: the test passes, the data is absent, and the
failure appears later somewhere unrelated. **Low effort** — this is the fastest critical win.

**LH-01 — HTTP 200 for application-level failures.** The broadest finding: **289 calls across 276
endpoints**. Already raised as `PAMIT-42744`. There is a concrete lever — the server already emits
a structured error-code prefix, so the fix is mapping existing codes to status codes, not
redesigning the API.

### P2 — High value, mostly quick (3 findings)

**LH-04** — **108 error codes in use, 4 documented.** Low effort: publishing the register is
largely a documentation task, and it unblocks precise assertions everywhere else.
**LH-09** — service passwords appearing in responses. Rated *Review* rather than Critical because
the caller is already authenticated, but it is low effort and worth closing.
**LH-03** — **9 response-shape families** across 872 endpoints. Every additional shape is bespoke
parsing logic for every consumer.

### P3 — Medium (4 findings)

**LH-05** (348 of 1,388 declared endpoints return 404) is low effort and mostly catalogue hygiene.
**LH-06** (state change over GET on 49 controllers) matters because anything that pre-fetches a URL
can trigger it. **LH-10** and **LH-07** are the two **High**-effort items — real value, but they are
refactors, so they are sequenced last deliberately.

### P4 — Low (2 findings)

**LH-11** (16 responses with stack traces) and **LH-12** (unfiltered datasets, largest 8.0 MB).
Worth fixing, not worth delaying anything else for. Note **LH-12 and LH-08 are the same defect
class** — unbounded queries — and LH-08 is its fatal case, so fixing LH-08 properly may resolve
LH-12 as a side effect.

---

## 5. Suggested sequencing

| Step | Findings | Why this order |
|---|---|---|
| 1 | LH-08, LH-13 | Availability and security first. Neither can wait on a refactor |
| 2 | LH-02, LH-04 | Both **Low** effort, both unblock automated verification immediately |
| 3 | LH-01, LH-03 | The contract fixes. Largest testability payoff |
| 4 | LH-09, LH-05, LH-11 | Low effort, closes three findings cheaply |
| 5 | LH-06, LH-12 | Same defect family — bound the queries once |
| 6 | LH-10, LH-07 | The two High-effort refactors, last by design |

**Related findings that share a fix.** LH-04 and LH-11 were both found *inside* LH-01's responses;
LH-02 is the `Success: true` half of LH-01; LH-08 is the fatal case of LH-12; LH-06 and LH-08 come
from the same 49-controller diagnostic scaffold. Grouping them at triage avoids the same code being
touched five times.

---

## 6. Evidence

Every finding has its own folder under `artifacts/loopholes/LH-NN-*/` containing a Jira-ready
write-up, a full evidence document, an Excel workbook and the raw captured data.

**Re-validation:** 8 of 13 findings were re-executed against a live environment and reproduced —
for example LH-01 reproduced **289 of 289**. Where re-validation is marked withheld, that is
deliberate: those calls would mutate data, and **LH-08 is never re-run at all** because doing so
takes the environment down.

---

## 7. What was deliberately left out of this document

Stated plainly so nobody assumes an omission is an oversight:

| Withheld | Reason |
|---|---|
| **LH-13 specifics** — affected endpoint names, counts, the reproduction, and which operations are reachable | It is an **open, unpatched and unraised** defect. This document is written to be shared; a working reproduction should not travel with it. The full detail exists in the evidence pack and should reach the development team through a **restricted channel** |
| **User identities** | The raw evidence contains **452 distinct email addresses and 1,456 usernames** captured from the test environment |
| **Internal hostnames and addresses** | The raw evidence references internal and production hostnames and an internal IP |
| **Credentials** | None exist to withhold — verified: **63,771 credential values are redacted**, and a scan found **zero** live tokens or password assignments |

⚠️ **This is why the summary is the shareable artefact and the full evidence folder is not.**
See the sharing guidance issued alongside this document.
