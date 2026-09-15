#!/usr/bin/env python3
"""Pop! Slots: hook CShakerServerUserDataParser::parseUserData to inspect each
server-delivered user's identity (name/id/profile) — the key to prove whether
lobby users are real players or server-generated bots."""
import frida
import json
import time

dev = frida.get_device_manager().add_remote_device("127.0.0.1:27044")
s = dev.attach(15177)

# CShakerServerUserDataParser::parseUserData
PARSE = 0x7a1c8aa92e90
# CRoomUsersManager::getUserByShakerId
# CShakerAvatar::getName = 0x7a1c8ac8d740

src = r'''
'use strict';
const parse = ptr(0x7a1c8aa92e90);
let n = 0;
Interceptor.attach(parse, {
  onEnter(args) {
    // parseUserData(void* data, CRoomUserModel* model)
    this.model = args[1];
    n++;
    send({ kind:'enter', n, model: this.model.toString() });
  },
  onLeave(retval) {
    // read CRoomUserModel: it's a C++ object. String members are std::string
    // (pointer to char data). Dump first ~200 bytes and look for ASCII name/id.
    const m = this.model;
    if (!m || m.isNull()) return;
    let ascii = '';
    try {
      const b = new Uint8Array(m.readByteArray(200));
      for (let i=0;i<b.length;i++){ if(b[i]>=32&&b[i]<=126) ascii += String.fromCharCode(b[i]); else ascii += '.'; }
    } catch(e){}
    send({ kind:'model', n, ascii: ascii.slice(0,180) });
  }
});
send({ kind:'ready' });
'''
script = s.create_script(src)
def onmsg(mm, d):
    p = mm.get('payload', {})
    if p.get('kind') == 'ready':
        print("parseUserData hook ready — have lobby update/join (walk around)", flush=True)
    elif p.get('kind') == 'enter':
        print("[enter] n={} model={}".format(p.get('n'), p.get('model')), flush=True)
    elif p.get('kind') == 'model':
        print("[model] n={} ascii={}".format(p.get('n'), p.get('ascii')), flush=True)
script.on('message', onmsg)
script.load()
print("running 30s — trigger lobby user updates (walk/sit/refresh)", flush=True)
time.sleep(30)
print("DONE", flush=True)
try: s.detach()
except: pass
