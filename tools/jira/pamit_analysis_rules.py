#!/usr/bin/env python3
"""Classification and grouping rules for client-raised PAMIT ticket analysis.

Kept separate from `pamit_client_analysis.py` so the rules can be reviewed,
diffed and argued about without reading the orchestration around them — and so
the taxonomy is visibly *derived* rather than hidden in a pipeline.

⛔ **The taxonomy was read out of the data, not assumed.** Every category below
was added because tickets in the HF12/HF13 client population demanded it, and
every `terms` entry is a string that actually occurs in those summaries. When a
new pattern appears, add a category here rather than forcing it into
`uncategorised` — but add it because tickets exist, not because the category
sounds plausible.

⚠️ **Jira's own categorisation fields cannot be used.** Measured across the 201
HF12/HF13 issues: `Module` (cf 10065) 0% populated, `Category` (cf 10051) 0%,
`Sub-Category` (cf 10058) 0%, `Root Cause` (cf 10113 / 10199) 0%, `Product
categorization` 0%, `Operational categorization` 0%. `components` is 95%
populated and is the only usable module axis; everything else here is derived
from `summary` + `description` text.
"""
from __future__ import annotations

import re

# --------------------------------------------------------------------------- scope

FIX_VERSIONS = {"35.8.29 HF12": "HF12", "35.8.29 HF13": "HF13"}

#: Values of `Primary Client` (cf 10112) that mean "not a client".
#: The owner's JQL listed five; only the first three occur in HF12/HF13, but the
#: other two are retained so the definition survives a different scope.
INTERNAL_CLIENTS = {
    "Internal", "Internal (ARCON)", "Internal(ARCON)",
    "Internal (Bulwark)", "Wipro Internal",
}

#: `D38` — the defect denominator. Story/Task/Sub-task are client-raised work but
#: are not defects; counting them in a defect rate understates module quality.
DEFECT_TYPES = {"Bug", "Security Fix", "Client-Support", "Performance"}

#: Statuses that mean "this ticket is not a distinct finding".
#: `Duplicate` tickets are kept for recurrence evidence but excluded from the
#: defect denominator, because a duplicate is by definition the same defect
#: counted twice — leaving them in inflates every module percentage.
NON_DISTINCT_STATUSES = {"Duplicate", "Rejected", "RCA Rejection"}

# --------------------------------------------------------------- the build axis
#
# ⛔ THE BUILD AXIS IS `Affected Milestone`, NOT `Fix versions` — owner ruling `D42`.
#
# The two fields answer different questions and disagree completely:
#
#   Affected Milestone (cf 10092)  = the build the CLIENT WAS RUNNING when they hit it.
#                                    "Where was this found?"  -> testing weakness.
#   Fix versions       (native)    = the build the FIX SHIPS IN.
#                                    "Where was this fixed?"  -> release content.
#
# Measured on the client population across the 20 `35.8.29` versions:
#
#   by fixVersion          1,384 tickets   -> heaviest build `base` (262)
#   by Affected Milestone  2,010 tickets   -> heaviest builds HF6 (399), HF1 (388);
#                                             `base` is only 69
#   AM present, no fixVersion at all       1,369  (invisible to a fixVersion query)
#   fixVersion present, no AM                 38
#
# A hotfix accumulates fixes for defects found on *earlier* builds, so a
# fixVersion-keyed build line reports where fixes landed and reads it as where
# quality was weak. That inverts the conclusion: HF12/HF13/HF14 carry 3/2/1
# Affected-Milestone tickets between them — almost nothing has been *reported
# against* the newest builds — while a fixVersion view credits them with 55/27.
#
#: `Affected Milestone.` — note the trailing period in the Jira field name.
#: ⚠️ THREE fields in this instance are named "Affected Milestone"-something.
#: Only this one is on the PAMIT screen; the other two are 0% populated and
#: picking one of them yields an empty build line that looks like a clean result:
#:     customfield_10214  "Affected Milestone"    0 / 1384
#:     customfield_10219  "Affected Milestone"    0 / 1384
#:     customfield_10092  "Affected Milestone."   1346 / 1384   <- this one
#: The native `versions` ("Affects versions") is also 0% and must not be used;
#: concluding from it that "no field records the build a client was on" is the
#: error that produced the fixVersion methodology in the first place.
AFFECTED_MILESTONE = "customfield_10092"

#: Every other milestone-shaped field in this instance, measured and rejected.
#: Kept as a registry so the next reader does not have to re-measure them.
MILESTONE_FIELDS_REJECTED = {
    "customfield_10214": ("Affected Milestone", "0% on PAMIT — not on the screen"),
    "customfield_10219": ("Affected Milestone", "0% on PAMIT — not on the screen"),
    "customfield_10143": ("Custom Affected Milestone", "0% — free-text escape hatch"),
    "customfield_10174": ("Custom Affected Milestone", "0% — free-text escape hatch"),
    "versions":          ("Affects versions (native)", "0% project-wide"),
    "customfield_10131": ("Release Milestone", "0%"),
    "customfield_10100": ("Release Milestone.", "9% and legacy — values are "
                                               "unrelated old lines (35.8.13 HF 7, "
                                               "4.8.5.0_U16SP2_B35.8.21), all singletons"),
    "customfield_10221": ("PAM_Release Milestone", "0%"),
    "customfield_10223": ("CI_Release_Milestone", "0%"),
    "customfield_10238": ("Forward Merge Milestone", "63% populated but 344 of 388 "
                                                     "values are the literal string "
                                                     "'None' — no usable signal"),
}

#: ⚠️ A select field can be *populated with the string* `None`. That is a real
#: option value meaning "there is no previous working version", and it is NOT the
#: same as an empty field. Counting it as populated overstates coverage; counting
#: it as a version corrupts every regression comparison. `Previous working
#: version` carries 130 of these on the build line.
NULL_SENTINELS = {"None", "none", "N/A", "NA", "-", "TBD", "Not Applicable"}

FIELDS = [
    "key", "summary", "issuetype", "status", "priority", "created", "updated",
    "components", "fixVersions", "labels", "reporter", "assignee", "parent",
    "issuelinks", "description", "resolution",
    AFFECTED_MILESTONE,    # Affected Milestone.   ( 97% — THE BUILD AXIS, `D42`)
    "customfield_10112",   # Primary Client        (100% populated)
    "customfield_10190",   # Severity              ( 11%)
    "customfield_10780",   # Is reopen from customer (25% of the AM population)
    "customfield_11253",   # Functionality working in previous version (25%)
    "customfield_11254",   # Previous working version                  (24%)
    "customfield_11220",   # Hosting Environment   ( 62%)
    # --- every remaining populated regression/RCA field (`REGRESSION_AUDIT`)
    "customfield_10245",   # RCA                                  ( 81% — the axis)
    "customfield_10567",   # RCA Details (Impact Analysis)        ( 79%)
    "customfield_10249",   # Fixed Date                           ( 51%)
    "customfield_10741",   # Reopen RCA                           (7.3%)
    "customfield_10600",   # Reopen RCA details                   (7.6%)
    "customfield_10781",   # Reopen Original Ticket ID            (7.1%, junk-prone)
    "customfield_10236",   # ReOpen Date                          (4.1%)
    "customfield_10235",   # ReOpen Time Spent                    (3.6%)
    "customfield_11353",   # RCA Category / Description updated?  (1.2%)
    "customfield_11355",   # RCA Review Remarks                   (1.2%)
    "customfield_10142",   # Secondary Clients
    "customfield_10065",   # Module                (  0% — measured, kept to detect it filling)
    "customfield_10051",   # Category              (  0%)
    "customfield_10113",   # Root Cause            (  0%)
]

FIELD_NAMES = {
    AFFECTED_MILESTONE: "affected_milestone",
    "customfield_10112": "primary_client",
    "customfield_10190": "severity",
    "customfield_10780": "reopen_from_customer",
    "customfield_11253": "func_working_prev",
    "customfield_11254": "prev_working_version",
    "customfield_11220": "hosting_env",
    "customfield_10245": "rca",
    "customfield_10567": "rca_details",
    "customfield_10249": "fixed_date",
    "customfield_10741": "reopen_rca",
    "customfield_10600": "reopen_rca_details",
    "customfield_10781": "reopen_original_id",
    "customfield_10236": "reopen_date",
    "customfield_10235": "reopen_time_spent",
    "customfield_11353": "rca_reviewed",
    "customfield_11355": "rca_review_remarks",
    "customfield_10142": "secondary_clients",
    "customfield_10065": "module_field",
    "customfield_10051": "category_field",
    "customfield_10113": "root_cause",
}

