#!/usr/bin/env python3
"""Install a mitmproxy CA into an Android instance's system trust store.

/system is read-only on these images, so the CA goes into a writable directory on
/data and that directory is bind-mounted over /system/etc/security/cacerts.

Portable: no adb path, instance serial or certificate hash is baked in — pass the
serial (or have exactly one device connected) and the certificate; the Android
file name is computed from the certificate itself. Both root channels work
(adbd-root, where the shell is already uid 0, and a `su` binary).

Usage:
  python try_bind_cacert.py --serial <serial> [--cert <mitmproxy-ca-cert.pem>]

Environment: POP_SERIAL, ADB, CA_LOCAL (path to the PEM) are honoured.
"""
from __future__ import annotations

import argparse
import os
import pathlib
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "capture"))
import ca_util  # noqa: E402


def adb_path(cli: str = "") -> str:
    for cand in (cli, os.environ.get("ADB", "")):
        if cand and pathlib.Path(cand).exists():
            return str(cand)
    found = shutil.which("adb")
    if found:
        return found
    for cand in (r"C:\platform-tools\adb.exe", "/usr/bin/adb", "/usr/local/bin/adb"):
        if pathlib.Path(cand).exists():
            return cand
    return "adb"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--serial", default=os.environ.get("POP_SERIAL", ""),
                    help="adb serial; auto-detected when exactly one device is connected")
    ap.add_argument("--cert", default=os.environ.get("CA_LOCAL", "mitmproxy-ca-cert.pem"),
                    help="local PEM of the CA to install")
    ap.add_argument("--adb", default="", help="path to adb (default: $ADB, PATH, platform-tools)")
    ap.add_argument("--dir", default="/data/local/cacerts", help="device-side staging dir")
    args = ap.parse_args()

    adb = adb_path(args.adb)
    pem = pathlib.Path(args.cert)
    if not pem.exists():
        print("找不到证书：{}（先跑一次 mitmdump 生成，或用 --cert 指定）".format(pem),
              file=sys.stderr)
        return 1

    def run(*cmd, timeout=60):
        r = subprocess.run([adb, *cmd], capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return ((r.stdout or "") + (r.stderr or "")).strip()

    serial = args.serial
    if not serial:
        out = run("devices")
        devices = [l.split()[0] for l in out.splitlines()[1:]
                   if len(l.split()) >= 2 and l.split()[1] == "device"]
        if len(devices) != 1:
            print("设备数不是 1（{}）：请用 --serial 指定".format(devices or "无"), file=sys.stderr)
            return 1
        serial = devices[0]

    def sh(command: str) -> str:
        return run("-s", serial, "shell", command)

    # root channel: adbd-root first, then su
    root_prefix = ""
    if "uid=0" not in sh("id"):
        if "uid=0" in sh("su -c id"):
            root_prefix = "su -c "
        else:
            print("实例没有 root（adbd 与 su 都不可用）：先 `adb -s {} root` 或为实例打开 root".format(serial),
                  file=sys.stderr)
            return 1

    def root_sh(command: str) -> str:
        return sh(root_prefix + "'" + command + "'") if root_prefix else sh(command)

    name = ca_util.android_cert_hash(pem)
    print("设备: {}   root 通道: {}".format(serial, "su" if root_prefix else "adbd(uid 0)"))
    print("证书: {}  →  Android 文件名 {}".format(pem, name))

    print("== 推送证书 ==")
    print(run("-s", serial, "push", str(pem), "/data/local/tmp/mitm-ca.pem"))

    print("== 写入可写目录 ==")
    print(root_sh("mkdir -p {d} && cp /data/local/tmp/mitm-ca.pem {d}/{n} && chmod 644 {d}/{n}".format(
        d=args.dir, n=name)))

    print("== bind-mount 覆盖系统信任区 ==")
    print(root_sh("mount -o bind {d} /system/etc/security/cacerts 2>&1 || echo FAIL".format(d=args.dir)))

    print("== 校验 ==")
    verify = root_sh("ls /system/etc/security/cacerts/{n} 2>&1".format(n=name))
    if name in verify:
        print("OK：证书已在系统信任区（{}）".format(verify.strip()))
        return 0
    print("失败：{}".format(verify.strip()))
    print("提示：该实例可能需要在每次重启后重做本步骤。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
