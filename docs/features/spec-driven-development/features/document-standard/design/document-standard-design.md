---
feature: document-standard
type: design
state: draft
final_date: 2026-10-30
health: active
owner: cicidi
last_verified: 2026-11-20
---

# Document Standard — 文档标准

本篇规定 `docs/features/` 下的 feature 文档怎么写：有哪几种文档、放在哪、叫什么名字、最长多少行、开头写什么、必须有哪些章节、编号怎么起、出现矛盾以谁为准。本篇不规定 skill 怎么拆文件、怎么加载这些规则，那属于实现。

相关文档：

- 写 spec 分几个阶段，见 [pipeline design](../../pipeline/design/pipeline-design.md)。
- 怎么测试，见 parent 的 [test-plan](../../../test-plan/spec-driven-development-test-plan.md)。被测的是 spec-write 和 spec-review 两个 skill；本篇的每条 MUST 都收进 MUST 清单，由测试逐条检查。
- 术语和缩写，见 [parent design 的术语表](../../../design/spec-driven-development-design.md#glossary)。

本篇的规则小节用 DSGN 编号，只在 document-standard 这个 feature 内有效：

| 编号 | 讲什么 |
|---|---|
| DSGN-A | 文档契约总览，包含下面的 DSGN-B 到 DSGN-F |
| DSGN-B | 文档类型、目录、文件名、行数上限、怎么拆分 |
| DSGN-C | 哪些文件不能提交 |
| DSGN-D | INDEX 和 book 这两层派生内容 |
| DSGN-E | frontmatter、必需章节、Decision Log 和 Change Log 的格式 |
| DSGN-F | 编号规则，以及怎么改已有正文 |
| DSGN-G | 冲突时以谁为准（按关注点分权威） |
| DSGN-H | design 文档写什么、不写什么 |
| DSGN-I | 内容的四个优先级（L1 到 L4） |
| DSGN-J | decision-history 怎么写 |
| DSGN-K | 名字撞车时怎么处理 |
| DSGN-L | 检查和整理文档的几种模式 |
| DSGN-M | 质量门槛：哪些是 MUST，哪些是 NICE |
| DSGN-N | 给人读的 reader HTML，见[分篇](document-standard-design-spec-reader-html.md) |

## Problem Statement

feature 文档一多，如果没有统一标准，会出现四类问题：

- 两份文档说法不一致时，不知道以哪份为准，AI 就会悄悄改掉其中一份。
- 文档放得到处都是，找不到。
- 分不清一份文档是「过时了」还是「写错了」。
- 同一个事实写在好几处，改了一处，其他几处还是旧的。

## Solution

用一份契约规定所有文档共同遵守的格式，再用几条补充规则处理语义和流程上的问题：

- **契约（DSGN-A，包含 DSGN-B 到 DSGN-F）**：类型、路径、行数、不能提交的文件、INDEX 和 book、frontmatter、章节、编号。大多数 MUST 规则在这里，脚本可以自动检查。
- **补充规则（DSGN-G 到 DSGN-L）**：冲突以谁为准、design 写什么、内容优先级、决定怎么记、撞名怎么办、检查模式。这些多数要靠 spec-review 判断。
- **质量门槛（DSGN-M）**：把上面的规则分成 MUST 和 NICE。

## User Stories

- 作为写 spec 的人，我想知道文档放在哪、叫什么、最长多少行、哪份说了算。
- 作为审 spec 的人，我希望格式规则能由脚本检查；内容上的问题只报告，不被悄悄改掉。
- 作为 AI，我希望 frontmatter、编号、Change Log 的规则写得明确，不用猜。

## Implementation Decisions

- 本篇的规则会摘要写进 `SPEC-STANDARD.md` 和 `SPEC-PRESENTATION.md`，spec-write 和 spec-review 读的是这两份摘要（[ARD-AJ](../../../decision-history/spec-driven-development-decision-history.md#ard-aj)）。摘要和本篇不一致时，先改本篇，再改摘要。
- 格式类的 MUST 由检查脚本执行；内容类的问题由 spec-review 报告。
- how-to 暂不做机械检查；其他五种文档按 DSGN-E 检查。
- 已有的不合规文档不迁移，只报告（[ARD-AF](../../../decision-history/spec-driven-development-decision-history.md#ard-af)）。
- 本篇是一份纯标准，没有需要 AI 去查、或要人来决定的子问题，所以「子问题归属表」不适用（pipeline design 的 PIPE-L 允许这样注明）。还没定的事项见 [Open Questions](#open-questions)。

## Design

### DSGN-A — Document Contract

文档契约由下面五条组成：DSGN-B 规定类型和路径，DSGN-C 规定哪些不能提交，DSGN-D 规定 INDEX 和 book，DSGN-E 规定格式，DSGN-F 规定编号。

#### DSGN-B — 文档类型、目录、文件名、行数上限、拆分

来源：parent PRD 的 PRD-D（行数上限）和 PRD-E（目录、文件名、目录之间的关系）。

`<f>` 表示 feature 的名字，用小写字母和连字符（例如 `spec-driven-development`），并且要和文件名里的 feature 部分一致。

feature 有两种放法：

| 放法 | 根目录 | frontmatter 里的 `feature` 写什么 |
|---|---|---|
| 普通 feature | `docs/features/<f>/` | `<f>` |
| sub-feature | `docs/features/<parent>/features/<sub>/` | `<sub>`，也就是 sub-feature 自己的名字 |

sub-feature 的例子（parent 是 `spec-driven-development`，sub-feature 是 `document-standard`）：

- 入口 design：`.../document-standard/design/document-standard-design.md`
- design 分篇：`.../document-standard/design/document-standard-design-<名词>.md`
- 调研笔记：`.../document-standard/raw/research/<主题>.md`
- 进度快照：`.../document-standard/raw/state/state-<YYYY-MM-DD>.md`
- 同级的另一个 sub-feature：`.../pipeline/design/pipeline-design.md`

**文件名规则（MUST）。** 提交的文档必须放在对应类型的目录里，文件名以 `<f>-<type>` 开头。有两种例外：`raw/` 下的文件；被某篇文档引用的辅助文件，它放在 `docs/features/<f>/<type>/<来源名>.md`，行数上限和它所在的类型相同。不允许单独建一个 `reference/` 类型；外部资料放在辅助文件里，或者放进 `raw/`。

六种类型，每种放在哪、叫什么：

| 类型 | 写什么 | 目录 | 入口文件名 | 分篇文件名 |
|---|---|---|---|---|
| `prd` | 做什么、为什么 | `docs/features/<f>/prd/` | `<f>-prd.md` | `<f>-prd-<名词>.md` |
| `design` | 怎么做 | `docs/features/<f>/design/` | `<f>-design.md` | `<f>-design-<名词>.md` |
| `impl-plan` | 任务和先后顺序 | `docs/features/<f>/impl-plan/` | `<f>-impl-plan.md` | `<f>-impl-plan-<两位序号>-<阶段>.md` |
| `test-plan` | 怎么验证 | `docs/features/<f>/test-plan/` | `<f>-test-plan.md` | `<f>-test-plan-<范围>.md` |
| `decision-history` | 所有决定 | `docs/features/<f>/decision-history/` | `<f>-decision-history.md` | `<f>-decision-history-<两位序号>-<时期>.md` |
| `how-to` | 怎么使用、怎么运维 | `docs/features/<f>/how-to/` | `<f>-how-to.md` | `<f>-how-to-<场景>.md` |

这六种都要提交到 git。六种都可以拆分篇；有分篇时，必须有入口文件 `<f>-<type>.md`，入口文件链到各分篇（MUST，[ARD-BQ](../../../decision-history/spec-driven-development-decision-history.md#ard-bq)）。分篇的命名规则：prd、design、test-plan、how-to 用名词，说明这篇讲哪个方面；impl-plan 和 decision-history 用「序号加阶段或时期」，因为它们有先后顺序（[ARD-G](../../../decision-history/spec-driven-development-decision-history.md#ard-g)）。

**行数（MUST）。** parent PRD 的 PRD-D 规定，除 decision-history 外，任何文档不超过 1,000 行。各类型的具体数字：

| 类型 | 建议行数 | 上限（MUST） |
|---|---|---|
| `prd` | 150–400 | 800 |
| `design` | 200–500；整体架构类 500–900 | 1,000 |
| `impl-plan` | 100–500 | 1,000 |
| `test-plan` | 200–600 | 800 |
| `decision-history` | 不设 | 不设（[ARD-E](../../../decision-history/spec-driven-development-decision-history.md#ard-e)） |
| `how-to` | 100–350 | 600 |
| `raw/` 下的文件 | 最好不超过 2,000 | 不设 |

上限包括 frontmatter 和 Change Log。超过上限就算失败，处理方法是：

1. 先按 DSGN-I 删减：从 L4 开始删，L1 永远不删。为了凑行数删掉 L1，本身就是错误。decision-history 不删条目，只能拆分篇。
2. 删减后仍然超过，就拆成分篇。按业务边界、领域、负责人、生命周期或时间段来拆，不要按行数机械地切。
3. 入口文件可以链到各分篇。拆分时如果名字撞车，见 DSGN-K。

**`raw/` 目录。** `raw/` 放本地草稿，在 `.gitignore` 里用 `docs/features/*/raw/` 排除。这里的文件不需要 frontmatter、Change Log，也不进 INDEX。草稿里的结论要正式写进文档时，在正式文档里写结论并链到草稿，不能把草稿当成权威出处。

| 子目录 | 放什么 | 文件名 |
|---|---|---|
| `raw/research/` | 调研的原始输出 | `<主题>.md` |
| `raw/review/` | AI 临时做的审查记录 | `<YYYY-MM-DD>-<审查者>-<对象>.md` |
| `raw/design/` | 还没写进正式 design 的草稿 | `<YYYY-MM-DD>-<对象>.md` |
| `raw/evidence/` | 证据、工具输出 | `<YYYY-MM-DD>-<简称>.md` |
| `raw/discussion/` | 讨论记录（可选） | `<主题>.md` |
| `raw/state/` | 进度快照，用来在长对话被压缩后恢复上下文 | `state-<YYYY-MM-DD>.md`（最多 400 行） |

旧项目里直接放在 feature 根目录的 `state/`、`research/`、`discussion/`，挪进 `raw/`。工单草稿放在 `.scratch/<feature>/`，同样不提交。

#### DSGN-C — 不能提交的文件

| 路径 | 说明 |
|---|---|
| `docs/features/<f>/raw/**` | 整个草稿目录，包括 `raw/state/` |
| `.scratch/<feature>/` | 工单等临时文件。它不在 `docs/features/` 下，但同样不能提交 |

这些路径必须写进 `.gitignore` 或用等效的办法排除。误提交算违反 DSGN-M 的 MUST。这些文件不需要 frontmatter、Change Log，也不进 INDEX。

**本地翻译副本（MUST）。** `<name>.<lang>.md` 这样的翻译副本只放在本地，不提交。副本开头写明以 `<name>.md` 为准；副本里的标题可以翻译（[ARD-AU](../../../decision-history/spec-driven-development-decision-history.md#ard-au)）。

#### DSGN-D — INDEX 和 book

`docs/features/` 里已提交的文档是唯一的真相来源。INDEX 和 book 都是从它们派生出来的，不用 DSGN-E 的 frontmatter 和 Change Log，也不能在里面写新的决定。

| | INDEX | book |
|---|---|---|
| 回答什么问题 | 文档在哪：路径、类型、feature 结构 | 文档讲了什么：短摘要，帮人和 AI 决定要不要打开原文 |
| 粒度 | 一行一个链接加标题，可以带一句说明 | 每篇或每组文档一段摘要，链回原文 |

**`docs/INDEX.md` 是什么。** 它是所有 feature 文档的地图：每个 feature 下有哪些 PRD、design、计划，各在什么路径。人、AI、脚本找文档时，先查 INDEX，再打开 `docs/features/` 里的原文。INDEX 不是 design，在 INDEX 里改标题或链接不等于改需求，INDEX 里也不写设计结论。

**INDEX 怎么维护：**

- 整个文件由脚本重新生成。要改内容就改生成脚本或模板，不要长期手工一行行改。
- 任何已提交的文档新建、移动、改名、删除之后，都要重新生成 INDEX，并且和那次文档改动一起推送。
- 只列已提交的文档，包括 sub-feature 的文档；不列 `raw/` 和 `.scratch/`。
- 按 feature 分块，块内按类型排序：prd、design、impl-plan、test-plan、decision-history。链接写成相对 `docs/` 的路径。
- 质量要求（MUST）：磁盘上有、INDEX 里没列的，叫孤立文档；INDEX 里列了、磁盘上没有的，叫死链。两种都不允许。

**`docs/book/` 是什么。** 它是从 feature 文档组装出来的摘要层，用短说明写清每份 PRD、design、计划覆盖什么、结论是什么、去哪里读全文，主要帮 AI 检索和挑选要读的文档。人和 AI 先扫 book，再打开原文。book 不是真相来源，不是全文拷贝，也不能和原文各自手工维护同一个事实。

**book 写什么：**

- 每条摘要都链到对应的原文路径。
- 写这篇的范围和主要结论或状态，不展开 L1 的全文。
- 新增或修改决定时，只改 feature 文档和 decision-history，然后重新生成 book；不能只在 book 里改说法。

**book 什么时候更新：**

- `docs/features/` 下已提交的文档有改动并推送到 GitHub 时，同一次推送里（或紧挨着的前一个 commit）应该已经重新生成了对应的 book 和 INDEX。具体用 pre-push hook、CI 还是手动，属于实现。本标准只要求远端能看到的文档和 book、INDEX 保持同步，避免 AI 在 GitHub 上读到新 spec，摘要却还是旧的。
- 原文还是 `state: draft` 时，可以暂不更新摘要；`final` 或已合并的改动必须反映到 book。

**其他：**

- book 在 `docs/book/` 下，不用 DSGN-E 的 frontmatter。检查只看链接是否有效、摘要指向的文件是否存在。
- HTML 页面在 `docs/book/html/`，目录结构和 `docs/features/` 一样。HTML 也不是真相来源（[ARD-BF](../../../decision-history/spec-driven-development-decision-history.md#ard-bf)）。
- book 可以另外用来发布 MkDocs 或 GitHub Pages 网站。网站的导航怎么排属于实现，但不能和 feature 目录、INDEX 矛盾。

另外两个不算 feature 文档的文件，同样不用 frontmatter，检查只看链接：`CONTEXT.md`（领域术语表）和 `README.md`（仓库说明）。

#### DSGN-E — 格式

**frontmatter（MUST）。** 每篇已提交的文档开头都有：

```yaml
---
feature: <feature-name>
type: prd | design | impl-plan | test-plan | decision-history | how-to
state: draft | final
final_date: YYYY-MM-DD   # state 是 final 时必填
---
```

可选字段：`spec_id`、`version`、`health`（`active`、`stale` 或 `deprecated`）、`owner`、`last_verified`、`audience`（`internal` 或 `external`，[ARD-AL](../../../decision-history/spec-driven-development-decision-history.md#ard-al)）。表示文档健康状况的字段叫 `health`，不叫 `status`（[ARD-D](../../../decision-history/spec-driven-development-decision-history.md#ard-d)）。

**必需章节（MUST）。** 每种文档必须有下面这些 `##` 章节。标题用英文原文，不翻译、不编号、不改名、不删；可以另外加章节（[ARD-AW](../../../decision-history/spec-driven-development-decision-history.md#ard-aw)）。比如把 Overview 写成 `## 1. 概述` 就违反规则。

| 类型 | 必需章节 |
|---|---|
| `prd` | Overview, Goals and Success Metrics, User Stories, Functional Requirements, Out of Scope, Resources Needed |
| `design` | Problem Statement, Solution, User Stories, Implementation Decisions, Design, Testing Decisions, Out of Scope, Further Notes, Alternatives Considered, Drawbacks, Risks and Mitigations, Open Questions, Reversibility |
| `impl-plan` | Global Constraints, Acceptance Criteria，以及每个任务一节 `## IMPL-*` |
| `test-plan` | Test Cases, Test Execution Order, Expected Pass Threshold |
| `decision-history` | Decision Log, Evidence Appendix |
| `how-to` | Overview, Prerequisites, Steps, Verification |

- how-to 暂不做机械检查，其他五种按本表检查。
- design 拆成多篇时，13 个必需章节只要求写在入口文件；分篇在开头链回入口，只写自己那部分（[ARD-AV](../../../decision-history/spec-driven-development-decision-history.md#ard-av)）。
- 某个必需章节对这篇确实不适用，就保留标题，正文写一句「不适用」并说明原因，或者链到写着这件事的地方。

**几个章节的意思。** 这几个章节借鉴自 Kubernetes 的设计提案模板（KEP）和 Rust 的 RFC 模板：

| 章节 | 写什么 |
|---|---|
| Alternatives Considered | 考虑过但放弃的方案，以及放弃的原因 |
| Drawbacks | 选定的方案本身有什么缺点 |
| Risks and Mitigations | 用起来可能出什么问题，怎么应对。和 Drawbacks 分开写 |
| Open Questions | 还没解决的问题，每个都有负责人 |
| Reversibility | 怎么撤回、怎么回到原来的状态（对应 KEP 的升级降级） |
| Acceptance Criteria | 做到什么程度算完成（对应 KEP 的 Graduation Criteria） |
| Resources Needed | 需要哪些资源（对应 KEP 的 Infrastructure Needed） |

KEP 里的版本偏移、发布签核、运维就绪问卷不采用：它们是为集群运维设计的，不适合非软件问题（parent PRD 的 PRD-Q 要求方法通用）。

**impl-plan 正文（MUST，由 spec-write 执行）。** 每个 `IMPL-*` 写明三件事：依赖哪个任务、挡住了哪个任务、完成标准。依赖和挡住要两头对得上：A 写了挡住 B，B 就要写依赖 A。最后的执行顺序把被挡住的任务排在后面，例如先改数据库，再改用到它的接口。优先级高又没被挡住的先做；互不相挡的可以同时做。先做只读的部分，再做会写入的部分；对方的接口还没上线时，写明用什么 mock 代替（[ARD-AT](../../../decision-history/spec-driven-development-decision-history.md#ard-at)）。

**引用代码（MUST）。** 写「某文件第几行」时，同时写明是哪个 commit（[ARD-AQ](../../../decision-history/spec-driven-development-decision-history.md#ard-aq)）。

**未决问题清单（MUST）。** 每个 feature 只有一份未决问题清单，一般是 design 的 `## Open Questions`；其他文档链过去，不抄一份。每个条目编号是 `QUES-` 加字母，写明问题、目前答案、负责人，以及是否阻塞（[ARD-AO](../../../decision-history/spec-driven-development-decision-history.md#ard-ao)、[ARD-AG](../../../decision-history/spec-driven-development-decision-history.md#ard-ag)）。在别处提到某个问题时，写的「未决」或「已决」要和清单一致（[ARD-BC](../../../decision-history/spec-driven-development-decision-history.md#ard-bc)）。

**可读性（MUST）。** 来源：parent PRD 的 PRD-M。一个本科水平的程序员，只读这一篇和术语表，就要能读懂（[ARD-BO](../../../decision-history/spec-driven-development-decision-history.md#ard-bo)，由 TST-V 检查）。具体要求：

- 写完整的句子。关键词串、`A → B → 失败` 这样的箭头链、塞满缩写的表格格子，都不算句子。
- 每个术语和缩写，第一次出现时解释，或者链到术语表。整套 spec 只有一份术语表，在 [parent design 的附录](../../../design/spec-driven-development-design.md#glossary)；新术语加到那里。
- 正文可以中英文混合，只要读着通顺；英文术语同样要解释或收进术语表。Problem Statement 可以保留作者原话（[ARD-BS](../../../decision-history/spec-driven-development-decision-history.md#ard-bs)）。
- 必需章节的标题和编号用英文。

**Decision Log（MUST）。** 表头是 `ID | Date | Decision`，可以加第四列 `Ready`；不能有 Status 列和 Supersedes 列（[ARD-AX](../../../decision-history/spec-driven-development-decision-history.md#ard-ax)）。最新的决定写在表的最上面。

**Change Log（MUST）。** 每篇文档的最后一节，只往末尾追加，不改旧行。

**其他：** 标为 PROTECTED 的段落，任何工具在任何模式下都不能改。文档新建、删除、移动后，重新生成 INDEX。

#### DSGN-F — 编号，以及怎么改已有正文

需要被引用的条目都用「前缀加字母」编号，字母按 Excel 列号的顺序：`A` 到 `Z`，接着 `AA` 到 `AZ`，再 `BA`……可以在已有条目之间插入新编号。

| 文档类型 | 前缀 | 例子 |
|---|---|---|
| `prd` | `PRD` | `PRD-A`、`PRD-AA` |
| `design` | `DSGN`（pipeline design 用 `PIPE`） | `DSGN-A`、`PIPE-B` |
| `decision-history` | `ARD` | `ARD-A`、`ARD-AA` |
| `impl-plan` | `IMPL` | `IMPL-A` |
| `test-plan` | `TST` | `TST-A` |
| 未决问题 | `QUES` | `QUES-A` |

**编号永不改（MUST）。** 一个编号一旦写进文档（表格、标题、正文、外部链接），就永远不变：不改字母、不改前缀、不「修正拼写」、不重新编号、不把一个条目并进另一个。用过的编号即使条目已作废，也不再给别的条目用。说法变了，就起一个新编号，旧的按 DSGN-J 处理。

**迁移时留对照（MUST）。** 如果确实必须改编号（例如修正不合规的编号，要记一条 ARD），保留一张新旧编号对照表。标题改名时，把旧锚点留在新标题上方，旧链接才不会失效（[ARD-AP](../../../decision-history/spec-driven-development-decision-history.md#ard-ap)）。

**凡是要被引用的都要编号（MUST）。** 需求、design 的规则小节、实现任务、测试用例、延后或未决的问题，都必须用上表的格式。不能用纯数字（`0001`），也不能用 `PRD-1`、`FR-3`、`OQ-1`、`QUES-1`、`D1` 这类数字编号。一个规则小节下面的子条款，可以在后面再加一个字母，例如 `DSGN-N-A`，只在本篇内使用。

**编号的范围（MUST）。** 编号在「同一个 feature 的同一种文档」里唯一。引用别的 feature 的编号时写成 `<feature>/<编号>`，例如 `document-standard/DSGN-B`，或者在句子里写明是哪个 feature。不带 feature 的编号只在本 feature 内有意义。

**整体设计的例外。** parent 的整体设计（HLD）里讲架构的章节不需要编号，只有可以被引用的规则小节才要编号（[ARD-AC](../../../decision-history/spec-driven-development-decision-history.md#ard-ac)）。

**检查方法。** `ids.py` 检查文档里有没有 `PRD-1` 这类数字编号，有就报错。

**改已有正文（MUST，由 spec-write 执行）。** 正文只写现行规则：不再成立的句子直接改写，在新句后面链到推翻旧说法的 ARD。删除线只用在 decision-history，正文的旧版本从 git 历史里找。错别字直接改（[ARD-BM](../../../decision-history/spec-driven-development-decision-history.md#ard-bm)、[ARD-AS](../../../decision-history/spec-driven-development-decision-history.md#ard-as)）。

AI 每次改动的大小上限（不超过 10 行，并且不超过 200 字符）不归本篇管，见 parent design 的 DSGN-A。

---

### DSGN-G — 冲突时以谁为准

不设一个「全局唯一的真相来源」，而是按关注点分：每类事实认一份文档为准。两份文档不一致时，按「发现、报告、问人」处理：不能悄悄改掉其中一份，也不能默认 design 一定比代码对。

| 关注点 | 以谁为准 |
|---|---|
| 想要的行为 | feature 的 design 文档 |
| 接口约定 | OpenAPI、protobuf、GraphQL、JSON Schema 等机器可读的定义文件 |
| 数据库结构 | migration 或 schema 文件 |
| 当前实现 | 代码 |
| 可执行的验证 | 测试 |

design 管「想要怎样」，代码管「现在怎样」和内部结构。机器可读的接口定义不要整段抄进 markdown，链过去或者自动生成。测试是验证手段，不能代替需求。文档变成 `final` 后只做维护性修改，不整篇重写。

---

### DSGN-H — design 写什么、不写什么

**写：** 系统的行为、接口约定、不变量、约束、错误怎么处理、状态怎么变化、和外部怎么交互、架构边界（包括画图）。

**不写：** 类的层级结构、私有方法、框架内部的细节。按 DSGN-I 删减时，这些本来就不该出现。

**判断方法：** 如果实现可以改、而外部看到的行为不变，那这部分就不该写进 design。

**AI 读文档的顺序：** 全局规则、领域 design、架构、接口约定、例子和测试、代码。如果回答一个很窄的问题也要读完整篇 design，说明 design 的边界划得不对，应该重新拆分。

行数和拆分见 DSGN-B，编号见 DSGN-F。

---

### DSGN-I — 内容的四个优先级

文档需要变短时，按 L4、L3、L2 的顺序删减或压缩，L1 永远不删。删减后仍然超过上限，就按 DSGN-B 拆分篇（[ARD-H](../../../decision-history/spec-driven-development-decision-history.md#ard-h)）。

| 级别 | 包括什么 | 删减时 |
|---|---|---|
| L1 决定性内容 | 行为、接口约定、不变量、错误处理、安全规则、边界、不在范围内的事项、前提假设、兼容性约束、未决问题 | 永远不删 |
| L2 理由 | 为什么这样设计 | 可以压缩 |
| L3 放弃的方案 | 为什么不选另一种做法 | 先删 |
| L4 参考资料 | 引用、原始输出、例子 | 先删；已经在别处写过的事实，只能放链接 |

---

### DSGN-J — decision-history 怎么写

**它是什么。** decision-history 是所有决定的索引加正文：Decision Log 一行一条，Evidence Appendix 每条一节（格式见 DSGN-E）。它不是 PRD 或 design 的摘要。

**顺序。** 新决定写在 Decision Log 的最上面，越往下越早。

**每条都有一节说明（MUST）。** 每条 ARD 在 Evidence Appendix 里有一节，写明原因；当时考虑过别的做法，就写出放弃了哪些、为什么。

**编号。** `ARD-` 加字母（DSGN-F），分配后不能改。表格里的编号和 `### ARD-A — …` 小节标题里的编号一致。

**推翻旧决定。** 旧行不删，用删除线划掉，后面链到新决定，例如：被划掉的旧说法，后面跟一个指向新决定的链接。新说法用一个新编号完整写一条，放在 Log 最上面。按 DSGN-I 删减时，不删被划掉的文字。这是整套 spec 里唯一使用删除线的地方（[ARD-BM](../../../decision-history/spec-driven-development-decision-history.md#ard-bm)）。

**拆分篇。** decision-history 不设行数上限，但也可以拆分篇。拆了之后编号在整个 feature 内唯一；新决定写在当前那篇的 Log 最上面；旧篇保留，篇与篇之间用链接连起来。

**什么时候加一条。** 详细规则见 parent design 的 DSGN-B，简单说：

| 要加 | 不加 |
|---|---|
| 别人定下来的说法（评审、结对、利益相关方），团队需要看到 | 还只在自己脑子里、没写进 design、也没改代码的试探 |
| 自己的转向会改已有代码或对外约定（不兼容的行为变化、路径或改名、谁说了算） | design 里改几句话就能说清的推敲；「想过又改主意」不用每次都记 |
| 改名、撞名等流程要求记录的事（DSGN-K） | AI 默认不自动批量加条目；拿不准就问人 |

---

### DSGN-K — 名字撞车时怎么处理

新建 feature 或文件时，必须和已有的名字比一比。符合下面任何一条，就算撞车：

| 情况 | 例子 |
|---|---|
| 大小写、符号统一后相同 | `Payment` 和 `payment` |
| 一个名字包含另一个 | `auth` 和 `auth-service` |
| 单复数或常见缩写 | `doc` 和 `docs` |
| 只差两个字符以内 | `payment-api` 和 `payments-api` |

怎么处理：

- 属于同一块业务：合并成一个 feature，再按方面拆 design 分篇。
- 不同业务但容易混淆：两边都改名，并在 decision-history 里记一条。
- 同一个 feature 内的文件撞名：给分篇换一个更准确的名词，或者给 feature 改名。

改名本身就是一个决定：要更新所有指向它的链接，不能悄悄改。

---

### DSGN-L — 检查和整理文档的几种模式

| 模式 | 由谁执行 | 做什么 |
|---|---|---|
| Organize | spec-organize | 按顺序处理：确定 feature 和类型、检查撞名、路径和文件名、frontmatter 和章节、Change Log、INDEX |
| Lint | spec-organize | 扫描 `docs/features/`；格式类的 MUST 直接修；内容上的问题只报告 |
| Consolidate | spec-organize | 先提出合并方案，人批准后再合并；所有决定都保留；`raw/` 里的旧内容要么被引用，要么删除 |
| Sync | spec-organize | 找出文档和代码不一致的地方，按 DSGN-G 判断以谁为准；内容冲突只报告 |
| Review | spec-review | 和 Lint 一样找问题（格式 MUST 加内容问题），但不改，只输出带严重度的修改建议 |

设计本身是否合理，由 Review 的内容审查负责，不属于本标准的 MUST。

---

### DSGN-M — 质量门槛

**MUST，做不到就算失败：**

- DSGN-A 契约全部满足，包括编号永不改、永不复用（DSGN-F）。
- 冲突不能悄悄处理（DSGN-G）。
- 不删 L1（DSGN-I）。
- 合并文档时不丢任何决定。
- 不能提交的路径没有被提交（DSGN-C）。
- INDEX 没有孤立文档和死链；文档里的链接和锚点都能打开（[ARD-AP](../../../decision-history/spec-driven-development-decision-history.md#ard-ap)）。
- 推送 `docs/features/` 的改动时，INDEX 和 book 已经同步。
- 新名字已经检查过撞车（DSGN-K）。
- 正文改动遵守 DSGN-F 的「改已有正文」规则。
- 结论有依据，查不到写 `UNKNOWN`（pipeline design 的 PIPE-L）。
- DSGN-E 的 impl-plan 正文、引用代码、未决问题清单、可读性四条。
- 本地翻译副本不提交（DSGN-C）；改编号时留对照表和旧锚点（DSGN-F）；每条 ARD 都有说明（DSGN-J）。

**NICE，做不到只提醒（[ARD-BN](../../../decision-history/spec-driven-development-decision-history.md#ard-bn)）：**

- 标题层级不跳级；术语和 `CONTEXT.md` 一致；`last_verified` 不要太旧；文档边界划得合理。
- 每节写明哪份文档对这些事实有权威（ARD-AL 的后半句）。
- 步骤编号只表示位置（ARD-AM）。
- 就绪程度、原地修订、按负责人分组（ARD-AN）。
- 不变量写成表格（ARD-AR）。
- §N 链接落点、步骤范围不重叠（ARD-AZ）。
- HTML 更新记录覆盖每个日期（ARD-BA）。
- 问题清单的数量统计对得上（ARD-BB）。
- 图的规则（ARD-BE）。

## Testing Decisions

测试见 parent 的 [test-plan](../../../test-plan/spec-driven-development-test-plan.md)。被测的是 spec-write 和 spec-review 两个 skill，不是本篇。本篇所有的 MUST 和禁止事项，由 TST-A 扫描收进 `must_registry.yaml`：格式类的由 Python 脚本判断，其余由判分模型判断。

## Out of Scope

- 写 spec 的阶段怎么安排，见 pipeline design。
- 一次性把所有旧文档迁移到新标准。旧文档逐步改到合规即可。
- 检查规则在 CI 或 skill 里具体怎么实现（拆几个文件、写什么 prompt、用什么 hook）。
- 把「自动发现文档和代码不一致」做成产品。

## Further Notes

**历史上不合规的例子。** 例如 `skill-factory/design/` 等。将来要迁移时，按 DSGN-M 逐项处理。

**2026-11-07 加入的规则在哪里。** 这些规则来自 ARD-AM 到 ARD-BE。其中的 MUST 已经写进对应小节的正文：翻译副本在 DSGN-C；引用代码、impl-plan 正文、未决问题清单在 DSGN-E；对照表和旧锚点在 DSGN-F。其余的是 NICE，列在 DSGN-M。

## Alternatives Considered

- **只用一种 `spec` 类型装下所有内容：** 放弃。文档会越来越大，也没法按关注点分开写（DSGN-B）。
- **按 initiative 而不是按 feature 组织目录：** 放弃。和已有的 `docs/features/` 目录结构冲突。
- **frontmatter 用 `status` 而不是 `health`：** 放弃（[ARD-D](../../../decision-history/spec-driven-development-decision-history.md#ard-d)）。
- **所有规则都是 MUST：** 放弃。纯格式规则太多，作者只好把文档写得像给机器读的（[ARD-BN](../../../decision-history/spec-driven-development-decision-history.md#ard-bn)）。

## Drawbacks

- 文档类型和必需章节偏多，小 feature 也要写全。sub-feature 可以不写全五篇（parent design 的 DSGN-E），能缓解一些。
- 机械检查只能检查结构，检查不了内容写得好不好。

## Risks and Mitigations

| 风险 | 应对 |
|---|---|
| 规则越来越多，人和 AI 都开始跳过检查 | 规则分 MUST 和 NICE，只有 MUST 算失败（[ARD-BN](../../../decision-history/spec-driven-development-decision-history.md#ard-bn)）；MUST 由 `must_registry.yaml` 和 `run_spec_checks.py` 强制检查 |
| 标准和检查脚本慢慢对不上 | `SPEC-STANDARD.md` 和本篇同一批修改；`registry_provenance` 检查每条 MUST 的出处 |
| 检查脚本有漏洞，不合规的文档也能通过 | 每个检查都配有必须报错的反例（TST-B）；发现漏洞记进 impl-plan 的 IMPL-P |

## Open Questions

本表是 document-standard 这个 feature 唯一的未决问题清单（[ARD-AO](../../../decision-history/spec-driven-development-decision-history.md#ard-ao)）。

| ID | 问题 | 目前答案 | 负责人 | 阻塞 |
|---|---|---|---|---|
| QUES-A | 所有工具是否都支持 sub-feature 目录和 sub-feature 下的 `raw/` | 未确认，等工具这边核实 | AI 查完人决定 | 否 |
| QUES-B | 行数上限要不要按 feature 的规模分档 | 未定 | 人决定 | 否 |
| QUES-C | DSGN-B 的具体数字（800、1,000、600）是否合适 | 沿用现值 | 人决定 | 否 |
| QUES-D | `raw/` 的六个子目录够不够用 | 目前够用 | 人决定 | 否 |
| QUES-E | 图（Mermaid）在 reader 里怎么渲染，要不要统一 | 未定 | 人决定 | 否 |

## Reversibility

- 必需章节可以撤回：同时改 DSGN-E、`SPEC-STANDARD.md` 和 `sections.py` 三处，旧文档补上章节即可，没有数据要迁移。
- 给必需章节改名属于新规则：旧文档还用旧名字，`sections` 检查会报错，所以要同一批修改所有文档。
- MUST 和 NICE 的划分可以调整：改 DSGN-M 和 ARD-BN，再同步检查脚本。

## Change Log

| Date | Change |
|------|--------|
| 2026-09-25 | Initial English spec + doc-organize adoption |
| 2026-10-31 | 中文重写；SDD sub 路径与小改动（Unverified） |
| 2026-11-03 | DSGN-A 契约表（含 sub/raw/size/split）；D2–D9 精简；state 在 `raw/state/` |
| 2026-11-03 | 全文去重精简（保留契约与非重复补充） |
| 2026-11-03 | Spec 独立化：去掉 doc-organize 倒推表述与 skill 文件映射；impl 出 scope |
| 2026-11-03 | DSGN-C Commit=no 不得入 git；D1-3 INDEX.md 与 docs/book 规范 |
| 2026-11-03 | DSGN-D 重写：INDEX / book 目的、读者、与 source of truth 关系 |
| 2026-11-03 | DSGN-D book：AI 摘要层、push 应更新；对齐 doc-organize「assembled from final」 |
| 2026-11-03 | AI edit 约束移至 parent HLD §4；本 spec 仅 pointer |
| 2026-11-03 | 术语：feature spec 合称；技术设计 type/folder 改为 `design`（原 `spec/`） |
| 2026-11-03 | D5：何时 append → parent HLD §5 |
| 2026-11-03 | 移除原 D4 Spec Health；D5–D9 重编号为 D4–D8 |
| 2026-11-03 | D5：decision-history 角色 / split / 何时 append 改写 |
| 2026-11-03 | D5/D1-4：字母 ID、倒序、supersede=strike+链；去 Supersedes 列 |
| 2026-11-03 | D1-5：PRD/DSGN/ARD/IMPL/TST 前缀 ID |
| 2026-11-03 | 前缀 `Design`→`DSGN`，`TEST`→`TST` |
| 2026-11-03 | D1-5：ID immutable；D8 MUST 引用 |
| 2026-11-03 | D1-5：凡有序号即前缀 ID；禁裸数字/伪前缀 |
| 2026-11-06 | Open Questions 的 ID 前缀为 `QUES`（`QUES-A`，禁止 `QUES-1` / `OQ-1`） |
| 2026-11-03 | 本篇 `D1`–`D8`/`D1-*` 重命名为 **DSGN-A**–**DSGN-M** |
| 2026-11-03 | Testing Decisions → `../test-plan/document-standard-test-plan.md` |
| 2026-11-03 | Feature 级 test plan（parent 仅 harness） |
| 2026-11-03 | Testing Decisions → parent test plan（被测 = skill）；DSGN-L 加 Review 行；doc-write → spec-write |
| 2026-11-03 | **DSGN-N** spec reader HTML → aspect design + `skills/spec-html-standard/` |
| 2026-11-04 | DSGN-E PRD 去掉 NFR；how-to 标未检查；DSGN-F ID 作用域、HLD 例外、标题检查 |
| 2026-11-04 | DSGN-E impl-plan 改为 IMPL-* tasks |
| 2026-11-04 | design 补 User Stories / Implementation Decisions 章节 |
| 2026-11-04 | decision-history 硬 cap 改为不设，与 ARD-E 一致 |
| 2026-11-04 | decision-history 去掉「宜 ≤600 行」，目标行数也不设 |
| 2026-11-06 | impl-plan 正文：依赖、挡住谁、Execution order |
| 2026-11-07 | 入口改为 spec-write 与 spec-review；标准见两份摘要（ARD-AJ） |
| 2026-11-07 | 开篇被测改为 spec-write / spec-review，与 test-plan 一致 |
| 2026-11-07 | Further Notes 写入 ARD-AM–BE 的 DSGN-C/E/F/G/H/J 规则 |
| 2026-11-07 | DSGN-D：book/html 镜像 features 树（ARD-BF） |
| 2026-11-18 | 改已有正文：删除线留旧句，旁边写新句和 ref |
| 2026-11-20 | 全文改写为完整句子；术语表改为链到 parent design；标题去掉「待 Review」；DSGN-B 大表拆成「路径」和「行数」两张；DSGN-F 改已有正文改为只写现行规则、删除线只在 decision-history（ARD-BM）；DSGN-M 分 MUST 与 NICE（ARD-BN）；Testing Decisions 被测改为 spec-write 与 spec-review；Open Questions 改为 QUES 清单；补写子问题归属不适用的说明（ARD-BK） |
| 2026-11-20 | 第 1 轮审查后：DSGN-E 加入可读性、未决问题清单、引用代码、impl 依赖两头对得上（ARD-BO、ARD-BS）；DSGN-C 加翻译副本、DSGN-F 加对照表和旧锚点、DSGN-J 加每条 ARD 都有说明，原来只在 Further Notes 里的规则移进正文；DSGN-B 六种文档都可拆分篇并需入口文件（ARD-BQ），写明辅助文件例外；跨 feature 的编号写明出处 |
