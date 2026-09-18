# tools/capture — 采集与模块筛选（游戏无关）

两条分离的关注点：

1. **采集是模块无关的**：`mitm_addon.py` 把解密后的**所有**请求/响应记到一个 JSONL
   （host / path / method + base64 原始体）。它不预设任何游戏或模块。
2. **模块由使用者选择**：先看有哪些端点（`endpoints.py`），再自己写一份映射
   （`modules.json`），然后用 `select_module.py` 只挑出该模块的记录；也可以直接在
   采集时用环境变量过滤。

这样"采集哪个模块"是**操作者的决定**，不是工具写死的。

## 文件

| 文件 | 用途 |
|---|---|
| `mitm_addon.py` | mitmproxy addon：记录所有解密流量到 JSONL（可选按 host/正则过滤）|
| `endpoints.py` | 列出采集里出现的端点 + 次数 + 方法 + **体形状**（json / protobuf? / gzip / binary），供你判断有哪些模块 |
| `select_module.py` | 按映射挑出某个模块的记录，另存为单独 JSONL |
| `modules.example.json` | 映射模板（`模块名 -> [匹配 host/path 的正则]`），可复制成 `modules.json` 后自行填写 |

## 环境变量（都不写死路径）

| 变量 | 作用 | 默认 |
|---|---|---|
| `MITM_OUT` | 采集输出路径 | `mitm_b64.jsonl`（当前目录）|
| `MITM_FILTER` | 采集时正则过滤 `"host path"`（例如 `/slots/`）| 不过滤（全采）|
| `MITM_HOSTS` | 逗号分隔的 host 子串白名单 | 不限 |
| `MITM_IN` | 各脚本读哪个采集文件 | `mitm_b64.jsonl` |
| `MODULE_MAP` | 模块映射文件 | `modules.json` |

## 流程

```bash
# 1) 采集（模块无关，先全收）
mitmdump --listen-port 8080 -s tools/capture/mitm_addon.py
#    只要某个模块时也可以直接过滤：
MITM_FILTER='/slots/' mitmdump --listen-port 8080 -s tools/capture/mitm_addon.py

# 2) 看有哪些端点、响应体是什么形状
python tools/capture/endpoints.py mitm_b64.jsonl --show-body 3
python tools/capture/endpoints.py mitm_b64.jsonl --grep slots

# 3) 自己写映射（把上一步看到的模式填进去）
cp tools/capture/modules.example.json modules.json
#    编辑 modules.json：{"slots": ["/slots/", "spin"], ...}

# 4) 挑出你要的模块
python tools/capture/select_module.py mitm_b64.jsonl --module slots --out slots.jsonl
python tools/capture/select_module.py --list           # 看已定义哪些模块
```

## 解码

记录体是**原始字节的 base64**，怎么解码取决于上一步看到的形状：

- `json` → 直接 `json.loads(base64.b64decode(...))`
- `protobuf?` → 用通用 wire 解码器：
  `python tools/analysis/toytycoon/full_decode.py`（读 `$MITM_IN`）或
  `python tools/analysis/toytycoon/proto_dump.py`
- `gzip` → 先 `gzip.decompress`，常见是 base64 包着 gzip 的 JSON（参考
  `tools/analysis/toytycoon/extract_save.py` 的写法）
- `binary` → 需要在具体游戏上进一步判定（可能是自研加密或自定义帧）

## 说明

- 采集内容含账号/会话/数值，**只留本地，不入 Git**（`.gitignore` 已排除 `*.jsonl`）。
- 各脚本都接受路径参数或 `MITM_IN` 等环境变量，**没有任何本机绝对路径**。
