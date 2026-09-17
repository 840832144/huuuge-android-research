#!/usr/bin/env python3
"""Hook the avatar behaviour state machine to quantify how the lobby stays busy
(stop-walking / arrived-to-sit / stand events), so the "stand -> walk -> sit ->
play/celebrate" cycle can be measured rather than assumed.

Symbols are resolved by name at attach time (ASLR-safe) — no addresses here.

Usage:
  python pop_behaviour.py --serial 127.0.0.1:5565 --outdir . --seconds 60
"""
from __future__ import annotations

import argparse
import json
import time

import pop_common as pc

TARGETS = ["avatar_stop_walking", "avatar_arrived_to_sit", "avatar_get_name", "avatar_stand_event"]

BODY = r"""
const targetKeys = __TARGETS__;
const resolved = {};
const installed = {};
let n = 0;
targetKeys.forEach(function (k) {
  const a = POP_SYMS[k];
  if (!a) return;
  resolved[k] = a.toString();
  try {
    Interceptor.attach(a, {
      onEnter(args) { n++; send({ kind: 'ev', ev: k, n: n }); }
    });
    installed[k] = true;
  } catch (e) {
    send({ kind: 'attach-error', ev: k, error: String(e) });
  }
});
send({ kind: 'installed', resolved: resolved, installed: Object.keys(installed) });
send({ kind: 'ready' });
"""


def main() -> None:
    ap = pc.add_common_args(argparse.ArgumentParser(description=__doc__))
    ap.add_argument("--seconds", type=float, default=60.0,
                    help="how long to listen (0 = until Ctrl+C)")
    ap.add_argument("--outfile", default="behaviour.jsonl",
                    help="output file name inside --outdir")
    args = ap.parse_args()

    pid = pc.resolve_pid(args.serial, args.package, args.adb, args.pid)
    print("pid:", pid)
    device = pc.frida_device(args.frida)
    session = pc.attach(device, pid, args.package)
    out = pc.out_path(args.outdir, args.outfile)
    print("writing:", out)

    src = ("'use strict';\n" + pc.js_symbol_prelude()
           + BODY.replace("__TARGETS__", json.dumps(TARGETS)))
    script = session.create_script(src)
    counts: dict[str, int] = {}

    def on_message(message, data):
        payload = message.get("payload", {})
        kind = payload.get("kind")
        if kind == "symbols":
            print("[symbols] base={} found={} missing={}".format(
                payload.get("base"), payload.get("found"), payload.get("missing")), flush=True)
        elif kind == "no-module":
            print("[!] module not loaded - is the game running?", flush=True)
        elif kind == "installed":
            print("[installed] {}".format(json.dumps(payload.get("installed"), ensure_ascii=False)),
                  flush=True)
        elif kind == "attach-error":
            print("[!] attach failed for", payload.get("ev"), payload.get("error"), flush=True)
        elif kind == "ready":
            print("behaviour hook ready — walk around / sit at machines", flush=True)
        elif kind == "ev":
            ev = payload.get("ev")
            counts[ev] = counts.get(ev, 0) + 1
            with out.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps({"ev": ev, "n": payload.get("n")}, ensure_ascii=False) + "\n")
            print("[{}] total={}".format(ev, counts[ev]), flush=True)

    script.on("message", on_message)
    script.load()
    try:
        if args.seconds and args.seconds > 0:
            time.sleep(args.seconds)
        else:
            while True:
                time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    print("event totals:", json.dumps(counts, ensure_ascii=False))
    try:
        session.detach()
    except Exception:
        pass


if __name__ == "__main__":
    main()
