# Huuuge 采集数据的 Agent 使用说明

> 面向 Codex、Trae + DeepSeek 以及其他本机 Agent。采集器本身不依赖 AI；Agent 的主要职责是安全地读取已生成的数据、回答策划问题、产出可复核的表格与结论。

## 1. 先判断要读哪一层

数据分为三层，不要一上来扫描全部 Raw：

1. **结构目录（可提交 Git/SVN）**：`artifacts/module_catalog/`
   - `MODULE_INDEX.md`：有哪些模块、live/schema-only 状态、缺什么玩法；
   - `modules.csv`：模块级覆盖概览；
   - `endpoints.csv`：service/method 与模块归属；
   - `fields.csv`：schema 字段角色与 live 覆盖；
   - 各模块 `.md`：流程、ID、状态、成本、奖励、时间、资格与待采集项。
2. **Session 整理结果（默认仅本机）**：最近一次结束采集后，GUI“查看最近结果”打开的目录。
   - `rpc_inventory.csv`：本次实际出现的 endpoint、方向和样本数；
   - `field_paths.csv`：本次 JSON 中实际出现的字段路径、类型和频次；
   - 该 Session 刷新的 module catalog。
3. **原始/含值证据（只留本机）**：`<capture-root>\<session-id>\`
   - `manifest.json`：版本、哈希、环境、采集起止、计数、hook 状态；
   - `index.csv`：每条 RPC 的时间、方向、service/method、解码状态及文件路径；
   - `messages.jsonl`：所有消息的批量 JSON；
   - `json\*.json`：逐条解码结果；
   - `raw\*.rpc.bin`：可重解码的底层证据；
   - `markers.jsonl`：采集器自动写入的 start/hooks-ready/ready/stop 生命周期事件。策划无需手工选择模块或打 marker。

推荐顺序是：**模块目录 → inventory/field paths → 与问题相关的 decoded JSON → 必要时才回到 Raw**。

## 2. Agent 必读与边界

开始分析前读取：

1. `AGENTS.md`
2. `CONTRIBUTING.md`
3. `CURRENT_STATUS.md`
4. `HUUUGE_DATA_COLLECTION_GUIDE.md`
5. 本文件
6. 目标模块 dossier
7. Session 的 `manifest.json`、`rpc_inventory.csv` 和 `field_paths.csv`

必须遵守：

- 只做被动分析，不修改游戏、余额、奖励、请求或服务器状态；
- 不伪造或重放 RPC；
- 不把账号 ID、token、完整余额轨迹、原始 JSON/Raw 提交 Git/SVN或粘贴到公共服务；
- 对外输出优先使用聚合、去标识化示例和字段关系；
- `observed-live`、`schema-only`、`inferred` 必须分开写；
- 没有足够样本时不要输出 RTP、EV、概率或付费价值的确定性结论。

## 3. 接到策划问题后的标准流程

例如策划问：“刚才玩的老虎机发生了什么？”

1. 从 `.local/controller/last_session.json` 取得最近 Session 与整理结果路径；
2. 检查 `manifest.json`：状态必须为 `stopped`，并记录游戏版本、descriptor/agent 哈希、RPC/decoded 计数；
3. 在 `rpc_inventory.csv` 中筛选 Slots/Spin 相关 endpoint；
4. 用 `index.csv` 按时间和 request/response 配对；
5. 只读取对应 `json\*.json`，提取 game ID、bet、win、feature/free-spin/jackpot 等已实际存在字段；
6. 输出样本数、覆盖时段、缺失字段和异常解码数；
7. 如需分享或提交，只生成去账号化的汇总 CSV/Markdown，不复制原始 Session。

模块问题使用同样流程：先由 `endpoints.csv` 找入口，再从本次 inventory 判断是否真的出现，最后追 decoded values。

## 4. 证据标签

每条重要结论至少标一个证据层级：

- **Observed-live**：当前/历史 Session 的 decoded RPC 中直接出现；写明 Session ID、endpoint、样本数和字段路径。
- **Schema-only**：descriptor 中存在，但当前 Session 没有对应 live sample。
- **Inferred**：根据命名、请求/响应时序或跨消息关系推断；写明推断理由和验证所需操作。

不要把“字段存在”写成“字段当前有值”，也不要把一次样本写成稳定规则。

## 5. 推荐输出模板

```text
问题：<策划问题>
数据范围：Session <id>，<开始>-<结束>，游戏版本 <version>
完整性：RPC <n>，decoded <n>，目标 endpoint <n>

Observed-live
- <结论>（endpoint / field path / sample count）

Schema-only
- <已知结构但本轮未触发的内容>

Inferred
- <推断及理由>

缺口
- <需要继续玩的动作或需要更多样本的原因>

输出文件
- <sanitized CSV/Markdown/Excel 的本地路径>
```

## 6. 可直接交给 Agent 的提示词

### 最近一轮概览

```text
请按 AGENT_DATA_USAGE_GUIDE.md 分析最近一次已 finalized 的 Session。先读 manifest、rpc_inventory 和 field_paths，不要全量展开 Raw。输出本轮出现的模块、endpoint/sample count、字段覆盖、解码完整性；区分 observed-live/schema-only/inferred。不要输出账号 ID 或完整余额轨迹。
```

### 指定模块

```text
请分析最近 Session 的 <模块名>。先读 artifacts/module_catalog 中该模块档案和 endpoints.csv，再用 rpc_inventory 定位本轮 live endpoint，只打开相关 decoded JSON。整理实体 ID、状态/进度、成本、奖励、时间、资格/限制和样本数。证据不足的结论明确标 inferred。
```

### 生成策划表

```text
请从最近 Session 为 <模块名> 生成去标识化 CSV/Excel。保留用于数值分析的字段与 endpoint/时间证据，删除账号 ID、token、绝对本地路径和无关完整余额。附一页字段说明与数据缺口，不要估算未观察到的概率或价值。
```

## 7. Codex 与 Trae + DeepSeek

- **Codex**：可直接在本机仓库和 capture 目录执行脚本、读取文件并生成本地输出；仍需遵守 Git/SVN 与隐私边界。
- **Trae + DeepSeek**：打开 SVN 项目目录后，把上述提示词交给 Agent。允许它读取本机 Session 时，应把输出限定到本机，不上传原始 value-bearing 数据；是否会把内容发送到模型服务取决于团队部署方式，应按公司数据政策配置。
- **没有 AI 也能采集**：开始、READY 检查、停止、inventory 和 catalog 更新全部由确定性脚本完成。

## 8. 何时需要重新采集

以下情况才建议策划继续玩以补数据：

- 目标模块在 `modules.csv` 中仍是 schema-only/live pending；
- 目标 endpoint 本轮样本为 0；
- 只出现 update，没有触发 request/response 主流程；
- cost/reward/timing/eligibility 某类关键字段从未实际有值；
- 需要统计结论但当前样本不足或玩法条件过于单一。

策划无需提前选择模块或手工打 marker。让采集保持全量，结束后由 endpoint、时间戳和字段路径自动归类即可。
