# Huuuge 数据采集器部署手册

_适用版本：1.0.1_

Huuuge 数据采集器可以在你正常玩游戏时，自动记录游戏客户端已经收到的活动和数值数据。停止采集后，它会把数据整理成 JSON、CSV 和模块清单，方便策划或 AI 查看老虎机 Spin、活动、任务、奖励、礼包、价格、进度和门槛。

它只负责记录和整理，不会修改游戏数据、奖励、筹码或服务器状态。日常使用不需要理解底层技术，也不需要复制 PowerShell 或 ADB 命令。

## 1. 你会拿到什么

正式发布包：

[点击下载 HuuugeCollector_Installer.zip（公司 SVN）](http://140.143.33.242/svn/cr/x_proj_design/trunk/HuuugeCollector/release/HuuugeCollector_Installer.zip)

文件名：`HuuugeCollector_Installer.zip`

解压后包含：

```text
HUUUGE_BOOTSTRAP.cmd                  安装或更新入口
HUUUGE_COLLECTOR_DEPLOYMENT_MANUAL.md 本手册
README.txt                            最短安装提示
package_manifest.json                 版本、来源和文件哈希
```

安装完成后，默认目录是：

```text
C:\HuuugeCollector
```

日常只需要双击：

```text
C:\HuuugeCollector\HUUUGE_COLLECTOR.cmd
```

## 2. 首次安装前准备

首次安装需要以下条件：

1. Windows 10/11 64 位电脑；
2. 能访问公司 SVN；
3. 已安装 TortoiseSVN，并勾选 command line client tools；
4. 已安装 Python 3；
5. 已安装 BlueStacks 5；
6. 在蓝叠多开管理器中新开一个专门用于采集的模拟器，名称为 `HuuugeResearch`，并在这个模拟器里安装、登录 Huuuge Casino。

公司 SVN 首次认证、蓝叠/Google Play/游戏账号登录必须由本人完成。新电脑第一次准备这个专用模拟器时，工具会先检查现状；涉及修改蓝叠环境时，必须先展示备份与恢复方法，再由使用者确认。

平时正常玩游戏的原蓝叠模拟器不要用于采集。采集只在新开的 `HuuugeResearch` 模拟器中进行。

## 3. 首次安装

1. 把 `HuuugeCollector_Installer.zip` 解压到任意临时目录；
2. 双击 `HUUUGE_BOOTSTRAP.cmd`；
3. 首次运行会从公司 SVN 安装到 `C:\HuuugeCollector`；
4. 等待安装和环境检查完成；
5. 安装完成后会自动打开“ Huuuge 数据采集器”窗口；
6. 点击“环境检查 / 修复”，按窗口中的中文提示处理尚未完成的一次性步骤。

如果公司要求先登录 SVN，请先使用 TortoiseSVN 完成一次认证，再重新运行安装入口。采集器不会保存 SVN 密码。

## 4. 更新采集器

更新时双击：

```text
C:\HuuugeCollector\HUUUGE_BOOTSTRAP.cmd
```

工具会先执行 SVN 更新，再检查本机环境并打开 GUI。不要通过复制旧文件覆盖安装目录。

如果安装目录中存在本人尚未提交的版本化修改，更新会停止覆盖并保留这些修改。让维护人员检查后再继续。

## 5. 开始采集

1. 打开 `HUUUGE_COLLECTOR.cmd`；
2. 点击“1. 开始采集”；
3. 等待工具自动启动并检查专用的 `HuuugeResearch` 模拟器，确认数据已经开始保存；
4. 只有窗口出现以下文字后再开始玩：

```text
READY，可以开始玩了
```

5. 正常操作 Huuuge。可以自由进入任何系统，不需要预先选择模块，也不需要手工打标记。

如果没有出现 READY，本次采集不算开始。点击“环境检查 / 修复”或“AI 接管”，不要自己修改平时使用的原蓝叠模拟器。

## 6. 停止采集并整理

玩完以后：

1. 回到采集器窗口；
2. 点击“2. 结束采集并整理”；
3. 等待窗口提示 clean stop、数据条数和结果目录；
4. 在完成提示出现前，不要强制关闭采集器或 BlueStacks。

停止后工具会自动完成：

- 刷新并关闭当前 Session；
- 生成 RPC 清单；
- 生成字段清单；
- 更新模块结构目录；
- 保留原始本地证据。

## 7. 数据放在哪里

默认原始数据目录：

```text
C:\huuuge_research\captures\<Session时间>\
```

每个 Session 主要包含：

```text
manifest.json    本次版本、环境、起止时间和计数
index.csv        每条消息的时间、方向和类型索引
messages.jsonl   适合 Agent 批量读取的数据
raw\             原始证据
json\            已解码结构化数据
markers.jsonl    自动生成的采集生命周期记录
```

整理后的最近结果位于：

```text
C:\HuuugeCollector\artifacts\analysis\<Session时间>\
```

可以在 GUI 点击“3. 查看最近结果”直接打开。

环境检查报告位于：

```text
C:\HuuugeCollector\.local\bootstrap\
C:\HuuugeCollector\.local\controller\
```

原始数据可能含账号或 Session 信息，只保留在采集电脑本地，不上传 Git、SVN 或飞书。

## 8. 如何让 AI 分析

采集和整理本身不依赖 AI。需要解释数据时：

1. 在 GUI 的“AI”下拉框选择 `Codex`、`Trae + DeepSeek` 或“不使用 AI”；
2. 点击“5. AI 接管”；
3. 工具会生成并复制安全交接提示；
4. 告诉 Agent 要分析哪个 Session、关注什么问题。

推荐直接这样提问：

```text
读取最近一次 Huuuge Session，先按 AGENT_DATA_USAGE_GUIDE.md 检查 manifest、inventory 和 decoded JSON。
告诉我本次实际出现了哪些系统、哪些字段有新覆盖，只输出脱敏统计，不上传账号或 Session 值。
```

专项分析示例：

```text
分析最近一次 Session 的 Slots Spin：整理请求数、成功解码数、bet/win 字段覆盖和游戏 ID 分布，输出脱敏 CSV，并把 observed-live、schema-only、inferred 分开。
```

Agent 的完整数据使用规范位于：

```text
C:\HuuugeCollector\AGENT_DATA_USAGE_GUIDE.md
```

## 9. GUI 六个按钮

| 按钮 | 用途 |
|---|---|
| 1. 开始采集 | 完整检查并启动；出现 READY 后才能开始玩 |
| 2. 结束采集并整理 | 安全停止、刷新数据、生成清单和模块目录 |
| 3. 查看最近结果 | 打开最近一次整理结果 |
| 4. 环境检查 / 修复 | 更新依赖并生成本机环境报告 |
| 5. AI 接管 | 打开 Codex 或 Trae，并复制安全交接提示 |
| 6. 打开说明 | 打开本部署手册 |

## 10. 常见问题

### 双击安装入口后提示找不到 SVN

重新安装 TortoiseSVN，并勾选 command line client tools。安装后关闭旧窗口，再重新运行。

### 提示找不到 Python

安装 Python 3，并在安装界面勾选“Add Python to PATH”，然后重新运行 Bootstrap。

### SVN 认证失败

先用 TortoiseSVN 对公司 SVN 完成一次登录。不要把密码发给 Agent，也不要写入项目文件。

### GUI 能打开，但不能 READY

点击“环境检查 / 修复”。如果仍失败，点击“AI 接管”，让 Agent 读取 `.local` 下的最新报告。不要自己反复修改蓝叠设置，也不要改动平时使用的原蓝叠模拟器。

### 提示专用模拟器尚未准备好或缺少采集组件

这是新电脑第一次部署时可能出现的正常提示。让本机 Agent 按 `AI_DEPLOYMENT_PLAYBOOK.md` 检查；任何蓝叠环境修改前必须说明备份、修改范围和恢复方法，并由使用者确认。

### 点击结束后提示没有活动采集

说明本轮没有通过 GUI 成功开始，或采集进程已经异常退出。先查看最近结果和环境报告，不要把旧目录当成本轮数据。

### 可以用我平时玩的蓝叠模拟器采集吗

不可以。请在蓝叠多开管理器中新开一个名为 `HuuugeResearch` 的专用模拟器。平时使用的原蓝叠模拟器不要接入采集器。

### 数据可以直接发到群里或上传云盘吗

原始 `raw/json/messages.jsonl` 默认不可以。需要分享时只导出脱敏统计、结构、字段关系和不含账号/Session 值的表格。

## 11. 最短日常流程

```text
双击 HUUUGE_COLLECTOR.cmd
  → 点“开始采集”
  → 看到 READY
  → 正常玩
  → 点“结束采集并整理”
  → 点“查看最近结果”或“AI 接管”
```

日常采集共需要点击 2 次：开始一次、结束一次。查看结果或 AI 分析按需再点。
