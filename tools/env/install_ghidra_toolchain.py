#!/usr/bin/env python3
"""一键装好无 IDA 的静态分析工具链（便携、无需管理员）。

装什么：
  - Ghidra（最新 release 的 zip，解压到 --apps）
  - Temurin JDK 21（Ghidra 12 需要；zip 便携版）
不修改 PATH / 注册表 / 系统环境，只解压到目录。已存在则跳过下载。

用法：
  python install_ghidra_toolchain.py                 # 默认 D:\\Apps
  python install_ghidra_toolchain.py --apps D:\\Tools
  python install_ghidra_toolchain.py --check         # 只报告是否就绪

装完后的复现命令（以 libBigCasino.so 为例）：
  $env:JAVA_HOME="<JDK>"; $env:MAXMEM="6G"
  <GHIDRA>\\support\\analyzeHeadless.bat <proj_dir> <proj_name> -import <binary> \\
      -scriptPath tools/analysis/ghidra_scripts -postScript ListFuncs.java CSlotsFinder 40
  # 复用已分析项目时务必加 -noanalysis，否则会重跑全量分析（大型库约 15 分钟）
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
import time
import urllib.request
import zipfile

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Adoptium 会 403 掉默认的 urllib UA，必须带一个常规 UA
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) dsh-toolchain/1.0"}
GHIDRA_API = "https://api.github.com/repos/NationalSecurityAgency/ghidra/releases/latest"
JDK_URL = ("https://api.adoptium.net/v3/binary/latest/21/ga/windows/x64/jdk/hotspot/"
           "normal/eclipse")


def fetch(url: str, dest: pathlib.Path, min_bytes: int = 1024 * 1024) -> pathlib.Path:
    if dest.exists() and dest.stat().st_size > min_bytes:
        print("  已存在，跳过: {} ({:.0f} MB)".format(dest.name, dest.stat().st_size / 1048576))
        return dest
    print("  下载: {}".format(url))
    t0 = time.time()
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=180) as r, dest.open("wb") as f:
        total = int(r.headers.get("Content-Length") or 0)
        got, last = 0, 0
        while True:
            chunk = r.read(1024 * 512)
            if not chunk:
                break
            f.write(chunk)
            got += len(chunk)
            if total and got - last > 60 * 1024 * 1024:
                last = got
                print("     {:.0f}/{:.0f} MB ({:.0f}s)".format(
                    got / 1048576, total / 1048576, time.time() - t0), flush=True)
    print("    完成 {:.0f} MB / {:.0f}s".format(dest.stat().st_size / 1048576, time.time() - t0))
    return dest


def extract(zip_path: pathlib.Path, into: pathlib.Path) -> pathlib.Path:
    print("  解压: {}".format(zip_path.name))
    with zipfile.ZipFile(zip_path) as z:
        tops = sorted({n.split("/")[0] for n in z.namelist() if n})
        z.extractall(into)
    return into / tops[0] if len(tops) == 1 else into


def find_existing(apps: pathlib.Path) -> tuple:
    ghidra = jdk = None
    for p in sorted(apps.glob("ghidra_*")):
        if (p / "support" / "analyzeHeadless.bat").exists():
            ghidra = p
    for p in sorted(apps.glob("jdk-*")):
        if (p / "bin" / "java.exe").exists():
            jdk = p
    return ghidra, jdk


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apps", default=r"D:\Apps", help="安装根目录（默认 D:\\Apps）")
    ap.add_argument("--downloads", default=r"D:\DSH_work\downloads", help="下载缓存目录")
    ap.add_argument("--check", action="store_true", help="只检查，不下载")
    args = ap.parse_args()

    apps = pathlib.Path(args.apps)
    dl = pathlib.Path(args.downloads)
    apps.mkdir(parents=True, exist_ok=True)
    dl.mkdir(parents=True, exist_ok=True)

    ghidra, jdk = find_existing(apps)
    print("Ghidra: {}".format(ghidra or "(未安装)"))
    print("JDK   : {}".format(jdk or "(未安装)"))
    if args.check:
        print("\n结论: {}".format("READY" if (ghidra and jdk) else "NOT READY"))
        return 0 if (ghidra and jdk) else 1

    if not ghidra:
        with urllib.request.urlopen(urllib.request.Request(GHIDRA_API, headers=UA),
                                    timeout=60) as r:
            rel = json.load(r)
        asset = next(a for a in rel["assets"] if a["name"].endswith(".zip"))
        print("Ghidra 版本: {}  资产: {} ({:.0f} MB)".format(
            rel["tag_name"], asset["name"], asset["size"] / 1048576))
        z = fetch(asset["browser_download_url"], dl / asset["name"])
        ghidra = extract(z, apps)

    if not jdk:
        z = fetch(JDK_URL, dl / "temurin-jdk21-win-x64.zip")
        jdk = extract(z, apps)

    notes = apps / "GHIDRA-PATHS.txt"
    notes.write_text("GHIDRA={}\nJDK={}\nJAVA_HOME={}\n".format(ghidra, jdk, jdk),
                     encoding="utf-8")
    print("\n就绪：\n  GHIDRA={}\n  JDK={}\n  已写入 {}".format(ghidra, jdk, notes))
    return 0


if __name__ == "__main__":
    sys.exit(main())
