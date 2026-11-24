---
feature: auto-tdd
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# auto-tdd — 需求

本篇从过去的对话和提交记录里，整理用户对 `auto-tdd` 这个 skill 的需求。
实现见 [design](../design/auto-tdd-design.md)。
决策的来由见 [decision-history](../decision-history/auto-tdd-decision-history.md)。
opencode 会话存在本机 opencode.db，下文按会话 id 前缀引用。

## Overview

TDD（test-driven development，测试驱动开发）指先写一个会失败的测试，再写刚好让它通过的代码。
`auto-tdd` 让 agent 按 TDD 开发功能或修 bug，分基本和自动两种模式。
需求起点是 2026-06-19 的一个聊天 agent 项目（会话 ses_122b36d0）。
用户要求"使用tdd 的开发方式"，一个 agent 写代码，一个 agent 写测试。
随后用户说"把我完整的测试的loop task 做一个skill"，并命名为 auto-tdd（同一会话）。

## Goals and Success Metrics

目标一：agent 在"工作没有真的完整以前"一直工作下去，不提前宣布完成（ses_122b36d0，2026-06-19）。
目标二：测试先行，并覆盖足够多的情况，"保证测试准确率"（同一会话）。
目标三：修代码时连同 spec 和 skill 一起修，形成闭环（同一会话）。
成功指标：UNKNOWN。对话里没有给出可量化的指标；完成标准见 PRD-D 和 PRD-J。

## User Stories

- 作为开发者，我想要一种简单的 TDD 流程，一次只写一个测试。
- 作为开发者，我想让一个 agent 写代码、一个写测试，测试不过时它们商量，商量不出来由裁判定。
- 作为开发者，我不想反复追问"做完了吗"，agent 应该自己找出没做完的事继续做。

## Functional Requirements

**PRD-A 两种模式，先问再分支。** 基本模式是经典 TDD，自动模式是多 agent 持续循环。
开始时只问用户一个问题：选哪种模式。
证据：2026-08-02 把 auto-tdd 和导入的 tdd 合成一个 skill（commit 6086424；parent design 合并表的 `/auto-tdd` 一行）。
提出这次合并的那段对话没有找到，属于 UNKNOWN。

**PRD-B 基本模式沿用导入的 tdd。** 用户要求把 mattpocock/skills 的 tdd skill 导入 skill factory（ses_14aa890f，2026-06-10）。
导入见 commit eed365c，随后 d98ed8d 改写了描述。
它的做法叫 red-green-refactor：先写一个失败的测试（红），再写最少的代码让它通过（绿），最后整理代码（重构）。

**PRD-C 一个写代码，一个写测试，裁判定对错。** 用户原话是"1个agent 干活，一个agent 写test"。
测试不通过时"两边agent 讨论"，讨论不出来就"来一个裁判判断"，错的那个改（ses_122b36d0，2026-06-19）。

**PRD-D 没做完就不停。** 用户发现很多任务没继续做，要求总结原因写进 skill，
"保证以后agent 能在'工作没有真的完整以前' 一直工作下去"（ses_122b36d0，2026-06-19）。
用户还要求"用一个loop 跑，每30分钟看做没做完"，发现别的必做的事时"可以给自己的loop job 加task"（同一会话）。
2026-11-24 已恢复每 30 分钟自查，见 decision-history 的 ARD-K。

**PRD-E 先主流程，再边界，每个都举一反三。** happy path 指一切正常的主流程，edge case 指边界和异常情况。
举一反三指每写一个测试，就只换一个条件再写几个变体。
用户说"happy path 和edge 都要举一反三"（ses_122b36d0，2026-06-19）。
edge case 的例子有客户问问题、给错的值、来回跳转（同一会话）。

**PRD-F 先跑固定场景的确定性测试。** 用户要求先建一组"fix 的场景"：每次语言一样，按顺序来（ses_122b36d0，2026-06-19）。
更早时用户提出用 mock LLM（假的 LLM 替身）来节省测试 token，
"只有用户说真的跑llm 才跑"（ses_12801d33，2026-06-17）。

**PRD-G 再让 LLM 扮演客户端。** 客户端是一个 LLM，每次根据 agent 的回复自己生成下一句话（ses_122b36d0，2026-06-19）。
用户指定可用 deepseek v4 flash 和 gpt 5 nano 跑这类测试，并说"当你觉得都差不多了"再跑（同一会话）。

**PRD-H 裁判逐轮评质量。** 用户要求"弄一个裁判，分析每一个轮tst 做的好不好"。
要看有没有错误，以及多轮对话里每一轮的提问和回复质量（ses_122b36d0，2026-06-19）。

**PRD-I 做一点就提交一次。** 用户原话："工作每做一点，就commit 一下，不要等着一堆一起commit"。
最终的 PR 可以一起提，"这些也写在skill 里面"（ses_122b36d0，2026-06-19）。
2026-11-24 已恢复，见 decision-history 的 ARD-K。

**PRD-J 用杠精 skill 验收。** 杠精 skill 指 contrarian review，即专门挑毛病的对抗式审查。
用户要求"用杠精skill 验收工作，没完成需要写报告，下一轮 ai 继续干"（ses_122b36d0，2026-06-19）。

**PRD-K 代码、spec、skill 闭环修。** 用户要求先修项目代码，再按代码修 spec 和 skill，然后再迭代修代码，
"形成闭环，直到完全没有问题了"，并说"写在tdd 里面"（ses_122b36d0，2026-06-19）。

**PRD-L 完整 skill 放在 skill 仓库。** 用户说"这个skill 放在ai coworker 里面"，
业务项目里只放一个指向它的 link 或 reference（ses_122b36d0，2026-06-19）。
当年 ai coworker 的 skill 目录就在本仓库：commit 7bfe010 首次加入，93d4a4a 移到 `skills/auto-tdd/`。

## Out of Scope

一行的小改动、纯配置或文档改动、会被丢弃的原型，都不用本 skill（SKILL.md 的 When NOT to Use 一节）。
对话里没找到用户划这条范围的原话，出处属于 UNKNOWN。

## Resources Needed

自动模式的第二层测试要调用真实 LLM，需要至少两个模型的 API key（PRD-G）。
人力上，用户开始时选一次模式（PRD-A）；自动模式之后尽量不需要人介入（PRD-D）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 auto-tdd 的 PRD |
| 2026-11-24 | PRD-D、PRD-I 的现状句改为已恢复（ARD-K） |
