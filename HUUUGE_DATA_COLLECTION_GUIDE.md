# Huuuge Casino 数据采集与部署说明

> 面向策划 / 数值 / 数据分析人员的完整说明。目标是让使用者尽量只需要“打开工具 → 正常玩 → 结束采集 → 看结果”，而不是学习 Android 逆向、Frida 或 Protobuf。

## 0. 先看这一页：策划实际需要做什么

日常使用希望最终压缩为四步：

```text
1. 双击 HUUUGE_BOOTSTRAP.cmd
          ↓
2. 工具确认“采集环境可用 / 可以开始玩”
          ↓
3. 正常操作 Huuuge：老虎机、乐透、任务、活动、礼包……
          ↓
4. 停止采集，让本地 AI / 分析脚本整理本次 Session
```

第一次在一台新电脑部署时，会比日常使用多出几个一次性步骤：GitHub 登录、Codex 登录、创建独立 BlueStacks 研究实例，以及对研究环境做 Root / Frida 部署。这些步骤完成后不应反复执行。

项目的核心原则不是“逆向得越复杂越好”，而是：

> **部署方便、操作简单、采集尽量全、原始证据保留、分析按需进行。**

---

## 1. 这个项目解决什么问题

Huuuge Casino 的数值体系分散在很多系统里，例如：

- Slots / Spin / Jackpot；
- Lottery / Sweepstakes / Draw；
- Missions / Quests；
- Battle Pass / MiniPass；
- Vault / Live Events / Milestones；
- Collection / Collectibles；
- Offers / Shop / Purchase / Free Gifts；
- Rewards / Mystery Reward / Hourly Bonus；
- Loyalty / VIP / Fame / Progression；
- Clubs / Charms / Trading；
- Currency / Balance / Economy Stats；
- 以及后续发现的其他模块。

如果只靠录屏 + OCR，每研究一个模块都要重新录制、识别、人工整理，而且很难拿到完整的隐藏字段。

本项目改成直接记录客户端已经处理过的结构化消息：

```text
用户正常操作游戏
        ↓
Huuuge 客户端收到/发出 RPC
        ↓
在客户端内部被动复制 Casino.RpcMessage
        ↓
使用恢复出的 Protobuf Schema 解码
        ↓
保存 Raw + JSON + Index
        ↓
统一模块目录
        ↓
需要研究哪个模块，再从历史 Session 深挖哪个模块
```

因此一次游戏操作可以服务很多后续问题，不需要每次从头录屏。

---

## 2. 核心设计原则

### 2.1 策划层与技术层分离

策划层只应该看到：

- 首次部署；
- 环境是否 Ready；
- 开始采集；
- 停止采集；
- 本次抓到了哪些模块；
- 想进一步研究哪个模块。

策划不需要手动处理：

- ADB 命令；
- Root 验证；
- Frida Server；
- ARM64 Gadget；
- Houdini native bridge；
- Protobuf Descriptor；
- RPC service / method 映射；
- Raw/JSON 文件组织。

这些由脚本和本地 AI 负责。

### 2.2 Structure first, values later

先建立整个游戏的模块结构地图，再逐步补真实数值。

一个模块可以处于：

- `observed-live`：真实运行中已经抓到专用 RPC / 字段；
- `live-confirmed (cross-cutting/config only)`：真实数据中出现相关配置字段，但还没抓到专门交互；
- `schema-only / live pending`：Proto 已经知道结构，但玩家还没有实际触发对应系统；
- `inferred`：根据字段和上下文推断，需要更多样本验证。

用户以后玩到哪个模块，就继续把该模块的档案补完整。

### 2.3 全量采集，按需展示

采集器的 console filter 只控制屏幕上显示什么，不能影响底层保存。

例如终端只显示 Battle Pass，不代表只保存 Battle Pass。Slots、Offers、Rewards、Unknown RPC 等仍然必须写入 Session。

### 2.4 Raw 永远是底层证据

每个 Session 同时保存：

- 原始 RPC wrapper；
- decoded JSON；
- service/method/type 索引；
- 时间戳与方向；
- 后续将增加 session manifest 和 action markers。

如果未来 Schema、字段解释或模块归类发生变化，可以从 Raw 重新解析，不需要重新玩。

---

## 3. 已验证的实验环境

当前已完整验证的机器环境为：

