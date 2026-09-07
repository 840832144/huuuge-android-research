#!/usr/bin/env python3
"""Extract the full player save from captured saveuserdata flows.
It is gzip(base64(json)) per data-block (f1 = block name, f2 = gzip base64).
Writes each block's decoded JSON to a .json. Planner-facing: full numeric
state (coins, energy, resources, building, bonus_lua, ...)."""
import json
import base64
import gzip
import os
import sys

CAP = r"C:\bigfish_research\toptycoon\mitm_b64.jsonl"
OUTDIR = r"C:\bigfish_research\toptycoon\save_blocks"
os.makedirs(OUTDIR, exist_ok=True)

def parse(buf):
    i = 0; out = []
    while i < len(buf):
        tag = buf[i]; i += 1
        fnum = tag >> 3; wt = tag & 7
        if wt == 0:
            v = 0; s = 0
            while i < len(buf):
                x = buf[i]; i += 1; v |= (x & 0x7f) << s
                if not (x & 0x80): break
                s += 7
            out.append((fnum, "V", v))
        elif wt == 2:
            L = 0; s = 0
            while i < len(buf):
                x = buf[i]; i += 1; L |= (x & 0x7f) << s
                if not (x & 0x80): break
                s += 7
            out.append((fnum, "B", buf[i:i+L])); i += L
        else:
            break
    return out

def main():
    rows = [json.loads(l) for l in open(CAP, encoding='utf-8') if l.strip()]
    n = 0
    for r in rows:
        if not (r.get('path') and 'saveuserdata' in r.get('path','')): continue
        if not r.get('req_b64'): continue
        b = base64.b64decode(r['req_b64'])
        fields = parse(b)
        block_name = None; gz_b64 = None
        for fnum, typ, val in fields:
            if typ == "B":
                try: txt = val.decode('utf-8')
                except: continue
                if fnum == 1:
                    block_name = txt
                elif fnum == 2:
                    gz_b64 = txt
        if block_name and gz_b64:
            try:
                raw = base64.b64decode(gz_b64)
                if raw[:2] == b'\x1f\x8b':
                    data = gzip.decompress(raw)
                else:
                    data = raw
                txt = data.decode('utf-8', errors='replace')
                fn = os.path.join(OUTDIR, "{}.json".format(block_name.replace('/', '_')))
                with open(fn, 'w', encoding='utf-8') as f:
                    f.write(txt)
                n += 1
                print("saved block {} -> {} ({} bytes)".format(block_name, fn, len(txt)))
            except Exception as e:
                print("err block {}: {}".format(block_name, e))
    print("total blocks:", n)

if __name__ == '__main__':
    main()
