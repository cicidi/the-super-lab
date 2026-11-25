---
feature: auto-tdd
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# auto-tdd — 测试驱动开发循环

本篇说明 `auto-tdd` 这个 skill 现在怎么工作。
源文件：`skills/auto-tdd/SKILL.md`（commit 6086424 定稿，93d4a4a 移到现在的位置）。

## Problem Statement

agent 写代码时，常在第一次测试全绿后就宣布完成，边界情况没测，质量没人评（PRD-D）。
2026-06-19 的项目里，用户反复追问"ft 为什么没跑""所有工作都干完了吗"（ses_122b36d0）。
ft 指 functional test，即功能测试。

## Solution

一个 skill，两种模式（PRD-A）。基本模式一次只写一个测试。
自动模式是四个角色组成的循环，完成标准全部满足才停。

## User Stories

- 作为开发者，我只想要 TDD 的纪律时，选基本模式。
- 作为开发者，任务复杂、需要多方把关时，选自动模式，之后不用盯着。

## Implementation Decisions

四个"agent"都写在同一份 SKILL.md 里，文中没有调用子 agent 的步骤。
2026-07-13 的一次分析认为，它是同一个 LLM 依次扮演各个角色（ses_0a0d1bce），见 QUES-E。
写代码的规模上限（每个文件不超过 1000 行，每个方法不超过 50 行）来自用户给自己框架定的代码规范（ses_12801d33，2026-06-17）。

## Design

**DSGN-A 选模式。** 开头只问用户一句：基本 TDD 还是自动 TDD（PRD-A）。

**DSGN-B 基本模式。** 测试只通过公开接口验证行为，不测内部实现（PRD-B）。分四个阶段。
计划：确认要改的接口，给要测的行为排优先级，取得用户批准。
tracer bullet（曳光弹）：先为一个行为写一个测试并让它通过，证明从头到尾的路径能走通。
增量循环：每个剩下的行为都先写测试并确认失败，再写最少的代码让它通过，然后立刻提交一次（ARD-K）。
重构：所有测试通过后才去掉重复、加深模块，每步重构后重跑测试；测试为红时不重构。
SKILL.md 把"先写完全部测试再写全部代码"列为反模式，要求一个测试、一段实现地交替推进。

**DSGN-C Agent-A 写代码。** 遵守框架约定和上面的规模上限（PRD-C）。
防停滞：发现已有的 bug，立即变成任务，不以"不是我的活"跳过（PRD-D）。

**DSGN-D Agent-B 三层测试。** 三层严格按第一、第二、第三的顺序跑，前一层过了才跑下一层。
第一层是确定性测试：用 MockGateway（按固定规则回答的假 LLM 接口）跑固定场景，同样输入永远得到同样输出（PRD-F）。
每写一个测试，就只改一个维度再写 2 到 3 个变体，这就是举一反三（PRD-E）。
第二层由真实 LLM 扮演用户，至少用两个不同的模型，同样写变体（PRD-G）。
第三层是质量评判：逐轮分析回复质量、找错误、看多轮对话是否连贯，打 1 到 10 分（PRD-H）。

**DSGN-E Agent-C 仲裁。** A 和 B 对测试失败的根因有分歧时，C 读失败的测试、实现代码和 spec 后裁定（PRD-C）。
优先级是 spec 高于框架约定，框架约定高于代码风格；裁定必须引用 spec 的具体章节。

**DSGN-F Agent-D 质量裁判。** 每次测试通过后都运行，输出带分数和具体建议的质量报告。
没有它的签字，不能算完成（PRD-H）。

**DSGN-G 完成标准。** 四条同时满足才停：todo 清单为空；三层测试都通过；Agent-D 签字；
contrarian review（挑毛病的对抗式审查）报告里没有 CRITICAL 和 HIGH 两个最高级别的问题（PRD-D、PRD-J）。
contrarian review 现在就是 `/spec-review` 的 Quick Scan，5 级算 CRITICAL，4 级算 HIGH（ARD-L）。
闭环规则：修代码时，也要修当初放过这个 bug 的 spec 和 skill（PRD-K）。

**DSGN-H 质量门。** 基本模式：测试描述行为而非实现，只用公开接口，代码对当前测试是最少的，红时不重构。
自动模式：不提前停，测试层按序跑，C 的裁定引用 spec，每个失败都变成跟踪的任务，每次通过后都跑 D。
两种模式都要求每个绿步单独提交；自动模式还要求每 30 分钟自查（ARD-K）。