| 项目 | 当前验证环境 |
|---|---|
| Host | Windows |
| 模拟器 | BlueStacks 5 China `5.22.170.6509` |
| Android | 9 |
| 正常实例 | `Pie64 / BlueStacks 5`，保持未 Root |
| 研究实例 | `Pie64_1 / HuuugeResearch` |
| 研究 ADB | `127.0.0.1:5565` |
| 模拟器架构 | `x86_64` |
| Huuuge ABI | `arm64-v8a` |
| Native Bridge | Houdini / `libnb.so` |
| Huuuge 包名 | `com.huuuge.casino.slots` |
| 已验证版本 | `12.07.27012` / versionCode `1784198526` |
| Frida | `17.17.0` |
| Host Frida Server | Android x86_64 |
| Huuuge 内部 Gadget | Android ARM64 |
| 主 native 模块 | `libClawApp.so` |
| Schema | 已恢复 36 个 Proto descriptor 文件 |

当前研究实例已经证明真实 `uid=0(root)` 可用；普通 `Pie64` 的关键磁盘文件哈希在实验前后保持一致，Root flag 保持 `0`。

---

## 4. 为什么需要 x86_64 Server + ARM64 Gadget 两层 Frida

BlueStacks 是 x86_64 Android，但 Huuuge 的原生核心是 ARM64：

```text
Windows x86_64
    ↓
BlueStacks Android x86_64
    ↓
Houdini / Native Bridge
    ↓
Huuuge ARM64 libClawApp.so
```

只运行 x86_64 Frida Server 时，可以控制外层 Android/Houdini 进程，但看不到 ARM64 `libClawApp.so` 的完整模块视图。

当前方案因此使用：

```text
x86_64 Frida Server
    │ 负责 Root 环境 / 外层进程控制
    ↓
Houdini Native Bridge
    │
ARM64 Frida Gadget
    │ 负责 Huuuge ARM64 模块视图
    ↓
libClawApp.so hooks
```

`bootstrap_houdini_gadget.py` 会在 Huuuge 冷启动时捕获真实 native-bridge namespace，并通过同一个 namespace 加载 ARM64 Gadget。

---

## 5. 实际 Hook 的位置

目前主要观察：

```text
Casino::Connection::WriteMessage(...)
Casino::Connection::HandleRequest(...)
Casino::Connection::HandleResponse(...)
```

这些位置处于客户端已经拥有结构化 Protobuf 数据、但还没有被外层网络加密/传输逻辑完全遮蔽的位置。

采集器只复制数据，不修改参数、返回值、筹码、奖励或服务器状态。

---

## 6. Protobuf 与 RPC 恢复

静态分析从 `libClawApp.so` 中恢复了序列化的 Protobuf descriptor，并建立：

- 36 个 Proto 文件；
- 1028 个 message 类型；
- 34 个 service；
- 356 个 service method；
- `Casino.RpcMessage` wrapper；
- request / response / update payload 映射。

因此采集到的二进制 RPC 不需要 OCR，可以直接解成有字段名的 JSON。

---

## 7. 当前数据输出格式

每次采集创建独立 Session，例如：

```text
captures/20260825_182300/
  index.csv
  messages.jsonl
  raw/
    *.rpc.bin
  json/
    *.json
```

后续计划增加：

```text
  manifest.json
  markers.jsonl
```

### index.csv

用于快速浏览：

- 时间；
- 方向；
- service；
- method；
- payload 类型；
- decode 是否成功；
- raw/json 文件位置。

### raw/*.rpc.bin

原始证据。未来解释变化时可以重跑。

### json/*.json

按恢复出的 Protobuf Schema 解码后的结构化数据。

### messages.jsonl

便于批量处理和二次分析。

---

## 8. 当前已经验证到什么程度

第一轮完整自由探索 Session：

- 741 条 RPC；
- 741 / 741 成功解码；
- 42 个实际出现的 `service.method` endpoint。

当前模块目录：

- 37 个模块 dossier；
- 15 个模块已有 live 证据；
- 22 个模块仍以 schema-only / live pending 为主；
- 36/36 Proto 文件覆盖；
- 1028/1028 message 类型覆盖；
- 356/356 service method 覆盖。

当前真实数据较完整的结构包括：

- Slots；
- Offers；
- Rewards；
- Player/Lobby；
- MiniPass；
- Vault；
- Loyalty；
- Progression；
- Charms；
- Purchases；
- Other LiveOps。

Lottery 已看到共享配置中的真实字段，但专门的 Lottery 交互 RPC 仍待补充。

Battle Pass、通用 Missions、Conquest、Sweepstakes、Adventure、Tournaments、Race、Elites、Personal Awards、Vouchers、Non-Spin Bonus 等仍需要以后通过实际游玩补 live 样本。

---

