#!/usr/bin/env python3
"""create_b01.py — raise ticket B1 of the repository-size issue set.

B1 = "Binary artifacts committed to version control", grouping findings F01, F02,
F03, F07 and F13 from `artifacts/repo-issues/`.

Evidence source is the OBJ-014 investigation, not an LH pack — the measurements come
from `git verify-pack -v` over both packfiles, so every size quoted here is the real
on-disk compressed byte count, not an uncompressed logical size.

    python tools/jira/create_b01.py --dry-run   # build and print the payload, create nothing
    python tools/jira/create_b01.py --create    # create the issue and attach evidence

⛔ The ticket draft (`B1-JIRA-TICKET.md`) is never attached to its own ticket.
"""
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from jira_client import Jira, load_env                                   # noqa: E402
from create_lh01 import (heading, para, txt, code_inline, codeblock,     # noqa: E402
                         table, bullets, panel, rule)

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
# OBJ-025 split this pack: the authored half is a document, the evidence is an
# artifact. Both are attached, so both roots are named.
PACK = ROOT / "docs" / "findings" / "repository"
PACK_EVIDENCE = ROOT / "artifacts" / "repo-issues"
ZIP = HERE / ".tmp" / "B1-repo-binary-artifacts-evidence.zip"
EXCLUDED_FROM_ATTACHMENTS = {"B1-JIRA-TICKET.md", "JIRA-TICKET.md"}
ATTACHMENTS = [PACK / "findings.csv", PACK / "README.md", ZIP]

IDS = {
    "issuetype_bug": "10009",
    "severity_sev1": "12936",
    "dept_automation": "13273",
    "client_internal_arcon": "11183",
    "hosting_windows": "22093",
    "complexity_large": "14248",
    "fixversion_hf12": "17321",
    "milestone_hf12": "21486",
    "os_all": "12766",
    "prev_working_no": "22131",
    "prev_version_none": "22194",
    "reopen_no": "18854",
    "component_scm": "10376",
    "db_mssql": "11188",
}

SUMMARY = ("Binary artifacts committed to version control — pam repository is 35.57 GB, "
           "with 73.3% of history from three third-party ZIP files")


