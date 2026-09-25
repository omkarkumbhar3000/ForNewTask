# PAMIT daily review — tracking format

**What:** one command that reports every tracked finding group — its ticket, status and assignee —
and flags the ones that are **our** action.
**Cadence:** daily. **Source of truth:** live Jira, read fresh on every run.
**Registry:** `tracked-tickets.json` · **Runner:** `track_tickets.py` · **Snapshot:** `.tracking-state.json`

> ⛔ **Read-only.** The tracker issues `GET` requests only. It never transitions, comments on,
> assigns, edits or creates an issue. A tracker that can mutate the board is one you cannot
> safely run unattended.

---

## 1. Run it

```powershell
python tools\jira\track_tickets.py              # the daily review
python tools\jira\track_tickets.py --json       # machine-readable
python tools\jira\track_tickets.py --no-state   # report without updating the snapshot
```

**Exit code** — so it can drive an alert without parsing text:

| Code | Meaning |
|---:|---|
| `0` | Nothing needs us |
| `1` | **Action items present** |
| `2` | A Jira lookup failed — treat as unknown, not as "clean" |

---

## 2. The two action rules

Agreed with the owner. Everything else is reported for awareness but **not** flagged, which is
what keeps the daily list short enough to actually read.

| # | Condition | Why it is ours |
|---:|---|---|
| **1** | `status == "QA Testing"` — **any assignee** | It needs QA verification, and QA is us |
| **2** | `status == "Awaiting Response"` **AND** assignee is **Omkar Kumbhar** | The reply is owed by us |

⚠️ **`Awaiting Response` assigned to anyone else is deliberately NOT flagged.** It is reported with
the note *"their action"*. Flagging it would fill the review with other people's work.

**Assignee matching is belt-and-braces:** the Atlassian `accountId` from `/rest/api/3/myself` is
compared first, with a case-insensitive display-name match as fallback. Account ID survives a
display-name change; the name catches the case where the ticket is assigned to a different
Omkar Kumbhar account than the API token's.

✅ **Both status strings are verified against the live PAMIT Bug workflow** (26 statuses).
`QA Testing` and `Awaiting Response` both exist verbatim. This matters: a tracker matching a
status name that does not exist reports "nothing needs us" forever and looks healthy while doing it.

---

## 3. Reading the output

```
->A1     PAMIT-42744   Open                   Trupti A Shirdhankar     2026-08-11
!!B1     PAMIT-43050   QA Testing             Somesh Hinduja           2026-08-12
         changed: Open -> QA Testing
  A2     —             Need to create a ticket —    LH-13, LH-09
```

| Marker | Meaning |
|---|---|
| `!!` | **Action item — ours.** Listed again in full underneath with the reason and URL |
| `->` | Status changed since the last review |
| *(blank)* | Unchanged, not ours |
| `—` in the Ticket column | **Need to create a ticket** — the group is scoped but unraised |

**"Reaches QA Testing" is a transition, not a state.** The run compares against
`.tracking-state.json` from the previous review and marks changes `[NEW since last review]`. The
first run has no baseline, so anything already matching is reported as NEW once.

Unraised groups stay in the table on purpose — work that has not been raised should not be
invisible just because it has no ticket.

---

## 4. Adding a ticket

When a group is raised, set its `key` in `tracked-tickets.json`. That is the only edit:

```json
{ "group": "B2", "key": "PAMIT-XXXXX", ... }
```

Nothing else needs changing — the tracker picks it up on the next run.

---

## 5. Current coverage

| Programme | Groups | Raised | Awaiting creation |
|---|---:|---:|---:|
| API implementation | A1–A5 | 1 (`PAMIT-42744`) | 4 |
| Repository size | B1–B4 | 1 (`PAMIT-43050`) | 3 |

⛔ **A2 contains `LH-13`**, the open authentication finding. It is held by owner decision and
may need restricted visibility when raised — see the note on that entry in the registry.