## 9. 模块目录如何使用

详细结构位于：

```text
artifacts/module_catalog/
  MODULE_INDEX.md
  modules.csv
  endpoints.csv
  fields.csv
  <37 个模块 dossier>.md
```

每个模块档案会整理：

- 对应 Proto；
- service / method；
- request / response / update 关系；
- entity id；
- state / progression；
- cost / input；
- reward / output；
- timing / reset / expiry；
- eligibility / segment / limit；
- 当前 live 样本数量；
- 已出现字段；
- 缺失内容；
- 下次用户需要做什么操作才能补齐。

这样策划不需要先决定“我要研究 Battle Pass 还是 Slots”，可以先正常玩，数据逐渐沉淀到对应模块。

---

## 10. 首次部署：推荐流程

### 10.1 策划视角

理想入口只有一个：

```text
HUUUGE_BOOTSTRAP.cmd
```

它负责尽量自动完成安全步骤：

1. 创建/定位本地项目目录；
2. Git clone 或 pull 最新仓库；
3. 检查 Git / Python / ADB / BlueStacks；
4. 安装 Python requirements；
5. 同步本地 descriptor / APK 信息；
6. 生成环境预检报告；
7. 如果本机有 Codex CLI，让 Codex 自动阅读项目文档并给出部署状态；
8. 已经部署过的机器直接判断是否 Ready；
9. 新机器若需要 Root / Frida 首次安装，转入本地 AI 引导，只在真正修改机器前要求一次确认。

### 10.2 为什么首次 Root 不直接静默执行

当前 BlueStacks China 方案需要修改研究实例的 guest `su`，并涉及 BlueStacks 共用 host binary 的已审计 patch。

这是一次性部署操作，但属于机器级变化。因此通用部署脚本不应在使用者毫不知情时直接修改。

推荐方式：

```text
Bootstrap 自动完成安全检查
        ↓
本地 AI 阅读 AI_DEPLOYMENT_PLAYBOOK.md
        ↓
展示将修改的文件、备份位置、回滚方法
        ↓
用户确认一次
        ↓
仅对 HuuugeResearch 执行部署
        ↓
验证 uid=0 + Frida + Gadget + RPC
```

普通 BlueStacks 实例永远不作为研究目标。

---

## 11. 本地 AI 的角色

本地 AI（当前优先 Codex CLI）不是数据源，而是“机器操作员”。

它负责：

- 自动读 Git 文档；
- 根据 `CURRENT_STATUS.md` 判断当前机器做到哪一步；
- 检查本机路径和版本；
- 调用已有脚本；
- 避免让策划复制粘贴大量命令；
- 第一次部署时完成 Root / Frida / Gadget 的机器特定工作；
- 出错时把证据写回协作日志；
- 后续采集完自动生成 inventory / module catalog。

本地 AI 必读：

```text
AGENTS.md
CONTRIBUTING.md
HUUUGE_DATA_COLLECTION_GUIDE.md
AI_DEPLOYMENT_PLAYBOOK.md
CURRENT_STATUS.md
TASKS.md
COLLAB_LOG.md（最新部分）
```

### Codex CLI

Windows 上 Codex CLI 可以作为推荐本地 AI。首次安装/登录属于一次性人工步骤；登录完成后可以由脚本使用 `codex exec` 让 AI 非交互读取仓库并做安全预检。

---

## 12. 一键 Bootstrap 当前设计

仓库根目录提供：

```text
HUUUGE_BOOTSTRAP.cmd
```

以及实际逻辑：

```text
scripts/huuuge_bootstrap.ps1
```

Bootstrap 的目标是“安全自动化”，不是“无提示地改机器”。

自动完成：

- 找到/更新 Git 项目；
- Python 依赖；
- descriptor 同步/构建；
- BlueStacks/ADB 基础检测；
- `.local/` 环境报告；
- Codex 文档预读/部署评估（Codex 已安装时）。

保留确认：

- GitHub 首次认证；
- Codex 首次登录；
- BlueStacks Root/host patch；
- 任何可能影响已有模拟器数据的机器级操作。

---

## 13. 日常采集：目标操作体验

首次部署完成后，目标是：

```text
打开采集入口
   ↓
自动检查研究实例 / Frida / Gadget
   ↓
显示：READY，可以开始玩
   ↓
策划正常操作 Huuuge
   ↓
停止采集
   ↓
自动保存 Session
   ↓
自动生成 RPC Inventory
   ↓
更新 Module Catalog
   ↓
AI 告诉策划：本次新增了哪些模块/字段
```

策划无需记录技术命令。

