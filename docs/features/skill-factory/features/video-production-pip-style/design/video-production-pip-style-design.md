---
feature: video-production-pip-style
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# video-production-pip-style — 画中画引用式视频制作指南

本篇说明 `video-production-pip-style` 这个 skill 现在怎么工作。
源文件：`personal-skills/video-production-pip-style/SKILL.md`（commit 9e4fb21 加入本仓库，之后没有改动）。
目录下只有 SKILL.md 一个文件。

## Problem Statement

用户在做一个房产类 YouTube 频道，看中一位博主"讲话人加大量引用"的视频形式，想照着做（PRD-A、PRD-B）。
但这种形式由哪些画面组成、各占多少时间、背景怎么做，用户并不清楚，还问了能不能用绿幕（PRD-C）。

## Solution

先按用户要求每 10 秒截一帧，量化样例视频的风格（PRD-D）。
再把结果写成一份制作指南：设备、背景、PiP 规格、五个制作阶段、分镜模板和检查清单（PRD-E）。
PiP 指讲话人缩成角落小框、主画面放引用素材的画面形式。

## User Stories

- 作为创作者，我写稿时就标出哪里要放引用，剪辑时照着标记做 PiP。
- 作为创作者，我按检查清单从拍摄走到导出，不漏掉来源标注等步骤。

## Implementation Decisions

本 skill 只有文字指南，没有脚本，也不调用任何工具（decision-history 的 ARD-D）。
指南里的比例和位置数字全部来自一支样例视频的分析（ARD-E）。
详细的逐帧统计不在本仓库，而在 mfangdai-video 项目的 `docs/superpowers/specs/2026-07-18-andrei-jikh-style-analysis.md`（ARD-B）。

## Design

**DSGN-A 何时使用。** 适合需要大量引用图片、片段、文章和数据，又要讲话人一直在画面里的观点分析类视频（PRD-A、PRD-E）。
纯口播、录屏教程、几乎不剪辑的视频不适用。触发词包括"pip video production"和"视频制作风格"。

**DSGN-B 风格基准。** 样例时长 30 分 47 秒，每 10 秒一帧共 185 帧（PRD-D）。
分类结果：PiP 占 74%，全屏讲话 6%，无人全屏素材 2%，空背景过渡 4%，其他 14%。
PiP 框 97% 出现在右下角。

**DSGN-C 设备与背景。** 设备分最低和推荐两档，最低档是 1080p 摄像头、纯色背景、两盏柔光灯和领夹麦。
背景给两个方案（PRD-C）。方案 A 是实体浅灰背景布，和样例一致，不用抠像。
方案 B 是绿幕，后期抠掉再换成浅灰渐变、品牌色或虚化的办公室。
如果想以绿色作为品牌色，SKILL.md 建议换成饱和度约 30% 的绿色渐变，而不是直接留着抠像用的绿。

**DSGN-D PiP 规格与用法。** PiP 框放右下角，圆角，可加 2px 白边（PRD-B）。
一张场景表规定何时用全屏讲话、何时用 PiP：开头、换段、情绪性结论和结尾用全屏讲话；引用来源、回应素材、讲数据时用 PiP。

**DSGN-E 五个制作阶段。** 第一阶段写稿，用 `[FULL]`（全屏讲话）和 `[PIP]`（画中画）标记每个引用点，目标是每 10 到 30 秒换一个新画面（ARD-F，PRD-A）。
第二阶段先把整篇稿当口播录完。第三阶段按稿件分段收集截图、图表和视频片段。
第四阶段在 DaVinci Resolve 里剪：引用素材放下层轨道全屏，讲话人放上层轨道缩小到右下角（PRD-B）。
讲话人缩小时用 0.5 秒交叉溶解，引用之间直接硬切；SKILL.md 还给了缩放关键帧和"保存为宏"的做法。
第五阶段调音频和画面：人声约 -6 到 -3 dB，背景音乐约 -25 dB 并在说话时自动压低。

**DSGN-F 引用来源标注。** 每个引用都要在屏幕下方、PiP 左侧加一行小字，格式是"Source: 刊物名 — 日期"（PRD-A）。
白字配半透明黑底，随引用淡入，显示时长和引用相同。

**DSGN-G 分镜模板。** 开头一分钟以全屏讲话的钩子起头，随后在 PiP 和全屏之间每 10 秒左右切换。
正文按"论点、两三个引用、自己的分析、反方材料、小结"循环。结尾一分钟全部用全屏讲话（PRD-A、PRD-B）。

