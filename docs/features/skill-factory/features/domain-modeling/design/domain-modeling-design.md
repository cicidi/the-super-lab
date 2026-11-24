---
feature: domain-modeling
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# domain-modeling — 领域模型与术语表

本篇说明 `domain-modeling` 这个 skill 现在怎么工作。
源文件：`skills/domain-modeling/` 下的 SKILL.md、CONTEXT-FORMAT.md、ADR-FORMAT.md。
commit f6255af 导入，93d4a4a 移到现在的位置，之后内容没有改过。

## Problem Statement

设计讨论里，同一个词常被当成不同的意思，例如 account 可能指客户，也可能指登录用户（SKILL.md 的例子）。
决定做了，几个月后没人记得为什么。
wayfinder 定方向时，需要一个能追问并记录的访谈步骤（PRD-A）。

## Solution

一个主动的 skill：讨论中追问术语，当场写进 `CONTEXT.md`；只在三个条件都满足时提议写 ADR（PRD-C）。
它很少单独使用，通常由 wayfinder 或 grill-with-docs 调起（PRD-D）。

## User Stories

- 作为开发者，我说出一个含糊的词时，agent 提出一个更准的叫法让我选。
- 作为开发者，我描述的规则和代码不一致时，agent 指出来，问哪个对。
- 作为后来的读者，我在 `CONTEXT.md` 里查到术语，在 ADR 里查到关键决定的原因。

## Implementation Decisions

全部行为写在 SKILL.md 里，没有脚本。
两个模板文件放在同一目录，SKILL.md 用相对链接引用它们（PRD-E）。
正文与原版一致，本仓库只改了 frontmatter（PRD-C，decision-history 的 ARD-B）。

## Design

**DSGN-A 主动，不是只读。** 本 skill 用于改动领域模型的时候：挑战术语、编边界场景、当场写下结论。
只是读 `CONTEXT.md` 取词汇，不需要调用它（PRD-C）。

**DSGN-B 文件结构。** context（上下文）指一块有自己术语的业务领域。大多数仓库只有一个。
单个 context 时，根目录一个 `CONTEXT.md`，决策放 `docs/adr/`（PRD-C）。
根目录有 `CONTEXT-MAP.md` 时表示有多个 context，它列出每个 context 的位置和相互关系。
文件懒创建：第一个术语定下来才建 `CONTEXT.md`，第一个 ADR 需要时才建 `docs/adr/`。

**DSGN-C 对照术语表挑战。** 用户用的词和 `CONTEXT.md` 的定义冲突时，立刻指出，问到底是哪个意思（PRD-C）。

**DSGN-D 收紧含糊的词。** 用户用了含糊或一词多义的说法时，提出一个精确的标准叫法（PRD-C）。

**DSGN-E 用具体场景压测。** 讨论概念之间的关系时，agent 自己编边界场景，逼用户说清边界在哪里（PRD-C）。

**DSGN-F 与代码对照。** 用户说某件事怎么运作时，查代码是否一致；不一致就当面指出（PRD-C）。

**DSGN-G 当场更新 CONTEXT.md。** 术语一定下来就写，不攒着批量写（PRD-C）。
格式按 CONTEXT-FORMAT.md：每个术语一到两句定义，写它是什么；同义词列在 `_Avoid_` 下（PRD-E）。
只收本项目特有的概念，不收超时、错误类型这类通用编程概念；文件里不放实现细节。

**DSGN-H ADR 少而精。** 三条同时成立才提议写 ADR（PRD-C）。
三条是：难以撤回；没有上下文会让后来的人意外；确实在几个方案之间做了取舍。
格式按 ADR-FORMAT.md：一段话即可；在 `docs/adr/` 里找最大编号加一，文件名形如 `0001-slug.md`（PRD-E）。

**DSGN-I 出处与部署。** frontmatter 的 `source_author: mattpocock` 和 `source_url` 指向原文（PRD-B）。
`compatibility: claude-code,opencode` 表示两种工具都能用；已安装的副本在 `~/.claude/skills/domain-modeling/`（PRD-F）。

