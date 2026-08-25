# Huuuge Casino Android 数值逆向 — Codex 接手文档

> 目标：让 Codex 直接接管后续操作，不再让用户手工逐条执行命令。
>
> 研究范围：用户自己的 BlueStacks / Huuuge Casino 测试环境；目标是被动采集和拆解系统、活动、任务、奖励、礼包、里程碑等数值，不修改金币、奖励、请求或服务端状态。

---

## 1. 最终目标

用户希望调研 Huuuge Casino Android 版的系统与活动数值。

原方案依赖：

`录屏 -> AI 看视频 -> OCR -> 人工整理`

问题是长视频容易漏帧、OCR 读错大数、弹窗/滚动页面信息不完整。

新的目标链路是：

```text
BlueStacks 中正常运行 Huuuge Casino
        ↓
动态观测客户端已经解密/序列化的 RPC
        ↓
Casino.RpcMessage
        ↓
service_index + method_index
        ↓
恢复出的 Protobuf descriptors
        ↓
按真实 message 类型自动解码
        ↓
JSON / CSV
        ↓
活动数值表 / Excel
```

目标示例：

```text
Battle Pass:
level
requirement
free_reward
premium_reward
deluxe_reward
daily_mission
weekly_mission
progress
action_type
limitation
pass_level
pass_points_balance
...
```

---

# 2. 用户本机当前环境

## Windows / ADB

ADB 已安装：

```text
C:\platform-tools\adb.exe
```

ADB 已成功连接 BlueStacks：

```text
emulator-5554   device
```

已经验证：

```powershell
C:\platform-tools\adb.exe devices
```

曾返回：

```text
List of devices attached
emulator-5554   device
```

不要假设 PID 永远不变；每次动态分析重新查询。

---

## BlueStacks

当前 BlueStacks Android：

```text
Android 9
```

系统 ABI：

```text
x86_64,x86,arm64-v8a,armeabi-v7a,armeabi
```

Huuuge package：

```text
com.huuuge.casino.slots
```

Huuuge package 的 ABI 已确认：

```text
primaryCpuAbi=arm64-v8a
secondaryCpuAbi=null
```

`dumpsys package` 还看到：

```text
legacyNativeLibraryDir=/data/app/com.huuuge.casino.slots-.../lib
```

游戏进程曾经的 PID：

```text
4087
```

此 PID 只是当时值，后续必须重新 `pidof`。

重要：BlueStacks host/system 首选 ABI 是 x86_64，但 Huuuge 安装的是 ARM64 native split。
这意味着它可能经过 BlueStacks native bridge / ARM translation。
**Frida server 架构与 attach 可行性必须现场验证，不要只根据 APK 的 arm64-v8a 就拍板。**

建议检查：

```powershell
C:\platform-tools\adb.exe shell getprop ro.dalvik.vm.native.bridge
C:\platform-tools\adb.exe shell getprop ro.product.cpu.abi
C:\platform-tools\adb.exe shell getprop ro.product.cpu.abilist
C:\platform-tools\adb.exe shell pidof com.huuuge.casino.slots
```

如有 root 后，再检查 `/proc/<pid>/maps`、`/proc/<pid>/exe` 等判断实际运行形态。

---

# 3. Root / Debuggable 当前状态

已经执行：

```powershell
C:\platform-tools\adb.exe shell id
```

结果：

```text
uid=2000(shell) gid=2000(shell) ...
```

执行：

```powershell
C:\platform-tools\adb.exe root
```

显示：

```text
restarting adbd as root
```

但随后 `shell id` 仍然是：

```text
uid=2000(shell)
```

因此 **adb root 实际没有获得 root**。

执行：

```powershell
C:\platform-tools\adb.exe shell su -c id
```

或 `su` 检测，结果：

```text
/system/bin/sh: su: not found
```

执行：

```powershell
C:\platform-tools\adb.exe shell run-as com.huuuge.casino.slots id
```

结果：

```text
run-as: setegid(AID_PACKAGE_INFO) failed: Operation not permitted
```

所以：

- 当前实例无可用 root；
- `run-as` 不可用；
- 不能直接依赖普通 `frida-server` attach；
- 下一步优先在 **克隆的研究实例** 上解决 root，若失败再考虑 Gadget / 其他研究模拟器；
- 不要先破坏用户的主实例。

---

# 4. BlueStacks 配置发现目前卡点

之前假设默认数据目录：

```text
C:\ProgramData\BlueStacks_nxt\bluestacks.conf
```

但用户机器上该路径不存在。

执行：

