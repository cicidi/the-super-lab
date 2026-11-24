---
feature: youtube-research
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# youtube-research — 需求

本篇从过去的对话和提交记录里，整理用户对 `youtube-research-pipeline` 这个 skill 的需求。
子 feature 叫 youtube-research，和 skill 名不同，原因见 [decision-history](../decision-history/youtube-research-decision-history.md) 的 ARD-A。
实现见 [design](../design/youtube-research-design.md)。
Claude Code 会话按 `~/.claude/history.jsonl` 里会话 id 的前八位引用，行号写作 `L<行号>`。

## Overview

用户在做一个讲美国房产的 YouTube 频道，项目是 `~/project/mfangdai-video`。
用户这样介绍项目："do research and convert research to youtube video transcripts"（ee946b73，2026-07-18，L1297）。
第一个题目是"The impact of AI on home prices"（同一会话，L1295）。
2026-07-18 晚上，用户在会话 b1cdd2d6 里用一串步骤做完这个题目，再要求把这串步骤做成 skill。
这串步骤是：补充调研、找带出处的数据、反方辩论、写口语文字稿、输出 HTML（L1334）。
产出的 skill 叫 `youtube-research-pipeline`，放在 `personal-skills/`（commit d7723a2）。

## Goals and Success Metrics

目标一：把一次性的流程变成能反复用的 skill。用户原话"先把这个总成可以复用的skill 然后跑这个research"（b1cdd2d6，L1334，原文有错别字，已按意思改正）。
目标二：任何题目都能用，不只房价。用户说"这个agent 不是只做这一个topic 的"（L1338）。
目标三：产出一份用户能照着读的视频稿，配好图表和图片（L1334、L1352）。
成功指标：UNKNOWN。对话里没有给出可量化的指标。

## User Stories

- 作为 YouTube 博主，我给一个题目，想拿到一份带数据、带出处、口语化的视频稿。
- 作为 YouTube 博主，我手上有一叠截图或幻灯片，想先转成文字，再在上面补充调研。
- 作为读者，我打开最终的 HTML，就像读一篇普通网页文章，图表会动，图片能当视频配图。

## Functional Requirements

**PRD-A 通用题目，由 AI 决定画什么图。** 用户说要"根据不同的需求，不同的topic，不同的数据，让ai 决定生成什么图"（b1cdd2d6，L1338）。

**PRD-B 数据必须有出处。** 用户原话"所有的数据必须有出处，搜索最新的网站，和论文，可以截图"（L1334 第 2 条）。

**PRD-C 三个子 agent 分头调研，再汇总。** 子 agent（subagent）指主 agent 派出去、各自独立干活的 agent。
用户说"deepresearch 用3个subagent 分别做，然后汇总结果"（L1337）。

**PRD-D 反方辩论。** advocate（反方）指专门挑毛病、找反例的一方。用户要求"advocate skill 讨论"（L1334 第 3 条）。
辩论的记录"应该在discussion 里面"（L1341）。

**PRD-E 口语化的文字稿。** 用户说文字"不是那种很论文形式的，而是很生活化的口气"（L1334 第 4 条）。
原因是用户"会照着这个文档读"，视频长 10 到 20 分钟（同一条）。

**PRD-F HTML 是最终产物。** 用户要"最终输出html，支持数据生成的动画，截图嵌在html 里面"（L1334 第 5 条）。
文字稿也放进这个 HTML；它是一个普通网页，用户读的时候"就是一个普通读者"（L1340）。
HTML"应该在prd 里面"（L1341）。

**PRD-G 文档位置按项目的文档约定。** 用户两次说按 doc-organize 放文档（L1334 第 6 条、L1339）。
doc-organize 在 2026-11-04 改名为 spec-organize，约定写在 SPEC-STANDARD.md（commit c44e983）。

**PRD-H 先把图片转成文字。** 同一会话里，用户先用 pic-to-txt 提取 `slides/` 里的文字（L1331）。
接着要求在这份文字上"继续做research"（L1333）。pic-to-txt 因此成了流程的第 0 步（pic-to-txt 的 PRD）。

**PRD-I 用 scatterbrain 主题。** scatterbrain 是一套暖色、像便利贴贴在软木板上的网页模板。
用户要求 HTML 背景、图片和图表"使用这个颜色的主题风格"，并给了模板链接（L1351）。

**PRD-J 每段配一张图。** 用户要"每段话都给我生成一个有意思的图片，或者google 搜索图片，作为以后视频的配图"（L1352）。
例子：讲商业大楼空置，就找美国商业大楼空置的图（同一条）。
图要从搜索结果里单独抽出来，不要把多张结果拼成一张（L1353）。截图不要黑色背景，要占满画面（L1354）。

**PRD-K 另派一个子 agent 审图。** 用户说每次放的图"请用另一个subagent 审核以下看是否符合"（L1355）。

**PRD-L 补充用户已有的调研。** 用户的第一步是"帮我补充 继续做research"，对象是已有的 `slides/the-impact-of-ai-on-home-prices.md`（L1333）。
用户点名用 superpowers:brainstorming 做这一步（同一条）。

## Out of Scope

只要调研、不要视频稿时不用本 skill；只要 OCR 时改用 pic-to-txt；改已有的稿子时直接改 HTML（SKILL.md 的 When NOT to Use 一节）。
完全没有数据可画图的题目也不用本 skill（同一节）。这几条范围没有找到用户的原话，出处属于 UNKNOWN。
把本 skill 和 youtube-summarize 合成一个 `/youtube`，2026-08-02 被推迟（youtube-summarize 的 ARD-A）。

## Resources Needed

工具：能并行派子 agent 的 agent；WebSearch；Playwright MCP 用来截图（SKILL.md Phase 1、Phase 3+4）。
HTML 运行时要从网上加载 Chart.js 和 Google Fonts（SKILL.md 的 Design System 一节）。
第 0 步要用 pic-to-txt 的 `ocr.py`，需要装好 pic-to-txt（PRD-H）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从会话 b1cdd2d6 和提交记录反推 youtube-research 的 PRD |
