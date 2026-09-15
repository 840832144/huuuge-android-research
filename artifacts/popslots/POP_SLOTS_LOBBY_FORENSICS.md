# Pop! Slots 大厅仿真系统拆解 —— 真人 + 机器人混合氛围（移植参考）

> 目标：拆解 Pop! Slots 的赌场大厅"真人+机器人混合"机制，对标设计一套
> 能让赌场长期热闹、同时玩家随时可玩的氛围系统（不抢座/不挡座/每台有人/永远给自己留空位）。

---

## 0. 一句话结论

Pop! Slots 的大厅是**真实多人房间架构**（`CRoomUsersManager`/`onUserJoined`/
`parseUserData`）上**叠加服务器填充的模拟用户**（大量 Guest + 聚集 ID + 美国主导），
用一套**角色行为状态机**（站→走→坐→玩→庆祝）让"看起来每个人都在玩"。
**这套行为状态机是可完全对标复刻的** —— 它正是"热闹氛围"的实现核心。

---

## 1. 系统架构（从符号还原）

### 1.1 房间/用户层（真实联机框架）
| 符号 | 作用 |
|---|---|
| `CRoomUsersManager` | 房间用户管理器（管理大厅里所有用户） |
| `CAvatarJoinedHandler::onUserJoined` | **用户加入事件**（新角色进入大厅） |
| `CUserEnterRoomEventHandler` | 用户进入房间处理器 |
| `CMergeRoomEventHandler` | 多房间合并（跨区拉人） |
| `CRoomUserModel` | **每个用户的数据模型**（名字/ID/国家/州/数值） |
| `CShakerServerUserDataParser::parseUserData` | **解析服务器下发的用户数据**（用户来源） |
| `CVenueLoginApiHandler` | 场地登录 API（join payload） |
| `CRTRoomDataUpdateEventHandler` | 房间数据实时更新 |

**关键**：用户是**服务器下发**的（`parseUserData`），大厅是**房间**概念（可合并）。
这决定了：**每个大厅用户都来自服务器数据包，不是客户端本地造**。

### 1.2 角色行为层（行为状态机核心）
| 符号 | 作用 |
|---|---|
| `CShakerAvatar` / `2D` / `3D` | 角色实体（2D/3D 实现） |
| `CShakerAvatarWalkHandler` | 走路（`stopWalking`） |
| `CShakerAvatarWalkToSitActivityHandler` | **走→坐下**（`onReachedDestinationCallback`）|
| `CShakerAvatarStandActivityHandler` | 站立（`EVENT_AVATAR_STANDING`）|
| `CShakerAvatarActivityHandler` | 行为活动基类 |
| `CShakerAvatarActivityHandlerFactory` | **行为工厂**（按状态/机台生成行为） |
| `CAvatarLifeCycleManager` | 角色生命周期 |
| `CAvatarStateEvent` | 角色状态事件 |
| `CSlotsFinder::sitUser` | **找机台并坐下**（`sitUser`）|
| `CRoomDataEvent`/`CRTRoomDataUpdateEvent` | 房间数据更新事件 |

**关键**：这层是**行为状态机**的实现 —— `CSlotsFinder::sitUser`（**找机台坐下**）+
`WalkToSit`（走→坐）+ `Stand`（站）+ 行为工厂。**这是"热闹氛围"的核心引擎**。

---

## 2. 行为状态机（逐个拆）

从符号 + 观察还原的角色行为流程：

```
[Stand 站立/闲逛]
    │  (CSlotsFinder::sitUser 找一台空闲机台)
    ▼
[Walk 走到目标机台]  ← CShakerAvatarWalkHandler
    │  (WalkToSit.onReachedDestinationCallback 到达)
    ▼
[Sit 坐下坐下]  ← CShakerAvatarWalkToSitActivityHandler
    │
    ├─[Play 玩老虎机]  ← 机台状态（转盘/奖励）
    │     └─[Celebrate 庆祝动作]（中奖/特殊）
    │
    └─[Stand 起身换位]  ──→ 回到 Stand，循环
```

**核心规律**：每个角色是一个**状态机**，核心是 `sitUser`（找机台）→ `WalkToSit`（入座）→ 玩 → 起身。**这个状态机保证"一直有人坐下玩"**（热闹），且**坐下是"找机台"**（不塞满）。

---

## 3. 机器人行为规律（你说的疑点 = 填充机器人特征）

从 29 个用户样本统计到的**填充机器人行为/数据规律**：

