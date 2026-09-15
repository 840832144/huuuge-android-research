# Toy Tycoon 采集工具（tools/analysis/toytycoon）

Top Tycoon（`com.monopoly.dream.idle.king`）采集脚本。**主路线是网络层
mitmproxy 抓 HTTPS**（不要用 Frida 进程内 hook，见下）。

完整文档在 `artifacts/toptycoon/`：
- `TT_CAPTURE_RUNBOOK.md` —— **正确部署 runbook（先读这个）**
- `MITM_CAPTURE.md` —— 跑通实证（业务 host、字段示例）
- `DEPLOY_AND_ONBOARD.md` —— AI 引导式接入
- `PLANNER_AI_REPLY.md` —— 如何记录"每次操作 + 数据变化"
- `TT_IOS_CAPTURE.md` —— iOS（不越狱）采集方案
- `GENERIC_CAPTURE.md` / `RUNTIME_CAPTURE_MINIMAL.md` —— Frida 路线的探索结论（为什么不通）

## 主路线：mitmproxy 网络层

| 文件 | 用途 |
|---|---|
| `mitm_addon.py` | mitmproxy addon：把 host/path/method + base64 请求/响应 写到 `mitm_b64.jsonl` |
| `toytycoon_protocol_dict.json` | 协议字典（422 消息 / 48 服务 / 1264 字段槽），字段名对照用 |
| `export_toytycoon_protocol.py` | 从 `Game.Hotfix.dll` 静态导出上面的协议字典 |
| `full_decode.py` | protobuf wire 解码 → `字段#=值` |
| `proto_dump.py` | protobuf dump（同类，简版） |
| `extract_save.py` | 解 `saveuserdata` 的 gzip 玩家存档 → `save_blocks/*.json` |
| `try_bind_cacert.py` | 把 CA bind-mount 进系统证书区（`/system` 只读时的做法）|
| `analyze_play.py` | 按时间线统计金币/能量变化（操作 → 数据变化）|
| `find_spin.py` | 列出被调用的 API，定位 spin 相关端点 |
| `decode_steal_amount.py` | 解 `steal/targethouse` 响应嵌套，取偷取数值 |
| `TT_CAPTURE_PROMPT.txt` | 一键发给 AI 的接入话术 |

## 备用：Frida 注入（Houdini，仅供了解，**业务抓取不走这条**）

| 文件 | 用途 |
|---|---|
| `bootstrap_gadget_tt.py` | 通过 `NativeBridgeLoadLibraryExt` 把 ARM64 Gadget 注入 Houdini 命名空间 |
| `gadget-listen.config.template.json` | Gadget 配置模板（拷到游戏 native 库目录，**命名为 `libfrida-gadget.config.so`**；改端口即可复用）|

## 重要：为什么主路线是网络层

Top Tycoon 是 **ARM64 Houdini 翻译 + il2cpp 符号剥离 + xLua 静态链接**，Frida
Gadget 钩业务函数基本走不通（Gadget 看不到 x86-64 侧 `libil2cpp.so`、libil2cpp
无标准导出、libxlua 的 Lua API 不导出、`UnitySendMessage` 不走业务逻辑）。
业务流量是 HTTPS（`api-tycoon-101.behefun.com`），网络层抓包已实测拿到
金币/能量/完整存档。

## 认证/端口注意

- 代理开关：采集时开 `settings put global http_proxy 10.0.2.2:<端口>`，
  **不采集时必须清 `:0`**，否则游戏报"链接中断"登不进。
- mitmproxy 端口按需选（示例 8080；被占用时可换 8899 等，并同步改代理）。
