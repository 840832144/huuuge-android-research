#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RTP 采样量 / 置信区间计算器（Pop! Slots 数值采集用）。

用途：回答"还要采多少盘才够"。给定逐次转盘记录，算出：
  - 实测 RTP（每盘派彩 / 每盘消耗）与样本标准差 σ
  - 95% 置信区间（当前样本的"误差棒"）
  - 达到 ±1% / ±2% / ±5% / ±10% 精度分别需要多少盘、要多少预算
  - 按 σ 的可能范围（小样本估不准）给出需求区间，而不是单一数字

设计口径（与 HANDOFF_20260918.md §2.1 一致）：
  * 每盘消耗 = lines × bet（接口里的 bet 是**每线**下注）
  * 每盘回收倍数 = totalWin / (lines × bet)
  * RTP 估计 = 回收倍数均值；标准差按样本标准差（n-1）算

注意：老虎机 RTP 与**下注额无关**（派彩按倍数缩放），所以「降低注额换更多盘数」在方法上成立，
真需要固定的是**同一台机器 + 同一 lines/bet 组合 + 同一版本**；本工具会把不一致的组合标出来。

用法：
  python tools/analysis/popslots/rtp_power.py <slots_values.csv> [--assume-sigma 5] [--target 0.05]
  python tools/analysis/popslots/rtp_power.py  # 默认读本地采集目录（不入库）
"""
from __future__ import annotations

import argparse
import csv
import math
import pathlib
import statistics
import sys

# 坑清单：stdout/stderr 重配必须在**导入期**完成，否则 --help 在 parse_args 之前就崩
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

DEFAULT_CSV = r"C:\bigfish_research\popslots_run_20260918\slots_values.csv"
Z95 = 1.959964
# 老虎机常见单盘波动量级（以"每盘倍数"计），用于小样本时给出需求区间
SIGMA_RANGE = (1.0, 2.0, 5.0, 8.0)


def load_rows(path: pathlib.Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return [r for r in csv.DictReader(fh) if r]


def stake_of(row: dict) -> float:
    lines = float(row.get("lines") or 0)
    bet = float(row.get("bet") or 0)
    return lines * bet


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path", nargs="?", default=DEFAULT_CSV)
    ap.add_argument("--assume-sigma", type=float, default=0.0,
                    help="用指定的每盘标准差代替样本估计（样本小时更稳）")
    ap.add_argument("--target", type=float, default=0.05, help="目标精度（绝对，默认 0.05 = ±5%）")
    args = ap.parse_args()

    path = pathlib.Path(args.csv_path)
    if not path.is_file():
        print(f"找不到数据文件：{path}")
        print("（本地采集数据不入库；路径见 artifacts/HANDOFF_20260918.md §2.1）")
        return 2

    rows = load_rows(path)
    if not rows:
        print("数据文件为空")
        return 2

    mults: list[float] = []
    stakes: set[float] = set()
    machines: set[str] = set()
    win_types: dict[str, int] = {}
    total_stake = total_win = 0.0
    for row in rows:
        stake = stake_of(row)
        win = float(row.get("totalWin") or 0)
        if stake <= 0:
            continue
        mults.append(win / stake)
        stakes.add(stake)
        machines.add(row.get("machine") or "?")
        wt = (row.get("winType") or "?").strip()
        win_types[wt] = win_types.get(wt, 0) + 1
        total_stake += stake
        total_win += win

    n = len(mults)
    if n == 0:
        print("没有可用的转盘记录")
        return 2

    rtp = statistics.fmean(mults)
    sigma_sample = statistics.stdev(mults) if n > 1 else float("nan")
    sigma = args.assume_sigma if args.assume_sigma > 0 else sigma_sample
    se = sigma / math.sqrt(n)
    half = Z95 * se
    wins = sum(1 for m in mults if m > 0)

    print("=" * 68)
    print(f"数据文件：{path}")
    print(f"盘数 n = {n}    机器 = {', '.join(sorted(machines))}    每盘消耗组合 = {sorted(stakes)}")
    print(f"总消耗 = {total_stake:,.0f}    总派彩 = {total_win:,.0f}    净 = {total_win - total_stake:,.0f}")
    print("-" * 68)
    print(f"实测 RTP        = {rtp*100:.2f}%")
    print(f"样本标准差 σ    = {sigma_sample:.3f}" if n > 1 else "样本标准差 σ    = n/a（只有 1 盘）")
    print(f"95% 置信区间    = [{max(0.0, rtp-half)*100:.2f}%, {(rtp+half)*100:.2f}%]"
          f"   （±{half*100:.1f} 个百分点）")
    print(f"中奖盘数        = {wins}/{n} = {wins/n*100:.1f}%")
    print(f"winType 分布    = {win_types}")
    print("-" * 68)

    if n < 30:
        print("⚠ n < 30：置信区间比估计值本身还宽，RTP 不能当期望值用。")
    if len(stakes) > 1:
        print("⚠ 每盘消耗组合不唯一：不同注额的**倍数**仍可比，但要确认是同一台同一版本。")
    feature = {k: v for k, v in win_types.items() if k not in ("NO_WIN", "PLAIN_WIN")}
    if feature:
        print(f"⚠ 出现非基础盘类型 {feature}：只统计基础盘会**低估** RTP（免费旋转/奖励盘要单列）。")
    else:
        print("提示：样本里没有任何 免费旋转/奖励 类 winType —— 若该机有 free spins，说明还没采到，"
              "这类机型的 RTP 必须包含奖励盘。")

    print("-" * 68)
    print("达到目标精度需要多少盘（按 σ 计算：n = (1.96·σ/精度)²）")
    header = f"{'目标精度':>10} | {'σ=样本':>14} | " + " | ".join(f"σ={s:g}".rjust(8) for s in SIGMA_RANGE)
    print(header)
    print("-" * len(header))
    for target in (0.01, 0.02, 0.05, 0.10):
        cells = []
        for s in ((sigma_sample,) if n > 1 else ()) + SIGMA_RANGE:
            need = (Z95 * s / target) ** 2
            cells.append(f"{math.ceil(need):>8,}")
        if n > 1:
            cells = cells[:1] + cells[1:]
        print(f"{target*100:>9.0f}% | " + " | ".join(cells))
    print()
    print("预算换算（按当前每盘消耗，最小/最大注额两种）")
    per_spin = sorted(stakes)[0]
    for target in (0.05, 0.02):
        for s in ((sigma_sample,) if n > 1 else ()) + SIGMA_RANGE:
            need = math.ceil((Z95 * s / target) ** 2)
            print(f"  ±{target*100:.0f}%  σ={s:.2f}  → {need:>8,} 盘 ≈ 预算 {need*per_spin:>14,.0f}"
                  f"（每盘 {per_spin:,.0f}）")
        print()

    print("-" * 68)
    print("逐批推进建议（每批 200 盘，边采边算；CI 半宽 ≤ 目标即可停）")
    for batch in (200, 500, 1000, 2000, 5000, 10000):
        hw = Z95 * (sigma if sigma == sigma else 0) / math.sqrt(batch)
        print(f"  n = {batch:>6,}  → 95% CI 半宽 ≈ ±{hw*100:5.2f} 个百分点"
              f"  （预算 ≈ {batch*per_spin:,.0f}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