def build_description(cfg: dict) -> dict:
    c = []

    c.append(panel("error", para(
        txt("The pam repository is ", ), txt("35.57 GB", "strong"),
        txt(". Of that, "), txt("27.88 GB (78.4%) is .git history", "strong"),
        txt(" — held in only 107 files. A single third-party file, "),
        code_inline("ARCONDbeaver.zip"),
        txt(", accounts for "), txt("41.1% of the entire repository", "strong"),
        txt(". All C# product source across 30,888 versions is "),
        txt("0.8%", "strong"), txt("."))))

    c.append(heading(2, "What we observed"))
    c.append(para(txt(
        "Large third-party binary archives were committed to git and then re-committed "
        "dozens of times. Because a ZIP is already DEFLATE-compressed, git cannot "
        "delta-compress it — each re-commit stores a complete fresh copy, permanently.")))
    c.append(para(txt(
        "This is not a checkout problem. Deleting the files today reclaims nothing, "
        "because git retains every version ever committed.")))

    c.append(heading(2, "Size attribution — measured on disk"))
    c.append(para(txt("All figures below are "), txt("real compressed packfile bytes", "strong"),
                  txt(" from "), code_inline("git verify-pack -v"),
                  txt(", covering both packs (26.790 + 1.074 = 27.864 GiB).")))
    c.append(table(
        ["Content", "On-disk", "Share of pack", "Versions stored"],
        [[".zip archives", "21.579 GiB", "80.6%", "262"],
         [".msi installers", "1.850 GiB", "6.9%", "112"],
         [".exe binaries", "1.230 GiB", "4.6%", "490"],
         [".deb / .pkg / .rpm", "0.817 GiB", "3.0%", "5"],
         [".dll libraries", "0.413 GiB", "1.5%", "1,690"],
         [".nupkg packages", "0.273 GiB", "1.0%", "170"],
         ["All C# source (.cs)", "0.204 GiB", "0.8%", "30,888"]]))
    c.append(para(txt("Binary artifacts are "), txt("98.1% of the packfile", "strong"),
                  txt(". Product source is 0.8%.")))

    c.append(heading(3, "Three files are 73.3% of the repository"))
    c.append(table(
        ["File", "Versions", "On-disk", "Share", "What it is"],
        [["ARCONDbeaver.zip", "50", "11.45 GiB", "41.1%", "DBeaver — open-source DB client"],
         ["multitab.zip", "48", "4.589 GiB", "16.5%", "MultiTab client installer"],
         ["dbeaver.zip", "36", "4.388 GiB", "15.8%", "DBeaver again, second copy"]]))
    c.append(panel("warning", para(
        txt("Two of the three are "), txt("DBeaver", "strong"),
        txt(", a third-party open-source download that was never ARCON source code."))))

    c.append(heading(3, "Why these cannot be compressed — measured, not theory"))
    c.append(para(txt("Git stores an object either as a delta against a similar object, or whole. "),
                  code_inline("git verify-pack -v"),
                  txt(" reports which. For "), code_inline("ARCONDbeaver.zip"), txt(":")))
    c.append(codeblock("versions in the main pack   : 47\n"
                       "stored WHOLE (no delta base) : 44      <- 93.6%\n"
                       "stored as a delta            :  3", "text"))
    c.append(para(txt("44 of 47 versions are stored in full — an average of "),
                  txt("229 MB of permanent storage per commit of that one file", "strong"),
                  txt(". This is also why "), code_inline("git gc"),
                  txt(" cannot help: there is no redundancy left to exploit.")))

    c.append(heading(2, "It is still growing"))
    c.append(para(txt("A routine 106-commit fast-forward pull on 2026-08-10, changing 142 files, "
                      "created a 1.074 GiB packfile. Attributing that pack object-by-object:")))
    c.append(table(
        ["Content", "On-disk", "Share of the pull"],
        [["ARCONDbeaver.zip — 3 new versions", "0.954 GiB", "88.8%"],
         ["SSHLogsConsumerBotInstaller.msi", "0.034 GiB", "3.1%"],
         ["graph.json (tooling output)", "0.032 GiB", "3.0%"],
         ["All C# source in the pull", "0.008 GiB", "0.7%"]]))
    c.append(para(txt("One file was 88.8% of a routine update, and "),
                  txt("none of those three ZIP versions is in HEAD", "strong"),
                  txt(" — they arrived on branches most developers never check out.")))

    c.append(heading(2, "Related findings grouped into this ticket"))
    c.append(table(
        ["Ref", "Finding", "Measured"],
        [["F01", "Three third-party ZIP archives dominate history", "20.43 GiB / 73.3%"],
         ["F02", "All .zip content across the repository", "21.58 GiB / 80.6%"],
         ["F03", "Installer packages committed as source (.msi/.exe/.deb/.rpm/.pkg)", "3.90 GiB"],
         ["F07", "PAM/AllSupportingDLLs — vendored dependency tree", "18.02 GiB logical, 734 versions"],
         ["F13", "Generated tooling output committed on a branch (graphify-out, syftSbomTable.json)", "0.15 GiB logical"]]))

    c.append(rule())
    c.append(heading(2, "Steps to reproduce"))
    c.append(panel("info", para(
        txt("Preconditions: a full clone of "), code_inline("root/pam.git"),
        txt(" and git 2.20+. Every command below is "), txt("read-only", "strong"),
        txt(" — none modifies the repository."))))
    c.append(para(txt("1. Confirm the split between history and checkout:")))
    c.append(codeblock("git count-objects -vH\n"
                       "#  in-pack: 210471 · packs: 2 · size-pack: 27.87 GiB\n"
                       "#  loose: 0 · garbage: 0 · prune-packable: 0", "bash"))
    c.append(para(txt("2. Attribute the packfile by actual on-disk size:")))
    c.append(codeblock("git verify-pack -v .git/objects/pack/pack-<sha>.idx > verifypack.txt\n"
                       "git rev-list --objects --all \\\n"
                       "  | git cat-file --batch-check='%(objecttype) %(objectname) "
                       "%(objectsize) %(rest)' > objsizes.txt\n"
                       "# join on SHA, aggregate column 4 of verifypack.txt by file extension",
                       "bash"))
    c.append(para(txt("3. Confirm the archives are stored whole rather than as deltas — "
                      "objects with only 5 fields have no delta base:")))
    c.append(codeblock("awk '$2==\"blob\" && NF<7' verifypack.txt | wc -l", "bash"))
    c.append(para(txt("4. Confirm the largest files are still tracked in HEAD:")))
    c.append(codeblock("git ls-tree -r -l HEAD | awk -F'\\t' '{print $1}' | sort -k4 -rn | head",
                       "bash"))
    c.append(panel("note", para(
        txt("Parse "), code_inline("git ls-tree -l"), txt(" on the "), txt("tab", "strong"),
        txt(" before the path, not on whitespace — many paths here contain spaces "),
        txt("(e.g. \"ARCON PAM.msi\"), and whitespace splitting silently truncates them."))))

    c.append(heading(2, "Expected vs actual"))
    c.append(table(
        ["", "Behaviour"],
        [["Expected", "A source repository stores source. Third-party downloads, installers and "
                      "build outputs are distributed through an artifact store or release page, "
                      "so repository size tracks the size of the code."],
         ["Actual", "Binary artifacts are 98.1% of the packfile and product source is 0.8%. "
                    "One third-party archive is 41.1% of the repository. A routine 106-commit "
                    "update transferred 1.074 GiB, 88.8% of it a single file."]]))

    c.append(heading(2, "Severity justification"))
    c.append(table(
        ["Dimension", "Assessment"],
        [["Scope", "Every developer and every CI agent that clones the repository"],
         ["Current cost", "27.88 GB transferred and stored per full clone; 35.57 GB on disk per checkout"],
         ["Trend", "Growing ~1 GB per routine update; 35,602 commits since 2021-07-01"],
         ["Comparator", "The sibling QA automation repository is 131 MB — this repository is 271x larger"],
         ["Reversibility", "Worsens permanently with every commit; reclamation requires a coordinated "
                           "history rewrite, and the cost of that rewrite grows over time"],
         ["Data loss risk", "None — this is a size and process defect, not a correctness defect"]]))
    c.append(para(txt("Rated "), txt("Sev-1 / High", "strong"),
                  txt(". Not ShowStopper: it does not gate the release, and it has been "
                      "accumulating across many releases.")))

    c.append(heading(2, "Proposed fix"))
    c.append(para(txt("There is a lever here that avoids the hard problem entirely. "),
                  txt("Item 1 needs no server change, no history rewrite and no coordination", "strong"),
                  txt(" — it can be adopted today and delivers most of the benefit.")))
    c.append(table(
        ["#", "Action", "Effect", "Risk"],
        [["1", "Adopt blobless clone as the standard: "
               "git clone --filter=blob:none <url>",
          "Since 98.1% of history is binaries almost nobody needs, this avoids nearly all "
          "of the 27.88 GB transfer while keeping full history", "None — reversible, client-side only"],
         ["2", "Use --depth 1 for CI jobs that do not need history",
          "CI stops paying the clone cost on every run", "Low"],
         ["3", "Stop the inflow: remove artifacts from tracking with git rm --cached and "
               "fetch them at build time instead",
          "Repository stops growing; history unchanged", "Low — build scripts must fetch instead"],
         ["4", "Add a server-side pre-receive hook rejecting files over ~10 MB",
          "Prevents recurrence — the only durable fix", "Low"],
         ["5", "Purge archives and installers from history with git filter-repo",
          "26.79 GiB -> approximately 1.3 GiB, a ~95% reduction", "HIGH — rewrites every commit SHA"]]))
    c.append(panel("warning", para(
        txt("Item 5 is a "), txt("destructive history rewrite", "strong"),
        txt(". Every SHA changes, so every clone must be re-made, every open merge request "
            "rebased, every tag re-signed and every pinned CI SHA updated. It should be a "
            "planned maintenance event with a scheduled freeze, never done opportunistically. "
            "Rehearse on a clone first."))))
    c.append(para(txt("Backward compatibility: items 1-4 change nothing about the repository's "
                      "contents or history, so existing clones, branches and tags keep working "
                      "unchanged. Only item 5 breaks compatibility.")))
    c.append(panel("note", para(
        txt("What will NOT work: "), code_inline("git gc"), txt(" and "),
        code_inline("git repack"), txt(" reclaim essentially nothing here. "),
        code_inline("git count-objects -vH"),
        txt(" reports loose: 0, garbage: 0, prune-packable: 0, and 3,326 remote branches keep "
            "every object reachable. There is also no Git LFS and no .gitattributes anywhere "
            "in the repository."))))

    c.append(heading(2, "Acceptance criteria"))
    c.append(bullets([
        "A documented clone command using --filter=blob:none is published to the development "
        "team, and a fresh blobless clone completes transferring materially less than 27.88 GB.",
        "No new file over 10 MB can be pushed to the repository — verified by attempting one "
        "against the pre-receive hook.",
        "Third-party archives (DBeaver, MultiTab) and installers are no longer added in new "
        "commits; the build fetches them from an artifact store instead.",
        "git count-objects -vH on a fresh clone shows the size-pack figure has stopped growing "
        "between releases.",
        "If item 5 is executed: pack size is measurably reduced, and every active branch and tag "
        "has been re-pointed, with all developers notified to re-clone.",
    ]))
    c.append(para(txt("QA verification: re-run the attribution commands in Steps to reproduce and "
                      "confirm the .zip share of the packfile has fallen, and that "),
                  code_inline("git ls-tree -r -l HEAD"),
                  txt(" no longer lists archives over 100 MB.")))

    c.append(heading(2, "Evidence and provenance"))
    c.append(table(
        ["Item", "Detail"],
        [["Repository", "root/pam.git, branch 35.8.29_Hotfix, commit 12234f037"],
         ["Measured", "Working tree clean at time of measurement; no modification made"],
         ["Method", "git verify-pack -v (on-disk compressed bytes) joined to "
                    "git rev-list --objects --all for paths"],
         ["Attached", "README.md — full findings document with all 16 findings; "
                      "findings.csv — machine-readable table; evidence .zip — raw command captures"],
         ["Scope of this ticket", "Findings F01, F02, F03, F07, F13 of the repository-size set"]]))
    c.append(panel("info", para(
        txt("Re-validation position: "), txt("all figures are freshly measured", "strong"),
        txt(" from the repository at commit 12234f037 during this investigation — they are not "
            "quoted from an earlier report. No repository-modifying command was run at any "
            "point; the analysis is entirely read-only and reproducible with the commands above."))))
    c.append(para(txt("Related: the remaining repository-size findings (checkout duplication, "
                      "prevention controls, and the partial-clone rollout) are grouped into "
                      "separate tickets and are not covered here.")))

    return {"type": "doc", "version": 1, "content": c}