#: The three regression-signal fields the owner asked to be brought in.
#: All three exist and all three are select (single-value) fields. `10780` was
#: already captured but never used in an analysis; `11253`/`11254` are new here.
#: Their IDs place them as recent additions — `10780` is far older than the pair.
REGRESSION_FIELDS = {
    "customfield_10780": "Is reopen from customer",
    "customfield_11253": "Functionality working in previous version",
    "customfield_11254": "Previous working version",
}

# ------------------------------------------------------------- client normalisation

#: `Primary Client` is free-form enough that one client appears under several
#: values. Left unmerged, "most affected client" is wrong: ICICI's 25 tickets
#: split into 21 + 4 and it loses first place to nothing.
#: Key is a lowercased substring test; value is the canonical name.
CLIENT_ALIASES = [
    ("icici", "ICICI Bank"),
    ("tcl global", "TCL Global"),
    ("itd-mc", "ITD-MC"),
    ("bank muscat", "Bank Muscat"),
    ("kotak", "Kotak Bank"),
    ("mashreq", "MashreqBank"),
]

#: Tokens that are client identity, not defect content. Stripped before
#: similarity scoring so "ICICI || login fails" and "Kotak || login fails"
#: are recognised as the same pattern rather than two unrelated strings.
CLIENT_NOISE = {
    "icici", "bank", "muscat", "kotak", "mashreq", "idfc", "canara", "gail",
    "bobcard", "iibx", "iifl", "iftas", "gfl", "pss", "sbi", "cards", "tcs",
    "csp", "tcl", "global", "international", "boi", "bm", "rhc", "ocl", "paytm",
    "xtelify", "airtel", "torrent", "power", "passport", "seva", "suryoday",
    "landmark", "dubai", "edelweiss", "diligenta", "sloc", "piramal", "finance",
    "catholic", "syrian", "renew", "avrioc", "ltd", "limited", "new", "onprem",
    "upgrade", "royal", "hashemite", "court", "jordan", "tata", "fyers",
    "securities", "cyber", "security", "punjab", "national", "obc", "iibx",
    "india", "state", "cwa", "tushar", "kiran",
}

#: Release/build noise. "CLONE 35.8.29 HF12 - ..." carries no defect content in
#: its prefix, but the build token *inside* a title often records where the
#: client found the issue — that is extracted first, by BUILD_RE, then removed.
STRUCTURAL_NOISE = {
    "clone", "u16", "u16sp2", "sp2", "hf", "b", "ver", "version", "issue",
    "issues", "getting", "unable", "not", "and", "the", "for", "with", "from",
    "when", "while", "after", "due", "please", "need", "into", "this", "that",
    "are", "was", "were", "has", "have", "been", "its", "via", "per", "all",
    "any", "can", "cannot", "does", "did", "will", "would", "should", "may",
    "one", "two", "get", "got", "set", "use", "used", "using", "also", "then",
    "than", "there", "their", "which", "what", "where", "who", "how", "why",
}

BUILD_RE = re.compile(
    r"\b(?:B\.?)?(?P<base>\d{2}\.\d{1,2}\.\d{1,2})?[\s_.]*(?:HF|hf)[\s_.]*(?P<hf>\d{1,2})\b"
    r"|\b(?P<bare>\d{2}\.\d{1,2}\.\d{1,2})\b"
)

# ------------------------------------------------------------------- the taxonomy

#: Ordered most-specific first. A ticket takes the first category it matches as
#: its primary, and keeps every match as a tag — a ticket genuinely can be both
#: a validation defect and a security finding, and forcing a single label would
#: lose exactly the cross-cutting signal this analysis is for.
CATEGORIES: list[tuple[str, tuple[str, ...]]] = [
    ("Security Hardening & Exposure", (
        "vulnerab*", "cipher", "weak cipher", "exposure", "exposed",
        "directly accessible", "non-html", "cve", "hardening", "penetration",
        "password exposure", "sensitive data", "encryption", "tls", "ssl",
        "request smuggling", "clickjack", "xss", "injection",
    )),
    ("Session Recording & Audit Evidence", (
        "video", "delta image", "delta video", "videorecord", "recording",
        "banner", "siem", "audit log", "session monitoring", "logs data mismatch",
        "log mismatch", "session log", "screen capture",
    )),
    ("Third-Party Tool & Platform Compatibility", (
        "dbeaver", "winscp", "ssms", "putty", "toad", "sql developer",
        "chrome driver", "chromedriver", "mac", "macos", "rdp",
        "windows patching", "browser", "mysql", "oracle client", "tj5100",
        "ems sso", "always_prompt_password", "web browser",
    )),
    ("Password & Credential Lifecycle", (
        "password rotation", "password change", "password closure",
        "password update", "password vault", "vault", "vpc", "hsm", "thales",
        "credential", "rotate", "checkin", "check-in", "checkout",
    )),
    ("Authentication & Identity Integration", (
        "saml", "azure ad", "sso", "ldap", "ad bridging", "jit", "mfa", "otp",
        "radius", "2fa", "single sign", "provisioning", "kerberos",
    )),
    ("Access Control, Workflow & Approval", (
        "workflow", "approve", "approval", "delegation", "my access",
        "entitlement", "privilege", "one time", "time based", "time-based",
        "restricted command", "command profiler", "access control",
        "authoris*", "authoriz*", "permission", "role",
    )),
    ("Service & Asset Management (CRUD/Bulk)", (
        "modify service", "create service", "service parameter",
        "service details", "bulk update", "bulk import", "tag validation",
        "duplicate service", "cannot perform the operation", "user discovery",
        "server group", "onboard", "auto-download", "preference",
        "child services", "rotate tab", "disabled service", "server count",
    )),
    ("Session Lifecycle & Connectivity", (
        "logged out", "logout", "log out", "autologout", "auto logout",
        "disconnect", "session extension", "session expire", "idle",
        "connection issue", "not accessible", "unable to access",
        "fails to launch", "session disconnection", "not working",
        "autoscaling",
    )),
    ("Reporting & Scheduling", (
        "report", "schedule", "envelope", "dashboard", "export", "download",
        "idle users report",
    )),
    ("Input Validation & Error Handling", (
        "special character", "input validation", "server side input",
        "script detected", "large values", "outofmemory", "out of memory",
        "string reference not set", "object reference", "exception",
        "invalid", "validation", "error while", "unable to fetch",
        "unable to update", "unable to add", "unable to edit", "unable to view",
        "unable to modify", "unable to create", "unable to schedule",
    )),
    ("Platform Services, Agent & Gateway", (
        "ipcservice", "ipc service", "arcon service", "agent", "web gateway",
        "webgateway", "gateway", "uag", "agw", "pycli", "windows service",
        "app pool", "service not triggering",
    )),
    ("API & Integration", (
        "api", "integration", "rest", "endpoint", "swagger", "ms api",
    )),
    # ---------------------------------------------------------------- OBJ-028
    # Appended, deliberately, *after* the original set. CATEGORIES is first-match,
    # so appending can only resolve tickets that previously fell through to
    # `Uncategorised` — it cannot silently re-label anything already classified.
    #
    # Why these exist: the original taxonomy was derived from 82 HF12/HF13
    # tickets and left **33.3% of the 1,377-ticket build line** uncategorised.
    # Sampling that bucket showed five recurring subjects it had no home for, all
    # of them real: slowness complaints, client VA/VAPT assessment findings,
    # requests for a new connector, LOB/organisation mapping, and outright
    # enhancement requests. Each term below is lifted from an actual title.
    ("Performance & Responsiveness", (
        "slowness", "slow", "hang", "hangs", "freeze", "screen freeze", "latency",
        "timeout", "time out", "not responding", "taking time", "degrad*",
        "outofmemory", "out of memory", "performance",
    )),
    ("Vulnerability Assessment (VA / VAPT)", (
        "vapt", "va point", "va report", "vulnerability assessment", "va",
        "penetration test", "pen test", "security audit",
    )),
    ("Connector Development & New Integration", (
        "connector development", "new connector", "connector request",
        "plugin development", "connector for", "develop connector",
    )),
    ("LOB / Organisation Mapping", (
        "lob mapping", "lob wise", "lob", "group admin", "map service",
        "organisation mapping", "organization mapping", "user mapping",
    )),
    ("Log Viewing & Audit Reports", (
        "service log", "activity log", "password status log", "user activity",
        "log column", "view log", "capture log", "service logs",
    )),
    ("UI Field & Control Defects", (
        "not visible", "not available", "not showing", "unable to select",
        "dropdown", "drop down", "checkbox", "status bar", "column required",
        "field should", "greyed out", "disabled button",
    )),
    ("Enhancement / Change Request", (
        "enhancement", "change in", "feature request", "provision to",
        "option to", "need help", "required in", "should be entered",
        "new requirement", "customisation", "customization",
    )),
]

