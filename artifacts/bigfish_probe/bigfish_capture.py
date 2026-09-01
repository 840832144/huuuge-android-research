from __future__ import annotations

import argparse
import json
import signal
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import frida


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Capture already-decoded Big Fish Casino HTTP JSON through an ARM64 Frida Gadget."
    )
    parser.add_argument("--host", default="127.0.0.1:27044")
    parser.add_argument("--process", default="Gadget")
    parser.add_argument("--agent", type=Path, default=Path(__file__).with_name("agent.js"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    output = args.output.resolve()
    events_dir = output / "events"
    events_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = output / "events.jsonl"
    meta_path = output / "capture_meta.json"

    meta = {
        "format": "bigfish-http-json-v1",
        "started_at": utc_now(),
        "host": args.host,
        "process": args.process,
        "agent": str(args.agent.resolve()),
        "event_count": 0,
        "http_event_count": 0,
        "last_event_at": None,
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    device = frida.get_device_manager().add_remote_device(args.host)
    session = device.attach(args.process)
    script = session.create_script(args.agent.read_text(encoding="utf-8"))

    jsonl = jsonl_path.open("a", encoding="utf-8", buffering=1)
    stopped = False

    def persist_meta() -> None:
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    def on_message(message, data) -> None:
        nonlocal stopped
        envelope = {
            "captured_at": utc_now(),
            "message": message,
        }
        if data is not None:
            envelope["data_size"] = len(data)

        meta["event_count"] += 1
        meta["last_event_at"] = envelope["captured_at"]
        payload = message.get("payload", {}) if message.get("type") == "send" else {}
        if payload.get("kind") == "bigfish-http":
            meta["http_event_count"] += 1
            sequence = meta["http_event_count"]
            event_path = events_dir / f"{sequence:08d}.json"
            event_path.write_text(
                json.dumps(payload["event"], ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        jsonl.write(json.dumps(envelope, ensure_ascii=False) + "\n")
        persist_meta()
        print(json.dumps(payload or message, ensure_ascii=False), flush=True)

    def request_stop(signum, frame) -> None:
        nonlocal stopped
        stopped = True

    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)

    script.on("message", on_message)
    script.load()
    print(json.dumps({"kind": "capture-started", "output": str(output)}, ensure_ascii=False), flush=True)

    try:
        while not stopped:
            time.sleep(0.25)
    finally:
        meta["stopped_at"] = utc_now()
        persist_meta()
        jsonl.close()
        try:
            script.unload()
        except frida.InvalidOperationError:
            pass
        try:
            session.detach()
        except frida.InvalidOperationError:
            pass

    return 0


if __name__ == "__main__":
    sys.exit(main())

