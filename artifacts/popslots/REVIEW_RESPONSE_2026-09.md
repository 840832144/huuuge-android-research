# 对 TASK-0030 评审意见的回应（脚本修订）

评审的三条脚本缺陷里，**2 条成立、1 条不成立**。已按下述结果修订并入库。

## 一、缺陷 #1 不成立（误报，附实证）

评审认为：

> PID 探测写成 `subprocess.run([..., "ps", "-A", "|", "grep", "popslots"])`，
> 管道作为单个 argv 传入且未开 shell → 探测必然失败。

**实测结论：该写法可用。** `adb shell <cmd> <args...>` 会把参数**拼成一个字符串交给设备端 shell**，
因此管道是在**设备侧**解析的，不依赖本地 shell。对照实验（同一台实例、同一调用方式）：

| 命令 | 返回码 | 输出 |
|---|---|---|
| `ps -A \| grep init` | **0** | 命中 `init` 进程（证明管道生效）|
| `ps -A \| grep popslots` | 1 | 空（因为当时游戏**未运行**，grep 没匹配）|
| `ps -A \| grep wonder` | 1 | 空（同理）|

即：返回码 1 + 空 stdout + **空 stderr** 是「grep 没匹配到」的特征；
若管道真的没生效，`ps` 会把 `|` 当参数并输出用法错误到 stderr（实测 stderr 为空）。

**不过**：该写法确实脆弱（依赖 adb 的参数拼接行为，且不能跨平台）。修订后已改为
**跨平台稳健方案**，与是否是 shell 无关：

```
resolve_pid():  --pid 显式指定  →  pidof <package>  →  Python 侧解析 `ps -A`
```

（在 Python 里过滤行，不再把过滤交给设备端管道。）

## 二、缺陷 #2、#3 成立，且范围比评审指出的更大

实际扫出的硬编码如下（评审只举了 2 个脚本，实际涉及 9 个）：

| 硬编码内容 | 涉及脚本 |
|---|---|
| 输出目录 `C:\bigfish_research\toptycoon\` | `pop_parse`、`pop_users_sampler`、`pop_behaviour`、`pop_shot`、`pull_bigcasino` |
| 游戏 PID `15177` | `pop_parse`、`pop_users_sampler`、`pop_syms`、`pop_net_syms` |
| 符号地址 `0x7a1c8aa92e90` | `pop_parse`、`pop_users_sample` |
| adb 路径 `C:/platform-tools/adb.exe` | 全部 adb 脚本 |
| **APK 安装哈希路径**（评审未发现） | `pop_webview`、`pull_bigcasino` |

最后一条是隐藏更深的问题：`/data/app/com.playstudios.popslots-<HASH>==/base.apk` 里的
`<HASH>` **每次安装都会变**，所以那两个脚本在任何一台新装的机器上都必错。
已改为 `pm path <package>` 动态解析。

### 修订方式

新增 `tools/analysis/popslots/pop_common.py` 作为公共层，全部脚本改为基于它：

- **符号**：`POP_SYMBOLS` 维护 mangled 名，attach 时用 `findSym()` 按名字解析
  （`getExportByName` → 失败则遍历 `enumerateExports` 子串匹配）。**脚本内不再有任何地址**；
  若游戏更新改了名字，脚本会打印 `symbols missing=[...]`。
- **PID**：`--pid` → `pidof` → Python 侧 `ps -A` 解析。
- **adb / 串号 / 包名 / frida 端口 / 输出目录**：全部可 CLI 或环境变量覆盖，
  输出默认落在当前目录。adbd 多版本冲突时可用 `ANDROID_ADB_SERVER_PORT` 隔离。
- **ABI 目录**：`pull_bigcasino` 从 APK 清单里自动发现，不再假定 x86_64。

## 三、评审提出的方法学限制：成立，已写入文档

> 脚本对 `CRoomUserModel` 只读 180–220 字节再抽 ASCII；这是模糊转储，不是字段映射。

完全成立。已在两处写明：

- `tools/analysis/popslots/README.md` →「⚠️ 方法学边界（引用结论前必读）」
- `artifacts/popslots/POP_SLOTS_LOBBY_FORENSICS.md` →「方法学限制」章节，
  含：①模糊转储≠字段映射 ②样本量/窗口有限、比例未量化 ③未覆盖三项 ④脚本入库时间差

## 四、评审未指出但一并处理的重复

`pop_users_sample.py` 与 `pop_parse.py` 功能重复 → **删除**，保留后者
（`--seconds N` 定时、`--seconds 0` 持续）。`pop_users_sampler.py` 改为薄封装（常驻版）。

## 五、对评审其余结论的态度

- 「附录 B 缺口已过期」—— **同意**，这是评审最有价值的产出；已在 forensics 文档
  方法学限制第 4 条记录该时间差与现状。
- 「E17 引用遗漏」—— 属**那份报告的文本问题**，不在本仓库，需报告作者自行补标注。
- 「视频事实无法核验」—— 同意，需在有材料的机器上做。
- 「不在日常实例上做研究」—— 同意并保留；但「Pop! Slots 只装在日常实例」这一判断
  需在目标机器上用 `pm list packages` 实测（在做过本项研究的机器上，研究实例是
  装有 Pop! Slots 的）。

## 六、修订验证

- `python -m py_compile` 全部 12 个脚本通过
- 公共参数在 `--help` 中可见（`--serial/--frida/--package/--pid/--outdir/--adb`）
- 真实实例冒烟：`pop_state.py` 在游戏未运行时优雅降级（`pid: None` 并继续）；
  `pop_webview.py` 的 `pm path` 动态解析成功