```powershell
Get-ItemProperty 'HKLM:\SOFTWARE\BlueStacks_nxt' -ErrorAction SilentlyContinue |
Select-Object Version,InstallDir,DataDir
```

没有输出。

执行：

```powershell
Select-String "C:\ProgramData\BlueStacks_nxt\bluestacks.conf" ...
```

报：

```text
路径不存在
```

所以 BlueStacks 可能是：

- 自定义安装/数据目录；
- 注册表键不在该路径；
- 或不同版本/渠道布局。

**Codex 下一步首先自动发现真实 BlueStacks 安装目录和 data dir，不要让用户自己找。**

建议 Codex 自己执行：

```powershell
Get-CimInstance Win32_Process |
Where-Object { $_.Name -match 'HD-Player|BlueStacks' } |
Select-Object Name,ExecutablePath,CommandLine
```

然后查询可能注册表：

```powershell
Get-ChildItem HKLM:\SOFTWARE,HKCU:\SOFTWARE -ErrorAction SilentlyContinue |
Where-Object { $_.Name -match 'BlueStacks' }
```

也可以：

```powershell
Get-ChildItem 'HKLM:\SOFTWARE\WOW6432Node' -ErrorAction SilentlyContinue |
Where-Object { $_.Name -match 'BlueStacks' }
```

再从实际 fixed drives / BlueStacks process path 附近定位：

```text
bluestacks.conf
Engine\
HD-Player.exe
BstkSVC.exe
```

避免一开始对整块磁盘做无边界慢速递归；优先从 process path、service path、registry 推 data path。

如果发现 clone/research 实例，辨认其内部 instance id，例如：

```text
Pie64
Pie64_1
...
```

原则：

**主实例不改；研究实例可备份配置后尝试。**

---

# 5. 已拉取 APK

安装路径当时：

```text
package:/data/app/com.huuuge.casino.slots-I1Tgs_EqghrLV5nwRBMgIw==/base.apk
package:/data/app/com.huuuge.casino.slots-I1Tgs_EqghrLV5nwRBMgIw==/split_config.arm64_v8a.apk
package:/data/app/com.huuuge.casino.slots-I1Tgs_EqghrLV5nwRBMgIw==/split_config.hdpi.apk
package:/data/app/com.huuuge.casino.slots-I1Tgs_EqghrLV5nwRBMgIw==/split_config.zh.apk
```

已经成功 pull 到用户 Windows：

```text
C:\huuuge_apk\base.apk
C:\huuuge_apk\split_config.arm64_v8a.apk
C:\huuuge_apk\split_config.hdpi.apk
C:\huuuge_apk\split_config.zh.apk
```

大小当时约：

```text
base.apk                         73,255,588 bytes
split_config.arm64_v8a.apk      37,749,561 bytes
split_config.hdpi.apk              174,513 bytes
split_config.zh.apk                135,577 bytes
```

如果 Codex workspace 能直接读取这些路径，应优先复用，不要重新 pull，除非游戏升级/路径变化。

---

# 6. APK 静态逆向已确认的核心事实

## 核心 native module

ARM64 split 里最重要的库：

```text
lib/arm64-v8a/libClawApp.so
```

已提取版本约：

```text
35,147,600 bytes
```

这是当前动态 hook / Ghidra / symbols 分析的主目标。

当前构建保留了大量有价值 C++ 符号。

---

## Lua

`libClawApp.so` 中确认存在 Lua API / Lua integration 痕迹，例如：

```text
lua_State
lua_getfield
lua_setfield
lua_pushnumber
luaL_checkinteger
lua_next
luaL_ref
Casino::LuaCallback
Claw::Lua
ConnectionLuaInterface
```

所以 C++ + Lua 客户端架构已经确认。

不过当前优先级不是先逆 Lua，而是先截 Protobuf 活动数据，因为数值很可能服务端下发。

---

## ZPK 资源

`base.apk/assets` 里大量 `.zpk`，例如：

```text
data-hc.zpk
data-games.zpk
data-slots.zpk
data-embedded-paks.zpk

atlas_battle_pass_common_2_etc2.zpk
atlas_collection_event_2_etc2.zpk
atlas_liveops_sku_hc_2_etc2.zpk
atlas_vault2_sku_hc_2_etc2.zpk

sound_charms.zpk
sound_collection_event.zpk
sound_conquest.zpk
sound_loyalty.zpk
sound_vault.zpk
```

ZPK 文件头观察到：

```text
5A 50 4B 00
Z P K \0
```

native strings/symbols 中还发现过与资源容器和压缩相关的痕迹，例如：

```text
Claw::ZMount
MountPak
PakTracker
LZ4
ZSTD
zlib
```

