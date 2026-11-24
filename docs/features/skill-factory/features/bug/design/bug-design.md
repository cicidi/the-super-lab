---
feature: bug
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# bug — 调试、报告与自愈

本篇说明 `bug` 这个 skill 现在怎么工作。
源文件：`skills/bug/SKILL.md`（commit 6086424 定稿，93d4a4a 移到现在的位置）。

## Problem Statement

agent debug 时容易凭猜测改代码，修了症状却没修根因（PRD-B）。
用户纠正过的错误，下个会话又犯；记录纠正的 self-heal 写好后从没被调用过（ses_1417bab9，2026-06-23；PRD-G）。

## Solution

一个 skill，三条分支（PRD-A）：Hunt 找根因并修好，Report 提 GitHub issue，Heal 记下纠正并生成规则。

## User Stories

- 作为开发者，遇到报错时选 Hunt，按证据和假设一步步修。
- 作为开发者，要给当前仓库或自己选定的仓库提 issue 时选 Report。
- 作为用户，刚纠正过 AI 时选 Heal，让它记下来；攒够了再让它总结规则。

## Implementation Decisions

三条分支写在同一份 SKILL.md 里（274 行），没有脚本，也不调用子 agent。
Heal 依赖的 hook 脚本不在本 skill 里。本机 `~/.claude/hooks/on-self-heal.sh` 存在，但 `~/.claude/settings.json` 没有注册它。Heal 每次先检查，并告诉用户（ARD-M）。
`~/project` 下也找不到任何 `.self-healing/` 目录（2026-11-24 查看），即 Heal 目前没有积累数据。

## Design

**DSGN-A 选分支。** 开头只问一句"What do you need?"，在 Hunt、Report、Heal 中三选一（PRD-A）。

**DSGN-B Hunt 收集证据。** 先选模式：已知代码 bug 走快速调试，原因不明走深挖（ARD-K）。
快速调试先收集：报错和堆栈、复现步骤、相关代码、git log、日志和配置、用户消息，并看主分支是否通过。
这一步不过滤、不判断相关性（PRD-C）。

**DSGN-C Hunt 假设与验证。** 先列出找到的每条证据，再列 3 到 5 个可能的根因，按可能性排序（PRD-B）。
每个假设都要指向具体的证据（ARD-K）。
按顺序逐个验证：为每个假设设计一个只检验它的最小测试，记下预期和实际，判为确认或排除。
遇到第一个被确认的假设就停，此前不许动手修。

**DSGN-D Hunt 修复与记录。** 定位到具体的文件和行，只做针对根因的最小修复，不顺手重构（PRD-B）。
加一个回归测试（regression test，能抓住同一 bug 复发的测试），再跑全套测试确认没有新问题。
提交信息用 `fix:` 前缀；如果这个错误有普遍性，建议接着走 Heal。

**DSGN-E Hunt 深挖模式。** 原因不明、跨多个服务的事故走深挖（PRD-D、ARD-K）。
先查遍日志、部署、监控、消息和配置变化，再列证据、标异常、排时间线，最后写事故报告并走 Report 提 issue。

**DSGN-F Report 写 issue。** 项目 bug、walter-worker 自身的问题、需要讨论的功能请求都可以提（PRD-E）。
先写清发生了什么、本该怎样、怎么复现；是 AI 犯错时写明涉及哪个 skill 或规则。
标题用 `fix:` 或 `feat:`，walter-worker 自身的问题再加 `[coworker]` 前缀。
正文分五节：发生了什么、预期行为、受影响的组件、复现步骤、建议修法。
标签用 `bug` 或 `enhancement`，walter-worker 自身的问题用 `coworker-bug` 或 `coworker-improvement`；是 AI 犯错时同时走 Heal。
目标仓库默认取当前仓库（`gh repo view`，不行就看 git remote），也可从项目目录里选（PRD-F）。
提交前必须问用户"提到这个仓库吗"，用户确认才提交（ARD-L）。

**DSGN-G Heal 记录纠正。** 用户纠正 AI 时，写一条 trace（PRD-G）。
识别纠正靠关键词，如 no、don't、stop、wrong、never、"I told you"。
trace 追加到当前项目的 `.self-healing/traces/YYYY-MM-DD.yaml`，每天一个文件。
字段有 id、timestamp、context（AI 做错了什么）、correction（用户说了什么）、category。
category 五选一：code-conventions、workflow、security、architecture、tool-use。
记录之前先检查 Claude Code 和 OpenCode 的 hook 脚本在不在、有没有注册（PRD-H）。
没生效就告诉用户"纠正只在手动跑 Heal 时记录"；用户没明确要求，不安装也不注册（ARD-M）。

