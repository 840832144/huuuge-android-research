#!/usr/bin/env python3
"""ELF 静态分诊 —— 不需要 IDA 也能快速回答"这是什么、导出了什么、某函数长什么样"。

用途：Android 原生库（libBigCasino.so / libgame.so / libil2cpp.so 之类）的第一轮分诊，
以及在装 IDA 之前对目标库做符号级定位。

依赖：`pip install capstone pyelftools lief`（都可选，缺了会降级：没有 capstone 就不反汇编）。

用法：
  python elf_triage.py <file.so>
  python elf_triage.py <file.so> --grep SSL_write,curl_,parseUserData
  python elf_triage.py <file.so> --disasm SSL_write --count 40
  python elf_triage.py <file.so> --json
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

MACHINES = {
    "EM_X86_64": ("x86", 64),
    "EM_386": ("x86", 32),
    "EM_AARCH64": ("arm64", 64),
    "EM_ARM": ("arm", 32),
}


def load(path: pathlib.Path):
    from elftools.elf.elffile import ELFFile
    fh = path.open("rb")
    elf = ELFFile(fh)
    return fh, elf


def symbols(elf) -> list:
    out = []
    for secname in (".dynsym", ".symtab"):
        sec = elf.get_section_by_name(secname)
        if not sec:
            continue
        for s in sec.iter_symbols():
            if s.name:
                out.append({"name": s.name, "addr": int(s["st_value"]),
                            "size": int(s["st_size"]), "tab": secname})
    return out


def disasm(elf, sym: dict, count: int) -> list:
    try:
        from capstone import Cs, CS_ARCH_X86, CS_ARCH_ARM64, CS_MODE_64, CS_MODE_32
    except Exception:
        return [{"error": "capstone 未安装"}]
    mach = elf["e_machine"]
    arch, bits = MACHINES.get(mach, (None, None))
    if arch == "x86":
        md = Cs(CS_ARCH_X86, CS_MODE_64 if bits == 64 else CS_MODE_32)
    elif arch == "arm64":
        md = Cs(CS_ARCH_ARM64, CS_MODE_64)
    else:
        return [{"error": "不支持的架构: {}".format(mach)}]

    text = elf.get_section_by_name(".text")
    if not text:
        return [{"error": "没有 .text"}]
    base = text["sh_addr"]
    data = text.data()
    off = sym["addr"] - base
    size = sym["size"] or 128
    if off < 0 or off >= len(data):
        return [{"error": "符号不在 .text 内（addr=0x{:x}）".format(sym["addr"])}]
    blob = data[off:off + min(max(size, 16), 4096)]
    rows = []
    for ins in md.disasm(blob, sym["addr"]):
        rows.append({"addr": hex(ins.address), "bytes": ins.bytes.hex(),
                     "mnemonic": ins.mnemonic, "op_str": ins.op_str})
        if len(rows) >= count:
            break
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="ELF 文件（.so / 可执行）")
    ap.add_argument("--grep", default="", help="按子串过滤符号名（逗号分隔，任一命中即列出）")
    ap.add_argument("--limit", type=int, default=40, help="--grep 每关键字最多列几个")
    ap.add_argument("--disasm", default="", help="反汇编该符号（需精确名或在 --grep 结果里唯一）")
    ap.add_argument("--count", type=int, default=30, help="反汇编条数")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    path = pathlib.Path(args.file)
    if not path.exists():
        print("找不到文件:", path, file=sys.stderr)
        return 1

    fh, elf = load(path)
    try:
        syms = symbols(elf)
        info = {
            "file": str(path),
            "size": path.stat().st_size,
            "class": str(elf.elfclass),
            "machine": elf["e_machine"],
            "type": elf["e_type"],
            "sections": elf.num_sections(),
            "dynsym": len([s for s in syms if s["tab"] == ".dynsym"]),
            "symtab": len([s for s in syms if s["tab"] == ".symtab"]),
            "text_size": elf.get_section_by_name(".text").data_size
            if elf.get_section_by_name(".text") else 0,
            "needed": [],
        }
        dyn = elf.get_section_by_name(".dynamic")
        if dyn:
            info["needed"] = [t.needed for t in dyn.iter_tags() if t.entry.d_tag == "DT_NEEDED"]

        matches: dict = {}
        if args.grep:
            for key in [k.strip() for k in args.grep.split(",") if k.strip()]:
                hits = [s for s in syms if key in s["name"]]
                matches[key] = hits[: args.limit]
                info.setdefault("grep_counts", {})[key] = len(hits)

        dis = []
        if args.disasm:
            exact = [s for s in syms if s["name"] == args.disasm]
            pool = exact or [s for s in syms if args.disasm in s["name"]]
            if not pool:
                dis = [{"error": "找不到符号 " + args.disasm}]
            else:
                dis = disasm(elf, pool[0], args.count)

        if args.json:
            info["matches"] = matches
            info["disassembly"] = dis
            print(json.dumps(info, ensure_ascii=False, indent=1))
            return 0

        print("=== {} ===".format(path.name))
        print("  {}-bit {} ({}) | {:.1f} MB | {} 节".format(
            info["class"], info["machine"], info["type"], info["size"] / 1048576, info["sections"]))
        print("  导出(.dynsym): {}  |  本地(.symtab): {}  |  .text: {:.1f} KB".format(
            info["dynsym"], info["symtab"], info["text_size"] / 1024))
        if info["needed"]:
            print("  依赖: {}".format(", ".join(info["needed"][:10])))

        for key, hits in matches.items():
            print("\n-- 符号匹配 '{}'（共 {}）:".format(key, info["grep_counts"][key]))
            for s in hits:
                print("   0x{:08x}  size={:<6} {}".format(s["addr"], s["size"], s["name"]))

        if dis:
            print("\n-- 反汇编:")
            for row in dis:
                if "error" in row:
                    print("   ", row["error"])
                else:
                    print("   {}  {:<20} {} {}".format(row["addr"], row["bytes"][:20],
                                                       row["mnemonic"], row["op_str"]))
        return 0
    finally:
        fh.close()


if __name__ == "__main__":
    sys.exit(main())
