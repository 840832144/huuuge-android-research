#!/usr/bin/env python3
"""Screenshot the instance and print a few engine/process facts (foreground
activity, whether the game loads any Lua/JS runtime, whether the Shaker engine
library is mapped). Handy first step when you land on an unknown build.

Usage:
  python pop_shot.py --serial 127.0.0.1:5565 --outdir .
  python pop_shot.py --serial 127.0.0.1:5565 --outdir . --name lobby.png
"""
from __future__ import annotations

import argparse
import base64

import pop_common as pc


def main() -> None:
    ap = pc.add_common_args(argparse.ArgumentParser(description=__doc__))
    ap.add_argument("--name", default="pop_shot.png", help="screenshot file name inside --outdir")
    args = ap.parse_args()

    pid = pc.resolve_pid(args.serial, args.package, args.adb, args.pid)
    print("pid:", pid)
    print("== foreground ==")
    print(pc.adb_shell(args.serial, "dumpsys window | grep mCurrentFocus",
                       adb_exe=args.adb) or "(no match)")

    if pid:
        print("== script runtimes in this process (lua / js) ==")
        print(pc.adb_su(args.serial,
                        "cat /proc/{}/maps 2>/dev/null | grep -iE 'lua|\\.js|jsc|v8' | head -5".format(pid),
                        adb_exe=args.adb) or "(none — pure native engine)")
        print("== engine library mapping ==")
        print(pc.adb_su(args.serial,
                        "cat /proc/{}/maps 2>/dev/null | grep -i {} | head -3".format(pid, pc.MODULE_NAME),
                        adb_exe=args.adb) or "(not mapped yet)")

    raw = pc.adb_shell(args.serial, "screencap -p | base64 -w0", adb_exe=args.adb, timeout=90)
    try:
        data = base64.b64decode(raw)
        target = pc.out_path(args.outdir, args.name)
        target.write_bytes(data)
        print("screenshot: {} bytes -> {}".format(len(data), target))
    except Exception as exc:
        print("screenshot failed:", exc)


if __name__ == "__main__":
    main()
