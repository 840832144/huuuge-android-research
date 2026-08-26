# Huuuge Collector Architecture Index

本目录是 TASK-0006 对 Huuuge Collector 当前状态的只读架构整理。内容基于 Git `main`、已提交脚本、已验证 Session 和已生成的脱敏目录，不代表新增功能。

## 文档

- [`CURRENT_CAPABILITIES.md`](CURRENT_CAPABILITIES.md) — 当前能力、证据、边界与缺口。
- [`DATA_FLOW.md`](DATA_FLOW.md) — 部署、采集、解码、整理和数据边界。
- [`MODULE_MAP.md`](MODULE_MAP.md) — 软件模块关系及其输入/输出。
- [`ROADMAP.md`](ROADMAP.md) — 从 ChatGPT Review 开始的 TODO Roadmap。

## 状态语义

- **已验证**：已有真实环境、真实 Session 或发布包验证证据。
- **已实现，待补验证**：代码路径存在，但目标环境或异常分支尚未端到端证明。
- **现有产物**：已有静态/脱敏输出，不等于运行能力完整。
- **待实现**：只有架构、任务或脚本骨架，不能对外宣称可用。

审计基线：`2026-08-26`，Git commit `a67bc31`。下一步必须先由 ChatGPT Review，本目录不授权继续开发。
