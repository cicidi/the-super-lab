---
feature: multi-model-team
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# multi-model-team — 需求

本篇从过去的对话和提交记录里，整理用户对 `multi-model-team` 这个 skill 的需求。
opencode 会话存在本机 opencode.db，下文按会话 id 前缀引用。
实现见 [design](../design/multi-model-team-design.md)。
决策的来由见 [decision-history](../decision-history/multi-model-team-decision-history.md)。

## Overview

multi-model 指一个团队里不同角色用不同的大模型。
本 skill 让"架构师"模型分析并拆分任务，几个"工人"子 agent 实现，最后架构师审查。
子 agent 指由主 agent 派生、只做一件子任务的 agent。
需求起点是 2026-07-13 的一次 opencode 会话（ses_0a0d1e98）。
用户原话是"create a team"，任务来了先由 glm5.2 当架构师"analyze and split the task"。
子 agent 用 deepseek v4 pro，做完后"glm 5.2 review the worker"，并问能否在 opencode 里跑（同一会话）。

## Goals and Success Metrics

目标一：架构师拆分、工人实现、架构师审查，端到端走通。
用户在访谈里把这一条选作成功标准（ses_0a0d1e98，2026-07-14）。
目标二：质量优先，正确性比速度重要（PRD-G）。
成功指标：UNKNOWN。对话里没有可量化的指标，也没有找到这个 skill 被实际调用过的记录。

## User Stories

- 作为开发者，我想把一个大任务交给一个团队：一个模型负责拆分和审查，另一个模型负责写代码。
- 作为开发者，我想在 opencode 里直接用这个团队，不用自己手动分派。
- 作为开发者，工人卡住时，我希望它先自己重试几次，实在不行再上报。

## Functional Requirements

**PRD-A 架构师用 GLM 分析和拆分。** 用户原话："use glm5.2 as the architect analyze and split the task"。现在用 glm-5.4（multi-model-team ARD-K）。
出处：ses_0a0d1e98（2026-07-13）。

**PRD-B 多个工人用 DeepSeek v4 Pro。** 用户要"create serveral sub agent to work on the task"。
工人"use deepseek v4 pro"（ses_0a0d1e98，2026-07-13）。

**PRD-C 做完由架构师（GLM）审查。** 用户原话："once the job done , glm 5.2 review the worker"。
出处：ses_0a0d1e98（2026-07-13）。

**PRD-D 在 opencode 里运行。** 用户问"is that possible run this in the opencode ?"（ses_0a0d1e98，2026-07-13）。
agent 查了 opencode 文档后回答可以：每个 agent 能单独指定模型（同一会话）。

**PRD-E 大任务才触发。** 访谈问哪些说法该触发本 skill，用户只选了一项（ses_0a0d1e98，2026-07-14）。
那一项是大任务：如"build a full feature""implement X system"。
当前 SKILL.md 还列了"use the team""break this down"等用户没选的说法，见 design 的 QUES-A。

**PRD-F 工人自己重试 3 次再上报。** 访谈问失败时怎么办，用户选了"workers retry up to 3 times, then escalate"。
出处：ses_0a0d1e98（2026-07-14）。

**PRD-G 质量优先。** 访谈让用户给五个取舍因素定权重，用户选了 Quality-first（ses_0a0d1e98，2026-07-14）。
权重是：准确 0.50，速度 0.15，边界情况 0.20，可读性 0.05，工具集成 0.10。

**PRD-H 提交并安装到各 AI 工具。** 用户先问"这个skill 在aicowork 了嘛？"，然后说"提交部署，安装"。
出处：ses_0a0d1e98（2026-07-14）；结果是 commit 56f3e00。

## Out of Scope

单文件小改、少于 3 步的小修、没有可独立子任务的任务，都不用本 skill（SKILL.md 的 When NOT to Use 一节）。
对话里没找到用户划这条范围的原话，出处属于 UNKNOWN。

## Resources Needed

需要 GLM（现为 glm-5.4，ARD-K）和 DeepSeek v4 Pro 两个模型的访问权限（PRD-A、PRD-B）。
用户的 GLM 5.2 走 Z.ai 订阅："change my default model to glm 5.2 use Z.ai"（ses_0d8c6356，2026-07-03）。
opencode 的配置里要有 architect 和 worker 两个 agent（PRD-D）。人力上，用户要批准一次拆分方案（见 design）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 multi-model-team 的 PRD |
| 2026-11-24 | PRD-A、PRD-C 的模型改为 glm-5.4（ARD-K） |
