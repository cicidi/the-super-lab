---
feature: multi-model-team
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# multi-model-team — 决策记录

本篇按时间倒序记录 `multi-model-team` 这个 skill 的关键决策。
需求见 [PRD](../prd/multi-model-team-prd.md)，设计见 [design](../design/multi-model-team-design.md)。

skill-factory 层面的旧决策在 [parent decision history](../../../decision-history/skill-factory-decision-history.md)。
opencode 会话按会话 id 前缀引用，数据在本机 opencode.db。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-J | 2026-11-24 | 配置示例的 GLM provider 改为 `zai-coding-plan`；SKILL.md 写明 architect、worker 两个 agent 要用户自己配 |
| ARD-A | 2026-08-02 | 合并 38 个 skill 时，multi-model-team 保持独立，不并入别的 skill |
| ARD-B | 2026-07-14 | 用户没有逐条审阅内容，直接要求提交、推送并部署到各 AI 工具 |
| ARD-C | 2026-07-14 | 采用分析、拆分、分派、审查、整合五个阶段，拆分方案先经用户批准再分派 |
| ARD-D | 2026-07-14 | 取舍权重用 Quality-first：准确 0.50，边界情况 0.20，速度 0.15 |
| ARD-E | 2026-07-14 | 失败时工人先自己重试，最多 3 次，再上报架构师 |
| ARD-F | 2026-07-14 | 成功标准定为端到端：架构师拆分、工人实现、架构师审查 |
| ARD-G | 2026-07-14 | 触发条件只选"大任务"一类，不设成所有任务的默认流程 |
| ARD-H | 2026-07-14 | 命名为 multi-model-team，不用 agent 推荐的 team-orchestrate |
| ARD-I | 2026-07-13 | 架构师用 GLM 5.2，工人用 DeepSeek v4 Pro，靠 opencode 给每个 agent 单独配模型来实现 |

## Evidence Appendix

### ARD-J

理由：用户的 GLM 走 `zai-coding-plan`（`~/.config/opencode/config.json` 的 model 字段），本机没有 `zhipu`。
本机 opencode.json 没有 architect、worker 两个 agent，装上 skill 也不会自动生成。
被否决的方案：保留 `zhipu`；由 skill 去改 `~/.config`。出处：用户 2026-11-24 审阅回复。

### ARD-A

理由：parent design 的合并表把它列在 "Independent — No Merge"，原因是 "Unique multi-model architecture"。
被否决的方案：并入别的编排类 skill。

出处：commit 6086424；[parent design](../../../design/skill-factory-design.md)。同日 93d4a4a 把文件移到 `skills/multi-model-team/`。
发起这次合并的对话没有找到，用户为何保留它独立属于 UNKNOWN。

### ARD-B

理由：agent 给出摘要并问"Does this look good"，用户只问是否已进 ai coworker，然后说"提交部署，安装"（PRD-H）。
被否决的方案：先改内容再发布。

出处：ses_0a0d1e98（2026-07-14）；commit 56f3e00。之后文件内容没有改过，只在 93d4a4a 换了路径。

### ARD-C

理由：五个阶段和"先批准拆分"这道闸由 agent 写入，SKILL.md 的 Sources 说拆分来自 subagent-driven-development。
用户没有逐条确认，见 design 的 QUES-F。

被否决的方案：UNKNOWN，对话里没有讨论别的流程。出处：ses_0a0d1e98（2026-07-14）；commit 56f3e00。

### ARD-D

理由：用户在四组权重里选了 Quality-first，即"maximize correctness"（PRD-G）。完整权重另有可读性 0.05、工具集成 0.10。
被否决的方案：Balanced、Speed-first、Default 三组权重。

出处：ses_0a0d1e98（2026-07-14）；SKILL.md 的 Sources 一节记了这组权重。

### ARD-E

理由：用户在四个失败处理选项里选了"workers retry up to 3 times, then escalate"（PRD-F）。
被否决的方案：架构师重新分析再派；退回单 agent；直接上报用户。

出处：ses_0a0d1e98（2026-07-14）。
当前 SKILL.md 把三个被否决的做法也写成了后备手段，见 design 的 QUES-B。

### ARD-F

理由：用户在四个成功标准里选了端到端一项（Goals 的目标一）。
被否决的方案：以拆分质量、速度、工人代码质量为标准。出处：ses_0a0d1e98（2026-07-14）。

### ARD-G

理由：用户在四组触发语里只选了大任务一组（PRD-E）。
被否决的方案：显式说法（"use the team"等）、拆分说法（"break this down"等）、所有任务默认使用。

出处：ses_0a0d1e98（2026-07-14）。当前 SKILL.md 仍写入了前两组，见 design 的 QUES-A。

### ARD-H

理由：用户在四个候选名里选了 multi-model-team，它强调"多模型"这一点。
被否决的方案：team-orchestrate（agent 推荐）、architect-worker-team、orchestrate-subagents。

出处：ses_0a0d1e98（2026-07-14）。

### ARD-I

理由：模型搭配是用户直接指定的（PRD-A、PRD-B、PRD-C）。agent 查 opencode 文档后确认可以给每个 agent 配不同模型（PRD-D）。
出处：ses_0a0d1e98（2026-07-13）。

用户为何这样分工，原话里没有说，属于 UNKNOWN。被否决的方案：所有角色用同一个模型（UNKNOWN，未讨论）。
背景：2026-06-24 的对比里，DeepSeek V4 Pro 按量价格低于 GLM-5.2（ses_1417bab9），这只是 agent 的分析。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 multi-model-team 的决策 |
| 2026-11-24 | 新增 ARD-J：provider 改为 zai-coding-plan，写明 agent 配置 |
