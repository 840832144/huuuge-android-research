# Pop! Slots 分析工具（tools/analysis/popslots）

Pop! Slots（`com.playstudios.popslots`）大厅/机器人行为分析脚本。
引擎是 **Shaker**（`libBigCasino.so`，x86_64 原生，非 Houdini）。

分析结论与设计对标见：`artifacts/popslots/POP_SLOTS_LOBBY_FORENSICS.md`
（真人+机器人混合氛围系统拆解）。环境见 `artifacts/popslots/ENVIRONMENT_LOCK.md`。

## 用途：判定大厅里的角色是真玩家还是机器人，并拆行为规律

思路：Pop! Slots 大厅是「真实多人房间架构」上叠加**服务器填充的模拟用户**。
判定靠两件事 —— **用户数据**（ID/名字/国家是否像真人）和**行为状态机**
（站→走→坐→玩→庆祝）。

| 文件 | 用途 |
|---|---|
| `pop_syms.py` | **枚举 `libBigCasino.so` 符号**（按关键词过滤 player/lobby/avatar/room/bot）—— 定位分析入口，最常用 |
| `pop_parse.py` | **hook `CShakerServerUserDataParser::parseUserData`**，读每个服务器下发用户的身份字段（ID/名字/国家/州/数值）—— 训练/判定机器人特征的核心 |
| `pop_users_sampler.py` | 常驻采样：连续抓多个 `parseUserData`，统计名字/ID/国家的**多样性 vs 聚集**（机器人判别）|
| `pop_users_sample.py` | 一次性采样版 |
| `pop_behaviour.py` | hook 角色行为状态机（walk/sit/stand 等）统计行为事件 |
| `pop_behaviour_syms.py` | 枚举行为相关符号（ActivityHandler/Walk/Sit/Stand/...）|
| `pop_net_syms.py` | 全模块搜索 TLS/网络符号（确认游戏真实 TLS 栈所在，如 BigCasino 内嵌）|
| `pop_webview.py` | 判断大厅是原生 Shaker 渲染还是 WebView（HTML5）|
| `pop_state.py` | 进程状态排查（前台 Activity / 线程 / 窗口）|
| `pop_proto.py` | 查业务连接与协议（TCP/UDP、IP 反查）|
| `pull_bigcasino.py` | 从 APK 提取 `libBigCasino.so` 供静态分析 |
| `pop_shot.py` | 截图工具 |

## 关键符号（分析结论，供对齐）

- 房间/用户：`CRoomUsersManager`、`CAvatarJoinedHandler::onUserJoined`、
  `CShakerServerUserDataParser::parseUserData`、`CRoomUserModel`
- 角色行为：`CShakerAvatar`、`CShakerAvatarWalkHandler`、
  `CShakerAvatarWalkToSitActivityHandler`、`CShakerAvatarStandActivityHandler`、
  `CShakerAvatarActivityHandlerFactory`、`CSlotsFinder::sitUser`

## 注意

- 这些脚本按 **PID / 符号名** 解析（ASLR 安全），但运行前需确认当前进程 PID
  （脚本内会自行 `ps` 查）。
- Frida server 需在该实例以 root 运行并转发端口（见 ENVIRONMENT_LOCK.md）。
- 抓到的用户样本（`pop_users.jsonl`）含账号相关数据，**只留本地，不入 Git**。
