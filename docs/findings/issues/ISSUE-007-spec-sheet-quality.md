# ISSUE-007 — The shared Swagger link sheet is 46% duplicate rows, with malformed and contradictory entries

**Severity:** 🟡 Low (quality of a hand-off artefact) · **Type:** Process / data quality
**Raised:** 2026-07-28 · **Source:** `data/sources/Automation PAM Endpoints Details_Shared(Swagger_JSON Links).csv`
**Evidence:** `../Execution/spec_quality.json`

---

## 1. Statement

The sheet the development team shared to hand over the API surface is usable — the harness parses it and
fetched 37 of 38 specs successfully — but it required defensive handling, and its own status column is not
reliable. Recording this because the sheet is now a **dependency of an automated pipeline**, so its quality
determines whether tomorrow's run works.

## 2. Evidence

| Measure | Value | % of 98 rows |
|---|---:|---:|
| Data rows | 98 | — |
| Marked `Done` | 37 | 37.8% |
| Marked `Duplicate` | **45** | **45.9%** |
| Marked `Unavailable` | 15 | 15.3% |
| Blank status | 1 | 1.0% |
| **Distinct usable spec URLs after dedup** | **38** | — |
| Rows with a URL **missing the `https://` scheme** | **7** | 7.1% |
| Specs that failed to fetch | 1 | — |

### Specific problems

**A — 42 consecutive identical rows.** Rows 30–71 are all `Video Logs`, all pointing at the same
`smLogsApi` spec, each marked `Duplicate — Same Data As Link_29`. One row would do.

**B — 7 URLs missing the scheme.** Rows 13–19 (`WebSM-User`, `WebSM-Service`, `WebSM-UserGroup`,
`WebSM-ServiceGroup`, `WebSM-LOB`, `WebSM-Roles`, `WebSM-Tag`) have JSON links beginning
`devint.arconnet.com:555/…` with no `https://`. These fail any naive fetch; the harness now prepends the
scheme defensively.

**C — Host/port disagreement within a single row.** The UAG rows give a Swagger UI link on
`:1302/ARCONAPIGateway/uagchallengeapi/` but a JSON link on `:555/uagChallengeApi/` — different port *and*
different path casing for the same service.

**D — A row marked `Done` that contradicts itself.** Row 91 (`AGWAURLGEN_MICROSERVICE`) has
`Extraction Status = Done` while its comment reads `No Swagger Links are available for this Module`. The
spec does in fact fetch, so the comment is stale — but the two fields disagree.

**E — One spec unreachable without a hosts entry.** Row 92 (`AGWAPI_LINUX`,
`devintagwpamu25.arconnet.com:7038`) fails DNS resolution:

```
URLError: <urlopen error [Errno 11001] getaddrinfo failed>
```

Its own comment documents the workaround — `Add Hosting: 10.10.2.24 devintagwpamu25.arconnet.com` — so this
is known, but it means the spec is not reachable from a standard CI agent without host-file surgery.

**F — Module labels are inaccurate.** Rows 1–11 are all labelled `Password`, but the URLs are eleven
different microservices (`Vault`, `downloads`, `customcommand`, `dashboard`, `dependency`, `envelope`,
`policy`, `reconauto`, `rotate`, `vault`, `logs`). Grouping or filtering by the `Module` column gives wrong
results.

**G — Mixed environments in one sheet.** Row 2 targets `u16hf.arconnet.com`; every other row targets
`devint.arconnet.com`. A run against "the sheet" therefore spans two environments unless filtered.

## 3. Consequence

| Area | Impact |
|---|---|
| **Automation** | The sheet is now an input to a pipeline. Malformed rows, mixed environments and unreachable hosts must each be handled or the run degrades silently |
| **Reporting** | `Module` cannot be used as a grouping key, so coverage-by-module has to be derived from the spec titles instead — which are themselves 29% placeholders (ISSUE-004 B) |
| **Trust** | The `Extraction Status` column cannot be relied on, as row 91 shows |

## 4. How the harness currently compensates

All of this is handled rather than assumed away, and each compensation is logged in
`../Execution/spec_quality.json`:

| Problem | Handling |
|---|---|
| Duplicates | Deduplicated by normalised URL — 98 rows → 38 URLs |
| Missing scheme | `https://` prepended when absent |
| Unreachable host | Recorded as a fetch failure with its exception, never silently dropped |
| Unusable rows | Counted and reported on the **Spec Quality** sheet of the workbook |

## 5. Recommended action

| # | Action | Owner |
|---|---|---|
| 1 | Replace the sheet with a **machine-readable manifest** — one row per service, absolute URL, environment column | Development |
| 2 | Or better: publish a **Swagger aggregation endpoint** on the gateway listing all service specs, so no sheet is needed | Development |
| 3 | Confirm whether `u16hf` (row 2) should be in scope, or whether the sheet should be devint-only | Development |
| 4 | Fix the `Module` labels, or drop the column | Development |

**Item 2 removes this issue permanently** and is the standard pattern for a gateway fronting many services.
Until then the harness will keep parsing the sheet defensively.
