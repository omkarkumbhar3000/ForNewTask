#!/usr/bin/env python3
"""track_tickets.py — the daily PAMIT review: status, assignee, and what needs us.

⛔ READ-ONLY against Jira. GET requests only. This never transitions, comments on,
assigns, edits or creates an issue — a tracker that can mutate the board is a tracker
you cannot run unattended.

Two conditions make a ticket OUR action item, per the owner:

  1. status == "QA Testing"            -> ours, whoever it is assigned to.
                                          It needs QA verification and that is us.
  2. status == "Awaiting Response"
     AND assignee is Omkar Kumbhar     -> ours, because the response is owed by us.
                                          Awaiting Response on anyone else is THEIR
                                          action and is reported without a flag.

Both status strings are verified to exist in the PAMIT Bug workflow — a tracker that
matches on a status name that does not exist would silently never fire.

"Reaches QA Testing" is a transition, not a state, so the run compares against the
previous run's snapshot and marks changes as NEW. First run has no baseline, so
everything currently matching is reported as NEW once.

    python tools/jira/track_tickets.py              # the daily review
    python tools/jira/track_tickets.py --json       # machine-readable
    python tools/jira/track_tickets.py --no-state   # do not update the snapshot

Exit code: 0 = nothing needs us · 1 = action items present · 2 = a lookup failed.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jira_client import Jira, load_env                                   # noqa: E402

HERE = Path(__file__).resolve().parent
REGISTRY = HERE / "tracked-tickets.json"
STATE = HERE / ".tracking-state.json"

FIELDS = "status,assignee,summary,updated,priority,resolution"


def fetch(j: Jira, key: str) -> dict:
    s, i = j.get(f"/rest/api/3/issue/{key}?fields={FIELDS}")
    if s != 200:
        return {"key": key, "error": f"HTTP {s}"}
    f = i["fields"]
    a = f.get("assignee") or {}
    return {
        "key": i["key"],
        "status": f["status"]["name"],
        "category": f["status"]["statusCategory"]["name"],
        "assignee": a.get("displayName"),
        "assignee_id": a.get("accountId"),
        "priority": (f.get("priority") or {}).get("name"),
        "resolution": (f.get("resolution") or {}).get("name"),
        "updated": f["updated"][:10],
        "summary": f["summary"],
    }


def classify(row: dict, rules: dict, me_id: str | None) -> tuple[bool, str]:
    """Return (is_action_for_us, reason)."""
    st = row.get("status")
    if st == rules["qa_testing_status"]:
        return True, "in QA Testing — needs QA verification"
    if st == rules["awaiting_response_status"]:
        who = row.get("assignee") or ""
        mine = (me_id and row.get("assignee_id") == me_id) or \
               who.strip().lower() == rules["awaiting_response_assignee"].strip().lower()
        if mine:
            return True, f"Awaiting Response and assigned to {who} — we owe the reply"
        return False, f"Awaiting Response, but assigned to {who} — their action"
    return False, ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-state", action="store_true",
                    help="report without updating the snapshot")
    a = ap.parse_args()

    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    rules = reg["action_rules"]
    cfg = load_env()
    j = Jira(cfg)

    me_id = None
    s, me = j.myself()
    if s == 200:
        me_id = me.get("accountId")

    prev = {}
    if STATE.exists():
        try:
            prev = json.loads(STATE.read_text(encoding="utf-8")).get("tickets", {})
        except Exception:
            prev = {}

    raised, unraised, errors = [], [], []
    for t in reg["tickets"]:
        if not t.get("key"):
            unraised.append(t)
            continue
        row = fetch(j, t["key"])
        if "error" in row:
            errors.append({**t, **row})
            continue
        row |= {"group": t["group"], "programme": t["programme"],
                "covers": t["covers"], "note": t.get("note")}
        act, why = classify(row, rules, me_id)
        was = prev.get(row["key"], {})
        row |= {"action": act, "reason": why,
                "changed": was.get("status") != row["status"] if was else True,
                "previous_status": was.get("status")}
        raised.append(row)

    actions = [r for r in raised if r["action"]]

    if a.json:
        print(json.dumps({
            "checked_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "raised": raised, "unraised": unraised, "errors": errors,
            "action_items": actions}, indent=1, ensure_ascii=False))
    else:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        print("=" * 96)
        print(f"  PAMIT DAILY REVIEW — {now}")
        print("=" * 96)
        print(f"  {'Group':6} {'Ticket':13} {'Status':22} {'Assignee':24} Updated")
        print("  " + "-" * 92)
        for r in sorted(raised, key=lambda x: x["group"]):
            mark = "!!" if r["action"] else ("->" if r["changed"] else "  ")
            print(f"{mark}{r['group']:6} {r['key']:13} {r['status']:22} "
                  f"{(r['assignee'] or '(unassigned)'):24} {r['updated']}")
            if r["changed"] and r["previous_status"]:
                print(f"         changed: {r['previous_status']} -> {r['status']}")
        for t in sorted(unraised, key=lambda x: x["group"]):
            print(f"  {t['group']:6} {'—':13} {'Need to create a ticket':22} "
                  f"{'—':24} {', '.join(t['covers'])}")
        for e in errors:
            print(f"!!{e['group']:6} {e['key']:13} LOOKUP FAILED: {e['error']}")

        print("  " + "-" * 92)
        if actions:
            print(f"\n  ⚠️  {len(actions)} ACTION ITEM(S) FOR US:\n")
            for r in actions:
                new = " [NEW since last review]" if r["changed"] else ""
                print(f"    • {r['key']} ({r['group']}){new}")
                print(f"      {r['reason']}")
                print(f"      {r['summary'][:82]}")
                print(f"      https://arcon-tech-solution.atlassian.net/browse/{r['key']}\n")
        else:
            print("\n  ✅ Nothing needs us today.")
            for r in raised:
                if r["reason"]:
                    print(f"     note: {r['key']} — {r['reason']}")
        print(f"\n  {len(raised)} raised · {len(unraised)} awaiting creation · "
              f"{len(errors)} lookup error(s)")
        print("=" * 96)

    if not a.no_state:
        STATE.write_text(json.dumps({
            "checked_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "tickets": {r["key"]: {"status": r["status"], "assignee": r["assignee"]}
                        for r in raised}}, indent=1), encoding="utf-8")

    return 2 if errors else (1 if actions else 0)


if __name__ == "__main__":
    raise SystemExit(main())
