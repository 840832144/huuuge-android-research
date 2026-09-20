#!/usr/bin/env python3
"""APK 资产侦察 —— 定位业务逻辑层（Lua 字节码 / 配置 / 协议描述符）并做关键字扫描。

手游（cocos2d-x + Lua）的玩法逻辑通常不在 .so 里，而在 APK 的脚本与配置资产中。
本工具回答四件事：
  1. --overview        资产结构（扩展名/顶层目录分布），判断逻辑在哪一层
  2. --extract KINDS   抽取指定类型的资产到工作目录（libef; proto/json/luac/config）
  3. --luac-sample N   采样 .luac 头部，判断是标准 Lua 字节码还是被加密/混淆
  4. --grep KWS        在文本类资产（proto/json/lua 源码/txt/xml）里扫关键字

用法：
  python apk_recon.py <apk> --overview
  python apk_recon.py <apk> --luac-sample 10
  python apk_recon.py <apk> --extract proto,json --out D:\\work\\cf
  python apk_recon.py <apk> --grep "rtp,winRate,newUser,control,adjust" --out D:\\work\\cf
"""
from __future__ import annotations

import argparse
import collections
import pathlib
import re
import sys
import zipfile

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 标准 Lua 字节码签名（各版本），非这些前缀 => 自定义/加密/混淆
LUA_SIGS = {
    b"\x1bLua": "标准 Lua 字节码（\\x1bLua）",
}

TEXT_KINDS = {
    "proto": (".proto",),
    "json": (".json",),
    "txt": (".txt", ".properties", ".version"),
    "xml": (".xml",),
    "lua_src": (".lua",),
    "js": (".js",),
}


