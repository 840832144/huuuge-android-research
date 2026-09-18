# Pop! Slots 大厅混合氛围系统 · 技术交接（Developer handoff）

> **定位**：本文是给**专业技术开发**的要点交接，不是完整逆向报告。
> TASK-0023 的深度逆向已按所有者指示**收敛**：证据与工具交出去，深挖留给开发。
> 相关：`POP_SLOTS_LOBBY_FORENSICS.md`（结论）、`SLOT_CAPTURE.md` / `OPERATOR_GUIDE.md`（采集）、`artifacts/env/INSTANCE_DESIGNATION.md`（环境）。

---

## 一、一句话结论

Pop! Slots 大厅是**真实多人房间架构 + 服务端填充的模拟用户**：客户端手里有**完整的
"机器人补位"策略函数**（找最满机台 / 坐到最满或最近机位），服务端下发填充用户记录，
大厅角色的头像资源来自带 `robots/` 字样的 CDN 路径。

---

## 二、证据分级（**引用前请看等级**）

### A. 高可信 —— 符号名（来自 `.dynsym`，共 30,695 个导出，名字即实现意图）

文件：`libBigCasino.so`（18.4 MB，ELF64 x86_64，ET_DYN）。地址为**文件虚拟地址**（Ghidra 里 +0x100000）。

**① 机位分配逻辑（`CSlotsFinder`，共 26 个符号）**

| 函数 | 地址 | size | 说明 |
|---|---|---|---|
| `CSlotsFinder::sitUser(CGameableItem*, CShakerAvatar*, char const*)` | `0x0068e230` | 571 | 让某角色坐下（入口） |
| `CSlotsFinder::sitUserAtMostOccupiedSlots(std::string)` | `0x0068e180` | 169 | **坐到"最满"的机位** |
| `CSlotsFinder::sitUserAtNearestSlots(std::string)` | `0x0068dac0` | 169 | 坐到最近的机位 |
| `CSlotsFinder::findMostOccupiedSlots(std::string)` | `0x0068db70` | **983** | **找"最满"的机台**（策略核心，体量最大） |
| `CSlotsFinder::findNearestSlots(std::string)` | `0x0068df50` | 169 | 找最近机台 |
| `CSlotsFinder::processEvent(CEvent const*)` | `0x0068e490` | 549 | 事件驱动入口 |
| `CSlotsFinder::init()` | `0x0068d5e0` | 357 | 初始化 |
| `CSlotsFinder::AUTO_WALKING_TO_MACHINE` | `0x0125ef10` | 8 | 事件 ID 常量（自动走向机台） |

> **对设计原则的直接意义**：客户端确实实现了"**把角色往人多的地方安排**"（most occupied）
> 与"就近安排"两套策略，并由一个 **AUTO_WALKING_TO_MACHINE** 事件驱动 —— 与
> "机台始终有人、热闹感"的设计目标一一对应。

**② 房间/用户（`CRoomUsersManager` 31 个符号、`CRoomUserModel` 21 个符号）**

| 符号 | 地址 | size |
|---|---|---|
| `CShakerServerUserDataParser::parseUserData(void*, CRoomUserModel*)` | `0x00812e90` | **3733**（本项目里最大的"用户解析"函数） |
| `CRoomUsersManager::getUserByShakerId(char const*)` | `0x00a34840` | 9（疑似 PLT 桩） |
| `CRoomUserModel::CRoomUserModel(std::string)` | `0x00a33fb0` | 190 |
| `CAvatarJoinedHandler::onUserJoined(CEvent const*)` | Ghidra: `0x00786770` / `0x00b01a60` | 200 / 115 |

**③ 角色行为状态机**（Frida 实测枚举，见 `tools/analysis/popslots/pop_common.py` 的 `POP_SYMBOLS`）
`CShakerAvatar`、`CShakerAvatarWalkHandler::stopWalking`、`CShakerAvatarWalkToSitActivityHandler::onReachedDestinationCallback`、`CShakerAvatarStandActivityHandler::EVENT_AVATAR_STANDING`、`CShakerAvatarActivityHandlerFactory`

