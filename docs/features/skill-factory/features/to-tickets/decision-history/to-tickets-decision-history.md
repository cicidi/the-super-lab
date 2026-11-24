---
feature: to-tickets
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# to-tickets — 决策记录

本篇按时间倒序记录 `to-tickets` 这个 skill 的关键决策。
需求见 [PRD](../prd/to-tickets-prd.md)，设计见 [design](../design/to-tickets-design.md)。
skill-factory 层面的旧决策在 [parent decision history](../../../decision-history/skill-factory-decision-history.md)。
会话按 `~/.claude/history.jsonl` 里的 id 前缀和时间引用。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-A | 2026-09-24 | 本地工单放在 `.scratch/<feature-slug>/`，和 `docs/features/<feature>/` 分成两棵树 |
| ARD-B | 2026-08-02 | to-tickets 拆出的工单交给 auto-tdd 实现，不交给 implement |
| ARD-C | 2026-08-02 | to-tickets 之前设一道文档审查关口；关口写在 wayfinder，不写进 to-tickets |
| ARD-D | 2026-08-02 | spec 自己的 ticket 由 to-spec 建，不由 to-tickets 建 |
| ARD-E | 2026-08-02 | "ticket" 只指 to-tickets 的执行工单；wayfinder 的决策工单改叫 brief |
| ARD-F | 2026-08-02 | 导入 mattpocock 的 to-tickets：沿用原版正文，加 frontmatter 和作者出处 |
| ~~ARD-G~~ | ~~2026-08-02~~ | ~~to-tickets 列为 wayfinder 导入的后续项，这次不导入~~ 已被 [ARD-F](#ard-f) 取代 |

## Evidence Appendix

### ARD-A

理由：commit e1465f1 说明，`docs/features/<feature>/` 放推理材料，`.scratch/<feature-slug>/` 放 wayfinder 和 to-tickets 写的临时工单。
工单是用完即弃的工作项，不进文档树。被否决的方案：把工单也放进 `docs/features/`。
提交说明称两棵树都被 git 忽略，但 `.gitignore` 里没有 `.scratch` 规则（2026-11-24 用 `git check-ignore` 核对）。
这条是用户要求的，还是 agent 在会话 ef7cf4dd 里自己补的，对话里看不出，属于 UNKNOWN。
出处：commit e1465f1；会话 ef7cf4dd（2026-09-24，analytics.db 的 messages 表）。

### ARD-B

理由：用户说"implement 我的替代是auto-tdd"（d8d2da7f，18:37）。
两分钟后 commit 43cb1ef 给 wayfinder 加了流水线图，顺序是 wayfinder、to-spec、doc-review、to-tickets、auto-tdd。
被否决的方案：由 implement 接手工单。implement 这个 skill 至今还在仓库里，见 design 的 QUES-C。
出处：d8d2da7f（18:37）；commit 43cb1ef（18:39）。

### ARD-C

理由：用户说"spec 一个文档不够"，在 to ticket 以前"还得有一个 doc-review 的过程"（PRD-F）。
commit 7c11a7b 把关口写进 wayfinder 的 SKILL.md，排在 to-spec 和 to-tickets 之间；to-tickets 正文没有改。
被否决的方案：spec 写完直接拆工单。把关口放进 to-tickets 本身是否讨论过，属于 UNKNOWN。
出处：d8d2da7f（17:55）；commit 7c11a7b（18:20）。

### ARD-D

理由：用户说 spec 也要一张 ticket，原话是让 toTicket 别忘了建（PRD-E）。
commit 7c11a7b 把它写成 to-spec 的职责：spec 是 1 个 issue，由 to-spec 建，标签 `ready-for-agent`。
被否决的方案：照原话放进 to-tickets。为什么改放 to-spec，对话没有留下理由，属于 UNKNOWN。
出处：d8d2da7f（17:55）；commit 7c11a7b（18:20）。

### ARD-E

理由：用户说 ticket 用得混乱，to-tickets 的 ticket 保留，wayfinder 前面的要换名（17:22 第 2 条，17:27 "2 ok"）。
wayfinder 导入规格的术语表把决策 ticket 改叫 brief，理由是和 to-tickets 的执行工单区分（commit 0f3ede7）。
被否决的方案：用户提过的 challenge、question、query，以及把 to-tickets 改名 toTaskTicket（17:15、17:22）。
出处：d8d2da7f；commit 7c11a7b、0f3ede7。

### ARD-F

理由：用户要求注明作者（PRD-B），没有替换的接口"就用matt 的ksill"（PRD-C）。
被否决的方案：像 wayfinder 那样改写正文。导入后正文没改过，git 里只有 8d451059、93d4a4a 两次搬目录。
导入时有没有改正文，属于 UNKNOWN：8730941 只有一个提交，看不出和原版的差别。
`docs/book/imported-skills.md` 说导入时把 Jira 换成 issue tracker、加了 `ready-for-agent`，但它写的导入日期是 2026-07-25，与 git 不符。
出处：commit 8730941（18:35）；d8d2da7f（17:22 第 1 条，17:27 第 4 条，18:35）。

### ARD-G

理由：wayfinder 的导入规格只导入 wayfinder 直接依赖的 skill，把"to-spec、to-tickets、implement"列为后续导入。
被否决的方案：一次导入整条流水线。出处：commit 0f3ede7（18:21）的 wayfinder-import-spec，Out of Scope 一节。
14 分钟后（18:35）用户说"continue with to-tickets"，本决策被 ARD-F 取代。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 to-tickets 的决策 |