#: Environment / configuration markers. These do not form a category — they are a
#: cross-cutting flag, because "config-specific" is a property of a defect in any
#: category and is one of the classifications the owner asked for.
ENV_CONFIG_TERMS = (
    "configuration", "config", "setting", "preference", "parameter",
    "environment", "on-prem", "onprem", "cloud", "patching", "upgrade",
    "migration", "deployment", "install", "post upgrade", "after upgrade",
)


def normalise_client(name: str | None) -> str:
    if not name:
        return "«unset»"
    low = name.lower()
    for needle, canon in CLIENT_ALIASES:
        if needle in low:
            return canon
    return name.strip()


def extract_builds(text: str) -> list[str]:
    """Return build tokens found in a title, e.g. ['35.8.29 HF6', '35.8.24 HF11'].

    Client titles routinely record the build where the issue was *found*
    ("DILIGENTA SLOC | 29HF6 | PASSWORD ROTATION..."), while `fixVersion` records
    where it is being *fixed*. The gap between the two is escape latency, and it
    is the only place in this data where that is recoverable.
    """
    out = []
    for m in BUILD_RE.finditer(text):
        base, hf, bare = m.group("base"), m.group("hf"), m.group("bare")
        if hf:
            out.append(f"{base or '35.8.29'} HF{int(hf)}")
        elif bare:
            out.append(bare)
    seen, uniq = set(), []
    for b in out:
        if b not in seen:
            seen.add(b)
            uniq.append(b)
    return uniq


def clean_title(summary: str) -> str:
    """Strip clone prefixes, client names and build tokens from a summary."""
    s = summary
    s = re.sub(r"^\s*(?:CLONE\b[\s\-–—:]*)+", "", s, flags=re.I)
    s = re.sub(r"^\s*(?:\d{2}\.\d{1,2}\.\d{1,2}\s*)?(?:HF\s*\d{1,2})?\s*[-–—:|]+\s*", "", s, flags=re.I)
    s = BUILD_RE.sub(" ", s)
    s = re.sub(r"\|{1,2}", " ", s)
    s = re.sub(r"\b0{2,}\d+\b", " ", s)          # ticket refs like 00196943
    return re.sub(r"\s+", " ", s).strip(" -–—:|")


_WORD = re.compile(r"[a-z][a-z0-9_.]{2,}")


def signature(text: str) -> set[str]:
    """Content tokens of a title, with client and structural noise removed."""
    toks = _WORD.findall(text.lower())
    return {t for t in toks
            if t not in CLIENT_NOISE and t not in STRUCTURAL_NOISE and len(t) > 2}


_MATCHERS: dict[int, "re.Pattern[str]"] = {}


def _matcher(terms: tuple[str, ...]) -> "re.Pattern[str]":
    """Compile a term list into a word-boundary matcher.

    ⚠️ **Plain substring matching is wrong here and produced a real
    misclassification.** `"log"` is a substring of `"Login"`, so
    "Login with SAML for Azure AD" was tagged *Logging / Monitoring*. Every term
    is therefore anchored at a word boundary. A term ending in `*` is an
    intentional stem (`vulnerab*` catches vulnerable/vulnerability) and is
    anchored only at the front.
    """
    key = id(terms)
    m = _MATCHERS.get(key)
    if m is None:
        # `s?` before the boundary admits a regular plural without reopening the
        # substring hole: `logs?\b` matches "log"/"logs" but never "login",
        # whereas a bare `cipher\b` missed "ciphers" and dropped two real tickets.
        parts = [re.escape(t[:-1]) if t.endswith("*") else re.escape(t) + r"s?\b"
                 for t in terms]
        m = _MATCHERS[key] = re.compile(r"\b(?:" + "|".join(parts) + r")", re.I)
    return m


def categorise(text: str) -> tuple[str, list[str]]:
    """Return (primary_category, all_matching_categories)."""
    hits = [name for name, terms in CATEGORIES if _matcher(terms).search(text)]
    return (hits[0] if hits else "Uncategorised"), hits


def is_env_config(text: str) -> bool:
    low = text.lower()
    return any(t in low for t in ENV_CONFIG_TERMS)


# ============================================================ OBJ-028 extensions
# Build scope, release-date handling, and the testing-area axis.

#: The build clients are currently on. **Owner-stated, not derived.** It cannot be
#: derived: `releaseDate` is non-monotonic against build number in this project
#: (HF13 2026-06-22 < HF14 2026-07-10 < HF11 2026-07-15 < HF12 2026-07-31) and
#: none of HF12/13/14/15 is flagged `released`.
CURRENT_BUILD = "35.8.29 HF13"
PREVIOUS_BUILD = "35.8.29 HF12"
BUILD_PREFIX = "35.8.29"

#: Focus builds for deep analysis: the current line plus what is in flight around
#: it. HF15 is retained even though it currently holds 0 client tickets — showing
#: an empty release is information, and dropping it would hide the fact.
FOCUS_BUILDS = [
    "35.8.29 HF12", "35.8.29 HF13", "35.8.29 HF14", "35.8.29 HF15",
    "35.8.29 HF11 P2", "35.8.29 HF11 P3", "35.8.29 HF9 P2",
]

CURRENT_WINDOW_DAYS = 30

#: Which objective this report is produced under. ⚠️ Stated in ONE place because
#: it was found stale: the header still read `OBJ-028` after `OBJ-029` replaced
#: the build-wise methodology, so the report cited the objective whose
#: methodology it had just superseded.
OBJECTIVE = "OBJ-029"

#: The engine's provenance, kept distinct from the active objective. `OBJ-028`
#: built the read-only Jira layer, the population rules (`D38`–`D41`) and the
#: taxonomy, all of which `OBJ-029` retains — so crediting only the current
#: objective would misattribute the work.
OBJECTIVE_LINEAGE = "engine, population rules D38-D41 and taxonomy from OBJ-028"


# ------------------------------------------------- milestone + regression helpers

HF_NUM = re.compile(r"HF\s*(\d+)", re.I)


def clean_value(v):
    """A field value with Jira's null-ish option strings removed.

    ⚠️ `Previous working version` is a *select* field whose option list includes
    the literal `None`. `field_value()` returns that as the string "None", which
    is truthy, so a plain emptiness test reports the field populated and a
    version comparison then tries to order "None" against "35.8.29 HF6".
    Returns `None` for absent-or-sentinel, so callers get one shape.
    """
    if v is None:
        return None
    if isinstance(v, list):
        out = [x for x in (clean_value(x) for x in v) if x is not None]
        return out or None
    t = str(v).strip()
    return None if not t or t in NULL_SENTINELS else t


def as_list(v) -> list[str]:
    """Any field value as a list of clean strings — multiselect or single."""
    c = clean_value(v)
    if c is None:
        return []
    return [str(x) for x in c] if isinstance(c, list) else [str(c)]


def hf_number(name: str) -> int | None:
    """Hotfix ordinal within a build line; the base release sorts as 0.

    Ordering is by this number, never by `releaseDate` — see `RELEASE_DATE_CAVEAT`.
    """
    if not name:
        return None
    if (m := HF_NUM.search(name)):
        return int(m.group(1))
    return 0 if name.strip() == BUILD_PREFIX else None


def milestone_builds(v) -> tuple[list[str], list[str]]:
    """Split an Affected Milestone value into (in-family, other-line) build names.

    49 tickets carry two Affected Milestone values, 6 carry three or more, and 41
    carry a value from a different build line alongside an in-family one — so this
    returns lists, and a caller that needs one build per ticket must say which
    (`earliest_build` does: the earliest, because that is where the defect first
    reached a client).
    """
    infam, other = [], []
    for name in as_list(v):
        (infam if name.startswith(BUILD_PREFIX) else other).append(name)
    return sorted(infam, key=lambda n: (hf_number(n) is None, hf_number(n) or 0)), other


def earliest_build(v) -> str | None:
    """The earliest in-family Affected Milestone — the ticket's build attribution.

    ⛔ Earliest, not latest. A ticket reported against both HF5 and HF9 escaped
    from HF5; attributing it to HF9 would credit the later build with a defect it
    inherited and understate how long the defect survived undetected.
    """
    infam, _ = milestone_builds(v)
    return infam[0] if infam else None


