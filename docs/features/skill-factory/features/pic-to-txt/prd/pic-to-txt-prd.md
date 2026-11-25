---
feature: pic-to-txt
type: prd
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# pic-to-txt — 需求

本篇从过去的对话和提交记录里，整理用户对 `pic-to-txt` 这个 skill 的需求。
实现见 [design](../design/pic-to-txt-design.md)。
决策的来由见 [decision-history](../decision-history/pic-to-txt-decision-history.md)。
会话按 id 前 8 位引用；已删除的会话从 analytics.db 的 messages 表取回。

## Overview

OCR（optical character recognition，光学字符识别）指从图片里认出文字。
`pic-to-txt` 先对一个文件夹的截图做 OCR，再交给 LLM 修正，得到一份干净的文档。
需求起点是 2026-07-18 的一个视频研究项目（会话 b1cdd2d6）。
用户说"做一个skill， 提炼视频里面的文字，首先用图像识别的工具 识别文字，然后再用llm 优化"。
当晚它就处理了一组英文幻灯片截图（同一会话）。
随后它成为 youtube-research-pipeline 的第 0 步（同一会话；该 skill 的 SKILL.md）。

## Goals and Success Metrics

目标一：一个文件夹的图片变成一份可编辑的文档，放回同一文件夹（b1cdd2d6，2026-07-18）。
目标二：OCR 的错字由 LLM 修掉，原始 OCR 结果不直接交付（同一会话）。
成功指标：UNKNOWN。对话里没有给出准确率或耗时之类的量化指标。

## User Stories

- 作为做视频研究的人，我想把一组幻灯片截图变成文字稿，再接着做研究。
- 作为用户，我只说"把图片里的文字提取出来"，agent 就该用这个 skill。
- 作为用户，我拍了一组手机照片，想要一份核对过、挑过错的文字稿。

## Functional Requirements

**PRD-A 一个文件夹一份文档，就地输出。** 用户原话："转化好的文档放在当前folder 里面一般来说一个folder的图片 就是一个文档"（b1cdd2d6，2026-07-18）。

**PRD-B 先识别，再用 LLM 优化。** 用户要求"首先用图像识别的工具 识别文字，然后再用llm 优化"（b1cdd2d6，2026-07-18）。
2026-11-11 用户又要求把照片"转文字稿,并且核对,挑错 让文件合理"（会话 78981854）。
核对和挑错正是 LLM 这一步的工作。

**PRD-C 用开源 OCR 库，按语言选引擎。** 用户提到"好像google 有个什么ocr 还是什么开源的图像识别lib"（b1cdd2d6，2026-07-18）。
agent 列出 Tesseract、EasyOCR、PaddleOCR 三个引擎让用户选。
之后 agent 复述结论"中文用 PaddleOCR（最强中文），英文用 EasyOCR"（同一会话）。
用户点选的原始答案没有存档，只有 agent 的复述，见 design 的 QUES-G。

**PRD-D 按文件名排序。** agent 问每个文件夹的图片是否按文件名排序，复述的结论是"按文件名排序"（b1cdd2d6，2026-07-18）。

**PRD-E 作为个人 skill 存放。** agent 问放在 personal-skills 还是项目本地。
最终放进 `personal-skills/pic-to-txt/`（b1cdd2d6；commit 1e029ae）。

**PRD-F 说"提取图片文字"就该用上。** 2026-07-26 用户让 agent 把一组图片"导成prd 文档"。
agent 却自己设计了一份 PRD（会话 a2dcb9ad）。
用户纠正："我要你把图片里面的文字写提取出来，我有skill pic 2 txt"（同一会话）。
这条需求由这次纠正推出。2026-11-24 补上了这类触发词（ARD-G）。

## Out of Scope

手写字、单张图片、PDF、讲究版面的表格和表单，都不用本 skill（SKILL.md 的 When NOT to Use 一节）。
对话里没找到用户划这条范围的原话，出处属于 UNKNOWN。

## Resources Needed

本机至少装好 PaddleOCR 或 EasyOCR 之一；EasyOCR 默认用 GPU（PRD-C）。
LLM 修正由运行 skill 的 agent 自己完成，创建当晚就是这样跑的（b1cdd2d6）。
人力上，用户在 OCR 前确认一次图片数量和顺序（SKILL.md 的 Quality Gates）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 pic-to-txt 的 PRD |
| 2026-11-24 | PRD-F 记录补上的触发词（ARD-G） |
