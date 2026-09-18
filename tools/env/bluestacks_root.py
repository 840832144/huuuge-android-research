#!/usr/bin/env python3
"""BlueStacks root 标准化 —— 在任意一台机器上复刻"研究实例可 root"的环境。

做三件事（就三件：能打吗 / 打了没有 / 怎么退；不做 manifest 哈希、不做多项测试门禁）：
  1. HD-Player.exe : _isDiskVerificationRequired() 序言 -> 31 C0 C3
                     （唯一总开关：完整性检查跳过 + developer mode 打开 -> guest su 放行）
                     plrCheckDiskIntegrity 调用 -> B0 01 90 90 90
  2. HD-MultiInstanceManager.exe : 重置 enable_root_access 的调用 -> 5x NOP
                     （蓝叠不再把开关改回 0）
  3. bluestacks.conf : 指定实例 enable_root_access="1"（字节级、不带 BOM）
  4. Data.vhdx（可选）: gated guest su -> B0 01 C3（仅当 1 仍不足时需要）

补丁按**签名定位**（复用上游 locator），不是死偏移；找不到就报"版本不匹配"，不乱写。

用法：
  python tools/env/bluestacks_root.py check  <实例名>
  python tools/env/bluestacks_root.py apply  <实例名>        # 需管理员终端
  python tools/env/bluestacks_root.py revert                 # 用上游的 .prepatch.bak 还原

上游（固定提交，已审计）：RobThePCGuy/BlueStacks-Root-GUI
  7002d185522c41a15ea9b184eff24393c5a62a11
  clone 到以下任一处即可被自动找到：./BlueStacks-Root-GUI、
  tools/thirdparty/BlueStacks-Root-GUI，或用 --upstream / 环境变量 BS_ROOT_GUI 指定。
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import subprocess
import sys
import time

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = pathlib.Path(__file__).resolve().parent
BLUESTACKS_PROCS = ("HD-Player.exe", "HD-MultiInstanceManager.exe", "BstkSVC.exe",
                    "BlueStacksServices.exe", "BlueStacksAppPlayer.exe", "BstkVMMgr.exe")


def say(msg=""):
    print(msg, flush=True)


def ok(msg):
    say("  [OK]  " + msg)


def bad(msg):
    say("  [!!]  " + msg)


def info(msg):
    say("  ...   " + msg)


def is_admin() -> bool:
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def find_upstream(explicit: str) -> str:
    cands = [explicit, os.environ.get("BS_ROOT_GUI", ""),
             str(pathlib.Path.cwd() / "BlueStacks-Root-GUI"),
             str(HERE.parent / "thirdparty" / "BlueStacks-Root-GUI"),
             str(HERE / "BlueStacks-Root-GUI")]
    for c in cands:
        if c and os.path.isfile(os.path.join(c, "integrity_patch.py")):
            return c
    return ""


def find_install_dir() -> str:
    """从注册表拿安装目录；两套安装（_cn 与 nxt）都查。"""
    try:
        import winreg
    except Exception:
        return ""
    for key in (r"SOFTWARE\BlueStacks_nxt_cn", r"SOFTWARE\BlueStacks_nxt",
                r"SOFTWARE\WOW6432Node\BlueStacks_nxt_cn", r"SOFTWARE\WOW6432Node\BlueStacks_nxt"):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as k:
                d = winreg.QueryValueEx(k, "InstallDir")[0]
                if d and os.path.isfile(os.path.join(d, "HD-Player.exe")):
                    return d
        except OSError:
            continue
    return ""


def find_conf(explicit: str) -> str:
    cands = [explicit]
    try:
        import winreg
        for key in (r"SOFTWARE\BlueStacks_nxt_cn", r"SOFTWARE\BlueStacks_nxt"):
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as k:
                for val in ("UserDefinedDir", "DataDir"):
                    try:
                        d = winreg.QueryValueEx(k, val)[0]
                        if d:
                            cands.append(os.path.join(d, "bluestacks.conf"))
                    except OSError:
                        pass
    except Exception:
        pass
    cands += [r"D:\BlueStacks_nxt_cn\bluestacks.conf",
              r"C:\ProgramData\BlueStacks_nxt\bluestacks.conf",
              r"C:\ProgramData\BlueStacks_nxt_cn\bluestacks.conf"]
    for c in cands:
        if c and os.path.isfile(c):
            return c
    return ""


def find_vhdx(instance: str, conf: str) -> str:
    conf_dir = os.path.dirname(conf) if conf else ""
    cands = []
    for base in (conf_dir, os.path.dirname(conf_dir)):
        if base:
            cands += [os.path.join(base, "Engine", instance, "Data.vhdx"),
                      os.path.join(base, instance, "Data.vhdx"),
                      os.path.join(base, "Engine", instance, "Root.vhd")]
    for c in cands:
        if os.path.isfile(c):
            return c
    return ""


def load_upstream(path: str):
    if not path:
        raise SystemExit(
            "找不到上游工具目录（需要 integrity_patch.py）。\n"
            "先 clone 并切到固定提交：\n"
            "  git clone https://github.com/RobThePCGuy/BlueStacks-Root-GUI\n"
            "  cd BlueStacks-Root-GUI && git checkout 7002d185522c41a15ea9b184eff24393c5a62a11\n"
            "然后用 --upstream <路径> 指定（或在仓库根放一份）。")
    sys.path.insert(0, path)
    import integrity_patch  # noqa: E402
    import root_persistence  # noqa: E402
    return integrity_patch, root_persistence


def _dry(spec, path, ip) -> str:
    """在内存副本上跑 locator+比对，不落盘：已补丁 / 未补丁 / 版本不匹配。"""
    if not os.path.isfile(path):
        return "文件不存在"
    data = bytearray(open(path, "rb").read())
    try:
        status = ip._apply_to_buffer(data, spec)
    except Exception as exc:
        return "版本不匹配（{}）".format(str(exc)[:70])
    if status.startswith("already patched"):
        return "已补丁"
    if status.startswith("patched"):
        return "未补丁"
    return "找不到该检查"


def su_offline(args, target: str, mode: str) -> str:
    script = os.path.join(args.upstream, "su_patch_offline.py")
    if not os.path.isfile(script):
        return "上游缺 su_patch_offline.py"
    cmd = [sys.executable, script, target] + ([mode] if mode else [])
    r = subprocess.run(cmd, cwd=args.upstream, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=900)
    out = ((r.stdout or "") + (r.stderr or "")).strip().splitlines()
    return "\n".join(out[-4:]) if out else "(无输出)"


def do_check(args) -> int:
    install = args.install_dir or find_install_dir()
    if not install:
        bad("找不到 BlueStacks 安装目录（用 --install-dir 指定）")
        return 1
    ip, rp = load_upstream(args.upstream)
    say("安装目录: {}".format(install))
    say("\n主机侧补丁：")
    for spec in (ip.UNLOCK_PLAYER, ip.DISK_INTEGRITY_CALL):
        say("  HD-Player.exe {:<50} {}".format(spec.name[:50],
                                              _dry(spec, os.path.join(install, "HD-Player.exe"), ip)))
    say("  HD-MultiInstanceManager.exe {:<34} {}".format(
        "停止重置 enable_root_access",
        _dry(rp.ROOT_RESET_NOP, os.path.join(install, "HD-MultiInstanceManager.exe"), ip)))

    conf = args.conf or find_conf(args.conf)
    say("")
    if conf:
        txt = open(conf, encoding="utf-8", errors="replace").read()
        flags = dict(re.findall(r'bst\.instance\.([^.]+)\.enable_root_access="([01])"', txt))
        say("实例 root 开关（{}）:".format(conf))
        for name, v in sorted(flags.items()):
            say("  [OK]  {} = {}{}".format(name, v, "   （已开）" if v == "1" else ""))
    else:
        bad("找不到 bluestacks.conf（用 --conf 指定）")

    inst = args.instance
    if inst and conf:
        vhdx = find_vhdx(inst, conf)
        say("")
        if vhdx:
            say("镜像侧 guest su（{}）:".format(vhdx))
            for line in su_offline(args, vhdx, "").splitlines()[-3:]:
                say("  " + line)
        else:
            info("没找到 {} 的 Data.vhdx（实例名不对？或该实例还没启动过）".format(inst))
    say("")
    say("说明（就这一条）：主机侧三项『已补丁』+ 目标实例开关为 1 = 环境就绪。")
    say("  · 只有『实际 root 不通』时才需要动镜像侧；扫描显示 no gated su found 通常是因为")
    say("    主机补丁生效后蓝叠已替换 guest su，属正常，不必处理。")
    say("  · 唯一真正要看的验证：启动实例后 `adb -s 127.0.0.1:<端口> shell \"su -c id\"` → uid=0。")
    return 0


def stop_bluestacks() -> None:
    for name in BLUESTACKS_PROCS:
        subprocess.run(["taskkill", "/IM", name, "/F"], capture_output=True)
    time.sleep(2)
    left = [n for n in BLUESTACKS_PROCS
            if n.lower() in subprocess.run(["tasklist", "/FI", "IMAGENAME eq " + n],
                                           capture_output=True, text=True,
                                           encoding="utf-8", errors="replace").stdout.lower()]
    ok("BlueStacks 进程已退出" if not left else "仍在运行: {}".format(", ".join(left)))


def set_instance_root(conf: str, instance: str) -> None:
    p = pathlib.Path(conf)
    raw = p.read_bytes()
    if raw[:3] == b"\xef\xbb\xbf":
        raise SystemExit("bluestacks.conf 带 BOM —— 先处理编码（BOM 会让 BlueStacks 起不来）")
    txt = raw.decode("utf-8", errors="replace")
    key = "bst.instance.{}.enable_root_access=".format(instance)
    if key not in txt:
        raise SystemExit("配置里没有 {}（实例名写对了吗？）".format(key))
    new = re.sub(re.escape(key) + r'"\d"', key + '"1"', txt)
    if new != txt:
        p.write_bytes(new.encode("utf-8"))
        ok("{}enable_root_access 设为 1".format(key))
    else:
        ok("{}enable_root_access 已是 1（未改动）".format(key))


def do_apply(args) -> int:
    install = args.install_dir or find_install_dir()
    ip, rp = load_upstream(args.upstream)
    if not install:
        bad("找不到安装目录")
        return 1
    if not is_admin():
        bad("需要管理员权限（要写 Program Files 并关闭蓝叠进程）—— 请用管理员终端重跑")
        return 1
    conf = args.conf or find_conf(args.conf)
    say("1) 停止 BlueStacks（改主机二进制前必须全停）")
    stop_bluestacks()
    say("\n2) 打主机侧补丁（上游自动留 .prepatch.bak 以便还原）")
    for line in ip.patch_installation(install):
        ok(line)
    for line in rp.patch_root_persistence(install):
        ok(line)
    say("")
    if args.instance and conf:
        say("3) 打开该实例的 root 开关" + ("，并放开镜像侧 guest su" if not args.no_su else ""))
        set_instance_root(conf, args.instance)
        vhdx = find_vhdx(args.instance, conf)
        if args.no_su:
            info("按要求跳过镜像侧（--no-su）")
        elif vhdx:
            say("  " + su_offline(args, vhdx, "--enable").replace("\n", "\n  "))
        else:
            bad("没找到 {} 的 Data.vhdx —— 先启动该实例一次再重跑本步".format(args.instance))
    else:
        info("未指定实例名，跳过实例开关（用法：apply <实例名>）")
    say("\n完成。下一步：启动该实例，然后验证一条命令：")
    say("  adb -s 127.0.0.1:<端口> shell \"su -c id\"     # 期望 uid=0(root)")
    say("提示：首次启动后 su 才会出现；若仍被拒，重启一次实例再试。")
    return 0


def do_revert(args) -> int:
    install = args.install_dir or find_install_dir()
    ip, rp = load_upstream(args.upstream)
    if not is_admin():
        bad("需要管理员权限")
        return 1
    stop_bluestacks()
    for line in ip.patch_installation(install, restore=True):
        ok(line)
    for line in rp.patch_root_persistence(install, restore=True):
        ok(line)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", choices=("check", "apply", "revert"))
    ap.add_argument("instance", nargs="?", default="", help="check/apply 用：实例名（如 Pie64_1）")
    ap.add_argument("--upstream", default="", help="上游工具目录（默认自动查找）")
    ap.add_argument("--install-dir", default="", help="BlueStacks 安装目录")
    ap.add_argument("--conf", default="", help="bluestacks.conf 路径")
    ap.add_argument("--no-su", action="store_true", help="apply 时跳过镜像侧 guest su 补丁")
    args = ap.parse_args()
    args.upstream = find_upstream(args.upstream)
    return {"check": do_check, "apply": do_apply, "revert": do_revert}[args.action](args)


if __name__ == "__main__":
    sys.exit(main())
