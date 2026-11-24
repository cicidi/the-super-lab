---
feature: video-production-pip-style
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# video-production-pip-style — 决策记录

本篇按时间倒序记录 `video-production-pip-style` 这个 skill 的关键决策。
需求见 [PRD](../prd/video-production-pip-style-prd.md)，设计见 [design](../design/video-production-pip-style-design.md)。
skill-factory 层面的旧决策在 [parent decision history](../../../decision-history/skill-factory-decision-history.md)。
会话按 id 前 8 位引用，548db334 的全文在本机 analytics.db 的 `messages` 表。
ARD-B、ARD-C、ARD-D、ARD-F 都由 agent 在同一次回复里做出，用户在会话里没有逐条确认。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-A | 2026-07-23 | skill 随一次 luma-event-scout 的提交进入本仓库的 `personal-skills/` |
| ARD-B | 2026-07-18 | skill 写进 skill-factory 的 `personal-skills/`，分析报告留在 mfangdai-video 项目 |
| ARD-C | 2026-07-18 | 背景首推实体浅灰背景布，绿幕作为可替换品牌背景的备选 |
| ARD-D | 2026-07-18 | 做成给人看的手工制作指南，以 DaVinci Resolve 为例，不做自动处理 |
| ARD-E | 2026-07-18 | 风格参数全部取自一支样例视频的 185 帧程序分析 |
| ARD-F | 2026-07-18 | 写稿时用 `[FULL]` 和 `[PIP]` 标记预先规划每个引用点 |

## Evidence Appendix

### ARD-A

理由：UNKNOWN。commit 9e4fb21 的说明只写了 luma-event-scout 的改动，同一提交里新增了本 skill 的 366 行 SKILL.md。
被否决的方案：UNKNOWN。
旧决策 0018 说 personal skills 被 gitignore（[parent decision history](../../../decision-history/skill-factory-decision-history.md)），本 skill 却已提交进 git，见 design 的 QUES-G。
出处：commit 9e4fb21（2026-07-23）。

### ARD-B

理由：UNKNOWN。用户没有指定存放位置，agent 在最后一条回复里列出两个位置。
skill 在 `~/project/skill-factory/personal-skills/video-production-pip-style/SKILL.md`，分析报告在 mfangdai-video 的 `docs/superpowers/specs/2026-07-18-andrei-jikh-style-analysis.md`。
agent 同时在 mfangdai-video 的 CLAUDE.md 里登记了这个 skill 命令。
被否决的方案：UNKNOWN。出处：548db334（2026-07-18）；mfangdai-video commit 56b2585；该项目的 memory 文件 `video-production-pip-style-skill.md`。

### ARD-C

理由：用户问能否用绿幕再替换（PRD-C）。分析报告测得绿色占优的像素一直低于 5%，没有抠像痕迹，于是判断样例用的是实体浅灰背景。
agent 的回答是两条路：实体背景布更简单，和样例一样；绿幕更灵活，可换成品牌色渐变。
被否决的方案：只用绿幕。出处：548db334 最后一条回复；mfangdai-video 的分析报告 Background Analysis 一节。

### ARD-D

理由：UNKNOWN。用户说"把我的视频做成他这种类型"（PRD-E），没有说是指南还是工具。
agent 写出的是设备清单、剪辑步骤和检查清单，所有剪辑由人在 DaVinci Resolve（一款视频剪辑软件）里完成。
被否决的方案：用脚本自动合成 PiP 画面。对话里没有讨论过这条，是否被有意否决属于 UNKNOWN，见 design 的 QUES-B。
出处：548db334（2026-07-18）；SKILL.md 的 Production Workflow 一节。

### ARD-E

理由：用户要求"每10妙做一个截图"后分析整个视频的风格（PRD-D）。
agent 下载样例，每 10 秒抽一帧，共 185 帧，再按颜色和版面逐帧分类，得出 PiP 占 74%、其中 97% 在右下角等数字。
被否决的方案：参考多支视频取平均。对话里没有提到，属于 UNKNOWN，见 design 的 QUES-E。
出处：548db334（2026-07-18）；分析报告的 Frame Type Distribution 一节。

### ARD-F

理由：分析报告的 Production Implications 一节认为引用密度高，每个引用点必须事先规划，剪辑师才知道哪里要做 PiP。
这一条由 agent 从分析中推出，用户没有提过（PRD-A、PRD-B）。
被否决的方案：UNKNOWN。出处：mfangdai-video 的分析报告；SKILL.md 的 Phase 1 一节。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 video-production-pip-style 的决策 |