如果有必要做行为对齐，后续 action marker 也应做成按钮/快捷输入，例如：

```text
进入 Slots A
开始 Spin
打开 Lottery
领取 Mission
打开 Offer
```

而不是要求用户记时间戳。

---

## 14. 后续分析能做什么

模块数据积累到一定程度后，可以针对指定系统生成：

### Slots

- game / room / machine id；
- bet；
- win；
- spin result；
- jackpot；
- feature/free-spin 状态；
- session 级消耗与返还；
- RTP/波动/体验统计（需足够样本后再做）。

### Lottery / Draw

- ticket / entry；
- cost；
- draw timing；
- prize tiers；
- payout；
- odds / weight（仅在数据可观察时）。

### Mission / Pass / Event

- requirement；
- progress；
- action type；
- reward；
- reset / expiry；
- milestone；
- reward track；
- skip / premium / segmentation。

### Offers / Economy

- price；
- reward composition；
- currency；
- quantity；
- limits；
- eligibility；
- expiry；
- segment / offer trail。

### 输出

后续可以按需求生成：

- CSV；
- Excel；
- 图表；
- 模块说明；
- 数值体验报告；
- 参数/奖励结构表；
- 系统间货币流转关系。

---

## 15. 安全与数据边界

本项目只做被动研究：

- 不修改筹码；
- 不修改奖励；
- 不伪造请求；
- 不重放请求获取优势；
- 不修改服务器状态；
- 不对正常 `Pie64` 做 instrumentation。

Git 中不提交：

- APK；
- proprietary `.so`；
- Frida 二进制；
- 账号 ID；
- session token；
- 原始含账号信息 capture；
- 密钥/密码/cookie。

Raw 数据默认只保存在本地研究目录。

---

## 16. 当前限制

### 16.1 RPC 不一定等于全部数学逻辑

某些系统可能把权重、概率、状态机或配置放在：

- GameServer 其他消息；
- Lua；
- native object；
- ZPK；
- 静态配置。

RPC 是当前最优主数据源，但不是唯一来源。

### 16.2 第一轮 Session 没有 action marker

当前可以确认哪些接口/字段出现过，但不能把所有 RPC 精确对应到每一次鼠标点击。

后续需要补：

- `manifest.json`；
- lightweight `markers.jsonl`。

### 16.3 新电脑不能做到真正“完全零交互”

有三类事情必须至少确认一次：

1. GitHub 私有仓库认证；
2. 本地 AI/Codex 登录；
3. Root / host patch 等机器级修改。

除此之外的流程尽量自动化。

---

## 17. 故障恢复原则

如果环境异常：

1. 不要修改正常 `Pie64`；
2. 先读 `.local/` 预检报告；
3. 让本地 AI 读取 `CURRENT_STATUS.md` 和最新 `COLLAB_LOG.md`；
4. 检查研究实例 ADB / root / Frida / Gadget 哪一层失败；
5. 不重复盲改 BlueStacks 配置；
6. Root/host patch 必须使用已有备份和哈希记录回滚。

当前已验证环境的完整备份记录保存在项目状态文档中。

---

## 18. 推荐目录角色

```text
huuuge-android-research/
  HUUUGE_BOOTSTRAP.cmd                # 策划入口
  HUUUGE_DATA_COLLECTION_GUIDE.md     # 完整说明
  HUUUGE_DATA_COLLECTION_OVERVIEW.md  # 简版说明
  AI_DEPLOYMENT_PLAYBOOK.md           # 本地 AI 操作说明
  CURRENT_STATUS.md                   # 当前事实
  TASKS.md                            # 下一步

  artifacts/live_probe/               # 采集器
  artifacts/module_catalog/           # 模块结构目录
  artifacts/recovered/                # Proto / RPC 恢复结果
  scripts/                            # 自动化脚本

  .local/                             # 本机状态/报告，不进 Git
  captures/                           # Raw Session，不进 Git
```

---

## 19. 最终目标

最终希望一个策划在已经准备好的研究机上不需要理解逆向细节：

```text
双击工具
  ↓
看到 READY
  ↓
正常玩
  ↓
停止
  ↓
AI 自动告诉你：
“本次新增了 Slots / Lottery / Mission 的哪些结构和数据”
  ↓
你说：
“现在把 Lottery 的数值体验详细拆出来”
  ↓
再生成专项 Excel / 图表 / 结论
```

也就是说，这个项目最终不是一套“逆向脚本集合”，而是一套 **面向策划的、可持续积累的 Huuuge 数据采集与数值研究工作台**。
