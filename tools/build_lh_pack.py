#!/usr/bin/env python3
"""Build the artifacts/loopholes evidence packs.

    python tools/build_lh_pack.py --list
    python tools/build_lh_pack.py --lh 02
    python tools/build_lh_pack.py --all
    $env:PAM_API_TOKEN = "<bearer>"
    python tools/build_lh_pack.py --all --revalidate

Deny-by-default: a bare run issues zero HTTP calls. `--revalidate` is required, and even
then a spec may refuse - LH-08 stops the IIS application pool and is never replayed.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lh_common import PACKS, build_pack                                  # noqa: E402
from lh_specs_obj010 import OBJ010_SPECS                                 # noqa: E402
from lh_specs_run import RUN_SPECS                                       # noqa: E402
from lh_specs_static import STATIC_SPECS                                 # noqa: E402

SPECS = {s.num: s
         for s in sorted(RUN_SPECS + STATIC_SPECS + OBJ010_SPECS, key=lambda s: s.num)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lh", action="append", metavar="NN",
                    help="loophole number, e.g. 02. Repeatable")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--revalidate", action="store_true",
                    help="replay against the live environment where the spec permits")
    args = ap.parse_args()

    if args.list:
        print(f"{'LH':<5} {'severity':<12} {'replay':<10} title")
        for num, s in SPECS.items():
            print(f"{num:<5} {s.severity.split(' ')[-1]:<12} "
                  f"{s.revalidate:<10} {s.title}")
        return 0

    if args.all:
        chosen = list(SPECS.values())
    elif args.lh:
        chosen = []
        for n in args.lh:
            n = n.zfill(2)
            if n not in SPECS:
                raise SystemExit(f"unknown loophole {n}; --list shows what is available")
            chosen.append(SPECS[n])
    else:
        ap.error("pass --lh NN, --all, or --list")

    built = []
    for spec in chosen:
        built.append((spec, build_pack(spec, do_replay=args.revalidate)))

    print(f"\n{'=' * 74}\nSummary\n{'=' * 74}")
    print(f"{'LH':<5} {'occurrences':>12} {'endpoints':>10} {'replay':>26}  title")
    for spec, payload in built:
        rv = payload.get("revalidation") or {}
        if rv.get("ok") and rv.get("attempted", 0) == 0:
            state = f"all {rv.get('withheld_by_guard', 0)} withheld"
        elif rv.get("ok"):
            state = f"{rv['reproduced']}/{rv['attempted']} reproduce"
            if rv.get("withheld_by_guard"):
                state += f" (+{rv['withheld_by_guard']} withheld)"
        elif rv.get("refused"):
            state = "FORBIDDEN - not replayed"
        elif rv.get("static"):
            state = "static - n/a"
        else:
            state = "not run"
        print(f"{spec.num:<5} {payload['occurrences']:>12} "
              f"{payload['distinct_endpoints']:>10} {state:>26}  {spec.title[:40]}")
    print(f"\npacks under {PACKS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