**④ 网络栈**（解释为什么 hook TLS 拿不到明文）

| 符号 | 地址 | size | 说明 |
|---|---|---|---|
| `curl_easy_setopt` | `0x00d8a1ad` | 145 | **实际收发明文的边界（我们用它采集成功）** |
| `SSL_write` | `0x00db3034` | 65 | 真实现（非桩），但业务流量不直接走它 |
| `SSL_write_ex` / `SSL_write_early_data` | `0x00db3075` / `0x00db3084` | 15 / 414 | — |

### B. 中可信 —— 实测协议与资源路径

- **老虎机游玩（明文 JSON，实测抓取）**
  - `GET https://gamesfe.pscapi.com/slots2/startgame?gameId=MGM&assetId=466`
  - `GET https://gamesfe.pscapi.com/slots2/spin?lines=20&bet=2500&BIsi=<序号>&sId=<局ID>`
  - 响应字段：`totalWin` / `winType` / `coinsBalance` / `matrix` / `reelStopPoint` / `wins[]` / `xp.level` / `casinoData[].data.{machineName,totalBet,winAmount,spinTimestamp}`
  - ⚠️ URL 里 `bet` 是**每线**下注，实际每次消耗 = `lines × bet`
- **大厅角色头像资源**：`https://assets.popslotscasino.com/robots/profiles/{male,female}/<英文名>.jpg`
  → 路径里**字面写着 `robots/`**，且名字是常见英文名（Algernon / Patricia / Jayden…），与"填充用户"吻合
- **大厅/社交相关端点**：`liveorcfe.pscapi.com/v1/featured/lobby`、`closetweb.pscapi.com/closet/costumes/*`、`socialfe.pscapi.com/api/social/*`、`pubnub/v3/configuration`（实时消息）、`tournamentsweb`、`eventsfe`、`finance`、`metareport`/`bireport`
- **填充用户样本特征**（前期采样，29 条）：ID 高度聚集（大量 `...0001284xxxx`）、国家 US 为主、
  存在 `Guest827` 类无真名账号；夹少量完整真实资料者。**比例未量化**（见方法学限制）

### C. 低可信 / 未完成 —— 反编译伪代码

- 已用 Ghidra 12.1.3 headless 完成全量分析（**46,859 个函数**，分析耗时 874 秒），项目在
  `D:\DSH_work\ghidra_proj\PopSlots`。
- 但**伪代码目前不可用于语义判断**：该库导入调用大量走 PLT，Ghidra 的
  "Non-Returning Functions" 分析误判了 137 个函数为"不返回"，导致控制流被截断
  （例如 `sitUser` 反编译只剩 262 字符，尾部真实逻辑丢失；`func_0x01290e60` 就是 PLT 桩）。
- 因此**本文不给出任何基于伪代码的逻辑结论**。深挖需要开发投入（见第五节）。

---

## 三、给开发的实现骨架（基于 A/B 证据的推断，非反编译结论）

```
// 推断：大厅"热闹且不挡你"的三层机制
on AvatarSpawn(avatar):
    if avatar.isLocalPlayer:                 # 真人优先
        slots = findNearestSlots(localZone)   # 就近、不抢
    else:
        slots = findMostOccupiedSlots(zone)   # 机器人往人多处聚
        if slots.hasFreeSeat():
            sitUserAtMostOccupiedSlots(zone)
        else:
            sitUserAtNearestSlots(zone)

on EVENT_AUTO_WALKING_TO_MACHINE:             # 客户端存在的事件
    avatar.walkTo(chosenSlot)                 # WalkHandler
    onReachedDestination -> sit              # WalkToSitActivityHandler

// 服务端侧：下发填充用户（parseUserData -> CRoomUserModel -> CRoomUsersManager）
// 这些用户的头像来自 assets.popslotscasino.com/robots/profiles/*
```

**三条设计原则与实现的对应关系**

