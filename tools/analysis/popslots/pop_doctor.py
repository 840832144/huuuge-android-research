#!/usr/bin/env python3
"""Preflight check: can this machine collect Pop! Slots right now?

Answers "is the collector usable here?" without guessing: it walks the whole
chain (adb -> device -> game -> root channel -> frida-server -> symbol resolution)
and prints exactly which step is missing and what to do about it.

Usage:
  python pop_doctor.py                 # auto-detect the only connected device
  python pop_doctor.py --serial <serial> [--frida 127.0.0.1:27042]

Exit code 0 = the hook-based tools can run; 1 = something is missing (the report
says what).
"""
from __future__ import annotations

import argparse
import socket
import sys

import pop_common as pc

OK, BAD, WARN = "[ok]  ", "[MISS]", "[warn]"


def check_frida_reachable(addr: str) -> tuple[bool, str]:
    host, _, port = addr.rpartition(":")
    try:
        with socket.create_connection((host or "127.0.0.1", int(port)), timeout=3):
            return True, "frida-server is listening on {}".format(addr)
    except Exception as exc:
        return False, "nothing is listening on {} ({})".format(addr, exc)


def main() -> int:
    ap = pc.add_common_args(argparse.ArgumentParser(description=__doc__))
    args = ap.parse_args()

    print("Pop! Slots collector preflight\n" + "=" * 34)
    missing: list[str] = []
    hints: list[str] = []

    # 1. adb
    adb_exe = pc.adb_path(args.adb)
    from pathlib import Path
    if Path(adb_exe).exists():
        print("{} adb: {}".format(OK, adb_exe))
    else:
        print("{} adb not found (looked at --adb, $ADB, PATH, platform-tools)".format(BAD))
        missing.append("adb")
        hints.append("Install platform-tools or pass --adb <path to adb>.")
        print("\nverdict: not usable yet")
        return 1

    # 2. device
    try:
        serial = pc.resolve_serial(args.serial, args.adb)
        print("{} device: {}".format(OK, serial))
    except SystemExit as exc:
        print("{} no usable device: {}".format(BAD, exc))
        missing.append("device")
        hints.append("Start the research instance, or pass --serial.")
        print("\nverdict: not usable yet")
        return 1

    abi = pc.adb_shell(serial, "getprop ro.product.cpu.abi", adb_exe=args.adb, timeout=30)
    print("{} abi: {}".format(OK if abi else WARN, abi or "(unknown)"))
    if abi and "x86_64" not in abi:
        hints.append("This instance reports '{}' - get a frida-server build for that ABI.".format(abi))

    # 3. game installed / running
    apk = ""
    for line in pc.adb_shell(serial, "pm path {}".format(args.package), adb_exe=args.adb).splitlines():
        if line.startswith("package:"):
            apk = line.split("package:", 1)[1].strip()
            break
    if apk:
        print("{} game installed: {}".format(OK, apk))
    else:
        print("{} {} is not installed on this instance".format(BAD, args.package))
        missing.append("game")
        hints.append("Install Pop! Slots on the research instance.")

    pid = pc.resolve_pid(serial, args.package, args.adb, args.pid)
    if pid:
        print("{} game running: pid {}".format(OK, pid))
    else:
        print("{} game not running (Hooks need a live process)".format(WARN))
        hints.append("Launch Pop! Slots and leave it in the lobby.")

    # 4. root channel
    mode = pc.root_mode(serial, args.adb)
    if mode == "adbd":
        print("{} root: adbd (shell is already uid 0; no su binary needed)".format(OK))
    elif mode == "su":
        print("{} root: su binary".format(OK))
    else:
        print("{} root: neither adbd-root nor su works".format(BAD))
        missing.append("root")
        hints.append("Run `adb -s {} root`, or enable root for the instance.".format(serial))

    # 5. frida-server
    ok, detail = check_frida_reachable(args.frida)
    if ok:
        print("{} {}".format(OK, detail))
    else:
        print("{} {}".format(BAD, detail))
        missing.append("frida-server")
        hints.append("Push and run frida-server on the instance (see "
                     "artifacts/popslots/ENVIRONMENT_LOCK.md), then forward the port: "
                     "adb -s {} forward tcp:{} tcp:27042".format(serial, args.frida.rsplit(":", 1)[-1]))

    # 6. end-to-end: can we attach and resolve the engine symbols?
    if ok and pid:
        try:
            device = pc.frida_device(args.frida)
            session = pc.attach(device, pid, args.package)
            probe = session.create_script(
                "'use strict';\n"
                "const m = Process.findModuleByName({mod!r});\n"
                "send({{ module: !!m, base: m ? m.base.toString() : null }});\n"
                "if (m) {{ let n = 0; m.enumerateExports().forEach(function (e) {{ n++; }}); send({{ exports: n }}); }}\n"
                .format(mod=pc.MODULE_NAME))
            got: dict = {}
            probe.on("message", lambda m, d: got.update(m.get("payload", {})))
            probe.load()
            import time
            for _ in range(30):
                if got:
                    break
                time.sleep(0.2)
            if got.get("module"):
                print("{} attach ok; {} loaded (base {}, {} exports)".format(
                    OK, pc.MODULE_NAME, got.get("base"), got.get("exports")))
            else:
                print("{} attached but {} is not loaded yet".format(WARN, pc.MODULE_NAME))
                hints.append("Wait until the lobby is up, then re-run.")
            try:
                session.detach()
            except Exception:
                pass
        except SystemExit as exc:
            print("{} attach failed: {}".format(BAD, exc))
            missing.append("attach")
        except Exception as exc:
            print("{} attach failed: {}".format(BAD, exc))
            missing.append("attach")
    elif ok:
        print("{} skipped the attach probe (game not running)".format(WARN))
    else:
        print("{} skipped the attach probe (frida-server unreachable)".format(WARN))

    # verdict
    print("\n" + "=" * 34)
    if not missing:
        print("verdict: READY - run e.g. `python pop_syms.py --serial {}`".format(serial))
        if hints:
            print("notes:")
            for h in hints:
                print("  - " + h)
        return 0
    print("verdict: NOT READY (missing: {})".format(", ".join(sorted(set(missing)))))
    for h in hints:
        print("  - " + h)
    return 1


if __name__ == "__main__":
    sys.exit(main())
