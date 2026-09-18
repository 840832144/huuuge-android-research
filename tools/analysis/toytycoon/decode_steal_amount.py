#!/usr/bin/env python3
"""Decode nested varints in steal/targethouse responses to extract the stolen
coin amount per attack."""
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

# targethouse response f3 is a nested message (varint pairs). Parse it.
print("===== steal/targethouse 响应 (嵌套解码, 找偷到金币) =====")
for r in new:
    path = r.get('path') or ''
    if '/steal/targethouse' in path and r.get('resp_b64'):
        b = base64.b64decode(r['resp_b64'])
        print("-" * 60)
        f = parse(b)
        for fn, typ, val in f:
            if typ == 'B':
                # nested message: parse varints
                nest = parse(val)
                nest_s = " ".join("f{}={}".format(nn, vv) if tt == 'V' else "f{}={!r}".format(nn, str(vv)[:40]) for nn, tt, vv in nest)
                print("  f{} (nested): {}".format(fn, nest_s))
            else:
                print("  f{} = {}".format(fn, val))
