# Pop! Slots 采集 · 自助部署提示词（交给策划 / 策划的 AI）

> 用法：把下面整段发给你那边的 AI（或自己照着敲）。目标是在**你自己的电脑**上跑通
> Pop! Slots 老虎机数值采集。全程约 20 分钟，其中只有 3 处需要人操作：
> ① 建一个研究实例、② 以管理员身份跑一次 root 脚本、③ 进机台点转盘（或让脚本自动点）。
>
> 配套文档：`artifacts/env/BLUESTACKS_ROOT_STANDARD.md`（root）、
> `artifacts/popslots/SLOT_CAPTURE.md`（采集）、`artifacts/popslots/OPERATOR_GUIDE.md`（排障）。

---

## 复制下面这一段给你的 AI

```
任务：在我的 Windows 电脑上部署 Pop! Slots 老虎机数值采集，并产出一份数值表。
请按顺序执行，每步都等确认后再继续；遇到与我这里描述不符的情况，停下来告诉我。

【前置条件，先逐条检查并报告】
1. Windows + BlueStacks 5（中国版 BlueStacks_nxt_cn，5.22.170.6509 最稳）
2. Python 3.11+（python --version）
3. 我有管理员权限（第 3 步需要）
4. 实例规划：
   - 我的日常实例绝不允许被注入/改动；需要另建一个"研究实例"
   - 如果你看到只有一个实例，先告诉我，别动它

【第 1 步：拿代码】
git clone https://github.com/840832144/huuuge-android-research.git
cd huuuge-android-research
git clone https://github.com/RobThePCGuy/BlueStacks-Root-GUI
cd BlueStacks-Root-GUI
git checkout 7002d185522c41a15ea9b184eff24393c5a62a11
cd ..
# 上游必须放在仓库根旁边（脚本会自动找到它），不要用别处的副本

【第 2 步：准备研究实例（要我做，你给指令）】
- 用 BlueStacks 多开管理器"克隆"一个实例作为研究实例，命名为 HuuugeResearch 之类的
- 启动它一次，在其中用 Google Play 安装 Pop! Slots（记录版本号）
- 关掉它（下面改配置前必须全部关闭）

【第 3 步：开 root（唯一需要管理员的一步）】
# 先只读看现状（不改任何东西），把输出贴给我
python tools/env/bluestacks_root.py check <研究实例名>

# 然后在"以管理员身份运行"的终端里执行：
python tools/env/bluestacks_root.py apply <研究实例名>

# 启动该实例，验证这一条即可（这是唯一权威验证）：
adb -s 127.0.0.1:<端口> shell "su -c id"      # 期望 uid=0(root)
# 端口用这个查：python tools/env/find_instance.py --package com.playstudios.popslots

【第 4 步：装 frida-server（自动匹配版本，不用你找）】
python tools/analysis/popslots/pop_capture.py --serial <串号> setup-frida --download

【第 5 步：采集（四步）】
# 先手动打开游戏，进一台机台，停在能看到 SPIN 的画面
python tools/analysis/popslots/pop_capture.py --serial <串号> check     # 期望 verdict: READY
python tools/analysis/popslots/pop_capture.py --serial <串号> start
python tools/analysis/popslots/pop_capture.py --serial <串号> spin --auto-spin 20
python tools/analysis/popslots/pop_capture.py --serial <串号> stop
python tools/analysis/popslots/pop_capture.py --serial <串号> export
# 产物：pop_capture/slots_values.csv（逐次数值）+ slots_summary.md（汇总）

【红线（必须遵守）】
- 只碰研究实例；日常实例不注入、不改配置、不启动（启动别的实例可能把它抢盘关机）
- 不要用 adb reboot（会卡死 adbd）
- 不要用"白名单里的命令"探测 su（su -c stop 会停掉 guest 系统）
- 采集文件含账号/会话数据：只留本地，不要提交到 Git
- 自动转盘会消耗该账号游戏币：跑之前先把次数告诉我

【出问题就查这本手册】artifacts/popslots/OPERATOR_GUIDE.md
  里面有 12 条实测排障（游戏卡 LOADING = DNS 被 VPN 劫持、adb 连不上、frida 掉了、
  查询失败不等于没装、root 开不了等）
```

---

## 三处需要人操作的地方（给策划本人）

1. **建研究实例 + 装游戏**：BlueStacks 多开管理器 → 克隆实例 → 启动一次 → 用 Google Play 装 Pop! Slots。
   （日常实例不动。）
2. **跑 root 脚本**：右键"以管理员身份运行"终端，执行
   `python tools/env/bluestacks_root.py apply <研究实例名>`。
   也可以用双击版：`tools/env/bluestacks-root-apply.cmd`（无参数=只检查）。
3. **决定采集量**：每次转盘的消耗 = **每线下注 × 线数**（例如 20 线 × 2500 = 50,000/次）。
   `spin --auto-spin N` 里 N 就是消耗上限。想采大样本先把机台注额调低。

## 环境一致性（怎么确认和别人一致）

跑完第 3 步，`check` 的输出应该长这样（这是所有者机器的基线，主机侧三项都必须「已补丁」）：

```
主机侧补丁：
  HD-Player.exe  _isDiskVerificationRequired -> 0 (unlock: integrity  已补丁
  HD-Player.exe  plrCheckDiskIntegrity call (force 'verified')        已补丁
  HD-MultiInstanceManager.exe 停止重置 enable_root_access              已补丁
实例 root 开关：
  <你的研究实例> = 1（已开）        <你的日常实例> = 0
唯一验证：adb -s 127.0.0.1:<端口> shell "su -c id" → uid=0(root)
```

## 常见卡点（先说在前面）

| 现象 | 原因 / 处理 |
|---|---|
| `check` 报「版本不匹配」 | 你的蓝叠构建与上游兼容表不一致（表里是 CN `5.22.170.6509`）。**不要硬打**，把版本号发我 |
| `apply` 报需要管理员 | 用管理员终端重跑（要写 Program Files 并关蓝叠进程） |
| `su -c id` 没输出 uid=0 | 先重启一次实例再试；仍不行就把 `check` 与 `cat /system/etc/.swl.cfg` 的输出发我 |
| 「主机侧三项已补丁但 root 仍不通」 | 极少见；这时才需要动镜像侧（`apply` 会自动做，可用 `--no-su` 跳过） |
| 游戏卡 `LOADING...` | DNS 被 VPN 应用劫持（`tun0`）；`OPERATOR_GUIDE.md` B2 有一键修复 |
| `adb devices` 是空的 | 实例启动后不会自动连 adb：`adb connect 127.0.0.1:<端口>` |
| 采到 0 条记录 | 没进机台 / 没点 SPIN —— 见 `OPERATOR_GUIDE.md` B5 |
