#!/usr/bin/env python3
"""Search every loaded module for TLS/network symbols (SSL_write, SSL_read,
BIO_write, send/recv, ...) to find which library actually carries the game's
traffic. For Pop! Slots the answer is the engine itself: libBigCasino.so embeds
its own TLS, so hooking the system libssl.so does not capture anything.

Usage:
  python pop_net_syms.py --serial 127.0.0.1:5565
"""
from __future__ import annotations

import argparse
import json
import time

import pop_common as pc

BODY = r"""
const mods = Process.enumerateModules();
send({ kind: 'modules', n: mods.length });
const hitRe = __HITRE__;
const netHits = {};
mods.forEach(function (m) {
  let exps = [];
  try { exps = m.enumerateExports(); } catch (e) { return; }
  exps.forEach(function (e) {
    if (hitRe.test(e.name)) {
      if (!netHits[m.name]) netHits[m.name] = [];
      netHits[m.name].push(e.name + '=' + e.address);
    }
  });
});
send({ kind: 'net', hits: netHits });
const libRe = /ssl|crypto|curl|okhttp|socket|http|net/i;
send({ kind: 'libs', names: mods.filter(function (m) { return libRe.test(m.name); }).map(function (m) { return m.name; }) });
"""


def main() -> None:
    ap = pc.add_common_args(argparse.ArgumentParser(description=__doc__))
    ap.add_argument("--pattern",
                    default="SSL_write|SSL_read|ssl_write|BIO_write|BIO_read|send|recv|WSAsend|ssl3_write",
                    help="regex over export names")
    ap.add_argument("--outfile", default="", help="optional JSON output file inside --outdir")
    args = ap.parse_args()

    pid = pc.resolve_pid(args.serial, args.package, args.adb, args.pid)
    print("pid:", pid)
    device = pc.frida_device(args.frida)
    session = pc.attach(device, pid, args.package)

    src = ("'use strict';\n"
           + BODY.replace("__HITRE__", json.dumps(args.pattern)))
    script = session.create_script(src)
    out_file = pc.out_path(args.outdir, args.outfile) if args.outfile else None

    def on_message(message, data):
        payload = message.get("payload", {})
        kind = payload.get("kind")
        if kind == "modules":
            print("loaded modules:", payload.get("n"), flush=True)
        elif kind == "net":
            hits = payload.get("hits", {})
            if not hits:
                print("no TLS/network symbols matched in any module", flush=True)
            for mod, entries in hits.items():
                print("{}:".format(mod), flush=True)
                for e in entries[:25]:
                    print("  " + e, flush=True)
            if out_file is not None:
                out_file.write_text(json.dumps(hits, ensure_ascii=False, indent=1), encoding="utf-8")
                print("wrote:", out_file, flush=True)
        elif kind == "libs":
            print("crypto/net-ish modules:", ", ".join(payload.get("names", [])), flush=True)

    script.on("message", on_message)
    script.load()
    time.sleep(3)
    try:
        session.detach()
    except Exception:
        pass


if __name__ == "__main__":
    main()