**DSGN-I 存放位置。** 完整 skill 就在本仓库的 `skills/auto-tdd/SKILL.md`，业务项目只引用它（PRD-L）。

**DSGN-J 逐次提交与自查。** 两种模式每个绿步都提交，提交信息带通过的测试数，自动模式再带层号（PRD-I、ARD-K）。
自动模式每 30 分钟自查做没做完；一段时间没进展，就分析原因并加纠正任务（PRD-D、ARD-K）。

## Testing Decisions

本 skill 没有自动测试或评测集，`skills/auto-tdd/` 下只有 SKILL.md 一个文件。
7bfe010 版曾有 5 个 Given/When/Then 形式的测试场景，合并时被删（ARD-B）。
skill 是否好用，目前只能在真实项目里用一次再人工判断。

## Out of Scope

一行且不改行为的小改动、纯配置或文档改动、会被丢弃的原型，都不用本 skill（SKILL.md 的 When NOT to Use 一节）。

## Further Notes

需求见 [PRD](../prd/auto-tdd-prd.md)，决策见 [decision-history](../decision-history/auto-tdd-decision-history.md)。
skill-factory 整体的设计和 2026-08-02 的合并表，见 [parent design](../../../design/skill-factory-design.md)。
完整的 7bfe010 版（约 350 行）含房贷场景的举一反三示例，可用 `git show 7bfe010` 查看。

## Alternatives Considered

保留 auto-tdd 和 tdd 两个独立 skill：被否决，2026-08-02 合成一个（ARD-A）。
只跑 mock 测试，或一开始就用真实 LLM 跑：被否决，改为三层按序（ARD-G）。
测试全绿就算完成：被否决，改为 Agent-D 签字加 contrarian review 验收（ARD-E、ARD-H）。

## Drawbacks

第二、三层假定被测对象是对话式 LLM agent；普通函数或 API 没有"用户"可扮演，见 QUES-D。
四个角色由同一个 LLM 扮演时，仲裁和质量评判的独立性有限，见 QUES-E。
"不完成就不停"没有写时间或花费上限。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| 第二层每次都调真实 LLM，耗费 token 和钱 | 用户原意是 mock 优先、用户同意才真跑（PRD-F）；SKILL.md 没写这道闸，见 QUES-C |
| 循环不收敛，一直跑下去 | 每 30 分钟自查，没进展就分析原因（ARD-K）；仍没有时间或花费上限 |
| 基本模式的原作者出处丢失 | d98ed8d 删掉了 mattpocock/skills 的 `source` 字段，见 QUES-F |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 要不要恢复"每做一点就提交"（PRD-I）？ | 恢复，每个绿步提交（ARD-K） | cicidi | no |
| QUES-B | 要不要恢复每 30 分钟自查一次（PRD-D）？ | 恢复（ARD-K） | cicidi | no |
| QUES-C | 第二层的真实 LLM 测试，要不要先得到用户同意再跑（PRD-F、PRD-G）？ | 已答：第一次跑前先问用户一次，不同意就跳过并写进报告（ARD-M） | cicidi | no |
| QUES-D | 被测对象不是对话 agent 时，第二、三层怎么做？ | SKILL.md 没有说 | cicidi | no |
| QUES-E | 四个角色要不要用真正的子 agent 分别执行？ | 目前是同一个 LLM 依次扮演（ses_0a0d1bce，2026-07-13） | cicidi | no |
| QUES-F | 基本模式要不要注明来自 mattpocock/skills？ | 当前 SKILL.md 没有出处 | cicidi | no |
| QUES-G | 完成标准里的 contrarian review 现在指哪个 skill？ | `/spec-review` 的 Quick Scan（ARD-L） | cicidi | no |

## Reversibility

所有改动都落在 git 跟踪的 `skills/auto-tdd/SKILL.md`，用 `git revert` 即可撤回。
被删的完整版可从 commit 7bfe010 取回。已安装到 `~/.claude/skills/` 的副本，须重跑 `install.sh` 才同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 auto-tdd 的 design，引用 PRD-A 到 PRD-L |
| 2026-11-24 | 按 ARD-K、ARD-L 改写 DSGN-B、G、J；QUES-A、B、G 已答；QUES-C 不动 |
| 2026-11-24 | QUES-C 已答（ARD-M） |
