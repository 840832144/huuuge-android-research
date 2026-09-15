#!/usr/bin/env python3
"""Pop! Slots: hook the avatar activity/behaviour state machine to quantify
bot behaviour patterns — walk/sit/stand/play transitions, per-slot occupancy,
and whether slots are always occupied. Symbol-based (ASLR-safe)."""
import frida
import json
import time
import pathlib
import subprocess

ADB = "C:/platform-tools/adb.exe"
r = subprocess.run([ADB, "-s", "127.0.0.1:5565", "shell", "ps", "-A", "|", "grep", "popslots"],
                   capture_output=True, text=True)
pid = None
for line in r.stdout.splitlines():
    if 'popslots' in line:
        try: pid = int(line.split()[1]); break
        except: pass
print("pid:", pid)

dev = frida.get_device_manager().add_remote_device("127.0.0.1:27044")
s = dev.attach(pid)
OUT = pathlib.Path(r"C:\bigfish_research\toptycoon\behaviour.jsonl")

src = r'''
'use strict';
const m = Process.findModuleByName('libBigCasino.so');
function sym(n){ try { return m.getExportByName(n); } catch(e){ return null; } }
// avatar activity handler methods
const targets = {
  'walk':  '_ZN24CShakerAvatarWalkHandler11stopWalkingEP13CShakerAvatar',   // stop walking
  'sit':   '_ZN37CShakerAvatarWalkToSitActivityHandler28onReachedDestinationCallbackEPvP6kmVec3',  // arrived to sit
  'name':  '_ZN13CShakerAvatar7getNameEv',
  'stand': '_ZN33CShakerAvatarStandActivityHandler21EVENT_AVATAR_STANDINGE',
};
const resolved = {};
for (const k in targets) { const a = sym(targets[k]); if (a) resolved[k] = a.toString(); }
send({ resolved });
let n = 0;
for (const k in targets) {
  const a = sym(targets[k]);
  if (!a) continue;
  Interceptor.attach(a, { onEnter(args) {
    n++;
    send({ kind:'ev', ev:k, n });
  }});
}
send({ kind:'ready' });
'''
script = s.create_script(src)
def onmsg(mm, d):
    p = mm.get('payload', {})
    if p.get('kind') == 'ready':
        print("behaviour hook ready — observe/walk in lobby", flush=True)
    elif p.get('kind') == 'ev':
        line = json.dumps({"ev": p.get('ev'), "n": p.get('n')}, ensure_ascii=False)
        with OUT.open('a', encoding='utf-8') as f:
            f.write(line + "\n")
        print("[{}] n={}".format(p.get('ev'), p.get('n')), flush=True)
    elif p.get('kind') == 'resolved':
        print("resolved:", json.dumps(p.get('resolved'), ensure_ascii=False), flush=True)
script.on('message', onmsg)
script.load()
try:
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
try: s.detach()
except: pass
