---
feature: youtube-summarize
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# youtube-summarize — YouTube 视频转写与总结

本篇说明 `youtube-summarize` 这个 skill 现在怎么工作。
源文件：`personal-skills/youtube-summarize/SKILL.md`（commit d64e05c 定稿，之后没有再改过）。

## Problem Statement

做频道调研时，要知道几十个同类频道的视频讲了什么，一条条看完太慢（PRD-B）。
很多视频没有字幕，只有声音或烧进画面的硬字幕（PRD-D）。
语音识别和文字识别的结果错误很多，尤其是中英混说的专业术语，原样不能用（PRD-F）。

## Solution

一个 skill，给一个链接，按六步走：取视频 id、抓元数据、分层转写、精校、总结、交付。
转写分三层，从最快的开始试，失败才往下一层退（PRD-C、PRD-D、PRD-E）。

## User Stories

- 作为频道运营者，我贴一个链接，拿回一份总结和一份修正过的文字稿。
- 作为研究者，视频没有字幕时，我不用自己下载和转写。

## Implementation Decisions

整个流程写在一份 SKILL.md 里，没有附带脚本；代码片段由运行 skill 的 agent 照着执行。
Whisper 是 OpenAI 开源的语音识别模型；OCR（光学字符识别）指从图片里认出文字。
EasyOCR 是一个支持中英文的开源 OCR 库。yt-dlp 是下载 YouTube 音视频的命令行工具。
兄弟 skill [pic-to-txt](../../pic-to-txt/design/pic-to-txt-design.md) 创建时，agent 读过本 skill 的结构作为参考（会话 b1cdd2d6，2026-07-18）。

## Design

**DSGN-A 触发和范围。** 用户给出 YouTube 链接，想知道内容、要 TL;DR 或要一份干净的文字稿时触发（PRD-B）。
不用于 Shorts、超过 2 小时的视频、下载视频本身和非公开视频（SKILL.md 的 When NOT to Use 一节）。

**DSGN-B 取视频 id。** 从链接的 `v=` 参数或 `youtu.be/` 短链路径里取出视频 id（Step 1）。

**DSGN-C 抓元数据和评论。** 用 Playwright 浏览器打开视频页，取标题、频道和订阅数、播放量、上传日期、完整描述、按相关度排的前 20 到 30 条评论（Step 2）。
这些信息有两个用途：第三层兜底，以及精校时的上下文（PRD-E、PRD-F）。

**DSGN-D 第一层：字幕接口。** 用 youtube-transcript-api 取手动或自动生成的字幕，拼成带时间戳的全文（PRD-C）。
成功就把它当作准确文本，跳过第二层。

**DSGN-E 第二层 a：音频加 Whisper。** 没有字幕时，用 yt-dlp 下载 mp3，交给 Whisper 的 `base` 模型转写，有显卡就用显卡（PRD-C、PRD-D）。
Whisper 不指定语言时会自动识别，中文、英文和中英混说都能转（PRD-H）。

**DSGN-F 第二层 b：截图加 OCR。** 针对硬字幕：用 ffmpeg 每 10 秒抽一帧，EasyOCR 以中文简体加英文识别每一帧（PRD-D、PRD-H）。
两层都有结果时合并。只有 Whisper 结果稀疏或用户确认有硬字幕时才跑这一层（Anti-Patterns 一节）。

**DSGN-G 第三层：只用元数据。** 前面都失败时，只用 DSGN-C 抓到的信息写总结，不出文字稿（PRD-E）。

**DSGN-H 精校。** 把原始转写、标题、描述、评论、频道主题一起交给 LLM，要求按上下文改正听错的术语（PRD-F）。
规则：不改说话人的观点；不加原文没有的内容；拿不准的改动用方括号标出；保留时间戳；输出纯文本。
任何第二层的结果都必须经过这一步，原始输出不能当最终文字稿。

**DSGN-I 结构化总结。** 从精校后的文字稿（第三层时从元数据）写出五块：一句话核心观点、3 到 7 条要点、目标观众、可操作建议、值得引用的话或数据（PRD-B）。

**DSGN-J 交付。** 返回三样东西：存成文本文件的文字稿、内联的 markdown 总结、处理报告（用了哪几层、耗时、置信度说明）（PRD-G）。
SKILL.md 没有规定文字稿存到哪里；保存文件只是 NICE 级要求，见 QUES-C。

**DSGN-K 质量门。** 必须先试第一层再下载；精校前必须先抓元数据；第二层之后必须精校；必须报告用了哪几层。
必须支持中英文；处理完必须删掉音频和截帧等临时文件；视频超过 1 小时前必须提醒用户。
超过 2 小时的视频，没有用户确认不处理（Anti-Patterns 一节）。

**DSGN-L 存放位置。** skill 文件在本仓库的 `personal-skills/youtube-summarize/`，业务项目只把它列为推荐 skill（PRD-I）。

