# Pop! Slots 老虎机数据采集 · 操作手册

> 面向不写代码的使用者。**全程只需 3 条命令 + 1 个菜单**，每步都写了"你应该看到什么"。
> 采到的是**具体数值**：下注、中奖、余额、牌面、中奖线、等级。

---

## 为什么不是"设代理抓包"

实测（真机验证）：**Pop! Slots 的引擎不读 Android 全局代理** —— 它直连 :443，
不经过代理；hook 它导出的 TLS 函数也只能拿到密文。
本工具改为在引擎内部的 **curl 边界**取明文（引擎把明文交给 libcurl 的位置），
所以**不需要证书、不需要代理**，只需要一次性的 frida-server。

---

## 第 0 步：一次性准备（只做一次）

```bash
git clone https://github.com/840832144/huuuge-android-research.git
cd huuuge-android-research
pip install frida frida-tools
```

frida-server **不需要你自己找**：第 1 步会自动按你本机的 frida 版本 + 实例 ABI
从 Frida 官方 releases 下载匹配的那个（公开文件，不依赖任何人提供）。

---

## 第 1 步：装 frida-server（一条命令）

先确认实例的 adb 串号（BlueStacks 多开时每个实例不同）：

```bash
adb devices
```

然后（只把 `<串号>` 换成你自己的）：

```bash
python tools/analysis/popslots/pop_capture.py --serial <串号> setup-frida --download
```

如果你想用手上已有的 frida-server 文件，把路径直接给它即可（不用 `--download`）：

```bash
python tools/analysis/popslots/pop_capture.py --serial <串号> setup-frida <frida-server文件>
```

**你应该看到：**
```
  ...    下载 frida-server-17.17.0-android-x86_64.xz ...
  [ok]   已下载并解压：...frida-server-17.17.0-android-x86_64（106.4 MB）
  [ok]   已推送
  [ok]   frida-server 正在运行，端口转发正常（127.0.0.1:27042）
好了。现在可以选 1 复查，然后选 2 开始采集。
```

失败时最常见两种：① 实例没开 root → `adb -s <串号> root` 或在该实例设置里打开 root；
② 网络下载失败 → 手动下载后按上面第二种写法传入文件路径。

---

## 第 2 步：开游戏 + 检查（一条命令）

**先手动打开 Pop! Slots，停在能看见大厅画面。**

```bash
python tools/analysis/popslots/pop_capture.py --serial <串号> check
```

**你应该看到最后一行是：**
```
verdict: READY
```

若有 `[MISS]` 项，按它给的提示补齐即可（它会直接写出该执行什么）。

---

## 第 3 步：开始采集

```bash
python tools/analysis/popslots/pop_capture.py --serial <串号> start
```

**你应该看到：**
```
  [ok]   采集已开始（pid ...）
现在去游戏里操作：进机台 → 点 SPIN 转盘
```

然后**在游戏里操作**（这一步就是正常玩）：

1. 在大厅点一台机台进入
2. 点右下角 **SPIN** 转几盘

想多采就多转几盘，想采别的模块就玩别的模块（采集本身不限定模块）。

### （可选）让工具自动转盘

仓库所有者**已授权自动点击**（限隔离研究实例 + 自有测试账号，见 `AGENTS.md` 的
Safety/scope）。工具会自动定位 SPIN 按钮（基准分辨率 1600x900，其他分辨率按比例缩放），
并在 `pop_capture/autoplay.jsonl` **逐次留痕**：

```bash
python tools/analysis/popslots/pop_capture.py --serial <串号> spin --auto-spin 20
# 位置不准时手动指定： --spin-xy 1464,706
# 调整间隔：           --spin-gap 7
```

注意：每次转盘按当前机台下注消耗游戏币，**次数即消耗上限**，按需设置即可。

---

## 第 4 步：停止采集

```bash
python tools/analysis/popslots/pop_capture.py --serial <串号> stop
```

**你应该看到：**
```
  [ok]   已停止采集
  [ok]   采集文件：...\pop_capture\pop_net.jsonl（NN 条记录）
```
记录数应当 > 0；若是 0，说明游戏里没有产生请求（没进机台 / 没点 SPIN）。

