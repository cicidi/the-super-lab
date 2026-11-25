---
feature: prototype
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# prototype — 需求

本篇从过去的对话和提交记录里，整理用户对 `prototype` 这个 skill 的需求。
实现见 [design](../design/prototype-design.md)。
决策的来由见 [decision-history](../decision-history/prototype-decision-history.md)。
Claude Code 会话原文没有保留；下文引用 `~/.claude/history.jsonl` 里用户输入的会话 id 前缀和时间。

## Overview

prototype（原型）指为回答一个设计问题而写的、用完就扔的代码。
`prototype` 让 agent 按问题的类型，做一个终端小程序或几种 UI 变体给用户看。
这个 skill 来自 Matt Pocock 的 mattpocock/skills，于 2026-08-02 导入（commit 78242fa）。
需求起点是同日的会话 d8d2da7f：用户在学习 wayfinder，问"what about prototype?"（12:12）。
wayfinder 是一个规划 skill，把大任务拆成多张 brief（待解决的问题卡片）；prototype 负责其中一类 brief。

## Goals and Success Metrics

目标一：给 wayfinder 的 prototype 类 brief 提供一个能用的实现（d8d2da7f，2026-08-02 17:22 第 6 条）。
目标二：沿用原作者的做法，并注明出处（同一会话 17:22 第 1 条、17:27 第 4 条）。
成功指标：UNKNOWN。对话和提交里都没有可量化的指标。

## User Stories

- 作为用 wayfinder 规划工作的开发者，遇到"应该长什么样""应该怎么动"的问题时，我想先看到一个粗糙但具体的东西再拍板。
- 作为开发者，我想一条命令就能跑起原型，看完就能扔，不污染主分支。
- 作为 skill 仓库的维护者，我想看出这个 skill 来自谁，原文在哪里。

## Functional Requirements

**PRD-A 作为 wayfinder 的依赖导入。** 用户要求"现在就把这个import matt skill 的任务做成一个wayfinder 编排的人物"（d8d2da7f，17:22）。
wayfinder 的 prototype brief 调用 `/prototype`，所以它和 grill-with-docs、domain-modeling 一起被导入（wayfinder-import-spec 的 Files to Import，commit 0f3ede7）。

**PRD-B 注明原作者。** 用户要求的第 1 条是"import 这个skill 著名作者"，即注明作者（d8d2da7f，17:22）。
commit 78242fa 在 frontmatter 里写了 `source_author` 和 `source_url`，导入测试计划的 TC-03 逐个检查这两个字段。

**PRD-C 沿用原版行为。** 用户说接口没有替换时"就用matt 的ksill"，自己只有 research 一个替代（d8d2da7f，17:27）。
导入规格据此要求 prototype 的正文保持原样，只改 frontmatter（wayfinder-import-spec 的 Body preservation 一行）。
frontmatter 是 SKILL.md 开头两条 `---` 之间的元数据，记录名字、描述和触发词。

**PRD-D 做成可替换的接口实现。** 用户要求 wayfinder 用到的 skill 都是接口，"我自己要能提供impl 替代"（d8d2da7f，17:22）。
安装时问用户提供哪些实现，没给就用 matt 的 skill（同一会话 17:27）。本 skill 是 prototype 接口的默认实现。

**PRD-E 原型要人参与。** HITL（human in the loop）指过程中要有人看、有人判断；AFK（away from keyboard）指 agent 可以独自完成。
用户复述 wayfinder 的 brief 类型时说"Research AFK, prototype HITL, grilling HITL, task both"（d8d2da7f，17:12）。

**PRD-F 能装到 Claude Code 和 OpenCode。** 导入规格的验收表要求四个导入的 skill 都能部署到这两个工具（wayfinder-import-spec 的 Deployment 一行）。
SKILL.md 的 `compatibility` 字段写的是 `claude-code,opencode`。用户的原话没有找到，属于 UNKNOWN。

## Out of Scope

答案在文档里已经清楚，或者直接写正式代码更快时，不用本 skill（SKILL.md 的 `when_not_to_use`）。
原型不写测试，不做多余的错误处理（SKILL.md 规则 4）。改写原版正文不在范围内（PRD-C）。
前两条来自原作者；用户自己划这些范围的原话没有找到，属于 UNKNOWN。

## Resources Needed

不需要外部服务或 API key。UI 原型要用项目已有的页面路由和任务命令（SKILL.md 规则 1、2）。
人力上，用户要看原型并给出结论（PRD-E）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 prototype 的 PRD |
