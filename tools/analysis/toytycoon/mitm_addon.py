import json
import time
import base64
from mitmproxy import http

OUT = r"C:\bigfish_research\toptycoon\mitm_b64.jsonl"

def _rec(req, resp):
    try:
        entry = {
            "ts": int(time.time() * 1000),
            "host": getattr(req, "host", None),
            "path": getattr(req, "path", None),
            "method": getattr(req, "method", None),
            "req_b64": base64.b64encode(req.raw_content).decode() if req.raw_content else None,
            "req_len": len(req.raw_content) if req.raw_content else 0,
            "resp_status": getattr(resp, "status_code", None) if resp else None,
            "resp_b64": base64.b64encode(resp.raw_content).decode() if (resp and resp.raw_content) else None,
            "resp_len": len(resp.raw_content) if (resp and resp.raw_content) else 0,
            "ct": getattr(resp, "headers", {}).get("content-type", "") if resp else "",
        }
        with open(OUT, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass

def request(flow: http.HTTPFlow):
    _rec(flow.request, flow.response if flow.response else None)

def response(flow: http.HTTPFlow):
    _rec(flow.request, flow.response)
