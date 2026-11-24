---
feature: to-spec
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# to-spec — 把对话整理成 spec

本篇说明 `to-spec` 这个 skill 现在怎么工作。
源文件：`skills/to-spec/SKILL.md`（commit 212aab5 导入，f67df5b 最后一次修改）。

## Problem Statement

wayfinder 把大任务拆成多个决策逐个定下来后，结论散在各个 issue 和对话里（PRD-A）。
下游的 to-tickets 拆工单时，需要一份完整、可链接的 spec 作为依据（PRD-D）。

## Solution

一个只整理、不访谈的 skill：读对话和代码库，按固定模板写 spec，发布到 issue tracker（PRD-C）。
模板每一节标了内容级别，篇幅超了就按级别删减（PRD-F）。

## User Stories

- 作为开发者，wayfinder 的地图走完后，我调用 to-spec，得到一份 spec 和一个对应的 issue。
- 作为开发者，我只在测试接缝这一件事上被问一次，其余由 agent 自己整理。

## Implementation Decisions

`skills/to-spec/` 下只有一个 SKILL.md，没有脚本或其他文件；整个 skill 就是给 agent 读的说明。
"不访谈"和"确认测试接缝"并存：接缝是唯一的提问点（SKILL.md Process 第 2 步）。
frontmatter 保留了原作者的 MIT 许可（`license: MIT`）。

## Design

**DSGN-A 触发与出处。** 对话已经足够清楚、决定需要记成 PRD 时触发；对话还含糊时，让用户改用 grill-with-docs（PRD-C）。
frontmatter 的 `source_author: mattpocock` 和 `source_url` 注明原作者和原文地址（PRD-B）。

**DSGN-B 选 tracker。** tracker 的配置来自项目的 init 流程；没有配置时，用本地 markdown tracker（PRD-D）。

**DSGN-C 先读代码库。** 用项目术语表（glossary）里的词写 spec，并遵守相关的 ADR（architecture decision record，架构决策记录）（PRD-C）。

**DSGN-D 测试接缝。** 接缝（seam）指测试从外部接入、观察行为的位置。优先用已有的接缝，选最高的一层（PRD-C）。
接缝越少越好，理想是一个。画好后和用户确认，这是全程唯一一次提问。

**DSGN-E 按仓库分两路。** SDD 仓库（有 `docs/features/` 且装了 spec-write）：把整理结果和接缝交给 `/spec-write`，
由它决定写哪几篇 prd、design；再发一个链接这些文档的 issue（ARD-F、PRD-D）。
非 SDD 仓库按模板写 PRD 并发布。模板有八节：Problem Statement、Solution、User Stories、Implementation Decisions，
Alternatives Considered（可选）、Testing Decisions、Out of Scope、Further Notes。
User Stories 要写成很长的编号列表；Testing Decisions 要求只测外部行为。
写完发布到 tracker，打 `ready-for-agent` 标签，表示 agent 可以直接认领，不用再分诊（PRD-D）。

**DSGN-F 内容级别和篇幅。** 每节标了级别：L1 决定性，从不删；L2 是理由；L3 是被否决的方案；L4 是参考材料（PRD-F）。
超长时先删 L4，再删 L3，再压缩 L2。全文不超过 1000 行；超出就按 bounded context（业务边界）拆分（PRD-G）。

**DSGN-G 不写进 spec 的内容。** 不写文件路径和代码片段，它们很快会过时；类结构、私有方法、内部算法属于代码（PRD-F）。
例外：原型产出的状态机、schema 这类片段比文字更准时，可摘关键部分并注明来自原型。
重复别的文档里的事实，只放链接（PRD-H）。

**DSGN-H 依赖的文档标准。** SDD 仓库里，放在哪、frontmatter、必需章节由 spec-write 按 `skills/spec-organize/SPEC-STANDARD.md` 定（PRD-F）。
内容取舍看 `skills/spec-organize/` 下的 `AUTHORITY-BY-CONCERN.md` 和 `CONTENT-PRIORITY.md`（QUES-A）。

**DSGN-I 在流水线里的位置。** wayfinder 写的顺序是 wayfinder、to-spec、spec-review、to-tickets、auto-tdd（PRD-A）。
spec-review 是 to-spec 之后、to-tickets 之前的关口，必须通过才能拆工单；它写在 wayfinder 里，不在本 skill 里（PRD-E）。

