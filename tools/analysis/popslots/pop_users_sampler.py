#!/usr/bin/env python3
"""Continuous variant of pop_parse.py — keeps sampling server-delivered lobby
users until Ctrl+C (``--seconds 0``).

Same implementation and the same method limitation as pop_parse.py (the user
record is a fuzzy ASCII dump of a byte window, not a field mapping).

Usage:
  python pop_users_sampler.py --serial <serial> --outdir .
"""
from __future__ import annotations

import sys

# Windows consoles default to a legacy code page; reconfigure before anything is
# printed, otherwise argparse's --help (and any early output) can fail to encode.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass


import pop_parse

if __name__ == "__main__":
    if not any(a == "--seconds" or a.startswith("--seconds=") for a in sys.argv[1:]):
        sys.argv += ["--seconds", "0"]
    pop_parse.main()
