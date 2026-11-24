---
feature: youtube-research
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# youtube-research — 从题目到视频稿 HTML

本篇说明 `youtube-research-pipeline` 这个 skill 现在怎么工作。
源文件：`personal-skills/youtube-research-pipeline/SKILL.md`（commit d7723a2 新建，70959e9 加图片和主题，c2b3f22 改输出目录）。
2026-11-24 修了 `ocr.py` 路径和旧 skill 名（ARD-B、ARD-C）。

## Problem Statement

用户做 YouTube 频道，每期视频都要调研、找数据、写稿、配图（PRD 的 Overview）。
2026-07-18 用户手动走了一遍这些步骤，步骤多，顺序也固定（b1cdd2d6，L1334）。
每次重做费时，而且容易漏掉出处或反方观点（PRD-B、PRD-D）。

## Solution

一个 skill 串起五个阶段：图片转文字、三路调研、汇总、反方辩论、写成一个 HTML 网页（PRD-A）。
HTML 是唯一交付物，里面有口语化的文字稿、会动的图表和配图（PRD-F）。

## User Stories

- 作为 YouTube 博主，我说"把这个题目做成视频"，skill 从调研一路做到 HTML。
- 作为 YouTube 博主，我给一个截图文件夹，skill 先 OCR 再调研。

## Implementation Decisions

本 skill 只有一个 SKILL.md，没有自己的脚本，全靠 agent 读文字执行。
唯一的外部脚本是 pic-to-txt 的 `ocr.py`（ARD-B）。
调研、汇总、辩论、出 HTML、审图都交给子 agent 做，主 agent 负责调度（ARD-I、ARD-E）。

## Design

**DSGN-A 五个阶段。** 顺序是：Phase 0 图片转文字、Phase 1 三路调研、Phase 1b 汇总、Phase 2 反方辩论、Phase 3+4 写 HTML、Phase 5 整理文件（PRD-A）。
题目不限；同一套流程用于任何题目（ARD-J）。

**DSGN-B Phase 0：图片转文字。** 只有用户给了图片文件夹时才跑；已有文字就跳过（PRD-H）。
命令是 `python3 ~/.claude/skills/pic-to-txt/ocr.py <folder> --lang auto`（ARD-B）。
这是 `install.sh` 装好的副本；没装时改用本仓库的 `personal-skills/pic-to-txt/ocr.py`（ARD-B）。

**DSGN-C Phase 1：三路调研。** 同时派出三个子 agent，题目和已有材料相同，方向不同（PRD-C、ARD-I）。
A 查学术论文，B 查行业和市场数据，C 查新闻、政策和趋势；已有的调研文字一并交给它们做底（PRD-L）。
每个数据都要附 URL 出处，关键图表用 Playwright 截图存到 `screenshots/`（PRD-B）。
三个 agent 的原始结果分别写到 `raw/agent-*-output.md`。

**DSGN-D Phase 1b：汇总。** 三个都做完后，第四个 agent 合并结果、去重、交叉核对出处，并标出互相矛盾的地方（PRD-B）。
产出两个文件：`research/` 下的调研文档，和列出全部出处的 `.evidence.md`。

**DSGN-E Phase 2：反方辩论。** 另派一个 agent 扮演反方，逐条反驳主要结论（PRD-D）。
它要问：数据是不是挑过的、方法有没有问题、怀疑者会怎么说，并上网找反例。
记录写到 `raw/advocate-discussion/`（ARD-H）。

**DSGN-F Phase 3+4：文字稿。** 一个 agent 把调研和辩论写成一个 HTML（PRD-F、ARD-H）。
语气像跟朋友聊天，长度约 2500 到 5000 词，读完 10 到 20 分钟（PRD-E）。
结构是：开场钩子、背景、主要发现、反方观点、结论、出处；每个数字旁边都标出处。

**DSGN-G 配图和审图。** 每个主要段落找一张真实照片当配图，不用插画或 logo（PRD-J、ARD-F）。
用 Playwright 打开单张图片的地址，只截 `img` 元素，存为 `screenshots/video-<段落名>.png` 并记下出处。
截完后另派一个子 agent 逐张审核：切不切题、够不够具体、可不可信、能不能当视频画面；不合格就换关键词重找（PRD-K、ARD-E）。
全文至少 5 到 7 张图。

**DSGN-H 图表。** agent 看数据的形状选图表：时间序列用折线图，排名用柱状图，占比用环形图，地区数据用带色条的表格（PRD-A、ARD-J）。
图表一律用 Chart.js，并带 1 秒的入场动画（PRD-F）。

**DSGN-I 主题。** 默认用 scatterbrain 主题：暖色纸张底、软木板背景、便利贴样式的段落、拍立得样式的截图（PRD-I、ARD-G）。
SKILL.md 列出了配色表和四种 Google 字体，其中一种用于中文标题。

