# Huuuge 数据采集实验说明（简版）

## 1. 目的

本实验用于对 **Huuuge Casino Android 客户端**进行被动数据采集与结构化研究，目标不是只分析 Battle Pass，而是逐步建立覆盖老虎机、乐透、任务、活动、礼包、奖励、VIP/成长等模块的完整数据底座。

核心思路是：

> **先把客户端已经接收/发送并处理过的数据完整记录下来，再按模块整理结构，最后根据研究需求单独做数值分析。**

实验只做观察、复制和解析，不修改筹码、奖励、请求或服务器状态。

---

## 2. 本次实验环境

- 操作系统：Windows
- 模拟器：BlueStacks 5 China `5.22.170.6509`
- Android：Android 9
- 普通实例：`Pie64 / BlueStacks 5`，保持未 Root，不用于采集
- 研究实例：`Pie64_1 / HuuugeResearch`
- 研究实例 ADB：`127.0.0.1:5565`
- 模拟器主架构：`x86_64`
- Huuuge APK 架构：`arm64-v8a`
- ARM 转译层：BlueStacks Houdini / native bridge
- Huuuge 版本：`12.07.27012`
- Frida：`17.17.0`
  - x86_64 Frida Server：用于模拟器 Root 环境和进程控制
  - ARM64 Frida Gadget：用于进入 Houdini 中的 ARM64 Huuuge 原生代码环境
- 主要原生模块：`libClawApp.so`
- Protobuf：已恢复 36 个 `.proto` 描述文件，并建立 RPC service/method 映射

研究实例的 Root、BlueStacks 主程序修改和虚拟磁盘修改均在操作前做了备份和 SHA-256 校验；普通 `Pie64` 实例的数据盘和 Root 状态保持不变。

---

## 3. 部署结构

整体链路如下：

```text
Windows
  │
  ├─ ADB / Python / Frida
  │
  ▼
BlueStacks HuuugeResearch（Root）
  │
  ├─ x86_64 Frida Server
  │
  ▼
Houdini / Native Bridge
  │
  ├─ ARM64 Frida Gadget
  │
  ▼
Huuuge ARM64 进程
  │
  ├─ libClawApp.so
  │   ├─ Casino::Connection::WriteMessage
  │   ├─ Casino::Connection::HandleRequest
  │   └─ Casino::Connection::HandleResponse
  │
  ▼
Casino.RpcMessage
  │
  ▼
live_decode.py
  │
  ├─ raw RPC
  ├─ decoded JSON
  ├─ index.csv
  └─ messages.jsonl
  │
  ▼
RPC Inventory / Module Catalog / 后续数值分析
```

由于 BlueStacks 本身是 x86_64，而 Huuuge 的核心原生代码是 ARM64，因此不能只依赖普通 x86_64 Frida Server。当前方案通过冷启动时获取真实 native-bridge namespace，再把 ARM64 Gadget 加载到同一进程中，从而能够直接观察 `libClawApp.so` 内部的 RPC 流程。

---

## 4. 采集流程

当前采集流程基本为：

1. 启动 `HuuugeResearch` 研究实例；
2. 使用 `bootstrap_houdini_gadget.py` 冷启动 Huuuge，并加载 ARM64 Frida Gadget；
3. 使用 `live_decode.py` 连接 Gadget；
4. 在游戏正常运行过程中，被动复制客户端已经处理过的 `Casino.RpcMessage`；
5. 根据恢复出的 Protobuf Descriptor 自动识别 service、method 和 payload 类型；
6. 将原始 RPC 和解码后的 JSON 同时保存在本地；
7. 游戏操作结束后，通过脚本生成 service/method 清单、字段覆盖表和模块结构目录；
8. 后续用户想研究哪个模块，再基于已有原始数据做更深的数值提取和展示。

采集器的 filter 只影响终端显示，不影响底层数据保存，因此可以长期保持“全量采集、按需分析”的模式。

---

## 5. 目前可以做什么

当前系统已经能够：

- 捕获 Huuuge 客户端可观察到的 `Casino.RpcMessage`；
- 自动识别 RPC 的 service / method / request / response / update 类型；
- 通过恢复出的 Protobuf Schema 将 payload 解码成结构化 JSON；
- 保存原始 RPC，便于未来 Schema 或解释变化后重新解析；
- 统计不同系统实际出现过哪些接口和字段；
- 将静态 Proto 结构与真实运行数据结合，建立模块级结构档案；
- 区分：
  - `observed-live`：真实运行中已经出现；
  - `schema-only`：Proto 中已经知道结构，但尚未采到真实样本；
  - `inferred`：根据字段或上下文推断，仍需更多数据确认；
- 后续可以针对单个模块继续生成专门的 CSV / Excel / 图表 / 数值模型。

目标模块包括但不限于：老虎机、Jackpot、Lottery、Missions、Battle Pass、MiniPass、Vault、Collection、Conquest、Offers、Rewards、Loyalty/VIP、Clubs、Charms、Progression、Currency/Economy 等。

---

## 6. 当前验证结果

当前已经完成一次无过滤的自由探索采集：

- 采集 RPC：**741 条**
- 成功解码：**741 / 741**
- 不同 `service.method`：**42 个**

基于恢复出的 Schema 和这批真实数据，目前已经建立：

- **37 个模块结构档案**
- **15 个模块已有 live 证据**
- **22 个模块目前为 schema-only / live pending**
- 已覆盖 36/36 Proto 文件、1028/1028 message 类型、356/356 service method

当前真实数据较丰富的模块包括 Slots、Offers、Rewards、Player/Lobby、MiniPass、Vault、Loyalty、Progression、Charms 等。

Lottery 已经在共享配置消息中看到相关字段，但尚未采到专门的 Lottery 交互 RPC；Battle Pass、通用 Missions、Conquest 等模块目前主要还是 Schema 结构，等待后续实际游玩补充。

---

## 7. 当前限制

这套方案记录的是**客户端能够观察到的数据**，并不意味着所有游戏数学逻辑都会通过 RPC 下发。

部分系统未来可能还需要结合：

- GameServer 其他消息；
- Lua 状态；
- `libClawApp.so` 内部对象或常量；
- ZPK / 静态配置资源。

另外，当前第一轮自由探索没有精确的点击/行为 marker，因此可以确定“哪些 RPC 和字段出现了”，但无法把所有消息精确对应到用户的每一次点击。后续会补充 session manifest 和轻量 action marker。

---

## 8. 后续使用方式

后续不需要每次重新搭环境。

推荐工作方式是：

```text
开始采集
  ↓
正常玩一批游戏内容
  ↓
停止并保存 Session
  ↓
更新对应模块结构档案
  ↓
继续积累
  ↓
选择某个模块
  ↓
做深度数值提取 / Excel / 图表 / 体验分析
```

也就是说，当前已经从“一次性的逆向实验”转成了一套可以持续积累的 **Huuuge 数值研究数据采集框架**。
