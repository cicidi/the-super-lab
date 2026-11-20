---
feature: spec-driven-development
type: test-plan
state: draft
final_date: 2026-11-03
health: active
owner: cicidi
last_verified: 2026-11-20
---

# Spec-Driven Development — 测试计划

本篇是整个 SDD 唯一的测试计划，sub-feature 不另写。

- **被测对象：** spec-write 和 spec-review 两个 skill。它们是仅有的交付物（[ARD-BH](../decision-history/spec-driven-development-decision-history.md#ard-bh)）。
- **判断对错的依据：** `SPEC-STANDARD.md` 和 `SPEC-PRESENTATION.md`，以及它们摘要的 document-standard design。
- **验收方式：** 人不读 skill 的正文；skill 好不好用，只看本计划的测试结果。

术语见 [parent design 的术语表](../design/spec-driven-development-design.md#glossary)。

## Test Scope

**要测的：** 把 spec-write 和 spec-review 装进任意项目后的行为。输入有三类：本仓库的 `docs/features/`、外部仓库（路径在 `eval.yaml` 里指定）、人工做的小样例（fixture）。可读性也在测试范围内（TST-V，[ARD-BO](../decision-history/spec-driven-development-decision-history.md#ard-bo)）。

**不测或暂时测不了的（Unverified）：**

- skill 正文怎么改。本篇只规定测什么。
- 设计本身是否合理；文档合并的策略。
- 阶段编排（PRD-I，见 pipeline design 的 QUES-A）。
- 单次改动的大小（PRD-C）。
- 四个非软件例子的 gold（PRD-K）。gold 放在别处；例子写进 skill 正文，由 TST-S 检查。

**parent 和 sub-feature：** spec-review 审 parent（`docs/features/spec-driven-development/` 这一层，不含 `features/<sub>/`）时，要确认五篇都在：prd、design、decision-history、impl-plan、test-plan（parent design 的 DSGN-E）。sub-feature 不要求五篇都有，只审已有的文档。

**几个只在本篇用的词：**

| 词 | 意思 |
|---|---|
| requirement | 固定的需求：「给我推荐一台 iPhone，并帮我购买」 |
| 复核 | 同一个模型独立裁决 3 次，得出最终的通过或不通过。`eval.yaml` 里对应的键叫 `checkers`。它和 Python 检查脚本是两回事 |
| 基线 | 只装被测 skill、不加任何辅助 skill 的配置，即 `grill.skills: []` |

## Test Assets

| 路径 | 内容 |
|---|---|
| `skills/spec-organize/tests/eval.yaml` | 判分模型 `judge.model: deepseek-flash`；gold 案例是 iPhone，版本 v1，路径 `gold/v1/`（[ARD-BL](../decision-history/spec-driven-development-decision-history.md#ard-bl)）；`gold.repeats: 3`；`grill.skills`（基线为 `[]`）；`target.repo: .`（可以用环境变量 `SDD_EVAL_REPO` 覆盖）；`checkers.models: [deepseek-flash]`；`checkers.repeats: 3`；`single_provider: true`。现在的文件还指向 SDD 目录，由 IMPL-P 改回 |
| `skills/spec-organize/tests/checks/` | Python 检查模块，每个机械 MUST 一个模块，清单见同目录的 `README.md` |
| `skills/spec-organize/tests/mock-mcp/` | 所有例子共用的 mock MCP 客户端和服务器，提供几个固定的工具；调用时打印调用记录，不真的下单 |
| `skills/spec-organize/tests/fixtures/neg/<check>/` | 反例：每个检查至少一个最小的违规样例 |
| `skills/spec-organize/tests/fixtures/pos/` | 正例：检查不能误报，例如编号中间有空缺、豁免的路径、`raw/` 下没有 frontmatter 的文件 |
| `skills/spec-organize/tests/must_registry.yaml` | MUST 清单，每条有 `id`（`MUST-` 加字母）、`source`（出处）、`text`、`method`（`python` 或 `llm`）、`check` |
| `skills/spec-organize/tests/gold/v1/` | iPhone gold 案例：`requirement.md`、`context.md`、`context-variants/<名字>.md`、`exemplar/`、`annotations.yaml` |
| `skills/spec-organize/tests/gold/v1/annotations.yaml` | 标注，`GOOD-*` 是应该做到的，`BAD-*` 是不该犯的错。每条有 `where`、`text`；`BAD` 还有 `expected_fix`；`added_in` 记录是哪个 gold 版本加的 |
| `skills/spec-organize/tests/reports/<run_id>.html` | 评测报告，一次运行一个 HTML；`run_id` 是「日期加分支名」；由 `tools/render_eval_report.py` 生成；不提交 |
| `skills/spec-review/tests/cases/<名字>/` | 审查案例：`input/`（故意埋了问题的文档）和 `expected.yaml`（应该找出的问题编号，以及应该忽略的严重度 1、2 的问题）；11 个机械案例，5 个语义案例 |

这套 SDD spec 本身不是打分用的 gold。它是写法样板，由 spec-review 审查，不参与打分（[ARD-BL](../decision-history/spec-driven-development-decision-history.md#ard-bl)）。

**分支：** 评测产出写在 `target.repo` 的新分支 `eval/<gold 版本>/<run_id>` 上，不开 PR。`runs/` 和 `reports/` 不提交。gold 的需求、背景资料、范例、标注可以提交。跨 skill 的检查器、gold、报告都放在 `skills/spec-organize/` 下（[ARD-Q](../decision-history/spec-driven-development-decision-history.md#ard-q)）。

## Scoring

**分数 1：MUST 合规。** 得分是「通过的条数 / 总条数」，总条数是 `must_registry.yaml` 里的条目数。`method: python` 的由检查脚本判断，`method: llm` 的由判分模型判断，每条只有通过或不通过。

**分数 2：和 gold 比。** 对 `annotations.yaml` 里的每一条打分：

| 标注 | 产出里有类似的 | 产出里没有 |
|---|---|---|
| GOOD | +1 | 0 |
| BAD | −1（犯了这个错） | 0 |

分数 2 =（加分合计 − 减分合计）× 10 ÷ 标注总数。满分 10，可以是负数。「类似」由判分模型判断。只在同一个 gold 版本内比较。

**门槛：** 分数 1 必须满分；分数 2 不能低于同一 gold 版本的上一次运行（[ARD-R](../decision-history/spec-driven-development-decision-history.md#ard-r)）。复核用同一个 `deepseek-flash` 独立裁决 3 次，3 次都通过才算通过，而且复核不能推翻 Python 检查的结果。不同模型之间的偏差暂时测不了，标为 Unverified。

**分数的用途：** 分数 1 和分数 2 是评测指标，不是产品的成功指标（PRD-G、[ARD-N](../decision-history/spec-driven-development-decision-history.md#ard-n)）。

**gold 增长：** 运行中发现新的好例子或坏例子，追加到 `annotations.yaml`，gold 版本号加一，`added_in` 写上新版本。报告里必须写明 gold 版本（[ARD-S](../decision-history/spec-driven-development-decision-history.md#ard-s)）。

## Test Cases

### TST-A — 生成 MUST 清单

**目标：** 扫描 document-standard design、pipeline design，以及 parent design 的 DSGN-A、DSGN-B，把所有「必须」「禁止」类规则收进 `must_registry.yaml`。spec 定稿后重新扫描。**输入：** 这三篇 design。**通过条件：** 覆盖率 100%；每条都标明 `python` 或 `llm`；NICE 规则不收（[ARD-BN](../decision-history/spec-driven-development-decision-history.md#ard-bn)）。**判定：** 出处比对脚本（`registry_provenance`）。

### TST-B — 检查脚本的反例和正例

**目标：** 证明检查脚本真的有效。**输入：** `fixtures/neg/*` 和 `fixtures/pos/*`。**通过条件：** 每个反例都报错；每个正例都不报错。**判定：** pytest。

### TST-C — 生成 gold（跑 3 次）

**目标：** 在基线配置下，用 iPhone 案例跑 3 次，写出 3 套 feature spec（[ARD-BL](../decision-history/spec-driven-development-decision-history.md#ard-bl)）。**输入：** `gold/v1/requirement.md` 和 `gold/v1/context.md`；`grill.skills: []`；`deepseek-flash`。**通过条件：** 每套都有 prd、design、decision-history、impl-plan、test-plan。**判定：** Python 检查文件，判分模型检查内容。不同模型之间的偏差标为 Unverified。

### TST-D — 提炼 gold

**目标：** 从 3 次运行的产出里，整理出范例 `exemplar/` 和第 1 版标注 `annotations.yaml`。**输入：** TST-C 的产出。**通过条件：** 范例通过 TST-B，分数 1 满分；每条标注都有 `where` 和 `text`；`BAD` 都有 `expected_fix`。**判定：** Python，加上人工认可（记在 Change Log）。

### TST-E — spec-write 的正常流程

**目标：** 修改 skill 后，用同一个需求重跑。**输入：** 同 TST-C。**通过条件：** 分数 1 满分；分数 2 不退步。**判定：** Python 加判分模型。

### TST-F — spec-write 的异常输入

**目标：** 背景资料有坑时，AI 不自己猜。**输入：** `context-variants/` 下的四种：`budget-conflict`（预算冲突）、`family-disagree`（家人意见不一）、`missing-info`（缺信息）、`midway-change`（中途改主意）。**通过条件：** 都要报告或询问。预算冲突和家人意见不一：decision-history 里看得出先后，就取较晚的那条，否则问用户，不能猜。中途改主意：要新加一条 ARD，旧的划掉并链到新的。缺信息：不能编造。**判定：** 判分模型，加 Python 检查 ARD 的结构。

### TST-G — 审查真实的文档

**目标：** 检查别人写的 spec 是否合规。**输入：** 本仓库的 `docs/features/`；外部仓库的路径。**通过条件：** spec-review 报出的机械问题和 `checks/` 的结果一致；豁免的路径不报。**判定：** Python 对比两份结果。

### TST-H — spec-review 找问题的能力

**目标：** 问题找全，而且不误报。**输入：** 11 个机械案例和 5 个语义案例；一份干净的范例。**通过条件：** 埋进去的每个问题都被找出，并引用对应的 DSGN 或 MUST 编号；干净的范例上没有严重度 3 及以上的问题；严重度 1、2 的问题不拿出来讨论。**判定：** 比对编号集合。

### TST-I — spec-review 修改建议的质量

**目标：** 修改建议是对的。**输入：** TST-H 找出的问题。**通过条件：** 把建议和 `expected_fix` 比较：照着建议改了之后，问题消失，而且没有引入新的 MUST 违反。**判定：** 判分模型；报告「建议正确的条数 / 找出的条数」。

### TST-J — 不同评测配置

**目标：** 比较加不同辅助 skill 的效果。**输入：** `grill.skills` 分别为 `[]`、`[wayfinder]`、`[grill-with-docs]`、两个都加。**通过条件：** 每种配置出一份报告；先跑基线；只报分数，不设门槛。**判定：** 同 TST-E。

### TST-K — 评测报告

**目标：** 每次运行生成一个 HTML 报告。**输入：** 任意一次运行。**通过条件：** 报告里有 run_id、分支、gold 版本、评测配置、分数 1 的逐条结果（注明 python 或 llm）、分数 2 的加减分、TST-F 四种输入的结果、3 次复核的结果。**判定：** 生成报告，再按结构检查。

### TST-L — 3 次独立复核

**目标：** 得出最终的通过或不通过。**输入：** 评测报告和改动。**通过条件：** 同一个 `deepseek-flash` 独立裁决 3 次，3 次都通过；不推翻 Python 检查的结果。**判定：** 跑 3 次。不同模型之间的偏差标为 Unverified。

### TST-M — 改了标准或 gold 之后同步测试

**目标：** 标准或 gold 变了，测试要跟着变。**输入：** 改了 `SPEC-STANDARD.md` 或 design；或者运行中发现了新的好例子、坏例子。**通过条件：** design 改了，同一批重跑 TST-A，并更新 MUST 清单和反例；加了新标注，gold 版本号加一。**判定：** 检查流程是否执行，以及覆盖率。

### TST-N — parent 五篇齐全，sub-feature 不要求

**目标：** parent 五篇都在；sub-feature 不会因为缺篇而失败。**输入：** SDD 的 parent 目录，以及 `features/pipeline/`、`features/document-standard/`。**通过条件：** parent 缺任何一篇，spec-review 报出严重度 3 及以上的问题；sub-feature 只有 design 也能通过。**判定：** Python 检查路径，加 spec-review 的报告。

### TST-O — PRD 到 design 的追溯

**目标：** PRD 的每条需求，在 design 里都有对应的规则。**输入：** parent PRD、parent design、pipeline design、document-standard design。**通过条件：** 每个 `PRD-*` 至少对应一个 `DSGN-*` 或 `PIPE-*`；有没对应上的就失败。**判定：** Python 比对编号集合。

### TST-P — 子问题归属、证据、UNKNOWN

**目标：** 有子问题的 design 都有「子问题归属」表，结论都能追溯。**输入：** 带归属表的 design；故意写了没有依据的结论的样例；`UNKNOWN` 的样例。**通过条件：** 缺表就失败；有结论没依据就失败；把 `UNKNOWN` 当事实写就失败。**判定：** Python 检查表的结构，判分模型判断依据的质量。

### TST-Q — mock MCP 的调用记录

**目标：** 执行只做到 mock。**输入：** `skills/spec-organize/tests/mock-mcp/` 的客户端和服务器。**通过条件：** 调用时打印出记录（工具名、参数、结果）；没有真实的下单或订票。**判定：** Python 检查记录存在、没有真实副作用。

### TST-R — 网页不能比 markdown 旧

**目标：** 网页不落后于 markdown。**输入：** `docs/book/html/spec-driven-development/spec-driven-development-reader.html` 和它的所有源 `.md`。**通过条件：** 网页的修改时间不早于任何一个源文件；否则失败。**判定：** Python。

### TST-S — skill 正文里的四个例子

**目标：** spec-write 和 spec-review 的正文都包含 PRD-Q 的四个例子。**输入：** 这两份 `SKILL.md`。**通过条件：** 每份都至少提到盖 shed、北京旅游、数学题、股票；缺一个就失败。**判定：** Python 查关键词，判分模型判断是否只是点了个名。

### TST-T — 外部仓库的参照 gold

**目标：** 在有问题的那个快照上，清单里应该找出的问题都被报出来；在修好的快照上，除了允许的以外没有任何问题。源仓库不在本机时跳过。**输入：** `gold/refs/<名字>/manifest.yaml`（[ARD-BD](../decision-history/spec-driven-development-decision-history.md#ard-bd)）。**判定：** Python。不把别人的 spec 原文复制进本仓库。

### TST-U — 问题编号、任务依赖、删除线、字号

**目标：** skill 和 gold 跟上现行标准。**输入：** 两份交付的 `SKILL.md`、`gold/v1/annotations.yaml`、reader 网页。**通过条件：** spec-write 的正文写了 `QUES-A` 这样的编号、写了 impl 任务要写依赖；并且规定删除线只用在 decision-history（[ARD-BM](../decision-history/spec-driven-development-decision-history.md#ard-bm)）。gold 里有三条坏例子：`QUES-1` 这样的数字编号、没有写依赖的 impl 任务、正文里出现删除线。reader 网页有「隐藏删除线」按钮，二级标题比三级标题大。**判定：** Python。

### TST-V — 本科生读得懂

**目标：** 每篇已提交的文档，本科水平的程序员只读这一篇就能读懂（PRD-M，[ARD-BO](../decision-history/spec-driven-development-decision-history.md#ard-bo)）。

**输入：** 一篇文档，加上 [parent design 的术语表](../design/spec-driven-development-design.md#glossary)。被测的有两类：SDD 自己的每篇文档；TST-C、TST-E 里 spec-write 写出的每篇文档。

**做法：**

1. 从这篇文档的编号条目（`PRD-*`、`DSGN-*`、`PIPE-*`、`IMPL-*`、`TST-*`、`ARD-*`）里，每条出一道题，最多抽 20 道。例如「PRD-F 规定，多人的决定冲突时怎么办」。
2. 对照：不给文档，先问一遍。不看文档也能答对的题太容易，作废。
3. 让判分模型扮演本科程序员，只读这一篇和术语表，回答剩下的题。
4. 再让它列出这篇里第一次出现时没有解释、术语表里也没有的词。

**通过条件：** 剩下的题答对至少 80%，并且没解释的词是 0 个。跑 3 次，至少 2 次通过才算这篇通过。可读性判断的波动比 MUST 判断大，所以这里不要求 3 次都通过。

**判定：** 判分模型 `deepseek-flash`。实现见 impl-plan 的 IMPL-Q。

## Test Execution Order

1. TST-A：MUST 清单覆盖率不到 100% 就停。
2. TST-B：检查脚本失效就停。
3. TST-O、TST-P、TST-V：design 的覆盖、证据、可读性。
4. TST-C，然后 TST-D：第一次运行，或者 gold 升版时。
5. TST-G、TST-N、TST-R、TST-S、TST-T、TST-U。
6. TST-E、TST-F。
7. TST-H，然后 TST-I。
8. TST-Q：mock 执行。
9. TST-K，然后 TST-L。
10. TST-J（可选）。
11. 有改动时跑 TST-M，再从第 1 步开始。

## Expected Pass Threshold

| 门槛 | 条件 |
|---|---|
| 测试框架可用 | TST-A 覆盖率 100%；TST-B 全部通过 |
| 设计完整 | TST-O 100% 对应；TST-P 全部通过 |
| 读得懂 | TST-V：每篇都通过 |
| mock 执行 | TST-Q 有调用记录，没有真实副作用 |
| 网页和 skill 正文 | TST-R 网页不旧于 markdown；TST-S 四个例子齐全；TST-U 通过 |
| 外部 gold | TST-T：有问题的快照上，应该找出的都找出；修好的快照上，除了允许的以外 0 个问题；源仓库不在本机就跳过 |
| gold v1 定稿 | TST-D：范例的分数 1 满分；标注经人工认可 |
| spec-write 可以发布 | TST-E 分数 1 满分、分数 2 不退步；TST-F 四种输入全部通过；TST-G 没有差异；TST-L 3 次都通过 |
| spec-review 可以发布 | TST-H 找出 100%、误报 0；TST-I 不低于上一次；TST-L 3 次都通过 |
| gold 升版 | TST-M 追加标注后，重跑 TST-E 和 TST-H，建立新的基线 |

## Traceability

| PRD | Covered by |
|---|---|
| PRD-A | Unverified（阶段编排） |
| PRD-B | TST-E；TST-H |
| PRD-C | Unverified（单次改动大小，PRD-I） |
| PRD-D | TST-B（行数上限） |
| PRD-E | TST-B（路径） |
| PRD-F | TST-B（decision_log）；TST-F |
| PRD-G | Unverified（[ARD-N](../decision-history/spec-driven-development-decision-history.md#ard-n)） |
| PRD-H | TST-M；TST-S |
| PRD-I | Unverified（本表里的 Unverified 标注本身就是这条的落实） |
| PRD-J | Unverified（阶段编排，PRD-I） |
| PRD-K | TST-S |
| PRD-L | TST-P |
| PRD-M | TST-V |
| PRD-N | TST-P；TST-F |
| PRD-O | TST-Q |
| PRD-P | TST-S；Expected Pass Threshold 表 |
| PRD-Q | TST-S |

## Change Log

| Date | Change |
|------|--------|
| 2026-11-03 | Initiative harness only；Phase 1 测例在 document-standard test-plan |
| 2026-11-03 | document-standard 改回 feature 级 test plan |
| 2026-11-03 | 重写为 initiative 级：被测 = spec-organize / spec-review；两分制；gold 版本化；资产在 skills/<skill>/tests |
| 2026-11-03 | 移除 wayfinder-import 例外与 out-of-scope 项 |
| 2026-11-03 | §8 对齐：parent 五篇齐备（TST-N）；sub 豁免 |
| 2026-11-04 | 被测三 skill + spec-pipeline 编排 out of scope（HLD §7） |
| 2026-11-04 | 验收：四个 skill 是产出；人不读正文，只看测试结果 |
| 2026-11-04 | PRD-C 单次编辑大小列为测不了，移出 test plan |
| 2026-11-04 | TST-F：多人冲突取 decision history 较晚者，否则问用户，不得猜 |
| 2026-11-04 | 选择题：PRD-M 与四套 gold 移出本计划；PRD-N 评测只用 context |
| 2026-11-04 | 单模型 deepseek-flash 3 次 run；gold case/version/exemplar/annotations 四词；runs/reports 不入库 |
| 2026-11-04 | 新增 TST-O PRD→design、TST-P 归属/证据、TST-Q mock MCP、TST-R reader、TST-S 四例 |
| 2026-11-04 | TST-D/TST-K 改为 3 次 run/checker；TST-H 改为 11 机械 + 5 语义案例 |
| 2026-11-04 | 标注 gold 实际目录 v1 与目标 iphone/v1 的迁移 |
| 2026-11-07 | 被测改为 spec-write 与 spec-review；TST-S 只查这两份（ARD-AJ） |
| 2026-11-07 | TST-T：外部 gold 只留 manifest，不复制私有正文（ARD-BD） |
| 2026-11-07 | TST-R 输入改为 docs/book/html/ 下的 reader（ARD-BF） |
| 2026-11-18 | TST-U：QUES、impl 依赖、删除线、字号 |
| 2026-11-18 | 验收：产出只有 spec-write 与 spec-review（ARD-BH） |
| 2026-11-18 | Gold spec 改为这套 spec-driven-development（ARD-BJ） |
| 2026-11-18 | 资产表与 TST-C 改指这套 spec；`gold/v1` 只是练习案例（ARD-BJ） |
| 2026-11-20 | gold 改回 iPhone 案例，资产表与 TST-C 去掉删除线（ARD-BL、ARD-BM）；新增 TST-V 可读性测试，PRD-M 从 Unverified 改为由 TST-V 覆盖（ARD-BO）；TST-E、TST-F、TST-G 和发布门槛从 spec-organize 改为 spec-write 和 spec-review；「checker」改称「复核」，避免和检查脚本混淆；TST-U 改为删除线只在 decision-history；TST-A、TST-N 改引 parent design 的 DSGN 编号；TST-S、TST-T 按编号顺序排列；追溯表补上能对应的测试；全文改写为完整句子（ARD-BK） |
