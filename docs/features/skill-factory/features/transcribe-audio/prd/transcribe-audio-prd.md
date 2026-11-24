---
feature: transcribe-audio
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# transcribe-audio — 需求

本篇从过去的对话和提交记录里，整理用户对 `transcribe-audio` 这个 skill 的需求。
实现见 [design](../design/transcribe-audio-design.md)。
决策的来由见 [decision-history](../decision-history/transcribe-audio-decision-history.md)。
会话按 id 前 8 位引用；1de9cb65 的全文存在本机 analytics.db 的 `messages` 表，用户的短回复见 `~/.claude/history.jsonl`。

## Overview

transcript 指把录音里说的话逐字写成的文字稿。
`transcribe-audio` 把 m4a、mp3、wav 等音频文件转成 transcript，用本机显卡上的 Whisper（OpenAI 开源的语音识别模型）来跑。
需求起点是 2026-07-22 深夜的一段对话（会话 1de9cb65），当时用户刚做完 create-video-workflow v3。
用户要求做一个把声音转文字的工具，"convert any m4a file to transcraipt and to a full transacrpit"（同一会话）。
它服务于兄弟 skill [create-video-workflow](../../create-video-workflow/prd/create-video-workflow-prd.md) 的 Phase 1，见 PRD-D。

## Goals and Success Metrics

目标一：任意一个 m4a 录音都能变成文字稿（1de9cb65，2026-07-22）。
目标二：在本机显卡上跑，不调用付费的云端接口（同一会话）。
成功指标：UNKNOWN。对话里没有给出准确率、速度之类的可量化指标。

## User Stories

- 作为创作者，我手里有一个 m4a 录音，想要一份文字稿。
- 作为 create-video-workflow 的使用者，素材里有音频时，我想让它自动变成文字，再汇进素材文档。
- 作为有一块好显卡的用户，我不想为转写按分钟付钱。

## Functional Requirements

**PRD-A 任意 m4a 转成文字稿。** 用户原话是"convert any m4a file to transcraipt and to a full transacrpit"（1de9cb65，2026-07-22）。
"full transcript"具体指什么（全部格式、带时间戳，还是经过整理的完整稿），对话里没有解释，属于 UNKNOWN，见 design 的 QUES-A。

**PRD-B 沿用已有的那个 skill。** 用户说要"like the previous video to text script, that extract audio"，并说"I want to use the same skill"。
随后又补一句"我have skill before"（1de9cb65，2026-07-22）。
agent 找到的是 openclaw 项目里的 `openai-whisper` 和 `openai-whisper-api` 两个 skill（同一会话）。
用户说的"previous video to text script"是不是这两个，还是 youtube-summarize，没有确认，见 design 的 QUES-B。

**PRD-C 用本地显卡，不用云端模型。** 用户先问"does whiper user token ?"，agent 解释了本地免费、云端按分钟计费。
用户随即说"我要用本地gpu 不要用模型"（1de9cb65，2026-07-22，见 history.jsonl）。
这里的"模型"按上下文指 OpenAI 的云端转写接口，因为本地 Whisper 本身也是模型。

**PRD-D 供 create-video-workflow 的 Phase 1 调用。** Phase 1 是那个 skill 收集和整理原始素材的一步。
agent 问用户三选一：新建 skill、只写进 Phase 1、两者都做（1de9cb65，2026-07-22）。
用户选择的原文没有保存；agent 接着复述为"独立 transcribe skill + 集成到 Phase 1"（同一会话），hvg commit ca6bb23 也照此落地。
hvg 是 hackathon-video-gen 仓库的简称。因为只有复述没有原文，置信度不足，列为 UNKNOWN 候选。

**PRD-E 中文和英文都要能转，最好自动识别语言。** 这两条出自更早的一段对话，当时在为 youtube-summarize 设计"没有字幕就下载音频转写"的退路。
用户问"中文英文， 都能转吗？"和"能自动识别语言吗？"，并说"我有好的显卡"（会话 ee946b73 与 history.jsonl，2026-07-18）。
它们是相邻 skill 的需求，用户没有对 transcribe-audio 重说一遍；本篇按背景需求收录。

## Out of Scope

SKILL.md 列出不用本 skill 的情况：内容本来就是文字、YouTube 已有字幕、需要区分说话人、噪音极大或口音极重、没有显卡。
对话里没有找到用户划这些范围的原话，出处属于 UNKNOWN。

## Resources Needed

本机要装 Whisper 命令行工具和 ffmpeg（从视频里抽音频用），最好有 NVIDIA 显卡（PRD-C）。
最大的 `large` 模型约需 10GB 显存（SKILL.md 的模型表）。不需要任何 API key（PRD-C）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 transcribe-audio 的 PRD |
