# Huuuge Collector — Codex Handoff

- Updated: 2026-08-26 16:32 +08:00
- Actor: Codex
- Task: TASK-0006
- State: Waiting for ChatGPT Review
- Product release: `1.0.1`

## Objective

整理采集器现状、能力清单、数据流、软件模块关系和 TODO Roadmap，不开发或修改采集功能。

## Completed

- 安全同步 Git，并对照 `AGENTS.md`、`CONTRIBUTING.md`、`CURRENT_STATUS.md`、最新 `COLLAB_LOG.md`、`TASKS.md` 和 `CHANGELOG.md`。
- 审计 Windows launchers、Bootstrap、GUI、Controller、Houdini/Gadget 启动、Frida Agent、live decoder、inventory builder、module catalog builder、release publisher 和现有脱敏产物。
- 新增 `docs/collector/CURRENT_CAPABILITIES.md`，以证据区分已验证、已实现待补验证、现有产物和待实现。
- 新增 `docs/collector/DATA_FLOW.md`，记录部署、采集、解码、Finalize 与数据分区。
- 新增 `docs/collector/MODULE_MAP.md`，记录软件职责、调用关系、关键耦合和下游 37 个游戏域的关系。
- 新增 `docs/collector/ROADMAP.md`，将 ChatGPT Review 设为开发前置关卡。

## Confirmed Current State

- release `1.0.1` 的 Bootstrap、六操作 GUI、Start → READY → Stop/Finalize 主链路已有真实验证。
- proof capture 84/84、broad capture 741/741、smoke Session 91/91 已 descriptor-decode。
- 当前 module catalog 有 37 dossiers、1028 message types、356 service methods；15 live-confirmed、22 schema-only/live-pending。
- Capture/Finalize 不依赖 AI；Codex/Trae 只用于可选 repair、interpretation 和 export。
- GUI 没有模块选择或手工行为 marker；只有自动 lifecycle markers。
- 本次没有执行 ADB、Frida、BlueStacks、SVN 或采集器运行时操作，没有修改 `feishu-doc-mcp` 或任何游戏/服务端状态。

## Confirmed Gaps / Risks

- 完整 recovered `.proto` 源集不在 Git，`build_descriptors.py` 目前不能仅凭干净 Git checkout 重建 descriptor。
- normalized fact/event layer、Slots/Lottery/Missions/Offers Extractor 和 Excel/report exporter 尚未实现。
- 已有 Sessions 全部 100% decode，未知/未解码消息的保存分支存在但缺少真实回归样本证明。
- 当前 shell 无法运行 WindowsApps Codex CLI，因此 Codex safe-preflight 未被证明。
- 新电脑的一次性 SVN/game login、独立研究模拟器和 Root/host patch 仍需明确人工授权。
- 部分生成 dossier 的 next-action 文案仍要求手工 marker，与当前 GUI 工作流不一致。

## Files for Review

- `docs/collector/README.md`
- `docs/collector/CURRENT_CAPABILITIES.md`
- `docs/collector/DATA_FLOW.md`
- `docs/collector/MODULE_MAP.md`
- `docs/collector/ROADMAP.md`
- `CURRENT_STATUS.md`
- `TASKS.md`

## Constraints

- 不在 ChatGPT Review 前开始 Roadmap 开发。
- 不修改普通 `Pie64`，只允许隔离的 `Pie64_1 / HuuugeResearch`。
- 不修改请求、余额、奖励或服务端状态。
- Raw、decoded values、账号/会话标识、APK、native/Frida binary 和 secrets 不进入 Git/SVN。

## Exact Next Action

ChatGPT 审阅 `docs/collector/`，返回 Accepted 或逐项修订意见。若接受，再由 User/ChatGPT 从 Roadmap 中选择唯一下一阶段；Codex 不自行启动实现。