**DSGN-J 谁来调用。** wayfinder 的 interview 接口默认是 grill-with-docs 加 domain-modeling，安装时可换掉（PRD-A、PRD-D）。
wayfinder 在定目的地和处理 grilling 类 brief 时调用它。
grill-with-docs 的正文只有一句：用 domain-modeling 跑一次 grilling。
用户也可以直接输入 `/domain-modeling`，例如 2026-10-09 在另一个项目里用过一次（会话 26017f7a）。

## Testing Decisions

本 skill 没有自动测试或评测集，目录下只有三个 markdown 文件。
效果只能在真实的设计讨论里用一次，再人工看 `CONTEXT.md` 和 ADR 写得对不对。

## Out of Scope

只读术语、不改动领域模型的场合不用本 skill（SKILL.md 的 `when_not_to_use`）。
`CONTEXT.md` 不是 spec，也不是草稿本，不放实现决定（SKILL.md 的 Update CONTEXT.md inline 一节）。

## Further Notes

需求见 [PRD](../prd/domain-modeling-prd.md)，决策见 [decision-history](../decision-history/domain-modeling-decision-history.md)。
docs/book/imported-skills.md 把导入日期写成 2026-07-25，但 commit f6255af 是 2026-08-02，以 commit 为准。
本仓库的 spec 标准里，`CONTEXT.md` 不加 frontmatter，归本 skill 管（skills/spec-organize/SKILL.md 的豁免表）。
SDD 的 ARD-C 决定把标准细节放在 skill 目录的其他文件里，引的先例就是本 skill 的两个模板。

## Alternatives Considered

自己写一个术语表 skill：被否决，直接导入原版（ARD-D）。
像 wayfinder 那样改写正文：被否决，只改 frontmatter（ARD-B）。
在 wayfinder 里写死 skill 名：被否决，改为可替换的接口（ARD-C）。

## Drawbacks

是否调用全靠 agent 自己判断。用户当时就说"the passive way is not guaranteed"（d8d2da7f，12:06）。
用户还指出不同模型调用 skill 的能力不同（同一会话 12:07），见 QUES-B。
ADR 的写入位置 `docs/adr/` 与本仓库的 spec 标准不一致，见 QUES-A。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| 在本仓库按原样写 `docs/adr/`，与 spec 标准冲突 | spec-organize 把 `docs/adr/` 当作旧布局，要求并入 decision-history；SKILL.md 没写，见 QUES-A |
| grill-with-docs 和 wayfinder 引用的 `/grilling` 找不到 | 目前没有缓解，见 QUES-C |
| 上游原版更新后，本地副本落后 | 没有同步机制；`source_url` 至少能找到原文，见 QUES-D |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 在本仓库用时，ADR 写到 `docs/adr/` 还是 feature 的 decision-history？ | SKILL.md 写 `docs/adr/`；spec-organize 要求并入 decision-history | cicidi | no |
| QUES-B | 被动触发不可靠，要不要在 wayfinder 之外加显式的触发点？ | 只靠 description 和 triggers 字段 | cicidi | no |
| QUES-C | `/grilling` 指哪个 skill？ | `skills/` 和 `~/.claude/skills/` 下都没有 | cicidi | no |
| QUES-D | 要不要跟进上游更新，补上 META.yaml？ | parent design 要求导入的 skill 带 upstream_commit，本目录没有 | cicidi | no |
| QUES-E | `CONTEXT.md` 每个项目一份，还是集中一份？ | 用户问过（d8d2da7f，10:24）；SKILL.md 是每个仓库一份；用户的结论 UNKNOWN | cicidi | no |

## Reversibility

所有改动都落在 git 跟踪的 `skills/domain-modeling/`，用 `git revert` 即可撤回。
它在别的项目写下的 `CONTEXT.md` 和 ADR 属于那些项目，要在那边撤回。
已安装到 `~/.claude/skills/` 的副本，须重跑 `install.sh` 才同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 domain-modeling 的 design，引用 PRD-A 到 PRD-F |
