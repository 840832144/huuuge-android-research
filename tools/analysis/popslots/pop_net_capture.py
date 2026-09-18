#!/usr/bin/env python3
"""Pop! Slots 网络采集（Frida，curl 边界）。

原理：libBigCasino.so 静态链接 libcurl，libcurl 在**明文**层面与引擎交互：
  CURLOPT_URL(10002) / CURLOPT_POSTFIELDS(10015) / CURLOPT_CUSTOMREQUEST(10036)
  CURLOPT_WRITEFUNCTION(20011) 回调 → 响应体（可能分块）
  CURLOPT_READFUNCTION(20012)  回调 → 请求体
因此在 curl 边界即可拿到 URL + 明文 body，不需要解密 TLS，也不依赖 TLS 函数导出。

归属策略：**不依赖 curl handle 身份**（同一回调函数会被多个 handle 复用），
而是维护"最近一次 URL 上下文"的队列，把请求体与响应分块挂到最新上下文上，
空闲 800ms 即认为该请求结束并落一条记录。

输出形状与 tools/capture/mitm_addon.py 一致（host/path/method + base64 body），
因此 endpoints.py / select_module.py 可直接复用做模块选择。

用法：
  python pop_net_capture.py <serial> [seconds] [--out file.jsonl] [--frida host:port]
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys

# Windows consoles default to a legacy code page; reconfigure before anything is
# printed, otherwise argparse's --help (and any early output) can fail to encode.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

import time

sys.path.insert(0, str(os.path.dirname(os.path.abspath(__file__))))
import pop_common as pc

JS = r"""
'use strict';
function findSym(name) {
  const mods = Process.enumerateModules();
  for (let i = 0; i < mods.length; i++) {
    try { const a = mods[i].findExportByName(name); if (a) return { addr: a, mod: mods[i].name }; }
    catch (e) {}
  }
  return null;
}
const OPT_URL = 10002, OPT_POSTFIELDS = 10015, OPT_WRITE = 20011,
      OPT_READ = 20012, OPT_CUSTOM = 10036;
const IDLE_MS = 800;
let ctx = [];                       // [{url, method, req_b64, req_len, chunks:[], bytes, last}]
const hookedWrite = {}, hookedRead = {};
let stats = { urls: 0, posts: 0, writeHits: 0, readHits: 0, emitted: 0, skips: 0 };

