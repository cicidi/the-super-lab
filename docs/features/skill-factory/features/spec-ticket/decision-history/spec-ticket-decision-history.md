---
feature: spec-ticket
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# spec-ticket — 决策记录

本篇按时间倒序记录 `spec-ticket` 这个新 skill 的关键决策；skill 还没有实现。
需求见 [PRD](../prd/spec-ticket-prd.md)，设计见 [design](../design/spec-ticket-design.md)。
skill-factory 层面的旧决策在 [parent decision history](../../../decision-history/skill-factory-decision-history.md)。
所有决策出自用户 2026-11-24（会话 80291c19）的问答，Q 编号是那次问答的题号。
审查报告指 `docs/features/skill-factory/raw/review/2026-11-24-spec-review-spec-ingest-spec-ticket-gaps.md`，R 编号是协调者转来的条目号。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-Q | 2026-11-24 | 复制的 IMPL 原文里相对链接改成仓库根路径（GitHub 为完整网址）；锚点按标题算；GHES 退路也写 Parent 行 |
| ARD-P | 2026-11-24 | Jira 只支持云版（Jira Cloud，REST API v3）；自建版（Data Center）暂不支持 |
| ARD-O | 2026-11-24 | 每个 feature 一张母工单，正文只放 PRD 和 design 的链接；每张 IMPL 工单是它的子工单 |
| ARD-N | 2026-11-24 | 本地夹具的结果由 `tools/check_spec_ticket_fixture.py` 比对期望清单，不用人工清单 |
| ARD-M | 2026-11-24 | PIPE-E-A 闸只看 Blocking 列：`yes` 或 `是` 就停，不判断答案一栏 |
| ARD-L | 2026-11-24 | 依赖标签在整个 IMPL 小节里找；非 IMPL 的依赖文字进报告；已完成的 IMPL 不开工单 |
| ARD-K | 2026-11-24 | GitHub 用 `gh issue create --blocked-by` 一遍建完，被依赖的先建；按标题精确匹配查找全部 issue |
| ARD-J | 2026-11-24 | 本地工单放 `docs/features/<f>/raw/state/spec-ticket/issues/`，文件名即对应关系；`tracker:` 行与 wayfinder 共用 |
| ARD-I | 2026-11-24 | 保留 local、github、jira 三个选项；Jira 做成真实适配器，用 REST API v3 和环境变量 |
| ARD-H | 2026-11-24 | spec-ticket 可用后移除 to-tickets；引用它的 skill 和文档在同一次改动里改指向 |
| ARD-G | 2026-11-24 | 新 skill 命名为 spec-ticket |
| ~~ARD-F~~ | ~~2026-11-24~~ | ~~Jira 先只定义接口；GitHub 用 gh 命令行；本地写 `.scratch/`~~ 已被 [ARD-I](#ard-i)、[ARD-J](#ard-j) 取代 |
| ARD-E | 2026-11-24 | IMPL 与工单的对应表放在 `docs/features/<f>/raw/state/`；重跑只加新 IMPL |
| ARD-D | 2026-11-24 | 最小范围：不做双向同步，不把工单状态写回 spec |
| ARD-C | 2026-11-24 | tracker 配置是 CLAUDE.local.md 里的一行 `tracker: github \| jira \| local`；缺省用本地（协调者推荐） |
| ARD-B | 2026-11-24 | 工单来源是 impl-plan 的 IMPL，一条 IMPL 一张，不再做纵向切片 |
| ARD-A | 2026-11-24 | 自己新建拆工单的 skill，灵感来自 Matt Pocock 的 to-tickets，不沿用原版 |

## Evidence Appendix

### ARD-Q

理由：本地测试发现工单里的相对链接全断，`#impl-x` 也对不上真实标题（标题 `IMPL-B — 读侧` 的锚点是 `#impl-b--读侧`）。
被否决：去掉锚点；不复制原文只放链接。出处：用户 2026-11-24（会话 80291c19）"验证都做完"。

### ARD-P

理由：DSGN-K 本来就按 v3 写；自建版用 v2 和别的认证方式，要另写适配器。被否决：两种都做。出处：用户 2026-11-24（会话 80291c19）"按照你的建议来吧".

### ARD-A

理由：用户说"to-spec to-ticket 我认为我自己应该创建一个 skill 灵感是来此matt pccock"。
被否决的方案：继续用导入的 to-tickets 原版（`skills/to-tickets/SKILL.md`）。
出处：用户 2026-11-24（会话 80291c19）的第一条消息。

### ARD-B

理由：用户说"to ticket 可以是impl 也要对应git issue or jira"（Q3）。
impl-plan 已经把工作切成带依赖的步骤（`skills/spec-organize/SPEC-STANDARD.md`），再切一次是重复劳动。
被否决的方案：沿用 to-tickets 的纵向切片，并在发布前让用户审拆法。
出处：用户 2026-11-24（会话 80291c19），Q3、Q8。

### ARD-C

理由：用户没有回答 Q4；本条按协调者的推荐处理，用户尚未确认，信心中等，见 design 的 QUES-C。
一行配置放在 CLAUDE.local.md，是因为不同机器可能用不同 tracker，而这个文件不提交。
缺省用本地，是沿用 to-tickets 和 wayfinder 的做法：没配置就写本地 markdown。本地工单的位置后来定在 `raw/state/` 下，见 ARD-J。
被否决的方案：放进提交的配置文件；没配置时直接报错停下。
出处：会话 80291c19 的协调者推荐；`.gitignore`；`skills/to-tickets/SKILL.md`。

### ARD-D

理由：用户说用途"只是为了demo/track job"（Q3），并同意"按照建议来"的最小方案（Q8）。
同步状态要处理冲突，花费远大于演示用途的收益。
被否决的方案：tracker 状态自动回写到 impl-plan；tracker 上的修改同步回 spec。
出处：用户 2026-11-24（会话 80291c19），Q3、Q8。

### ARD-E

理由：对应表是本机的运行状态，不是需求或设计，所以放在被 git 忽略的 `raw/state/` 下（Q8）。
有了对应表，重跑时就知道哪些 IMPL 已开过工单，只给新的开。本地模式后来不用对应表，见 ARD-J。
被否决的方案：把工单号写进 impl-plan 正文；每次重跑都全部重开。
出处：用户 2026-11-24（会话 80291c19），Q8；`.gitignore` 的 `docs/features/**/raw/` 规则。

### ARD-F

理由：本机没有 Jira 的 MCP 服务，GitHub 有 gh 命令行和 GitHub MCP（Q8）。没有连接就没法测试 Jira 实现。
被否决的方案：v1 就实现 Jira；完全不提 Jira。
用哪种 Jira（云版还是自建）未知，见 design 的 QUES-B。
出处：用户 2026-11-24（会话 80291c19），Q8。

### ARD-G

理由：用户对命名的回答是"可以"（Q6）。名字已通过 document-standard 的 DSGN-K 重名检查，和 `docs/features/*` 下的 feature 不冲突。
被否决的方案：沿用 to-tickets 这个名字。
出处：用户 2026-11-24（会话 80291c19），Q6。

### ARD-H

理由：用户说 Matt 的两个 skill"可以去掉"（Q5）。
顺序是 spec、spec-review、用户审阅、SKILL.md、最后移除旧 skill 并改指向（Q9），避免中间出现断链。
被否决的方案：新旧 skill 长期并存。
出处：用户 2026-11-24（会话 80291c19），Q5、Q9。

### ARD-I

理由：用户说"jira 保留，给其他人用。保留三个选项"（R7）。REST API v3 只要 curl 和三个环境变量。
被否决的方案：只留接口（ARD-F）；改用 ankitpokhrel/jira-cli，要多装工具。本机没有 Jira，未实测。
出处：用户 2026-11-24 审阅回复；审查报告第 7 条。

### ARD-J

理由：`.scratch/` 是要删掉的 to-tickets 的旧布局；放在 wayfinder 进度图旁，每个 feature 一棵被忽略的目录（R6）。
被否决的方案：`.scratch/<feature>/issues/`；本地也另存对应表。出处：用户 2026-11-24 审阅同意；审查报告第 6 条。
`tracker:` 行与 wayfinder 共用，免得改指向后两个 skill 读不同的配置。

### ARD-K

理由：gh 2.94 起 `gh issue create` 支持 `--blocked-by`（本机 2.101），被依赖的先建就不用第二遍连边（R3）。
`gh issue list --search` 默认只列打开的，且走搜索索引；改用 `--state all --json` 加精确匹配。
被否决的方案：先建后连的两遍做法；经 `gh api` 连依赖。正文 "Blocked by" 行只留给旧的自建 GitHub。
出处：审查报告第 3 条；本机 `gh --version`。这条来自审查，不是用户提出的。

### ARD-L

理由：SDD impl-plan 里 `**挡住：**` 都在行中间，跟在依赖句后面；IMPL-A 写着"这一项已经完成"（R2）。
被否决的方案：只认行首标签；悄悄丢掉非 IMPL 的依赖；已完成的也开票。
出处：审查报告第 2 条；`docs/features/spec-driven-development/impl-plan/spec-driven-development-impl-plan.md`。

### ARD-M

理由：SDD 的 design 用 `是`/`否` 填 Blocking 列；每行都有目前答案（"暂定…"），"有没有答案"无法判断（R4）。
留在表里的行就算开着（SPEC-STANDARD 的 ARD-BC）。被否决的方案：只认 `yes`；再看答案一栏。
出处：审查报告第 4 条；`skills/spec-organize/SPEC-STANDARD.md`。

### ARD-N

理由：skill 是 agent 读的散文，要有东西检查结果（R10）。重跑、删表要反复比对，脚本比人工清单不易漏。
被否决的方案：人工逐项清单。出处：审查报告第 10 条；协调者 2026-11-24 让二选一。

### ARD-O

理由：用途是演示和跟踪，母工单一眼看出进度（GitHub、Jira 自动显示"3/7 完成"）；满足 to-spec 的 PRD-D。
正文只有链接，spec 仍是文档，不违反 wayfinder"SDD 里 spec 不是 issue"。
被否决的方案：A，不建母工单，只给每张工单打 `feature:<f>` 标签。
出处：用户 2026-11-24 审阅回复"B"；`skills/wayfinder/SKILL.md` 第 282 行。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：记录用户 2026-11-24 对 spec-ticket 的决策 ARD-A 到 ARD-H |
| 2026-11-24 | 按审查报告加 ARD-I 到 ARD-N；ARD-F 被 ARD-I、ARD-J 取代 |
| 2026-11-24 | 加 ARD-O：每个 feature 一张母工单（用户选 B） |
| 2026-11-24 | 加 ARD-P：Jira 只支持云版 |
| 2026-11-24 | 加 ARD-Q：链接、锚点和 Parent 退路 |
