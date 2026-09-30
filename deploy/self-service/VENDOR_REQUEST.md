# TASK-0037 无影技术咨询草稿（尚未提交）

收件方：阿里云无影云手机技术支持。主题：现有单台实例的 Web SDK Ticket 撤销及应用控制边界。

以下正文可在 Owner 明确同意后，通过已登录的官方工单入口提交。只提供产品类型、既有实例定位和下列测试事实；不附 Ticket、Cookie、Google/游戏账号、ADB/TLS 密钥或完整 API 日志。不授权新增收费、重建、重启或清数据。

---

我们已有一台香港地域的无影云手机，Android 12，当前 API 返回 StreamMode=1。准备让两个内部策划通过官方 Web SDK 轮流独占体验同一固定 Huuuge 账号，不同时使用。

2026-09-30 已验证：

1. 通过官方 `BatchGetAcpConnectionTicket` 可对该现有实例取得 Finished 连接凭证。
2. 使用官方 Web SDK 的 Ticket 模式得到 onConnected；测试始终关闭输入，没有操作游戏。
3. 调用 `DisconnectAndroidInstance` 后，SDK 显示管理侧断开（2027）。但原 Ticket 曾再次得到 onConnected；不能据 API 成功就释放给下一人。
4. 另做过换发 Ticket 的检查，新旧 Ticket 不同；后续旧 Ticket 测试出现协议网关错误2507。该错误不能证明凭证被明确吊销。
5. 测试已结束，API 回读 SessionStatus=disconnect，实例继续运行。

请确认以下问题，提供适用于**现有这台实例**的官方方法和可复现验收步骤：

- 是否支持立即吊销某次控制 Ticket，使旧标签页、旧 Ticket 及可能的续期材料均不能重新连接或干扰下一位？需要哪个 API、参数、产品开关及等待/回读条件？
- 如果实例版/当前串流模式只支持断开而不支持吊销，便捷账号的取消分配或其他官方机制是否会实质阻止已发出的旧 Ticket？能否在不重建、不重启、不新增付费资源的条件下使用？
- 如何在服务端限制普通 SDK 使用者仅控制指定 Huuuge 应用，禁止任意 `lync_adb_shell`、系统设置/账号/支付信息访问及文件、剪贴板、摄像头、麦克风功能？仅隐藏SDK按钮不满足要求。
- 上述必要 API 的 RAM Action、资源级约束与有效条件是什么？希望常驻服务只管理指定实例，不授予云管理员或网络/IAM修改权限。

任何收费、资源替换、重启、清数据或安全策略改动，请先说明，不要直接执行。

---

确认来源：[无影断连API](https://help.aliyun.com/zh/ecp/api-eds-aic-2023-09-30-disconnectandroidinstance)只对矩阵版协同模式明确描述 Ticket 失效；[Web SDK](https://help.aliyun.com/zh/ecp/web-sdk-of-cloudphone)的控制与错误码说明。当前实测不应被泛化为所有模式都不可撤销。
