---
feature: youtube-research
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# youtube-research — 决策记录

本篇按时间倒序记录 `youtube-research-pipeline` 这个 skill 的关键决策。
需求见 [PRD](../prd/youtube-research-prd.md)，设计见 [design](../design/youtube-research-design.md)。
Claude Code 会话按 `~/.claude/history.jsonl` 里会话 id 的前八位引用，行号写作 `L<行号>`。
2026-07-18 的决策都发生在会话 b1cdd2d6 里，两次提交 d7723a2 和 70959e9 前后只隔约 40 分钟。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-A | 2026-11-24 | 子 feature 名用 youtube-research，不用 skill 名 youtube-research-pipeline |
| ARD-B | 2026-11-24 | 第 0 步改用安装位置的 `~/.claude/skills/pic-to-txt/ocr.py`，没装时用本仓库的 `personal-skills/pic-to-txt/ocr.py` |
| ARD-C | 2026-11-24 | SKILL.md 里的 doc-organize 改成 spec-organize（SPEC-STANDARD.md），contrarian-review 注明现在是 spec-review |
| ARD-D | 2026-09-24 | 输出目录从 `docs/initiatives/<topic>/` 改为 `docs/features/<topic>/` |
| ARD-E | 2026-07-18 | 图片截好后，另派一个子 agent 逐张审核是否切题 |
| ARD-F | 2026-07-18 | 每个段落配一张真实照片，用 Playwright 只截图片元素 |
| ARD-G | 2026-07-18 | HTML 默认用 scatterbrain 主题 |
| ARD-H | 2026-07-18 | HTML 是唯一交付物，文字稿嵌在里面；HTML 放 `prd/`，辩论放 `raw/advocate-discussion/` |
| ARD-I | 2026-07-18 | 调研由三个子 agent 并行做（学术、行业数据、新闻），再由第四个 agent 汇总 |
| ARD-J | 2026-07-18 | 不绑定题目，图表类型由 agent 按数据的形状决定 |
| ~~ARD-K~~ | ~~2026-07-18~~ | ~~第 0 步调用 `~/project/skill-factory/personal-skills/pic-to-txt/ocr.py`~~ 已被 [ARD-B](#ard-b) 取代 |
| ARD-L | 2026-07-18 | 把一次房价调研的步骤做成可复用的 skill，放在 `personal-skills/` |

## Evidence Appendix

### ARD-A

理由：SDD 的命名规则（[document-standard 的 DSGN-K](../../../../spec-driven-development/features/document-standard/design/document-standard-design.md)）不许新名字和已有 feature 撞车。
`youtube-research-pipeline` 含有 `pipeline` 这个词，和 SDD 的 `pipeline` 子 feature 撞车（[skill catalog](../../../design/skill-factory-design-skill-catalog.md)）。
被否决的方案：沿用 skill 名做子 feature 名；或者给 skill 改名。skill 名保持不变，只有规格目录换名。
出处：用户 2026-11-24 审阅回复（选定 youtube-research）。

### ARD-B

理由：旧路径指向 `~/project/skill-factory/`，这个目录已经不存在（skill catalog 的 DSGN-AJ；pic-to-txt 的 QUES-F）。
`install.sh` 会把每个 personal skill 整个目录复制到 `~/.claude/skills/<name>/`（walter-worker 的 `setup/install.sh` 第 556 行），所以 `ocr.py` 装好后就在 `~/.claude/skills/pic-to-txt/`。
被否决的方案：写死本仓库的绝对路径，换一台机器或换目录就会失效。本仓库路径只作为没装时的退路。
出处：用户 2026-11-24 审阅回复；`personal-skills/youtube-research-pipeline/SKILL.md` Phase 0。

### ARD-C

理由：doc-organize 和 doc-review 在 commit c44e983（2026-11-04）改名为 spec-organize 和 spec-review。
contrarian-review 早在 commit 6086424（2026-08-02）并入 doc-review，所以现在是 spec-review。
被否决的方案：删掉这些引用。用户要求按文档约定放文件（PRD-G），引用要保留，只换成现在的名字。
Sources 一节是历史说明，保留旧名并在括号里注明新名，不改原意。出处：用户 2026-11-24 审阅回复；commit c44e983。

### ARD-D

理由：项目把 initiative 一词全面改成 feature，本 skill 的输出目录随之改名（commit c2b3f22）。
被否决的方案：保留 `docs/initiatives/<topic>/`。这次是全仓库批量改动，没有找到单独讨论本 skill 的对话。

### ARD-E

理由：用户说每次放的图"请用另一个subagent 审核以下看是否符合"，例子是旧金山房屋的图配不配主题（b1cdd2d6，L1355；PRD-K）。
被否决的方案：由出图的 agent 自己判断。出处：commit 70959e9 的 Image Review Gate 一节。

### ARD-F

理由：用户要每段话都配一张图，当作以后视频的配图（L1352）。
用户又要求把单张图从搜索结果里抽出来（L1353），截图不要黑色背景、要占满画面（L1354；PRD-J）。
SKILL.md 因此用 Playwright 只截 `img` 元素。被否决的方案：截整个搜索结果页。出处：commit 70959e9。

### ARD-G

理由：用户要求 HTML 的背景、图片和图表用 scatterbrain 模板的配色（L1351；PRD-I）。
被否决的方案：首版 d7723a2 里没有指定主题。出处：commit 70959e9。

### ARD-H

理由：用户说文字稿也放进 HTML，这个 HTML 就是一个给普通读者看的网页（L1340）。
用户又说辩论"应该在discussion 里面"，HTML"应该在prd 里面"（L1341；PRD-D、PRD-F）。
被否决的方案：文字稿和 HTML 分成两个文件（SKILL.md 的 Anti-Patterns 一节明确禁止）。出处：commit d7723a2。

### ARD-I

理由：用户说"deepresearch 用3个subagent 分别做，然后汇总结果"（L1337；PRD-C）。
按学术、行业数据、新闻三个方向分工是 agent 的设计，用户没有逐条确认。
被否决的方案：一个 agent 串行调研。出处：commit d7723a2 的 Phase 1 和 Phase 1b。

### ARD-J

理由：用户说这个 agent 不是只做一个题目，要按需求、题目和数据，让 AI 决定画什么图（L1338；PRD-A）。
被否决的方案：按房价题目写死图表。出处：commit d7723a2 的 Chart Selection 一节。

### ARD-K

理由：首版写的路径就是当时 skill 仓库的位置（commit d7723a2）。
后来仓库改名搬家，这个路径失效，被 ARD-B 取代。为什么写成绝对路径，没有找到讨论，属于 UNKNOWN。

### ARD-L

理由：用户在一串步骤的最后要求"先把这个总成可以复用的skill 然后跑这个research"（L1334 第 7 条）。
L1333 的版本写作"把这个变成skill"。被否决的方案：每次手动重做这串步骤。出处：commit d7723a2。
放在 `personal-skills/` 而不是 `skills/`，没有找到用户的原话，属于 UNKNOWN。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：反推 youtube-research 的决策，含 2026-11-24 的路径和改名修复（ARD-A 到 ARD-C） |
