#!/usr/bin/env python3
"""从明文 Lua 源码树里抽取"客户端实际读取的服务端字段"目录。

用途：cocos2d-x + Lua 手游的协议通常是**自定义 TCP + 自定义加密**，抓包难，
但客户端已经把响应解成了 Lua table。把 `ret["x"] / result["x"] / data["x"]` 这类
字段读取全部收集起来，就等于拿到了**服务端响应 schema 的客户端视角** ——
足以回答"协议里有没有某个字段"（例如玩法调控、保底、风控标志）。

配合 `apk_recon.py --extract-lua-plain` 使用：先抽出明文 Lua，再跑本工具。

用法：
  python lua_field_catalog.py <lua_plain 目录>
  python lua_field_catalog.py <dir> --focus "novice,win,rate,control,adjust,recoup"
  python lua_field_catalog.py <dir> --json out.json
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 这些是"装服务端响应的变量名"，覆盖常见命名
HOLDERS = ("ret", "result", "data", "msg", "res", "info", "pkg", "response",
           "reply", "rsp", "resp", "body", "obj", "serverData", "svr_data")
FIELD_RE = re.compile(
    r"\b(?:%s)\[\s*[\"']([A-Za-z_][A-Za-z0-9_]{1,40})[\"']\s*\]" % "|".join(HOLDERS))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", help="明文 Lua 目录（apk_recon.py --extract-lua-plain 的产物）")
    ap.add_argument("--focus", default="",
                    help="逗号分隔：只看含这些子串的字段名（不区分大小写）")
    ap.add_argument("--top", type=int, default=60, help="打印前 N 个字段")
    ap.add_argument("--json", default="", help="把完整目录写成 JSON")
    args = ap.parse_args()

    root = pathlib.Path(args.root)
    if not root.is_dir():
        print("不是目录:", root, file=sys.stderr)
        return 1

    counts: collections.Counter = collections.Counter()
    where: dict = collections.defaultdict(set)
    lua_files = 0
    for p in root.rglob("*.luac"):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        lua_files += 1
        for m in FIELD_RE.finditer(text):
            f = m.group(1)
            counts[f] += 1
            if len(where[f]) < 6:
                where[f].add(p.name)

    print("=== 服务端字段目录 ===")
    print("  扫描明文 Lua 文件: {}".format(lua_files))
    print("  唯一字段名: {}".format(len(counts)))

    focus = [k.strip().lower() for k in args.focus.split(",") if k.strip()]
    if focus:
        picked = [f for f in counts if any(k in f.lower() for k in focus)]
        print("\n-- 命中 focus={} 的字段（{} 个）--".format(focus, len(picked)))
        for f in sorted(picked, key=lambda x: -counts[x]):
            print("  {:<34} {:>5}x   {}".format(f, counts[f], ", ".join(sorted(where[f])[:3])))
    else:
        print("\n-- 出现最多的字段 top {} --".format(args.top))
        for f, c in counts.most_common(args.top):
            print("  {:<34} {:>5}x   {}".format(f, c, ", ".join(sorted(where[f])[:3])))

    if args.json:
        pathlib.Path(args.json).write_text(json.dumps(
            {f: {"count": counts[f], "files": sorted(where[f])} for f in counts},
            ensure_ascii=False, indent=1), encoding="utf-8")
        print("\n完整目录 -> {}".format(args.json))
    return 0


if __name__ == "__main__":
    sys.exit(main())
