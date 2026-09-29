#!/usr/bin/env python3
"""把采集到的老虎机响应导出成**数值表（CSV）**，使用者不需要写代码。

输入：pop_net_capture.py / pop_capture.py 采到的 JSONL（每行一条记录，
      含 host/path 与 base64 响应体）。
输出：每个老虎机相关端点一张 CSV（默认写到 --outdir，文件名带端点名）。

能识别的内容（Pop! Slots 的 /slots2/spin、/slots2/startgame 等）：
  下注 lines/bet、中奖 totalWin/winType、余额 coinsBalance、
  牌面 matrix、中奖线 wins[]、等级/经验、机台名与时间戳、state（若为奖励游戏）

用法：
  python pop_spin_export.py <capture.jsonl> [--outdir .] [--match slots]
"""
from __future__ import annotations

import argparse
import base64
import csv
import json
import pathlib
import re
import sys

# Windows consoles default to a legacy code page; reconfigure before anything is
# printed, otherwise argparse's --help (and any early output) can fail to encode.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

from urllib.parse import parse_qs, urlparse

# 老虎机相关（默认；--match 可换）
DEFAULT_MATCH = r"/slots|/spin|startgame|gameId="


def iter_json_objects(text: str):
    """容忍一个 body 里串联多个 JSON 对象（引擎会把多段拼在一次响应里）。"""
    dec = json.JSONDecoder()
    i, n = 0, len(text)
    while i < n:
        while i < n and text[i] in " \r\n\t":
            i += 1
        if i >= n:
            return
        try:
            obj, end = dec.raw_decode(text, i)
        except Exception:
            return
        yield obj
        i = end


def deep_first(obj, *names):
    """在嵌套结构里找第一个出现的键（不区分层级）。"""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in names:
                return v
        for v in obj.values():
            r = deep_first(v, *names)
            if r is not None:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = deep_first(v, *names)
            if r is not None:
                return r
    return None


def winner_of(payload: dict) -> dict:
    """合并一个响应里所有 payload，得到一行数值。"""
    row: dict = {}
    for obj in (payload.get("_objs") or []):
        p = obj.get("payload") if isinstance(obj, dict) else None
        if not isinstance(p, dict):
            continue
        for k in ("sId", "totalWin", "winType", "coinsBalance", "balance", "balanceVersion",
                  "reelStopPoint", "matrix", "wins", "xp", "casinoData", "state",
                  "isMilestoneReached", "tournamentRound", "jackpotWins"):
            if k in p and k not in row:
                row[k] = p[k]
    return row


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("capture", help="采集 JSONL")
    ap.add_argument("--outdir", default=".", help="CSV 输出目录")
    ap.add_argument("--match", default=DEFAULT_MATCH, help="端点正则（默认老虎机相关）")
    ap.add_argument("--all", action="store_true", help="导出所有端点（不只老虎机）")
    ap.add_argument("--no-summary", action="store_true", help="不打印/不写数值汇总")
    args = ap.parse_args()

    cap = pathlib.Path(args.capture)
    if not cap.exists():
        print("找不到采集文件:", cap, file=sys.stderr)
        return 1
    matcher = None if args.all else re.compile(args.match, re.I)
    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    rows: list[dict] = []
    by_endpoint: dict[str, int] = {}
    for line in cap.open(encoding="utf-8-sig"):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except Exception:
            continue
        key = "{} {}".format(rec.get("host"), rec.get("path"))
        if matcher and not matcher.search(key):
            continue
        by_endpoint[key] = by_endpoint.get(key, 0) + 1
        body = rec.get("resp_b64")
        if not body:
            continue
        try:
            text = base64.b64decode(body).decode("utf-8", "replace")
        except Exception:
            continue
        if not text.lstrip().startswith("{"):
            continue
        objs = list(iter_json_objects(text))
        if not objs:
            continue

        url = urlparse("https://{}{}".format(rec.get("host", ""), rec.get("path", "")))
        q = {k: v[0] for k, v in parse_qs(url.query).items()}
        merged = winner_of({"_objs": objs})
        wins = merged.get("wins") if isinstance(merged.get("wins"), list) else []
        cas = merged.get("casinoData")
        machine = None
        if isinstance(cas, list) and cas:
            machine = deep_first(cas, "machineName")
        if not machine:
            machine = q.get("gameId")

        rows.append({
            "ts": rec.get("ts"),
            "endpoint": "{}{}".format(rec.get("host"), url.path),
            "machine": machine,
            "lines": q.get("lines"),
            "bet": q.get("bet"),
            "sId": merged.get("sId") or q.get("sId"),
            "spinIndex": q.get("BIsi"),
            "totalWin": merged.get("totalWin"),
            "winType": merged.get("winType"),
            "winCount": len(wins),
            "winSum": sum(float(w.get("winSum") or 0) for w in wins) if wins else None,
            "coinsBalance": merged.get("coinsBalance"),
            "balanceVersion": merged.get("balanceVersion"),
            "level": (merged.get("xp") or {}).get("level") if isinstance(merged.get("xp"), dict) else None,
            "xp": (merged.get("xp") or {}).get("xp") if isinstance(merged.get("xp"), dict) else None,
            "matrix": json.dumps(merged.get("matrix"), ensure_ascii=False) if merged.get("matrix") else None,
            "reelStopPoint": json.dumps(merged.get("reelStopPoint")) if merged.get("reelStopPoint") else None,
            "bodyLen": len(text),
        })

    if not rows:
        print("没有可导出的数值行。端点命中情况：")
        for k, n in sorted(by_endpoint.items(), key=lambda kv: -kv[1])[:20]:
            print("  {:>4}x {}".format(n, k))
        if not by_endpoint:
            print("  (没有任何端点匹配；用 --all 或调 --match)")
        return 0

    out = outdir / "slots_values.csv"
    fields = list(rows[0].keys())
    with out.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    print("导出 {} 行数值 -> {}".format(len(rows), out))
    print("\n端点命中：")
    for k, n in sorted(by_endpoint.items(), key=lambda kv: -kv[1])[:10]:
        print("  {:>4}x {}".format(n, k))
    print("\n前 3 行（关键列）：")
    show = ["machine", "bet", "spinIndex", "totalWin", "winType", "winCount", "coinsBalance", "level"]
    print("  " + " | ".join(show))
    for r in rows[:3]:
        print("  " + " | ".join(str(r.get(k)) for k in show))

    if not args.no_summary:
        print_summary(rows, outdir)
    return 0


