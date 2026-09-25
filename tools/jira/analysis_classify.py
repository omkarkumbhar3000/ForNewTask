#!/usr/bin/env python3
"""Shared Open/Closed and Client/Internal classification for the 2026 census reports.

Imported by both `jira_analysis_2026.py` (PAMIT) and `ci_analysis_2026.py` (CI) so the
two reports cannot drift apart on the definitions that drive every bifurcated table.

⛔ **The owner's status lists are not Jira's spellings.** The lists below are recorded
exactly as the owner gave them; `STATUS_ALIASES` maps Jira's actual value onto the
owner's entry. Matching is case-insensitive and whitespace-collapsed. Measured against
the 21 Sep snapshots, the alias table is the difference between 137/262 unmapped tickets
and 469/691 — three of the four aliases are wording drift and the rest of the gap was
pure capitalisation (`Awaiting Session`, `Patch Shared`, `In Progress`).

⛔ **An unmapped status is never guessed into a bucket.** `classify_status()` returns
`UNMAPPED` and the caller carries it as its own column, because the owner asked for both
"identify unmapped separately" and "counts reconcile". With 137 PAMIT / 262 CI unmapped
tickets those two are only simultaneously satisfiable if Unmapped is visible. The
reconciliation identity is therefore:

    Total Count  = Open Total + Closed Total + Unmapped
    Open Total   = Open Client + Open Internal
    Closed Total = Closed Client + Closed Internal

⚠️ **The internal-client marker differs per project and only one value is live in each.**
PAMIT uses `Internal (ARCON)` / `Internal` / `Internal(ARCON)`; CI uses `Internal Arcon`,
which matches none of PAMIT's variants. Applying PAMIT's set to CI classified 3,713
internal tickets as *Client* — the `D42` error class exactly. The union below reproduces
both projects' published splits from one rule: PAMIT 3,705 client / 2,035 internal,
CI 1,456 / 4,538.

⚠️ **Primary Client is 100% populated in PAMIT and 86.2% in CI.** The 825 CI tickets with
no Primary Client fall to Internal, which is PAMIT's own long-standing rule for `Unknown`.
That is an owner decision, not a measurement: `unspecified_client()` exists so the report
lists those 825 in their own table rather than letting them vanish into Internal (`D46`).
"""
from __future__ import annotations

import collections

# --------------------------------------------------------------------------- statuses

#: Verbatim as the owner listed them. Do not re-spell these to match Jira — that is what
#: STATUS_ALIASES is for, and keeping them verbatim keeps the ruling auditable.
CLOSED_STATUSES = (
    "Closed", "Resolved", "Client Release", "Documentation",
    "Ready for Release", "Document Review", "Rejected",
)

OPEN_STATUSES = (
    "Open", "Awaiting Response", "Dev Analysis", "Business Analysis", "Under obs",
    "Awaiting session", "Security Check", "Dev Review & Testing", "Patch shared",
    "Solution Analysis", "Development", "QA Testing", "Product Hold", "Audit",
    "Reopen", "Forward Merge", "In progress", "Functional Testing",
    "Patch Developed", "Pending from DevOps",
)

#: Jira's actual status value (normalised) -> the owner's list entry (normalised).
#: Only wording drift lives here; pure case differences are handled by _norm().
#: Every entry was confirmed present in the 21 Sep snapshots.
STATUS_ALIASES = {
    "development analysis":               "dev analysis",
    "under observation (no code change)": "under obs",
    "ready for released":                 "ready for release",
    "dev review and testing":             "dev review & testing",
}

OPEN = "Open"
CLOSED = "Closed"
UNMAPPED = "Unmapped"


def _norm(value) -> str:
    """Casefold and collapse whitespace, so `Awaiting  Session` == `awaiting session`."""
    return " ".join(str(value or "").split()).casefold()


_CLOSED_KEYS = {_norm(s) for s in CLOSED_STATUSES}
_OPEN_KEYS = {_norm(s) for s in OPEN_STATUSES}

# Fail loudly at import if an alias points at a status the owner never listed. A typo
# here would silently move tickets into Unmapped, which is the failure this module
# exists to make impossible.
for _jira_value, _owner_value in STATUS_ALIASES.items():
    if _owner_value not in _CLOSED_KEYS and _owner_value not in _OPEN_KEYS:
        raise SystemExit(
            f"analysis_classify: alias {_jira_value!r} -> {_owner_value!r} targets a "
            f"status that is in neither CLOSED_STATUSES nor OPEN_STATUSES"
        )


