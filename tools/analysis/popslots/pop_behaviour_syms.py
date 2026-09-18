#!/usr/bin/env python3
"""Behaviour-focused variant of pop_syms.py: enumerate the avatar
behaviour/activity handler symbols used to reconstruct the state machine
(activity handlers, walk, sit, stand, play, idle, seat, ...).

Usage:
  python pop_behaviour_syms.py --serial <serial>
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


import pop_syms

BEHAVIOUR_FILTER = ("ActivityHandler|Walk|Sit|Stand|Celebrate|Idle|Seat|Chair|Machine"
                    "|Slot|Play|AvatarState|Activity|Random|Lobby")

if __name__ == "__main__":
    if not any(a == "--filter" or a.startswith("--filter=") for a in sys.argv[1:]):
        sys.argv += ["--filter", BEHAVIOUR_FILTER]
    pop_syms.main()