**DSGN-H 检查清单与完成标准。** 清单分前期、拍摄、后期三段（PRD-E）。
完成标准有六条：每个 `[PIP]` 段都做了 PiP，每个引用都有来源标注，缩放动画平滑，音频干净，1080p 导出可播放，时长和稿件相符。
SKILL.md 还列了反模式，例如 PiP 框过大、没有来源标注、一分钟才一个引用。

**DSGN-I 相关 skill。** 研究和写稿交给 youtube-research-pipeline，图片转文字交给 [pic-to-txt](../../pic-to-txt/design/pic-to-txt-design.md)，文档整理交给 spec-write（SKILL.md 的 Companion Resources；ARD-G）。
把研究文档做成视频的完整流程见 [create-video-workflow](../../create-video-workflow/design/create-video-workflow-design.md)，音频转文字见 [transcribe-audio](../../transcribe-audio/design/transcribe-audio-design.md)。
本 skill 没有被这两个兄弟 skill 引用，也不引用它们。

**DSGN-J 和用户原意的差距。** 用户要的是"能把我的视频做成他这种类型"（PRD-E），当前 skill 只告诉人怎么做，不处理视频文件，见 QUES-B。
SKILL.md 的 Background Tips 一节直接引用了用户当时的提问，是写给那一次对话的回答（PRD-C）。

## Testing Decisions

本 skill 没有自动测试或评测集。
SKILL.md 里的剪辑参数（缩放比例、位置坐标、宏的做法）在会话里没有在 DaVinci Resolve 中实际验证过，见 QUES-C、QUES-D。
是否好用，目前只能拍一支视频后人工判断。

## Out of Scope

纯口播 vlog、录屏教程、几乎不剪辑的视频（SKILL.md 的 `when_not_to_use`）。
选题研究和写稿（交给 youtube-research-pipeline）。

## Further Notes

需求见 [PRD](../prd/video-production-pip-style-prd.md)，决策见 [decision-history](../decision-history/video-production-pip-style-decision-history.md)。
skill-factory 整体设计见 [parent design](../../../design/skill-factory-design.md)。
逐帧统计、背景色值和转场时间线，见 mfangdai-video 项目里的分析报告（commit 56b2585）。

## Alternatives Considered

只用绿幕：没有采用，改为实体背景首推、绿幕备选（ARD-C）。
用脚本自动合成 PiP：对话里没有讨论，当前是手工指南（ARD-D）。
参考多支视频取平均：对话里没有讨论，当前只用一支样例（ARD-E）。

## Drawbacks

所有数字来自一支视频，换一位博主或换一期节目，比例可能不同。
SKILL.md 里有写给那一次对话的段落（Your Specific Questions），别人用时会觉得突兀。
指南绑定 DaVinci Resolve，用其他剪辑软件的人要自己换算参数。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| PiP 尺寸的几处数字互相矛盾，照做会得到过大的框 | 暂无；见 QUES-C |
| 关键帧坐标和 Inspector 位置用的不是同一套坐标，照抄会放错位置 | 暂无；见 QUES-D |
| 分析报告在另一个项目里，项目删掉后来源就断了 | 本篇和 decision-history 已摘录主要数字；是否搬进本仓库见 QUES-F |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 用户说的"望着"指什么（PRD-A）？ | 不确定；SKILL.md 按新闻文章和社交媒体帖子处理 | cicidi | no |
| QUES-B | "把我的视频做成这种类型"是要指南还是自动工具（PRD-E）？ | 当前只有手工指南 | cicidi | no |
| QUES-C | PiP 框到底多大？ | SKILL.md 同时写了占宽 25% 到 30%、缩放 50% 到 55%、不超过屏幕 25%，三者不一致。原始分析报告也自相矛盾：占宽 25% 到 30%，又写占面积约 25% | cicidi | no |
| QUES-D | 关键帧和宏的参数在 DaVinci Resolve 里是否可用？ | 关键帧用中心点绝对坐标，Inspector 用偏移量，未验证 | cicidi | no |
| QUES-E | 要不要再分析几支视频，校正 74% 等数字？ | 目前只有一支样例 | cicidi | no |
| QUES-F | 分析报告要不要搬进本仓库？ | 目前在 mfangdai-video 项目 | cicidi | no |
| QUES-G | 本 skill 要不要留在 git 里？ | 旧决策 0018 说 personal skills 被 gitignore，但 commit 9e4fb21 已提交它 | cicidi | no |

## Reversibility

所有改动都落在 git 跟踪的 `personal-skills/video-production-pip-style/SKILL.md`，用 `git revert` 即可撤回。
已安装到 `~/.claude/skills/` 的副本，须重跑 install.sh 才同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 video-production-pip-style 的 design，引用 PRD-A 到 PRD-E |
| 2026-11-24 | DSGN-I 改指 spec-write（ARD-G）；QUES-C 补上原始报告的证据 |
