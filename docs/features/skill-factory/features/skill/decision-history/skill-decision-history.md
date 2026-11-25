---
feature: skill
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# skill — 决策记录

本篇按时间倒序记录 `skill` 这个 skill 的关键决策。
需求见 [PRD](../prd/skill-prd.md)，设计见 [design](../design/skill-design.md)。
整个 skill-factory 层面的旧决策（编号 0001 起）在
[parent decision history](../../../decision-history/skill-factory-decision-history.md)。
opencode 会话按会话 id 前缀引用，数据在本机 opencode.db。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-L | 2026-11-24 | check_skills.py 也进 CI（`skills-check.yml`）和 pre-commit 钩子（`tools/git-hooks/pre-commit`，只在提交 SKILL.md 时跑） |
| ARD-K | 2026-11-24 | 新增 `tools/check_skills.py` 查 frontmatter、断掉的 skill 引用、链接和仓库路径；create、edit、import 保存后都要跑 |
| ARD-J | 2026-11-24 | import 记录 source_author、source_url（带 commit sha）和导入日期，并检查依赖 |
| ARD-A | 2026-08-02 | 把 skill-create、skill-edit、skill-import、skill-list 合成一个带子命令的 `skill` |
| ARD-B | 2026-08-02 | 导入的 skill 和自写的放在同一个 `skills/` 下，不再单设 import 目录；保留作者出处的要求不变 |
| ARD-C | 2026-07-22 | create 增加 Precision & Examples 一步：像法律条文一样写清边界，并给 2 到 3 个示例 |
| ARD-D | 2026-06-11 | skill 文件夹名不加 `ai-coworker-` 前缀；导入的 skill 也不加 |
| ARD-E | 2026-06-11 | create 先搜 GitHub（至少 10 个 repo）和网页，再在导入、借鉴、自写三者中选一 |
| ~~ARD-F~~ | ~~2026-06-11~~ | ~~导入时保留原作者，并写到单独的 import 子目录~~ 已被 [ARD-B](#ard-b) 取代 |
| ARD-G | 2026-06-10 | 每个 skill 只有一份 SKILL.md；没有 deploy 概念，只留一个版本；change log 用 git log |
| ARD-H | 2026-06-10 | edit 只做小改动，不另建重复的 skill；目标不存在或要重写大半时转去 create |
| ARD-I | 2026-06-10 | 用 create 自举出 import 和 edit；产出不好时先修 create 再重做 |

## Evidence Appendix

### ARD-L

理由：只靠 /skill 拦不住手改的 SKILL.md。钩子测过三种情况：坏的拦下，好的和不含 SKILL.md 的放行。出处：用户 2026-11-24（会话 80291c19）"8 -10 按照你的建议来"。

### ARD-K

理由：2026-11-24 审查发现 7 个 skill 引用已改名的 skill，没有工具能自动发现。旧名单取自 git 历史，不用手写。
用 4 个修复前的 SKILL.md 试跑，查出 11 处断引用；当前 27 个 skill 为 0。
被否决：沿用 `tests/test_skills.sh`（指向已不存在的 `~/project/skill-factory`）；先上 pre-commit 和 CI。
出处：用户 2026-11-24（会话 80291c19）"其他几个按照你说的修"。

### ARD-J

理由：用户两次要求导入保留原作者和出处（PRD-F）。缺依赖检查，导致 08-02 导入的
grill-with-docs 和 prototype 无法运行。被否决：只补格式。出处：用户 2026-11-24 审阅回复；commit 773594b。

### ARD-A

理由：四个 skill 是同一组增删改查操作，合并后只有一个入口，用子命令分流（PRD-A）。
被否决的方案：保留四个独立的 skill。
出处：commit 6086424；parent design 的 Skill Consolidation 一节。
发起这次合并的那段对话没有找到，属于 UNKNOWN。

### ARD-B

理由：目录越少越好找；`CONVENTIONS.md` 现在写明导入的 skill 保留原名，和自写的同放 `skills/`（PRD-E）。
被否决的方案：单设 import 目录，即 ARD-F 的做法。
出处：commit 8d451059（import-skills 并入根目录）和 93d4a4a（全部移入 `skills/`）。
ARD-F 里保留原作者的部分仍然有效（PRD-F）。
但当前 SKILL.md 的 import 流程没写这一步；是有意去掉还是合并时漏掉，属于 UNKNOWN。

### ARD-C

理由：让新 skill 的规则边界更精确，并用示例说明。被否决的方案：UNKNOWN。
出处：commit a7f57de。当前 SKILL.md 已没有这一步，去掉的原因属于 UNKNOWN。

### ARD-D

理由：用户先要求所有自写 skill 加 `ai-coworker-` 前缀，随后改口：导入的"不要加前缀"，
文件夹名"不用加prefix，可以改 conventions"（ses_14aa890f，2026-06-11）。
被否决的方案：所有 skill 文件夹都加 `ai-coworker-` 前缀。
另有一条要求：安装后显示时带前缀（ses_14b5b4b7，2026-06-10）。
现行 `CONVENTIONS.md` 没有前缀规则；这条何时取消，属于 UNKNOWN。

### ARD-E

理由：用户希望先看有没有好的同类 skill，"给我一些idea"，再决定导入后改还是只吸收灵感（PRD-B）。
被否决的方案：只在本地扫描（parent decision history 第 0083 条）。
出处：ses_14bdec5d（2026-06-10）、ses_14aa890f（2026-06-11）；commit d30f01c。

### ARD-F

理由：用户要求导入的 skill"保留原作者信息"，并且不放在自写目录，而放 import 目录下（ses_14aa890f，2026-06-11）。
被否决的方案：不记录来源（parent decision history 第 0085 条）。
出处：commit 773594b。目录部分已被 ARD-B 推翻，作者部分在 ARD-B 中重申。

### ARD-G

理由：用户嫌多层目录复杂，问"为什么不是世界一个Skill.md 就行了"（ses_14b5b4b7，2026-06-10）。
又说"可以没有deploy 概念"，"change log 放在github log 就行"（ses_14bdec5d，2026-06-10）（PRD-G）。
被否决的方案：每个 skill 多层目录、带 deploy 副本、在文件里写 change log。
出处另见 `CONVENTIONS.md`（单一版本、不写 Changelog 两条）和 parent decision history 第 0112 条。

### ARD-H

理由：edit 是用户"发现问题了"后做"微小的改动"，不该"创建新的skill，去重复"（ses_14aa890f，2026-06-10）（PRD-D）。
被否决的方案：编辑不存在的 skill，或借 edit 整篇重写（parent decision history 第 0099 条）。

### ARD-I

理由：用户说 create"可以创建both skill-import and skill-edit"，产出不好就"修理skill-create"再重建（PRD-I）。
被否决的方案：删掉 skill-create 从零开始（parent decision history 第 0087 条）。
出处：ses_14aa890f（2026-06-10）；commit 1d7bb7e、33e48d2。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 skill 的决策 |
| 2026-11-24 | 新增 ARD-J：import 记录出处并检查依赖 |
| 2026-11-24 | 新增 ARD-K：check_skills.py |
| 2026-11-24 | 新增 ARD-L：CI 和 pre-commit |
