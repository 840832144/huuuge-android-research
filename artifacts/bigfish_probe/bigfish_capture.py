from __future__ import annotations

"""
Big Fish Casino passive HTTP JSON capture (logcat transport).

The Big Fish JS client logs every already-decoded HTTP request/response
through cc.log/console.log, which land in logcat under the tags
"Cobra Log" and "cocos2d-x debug info" with the marker prefix
``__CODEX_BIGFISH_HTTP_V1__``. This collector consumes that logcat stream,
parses the tagged JSON events and writes them locally (events.jsonl plus one
file per HTTP event under events/).

Two modes:

- ``--mode logcat`` (default): stream ``adb logcat`` and parse tagged events.
  No Frida hook is needed. Use this for normal capture.
- ``--mode frida``: attach the ARM64 Gadget and (re)inject agent.js to make
  sure the JS collector is installed; the tagged receipt/events still arrive
  through logcat. Use this once to obtain the ``collector-installed`` /
  ``collector-already-installed`` receipt.

Raw output may contain account/session/value-bearing data. Keep capture
folders outside Git (for example under ``C:\\bigfish_research\\captures``).
"""

import argparse
import json
import re
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import frida

MARKER = "__CODEX_BIGFISH_HTTP_V1__"
LOG_TAGS = ("Cobra Log", "cocos2d-x debug info")
EVENT_RE = re.compile(r"__CODEX_BIGFISH_HTTP_V1__(.*)$", re.DOTALL)


def try_parse_json(raw: str):
    """Try to json.loads raw. If it ends mid-string (logcat truncated a large
    response across multiple lines), return (None, is_partial)."""
    try:
        return json.loads(raw), False
    except json.JSONDecodeError:
        # Incomplete (truncated). Return partial flag; caller should buffer.
        return None, True


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _adb_path() -> str:
    """Locate adb: explicit platform-tools path first, then PATH."""
    candidates = [
        r"C:\platform-tools\adb.exe",
        r"C:\platform-tools\adb",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    return "adb"


class CaptureStore:
    """Local event store: events.jsonl + per-event JSON under events/."""

    def __init__(self, output: Path) -> None:
        self.output = output.resolve()
        self.events_dir = output / "events"
        self.events_dir.mkdir(parents=True, exist_ok=True)
        self.jsonl_path = output / "events.jsonl"
        self.meta_path = output / "capture_meta.json"
        self.meta = {
            "format": "bigfish-http-json-v1",
            "started_at": utc_now(),
            "event_count": 0,
            "http_event_count": 0,
            "receipt_count": 0,
            "last_event_at": None,
        }
        self.jsonl = self.jsonl_path.open("a", encoding="utf-8", buffering=1)
        self._partial = ""
        self._partial_at = None

    def __getattr__(self, name):
        if name == "partial":
            return self._partial
        raise AttributeError(name)

    def persist_meta(self) -> None:
        self.meta_path.write_text(json.dumps(self.meta, ensure_ascii=False, indent=2), encoding="utf-8")

    def accept_line(self, line: str, captured_at: str) -> None:
        """Parse one logcat line; persist any tagged Big Fish event.

        Large responses may be truncated by logcat across multiple lines
        (each line ends mid-JSON). We buffer consecutive partial lines until
        the JSON parse succeeds or a non-marker line breaks the run.
        """
        match = EVENT_RE.search(line)
        if not match:
            return
        raw = match.group(1).strip()
        if not raw:
            return
        # If previous line was partial, append; otherwise start fresh.
        if self._partial:
            raw = self._partial + raw
        try:
            event = json.loads(raw)
            self._partial = ""
        except json.JSONDecodeError:
            # Maybe truncated mid-string. Buffer and wait for continuation.
            # (Logcat truncation replaces nothing; the run ends on next tag.)
            self._partial = raw
            self._partial_at = captured_at
            return

        if event.get("kind") in ("collector-installed", "collector-already-installed"):
            self.meta["receipt_count"] += 1
        if event.get("kind") in ("request", "response", "reject", "throw"):
            self.meta["http_event_count"] += 1
            sequence = self.meta["http_event_count"]
            (self.events_dir / f"{sequence:08d}.json").write_text(
                json.dumps(event, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        self.meta["event_count"] += 1
        self.meta["last_event_at"] = captured_at
        self.jsonl.write(json.dumps({"captured_at": captured_at, "event": event}, ensure_ascii=False) + "\n")
        self.persist_meta()
        print(json.dumps(event, ensure_ascii=False), flush=True)

    def close(self) -> None:
        self.meta["stopped_at"] = utc_now()
        self.persist_meta()
        self.jsonl.close()


def run_logcat(serial: str, store: CaptureStore) -> int:
    adb = _adb_path()
    cmd = [adb, "-s", serial, "logcat", "-v", "threadtime"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace")
    stopped = False

    def request_stop(signum, frame) -> None:
        nonlocal stopped
        stopped = True

    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)
    print(json.dumps({"kind": "capture-started", "mode": "logcat", "output": str(store.output), "serial": serial}, ensure_ascii=False), flush=True)

    try:
        for raw_line in proc.stdout:
            if stopped:
                break
            if any(tag in raw_line for tag in LOG_TAGS) and MARKER in raw_line:
                store.accept_line(raw_line, utc_now())
    except KeyboardInterrupt:
        pass
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    return 0


def ensure_collector(host: str, agent: Path) -> None:
    """Attach the Gadget and (re)inject agent.js to guarantee the JS collector
    is installed. The tagged receipt arrives through logcat afterwards."""
    device = frida.get_device_manager().add_remote_device(host)
    session = device.attach("Gadget")
    script = session.create_script(agent.read_text(encoding="utf-8"))
    script.on("message", lambda m, d: print(json.dumps(m, ensure_ascii=False, default=str), flush=True))
    script.load()
    time.sleep(3)
    try:
        script.unload()
    except frida.InvalidOperationError:
        pass
    try:
        session.detach()
    except frida.InvalidOperationError:
        pass


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Capture already-decoded Big Fish Casino HTTP JSON via logcat."
    )
    parser.add_argument("--output", type=Path, required=True, help="Local capture folder (keep out of Git)")
    parser.add_argument("--mode", choices=("logcat", "frida"), default="logcat")
    parser.add_argument("--serial", default="127.0.0.1:5565", help="ADB serial of the research emulator")
    parser.add_argument("--host", default="127.0.0.1:27044", help="Frida Gadget host:port (frida mode)")
    parser.add_argument("--agent", type=Path, default=Path(__file__).with_name("agent.js"))
    args = parser.parse_args()

    store = CaptureStore(args.output)
    if args.mode == "frida":
        ensure_collector(args.host, args.agent)
    rc = run_logcat(args.serial, store)
    store.close()
    return rc


if __name__ == "__main__":
    sys.exit(main())
