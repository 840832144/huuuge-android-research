# Pop! Slots 分析环境（ENVIRONMENT_LOCK）

> Game: **Pop! Slots**（PlayStudios），包名 `com.playstudios.popslots`。
> 分析目标：大厅「真人 + 机器人混合氛围」拆解（见
> `POP_SLOTS_LOBBY_FORENSICS.md`）。

## 环境（确认于本轮分析）

| 项 | 值 |
|---|---|
| 模拟器 | BlueStacks 5，实例 `Pie64_1`（Huuuge 研究实例），adb `127.0.0.1:5565` |
| 系统 | Android 9，**x86_64**（**非 Houdini**，游戏原生 x86_64）|
| root | 已开（`su -c id` → uid 0），可直接用 frida-server |
| 游戏进程 | `com.playstudios.popslots`，前台 Activity `com.playstudios.ShakerGameActivity` |

## 引擎与网络

- **引擎：Shaker**，主库 `libBigCasino.so`（x86_64，约 19MB，**带导出符号**，
  可符号级分析）。
- 内置完整 TLS（`libBigCasino.so` 内含 `SSL_write`/`SSL_read`/`BIO_write` 等），
  另有系统 `libssl.so`（游戏实际用的是引擎内嵌那份）。
- 网络：HTTPS，连接**多台**服务器（AWS `ec2-*.compute-1.amazonaws.com` 等）+ Google 基础设施；
  也有 WebView（`app_webview`，Chrome `libmonochrome.so`）用于营销/登录类功能，
  **大厅是 Shaker 原生 3D 渲染**。

## 工具链（复现步骤）

> 本节的命令都是**可移植**的：把 `<serial>` 换成你自己实例的 adb 串号即可。
> 先跑自检，它会告诉你每一步是否就绪：
> `python tools/analysis/popslots/pop_doctor.py --serial <serial>`

1. **准备 frida-server**（公开产物，不需要任何人提供文件）：
   到 Frida 官方发布页下载与本地 `frida` Python 版本一致的 **x86_64** 构建
   （`frida-server-<ver>-android-x86_64.xz`），解压后推入设备。

2. **以 root 运行 frida-server**。注意 root 通道**因实例而异**，两种都要能处理：
   - **`adbd` 通道**（实例没有 `su` 二进制，例如只用 `adb root` 的研究实例）：
     ```
     adb -s <serial> root          # 之后 adb shell 直接是 uid 0
     adb -s <serial> push frida-server-<ver>-android-x86_64 /data/local/tmp/fs
     adb -s <serial> shell "chmod 755 /data/local/tmp/fs"
     adb -s <serial> shell "/data/local/tmp/fs -D &"
     ```
   - **`su` 通道**：
     ```
     adb -s <serial> push frida-server-<ver>-android-x86_64 /data/local/tmp/fs
     adb -s <serial> shell "su -c 'chmod 755 /data/local/tmp/fs'"
     adb -s <serial> shell "su -c '/data/local/tmp/fs -D &'"
     ```
   - 工具会用 `pop_common.root_mode()` 自动识别是哪种通道，**不用手工判断**。

3. **转发端口并确认连通**（工具默认连 `127.0.0.1:27042`，与 frida-server 自身默认端口一致；
   用别的端口就加 `--frida <host:port>`）：
   ```
   adb -s <serial> forward tcp:27042 tcp:27042
   ```

4. **跑自检确认就绪**：
   ```
   python tools/analysis/popslots/pop_doctor.py --serial <serial>
   # 期望最后一行 verdict: READY
   ```

5. **用本目录工具脚本（`tools/analysis/popslots/`）分析**：
   - `pop_syms.py` 枚举符号 → 找房间/角色/行为入口
   - `pop_parse.py` hook `parseUserData` → 读用户身份字段
   - `pop_users_sampler.py` 常驻采样 → 统计机器人特征
   - 大厅未加载时 attach 会提示 `libBigCasino.so is not loaded yet`，进大厅后重跑即可。

## 判定的证据（本轮结论摘要）

- 用户样本呈现**填充特征**：ID 高度聚集（大量 `...0001284xxxx`）、国家集中于 US、
  存在 `Guest827` 这类无真名账号、部分样本无真人名；夹杂少量完整真实资料
  （人名 + 州 + 数值）作点缀。
- 行为：站立 → 走到机台 → 坐下 → 玩/庆祝（`CShakerAvatarWalkToSitActivityHandler`
  等），机台基本始终有人。
- 结论：**真实多人房间架构 + 服务器填充模拟用户**，用于营造大厅热闹氛围。

## 注意

- 采样到的用户数据（`pop_users.jsonl` 等）含账号/身份信息，**只留本地，勿入 Git**。
- 该实例同时用于其他研究，注意别污染其它任务的代理/证书配置。
