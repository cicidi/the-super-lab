---
feature: video-production-pip-style
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# video-production-pip-style — 需求

本篇从过去的对话和提交记录里，整理用户对 `video-production-pip-style` 这个 skill 的需求。
实现见 [design](../design/video-production-pip-style-design.md)。
决策的来由见 [decision-history](../decision-history/video-production-pip-style-decision-history.md)。
会话按 id 前 8 位引用；548db334 的全文存在本机 analytics.db 的 `messages` 表，用户原话也在 `~/.claude/history.jsonl`。

## Overview

PiP 是 Picture-in-Picture（画中画）的缩写：主画面放别的内容，讲话人缩成角落里的一个小框。
`video-production-pip-style` 是一份制作指南，教人拍出一种"讲话人加大量引用素材"的 YouTube 视频风格。
需求起点是 2026-07-18 深夜 mfangdai-video 项目里的一段对话（会话 548db334）。
用户贴了一个 YouTube 视频链接，说这个人的视频形式有几个特点，要求据此"做一个能把我的视频做成他这种类型的skill"（同一会话）。
同一晚的另一个会话里，用户说这个项目是把研究变成 YouTube 视频稿，"we are build a youtube influcence chanenl"（ee946b73，2026-07-18）。
用户发起后只说了这一条需求，skill 由 agent 一次写成，会话里没有后续确认。

## Goals and Success Metrics

目标一：把样例视频的形式拆清楚，作为用户自己频道的参照（548db334，2026-07-18）。
目标二：得到一个能复用的 skill，让用户的视频变成同一种风格（同一会话）。
成功指标：UNKNOWN。对话里没有给出可量化的指标。SKILL.md 自带的完成标准见 design 的 DSGN-H。

## User Stories

- 作为 YouTube 创作者，我看中一个博主的视频形式，想知道它由哪些画面组成。
- 作为创作者，我想在讲解中大量引用图片、视频片段和数据，同时观众一直能看到我。
- 作为创作者，我想知道背景要不要用绿幕。

## Functional Requirements

**PRD-A 大量引用外部素材。** 用户观察到的第一个特点是"大量的引用图片， 别人的视频， 或者望着， 数据"（548db334，2026-07-18）。
其中"望着"很可能是语音输入的错字，指什么属于 UNKNOWN，见 design 的 QUES-A。

**PRD-B 引用时讲话人缩小。** 用户原话是"如果引用的时候自己的投降缩小"（548db334，2026-07-18）。
agent 把它理解为讲话人的头像缩小，也就是 PiP。

**PRD-C 背景清晰，问能否用绿幕替换。** 用户原话是"北京做的很清晰。 是不是我们可以用绿色背景，然后用别的替换？"（548db334，2026-07-18）。
"北京"按上下文是"背景"的错字。绿幕指纯绿色的幕布，后期软件可以把绿色抠掉，换成任意背景。
这是一个提问，需要 skill 给出答案。

**PRD-D 每 10 秒截一张图，分析整体风格。** 用户原话是"你每10妙做一个截图， 然后分信息他整个的视频的风格"（548db334，2026-07-18）。
agent 照此对 30 分 47 秒的样例抽了 185 帧（同一会话的最后一条回复）。

**PRD-E 做成 skill，用于用户自己的视频。** 用户要的是"一个能把我的视频做成他这种类型的skill"（548db334，2026-07-18）。
"做成"是指给人看的制作指南，还是能自动处理视频的工具，对话里没有说明，见 design 的 QUES-B。

## Out of Scope

纯口播 vlog、录屏教程、几乎不剪辑的视频，都不用本 skill（SKILL.md frontmatter 的 `when_not_to_use`）。
对话里没找到用户划这条范围的原话，出处属于 UNKNOWN。
研究和写稿不归本 skill，由 youtube-research-pipeline 负责（SKILL.md 的 Companion Resources 一节）。

## Resources Needed

用户自备拍摄设备和剪辑软件；SKILL.md 列了最低和推荐两档设备，剪辑以 DaVinci Resolve 为例。
人力上，剪辑全部由人在剪辑软件里手工完成，本 skill 不调用任何外部服务。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 video-production-pip-style 的 PRD |
