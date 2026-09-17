#!/usr/bin/env python3
"""Process/UI state snapshot for the instance: resumed activity, PID, thread
count (a rising count usually means the engine is still loading), window tokens
and the tail of the game's own logcat.

Usage:
  python pop_state.py --serial <serial>
"""
from __future__ import annotations

import argparse

import pop_common as pc


def main() -> None:
    ap = pc.add_common_args(argparse.ArgumentParser(description=__doc__))
    ap.add_argument("--loglines", type=int, default=15, help="logcat tail length")
    args = ap.parse_args()

    pid = pc.resolve_pid(args.serial, args.package, args.adb, args.pid)
    print("pid:", pid)

    print("== resumed activity ==")
    print(pc.adb_shell(args.serial,
                       "dumpsys activity activities | grep -iE 'ResumedActivity|{}'".format(args.package),
                       adb_exe=args.adb) or "(no match)")

    if pid:
        print("== thread count (engine loading if still climbing) ==")
        print(pc.adb_su(args.serial, "ls /proc/{}/task 2>/dev/null | wc -l".format(pid),
                        adb_exe=args.adb))
        print("== logcat tail for this pid ==")
        print(pc.adb_shell(args.serial,
                           "logcat -d --pid={} | tail -{}".format(pid, args.loglines),
                           adb_exe=args.adb, timeout=90) or "(no output)")

    print("== window tokens ==")
    print(pc.adb_shell(args.serial,
                       "dumpsys window windows | grep -iE '{}|Window #'".format(args.package),
                       adb_exe=args.adb, timeout=90) or "(no match)")


if __name__ == "__main__":
    main()