**DSGN-H Heal 分析规律。** 读所有 trace，按 category 分组，统计每条纠正出现的次数（PRD-I）。
同一条纠正出现 2 次及以上才算规律，单次纠正不生成规则（decision-history 的 ARD-H）。
把规则写成一段 markdown，放进项目 CLAUDE.md：已有 SELF-ANALYZE 块就替换，没有就追加到末尾。
最后报告分析了几条 trace、找到几个规律、写入几条规则。

**DSGN-I 质量门。** MUST 会挡住交付：Hunt 先列证据、假设指向证据、先有假设再修、加回归测试、修复最小。
深挖报告要有证据和时间线。Report 要用户确认过仓库，有复现步骤，指明受影响的组件。
Heal 要报告 hook 状态，trace 类别合法，只有 2 次以上的规律生成规则。
NICE 只提醒：查过 git log、附上建议修法、提醒积累后跑分析。

**DSGN-J 存放位置。** skill 在本仓库的 `skills/bug/SKILL.md`，不在 personal-skills（PRD-J）。

## Testing Decisions

本 skill 没有自动测试或评测集，`skills/bug/` 下只有 SKILL.md 一个文件。
旧 bug-report 曾有 4 个测试场景，例如"业务项目的 bug 应转去项目自己的 tracker"，合并时被删（6086424）。
skill 是否好用，目前只能在真实场景里用一次再人工判断。

## Out of Scope

功能需求转 `/feature`，代码评审转 `/spec-review` 的设计评审分支（由 doc-review 改名而来，ARD-N），一般性提问直接问（SKILL.md 的 When NOT to Use 一节）。

## Further Notes

需求见 [PRD](../prd/bug-prd.md)，决策见 [decision-history](../decision-history/bug-decision-history.md)。
2026-08-02 的合并表见 [parent design](../../../design/skill-factory-design.md)。
Hunt 的恢复原文来自 walter-worker 历史，可用 `git show f8b7ffb:skills/bug-hunt/SKILL.md` 查看（ARD-K）。

## Alternatives Considered

保留四个独立 skill：被否决，2026-08-02 合成一个（ARD-A）。
bug-sleuth 单独保留：被否决，用户要求并入 Hunt（ARD-D）。
让 AI 每轮自查有没有被纠正、不用 hook：被否决，改为检查 hook（ARD-F）。

## Drawbacks

没有注册的 hook，Heal 的记录只能靠 agent 自己察觉被纠正；目前没有任何 trace 数据。
现有 hook 脚本写入的 context 为空，category 固定为 workflow，按类别分组的分析会失真。
Report 每次都要用户确认仓库，多一步问答，换来不会提错仓库（ARD-L）。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| hook 按 no、never 等词匹配，普通句子也会被记成纠正 | 分析时只取出现 2 次以上的规律（ARD-H） |
| 2026-08-02 合并丢了用户 06-23 要的改动 | 2026-11-24 已按 walter-worker 原文恢复（ARD-K、ARD-L、ARD-M） |
| 自动写 CLAUDE.md 会改动用户的项目文件 | 只替换 SELF-ANALYZE 注释块内的内容，块外不动 |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 要不要恢复"先收集一切、再推理并列证据"（PRD-C）？ | 恢复，Collect 后 Reason 并列证据（ARD-K） | cicidi | no |
| QUES-B | 要不要恢复原因不明时的深挖模式（PRD-D）？ | 恢复，含事故报告格式（ARD-K） | cicidi | no |
| QUES-C | Report 要不要恢复"先选仓库"，面向所有 GitHub 仓库（PRD-F）？ | 默认当前仓库，可另选，提交前请用户确认（ARD-L） | cicidi | no |
| QUES-D | Heal 要不要恢复"先检查 hook、没有就提示安装"，并注册已有的 hook（PRD-H）？ | 先检查并告诉用户（ARD-M）；要不要注册仍待用户决定 | cicidi | no |
| QUES-E | "2 次以上才生成规则"这个阈值是用户定的吗（ARD-H）？ | UNKNOWN，沿用迁入的旧版 | cicidi | no |
| QUES-F | Report 和全局 CLAUDE.md 里的 walter-worker-fix skill 怎么分工？ | 都处理 walter-worker 自身的问题，未划分 | cicidi | no |

## Reversibility

所有改动都落在 git 跟踪的 `skills/bug/SKILL.md`，用 `git revert` 即可撤回。
Heal 写入 CLAUDE.md 的规则只在 SELF-ANALYZE 块里，删掉这个块即可撤回。已安装的副本须重跑 `install.sh` 才同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 bug 的 design，引用 PRD-A 到 PRD-J |
| 2026-11-24 | 按 ARD-K 到 ARD-N 改写 DSGN-B、C、E、F、G、I；QUES-A 到 QUES-C 已答，QUES-D 部分答 |
