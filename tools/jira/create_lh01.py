#!/usr/bin/env python3
"""Create the PAMIT Jira ticket for developer loophole LH-01 and attach its evidence.

Jira Cloud REST v3 requires the description as ADF (Atlassian Document Format), not
wiki markup, so the description is composed as ADF nodes here rather than converted
from JIRA-TICKET.md. JIRA-TICKET.md stays the human-readable draft; this file is the
machine-readable version of the same content.

Field values were resolved against the live createmeta for PAMIT/Bug - see
jira.md for how they were discovered and why each was chosen.

Usage
-----
    python tools/jira/create_lh01.py --dry-run     # print the payload, create nothing
    python tools/jira/create_lh01.py --create      # create the issue and attach evidence
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jira_client import Jira, load_env                                   # noqa: E402

HERE = Path(__file__).resolve().parent
def _workspace_root():
    """Locate the workspace root by marker, not by counting parents (`OBJ-025`).

    Mirrors tools/paths.py. Duplicated rather than imported because this package
    is not a sibling of it; what matters is that the markers are identical and
    that neither counts parent hops. ROOT was `HERE.parent` - a one-hop guess
    that was correct only while tools/jira/ sat at the workspace root."""
    for candidate in (HERE, *HERE.parents):
        if (candidate / "CLAUDE.md").is_file() and (candidate / ".claude").is_dir():
            return candidate
    raise SystemExit(f"cannot locate the workspace root above {HERE}")


ROOT = _workspace_root()
PACK = ROOT / "artifacts" / "loopholes" / "LH-01-http-200-application-failures"
ZIP = HERE / ".tmp" / "LH-01-http-200-application-failures-evidence.zip"

# Attached in this order. JIRA-TICKET.md is deliberately excluded - it is the internal
# draft of this very ticket, so attaching it to the ticket would be circular.
ATTACHMENTS = [PACK / "EVIDENCE.xlsx", PACK / "EVIDENCE.md", ZIP]
EXCLUDED_FROM_ATTACHMENTS = {"JIRA-TICKET.md"}

# Resolved from GET /rest/api/3/issue/createmeta/PAMIT/issuetypes/10009
IDS = {
    "issuetype_bug": "10009",
    "severity_sev1": "12936",            # Sev-0..Sev-3; Sev-1 = critical, non-blocking
    "dept_automation": "13273",          # Department Of Created By -> Automation Team
    "client_internal_arcon": "11183",    # Primary Client -> Internal (ARCON)
    "db_mssql": "11188",                 # Database Type -> MSSQL
    "hosting_windows": "22093",          # Hosting Environment -> Windows (IIS)
    "complexity_medium": "14247",        # Task Complexity -> Medium
    "fixversion_hf12": "17321",          # 35.8.29 HF12 (unreleased)
    # The six below are reported optional by createmeta but enforced by a project
    # validator on the create screen - a create without them fails HTTP 400.
    "milestone_hf12": "21486",           # Affected Milestone. -> 35.8.29 HF12
    "os_all": "12766",                   # End-User OS -> All (server-side API defect)
    "prev_working_no": "22131",          # Functionality working in previous version -> No
    "prev_version_none": "22194",        # Previous working version -> None
    "reopen_no": "18854",                # Is reopen from customer -> No
}


# ------------------------------------------------------------------- ADF builders
def txt(s, *marks):
    n = {"type": "text", "text": s}
    if marks:
        n["marks"] = [{"type": m} for m in marks]
    return n


def code_inline(s):
    return txt(s, "code")


def para(*content):
    return {"type": "paragraph", "content": list(content)}


def heading(level, s):
    return {"type": "heading", "attrs": {"level": level},
            "content": [txt(s)]}


def codeblock(s, lang="json"):
    return {"type": "codeBlock", "attrs": {"language": lang},
            "content": [txt(s)]}


def _cell(kind, content):
    return {"type": kind, "attrs": {}, "content": content}


def table(headers, rows):
    """Rows accept a plain string or a list of inline nodes per cell."""
    def cellcontent(v):
        return [para(*(v if isinstance(v, list) else [txt(str(v))]))]
    head = {"type": "tableRow",
            "content": [_cell("tableHeader", [para(txt(str(h), "strong"))])
                        for h in headers]}
    body = [{"type": "tableRow",
             "content": [_cell("tableCell", cellcontent(v)) for v in r]}
            for r in rows]
    return {"type": "table", "attrs": {"isNumberColumnEnabled": False,
                                       "layout": "default"},
            "content": [head, *body]}


def bullets(items):
    return {"type": "bulletList",
            "content": [{"type": "listItem",
                         "content": [para(*(i if isinstance(i, list) else [txt(str(i))]))]}
                        for i in items]}


def panel(kind, *content):
    return {"type": "panel", "attrs": {"panelType": kind}, "content": list(content)}


def rule():
    return {"type": "rule"}


# --------------------------------------------------------------------- the ticket
SUMMARY = ("API returns HTTP 200 for application-level failures - 289 calls across 276 "
           "endpoints report Success:false inside a 200 OK")


def build_description(cfg: dict) -> dict:
    env = cfg.get("TEST_ENVIRONMENT", "QA_MsSQL")
    app = cfg.get("APPLICATION_URL", "")
    api = cfg.get("API_URL", "")
    build = cfg.get("BUILD_NUMBER", "")

    c = []
    c.append(panel(
        "error",
        para(txt("The API returns HTTP 200 OK while the response body reports a hard "
                 "application-level failure. Any client that branches on the status "
                 "code records a rejected request as a success.", "strong")),
        para(txt("289 of 1,688 HTTP 200 responses in a single run were failures. "
                 "Re-validated live on 2026-07-31: 289 of 289 (100%) still reproduce."))))

    c.append(heading(2, "Environment"))
    c.append(table(["Item", "Value"], [
        ["Environment", env],
        ["Application URL", [txt(app, "code")]],
        ["API URL", [txt(api, "code")]],
        ["Build", build],
        ["Database", "MSSQL"],
        ["Found in", "Dynamic API validation run 2026-07-29_181439 - 1,868 live calls"],
        ["Re-validated", "2026-07-31 - all 289 replayed, 289/289 reproduce"],
    ]))

    c.append(heading(2, "What happens"))
    c.append(para(txt("The transport layer and the application layer disagree about "
                      "whether the request succeeded. Measured across a full dynamic "
                      "validation run, one retained evidence file per call:")))
    c.append(table(["Measure", "Value"], [
        ["Calls issued", "1,868"],
        ["Returned HTTP 200", "1,688"],
        ["...of which carried Success: false", [txt("289", "strong")]],
        ["Distinct endpoints affected", [txt("276", "strong")]],
        ["Distinct controllers affected", [txt("36", "strong")]],
        ["Distinct ErrorCode values observed", "104 (plus 7 emitting no usable code)"],
        ["Status-only suite would score this run", "90% green"],
        ["True pass rate under full validation", [txt("64%", "strong")]],
    ]))
    c.append(para(txt("Example response, captured verbatim:")))
    c.append(codeblock(
        'HTTP/1.1 200 OK\n'
        'Content-Type: application/json\n\n'
        '{ "Program": "ARCON PAM API",\n'
        '  "Version": "1.0",\n'
        '  "DateTime": "29/Jul/2026 07:13:24",\n'
        '  "Success": false,\n'
        '  "ErrorCode": "103-ADB-SGL",\n'
        '  "ErrorMessage": "Input parameter is null" }'))

    c.append(heading(2, "Why this is Critical"))
    c.append(para(txt("Every consumer that branches on the status code is wrong on these "
                      "paths - the PAM UI, partner integrations, load-balancer health "
                      "checks, APM and alerting, and our own test suite.")))
    c.append(bullets([
        "A status-code-only suite scores this run 90% green. The true pass rate is 64%. "
        "The 26-point gap is 406 calls reported as passing while the server rejected them.",
        "84 of the 289 are genuine server faults - unhandled exceptions, a missing "
        "assembly, database errors - that never appear as 5xx in any dashboard, so "
        "monitoring cannot see them.",
    ]))

    c.append(heading(2, "Re-validated live on 2026-07-31"))
    c.append(para(txt("All 289 calls were replayed against " + env + " using the same "
                      "verb, body and headers as the original run.")))
    c.append(table(["Measure", "Result"], [
        ["Calls replayed", "289"],
        ["Still returning HTTP 200 with Success: false", [txt("289 (100%)", "strong")]],
        ["No longer reproducing", "0"],
        ["Returning the identical ErrorCode two days later", "288 of 289"],
    ]))
    c.append(para(
        txt("The one exception is not a fix: "),
        code_inline("DeviceOnboarding/CreateGenericIdsV2"),
        txt(" still fails at HTTP 200 but now reports "),
        code_inline("203-DOC-CGI"),
        txt(" where it previously reported "),
        code_inline("104 - DOC-OTUV2"),
        txt(". The failure is unchanged; only its label moved - itself evidence that the "
            "code register is not stable enough for a client to branch on.")))

    c.append(heading(2, "The server already classifies every failure"))
    c.append(para(txt("This is what makes the fix mechanical rather than a redesign. "
                      "Every ErrorCode carries a three-digit prefix that already encodes "
                      "the failure class. That classification is computed server-side and "
                      "then discarded before the status line is written. Mapping it back "
                      "is a lookup, not new logic.")))
    c.append(table(
        ["ErrorCode prefix", "Meaning (from observed messages)", "Calls",
         "Correct HTTP status"],
        [["103", "Input parameter null/missing", "20", "400 Bad Request"],
         ["104", "Input parameter invalid", "5", "400 Bad Request"],
         ["201", "Validation error", "87", "400 Bad Request"],
         ["203", "Parameter error", "82", "400 Bad Request"],
         ["204", "No record found", "1", "404 Not Found"],
         ["206", "Parameter error", "1", "400 Bad Request"],
         ["902", "System error", "46", "500 Internal Server Error"],
         ["903", "System error / database exception", "38", "500 Internal Server Error"],
         ["(none emitted)", "Failure with no ErrorCode", "7", "400 Bad Request"],
         ["(unparseable)", "Failure with malformed ErrorCode", "2", "400 Bad Request"]]))
    c.append(para(txt("Collapsed: 205 calls should be 4xx, 84 should be 5xx. None of the "
                      "289 is a legitimate 200.", "strong")))

    c.append(heading(2, "The platform is capable of correct status codes"))
    c.append(para(txt("During a replay pass that omitted the Content-Type header, six of "
                      "these same endpoints returned "),
                  txt("HTTP 415 Unsupported Media Type", "strong"),
                  txt(" - correctly. The stack returns an accurate status code for a "
                      "transport-level problem and 200 for an application-level failure. "
                      "Returning 200 here is an application-layer choice, not a framework "
                      "limitation.")))

    c.append(heading(2, "Two defects found inside the same responses"))
    c.append(heading(3, "1. Internal server detail leaked to the caller (11 responses)"))
    c.append(para(txt("Some failures return a full .NET stack trace including "
                      "build-server absolute paths, source file names, line numbers and "
                      "assembly versions - at HTTP 200, to any authenticated caller:")))
    c.append(codeblock(
        "902-SPC-GTDOS-System.IO.FileNotFoundException: Could not load file or assembly\n"
        "'ChilkatDotNet47, Version=9.5.0.86, Culture=neutral, "
        "PublicKeyToken=eb5fc1fc52ef09bd'\n"
        "   at EntityDataAccessLayer.ServiceDetails.DatabaseCrud."
        "GetTargetDeviceOpenSSHKey(...)\n"
        "   at ARCONPAMAPI.Controllers.ServicePassword.ServicePasswordController."
        "GetTargetDeviceOpenSSHKey(...)\n"
        "     in E:\\Jenkins\\workspace\\PAMAPI_QA\\ARCONPAMAPI\\ARCONPAMAPI\\Controllers"
        "\\ServicePassword\\ServicePasswordController.cs:line 148", "text"))
    c.append(para(txt("That one is also a genuine deployment fault - ChilkatDotNet47 is "
                      "missing from the QA server - and it is being reported as HTTP 200.")))

    c.append(heading(3, "2. The ErrorCode field is not machine-readable"))
    c.append(para(txt("104 distinct codes were observed against a documented register of "
                      "four. They are also not consistently formed - 26 occurrences across "
                      "15 distinct codes are malformed:")))
    c.append(table(["Format defect", "Occurrences", "Example"],
                   [["Missing separator after numeric prefix", "9", "201SDC-GSDBI"],
                    ["Stack trace concatenated into the code", "9", "902-LSC-GLSTL-System..."],
                    ["No ErrorCode emitted at all", "7", "null or empty string"],
                    ["Trailing separator", "3", "203-ACC-GAC-"],
                    ["Space inside the prefix separator", "2", "203 -ULC-GUL"],
                    ["No numeric prefix", "2", "GSAPLR, GLOBCD"],
                    ["Leading/trailing whitespace", "3", "902-RAC-GUS "]]))
    c.append(para(txt("Message text is unstable too: "),
                  code_inline("System error has occurred"),
                  txt(" and "),
                  code_inline("System error has occurred."),
                  txt(" are both emitted for the same condition. Because the contract "
                      "forces clients to string-match, that difference breaks them.")))

    c.append(heading(2, "Performance note"))
    c.append(para(txt("These are not fast rejections. Median latency 647 ms, p95 1,270 ms, "
                      "max 9,415 ms. The server performs the full unit of work, fails, and "
                      "then reports success.")))

    c.append(heading(2, "Scope"))
    c.append(para(txt("36 controllers. The ServiceDetails* and UserDetails* families "
                      "account for 208 of the 289 calls. Those controllers exist in up to "
                      "four versioned copies (V2/V3/V4) that behave identically, so a fix "
                      "applied where the envelope is serialised covers every version at "
                      "once.")))

    c.append(rule())
    c.append(heading(2, "Steps to reproduce"))
    c.append(panel("warning", para(
        txt("Token safety: generate ONE token and reuse it. Repeated /arcontoken requests "
            "lock the GenericScheduler service account, which is also the data-warehouse "
            "ETL account. That account is locked at the time of writing.", "strong"))))
    c.append(para(txt("Case A - read-only, no request body. Simplest reproduction.",
                      "strong")))
    c.append(codeblock(
        f"1. GET {api}/api/ServicePasswordV2/GetSyncFailedServices\n"
        "   Header: Authorization: Bearer <token>\n"
        "   Header: Content-Type: application/json\n\n"
        "2. Observe the HTTP status line.\n"
        "   EXPECTED: 404 Not Found (the server found no records)\n"
        "   ACTUAL:   200 OK\n\n"
        "3. Observe the response body:\n"
        '   { "Success": false, "ErrorCode": "204-SPC-GFSP",\n'
        '     "ErrorMessage": "No Record Found" }\n\n'
        "   The body says the call failed. The status line says it succeeded.", "text"))
    c.append(para(txt("Case B - validation failure.", "strong")))
    c.append(codeblock(
        f"4. POST {api}/api/ServiceCreation/SetServiceDetails\n"
        "   Header: Authorization: Bearer <token>\n"
        "   Header: Content-Type: application/json\n"
        '   Body:   { "LOBID": 108, "ServerGroupId": 282, "Hostname": "10.11.0.48",\n'
        '             "IPAddress": "10.11.0.48", "Domain": 2, "ServiceTypeId": 1,\n'
        '             "DBInstanceName": "", "ServiceUserName": "SVC40PC47" }\n'
        "           (Port deliberately omitted)\n\n"
        "5. EXPECTED: 400 Bad Request\n"
        "   ACTUAL:   200 OK with\n"
        '   { "Success": false, "ErrorCode": "201-SCC-SSDN",\n'
        '     "ErrorMessage": "Validation error occurred - Port is Mandatory" }', "text"))
    c.append(para(txt("Case C - server fault reported as success.", "strong")))
    c.append(codeblock(
        f"6. POST {api}/api/ServiceDetails/SetRDPSessionProcessLog\n"
        "   Header: Authorization: Bearer <token>\n"
        "   Header: Content-Type: application/json\n"
        '   Body:   { "ServiceSessionId": 56, "UserSessionId": 4, "ServiceID": 1,\n'
        '             "UserID": "AUTO40PC47", "ProcessName": "explorer",\n'
        '             "ProcessTitle": "Start menu", "ProcessLogType": "5",\n'
        '             "LogResponse": "Test", "LogNo": "1" }\n\n'
        "7. EXPECTED: 500 Internal Server Error\n"
        "   ACTUAL:   200 OK with\n"
        '   { "Success": false, "ErrorCode": "903-SDC-SPL",\n'
        '     "ErrorMessage": "System error has occurred" }', "text"))
    c.append(para(txt("Case D - internal detail leaked, also at 200.", "strong")))
    c.append(codeblock(
        f"8. POST {api}/api/ServicePassword/GetTargetDeviceOpenSSHKey\n"
        "   Header: Authorization: Bearer <token>\n"
        "   Header: Content-Type: application/json\n"
        "   Body:   {}\n\n"
        "9. EXPECTED: 500 Internal Server Error, exception detail in the server log only\n"
        "   ACTUAL:   200 OK, full .NET stack trace and the build-server path\n"
        "             E:\\Jenkins\\workspace\\PAMAPI_QA\\... returned in ErrorMessage",
        "text"))
    c.append(para(
        txt("All 289 occurrences, each with its request body, response, error code and a "
            "retained evidence file, are in the attached "),
        code_inline("EVIDENCE.xlsx"),
        txt(" (sheet \"Affected Calls\") and "),
        code_inline("EVIDENCE.md"),
        txt(" section 7. The \"Reproduction\" sheet gives one worked case per failure "
            "class.")))

    c.append(rule())
    c.append(heading(2, "Expected vs actual"))
    c.append(table(["", "Behaviour"], [
        ["EXPECTED", "The HTTP status line agrees with the outcome in the body - 4xx when "
                     "the client is at fault, 5xx when the server is at fault, 2xx only on "
                     "success."],
        ["ACTUAL", "HTTP 200 OK is returned for every application-level failure, with the "
                   "real outcome placed in a Success/ErrorCode/ErrorMessage envelope that "
                   "only a client parsing the body can see."],
    ]))

    c.append(heading(2, "Proposed fix"))
    c.append(table(["#", "Action", "Effort", "Effect"], [
        ["1", "At the point the envelope is serialised, map the ErrorCode prefix to an "
              "HTTP status using the table above", "Low - one place, one lookup",
         "Resolves all 289"],
        ["2", "Keep the existing envelope in the body unchanged", "None",
         "Backward compatible for clients already parsing it"],
        ["3", "Strip stack traces from ErrorMessage; return a stable code plus a safe "
              "message, log detail server-side", "Low", "Closes the disclosure"],
        ["4", "Publish the error-code register - code, meaning, emitting endpoints, "
              "corrective action", "Low", "Unblocks automated negative testing"],
        ["5", "Normalise code format; 26 occurrences across 15 codes are malformed",
         "Low", "Makes the field machine-readable"],
        ["6", "Install the missing ChilkatDotNet47 assembly on QA", "Low",
         "Separate defect; can be split out"],
    ]))
    c.append(panel("info", para(
        txt("Backward compatibility: ", "strong"),
        txt("step 1 changes status codes for existing clients. If any consumer already "
            "relies on receiving 200, the safe rollout is to gate step 1 behind a config "
            "flag or an x-pam-version header for one release, then flip the default. The "
            "envelope itself does not change either way, so a body-parsing client is "
            "unaffected."))))

    c.append(heading(2, "Acceptance criteria"))
    c.append(codeblock(
        "1. For every failing request, the HTTP status line reflects the failure class:\n"
        "   - ErrorCode prefix 1xx or 2xx  -> 4xx (400, or 404 for \"no record found\")\n"
        "   - ErrorCode prefix 9xx         -> 500\n"
        "   - Success: true                -> 2xx\n"
        "2. No response body contains a .NET stack trace, an exception type name, a\n"
        "   source file path, a source line number or an assembly version.\n"
        "3. Every ErrorCode matches a single documented format and appears in a\n"
        "   published register.\n"
        "4. Re-running the QA harness against the fixed build shows 0 calls with\n"
        "   (HTTP 200 AND Success:false).", "text"))

    c.append(heading(2, "Evidence attached"))
    c.append(table(["Attachment", "Contents"], [
        ["EVIDENCE.xlsx", "8 sheets - Summary, Taxonomy & Fix, all 289 Affected Calls, "
                          "Error Code Register, By Controller, Leaked Internals, "
                          "Reproduction, Re-validation"],
        ["EVIDENCE.md", "Full write-up including the complete per-occurrence register"],
        ["LH-01-...-evidence.zip", "The whole evidence pack including the machine-readable "
                                   "JSON extract and the live re-validation results"],
    ]))
    c.append(para(
        txt("Raw source responses (1,868 files, one per call, secrets redacted) are "
            "retained in the QA workspace at "),
        code_inline("artifacts/runs/2026-07-29_181439/evidence/"),
        txt(". Related existing analyses: ISSUE-001 (status-code contract), ISSUE-003 "
            "(contradictory envelope), ISSUE-009 (token lockout).")))

    return {"type": "doc", "version": 1, "content": c}


def build_payload(cfg: dict) -> dict:
    return {"fields": {
        "project": {"key": cfg["JIRA_PROJECT_KEY"]},
        "issuetype": {"id": IDS["issuetype_bug"]},
        "summary": SUMMARY,
        "description": build_description(cfg),
        "priority": {"name": "High"},
        "components": [{"name": "PAM API"}],
        "fixVersions": [{"id": IDS["fixversion_hf12"]}],
        "labels": ["api-contract", "http-status", "error-handling",
                   "qa-automation", "developer-loophole-01"],
        "customfield_10190": {"id": IDS["severity_sev1"]},        # Severity
        "customfield_10114": {"id": IDS["dept_automation"]},      # Dept Of Created By
        "customfield_10112": {"id": IDS["client_internal_arcon"]},  # Primary Client
        "customfield_10156": {"id": IDS["db_mssql"]},             # Database Type
        "customfield_11220": {"id": IDS["hosting_windows"]},      # Hosting Environment
        "customfield_10251": {"id": IDS["complexity_medium"]},    # Task Complexity
        # Validator-enforced. "No"/"None" on the regression fields is the accurate
        # answer, not a placeholder: this is long-standing designed behaviour, so
        # there is no earlier build in which it worked.
        "customfield_10092": [{"id": IDS["milestone_hf12"]}],     # Affected Milestone.
        "customfield_10115": {"id": IDS["os_all"]},               # End-User OS
        "customfield_11253": {"id": IDS["prev_working_no"]},      # Worked previously?
        "customfield_11254": {"id": IDS["prev_version_none"]},    # Previous working ver
        "customfield_10780": {"id": IDS["reopen_no"]},            # Is reopen from customer
        "customfield_10781": "NA",                                # Reopen Original Ticket ID
    }}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--create", action="store_true")
    args = ap.parse_args()
    if not (args.dry_run or args.create):
        ap.error("pass --dry-run or --create")

    cfg = load_env()
    payload = build_payload(cfg)

    for f in ATTACHMENTS:
        if not f.exists():
            raise SystemExit(f"attachment missing: {f}")
        if f.name in EXCLUDED_FROM_ATTACHMENTS:
            raise SystemExit(f"refusing to attach excluded file: {f.name}")

    if args.dry_run:
        print(json.dumps(payload, indent=1)[:3000])
        print(f"\n... description nodes: {len(payload['fields']['description']['content'])}")
        print("attachments:")
        for f in ATTACHMENTS:
            print(f"  {f.name}  ({f.stat().st_size / 1024:.0f} KB)")
        return 0

    j = Jira(cfg)
    status, res = j.post("/rest/api/3/issue", payload)
    if status not in (200, 201):
        print(f"CREATE FAILED (HTTP {status})")
        print(json.dumps(res, indent=1)[:2000])
        return 1
    key = res["key"]
    print(f"CREATED: {key}")
    print(f"  {cfg['JIRA_BASE_URL']}/browse/{key}")

    print("\nattaching evidence:")
    attached = []
    for f in ATTACHMENTS:
        st, ar = j.attach(key, f)
        ok = st in (200, 201)
        print(f"  [{'ok' if ok else 'FAIL ' + str(st)}] {f.name} "
              f"({f.stat().st_size / 1024:.0f} KB)")
        if ok:
            attached.extend(a["filename"] for a in ar)
        else:
            print("      ", str(ar)[:300])

    (HERE / "last-created-issue.json").write_text(json.dumps({
        "key": key, "url": f"{cfg['JIRA_BASE_URL']}/browse/{key}",
        "attachments": attached}, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
