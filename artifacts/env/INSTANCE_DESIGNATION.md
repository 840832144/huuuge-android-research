# 实例指定记录（Instance designation）

> **用途**：一次性写下"哪台机器上哪个实例是研究实例、哪个是日常实例"，让后续每个会话
> 都直接读到答案，**不再重新推导、也不再反复问所有者**。
>
> **纪律：本表每一行都必须来自 `tools/env/find_instance.py` 的实测输出。口头描述、
> 记忆、别的会话的结论都不算 —— 本文件已经因为"照描述写表"出过一次错（见下）。**

## 为什么需要这份记录

Pop! Slots 项目上真实发生过三次代价：① agent 按"名字"启动实例，拿到的是没有目标包、没有
root 的实例；② 启动了一个无法证明身份的同名实例，导致**正在运行的实例被抢盘关机**；
③ 本文件曾按"口头描述"写下一行 **Android 12 / 有包 / 有 root** 的实例，实测为
**Android 9 / 无包 / 无 root** —— 于是下一个 agent 按错表推进。

## 记录格式（每台机器一段）

| 机器 | 安装（注册表键 / 版本） | 实例 | 显示名 | adb | Android | 角色 | 实测证据 |
|---|---|---|---|---|---|---|---|
| 所有者研究机（`C:\Users\admin`） | `BlueStacks_nxt_cn` / 5.22.170.6509 | `Pie64` | BlueStacks | 5555 | 9 | **日常（禁止碰）** | root flag 0 |
| 同左 | 同上 | `Pie64_1` | AppResearch | 5565 | 9 | **研究** | root=1；`su -c id` → uid 0；`pm list packages` 含 `com.playstudios.popslots` |
| 同左 | 同上 | `Pie64_3` | AppResearch | 5585 | 9 | 备用研究 | — |
| 同左 | 同上 | `Pie64_5` | topTycoon | 5605 | 9 | 研究（Toy Tycoon） | — |

## 另一台部署机（实测：**没有可用环境**，待重建）

实测结论（2026-09-18，由该机 agent 逐项测量）：

| 安装 | 实例 | Android | `com.playstudios.popslots` | 可用 root |
|---|---|---|---|---|
| `BlueStacks_nxt_cn` 5.22.170.6509 | `Pie64` | 9 | ❌ | ❌ |
| `BlueStacks_nxt_cn` 5.22.170.6509 | `Pie64_1`（HuuugeResearch） | 9 | ❌ | ❌ |
| `BlueStacks_nxt`（D: 那套） | `Pie64` | 9 | ❌ | ❌ |

**该机没有任何实例同时具备「目标包 + 可用 root」，也没有任何实例装过该游戏。**

> ⚠️ **更正**：本文件早先在该表里写过 `BlueStacks_nxt` 的 `Pie64` = Android 12 / 有包 / 有 root。
> 那是照口头描述写的、**未经实测**，与实测不符，已作废。教训：本表只接受实测输出。

**未解决**：该机会话早期出现过 `emulator-5562`（Android 12 / SM-S9110 / 有包 / `adb root` → uid 0），
之后再也找不到。已排除一种可能：`find_instance.py` 原先只按 `*.display_name` 键枚举实例，
**缺该键的实例会被整条跳过**；该缺陷已修（改为匹配任意 `bst.instance.<name>.` 键，并额外扫描
注册表之外的常见配置位置，支持 `--conf` 指定）。**修好后需重扫一次**，再判断那个实例是否真的不存在。

### 为什么有的实例开不了 root（机制，来自该机实测）

`enable_root_access="1"` **是必要条件、不是充分条件**：

- `adb root` 在部分镜像上是 **no-op**：即使 `ro.secure=0`、`ro.debuggable=1`、
  `service.adb.root=1` 都就位，adbd 仍以 `uid=2000(shell)` 运行（命令行带
  `--root_seclabel=u:r:su:s0`）——蓝叠把 adbd 改成不真正提权。
- `/system/xbin/su` 存在且 setuid root，但由 **签名校验的 uid/包白名单**（`/system/etc/.swl.cfg` + `.sig`）
  控制：只允许 `uid:0` 与白名单包（`com.bluestacks.*` 等）。shell(2000) 调用一律 `exit 1`，
  且无 root 无法改该白名单 —— 死循环。**白名单里的命令是破坏性的**（`cmd:stop` 会停 guest
  framework），不要拿它们探测 `su`，见 `OPERATOR_GUIDE.md` B9。
- **`bst.feature.rooting` 不由配置文件控制**：实测手工改 `1` 并重启后被 BlueStacks **回写为 `0`**；
  只有 `bst.instance.<名>.enable_root_access` 会保留。改它只影响 BlueStacks 是否**注入 root 组件**
  （实测确实注入出了 `su`），**不改变白名单**，所以仍然不通。
- **结论**：root 能力是**镜像相关的**。符合 `find_instance` 结论 `★ 研究候选` 的镜像才可用；
  在开不了 root 的镜像上换 agent 也开不了，别反复试。
  可行方向：① 换/克隆一个 root 能力正常的镜像实例；② 无 root 路线（gadget 重打包，最侵入，
  需 Java/apktool）；③ **换一台已验证可用的机器采集（最省事）**。

### 另一台部署机的实测终局（2026-09-18）

两套安装的镜像 **`su` 白名单都不放行 shell**，且 `bst.feature.rooting` 手改无效：

| 安装 | 实例 | 游戏 | `enable_root_access` | `su` 放行 shell |
|---|---|---|---|---|
| `BlueStacks_nxt_cn` | `Pie64_1` | ❌ | 1（原有）| ❌ |
| `BlueStacks_nxt`（D:）| `Pie64_1` | ✅（本轮装上）| 1（本轮开启，配置有备份 + 前后哈希）| ❌ |
| 两套的 `Pie64` | — | ❌ | **未改动**（日常实例）| — |

**该机结论：root 打不通 → 无法 frida 注入 → 采集无法在本机完成。**
替代路径只有：换机器采集，或走无 root 的 gadget 重打包（需 Java/apktool）。

> 注：`find_instance.py` 修复后能列出该机 **4 个实例**（D: 的 `Pie64_1` 之前因只按
> `display_name` 枚举被整条跳过）。

### 曾经的错误数据（保留作教训）

本文件早先写过 `BlueStacks_nxt` 的 `Pie64` = Android 12 / 有包 / 有 root —— 那是**照口头描述写的、
未经实测**，与实测不符，已作废。纪律：**本表只接受实测输出**（`find_instance.py` 的结果）。

## 查询命令

```bash
python tools/env/find_instance.py --package com.playstudios.popslots
python tools/env/find_instance.py --package com.playstudios.popslots --conf <某个 bluestacks.conf>
```
输出为只读证据表（实例名/显示名/adb端口/Android/型号/root/是否装有目标包/结论）。
看到 `★ 研究候选（有包 + 有 root）` 即目标；显示 `未运行` 的行**不要贸然启动** ——
启动已在运行的实例会抢盘关机（见 `AGENTS.md`）。
