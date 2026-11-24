---
feature: english-grammar-fix
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# english-grammar-fix — 决策记录

本篇按时间倒序记录 `english-grammar-fix` 这个 skill 的关键决策。
需求见 [PRD](../prd/english-grammar-fix-prd.md)，设计见 [design](../design/english-grammar-fix-design.md)。
skill-factory 层面的旧决策在 [parent decision history](../../../decision-history/skill-factory-decision-history.md)。
opencode 会话按会话 id 前缀引用，数据在本机 opencode.db。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-A | 2026-08-02 | 把 38 个 skill 合成 11 个时，本 skill 保持独立，不与任何 skill 合并 |
| ARD-B | 2026-06-24 | 补上使用场景、不适用场景和四步流程；触发词加上 fix grammar、correct english |
| ARD-C | 2026-06-23 | 改名为 english-grammar-fix，名字直接说明用途 |
| ~~ARD-D~~ | ~~2026-06-23~~ | ~~从 auto-patches 改名为 self-patch，归入 self-* 一组~~ 已被 [ARD-C](#ard-c) 取代 |
| ARD-E | 2026-03-30 | 语法小错静默改；风格改动用斜体标出并附原文，由用户审阅 |
| ARD-F | 2026-03-30 | 只在用户手动调用时运行，不挂 hook 自动运行 |

## Evidence Appendix

### ARD-A

理由：parent design 的 Independent — No Merge 表写的是"Pure utility, no overlap with anything"。
被否决的方案：并入某个合并后的 skill。
出处：commit 6086424；parent design 的 Independent — No Merge 表。提出这条判断的对话没有找到，属于 UNKNOWN。

### ARD-B

理由：用户要求用 contrarian review 检查两个仓库里"不合理的地方，旧的信息，不match 的内容，并修复"（ses_107972d8，2026-06-24）。
改名后旧的触发词 self-patch 和 `/auto-patches` 已经对不上，agent 在这次检查里补齐了各节（PRD-B、PRD-E）。
具体条目由 agent 写入，用户没有逐条确认。被否决的方案：保留旧触发词和旧的 Trigger 一节。
出处：commit cca25cd；ses_107972d8（2026-06-24）。

### ARD-C

理由：UNKNOWN。用户只说了"self-patch 改名english-grammar-fix"（ses_1417bab9，2026-06-23 23:26）。
当时同一会话生成的 README 把 self-patch 写成"Auto-generate patches"，旧名字容易被读错（PRD-F）。
被否决的方案：保留 self-patch。
出处：skill-factory commit 7226d53、c329159；walter-worker commit be857b4。

### ARD-D

理由：用户问"这些命名合理吗"，要 agent 给不合理的推荐"好记的"名字（ses_1417bab9，2026-06-23 22:07）。
agent 的方案把 coworker-meta-auto-patches 归入 self-* 一组，叫 self-patch；用户回复"可以"（同一会话 22:08）。
被否决的方案：保留 auto-patches 或带前缀的旧名。出处：commit 3395648。约一小时后被 ARD-C 取代。

### ARD-E

理由：UNKNOWN。规则在 2026-03-30 的首版里就有（walter-worker commit c3f771f 的 How It Works 一节）。
被否决的方案：UNKNOWN。同一提交的蓝图写"Minor in italics"，与 SKILL.md 的"语法静默改"不一致（PRD-B）。
2026-06-24 的 cca25cd 把这条拆成分类和审阅两步，规则没变（ARD-B）。出处：c3f771f；cca25cd。

### ARD-F

理由：UNKNOWN。首版的 Trigger 一节写"Run manually"，对一段文字运行 `/auto-patches`（c3f771f；PRD-E）。
被否决的方案：用 hook 在 AI 写完 commit message 或 PR 时自动运行。两个仓库里都没有这样的 hook（git grep）。
这个方案是否讨论过，属于 UNKNOWN。出处：c3f771f；会话 e6c678f2（2026-03-30 的手动调用）。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 english-grammar-fix 的决策 |