| 设计原则（来自 forensics） | 客户端对应物（证据） |
|---|---|
| 真人优先 | `sitUserAtNearestSlots`（就近，不与真人争"最满"位） |
| 机器人补足、机台始终有人 | `findMostOccupiedSlots` + `sitUserAtMostOccupiedSlots` |
| 永远给玩家留空位 | 未见"占满"函数；`sitUserAtMostOccupiedSlots` 的语义是"坐到**最满**的机台"而非"坐满所有位"，与留空位一致 |

> ⚠️ 这些是**符号语义层面的对应**，不是从伪代码读出的控制流。实现细节（阈值、抢占/让座时机）
> 需要开发在 IDA/Ghidra 里继续确认。

---

## 四、可直接复用的设施（开发用得上）

| 设施 | 位置 | 用途 |
|---|---|---|
| 数值采集管道 | `tools/analysis/popslots/pop_capture.py`（向导：check/start/spin/stop/export） | 一键采老虎机数值 → `slots_values.csv` + `slots_summary.md` |
| 采集核心 | `pop_net_capture.py`（Frida 挂 curl 边界） | 明文请求/响应，输出与 `tools/capture/` 同形 JSONL |
| 符号级分诊 | `tools/analysis/elf_triage.py`（已入 Git） | 不用 IDA 即可列架构/依赖/导出符号/grep/反汇编 |
| 已分析好的 Ghidra 项目 | `D:\DSH_work\ghidra_proj\PopSlots`（程序 `/libBigCasino.so`） | 直接 `-process -noanalysis` 复用，省 15 分钟分析 |
| Ghidra 脚本 | `D:\DSH_work\tools\ghidra_scripts\`（`ListFuncs` / `DecompileRange` / `DecompileClean`） | 按关键字列函数、按 ELF 真实 size 修函数体、清 noReturn 后反编译 |
| 工具链 | Ghidra 12.1.3 + JDK 21（`D:\Apps\`，便携、无需管理员） | 免费替代，含反编译器 |

**复现一条命令**（列座位分配函数）：

```powershell
$env:JAVA_HOME="D:\Apps\jdk-21.0.12.1+1"; $env:MAXMEM="6G"
D:\Apps\ghidra_12.1.3_PUBLIC\support\analyzeHeadless.bat D:\DSH_work\ghidra_proj PopSlots `
  -process libBigCasino.so -noanalysis -scriptPath D:\DSH_work\tools\ghidra_scripts `
  -postScript ListFuncs.java sitUser SlotsFinder RoomUsers onUserJoined 40
```

> 注意两个坑（都踩过）：① 脚本参数**不能用 `|` 或逗号拼接**（cmd 当管道 / Ghidra 会再切分）；
> ② 复用项目时**必须加 `-noanalysis`**，否则每次重跑 874 秒全量分析。

---

## 五、建议开发接手后先做的三件事

1. **修函数体后重析**：用 `.dynsym` 的 size 强制重建 `CSlotsFinder` 那组函数体（脚本已备）
   → 或在 IDA 里直接看，IDA 对 ELF 导入/PLT 的处理更稳。
2. **确认"留空位"的实现位置**：`findMostOccupiedSlots`(983B) 是最大的一块逻辑，
   值得单独读它如何挑机台、以及是否排除"玩家所在/即将进入"的机台。
3. **量化填充用户比例**：现有采样只有 29 条、比例未量化。用已跑通的采样脚本
   （`pop_parse.py`）在大厅停留足够长时间，统计"填充记录 : 真实记录"，并解释
   forensics 文档里 29/28 的分母差异。

---

## 六、边界与方法学限制（必须随文档一起引用）

- 全流程**只读**：未修改游戏数值、未伪造/重放请求、未改服务器状态。
- `parseUserData` 的采样是**固定长度字节窗口 + 抽 ASCII**，是**模糊转储不是字段映射**：
  能区分"填充/像真人"，拿不到字段语义。
- 采到的用户/数值数据**只留本地**（`C:\bigfish_research\popslots_run_20260918\`），不入 Git。
- 填充用户比例、完整行为循环、跨界面一致性**均未覆盖**，不要从符号名外推为已测行为。
