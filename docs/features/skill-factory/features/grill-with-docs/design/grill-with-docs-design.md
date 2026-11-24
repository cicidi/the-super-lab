---
feature: grill-with-docs
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# grill-with-docs — 带文档的拷问式访谈

本篇说明 `grill-with-docs` 这个 skill 现在怎么工作。
源文件：`skills/grill-with-docs/SKILL.md`（commit 6835420 导入，93d4a4a 移到现在的位置）。

## Problem Statement

计划或设计还含糊时，需要有人逐个追问，并把定下的术语和决策当场记下来（SKILL.md 的 `when_to_use`）。
wayfinder 的 interview（访谈）接口需要一个默认实现来做这件事（PRD-A、PRD-D）。

## Solution

一个只有一句正文的组合 skill：跑一次 `/grilling` 访谈，同时用 `/domain-modeling` 记录术语和决策（PRD-C）。
真正的追问和记录逻辑都在这两个被调用的 skill 里，本 skill 只负责把它们串起来。

## User Stories

- 作为开发者，我说"grill with docs"或"sharpen plan"，agent 就开始逐个追问我的计划。
- 作为用 wayfinder 的开发者，定目的地时自动用上这套访谈，不用另外配置。

## Implementation Decisions

正文按上游原样保留，只改 frontmatter（decision-history 的 ARD-D）。
`skills/grill-with-docs/` 下只有 SKILL.md 一个文件，没有模板或脚本。
模板（`CONTEXT-FORMAT.md`、`ADR-FORMAT.md`）放在被调用的 `skills/domain-modeling/` 里。

## Design

**DSGN-A 何时触发。** frontmatter 列了四个触发词：grill with docs、sharpen plan、grilling session、domain interview（PRD-A）。
适用场景是计划含糊、需要把术语写进 `CONTEXT.md` 和 ADR；需求已清楚或只要快速回答时不用。

**DSGN-B 正文只有一句。** 原文是"Run a `/grilling` session, using the `/domain-modeling` skill."（PRD-C）。
agent 读到后，应当用 `/grilling` 的方式追问，再按 `/domain-modeling` 的规则把结论写进文档。
文中没有步骤、轮数或结束条件，这些都交给两个被调用的 skill。

**DSGN-C `/grilling` 的来源。** `skills/grilling/` 是 2026-11-24 补导的上游 fa460cb 版（ARD-G）。
它要求一次问一个问题，每题附推荐答案，事实自己查，决定交给用户（PRD-A）。
wayfinder 对 grilling 的描述是"one question at a time"、必须有真人回答（skills/wayfinder/SKILL.md 的 Brief Types）。
上游 a4b2009（2026-07-16）起改为一轮问多个问题，与 wayfinder 不符，所以没取 HEAD（ARD-G）。

**DSGN-D 由 domain-modeling 负责记录。** `skills/domain-modeling/` 存在，负责收紧术语、写 `CONTEXT.md` 和 `docs/adr/`（PRD-A）。
它的行为见 [domain-modeling design](../../domain-modeling/design/domain-modeling-design.md)。

**DSGN-E 注明出处。** frontmatter 写了 `source_author: mattpocock`、`source_url`（上游原文链接）和 `license: MIT`（PRD-B）。

**DSGN-F 可替换的接口实现。** wayfinder 的 interview 接口默认是 grill-with-docs 加 domain-modeling（PRD-D）。
接口表的替换一栏写的是"(ask on install)"，即安装时问用户；这一步是否真的实现，本次没有核实，见 QUES-D。

**DSGN-G 其他调用方。** `skills/to-spec/` 在对话仍含糊时，让用户改用 grill-with-docs（其 `when_not_to_use`）。
SDD 流程在 Map 阶段把它列为可选的压力测试（skills/spec-pipeline/INTEGRATIONS.md；decision-history 的 ARD-A）。

**DSGN-H 安装目标。** `compatibility` 写的是 `claude-code,opencode`（PRD-E）。
`~/.coworker/install-manifest.json` 记录它装到了 `~/.claude/skills/`、OpenCode 和 Cursor 三处。
`~/.claude/skills/grill-with-docs/SKILL.md` 与仓库版本逐字相同（2026-11-24 比对）。

**DSGN-I 与上游的差异。** 上游现在的正文是"Call the Skill tool twice, for "grilling" and "domain-modeling"."（2026-11-24 查看）。
上游 frontmatter 还有 `disable-model-invocation: true`，即只能由用户手动调用；本仓库版本没有这一项（PRD-C）。
这两处差异是导入后上游改的，还是导入时就不同，属于 UNKNOWN，见 QUES-B。

## Testing Decisions

本 skill 没有自动测试。导入时只查 frontmatter 格式、出处字段、正文原样和能否部署（wayfinder-import-spec 的 9.2 节，commit 0f3ede7）。
SDD 评测矩阵 TST-J 有 grill-docs 一行，用来比较加不加本 skill 的效果；只报分数，不设门槛（TST-J-MATRIX.md）。
没有测试会发现 `/grilling` 缺失这类断链。

## Out of Scope

需求已经很清楚、或用户只想要一个快速回答时，不用本 skill（SKILL.md 的 `when_not_to_use`）。
改写原版正文不在范围内（PRD-C）。

## Further Notes

需求见 [PRD](../prd/grill-with-docs-prd.md)，决策见 [decision-history](../decision-history/grill-with-docs-decision-history.md)。
domain-modeling（其 QUES-C）和 wayfinder 同样调用 `/grilling`，三者都随 ARD-G 一起解决。

## Alternatives Considered

自己从头写一个访谈 skill：被否决，直接导入上游版本（ARD-F）。
在 wayfinder 里写死访谈 skill 的名字：被否决，改为可替换的接口（ARD-E）。
导入上游 HEAD 版 `/grilling`：被否决，它一轮问多个问题；改取 fa460cb 版（ARD-G）。

## Drawbacks

正文只有一句，行为完全取决于两个被调用的 skill；缺一个，本 skill 就只剩一个名字（DSGN-C）。
没有结束条件，访谈何时停全凭 agent 和用户判断。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| `/grilling` 曾找不到，访谈没有固定规则 | 2026-11-24 已补导 fa460cb 版（ARD-G） |
| 与上游渐行渐远，agent 可自行触发而上游不允许 | 目前没有同步机制，见 QUES-B |
| docs/book/imported-skills.md 把导入日期写成 2026-07-25 | 以 commit 6835420（2026-08-02）为准，见 QUES-C |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | `/grilling` 指哪个 skill？要导入上游的 grilling 吗？ | 已导入：`skills/grilling/` 取自上游 fa460cb（ARD-G） | cicidi | no |
| QUES-B | 要不要按上游更新正文，并加 `disable-model-invocation: true`？ | 未同步；本仓库版本允许 agent 自行触发 | cicidi | no |
| QUES-C | 要不要把 docs/book/imported-skills.md 的导入日期改成 2026-08-02？ | 该文写 2026-07-25，git 是 2026-08-02 | cicidi | no |
| QUES-D | 安装时真的会问用户替换 interview 接口吗？ | wayfinder 接口表写"(ask on install)"，实现未核实 | cicidi | no |

## Reversibility

所有改动都落在 git 跟踪的 `skills/grill-with-docs/SKILL.md`，用 `git revert` 即可撤回。
已安装到 `~/.claude/skills/` 等处的副本，须重跑安装脚本才同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 grill-with-docs 的 design，引用 PRD-A 到 PRD-E |
| 2026-11-24 | `/grilling` 已补导（ARD-G）：改写 DSGN-C，QUES-A 有答案 |
