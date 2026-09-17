#!/usr/bin/env python3
"""Extract libBigCasino.so (the Shaker engine, which embeds the game's TLS) from
the installed APK and pull it to the host for static/symbol analysis.

The APK path is resolved with ``pm path`` because it contains a per-install hash.
The native ABI directory is discovered from the APK listing instead of assuming
one, so this also works on an arm64 build.

Usage:
  python pull_bigcasino.py --serial <serial> --outdir .
  python pull_bigcasino.py --serial <serial> --lib libs/libBigCasino.so
"""
from __future__ import annotations

import argparse
import pathlib

import pop_common as pc

LIB_NAME = "libBigCasino.so"
TMP = "/data/local/tmp/pop_extract"


def main() -> None:
    ap = pc.add_common_args(argparse.ArgumentParser(description=__doc__))
    ap.add_argument("--outdir", default=".", help="where to write the pulled library")
    ap.add_argument("--lib", default=LIB_NAME, help="library file name inside the APK")
    args = ap.parse_args()

    apk = ""
    for line in pc.adb_shell(args.serial, "pm path {}".format(args.package), adb_exe=args.adb).splitlines():
        if line.startswith("package:"):
            apk = line.split("package:", 1)[1].strip()
            break
    if not apk:
        raise SystemExit("APK not found for {} on {}. Is the game installed on this instance?".format(
            args.package, args.serial))
    print("apk:", apk)

    print("== locate the library inside the APK ==")
    listing = pc.adb_su(args.serial, "unzip -l '{}' 2>/dev/null | grep -i {}".format(apk, args.lib),
                        adb_exe=args.adb, timeout=90)
    print(listing or "(not found in the APK)")
    member = ""
    for line in listing.splitlines():
        parts = line.split()
        if parts and parts[-1].endswith(args.lib):
            member = parts[-1]
            break
    if not member:
        raise SystemExit("{} not found inside {}".format(args.lib, apk))

    print("== extract on device ==")
    print(pc.adb_su(args.serial,
                    "mkdir -p {tmp} && unzip -o '{apk}' '{member}' -d {tmp} >/dev/null 2>&1 "
                    "&& cp {tmp}/{member} {tmp}/{lib} && chmod 644 {tmp}/{lib} && ls -la {tmp}/{lib}".format(
                        tmp=TMP, apk=apk, member=member, lib=args.lib),
                    adb_exe=args.adb, timeout=180))

    target = pc.out_path(args.outdir, args.lib)
    print("== pull to host ==")
    print(pc.adb(args.serial, "pull", "{}/{}".format(TMP, args.lib), str(target),
                 adb_exe=args.adb, timeout=300))
    if target.exists():
        print("pulled:", target, target.stat().st_size, "bytes")


if __name__ == "__main__":
    main()
