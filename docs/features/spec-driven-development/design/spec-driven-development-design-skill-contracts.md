---
feature: spec-driven-development
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-20
---

# Spec-Driven Development — Skill 契约

本篇是 [整体设计 spec-driven-development-design.md](spec-driven-development-design.md) 的一个分篇，只讲两个交付的 skill 各自做什么。术语见 [术语表](spec-driven-development-design.md#glossary)。

## Problem Statement

spec-write 和 spec-review 是仅有的两个交付物（[ARD-BH](../decision-history/spec-driven-development-decision-history.md#ard-bh)）。如果它们的职责只写在各自的 `SKILL.md` 里，改 skill 的人可以随手改掉职责边界，而没人察觉。所以需要一份独立的契约：说清每个 skill 什么时候用、要什么输入、产出什么、不能做什么。

## Solution

本篇是两个 skill 行为的权威来源，`SKILL.md` 只是它的实现。两者不一致时，以本篇为准：先改本篇，再改 `SKILL.md`。具体的写作规则不在本篇重复，以 `SPEC-STANDARD.md` 和 `SPEC-PRESENTATION.md` 为准（[ARD-AJ](../decision-history/spec-driven-development-decision-history.md#ard-aj)）。

## Design

| Skill | 什么时候用 | 输入 | 产出 | 不能做的事 |
|---|---|---|---|---|
| spec-write | 新建或修改 spec 文档 | 用户的意图；两份标准文件 | 改好的文档 | 动笔前没判断「新建哪篇、还是改哪几篇」；一次改动超过 10 行或 200 字符而没有授权（parent design 的 DSGN-A）；悄悄改动上游文档 |
| spec-review | 提交前；或者有人要求审查设计 | 要审的文档目录或改动；两份标准文件 | 一张问题表，每个问题有严重度和修改建议；一次只问用户一个问题 | 直接改文档；改写别人的结论；讨论严重度 1 或 2 的小问题 |
| spec-organize（内部工具，不交付） | 检查或整理路径、格式、INDEX（document-standard 的 DSGN-L） | 文档目录 | 格式问题的修正，或一份问题清单 | 改动文档的内容；当作交付物或入口（[ARD-BH](../decision-history/spec-driven-development-decision-history.md#ard-bh)） |

几项能力落在哪里：

| 能力 | 落点 |
|---|---|
| 子问题归属表（PRD-L） | 每个有子问题的 feature 的 design 里；spec-write 写，spec-review 查 |
| 结论要有依据，查不到写 `UNKNOWN`（PRD-N） | spec-write 写，spec-review 查 |
| 本科生读得懂（PRD-M） | spec-write 写的时候遵守；spec-review 发现读不懂的地方，作为问题报出来；最终由 TST-V 判定 |
| mock MCP 服务器（PRD-O） | `skills/spec-organize/tests/mock-mcp/` |
| 四个例子（PRD-Q） | 写进两个 skill 的 `SKILL.md` 正文，由 TST-S 检查 |

## User Stories

- 作为调用 skill 的人，我想知道每个 skill 什么时候用、要给它什么、它会产出什么。
- 作为审查的人，我希望写和审的职责不重叠，每条标准规则只在一个地方有正式说法。
- 作为维护 skill 的人，我希望修改 `SKILL.md` 不会悄悄改变契约；契约要变，先改本篇。

## Implementation Decisions

- **以谁为准：** 以本篇为准。`SKILL.md` 和本篇冲突时，先改本篇，再改 `SKILL.md`。这条沿用「按关注点分权威」的原则（document-standard 的 DSGN-G）。
- **故意不定义：** 失败处理、版本和迁移、信息来源可信度分级、数据清理（[ARD-AF](../decision-history/spec-driven-development-decision-history.md#ard-af)）。
- **四个例子：** 两个 skill 的正文都要提到盖 shed、北京旅游、数学题、股票（PRD-Q）。它们只是说明用的例子，不是本仓库的 gold。
- **暂时测不了的：** 阶段编排、单次改动大小、不同模型之间的偏差，按 PRD-I 标为 `Unverified`。

## Testing Decisions

- TST-S：两个 skill 的 `SKILL.md` 都包含四个例子。
- TST-O、TST-P：PRD 的每条需求都能在 design 里找到对应；归属、证据、`UNKNOWN` 写得对。
- TST-Q：mock MCP 调用打印出记录，并且没有真实副作用。
- TST-V：每篇文档本科生读得懂。
- 暂时测不了：阶段编排（pipeline design 的 PIPE-A-D、PIPE-A-E、PIPE-H）、单次改动大小（PRD-C）、不同模型之间的偏差（[ARD-AD](../decision-history/spec-driven-development-decision-history.md#ard-ad)）。

## Out of Scope

- 故意不定义的事项，见上面 Implementation Decisions。
- 已有不合规文档的迁移。
- 每个 skill 具体的 prompt 措辞，由 `SKILL.md` 自己决定。

## Further Notes

- 新增 skill 时，先在本篇的表里加一行，再写它的 `SKILL.md`。
- 契约改了，要同步检查 document-standard 和 pipeline 里相关的 DSGN、PIPE 规则。

## Alternatives Considered

- **合成一个 skill：** 放弃。写和审必须分开，自己审自己写的东西看不出问题（[ARD-AJ](../decision-history/spec-driven-development-decision-history.md#ard-aj)）。
- **把契约直接写进 `SKILL.md`：** 放弃。那样 `SKILL.md` 就成了权威，契约没有独立的位置，改 skill 时也没有东西能拦住越界的修改。

## Drawbacks

- 多了一层：改 skill 的行为，要同时改本篇和 `SKILL.md`。

## Risks and Mitigations

- **`SKILL.md` 和本篇慢慢不一致：** 冲突时以本篇为准；spec-review 审 skill 时对照本篇。

## Open Questions

本 feature 的未决问题统一记在 [parent design 的 Open Questions](spec-driven-development-design.md#open-questions)。和本篇有关的是 QUES-A（交付的 skill 怎么带上标准文件）和 QUES-C（新工具要不要进契约表）。

## Reversibility

- 契约修改可以撤回：改回本篇和 `SKILL.md` 即可，没有数据要迁移。
- 新增 skill 只要在表里加一行；去掉一个 skill，要同一批修改 pipeline design 和 test-plan。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-04 | Initial creation; four skill contracts, shared capabilities, testing pointers |
| 2026-11-07 | 契约改为 spec-write 与 spec-review；标准两份文档（ARD-AJ） |
| 2026-11-07 | part 链回 spec-driven-development-design.md（ARD-AV） |
| 2026-11-20 | 全文改写为完整句子；Problem Statement 写明为什么需要契约；Alternatives 不再引用已推翻的 ARD-AB；Open Questions 链到 parent 的唯一问题清单；加入可读性的落点与 TST-V（ARD-BK、ARD-BO） |
| 2026-11-20 | 第 1 轮审查后：契约表加 spec-organize 一行，写明它是内部工具、不交付；PIPE 子条款编号改为字母（ARD-BR） |
