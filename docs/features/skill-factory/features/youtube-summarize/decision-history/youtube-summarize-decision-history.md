---
feature: youtube-summarize
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# youtube-summarize — 决策记录

本篇按时间倒序记录 `youtube-summarize` 这个 skill 的关键决策。
需求见 [PRD](../prd/youtube-summarize-prd.md)，设计见 [design](../design/youtube-summarize-design.md)。
skill-factory 层面的旧记录在 [parent decision history](../../../decision-history/skill-factory-decision-history.md)（条目 0063、0064）。
2026-07-18 的决策都发生在会话 ee946b73 里，4 次提交前后只隔约 9 分钟。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-A | 2026-08-02 | personal-skills 的合并推迟到下一轮；两个 YouTube skill 合成 `/youtube` 只记下，不动 |
| ARD-B | 2026-07-18 | 原始转写一律先用标题、描述和评论精校；元数据提前到转写之前抓 |
| ARD-C | 2026-07-18 | 所有转写都失败时，第三层只用元数据和评论写总结，不出文字稿 |
| ARD-D | 2026-07-18 | 加截图加 OCR 一层抓硬字幕，用 EasyOCR 识别中英文，只在需要时跑 |
| ARD-E | 2026-07-18 | 先用字幕接口拿字幕；没有字幕再用 yt-dlp 下载音频，交给 Whisper 的 base 模型转写 |
| ARD-F | 2026-07-18 | skill 放在 skill factory 的 personal-skills 下，业务项目只把它列为推荐 skill |
| ~~ARD-G~~ | ~~2026-07-18~~ | ~~首版只用浏览器读网页上的标题、描述和评论来写总结~~ 已被 [ARD-E](#ard-e) 取代 |

## Evidence Appendix

### ARD-A

理由：用户合并 skill 时说"youtube skill 也是压缩， 变成一个， 然后每次问你要干什么"（8903e04e，2026-08-02，history.jsonl）（PRD-J）。
合并 commit 6086424 的设计写明 `personal-skills/` 的合并另开一轮，两个 YouTube skill 合成 `/youtube` "noted but not touched"。
被否决的方案：在同一轮里合并。为什么推迟，属于 UNKNOWN；用户随后回的"B"指什么，也没有保存。
出处：commit 6086424；[parent design](../../../design/skill-factory-design.md) 的 Out of Scope (personal-skills) 一节。

### ARD-B

理由：用户说音频和截图转出的文本"本不能直接用"，要结合聊天和 metadata description "review 一下文本，correct 以下文本"（PRD-F）。
agent 回复"Whisper和OCR的识别错误率不低，特别是中英文混着讲房贷术语的时候"，并重写了 skill（ee946b73，2026-07-18）。
为了给精校提供上下文，抓元数据和评论被提到转写之前，成为 Step 2。
精校提示词里的规则（不改说话人的观点、不加原文没有的内容、拿不准的用方括号标出）由 agent 写入，用户没有逐条确认。
被否决的方案：直接用 Whisper 或 OCR 的原始输出。出处：commit d64e05c。
随后的实测里，一条中文视频精校约改了 30 处，例如把"BrayJL"改回社区名"Bridgeland"（同一会话）。

### ARD-C

理由：用户原话"如果在都失败就是tier3"（PRD-E）。
首版那种"只读网页"的做法被保留下来，改作兜底的第三层。
被否决的方案：转写失败就报错退出。第三层只出总结、不出文字稿，是 agent 的选择。出处：ee946b73（2026-07-18）；commit d64e05c。

### ARD-D

理由：用户说"我有好的显卡"，没有字幕时要退到"音频下载，或者视频截图， 抓字母"（PRD-D）。
agent 先检查本机 OCR 工具，再加入 Tier 2b：用 ffmpeg 每 10 秒抽一帧，EasyOCR 以中文简体加英文识别（ee946b73，2026-07-18）。
"只有 Whisper 结果稀疏或用户确认有硬字幕时才跑 OCR"这条限制由 agent 写入，用户没有说过。
被否决的方案：每一帧都做 OCR（SKILL.md 的 Anti-Patterns 一节）。出处：commit b04f00a。

### ARD-E

理由：用户问"有没有能先下载理解字母， 下载，提取视频音频，然后转文本的skill"（PRD-C）。
agent 先试了用 yt-dlp 直接下载字幕，发现"很多视频没有字幕"；又搜到 youtube-transcript-api 可以免登录取字幕（ee946b73，2026-07-18）。
同一段里 agent 现场装了 Whisper，用一条中文视频跑通了下载加转写（同一会话）。
被否决的方案：只靠 yt-dlp 下载字幕。选 `base` 模型的理由，对话里没有，属于 UNKNOWN。
出处：commit cd0e658。

### ARD-F

理由：agent 判断"skill should be created"在 skill-factory 项目里，并在那里提交（ee946b73，2026-07-18；commit db0261d）。
用户随后说"把skill 放到initiative 里面就行了"，agent 把它登记为该 initiative 的推荐 skill（同一会话）（PRD-I）。
业务仓库 mfangdai-video 的 CLAUDE.md 至今把它列在 Key Skills 里。
被否决的方案：把 skill 文件复制进业务项目。用户这句话是否就是这个意思，没有再确认，见 design 的 QUES-G。

### ARD-G

理由：用户要一个"总结理解视频内容"的 skill（PRD-B）。agent 用 Playwright 打开视频页面，读标题、描述、评论来推断内容。
agent 自己承认它"不能获取语音转录文字"，并提议加字幕（ee946b73，2026-07-18）。
被否决的方案：先到 GitHub 找现成 skill（PRD-A）。agent 没有汇报搜索结果，为什么没有采用现成方案，属于 UNKNOWN。
出处：commit db0261d。约 5 分钟后被 ARD-E 的三层转写取代（commit cd0e658）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 youtube-summarize 的决策 |
