# Pop! Slots 采集 · 手把手排障手册（Operator guide）

> 面向**实际操作采集的 agent/人**。每一步都写了**你应该看到什么**；出问题时按下面对照表处理。
> 配套：`artifacts/popslots/SLOT_CAPTURE.md`（正常流程）、`artifacts/env/INSTANCE_DESIGNATION.md`（实例指定）。

---

## 一、开跑前的前置检查（按顺序，全部通过再采集）

| # | 命令 | 你应该看到 |
|---|---|---|
| 1 | `python tools/env/find_instance.py --package com.playstudios.popslots` | 有一行 **`★ 研究候选（有包 + 有 root）`**，记下它的**串号** |
| 2 | `adb devices` | 上面那个串号处于 `device`（不是 offline；**若列表为空，见 B1**）|
| 3 | `python tools/analysis/popslots/pop_capture.py --serial <串号> setup-frida --download` | `[ok] frida-server 正在运行，端口转发正常` |
| 4 | 手动打开游戏，停在能看到大厅/机台的画面 | — |
| 5 | `python tools/analysis/popslots/pop_capture.py --serial <串号> check` | 最后一行 **`verdict: READY`** |
| 6 | 游戏是否**在机台里**？不在就先从大厅进一台机台 | 看到转盘与右下角 **SPIN** |

> ⚠️ **消耗口径**：接口 URL 里的 `bet` 是**每线**下注，实际每次消耗 = `lines × bet`。
> 实测 `bet=2500 & lines=20` → **每次 50,000**。跑之前先看清机台上的注额（SPIN 按钮上的数字），
> 再决定 `--auto-spin` 的次数：**次数 × 单次消耗 = 消耗上限**。必要时先在机台里用 `BET` 面板调低。

## 二、采集四步

```bash
python tools/analysis/popslots/pop_capture.py --serial <串号> start
python tools/analysis/popslots/pop_capture.py --serial <串号> spin --auto-spin 10      # 或人工玩
python tools/analysis/popslots/pop_capture.py --serial <串号> stop
python tools/analysis/popslots/pop_capture.py --serial <串号> export
```

- `start` → `[ok] 采集已开始（pid …）`
- `spin` → 逐次打印 `第 i/N 次`；每次点击都写进 `pop_capture/autoplay.jsonl`
- `stop` → `[ok] 采集文件：…（NN 条记录）`；**NN 必须 > 0**，否则见 B5
- `export` → 打印端点表 + 关键列 + **数值汇总**，并写出
  `slots_values.csv`（逐次数值）与 `slots_summary.md`（汇总）

---

## 三、排障对照表（全部来自真实踩坑）

### B1 `adb devices` 是空的，但实例明明在跑
**原因**：BlueStacks 实例启动后不会自动连到 adb server。
**处理**：
```bash
adb connect 127.0.0.1:<该实例的 adb 端口>     # 端口用 find_instance.py 查
adb devices                                   # 应出现 127.0.0.1:<端口>  device
```

### B2 游戏卡在 `LOADING...`，或画面全黑
**先看日志**：
```bash
adb -s <串号> shell "logcat -d -t 400 | grep -iE 'ERR_NAME_NOT_RESOLVED|FATAL|ANR' | tail"
```
- 出现 **`net::ERR_NAME_NOT_RESOLVED`** → **DNS 被 VPN 应用劫持**（本机实测是
  `com.wonderustech.aurora` 拉起 `tun0`）。确认与修复：
  ```bash
  adb -s <串号> shell "ip -o link | grep tun"          # 有 tun0 就是它
  adb -s <串号> shell "ping -c 1 -W 3 www.baidu.com"   # unknown host = 确实挂了
  adb -s <串号> shell "am force-stop com.wonderustech.aurora"
  adb -s <串号> shell "pm disable-user --user 0 com.wonderustech.aurora"   # 防复发，可 pm enable 还原
  adb -s <串号> shell "setprop net.dns1 10.0.2.3"      # 恢复模拟器 NAT DNS
  ```
  然后**重启游戏**（force-stop + 重新启动），它会自动恢复上次会话。
