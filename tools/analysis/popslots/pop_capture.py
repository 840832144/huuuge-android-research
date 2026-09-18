#!/usr/bin/env python3
"""Pop! Slots 采集向导（面向不写代码的使用者）——菜单式，四步完成。

采集路线说明：Pop! Slots 的引擎 **不读 Android 全局代理**（实测：它直连 :443，
不经过代理），所以不能用"设代理 + mitmproxy"。本工具走 **Frida 挂 curl 边界**，
在引擎收到明文的位置取数据 —— 使用者不需要写任何 hook 代码。

菜单：
  1 环境检查（不采集，先看是否就绪；会明确告诉你缺什么）
  2 开始采集（挂上引擎，开始在后台记录）
  3 停止采集
  4 导出数值（生成 slots_values.csv）+ 查看抓到哪些端点/模块
  0 退出

首次使用需要一次 frida-server（官方公开下载，见 --help 或文档），装它只需一条命令：
  python pop_capture.py setup-frida <你下载的 frida-server 文件路径>

用法：
  python pop_capture.py --serial <你的adb串号>                 # 进菜单（推荐）
  python pop_capture.py --serial <串号> check|start|stop|export
  python pop_capture.py --serial <串号> setup-frida <frida-server路径>
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import socket
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pop_common as pc  # noqa: E402

TOOLS_CAPTURE = HERE.parents[1] / "capture"
DEFAULT_PORT = "27042"


def say(msg: str) -> None:
    print(msg, flush=True)


def ok(msg: str) -> None:
    say("  [ok]   " + msg)


def bad(msg: str) -> None:
    say("  [缺]   " + msg)


def info(msg: str) -> None:
    say("  ...    " + msg)


def outdir(args) -> pathlib.Path:
    d = pathlib.Path(args.outdir).expanduser().resolve()
    d.mkdir(parents=True, exist_ok=True)
    return d


def state_file(args) -> pathlib.Path:
    return outdir(args) / "capture_state.json"


def load_state(args) -> dict:
    p = state_file(args)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_state(args, data: dict) -> None:
    state_file(args).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


def frida_alive(addr: str) -> bool:
    host, _, port = addr.rpartition(":")
    try:
        with socket.create_connection((host or "127.0.0.1", int(port)), timeout=3):
            return True
    except Exception:
        return False


# ------------------------------------------------------------------ 步骤

def do_check(args) -> int:
    doctor = HERE / "pop_doctor.py"
    cmd = [sys.executable, str(doctor), "--serial", args.serial or "",
           "--frida", args.frida]
    if args.adb:
        cmd += ["--adb", args.adb]
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    say(r.stdout.strip())
    if r.returncode != 0:
        say("")
        say("把上面的 [MISS] 补齐后重试；frida-server 尚未安装时可用：")
        say("  python pop_capture.py --serial <串号> setup-frida <frida-server文件>")
    return r.returncode


ARCH_MAP = {"x86_64": "x86_64", "x86": "x86", "arm64-v8a": "arm64", "armeabi-v7a": "arm"}


def _local_frida_version() -> str:
    try:
        import frida
        return getattr(frida, "__version__", "") or ""
    except Exception:
        return ""


def fetch_frida_server(serial: str, adb_exe: str, dest_dir: pathlib.Path) -> pathlib.Path:
    """按本机 frida 版本 + 设备 ABI 从官方 releases 拉取匹配的 frida-server。

    省掉使用者"自己找版本、自己解压"这一步；产物是公开文件，不依赖任何人。
    """
    import lzma
    import urllib.request

    ver = _local_frida_version()
    if not ver:
        raise SystemExit("本机没有 frida：先执行  pip install frida frida-tools")
    abi = (pc.adb_shell(serial, "getprop ro.product.cpu.abi", adb_exe=adb_exe) or "").strip()
    arch = ARCH_MAP.get(abi)
    if not arch:
        raise SystemExit("无法识别设备 ABI（{}）".format(abi or "未知"))
    name = "frida-server-{}-android-{}.xz".format(ver, arch)
    url = "https://github.com/frida/frida/releases/download/{}/{}".format(ver, name)
    dest = dest_dir / name.replace(".xz", "")

    info("下载 {} ...".format(name))
    with urllib.request.urlopen(url, timeout=180) as resp:
        raw = resp.read()
    dest.write_bytes(lzma.decompress(raw))
    ok("已下载并解压：{}（{:.1f} MB）".format(dest, dest.stat().st_size / 1048576))
    return dest


def do_setup_frida(args) -> int:
    serial = pc.resolve_serial(args.serial, args.adb)
    src = pathlib.Path(args.frida_server) if args.frida_server else None
    if src is None or not src.exists():
        if not args.download:
            say("用法：python pop_capture.py --serial <串号> setup-frida <frida-server 文件路径>")
            say("     或让它自己下载匹配版本：... setup-frida --download")
            return 1
        try:
            src = fetch_frida_server(serial, args.adb, outdir(args))
        except SystemExit as exc:
            bad(str(exc))
            return 1
        except Exception as exc:
            bad("下载失败（{}）。可改为手动下载后把文件路径作为参数传入".format(exc))
            return 1

    say("安装 frida-server 到实例 {}".format(serial))
    dst = "/data/local/tmp/fs"

    info("推送 ...")
    r = pc.adb(serial, "push", str(src), dst, adb_exe=args.adb, timeout=300)
    if "error" in r.lower() and "pushed" not in r.lower():
        bad(r)
        return 1
    ok("已推送")

    mode = pc.root_mode(serial, args.adb)
    if mode == "none":
        bad("实例没有 root（adbd 与 su 都不可用）：先 `adb -s {} root` 或打开实例 root".format(serial))
        return 1

    info("以 root 启动（root 通道：{}）...".format(mode))
    port = args.frida.rsplit(":", 1)[-1]
    pc.adb_su(serial, "chmod 755 {}".format(dst), adb_exe=args.adb)
    # -D 后台常驻；分两种启动方式各试一次，最后以端口连通为准（比解析 ps 可靠）
    for attempt, cmd in enumerate((
            "{} -D >/dev/null 2>&1 &".format(dst),
            "nohup {} -D >/dev/null 2>&1 &".format(dst))):
        pc.adb_su(serial, cmd, adb_exe=args.adb)
        time.sleep(3)
        pc.adb(serial, "forward", "tcp:{}".format(port), "tcp:27042", adb_exe=args.adb)
        if frida_alive(args.frida):
            ok("frida-server 正在运行，端口转发正常（{}）".format(args.frida))
            say("")
            say("好了。现在可以选 1 复查，然后选 2 开始采集。")
            return 0
        if attempt == 0:
            info("第一次启动没连上，换个方式再试 ...")

    info("最后再确认一次设备端进程：")
    ps = pc.adb_shell(serial, "ps -A | grep -v grep | grep fs", adb_exe=args.adb)
    say("  " + (ps.replace("\n", "\n  ") or "(设备上没有 fs 进程)"))
    bad("端口 {} 仍不通。手动排查：".format(args.frida))
    say("  adb -s {s} shell \"su -c '{dst} -D &'\"        # 或 adb root 后去掉 su -c".format(
        s=serial, dst=dst))
    say("  adb -s {s} forward tcp:{p} tcp:27042".format(s=serial, p=port))
    return 1


def do_start(args) -> int:
    st = load_state(args)
    if st.get("pid"):
        say("已经在采集（pid {}）。先选 3 停止。".format(st["pid"]))
        return 1
    if not frida_alive(args.frida):
        bad("frida-server 没在 {} 上监听。先执行 setup-frida，或选 1 看缺什么。".format(args.frida))
        return 1

    serial = pc.resolve_serial(args.serial, args.adb)
    pid = pc.resolve_pid(serial, args.package, args.adb)
    if not pid:
        bad("游戏没在运行：先打开 Pop! Slots 并进入大厅")
        return 1

    out = outdir(args) / "pop_net.jsonl"
    log = outdir(args) / "capture.log"
    cmd = [sys.executable, str(HERE / "pop_net_capture.py"), serial, "86400",
           "--frida", args.frida, "--out", str(out), "--quiet"]
    if args.adb:
        cmd += []          # pop_net_capture 走 pop_common 的 adb 查找
    proc = subprocess.Popen(cmd, stdout=log.open("a", encoding="utf-8"),
                            stderr=subprocess.STDOUT)
    time.sleep(4)
    if proc.poll() is not None:
        bad("采集进程启动失败，看日志：{}".format(log))
        return 1
    save_state(args, {"pid": proc.pid, "serial": serial, "out": str(out), "log": str(log)})

    ok("采集已开始（pid {}）".format(proc.pid))
    say("")
    say("现在去游戏里操作：进机台 → 点 SPIN 转盘（想采哪个模块就玩哪个模块）。")
    say("采完回到这里选 3 停止，再选 4 导出数值。")
    return 0


def do_stop(args) -> int:
    st = load_state(args)
    pid = st.get("pid")
    if not pid:
        say("没有正在进行的采集。")
        return 0
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True)
        else:
            os.kill(pid, 15)
        ok("已停止采集（pid {}）".format(pid))
    except Exception as exc:
        info("停止时提示：{}".format(exc))
    st["pid"] = None
    save_state(args, st)
    out = pathlib.Path(st.get("out") or (outdir(args) / "pop_net.jsonl"))
    if out.exists():
        n = sum(1 for _ in out.open(encoding="utf-8-sig"))
        ok("采集文件：{}（{} 条记录）".format(out, n))
    say("")
    say("接着选 4 导出数值。")
    return 0


def do_export(args) -> int:
    st = load_state(args)
    cap = pathlib.Path(st.get("out") or (outdir(args) / "pop_net.jsonl"))
    if not cap.exists():
        bad("还没有采集文件（{}）。先选 2 采集。".format(cap))
        return 1

    say("一、抓到哪些端点")
    r = subprocess.run([sys.executable, str(TOOLS_CAPTURE / "endpoints.py"), str(cap),
                        "--show-body", "3"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    say(r.stdout.strip() or r.stderr.strip())

    say("")
    say("二、导出老虎机数值（CSV）")
    r = subprocess.run([sys.executable, str(HERE / "pop_spin_export.py"), str(cap),
                        "--outdir", str(outdir(args))], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    say(r.stdout.strip() or r.stderr.strip())
    say("")
    say("如需按模块拆分（例如只要老虎机），可用：")
    say("  python {} {} --modules <你的modules.json> --module slots --out {}/slots.jsonl".format(
        TOOLS_CAPTURE / "select_module.py", cap, outdir(args)))
    return 0


def menu(args) -> int:
    while True:
        say("")
        say("Pop! Slots 采集向导     实例: {}".format(args.serial or "(自动探测)"))
        say("  1 环境检查（不采集）")
        say("  2 开始采集")
        say("  3 停止采集")
        say("  4 导出数值 / 查看端点")
        say("  0 退出")
        try:
            c = input("请选择: ").strip()
        except EOFError:
            return 0
        if c == "1":
            do_check(args)
        elif c == "2":
            do_start(args)
        elif c == "3":
            do_stop(args)
        elif c == "4":
            do_export(args)
        elif c in ("0", "q"):
            return 0
        else:
            say("请输入 0-4。")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", nargs="?", default="menu",
                    choices=("menu", "check", "start", "stop", "export", "setup-frida"))
    ap.add_argument("frida_server", nargs="?", default="",
                    help="setup-frida 用：你下载的 frida-server 文件路径（给 --download 时不必填）")
    ap.add_argument("--download", action="store_true",
                    help="setup-frida 用：按本机 frida 版本 + 设备 ABI 自动从官方 releases 下载")
    ap.add_argument("--serial", default=os.environ.get("POP_SERIAL", ""))
    ap.add_argument("--package", default=pc.DEFAULT_PACKAGE)
    ap.add_argument("--frida", default=os.environ.get("POP_FRIDA", "127.0.0.1:" + DEFAULT_PORT))
    ap.add_argument("--outdir", default="pop_capture")
    ap.add_argument("--adb", default="")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    if args.action == "menu":
        return menu(args)
    return {"check": do_check, "start": do_start, "stop": do_stop,
            "export": do_export, "setup-frida": do_setup_frida}[args.action](args)


if __name__ == "__main__":
    sys.exit(main())
