#!/usr/bin/env python3
"""Self-check for pop_common's adb plumbing, guarding the failure mode reported
from another machine: a subprocess decode failure leaves stdout as None and the
real error gets masked by "can only concatenate str (not NoneType) to str".

It also asserts that adb output is decoded as UTF-8 rather than through the
console code page, which is what caused that failure on a localised Windows.

Run:  python test_pop_common.py      (exit code 0 = pass)
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pop_common as pc  # noqa: E402


class _Fake:
    def __init__(self, stdout, stderr):
        self.stdout = stdout
        self.stderr = stderr


def main() -> int:
    failures = []
    calls: list[dict] = []
    original = subprocess.run

    def fake(cmd, **kwargs):
        calls.append({"cmd": cmd, "kwargs": kwargs})
        # simulate exactly what a crashed reader thread leaves behind
        return _Fake(None, "adb: device 'emulator-5562' not found")

    subprocess.run = fake
    try:
        pc._SERIAL_CACHE.clear()
        pc._SERIAL_CACHE["auto"] = "127.0.0.1:5555"      # keep resolve_serial offline
        try:
            out = pc.adb("127.0.0.1:5555", "shell", "getprop", "ro.product.cpu.abi", adb_exe="adb")
        except Exception as exc:
            failures.append("adb() raised {} instead of returning the stderr text".format(
                type(exc).__name__ + ": " + str(exc)))
            out = ""
        if "not found" not in (out or ""):
            failures.append("adb() lost the real error text: {!r}".format(out))
        if calls:
            kwargs = calls[-1]["kwargs"]
            if kwargs.get("encoding") != "utf-8":
                failures.append("adb() does not decode as UTF-8 (encoding={!r})".format(
                    kwargs.get("encoding")))
            if kwargs.get("errors") != "replace":
                failures.append("adb() does not tolerate undecodable bytes (errors={!r})".format(
                    kwargs.get("errors")))
            if not kwargs.get("text"):
                failures.append("adb() no longer requests text output")
    finally:
        subprocess.run = original
        pc._SERIAL_CACHE.pop("auto", None)

    if failures:
        print("FAIL")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS: adb() survives a None stdout, keeps the real error, decodes as UTF-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
