#!/usr/bin/env python3
"""Full decoder: read captured mitm_b64.jsonl, decode protobuf bodies to
field#=value pairs, and where the static dict has a message for that endpoint,
label the fields. Output is planner-facing: endpoint -> message -> field=value.
"""
import json
import base64
import os

DICT = r"C:\bigfish_research\toptycoon\toytycoon_protocol_dict.json"
CAP = r"C:\bigfish_research\toptycoon\mitm_b64.jsonl"

# endpoint path -> likely message name hint (best-effort; schemas lack tags)
def msg_hint(path):
    p = path.replace("/tycoon/", "").replace("/", "_")
    cand = []
    seg = [s for s in path.split("/") if s]
    # last 2 segments as CG/GC name candidates
    if len(seg) >= 2:
        for prefix in ("CG", "GC"):
            for n in (seg[-1], seg[-2] + "_" + seg[-1]):
                cand.append(prefix + n.title().replace("_", ""))
    return cand

def dump(b, indent=0):
    i = 0; out = []
    while i < len(b):
        tag = 0; s = 0
        while i < len(b):
            x = b[i]; i += 1; tag |= (x & 0x7f) << s
            if not (x & 0x80): break
            s += 7
        fnum = tag >> 3; wt = tag & 7
        if wt == 0:
            v = 0; ss = 0
            while i < len(b):
                x = b[i]; i += 1; v |= (x & 0x7f) << ss
                if not (x & 0x80): break
                ss += 7
            out.append((fnum, "V", v))
        elif wt == 2:
            L = 0; ss0 = 0
            while i < len(b):
                x = b[i]; i += 1; L |= (x & 0x7f) << ss0
                if not (x & 0x80): break
                ss0 += 7
            data = b[i:i+L]; i += L
            try:
                out.append((fnum, "S", data.decode('utf-8')))
            except Exception:
                # nested message? try dump
                nested = dump(data, indent+1)
                if nested and len(nested) > 1:
                    out.append((fnum, "MSG", nested))
                else:
                    out.append((fnum, "B", data.hex()))
        elif wt == 5:
            v = int.from_bytes(b[i:i+4], 'little'); i += 4
            out.append((fnum, "I32", v))
        elif wt == 1:
            v = int.from_bytes(b[i:i+8], 'little'); i += 8
            out.append((fnum, "I64", v))
        else:
            out.append((fnum, "?", wt)); break
    return out

def main():
    dict_msgs = json.load(open(DICT, encoding='utf-8'))['messages']
    rows = [json.loads(l) for l in open(CAP, encoding='utf-8') if l.strip()]
    for r in rows:
        path = r.get('path') or ''
        if r.get('req_b64'):
            f = dump(base64.b64decode(r['req_b64']))
            print("=" * 70)
            print("REQ {}  {}  hints={}".format(r.get('host'), path, msg_hint(path)))
            for fnum, typ, val in f:
                print("   f{:<4}{} = {}".format(fnum, typ, str(val)[:100]))
        if r.get('resp_b64'):
            f = dump(base64.b64decode(r['resp_b64']))
            print("=" * 70)
            print("RESP {}  {}  hints={}".format(r.get('host'), path, msg_hint(path)))
            for fnum, typ, val in f:
                if typ == "MSG":
                    print("   f{:<4}MSG =".format(fnum))
                    for ff, tt, vv in val:
                        print("        f{}{}={}".format(ff, tt, str(vv)[:80]))
                else:
                    print("   f{:<4}{} = {}".format(fnum, typ, str(val)[:100]))

if __name__ == '__main__':
    main()
