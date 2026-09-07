#!/usr/bin/env python3
"""Generic protobuf wire-format dumper. Reads base64 protobuf bodies from
mitm_b64.jsonl and prints field# = value (varint/string/bytes/nested).
Module-agnostic — any message decodes to readable tag:value pairs."""
import json
import base64
import sys

def read_varint(b, i):
    r = 0; s = 0
    while True:
        if i >= len(b): raise ValueError("eof")
        x = b[i]; i += 1
        r |= (x & 0x7F) << s
        if not (x & 0x80): break
        s += 7
    return r, i

def dump(b, indent=0):
    i = 0; out = []
    while i < len(b):
        try:
            tag, i = read_varint(b, i)
        except Exception:
            out.append("  "*indent + "...truncated"); break
        fnum = tag >> 3; wt = tag & 7
        if wt == 0:  # varint
            v, i = read_varint(b, i)
            out.append("  "*indent + "f{} = V({})".format(fnum, v))
        elif wt == 2:  # bytes/string
            L, i = read_varint(b, i)
            data = b[i:i+L]; i += L
            try:
                s = data.decode('utf-8')
                out.append("  "*indent + "f{} = S({!r})".format(fnum, s))
            except Exception:
                out.append("  "*indent + "f{} = B[{}]".format(fnum, data[:60].hex()))
        elif wt == 5:  # 32-bit
            v = int.from_bytes(b[i:i+4], 'little'); i += 4
            out.append("  "*indent + "f{} = I32({})".format(fnum, v))
        elif wt == 1:  # 64-bit
            v = int.from_bytes(b[i:i+8], 'little'); i += 8
            out.append("  "*indent + "f{} = I64({})".format(fnum, v))
        else:
            out.append("  "*indent + "f{} = (unk wt {})".format(fnum, wt)); break
    return "\n".join(out)

def main():
    src = r"C:\bigfish_research\toptycoon\mitm_b64.jsonl"
    rows = [json.loads(l) for l in open(src, encoding='utf-8') if l.strip()]
    for r in rows:
        path = r.get('path') or ''
        if r.get('req_b64'):
            b = base64.b64decode(r['req_b64'])
            print("="*60)
            print("REQ {} {}\n{}".format(r.get('host'), path, dump(b)))
        if r.get('resp_b64'):
            b = base64.b64decode(r['resp_b64'])
            print("="*60)
            print("RESP {} {}\n{}".format(r.get('host'), path, dump(b)))

if __name__ == '__main__':
    main()
