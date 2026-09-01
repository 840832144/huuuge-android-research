# Agent Git 接管速查

> 面向 Trae + DeepSeek（简称 DSH）、Codex 及其他本机 Agent。GitHub `main` 是研发协作与跨 Agent 交接的事实源；策划日常使用的采集器仍从 SVN 更新。

## 1. 第一次接管

如果仓库还不存在，在 PowerShell 中执行：

```powershell
git clone https://github.com/840832144/huuuge-android-research.git D:\huuuge-research
Set-Location D:\huuuge-research
git switch main
git pull --rebase origin main
```

这是私有仓库。第一次使用可能需要用户完成 GitHub 登录或凭据授权，Agent 不得索要、复制或保存用户 token。

如果仓库已经存在：

```powershell
Set-Location D:\huuuge-research
git status --short
git pull --rebase origin main
```

只有 `git status --short` 没有输出时，才直接执行上面的 pull。若存在本地修改，先判断是谁的改动；不得 reset、checkout 覆盖、删除或用自动 stash 隐藏不明改动。

## 2. 每轮工作前必须读什么

更新成功后按顺序读取：

1. `AGENTS.md`
2. `CONTRIBUTING.md`
3. `CURRENT_STATUS.md`
4. `COLLAB_LOG.md` 最新记录
5. `TASKS.md`
6. `CHANGELOG.md`
7. 当前任务对应的 handoff、guide 或模块档案

不要只依赖聊天内容。仓库中的已确认事实、证据边界和下一步优先级高于旧对话摘要。

## 3. 修改时的基本规则

- 只改当前任务需要的文件，不顺手格式化整个仓库。
- 不覆盖用户或其他 Agent 的本地修改。
- APK、`.so`、Frida 二进制、原始 capture、账号/Session ID、token、完整余额和 value-bearing JSON 不得进入 Git。
- 原始数据放在 `.local`、capture root 或任务明确指定的本机目录中。
- Confirmed、Schema-only、Inferred 必须分开；未验证的推断不能写入 `CURRENT_STATUS.md` 作为事实。
- 不使用 `git reset --hard`、`git clean -fd`、force-push 或改写共享 `main` 历史。

## 4. 提交前怎么检查

先运行与改动相匹配的测试，再检查差异：

```powershell
git status --short
git diff --check
git diff -- <明确的文件路径>
```

有意义的工作结束前，按 `CONTRIBUTING.md` 更新：

- `COLLAB_LOG.md`
- `CURRENT_STATUS.md`
- 发生工具/流程/输出变化时更新 `CHANGELOG.md`
- 完成或新增任务时更新 `TASKS.md`
- 明确交接给其他 Agent 时更新相关 handoff

只暂存本轮确认过的文件，不使用不加检查的 `git add -A`：

```powershell
git add -- <文件1> <文件2> <协调记录文件>
git diff --cached --check
git diff --cached --stat
```

## 5. Commit 和 Push

Commit 格式：

```text
<prefix>: <简洁动作说明>
```

常用 prefix：`docs`、`probe`、`proto`、`env`、`analysis`、`export`、`fix`、`chore`。

示例：

```powershell
git commit -m "probe: add Big Fish passive capture diagnostics"
git pull --rebase origin main
git push origin main
```

提交完成后再次 pull，是为了在 push 前吸收其他 Agent 刚提交的远端更新。若 rebase 发生冲突：

1. 逐文件读取双方内容；
2. 对 `CURRENT_STATUS.md`、`COLLAB_LOG.md`、`TASKS.md` 和 `CHANGELOG.md` 做语义合并；
3. 不盲目选择 `ours` 或 `theirs`；
4. 解决后执行 `git add -- <已解决文件>` 和 `git rebase --continue`；
5. 重新运行相关验证，再 push。

如果不能判断冲突哪一方正确，停止并把冲突文件与两边证据报告给用户，不要猜。

## 6. 如何确认真的上传成功

不能只看 `git push` 没报错。最后核对：

```powershell
git status --short
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

成功标准：

- `git status --short` 没有输出；
- 本地 `HEAD` 与远端 `refs/heads/main` 哈希一致；
- 最终回复写明 commit 哈希、已完成结果、仍有的 blocker 和下一步。

没有终端权限、GitHub 认证失败或 push 未成功时，必须明确写“只生成了本地修改，尚未提交/上传”，不能声称已同步。

## 7. Git 与 SVN 的边界

- GitHub `main`：工程代码、结构化分析、状态与跨 Agent 交接。
- SVN `trunk/HuuugeCollector`：策划可部署的安全 allowlist 包。
- 只有策划工具、工作流或说明发生变化并完成验证时，才按 `CONTRIBUTING.md` 镜像 SVN。
- SVN 中文日志必须使用已验证的 UTF-8 文件工作流；不要直接执行中文 `svn commit -m`。
- 不得把 Git 中不允许提交的敏感文件复制到 SVN。

## 8. 可直接交给 DSH 的开场提示词

```text
你现在接管本机 D:\huuuge-research。先执行 git status --short；工作区干净时 pull --rebase origin main，不干净时先保护并报告现有修改。然后严格读取 AGENTS.md、CONTRIBUTING.md、CURRENT_STATUS.md、最新 COLLAB_LOG.md、TASKS.md、CHANGELOG.md 和当前 handoff。GitHub main 是跨 Agent 事实源。完成任务后运行相关验证，更新协作记录，只暂存本轮明确文件，使用有意义的 commit message，pull --rebase 后 push，并核对本地 HEAD 与远端 main 一致。禁止 force-push、reset --hard、覆盖他人改动，以及提交 APK、二进制、原始 capture、账号/Session/token/完整余额数据。若没有终端权限或 push 失败，明确报告尚未上传，不得假装成功。
```
