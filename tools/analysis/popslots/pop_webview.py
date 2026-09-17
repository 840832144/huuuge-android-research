#!/usr/bin/env python3
"""Decide whether the lobby/characters are rendered by a WebView (JS/HTML5) or
by the native Shaker engine: looks at WebView storage, the APK's web assets and
which processes/net handles exist.

Note: the APK path is resolved with ``pm path`` because it contains a per-install
hash that changes on every install.

Usage:
  python pop_webview.py --serial <serial>
"""
from __future__ import annotations

import argparse

import pop_common as pc


def main() -> None:
    ap = pc.add_common_args(argparse.ArgumentParser(description=__doc__))
    ap.add_argument("--head", type=int, default=20, help="lines per section")
    args = ap.parse_args()

    pkg = args.package
    data_dir = "/data/data/{}".format(pkg)

    apk_path = ""
    for line in pc.adb_shell(args.serial, "pm path {}".format(pkg), adb_exe=args.adb).splitlines():
        if line.startswith("package:"):
            apk_path = line.split("package:", 1)[1].strip()
            break
    print("apk:", apk_path or "(not found — is the game installed on this instance?)")

    print("\n== webview storage ==")
    print(pc.adb_su(args.serial,
                    "ls -R {} 2>/dev/null | head -{}".format(data_dir + "/app_webview", args.head * 2),
                    adb_exe=args.adb) or "(no app_webview directory)")

    print("\n== web-ish files under app data ==")
    print(pc.adb_su(args.serial,
                    "find {} -type f 2>/dev/null | grep -iE 'webview|cache|http' | head -{}".format(
                        data_dir, args.head),
                    adb_exe=args.adb) or "(none)")

    if apk_path:
        print("\n== web assets inside the APK ==")
        print(pc.adb_su(args.serial,
                        "unzip -l {} 2>/dev/null | grep -iE '\\.js$|\\.html$|assets/' | head -{}".format(
                            apk_path, args.head),
                        adb_exe=args.adb) or "(none)")

    pid = pc.resolve_pid(args.serial, pkg, args.adb, args.pid)
    print("\npid:", pid)
    if pid:
        print("== tcp handles (look for non-80/443 / websockets) ==")
        print(pc.adb_su(args.serial,
                        "cat /proc/{}/net/tcp 2>/dev/null | awk 'NR>1{{print $2,$3,$4}}' | head -{}".format(
                            pid, args.head),
                        adb_exe=args.adb) or "(no data)")

    print("\n== webview / chrome processes ==")
    print(pc.adb_shell(args.serial,
                       "ps -A | grep -iE 'popslot|webview|chrome|sandbox'",
                       adb_exe=args.adb) or "(none)")


if __name__ == "__main__":
    main()