def classify_status(status) -> str:
    """Return OPEN, CLOSED or UNMAPPED for a Jira status name.

    Never guesses. A status absent from both owner lists, after aliasing, is UNMAPPED
    and must be reported as such.
    """
    key = _norm(status)
    key = STATUS_ALIASES.get(key, key)
    if key in _CLOSED_KEYS:
        return CLOSED
    if key in _OPEN_KEYS:
        return OPEN
    return UNMAPPED


# ---------------------------------------------------------------------- client/internal

#: Every internal-client marker measured across both projects, normalised. The CI-only
#: value `internal arcon` is the one whose absence caused the misclassification noted in
#: the module docstring.
INTERNAL_CLIENT_VALUES = {
    "internal",
    "internal (arcon)",
    "internal(arcon)",
    "internal arcon",
    "internal (bulwark)",
    "wipro internal",
}

#: Values meaning "the field was not filled in". `Unknown` is what the generators'
#: field_value() fallback produces for an absent Primary Client.
UNSPECIFIED_CLIENT_VALUES = {"", "unknown", "none", "not set", "n/a"}

CLIENT = "Client"
INTERNAL = "Internal"


def unspecified_client(primary_client) -> bool:
    """True when Primary Client carries no usable value.

    Kept separate from the Client/Internal split so the report can state how many
    tickets were bucketed by the fallback rather than by a real value (`D46`).
    """
    if isinstance(primary_client, list):
        values = [v for v in primary_client if v is not None]
        return not values or all(_norm(v) in UNSPECIFIED_CLIENT_VALUES for v in values)
    return _norm(primary_client) in UNSPECIFIED_CLIENT_VALUES


def client_bucket(primary_client) -> str:
    """Return CLIENT or INTERNAL for a Primary Client value.

    Internal when any value is a known internal marker, or when the field is unset.
    A multi-valued field naming even one internal party is internal — that is PAMIT's
    long-standing rule, preserved here unchanged.
    """
    if unspecified_client(primary_client):
        return INTERNAL
    if isinstance(primary_client, list):
        if any(_norm(v) in INTERNAL_CLIENT_VALUES
               for v in primary_client if v is not None):
            return INTERNAL
        return CLIENT
    return INTERNAL if _norm(primary_client) in INTERNAL_CLIENT_VALUES else CLIENT


def is_client_ticket(primary_client) -> bool:
    """Back-compatible wrapper — the generators' original predicate."""
    return client_bucket(primary_client) == CLIENT


# ------------------------------------------------------------------------- bifurcation

#: The two header rows every bifurcated table carries. The first row groups, the second
#: names the leaves; the renderers turn this pair into merged cells in .docx and .xlsx.
#: `label` is substituted with the category column's name (Priority, Severity, ...).
BIFURCATED_GROUP_HEADER = ["{label}", "Total Count", "Open", "", "", "Closed", "", "", "Unmapped"]
BIFURCATED_LEAF_HEADER = ["", "", "Client", "Internal", "Total", "Client", "Internal", "Total", ""]


class Bucket:
    """Counts for one category row of a bifurcated table."""

    __slots__ = ("open_client", "open_internal", "closed_client", "closed_internal",
                 "unmapped")

    def __init__(self) -> None:
        self.open_client = 0
        self.open_internal = 0
        self.closed_client = 0
        self.closed_internal = 0
        self.unmapped = 0

    def add(self, state: str, bucket: str) -> None:
        if state == UNMAPPED:
            self.unmapped += 1
        elif state == OPEN:
            if bucket == CLIENT:
                self.open_client += 1
            else:
                self.open_internal += 1
        else:
            if bucket == CLIENT:
                self.closed_client += 1
            else:
                self.closed_internal += 1

    @property
    def open_total(self) -> int:
        return self.open_client + self.open_internal

    @property
    def closed_total(self) -> int:
        return self.closed_client + self.closed_internal

    @property
    def total(self) -> int:
        return self.open_total + self.closed_total + self.unmapped

    def cells(self) -> list:
        """The eight numeric cells, in BIFURCATED_LEAF_HEADER order."""
        return [self.total,
                self.open_client, self.open_internal, self.open_total,
                self.closed_client, self.closed_internal, self.closed_total,
                self.unmapped]

    def merge(self, other: "Bucket") -> None:
        self.open_client += other.open_client
        self.open_internal += other.open_internal
        self.closed_client += other.closed_client
        self.closed_internal += other.closed_internal
        self.unmapped += other.unmapped


