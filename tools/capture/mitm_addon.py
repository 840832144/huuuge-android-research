#!/usr/bin/env python3
"""Generic mitmproxy capture addon — game- and module-agnostic.

Records every decrypted request/response it sees (host, path, method and the raw
bytes as base64) to a local JSONL so a later step can decode or select a module.
Nothing about a specific game or module is hardcoded here.

Environment:
  MITM_OUT     output JSONL path                 (default: mitm_b64.jsonl in the CWD)
  MITM_FILTER  optional regex on "host/path"     (default: capture everything)
               e.g. MITM_FILTER='/slots/' captures only slot-related flows
  MITM_HOSTS   optional comma-separated host allow-list (substring match)

Usage:
  mitmdump --listen-port 8080 -s tools/capture/mitm_addon.py
  MITM_FILTER='/slots/' mitmdump --listen-port 8080 -s tools/capture/mitm_addon.py
"""
import base64
import json
import os
import re
import time

from mitmproxy import http

OUT = os.environ.get("MITM_OUT", "mitm_b64.jsonl")
FILTER = os.environ.get("MITM_FILTER", "")
HOSTS = [h.strip() for h in os.environ.get("MITM_HOSTS", "").split(",") if h.strip()]

_FILTER_RE = re.compile(FILTER) if FILTER else None


def _wanted(host: str, path: str) -> bool:
    if HOSTS and not any(h in host for h in HOSTS):
        return False
    if _FILTER_RE is not None and not _FILTER_RE.search("{} {}".format(host, path)):
        return False
    return True


def _rec(req, resp) -> None:
    try:
        host = getattr(req, "host", "") or ""
        path = getattr(req, "path", "") or ""
        if not _wanted(host, path):
            return
        entry = {
            "ts": int(time.time() * 1000),
            "host": host,
            "path": path,
            "method": getattr(req, "method", None),
            "req_b64": base64.b64encode(req.raw_content).decode() if req.raw_content else None,
            "req_len": len(req.raw_content) if req.raw_content else 0,
            "resp_status": getattr(resp, "status_code", None) if resp else None,
            "resp_b64": base64.b64encode(resp.raw_content).decode()
                       if (resp and resp.raw_content) else None,
            "resp_len": len(resp.raw_content) if (resp and resp.raw_content) else 0,
            "ct": getattr(resp, "headers", {}).get("content-type", "") if resp else "",
        }
        with open(OUT, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


def request(flow: http.HTTPFlow) -> None:
    _rec(flow.request, flow.response if flow.response else None)


def response(flow: http.HTTPFlow) -> None:
    _rec(flow.request, flow.response)
