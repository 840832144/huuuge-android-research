#!/usr/bin/env python3
"""Analyze player's actions from captured traffic since game start:
coin/energy deltas from uploadcoin + full save state + key API calls."""
import json
import os
import base64
import gzip
import re

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

# 1. coin balance sequence from uploadcoin
print("===== 金币余额变化 (uploadcoin f1) =====")
coins = []
for r in new:
    if '/attribute/uploadcoin' in (r.get('path') or '') and r.get('req_b64'):
        f = parse(base64.b64decode(r['req_b64']))
        for fn, typ, val in f:
            if typ == 'V':
                # first varint is coin
                coins.append(val); break
for c in coins:
    print("   金币 =", c)
if len(coins) >= 2:
    d = coins[-1] - coins[0]
    print("   => 净变化: {} {} {}".format(d, '+' if d > 0 else '', ''))
    for i in range(1, len(coins)):
        dv = coins[i] - coins[i-1]
        if dv != 0:
            print("     步{}: {} ({})".format(i, coins[i], '+{}'.format(dv) if dv > 0 else str(dv)))

# 2. full save blocks (latest), look at coin/energy
print("\n===== 完整存档状态 (saveuserdata) =====")
blocks = {}
for r in new:
    if '/saveuserdata' in (r.get('path') or '') and r.get('req_b64'):
        f = parse(base64.b64decode(r['req_b64']))
        bn = None; gz = None
        for fn, typ, val in f:
            if typ == 'B':
                try: t = val.decode('utf-8')
                except: continue
                if fn == 1: bn = t
                elif fn == 2: gz = t
        if bn and gz:
            try:
                raw = base64.b64decode(gz)
                data = gzip.decompress(raw) if raw[:2] == b'\x1f\x8b' else raw
                blocks[bn] = data.decode('utf-8', errors='replace')
            except: pass
for bn, txt in blocks.items():
    print("--- block {} ---".format(bn))
    for m in re.finditer(r'"(bonus_lua|energy|coin|gold|money|balance|estate|total_coin)[^,}]*', txt):
        s = m.group(0)
        if len(s) < 120: print("   ", s)