- 没有 DNS 报错但画面黑 → **实例窗口被最小化/显示休眠**：
  ```bash
  adb -s <串号> shell "input keyevent KEYCODE_WAKEUP"
  ```
  仍为黑：让实例窗口在前台（不要最小化）再截一次。

### B3 `check` 报 `frida-server` 不可达
**原因**：实例重启后设备侧 `frida-server` 进程没了（端口转发也会丢）。
**处理**：重跑第 3 步 `setup-frida`（用本地文件更快，不必再下 110MB）。
**注意**：设备侧没有 `su` 的实例（adbd root）也能跑——工具会自动识别 root 通道。

### B4 点了 SPIN 但采集里没有 `/slots2/spin`
- 游戏不在机台里（只在大厅）→ 先进机台；大厅流量只会看到 `robots/profiles/*.jpg` 之类的资源。
- 采集是在进入机台**之前**启动的、但 hook 尚未就绪 → 重新 `start` 后再转。
- 转盘响应只有 `NO_WIN` 时也可能被漏（罕见），以 `records > 0` 与端点表为准。

### B5 `stop` 报 0 条记录
游戏内没有任何请求发生：没进机台、没点 SPIN、或游戏卡在 LOADING（见 B2）。

### B6 混用 adb 导致 `adb server version doesn't match`
BlueStacks 自带的 `HD-Adb.exe` 是旧协议（v36），与本机 platform-tools（v41）**不能混用**：
混用会杀掉 server 并挂起数分钟。**统一用 platform-tools 的 adb**；必要时
`set ANDROID_ADB_SERVER_PORT=<另一个端口>` 起独立 server 避免与别的任务抢。

### B7 实例身份不确定 / 找不到某个实例
```bash
python tools/env/find_instance.py --package com.playstudios.popslots --conf "<某安装的 bluestacks.conf>"
```
- 一台机器可能有**多套安装**、**实例名重复**；`--instance <名字>` 只在"你所调用的那个
  `HD-Player.exe` 所属安装"内解析。
- **不要贸然启动一个身份未确认的实例**：启动已在运行的实例会让 BlueStacks 抢盘并**关掉原实例**。
- 枚举只按配置键、不要求 `display_name`；必要时用 `--conf` 指定每个 install 的配置文件。

### B8 root 开不了（`adb root` 是 no-op、`su` 被拒）
这是**镜像相关**的：部分蓝叠镜像的 adbd 不真正提权，`su` 又受签名白名单
（`/system/etc/.swl.cfg` + `.sig`）限制，无 root 改不了。
**不要在同一镜像上反复试**；改用：① GUI 里关/开一次 root 开关；② 换/克隆一个有 root 能力的镜像实例；
③ 无 root 路线（gadget 重打包，最侵入）。详见 `artifacts/env/INSTANCE_DESIGNATION.md`。

---

## 四、产物与去向

| 文件 | 内容 |
|---|---|
| `pop_capture/pop_net.jsonl` | 原始采集（**含账号/会话，只留本地，不入 Git**）|
| `pop_capture/autoplay.jsonl` | 自动点击留痕（时间戳/序号/坐标）|
| `pop_capture/slots_values.csv` | **逐次数值**：机台/每线下注/线数/中奖/类型/中奖线/余额/等级/牌面 |
| `pop_capture/slots_summary.md` | **数值汇总**：总下注/总中奖/净变化/实测 RTP/中奖率/类型分布 |
| `pop_capture/capture.log` | 采集进程日志 |

## 五、纪律

- 只碰**指定为研究实例**的那一个；`★ 研究候选` 之外的实例一律不注入。
- 自动点击已获授权，但**次数即消耗上限**；每次都要在 `COLLAB_LOG` 记录次数与消耗。
- 采集到的 JSONL 只留本地；提交到仓库的只能是工具/文档。
