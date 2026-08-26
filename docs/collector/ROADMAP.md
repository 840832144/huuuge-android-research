# Collector TODO Roadmap

本 Roadmap 以 TASK-0006 的文档化结果为起点。当前没有授权继续开发；首个关卡是 ChatGPT Review。

## Phase 0 — Architecture Review

状态：**Waiting for ChatGPT Review**

- [ ] 审阅 `CURRENT_CAPABILITIES.md` 中“已验证 / 已实现待验证 / 待实现”的分级。
- [ ] 审阅 `DATA_FLOW.md` 的本地敏感数据、Git、SVN 三类边界。
- [ ] 审阅 `MODULE_MAP.md` 的职责和耦合描述是否与当前源码一致。
- [ ] 确认下一阶段优先目标，避免同时推进采集、Extractor 和部署重构。

退出标准：ChatGPT 给出 Accepted / Needs changes，并把决定记录到协作日志或任务状态。

## Phase 1 — Reproducibility and Documentation Consistency

状态：Planned

- [ ] 在合规和仓库体积审阅后，版本化完整 36-file recovered `.proto` source set。
- [ ] 验证 `build_descriptors.py` 生成的 descriptor 与已验证 runtime descriptor 等价。
- [ ] 统一旧文档/dossier 中“手工 action marker”措辞与当前“无模块选择、自动生命周期 marker”工作流。
- [ ] 为 Session manifest、state、inventory 和 module tables 固化 schema/version 兼容规则。
- [ ] 在可调用 Codex CLI 的环境证明 safe-preflight 与中文 assessment。

退出标准：干净 Git checkout 能重建 schema backbone；文档没有 marker/能力状态冲突；关键结构产物有稳定版本契约。

## Phase 2 — Broad Evidence Enrichment

状态：Planned

- [ ] 进行新的 unrestricted normal-play capture，覆盖当前可访问的主要系统，不要求策划选择模块。
- [ ] 为 Lottery、Missions、Battle Pass、Conquest、Tournaments 等 live-pending dossier 补充真实 evidence。
- [ ] 证明 unknown/undecoded RPC 的 raw/error/aggregate 保留路径，而不是只依赖 100% decoded Sessions。
- [ ] 每次 capture 后先更新既有 37 dossiers，再决定是否拆分 `other_protocol` 新模块。
- [ ] 记录 game version、descriptor hash 和 Session lineage，避免跨版本混合结论。

退出标准：新增 Session 可复现整理，目录覆盖被证据提升，未知/未解码数据不会丢失。

## Phase 3 — Normalized Analytical Layer

状态：Future

- [ ] 定义 normalized event/fact schema、stable IDs、raw references 和 evidence labels。
- [ ] 建立首个高价值 gameplay Extractor；候选为 Slots，需 User/ChatGPT 选择。
- [ ] 建立一个 meta/economy Extractor；候选为 Missions 或 Offers。
- [ ] 以命名 schema 验证 JSON/CSV 输出，不在 Capture Layer 写死业务模块。
- [ ] 只有在字段含义和样本覆盖充分时，才计算 RTP、EV、付费价值或最终数值结论。

退出标准：至少一个 gameplay 和一个 meta/economy 模块能从 preserved Session 生成可追溯 normalized output。

## Phase 4 — Planner Reporting and Release Closure

状态：Future

- [ ] 在 normalized outputs 之上增加按需 Excel/图表/报告模板。
- [ ] 在另一台 Windows 电脑验证首次安装和显式授权的一次性研究环境建立。
- [ ] 重新验证 release package、SVN allowlist、UTF-8 log 和 Feishu 手册一致性。
- [ ] 只在功能或操作行为真正变化后发布新版本；纯架构文档 Review 不触发产品版本升级。

退出标准：策划可以从已验证的 normalized data 获得可追溯报告，且新机器部署边界清晰、无静默机器级修改。

## 优先级原则

1. 先完成 Review 和可重建性，再扩大功能。
2. 先保留 broad evidence，再做单模块深度模型。
3. 先建立 normalized lineage，再做 Excel/图表。
4. 任何数据解释都区分 Confirmed、Hypothesis 和 Derived。
5. 不修改游戏请求、余额、奖励或服务端状态。