def build_payload(cfg: dict) -> dict:
    return {"fields": {
        "project": {"key": cfg["JIRA_PROJECT_KEY"]},
        "issuetype": {"id": IDS["issuetype_bug"]},
        "summary": SUMMARY,
        "description": build_description(cfg),
        "priority": {"name": "High"},
        "components": [{"id": IDS["component_scm"]}],
        "fixVersions": [{"id": IDS["fixversion_hf12"]}],
        "labels": ["repository-size", "binary-artifacts", "source-control",
                   "qa-automation", "repo-finding-B1"],
        "customfield_10190": {"id": IDS["severity_sev1"]},
        "customfield_10114": {"id": IDS["dept_automation"]},
        "customfield_10112": {"id": IDS["client_internal_arcon"]},
        "customfield_11220": {"id": IDS["hosting_windows"]},
        "customfield_10251": {"id": IDS["complexity_large"]},
        # ⚠️ Validator-enforced, and NOT reported by createmeta as required — a create
        # without it returns HTTP 400 "Field Database Type is required." It carries no
        # meaning for a source-control defect; MSSQL is set only to satisfy the screen.
        # This is a 7th enforced field beyond the 6 recorded in tools/jira/jira.md §3.2.
        "customfield_10156": {"id": IDS["db_mssql"]},
        # Validator-enforced beyond what createmeta reports. "No"/"None" is the accurate
        # answer here: the repository has grown continuously since 2021, so there is no
        # earlier build in which this behaved differently.
        "customfield_10092": [{"id": IDS["milestone_hf12"]}],
        "customfield_10115": {"id": IDS["os_all"]},
        "customfield_11253": {"id": IDS["prev_working_no"]},
        "customfield_11254": {"id": IDS["prev_version_none"]},
        "customfield_10780": {"id": IDS["reopen_no"]},
        "customfield_10781": "NA",
    }}


