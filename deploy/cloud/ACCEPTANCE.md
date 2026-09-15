# TASK-0031 验收记录

- 日期：2026-09-15
- 执行：Codex；Subagents: none
- 范围：[Issue #1 v3](https://github.com/840832144/huuuge-android-research/issues/1)
- 当前状态：代码与部署准备待 Review；真实云端验证待资源。
- User 已明确：资源尚未就绪，先完成代码与部署准备。

## 真实三项验收

| 验收项 | 本轮实际结果 | 缺少的证据 |
| --- | --- | --- |
| 网页登录并正常玩 | 未执行 | 实例与网页授权入口、User 亲自登录并操作 |
| 本轮新增采集且成功解码 | 未执行；捕获/成功/失败计数均 unknown | 云端连接、实际 build/ABI/descriptor、真实普通操作及对应业务响应 |
| 正常结束并保存 | 未执行；最终状态 unknown | 真实 Session stop/flush、进程退出、结果回读 |

云端 Android/Huuuge/Frida 的实际版本、资源现状、受控结果位置均待技术现场提供。代码中的版本/ABI gate 和模板不是现场检测结果。没有借用本机蓝叠、历史数据或合成回放填充此表。

## 准备检查

- Python 语法检查通过。使用现有 Windows Python 3.12.9 和已安装依赖进行合成测试，没有安装采集组件或启动 ADB/Frida/游戏。
- 本机最终检查：14 项，11 通过、3 项 Linux 专属检查跳过。
- Linux CI 已通过全部 14 项（Python 3.12.14 / protobuf 7.36.1），包括真实子进程锁、SIGTERM 和 supervisor 的 probe → run → 人工窗口 → stop → 退出后文件回读。最终代码证据：[run 34957001266](https://github.com/840832144/huuuge-android-research/actions/runs/34957001266)，代码 commit `9bb241b`；还覆盖最终文件被移除后 finalize 必须返回 incomplete/非零，不能依赖缓存。
- 测试通过伪造的 Frida 接口传送**测试生成的 protobuf 字节**，执行真实 `live_decode.py` 子进程、解码、文件保存和结束路径。合成 3 条、成功 2 条、失败 1 条仅用于证明程序行为，**不是真实 Huuuge 新增数据**。
- 覆盖旧 Session 不覆盖、路径穿越阻断、wrapper 失败 Raw 保留、断连失败、hook 失败、启动异常、缺失文件、未知退出码、人工窗口与脱敏摘要。
- Windows 未配置可用 WSL，本轮不安装 Linux 或云端模拟环境。Linux 锁、SIGTERM、完整 supervisor 路径使用 GitHub CI 合成检查；仍不替代云手机验收。

## Review 与下一步

[准备 Review PR #2](https://github.com/840832144/huuuge-android-research/pull/2) 已建立。ChatGPT 审查云端适配、异常状态和短部署说明；不得标记云端已验证或全项目上线。User/技术提供一台实例、云端执行端和受控权限后，按 [部署步骤](README.md) 在真实环境执行上表三项并更新计数、版本、证据与资源收尾状态。
