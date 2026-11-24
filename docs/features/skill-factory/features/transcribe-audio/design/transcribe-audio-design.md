---
feature: transcribe-audio
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# transcribe-audio — 本地显卡音频转文字

本篇说明 `transcribe-audio` 这个 skill 现在怎么工作。
源文件：`personal-skills/transcribe-audio/SKILL.md`（commit ee5f3d5），与 hackathon-video-gen 仓库 commit ca6bb23 的版本完全相同。
下文把 hackathon-video-gen 简称 hvg。

## Problem Statement

用户手里有 m4a 等录音，想得到文字稿（PRD-A）。
没有本 skill 时，create-video-workflow 收集素材只能读文字类素材，音频只能记为缺口。
现在它的 Phase 1 把音频交给本 skill（见 DSGN-G）。
用户有一块好显卡，不想为转写按分钟付钱（PRD-C）。

## Solution

一个只含 SKILL.md 的 skill，指导 agent 在本机调用 Whisper 命令行工具。
流程分五步：查显卡、处理输入、转写、清理、展示结果。没有自带脚本，也不需要 API key（PRD-C）。

## User Stories

- 作为用户，我说"transcribe this"并给一个 m4a，几分钟后拿到文字稿（PRD-A）。
- 作为用户，我有一段中文采访视频，想要带时间戳的中文字幕（SKILL.md 的 Full 例子，PRD-E）。
- 作为 create-video-workflow，Phase 1 遇到音频时交给本 skill，拿回文字再汇总（PRD-D）。

## Implementation Decisions

skill 不写代码，只给出命令和判断规则，由 agent 在终端里执行。
写法改编自 openclaw 项目的 `openai-whisper` skill（SKILL.md 的 Sources 一节；PRD-B）。
Whisper 首次运行会把模型下载到本机缓存，之后离线可用（openclaw 那份 skill 的说明）。

## Design

**DSGN-A 先查显卡。** 用 `nvidia-smi` 查有没有 NVIDIA 显卡（PRD-C）。
没有时提醒用户：CPU 上会慢 5 到 10 倍，应改用 `tiny` 或 `base` 这类小模型。

**DSGN-B 处理输入。** 视频文件（mp4、webm、mkv）先用 ffmpeg 抽出音轨，存成临时 mp3（PRD-A）。
m4a、mp3、wav 直接交给 Whisper。多个文件时用一个简单的 bash 循环批量处理。
没有 ffmpeg 时，请用户自己先把音频抽出来。

**DSGN-C 转写并选模型。** 命令是 `whisper <文件> --model <模型> --output_format <格式> --output_dir <目录>`（PRD-A、PRD-C）。
`--language` 可选；不写时 Whisper 自动识别语言（PRD-E）。
模型从小到大有 tiny、base、small、medium、large，另有可选的 turbo；越大越准，也越慢、越占显存。
默认英文用 medium，中文或中英混合用 large，用户可以改（decision-history 的 ARD-C）。
输出格式有四种：txt 纯文本、srt 带时间戳的字幕、tsv 带时间戳的表格、all 一次输出全部。

**DSGN-D 清理文字稿。** Whisper 在静音段有时会重复同一句话，要删掉（PRD-A）。
整段连成一块时，按停顿或句末分段；可以借 tsv 里的时间间隔判断停顿。
还要删掉模型凭空编出的字幕套话，例如"Thanks for watching"。

**DSGN-E 展示结果。** 告诉用户字数、预计阅读时间、识别出的语言，并预览前 10 行（PRD-A）。
同时提供换模型或指定语言重跑的选项。文字明显不对（语言错、乱码）时，显式加上 `--language` 重跑（PRD-E）。

**DSGN-F 质量门。** 四项检查：有显卡或已提醒用户；音频文件存在且可读；输出非空且通顺；语言符合预期（抽查前几行）。

