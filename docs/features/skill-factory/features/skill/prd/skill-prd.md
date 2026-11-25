---
feature: skill
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# skill — 需求

本篇从过去的对话和提交记录里，整理用户对 `skill` 这个 skill 的需求。
实现见 [design](../design/skill-design.md)。
决策的来由见 [decision-history](../decision-history/skill-decision-history.md)。
opencode 会话存在本机 opencode.db，下文按会话 id 前缀引用。

## Overview

skill 是一份 SKILL.md 文件，告诉 AI agent 遇到某类任务时按什么步骤做。
`skill` 负责在 the-super-lab 里创建、修改、导入和列出 skill。
需求起点是用户的一句话："我要做一个skill factory"。
里面放自己写的好 skill，也放导入的别人的 skill（会话 ses_14b5b4b7，2026-06-10）。

## Goals and Success Metrics

目标一：新 skill 格式一致，并且不和已有 skill 重复。
目标二：导入别人的 skill 时，版权和出处清楚。
目标三：create 好到能造出 import 和 edit，而它们又能导入、改进别的 skill
（会话 ses_14aa890f，2026-06-10）。
成功指标：UNKNOWN。对话里没有给出可量化的指标。

## User Stories

- 作为 skill 作者，我想先看 GitHub 上有没有类似的 skill，再决定导入、借鉴还是自己写。
- 作为维护者，我发现某个 skill 有问题时，想做小改动，而不是另建一个重复的。
- 作为使用者，我想导入别人的 skill，并保留原作者和出处。

## Functional Requirements

**PRD-A 单一入口。** 创建、修改、导入、列出 skill 都走一个 `/skill`。
四件事用子命令区分：create、edit、import、list。
证据：2026-08-02 把原来四个独立 skill 合成一个（commit 6086424；
parent design 的 Skill Consolidation 一节）。

**PRD-B 先查重再创建。** 创建前先在本地、GitHub 和网上找类似的 skill。
用户要求在 GitHub 上"至少找到10个类似的skill"，并对比功能和优缺点（ses_14bdec5d，2026-06-10）。
找到后让用户三选一：导入后再改、只吸收灵感、自己从头写（ses_14aa890f，2026-06-11；commit d30f01c）。
当前 SKILL.md 保留了搜索这一步，但没有写"至少 10 个"的下限。

**PRD-C 格式规则只有一个出处。** 名字用 kebab-case（小写加连字符），name 字段必须和文件夹名一致。
用户原话是"name 和文件夹必须匹配"（ses_14aa890f，2026-06-11）。
这些规则统一写在仓库根目录的 `CONVENTIONS.md`，它随第一个提交出现（commit 5d9747e）。

**PRD-D edit 只做小改动。** edit 用于用户"发现问题了"时做"微小的改动"，不另建重复的 skill。
写法和验证流程照样要走一遍（ses_14aa890f，2026-06-10）。
目标 skill 不存在，或改动达到重写八成以上时，转去 create（parent decision history 第 0099 条）。

**PRD-E 导入保留原名。** 导入的 skill 保留原名，不加本仓库的前缀。
用户原话是"skill-import 不要加前缀"（ses_14aa890f，2026-06-11）。缺的格式字段要补齐。

**PRD-F 导入保留作者和出处。** 导入时要"复合版权，著名出处"（ses_14b5b4b7，2026-06-10），
也就是符合版权、注明出处；并"保留原作者信息"（ses_14aa890f，2026-06-11；commit 773594b）。
2026-11-24 起，import 流程记录作者、出处 URL 和导入日期，见 design 的 DSGN-C 和 ARD-J。

**PRD-G 一个 skill 一个文件。** 每个 skill 就是一份 SKILL.md，不要做多层目录。
用户问过"为什么不是世界一个Skill.md 就行了"（ses_14b5b4b7，2026-06-10）。
没有 deploy（部署副本）概念，只留一个版本；change log 不写进 skill，用 git log（ses_14bdec5d，2026-06-10）。

**PRD-H 先给人看，再保存。** create 的草稿和 edit 的 diff，都要用户确认后才写入文件。
证据是 `skills/skill/SKILL.md`（commit c2b3f22）和合并原则 "Ask first"（parent design）。
对话里没有找到用户直接提出这一条的原话，出处属于 UNKNOWN。

**PRD-I 自举并迭代。** 自举指用 create 造出 import 和 edit 这两个工具本身。
产出的 skill 不好时，先修 create，再重新生成并复审，如此反复（ses_14aa890f，2026-06-10）。

## Out of Scope

运行已有 skill、管理 feature、管理项目目录，都不归本 skill 管（见 SKILL.md 的 When NOT to Use 一节）。
导入时是否审查 skill 内容的安全性，对话里没有提过，属于 UNKNOWN，记在 design 的 QUES-B。

## Resources Needed

需要 GitHub 和网页搜索能力（PRD-B），以及 `coworker` 命令行工具来列出 skill。
人力上，每次 create、edit、import 都要用户审阅一次（PRD-H）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 skill 的 PRD |
| 2026-11-24 | PRD-F 改为当前行为：import 已记录出处（ARD-J） |
