#!/usr/bin/env python3
"""Continuous variant of pop_parse.py — keeps sampling server-delivered lobby
users until Ctrl+C (``--seconds 0``).

Same implementation and the same method limitation as pop_parse.py (the user
record is a fuzzy ASCII dump of a byte window, not a field mapping).

Usage:
  python pop_users_sampler.py --serial 127.0.0.1:5565 --outdir .
"""
from __future__ import annotations

import sys

import pop_parse

if __name__ == "__main__":
    if not any(a == "--seconds" or a.startswith("--seconds=") for a in sys.argv[1:]):
        sys.argv += ["--seconds", "0"]
    pop_parse.main()
