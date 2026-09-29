# TASK-0031 验收记录

- 日期：2026-09-29（保留 2026-09-15 准备检查）
- 执行：Codex；Subagents: none
- 范围：[Issue #1 v3](https://github.com/840832144/huuuge-android-research/issues/1)
- 当前状态：In Progress；按 PR #11 `5ff7190` 的 v2-GooglePlay 续接，真实云端验证未执行。
- User 本人负责权限、登录和手动游戏；Workbench 与 Google 环境准备由 Codex 完成，不等待其他技术对接人。

## 2026-09-29 按步骤记录

| 步骤 | 实际方法及结果 | 未验证内容 |
| --- | --- | --- |
| 原任务同步与登记 | 治理 main `b0a36c8`、业务 main `6cdb1d6` 合入原分支；Registry 19 canonical / 0 collision / valid；未新建 Task/PR | 准备 Review 不等于云端通过 |
| Workbench 安装 | 官方 Windows amd64 ZIP + 同源 SHA-256 校验；安装用户 Programs/workbench，加入用户 PATH；version=v1.0.1 / 86c0aff，帮助已核验 | 默认配置不存在，认证/连接未执行；未改安全组 |
| 真实目标核验 | 后续经普通入口到官方阿里云登录，User 本人登录后 URL 回到无影 instanceLayouts；唯一已购实例可用，香港/4c8g32G/Android 12/镜像 26.09.1。点击连接超时，后续浏览器枚举 fetch 失败，无法核验当前 URL，已停止 | 连接结果 unknown；ABI、设备 Google 组件与网络、Linux 目标均未核验；控制台安装列表不能代替设备组件检查 |
| Google Play/GMS | 未检测、未安装、未启用；已查官方 FAQ/镜像说明，但未取得本实例适用入口 | 组件前后状态、手机网络、具体安装方法与结果均 unknown |
| Google 登录/商店 | 未到登录页，无账号读取或输入 | User 登录、首页/搜索/详情、Play Protect 认证均未验证 |
| Play 获取 Huuuge | 未执行；未侧载第三方 APK | 商店来源、下载或复用、实际版本/ABI未验证 |
| 无探针游戏基线 | 未执行，未接入 Frida | User 登录与普通大厅/机台操作未验证 |
| 真实采集与停止 | 未启动，无云端 Session | 新增解码、退出/flush、保存文件及计数均 unknown |

安装失败尝试：checksum HTTP 返回字节数组，首次文本匹配失败即停止；按 UTF-8 解码后匹配官方条目并校验成功，没有跳过校验。没有更换第三方下载源。浏览器安全检查阻断后未继续界面操作；这不是手机缺少 GMS 或网络不可达的证据。

定向代码审阅覆盖 `cloud_capture.py` 的私网/ABI/版本/转发归属、单运行锁、人工窗口和最终文件回读，以及 `live_decode.py` 的新 Session、异常保留、stop 文件、卸载/detach、flush/fsync、生命周期计数。同步 main 在这条调用链只改变一处 CLI 帮助文本，原云端逻辑和测试不变；没有重写采集器，没有借用历史本机结果。

## 普通入口重试的工具结果

- 已读取的官方路径为 `wya.wuying.aliyun.com/instanceLayouts`；登录页为 `account.aliyun.com/login/login.htm`，只记录域名/路径和标题，不保存认证参数、账号、实例标识或真实 IP。User 本人确认登录后才继续读取。
- 连接动作错误：`js execution timed out; kernel reset, rerun your request`。状态恢复枚举错误：`Browsers: Error: nodeRepl.fetch request failed`。未确认连接成功或失败，不盲点重试、不绕过 URL 检查；Workbench/Linux 不作为手机准备前置阻塞。
- 既有业务 `2ddaeb8` 的 [Linux CI 36518139017](https://github.com/840832144/huuuge-android-research/actions/runs/36518139017) 已回读 14/14 合成检查通过，仍不代表设备或 Google 验收。

## 真实三项验收

| 验收项 | 本轮实际结果 | 缺少的证据 |
| --- | --- | --- |
| 网页登录并正常玩 | 未执行 | 实例与网页授权入口、User 亲自登录并操作 |
| 本轮新增采集且成功解码 | 未执行；捕获/成功/失败计数均 unknown | 云端连接、实际 build/ABI/descriptor、真实普通操作及对应业务响应 |
| 正常结束并保存 | 未执行；最终状态 unknown | 真实 Session stop/flush、进程退出、结果回读 |

云端 Android/Huuuge/Frida 的实际版本、资源归属和受控结果位置仍待 Codex 与 User 现场核验。代码中的版本/ABI gate 和模板不是现场检测结果。没有借用本机蓝叠、历史数据或合成回放填充此表。

## 历史准备检查（2026-09-15）

- Python 语法检查通过。使用现有 Windows Python 3.12.9 和已安装依赖进行合成测试，没有安装采集组件或启动 ADB/Frida/游戏。
- 本机最终检查：14 项，11 通过、3 项 Linux 专属检查跳过。
- Linux CI 已通过全部 14 项（Python 3.12.14 / protobuf 7.36.1），包括真实子进程锁、SIGTERM 和 supervisor 的 probe → run → 人工窗口 → stop → 退出后文件回读。最终代码证据：[run 34957001266](https://github.com/840832144/huuuge-android-research/actions/runs/34957001266)，代码 commit `9bb241b`；还覆盖最终文件被移除后 finalize 必须返回 incomplete/非零，不能依赖缓存。
- 测试通过伪造的 Frida 接口传送**测试生成的 protobuf 字节**，执行真实 `live_decode.py` 子进程、解码、文件保存和结束路径。合成 3 条、成功 2 条、失败 1 条仅用于证明程序行为，**不是真实 Huuuge 新增数据**。
- 覆盖旧 Session 不覆盖、路径穿越阻断、wrapper 失败 Raw 保留、断连失败、hook 失败、启动异常、缺失文件、未知退出码、人工窗口与脱敏摘要。
- Windows 未配置可用 WSL，本轮不安装 Linux 或云端模拟环境。Linux 锁、SIGTERM、完整 supervisor 路径使用 GitHub CI 合成检查；仍不替代云手机验收。

## Review 与下一步

[原 PR #2](https://github.com/840832144/huuuge-android-research/pull/2) 继续使用，当前不能提交完整云端验收成功。受支持浏览器恢复后先读取现有标签 URL 和连接结果；可靠核验后由 Codex 按 [部署步骤](README.md) 检查并准备 Google Play/GMS，到原生登录页才通知 User 本人登录；随后按 v2 顺序逐项记录真实结果。云端 Session 尚不存在，本轮没有停止/保存结果可回读；未新增资源或端口、未部署本机采集、未修改晨会。
