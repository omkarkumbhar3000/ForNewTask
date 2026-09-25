#!/usr/bin/env python3
"""Read-only Jira query layer — search, paging, and field normalisation.

`jira_client.Jira` can create, update and attach. This module wraps it in a
guard that **cannot** do any of those things, so an analysis script can state
"read-only" as a structural property rather than a promise.

    from jira_query import ReadOnlyJira
    j = ReadOnlyJira()
    for issue in j.search('project = PAMIT AND fixVersion = "35.8.29 HF12"'):
        ...

⛔ Why the guard is a whitelist and not a blacklist. `POST` is genuinely needed
for search (`/search/approximate-count`), so "block POST" is not an option and
"block the write paths" would need every write path enumerated correctly for
ever. Instead `_check()` permits exactly three request shapes and refuses
everything else, so a future edit that reaches for `/issue/{key}` with PUT fails
at the guard rather than at Jira.

⚠️ **`/search/approximate-count` is approximate and was measured wrong here.**
It reported 190 issues for a query that enumerates to 201 — an 11-issue (5.5%)
undercount. Use it for a cheap order-of-magnitude check only; every figure that
reaches a report must come from `search()`, which enumerates.

Three API facts this module exists to absorb, each of which cost a wrong result:

  * `GET /rest/api/3/search` is **gone** — HTTP 410 with a migration notice.
    Only `/rest/api/3/search/jql` remains, and it pages by opaque
    `nextPageToken`, not by `startAt`. There is no `total` in the response.
  * `description` and `environment` come back as **ADF documents** (nested
    `{type, content[]}`), not strings. Reading `.get("value")` on one yields
    `None`, which silently looks like an empty field. `adf_text()` flattens them.
  * A select custom field is `{"value": ...}` but a version/component/user is
    `{"name": ...}` / `{"displayName": ...}`. `field_value()` handles all three;
    guessing one of them wrongly reports a populated field as empty.
"""
from __future__ import annotations

import sys
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from jira_client import Jira, load_env  # noqa: E402

# --------------------------------------------------------------------------- guard

#: Exact paths that may be POSTed to. Both are search endpoints: they read.
_POST_ALLOWED = {
    "/rest/api/3/search/jql",
    "/rest/api/3/search/approximate-count",
}

#: GET path prefixes this layer needs. Anything else is refused, so a typo
#: cannot quietly walk into an endpoint with side effects.
_GET_ALLOWED = (
    "/rest/api/3/search/jql",
    "/rest/api/3/field",
    "/rest/api/3/project",
    "/rest/api/3/myself",
    "/rest/api/3/status",
)

#: Sub-resources permitted under `/rest/api/3/issue/{key}/`. The bare issue path
#: is always allowed. `transitions` is deliberately **not** here: reading it is
#: harmless, but it is the entry point to a workflow write, and narrowest
#: capability is worth more than a convenience this analysis does not need.
_ISSUE_SUBRESOURCES = {"comment", "changelog"}


class ReadOnlyViolation(RuntimeError):
    """Raised when a caller attempts a request this layer will not make."""


