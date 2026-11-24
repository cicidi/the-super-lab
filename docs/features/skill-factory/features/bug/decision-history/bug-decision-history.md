---
feature: bug
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# bug — 决策记录

本篇按时间倒序记录 `bug` 这个 skill 的关键决策。
需求见 [PRD](../prd/bug-prd.md)，设计见 [design](../design/bug-design.md)。
skill-factory 层面的旧决策在 [parent decision history](../../../decision-history/skill-factory-decision-history.md)。
opencode 会话按会话 id 前缀引用，数据在本机 opencode.db。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-A | 2026-08-02 | 把 bug-hunt、bug-report、self-heal、self-analyze 合成一个三分支 skill；开头只问一个问题选分支 |
| ARD-B | 2026-08-02 | 合并时采用 skill-factory 里的旧版 bug-hunt 和 bug-report，没有带上 06-23 在 walter-worker 的改动 |
| ARD-C | 2026-06-23 | debug 先收集一切可能相关的信息，不急着分析；再推理，并列出证据 |
| ARD-D | 2026-06-23 | bug-sleuth 并入 bug-hunt，分"已知代码 bug"和"原因不明的深挖"两种模式 |
| ARD-E | 2026-06-23 | bug-create 并入 bug-report，并改为可以向任意 GitHub 仓库提 issue |
| ARD-F | 2026-06-23 | hook 装在全局（Claude Code 和 OpenCode 各一份），trace 存在项目里；skill 触发时先检查 hook |
| ARD-G | 2026-06-23 | 分析结果写进项目 CLAUDE.md 的 SELF-ANALYZE 块；已有就替换，没有就追加 |
| ARD-H | 2026-06-23 | 同一条纠正出现 2 次及以上才生成规则，单次纠正不生成 |
| ARD-I | 2026-06-23 | self-heal 和 self-analyze 放进 skill-factory 的 ai-coworker-skills，从 personal-skills 删除 |
| ~~ARD-J~~ | ~~2026-06-11~~ | ~~self-analyze 和 self-healing-trace 迁到 personal 目录~~ 已被 [ARD-I](#ard-i) 取代 |

## Evidence Appendix

### ARD-A

理由：commit 6086424 的说明是，近似重复的 skill 合成一个，先问清问题，再分到对应流程（PRD-A）。
被否决的方案：保留四个独立 skill。同一天 walter-worker commit e964925 也换成同样的 `bug`。
出处：commit 6086424；parent design 合并表的 `/bug` 一行。发起合并的那段对话没有找到，属于 UNKNOWN。

### ARD-B

理由：UNKNOWN。6086424 合并的输入是本仓库 `ai-coworker-skills/` 里的旧版，最后改动在 3395648 和 cca25cd。
因此丢了：先收集后推理（ARD-C）、深挖模式（ARD-D）、任意仓库（ARD-E）、触发时检查 hook（ARD-F）。
这些改动当时只提交在 walter-worker（f8b7ffb、af88df6、6511f37、5138ea3），e964925 合并时也被同一份旧内容覆盖。
被否决的方案：以 walter-worker 的新版为输入。是有意取舍还是漏掉，属于 UNKNOWN，见 design 的 QUES-A 到 QUES-D。

### ARD-C

理由：用户说 debug 一个重要的地方是"收集所有信息，只要可能相关的，先不分析"，然后"推理，并列证据"（PRD-C）。
被否决的方案：UNKNOWN，对话里没有列出别的方案。出处：ses_1417bab9（2026-06-23）；walter-worker commit f8b7ffb。
当前 SKILL.md 的 Phase 1 只收集报错、测试、代码和 git log，没有日志和消息，也没写"先不过滤"，原因见 ARD-B。

### ARD-D

理由：agent 解释了两者区别：bug-hunt 管已知代码 bug，bug-sleuth 管不知原因的多服务事故；用户回复"合并"（PRD-D）。
被否决的方案：保留两个独立 skill（agent 当时给的另一个选项）。出处：ses_1417bab9（2026-06-23）；walter-worker af88df6。
当前 SKILL.md 没有深挖模式和事故报告格式，原因见 ARD-B。

### ARD-E

理由：用户说 bug-create 和 bug-report"重复了， merge成一个"，又说要"对于所有github"（PRD-E、PRD-F）。
被否决的方案：只向 ai-coworker 一个仓库提 issue（旧 bug-report 的做法）。
出处：ses_1417bab9（2026-06-23）；walter-worker 4285718、6511f37。当前 SKILL.md 又回到只写 walter-worker，见 ARD-B。

### ARD-F

理由：agent 分析 self-heal 从没被调用，是因为没有触发机制：Claude Code 不会自己按关键词调用 skill（PRD-H）。
用户随后定下：触发时检查 hook，hook 全局装在两个 IDE，数据存项目级（PRD-G）。
被否决的方案：在 CLAUDE.md 加规则让 AI 每轮自查有没有被纠正（agent 当时给的第二个方案）。
出处：ses_1417bab9（2026-06-23）；walter-worker 5138ea3、45e9edf。当前 SKILL.md 没有检查 hook 的步骤，见 ARD-B。

### ARD-G

理由：用户要求 self-analyze 总结后"放到当前project level 的claude.md"（PRD-I）。
用 `<!-- SELF-ANALYZE -->` 注释包住、已有就替换，是 agent 写入的做法，用户没有逐条确认。
被否决的方案：UNKNOWN。出处：ses_1417bab9（2026-06-23）；commit dce0d79。

### ARD-H

理由：UNKNOWN。"2+ 次才算规律"在 2026-06-23 迁入的 personal-skills 版 self-analyze 里就有（commit 3395648）。
对话里没找到用户定这个阈值的原话。被否决的方案：UNKNOWN。见 design 的 QUES-E。

### ARD-I

理由：用户说"这个self healing move 到skill-factory/ai-coworker-skill factory 里面"（PRD-J）。
又问"怎么还在personal folder 里面"。被否决的方案：放在 personal-skills（ARD-J）。
出处：ses_1417bab9（2026-06-23）；commit dce0d79（加入）、bd9bb02（从 personal 删除）。

### ARD-J

理由：清理 ai-coworker 时，用户把 coworker-meta-self-analyze 和 coworker-meta-self-healing-trace 映射到 personal 目录。
同一条消息把 coworker-meta-report-issue 映射为 ai-coworker-issue-report，即后来的 bug-report。
被否决的方案：UNKNOWN。出处：ses_14a669c2（2026-06-11）。personal 的位置被 ARD-I 取代。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 bug 的决策 |
