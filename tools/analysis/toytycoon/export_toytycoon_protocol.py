#!/usr/bin/env python3
"""Toy Tycoon protocol dictionary exporter (static, read-only, reusable).

Extracts the full CG/GC/CL/LC message schema (fields + field numbers) and the
*Reflection service registry from the game's hot-update assembly
Game.Hotfix.dll, which is embedded in a YooAsset UnityFS bundle.

Prereqs:
  - UnityPy (to extract the .dll from the bundle)
  - dnfile (to parse the .NET metadata)
  - The extracted PE already sliced (see PROTOCOL_RECOVERY.md)

Usage:
  python export_toytycoon_protocol.py <Game_Hotfix_pe.dll> <out.json>
"""
import sys
import re
import json
import dnfile


def idx_of(md):
    try:
        return int(md.value)
    except Exception:
        try:
            return int(md.row_index)
        except Exception:
            return None


def main():
    pe_path = sys.argv[1] if len(sys.argv) > 1 else r"C:\bigfish_research\toptycoon\dump\Game_Hotfix_dll_pe.dll"
    out = sys.argv[2] if len(sys.argv) > 2 else r"C:\bigfish_research\toptycoon\toytycoon_protocol_dict.json"

    pe = dnfile.dnPE(pe_path)
    mdt = pe.net.mdtables

    fields_by_row = {}
    for i, f in enumerate(mdt.Field, start=1):
        try:
            fields_by_row[i] = (str(f.Name), str(getattr(f, "Type", "?")))
        except Exception:
            fields_by_row[i] = ("?", "?")

    messages = []
    reflections = []
    for trow in mdt.TypeDef:
        try:
            ns = str(trow.TypeNamespace)
            name = str(trow.TypeName)
        except Exception:
            continue
        if not ns.startswith("Protos"):
            continue
        if name.endswith("Reflection"):
            reflections.append({"namespace": ns, "name": name})
            continue
        fl = getattr(trow, "FieldList", None)
        field_names = []
        field_numbers = []
        if fl:
            for x in fl:
                r = idx_of(x)
                if not r:
                    continue
                fn, ft = fields_by_row.get(r, ("?", "?"))
                if fn.endswith("FieldNumber"):
                    field_numbers.append(fn.replace("FieldNumber", ""))
                elif fn.endswith("_") and not fn.startswith("_"):
                    field_names.append(fn.rstrip("_"))
        messages.append({
            "namespace": ns,
            "name": name,
            "proto_field": None,
            "fields": [{"name": f} for f in field_names],
            "field_numbers": field_numbers,
        })

    real = [m for m in messages if re.match(r"^(CG|GC|CL|LC)", m["name"])]
    doc = {
        "schema_version": "toptycoon-protocol-dict-v1",
        "source": "Game.Hotfix.dll",
        "services": reflections,
        "messages": real,
    }
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=2)
    print("wrote {} ({} messages, {} services)".format(out, len(real), len(reflections)))


if __name__ == "__main__":
    main()
