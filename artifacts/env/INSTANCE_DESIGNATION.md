# 实例指定记录（Instance designation）

> **用途**：一次性写下"哪台机器上哪个实例是研究实例、哪个是日常实例"，让后续每个会话
> 都直接读到答案，**不再重新推导、也不再反复问所有者**。
>
> **规则见 `AGENTS.md`**：「Which instance is 'the research instance'」。要点：实例名会跨安装
> 重复，`--instance <name>` 在**你所调用的那个 `HD-Player.exe` 所属安装内**解析；日常实例
> 永不做仪表化；**启动一个已经在运行的实例会把它抢盘关机**，所以启动前必须先确认身份。

## 为什么需要这份记录

Pop! Slots 项目上真实发生过两次代价：一次是 agent 按"名字"启动实例，拿到的是没有目标包、
没有 root 的实例；另一次是启动了一个无法证明身份的同名实例，导致**正在运行的实例被抢盘
关机**。两次都不是"不守流程"，而是**流程里缺了一份权威的实例指定**。

## 记录格式（每台机器一段）

| 机器 | 安装（注册表键 / 版本） | 实例 | 显示名 | adb | Android | 角色 | 备注 |
|---|---|---|---|---|---|---|---|
| 本机（所有者研究机） | `BlueStacks_nxt_cn` / 5.22.170.6509 | `Pie64` | BlueStacks | 5555 | 9 | **日常（禁止碰）** | root flag 0 |
| 本机（所有者研究机） | `BlueStacks_nxt_cn` / 5.22.170.6509 | `Pie64_1` | AppResearch | 5565 | 9 | **研究** | root=1；`su -c id` → uid 0；已装 `com.playstudios.popslots` |
| 本机（所有者研究机） | `BlueStacks_nxt_cn` / 5.22.170.6509 | `Pie64_3` | AppResearch | 5585 | 9 | 备用研究 | — |
| 本机（所有者研究机） | `BlueStacks_nxt_cn` / 5.22.170.6509 | `Pie64_5` | topTycoon | 5605 | 9 | 研究（Toy Tycoon） | — |
| 另一台部署机 | （待填：`BlueStacks_nxt` / 5.22.265.1012 或 `_cn`） | （待所有者指定） | — | — | — | 待指定 | 见下方决策 |

## 待指定机器的决策记录

**场景（已在另一台机器上实测）**：该机有两套安装，但**没有任何实例同时满足「有目标包 + 有 root」**：

| 安装 | 实例 | Android | popslots | root |
|---|---|---|---|---|
| `BlueStacks_nxt_cn`（5.22.170.6509） | `Pie64` | 9 | ❌ | ❌ |
| `BlueStacks_nxt_cn`（5.22.170.6509） | `Pie64_1`（HuuugeResearch） | 9 | ❌ | 配置可开 |
| `BlueStacks_nxt`（5.22.265.1012） | `Pie64` | 12 | ✅ | ✅ | 

而 `BlueStacks_nxt` 的 `Pie64` **同时是日常实例**（Pop! Slots 桌面快捷方式指向它）。
→ 因此**不能**把它当研究实例；应改为在隔离实例上复现环境。

**推荐处置（已获所有者授权）**：
1. 用 `tools/env/find_instance.py --package com.playstudios.popslots` 确认证据；
2. 选定 `BlueStacks_nxt_cn` 的 **`Pie64_1`（HuuugeResearch）** 作为研究实例；
3. 按 `AGENTS.md` 常设授权：先备份 `bluestacks.conf`，**字节级**打开该实例的 root（不得带 BOM），
   记录前后哈希；
4. 复现同一构建：从日常实例**只读**取 APK（`pm path` + `adb pull`），或在该实例的商店内安装；
5. 全部记入 `COLLAB_LOG.md`。

## 查询命令

```bash
python tools/env/find_instance.py --package com.playstudios.popslots
```
输出为只读证据表（实例名/显示名/adb端口/Android/型号/root/是否装有目标包/结论）。
看到 `★ 研究候选（有包 + 有 root）` 即目标；显示 `未运行` 的行**不要贸然启动** ——
先用证据确认它是哪一个（见上）。