#: How a ticket's regression signal reads, from the three owner-named fields.
#: ⛔ These are *gates*, not denominators — see `REGRESSION_CONFIDENCE`.
REGRESSION_CLASSES = {
    "confirmed-regression": "Worked in a previous version and that version is named",
    "likely-regression":    "Worked in a previous version; the version is not named",
    "not-a-regression":     "Did not work in the previous version — pre-existing or new feature gap",
    "customer-reopen":      "Reopened by the customer, regression status not stated",
    "unstated":             "None of the three fields is populated",
}


def regression_class(func_prev, prev_ver, reopen) -> str:
    """Classify one ticket's regression signal. Order matters: most specific first."""
    fp, pv, ro = clean_value(func_prev), clean_value(prev_ver), clean_value(reopen)
    yes = isinstance(fp, str) and fp.strip().lower() in {"yes", "y", "true"}
    no = isinstance(fp, str) and fp.strip().lower() in {"no", "n", "false"}
    if yes and pv:
        return "confirmed-regression"
    if yes:
        return "likely-regression"
    if no:
        return "not-a-regression"
    if isinstance(ro, str) and ro.strip().lower() in {"yes", "y", "true"}:
        return "customer-reopen"
    return "unstated"


#: ⛔ The population bound that must travel with every regression figure.
#: Measured on the 2,010-ticket Affected-Milestone build line:
#:   Functionality working in previous version   499 / 2010  (24.8%)
#:   Previous working version                    491 / 2010  (24.4%)  — 130 of them "None"
#:   Is reopen from customer                     512 / 2010  (25.5%)
#: So ~75% of tickets are `unstated`. A regression *rate* over the whole
#: population would be wrong by construction; the rate is quoted over the
#: populated subset and the subset size is always shown beside it.
REGRESSION_CONFIDENCE = (
    "The three regression fields are populated on ~25% of the build line, so "
    "every regression figure is quoted over the **populated subset** with that "
    "subset's size beside it, never over the full population. An `unstated` "
    "ticket is not evidence of 'no regression' — it is evidence of an unfilled "
    "field, and the two must never be merged."
)


#: The release-date rule, stated once and quoted into the report.
RELEASE_DATE_CAVEAT = (
    "Jira `releaseDate` is a planned date, not confirmed client availability. In "
    "this project it is non-monotonic against build number and none of the "
    "in-flight builds is flagged released, so ordering and grouping use the "
    "build/fix version, never the date."
)

# --------------------------------------------------------------- testing areas

#: A second, independent axis over the same tickets. Issue category answers what
#: broke; a testing area answers which kind of testing would have caught it. A
#: ticket belongs to as many areas as it matches — a bulk-import failure on
#: oversized values is simultaneously Boundary and Negative testing, and
#: collapsing that to a single label is what hides a gap.
TESTING_AREAS: list[tuple[str, tuple[str, ...]]] = [
    ("Third-Party Compatibility", (
        "dbeaver", "winscp", "ssms", "putty", "toad", "sql developer", "mysql",
        "oracle client", "chrome driver", "chromedriver", "tj5100", "thales",
        "hsm", "third party", "third-party", "ems sso", "sap", "vmware",
    )),
    ("Session Recording", (
        "video", "delta image", "delta video", "videorecord", "recording",
        "banner", "session monitoring", "screen capture", "playback",
    )),
    ("Authentication / Authorization", (
        "saml", "sso", "azure ad", "ldap", "jit", "mfa", "otp", "radius",
        "kerberos", "privilege", "permission", "role", "entitlement",
        "delegation", "my access", "unauthorized", "unauthoris*", "access denied",
        "login", "logon", "single sign", "provisioning",
    )),
    ("API / Integration", (
        "api", "rest", "endpoint", "integration", "ms api", "webservice",
        "web service", "soap", "payload", "connector api", "siem",
    )),
    # "parameter", "profile" and "policy" dropped — all three are ordinary PAM
    # domain nouns and pulled in 132 tickets regardless of whether configuration
    # was the subject.
    ("Configuration", (
        "configuration", "config", "setting", "preference", "command profiler",
        "gateway server", "gateway configuration", "misconfigur", "config file",
    )),
    ("Upgrade / Migration", (
        "upgrade", "migration", "migrat*", "post upgrade", "after upgrade",
        "patching", "patched", "hotfix",
    )),
    # ⚠️ Bare "log" is deliberately absent. With it, this area matched 133 tickets
    # — "logs" appears in half the PAM corpus — and the weak-spot ranking measured
    # term breadth instead of signal. Every term here names a *logging artefact*.
    ("Logging / Monitoring", (
        "audit log", "activity log", "error log", "session log", "event log",
        "log mismatch", "logs data mismatch", "logging", "monitoring", "siem",
        "log file", "log details", "log report", "trace",
    )),
    ("Performance", (
        "performance", "slow", "timeout", "time out", "hang", "latency",
        "outofmemory", "out of memory", "memory", "cpu", "degrad*",
        "response time", "not responding", "taking time",
    )),
    # "page", "screen" and "display" dropped — they name where almost any UI defect
    # occurs rather than a browser/rendering problem.
    ("UI / Browser Compatibility", (
        "browser", "chrome", "firefox", "edge", "internet explorer", "safari",
        "layout", "grid", "icon", "not visible", "blank page", "rendering",
        "css", "ui rendering", "web browser",
    )),
    ("Workflow / Approval", (
        "workflow", "approve", "approval", "one time", "time based",
        "time-based", "authoris*", "authoriz*", "delegation",
    )),
    ("Security", (
        "vulnerab*", "cipher", "exposure", "exposed", "xss", "injection",
        "smuggling", "clickjack", "cve", "encryption", "tls", "ssl",
        "sensitive", "plaintext", "plain text", "directly accessible",
        "non-html", "hardening",
    )),
    # ⚠️ "unable to", "failed", "fails", "error while" were removed. They matched
    # 169 tickets — every defect is a failure, so the area stopped discriminating.
    # What remains names invalid-input handling and leaked runtime errors.
    ("Negative Testing", (
        "invalid", "special character", "script detected", "input validation",
        "server side input", "server side validation", "malformed",
        "outofmemory", "out of memory", "object reference",
        "string reference not set", "unhandled", "stack trace", "sql exception",
        "null reference",
    )),
    ("Boundary Testing", (
        "large values", "limit", "maximum", "minimum", "length", "bulk",
        "volume", "size", "exceed", "truncat*", "count not matching",
        "large number",
    )),
    ("Environment Compatibility", (
        "windows", "linux", "mac", "macos", "database", "mssql",
        "on-prem", "onprem", "cloud", "infrastructure", "deployment",
        "rdp", "autoscaling",
    )),
    ("Data Integrity / Consistency", (
        "mismatch", "not matching", "duplicate entries", "duplicate service",
        "incorrect data", "missing data", "data mismatch", "not reflecting",
        "inconsistent", "missing in",
    )),
]

#: What each area's evidence implies about coverage. Phrased as a testing
#: statement, never as a product diagnosis.
AREA_GAP = {
    "Third-Party Compatibility": (
        "No client-tool/OS version matrix in the regression suite",
        "Pin a supported matrix (DBeaver, WinSCP, SSMS, Chrome driver, RDP post-patch, "
        "HSM) and run the launch plus core journey per entry every hotfix"),
    "Session Recording": (
        "Recording asserted as session-opened, not as evidence-correct-and-retrievable",
        "Per connector type: assert the artefact exists, plays, maps to the correct "
        "session, and displays the banner"),
    "Authentication / Authorization": (
        "Federated identity and privilege boundaries are not in the regression suite",
        "SAML/Azure AD login, JIT provisioning, AD-bridging toggle, and a negative "
        "privilege test per role"),
    "API / Integration": (
        "API assertions check transport, not application semantics",
        "Assert the application-level errorCode and payload semantics; never "
        "status==200 alone"),
    "Configuration": (
        "Configuration screens tested on defaults only",
        "Save and reload each configuration page, including duplicate-name and "
        "already-exists paths"),
    "Upgrade / Migration": (
        "No post-upgrade regression pass on an upgraded instance",
        "Upgrade a seeded instance from N-2, then run the core journeys against the "
        "migrated data"),
    "Logging / Monitoring": (
        "Log content is not asserted, only that the action completed",
        "Assert log presence, correctness and SIEM forwarding for each audited action"),
    "Performance": (
        "No load or endurance testing on the affected journeys",
        "Memory and endurance runs on vault load and bulk operations at client data "
        "volumes"),
    "UI / Browser Compatibility": (
        "Single-browser UI coverage",
        "Run the core journeys across the supported browser set and assert rendering, "
        "not just navigation"),
    "Workflow / Approval": (
        "Approval paths tested on the happy path only",
        "Time-based and one-time grants, delegation add/approve, revocation at expiry"),
    "Security": (
        "Security findings arrive from client audits rather than internal scans",
        "Add cipher/TLS posture, direct-object and unauthenticated-resource checks to "
        "the pre-release gate"),
    "Negative Testing": (
        "Invalid and unexpected input is under-tested; raw exceptions reach the user",
        "Negative matrix per input, asserting a product error code rather than a "
        "framework exception string"),
    "Boundary Testing": (
        "Field limits and bulk volumes are not exercised",
        "Oversized parameter values, bulk import/update at client volume, and min/max "
        "boundaries per field"),
    "Environment Compatibility": (
        "One reference environment; client OS/DB/deployment variants untested",
        "Matrix the supported OS and deployment shapes for the affected journeys"),
    "Data Integrity / Consistency": (
        "Reads asserted for success, not for agreement with the source of truth",
        "Cross-check list, report and counter values against the database after each "
        "mutating action"),
}


