---
feature: find-unknowns
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# research — 决策记录

本篇按时间倒序记录 `research` 这个 skill 的关键决策。
需求见 [PRD](../prd/find-unknowns-prd.md)，设计见 [design](../design/find-unknowns-design.md)。
Claude Code 会话按 `~/.claude/history.jsonl` 里会话 id 的前八位引用。
会话 ca8d23f7 的完整对话存在本机 `~/.coworker/analytics/analytics.db` 的 messages 表。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-M | 2026-11-24 | 加无人值守调研分支（Branch C）、照原样恢复小测验（Branch D）；SDD 仓库里 B5 交给 spec-write |
| ARD-L | 2026-11-24 | 子 feature 名用 find-unknowns，不用 skill 名 research |
| ARD-A | 2026-11-04 | Design spec 分支的输出改为 `docs/features/<feature>/design/<topic>-design.md` |
| ARD-B | 2026-10-30 | SDD 的盲区发现直接用 research 和 grill-with-docs，不新建 skill |
| ~~ARD-C~~ | ~~2026-09-24~~ | ~~输出改为 `docs/features/<feature>/spec/<topic>-spec.md`~~ 已被 [ARD-A](#ard-a) 取代 |
| ARD-D | 2026-08-02 | research 作为 wayfinder 调研（investigate）接口的默认实现 |
| ARD-E | 2026-08-02 | find-my-unknown 和 brainstorming 合成两分支的 research，开头只问一个问题 |
| ARD-F | 2026-08-02 | 合并时删掉实现中、实现后两个阶段和小测验，文件从 264 行压到 147 行；小测验后由 [ARD-M](#ard-m) 恢复 |
| ARD-G | 2026-07-18 | 判定 brainstorming 和 find-my-unknown 互补：前者发散出方案，后者收敛出决策 |
| ARD-H | 2026-07-18 | 访谈做主线，贯穿每个阶段；五种技巧中的三种降为辅助工具 |
| ARD-I | 2026-07-18 | 追问深度按改错代价定，每个话题最多 2 到 3 轮 |
| ARD-J | 2026-07-18 | 命名 find-my-unknown，去掉 ai-coworker- 前缀，放进 skill 仓库 |
| ARD-K | 2026-07-18 | 把 Thariq Shihipar 讲"找出你的未知"的文章转成一个 skill |

## Evidence Appendix

### ARD-M

理由：wayfinder 把 research 当作无人值守的子 agent 调用，要它交回带出处的 markdown 文件（`skills/wayfinder/SKILL.md` 第 124、137、306 行；PRD-M）。
旧的 Step 0 先问用户，两条分支都要访谈，子 agent 会卡住或替用户作答（旧 design 的 QUES-A）。
小测验照 commit 9e4fb21 里 find-my-unknown 的 Quiz 一节恢复：HTML 报告含背景、思路、改动和 3 到 5 道理解题（PRD-N）。
用户用过的"/research 你来考考我"考的是刚讨论的话题，没有代码改动（d8d2da7f），所以题目对象也可以是刚讨论的话题。
B5 在有 `docs/features/spec-driven-development/` 的仓库里交给 spec-write（PRD-O）；其他仓库照旧写文件，ARD-A 的路径仍然有效。
被否决的方案：另造一个调研 skill 给 wayfinder 用；小测验重新设计成一问一答。前者违背 ARD-B 的"不新建 skill"，后者没有历史依据。
出处：用户 2026-11-24 审阅回复；commit 6086424（删除小测验）、9e4fb21（原文）。

### ARD-L

理由：SDD 的命名规则（[document-standard 的 DSGN-K](../../../../spec-driven-development/features/document-standard/design/document-standard-design.md)）不许新名字和已有 feature 撞车。
`research` 和已有的 `docs/features/discovery-research` 撞车（[skill catalog](../../../design/skill-factory-design-skill-catalog.md)）。
被否决的方案：沿用 skill 名做子 feature 名；`research-skill`（和已有子 feature `skill` 撞车）；给 skill 改名。skill 名保持不变，只有规格目录换名。
出处：用户 2026-11-24（会话 80291c19）"其他几个按照你说的修"，即采用推荐名 find-unknowns。

### ARD-A

理由：commit c127ef7 加了"五篇文档"检查，设计文档统一放 `design/` 目录（PRD-I）。
被否决的方案：沿用 `spec/` 目录。出处：commit c127ef7。讨论这次改动的会话没有找到，属于 UNKNOWN。

### ARD-B

理由：SDD 的 PRD-H 要求优先用现有工具；research 已有"发现未知"分支（PRD-K）。
被否决的方案：专门新建一个盲区发现 skill。出处：SDD decision-history 的 ARD-L。

### ARD-C

理由：项目把 initiative 一词改成 feature，路径随之改名（commit c2b3f22，PRD-I）。
被否决的方案：保留 `docs/<initiative>/spec/`。后来被 ARD-A 取代。

### ARD-D

理由：用户要求 wayfinder 依赖的 skill 都是可替换的接口，并说"对于ai -cowork 我有自己的research"（d8d2da7f，2026-08-02）。
被否决的方案：调研接口也用 mattpocock 原版。出处：commit 7c11a7b；`skills/wayfinder/SKILL.md` 接口表的 investigate 一行（PRD-J）。
wayfinder 把它当作不需要人参与的子 agent 来调用，和当时先问用户的做法有冲突；ARD-M 加了 Branch C 解决。

### ARD-E

理由：用户嫌 skill 太多，问二者相似度后答"合并"，并要求开头问清走哪条分支（8903e04e，2026-08-02；PRD-A）。
被否决的方案：两个 skill 各自独立，这是 ARD-G 当时的结论。出处：commit 6086424；parent design 合并表第 10 行。

### ARD-F

理由：UNKNOWN。用户说过合并时"不要原封不动保留"（PRD-B），但没有点名删哪些内容。
commit 6086424 删掉的有：四类未知的表、实现中的访谈、实现后的审查和小测验、反模式表、`source` 出处字段。
被否决的方案：保留 find-my-unknown 完整版（commit 9e4fb21 里的 264 行）。是否有意删减属于 UNKNOWN，见 design 的 QUES-C。
小测验在 2026-11-24 由 ARD-M 恢复；其余删掉的内容仍未恢复。

### ARD-G

理由：用户让 agent 对比二者"互补还是重叠"；agent 的结论是互补，"不是谁比谁好，而是前后手"（ca8d23f7，2026-07-18）。
该会话在 analytics.db 的 session_summaries 里记为用户认可这个结论。被否决的方案：二选一，只留一个。
两周后的 ARD-E 把二者合成一个 skill，但仍分成两条分支，没有推翻"互补"这个判断。

### ARD-H

理由：用户问"五选一什么意思"，随后说"每个阶段"都要用访谈方式（PRD-C）。
用户再要求"把 1 2 4 作为辅助手段加回去"（PRD-G）。第 5 种"写实现计划"变成结尾交给 writing-plans。
被否决的方案：五种技巧按情况五选一。出处：ca8d23f7（2026-07-18）。

### ARD-I

理由：用户说 backend、API、data model 要问深，LLM provider 这类不用深，问了 2 到 3 轮就换话题（PRD-F）。
"连续两次回答'你看着办'就停止访谈"这条由 agent 写入，用户没有逐条确认，见 design 的 QUES-E。
被否决的方案：所有问题同样深度。出处：ca8d23f7（2026-07-18）。

### ARD-J

理由：agent 先起名 ai-coworker-find-my-unknown，用户要求"去掉前缀"（PRD-L）。
同一会话定下：通用 skill 放 skill 仓库，和 ai-coworker 深度绑定的才放 ai-coworker 项目。
被否决的方案：留在 ai-coworker 的 `skills/` 下（最初 fable-guide 的位置）。
出处：ca8d23f7（2026-07-18）。首次入库在 commit 9e4fb21（2026-07-23），它是一次 luma-event-scout 提交，顺带把这个文件带了进来。

### ARD-K

理由：用户发来文章链接，说"读这个文章，帮我转变称一个skill"（ca8d23f7，2026-07-18）。
最初叫 fable-guide，放在 ai-coworker 项目（同一会话）。被否决的方案：UNKNOWN，对话里没有讨论别的做法。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 research 的决策 |
| 2026-11-24 | 加 ARD-L（子 feature 名 find-unknowns）和 ARD-M（Branch C、Branch D、B5 交给 spec-write） |