class ReadOnlyJira:
    """A Jira handle that can only read.

    Every request funnels through `_check()`. There is deliberately no `put`,
    `post_issue`, `transition` or `attach` method to reach for.
    """

    def __init__(self, cfg: dict | None = None):
        self._cfg = cfg or load_env()
        self._j = Jira(self._cfg)
        self.project = self._cfg["JIRA_PROJECT_KEY"]
        self.base = self._cfg["JIRA_BASE_URL"]
        self.calls = 0

    # ------------------------------------------------------------------ internals
    @staticmethod
    def _check(method: str, path: str) -> None:
        if method == "GET":
            bare = path.split("?")[0]
            if bare.startswith("/rest/api/3/issue/"):
                # /issue/{key} -> [] ; /issue/{key}/comment -> ["comment"]
                tail = bare[len("/rest/api/3/issue/"):].strip("/").split("/")[1:]
                if not tail or tail[0] in _ISSUE_SUBRESOURCES:
                    return
                raise ReadOnlyViolation(
                    f"issue sub-resource not permitted: /{'/'.join(tail)} — "
                    f"allowed: {sorted(_ISSUE_SUBRESOURCES) or 'none'}")
            if not bare.startswith(_GET_ALLOWED):
                raise ReadOnlyViolation(f"GET not permitted by this layer: {path}")
            return
        if method == "POST":
            if path.split("?")[0] not in _POST_ALLOWED:
                raise ReadOnlyViolation(f"POST permitted only to search endpoints: {path}")
            return
        raise ReadOnlyViolation(f"{method} is never permitted — this layer is read-only")

    def _get(self, path: str) -> tuple[int, dict]:
        """Object-returning GET. Use `_get_list` for endpoints that return an array."""
        self._check("GET", path)
        self.calls += 1
        st, body = self._j.get(path)
        return st, body if isinstance(body, dict) else {}

    def _get_list(self, path: str) -> tuple[int, list]:
        """Array-returning GET — `/project/{k}/versions` and `/field` are lists.

        ⚠️ Kept separate because coercing a list body to `{}` in `_get` silently
        returned "no versions" for a project with 122 of them: the call reported
        HTTP 200 and an empty result, which reads exactly like a project with no
        releases. Endpoints that return arrays must go through here.
        """
        self._check("GET", path)
        self.calls += 1
        st, body = self._j.get(path)
        return st, body if isinstance(body, list) else []

    def _post(self, path: str, body: dict) -> tuple[int, dict]:
        self._check("POST", path)
        self.calls += 1
        st, out = self._j.post(path, body)
        return st, out if isinstance(out, dict) else {}

    # ---------------------------------------------------------------------- public
    def whoami(self) -> str:
        st, r = self._get("/rest/api/3/myself")
        if st != 200:
            raise SystemExit(f"Jira auth failed: HTTP {st} — check tools/jira/.env")
        return (r or {}).get("displayName", "?")

    def versions(self, prefix: str = "") -> list[dict]:
        """Project versions, optionally filtered by name prefix.

        Each carries `name`, `releaseDate`, `released`, `archived`. ⚠️ Treat
        `releaseDate` as a *planned* date, not the date clients received the
        build: in this project `35.8.29 HF13` records 2026-06-22, earlier than
        HF12's 2026-07-31, and neither is flagged released.
        """
        st, vs = self._get_list(f"/rest/api/3/project/{self.project}/versions")
        if st != 200:
            raise SystemExit(f"versions failed: HTTP {st}")
        return [v for v in vs if (v.get("name") or "").startswith(prefix)]

    def approximate_count(self, jql: str) -> int:
        """Cheap, and genuinely approximate — never quote this in a report."""
        st, r = self._post("/rest/api/3/search/approximate-count", {"jql": jql})
        if st != 200:
            raise SystemExit(f"approximate-count failed: HTTP {st} {str(r)[:200]}")
        return (r or {}).get("count", -1)

    def search(self, jql: str, fields: list[str], page_size: int = 100,
               max_pages: int = 60, progress=None) -> list[dict]:
        """Enumerate every issue matching `jql`. This is the authoritative count.

        Pages by `nextPageToken` until `isLast`. `max_pages` is a runaway stop,
        not a result cap — if it is ever hit the caller is told loudly, because a
        silently truncated population is the one failure mode that would make
        every downstream percentage wrong.
        """
        out: list[dict] = []
        token, pages = None, 0
        fq = urllib.parse.quote(",".join(fields))
        while True:
            path = (f"/rest/api/3/search/jql?maxResults={page_size}"
                    f"&fields={fq}&jql={urllib.parse.quote(jql)}")
            if token:
                path += "&nextPageToken=" + urllib.parse.quote(token)
            st, r = self._get(path)
            if st != 200:
                raise SystemExit(f"search failed: HTTP {st} {str(r)[:300]}\n  jql: {jql}")
            batch = r.get("issues") or []
            out.extend(batch)
            pages += 1
            if progress:
                progress(pages, len(batch), len(out))
            if r.get("isLast") or not r.get("nextPageToken"):
                break
            if pages >= max_pages:
                raise SystemExit(
                    f"search hit the {max_pages}-page stop with {len(out)} issues and "
                    f"more remaining — refusing to return a truncated population")
            token = r["nextPageToken"]
        return out

    def issue(self, key: str, fields: list[str]) -> dict:
        st, r = self._get(f"/rest/api/3/issue/{key}?fields={urllib.parse.quote(','.join(fields))}")
        return r if st == 200 else {}


