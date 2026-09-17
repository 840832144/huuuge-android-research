#!/usr/bin/env python3
"""Hook CShakerServerUserDataParser::parseUserData to inspect each lobby user
the server delivers (id / name / country / state / numeric value).

Method note — limitation: the CRoomUserModel object is read as a fixed-size byte
window and the printable ASCII is extracted. That is a **fuzzy dump, not a field
mapping**: it is enough to see identity strings and values and to tell filler
records from real-looking ones, but it does **not** yield structured field
definitions. Do not describe its output as parsed fields.

Usage:
  python pop_parse.py --serial <serial> --outdir . --seconds 60
"""
from __future__ import annotations

import argparse
import json
import time

import pop_common as pc

BODY = r"""
const parse = POP_SYMS['parse_user_data'];
if (!parse) {
  send({ kind: 'no-symbol', name: 'parse_user_data' });
} else {
  let n = 0;
  Interceptor.attach(parse, {
    onEnter(args) { this.model = args[1]; n++; },
    onLeave(retval) {
      const mm = this.model;
      if (!mm || mm.isNull()) return;
      let ascii = '';
      try {
        const b = new Uint8Array(mm.readByteArray(__WINDOW__));
        for (let i = 0; i < b.length; i++) {
          ascii += (b[i] >= 32 && b[i] <= 126) ? String.fromCharCode(b[i]) : '.';
        }
      } catch (e) {}
      send({ kind: 'user', n: n, ascii: ascii });
    }
  });
  send({ kind: 'ready' });
}
"""


def main() -> None:
    ap = pc.add_common_args(argparse.ArgumentParser(description=__doc__))
    ap.add_argument("--seconds", type=float, default=60.0, help="how long to listen")
    ap.add_argument("--window", type=int, default=220,
                    help="bytes to dump from CRoomUserModel (default: %(default)s)")
    ap.add_argument("--outfile", default="pop_users.jsonl",
                    help="output file name inside --outdir")
    args = ap.parse_args()

    pid = pc.resolve_pid(args.serial, args.package, args.adb, args.pid)
    print("pid:", pid)
    device = pc.frida_device(args.frida)
    session = pc.attach(device, pid, args.package)
    out = pc.out_path(args.outdir, args.outfile)
    print("writing:", out)

    src = ("'use strict';\n" + pc.js_symbol_prelude()
           + BODY.replace("__WINDOW__", str(args.window)))
    script = session.create_script(src)
    count = 0

    def on_message(message, data):
        nonlocal count
        payload = message.get("payload", {})
        kind = payload.get("kind")
        if kind == "symbols":
            print("[symbols] base={} found={} missing={}".format(
                payload.get("base"), payload.get("found"), payload.get("missing")), flush=True)
        elif kind == "no-module":
            print("[!] module not loaded:", payload.get("module"), flush=True)
        elif kind == "no-symbol":
            print("[!] symbol not found:", payload.get("name"),
                  "- this game build's mangled name differs", flush=True)
        elif kind == "ready":
            print("hook ready — play/navigate the lobby to trigger user loads", flush=True)
        elif kind == "user":
            count += 1
            with out.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps({"n": payload.get("n"), "ascii": payload.get("ascii")},
                                    ensure_ascii=False) + "\n")
            print("[user {}] {}".format(count, (payload.get("ascii") or "")[:110]), flush=True)

    script.on("message", on_message)
    script.load()
    try:
        if args.seconds and args.seconds > 0:
            time.sleep(args.seconds)
        else:
            while True:          # --seconds 0 = keep sampling until Ctrl+C
                time.sleep(0.3)
    except KeyboardInterrupt:
        pass
    print("total users captured:", count)
    try:
        session.detach()
    except Exception:
        pass


if __name__ == "__main__":
    main()
