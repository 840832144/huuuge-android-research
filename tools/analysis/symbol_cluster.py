#!/usr/bin/env python3
"""按前缀给 ELF 导出符号聚类 —— 快速判断"这个库是干什么的、业务逻辑在哪一层"。

用途：拿到一个大的原生库（手游 .so 常见 3–5 万导出），先看导出的**前缀分布**，
就能判断它是引擎绑定层（如 `lua_cocos2dx_*`）、业务逻辑层，还是通用库；
再按关键字过滤出候选面（加密/网络/JNI/…）。

用法：
  python symbol_cluster.py <file.so>                        # 前缀 top-N
  python symbol_cluster.py <file.so> --top 40
  python symbol_cluster.py <file.so> --grep "Encrypt,Crypto,Http,Jni"
  python symbol_cluster.py <file.so> --prefix-length 3       # 用更短前缀（更粗的聚类）
"""
from __future__ import annotations

import argparse
import collections
import pathlib
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def demangle_basic(name: str) -> str:
    """只做最小处理：Itanium 名字取 `_ZN…` 后的可读片段；足够用于前缀聚类。"""
    if name.startswith("_ZN") or name.startswith("_Z"):
        # 去掉 _Z/_ZN 与长度前缀，粗略还原：4Foo7bar -> Foo::bar
        s = name[2:] if name.startswith("_Z") else name
        s = s[1:] if s.startswith("N") else s
        out, i = [], 0
        while i < len(s):
            m = re.match(r"(\d+)", s[i:])
            if not m:
                break
            n = int(m.group(1))
            i += len(m.group(1))
            out.append(s[i:i + n])
            i += n
        return "::".join(out) if out else name
    return name


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--top", type=int, default=30)
    ap.add_argument("--prefix-length", type=int, default=0,
                    help="按前 N 个字符聚类（默认按首个分隔符切分）")
    ap.add_argument("--grep", default="", help="逗号分隔关键字（子串匹配，任一命中即列出）")
    ap.add_argument("--limit", type=int, default=25, help="--grep 每关键字最多列几个")
    ap.add_argument("--save", default="", help="把全部符号导出到该文件（每行一个）")
    args = ap.parse_args()

    path = pathlib.Path(args.file)
    if not path.exists():
        print("找不到文件:", path, file=sys.stderr)
        return 1

    from elftools.elf.elffile import ELFFile
    with path.open("rb") as fh:
        elf = ELFFile(fh)
        syms = []
        for secname in (".dynsym", ".symtab"):
            sec = elf.get_section_by_name(secname)
            if not sec:
                continue
            for s in sec.iter_symbols():
                if s.name:
                    syms.append(s.name)
    names = sorted(set(syms))
    print("=== {} ===".format(path.name))
    print("  唯一符号: {} （.dynsym+.symtab 去重）".format(len(names)))

    if args.save:
        pathlib.Path(args.save).write_text("\n".join(names), encoding="utf-8")
        print("  已导出全部符号 -> {}".format(args.save))

    counter = collections.Counter()
    for raw in names:
        d = demangle_basic(raw)
        if args.prefix_length:
            key = d[: args.prefix_length]
        else:
            parts = re.split(r"[:_\s]", d, 1)
            key = parts[0] if parts and parts[0] else d
        counter[key] += 1

    print("\n-- 前缀分布 top {} --".format(args.top))
    for key, n in counter.most_common(args.top):
        print("  {:>7}  {}".format(n, key))

    if args.grep:
        keys = [k.strip() for k in args.grep.split(",") if k.strip()]
        print("\n-- 关键字命中 --")
        for k in keys:
            hits = [x for x in names if k.lower() in x.lower()]
            print("  '{}': {} 命中".format(k, len(hits)))
            for h in hits[: args.limit]:
                print("     {}".format(demangle_basic(h)[:110]))
            # 打印原始名便于直接 Hook（Frida 需要 mangled 名）
            if hits and len(hits) <= args.limit:
                for h in hits[:3]:
                    if h != demangle_basic(h):
                        print("       raw: {}".format(h[:120]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
