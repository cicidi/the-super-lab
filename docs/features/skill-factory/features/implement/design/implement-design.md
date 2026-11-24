---
feature: implement
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# implement — 按 spec 和 ticket 实现

本篇说明 `implement` 这个 skill 现在怎么工作。
源文件：`skills/implement/SKILL.md`（commit 12c7dce 导入，f67df5b 加了 Skill Dependencies 一节）。

## Problem Statement

wayfinder、to-spec、to-tickets 产出的是决策、spec 和工单，还缺一步把它们变成经过测试和审查的代码（PRD-A）。
写代码时，spec 和代码还容易悄悄走偏：改了行为却不改 spec，或者看到不一致就随手改掉一边（PRD-F、PRD-G）。

## Solution

一份 SKILL.md，正文沿用原作者的五句话（PRD-C），TDD 和审查两句改指本仓库的 skill（ARD-F、ARD-G）：照 spec 或 ticket 实现，用 auto-tdd 做 TDD，勤跑类型检查和单个测试，最后跑全量，审查后提交。
后加的 Skill Dependencies 一节管动手前的分类和冲突处理（PRD-F、PRD-G）。

## User Stories

- 作为开发者，ticket 定好后，我说"implement tickets"，agent 就按工单写代码、跑测试、审查、提交。
- 作为维护者，agent 发现代码和 spec 不一致时，我想先看到两边的证据，再由我决定。

## Implementation Decisions

整个 skill 只有 `skills/implement/` 下的一个 SKILL.md，没有脚本、模板或附属文件。
触发词是 implement、build、implement tickets；`compatibility` 写的是 claude-code 和 opencode。
正文的执行步骤全部委托给别的 skill：TDD 交给 `/auto-tdd`，审查先交给 `/matt-code-review`；分类规则交给 spec-organize 的两份参考文件。
2026-11-24 改过仓库版后，须重跑 `install.sh`，`~/.claude/skills/implement/` 才同步。

## Design

**DSGN-A 什么时候用。** spec 和 ticket 已经备好，验收标准清楚，测试接入点也事先商量好（PRD-A）。
spec 还含糊时先用 wayfinder 或 grill-with-docs；没有 ticket 时不用。

**DSGN-B 动手前先分类。** 先判断这次改动是行为改动还是只改实现（PRD-F）。
行为改动指外部能观察到的行为变了，要同时改 spec；重构、改名、内部优化、换框架都不用改 spec。
SKILL.md 指向 `skills/spec-organize/` 下的 `CONTENT-PRIORITY.md` 和 `AUTHORITY-BY-CONCERN.md`（QUES-A）。
要改 spec 时，用 `/spec-write` 去改。

**DSGN-C 在约定的接入点做 TDD。** TDD 指先写一个会失败的测试，再写刚好让它通过的代码（PRD-C）。
seam（接入点）指测试能插进去观察行为的位置，例如一个公开函数或一个接口；SKILL.md 要求只在事先商量好的接入点上做。
这一步转调 `/auto-tdd`，由 auto-tdd 问用户用基本模式还是自动模式（ARD-F）。
原版的 `/tdd` 已在 commit 6086424 并入 auto-tdd。

**DSGN-D 测试节奏。** 类型检查和单个测试文件要经常跑；全量测试只在最后跑一次（PRD-C）。
这样每一步的反馈快，又不在中途反复付出全量测试的时间。

**DSGN-E 做完先审查。** 全部完成后先用 `/matt-code-review` 审查这次的改动（PRD-E、ARD-G）。
没装 matt-code-review 时，退回通用的 `/code-review`。

**DSGN-F 提交到当前分支。** 审查之后，把工作提交到当前所在的分支，不另开分支（PRD-C）。

**DSGN-G 冲突先报告。** 代码和 spec 说法不一致时，两边都不悄悄改（PRD-G）。
agent 报告冲突，列出两边的证据，然后问用户以哪边为准。

**DSGN-H 和 auto-tdd 的关系。** wayfinder 的流水线是 wayfinder、to-spec、doc-review、to-tickets、auto-tdd，build 一步用的是 auto-tdd（PRD-D）。
implement 保留，但 TDD 一步转调 auto-tdd，所以两条路最终都由 auto-tdd 写代码（ARD-F）。

**DSGN-I 出处。** frontmatter 的 `source_author` 是 mattpocock，`source_url` 指向原仓库的 engineering/implement/SKILL.md（PRD-B）。
README 的 skill 表用 🔗 标出它来自 mattpocock/skills。

## Testing Decisions

本 skill 没有自动测试或评测集，`skills/implement/` 下只有 SKILL.md 一个文件。
是否好用，目前只能在真实项目里跑一次再人工判断；没找到实际调用过它的会话记录。

## Out of Scope

spec 还含糊或决定未做完时不用本 skill；没有 ticket 可依据时也不用（SKILL.md 的 `when_not_to_use`）。
本 skill 不写 spec、不拆 ticket，这些分别是 to-spec 和 to-tickets 的事。

## Further Notes

需求见 [PRD](../prd/implement-prd.md)，决策见 [decision-history](../decision-history/implement-decision-history.md)。
用户指定的替代实现见 [auto-tdd design](../../auto-tdd/design/auto-tdd-design.md)；skill-factory 整体见 [parent design](../../../design/skill-factory-design.md)。

## Alternatives Considered

改写正文、换成自己的步骤：没有采用，导入时原样保留（ARD-C）。
流水线的 build 一步用 implement：被否决，用户指定 auto-tdd（ARD-B）。
代码是唯一事实来源、冲突时直接改 spec：被否决，改为按关注点分权威、冲突先问（ARD-A）。

## Drawbacks

正文很短，几乎所有动作都委托给别的 skill；被委托的 skill 改名时，这里也要跟着改。
implement 的描述是按 spec 实现、用 TDD；auto-tdd 的描述是用 TDD 开发功能。两者范围重叠，agent 可能选错。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| 分类规则的两个路径失效，agent 读不到规则就跳过分类 | 已改成 `skills/spec-organize/` 下的现有路径（QUES-A） |
| 调用 `/tdd` 找不到 skill，TDD 一步被省掉 | 已改为转调 auto-tdd（ARD-F） |
| 审查用的不是用户首选的 `matt-code-review` | 已写明先用 matt-code-review，没有再用通用的（ARD-G） |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | Skill Dependencies 里的 `doc-organize/` 路径要改成 `spec-organize/` 吗（PRD-F）？ | 已改为 `skills/spec-organize/` 下的路径；改 spec 用 spec-write | cicidi | no |
| QUES-B | `/tdd` 要改成 auto-tdd 吗（PRD-C、PRD-D）？ | 是，已改为 `/auto-tdd`（ARD-F） | cicidi | no |
| QUES-C | `/code-review` 指哪一个（PRD-E）？ | 先用 matt-code-review，没装再用通用的 `/code-review`（ARD-G） | cicidi | no |
| QUES-D | 用户说替代是 auto-tdd 后，implement 该删除、改成转调 auto-tdd，还是加一个可替换的 build 接口（PRD-D）？ | 改成转调 auto-tdd，implement 保留（ARD-F） | cicidi | no |

## Reversibility

所有改动都落在 git 跟踪的 `skills/implement/SKILL.md`，用 `git revert` 即可撤回；原始导入版可从 commit 12c7dce 取回。
已安装到 `~/.claude/skills/` 的副本，须重跑 `install.sh` 才同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 implement 的 design，引用 PRD-A 到 PRD-G |
| 2026-11-24 | 转调 auto-tdd、先用 matt-code-review、修路径（ARD-F、ARD-G），QUES-A 到 D 已答 |
