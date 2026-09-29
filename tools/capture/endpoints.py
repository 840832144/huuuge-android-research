#!/usr/bin/env python3
"""List the endpoints present in a capture, so an operator can see what exists
and then decide which module(s) to collect.

Reads the JSONL written by tools/capture/mitm_addon.py (host/path/method and
base64 bodies) and prints a summary, optionally with a peek at the body shape so
you can tell JSON from protobuf from opaque binary without decoding anything.

Usage:
  python endpoints.py [capture.jsonl] [--host api.example.com] [--grep slots]
                      [--show-body 3] [--json out.json]
"""
from __future__ import annotations

import argparse
import base64
import collections
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



def load(path: pathlib.Path):
    # utf-8-sig so a capture re-saved by a Windows editor (BOM) still parses
    with path.open(encoding="utf-8-sig") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except Exception:
                continue


def body_shape(b64: str | None) -> str:
    """Best-effort description of a body's shape (no decoding of the meaning)."""
    if not b64:
        return "-"
    try:
        raw = base64.b64decode(b64)
    except Exception:
        return "?"
    if not raw:
        return "empty"
    head = raw[:1]
    if head in (b"{", b"["):
        return "json"
    if head == b"\x1f" or raw[:2] == b"\x1f\x8b":
        return "gzip"
    if raw[:2] in (b"H4", b"\x1f\x8b"):
        return "gzip-b64"
    if len(raw) >= 2 and raw[0] in (0x08, 0x0A, 0x12, 0x1A, 0x22, 0x32):
        return "protobuf?"
    if all(32 <= c < 127 for c in raw[:16]):
        return "text"
    return "binary"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("capture", nargs="?", default=os.environ.get("MITM_IN", "mitm_b64.jsonl"),
                    help="capture JSONL (default: $MITM_IN or mitm_b64.jsonl)")
    ap.add_argument("--host", default="", help="only endpoints whose host contains this")
    ap.add_argument("--grep", default="", help="only endpoints whose path matches this regex")
    ap.add_argument("--show-body", type=int, default=0,
                    help="also show the body shape for the first N endpoints")
    ap.add_argument("--json", default="", help="write the summary as JSON to this path")
    args = ap.parse_args()

    path = pathlib.Path(args.capture)
    if not path.exists():
        print("capture not found:", path, file=sys.stderr)
        return 1

    host_re = re.compile(re.escape(args.host)) if args.host else None
    path_re = re.compile(args.grep) if args.grep else None

    counts = collections.Counter()
    methods = collections.defaultdict(collections.Counter)
    shapes = {}
    for rec in load(path):
        host, p = rec.get("host", ""), rec.get("path", "")
        if host_re and not host_re.search(host):
            continue
        if path_re and not path_re.search(p):
            continue
        key = (host, p)
        counts[key] += 1
        methods[key][rec.get("method")] += 1
        if key not in shapes:
            shapes[key] = (body_shape(rec.get("req_b64")), body_shape(rec.get("resp_b64")))

    if not counts:
        print("no endpoints matched")
        return 0

    width = max(len("{} {}".format(h, p)) for h, p in counts)
    print("{} endpoint(s):\n".format(len(counts)))
    for (host, p), n in counts.most_common():
        meth = ",".join(sorted(m for m in methods[(host, p)] if m))
        line = "{} {}".format(host, p)
        extra = ""
        if args.show_body:
            req_shape, resp_shape = shapes[(host, p)]
            extra = "   [req:{}/resp:{}]".format(req_shape, resp_shape)
        print("  {:<{w}}  {:>4}x {}{}".format(line, n, meth, extra, w=width))

    if args.json:
        out = [{"host": h, "path": p, "count": c,
                "methods": sorted(m for m in methods[(h, p)] if m),
                "req_shape": shapes[(h, p)][0], "resp_shape": shapes[(h, p)][1]}
               for (h, p), c in counts.most_common()]
        pathlib.Path(args.json).write_text(json.dumps(out, ensure_ascii=False, indent=1),
                                          encoding="utf-8")
        print("\nwrote:", args.json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
