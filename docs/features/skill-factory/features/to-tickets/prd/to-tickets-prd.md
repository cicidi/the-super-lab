---
feature: to-tickets
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# to-tickets — 需求

本篇从过去的对话和提交记录里，整理用户对 `to-tickets` 这个 skill 的需求。
实现见 [design](../design/to-tickets-design.md)。
决策的来由见 [decision-history](../decision-history/to-tickets-decision-history.md)。
Claude Code 会话原文没有保留；下文引用 `~/.claude/history.jsonl` 里的会话 id 前缀和时间。

## Overview

ticket 指 issue tracker 上的一条工单；issue tracker 是问题跟踪系统，例如 GitHub Issues 或 Jira。
`to-tickets` 把一份计划、spec 或一段对话拆成一组执行工单，并写明每张工单被哪些工单挡住。
spec 是写给开发者的需求和设计文档，通常由 to-spec 产出。
这个 skill 来自 Matt Pocock 的 mattpocock/skills，于 2026-08-02 导入（commit 8730941）。
导入发生在会话 d8d2da7f：用户导入 to-spec 后说"continue with to-tickets"（18:35）。
导入之后正文没有再改过；git 里只有两次目录搬迁（commit 8d451059、93d4a4a）。

## Goals and Success Metrics

目标一：把定好的 spec 拆成能直接动手的执行工单，和 wayfinder 产出的决策分开。
用户在自测问答里写道"Wayfinder 产出的是决策，to-tickets 产出的是执行工单"（d8d2da7f，17:14）。
目标二：沿用原作者的做法，并注明出处（同一会话 17:22 第 1 条、17:27 第 4 条）。
目标三：拆出的工单交给 auto-tdd 实现（同一会话 18:37）。
成功指标：UNKNOWN。对话和提交里都没有可量化的指标。

## User Stories

- 作为开发者，spec 定下后，我想让 agent 把它拆成一组工单，每张都能单独演示或验证。
- 作为开发者，我想看清每张工单被谁挡住，好知道哪些现在就能开工。
- 作为开发者，我想区分决策和执行：wayfinder 里的问题叫 brief，只有执行工单才叫 ticket。
- 作为 skill 仓库的维护者，我想看出这个 skill 来自谁，原文在哪里。

## Functional Requirements

**PRD-A 作为 wayfinder 流水线的一环导入。** wayfinder 的导入规格先把 to-tickets 列为"future imports"（commit 0f3ede7，18:21）。
14 分钟后用户说"continue with to-tickets"，commit 8730941 在 18:35 导入（d8d2da7f）。

**PRD-B 注明原作者。** 用户要求的第 1 条是"import 这个skill 著名作者"，即注明作者（d8d2da7f，17:22）。
commit 8730941 在 frontmatter 里写了 `source_author` 和 `source_url`。frontmatter 是 SKILL.md 开头的元数据块。

**PRD-C 沿用原版做法。** 用户说接口没有替换时"就用matt 的ksill"（d8d2da7f，17:27 第 4 条）。
原版做法是：按纵向切片拆工单，标出阻塞关系，先请用户审拆法，再发布到 tracker。
这几步是原作者的做法，用户没有逐条提出过。

**PRD-D "ticket" 一词只留给执行工单。** 用户说 ticket 用得混乱：to-tickets 的 ticket 保留，wayfinder 前面的要换名（17:22 第 2 条）。
用户 17:27 回复"2 ok"。wayfinder 随后把决策工单改叫 brief（commit 7c11a7b）。

**PRD-E spec 也要有一张 ticket。** 用户说"spec 本身也得有一个ticket"，要 toTicket 别忘了为 spec 的文档建一张 Jira（d8d2da7f，17:55）。
实际落在 to-spec 上：wayfinder 写明 spec 的 issue 由 to-spec 建（commit 7c11a7b）；to-tickets 的 SKILL.md 没有这一步。

**PRD-F 拆工单前先审文档。** 用户说"在to ticket 以前，还得有一个 doc-review 的过程"，审查所有文档（d8d2da7f，17:55）。
这道关口写在 wayfinder 里，排在 to-spec 和 to-tickets 之间（commit 7c11a7b）；to-tickets 本身不检查它。

**PRD-G 工单交给 auto-tdd 实现。** 用户说"implement 我的替代是auto-tdd"（d8d2da7f，18:37）。
两分钟后 commit 43cb1ef 给 wayfinder 加了流水线图，to-tickets 的下一站是 auto-tdd。

## Out of Scope

没有 spec 或计划可依据、一张工单就够、或决策还没定时，不用本 skill；决策没定先用 wayfinder。
这条来自 SKILL.md 的 `when_not_to_use` 字段（commit 8730941）。写代码也不归本 skill，是 auto-tdd 的事（PRD-G）。
用户划这条范围的原话没有找到，属于 UNKNOWN。

## Resources Needed

项目要配置好 issue tracker；没有配置时，默认写到本地 markdown 文件（PRD-C）。
需要一份已经审过的 spec 或计划作为输入（PRD-F）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 to-tickets 的 PRD |