def testing_areas(text: str) -> list[str]:
    """Every testing area a ticket's text implicates. Multi-label by design."""
    return [name for name, terms in TESTING_AREAS if _matcher(terms).search(text)]


# ============================================ testing weak spots — the full detail
#
# `AREA_GAP` above holds (gap, recommended scenario) — enough for a summary row.
# The owner asked for a practical, PAM-specific recommendation per weak spot, so
# this table carries the remaining seven columns of the workbook's Testing Weak
# Spots sheet.
#
# ⛔ EVERY `pam_recommendation` NAMES A REAL FILE, FLAG OR MEASURED FACT from this
# workspace. A recommendation that could be pasted into any product's QA report
# is not a PAM recommendation and does not belong here. Where a statement is an
# inference rather than a measurement it is marked "(inferred)".
#
# Sources drawn on, all workspace-local:
#   `.claude/rules/automation-repo.md`         the bootstrap suite layout + defects
#   `.claude/rules/api-surface.md`             the 1,306-endpoint surface
#   root `CLAUDE.md` §The response envelope    HTTP 200 + application errorCode
#   `docs/findings/issues/ISSUE-009`/`-010`    token lockout, the IIS-killing endpoints
#   `Automation gitlab repo/.../performance/`  the k6 framework, never executed
#   `artifacts/analysis-data/envelope-shapes.json`  the 31 measured response shapes