ZPK 后续可以逆，但当前不是第一优先级。

---

# 7. 最大成果：Protobuf descriptors 已恢复

从 `libClawApp.so` 中恢复了 **36 个 `.proto` schema** 对应的 serialized FileDescriptorProto。

恢复结果中包括：

```text
Adventure.proto
AppCharge.proto
AppClient.proto
AppServer.proto
Baccarat.proto
BattlePass.proto
Blackjack.proto
Clubs.proto
Common.proto
CommonGameClient.proto
ContactPoint.proto
ContentTournament.proto
Definition.proto
Elites.proto
GameHost.proto
GameServer.proto
Htf.proto
HtfApp.proto
HuuugeLogin.proto
Lottery.proto
MiniPass.proto
NonSpinBonusGame.proto
Offers.proto
PersonalAwards.proto
ProxyTestServer.proto
Purchases.proto
Race.proto
Roulette.proto
Rpc.proto
Services.proto
Slots.proto
Sweepstakes.proto
Texas.proto
Vault.proto
VideoPoker.proto
Vouchers.proto
```

机器可读 descriptor set 已在原始分析阶段生成；Git 仓库中不跟踪该二进制文件，而是通过 `scripts/build_descriptors.py` 从恢复出的 `.proto` 文件可复现生成。

已生成：

```text
proto_inventory.csv
service_method_map.csv
```

这意味着动态抓到 RPC 后，不需要 `protoc --decode_raw` 盲猜字段号，可以按真实 message type 自动解码。

---

# 8. RpcMessage wrapper

从 `Services.proto` 恢复：

```proto
message RpcMessage {
    required Type type = 1;
    required int32 service_index = 2;
    required int32 method_index = 3;
    repeated bytes payload = 4;
    optional int64 user_id = 5;
    optional uint32 seq_number = 6;
    optional uint32 uncompressed_payload_size = 7;
    optional ProxyError proxy_error = 8;
    optional uint32 method_hash = 9;
}
```

已确认主要 service index：

```text
0 = AppServer
1 = AppClient
```

`service_method_map.csv` 保存全部 method index/type mapping。

---

# 9. Battle Pass 已恢复字段

## BattlePassMilestone

```text
1  level           int32
2  requirement     int64
3  free_reward     BattlePassReward
4  premium_reward  BattlePassReward
5  deluxe_reward   BattlePassReward
```

## BattlePassMission

```text
id
set_id
type
status
progress
requirement
action_type
limitation
reward
reward_bundle_id
hbi_name
segment_id
skippable
```

## BattlePassUpdateRequest

```text
status
event_id
battle_pass_id
daily_expire
pass_expire
pass_type
pass_level
pass_points_balance
tutorial_completed
premium_product
deluxe_product
unlock_level
daily_mission
weekly_mission
milestone
final_bundle
config_hbi_data
art_config
prestige
mission_skip_balance
event_items
```

## BattlePassGetMilestonesResponse

```text
status
error_code
milestone
final_bundle
```

因此只要抓到真实 BattlePass update/milestone 响应，就能直接做奖励轨、需求积分、任务进度等结构化表。

---

# 10. 已恢复的 Battle Pass RPC mapping

AppServer：

```text
139 BattlePassGetDailyMissions
140 BattlePassGetWeeklyMissions
141 BattlePassGetMilestones
142 BattlePassTutorialCompleted
143 BattlePassSkipMission
```

AppClient：

```text
53 BattlePassUpdate
54 BattlePassMissionProgressUpdate
55 BattlePassLevelCompleted
56 BattlePassPremiumUpdate
```

完整 mapping 见：

```text
service_method_map.csv
```

---

# 11. 动态 hook 设计已经做好

已经生成一个 `huuuge_live_probe`。

关键 hook 目标：

```text
Casino::Connection::WriteMessage(google::protobuf::Message const&)
Casino::Connection::HandleRequest(Casino::RpcMessage const&)
Casino::Connection::HandleResponse(Casino::RpcMessage const&)
Casino::RpcMessage::ByteSize() const
Casino::RpcMessage::SerializeWithCachedSizesToArray(unsigned char*) const
```

已写 `agent.js`：

- 等待 `libClawApp.so` 加载；
- 通过 exact symbols 找地址；
- hook `WriteMessage / HandleRequest / HandleResponse`；
- 验证对象 vtable 是 `Casino::RpcMessage`；
- 调用游戏自己的 `ByteSize()` 和 `SerializeWithCachedSizesToArray()`；
- 只复制 RPC bytes；
- 不改函数参数/返回值，不修改游戏状态。

