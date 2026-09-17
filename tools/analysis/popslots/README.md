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
| `pop_common.py` | **共享公共层**：adb 路径/串号/PID 解析/输出目录/符号名解析（其它脚本都基于它）|
| `pop_syms.py` | **枚举 `libBigCasino.so` 符号**（默认按 player/lobby/avatar/room/seat/... 过滤）—— 定位分析入口，最常用 |
| `pop_parse.py` | **hook `CShakerServerUserDataParser::parseUserData`**，采样服务器下发的每个大厅用户 —— 判定机器人特征的核心 |
| `pop_users_sampler.py` | `pop_parse.py` 的**常驻版**（等价于 `--seconds 0`，Ctrl+C 结束）|
| `pop_behaviour.py` | hook 角色行为状态机（stop-walking / arrived-to-sit / stand / getName）统计行为事件 |
| `pop_behaviour_syms.py` | `pop_syms.py` 的**行为过滤版**（ActivityHandler/Walk/Sit/Stand/...）|
| `pop_net_syms.py` | 全模块搜索 TLS/网络符号（确认真实 TLS 栈在哪 —— 结论：内嵌在 `libBigCasino.so`）|
| `pop_webview.py` | 判断大厅是原生 Shaker 渲染还是 WebView（HTML5）；APK 路径用 `pm path` 动态解析 |
| `pop_state.py` | 进程状态排查（前台 Activity / 线程数 / 窗口 / logcat 尾部）|
| `pop_proto.py` | 查业务连接（TCP 端点 + 远端 IP 反查）与已加载的网络/TLS 库 |
| `pull_bigcasino.py` | 从已安装 APK 提取 `libBigCasino.so`（ABI 目录自动发现）供静态分析 |
| `pop_shot.py` | 截图 + 打印进程/引擎基本事实 |

## 公共参数（所有脚本都支持）

```
--serial SERIAL   adb 串号或 host:port         （env POP_SERIAL，默认 127.0.0.1:5565）
--frida ADDR      已转发的 frida-server 地址    （env POP_FRIDA， 默认 127.0.0.1:27044）
--package NAME    游戏包名                     （env POP_PACKAGE，默认 com.playstudios.popslots）
--pid PID         直接指定 PID，跳过探测
--outdir DIR      输出目录                     （env POP_OUTDIR，默认当前目录）
--adb PATH        adb 可执行文件路径            （env ADB，默认 PATH 再查常见安装位置）
```

例：
```bash
# 1) 先看大厅/社交相关符号
python pop_syms.py --serial 127.0.0.1:5565
# 2) 采样服务器下发的用户（60 秒），结果写到当前目录
python pop_parse.py --serial 127.0.0.1:5565 --outdir . --seconds 60
# 3) 抓取引擎库做静态分析
python pull_bigcasino.py --serial 127.0.0.1:5565 --outdir .
```

> 若本机有多个 adb 版本互相冲突（另一任务起了旧版 daemon），可给工具设
> `ANDROID_ADB_SERVER_PORT=<端口>` 用独立 adb server 隔离。

## 关键符号（分析结论，供对齐）

- 房间/用户：`CRoomUsersManager`、`CAvatarJoinedHandler::onUserJoined`、
  `CShakerServerUserDataParser::parseUserData`、`CRoomUserModel`
- 角色行为：`CShakerAvatar`、`CShakerAvatarWalkHandler`、
  `CShakerAvatarWalkToSitActivityHandler`、`CShakerAvatarStandActivityHandler`、
  `CShakerAvatarActivityHandlerFactory`、`CSlotsFinder::sitUser`

## ⚠️ 方法学边界（引用结论前必读）

`pop_parse.py` / `pop_users_sampler.py` 对 `CRoomUserModel` 的处理是：
**读取固定长度的字节窗口（默认 220B）并抽出可打印 ASCII**。
这是**模糊转储，不是字段映射**：

- ✅ 能拿到：身份字符串（id / 人名 / 国家 / 州）与数值，足以区分"填充记录"和"像真人的记录"
- ❌ 拿不到：结构化字段定义、字段类型、字段偏移语义

因此 forensics 报告里「缺字段语义」的判断是成立的 —— **不要把它的输出描述成"已解析出字段"**。

## 注意

- 符号**一律按名字在 attach 时解析**（`POP_SYMBOLS` + `findSym`），ASLR 安全；
  **脚本内不再有任何硬编码地址**。若某次游戏更新改了 mangled name，
  脚本会打印 `symbols missing=[...]`，改 `pop_common.POP_SYMBOLS` 即可。
- PID 解析顺序：`--pid` → `pidof` → Python 侧解析 `ps -A`（不依赖设备端管道细节）。
- 输出默认落在**当前目录**，不再写死到作者机器的路径。
- Frida server 需在该实例以 root 运行并转发端口（见 `artifacts/popslots/ENVIRONMENT_LOCK.md`）。
- 采到的用户样本（`pop_users.jsonl` 等）含账号相关数据，**只留本地，不入 Git**
  （`.gitignore` 已排除 `*.jsonl`）。

## 修订记录

- 2026-09：首版脚本硬编码了作者机器的 adb 路径、输出目录、游戏 PID 与符号地址。
  现已全部去除（改用 `pop_common.py`）：PID/adb/串号/输出/符号名均可配置或运行时解析；
  `pop_webview.py`/`pull_bigcasino.py` 里写死的「APK 安装哈希路径」也改为 `pm path` 动态解析。
  删除了与 `pop_parse.py` 重复的一次性脚本 `pop_users_sample.py`。
