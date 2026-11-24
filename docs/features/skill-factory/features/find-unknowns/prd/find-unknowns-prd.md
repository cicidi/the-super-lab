---
feature: find-unknowns
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# research — 需求

本篇从过去的对话和提交记录里，整理用户对 `research` 这个 skill 的需求。
子 feature 叫 find-unknowns，和 skill 名不同，原因见 [decision-history](../decision-history/find-unknowns-decision-history.md) 的 ARD-L。
实现见 [design](../design/find-unknowns-design.md)。
Claude Code 会话按 `~/.claude/history.jsonl` 里会话 id 的前八位引用。

## Overview

`research` 用在动手写代码之前，帮用户找出还没想清楚的地方，这些地方叫 unknowns（未知点）。
它有四个分支：发现未知（Discover unknowns）、写设计文档（Design spec）、无人值守调研（Investigate AFK）和小测验（Quiz）。
源头是 2026-07-18 用户发来 Thariq Shihipar 的一篇文章，说"读这个文章，帮我转变称一个skill"（会话 ca8d23f7）。
文章讲怎样找出自己的未知，产出的 skill 起名 find-my-unknown（同一会话）。
brainstorming 是 superpowers 插件里的 skill，通过一问一答把想法变成设计文档。
2026-08-02 用户要求把这两个合并，合并后叫 research（会话 8903e04e，commit 6086424）。
2026-11-24 用户批准加上无人值守调研分支、恢复小测验（PRD-M、PRD-N）。

## Goals and Success Metrics

目标一：写代码前找出用户的未知，用户原话是"find user unknown的部分"（ca8d23f7，2026-07-18）。
目标二：减少 skill 数量，用户说 skill"太多了，不好管理"（8903e04e，2026-08-02）。
目标三：给别的 skill 提供"找未知、查资料"的能力，见 PRD-J、PRD-K 和 PRD-M。
成功指标：UNKNOWN。对话里没有给出可量化的指标。

## User Stories

- 作为开发者，我有任务但不知道漏了什么，想让 agent 一次问一个问题帮我理清。
- 作为开发者，我只有模糊的想法，想让 agent 陪我比较方案，再写成设计文档。
- 作为 wayfinder 这类规划 skill，我需要一个不用人参与、能交回带出处文件的调研能力。
- 作为开发者，我刚听完一段讲解或看完一次改动，想让 agent 考考我是否真懂了。

## Functional Requirements

**PRD-A 先选分支。** 用户问"find-my-unknown 和 brainstorming 有什么相似度"，随后答"合并"（8903e04e，2026-08-02）。
同一会话要求：分支需要的参数和条件，"skill 一开始的时候要问清楚"。

**PRD-B 合并要融合逻辑。** 用户说合并 skill 时"不要原封不动保留"（8903e04e，2026-08-02）。
能合并的逻辑合并，不能合并的加分支（同一会话）。

**PRD-C 以访谈为主线。** interview（访谈）指 agent 提问、用户回答，agent 再根据回答追问。
用户要求"通过interview 的手段"找未知，"可以根据每一个问题，继续追问"（ca8d23f7，2026-07-18）。
用户还说"每个阶段"都要用类似的访谈方式和用户交流、提炼结果（同一会话）。

**PRD-D 一次只问一个问题。** 用户原话"每次一个问题"（ca8d23f7，2026-07-18）。
用户贴的参考提示词也写着"only one question at a time"（同一会话）。

**PRD-E 可以默默扫描，关键处必须问。** 用户说 agent"可以默默扫描"代码（ca8d23f7，2026-07-18）。
但不清楚的，或"对决策方向有大的影响的一定要问清楚"（同一会话）。

**PRD-F 按改错的代价决定追问深度。** backend、API、data model（数据模型）这类以后不好改的，要问得深一点（ca8d23f7，2026-07-18）。
选哪个 LLM provider 这类以后能换的属于优化，"不用那么深"；不影响当前开发的不追问（同一会话）。
一个话题问了 2 到 3 轮，就换下一个话题（同一会话）。

