# Collector Current Capabilities

本文梳理 Huuuge Collector 在 TASK-0006 时点的真实能力。它区分运行证据、代码存在和未来计划，不对采集器做任何功能修改。

## 总体结论

当前采集器已经形成一条可由策划 GUI 驱动、在隔离研究环境中被动采集、自动解码并生成脱敏结构目录的闭环。主链路已在本机真实验证，当前策划发布版本为 `1.0.1`。

当前成熟度集中在“广泛采集、结构恢复、目录化和低操作部署”。规范化事实层、模块级数值 Extractor、完整 Git 内 descriptor 重建和另一台电脑的一次性研究环境初始化尚未完成。

## 1. 发布与部署

| 能力 | 状态 | 当前边界 | 证据 |
| --- | --- | --- | --- |
| Windows 安装/更新入口 | 已验证 | `HUUUGE_BOOTSTRAP.cmd` 支持 SVN-first 安装/更新并打开 GUI | release `1.0.1`；SVN r6429；空目录安装验证记录见 `CURRENT_STATUS.md` |
| 日常 GUI 入口 | 已验证 | `HUUUGE_COLLECTOR.cmd` 启动六操作 WinForms GUI | `scripts/huuuge_gui.ps1`；真实 preflight 与 Start/Stop smoke Session |
| Git / SVN / unmanaged source preflight | 已验证主要路径 | 干净源更新；有本地修改时保留并跳过覆盖 | `scripts/huuuge_bootstrap.ps1`；Git/SVN clean-tree 验证记录 |
| Python 环境与依赖准备 | 已验证 | 创建 `.venv` 并安装 `requirements.txt` | 新目录 SVN 安装验证 |
| Runtime descriptor 同步 | 已验证 | 可从受控本机路径同步；SVN 包携带 schema-only descriptor | `scripts/sync_local_runtime.ps1`、`scripts/sync_svn_package.ps1` |
| Git 内 descriptor 可重建 | 待补齐 | `build_descriptors.py` 已存在，但完整 36-file `.proto` 源集尚未提交 Git | `TASKS.md` 仍有未完成项；默认 proto 目录在 Git 中不存在 |
| 安装包安全 allowlist | 已验证 | ZIP 只含 Bootstrap、手册、README、manifest；不含 capture/APK/Frida binary/secret | release `1.0.1` manifest/hash 验证记录 |

## 2. 环境与安全控制

| 能力 | 状态 | 当前边界 | 证据 |
| --- | --- | --- | --- |
| 研究环境唯一目标约束 | 已验证 | 只连接 `127.0.0.1:5565` / `Pie64_1 / HuuugeResearch` | `huuuge_controller.ps1` 常量和真实 smoke Session |
| 普通 BlueStacks 保护 | 已验证 | GUI/Controller 不对普通 `Pie64` 执行 Root 或 instrumentation | `CURRENT_STATUS.md` 的磁盘/配置 hash 与运行验证 |
| Root 身份验证 | 已验证 | 启动前要求 guest `su` 返回真实 `uid=0`；失败时停止，不自动重复 Root | `Assert-ResearchRoot` |
| Frida 版本一致性 | 已验证 | host 与 root x86_64 server 必须匹配 `17.17.0` | `Ensure-FridaServer` 与 Bootstrap preflight |
| ARM64 Gadget 存在性检查 | 已验证 | 只接受研究 APK 目录中的 `libhuuuge-gadget.so` | `Get-GadgetPath` 与 preflight |
| 新电脑一次性研究环境建立 | 待实现/需授权 | SVN 登录、游戏登录、独立模拟器建立和审计过的 Root/host patch 仍需人工授权 | `CURRENT_STATUS.md` blockers |
| 被动研究边界 | 已验证为设计和操作约束 | 不修改余额、奖励、请求或服务端状态 | `AGENTS.md`、Controller/Agent 的只读拷贝链路 |

## 3. 采集与解码

| 能力 | 状态 | 当前边界 | 证据 |
| --- | --- | --- | --- |
| Houdini ARM64 启动链 | 已验证 | 冷启动 App，在真实 native-bridge namespace 中加载 ARM64 Gadget | `bootstrap_houdini_gadget.py`；Gadget 报告 ARM64 module view |
| 高层 RPC Hook | 已验证 | Hook `WriteMessage`、`HandleRequest`、`HandleResponse`，复制 `Casino::RpcMessage` | `agent.js`；proof/broad/smoke Sessions |
| 广泛、非模块过滤采集 | 已验证 | console filter 只影响显示，所有可观察 RPC 都落盘 | `live_decode.py` manifest 字段与 broad capture |
| Descriptor-backed Protobuf 解码 | 已验证 | 解析 wrapper、服务/方法、请求/响应类型和 payload；支持 LZ4 分支 | proof 84/84、broad 741/741、smoke 91/91 decoded |
| 未知/未解码消息保存 | 已实现，待出现样本验证 | 对无 payload descriptor 或解码失败记录 raw、JSONL 元数据和错误；当前已报告 Sessions 均 100% 解码 | `live_decode.py`；尚无已确认 undecoded 样本回归案例 |
| READY 证据关卡 | 已验证 | 同时要求 hooks、至少一个真实 RPC、raw 文件、decoded JSON 和 manifest | `huuuge_controller.ps1`、Session `20260826_110725` |
| Clean Stop/Flush | 已验证 | stop control file → detach/close → manifest `stopped` → lifecycle marker | Session `20260826_110725` |
| 自动生命周期 marker | 已验证 | `collector-start`、`hooks-installed`、`collector-ready`、`collector-stop` | smoke Session marker 检查 |
| 手工模块/行为 marker | 未实现，当前不需要 | GUI 已明确移除手工标注；当前通过时间、endpoint 和字段做自动归类 | `huuuge_gui.ps1`、`CURRENT_STATUS.md`；部分旧 dossier 文案仍需统一 |

