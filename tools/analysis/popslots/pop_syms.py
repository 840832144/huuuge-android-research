#!/usr/bin/env python3
"""Enumerate libBigCasino.so symbols (via frida .dynsym) filtered for lobby/
player/character/room/bot/join/etc to reveal the social/lobby system."""
import frida
import json
import time

dev = frida.get_device_manager().add_remote_device("127.0.0.1:27044")
s = dev.attach(15177)

src = r'''
'use strict';
const m = Process.findModuleByName('libBigCasino.so');
send({ base: m.base.toString(), size: m.size });
const hits = [];
m.enumerateExports().forEach(e => {
  const n = e.name;
  if (/lobby|Lobby|player|Player|character|Character|room|Room|join|Join|avatar|Avatar|session|Session|social|Social|friend|Friend|presence|Presence|bot|Bot/i.test(n)) {
    hits.push(n + '=' + e.address);
  }
});
send({ n: hits.length, hits: hits.slice(0, 200) });
'''
script = s.create_script(src)
script.on('message', lambda m, d: print(json.dumps(m.get('payload',{}), ensure_ascii=False)))
script.load()
time.sleep(3)
try: s.detach()
except: pass