# ----------------------------------------------------------------- normalisation

def adf_text(node) -> str:
    """Flatten an Atlassian Document Format value to plain text.

    Jira returns `description` and `environment` as ADF. Reading `.get("value")`
    on one silently yields None, which is indistinguishable from an empty field —
    it made `description` look 0% populated across 201 issues until measured
    against a direct issue GET.
    """
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if isinstance(node, list):
        return " ".join(adf_text(x) for x in node)
    if isinstance(node, dict):
        text = node.get("text", "")
        inner = adf_text(node.get("content"))
        # A hard break or paragraph boundary should not glue two words together.
        sep = " " if node.get("type") in ("paragraph", "heading", "listItem",
                                          "tableRow", "hardBreak", "rule") else ""
        return f"{text}{sep}{inner}".strip()
    return ""


def field_value(fields: dict, key: str):
    """Read one field without caring which of Jira's three shapes it uses.

    Returns a scalar for select/version/user shapes, a list for array shapes,
    and None when genuinely absent.
    """
    v = fields.get(key)
    if v is None:
        return None
    if isinstance(v, dict):
        return v.get("value") or v.get("name") or v.get("displayName") or v.get("key")
    if isinstance(v, list):
        vals = [
            (x.get("value") or x.get("name") or x.get("displayName") or x.get("key"))
            if isinstance(x, dict) else x
            for x in v
        ]
        return [x for x in vals if x] or None
    return v


def link_edges(fields: dict) -> list[tuple[str, str, str]]:
    """Return (link_type, direction, other_key) for every issue link."""
    out = []
    for link in fields.get("issuelinks") or []:
        t = (link.get("type") or {}).get("name", "?")
        if link.get("outwardIssue"):
            out.append((t, "outward", link["outwardIssue"]["key"]))
        elif link.get("inwardIssue"):
            out.append((t, "inward", link["inwardIssue"]["key"]))
    return out


def _selftest() -> int:
    """Assert the guard's exact contract. Makes zero network calls."""
    must_block = [
        ("PUT", "/rest/api/3/issue/PAMIT-1"),
        ("DELETE", "/rest/api/3/issue/PAMIT-1"),
        ("POST", "/rest/api/3/issue"),
        ("POST", "/rest/api/3/issue/PAMIT-1/comment"),
        ("POST", "/rest/api/3/issue/PAMIT-1/transitions"),
        ("GET", "/rest/api/3/issue/PAMIT-1/transitions"),
        ("GET", "/rest/api/3/issue/PAMIT-1/attachments"),
        ("GET", "/rest/api/3/user/bulk"),
        ("GET", "/rest/api/3/webhook"),
    ]
    must_allow = [
        ("GET", "/rest/api/3/myself"),
        ("GET", "/rest/api/3/search/jql?maxResults=100&jql=x"),
        ("GET", "/rest/api/3/issue/PAMIT-1?fields=summary"),
        ("GET", "/rest/api/3/issue/PAMIT-1/comment"),
        ("GET", "/rest/api/3/issue/PAMIT-1/changelog"),
        ("GET", "/rest/api/3/project/PAMIT/versions"),
        ("POST", "/rest/api/3/search/approximate-count"),
    ]
    fails = 0
    for m, p in must_block:
        try:
            ReadOnlyJira._check(m, p)
            print(f"  FAIL  should have blocked {m} {p}")
            fails += 1
        except ReadOnlyViolation:
            print(f"  ok    blocked  {m:<6} {p}")
    for m, p in must_allow:
        try:
            ReadOnlyJira._check(m, p)
            print(f"  ok    allowed  {m:<6} {p}")
        except ReadOnlyViolation as e:
            print(f"  FAIL  should have allowed {m} {p} -> {e}")
            fails += 1
    print(f"\n{len(must_block) + len(must_allow)} assertions, {fails} failure(s)")
    return fails


if __name__ == "__main__":
    rc = _selftest()
    if "--offline" not in sys.argv:
        j = ReadOnlyJira()
        print("\nconnected as:", j.whoami(), "| project:", j.project)
    sys.exit(1 if rc else 0)
