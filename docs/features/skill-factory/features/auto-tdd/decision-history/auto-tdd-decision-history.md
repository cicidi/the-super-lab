---
feature: auto-tdd
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# auto-tdd — 决策记录

本篇按时间倒序记录 `auto-tdd` 这个 skill 的关键决策。
需求见 [PRD](../prd/auto-tdd-prd.md)，设计见 [design](../design/auto-tdd-design.md)。
skill-factory 层面的旧决策在 [parent decision history](../../../decision-history/skill-factory-decision-history.md)。
opencode 会话按会话 id 前缀引用，数据在本机 opencode.db。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-M | 2026-11-24 | 第二层（真实 LLM 扮演用户）第一次跑之前先问用户一次；用户不同意就跳过，并在报告里写明 |
| ARD-L | 2026-11-24 | 完成标准里的 contrarian review 指 `/spec-review` 的 Quick Scan；4、5 级问题算 HIGH、CRITICAL |
| ARD-K | 2026-11-24 | 恢复逐次提交（每个绿步提交一次，提交信息带通过的测试数）和每 30 分钟自查 |
| ARD-A | 2026-08-02 | 把 auto-tdd 和导入的 tdd 合成一个两模式 skill；开头只问一个问题选模式 |
| ARD-B | 2026-08-02 | 合并时把自动模式从约 350 行的完整版压成摘要版 |
| ARD-C | 2026-06-19 | 完整 skill 放在 ai coworker 的 skill 仓库，业务项目只留引用 |
| ARD-D | 2026-06-19 | 修 bug 时连同 spec 和 skill 一起修，闭环迭代到没有 CRITICAL 和 HIGH 问题 |
| ARD-E | 2026-06-19 | 测试全过后用 contrarian review 做最后一道验收，没过就写报告继续 |
| ARD-F | 2026-06-19 | 每做一点就提交一次，PR 最后合起来提 |
| ARD-G | 2026-06-19 | 测试分三层并严格按序：固定场景的确定性测试、LLM 扮演客户端、质量裁判 |
| ARD-H | 2026-06-19 | 循环到真正做完才停；新发现的问题立刻变成任务；每 30 分钟自查一次 |
| ARD-I | 2026-06-19 | 设四个角色：A 写代码，B 写测试，C 仲裁 A 与 B 的分歧，D 评质量 |
| ~~ARD-J~~ | ~~2026-06-11~~ | ~~导入 mattpocock 的 tdd，作为独立的 skill~~ 已被 [ARD-A](#ard-a) 取代 |

## Evidence Appendix

### ARD-M

理由：第二层至少调用两个真实模型，要花钱。被否决：无条件跑；完全不跑。出处：用户 2026-11-24（会话 80291c19）"按照你的建议来吧"。

### ARD-A

理由：commit 6086424 的说明是，近似重复或互补的 skill 合成一个，先问清问题，再分到对应流程。
被否决的方案：保留 auto-tdd 和 tdd 两个独立 skill。
ARD-J 导入的 red-green-refactor 仍然有效，成为基本模式（PRD-A、PRD-B）。
出处：commit 6086424；parent design 合并表的 `/auto-tdd` 一行。发起合并的那段对话没有找到，属于 UNKNOWN。

### ARD-B

理由：UNKNOWN。commit 6086424 把 7bfe010 时约 350 行的文件压到 138 行。
删掉的内容有：逐次提交、每 30 分钟自查、A 与 B 不得同时改代码、常见借口表、5 个测试场景。
被否决的方案：保留完整版。是有意删减还是压缩时漏掉，属于 UNKNOWN，见 design 的 QUES-A 和 QUES-B。

### ARD-C

理由：用户问"tdd skill 做好了吗"后说"这个skill 放在ai coworker 里面"，项目里只放 link 或 reference（PRD-L）。
被否决的方案：把完整 skill 放在业务项目里。
出处：ses_122b36d0（2026-06-19）；commit 7bfe010 把完整版加入 skill 仓库。

### ARD-D

理由：用户要求先修项目代码，再修 spec 和 skill，再迭代修代码，"形成闭环"，并"写在tdd 里面"（PRD-K）。
CRITICAL 和 HIGH 是 contrarian review 报告里最高的两级问题；"零 CRITICAL 加零 HIGH"这个收敛线由 agent 写入，用户原话是"直到完全没有问题了"。
被否决的方案：只修代码，不回头修 spec 和 skill。
出处：ses_122b36d0（2026-06-19）；规则原文见子会话 ses_11f817c2（同日）和 commit 7bfe010 的第 12 条。

### ARD-E

理由：用户要求"用杠精skill 验收工作，没完成需要写报告，下一轮 ai 继续干"（PRD-J）。
7bfe010 版写明调用 contrarian-review 的 Mode 1（轻量验证），报告写成 `GAPS.md`，有缺口就继续循环。
被否决的方案：测试全绿就算完成。出处：ses_122b36d0（2026-06-19）；commit 7bfe010。

### ARD-F

理由：用户说"工作每做一点，就commit 一下"，最终 PR 可以一起提，并要求写进 skill（PRD-I）。
被否决的方案：攒一堆改动一起提交。出处：ses_122b36d0（2026-06-19）；commit 7bfe010 的第 7、8 条。
6086424 合并时删了这条（ARD-B），2026-11-24 已恢复，见 ARD-K。

### ARD-G

理由：用户要求先建固定场景，"每次语言是一样的，按顺序来的"；再让 LLM 做客户端；第三弄一个裁判（PRD-F、PRD-G、PRD-H）。
"至少两个模型"来自用户先后提到 deepseek v4 flash 和 gpt 5 nano 两个模型。
被否决的方案：只跑 mock 测试，或直接用真实 LLM 跑。出处：ses_122b36d0（2026-06-19）；ses_12801d33（2026-06-17）。

### ARD-H

理由：用户在一轮开发后发现很多任务没做完，要求"用一个loop 跑，每30分钟看做没做完"，并可以给自己加任务（PRD-D）。
7bfe010 版把停滞的原因归到 "yolo aggressive" 式的走捷径，并列成防停滞表。
被否决的方案：第一次测试全绿就宣布完成。出处：ses_122b36d0（2026-06-19）；commit 7bfe010。
6086424 合并时删了 30 分钟自查（ARD-B），2026-11-24 已恢复，见 ARD-K。

### ARD-I

理由：A、B、C 三个角色来自用户的原始要求，C 是"来一个裁判判断"（PRD-C）。
D 来自用户后来要的"裁判，分析每一个轮tst"（PRD-H）。
C 的判定顺序（spec 优先于框架约定，约定优先于风格）由 agent 写入，用户没有逐条确认。
被否决的方案：一个 agent 同时写代码和测试。出处：ses_122b36d0（2026-06-19）；commit 7bfe010。

### ARD-J

理由：用户给 skill factory 选的第一个导入对象就是 mattpocock 的 tdd skill（ses_14aa890f，2026-06-10）。
被否决的方案：自己从头写 TDD skill。出处：commit eed365c（导入）、d98ed8d（改写描述，同时删掉了 `source` 出处字段）。
独立 skill 的形式被 ARD-A 取代，内容成为基本模式。

### ARD-K

理由：用户原话"工作每做一点，就commit 一下"和"每30分钟看做没做完"（ses_122b36d0）；6086424 合并时删了（ARD-B）。
按 6086424 之前版本的第 7、8、10 条原文恢复，两种模式都要逐次提交。
被否决的方案：保持删减后的版本。出处：用户 2026-11-24 审阅回复；ses_122b36d0；commit 6086424 的父版本。

### ARD-L

理由：contrarian-review 在 6086424 并入 doc-review，c44e983 又改名为 spec-review。
旧版调用它的 Mode 1（轻量验证）写缺口报告；spec-review 里对应的是 Quick Scan，按 1 到 5 级打分。
被否决的方案：用 Work Completion Review，它做验收签字，不按严重度分级。
出处：用户 2026-11-24 审阅回复；commit 6086424、c44e983；`skills/spec-review/SKILL.md` 的 Sources 一节。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 auto-tdd 的决策 |
| 2026-11-24 | 加 ARD-K（恢复逐次提交和 30 分钟自查）、ARD-L（contrarian review 指 spec-review） |
| 2026-11-24 | 加 ARD-M：第二层先问用户 |
