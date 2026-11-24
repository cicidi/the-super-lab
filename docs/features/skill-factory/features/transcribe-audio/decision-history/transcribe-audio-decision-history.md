---
feature: transcribe-audio
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# transcribe-audio — 决策记录

本篇按时间倒序记录 `transcribe-audio` 这个 skill 的关键决策。
需求见 [PRD](../prd/transcribe-audio-prd.md)，设计见 [design](../design/transcribe-audio-design.md)。
skill-factory 层面的旧记录在 [parent decision history](../../../decision-history/skill-factory-decision-history.md)（条目 0065）。
所有决策都发生在 2026-07-22 的会话 1de9cb65 里，前后约 4 分钟。hvg 指 hackathon-video-gen 仓库。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-A | 2026-07-22 | 同一份 SKILL.md 同时提交到 hvg 和 skill factory；只在 hvg 里把 Phase 1 的音频路由到它 |
| ARD-B | 2026-07-22 | 改用本地 Whisper 命令行在显卡上跑，不调用 OpenAI 的云端转写接口 |
| ARD-C | 2026-07-22 | 默认模型：英文用 medium，中文或中英混合用 large，用户可改 |
| ~~ARD-D~~ | ~~2026-07-22~~ | ~~首稿包装 openclaw 的 transcribe.sh，走 OpenAI 转写接口~~ 已被 [ARD-B](#ard-b) 取代 |
| ARD-E | 2026-07-22 | 做成独立的 skill，同时接进 create-video-workflow 的 Phase 1 |

## Evidence Appendix

### ARD-A

理由：agent 的收尾总结说两个仓库都已提交并推送（1de9cb65 的最后一条回复）。
hvg commit ca6bb23 新增 skill，并改了 create-video-workflow 的 Phase 1 和 hvg 的 CLAUDE.md。
本仓库 commit ee5f3d5（当年在 skill-factory 仓库）只新增了 `personal-skills/transcribe-audio/SKILL.md`，两份内容完全相同。
被否决的方案：只放在 hvg。用户有没有要求同时放进 skill factory，没有找到原话，属于 UNKNOWN。
后果：本仓库的 create-video-workflow 副本没有带上 ca6bb23 的 Phase 1 改动，见 design 的 QUES-C。

### ARD-B

理由：用户问"does whiper user token ?"，得知云端按音频分钟收费后说"我要用本地gpu 不要用模型"（PRD-C）。
agent 回复"明白——用本地 GPU 跑 Whisper CLI，不走 API"，并重写了 skill（1de9cb65，2026-07-22）。
被否决的方案：OpenAI 的 `whisper-1` 或 `gpt-4o-transcribe` 接口（ARD-D）。
出处：1de9cb65；history.jsonl 同日的两条用户输入；hvg commit ca6bb23。

### ARD-C

理由：UNKNOWN。模型表和默认值由 agent 在重写时写入，用户没有逐条确认。
它沿用了 openclaw `openai-whisper` skill 的示例命令（`--model medium`），SKILL.md 的 Sources 一节写了"adapted pattern"。
被否决的方案：openclaw 那份安装下默认的 `turbo` 模型；SKILL.md 只把它列为"如果装了"的选项。
出处：1de9cb65 的第二次 Write；`~/project/openclaw/skills/openai-whisper/SKILL.md`。

### ARD-D

理由：agent 找到 openclaw 的 `openai-whisper-api` skill 和它的 `transcribe.sh`，认为那就是用户说的"previous video to text script"（PRD-B）。
首稿描述写的是"using OpenAI's transcription API"，支持 gpt-4o-transcribe、whisper-1 和区分说话人的模型。
被否决的原因：用户要求本地显卡（PRD-C），首稿在约 30 秒后被整份重写，从未提交。
出处：1de9cb65 的第一次 Write（tool_calls 表，2026-07-22）。被 ARD-B 取代。

### ARD-E

理由：agent 用三选一问用户：新建 skill、只写进 Phase 1、两者都做。
用户选择的原文没有保存；agent 接着说"你要的是：独立 transcribe skill + 集成到 Phase 1"（1de9cb65，2026-07-22）。
被否决的方案：只在 Phase 1 里写死转写命令；或者扩展用户已有的那个 video-to-text skill（PRD-B）。
出处：1de9cb65；hvg commit ca6bb23。因为只有复述，这条的置信度低于 80%。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 transcribe-audio 的决策 |
