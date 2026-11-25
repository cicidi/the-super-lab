---
feature: skill
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# skill — Skill 管理入口

本篇说明 `skill` 这个 skill 做什么：创建、修改、导入、列出 the-super-lab 里的 skill。
源文件：`skills/skill/SKILL.md`（commit 8ba542e）。

## Problem Statement

一个工作流反复手动做，就该收成 skill。没有统一入口时，新 skill 格式不一，
还可能和已有 skill 重复。

## Solution

`skill` 提供四个子命令：`create`、`edit`、`import`、`list`（PRD-A）。
不带子命令时，先列出现有 skill，再问用户要做什么。

## User Stories

- 作为 skill 作者，我想把一个工作流收成新 skill，并且不和已有的重复。
- 作为维护者，我想改一个 skill，改完先看 diff 再保存。
- 作为使用者，我想从 GitHub 导入别人的 skill，并转成本仓库的格式。

## Implementation Decisions

格式规则不写在本 skill 里，统一引用仓库根目录的 `CONVENTIONS.md`（PRD-C）。
这样规则只有一个出处，改规则时不用同时改多个 skill。

## Design

**DSGN-A create。** 先问名字（kebab-case，即小写加连字符，如 `fix-bug`）。
再在本地、GitHub 和网上搜相似 skill，避免重复（PRD-B）。
然后按 `CONVENTIONS.md` 起草，给用户审阅；批准后才写入 `skills/<name>/SKILL.md`（PRD-G、PRD-H）。

**DSGN-B edit。** 先读现有 SKILL.md，问清改什么，改后展示 diff，确认才保存（PRD-D）。
改动必须守住三条：没有 TBD/TODO；正文不用装饰性 emoji；
description（frontmatter 里告诉 agent 何时调用的那段话）以 "Use when" 开头且不超过 1024 字符。

**DSGN-C import。** 从 GitHub URL 取 SKILL.md，保留原名存到 `skills/<原名>/`（PRD-E）。
缺 `license` 补 MIT，缺 `compatibility` 补 `claude-code,opencode`，
缺 When to Use / When NOT to Use 两节就补上。
`metadata` 里记下 `source_author`、`source_url`（有 commit sha 就带上）和 `imported` 日期（PRD-F、ARD-J）。
再检查依赖：列出原文引用的每个 skill 和文件（如 `/grilling`、`LOGIC.md`），缺的一并导入或在报告里标出（ARD-J）。
最后报告哪些改了、哪些原样保留、出处和依赖情况。

**DSGN-D list。** 运行 `coworker skill list`，显示每个 skill 的名字、路径和是否启用。

## Testing Decisions

正确性靠 DSGN-B 的 diff 确认、人工审阅和 `tools/check_skills.py`（ARD-K）。
该脚本查 frontmatter、断掉的 skill 引用、链接和仓库路径，不查内容好坏。CI 和 pre-commit 钩子也跑它（ARD-L）。
产出的 skill 不好时，先修 create 再重新生成（PRD-I）。

## Out of Scope

运行已有 skill（直接调用即可）、管理 feature（用 `/feature`）、
管理项目目录（用 `/project`）都不归本 skill 管。

## Further Notes

skill-factory 整体怎么设计，见 [parent design](../../../design/skill-factory-design.md)。
需求见 [PRD](../prd/skill-prd.md)，决策见 [decision-history](../decision-history/skill-decision-history.md)。

## Alternatives Considered

拆成 skill-create、skill-edit、skill-import、skill-list 四个 skill：被否决。
2026-08-02 的合并把它们收成一个带子命令的 skill，见 parent design 的 Skill Consolidation 一节。

## Drawbacks

DSGN-A 的查重靠 agent 搜索，搜不到不代表没有重复。
create、edit、import 都靠人审，skill 多了以后审阅成本会上升。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| 导入的 skill 带有恶意或越权指令 | DSGN-C 只补格式，不审内容；用前须人读一遍。是否加内容审查见 QUES-B |
| 改名后旧 skill 残留在安装目录 | walter-worker `setup/install.sh` 的 `install_skill()` 没有删除分支（commit a0f4ce0）；改名后须手动删除 |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 要不要一个自动检查 SKILL.md 格式的工具？ | 已加 `tools/check_skills.py`，create、edit、import 保存后跑（ARD-K） | cicidi | no |
| QUES-B | import 要不要审查 skill 的内容，而不只补格式？ | 目前只补格式 | cicidi | no |
| QUES-C | import 要不要记录原作者和出处（PRD-F）？ | 要记录：作者、URL（带 sha）、导入日期，见 DSGN-C、ARD-J | cicidi | no |

## Reversibility

所有改动都落在 git 跟踪的 `skills/` 下，用 `git revert` 即可撤回。
已安装到 `~/.claude/skills/` 的副本，须重跑 `install.sh` 才同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 skill 的 design |
| 2026-11-24 | 引用 PRD-A 到 PRD-I，新增 QUES-C，链接 PRD 和 decision-history |
| 2026-11-24 | DSGN-C 加出处记录和依赖检查（ARD-J），QUES-C 已答 |
| 2026-11-24 | Testing Decisions 加 check_skills.py，QUES-A 已答（ARD-K） |
| 2026-11-24 | 加 CI 和 pre-commit（ARD-L） |