#: Keys match `AREA_GAP` exactly. Seven fields per area:
#:   root_cause · existing_coverage · missing_coverage · precaution
#:   pam_recommendation · suggested_coverage · automation
AREA_DETAIL = {
    "Environment Compatibility": dict(
        root_cause="QA validates on one reference environment. The framework can "
                   "already address 20 environments — `Environments/*.properties` "
                   "holds 20 files — but a suite run targets exactly one via "
                   "`-Denv`, and CI passes the default.",
        existing_coverage="Functional suites on a single `-Denv` target, typically "
                          "`QA_MsSQL`. `Hosting Environment` (`cf 11220`) shows the "
                          "client spread that is not mirrored in QA.",
        missing_coverage="No matrix execution across OS / DB engine / deployment "
                         "shape. MsSQL vs Oracle, on-prem vs cloud, and Windows "
                         "Server variants are never combined with the core journeys.",
        precaution="Before a hotfix ships, run the smoke suite against at least the "
                   "two DB engines and the two deployment shapes that dominate the "
                   "client base, rather than against the default env only.",
        pam_recommendation="Drive the existing `-Denv` switch from CI instead of "
                           "adding a framework: `mvn clean test -Denv=<env> "
                           "-DsuiteFile=CICD_Suites/APISuite.xml` already "
                           "parameterises every URL, credential, DB and timeout. "
                           "Pick the 4–5 `Environments/*.properties` files that "
                           "match the top client deployments and add one Jenkins "
                           "axis per file. The cost is pipeline time, not new code.",
        suggested_coverage="Core journeys (login, vault fetch, session launch, "
                           "connector open, report generation) × {MsSQL, Oracle} × "
                           "{on-prem, cloud}.",
        automation="High value, low effort — the parameterisation exists. Make it a "
                   "Jenkins matrix axis over `-Denv`.",
    ),
    "Authentication / Authorization": dict(
        root_cause="Two independent identity mechanisms exist and only one is "
                   "exercised. The API tier authenticates via `POST /arcontoken`; "
                   "the web tier authenticates via `POST /frmLoginACMO.aspx` on "
                   ":1302. They are separate identity stores, so a test passing "
                   "against one proves nothing about the other.",
        existing_coverage="`ApiHelper.getToken()` for API auth; UI login in the "
                          "Playwright E2E suites. Local accounts only.",
        missing_coverage="Federated identity (SAML, Azure AD), JIT provisioning, "
                         "AD-bridging on/off, and negative privilege tests per role. "
                         "No test asserts that a role *cannot* reach a resource.",
        precaution="Treat every privilege boundary as needing a negative test. A "
                   "passing positive test on an over-privileged account hides an "
                   "authorisation defect completely.",
        pam_recommendation="Add a role-matrix suite under `API_Suites/` that drives "
                           "the same endpoint with tokens minted for each role and "
                           "asserts the **application-level** rejection, not the "
                           "HTTP status — a PAM rejection is normally HTTP 200 with "
                           "an `errorCode` in the body. Use "
                           "`PamApiValidator`/`ErrorCodeRegistry` from "
                           "`com.arcon.utils.validation`, not a status check. "
                           "⛔ Mint one token per run and pin it to `$PAM_API_TOKEN`: "
                           "`GenericScheduler` is a shared service account and has "
                           "been locked twice by retry loops (`ISSUE-009`).",
        suggested_coverage="Per role × per protected endpoint: one positive, one "
                           "negative. SAML and Azure AD login end-to-end. "
                           "AD-bridging toggled both ways.",
        automation="Automate the role matrix — it is pure API and highly repetitive. "
                   "Keep federated-login setup manual or semi-automated; the IdP "
                   "side is environment-bound.",
    ),
    "Configuration": dict(
        root_cause="Configuration screens are exercised with default values, so the "
                   "save/reload round trip and the already-exists path are never "
                   "reached. The product signals both as success.",
        existing_coverage="Create-path tests that assert the call succeeded.",
        missing_coverage="Save-then-reload verification, duplicate-name handling, "
                         "and the distinction between *inserted* and *no-op*.",
        precaution="⛔ `Success: true` is not evidence of a write. Measured on this "
                   "product: `POST /api/ServiceCreation/SetServiceDetails` returns "
                   "`Success: true` with `Message: \"Already Exists\"` when the "
                   "record is already present — nothing was inserted, and both the "
                   "status code and the success flag are green.",
        pam_recommendation="Make every configuration assertion read `Message` "
                           "semantics, not `Success`: `\"Inserted Successfully\"` "
                           "means inserted, `\"Already Exists\"` means no-op. Then "
                           "add a reload step that re-reads the entity and compares "
                           "field by field. `DbPersistenceValidator` in "
                           "`com.arcon.utils.validation` already checks persistence "
                           "against the database — wire it into the configuration "
                           "suites, where it is currently unused.",
        suggested_coverage="Per configuration page: save → reload → compare; "
                           "duplicate name; empty and boundary values; cancel "
                           "without saving.",
        automation="Automate fully. This is the highest-yield, lowest-risk "
                   "automation target in the set — it is deterministic and "
                   "API-driven.",
    ),
    "Logging / Monitoring": dict(
        root_cause="Log assertions stop at 'the action completed'. Log *content* and "
                   "downstream forwarding are never checked, so an audit gap looks "
                   "identical to a working audit trail.",
        existing_coverage="Action-level success assertions. `ActivityLogs` suite "
                          "exists.",
        missing_coverage="Assertion of log record content, correctness of the actor "
                         "and target, and SIEM forwarding.",
        precaution="⛔ Two `ActivityLogs` endpoints must never be called: "
                   "`GET /api/ActivityLogs/GetErrorLogs` and "
                   "`GET /api/ActivityLogs/GetLogs` hang for 30 s and stop the IIS "
                   "application pool — three sequential requests took the whole API "
                   "to 503 with no recovery (`ISSUE-010`). Assert log content "
                   "through the database or a log-file reader, never through those "
                   "endpoints.",
        pam_recommendation="Read the audit record from the database via "
                           "`DbPersistenceValidator` after each audited action and "
                           "assert actor, target, timestamp and outcome. This routes "
                           "around the blocklisted endpoints entirely, which is the "
                           "only safe way to test logging on this product.",
        suggested_coverage="Per audited action: record exists, names the right "
                           "actor/target, and is forwarded. Negative: a failed "
                           "action is also logged.",
        automation="Automate the DB-side assertions. Keep SIEM forwarding as a "
                   "manual or integration-environment check.",
    ),
    "Session Recording": dict(
        root_cause="A recording is asserted as 'session opened', which is a "
                   "different fact from 'the evidence exists, plays, and maps to "
                   "the right session'. Session recording is a compliance feature, "
                   "so the artefact is the deliverable, not the session.",
        existing_coverage="Session-launch tests per connector.",
        missing_coverage="Artefact existence, playability, correct session mapping, "
                         "and the recording banner.",
        precaution="Test per connector type. Connector is the single heaviest module "
                   "in the client-ticket data, and recording behaviour differs by "
                   "connector.",
        pam_recommendation="Extend the existing session-launch tests with a "
                           "post-session assertion phase: locate the artefact, check "
                           "it is non-trivial in size, and confirm it resolves to the "
                           "session id the test created. Cover RDP, SSH and database "
                           "connectors separately — the client tickets cluster by "
                           "connector, not by the recording subsystem.",
        suggested_coverage="Per connector: launch → act → close → artefact exists, "
                           "plays, maps to session, banner shown. Negative: a "
                           "denied session produces no artefact.",
        automation="Partially automatable — existence and mapping yes, playback "
                   "quality realistically manual.",
    ),
    "Third-Party Compatibility": dict(
        root_cause="No pinned support matrix for the client tools and OS patch "
                   "levels PAM brokers access to, so a vendor-side change surfaces "
                   "as a client ticket.",
        existing_coverage="Ad-hoc validation when a defect is reported.",
        missing_coverage="A declared, version-pinned matrix exercised every hotfix.",
        precaution="A third-party version bump is a change to PAM's tested surface "
                   "even though no PAM code changed. Treat it as one.",
        pam_recommendation="Pin the matrix the client tickets actually name — "
                           "DBeaver, WinSCP, SSMS, Chrome driver, RDP after Windows "
                           "patching, HSM — and run the launch plus one core journey "
                           "per entry every hotfix. Derive the list from the "
                           "`Third-Party Tool & Platform` category in this analysis "
                           "rather than from a vendor doc; the tickets name what "
                           "clients really run.",
        suggested_coverage="Per matrix entry: connect, authenticate, run one "
                           "representative operation, close cleanly.",
        automation="Automate what has a CLI or driver (SSMS, DBeaver, WinSCP). RDP "
                   "post-patch needs a real desktop and stays manual.",
    ),
    "UI / Browser Compatibility": dict(
        root_cause="`-DbrowserType` already accepts chrome, chromium, firefox, "
                   "safari and edge, but suites are executed on the default "
                   "(chrome), so the capability is present and unused.",
        existing_coverage="Playwright E2E on chrome.",
        missing_coverage="The other four browsers, and rendering assertions rather "
                         "than navigation assertions.",
        precaution="Navigation success is not rendering correctness. A page that "
                   "loads with a broken layout passes a navigation test.",
        pam_recommendation="Add a browser axis to the Jenkins pipeline over the "
                           "existing `-DbrowserType` flag — no framework change "
                           "required — and add visual or structural assertions to "
                           "the core journeys. Start with edge and firefox: they "
                           "cover the majority of the enterprise client base "
                           "(inferred from the client list, not measured).",
        suggested_coverage="Core journeys × {chrome, edge, firefox}, with layout "
                           "assertions on the dashboard and session-launch pages.",
        automation="Fully automatable via the existing flag. Cheapest win in the set.",
    ),
    "Boundary Testing": dict(
        root_cause="Field limits and bulk volumes are not exercised, so defects "
                   "appear only at client data volumes.",
        existing_coverage="Functional tests at nominal input sizes.",
        missing_coverage="Oversized values, bulk import/update at client volume, and "
                         "min/max per field.",
        precaution="Bulk operations are where this product fails: a measured client "
                   "ticket (`PAMIT-43186`, ICICI Bank) is a bulk import failing on "
                   "large parameter values.",
        pam_recommendation="Drive boundary cases from the Excel test data the API "
                           "suites already consume — the framework is Excel-driven, "
                           "so adding oversized and boundary rows costs data, not "
                           "code. Assert the product's `errorCode`, not a framework "
                           "exception string. Add one bulk-import case at "
                           "realistic client volume (thousands of rows, not tens).",
        suggested_coverage="Per input field: min, max, max+1, empty, oversized. "
                           "Bulk import and bulk update at client volume.",
        automation="Fully automatable through the existing Excel-driven data layer.",
    ),
    "API / Integration": dict(
        root_cause="API assertions check transport, not application semantics. On "
                   "this product that is a structural defect in the test approach, "
                   "not an oversight: most PAM endpoints return **HTTP 200 with an "
                   "application-level `errorCode` in the body**, so a rejected "
                   "request is normally a 200.",
        existing_coverage="Status-code and response-time assertions across the API "
                          "suites (71 per-module suite files).",
        missing_coverage="Application-level `errorCode` and payload-shape "
                         "assertions. 31 distinct response shapes were measured "
                         "across 1,868 captured calls; a fixed-shape assertion "
                         "breaks on most of them.",
        precaution="⛔ Never write an assertion that checks only "
                   "`response.status() == 200`. It passes against a fully rejected "
                   "request. This is the single highest-impact rule on this product.",
        pam_recommendation="Use `com.arcon.utils.validation` for anything new: "
                           "`PamEnvelope` normalises the 31 measured shapes, "
                           "`PamApiValidator` runs twelve layers, "
                           "`ErrorCodeRegistry` matches on the numeric prefix and "
                           "records an unrecognised code as an observation. ⛔ Do "
                           "**not** reuse `ApiHelper.validateResponseErrorCode` "
                           "patterns from before OBJ-007: that code read "
                           "`node.has(\"success\")` in camelCase while every "
                           "response on this API carries PascalCase `Success` "
                           "(0 vs 1,580 occurrences), so its first assertion failed "
                           "on every response the product can produce. Negative "
                           "cases need both an `ExpectedStatus` (often 200) and an "
                           "`ExpectedErrorCode`.",
        suggested_coverage="Per endpoint: positive with payload-semantic assertion; "
                           "negative with expected `errorCode`; malformed body; "
                           "missing required field.",
        automation="Already automated in shape — the change is the assertion layer, "
                   "not new tests. Highest priority remediation.",
    ),
    "Upgrade / Migration": dict(
        root_cause="Testing runs against freshly provisioned instances, so "
                   "migrated-data defects cannot appear. Clients upgrade; QA "
                   "installs.",
        existing_coverage="Functional suites on clean installs.",
        missing_coverage="Any post-upgrade regression pass on an instance carrying "
                         "pre-upgrade data.",
        precaution="A clean-install pass says nothing about an upgraded instance. "
                   "Most client deployments are upgrades.",
        pam_recommendation="Seed an instance on N-2, upgrade it, then run the "
                           "existing `CICD_Suites/APISuite.xml` against the migrated "
                           "data. The suite needs no modification — only the "
                           "environment does — so this is an infrastructure task, "
                           "not a test-authoring task. Pair it with "
                           "`DbPersistenceValidator` checks on the migrated tables.",
        suggested_coverage="Upgrade from N-1 and N-2, then: login, vault fetch, "
                           "session launch, report generation, and a spot check on "
                           "migrated entity counts.",
        automation="Automate the suite run. The upgrade step itself is best scripted "
                   "as environment provisioning rather than as a test.",
    ),
    "Negative Testing": dict(
        root_cause="Invalid and unexpected input is under-tested, and where it is "
                   "tested the assertion accepts a framework exception string as a "
                   "pass. Raw exceptions therefore reach clients.",
        existing_coverage="A negative-case column exists in the Excel test data and "
                          "`validateApiResponseWithResponseTime_ExcelBasedsetting"
                          "negative(...)` consumes it.",
        missing_coverage="A systematic negative matrix per input, and assertions "
                         "that require a *product* error code rather than any error.",
        precaution="A test that passes because the product threw "
                   "`\"String reference not set to an instance of an object\"` is "
                   "asserting a bug, not preventing one — that exact string is a "
                   "live client ticket (`PAMIT-43087`, TCS Cyber Security).",
        pam_recommendation="Require an `ExpectedErrorCode` on every negative row in "
                           "the Excel data and fail the case when the response body "
                           "carries a .NET exception string instead. "
                           "`ErrorCodeRegistry` records an unrecognised code as an "
                           "observation rather than a failure, so the missing "
                           "product error-code registry is surfaced as a finding "
                           "instead of failing the run — that is the correct "
                           "behaviour and should not be 'fixed' by hardcoding codes.",
        suggested_coverage="Per input: null, empty, wrong type, oversized, injection "
                           "string, unauthorised actor. Each with a named expected "
                           "error code.",
        automation="Fully automatable through the existing Excel negative-case path.",
    ),
    "Performance": dict(
        root_cause="No load or endurance testing runs against the affected "
                   "journeys. A k6 framework for the login journey exists at "
                   "`Automation gitlab repo/pam_automation_bootstrap/performance/` "
                   "and **has never been executed**.",
        existing_coverage="Per-call response-time capture in the API suites. No "
                          "sustained load, no endurance, no concurrency.",
        missing_coverage="Load, soak and concurrency on vault load, bulk operations "
                         "and session launch.",
        precaution="⛔ Three endpoints stop the IIS application pool after three "
                   "sequential requests — `GetErrorLogs`, `GetLogs`, "
                   "`GetAllActiveUserDetails` (`ISSUE-010`). A naive load test "
                   "against this API can take the environment down; enforce the "
                   "blocklist at planning time, before a request is built.",
        pam_recommendation="Execute the k6 framework that already exists rather than "
                           "building one. It is deny-by-default "
                           "(`PERF_EXECUTE=true` is required, checked in `setup()` "
                           "and on the request path) and authenticates against the "
                           "**web tier** (`POST /frmLoginACMO.aspx` on :1302), not "
                           "`/arcontoken` — so it does not risk the "
                           "`GenericScheduler` lockout. ⛔ Running it generates load "
                           "against an authentication endpoint and is a separate, "
                           "named owner decision; it is explicitly not covered by "
                           "'execute everything'. Start at "
                           "`performance/README.md`.",
        suggested_coverage="Login at expected concurrency; vault fetch under "
                           "sustained load; bulk import at client volume; a soak run "
                           "long enough to expose the memory growth clients report.",
        automation="The harness exists. This is an execution and owner-approval "
                   "question, not an authoring question.",
    ),
    "Security": dict(
        root_cause="Security findings arrive from client audits rather than internal "
                   "scans, so the product's first security reviewer is the customer.",
        existing_coverage="None systematic in the QA suites.",
        missing_coverage="Cipher/TLS posture, direct-object reference checks, and "
                         "unauthenticated-resource checks in the pre-release gate.",
        precaution="This workspace already holds an unraised security finding: "
                   "`LH-13` records 19 endpoints accepting an invalid bearer token, "
                   "6 of them writes. Raising it is the owner's call and it has not "
                   "been raised — do not treat its absence from Jira as absence of "
                   "the defect.",
        pam_recommendation="Add an unauthenticated-and-invalid-token sweep to the "
                           "pre-release gate, driven from the endpoint inventory "
                           "the harness already has (1,306 endpoints). Assert that "
                           "a protected endpoint rejects an invalid bearer token "
                           "**at the application level** — an HTTP 200 with a "
                           "success envelope is the failure mode to look for, and "
                           "it is exactly what LH-13 measured. Note credentials sit "
                           "in plaintext across all 20 `Environments/*.properties` "
                           "files; that is a separate finding worth its own ticket.",
        suggested_coverage="Per protected endpoint: no token, malformed token, "
                           "expired token, valid token for the wrong role. Plus TLS "
                           "and cipher posture on the two listening tiers.",
        automation="Automate the token sweep — it is mechanical and the inventory "
                   "exists. TLS posture is a scanner job, not a suite.",
    ),
    "Workflow / Approval": dict(
        root_cause="Approval paths are tested on the happy path only, so expiry, "
                   "delegation and revocation are unexercised.",
        existing_coverage="Request-and-approve happy path.",
        missing_coverage="Time-based and one-time grants, delegation add/approve, "
                         "revocation at expiry.",
        precaution="An access grant that fails to expire is a security defect that "
                   "a happy-path test reports as a pass.",
        pam_recommendation="Add a time-manipulation or short-TTL configuration to "
                           "the test environment so expiry can be asserted inside a "
                           "suite run rather than being untestable. Then assert the "
                           "**negative** side of every grant: after expiry or "
                           "revocation the session launch must be refused, and the "
                           "refusal must carry a product error code rather than a "
                           "generic failure.",
        suggested_coverage="Grant → use → expire → use again (must fail). "
                           "Delegation add, approve, revoke. One-time grant used "
                           "twice.",
        automation="Automatable once short TTLs are configurable in the test "
                   "environment; that configuration is the blocker, not the test.",
    ),
    "Data Integrity / Consistency": dict(
        root_cause="Reads are asserted for success, not for agreement with the "
                   "source of truth, so a list or counter can disagree with the "
                   "database and every test still passes.",
        existing_coverage="Read-succeeds assertions.",
        missing_coverage="Cross-checks of list, report and counter values against "
                         "the database after each mutating action.",
        precaution="A client ticket in this data is exactly this shape: "
                   "`PAMIT-38793` (OCL-Paytm) reports an autoscaling group server "
                   "count not matching. The API returned success; the number was "
                   "wrong.",
        pam_recommendation="`DbPersistenceValidator` in `com.arcon.utils.validation` "
                           "exists for this and is under-used. After each mutating "
                           "call, re-read the entity from the database and compare "
                           "field by field — not just row existence. The 20 "
                           "`Environments/*.properties` files already carry the DB "
                           "connection details the validator needs, so no new "
                           "configuration is required.",
        suggested_coverage="Per mutating action: DB state matches API response; "
                           "list counts match DB counts; report totals match "
                           "underlying rows.",
        automation="Fully automatable and already supported by the validation "
                   "package.",
    ),
}