def kind_of(name: str) -> str:
    low = name.lower()
    for kind, exts in TEXT_KINDS.items():
        if low.endswith(exts):
            return kind
    if low.endswith(".luac"):
        return "luac"
    return ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("apk")
    ap.add_argument("--overview", action="store_true")
    ap.add_argument("--luac-sample", type=int, default=0)
    ap.add_argument("--extract", default="", help="逗号分隔: proto,json,lua_src,txt,xml,js,luac")
    ap.add_argument("--grep", default="", help="逗号分隔关键字（在文本类资产里扫）")
    ap.add_argument("--raw-grep", default="",
                    help="逗号分隔关键字：对【所有条目按原始字节】扫描（LuaJIT 字节码里的字符串常量也能扫到）")
    ap.add_argument("--raw-limit", type=int, default=3, help="--raw-grep 每关键字最多打印几处")
    ap.add_argument("--extract-lua-plain", action="store_true",
                    help="抽取【看起来是明文 Lua 源码】的脚本（cocos-lua 包常把明文源码与 "
                         "LuaJIT 字节码混装在 .luac 里）；配合 --out 使用，并会列出命中的关键字")
    ap.add_argument("--grep-limit", type=int, default=4, help="每个关键字最多打印几处上下文")
    ap.add_argument("--out", default="", help="抽取/扫描输出的工作目录（建议放在 local-only 下）")
    args = ap.parse_args()

    apk = pathlib.Path(args.apk)
    if not apk.exists():
        print("找不到 APK:", apk, file=sys.stderr)
        return 1
    out = pathlib.Path(args.out) if args.out else None
    if out:
        out.mkdir(parents=True, exist_ok=True)

    z = zipfile.ZipFile(apk)
    names = [n for n in z.namelist() if not n.endswith("/")]
    print("=== {} ===".format(apk.name))
    print("  条目: {}".format(len(names)))

    if args.overview or not (args.extract or args.grep or args.luac_sample):
        ext = collections.Counter(pathlib.Path(n).suffix.lower() or "(noext)" for n in names)
        print("\n-- 扩展名 top 18 --")
        for e, n in ext.most_common(18):
            print("  {:>7}  {}".format(n, e))
        tops = collections.Counter(n.split("/")[0] for n in names)
        print("\n-- 顶层 --")
        for t, n in tops.most_common(10):
            print("  {:>7}  {}".format(n, t))
        # 二级目录（assets/ 下）通常就是"逻辑层"
        a1 = collections.Counter("/".join(n.split("/")[:2]) for n in names
                                 if n.startswith("assets/") and len(n.split("/")) > 2)
        print("\n-- assets 二级目录 top 12 --")
        for k, n in a1.most_common(12):
            print("  {:>7}  {}".format(n, k))

    if args.luac_sample:
        luacs = [n for n in names if n.lower().endswith(".luac")]
        print("\n-- .luac 头部采样（共 {} 个）--".format(len(luacs)))
        seen = collections.Counter()
        for n in luacs[: args.luac_sample]:
            head = z.read(n)[:8]
            sig = next((v for k, v in LUA_SIGS.items() if head.startswith(k)), None)
            label = sig or "非标准前缀（疑似加密/混淆）"
            seen[label] += 1
            print("  {:<58} {}  {}".format(n.split("/")[-1][:58], head.hex(" "), label))
        print("  小结: {}".format(dict(seen)))

    if args.extract:
        kinds = [k.strip() for k in args.extract.split(",") if k.strip()]
        if not out:
            print("\n[!] --extract 需要 --out 指定工作目录", file=sys.stderr)
        else:
            print("\n-- 抽取 --")
            for kind in kinds:
                picked = [n for n in names if kind_of(n) == kind]
                total = 0
                for n in picked:
                    dest = out / kind / n.replace("\\", "/")
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(z.read(n))
                    total += int(z.getinfo(n).file_size)
                print("  {:<8} {:>6} 个文件  {:>10,} B  -> {}".format(
                    kind, len(picked), total, out / kind))

    if args.grep:
        kws = [k.strip() for k in args.grep.split(",") if k.strip()]
        print("\n-- 文本资产关键字扫描 --")
        counts = collections.Counter()
        samples: dict = collections.defaultdict(list)
        for n in names:
            if not kind_of(n) or kind_of(n) == "luac":
                continue
            try:
                txt = z.read(n).decode("utf-8", "replace")
            except Exception:
                continue
            low = txt.lower()
            for k in kws:
                if k.lower() in low:
                    counts[k] += 1
                    if len(samples[k]) < args.grep_limit:
                        i = low.index(k.lower())
                        ctx = txt[max(0, i - 60): i + 90].replace("\n", " ")
                        samples[k].append((n, ctx))
        for k in kws:
            print("  '{}': {} 个文件命中".format(k, counts[k]))
            for n, ctx in samples[k]:
                print("     {:<48} …{}…".format(pathlib.Path(n).name[:48], ctx[:110]))
            if out and samples[k]:
                (out / "grep_{}.txt".format(re.sub(r"\W+", "_", k))).write_text(
                    "\n".join("{} :: {}".format(n, c) for n, c in samples[k]), encoding="utf-8")
    if args.raw_grep:
        kws = [k.strip() for k in args.raw_grep.split(",") if k.strip()]
        # 单次扫描：把关键字合成一个正则，避免"每关键字遍历一遍 700MB"
        pattern = re.compile("|".join(re.escape(k) for k in kws), re.I)
        print("\n-- 原始字节扫描（全部条目，含 LuaJIT 字节码里的字符串常量）--")
        counts = collections.Counter()
        by_file: dict = collections.defaultdict(list)
        for n in names:
            try:
                data = z.read(n)
            except Exception:
                continue
            text = data.decode("latin-1")
            found = collections.Counter(m.group(0).lower() for m in pattern.finditer(text))
            for low, c in found.items():
                label = next((k for k in kws if k.lower() == low), low)
                counts[label] += c
                if len(by_file[label]) < args.raw_limit:
                    j = text.lower().index(low)
                    ctx = text[max(0, j - 50): j + 80]
                    printable = "".join(ch if 32 <= ord(ch) < 127 else "." for ch in ctx)
                    by_file[label].append((n, c, printable))
        for label in kws:
            print("  '{}': {} 处".format(label, counts[label]))
            for n, c, ctx in by_file[label]:
                print("     {:>4}x  {:<52} …{}…".format(c, pathlib.Path(n).name[:52], ctx[:110]))
    if args.extract_lua_plain:
        if not out:
            print("\n[!] --extract-lua-plain 需要 --out 指定工作目录", file=sys.stderr)
        else:
            print("\n-- 抽取明文 Lua 源码（.luac 里混装的那种）--")
            hit_kws = [k.strip() for k in (args.grep or args.raw_grep or "").split(",") if k.strip()]
            kept, hits = 0, collections.defaultdict(list)
            for n in names:
                low = n.lower()
                if not (low.endswith(".luac") or low.endswith(".lua")):
                    continue
                data = z.read(n)
                if data[:3] == b"\x1bLJ":            # LuaJIT 字节码，跳过
                    continue
                head = data[:64]
                if b"\x00" in head:                   # 含 NUL 视为二进制，跳过
                    continue
                try:
                    text = data.decode("utf-8")
                except Exception:
                    text = data.decode("latin-1")
                dest = out / "lua_plain" / n.replace("\\", "/")
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(text, encoding="utf-8")
                kept += 1
                for k in hit_kws:
                    if k.lower() in text.lower():
                        hits[k].append(n)
            print("  明文 Lua 文件: {} 个 -> {}".format(kept, out / "lua_plain"))
            for k in hit_kws:
                if hits[k]:
                    print("  关键字 '{}': {} 个明文文件命中".format(k, len(hits[k])))
                    for n in hits[k][:6]:
                        print("     {}".format(n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
