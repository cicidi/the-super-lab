---
feature: spec-ticket
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# spec-ticket — 需求

本篇写用户对一个**还没有实现**的新 skill `spec-ticket` 的需求，是前瞻式 spec（forward spec）。
实现方案见 [design](../design/spec-ticket-design.md)。
决策的来由见 [decision-history](../decision-history/spec-ticket-decision-history.md)。
需求全部来自用户 2026-11-24（会话 80291c19）的原话和问答，下文简称"用户 2026-11-24"。

## Overview

ticket 指 issue tracker 上的一条工单；issue tracker 是问题跟踪系统，例如 GitHub Issues 或 Jira。
impl-plan 是 spec 里的实施计划文档，每一步写成一个 `IMPL-*` 小节，并写明它依赖谁、挡住谁、怎样算完成。
`spec-ticket` 读一份 impl-plan，为每条 `IMPL-*` 开一张工单，发到用户配置的 tracker。
用户的出发点是："to ticket 可以转成jira 或者github issue 。 看用户自己的配置"（用户 2026-11-24）。
灵感来自 Matt Pocock 的 to-tickets（`skills/to-tickets/SKILL.md`）；新 skill 可用后，to-tickets 会被移除（PRD-I）。
与它配对的上游新 skill 是 spec-ingest，负责把聊天和已有材料整理进 spec，见
`docs/features/skill-factory/features/spec-ingest/prd/spec-ingest-prd.md`。

## Goals and Success Metrics

目标一：把 impl-plan 里已经拆好的每一步，变成 tracker 上能看、能跟踪的工单（PRD-A）。
目标二：tracker 由用户自己选，GitHub、Jira 或本地文件都行（PRD-B）。
用途说明：用户说这"只是为了demo/track job"，"目前没发现什么实际用途。比如提高 工作效率，准确度"（用户 2026-11-24）。
所以本 skill 的目标是演示和跟踪进度，不承诺提高效率或准确度。
成功指标：UNKNOWN。用户没有给出可量化的指标；可检查的底线是重跑不产生重复工单（PRD-E）。

## User Stories

- 作为开发者，impl-plan 定稿后，我调用 spec-ticket，每条 IMPL 在 tracker 上都有一张对应的工单。
- 作为开发者，我在工单上能看出哪张挡住哪张，知道哪些现在能开工。
- 作为开发者，我在 impl-plan 里加了新的 IMPL，再跑一次，只多出新的那几张，旧的不重复。
- 作为演示者，我想给别人看"spec 里的计划"和"tracker 上的工单"是一一对应的。

## Functional Requirements

**PRD-A 一条 IMPL 一张工单。** 用户说"to ticket 可以是impl 也要对应git issue or jira"（用户 2026-11-24）。
用户同意的最小方案是：读 impl-plan 里的每条 `IMPL-*`，每条开一张工单（Q8"按照建议来"）。

**PRD-B 按用户配置选 tracker。** 可选 GitHub issue、Jira 或本地 markdown，"看用户自己的配置"（用户 2026-11-24）。
配置写在哪、缺省怎么办，用户没有回答；按协调者的推荐处理，见 decision-history 的 ARD-C 和 design 的 QUES-C。

**PRD-C 阻塞关系来自 IMPL 自己写的依赖。** 每条 IMPL 写明依赖谁、挡住谁（`skills/spec-organize/SPEC-STANDARD.md`）。
工单之间的阻塞边（谁必须先完成）照这两项连，不另行推断（用户 2026-11-24，Q8）。

**PRD-D 记下 IMPL 和工单的对应表。** 对应表存在 `docs/features/<f>/raw/state/` 下（用户 2026-11-24，Q8）。
本地模式的工单文件放在同一处的 `spec-ticket/issues/`，文件名就是对应关系（用户 2026-11-24 审阅同意，ARD-J）。
这个目录被 git 忽略（`.gitignore` 的 `docs/features/**/raw/` 规则），不进提交。

**PRD-E 重跑只加新的，不重复。** 再次运行时只为新出现的 IMPL 开工单，已开过的不再开（用户 2026-11-24，Q8）。

**PRD-F 单向，不回写。** 不做双向同步，也不把工单状态写回 spec 文档（用户 2026-11-24，Q8）。
双向同步指 tracker 上的改动会自动反映回 spec，反之亦然。

**PRD-G 保留 Jira，给其他人用。** 用户说"jira 保留，给其他人用。保留三个选项"（用户 2026-11-24 审阅）。 本机没有 Jira 连接：没有 Jira 的 MCP 服务；GitHub 有 gh 命令行和 GitHub MCP。
所以 Jira 这一路在本机没法实测；早先"先只留接口"（Q8）的决定已被取代（ARD-I）。用哪种 Jira（云版还是自建）未知，见 design 的 QUES-B。

**PRD-H 有阻塞问题时不开工单。** wayfinder 规定：feature design 里有标为 blocking 的 `QUES-*` 还开着时，
不开始下游工作，包括拆工单（`skills/wayfinder/SKILL.md` 的 PIPE-E-A 规则）。spec-ticket 同样遵守。

**PRD-I 取代 to-tickets。** 用户说 Matt 的 to-spec 和 to-tickets"可以去掉"（用户 2026-11-24，Q5）。
移除在新 skill 可用之后进行；引用旧 skill 的文件（`grep -rln 'to-spec\|to-tickets'` 找到的每一个），在同一次改动里改指向。
顺序是：spec、spec-review、用户审阅、写 SKILL.md、最后移除旧 skill 并改指向（用户 2026-11-24，Q9）。

## Out of Scope

v1 不做：双向同步、把状态写回 spec（PRD-F）。
不重新切分工作：to-tickets 的纵向切片（tracer bullet）不要了，切分已在 impl-plan 里做完（PRD-A）。
不写 spec 文档，那是 spec-ingest 和 spec-write 的事；不写代码，那是 implement 的事。

## Resources Needed

GitHub 这一路需要本机装好并登录 gh 命令行（本机已有）。
Jira 这一路需要 Jira 网址、账号邮箱、API token 和项目 key（环境变量），本机目前没有（PRD-G）。
输入需要一份已过 spec-review 的 impl-plan（PRD-A、PRD-H）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按用户 2026-11-24 的问答写出 spec-ticket 的前瞻式 PRD |
| 2026-11-24 | 按审阅改 PRD-D（本地路径）、PRD-G（保留 Jira）、PRD-I（改指向清单） |
