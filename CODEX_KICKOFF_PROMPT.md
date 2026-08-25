# 给 Codex 的启动指令

请接管这个 Huuuge Casino Android 数值逆向项目。

先完整阅读 `HUUUGE_CODEX_HANDOFF.md`，然后检查当前 Windows 机器上的实际环境，不要让我手工复制执行命令。你拥有终端时，请自己执行 discovery、安装依赖、验证、修复和重试。

当前最高优先级：

1. 自动发现 BlueStacks 的真实安装目录、data dir、版本、实例 id 和 `bluestacks.conf`；
2. 保证正常主实例不被修改，所有 root/Frida 实验只放在 clone/research 实例；
3. 验证 BlueStacks x86_64 + Huuuge arm64-v8a native bridge 的实际运行方式；
4. 尝试在研究实例获得可用于 Frida 的 root；
5. root 成功后部署与 host 完全同版本的 frida-server，并实测 `frida-ps -U` + attach；
6. 复用 `artifacts/live_probe/agent.js` 和 `live_decode.py`；
7. 优先抓通 BattlePass 的 `Casino.RpcMessage`，用已恢复的 `huuuge_descriptors.pb` 自动解码；
8. 抓通后保存 JSON/CSV，并进一步生成 Battle Pass milestone / mission 数值表。

已完成的 APK pull、Protobuf descriptor 恢复和 hook 代码不要重做，除非你验证发现版本变化或已有结果错误。

重要约束：
- 不要修改金币、奖励、请求或服务端状态；
- 不做请求重放或作弊功能；
- 动态观测以被动采集为主；
- 任何 BlueStacks 配置修改前先备份；
- 不要破坏正常游戏实例；
- 遇到默认路径不存在，自己从进程、注册表、服务和磁盘布局 discovery；
- 不要把“APK 是 ARM64”直接当成 Frida server 一定要 ARM64，native bridge 场景需要实测；
- 能自己执行的步骤不要让我再手工执行。

每完成一个阶段，把结论和命令/脚本沉淀到 workspace 的 notes/scripts 中，保持项目可复现。