def bifurcate(triples, *, multi=False):
    """Group (state, client_bucket, category) triples into Buckets.

    With `multi=True` the third element is a list and the ticket is counted once per
    category. Components are the multi-valued case: a ticket carrying two components
    appears in both rows, so the column sums exceed the ticket count by construction.
    The caller must state that beside the table.

    Returns `(rows, grand, distinct)`. `grand` counts each ticket exactly ONCE even when
    `multi=True`, so a multi-valued table's Total row still reconciles to the project
    count; `rows` is ordered by descending total then by category name.
    """
    buckets = collections.defaultdict(Bucket)
    grand = Bucket()
    distinct = 0
    for state, client, categories in triples:
        cats = categories if multi else [categories]
        for cat in cats:
            buckets[cat].add(state, client)
        grand.add(state, client)
        distinct += 1
    rows = sorted(buckets.items(), key=lambda kv: (-kv[1].total, str(kv[0])))
    return rows, grand, distinct


def prepare(records, status_fn, client_fn, category_fn):
    """Map ticket dicts onto the (state, bucket, categories) triples `bifurcate` wants."""
    return [(classify_status(status_fn(r)),
             client_bucket(client_fn(r)),
             category_fn(r))
            for r in records]


# ------------------------------------------------------------------- markdown emitters
# These live here rather than in `pamit_fmt` on purpose: `pamit_fmt` is shared with the
# `pamit_*` client-analysis line, which has diverged against the maintained copy on E:.
# Adding to it here would edit a file both copies own. Nothing below imports pamit_fmt.

def _md_row(cells) -> str:
    return "| " + " | ".join("" if c is None else str(c) for c in cells) + " |"


def grouped_table(label, rows, grand, *, total_label="**Total**", note_zero_rows=True):
    """Render a bifurcated table with the two-row grouped header.

    `rows` is the `(category, Bucket)` sequence from `bifurcate()`; `grand` is its
    grand-total Bucket. The first header row groups (Open, Closed) and the second names
    the leaves (Client, Internal, Total), which the .docx and .xlsx renderers turn into
    merged cells. Markdown has no colspan, so the grouping reads as blank cells beneath
    the group label — that is the shape the owner specified.

    The Total row is always emitted and always sums every numeric column.
    """
    group = [c.format(label=label) if "{label}" in c else c
             for c in BIFURCATED_GROUP_HEADER]
    align = ["---"] + ["---:"] * 8
    out = [_md_row(group), _md_row(align), _md_row(BIFURCATED_LEAF_HEADER)]
    for category, bucket in rows:
        if note_zero_rows or bucket.total:
            out.append(_md_row([category] + bucket.cells()))
    out.append(_md_row([total_label] + [f"**{v}**" for v in grand.cells()]))
    return "\n".join(out)


def simple_open_closed_table(label, rows, grand, *, total_label="**Total**"):
    """Render the compact `Category | Total Count | Open | Closed | Unmapped` table.

    This is section 6A for components — the plain distribution — with 6B carrying the
    full Client/Internal bifurcation.
    """
    out = [_md_row([label, "Total Count", "Open", "Closed", "Unmapped"]),
           _md_row(["---", "---:", "---:", "---:", "---:"])]
    for category, bucket in rows:
        out.append(_md_row([category, bucket.total, bucket.open_total,
                            bucket.closed_total, bucket.unmapped]))
    out.append(_md_row([total_label, f"**{grand.total}**", f"**{grand.open_total}**",
                        f"**{grand.closed_total}**", f"**{grand.unmapped}**"]))
    return "\n".join(out)


def unmapped_table(breakdown, *, label="Status"):
    """Render the standalone Unmapped Status table, with its own Total row."""
    out = [_md_row([label, "Client", "Internal", "Total"]),
           _md_row(["---", "---:", "---:", "---:"])]
    tc = ti = tt = 0
    for status, counts in breakdown:
        out.append(_md_row([status, counts["client"], counts["internal"], counts["total"]]))
        tc += counts["client"]
        ti += counts["internal"]
        tt += counts["total"]
    out.append(_md_row(["**Total**", f"**{tc}**", f"**{ti}**", f"**{tt}**"]))
    return "\n".join(out)


def unmapped_breakdown(records, status_fn, client_fn):
    """Per-status counts for every UNMAPPED ticket, ordered by descending total."""
    rows = collections.defaultdict(lambda: {"client": 0, "internal": 0, "total": 0})
    for r in records:
        status = status_fn(r)
        if classify_status(status) != UNMAPPED:
            continue
        entry = rows[str(status)]
        entry["total"] += 1
        if client_bucket(client_fn(r)) == CLIENT:
            entry["client"] += 1
        else:
            entry["internal"] += 1
    return sorted(rows.items(), key=lambda kv: (-kv[1]["total"], kv[0]))
