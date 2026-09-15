#!/usr/bin/env python3
"""Adaptive parseUserData sampler: resolve the symbol by name (ASLR-safe),
attach to whatever Pop Slots PID is current. Capture many lobby users while
the user navigates rooms."""
import frida
import json
import time
import pathlib
import subprocess

ADB = "C:/platform-tools/adb.exe"
# find current popslots pid
r = subprocess.run([ADB, "-s", "127.0.0.1:5565", "shell", "ps", "-A", "|", "grep", "popslots"],
                   capture_output=True, text=True)
pid = None
for line in r.stdout.splitlines():
    if 'popslots' in line:
        parts = line.split()
        try: pid = int(parts[1]); break
        except: pass
print("pid:", pid)

dev = frida.get_device_manager().add_remote_device("127.0.0.1:27044")
s = dev.attach(pid)
OUT = pathlib.Path(r"C:\bigfish_research\toptycoon\pop_users.jsonl")

src = r'''
'use strict';
const m = Process.findModuleByName('libBigCasino.so');
function sym(n){ try { return m.getExportByName(n); } catch(e){ return null; } }
function findParse() {
  // CShakerServerUserDataParser::parseUserData — mangled symbol
  const names = ['_ZN27CShakerServerUserDataParser13parseUserDataEPvP14CRoomUserModel'];
  for (const n of names) { const a = sym(n); if (a) return a; }
  return null;
}
const parse = findParse();
send({ find: parse ? parse.toString() : null });
if (!parse) { send({ kind:'no-parse' }); }
else {
  let n = 0;
  Interceptor.attach(parse, {
    onEnter(args) { this.model = args[1]; n++; },
    onLeave(retval) {
      const mm = this.model; if (!mm || mm.isNull()) return;
      let ascii = '';
      try { const b = new Uint8Array(mm.readByteArray(220)); for(let i=0;i<b.length;i++) ascii += (b[i]>=32&&b[i]<=126)?String.fromCharCode(b[i]):'.'; } catch(e){}
      send({ kind:'u', n, ascii });
    }
  });
  send({ kind:'ready' });
}
'''
script = s.create_script(src)
def onmsg(mm, d):
    p = mm.get('payload', {})
    if p.get('kind') == 'ready':
        print("sampler ready — navigate rooms/refresh lobby", flush=True)
    elif p.get('kind') == 'u':
        with OUT.open('a', encoding='utf-8') as f:
            f.write(json.dumps({"n": p.get('n'), "ascii": p.get('ascii')}, ensure_ascii=False) + "\n")
        print("[u{}] {}".format(p.get('n'), p.get('ascii')[:110]), flush=True)
    elif p.get('kind') == 'no-parse':
        print("parseUserData symbol NOT found", flush=True)
    elif p.get('kind') == 'find':
        print("parse address:", p.get('find'), flush=True)
script.on('message', onmsg)
script.load()
try:
    while True:
        time.sleep(0.3)
except KeyboardInterrupt:
    pass
try: s.detach()
except: pass
