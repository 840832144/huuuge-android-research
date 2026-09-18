#!/usr/bin/env python3
"""Find the spin action API and decode its coin production, then correlate
with building consumption. Player stated: spin produces coins (consumes energy);
building consumes coins."""
import json
import os
import base64

CAP = os.environ.get("MITM_IN", "mitm_b64.jsonl")
rows = [json.loads(l) for l in open(CAP, encoding='utf-8') if l.strip()]
new = rows[135:]

def parse(buf):
    i = 0; out = []
    while i < len(buf):
        tag = buf[i]; i += 1; fn = tag >> 3; wt = tag & 7
        if wt == 0:
            v = 0; s = 0
            while i < len(buf):
                x = buf[i]; i += 1; v |= (x & 0x7f) << s
                if not (x & 0x80): break
                s += 7
            out.append((fn, 'V', v))
        elif wt == 2:
            L = 0; s = 0
            while i < len(buf):
                x = buf[i]; i += 1; L |= (x & 0x7f) << s
                if not (x & 0x80): break
                s += 7
            out.append((fn, 'B', buf[i:i+L])); i += L
        else:
            break
    return out

# list ALL endpoints not seen before, to find the spin action
print("===== 所有被调用的 API (去重) =====")
seen = set()
for r in new:
    path = r.get('path') or ''
    if path not in seen:
        seen.add(path)
        print("  " + path)

# spin-related: look for slot/spin/roll action endpoints
print("\n===== spin/roll/slot 相关 API =====")
for r in new:
    path = r.get('path') or ''
    if any(k in path.lower() for k in ['spin', 'roll', 'slot', 'play', 'game/']):
        if r.get('req_b64'):
            f = parse(base64.b64decode(r['req_b64']))
            req = " ".join("f{}={}".format(fn, val) if typ == 'V' else "f{}={!r}".format(fn, str(val)[:30]) for fn, typ, val in f)
        else:
            req = "(no body)"
        if r.get('resp_b64'):
            fr = parse(base64.b64decode(r['resp_b64']))
            resp = " ".join("f{}={}".format(fn, val) if typ == 'V' else "f{}={!r}".format(fn, str(val)[:30]) for fn, typ, val in fr)
        else:
            resp = "(no resp)"
        print("  {} REQ[{}] RESP[{}]".format(path, req[:110], resp[:110]))