Python `live_decode.py`：

- Frida attach；
- 接收 RPC bytes；
- 读取 `huuuge_descriptors.pb`；
- 解析 `Casino.RpcMessage`；
- 根据 `service_index + method_index + RpcMessage.Type` 找 request/response descriptor；
- 支持 LZ4 payload；
- 输出 JSON/CSV/raw；
- 支持活动 filter。

预期输出：

```text
captures/YYYYMMDD_HHMMSS/
  index.csv
  messages.jsonl
  raw/*.rpc.bin
  json/*.json
```

运行样例（root/Frida 成功后）：

```powershell
py live_decode.py --filter BattlePass,MiniPass,Vault,Offer,Collection,Conquest,Charm,Loyalty
```

以及：

```powershell
py live_decode.py --filter BattlePass --all-json
```

---

# 12. 为什么 hook 高层 RPC，不优先 MITM

静态分析已经表明核心连接链里有：

```text
Claw::MbedTlsStreamSocket
Claw::WebSocket
Casino::Connection
RpcMessage
```

并发现 `Connection` 层在更高层直接处理 Protobuf。

当前方案的原则：

```text
客户端已经解密/准备序列化
       ↓
hook 高层 Connection / RpcMessage
       ↓
复制明文结构
```

因此不优先做：

```text
Charles
安装 CA
SSL pinning 绕过
抓 TLS ciphertext
```

原因：高层拿结构化 Protobuf 更直接、稳定、对活动数值更有价值。

---

# 13. Codex 当前第一任务

## A. 自动发现 BlueStacks 真实安装 / data dir

不要问用户去找。

优先检查运行进程：

```powershell
Get-CimInstance Win32_Process |
Where-Object { $_.Name -match 'HD-Player|BlueStacks' } |
Select-Object Name,ExecutablePath,CommandLine
```

必要时检查 services / registry。

定位：

```text
HD-Player.exe
bluestacks.conf
Engine\
instance id
```

确认是否已经有 clone 的 `HuuugeResearch` 实例；如果没有，可通过 BlueStacks Multi-instance 机制创建/克隆，但尽量由 Codex调用现有 CLI/GUI可控方式，不让用户手工敲配置。

---

## B. 主实例绝对不作为 root 实验场

必须优先：

```text
正常实例：保留
研究 clone：所有 root / Frida 实验在这里
```

任何修改 `bluestacks.conf` 前：

1. 停止相关 BlueStacks 进程；
2. 备份配置；
3. 明确 instance id；
4. 只修改研究 instance；
5. 保留一键恢复。

不要因为网上某个旧版教程就直接改主实例。

---

## C. 判断 BlueStacks 当前版本能否通过内置 root flags 获得 root

可能的历史配置键包括：

```text
bst.feature.rooting
bst.instance.<id>.enable_root_access
```

但不同 BlueStacks 版本行为不同。

Codex要先：

- 找真实 config；
- 找当前版本；
- 读取已有 key；
- 做备份；
- 只在研究 instance 尝试；
- 启动后验证 `adb shell id` 或 `su -c id`；
- 如果失败，不要无限叠加未知 patch。

---

## D. Root 成功后：部署匹配的 Frida server

原则：

- host Python `frida` 与 Android `frida-server` 版本必须一致；
- BlueStacks 是 x86_64 系统但 Huuuge 是 ARM64 app/native split；
- native bridge 可能影响 attach。

因此先验证：

```text
ro.product.cpu.abi
ro.product.cpu.abilist
ro.dalvik.vm.native.bridge
Huuuge pid
/proc/<pid>/maps
```

然后实际测试：

```text
frida-ps -U
```

能否看到并 attach Huuuge。

**不要把“APK 是 arm64”简单等价成“server 一定选 android-arm64”。**
Frida server 应匹配 Android 运行环境；native bridge 场景必须实测。

如果 x86_64 Frida server 能列出进程但无法正确 instrument ARM-translated app，应停止浪费时间，考虑：

1. 一个真正 ARM64/rooted Android emulator/device；
2. 或 Frida Gadget 注入 ARM64 app；
3. 或其他能运行 ARM64 且支持 root/debug 的研究环境。

---

# 14. 如果 BlueStacks root 路线失败

Fallback 优先级：

## 方案 1：Frida Gadget 测试版 APK

对 pulled APK 创建研究版：

- arm64-v8a Gadget；
- 重打包；
- 新签名；
- 只安装到独立研究 instance；
- 不覆盖用户正常 Google Play 版本。

风险：