## 4. Session 数据产物

| 产物 | 状态 | 内容与边界 |
| --- | --- | --- |
| `manifest.json` | 已验证 | 版本、hash、环境、状态、计数和起止时间 |
| `collector_state.json` | 已验证 | GUI/Controller 使用的实时状态、hooks 和计数 |
| `index.csv` | 已验证 | 每条 RPC 的方向、服务/方法、类型、字节数、解码状态和本地文件引用 |
| `messages.jsonl` | 已验证 | wrapper 元数据、解码结果或错误；可能包含敏感值，只能留本机 |
| `raw/*.rpc.bin` | 已验证 | 原始 wrapper bytes；只留本机 |
| `json/*.json` | 已验证 | 解码后的逐消息 JSON；只留本机 |
| `markers.jsonl` | 已验证 | 自动生命周期事件；没有策划手工 action marker |
| `.local/controller/` | 已验证 | active/last state、控制文件和进程日志；不进入 Git/SVN |

## 5. 后处理与结构目录

| 能力 | 状态 | 当前边界 | 证据 |
| --- | --- | --- | --- |
| 脱敏 RPC inventory | 已验证 | 从 Session 生成 service/method/type/direction/count/decode 聚合 | `scripts/build_rpc_inventory.py`；broad capture 66 rows |
| 脱敏 field-path inventory | 已验证 | 只保留字段路径和标量类型，不保留值 | broad capture 511 observed field-path/type rows |
| Module catalog 生成 | 已验证 | 合并 descriptor、sanitized live、可选本地 variability 和 APK ZPK filename | `scripts/build_module_catalog.py` |
| 结构目录覆盖 | 现有产物 | 37 dossiers；36 proto files；1028 message types；356 service methods | `artifacts/module_catalog/MODULE_INDEX.md` |
| Live 结构覆盖 | 现有产物 | 15 live-confirmed；22 schema-only/live-pending | `modules.csv` 37 rows |
| 规范化事实/事件层 | 待实现 | 只在 `RESEARCH_DATA_ARCHITECTURE.md` 定义，尚无生成器或稳定 schema | `TASKS.md` 未完成项 |
| 系统级 Extractor | 待实现 | Slots/Lottery/Missions/Offers 等尚无正式 normalized extractor | `TASKS.md` 未完成项 |
| Excel/图表/报告 Exporter | 待实现 | 仅规划为下游按需输出 | `RESEARCH_DATA_ARCHITECTURE.md` |

## 6. 操作与协作

| 能力 | 状态 | 当前边界 | 证据 |
| --- | --- | --- | --- |
| 六操作 GUI | 已验证 | Start、Stop/Finalize、Recent、Preflight、AI Handoff、Guide | `scripts/huuuge_gui.ps1` |
| AI-independent capture | 已验证 | 采集与整理不依赖 Codex/Trae | real smoke Session |
| Trae + DeepSeek handoff | 已实现 | 可打开 Trae 并生成/复制固定 prompt | `Invoke-AIHandoff`；Trae 可执行文件已发现 |
| Codex CLI handoff | 已实现，环境阻塞 | 已生成 prompt 和启动分支，但 WindowsApps Codex 在当前 shell `Access denied` | `CURRENT_STATUS.md` |
| Git 工程真相源 | 已验证 | ChatGPT/Codex 协作记录、代码和脱敏产物走 Git | `AGENTS.md` / `CONTRIBUTING.md` |
| SVN 策划发布 | 已验证 | safe allowlist 镜像到 `trunk/HuuugeCollector` | r6429 与 UTF-8 log readback |

## 当前能力边界

当前可以可靠回答“采到了哪些 RPC、它们属于哪些服务/方法、有哪些结构字段、哪些游戏模块已有 live evidence”。

当前不能仅凭已有工具稳定回答完整 RTP/EV、某活动最终数值、购买价值或所有 UI 行为到 RPC 的精确因果关系。此类结论需要更完整的现场样本、规范化模型和模块级 Extractor，并继续区分 Confirmed 与 Hypothesis。