## Testing Decisions

本 skill 没有自动测试或评测集，`skills/to-spec/` 下只有 SKILL.md 一个文件。
downstream-delivery 的 test-plan 列了 TST-A：to-spec 的产出要通过 spec-organize 的检查；没找到运行记录，见 QUES-D。

## Out of Scope

不访谈用户补齐信息（那是 grill-with-docs 的事）；不拆工单（to-tickets）；不写代码（auto-tdd 或 implement）。

## Further Notes

需求见 [PRD](../prd/to-spec-prd.md)，决策见 [decision-history](../decision-history/to-spec-decision-history.md)。
和 SDD 的关系：SDD 的 design 必需章节共 13 节，其中八节来自 to-spec 的模板（`skills/spec-organize/SKILL.md` 的 Sources 一节）。
SDD 指 spec-driven-development，即从 spec 驱动开发；它定下写 spec 的入口只有 spec-write，审 spec 用 spec-review。
出处是 SDD decision-history 的 ARD-AJ（2026-11-07）和 ARD-BX（2026-11-20）；那份记录没有提到 to-spec。
导入前用户问过 spec 为什么记作 PRD，"从头到位我没有看到prd 讨论"（d8d2da7f，17:08）；当时的回答没有保留。

## Alternatives Considered

像 wayfinder 那样改写正文：没有采用，只加 frontmatter 和出处（ARD-D）。
spec 写完直接拆工单：被否决，改为先过 spec-review 关口（ARD-B）。
模板不分级、篇幅不设上限：被否决，2026-09-25 改为 L1 到 L4 分级加 1000 行上限（ARD-A）。

## Drawbacks

不访谈意味着对话里漏掉的内容会直接漏进 spec，只能靠后面的 spec-review 补。
模板的八节和现行标准的 prd（6 节）、design（13 节）都对不上，所以 SDD 仓库里不用模板，改交 spec-write（ARD-F）。
spec 发到 tracker，和写进 `docs/features/` 是两条路；同一份 spec 可能在两处各存一份。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| 引用的 `doc-organize/` 文件已不存在，agent 读不到标准 | 已改指 `skills/spec-organize/`（QUES-A） |
| to-spec 和 spec-write 都写 spec，规则可能分叉 | 写明两者分工，见 QUES-C |
| 没配置 tracker 时写到本地 markdown，但位置没写 | 见 QUES-E |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | Skill Dependencies 要不要改指 spec-organize（PRD-F）？ | 是，已改指 `skills/spec-organize/` 下的文件 | cicidi | no |
| QUES-B | 产出应是哪种文档类型？ | SDD 仓库交 spec-write 定 prd、design；非 SDD 仓库是 tracker 上的 PRD（ARD-F） | cicidi | no |
| QUES-C | to-spec 和 spec-write 怎么分工？ | SDD 只把 spec-write 列为写 spec 的入口（ARD-AJ、ARD-BX），没提 to-spec | cicidi | no |
| QUES-D | downstream-delivery 的 TST-A 跑过吗？ | 没找到运行记录 | cicidi | no |
| QUES-E | 本地 markdown tracker 写到哪个目录（PRD-D）？ | SKILL.md 没写 | cicidi | no |
| QUES-F | 关口用 doc-review 还是 spec-review（PRD-E）？ | spec-review。688cace（2026-11-24）已把 wayfinder 里的 doc-review 改成 spec-review | cicidi | no |

## Reversibility

所有改动都落在 git 跟踪的 `skills/to-spec/SKILL.md`，用 `git revert` 即可撤回；导入时的原样可从 commit 212aab5 取回。
已安装到 `~/.claude/skills/` 的副本，须重跑 `install.sh` 才同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 to-spec 的 design，引用 PRD-A 到 PRD-H |
| 2026-11-24 | QUES-F 有答案：wayfinder 已在 688cace 改用 spec-review |
| 2026-11-24 | DSGN-E、DSGN-H 改为按仓库分两路并修路径（ARD-F），QUES-A、QUES-B 已答 |
| 2026-11-24 | 正文里的 doc-review 改为 spec-review，跟上 688cace |