def area_detail(area: str) -> dict:
    """Detail for one testing area, with explicit gaps rather than silent blanks.

    ⛔ Returns `"not yet authored"` rather than `""` for a missing area. An empty
    cell in the workbook is indistinguishable from "no recommendation needed",
    and a weak spot with no recommendation is the one thing the owner asked this
    table not to produce.
    """
    d = AREA_DETAIL.get(area)
    if d:
        return d
    return {k: "not yet authored — area appeared after this table was written"
            for k in ("root_cause", "existing_coverage", "missing_coverage",
                      "precaution", "pam_recommendation", "suggested_coverage",
                      "automation")}


# ==================================== regression + RCA fields — the complete sweep
#
# ⛔ OWNER REQUIREMENT (#9): use **every** regression-related field Jira actually
# has, not a fixed set of three. Where a field does not exist or is empty, say
# `Info not available in JIRA` explicitly rather than leaving it ambiguous.
#
# ⛔ THE SECOND INSTANCE OF THE SAME ERROR CLASS AS `affectedVersion`. §13 of the
# report claimed:
#
#     "`Module`, `Category`, `Sub-Category`, `Root Cause` ... all unpopulated
#      (0 / 376). The whole taxonomy is derived from ticket text. Jira holds no
#      categorisation to cross-check it against."
#
# That checked `customfield_10113` ("Root Cause", 0.2%) and `customfield_10199`
# ("Root cause", 0.1%). It never checked **`customfield_10245` ("RCA")**, which
# is **80.7% populated** (1,622 / 2,010) with a 33-value, 15-family structured
# taxonomy. Jira has held a cross-checkable root-cause classification all along.
#
# The lesson is identical to `D42`'s and is now stated twice for a reason: in this
# instance, several fields share a concept and only one of them is the live one.
# **Measure every same-named candidate before concluding a fact is unrecorded.**

#: The sentinel value written wherever Jira genuinely has nothing. Owner-specified
#: wording — do not paraphrase it, and never substitute a blank cell, "—", "N/A"
#: or a derived guess. A blank is indistinguishable from "not applicable"; this
#: string says which.
NOT_IN_JIRA = "Info not available in JIRA"

RCA_FIELD = "customfield_10245"          # "RCA"                        80.7%
RCA_DETAILS_FIELD = "customfield_10567"  # "RCA Details (Impact Analysis)" 79.2%

