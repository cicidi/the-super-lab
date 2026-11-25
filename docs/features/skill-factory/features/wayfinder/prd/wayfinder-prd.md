---
feature: wayfinder
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# wayfinder — 需求

本篇从过去的对话和提交记录里，整理用户对 `wayfinder` 这个 skill 的需求。
实现见 [design](../design/wayfinder-design.md)。
决策的来由见 [decision-history](../decision-history/wayfinder-decision-history.md)。
主要证据是 2026-08-02 的 Claude Code 会话 d8d2da7f；下文只写那天的时间，例如（17:22）。
to-spec、to-tickets、implement 三个兄弟 skill 已写过的事实，这里只链接，不重复。

## Overview

wayfinder 来自 mattpocock/skills，用来规划一个 agent 会话装不下的大任务。
它在 issue tracker（GitHub Issues、Jira 这类工单系统）上建一张地图，把待定的决策一个个定下来。
用户当天先花几小时学习它，然后说"这个wayfind 大部分我是同意的。 我也想使用。但是要改造以下"（17:22）。
导入和改造在同一会话完成：commit 7c11a7b（18:20）导入 skill，0f3ede7（18:21）提交导入规格。

## Goals and Success Metrics

目标一：大任务的决策持久地记在 tracker 上，下个会话说一声就能接着做（14:45 的提问）。
目标二：接进用户自己的 skill 体系，依赖可替换，下游一直走到写代码（17:22 第 4 条，18:37）。
目标三：交付前一定有审查，产出的文档能直接发布成网站（17:27 第 7 条，17:57）。
成功指标：UNKNOWN。对话里没有量化指标；导入时只有一份 12 条用例的检查清单（commit 0f3ede7 的 test plan）。

## User Stories

- 作为开发者，我想在下个会话只说"我还在做这张地图"，就拿到下一件该做的事。
- 作为开发者，我想把 wayfinder 依赖的某个 skill 换成我自己的实现。
- 作为开发者，我想分清"待定的决策"和"要执行的工单"，不被同一个词搞混。

## Functional Requirements

**PRD-A 注明原作者。** 用户第 1 条要求是"import 这个skill 著名作者"（17:22），17:27 回复"1。ok"。
commit 7c11a7b 在 frontmatter 里写了 `source_author` 和 `source_url` 两个字段。

**PRD-B 决策工单改叫 brief。** 用户说 ticket 用得混乱：to-tickets 的 ticket 保留，前面的要换名（17:22 第 2 条）。
用户给的候选是 challenge、question、query，也可由 agent 推荐；17:27 回复"2 ok"，最终用 brief（commit 0f3ede7 术语表）。
经过见 [to-tickets 的 ARD-E](../../to-tickets/decision-history/to-tickets-decision-history.md#ard-e)。

**PRD-C 其他术语不改。** 用户说"map 不改， 还是这个名字""fog of war 也不该"（17:47）。
fog of war（战争迷雾）指地图上看得到方向、但还说不清的那部分问题。
用户下午曾想把术语全换成美剧《绝命毒师》(Breaking Bad)的词（14:25），17:50 改口"不用非要按照break bad 来"。

**PRD-D 定终点就是讨论 PRD，应当是第一个问题。** destination（终点）指这张地图最后要得到的东西，比如一份 spec。
用户认为设计终点"其实就是讨论一个prd 的过程"，它应是一个 challenge，定下来以前没法拆出别的（17:22 第 3 条）。
17:27 回复"3 yes"。当前 SKILL.md 把它写成一个步骤，不是一个 brief，见 design 的 QUES-A。

**PRD-E 依赖的 skill 都是可替换的接口。** 用户要求"他用的所有的skill 应该是一个接口，我自己要能提供impl 替代"（17:22 第 4 条）。
17:27 补充：安装时就问用户这四个接口；没给替代就用 matt 的 skill；research 用自己的，其他都用 matt 的。

**PRD-F 每次交付前都要审查。** 用户原话："每次delivery 以前，所有的代码都需要review 以下"（17:27 第 7 条）。
文档用 ai-coworker 的 doc-review，代码用 ai-coworker 的 code review；没有实现时用 Claude 自带的审查（同一条）。
17:52 用户追问"wayfinder 应该有一个doc review 或者code review 你放了吗？"。

**PRD-G spec 也有一个 issue，拆工单前全面审一次文档。** 用户说"spec 本身也得有一个ticket"（17:55）。
同一句还要求 to-tickets 以前"还得有一个 doc-review 的过程"，审查所有文档。
落地细节见 [to-spec 的 ARD-B](../../to-spec/decision-history/to-spec-decision-history.md#ard-b)。
现在 spec 是文档；"spec 的 ticket"由 spec-ticket 为每个 feature 开的母工单满足，审查关口在 spec-ticket 之前（ARD-L）。

**PRD-H 文档能直接发布成网站。** 用户问 doc-organize"还得保证 所有文档 mkdoc ready to deploy as github webpage 这个有吗？"（17:57）。
MkDocs 是把一组 markdown 生成静态网站的工具，生成的网站可放在 GitHub Pages 上。

**PRD-I 给一个完整的生命周期示例。** 用户第 5 条："我需要给我一个完整的example ， life cyle"（17:22），17:27 回复"5. 好的"。
示例写在导入规格第 8 节（commit 0f3ede7）；SKILL.md 里只有流水线和实体关系两张小图，见 design 的 QUES-F。

**PRD-J 用 wayfinder 自己编排这次导入。** 用户第 6 条：把"import matt skill 的任务做成一个wayfinder 编排的人物"（17:22）。
之后用户多次问"wayfinder 下一步"（18:04、18:07、18:28），按地图往下走。

**PRD-K 先写测试计划，再写实现计划。** 用户说"应该先写test plan 在写impl plan"，并要求加进 spec（18:02、18:04）。
导入规格第 9.1 节写了这条（commit 0f3ede7）。它约束的是导入工作，SKILL.md 里没有。

**PRD-L 下游接到用户自己的 build skill。** 用户说"implement 我的替代是auto-tdd"（18:37）。
commit 43cb1ef（18:39）给 SKILL.md 加了流水线图，最后一步是 auto-tdd。
详见 [implement 的 ARD-B](../../implement/decision-history/implement-decision-history.md#ard-b)。

## Out of Scope

wayfinder 不做执行。用户问"so wayfinder is just assign the work , but not do the work?"（14:46）；SKILL.md 的 Plan, don't do 一节确认这点。
导入规格写明不导入 setup-matt-pocock-skills（改用 ai-coworker 的 init）和 triage（wayfinder 用不到）（commit 0f3ede7 第 11 节）。
to-spec、to-tickets、implement 当时列为后续导入，同一晚就导入了，见各自 PRD 的 PRD-A。

## Resources Needed

需要一个 issue tracker 和能操作它的工具；SKILL.md 的接口表默认用 `gh` 命令行操作 GitHub Issues（PRD-E）。
人力上，grilling 和 prototype 两类 brief 必须有人在场回答（SKILL.md 的 Brief Types 一节）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 wayfinder 的 PRD |
| 2026-11-24 | PRD-G 补一句现状：母工单由 spec-ticket 建（ARD-L） |