- 签名变化；
- Google Play / integrity / login 可能受影响；
- split APK 与 native library loading 需处理；
- 可能需要 patch manifest/loader。

所以它是 root clone 失败后的方案，不是第一选择。

## 方案 2：换可 root 的研究模拟器 / 设备

如果 BlueStacks ARM translation 让 Frida 非常难用，考虑创建独立 Android ARM64 research environment。

目标只是活动数值采集，不要求继续执着 BlueStacks。

---

# 15. 动态抓通后的优先采集顺序

先不要一次全抓。

### 第一优先：Battle Pass

因为 schema / RPC mapping 已经验证最完整。

打开：

```text
Battle Pass 主界面
任务页
奖励轨
付费轨
领取动作前后
```

观察：

```text
BattlePassUpdate
BattlePassGetMilestones
BattlePassGetDailyMissions
BattlePassGetWeeklyMissions
BattlePassMissionProgressUpdate
BattlePassLevelCompleted
```

先验证解码链条。

### 第二优先：

```text
MiniPass
Vault
Offers / purchases
Collection event
Conquest
Charms
Loyalty
```

通过 `service_method_map.csv` 与 descriptors 自动检索相关 RPC。

---

# 16. 最终数据模型

建议输出统一活动事实表：

```text
system
event_id
event_name
screen/action
timestamp
rpc_service
rpc_method
message_type
field_path
value
before
after
source
```

并生成针对活动的宽表，例如 Battle Pass：

```text
level
requirement
free_reward_type
free_reward_value
premium_reward_type
premium_reward_value
deluxe_reward_type
deluxe_reward_value
cumulative_requirement
```

任务：

```text
mission_id
set_id
type
action_type
requirement
progress
limitations
reward
reward_bundle_id
segment_id
skippable
```

后续可以继续算：

```text
累计门槛
阶段边际成本
奖励价值
单位积分价值
免费/付费轨价值比
礼包性价比
活动消耗与产出
任务权重
完成成本
```

---

# 17. 现有文件 / 工具

本 handoff 包里包含：

```text
artifacts/recovered/
  proto_inventory.csv
  service_method_map.csv
  BattlePass_schema.md
  Rpc_wrapper.md
  recovered_protos/*.proto

artifacts/live_probe/
  agent.js
  live_decode.py
  check_device.ps1
  start_frida_server.ps1
  requirements.txt
  service_method_map.csv
  README.md
```

用户 Windows 上已有 APK：

```text
C:\huuuge_apk\base.apk
C:\huuuge_apk\split_config.arm64_v8a.apk
```

用户之前解压 live probe 的路径：

```text
C:\huuuge_live_probe
```

Codex应优先检查这些路径是否存在，然后直接继续，不要要求用户重复下载/执行已经完成的步骤。

---

# 18. 操作风格要求

用户切换到 Codex 的核心诉求就是：

> 不要再让用户一条条复制命令；Codex自己在本机执行、检查结果、继续迭代。

所以：

1. 能自动执行就自动执行。
2. 不重复问已经知道的信息。
3. 遇到路径差异先自行 discovery。
4. 任何破坏性修改先备份。
5. 主游戏实例保持原状。
6. 研究行为以被动读取/抓包/逆向为主。
7. 不做金币篡改、奖励伪造、请求重放、服务端状态修改。
8. 每取得阶段成果，把可复现脚本和结果写回 workspace。
9. 把“已确认事实”与“推测/下一步实验”分开记录。

---

# 19. Codex 建议 workspace

建议在用户本机创建：

```text
C:\huuuge_research\
```

结构：

```text
C:\huuuge_research\
  apks\
  static\
  proto\
  live_probe\
  captures\
  scripts\
  notes\
  backups\
```

可以链接/复制现有：

```text
C:\huuuge_apk\
C:\huuuge_live_probe\
```

不要移动或删掉原文件，先复制/引用。

---

# 20. Codex 第一轮执行完应给用户什么

不要只说“root成功/失败”。

至少输出：

```text
1. BlueStacks 真实版本 / install dir / data dir
2. 主实例 id 与研究实例 id
3. root 当前可行性
4. native bridge / Huuuge process 架构判断
5. Frida server 选择依据
6. frida-ps -U 是否成功
7. 是否能 attach com.huuuge.casino.slots
8. agent.js 三个 hook 是否成功安装
9. 是否抓到首条 RpcMessage
10. 是否能自动解码 BattlePass RPC
11. captures 保存位置
```

如果动态链路暂时失败，也要留下：

- exact error；
- 已排除的原因；
- 下一 fallback；
- 不要求用户重做前面成功过的步骤。
