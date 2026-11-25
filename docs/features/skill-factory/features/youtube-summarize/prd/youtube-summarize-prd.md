---
feature: youtube-summarize
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# youtube-summarize — 需求

本篇从过去的对话和提交记录里，整理用户对 `youtube-summarize` 这个 skill 的需求。
实现见 [design](../design/youtube-summarize-design.md)。
决策的来由见 [decision-history](../decision-history/youtube-summarize-decision-history.md)。
会话按 id 前 8 位引用。ee946b73 的全文存在本机 analytics.db 的 `messages` 表；
其中几条排队发出的用户消息只留在 `~/.claude/history.jsonl`，下文注明。日期按美国太平洋时间。

## Overview

transcript 指把视频里说的话逐字写成的文字稿。
`youtube-summarize` 拿到一个 YouTube 链接后，先取得 transcript，修正识别错误，再写一份结构化总结。
需求起点是 2026-07-18 晚上的一个房产视频研究项目（会话 ee946b73，mfangdai-video 仓库）。
用户当时在调研同类频道，要求"在github 上总结归纳youtube视频的skill"（history.jsonl）。
agent 当晚连续 4 次提交，把它从"只读网页"扩成三层转写加精校（commit db0261d、cd0e658、b04f00a、d64e05c）。
兄弟 skill [transcribe-audio](../../transcribe-audio/prd/transcribe-audio-prd.md) 的 PRD-E 也出自这段对话。

## Goals and Success Metrics

目标一：不用看完视频，也能知道视频讲了什么（ee946b73，2026-07-18）。
目标二：没有字幕的视频也能变成文字（同一会话）。
目标三：最后拿到的文字稿是修正过的，可以直接用（同一会话）。
成功指标：UNKNOWN。对话里没有给出准确率、速度之类的可量化指标。

## User Stories

- 作为频道运营者，我想快速知道同类频道的一条视频讲了什么，不想从头看到尾。
- 作为研究者，视频没有字幕时，我仍然想要一份文字稿。
- 作为中文内容创作者，我要的文字稿里，专业术语和中英混说要写对。

## Functional Requirements

**PRD-A 先到 GitHub 找现成的 skill。** 用户先误说成在 YouTube 上找，随即更正："错了 ，在github 上总结归纳youtube视频的skill"。
随后又说"你给我github 搜索， 总结youtube 视频， 总结理解视频内容的skill"（ee946b73，2026-07-18，history.jsonl）。
agent 没有汇报任何 GitHub 搜索结果，直接自己写了一个（commit db0261d），见 design 的 QUES-A。

**PRD-B 归纳和理解视频内容。** 用户要的是"总结理解视频内容"的 skill（ee946b73，2026-07-18，history.jsonl）。
总结分核心观点、要点、目标观众、可操作建议几块，这个格式是 agent 在 db0261d 里写的，用户没有逐条确认。

**PRD-C 先拿字幕，再下载音频转文本。** 用户听完首版"只读网页文字"的原理后问：
"有没有能先下载理解字母， 下载，提取视频音频，然后转文本的skill"（ee946b73，2026-07-18）。
"字母"按上下文是"字幕"的笔误。

**PRD-D 没有字幕时，退到音频或截图。** 用户说"有些视频没有字幕，只是视频里面有字幕，或者音频"（history.jsonl）。
接着说"我有好的显卡，如果没有youtube 的字母，就需要fallback 使用音频下载，或者视频截图， 抓字母"（ee946b73，2026-07-18）。
fallback 指主路走不通时的退路。"视频里面有字幕"指烧进画面、不能关掉的硬字幕。

**PRD-E 全都失败时，还有第三层。** 用户原话："如果在都失败就是tier3"（ee946b73，2026-07-18）。
用户没有说第三层具体做什么；"只用标题、描述和评论来总结"是 agent 在 d64e05c 里定的。

**PRD-F 转出来的文字要先修正，不能直接用。** 用户说音频和截图转出的文本"可能还不是很准"，"本不能直接用"。
要"把视频的聊天， 视频的metadata description 综合， review 一下文本，correct 以下文本"（ee946b73，2026-07-18）。
metadata 指标题、频道、描述这类视频信息。"聊天"按 agent 的落地理解为评论区（commit d64e05c）。

**PRD-G 产出一份文字稿文档。** 同一句话的结尾是"然后生成一个文本的文档"（ee946b73，2026-07-18）。
测试视频的文字稿在清理临时文件时被删，用户追问"刚才转得transcript 呢？"（history.jsonl，同日）。
这说明用户期望文字稿留下来。当前 SKILL.md 把保存文件列为 NICE（可选），见 design 的 QUES-C。

**PRD-H 中文英文都能转，能自动识别语言。** 用户问"中文英文， 都能转吗？"和"能自动识别语言吗？"（ee946b73，2026-07-18，history.jsonl）。
agent 用一条中文视频演示了 Whisper 自动识别出中文（同一会话）。这两条也被 transcribe-audio 的 PRD-E 引为背景。

**PRD-I skill 放进 initiative。** initiative 是用户给一组跨项目工作起的名字，后来改叫 feature。
用户说"把skill 放到initiative 里面就行了"（ee946b73，2026-07-18）。
agent 把它登记为该 initiative 的推荐 skill，skill 文件本身留在 skill factory（同一会话）。
用户的意思是不是这样，没有再确认，置信度不足，见 design 的 QUES-G。

**PRD-J 两个 YouTube skill 合成一个，开头先问要做什么。** 2026-08-02 合并 skill 时，用户说"youtube skill 也是压缩， 变成一个， 然后每次问你要干什么"（8903e04e，history.jsonl）。
用户随后回了一个"B"，B 选项的内容没有保存，属于 UNKNOWN。
合并 commit 6086424 只记下了 `youtube-research-pipeline` 加 `youtube-summarize` 合成 `/youtube`，推迟到下一轮，至今没做。

## Out of Scope

SKILL.md 列出不用本 skill 的情况：60 秒以内的 Shorts、超过 2 小时的视频、要下载视频本身、非公开视频。
对话里没有找到用户划这些范围的原话，出处属于 UNKNOWN。

## Resources Needed

本机要装 youtube-transcript-api、yt-dlp、ffmpeg、openai-whisper 和 easyocr（SKILL.md 的 Prerequisites 一节）。
最好有 NVIDIA 显卡（PRD-D）。抓元数据和评论要用 Playwright 浏览器。不需要 API key。
人力上，用户只给链接；视频超过 1 小时时要回答一次是否继续（SKILL.md 的 Quality Gates）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 youtube-summarize 的 PRD |