def _f(v) -> float:
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def print_summary(rows: list, outdir: pathlib.Path) -> None:
    """把数值汇总成策划可直接看的结论，省掉自己拉透视表。

    注意：URL 里的 `bet` 是**每线**下注，实际每次消耗 = lines × bet
    （实测 bet=2500、lines=20 → 每次 50,000），所以总消耗按乘积算。
    """
    spin_rows = [r for r in rows if "spin" in (r.get("endpoint") or "")] or rows

    total_bet = total_win = 0.0
    wins = []
    kinds: dict = {}
    for r in spin_rows:
        cost = (_f(r.get("lines")) or 1) * _f(r.get("bet"))
        win = _f(r.get("totalWin"))
        total_bet += cost
        total_win += win
        kind = r.get("winType") or "?"
        kinds[kind] = kinds.get(kind, 0) + 1
        wins.append((r.get("spinIndex"), cost, win))

    n = len(spin_rows)
    hits = sum(1 for _, _, w in wins if w > 0)
    biggest = max(wins, key=lambda x: x[2]) if wins else (None, 0.0, 0.0)
    rtp = (total_win / total_bet * 100) if total_bet else 0.0

    lines_out = [
        "数值汇总（{} 次转盘）".format(n),
        "  总下注: {:.0f}".format(total_bet),
        "  总中奖: {:.0f}".format(total_win),
        "  净变化: {:+.0f}".format(total_win - total_bet),
        "  实测回收率(RTP): {:.2f}%   ← 样本小时波动极大，不要当期望值".format(rtp),
        "  中奖次数: {} / {} ({:.1f}%)".format(hits, n, hits * 100.0 / n if n else 0.0),
        "  单次最大中奖: {:.0f} (第 {} 次)".format(biggest[2], biggest[0]),
        "  中奖类型分布: " + ", ".join(
            "{}×{}".format(v, k) for k, v in sorted(kinds.items(), key=lambda kv: -kv[1])),
    ]
    print("")
    for line in lines_out:
        print(line)
    summary = outdir / "slots_summary.md"
    summary.write_text("# Pop! Slots 老虎机数值汇总\n\n```\n" + "\n".join(lines_out) + "\n```\n",
                       encoding="utf-8")
    print("\n汇总已写入: {}".format(summary))


if __name__ == "__main__":
    sys.exit(main())
