#!/usr/bin/env python3
"""Pop! Slots: capture MULTIPLE parseUserData calls to sample many lobby
users. Analyze: are names/IDs/countries diverse (real players) or repeated/
patterned (bots)? The decisive statistical check."""
import frida
import json
import time
import re
import pathlib

dev = frida.get_device_manager().add_remote_device("127.0.0.1:27044")
s = dev.attach(15177)

PARSE = 0x7a1c8aa92e90
OUT = pathlib.Path(r"C:\bigfish_research\toptycoon\pop_users.jsonl")

src = r'''
'use strict';
const parse = ptr(0x7a1c8aa92e90);
let n = 0;
Interceptor.attach(parse, {
  onEnter(args) { this.model = args[1]; n++; },
  onLeave(retval) {
    const m = this.model;
    if (!m || m.isNull()) return;
    let ascii = '';
    try { const b = new Uint8Array(m.readByteArray(220)); for(let i=0;i<b.length;i++){ ascii += (b[i]>=32&&b[i]<=126)?String.fromCharCode(b[i]):'.'; } } catch(e){}
    send({ kind:'u', n, ascii });
  }
});
send({ kind:'ready' });
'''
script = s.create_script(src)
def onmsg(mm, d):
    p = mm.get('payload', {})
    if p.get('kind') == 'ready':
        print("sample-hook ready — walk/refresh lobby to gather many users", flush=True)
    elif p.get('kind') == 'u':
        with OUT.open('a', encoding='utf-8') as f:
            f.write(json.dumps({"n": p.get('n'), "ascii": p.get('ascii')}, ensure_ascii=False) + "\n")
        print("[u{}] {}".format(p.get('n'), p.get('ascii')[:120]), flush=True)
script.on('message', onmsg)
script.load()
print("running 40s (try to trigger many user loads)", flush=True)
time.sleep(40)
print("DONE", flush=True)
try: s.detach()
except: pass
