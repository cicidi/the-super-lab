---
feature: spec-ingest
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# spec-ingest — 需求

本篇整理用户对新 skill `spec-ingest` 的需求。这个 skill 还不存在，本篇是先于实现的正向 spec。
实现方案见 [design](../design/spec-ingest-design.md)。
决策的来由见 [decision-history](../decision-history/spec-ingest-decision-history.md)。
同时设计的姊妹 skill 是 spec-ticket，见 [spec-ticket PRD](../../spec-ticket/prd/spec-ticket-prd.md)。
下文"用户 2026-11-24（会话 80291c19）"指本次需求会话。

## Overview

spec 指一个 feature 的一组提交进仓库的文档：PRD、design、impl-plan、test-plan、decision-history。
它们的格式由 `skills/spec-organize/SPEC-STANDARD.md` 规定。
`spec-ingest` 读取已有的信息，例如聊天内容或本地文件，把其中每一条内容分到对应的文档类型里。
真正动笔写文档的仍然是 spec-write，spec-ingest 只读和分拣。
灵感来自 Matt Pocock 的 to-spec（`skills/to-spec/SKILL.md`）。
用户原话："to-spec to-ticket 我认为我自己应该创建一个 skill 灵感是来此matt pccock 这个"（用户 2026-11-24（会话 80291c19））。

## Goals and Success Metrics

目标一：把聊天内容或任何已有信息，转成用户自己的 spec 文档，不再依赖 Matt 原版的单一 PRD 模板（PRD-A）。
目标二：写 spec 的入口只有一个，即 spec-write，不出现第二条写入路径（PRD-B）。
目标三：新 skill 能用后，删掉 to-spec，仓库里不留两个做同一件事的 skill（PRD-F）。
成功指标：UNKNOWN。用户没有给出可量化的指标。

## User Stories

- 作为开发者，讨论已经有结论时，我想让 agent 把聊天内容分拣到 PRD、design 等文档里，不用自己逐条搬。
- 作为开发者，我手上有一份旧的 md、pdf 或 txt 文档，我想把它的内容并进某个 feature 的 spec。
- 作为维护者，我想在写入前看到每条内容去了哪个文档、出处是什么，没有出处的标成 UNKNOWN。
- 作为维护者，我不想让两个 skill 用两套规则写同一份 spec。

## Functional Requirements

**PRD-A 自建 skill，产出是用户自己的 spec 文档类型。** 用户要把"聊天内容，或者一个任何existing 信息"转成自己 spec 里的
"design prd impl test decision history"（用户 2026-11-24（会话 80291c19））。
impl 指 impl-plan，test 指 test-plan。

**PRD-B 只读和分拣，spec-write 是唯一的写入者。** 用户对"spec-ingest 只分拣、spec-write 才写"回答 yes（用户 2026-11-24（会话 80291c19），Q1）。
spec-ingest 只给出条目、出处、文档类型和目标 feature；写进哪个文件由 spec-write 决定（ARD-I）。
这与 SDD（spec-driven-development，从规格驱动开发）的 ARD-AJ 一致：写 spec 的入口 skill 是 spec-write（`docs/features/spec-driven-development/decision-history/`）。

**PRD-C 第一版只接受两种输入。** 一是当前聊天的上下文，二是本地文件，格式为 md、pdf、txt。
网址、会议转写稿、从代码反推 spec 都放到以后（用户 2026-11-24（会话 80291c19），Q2）。

**PRD-D 不访谈，只整理。** 沿用 to-spec 的做法：不向用户追问内容，只整理已有的信息（`skills/to-spec/SKILL.md`）。
用户导入 to-spec 时说过接口不变就"用matt 的ksill"（[to-spec PRD](../../to-spec/prd/to-spec-prd.md) 的 PRD-C）。

**PRD-E 名字叫 spec-ingest。** 用户对这个名字回答"可以"（用户 2026-11-24（会话 80291c19），Q6）。

**PRD-F 能用后删掉 to-spec，并改指所有引用。** 用户说 Matt 的 to-spec"可以去掉"（用户 2026-11-24（会话 80291c19），Q5）。
`grep -rln 'to-spec\|to-tickets'` 找到的每个文件，都在同一个改动里改指新 skill；改前改后各查一次（ARD-K）。
顺序是：先写 spec，再 spec-review，再用户审阅，再写 SKILL.md，最后删旧 skill 并改指（同一会话，Q9）。

**PRD-G 没有出处的事实标 UNKNOWN。** 分拣出的每条内容都要带出处；找不到出处就写 UNKNOWN，不猜。
这条是 spec-write 的现行规则（`skills/spec-write/SKILL.md` 的 Example Domains 一节）。

## Out of Scope

第一版不读网址、会议转写稿，也不从代码反推 spec（PRD-C）。这些是以后的方向。
不直接写或改任何提交进仓库的 spec 文档，写入归 spec-write（PRD-B）。
不建 GitHub issue 或 Jira 工单，那是 [spec-ticket](../../spec-ticket/prd/spec-ticket-prd.md) 的事。
不做 spec-review 的对抗式审查。

## Resources Needed

需要 spec-write 和它读取的标准文件：`SPEC-STANDARD.md`、`SPEC-PRESENTATION.md`（PRD-B）。
读 pdf 需要 agent 的文件读取工具支持 pdf（PRD-C）。
人力上，用户在写入前确认一次分拣结果（见 design 的 DSGN-H）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按会话 80291c19 的用户决定写出 spec-ingest 的正向 PRD |
| 2026-11-24 | 按 spec-review：PRD-B 加分工（ARD-I）并定义 SDD；PRD-F 改指清单改为 grep（ARD-K） |
