# BlueStacks root 标准化（多台机器环境一致）

> 目的：让任意一台机器复刻"研究实例可 root"的环境，且**流程尽可能短**。
> 所有者要求：**不做 manifest 哈希、不做多项测试门禁、不加额外检查清单**。
> 因此本流程只有三件事：**能打吗 / 打了没有 / 怎么退**。

## 为什么需要它（一句话）

root 不是配置差异，是**二进制差异**：原生镜像的 guest `su` 由签名白名单
（`/system/etc/.swl.cfg` + `.sig`）控制，只放行 `uid:0` 与 `com.bluestacks.*` 包，
因此 `uid=2000(shell)` 一律被拒；`adb root` 在蓝叠镜像上也是 no-op。
让 `su -c id` 返回 `uid=0` 的，是下面三处补丁 —— 配置里的 `enable_root_access` 只是开关。

## 补丁内容（三处主机 + 一处实例 + 可选镜像侧）

| # | 目标 | 补丁 | 作用 |
|---|---|---|---|
| 1 | `HD-Player.exe` | `_isDiskVerificationRequired()` 序言 → `31 C0 C3` | **唯一总开关**：完整性检查跳过 + developer mode 打开 → guest `su` 对所有应用放行 |
| 2 | `HD-Player.exe` | `plrCheckDiskIntegrity` 调用 → `B0 01 90 90 90` | 完整性检查恒为"已校验" |
| 3 | `HD-MultiInstanceManager.exe` | 重置 `enable_root_access` 的调用 → `90 90 90 90 90` | 蓝叠不再把 root 开关改回 `0` |
| 4 | `bluestacks.conf` | `bst.instance.<实例>.enable_root_access="1"` | 打开该实例的 root 交付 |
| 5 | `Data.vhdx`（可选）| gated `su` 序言 → `B0 01 C3`（`mov al,1; ret`）| 仅当第 1 项仍不足以放行 `su` 时才需要 |

补丁**按签名定位**（不是死偏移），所以小版本更新后仍能找到；找不到时报"版本不匹配"，
**不会乱写**。

## 标准流程（4 步）

```powershell
# 1) 上游工具（固定提交，已审计；见 artifacts/recovered/BlueStacks_Root_GUI_audit.md）
git clone https://github.com/RobThePCGuy/BlueStacks-Root-GUI
cd BlueStacks-Root-GUI && git checkout 7002d185522c41a15ea9b184eff24393c5a62a11

# 2) 看现状（只读，什么都不改）
python D:\DSH_work\tools\bluestacks_root_apply.py check <实例名>

# 3) 打补丁（必须管理员终端：要写 Program Files 并关闭蓝叠进程）
python D:\DSH_work\tools\bluestacks_root_apply.py apply <实例名>

# 4) 唯一验证：启动该实例，然后
adb -s 127.0.0.1:<端口> shell "su -c id"        # 期望 uid=0(root)
```

双击版：`D:\DSH_work\tools\bluestacks-root-apply.cmd`（无参数 = `check Pie64_1`；
`bluestacks-root-apply.cmd apply Pie64_1` / `... revert`）。

脚本在 `apply` 时**自己按顺序**做：停所有蓝叠进程 → 打 3 处主机补丁（上游自动留
`.prepatch.bak`）→ 打开该实例开关 → 可选镜像侧 `su`。

## 回滚

```powershell
python D:\DSH_work\tools\bluestacks_root_apply.py revert
```
用上游的 `.prepatch.bak` 还原主机二进制；镜像侧若做过，用 su 侧车
（`<vhd>.suroot.json`）还原。**日常实例的开关脚本不会动**（只改你指定的实例）。

## 本机基线（对照用）

```
主机侧补丁：
  HD-Player.exe  _isDiskVerificationRequired -> 0 (unlock: integrity  已补丁
  HD-Player.exe  plrCheckDiskIntegrity call (force 'verified')        已补丁
  HD-MultiInstanceManager.exe 停止重置 enable_root_access              已补丁
实例 root 开关：
  Pie64 = 0（日常，保持关闭）   Pie64_1 = 1（研究）   Pie64_5 = 1（Toy Tycoon 研究）
唯一验证：adb -s 127.0.0.1:5565 shell "su -c id" → uid=0(root)  ✅
```

任何机器跑完 `check` 得到同样三行「已补丁」+ 目标实例开关为 `1`，即与本机环境一致。

## 风险与限制（诚实列出，不回避）

1. **破坏 Authenticode 签名**：主机二进制被改 → 蓝叠进入 integrity-bypass 模式，这是**主机级**影响。
2. **与构建版本绑定**：上游兼容表列的是 CN `5.22.170.6509`。另一套安装
   （`nxt` `5.22.265.1012`）定位器可能对不上 —— 脚本会明确报"版本不匹配"。
3. **升级会被覆盖**：蓝叠更新会换回原版二进制 → 重新跑 `apply` 即可（开关与镜像侧不受影响）。
4. **只对研究实例**：`apply <实例>` 只改指定实例；日常实例必须保持 `0`。
5. 关于"镜像侧 su 扫描显示 `no gated su found`"：主机补丁生效后蓝叠会替换 guest `su`，
   属正常现象；**不必处理**，以 `su -c id` 为准。
