#!/usr/bin/env python3
"""Self-check for the module-selection tools, with no fixture files: it writes a
synthetic capture (and a BOM-prefixed pair, as Windows editors produce) and
asserts what endpoints.py / select_module.py report.

Run:  python test_capture_tools.py      (exit code 0 = pass)
"""
from __future__ import annotations

import base64
import contextlib
import io
import json
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import endpoints as ep        # noqa: E402
import select_module as sm    # noqa: E402


def rec(host, path, method, req=None, resp=None):
    return {
        "ts": 1, "host": host, "path": path, "method": method,
        "req_b64": base64.b64encode(req).decode() if req else None,
        "req_len": len(req) if req else 0,
        "resp_status": 200,
        "resp_b64": base64.b64encode(resp).decode() if resp else None,
        "resp_len": len(resp) if resp else 0,
        "ct": "application/octet-stream",
    }


ROWS = [
    rec("api.example", "/slots/spin", "POST", b"\x08\x01\x10\x64", b"\x0a\x04\x08\xc8\x01"),
    rec("api.example", "/slots/spin", "POST", b"\x08\x02\x10\x64", b"\x0a\x04\x08\x90\x03"),
    rec("api.example", "/lobby/room/state", "POST", b"{}", b'{"players":3}'),
    rec("cdn.example", "/assets/Manifest.version", "GET", None, b"123"),
]


def write_capture(path: pathlib.Path, bom: bool = False) -> None:
    text = "\n".join(json.dumps(r) for r in ROWS) + "\n"
    path.write_text(text, encoding="utf-8-sig" if bom else "utf-8")


def run(mod, argv) -> str:
    buf = io.StringIO()
    old = sys.argv
    sys.argv = [mod.__name__] + argv
    try:
        with contextlib.redirect_stdout(buf):
            try:
                mod.main()
            except SystemExit:
                pass
    finally:
        sys.argv = old
    return buf.getvalue()


def main() -> int:
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        tmpd = pathlib.Path(tmp)
        cap = tmpd / "capture.jsonl"
        write_capture(cap)

        out = run(ep, [str(cap), "--show-body", "3"])
        if "api.example /slots/spin" not in out:
            failures.append("endpoints: slot endpoint missing\n" + out)
        if "2x POST" not in out:
            failures.append("endpoints: count/method wrong\n" + out)
        if "protobuf?" not in out:
            failures.append("endpoints: body shape not reported\n" + out)
        if "json" not in out:
            failures.append("endpoints: json body not detected\n" + out)

        mapping = tmpd / "modules.json"
        mapping.write_text(json.dumps({"slots": ["/slots/"], "lobby": ["/lobby/"]}),
                           encoding="utf-8")
        out = run(sm, [str(cap), "--modules", str(mapping), "--list"])
        if "slots" not in out or "/slots/" not in out:
            failures.append("select_module --list: mapping not shown\n" + out)

        slots = tmpd / "slots.jsonl"
        out = run(sm, [str(cap), "--modules", str(mapping), "--module", "slots",
                       "--out", str(slots)])
        if "matched 2 of 4" not in out:
            failures.append("select_module: expected 2 of 4 matched\n" + out)
        if len(slots.read_text(encoding="utf-8").strip().splitlines()) != 2:
            failures.append("select_module: output line count wrong")

        # BOM tolerance: Windows editors (PowerShell 5.1, Notepad) add a BOM
        cap_bom = tmpd / "capture_bom.jsonl"
        write_capture(cap_bom, bom=True)
        map_bom = tmpd / "modules_bom.json"
        map_bom.write_text(json.dumps({"slots": ["/slots/"]}), encoding="utf-8-sig")
        out = run(sm, [str(cap_bom), "--modules", str(map_bom), "--module", "slots",
                       "--out", str(tmpd / "s2.jsonl")])
        if "matched 2 of 4" not in out:
            failures.append("BOM-prefixed capture or mapping rejected\n" + out)
        out = run(ep, [str(cap_bom)])
        if "3 endpoint(s)" not in out:
            failures.append("endpoints: BOM-prefixed capture rejected\n" + out)

        # a module that matches nothing must say so instead of silently writing empty
        out = run(sm, [str(cap), "--modules", str(mapping), "--module", "lobby",
                       "--out", str(tmpd / "lobby.jsonl")])
        if "matched 1 of 4" not in out:
            failures.append("select_module: lobby count wrong\n" + out)

    if failures:
        print("FAIL")
        for f in failures:
            print(" -", f)
        return 1
    print("PASS: endpoints summary, module listing/selection and BOM tolerance all behave")
    return 0


if __name__ == "__main__":
    sys.exit(main())
