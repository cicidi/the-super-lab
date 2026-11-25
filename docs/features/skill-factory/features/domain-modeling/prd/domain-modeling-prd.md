---
feature: domain-modeling
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# domain-modeling — 需求

本篇从过去的对话和提交记录里，整理用户对 `domain-modeling` 这个 skill 的需求。
实现见 [design](../design/domain-modeling-design.md)。
决策的来由见 [decision-history](../decision-history/domain-modeling-decision-history.md)。
Claude Code 会话原文没有保留；下文引用 `~/.claude/history.jsonl` 里用户输入的会话 id 前缀和时间。

## Overview

domain model（领域模型）指一个项目里业务概念的名字、含义和它们之间的关系。
`domain-modeling` 让 agent 在讨论设计时主动收紧术语，把结论写进 glossary（术语表）和 ADR。
ADR（architecture decision record，架构决策记录）是一段记下"做了什么决定、为什么"的短文。
这个 skill 来自 Matt Pocock 的 mattpocock/skills，于 2026-08-02 导入（commit f6255af）。
需求起点是同日的会话 d8d2da7f：用户在学习 wayfinder，问"what does domain-modeling do?"。

## Goals and Success Metrics

目标一：给 wayfinder 提供访谈能力，定方向时把术语和决策写下来（d8d2da7f，2026-08-02）。
目标二：沿用原作者的做法，并注明出处（同一会话 17:22 的第 1 条）。
成功指标：UNKNOWN。对话和提交里都没有可量化的指标。

## User Stories

- 作为用 wayfinder 规划工作的开发者，我想在讨论时有人追问含糊的词，并当场记进术语表。
- 作为开发者，我想只为真正重要的决定写 ADR，其余不写。
- 作为 skill 仓库的维护者，我想看出这个 skill 来自谁，原文在哪里。

## Functional Requirements

**PRD-A 作为 wayfinder 的依赖导入。** 用户读完 wayfinder 后，要求把导入 matt skill 的任务交给 wayfinder 编排。
原话是"现在就把这个import matt skill 的任务做成一个wayfinder 编排的人物"（d8d2da7f，2026-08-02 17:22）。
wayfinder 的访谈步骤调用 `/domain-modeling`，所以它和 grill-with-docs 一起被导入（wayfinder-import-spec，commit 0f3ede7）。

**PRD-B 注明原作者。** 用户要求的第 1 条是"import 这个skill 著名作者"，即注明作者（d8d2da7f，17:22）。
commit f6255af 在 frontmatter 里写了 `source_author` 和 `source_url` 两个字段。

**PRD-C 沿用原版行为。** 用户说接口没有替换时"就用matt 的skill"，自己只有 research 一个替代（d8d2da7f，17:27）。
导入规格据此要求正文保持原样，只改 frontmatter（wayfinder-import-spec 的 Body preservation 一行）。
frontmatter 是 SKILL.md 开头两条 `---` 之间的元数据，记录名字、描述和触发词。

**PRD-D 做成可替换的接口实现。** 用户要求 wayfinder 用到的 skill 都是接口，"我自己要能提供impl 替代"（d8d2da7f，17:22）。
安装时问用户提供哪些实现，没给就用 matt 的 skill（同一会话 17:27）。
domain-modeling 是 interview（访谈）接口的默认实现之一。

**PRD-E 模板跟着 skill 走。** `CONTEXT-FORMAT.md` 和 `ADR-FORMAT.md` 两个模板放在 skill 目录里，与 SKILL.md 一起导入（commit f6255af）。
出处是 docs/book/imported-skills.md 的改编表；用户提出这一点的原话没有找到，属于 UNKNOWN。

**PRD-F 能装到 Claude Code 和 OpenCode。** 导入规格的验收表要求四个导入的 skill 都能部署到这两个工具（wayfinder-import-spec）。
SKILL.md 的 `compatibility` 字段写的是 `claude-code,opencode`。用户的原话没有找到，属于 UNKNOWN。

## Out of Scope

只读 `CONTEXT.md` 里的术语，不算本 skill；那是任何 skill 都能做的一行习惯（SKILL.md 的 `when_not_to_use`）。
改写原版正文不在范围内（PRD-C）。
research 不随这批导入，用户用自己的 research skill 代替（d8d2da7f，17:27；wayfinder-import-spec 的来源表）。

## Resources Needed

不需要外部服务或 API key。运行时只读写项目里的 `CONTEXT.md`、`CONTEXT-MAP.md` 和 `docs/adr/`。
人力上，术语由用户在对话里拍板，agent 负责追问和记录（SKILL.md 的 During the session 一节）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 domain-modeling 的 PRD |
