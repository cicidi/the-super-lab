---
feature: create-video-workflow
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# create-video-workflow — 需求

本篇从过去的对话和提交记录里，整理用户对 `create-video-workflow` 这个 skill 的需求。
实现见 [design](../design/create-video-workflow-design.md)，决策见 [decision-history](../decision-history/create-video-workflow-decision-history.md)。
会话按 Claude Code 会话 id 前 8 位引用；ai-coworker 项目的会话全文存在本机 analytics.db 的 messages 表。

## Overview

`create-video-workflow` 把用户做好的研究文档，变成面向特定听众的内容：演示、自媒体视频、网站或多种格式的组合。
它是个人 skill，放在 `personal-skills/` 下。
它最早是 hackathon-video-gen 项目里的短视频 skill（commit 35b8eda，2026-04-18）：一个创业故事想法，生成 60 秒竖屏视频。
2026-07-22 用户要求做一个 skill 驱动的 workflow：研究做完后，按给的文档做 presentation 或自媒体视频（会话 1de9cb65）。
同日它被重写成 7 个阶段的 v3 版，并复制到本仓库（commit c4159a9）。

## Goals and Success Metrics

目标一：同一批研究材料，能按听众和传播渠道产出不同风格的内容（1de9cb65，2026-07-22）。
目标二：流程灵活，"worflow 不要定的太死"（同一会话）。
目标三：发布前先验收，确认听众接收到的信息和最初的 goal 对得上（同一会话）。
成功指标：UNKNOWN。对话里没有可量化的指标；验收方式见 PRD-I。

## User Stories

- 作为内容创作者，我做完研究后，想把几份文档直接变成一个 YouTube 视频或一套演示。
- 作为工程师，我想把内部文档做成给团队看的演示，语气要专业，不像论文。
- 作为发布者，我想在内容上线前，先看到一个模拟听众的观后感，再决定发不发。

## Functional Requirements

**PRD-A 从一份或多份研究文档出发。** 输入是用户给的文档，输出是 presentation 或自媒体播放的视频（1de9cb65，2026-07-22）。

**PRD-B 先想清楚听众。** 用户说做项目通常先考虑"听众是谁，是否有专业的背景"。
还要判断哪些地方要讲细节，哪些可以默认大家都知道（同一会话）。

**PRD-C 文稿口语化，风格跟着传播渠道走。** transcript 指要念出来的文稿。用户说演讲是口语化的，"不太像论文"。
渠道有 YouTube 类自媒体、网站展出的论文、GitHub demo（1de9cb65，2026-07-22）。
用户随后纠正：风格要结合"以后传播的地方"，并"多加一个公司内部文档"（同一会话）。

**PRD-D 多种产出，按场景选模型。** 产出可以是视频、文字、图片、动画，或几种混合。
可用 seedance、chatgpt、gemini 等不同 API，"根据不同的场景选不同的model"（1de9cb65，2026-07-22）。

**PRD-E 复用视频项目的脚本，流程不定死。** 生成视频、图片、动画时，要走 hackathon-video-gen 项目已有的流程（同一会话）。
生成动画的步骤是 idea、transcript、prompt、再交给生成式 AI。用户确认旧的 Python 脚本"并不是扔掉了"（同一会话）。

**PRD-F 并行生成，按类型合成。** 一个任务可能同时生成多个视频、图片、动画，网站和 markdown 也并行（同一会话）。
合成时看类型：markdown 先留一个 placeholder（占位符），视频则在最后拼成一个文件（同一会话）。

**PRD-G 文档走 doc-organize，每份都要人审。** 用户说生成文档"要使用doc organize skill"。
写每一个文档都是 human in the loop（人参与其中）的讨论和 review（1de9cb65，2026-07-22）。

**PRD-H 按软件工程的阶段来组织。** 用户说 phase 0-2 类似写代码的需求分析和 design，phase 3 是 spec。
phase 4 是具体实施，phase 5 类似 build（同一会话）。
用户还要求核对"前面的生成的spec 文档就是phase 4 的输入"（同一会话）。

**PRD-I 需求文档要有 goal，最后由听众 agent 验收。** goal 指这个 demo 或 presentation 想表达什么（1de9cb65，2026-07-22）。
验收时模拟第一步定下的听众，让这个 agent 写观后感和总结，再和最初的设计、听众、goal 对照（同一会话）。
用户原话："听众agent 必须能听， 读， 看video"。

**PRD-J 验收通过后自动发布。** 用户要求"多加一个deploy"：像 CI/CD 流水线一样，只是部署目标是 YouTube 或抖音等平台的 API。
CI/CD 指代码合入后自动构建和发布的流水线。用户说"我们也需要一个 release 的pipeline"（1de9cb65，2026-07-22）。

**PRD-K 放进视频项目并由它引导，同时进 skill factory。** 用户要求把 skill 放进 hackathon-video-gen 的 skill 目录。
并在那个项目的 CLAUDE.md 里写明"要靠这个skill 引导"（1de9cb65，2026-07-22）。
写完后用户又说"skill 也要放到skill factory"（同一会话；commit c4159a9）。

**PRD-L 视频一段段生成，用上一段的尾帧接下一段。** 用户要求视频逐个生成：前一段最后一个镜头截一张图，作为下一段的开头（会话 5cf6decf，2026-05-01）。
Seedance 是离线任务，提交后返回 task id；用户要求把 task id 和状态记进 task.json，后台轮询更新（会话 18d4bf16，2026-04-19）。

**PRD-M 视频要有人声，不做无声视频。** 用户看到旧 skill 说做 silence 视频，要求"生成要背景说话的"（18d4bf16，2026-04-18）。

**PRD-N 模板可选，不绑死。** 用户说不要绑定在创业者叙事视频上，它只是一个故事模板；workflow 可以"问是否要模板"（18d4bf16，2026-04-18）。
当前 v3 版不再提模板，也不问用户，见 design 的 QUES-C。

## Out of Scope

已有成稿、只需拼一段 30 到 60 秒短视频；只要一份文字摘要；单个 PDF 且无演示意图。这三类不用本 skill。
出处是 SKILL.md 的 When NOT to Use 一节；用户划这条范围的原话没有找到，属于 UNKNOWN。

## Resources Needed

生成视频和图片要 Seedance、Gemini 等模型的 API key（PRD-D）；拼接视频要 ffmpeg（PRD-F）。
发布要各平台的 API 权限，没有时手动上传（PRD-J）。人力上，每个检查点都需要用户审阅（PRD-G）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 create-video-workflow 的 PRD |
