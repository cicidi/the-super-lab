---
feature: doc-protect
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# doc-protect — 锁住文档段落

本篇说明 `doc-protect` 这个 skill 现在怎么工作。
源文件：`personal-skills/doc-protect/SKILL.md`（3395648 改名，40a10e4 改正文标题）。

## Problem Statement

AI 编辑或合并文档时，可能顺手改掉人写下的关键决定，例如需求、架构选择、法律条款（PRD-B）。
AI 不知道这些决定背后的背景，所以不该替人改（decision-history 的 ARD-F）。

## Solution

用一对 HTML 注释把要锁的段落包起来，再写下 AI 必须遵守的规则（PRD-A、PRD-B）。
HTML 注释在 Markdown 渲染后看不见，不影响读者阅读。

## User Stories

- 作为文档作者，我说"保护架构决定这一节"，agent 就加上标记，不动内容。
- 作为文档作者，我让 agent 改一个含受保护块的文件，它只改块外的部分。

## Implementation Decisions

skill 只有一个 SKILL.md，全是给 agent 读的文字规则，没有脚本。
真正用代码检查的是 walter-worker 的 `semantic_merge.py`：升级 CLAUDE.md 时保留受保护块（0936956）。

## Design

**DSGN-A 何时用。** 用户要锁一段内容，或说"never change this""lock this section"时（PRD-E）。
内容本该自由编辑，或只是临时笔记时，不用。

**DSGN-B 加保护。** 先问用户要保护哪一段，再在段前加开始标记、段后加结束标记（PRD-A）。
然后提交，信息为 `docs: protect {section name}`（PRD-D）。

**DSGN-C 解除保护。** 只有用户明确说"unprotect this section"才做（PRD-C）。
去掉两行标记，块内文字不动，提交信息为 `docs: unprotect {section name}`（PRD-D）。

**DSGN-D AI 的规则。** 不得修改、移动、删除或重排块内内容；可以读它，可以在块外加内容（PRD-B）。
可以建议加保护，但不给用户没要求的内容加（PRD-E）。
反模式：没有用户指示就去掉标记；为了格式改动块内文字。

**DSGN-E 质量门。** MUST：任何编辑后受保护块保持原样；开始和结束标记成对出现。
NICE：找出值得保护的段落，如 PRD 需求、架构决定、法律条款、安全策略（PRD-E）。

**DSGN-F 标记写法与工具。** SKILL.md 只教 `<!-- PROTECTED -->` 和 `<!-- END PROTECTED -->` 这一种写法（PRD-A）。
walter-worker 的合并工具还认 `PROTECTED START`/`PROTECTED END`；没写结束标记时，保护会延伸到文件末尾（0936956）。
walter-worker 的 CLAUDE.md 还用带名字的写法 `<!-- PROTECTED:CRITICAL-RULES -->`，工具认，SKILL.md 没提（QUES-C）。

**DSGN-G 存放与命名。** 文件在 `personal-skills/doc-protect/`，属于个人 skill（PRD-F）。
`name` 字段是 `doc-protect`（PRD-H），正文标题却是 `walter-worker-doc-protect`（QUES-E）。

**DSGN-H 内容来源。** 现在的规则和流程与 c3f771f 原版一致，只改成了 skill 的固定章节格式（PRD-G）。
用户要的是"通过 skill create 新建"，这次迁移更像搬运，见 QUES-D。

## Testing Decisions

本 skill 没有自动测试或评测集。SKILL.md 列了 4 个文字场景：加保护、编辑含受保护块的文件、解除保护、建议保护。
这些场景没有对应脚本，只能人工核对。合并工具的测试在 walter-worker 仓库，覆盖两种标记写法（0936956）。

## Out of Scope

可以自由编辑的内容、临时笔记，都不用本 skill（SKILL.md 的 When NOT to Use 一节）。
合并上游文档时怎么保留受保护块，归 doc-organize 的 merge 模式（parent design 的合并表第 7 行）。

## Further Notes

需求见 [PRD](../prd/doc-protect-prd.md)，决策见 [decision-history](../decision-history/doc-protect-decision-history.md)。
skill-factory 整体的设计见 [parent design](../../../design/skill-factory-design.md)。
原版在 walter-worker 的 c3f771f，路径 `templates/team-common/skills/doc-protection.md`。

## Alternatives Considered

以 `PROTECTED START`/`PROTECTED END` 为标准写法：被否决，现行写法用得多得多（ARD-A）。
保留 `ai-coworker-` 前缀：被否决，改成简短名字（ARD-C）。
留在 ai-coworker 仓库：被否决，迁到 skill factory（ARD-E）。

## Drawbacks

规则只靠 agent 自觉遵守；普通编辑时没有工具拦截对块内的修改，见 QUES-B。
每次加、减保护都要求提交，SKILL.md 没写要不要先问用户，见 QUES-A。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| 结束标记写错或漏写，保护范围延伸到文件末尾 | 合并工具已认两种结束写法（0936956）；SKILL.md 只教一种写法 |
| agent 为了统一格式，改了块内的空格或换行 | SKILL.md 把这列为反模式；普通编辑没有自动检查（QUES-B） |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 加、减保护后要不要自动提交（PRD-D）？ | SKILL.md 要求每次提交，没写先问用户 | cicidi | no |
| QUES-B | 要不要在普通编辑时也自动检查块内是否被改（PRD-B）？ | 只有 walter-worker 合并时检查 | cicidi | no |
| QUES-C | 带名字的标记 `PROTECTED:名字` 要不要写进 SKILL.md（PRD-A）？ | 工具认，SKILL.md 没写 | cicidi | no |
| QUES-D | 迁移时为什么没按"skill create 新建"重写（PRD-G）？ | UNKNOWN；a5dcc4e 基本是原版 | cicidi | no |
| QUES-E | `name` 与正文标题不一致，要不要统一（PRD-H）？ | parent 决策 0082 要前缀，3395648 去掉了 | cicidi | no |
| QUES-F | 为什么留在个人目录，而不是公开的 `skills/`（PRD-F）？ | UNKNOWN（ARD-D、ARD-E） | cicidi | no |
| QUES-G | frontmatter 写 `compatibility: opencode`，它也装进 Claude Code，要不要改？ | 当前没改 | cicidi | no |

## Reversibility

skill 的改动都在 git 跟踪的 `personal-skills/doc-protect/SKILL.md`，用 `git revert` 即可撤回。
已经加进各文档的标记由那些文档自己的提交管，撤回 skill 不会去掉它们。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 doc-protect 的 design，引用 PRD-A 到 PRD-H |