#: ⚠️ Field-specific sentinels. `Reopen Original Ticket ID` is a free-text field
#: and 64 of its 142 values are junk answers to a question it does not ask —
#: "No", "NONE", "na", "no". Treating those as ticket IDs would invent links.
#: ⛔ Cannot go in the global `NULL_SENTINELS`: "No" is a legitimate value for
#: every Yes/No select in this project, including `Is reopen from customer`.
FIELD_SENTINELS = {
    "customfield_10781": {"No", "no", "NO", "NONE", "None", "none", "na", "NA",
                          "N/A", "n/a", "-", "nil", "Nil", "NIL", "0"},
}

#: Every regression-shaped field in this Jira instance, measured on the
#: 2,010-ticket Affected-Milestone client build line. `available` drives whether
#: the analysis reports a value or `NOT_IN_JIRA`.
#:
#: Ordered most useful first. Populations are point measurements, not invariants —
#: the drift loop is the place to catch them moving, not a comment.
REGRESSION_AUDIT = [
    # id, name, populated, pct, available, role
    ("customfield_10245", "RCA", 1622, 80.7, True,
     "Structured root-cause taxonomy — 33 values in 15 families. THE most "
     "populated analytical field in the project and previously unused"),
    ("customfield_10567", "RCA Details (Impact Analysis)", 1591, 79.2, True,
     "Free-text impact analysis behind the RCA value"),
    ("customfield_10249", "Fixed Date", 1026, 51.0, True,
     "When the fix was recorded — the second half of a fix-latency measure"),
    ("customfield_10780", "Is reopen from customer", 512, 25.5, True,
     "A Yes is a FAILED FIX, not a new defect"),
    ("customfield_11253", "Functionality working in previous version", 499, 24.8, True,
     "The regression gate"),
    ("customfield_11254", "Previous working version", 491, 24.4, True,
     "The last working build. 130 of these carry the literal string 'None', "
     "leaving 361 that name a real version"),
    ("customfield_10600", "Reopen RCA details", 152, 7.6, True,
     "Free text on why a reopen happened"),
    ("customfield_10741", "Reopen RCA", 147, 7.3, True,
     "Why the fix failed — Code Fix (48), Dependency failure (29), Audit (23), "
     "Hosting Issue (22), Tester Understanding (17), Data Issue (8)"),
    ("customfield_10781", "Reopen Original Ticket ID", 142, 7.1, True,
     "The original ticket a reopen descends from. ⚠️ 64 of 142 values are junk "
     "('No', 'NONE', 'na') — see FIELD_SENTINELS"),
    ("customfield_10236", "ReOpen Date", 82, 4.1, True, "When the reopen happened"),
    ("customfield_10235", "ReOpen Time Spent", 72, 3.6, True,
     "Hours spent on the reopen — rework cost"),
    ("customfield_11353", "RCA Category / Description updated?", 25, 1.2, True,
     "RCA review hygiene flag. Too sparse for a rate"),
    ("customfield_11355", "RCA Review Remarks", 24, 1.2, True,
     "Reviewer commentary on the RCA. Too sparse for a rate"),
    ("customfield_10136", "Affected QA Build", 9, 0.4, True,
     "Near-empty; all nine read 'Build 35.8.29'"),
    ("customfield_10150", "QA Build/Drop", 9, 0.4, True, "Near-empty"),
    ("customfield_10113", "Root Cause", 5, 0.2, False,
     "⛔ Effectively empty — and this is the field whose emptiness was previously "
     "read as 'Jira holds no root-cause categorisation'. Use RCA (10245)"),
    ("customfield_10199", "Root cause", 3, 0.1, False,
     "⛔ Effectively empty. A second same-named decoy alongside 10113"),
    ("customfield_10147", "Hotfix Release Date", 1, 0.0, False,
     "⛔ One value, dated 2022. Unusable"),
    ("customfield_11018", "ReopenCount", 0, 0.0, False,
     "⛔ EXISTS BUT IS NEVER POPULATED. A reopen count must be derived from "
     "ReOpen Date / Reopen RCA presence instead"),
    ("customfield_10164", "Phase", 0, 0.0, False,
     "⛔ EXISTS BUT IS NEVER POPULATED. Defect-injection phase (requirement / "
     "design / code / test) is therefore NOT ANSWERABLE from Jira"),
    ("customfield_10065", "Module", 0, 0.0, False, "⛔ Never populated"),
    ("customfield_10051", "Category", 0, 0.0, False, "⛔ Never populated"),
]

#: Regression questions this analysis cannot answer, and why. ⛔ Reported rather
#: than estimated: an inferred defect-injection phase would look like a
#: measurement and drive real test-strategy decisions.
REGRESSION_NOT_AVAILABLE = [
    ("Defect injection phase", "`Phase` (`cf 10164`) exists but is 0% populated",
     "Cannot say whether a defect was introduced in requirements, design, code "
     "or test. Deriving it from the RCA family would be an inference presented "
     "as a fact — `Code - *` is where the defect was *found in code*, not "
     "necessarily where it was *introduced*"),
    ("Reopen count per ticket", "`ReopenCount` (`cf 11018`) exists but is 0%",
     "A reopen is visible as a boolean (`Is reopen from customer`, `ReOpen "
     "Date`), not as a count. 'Reopened three times' is not answerable"),
    ("Regression test executed / suite name", "no such field exists in PAMIT",
     "Cannot link a defect to the test that should have caught it, so "
     "'was this covered?' is answered by the derived testing-area axis, not "
     "by Jira"),
    ("Requirement or user-story link", "no requirement link field is populated",
     "Scenario gaps cannot cite a requirement, which is why the gap provenance "
     "table marks requirements as NOT USED"),
    ("Detected-by / found-in-testing stage", "no such field exists in PAMIT",
     "Every ticket in this population is client-raised by definition, so "
     "internal-vs-external detection ratio is not measurable here"),
]

#: RCA values that mean **this was never a product defect**. ⛔ Load-bearing for
#: the weak-spot analysis: a testing gap attributed to an enhancement request or
#: a working-as-expected ticket is a false finding. 315 of the 1,622 RCA-carrying
#: tickets fall here — Jira's own classification disagreeing with the defect
#: type, which is a finding in itself and is reported, not silently applied.
RCA_NON_DEFECT = {
    "Others - Working as expected", "Not a bug", "Requests - Enhancement",
    "Requests - Information Request", "Requests - APEM Tool",
    "Requests - Script Request", "Miscommunication",
}

#: RCA values that are a **testing** failure by Jira's own classification.
#: These are the strongest possible evidence for a testing weak spot: the product
#: team recorded the cause as inadequate coverage, not the analysis inferring it.
RCA_TESTING_FAILURE = {
    "Analysis - Inadequate Test Coverage", "Insufficient Unit Test case",
    "Analysis - Incomplete Requirement", "Analysis - Inadequate Technical Design",
    "Environment - Non replicated",
}


def clean_field(fields: dict, cf: str):
    """`clean_value` plus this field's own sentinel set. Returns None or a value."""
    from_jira = fields.get(cf)
    v = clean_value(
        from_jira.get("value") or from_jira.get("name") if isinstance(from_jira, dict)
        else from_jira)
    if v is None:
        return None
    if isinstance(v, str) and v.strip() in FIELD_SENTINELS.get(cf, ()):
        return None
    return v


def rca_family(rca: str | None) -> str:
    """The family before the dash — `Code - Logic Issue` -> `Code`.

    ⚠️ Two values break the ` - ` convention and must not be mangled:
    `Environment- Env unavailable` (no space before the dash, 47 tickets) and the
    bare values `Not a bug`, `Data Issue`, `Miscommunication`,
    `Deployment Issue`, `Missing Code / DB Scripts`, `Insufficient Unit Test
    case`, `Insufficient Data`, `Code not checked-in`. Splitting naively on `-`
    turns `Code not checked-in` into family `Code not checked`.
    """
    if not rca:
        return NOT_IN_JIRA
    t = str(rca).strip()
    if " - " in t:
        return t.split(" - ")[0].strip()
    if t.startswith("Environment-"):
        return "Environment"
    return t


def rca_class(rca: str | None) -> str:
    """`non-defect` · `testing-failure` · `product-defect` · `unstated`."""
    if not rca:
        return "unstated"
    t = str(rca).strip()
    if t in RCA_NON_DEFECT:
        return "non-defect"
    if t in RCA_TESTING_FAILURE:
        return "testing-failure"
    return "product-defect"