**DSGN-J Phase 5：整理文件。** 所有产物放在 `docs/features/<topic>/` 下，HTML 存为 `prd/presentation.html`（PRD-F、PRD-G、ARD-D）。
SKILL.md 要求文件位置符合 spec-organize 的约定，即 SPEC-STANDARD.md（ARD-C）。最后在 INDEX.md 里加一条。
这个目录结构和 SPEC-STANDARD.md 是否一致，见 QUES-B。

**DSGN-K 质量门。** 三个调研 agent 必须并行，全部完成后才汇总（PRD-C）。
每个数据必须有出处；每个主要结论至少有一条反方意见；HTML 必须有效、手机上能读，文字稿要读出声来检查是否口语（PRD-B、PRD-D、PRD-E）。

**DSGN-L 名字。** skill 名是 `youtube-research-pipeline`，规格所在的子 feature 名是 `youtube-research`（ARD-A）。
两个名字不同，是因为 skill 名里的 `pipeline` 和 SDD 的 `pipeline` 子 feature 撞车（document-standard 的 DSGN-K 命名规则）。
skill 名没有改，已安装的副本和触发词都不受影响。

## Testing Decisions

本 skill 没有自动测试或评测集，目录下只有 SKILL.md 一个文件。
首次真实运行就是创建它的那次：2026-07-18 用"The impact of AI on home prices"跑通（b1cdd2d6）。
opencode 的 skill 使用计数里记了 1 次使用，最后一次在 2026-07-23（`~/.local/share/opencode/opencode.db`，会话 ses_043c755b 读到的计数文件）。
那次用在哪个题目、效果如何，属于 UNKNOWN。

## Out of Scope

不要视频稿的调研、只做 OCR、改已有稿子、没有数据可画的题目，都不用本 skill（SKILL.md 的 When NOT to Use 一节）。
和 youtube-summarize 合成 `/youtube` 已推迟（youtube-summarize 的 ARD-A）。

## Further Notes

需求见 [PRD](../prd/youtube-research-prd.md)，决策见 [decision-history](../decision-history/youtube-research-decision-history.md)。
本 skill 在 skill-factory 里的位置见 [skill catalog](../../../design/skill-factory-design-skill-catalog.md)。
OCR 的细节见 [pic-to-txt design](../../pic-to-txt/design/pic-to-txt-design.md)。

## Alternatives Considered

一个 agent 串行调研：被否决，改为三个子 agent 并行再汇总（ARD-I）。
按题目写死图表：被否决，改为按数据形状选（ARD-J）。
文字稿和 HTML 分开：被否决，文字稿嵌在 HTML 里（ARD-H）。
写死 skill 仓库里的 `ocr.py` 路径：被否决，改为安装位置加仓库退路（ARD-B）。

## Drawbacks

HTML 从网上加载 Chart.js 和字体，离线打开时图表和字体会缺失（DSGN-H、DSGN-I）。
图片取自网上搜索，版权只靠记下出处，没有检查授权（DSGN-G）。
SKILL.md 里的配图关键词表是房价题目的例子，换题目时 agent 需要自己改写（DSGN-G）。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| pic-to-txt 没装，第 0 步找不到 `ocr.py` | SKILL.md 写明退回本仓库的 `personal-skills/pic-to-txt/ocr.py`（ARD-B） |
| 三个调研 agent 引用了过时或错误的数据 | 汇总时交叉核对出处，反方辩论再挑一遍（DSGN-D、DSGN-E） |
| 搜到的图和段落意思不符 | 另派子 agent 审图，不合格就重找（DSGN-G） |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 用户点名用 superpowers:brainstorming 补充已有调研（PRD-L），要不要在流程里加这一步？ | SKILL.md 没有调用 brainstorming，只把已有材料交给三个调研 agent | cicidi | no |
| QUES-B | `docs/features/<topic>/` 下的 `research/`、`screenshots/`、`prd/presentation.html` 是否符合 SPEC-STANDARD.md？ | 未核对；SPEC-STANDARD.md 的 `prd/` 放 PRD 文档，不放 HTML | cicidi | no |
| QUES-C | 三路调研的数据源（Moody's、Zillow、FHFA 等）偏房产，换题目时要不要改成通用写法？ | SKILL.md 写的是房产数据源的例子 | cicidi | no |

## Reversibility

所有改动都落在 git 跟踪的 `personal-skills/youtube-research-pipeline/SKILL.md`，用 `git revert` 即可撤回。
已安装的副本须重跑 `install.sh` 才同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 youtube-research 的 design，含 ARD-B、ARD-C 的修复 |