**PRD-G 其他技巧做辅助。** 文章给了五种技巧，agent 起初写成"五选一"（ca8d23f7，2026-07-18）。
用户要求"把 1 2 4 作为辅助手段加回去，主线还是 interview"（同一会话）。
1、2、4 指盲区扫描、头脑风暴加原型、参考已有实现，见同一会话里 agent 列的表。

**PRD-H 设计文档分支沿用 brainstorming。** parent design 合并表第 10 行写明，Design spec 分支吸收了 superpowers:brainstorming。
用户此前常用 brainstorming 推进设计，例如 ses_14b5b4b7（opencode，2026-06-10）和 b1cdd2d6（2026-07-18）。
吸收时保留哪些步骤，没有找到用户的原话，属于 UNKNOWN。

**PRD-I 设计文档放在 feature 目录。** 输出路径随项目的文档约定改过两次：commit c2b3f22（2026-09-24）和 c127ef7（2026-11-04）。
两次都是全仓库批量改动的一部分，没有找到单独讨论 research 的对话。

**PRD-J 做 wayfinder 的调研实现。** wayfinder 是从 mattpocock/skills 导入的规划 skill（commit 7c11a7b）。
用户要求它依赖的 skill 能替换，并说"对于ai -cowork 我有自己的research，其他的都用 matt 的"（d8d2da7f，2026-08-02）。

**PRD-K 做 SDD 的盲区发现工具。** SDD 即 spec-driven development，从 spec 驱动开发。
SDD 的决策 ARD-L（2026-10-30）定下：盲区由现有的 research 和 grill-with-docs 发现，不另造新 skill。
出处：[SDD decision-history](../../../../spec-driven-development/decision-history/spec-driven-development-decision-history.md)。

**PRD-L 通用 skill，不带前缀。** 用户把名字从 ai-coworker-find-my-unknown 改成 find-my-unknown，"去掉前缀"（ca8d23f7，2026-07-18）。
同一会话定下放置规则：不依赖 ai-coworker 也能工作的通用 skill，放在 skill 仓库，而不是 ai-coworker 项目里。

**PRD-M 无人值守调研。** AFK（away from keyboard）指用户不在场，agent 独自完成。
wayfinder 把 research 当作 AFK 子 agent 调用，要它交回一份带出处的 markdown 文件（`skills/wayfinder/SKILL.md` 第 124、137、306 行）。
这时不能问用户问题；查不到的事实标为 UNKNOWN。出处：用户 2026-11-24 审阅回复。

**PRD-N 小测验。** 用户在听完 wayfinder 的讲解后输入"/research 你来考考我"（d8d2da7f，2026-08-02）。
这个小测验在 find-my-unknown 里有（commit 9e4fb21），合并时被删掉；用户 2026-11-24 批准照原样恢复。

**PRD-O 设计文档交给 spec-write。** SDD 的决策 ARD-AJ 定下 spec-write 是写规格的入口（SDD decision-history）。
在有 SDD 规格的仓库里，写设计文档要交给 spec-write，格式才符合 SPEC-STANDARD.md。出处：用户 2026-11-24 审阅回复。

## Out of Scope

拼写错误、一行改动这类小任务，以及需求已写得毫无歧义的任务，不用本 skill（SKILL.md 的 When NOT to Use 一节）。
已经在写代码时，改用 `/bug`（同一节）。对话里没找到用户划这条范围的原话，出处属于 UNKNOWN。

## Resources Needed

人力：发现未知和写设计文档两个分支要用户回答问题，一次一个（PRD-D）；无人值守调研分支不需要人（PRD-M）。
工具：Design spec 分支最后交给 superpowers:writing-plans 写实现计划，要求装了 superpowers 插件（SKILL.md 的 B7 一节）。
在 SDD 仓库里，B5 还要用到 spec-write（PRD-O）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 research 的 PRD |
| 2026-11-24 | 加 PRD-M、PRD-N、PRD-O：无人值守调研、小测验、B5 交给 spec-write；子 feature 改名 find-unknowns |
