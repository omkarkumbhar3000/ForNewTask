#!/usr/bin/env python3
"""Shared counting and markdown-table helpers for the PAMIT client analysis.

A separate module purely to break a cycle: the engine needs `pct`/`tally` while
analysing, the report module needs them while rendering, and the engine imports
the report module to write its outputs. Putting them here keeps that import
one-directional.
"""
from __future__ import annotations

import collections
import hashlib


def pct(n: int, d: int) -> str:
    """Percentage as a string, or an em dash when the denominator is zero.

    Never returns "0.0%" for an empty base — a zero denominator means the
    question does not apply, which is different from a genuine zero.
    """
    return "—" if not d else f"{100.0 * n / d:.1f}%"


def delta(a: int, b: int) -> str:
    return f"{b - a:+d}"


def tally(items, key) -> collections.Counter:
    """Count `key(item)` across items; a list-valued key contributes each element."""
    c: collections.Counter = collections.Counter()
    for i in items:
        v = key(i)
        if isinstance(v, list):
            for x in v:
                c[x] += 1
        else:
            c[v] += 1
    return c


def row(cells) -> str:
    return "| " + " | ".join("" if c is None else str(c) for c in cells) + " |"


def table(headers, rows, align=None) -> str:
    """Render a markdown table. `align` supplies the separator cells.

    An empty `rows` yields a header plus an explicit "no rows" line rather than a
    bare header, so a reader can tell "nothing matched" from "section unfinished".
    """
    sep = align or ["---"] * len(headers)
    out = [row(headers), row(sep)]
    if not rows:
        out.append(row(["_none_"] + [""] * (len(headers) - 1)))
    else:
        out.extend(row(r) for r in rows)
    return "\n".join(out)


def snapshot_provenance(path) -> str:
    """One markdown line naming the exact source data a report was built from.

    A report that says only "generated at 18:37" cannot be traced: the same command on
    the same day can produce different numbers if the snapshot underneath it was
    re-fetched. Naming the file and hashing its bytes makes the link checkable — the
    validator recomputes this digest, so a report can no longer claim a source it was
    not actually built from.

    Truncated to 16 hex characters: enough to identify a file among a handful of
    snapshots, short enough to sit in a document header.
    """
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return f"**Source snapshot:** `{path.name}` · sha256 `{h.hexdigest()[:16]}`"