**DSGN-G 与 create-video-workflow 的衔接。** 在 hvg 里，create-video-workflow 的 Phase 1 把音频，以及抽出音轨的视频，交给本 skill（hvg commit ca6bb23；PRD-D）。
2026-11-24 起，本仓库的 create-video-workflow 也补上了这段分流（[create-video-workflow 的 ARD-P](../../create-video-workflow/decision-history/create-video-workflow-decision-history.md#ard-p)）。

## Testing Decisions

本 skill 没有自动测试或评测集，`personal-skills/transcribe-audio/` 下只有 SKILL.md 一个文件。
是否转得准，目前靠 DSGN-F 的质量门和人工抽查。
1de9cb65 里没有看到用真实录音跑过一次再提交的记录，属于 UNKNOWN。

## Out of Scope

需要区分谁在说话（speaker diarization，说话人分离）时不用本 skill；Whisper 命令行不标说话人。
内容本来是文字、YouTube 已有字幕、噪音或口音极重、没有显卡时，也不用或要降级（SKILL.md 的 When NOT to Use 一节）。

## Further Notes

需求见 [PRD](../prd/transcribe-audio-prd.md)，决策见 [decision-history](../decision-history/transcribe-audio-decision-history.md)。
上游调用方见兄弟 feature [create-video-workflow](../../create-video-workflow/design/create-video-workflow-design.md)。
skill-factory 整体设计的技术选择表里也记了"Whisper（本地 GPU）"一行，见 [parent design](../../../design/skill-factory-design.md)。

## Alternatives Considered

调用 OpenAI 的云端转写接口：被否决，用户要求本地显卡（ARD-B、ARD-D）。
只在 Phase 1 里写死转写命令，不单独做 skill：被否决（ARD-E）。
扩展已有的 youtube-summarize：没有被讨论过；它的第二层退路也用 Whisper 转写，见 QUES-B。

## Drawbacks

没有显卡时会很慢，而且 SKILL.md 只给提醒，不会自动换小模型。
不能区分说话人，多人对话的稿子需要人工标注。
本 skill 与 youtube-summarize 各写了一套 Whisper 用法，一个用命令行，一个用 Python 的 `base` 模型。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| Whisper 编出原音频里没有的句子 | DSGN-D 删除常见套话；DSGN-F 要求人工抽查 |
| 批量处理时都写到同一个临时 mp3，后一个覆盖前一个 | SKILL.md 没有处理，见 QUES-D |
| large 模型显存不够而失败 | 模型表写了显存需求，用户可改用更小的模型 |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 用户说的"full transcript"指什么（PRD-A）？ | SKILL.md 只有 `--output_format all` 可能对应 | cicidi | no |
| QUES-B | 要不要把转写合到用户"已有的那个 skill"里，而不是另起一个（PRD-B）？ | 现在是独立 skill，与 youtube-summarize 的 Whisper 退路重复 | cicidi | no |
| QUES-C | 本仓库的 create-video-workflow 要不要补上 hvg ca6bb23 的 Phase 1 路由（PRD-D）？ | 已补上（create-video-workflow 的 ARD-P） | cicidi | no |
| QUES-D | 批量处理时，临时音频文件要不要按输入文件命名？ | SKILL.md 写死一个临时路径 | cicidi | no |
| QUES-E | webm 算音频还是视频？ | 描述里列为音频，DSGN-B 里列为视频 | cicidi | no |

## Reversibility

所有改动都落在 git 跟踪的 `personal-skills/transcribe-audio/SKILL.md`，用 `git revert` 即可撤回。
hvg 里还有一份相同的副本，两边要分别撤回。已安装到 `~/.claude/skills/` 的副本，须重跑 `install.sh` 才同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 transcribe-audio 的 design，引用 PRD-A 到 PRD-E |
| 2026-11-24 | DSGN-G 和 QUES-C：本仓库 create-video-workflow 已补上 Phase 1 分流 |
