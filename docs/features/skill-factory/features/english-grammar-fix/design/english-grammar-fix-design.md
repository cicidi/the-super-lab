---
feature: english-grammar-fix
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# english-grammar-fix — 英文语法修正

本篇说明 `english-grammar-fix` 这个 skill 现在怎么工作。
源文件：`skills/english-grammar-fix/SKILL.md`（commit cca25cd 定稿，40a10e4 改了 audience 字段，93d4a4a 移到现在的位置）。

## Problem Statement

用户英语不是母语。AI 写的英文出现主谓不一致、冠词用错这类小错时，用户不一定看得出来（PRD-A）。
这些文字会进入 commit 历史、PR 和文档，被别人读到（PRD-E）。

## Solution

一个只有说明文字、没有脚本的 skill。它按扫描、分类、修改、审阅四步处理一段英文（PRD-B）。
语法小错直接改；风格改动标出来，由用户决定。

## User Stories

- 作为开发者，提交前我对一段 commit message 说"fix grammar"，拿回改好的版本。
- 作为开发者，我看到斜体标出的措辞建议和原文对照，逐条接受或拒绝。

## Implementation Decisions

整个 skill 只有一份 70 行的 SKILL.md，没有脚本、测试或 hook。
frontmatter 的 compatibility 写了 claude-code、opencode、gemini 三个工具。
触发词有三个：english-grammar-fix、fix grammar、correct english（frontmatter 的 triggers）。
audience 字段在 2026-08-02 从 ai-coworker 改为 walter-worker（commit 40a10e4）。

## Design

**DSGN-A 扫描。** 读目标文字，找出语法、风格和措辞问题（PRD-A）。

**DSGN-B 分类。** 每个问题归入两类之一：语法类直接改，不提示；风格类用斜体标出，等用户审阅（PRD-B）。

**DSGN-C 修改。** 修正直接写在原位置；小错的修正版替换原文，不加说明（PRD-B）。

**DSGN-D 审阅。** 风格改动和原文并排显示，用户逐条接受或拒绝（PRD-B）。

**DSGN-E 语法检查项。** 主谓一致、冠词 a 和 an、同一句内时态一致、单复数一致（PRD-A）。
还查技术写作里常混的词：it's 和 its、affect 和 effect、关系从句里的 which 和 that。
Oxford comma 指列举三项以上时 and 前面的逗号，统一加上。

**DSGN-F commit message 规则。** 用祈使语气，用 Conventional Commits 格式，标题不超过 72 个字符（PRD-D）。

**DSGN-G 不改的内容。** 技术术语、变量名和函数名、故意简短的注释、正确但口语化的表达（PRD-C）。

**DSGN-H 触发方式。** 只在用户点名调用或说出触发词时运行；仓库里没有自动调用它的 hook（PRD-E）。

**DSGN-I 名字。** 目录名、name 字段和第一个触发词都是 english-grammar-fix，与用途一致（PRD-F）。

## Testing Decisions

本 skill 没有自动测试或评测集，`skills/english-grammar-fix/` 下只有 SKILL.md 一个文件。
是否好用，目前只能拿一段真实的英文跑一次，再人工判断。

## Out of Scope

不改代码，不改 DSGN-G 列出的内容；用户想自己审阅时不用本 skill（SKILL.md 的 When NOT to Use 一节）。

## Further Notes

需求见 [PRD](../prd/english-grammar-fix-prd.md)，决策见 [decision-history](../decision-history/english-grammar-fix-decision-history.md)。
2026-08-02 的合并表把它列为独立 skill，见 [parent design](../../../design/skill-factory-design.md)。
最早的 auto-patches 版在 walter-worker 仓库，可用 `git show c3f771f:templates/personal/skills/dev-ai-tool-auto-patches.md` 查看。

## Alternatives Considered

并入某个合并后的 skill：被否决，2026-08-02 保持独立（ARD-A）。
叫 self-patch：被否决，约一小时后改成 english-grammar-fix（ARD-D、ARD-C）。
用 hook 自动运行：仓库里没有这样做，是否讨论过属于 UNKNOWN（ARD-F）。

## Drawbacks

description 说 "Auto-correct"，但它不会自己运行，用户忘了调用就没有效果，见 QUES-A。
commit message 规则和 commit skill 都写了 Conventional Commits，两处可能说法不同，见 QUES-C。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| 静默修改改掉了用户有意的写法 | 只静默改语法类；术语、代码名和口语表达不改（DSGN-G） |
| which/that、Oxford comma 这类偏风格的规则被当成语法静默改 | SKILL.md 没写它们属于哪一类，见 QUES-D |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | AI 写完 commit message 或 PR 后要不要自动运行（PRD-E）？ | 只能手动调用；description 却写 Auto-correct | cicidi | no |
| QUES-B | 要不要也修正用户自己写的英文（PRD-A）？ | SKILL.md 只说 AI 写的文字；原意 UNKNOWN | cicidi | no |
| QUES-C | commit message 格式以本 skill 还是 commit skill 为准（PRD-D）？ | 两处都写了 Conventional Commits | cicidi | no |
| QUES-D | which/that 和 Oxford comma 算语法类还是风格类（PRD-B）？ | SKILL.md 没写 | cicidi | no |
| QUES-E | 语法小错要不要像蓝图说的那样用斜体标出（PRD-B）？ | 蓝图写 Minor in italics，SKILL.md 写静默改 | cicidi | no |

## Reversibility

所有改动都落在 git 跟踪的 `skills/english-grammar-fix/SKILL.md`，用 `git revert` 即可撤回。
已安装到 `~/.claude/skills/` 的副本，须重跑 `install.sh` 才同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 english-grammar-fix 的 design，引用 PRD-A 到 PRD-F |