---

## 第 5 步：导出数值

```bash
python tools/analysis/popslots/pop_capture.py --serial <串号> export
```

**你应该看到：**
```
一、抓到哪些端点
  17 endpoint(s):
     gamesfe.pscapi.com /slots2/spin?lines=20&bet=2500...  1x GET  [req:-/resp:json]
    ...
二、导出老虎机数值（CSV）
导出 N 行数值 -> ...\pop_capture\slots_values.csv

  machine | bet | spinIndex | totalWin | winType | winCount | coinsBalance | level
  MGM | 2500 | 12 | 15000.0 | PLAIN_WIN | 3 | 6575000.0 | 4
```

**产出文件**：`pop_capture/slots_values.csv`，一列一个字段，可直接用 Excel 打开。
包含：时间、端点、机台、下注 `bet`/`lines`、中奖 `totalWin`/`winType`、
中奖线数 `winCount`/`winSum`、余额 `coinsBalance`、等级/经验、牌面 `matrix`、`reelStopPoint`。

---

## 想只看某个模块（可选）

工具自带 Pop! Slots 的模块预设（`modules.popslots.json`）：

```bash
# 看看有哪些模块
python tools/capture/select_module.py <采集文件> --modules tools/analysis/popslots/modules.popslots.json --list

# 只留老虎机
python tools/capture/select_module.py <采集文件> --modules tools/analysis/popslots/modules.popslots.json --module slots --out slots.jsonl
```

也可在采集时就只记老虎机（可选）：

```bash
# 在 pop_net_capture.py 上直接过滤路径
python tools/analysis/popslots/pop_net_capture.py <串号> 600 --out slots.jsonl
python tools/capture/select_module.py slots.jsonl --modules tools/analysis/popslots/modules.popslots.json --module slots --out slots_only.jsonl
```

---

## 采集到的数值长什么样（真实样例，已脱敏结构）

`GET gamesfe.pscapi.com/slots2/spin?lines=20&bet=2500&BIsi=12` 的响应是**明文 JSON**：

```json
{ "payload": {
    "totalWin": 15000.0, "winType": "PLAIN_WIN",
    "coinsBalance": 6575000.0, "sId": "5428829742844414976",
    "matrix": [[3,3,9,1,1],[10,9,4,1,9],[4,9,2,2,9]],
    "reelStopPoint": [7,339,213,206,26],
    "wins": [ {"winSum":5000.0,"winLine":2,"winningSymbol":3,
               "coordinates":[{"row":0,"col":0},{"row":0,"col":1},{"row":0,"col":2}]} ],
    "casinoData": [ {"data":{"winAmount":20000.0,"totalBet":50000.0,
                             "machineName":"MGM","spinTimestamp":1789698798518}} ]
}}
```

---

## 常见问题

| 现象 | 原因 / 处理 |
|---|---|
| `check` 报 `frida-server` 不可达 | 没做第 1 步，或实例重启后 frida-server 掉了 → 重跑第 1 步 |
| `setup-frida` 报端口不通 | 手动补一次 `adb -s <串号> forward tcp:27042 tcp:27042` |
| 停止后记录数是 0 | 游戏里没产生请求：先确认已进机台并点了 SPIN |
| 只采到 `robots/profiles/*.jpg` | 只在大厅没进机台 → 进机台转盘即可 |
| `slots_values.csv` 行数少于转盘次数 | 有些转盘响应没有 JSON（例如断线重连），属正常 |
| frida 报版本不匹配 | 重新下载与 `frida --version` 一致的 frida-server |

## 说明

- 采集内容含账号/会话/数值：**只留本地，不要提交到 Git**（`.gitignore` 已排除 `*.jsonl`）。
- 实例重启后：frida-server 需要重新 `setup-frida`。
- 本手册对应的工具（全部在仓库内，无本机绝对路径）：
  `pop_capture.py`（向导）、`pop_net_capture.py`（采集）、`pop_spin_export.py`（导数值）、
  `pop_doctor.py`（自检）、`modules.popslots.json`（模块预设）。
