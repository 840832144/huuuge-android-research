#!/usr/bin/env python3
"""Pop! Slots: search ALL modules for TLS/network write symbols to find the
real network path (SSL_write / send / custom). Then decide capture method."""
import frida
import json
import time

dev = frida.get_device_manager().add_remote_device("127.0.0.1:27044")
s = dev.attach(15177)

src = r'''
'use strict';
const mods = Process.enumerateModules();
send({ n: mods.length });
const net_hits = {};
mods.forEach(m => {
  let exps = [];
  try { exps = m.enumerateExports(); } catch(e){ return; }
  exps.forEach(e => {
    if (/SSL_write|SSL_read|ssl_write|BIO_write|BIO_read|send\(|recv\(|ws_send|WSAsend|sslv3_write|ssl3_write/i.test(e.name)) {
      if (!net_hits[m.name]) net_hits[m.name] = [];
      net_hits[m.name].push(e.name + '=' + e.address);
    }
  });
});
send({ net_hits });
// also crypto/network libs loaded
const crypto = mods.filter(m => /ssl|crypto|curl|okhttp|socket|http/i.test(m.name)).map(m => m.name);
send({ crypto });
'''
script = s.create_script(src)
script.on('message', lambda m, d: print(json.dumps(m.get('payload',{}), ensure_ascii=False)))
script.load()
time.sleep(2)
try: s.detach()
except: pass