def build_zip() -> Path:
    """Zip the evidence pack. Excludes the ticket draft — attaching a ticket's own
    draft to that ticket is circular. Enforced here AND in the attach loop."""
    ZIP.parent.mkdir(parents=True, exist_ok=True)
    if ZIP.exists():
        ZIP.unlink()
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted([*PACK.rglob("*"), *PACK_EVIDENCE.rglob("*")]):
            if not f.is_file():
                continue
            if f.name in EXCLUDED_FROM_ATTACHMENTS:
                continue
            if f.resolve() == ZIP.resolve():
                continue
            base = PACK if PACK in f.parents else PACK_EVIDENCE
            z.write(f, f.relative_to(base).as_posix())
    with zipfile.ZipFile(ZIP) as z:
        names = z.namelist()
        assert not any("JIRA-TICKET" in n for n in names), \
            f"ticket draft leaked into the evidence zip: {names}"
    return ZIP


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--create", action="store_true")
    a = ap.parse_args()
    if not (a.dry_run or a.create):
        ap.error("pass --dry-run or --create")

    cfg = load_env()
    payload = build_payload(cfg)
    build_zip()

    for f in ATTACHMENTS:
        if not f.exists():
            raise SystemExit(f"attachment missing: {f}")
        if f.name in EXCLUDED_FROM_ATTACHMENTS:
            raise SystemExit(f"refusing to attach excluded file: {f.name}")

    if a.dry_run:
        fields = payload["fields"]
        print(json.dumps({k: v for k, v in fields.items() if k != "description"},
                         indent=1, ensure_ascii=False))
        print(f"\nsummary       : {fields['summary']}")
        print(f"description   : {len(fields['description']['content'])} ADF nodes")
        print("attachments:")
        for f in ATTACHMENTS:
            print(f"  {f.name:52} {f.stat().st_size/1024:8.0f} KB")
        with zipfile.ZipFile(ZIP) as z:
            print(f"  zip contains {len(z.namelist())} files, ticket draft excluded")
        return 0

    j = Jira(cfg)
    status, res = j.post("/rest/api/3/issue", payload)
    if status not in (200, 201):
        print(f"CREATE FAILED  HTTP {status}")
        print(json.dumps(res, indent=1)[:2500])
        return 1
    key = res["key"]
    url = f"{cfg['JIRA_BASE_URL']}/browse/{key}"
    print(f"created: {key}   {url}")

    for f in ATTACHMENTS:
        st, ar = j.attach(key, f)
        ok = "ok" if st in (200, 201) else f"FAILED {st}"
        print(f"  attach {f.name:52} {ok}")

    (HERE / "last-created-issue.json").write_text(json.dumps(
        {"key": key, "url": url, "summary": SUMMARY,
         "attachments": [f.name for f in ATTACHMENTS]}, indent=1), encoding="utf-8")
    print(f"\n{key}  {url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