function hostOf(u) {
  const m = String(u || '').match(/^[a-z]+:\/\/([^\/]+)(\/.*)?$/i);
  return m ? { host: m[1], path: m[2] || '/' } : { host: String(u || ''), path: '/' };
}
function newest() {
  for (let i = ctx.length - 1; i >= 0; i--) if (!ctx[i].done) return ctx[i];
  const c = { url: '', method: 'GET', chunks: [], bytes: 0, last: 0, done: false };
  ctx.push(c);
  return c;
}
function pushUrl(u) {
  const c = { url: u, method: 'GET', chunks: [], bytes: 0, last: Date.now(), done: false };
  ctx.push(c);
  if (ctx.length > 200) ctx = ctx.slice(-120);
}
function flushOne(c, why) {
  if (c.done) return;
  c.done = true;
  if (!c.url) { stats.skips++; send({ kind: 'skip', why: why, bytes: c.bytes }); return; }
  let buf = null;
  if (c.chunks.length) {
    let total = 0; c.chunks.forEach(function (x) { total += x.length; });
    const all = new Uint8Array(total); let o = 0;
    c.chunks.forEach(function (x) { all.set(x, o); o += x.length; });
    buf = all.buffer;
  }
  const hp = hostOf(c.url);
  stats.emitted++;
  // 二进制体走 Frida 的 data 通道（该运行时没有 base64encode）
  send({ kind: 'record', rec: {
    ts: Date.now(), host: hp.host, path: hp.path, method: c.method || 'GET',
    req_text: (typeof c.req_text === 'string' ? c.req_text : null),
    req_len: c.req_len || 0,
    resp_len: c.bytes, ct: '', via: 'curl/' + why } }, buf);
}
const setopt = findSym('curl_easy_setopt');
if (!setopt) { send({ kind: 'nocurl' }); }
Interceptor.attach(setopt.addr, {
  onEnter(args) {
    const opt = args[1].toInt32();
    const val = args[2];
    if (opt === OPT_URL) {
      try { const u = val.readUtf8String(); stats.urls++; pushUrl(u); } catch (e) {}
    } else if (opt === OPT_POSTFIELDS) {
      try {
        const s = val.readUtf8String();
        if (s && s.length < 1024 * 1024) {
          const c = newest();
          c.req_text = s; c.req_len = s.length; c.method = 'POST'; c.last = Date.now();
          stats.posts++;
        }
      } catch (e) {}
    } else if (opt === OPT_CUSTOM) {
      try { newest().method = val.readUtf8String(); } catch (e) {}
    } else if (opt === OPT_WRITE) {
      const key = val.toString();
      if (hookedWrite[key]) return;
      hookedWrite[key] = true;
      try {
        Interceptor.attach(val, {
          onEnter(a) {
            const n = a[1].toInt32() * a[2].toInt32();
            if (n <= 0 || n > 8 * 1024 * 1024) return;
            stats.writeHits++;
            try {
              const ab = a[0].readByteArray(n);
              if (!ab) { stats.skips++; return; }
              const c = newest();
              c.chunks.push(new Uint8Array(ab));
              c.bytes += n; c.last = Date.now();
            } catch (e) { send({ kind: 'err', where: 'write', msg: String(e) }); }
          }
        });
      } catch (e) { send({ kind: 'err', where: 'attach-write', msg: String(e) }); }
    } else if (opt === OPT_READ) {
      const key = val.toString();
      if (hookedRead[key]) return;
      hookedRead[key] = true;
      try {
        Interceptor.attach(val, {
          onEnter(a) { this.buf = a[0]; },
          onLeave(retval) {
            const n = retval.toInt32();
            if (n <= 0 || n > 2 * 1024 * 1024) return;
            stats.readHits++;
            try {
              const ab = this.buf.readByteArray(n);
              if (!ab) return;
              const c = newest();
              c.req_b64 = base64encode(ab); c.req_len = n; c.method = c.method || 'POST';
              c.last = Date.now();
            } catch (e) {}
          }
        });
      } catch (e) {}
    }
  }
});
setInterval(function () {
  const now = Date.now();
  ctx.forEach(function (c) { if (!c.done && c.last && now - c.last > IDLE_MS) flushOne(c, 'idle'); });
  ctx = ctx.filter(function (c) { return !c.done; });
  send({ kind: 'stats', stats: stats, open: ctx.length });
}, IDLE_MS);
send({ kind: 'ready', setopt: setopt.mod });
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("serial", nargs="?", default=os.environ.get("POP_SERIAL", ""))
    ap.add_argument("seconds", nargs="?", type=float, default=60.0)
    ap.add_argument("--frida", default=os.environ.get("POP_FRIDA", "127.0.0.1:27042"))
    ap.add_argument("--package", default=pc.DEFAULT_PACKAGE)
    ap.add_argument("--out", default=os.environ.get("MITM_OUT", "pop_net.jsonl"))
    ap.add_argument("--quiet", action="store_true", help="只打印统计与端点汇总")
    args = ap.parse_args()

    pid = pc.resolve_pid(args.serial, args.package)
    print("pid:", pid)
    device = pc.frida_device(args.frida)
    session = pc.attach(device, pid, args.package)
    script = session.create_script("'use strict';\n" + JS)

    seen: dict[str, int] = {}
    written = 0

    def on_message(message, data):
        nonlocal written
        p = message.get("payload", {})
        k = p.get("kind")
        if k == "ready":
            print("hook ready (curl in {})".format(p.get("setopt")))
        elif k == "nocurl":
            print("!! curl_easy_setopt not found - the engine may not use libcurl")
        elif k == "err":
            print("  [js-error] {}: {}".format(p.get("where"), p.get("msg")), flush=True)
        elif k == "skip":
            print("  [skip] no URL for a {} byte body".format(p.get("bytes")), flush=True)
        elif k == "stats":
            s = p.get("stats", {})
            print("  urls={urls} posts={posts} write={writeHits} read={readHits} "
                  "emitted={emitted} open={}".format(p.get("open"), **s), flush=True)
        elif k == "record":
            rec = p["rec"]
            if data:                       # response bytes arrive on the data channel
                rec["resp_b64"] = base64.b64encode(data).decode()
            if rec.get("req_text") is not None:
                rec["req_b64"] = base64.b64encode(rec["req_text"].encode("utf-8")).decode()
            rec.pop("req_text", None)
            key = "{} {}".format(rec.get("host"), rec.get("path"))
            seen[key] = seen.get(key, 0) + 1
            with open(args.out, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            written += 1
            if not args.quiet:
                shown = ""
                raw = rec.get("resp_b64") or rec.get("req_b64")
                if raw:
                    try:
                        shown = base64.b64decode(raw)[:90].decode("utf-8", "replace")
                    except Exception:
                        shown = "(binary)"
                print("  [{}] {} {}{}  resp_len={}  {}".format(
                    rec.get("method"), rec.get("host"), rec.get("path"),
                    "?q" if "?" in (rec.get("path") or "") else "",
                    rec.get("resp_len"), shown.replace("\n", " ")), flush=True)

    script.on("message", on_message)
    script.load()
    print("collecting {}s -> {}".format(args.seconds, args.out))
    try:
        time.sleep(args.seconds)
    except KeyboardInterrupt:
        pass
    print("\n--- endpoints ({} distinct) ---".format(len(seen)))
    for k, n in sorted(seen.items(), key=lambda kv: -kv[1]):
        print("  {:>4}x {}".format(n, k))
    print("records written:", written)
    try:
        session.detach()
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
