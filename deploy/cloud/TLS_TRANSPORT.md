# TASK-0031：现有公网 ADB 上的加密采集通道

## 契约

本路径明确记录真实公网 `adb_serial`。传统 TCP ADB 保留原密钥鉴权，但自身不提供加密；它只承载本次专用转发。Frida 从云手机回环端口到云端 Linux 的回环端口使用 TLS、固定手机证书和独立令牌，业务数据始终在该加密连接内。禁止用一个回环别名把明文公网通道伪装成私网。

原私网配置仍有效。公网模式必须在原配置中增加完整对象，缺项、假私网地址或无 TLS 时拒绝：

```json
"transport": {
  "kind": "public-adb-frida-tls",
  "certificate": "/srv/huuuge-private/runtime/phone.crt",
  "token_file": "/srv/huuuge-private/runtime/frida.token",
  "device_port": 27042
}
```

`adb_serial` 填已通过厂商 API 归属核验的真实入口，仅保存在受控配置中；`frida_endpoint` 必须是 Linux 本机回环地址。controller 继续检查 Huuuge 包、版本、ARM64、Root、专用 ADB server、唯一 forward 的两端及 TLS 证书；token 文件必须由运行用户拥有且无组/其他用户权限。live_decode 只从文件读取令牌并传给官方 Frida API，无明文回退，不把令牌写进命令参数或 manifest。

## 本轮实际准备方法

1. 通过现有 ECS Cloud Assistant 和手机 EdsAgent 执行任务，管理身份、手机绑定和公网映射保持原有配置。本机只发管理命令，不承载采集或转发。
2. 找到既有 Python 3.11.13，以 `python3.11 -m venv` 在任务独立目录创建环境；PyPI 安装原 requirements 的 Frida 17.17.0、protobuf、lz4。系统 Python 3.6.8 不替换。
3. 官方 Frida release 下载 `frida-server-17.17.0-android-arm64.xz`，云端解压；通过已有 ADB 传输公开工具二进制，回读 SHA256 核对，不在明文 ADB 上传送私钥、令牌或采集数据。
4. 手机原无可用 OpenSSL CLI。仅将 Termux 官方仓库的 OpenSSL 工具及必要库解包到本任务独立目录，核对仓库元数据与包 SHA256；不安装 Termux APK、不改系统库。该工具只用于在手机内生成短期 TLS 私钥/自签名证书及解密本次令牌。手机私钥始终留在手机内，目录0700、文件0600；只通过已核验 EdsAgent 回读公开证书并固定在 Linux。
5. Linux 在独立目录生成随机令牌，用已固定的手机公钥做 RSA-OAEP-SHA256 加密；ADB 仅传密文，手机在本地解密。不得把明文秘密放进 RunCommand/SendFile 正文、平台输出、聊天或 Git。
6. Frida server 仅监听手机 `127.0.0.1:27042`，启用 `--certificate` / `--token`，加 `--disable-preload --ignore-crashes`；不设置全局 `setenforce`。创建专用 `adb forward --no-rebind`，核验 Linux 监听仅回环且精确映射到本台手机和上述端口。
7. 挂接前检查：TLS 最低1.2、固定证书实际一致、错误证书被拒、错误令牌被拒、正确令牌可鉴权、两端监听回环；结果保存在云端受控记录。只有全部通过才进入原 controller `probe/run`。公网 ADB 鉴权成功或转发成功不替代这些检查。
8. 当前游戏 build 必须重新核对。`extract_embedded_descriptors.py` 从当前安装 APK 的原生 ELF 中读取完整嵌入 descriptor，旧 descriptor 只用于必需文件名检查；歧义、缺名、依赖不完整时停止，不能补入旧结构冒充当前版本。只读取应用代码，不读取账号或历史 capture。

## 部署、执行与收尾

部署已提交的源码：从受控 Git checkout 用 `git archive` 导出本次 commit，校验归档的 commit 元数据后解包到云端任务目录，并将同一完整40位 SHA 写入 `.cloud-revision`。controller 在 Git checkout 读取 HEAD；归档部署读取该文件。不需在共享主机安装 Git，不手填虚假版本。

保留原 `check → probe → run → READY → play-start/play-end → stop → finalize/status` 流程；只启动一个新批次。READY 必须已有新增 Raw 和成功解码，之后通知 User 做普通 Slots。退出与文件回读后再清理本次 Frida、精确 forward、连接及专用 ADB server；检查监听/PID不存在。保留结果和脱敏统计，清理临时令牌、私钥及测试用材料，原绑定密钥保持不变。停止 server 不代表删除 User 的原公网映射。

真实 TLS、descriptor 和采集结果分开登记在 [验收记录](ACCEPTANCE.md)。合成测试不计入真实消息数。

## 官方依据

- [Android：传统 TCP ADB 与 TLS 无线调试](https://android.googlesource.com/platform/packages/modules/adb/+/HEAD/docs/dev/adb_wifi.md)
- [Frida：TLS 和认证接口](https://frida.re/news/2021/07/18/frida-15-0-released/)
- [Frida 17.17.0 server 参数](https://github.com/frida/frida-core/blob/17.17.0/server/server.vala)
- [Frida 17.17.0 socket provider：TLS 后的消息连接](https://github.com/frida/frida-core/blob/17.17.0/src/socket/socket-host-session.vala)
- [Termux OpenSSL 官方包定义](https://github.com/termux/termux-packages/blob/master/packages/openssl/build.sh)

### 挂接前启动失败的有限恢复

只有子进程已exit1、Session目录从未创建、未发出stop且原run锁可获得时，`retry-start`才允许保留同一批次标识恢复一次。原日志和失败状态另存，第二次恢复或已有任何Session目录均拒绝。当前APK自带Google descriptor时优先使用它，避免与运行库预置版本重名；controller的probe使用相同加载器提前验证。
