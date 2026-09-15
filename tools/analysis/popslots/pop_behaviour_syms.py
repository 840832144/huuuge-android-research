#!/usr/bin/env python3
"""Enumerate avatar behaviour/activity handler symbols to reconstruct the full
behaviour state machine (walk/sit/stand/play/idle/celebrate/seat). For the
bot-behaviour design report."""
import frida
import json
import time
import subprocess

ADB = "C:/platform-tools/adb.exe"
r = subprocess.run([ADB, "-s", "127.0.0.1:5565", "shell", "ps", "-A", "|", "grep", "popslots"],
                   capture_output=True, text=True)
pid = None
for line in r.stdout.splitlines():
    if 'popslots' in line:
        try: pid = int(line.split()[1]); break
        except: pass

dev = frida.get_device_manager().add_remote_device("127.0.0.1:27044")
s = dev.attach(pid)

src = r'''
'use strict';
const m = Process.findModuleByName('libBigCasino.so');
const hits = [];
m.enumerateExports().forEach(e => {
  const n = e.name;
  if (/ActivityHandler|Walk|Sit|Stand|Believe|Celebrate|Idle|Lobby|Seat|Chair|Machine|Slot|Play|Idle|AvatarState|Activity|Random/i.test(n)) {
    hits.push(n);
  }
});
send({ n: hits.length, hits: hits.slice(0, 400) });
'''
script = s.create_script(src)
script.on('message', lambda m, d: print(json.dumps(m.get('payload',{}), ensure_ascii=False)))
script.load()
time.sleep(3)
try: s.detach()
except: pass
