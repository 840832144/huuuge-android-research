#!/usr/bin/env python3
"""Business-protocol reconnaissance: list the process's TCP endpoints (with
reverse DNS on the remote IPs) and the network-ish libraries it has mapped, so
you can see what the client actually talks to and with which TLS stack.

Usage:
  python pop_proto.py --serial <serial>
  python pop_proto.py --serial <serial> --hide-established
"""
from __future__ import annotations

import argparse
import socket

import pop_common as pc

STATE_ESTABLISHED = "01"
STATE_LISTEN = "0A"

# /proc/net/tcp remote port is hex: 01BB=443, 0050=80
PORT_NAMES = {"01BB": 443, "0050": 80}


def ip_of(hex_addr: str) -> str:
    """Convert a /proc/net/tcp little-endian hex address to dotted-quad."""
    raw = bytes.fromhex(hex_addr)
    return "{}.{}.{}.{}".format(raw[3], raw[2], raw[1], raw[0])


def main() -> None:
    ap = pc.add_common_args(argparse.ArgumentParser(description=__doc__))
    ap.add_argument("--hide-established", action="store_true",
                    help="only show non-established sockets")
    ap.add_argument("--no-dns", action="store_true", help="skip reverse DNS lookups")
    args = ap.parse_args()

    pid = pc.resolve_pid(args.serial, args.package, args.adb, args.pid)
    print("pid:", pid)
    if not pid:
        raise SystemExit("Game not running on this instance.")

    raw = pc.adb_su(args.serial, "cat /proc/{}/net/tcp 2>/dev/null".format(pid), adb_exe=args.adb)
    print("\n== tcp endpoints ==")
    remote_ips = []
    for line in raw.splitlines()[1:]:
        parts = line.split()
        if len(parts) < 4:
            continue
        local, rem, state = parts[1], parts[2], parts[3]
        if args.hide_established and state == STATE_ESTABLISHED:
            continue
        try:
            l_ip, l_port = local.split(":")
            r_ip, r_port = rem.split(":")
            rip = ip_of(r_ip)
            rport = int(r_port, 16)
            kind = "ESTABLISHED" if state == STATE_ESTABLISHED else (
                "LISTEN" if state == STATE_LISTEN else "state=" + state)
            print("  local :{} -> {}:{}  {}".format(int(l_port, 16), rip, rport, kind))
            if rport in (80, 443) and state == STATE_ESTABLISHED:
                remote_ips.append(rip)
        except Exception:
            continue

    if not args.no_dns:
        print("\n== reverse DNS on remote hosts ==")
        for ip in sorted(set(remote_ips)):
            try:
                print("  {} -> {}".format(ip, socket.gethostbyaddr(ip)[0]))
            except Exception:
                print("  {} -> (no PTR)".format(ip))

    print("\n== network-ish mapped libraries ==")
    maps = pc.adb_su(args.serial, "cat /proc/{}/maps 2>/dev/null".format(pid), adb_exe=args.adb)
    names = set()
    for line in maps.splitlines():
        if "/" not in line:
            continue
        path = line.rsplit(" ", 1)[-1].strip()
        base = path.rsplit("/", 1)[-1]
        if any(k in base.lower() for k in ("ssl", "crypto", "curl", "socket", "http", "nghttp", "cronet")):
            names.add(base)
    for n in sorted(names):
        print("  " + n)
    if not names:
        print("  (none found — the TLS stack is likely linked inside {}".format(pc.MODULE_NAME) + ")")


if __name__ == "__main__":
    main()
