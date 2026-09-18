#!/usr/bin/env python3
"""找出"哪个模拟器实例才是目标" —— 按证据，不按名字。

背景：同一台机器上可以存在**两套 BlueStacks 安装**（例如 BlueStacks_nxt_cn 与
BlueStacks_nxt），它们的实例名可以重复（都叫 `Pie64`），而且各自的 Android 镜像、
已装应用、端口都不同。因此：

    **实例名不是标识。唯一的标识是证据** —— 该实例是否装了目标包、能否 root、
    跑的哪个 Android 版本。

本工具枚举**所有**安装下的**所有**实例，逐条给出证据与结论，避免"在错误实例上注入"。

用法：
  python find_instance.py                                  # 默认找 Pop! Slots
  python find_instance.py --package com.monopoly.dream.idle.king
  python find_instance.py --json                            # 机器可读输出

只做只读查询：读注册表/配置、adb getprop / pm list packages / id。
不启动实例、不改配置、不注入。
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import subprocess
import sys

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "analysis" / "popslots"))
try:
    import pop_common as pc          # 复用公共 adb 层（路径/PID/root 通道）
except Exception:                    # 允许在没装依赖的机器上仍给出注册表信息
    pc = None

REG_KEYS = [
    (r"SOFTWARE\BlueStacks_nxt_cn"),
    (r"SOFTWARE\BlueStacks_nxt"),
    (r"SOFTWARE\WOW6432Node\BlueStacks_nxt_cn"),
    (r"SOFTWARE\WOW6432Node\BlueStacks_nxt"),
    (r"SOFTWARE\BlueStacks"),
]


def read_installs() -> list:
    """从注册表读取每套安装的版本、安装目录与配置目录。"""
    installs = []
    try:
        import winreg
    except Exception:
        return installs
    for path in REG_KEYS:
        for hive in (winreg.HKEY_LOCAL_MACHINE,):
            try:
                key = winreg.OpenKey(hive, path)
            except OSError:
                continue
            props = {}
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                except OSError:
                    break
                props[name] = value
                i += 1
            installs.append({
                "registry": path,
                "version": str(props.get("Version", "")),
                "install_dir": str(props.get("InstallDir", "")),
                "data_dir": str(props.get("DataDir", "")),
                "user_dir": str(props.get("UserDefinedDir", "")),
            })
    return installs


def conf_path(install: dict) -> pathlib.Path:
    for base in (install.get("user_dir"), install.get("data_dir")):
        if not base:
            continue
        cand = pathlib.Path(base)
        if cand.name.lower().endswith(".conf"):
            return cand
        p = cand / "bluestacks.conf"
        if p.exists():
            return p
        p2 = cand.parent / "bluestacks.conf"
        if p2.exists():
            return p2
    # 该机器的常见回退位置（两套安装的数据目录命名不同）
    for cand in (r"D:\BlueStacks_nxt_cn\bluestacks.conf", r"C:\ProgramData\BlueStacks_nxt\bluestacks.conf",
                 r"C:\ProgramData\BlueStacks_nxt_cn\bluestacks.conf"):
        if pathlib.Path(cand).exists():
            return pathlib.Path(cand)
    return pathlib.Path("")


def read_conf(path: pathlib.Path) -> dict:
    conf = {}
    if not path or not path.exists():
        return conf
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "=" in line and line.count('"') >= 2:
            k, _, v = line.partition("=")
            conf[k.strip()] = v.strip().strip('"')
    return conf


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--package", default="com.playstudios.popslots", help="要查找的包名")
    ap.add_argument("--adb", default="", help="adb 路径（默认自动查找）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    adb_exe = pc.adb_path(args.adb) if pc else "adb"
    installs = read_installs()
    rows = []

    for install in installs:
        cfg = conf_path(install)
        conf = read_conf(cfg)
        install["config"] = str(cfg)
        install["config_found"] = bool(conf)
        names = sorted({k.split(".")[2] for k in conf
                        if k.startswith("bst.instance.") and k.endswith(".display_name")})
        for name in names:
            pre = "bst.instance.{}.".format(name)
            port = conf.get(pre + "adb_port", "")
            serial = "127.0.0.1:{}".format(port) if port else ""
            alt = "emulator-{}".format(int(port) - 2) if port.isdigit() else ""

            def probe(cmd, s):
                if not pc or not s:
                    return ""
                return pc.adb(s, *cmd, adb_exe=adb_exe, timeout=25)

            def version_of(text: str) -> str:
                """adb 的错误文本（device not found 等）不是版本号，要过滤掉。"""
                t = (text or "").strip()
                return t if re.match(r"^\d+(\.\d+)*$", t) else ""

            first = probe(["shell", "getprop", "ro.build.version.release"], serial)
            android = version_of(first)
            used = serial
            if not android and alt:
                second = probe(["shell", "getprop", "ro.build.version.release"], alt)
                android = version_of(second)
                if android:
                    used = alt
            reachable = bool(android)
            note = "" if reachable else (first or "adb 无输出").strip().splitlines()[0][:60]
            model = probe(["shell", "getprop", "ro.product.model"], used) if reachable else ""
            pkgs = probe(["shell", "pm", "list", "packages", args.package], used) if reachable else ""
            has_pkg = args.package in pkgs
            root = False
            if reachable:
                if "uid=0" in probe(["shell", "id"], used):
                    root = True
                elif "uid=0" in probe(["shell", "su", "-c", "id"], used):
                    root = True

            if not reachable:
                verdict = "未运行"
            elif has_pkg and root:
                verdict = "★ 研究候选（有包 + 有 root）"
            elif has_pkg and not root:
                verdict = "有包但无 root（若是日常实例，不要碰）"
            else:
                verdict = "无目标包"

            rows.append({
                "install": pathlib.Path(install.get("data_dir") or install["registry"]).name,
                "version": install["version"],
                "instance": name,
                "display": conf.get(pre + "display_name", ""),
                "adb_port": port,
                "serial": used or serial,
                "android": android,
                "model": model.strip() if reachable else "",
                "root_flag": conf.get(pre + "enable_root_access", ""),
                "root": root,
                "has_package": has_pkg,
                "verdict": verdict,
                "note": note,
                "install_dir": install.get("install_dir", ""),
                "config": install.get("config", ""),
            })

    if args.json:
        print(json.dumps({"adb": adb_exe, "package": args.package,
                          "installs": installs, "instances": rows},
                         ensure_ascii=False, indent=1))
        return 0

    print("adb: {}".format(adb_exe))
    print("目标包: {}".format(args.package))
    print("\n找到的 BlueStacks 安装（一个机器上可能有多套，实例名可能重复）:")
    if not installs:
        print("  (注册表里没有找到；只读枚举不到安装)")
    for inst in installs:
        mark = "" if inst.get("config_found") else "   <-- 配置未找到，其实例未枚举"
        print("  {}  v{}{}".format(inst["registry"], inst["version"], mark))
        if inst.get("config_found"):
            print("      安装目录: {}\n      配置: {}".format(inst.get("install_dir"), inst.get("config")))

    print("\n实例证据表:")
    if not rows:
        print("  (没有枚举到任何实例)")
    else:
        head = "{:<14} {:<10} {:<8} {:<9} {:<12} {:<6} {:<6} {}".format(
            "实例", "显示名", "adb端口", "Android", "型号", "root", "有包", "结论")
        print("  " + head)
        for r in rows:
            print("  {:<14} {:<10} {:<8} {:<9} {:<12} {:<6} {:<6} {}".format(
                r["instance"][:14], (r["display"] or "")[:10], r["adb_port"],
                (r["android"] or "-")[:9], (r["model"] or "-")[:12],
                "yes" if r["root"] else "no", "yes" if r["has_package"] else "no", r["verdict"]))
            if r.get("note"):
                print("      └─ {}".format(r["note"]))

    cands = [r for r in rows if r["has_package"] and r["root"]]
    print("")
    if len(cands) == 1:
        c = cands[0]
        print("=> 用实例 '{}'（serial {}）：它装了 {} 且 root 可用。".format(
            c["instance"], c["serial"], args.package))
        print("   （仍请确认它不是你的日常实例）")
    elif len(cands) > 1:
        print("=> 有多个实例同时满足（{}）：请挑隔离的研究实例，"
              "**绝不要用日常实例**。".format("、".join(c["instance"] for c in cands)))
    else:
        print("=> 没有任何实例同时具备「目标包 + root」。**现在不要在任意实例上注入**：")
        print("   先启动研究实例；若它确实没装包或没开 root，需所有者授权后再装包/开 root。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
