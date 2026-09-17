#!/usr/bin/env python3
"""Shared helpers for the Pop! Slots analysis scripts.

Why this module exists: the first-generation scripts hardcoded this author's
machine paths, the game PID and raw symbol addresses, so they could not run on
another machine and broke on every game update. Everything here is resolved at
runtime and overridable from the CLI or the environment.

Common flags (added by ``add_common_args``):

  --serial SERIAL   adb serial or host:port of the target instance  (env POP_SERIAL,  default 127.0.0.1:5565)
  --frida ADDR      host:port of the forwarded frida-server         (env POP_FRIDA,   default 127.0.0.1:27044)
  --package NAME    game package name                               (env POP_PACKAGE, default com.playstudios.popslots)
  --pid PID         attach to this PID instead of detecting it
  --outdir DIR      directory for output files                      (env POP_OUTDIR,  default: current directory)
  --adb PATH        path to the adb binary                          (env ADB,         default: PATH, then common locations)

No symbol address is ever hardcoded: the JS prelude resolves the mangled names
from ``POP_SYMBOLS`` through the module export table at attach time, which is
ASLR-safe and survives most game updates as long as the symbol names do not
change.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys

DEFAULT_PACKAGE = "com.playstudios.popslots"
DEFAULT_SERIAL = "127.0.0.1:5565"
DEFAULT_FRIDA = "127.0.0.1:27044"
MODULE_NAME = "libBigCasino.so"

# Mangled (Itanium ABI) names of the symbols the tooling needs, keyed by a short
# logical name. Resolved at runtime, never used as an address.
POP_SYMBOLS = {
    # server-delivered lobby user records (identity: id / name / country / value)
    "parse_user_data": [
        "_ZN27CShakerServerUserDataParser13parseUserDataEPvP14CRoomUserModel",
        "parseUserData",
    ],
    # room / user management
    "room_users_manager_get_user": ["_ZNK17CRoomUsersManager17getUserByShakerIdEPKc"],
    "user_joined": ["_ZN20CAvatarJoinedHandler12onUserJoinedEPK6CEvent"],
    # avatar behaviour state machine
    "avatar_get_name": ["_ZN13CShakerAvatar7getNameEv"],
    "avatar_stop_walking": ["_ZN24CShakerAvatarWalkHandler11stopWalkingEP13CShakerAvatar"],
    "avatar_arrived_to_sit": [
        "_ZN37CShakerAvatarWalkToSitActivityHandler28onReachedDestinationCallbackEPvP6kmVec3",
    ],
    "avatar_stand_event": ["_ZN33CShakerAvatarStandActivityHandler21EVENT_AVATAR_STANDINGE"],
    # seat allocation
    "slots_finder_sit_user": ["_ZN12CSlotsFinder7sitUserEP13CGameableItemP13CShakerAvatarPKc"],
}


def add_common_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser.add_argument("--serial", default=os.environ.get("POP_SERIAL", DEFAULT_SERIAL),
                        help="adb serial or host:port (default: %(default)s)")
    parser.add_argument("--frida", default=os.environ.get("POP_FRIDA", DEFAULT_FRIDA),
                        help="forwarded frida-server host:port (default: %(default)s)")
    parser.add_argument("--package", default=os.environ.get("POP_PACKAGE", DEFAULT_PACKAGE),
                        help="game package (default: %(default)s)")
    parser.add_argument("--pid", type=int, default=None,
                        help="attach to this PID instead of detecting the game process")
    parser.add_argument("--outdir", default=os.environ.get("POP_OUTDIR", ""),
                        help="output directory (default: current directory)")
    parser.add_argument("--adb", default=os.environ.get("ADB", ""),
                        help="path to adb (default: PATH, then common install locations)")
    return parser


def parse_common(argv=None) -> argparse.Namespace:
    p = argparse.ArgumentParser(add_help=True)
    add_common_args(p)
    return p.parse_args(argv)


def adb_path(cli_value: str = "") -> str:
    """Resolve the adb binary: --adb, then $ADB, then PATH, then common paths."""
    for cand in (cli_value, os.environ.get("ADB", "")):
        if cand and pathlib.Path(cand).exists():
            return str(cand)
    found = shutil.which("adb")
    if found:
        return found
    for cand in (r"C:\platform-tools\adb.exe", r"C:\Program Files\platform-tools\adb.exe",
                 "/usr/bin/adb", "/usr/local/bin/adb"):
        if pathlib.Path(cand).exists():
            return cand
    # last resort: bare name so the error comes from adb itself
    return "adb"


def adb(serial: str, *args: str, adb_exe: str = "", timeout: int = 60) -> str:
    """Run an adb command against the explicit serial and return combined output."""
    cmd = [adb_path(adb_exe), "-s", serial, *args]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "(timeout)"
    return (r.stdout + r.stderr).strip()


def adb_shell(serial: str, command: str, adb_exe: str = "", timeout: int = 60) -> str:
    return adb(serial, "shell", command, adb_exe=adb_exe, timeout=timeout)


_ROOT_MODE: dict[str, str] = {}


def root_mode(serial: str, adb_exe: str = "") -> str:
    """Detect how this instance exposes root: 'adbd', 'su' or 'none'.

    Root channel differs per instance and is worth detecting instead of assuming:
    some images ship a `su` binary, while others are rooted through adbd
    (`adb root`) and have no `su` at all — a BlueStacks research instance was
    observed in that state, where `su -c` fails even though the shell is uid 0.
    """
    cached = _ROOT_MODE.get(serial)
    if cached:
        return cached
    if "uid=0" in adb_shell(serial, "id", adb_exe=adb_exe, timeout=30):
        mode = "adbd"
    elif "uid=0" in adb(serial, "shell", "su", "-c", "id", adb_exe=adb_exe, timeout=30):
        mode = "su"
    else:
        mode = "none"
    _ROOT_MODE[serial] = mode
    return mode


def adb_su(serial: str, command: str, adb_exe: str = "", timeout: int = 60) -> str:
    """Run a command as root, using whichever root channel the instance provides.

    Order: adbd-root (already uid 0) -> `su -c`. When neither works the caller
    gets an explanation instead of a silently empty result.
    """
    mode = root_mode(serial, adb_exe)
    if mode == "adbd":
        return adb_shell(serial, command, adb_exe=adb_exe, timeout=timeout)
    if mode == "su":
        return adb(serial, "shell", "su", "-c", command, adb_exe=adb_exe, timeout=timeout)
    return ("[no root channel on {}] run `adb -s {} root` (or enable root for this "
            "instance) and retry; not executed: {}".format(serial, serial, command))


def resolve_pid(serial: str, package: str, adb_exe: str = "", explicit: int | None = None) -> int | None:
    """Find the game PID portably.

    Order: ``--pid`` > ``pidof`` > parse ``ps -A`` in Python.

    The parsing is done in Python rather than by piping to a device-side grep so
    that the outcome does not depend on shell/pipe details.
    """
    if explicit:
        return explicit
    out = adb_shell(serial, "pidof {}".format(package), adb_exe=adb_exe, timeout=30)
    for tok in out.split():
        if tok.isdigit():
            return int(tok)
    ps = adb_shell(serial, "ps -A", adb_exe=adb_exe, timeout=30)
    if not ps or ps.startswith("(timeout)") or "not found" in ps:
        ps = adb_shell(serial, "ps", adb_exe=adb_exe, timeout=30)
    for line in ps.splitlines():
        if package in line:
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit():
                return int(parts[1])
    return None


def out_path(outdir: str, name: str) -> pathlib.Path:
    """Output path that defaults to the current directory (never a hardcoded box)."""
    base = pathlib.Path(outdir) if outdir else pathlib.Path.cwd()
    base.mkdir(parents=True, exist_ok=True)
    return base / name


def frida_device(addr: str):
    """Connect to the forwarded frida-server."""
    import frida  # imported lazily so adb-only scripts work without frida
    try:
        return frida.get_device_manager().add_remote_device(addr)
    except Exception as exc:  # pragma: no cover - environment dependent
        sys.exit("Cannot reach frida-server at {}: {}\n"
                 "Start it on the instance (root) and forward the port:\n"
                 "  adb -s <serial> push frida-server-<ver>-android-x86_64 /data/local/tmp/fs\n"
                 "  adb -s <serial> shell \"su -c 'chmod 755 /data/local/tmp/fs'\"\n"
                 "  adb -s <serial> shell \"su -c '/data/local/tmp/fs -D &'\"\n"
                 "  adb -s <serial> forward tcp:{} tcp:27042".format(
                     addr, exc, addr.rsplit(":", 1)[-1]))


def attach(device, pid: int | None, package: str):
    """Attach to the game, failing with a clear message when it is not running."""
    import frida
    if pid is None:
        sys.exit("Game process not found. Is {} running on the instance? "
                 "Use --pid to attach to an explicit PID.".format(package))
    try:
        return device.attach(pid)
    except frida.ProcessNotFoundError:
        sys.exit("PID {} is gone. Re-detect the PID (the game may have restarted).".format(pid))


def js_symbol_prelude() -> str:
    """JS prelude that resolves symbols by name (ASLR-safe) and exposes the map.

    Provides:
      POP_SYMS[name] -> NativePointer | null
      findSym(m, [names...]) -> NativePointer | null
    """
    return (
        "const POP_SYM_NAMES = {names};\n"
        "function findSym(m, names) {{\n"
        "  for (const n of names) {{ try {{ const a = m.getExportByName(n); if (a) return a; }} catch (e) {{}} }}\n"
        "  let hit = null;\n"
        "  try {{ m.enumerateExports().forEach(function (e) {{\n"
        "    if (hit) return;\n"
        "    for (const n of names) {{ if (e.name.indexOf(n) !== -1) {{ hit = e.address; break; }} }}\n"
        "  }}); }} catch (e) {{}}\n"
        "  return hit;\n"
        "}}\n"
        "const POP_SYMS = {{}};\n"
        "(function () {{\n"
        "  const m = Process.findModuleByName({module!r});\n"
        "  if (!m) {{ send({{ kind: 'no-module', module: {module!r} }}); return; }}\n"
        "  for (const k in POP_SYM_NAMES) {{ POP_SYMS[k] = findSym(m, POP_SYM_NAMES[k]); }}\n"
        "  const missing = [];\n"
        "  for (const k in POP_SYMS) if (!POP_SYMS[k]) missing.push(k);\n"
        "  send({{ kind: 'symbols', base: m.base.toString(), found: Object.keys(POP_SYMS).length, missing: missing }});\n"
        "}})();\n"
    ).format(names=json.dumps(POP_SYMBOLS), module=MODULE_NAME)
