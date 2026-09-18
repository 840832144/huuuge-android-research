#!/usr/bin/env python3
"""Select one module out of an existing capture, so the operator chooses what to
collect instead of having the tool decide.

The capture itself is module-agnostic (tools/capture/mitm_addon.py records
everything). A module is defined by a small JSON mapping of name -> list of
regexes matched against "host/path". Because endpoint naming differs per game,
the intended workflow is:

  1. capture broadly
  2. python endpoints.py capture.jsonl --show-body 3     # see what exists
  3. write/extend modules.json with the patterns you decide
  4. python select_module.py capture.jsonl --module slots --out slots.jsonl

Usage:
  python select_module.py [capture.jsonl] --module slots [--modules modules.json]
                          [--out slots.jsonl] [--list]
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys

# Windows consoles default to a legacy code page; reconfigure before anything is
# printed, otherwise argparse's --help (and any early output) can fail to encode.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass


DEFAULT_MAP = os.environ.get("MODULE_MAP", "modules.json")


def load_modules(path: pathlib.Path) -> dict:
    if not path.exists():
        return {}
    # utf-8-sig: a mapping edited on Windows (PowerShell, Notepad, VS Code "UTF-8
    # with BOM") starts with a BOM that plain utf-8 decoding rejects.
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise SystemExit("{} must be an object of name -> [regex, ...]".format(path))
    return data


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("capture", nargs="?", default=os.environ.get("MITM_IN", "mitm_b64.jsonl"))
    ap.add_argument("--module", default="", help="module name from the mapping")
    ap.add_argument("--modules", default=DEFAULT_MAP, help="mapping file (default: %(default)s)")
    ap.add_argument("--out", default="", help="write matching records here (JSONL)")
    ap.add_argument("--list", action="store_true", help="list the defined modules and exit")
    args = ap.parse_args()

    mapping = load_modules(pathlib.Path(args.modules))
    if args.list or not args.module:
        if not mapping:
            print("no mapping found at {} - create one, e.g.\n"
                  '  {{"slots": ["/slots/", "spin"], "lobby": ["room", "avatar"]}}'.format(args.modules))
            return 0
        print("modules in {}:".format(args.modules))
        for name, pats in mapping.items():
            print("  {:<16} {}".format(name, ", ".join(pats)))
        return 0

    if args.module not in mapping:
        raise SystemExit("module {!r} is not defined in {} (use --list to see what is)".format(
            args.module, args.modules))
    patterns = [re.compile(p) for p in mapping[args.module]]

    capture = pathlib.Path(args.capture)
    if not capture.exists():
        raise SystemExit("capture not found: {}".format(capture))

    out_path = pathlib.Path(args.out) if args.out else pathlib.Path(
        "{}.{}.jsonl".format(capture.stem, args.module))
    matched = total = 0
    hosts: dict[str, int] = {}
    with capture.open(encoding="utf-8-sig") as src, out_path.open("w", encoding="utf-8") as dst:
        for line in src:
            line = line.strip()
            if not line:
                continue
            total += 1
            try:
                rec = json.loads(line)
            except Exception:
                continue
            key = "{} {}".format(rec.get("host", ""), rec.get("path", ""))
            if any(p.search(key) for p in patterns):
                dst.write(json.dumps(rec, ensure_ascii=False) + "\n")
                matched += 1
                hosts[rec.get("host", "?")] = hosts.get(rec.get("host", "?"), 0) + 1

    print("module {!r}: matched {} of {} records -> {}".format(
        args.module, matched, total, out_path))
    for host, n in sorted(hosts.items(), key=lambda kv: -kv[1]):
        print("  {} x{}".format(host, n))
    if matched == 0:
        print("nothing matched - check the patterns against `python endpoints.py {}`".format(capture))
    return 0


if __name__ == "__main__":
    sys.exit(main())