### 3.1 数据特征（机器人判别）
| 特征 | 证据 | 说明 |
|---|---|---|
| **ID 聚集段** | 25/28 个 ID 后段都是 `0001284xxxx`（`418xx~422xx` 连续）| **ID 密集连续** = 批量生成填充 |
| **国家集中** | 25/28 是 US（美国）| 填充样本用美服主导 |
| **Guest 用户** | `Guest827`（无姓名，只有 Guest+编号+数值 350,000）| **游客占位账号** = 填充特征 |
| **无真名** | 多数样本名字解析是国家名（United States）而非人名 | 填充用户无真实姓名 |
| **少数真资料** | `Sofia Abel`/`Lucy Abel`（人名+州+3,185,909）| **点缀的真实玩家**（营造真实感）|

### 3.2 行为规律
- **坐下→玩**：机器人坐下后**玩机台**（有庆祝动作）
- **走动**：站立角色**走动**（`WalkHandler`），找机台/换位置
- **机台占用**：机台**基本都有人**（`sitUser` 填满），营造热闹
- **混合策略**：**真资料玩家（Sofia/Lucy）+ 填充用户（Guest/聚集ID）混合**，真资料做点缀

### 3.3 仿真策略总结
**Fill-the-floor（填充大厅）模式**：
1. 用**批量生成的模拟用户**（聚集ID/美国/Guest/无真名）填满大厅，让**每台机台有人**
2. 混入**少量真实资料玩家**（Sofia/Lucy 这种有人名+州+数值）**做真实感点缀**
3. 用**行为状态机**（站→走→坐→玩→庆祝）让所有人**看起来在活动**
4. **玩家自己（你）走进去**，机台有空位（`sitUser` 找空位，不挡真实玩家）

---

## 4. 对标你们系统的设计（移植建议）

你们的**核心原则**：真人优先 → 机器人补足 → 每台机台始终有人 → 永远给自己留空位。

### 4.1 行为状态机（对标实现）
```
每个 NPC：
  Idle(站立/闲逛) →
    [系统分配: 优先真实玩家空闲机台, 机器人补足] 找一台空闲机台
  Walk(走过去) →
  Sit(坐下) →
    Play(玩) → 随机时长 →
    [若该机台有真实玩家想坐, 起身让座] → Stand/离开 → 回 Idle
```

### 4.2 关键机制（落实你的原则）
| 你的原则 | 实现机制 |
|---|---|
| **真人优先** | 机台分配时**先给真实玩家**；真实玩家进大厅，优先安排机台 |
| **机器人补足** | 真实玩家不足某台位时，机器人**补位**（Fill-the-floor）|
| **每台机台始终有人** | 机器人在**空机台**补位（`sitUser` 找空机台）|
| **永远给自己留空位** | **保留 N 台空机台**给真实玩家；机器人**不占满**；当真实玩家靠近某机台，该机台机器人**起身让座**|
| **不抢座/挡座** | 机器人**从不占据"玩家正在用/要去"的机台**；机器人在玩家走近时**主动起身/走开** |

### 4.3 机器人数据设计（对标 Pop Slots 的填充数据）
- **ID**：用分散的 ID 段（不要像 Pop Slots 那样聚集，避免被玩家识破）
- **名字**：混合真实风格（人名）+ 游客（Guest），但**别都用同一姓氏**（Pop Slots 的 Abel 姓氏聚集是破绽）
- **国家**：分散（不要全美国），更像真实国际玩家
- **数值**：给每个机器人随机合理的金币/等级
- **行为**：状态机驱动（站→走→坐→玩→庆祝），**随机化时长/路径**，避免机械重复

---

## 5. 避免的坑（Pop Slots 的破绽 → 你们优化）

1. **ID 聚集段**（`0001284xxxx` 连续）→ 机器人身份破绽。**你们用分散 ID**
2. **国家全美国** → 破绽。**你们分散国家**
3. **Guest 太多** → 破绽。**你们控制 Guest 比例，多数用真实风格名**
4. **姓氏重复**（Abel）→ 破绽。**你们名字多样化**
5. **行为机械**（固定动画循环）→ 破绽。**你们随机化行为时长/路径/动作**

---

## 6. 验证方法（移植后如何自测）

对标 Pop Slots 的验证逻辑：
- **抓 `对 bot 的一次 parse`** 看数据（ID/名字/国家是否像真人）
- **观察行为**：机器人是否随机走动/坐机台/庆祝（不机械）
- **统计**：机台占用率（热闹）、真实玩家能否随时坐下（不抢座）
- **长期**：大厅是否持续热闹（机器人随玩家行为动态补位/让座）

---

*注：本报告基于 Pop! Slots（com.playstudios.popslots，Shaker/libBigCasino.so）
符号还原 + 29 个用户数据采样 + 大厅行为观察。符号证据（CRoomUsersManager/
onUserJoined/parseUserData/CShakerAvatar 行为状态机/CSlotsFinder::sitUser）为
最可靠依据。*
