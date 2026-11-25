---
feature: grill-with-docs
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# grill-with-docs — 需求

本篇从过去的对话和提交记录里，整理用户对 `grill-with-docs` 这个 skill 的需求。
实现见 [design](../design/grill-with-docs-design.md)。
决策的来由见 [decision-history](../decision-history/grill-with-docs-decision-history.md)。
Claude Code 会话原文没有保留；下文引用 `~/.claude/history.jsonl` 里的会话 id 前缀和时间。

## Overview

grilling（拷问式访谈）指 agent 一个接一个地追问用户，直到计划或设计足够清楚。
`grill-with-docs` 跑一次这种访谈，并借 `domain-modeling` 把术语和决策当场写进文档。
这个 skill 来自 Matt Pocock 的 mattpocock/skills，于 2026-08-02 导入（commit 6835420）。
需求起点是同日的会话 d8d2da7f：用户在学习 wayfinder，问"grill with docs , what does this do?"（10:15）。
它调用的 `/grilling` 于 2026-11-24 从上游 commit fa460cb 补导到 `skills/grilling/`（decision-history 的 ARD-G）。

## Goals and Success Metrics

目标一：给 wayfinder 提供访谈能力，定目的地时把术语和决策写下来（d8d2da7f，2026-08-02）。
目标二：沿用原作者的做法，并注明出处（同一会话 17:22 的第 1 条）。
成功指标：UNKNOWN。对话和提交里都没有可量化的指标。

## User Stories

- 作为用 wayfinder 规划工作的开发者，我想在定方向时被逐个追问，含糊的地方当场说清。
- 作为开发者，我想让访谈中定下的术语和决策自动落到 `CONTEXT.md` 和 ADR 里。
  `CONTEXT.md` 是项目的术语表；ADR（architecture decision record）是记下"做了什么决定、为什么"的短文。
- 作为 skill 仓库的维护者，我想看出这个 skill 来自谁，原文在哪里。

## Functional Requirements

**PRD-A 作为 wayfinder 的依赖导入。** 用户读完 wayfinder 后说"这个wayfind 大部分我是同意的。 我也想使用"（d8d2da7f，17:22）。
同一条消息的第 6 条要求把导入 matt skill 的任务交给 wayfinder 编排。
wayfinder 定目的地和处理 grilling 类 brief 时都调用本 skill，所以它被列进导入清单（wayfinder-import-spec，commit 0f3ede7）。
brief 是 wayfinder 地图上的一个待决问题；grilling 类 brief 要和真人对话才能解决。

**PRD-B 注明原作者。** 用户要求的第 1 条是"import 这个skill 著名作者"，即注明作者（d8d2da7f，17:22）。
commit 6835420 在 frontmatter 里写了 `source_author` 和 `source_url` 两个字段。
frontmatter 是 SKILL.md 开头两条 `---` 之间的元数据，记录名字、描述和触发词。

**PRD-C 沿用原版正文。** 用户说接口没有替换时"就用matt 的ksill"，自己只替换 research（d8d2da7f，17:27）。
导入规格据此要求正文保持原样，只改 frontmatter（wayfinder-import-spec 的 Body preservation 一行）。

**PRD-D 做成可替换的接口实现。** 用户要求 wayfinder 用到的 skill 都是接口，"我自己要能提供impl 替代"（d8d2da7f，17:22）。
安装时问用户提供哪些实现，没给就用 matt 的 skill（同一会话 17:27）。
grill-with-docs 和 domain-modeling 一起，是 interview（访谈）接口的默认实现（skills/wayfinder/SKILL.md 的接口表）。

**PRD-E 能装到 Claude Code 和 OpenCode。** 导入规格的验收表要求四个导入的 skill 都能部署到这两个工具（wayfinder-import-spec）。
SKILL.md 的 `compatibility` 字段写的是 `claude-code,opencode`。用户的原话没有找到，属于 UNKNOWN。

## Out of Scope

需求已经很清楚、或用户只想要一个快速回答时，不用本 skill（SKILL.md 的 `when_not_to_use`）。
改写原版正文不在范围内（PRD-C）。
导入清单只有 wayfinder、grill-with-docs、domain-modeling、prototype 四个，没有 `/grilling`（wayfinder-import-spec 的 Files to Import）。
2026-11-24 用户同意补导 `/grilling`（ARD-G）。

## Resources Needed

不需要外部服务或 API key。运行时依赖两个 skill：`/grilling` 和 `/domain-modeling`。
两者都在 `skills/` 下（见 Overview）。人力上，访谈必须有真人在场回答问题（skills/wayfinder/SKILL.md 的 HITL 定义）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 grill-with-docs 的 PRD |
| 2026-11-24 | `/grilling` 已补导（ARD-G）：更新 Overview、Out of Scope、Resources Needed |
