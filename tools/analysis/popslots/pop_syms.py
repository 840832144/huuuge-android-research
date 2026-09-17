#!/usr/bin/env python3
"""Enumerate libBigCasino.so exports filtered for the lobby/social system
(lobby, player, character, room, join, avatar, session, social, friend,
presence, bot). This is the entry point for finding the room/user and avatar
behaviour symbols.

Usage:
  python pop_syms.py --serial 127.0.0.1:5565
  python pop_syms.py --serial 127.0.0.1:5565 --filter "ActivityHandler" --outdir .
"""
from __future__ import annotations

import argparse
import json
import time

import pop_common as pc

DEFAULT_FILTER = ("lobby|player|character|room|join|avatar|session|social|friend"
                  "|presence|bot|seat|sit|walk|stand|activity")

BODY = r"""
const m = Process.findModuleByName(__MODULE__);
if (!m) {
  send({ kind: 'no-module' });
} else {
  send({ kind: 'module', base: m.base.toString(), size: m.size });
  const re = new RegExp(__FILTER__, 'i');
  const hits = [];
  try {
    m.enumerateExports().forEach(function (e) {
      if (re.test(e.name)) hits.push(e.name + '=' + e.address);
    });
  } catch (e) {}
  send({ kind: 'hits', n: hits.length, hits: hits });
}
"""


def main() -> None:
    ap = pc.add_common_args(argparse.ArgumentParser(description=__doc__))
    ap.add_argument("--filter", default=DEFAULT_FILTER, help="regex over export names")
    ap.add_argument("--limit", type=int, default=400, help="max hits printed")
    ap.add_argument("--outfile", default="", help="optional JSON output file inside --outdir")
    args = ap.parse_args()

    pid = pc.resolve_pid(args.serial, args.package, args.adb, args.pid)
    print("pid:", pid)
    device = pc.frida_device(args.frida)
    session = pc.attach(device, pid, args.package)

    src = ("'use strict';\n"
           + BODY.replace("__MODULE__", json.dumps(pc.MODULE_NAME))
                 .replace("__FILTER__", json.dumps(args.filter)))
    script = session.create_script(src)
    out_file = pc.out_path(args.outdir, args.outfile) if args.outfile else None
    collected = []

    def on_message(message, data):
        payload = message.get("payload", {})
        kind = payload.get("kind")
        if kind == "module":
            print("module base={} size={}".format(payload.get("base"), payload.get("size")), flush=True)
        elif kind == "no-module":
            print("[!] {} not loaded - is the game running?".format(pc.MODULE_NAME), flush=True)
        elif kind == "hits":
            total = payload.get("n", 0)
            hits = payload.get("hits", [])
            print("matched exports: {}".format(total), flush=True)
            for h in hits[:args.limit]:
                print("  " + h, flush=True)
            collected.extend(hits)
            if out_file is not None:
                out_file.write_text(json.dumps({"filter": args.filter, "exports": hits},
                                               ensure_ascii=False, indent=1), encoding="utf-8")
                print("wrote:", out_file, flush=True)

    script.on("message", on_message)
    script.load()
    time.sleep(4)
    try:
        session.detach()
    except Exception:
        pass


if __name__ == "__main__":
    main()
