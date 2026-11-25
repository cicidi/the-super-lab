---
feature: to-spec
type: prd
state: draft
health: stale
owner: cicidi
last_verified: 2026-11-24
---

# to-spec — 需求

本篇从过去的对话和提交记录里，整理用户对 `to-spec` 这个 skill 的需求。
本 skill 已于 2026-11-24 移除（ARD-G），需求由 [spec-ingest PRD](../../spec-ingest/prd/spec-ingest-prd.md) 接手。
实现见 [design](../design/to-spec-design.md)。
决策的来由见 [decision-history](../decision-history/to-spec-decision-history.md)。
Claude Code 会话原文没有保留；下文引用 `~/.claude/history.jsonl` 里的会话 id 前缀和时间。

## Overview

spec 是写给开发者的需求和设计文档，PRD（product requirements document，产品需求文档）是它的另一个叫法。
`to-spec` 把当前对话里已经谈清楚的内容整理成一份 spec，发布到项目的 issue tracker。
issue tracker 指问题跟踪系统，例如 GitHub Issues 或 Jira。它不访谈用户，只做整理。
这个 skill 来自 Matt Pocock 的 mattpocock/skills，于 2026-08-02 导入（commit 212aab5）。
导入发生在会话 d8d2da7f：用户当天先学习 wayfinder，问"what does to spec to"，随后说"continue importing to-spec"（18:33、18:34）。
wayfinder 是另一个导入的 skill，把大任务拆成一串决策逐个定下来；to-spec 接在它后面。

## Goals and Success Metrics

目标一：wayfinder 的决策走完后，把结论写成一份 spec，交给下游拆成工单（d8d2da7f，17:55；commit 7c11a7b）。
目标二：沿用原作者的做法，并注明出处（同一会话 17:22 第 1 条、17:27 第 4 条）。
目标三：spec 只留决定性内容，篇幅受控（会话 631b8662，2026-09-25 09:26）。
成功指标：UNKNOWN。对话和提交里都没有可量化的指标。

## User Stories

- 作为开发者，讨论已经有结论时，我想让 agent 直接把它整理成 spec，不再问一遍。
- 作为开发者，我想让 spec 作为一个 issue 发出去，后面的工单都能链到它。
- 作为维护者，spec 太长时，我想知道先删哪些内容，哪些绝不能删。
- 作为 skill 仓库的维护者，我想看出这个 skill 来自谁，原文在哪里。

## Functional Requirements

**PRD-A 作为 wayfinder 流水线的一环导入。** wayfinder 的导入规格先把 to-spec 列为"future imports"（commit 0f3ede7，18:21）。
13 分钟后用户说"continue importing to-spec"，commit 212aab5 在 18:34 导入（d8d2da7f）。

**PRD-B 注明原作者。** 用户要求的第 1 条是"import 这个skill 著名作者"，即注明作者（d8d2da7f，17:22）。
commit 212aab5 在 frontmatter 里写了 `source_author` 和 `source_url`。frontmatter 是 SKILL.md 开头的元数据块。

**PRD-C 沿用原版做法。** 用户说接口没有替换时"就用matt 的ksill"（d8d2da7f，17:27 第 4 条）。
原版做法是：只整理、不访谈；先读代码库，再和用户确认测试接缝，然后按模板写 spec 并发布。
这几步是原作者的做法，用户没有逐条提出过。

**PRD-D spec 本身也是一个 issue。** 用户说"spec 本身也得有一个ticket"（d8d2da7f，17:55）。
ticket 在这里指 issue tracker 上的一条工单。wayfinder 据此写明：to-spec 为 spec 建一个 issue（commit 7c11a7b）。

**PRD-E 发布 spec 后、拆工单前要审查文档。** 用户说"在to ticket 以前，还得有一个 doc-review 的过程"，审查所有文档（d8d2da7f，17:55）。
这道关口写在 wayfinder 里（commit 7c11a7b），to-spec 的 SKILL.md 本身没有这一步。

**PRD-F 内容分四级，删减有顺序。** 用户定的四级：一级是决定性内容，没有它实现会出错、方向会偏，不能删（631b8662，09:26）。
二级解释为什么这么做；三级说明为什么不选别的做法；四级是参考、调研和例子（同一条）。
用户要求优先删四级和三级。commit f67df5b 给 to-spec 模板的每一节标了级别（L1 到 L4）。

**PRD-G 篇幅不超过 1000 行。** 用户要求文档小于 1000 行，超出就拆分（631b8662，09:26）。
to-spec 模板开头的注释写了这条上限（commit f67df5b）。

**PRD-H 重复的事实只放链接。** 用户说同一事实在别的文档出现过，第二处只放一个 link，也算四级（631b8662，09:37）。
模板的 Further Notes 一节写了这条（commit f67df5b）。

## Out of Scope

对话还含糊、需要先访谈补齐时不用本 skill，改用 grill-with-docs（SKILL.md 的 `when_not_to_use` 字段，commit 212aab5）。
拆工单和写代码也不归本 skill，分别是 to-tickets 和 auto-tdd 的事（commit 7c11a7b 的流水线图）。
用户划这条范围的原话没有找到，属于 UNKNOWN。

## Resources Needed

项目要配置好 issue tracker；没有配置时，默认写到本地 markdown（PRD-C、PRD-D）。
还需要 SKILL.md 引用的文档标准文件（PRD-F），现在在 `skills/spec-organize/` 下；SDD 仓库里还要有 spec-write（ARD-F）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 to-spec 的 PRD |
| 2026-11-24 | 资源一节改为当前路径，并补上 spec-write（ARD-F） |
| 2026-11-24 | 开头注明本 skill 已移除，由 spec-ingest 取代（ARD-G）；health 改为 stale |
