#!/usr/bin/env python3
"""Pop! Slots 采集向导 —— 面向不写代码的使用者，菜单式一键操作。

把"装证书 / 设代理 / 起采集 / 停止清理 / 看采集到什么"全部封装成菜单项，
不需要手敲 adb / mitmproxy 命令，也不需要自己算证书哈希。

用法：
  python pop_capture.py --serial <你的adb串号>            # 进菜单（推荐）
  python pop_capture.py --serial <串号> check            # 只做环境检查
  python pop_capture.py --serial <串号> start            # 开始采集
  python pop_capture.py --serial <串号> stop             # 停止并清理
  python pop_capture.py --serial <串号> report           # 看采集到什么 + 选模块

菜单：
  1 环境检查（不采集，先看能不能采）
  2 开始采集（自动装证书 + 设代理 + 起 mitmproxy）
  3 停止并清理（清代理 + 停 mitmproxy）
  4 查看采集结果 / 挑选模块导出
  0 退出

说明：采集本身是"模块无关"的——先全采，之后用第 4 项挑你要的模块（例如老虎机）。
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pop_common as pc  # noqa: E402

DEFAULT_PORT = "8080"
DEFAULT_HOST_IP = "10.0.2.2"          # BlueStacks：设备视角下的宿主机
CA_NAME = "mitm-ca.pem"
DEV_CA = "/data/local/tmp/" + CA_NAME
DEV_DIR = "/data/local/cacerts"


# ---------------------------------------------------------------- helpers

def say(msg: str) -> None:
    print(msg, flush=True)


def step_ok(msg: str) -> None:
    say("  [ok]   " + msg)


def step_bad(msg: str) -> None:
    say("  [MISS] " + msg)


def step_info(msg: str) -> None:
    say("  ...    " + msg)


def capture_dir(args) -> pathlib.Path:
    d = pathlib.Path(args.outdir).expanduser().resolve()
    d.mkdir(parents=True, exist_ok=True)
    return d


def state_path(args) -> pathlib.Path:
    return capture_dir(args) / "pop_capture_state.json"


def load_state(args) -> dict:
    p = state_path(args)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_state(args, data: dict) -> None:
    state_path(args).write_text(json.dumps(data, ensure_ascii=False, indent=1),
                                encoding="utf-8")


def mitmdump_exe(args) -> str:
    cand = args.mitmdump or os.environ.get("MITMDUMP", "")
    if cand and pathlib.Path(cand).exists():
        return cand
    found = shutil.which("mitmdump") or shutil.which("mitmdump.exe")
    if found:
        return found
    # the common per-user Python Scripts location
    scripts = pathlib.Path(os.environ.get("APPDATA", "")) / "Python" / "Python312" / "Scripts"
    for name in ("mitmdump.exe", "mitmdump"):
        p = scripts / name
        if p.exists():
            return str(p)
    return ""


def ca_hash(path: pathlib.Path) -> str:
    """Android 系统证书文件名：subject_hash_old（用 cryptography 计算）。"""
    try:
        from cryptography import x509
        import base64
        import hashlib
        import re
        import struct
    except Exception:
        raise SystemExit("缺少 cryptography：请先执行  pip install cryptography")
    pem = path.read_bytes()
    m = re.search(rb"-----BEGIN CERTIFICATE-----(.*?)-----END CERTIFICATE-----", pem, re.S)
    if not m:
        raise SystemExit("{} 不是 PEM 证书".format(path))
    der = base64.b64decode(m.group(1).strip())
    cert = x509.load_der_x509_certificate(der)
    digest = hashlib.sha1(cert.subject.public_bytes()).digest()
    return "%08x.0" % struct.unpack("<I", digest[:4])[0]


# ---------------------------------------------------------------- actions

def ensure_ca(args, mitm_dir: pathlib.Path) -> pathlib.Path:
    """确保 mitmproxy 的 CA 已生成，返回 PEM 路径。"""
    pem = mitm_dir / "mitmproxy-ca-cert.pem"
    if pem.exists():
        return pem
    exe = mitmdump_exe(args)
    if not exe:
        raise SystemExit("找不到 mitmdump：请先  pip install mitmproxy")
    step_info("首次运行 mitmproxy 生成证书 ...")
    # 让它跑一下再杀掉——首次启动即会创建 CA
    proc = subprocess.Popen([exe, "--listen-port", str(args.port), "--set", "confdir={}".format(mitm_dir)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(40):
        if pem.exists():
            break
        time.sleep(0.25)
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except Exception:
        proc.kill()
    if not pem.exists():
        raise SystemExit("生成证书失败：{} 不存在".format(pem))
    return pem


def do_check(args) -> int:
    say("环境检查")
    ok = True

    adb = pc.adb_path(args.adb)
    if pathlib.Path(adb).exists():
        step_ok("adb: {}".format(adb))
    else:
        step_bad("找不到 adb（可用 --adb 指定）")
        return 1

    try:
        serial = pc.resolve_serial(args.serial, args.adb)
        step_ok("设备: {}".format(serial))
    except SystemExit as exc:
        step_bad(str(exc))
        return 1

    abi = pc.adb_shell(serial, "getprop ro.product.cpu.abi", adb_exe=args.adb)
    step_ok("ABI: {}".format(abi or "(未知)"))

    apk = ""
    for line in pc.adb_shell(serial, "pm path {}".format(args.package), adb_exe=args.adb).splitlines():
        if line.startswith("package:"):
            apk = line.split("package:", 1)[1].strip()
            break
    if apk:
        step_ok("游戏已安装")
    else:
        step_bad("{} 没装在这个实例上".format(args.package))
        ok = False

    mode = pc.root_mode(serial, args.adb)
    if mode in ("adbd", "su"):
        step_ok("root 通道: {}".format("adbd（adb root）" if mode == "adbd" else "su"))
    else:
        step_bad("没有 root：先执行  adb -s {} root   或为实例打开 root".format(serial))
        ok = False

    if mitmdump_exe(args):
        step_ok("mitmdump: {}".format(mitmdump_exe(args)))
    else:
        step_bad("找不到 mitmdump：pip install mitmproxy")
        ok = False

    try:
        import cryptography  # noqa: F401
        step_ok("cryptography 可用（用于算证书文件名）")
    except Exception:
        step_bad("缺少 cryptography：pip install cryptography")
        ok = False

    say("")
    if ok:
        say("结论：可以采集。选菜单 2 开始。")
        return 0
    say("结论：还差上面的 [MISS] 项，补齐后再试。")
    return 1


def do_start(args) -> int:
    d = capture_dir(args)
    mitm_dir = d / "mitm"
    mitm_dir.mkdir(parents=True, exist_ok=True)
    state = load_state(args)
    if state.get("pid"):
        say("似乎已经在采集（pid {}）。先选 3 停止。".format(state["pid"]))
        return 1

    try:
        serial = pc.resolve_serial(args.serial, args.adb)
    except SystemExit as exc:
        step_bad(str(exc))
        return 1

    say("开始采集（实例 {}）".format(serial))

    pem = ensure_ca(args, mitm_dir)
    h = ca_hash(pem)
    step_ok("证书: {}  → 系统文件名 {}".format(pem, h))

    step_info("推送到设备 ...")
    out = pc.adb(serial, "push", str(pem), DEV_CA, adb_exe=args.adb)
    if "error" in out.lower() and "pushed" not in out.lower():
        step_bad(out)
        return 1

    step_info("装进系统信任区（/system 只读时用 bind-mount）...")
    r = pc.adb_su(serial, "mkdir -p {d} && cp {src} {d}/{h} && chmod 644 {d}/{h}".format(
        d=DEV_DIR, src=DEV_CA, h=h), adb_exe=args.adb)
    if r.startswith("[no root"):
        step_bad(r)
        return 1
    r = pc.adb_su(serial, "mount -o bind {d} /system/etc/security/cacerts".format(d=DEV_DIR),
                  adb_exe=args.adb)
    check = pc.adb_su(serial, "ls /system/etc/security/cacerts/{}".format(h), adb_exe=args.adb)
    if h in check:
        step_ok("证书已在系统信任区")
    else:
        step_bad("证书没装进去：{}".format(check))
        return 1

    step_info("设置设备代理 ...")
    pc.adb_shell(serial, "settings put global http_proxy {}:{}".format(args.host_ip, args.port),
                 adb_exe=args.adb)
    got = pc.adb_shell(serial, "settings get global http_proxy", adb_exe=args.adb)
    if ":" in got and "null" not in got:
        step_ok("代理: {}".format(got))
    else:
        step_bad("代理没设上（当前 {}）".format(got))

    addon = pathlib.Path(__file__).resolve().parents[2] / "capture" / "mitm_addon.py"
    if not addon.exists():
        raise SystemExit("找不到 addon：{}".format(addon))
    log = d / "mitmdump.log"
    exe = mitmdump_exe(args)
    env = dict(os.environ)
    env["MITM_OUT"] = str(d / "mitm_b64.jsonl")
    env["MITM_FILTER"] = args.filter
    proc = subprocess.Popen(
        [exe, "--listen-port", str(args.port), "--set", "confdir={}".format(mitm_dir),
         "-s", str(addon)],
        stdout=log.open("a", encoding="utf-8"), stderr=subprocess.STDOUT, env=env)
    time.sleep(2)
    if proc.poll() is not None:
        step_bad("mitmdump 启动失败，看日志：{}".format(log))
        return 1
    step_ok("mitmproxy 已在端口 {} 采集（pid {}）".format(args.port, proc.pid))

    save_state(args, {"pid": proc.pid, "serial": serial, "port": str(args.port),
                      "hash": h, "mitm_dir": str(mitm_dir), "out": str(d / "mitm_b64.jsonl"),
                      "addon": str(addon), "filter": args.filter})

    say("")
    say("现在去游戏里玩（要采集哪个模块就玩哪个模块，例如进机台转老虎机）。")
    say("玩完回到这里选 3 停止并清理。")
    return 0


def do_stop(args) -> int:
    state = load_state(args)
    say("停止并清理")
    if state.get("pid"):
        pid = state["pid"]
        try:
            subprocess.run(["taskkill", "/PID", str(pid), "/F"],
                           capture_output=True) if os.name == "nt" else os.kill(pid, 15)
            step_ok("已停止 mitmproxy（pid {}）".format(pid))
        except Exception as exc:
            step_info("停止 mitmproxy 时提示：{}".format(exc))
    else:
        step_info("没有记录到正在运行的 mitmproxy")

    serial = state.get("serial") or args.serial
    if serial:
        try:
            pc.adb_shell(serial, "settings put global http_proxy :0", adb_exe=args.adb)
            got = pc.adb_shell(serial, "settings get global http_proxy", adb_exe=args.adb)
            if got.strip() in (":0", "null", ""):
                step_ok("设备代理已清除（游戏可正常联网）")
            else:
                step_bad("代理仍是 {}，请手动清：settings put global http_proxy :0".format(got))
        except SystemExit as exc:
            step_info("清代理跳过：{}".format(exc))

    save_state(args, {})
    say("")
    say("清理完成。要看看采集到了什么，选 4。")
    return 0


def do_report(args) -> int:
    d = capture_dir(args)
    cap = pathlib.Path(load_state(args).get("out") or (d / "mitm_b64.jsonl"))
    if not cap.exists():
        say("还没采到东西（{} 不存在）。先选 2 采集，去游戏里玩一会儿。".format(cap))
        return 1

    tools = pathlib.Path(__file__).resolve().parents[2] / "capture"
    say("采集文件: {}".format(cap))
    say("")
    subprocess.run([sys.executable, str(tools / "endpoints.py"), str(cap), "--show-body", "5"])
    say("")
    mapping = d / "modules.json"
    if not mapping.exists():
        example = tools / "modules.example.json"
        shutil.copy2(example, mapping)
        say("已生成模块映射模板（请按上面的端点自己改）：{}".format(mapping))
    say("改好 {} 里的规则后，挑模块：".format(mapping))
    say("  python {} {} --modules {} --module <模块名> --out {}/<模块名>.jsonl".format(
        tools / "select_module.py", cap, mapping, d))
    return 0


# ---------------------------------------------------------------- menu

def menu(args) -> int:
    while True:
        say("")
        say("Pop! Slots 采集向导   实例: {}".format(args.serial or "(自动探测)"))
        say("  1 环境检查（不采集）")
        say("  2 开始采集")
        say("  3 停止并清理")
        say("  4 查看采集结果 / 挑选模块导出")
        say("  0 退出")
        try:
            choice = input("请选择: ").strip()
        except EOFError:
            return 0
        if choice == "1":
            do_check(args)
        elif choice == "2":
            do_start(args)
        elif choice == "3":
            do_stop(args)
        elif choice == "4":
            do_report(args)
        elif choice in ("0", "q", "exit"):
            return 0
        else:
            say("请输入 0-4。")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("action", nargs="?", default="menu",
                    choices=("menu", "check", "start", "stop", "report"))
    ap.add_argument("--serial", default=os.environ.get("POP_SERIAL", ""),
                    help="adb 串号；省略且只连一台设备时自动探测")
    ap.add_argument("--package", default=pc.DEFAULT_PACKAGE)
    ap.add_argument("--port", default=DEFAULT_PORT, help="mitmproxy 端口（默认 8080）")
    ap.add_argument("--host-ip", default=DEFAULT_HOST_IP,
                    help="设备视角下的宿主机 IP（BlueStacks 默认 10.0.2.2）")
    ap.add_argument("--outdir", default="pop_capture", help="采集与证书放这里")
    ap.add_argument("--filter", default="", help="可选：采集时正则过滤，例如 /slots/")
    ap.add_argument("--adb", default="", help="adb 路径（默认自动查找）")
    ap.add_argument("--mitmdump", default="", help="mitmdump 路径（默认自动查找）")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    if args.action == "menu":
        return menu(args)
    return {"check": do_check, "start": do_start, "stop": do_stop,
            "report": do_report}[args.action](args)


if __name__ == "__main__":
    sys.exit(main())