**DSGN-M 尚未落地的需求。** 到 GitHub 找现成 skill 的结果从未汇报（PRD-A），见 QUES-A。
和 `youtube-research-pipeline` 合成一个、开头先问要做什么的 `/youtube`，2026-08-02 推迟后没有再做（PRD-J），见 QUES-B。

## Testing Decisions

本 skill 没有自动测试或评测集，目录下只有 SKILL.md 一个文件。
创建当晚用两条视频人工跑过：一条中文视频没有字幕，走第二层 a 并精校；一条英文视频有字幕，走第一层（ee946b73，2026-07-18）。
当时服务器上的 PyTorch 是 CPU 版，Whisper 跑在 CPU 上；后来重装显卡版才用上 GPU（同一会话）。

## Out of Scope

Shorts、超过 2 小时的视频、下载视频本身、非公开或有年龄限制的视频，都不用本 skill（SKILL.md 的 When NOT to Use 一节）。
批量处理整个频道也不在本 skill 里；当晚的 40 个频道批量转写是 agent 另写脚本完成的（ee946b73，2026-07-18），见 QUES-E。

## Further Notes

需求见 [PRD](../prd/youtube-summarize-prd.md)，决策见 [decision-history](../decision-history/youtube-summarize-decision-history.md)。
本地音频转写另有兄弟 skill [transcribe-audio](../../transcribe-audio/design/transcribe-audio-design.md)，两者的 Whisper 用法重复，那边的 QUES-B 已经记下。
首版只读网页的写法可用 `git show db0261d` 查看。

## Alternatives Considered

只读网页上的标题、描述和评论：首版这样做，约 5 分钟后被三层转写取代（ARD-G、ARD-E）。
只靠 yt-dlp 下载字幕：agent 实测后发现很多视频没有字幕，改用字幕接口加 Whisper 退路（ARD-E）。
直接用 Whisper 或 OCR 的原始输出：被否决，改为必须精校（ARD-B）。

## Drawbacks

Whisper 的 `base` 模型固定写死，中文准确率有限；兄弟 skill transcribe-audio 中文默认用 `large`，见 QUES-D。
SKILL.md 内部有不一致：Tier Selection 一节建议"大多数视频跑第二层 a"，质量门却要求先试第一层；提醒线是 1 小时，拒绝线是 2 小时，见 QUES-F。
示例代码也对不上：yt-dlp 输出 `/tmp/yt_audio_<id>.mp3`，Whisper 却读 `/tmp/yt_audio.mp3`；第二层 b 要的视频文件没有给下载命令。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| 清理临时文件时把文字稿也删了 | 当晚真的发生过，用户追问文字稿去哪了（PRD-G）；SKILL.md 没有规定保存位置，见 QUES-C |
| 文字稿全挤在一行，看起来像没转完 | 当晚一条 30 分钟视频就这样，用户问"why transcript so short"（ee946b73，history.jsonl）；SKILL.md 没有排版规则 |
| 机器有显卡但 PyTorch 是 CPU 版，Whisper 很慢 | 当晚重装显卡版解决（ee946b73）；SKILL.md 只说"有显卡就用"，不检查 |
| 精校时 LLM 编造内容 | 提示词禁止加原文没有的内容，拿不准的用方括号标出（DSGN-H） |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 要不要补做 GitHub 搜索，和现成的开源 skill 比一比（PRD-A）？ | 从未汇报过搜索结果 | cicidi | no |
| QUES-B | 要不要把本 skill 和 youtube-research-pipeline 合成 `/youtube`（PRD-J）？ | 2026-08-02 推迟，用户回的"B"含义不明 | cicidi | no |
| QUES-C | 文字稿要不要改成必须保存，并规定保存位置（PRD-G）？ | 现在是 NICE 级，位置没写 | cicidi | no |
| QUES-D | 转写要不要改用 transcribe-audio，或按语言选模型？ | 现在固定用 `base` | cicidi | no |
| QUES-E | 要不要支持一次处理一个频道最近一年的视频？ | 当晚用户要过，agent 另写了脚本，skill 没有 | cicidi | no |
| QUES-F | 第一层与第二层 a 的先后、1 小时和 2 小时两条线，以哪个为准？ | SKILL.md 前后不一致 | cicidi | no |
| QUES-G | "把skill 放到initiative 里面"是不是指只登记为推荐 skill（PRD-I）？ | agent 这样理解，用户没确认 | cicidi | no |

## Reversibility

所有改动都落在 git 跟踪的 `personal-skills/youtube-summarize/SKILL.md`，用 `git revert` 即可撤回。
已安装到 `~/.claude/skills/` 的副本，须重跑 `install.sh` 才同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 youtube-summarize 的 design，引用 PRD-A 到 PRD-J |
