---
feature: spec-driven-development
type: test-plan
state: draft
final_date: 2026-11-03
health: active
owner: cicidi
last_verified: 2026-11-24
---

# Spec-Driven Development — 测试计划

本篇是整个 SDD 唯一的测试计划，sub-feature 不另写。

- **被测对象：** 交付的三个 skill：spec-write、spec-review，以及只做静态检查（TST-AA）的 wayfinder（[ARD-CH](../decision-history/spec-driven-development-decision-history.md#ard-ch)）。
- **判断对错的依据：** 三份标准文件 `SPEC-STANDARD.md`、`SPEC-PRESENTATION.md`、`SPEC-HTML-STANDARD.md`，以及它们摘要的 document-standard design 和 reader design（[ARD-CH](../decision-history/spec-driven-development-decision-history.md#ard-ch)）。
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

**本篇常用的几个词**（复核、基线也在[术语表](../design/spec-driven-development-design.md#glossary)里，这里补充它们在本篇的用法）：

| 词 | 意思 |
|---|---|
| requirement | 固定的需求：「给我推荐一台 iPhone，并帮我购买」 |
| 复核 | 同一个模型独立裁决 5 次，得出最终的通过或不通过（[ARD-CJ](../decision-history/spec-driven-development-decision-history.md#ard-cj)）。`eval.yaml` 里对应的键叫 `checkers`。它和 Python 检查脚本是两回事 |
| 基线 | 只装被测 skill、不加任何辅助 skill 的配置，即 `grill.skills: []` |

## Test Assets

| 路径 | 内容 |
|---|---|
| `skills/spec-organize/tests/eval.yaml` | 评测配置，每个键的含义见下表。`cases.iphone.path` 指向 iPhone 案例 `gold/v1`（IMPL-P） |
| `skills/spec-organize/tests/checks/` | Python 检查模块，每个机械 MUST 一个模块，清单见同目录的 `README.md` |
| `skills/spec-organize/tests/mock-mcp/` | 所有例子共用的 mock MCP 客户端和服务器，提供几个固定的工具；调用时打印调用记录，不真的下单 |
| `skills/spec-organize/tests/fixtures/neg/<check>/` | 反例：每个检查至少一个最小的违规样例 |
| `skills/spec-organize/tests/fixtures/pos/` | 正例：检查不能误报，例如编号中间有空缺、豁免的路径、`raw/` 下没有 frontmatter 的文件 |
| `skills/spec-organize/tests/must_registry.yaml` | MUST 清单，每条有 `id`（`MUST-` 加字母）、`source`（出处）、`text`、`method`（`python` 或 `llm`）、`check` |
| `skills/spec-organize/tests/gold/v1/` | iPhone gold 案例：`requirement.md`、`context.md`、`context-variants/<名字>.md`、`exemplar/`、`annotations.yaml` |
| `skills/spec-organize/tests/gold/v1/annotations.yaml` | 标注，`GOOD-*` 是应该做到的，`BAD-*` 是不该犯的错。每条有 `where`、`text`；`BAD` 还有 `expected_fix`；`added_in` 记录是哪个 gold 版本加的 |
| `skills/spec-organize/tests/reports/<run_id>.html` | 评测报告，一次运行一个 HTML；`run_id` 是「日期加分支名」；由 `tools/render_eval_report.py` 生成；不提交 |
| `skills/spec-organize/tests/judgments/*-deepseek-flash.yaml` | 复核结论：每条的结论、5 次票数、`claude_audit`、语料 sha；要提交（TST-L） |
| `skills/spec-review/tests/cases/<名字>/` | 审查案例：`input/`（故意埋了问题的文档）和 `expected.yaml`（应该找出的问题编号，以及应该忽略的严重度 1、2 的问题）；11 个机械案例，外加一个干净的；5 个语义案例还没写，要等能判 spec-review 输出的执行器 |

`eval.yaml` 的键：

| 键 | 值 | 含义 |
|---|---|---|
| `judge.model` | `deepseek-flash` | 判分用的模型 |
| `gold.cases` | `gold/v1/` | iPhone 案例（[ARD-BL](../decision-history/spec-driven-development-decision-history.md#ard-bl)） |
| `gold.repeats` | `3` | 每个案例跑几次 |
| `grill.skills` | `[]` | 辅助 skill；空表示基线 |
| `target.repo` | `.` | 写 spec 的仓库；环境变量 `SDD_EVAL_REPO` 可覆盖 |
| `checkers.models`、`checkers.repeats` | `[deepseek-flash]`、`5` | 复核用的模型和次数（[ARD-CJ](../decision-history/spec-driven-development-decision-history.md#ard-cj)） |
| `single_provider` | `true` | 所有模型来自同一家服务商 |

这套 SDD spec 本身不是打分用的 gold。它是写法样板，由 spec-review 审查，不参与打分（[ARD-BL](../decision-history/spec-driven-development-decision-history.md#ard-bl)）。

**分支：** 评测产出写在 `target.repo` 的新分支 `eval/<gold 版本>/<run_id>` 上，不开 PR。`runs/` 和 `reports/` 不提交。gold 的需求、背景资料、范例、标注可以提交。跨 skill 的检查器、gold、报告都放在 `skills/spec-organize/` 下（[ARD-Q](../decision-history/spec-driven-development-decision-history.md#ard-q)）。

## Scoring

**分数 1：MUST 合规。** 得分是「通过的条数 / 总条数」，总条数是 `must_registry.yaml` 里的条目数。`method: python` 的由检查脚本判断，`method: llm` 的由判分模型判断，每条只有通过或不通过。

**分数 2：和 gold 比。** 对 `annotations.yaml` 里的每一条打分：

| 标注 | 产出里有类似的 | 产出里没有 |
|---|---|---|
| GOOD | +1 | 0 |
| BAD | −1（犯了这个错） | 0 |

分数 2 =（加分合计 − 减分合计）× 10 ÷ 标注总数。最高分是 GOOD 标注数 × 10 ÷ 标注总数（全是 GOOD 时才是 10），可以是负数。「类似」由判分模型判断。只在同一个 gold 版本内比较。

**门槛：** 分数 1 必须满分；分数 2 不能低于同一 gold 版本的上一次运行（[ARD-R](../decision-history/spec-driven-development-decision-history.md#ard-r)）。复核用同一个 `deepseek-flash` 独立裁决 5 次，至少 4 次通过才算通过；复核不能推翻 Python 检查的结果（[ARD-CJ](../decision-history/spec-driven-development-decision-history.md#ard-cj)）。不同模型之间的偏差暂时测不了，标为 Unverified。

**分数的用途：** 分数 1 和分数 2 是评测指标，不是产品的成功指标（PRD-G、[ARD-N](../decision-history/spec-driven-development-decision-history.md#ard-n)）。

**gold 增长：** 运行中发现新的好例子或坏例子，追加到 `annotations.yaml`，gold 版本号加一，`added_in` 写上新版本。报告里必须写明 gold 版本（[ARD-S](../decision-history/spec-driven-development-decision-history.md#ard-s)）。

## Test Cases

### TST-A — 生成 MUST 清单

**目标：** 扫描每篇 design 的入口和分篇（document-standard design 和它的 reader 分篇、pipeline design），以及 parent design 的 DSGN-A、DSGN-B、DSGN-C、DSGN-E，把所有「必须」「禁止」类规则收进 `must_registry.yaml`。spec 定稿后重新扫描。**输入：** 上面这些 design。**通过条件：** 覆盖率 100%；每条都标明 `python` 或 `llm`；parent DSGN-A 的单次改动上限不收，它明确不作通过条件（PRD-I）；NICE 规则不收（[ARD-BN](../decision-history/spec-driven-development-decision-history.md#ard-bn)）。**判定：** 出处比对脚本（`registry_provenance`）。

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

**目标：** 问题找全，而且不误报。**输入：** 11 个机械案例和 5 个语义案例（语义案例还没写，这一半暂时跑不了，标为 Unverified）；一份干净的范例。**通过条件：** 埋进去的每个问题都被找出，并引用对应的 DSGN 或 MUST 编号；干净的范例上没有严重度 3 及以上的问题；严重度 1、2 的问题不拿出来讨论。**判定：** 比对编号集合。

### TST-I — spec-review 修改建议的质量

**目标：** 修改建议是对的。**输入：** TST-H 找出的问题。**通过条件：** 把建议和 `expected_fix` 比较：照着建议改了之后，问题消失，而且没有引入新的 MUST 违反。**判定：** 判分模型；报告「建议正确的条数 / 找出的条数」。这个比例不能低于同一 gold 版本的上一次运行；第一次运行建立基线。

### TST-J — 不同评测配置

**目标：** 比较加不同辅助 skill 的效果。**输入：** `grill.skills` 分别为 `[]`、`[research]`、`[grill-with-docs]`、两个都加；wayfinder 是交付物，每种配置都带（ARD-CH）。**通过条件：** 每种配置出一份报告；先跑基线；只报分数，不设门槛。**判定：** 同 TST-E。

### TST-K — 评测报告

**目标：** 每次运行生成一个 HTML 报告。**输入：** 任意一次运行。**通过条件：** 报告里有 run_id、分支、gold 版本、评测配置、分数 1 的逐条结果（注明 python 或 llm）、分数 2 的加减分、TST-F 四种输入的结果、5 次复核的结果和 Claude 的核对意见。**判定：** 生成报告，再按结构检查。

### TST-L — 5 次独立复核

**目标：** 得出最终的通过或不通过。**输入：** 分数 1 的逐条结果和改动；结果写进 TST-K 的报告。**通过条件：** 同一个 `deepseek-flash` 独立裁决 5 次，至少 4 次通过；不推翻 Python 检查的结果。**判定：** 跑 5 次，Claude 再核对没通过和有分歧的条目。结论写进 `judgments/*-deepseek-flash.yaml` 并提交，里面记着语料 sha；SDD 文档、skill 或检查脚本改了，sha 就对不上，`test_judge_freshness.py` 失败，要重跑复核（[ARD-CJ](../decision-history/spec-driven-development-decision-history.md#ard-cj)）。不同模型之间的偏差标为 Unverified。

### TST-M — 改了标准或 gold 之后同步测试

**目标：** 标准或 gold 变了，测试要跟着变。**输入：** 改了 `SPEC-STANDARD.md` 或 design；或者运行中发现了新的好例子、坏例子。**通过条件：** design 改了，同一批重跑 TST-A，并更新 MUST 清单和反例；加了新标注，gold 版本号加一。**判定：** 检查流程是否执行，以及覆盖率。

### TST-N — parent 五篇齐全，sub-feature 不要求

**目标：** parent 五篇都在；sub-feature 不会因为缺篇而失败。**输入：** SDD 的 parent 目录，以及 `features/pipeline/`、`features/document-standard/`。**通过条件：** parent 缺任何一篇，spec-review 报出严重度 3 及以上的问题；sub-feature 只有 design 也能通过。**判定：** Python 检查路径，加 spec-review 的报告。

### TST-O — PRD 到 design 的追溯

**目标：** PRD 的每条需求，在 design 里都有对应的规则。**输入：** parent PRD、document-standard 的 reader PRD，以及 parent design、pipeline design、document-standard design 和它的 reader 分篇。**通过条件：** 两份 PRD 的每个 `PRD-*` 都至少对应一个 `DSGN-*` 或 `PIPE-*`。两份 PRD 的编号会重复（都有 PRD-A），所以按 feature 分开比对：parent 的 PRD 对 parent design、pipeline design 和 document-standard design，reader PRD 对 reader design。parent 的 PRD-G 已延后（[ARD-N](../decision-history/spec-driven-development-decision-history.md#ard-n)），不要求对应；有没对应上的就失败。「对应」指编号出现在 `DSGN-*` 或 `PIPE-*` 规则小节的正文里；只在 Open Questions 或 Change Log 里提到不算。**判定：** Python（`test_tst_o_trace.py`）。

### TST-P — 子问题归属、证据、UNKNOWN

**目标：** 有子问题的 design 都有「子问题归属」表，结论都能追溯。**输入：** 带归属表的 design；故意写了没有依据的结论的样例；`UNKNOWN` 的样例。**通过条件：** 缺表就失败；有结论没依据就失败；把 `UNKNOWN` 当事实写就失败。**判定：** Python 检查表的结构，判分模型判断依据的质量。

### TST-Q — mock MCP 的调用记录

**目标：** 执行只做到 mock。**输入：** `skills/spec-organize/tests/mock-mcp/` 的客户端和服务器。**通过条件：** 调用时打印出记录（工具名、参数、结果）；没有真实的下单或订票。**判定：** Python 检查记录存在、没有真实副作用。

### TST-R — 网页不能比 markdown 旧

**目标：** 网页不落后于 markdown。**输入：** `docs/book/html/spec-driven-development/spec-driven-development-reader.html` 和它的所有源 `.md`。**通过条件：** 用源文件重新生成一遍，除第一行（构建标记）外和已提交的网页逐字相同；否则失败。不比修改时间，新 checkout 的修改时间没有意义。**判定：** Python。

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

1. 从这篇文档的编号条目（`PRD-*`、`DSGN-*`、`PIPE-*`、`IMPL-*`、`TST-*`、`ARD-*`）里，每条出一道题，最多抽 20 道；超过 20 条时从头到尾等间隔抽。这篇没有编号条目时，每个 `##` 小节出一道题。例如「PRD-F 规定，多人的决定冲突时怎么办」。
2. 对照：不给文档，先问一遍。不看文档也能答对的题太容易，作废。
3. 让判分模型扮演本科程序员，只读这一篇和术语表，回答剩下的题。
4. 再让它列出这篇里第一次出现时没有解释、术语表里也没有的词。

**通过条件：** 剩下的题答对至少 80%，并且没解释的词是 0 个。跑 3 次，至少 2 次通过才算这篇通过。可读性判断的波动比 MUST 判断大，所以这里不要求 3 次都通过。

**判定：** 判分模型 `deepseek-flash`。实现见 impl-plan 的 IMPL-Q。

### TST-W — 网页插图与样式

**目标：** 网页里的插图都已经嵌进页面，用 diagram-design 的默认配色；页面里没有留下等待替换的 `data-svg` 占位标记（document-standard 的 DSGN-N-D、[ARD-CA](../decision-history/spec-driven-development-decision-history.md#ard-ca)）。

**通过条件：** `tests/test_sdd_site_render.py` 通过；每个 `-fig-*.svg` 在对应 HTML 中出现一次；`docs/book/html` 里没有 `data-svg="` 占位属性。插图命名、同目录、无脚本由 `checks/figures.py` 检查。

**判定：** Python。

### TST-X — L1 内容不减少

**目标：** 改文档时不靠删 L1 内容凑分（document-standard 的 DSGN-I）。**输入：** 两个 git 版本之间的 `docs/features/<f>/`。

**通过条件：** 旧版本的每个编号标题在新版本里还在；每篇的 MUST 句数不减少。例外：decision-history 新增的 ARD 提到了这个编号或这篇文档。**判定：** Python（`tools/check_l1_delta.py`）。

### TST-Y — skill 版本戳和 PRD 一致

**目标：** 五个 SDD `SKILL.md`（交付的 spec-write、spec-review、wayfinder，以及也引用标准文件的 spec-organize、spec-pipeline）的版本戳等于 parent PRD 的 `version`，且 frontmatter 里的 `spec_*` 键各只出现一次；每次 build 版本末位加 1（[ARD-CK](../decision-history/spec-driven-development-decision-history.md#ard-ck)）。**判定：** Python（`build_spec_skills.py --check` 查戳；升版本由 `test_build_spec_skills.py` 查）。

### TST-Z — 每页都能从首页点到

**目标：** `docs/book/html/` 下每个 HTML 页面都能从 `index.html` 顺着链接点到（[ARD-CD](../decision-history/spec-driven-development-decision-history.md#ard-cd)）。**判定：** Python（`tools/check_site_reachable.py`）。

### TST-AA — wayfinder 执行进度规则

**目标：** `skills/wayfinder/SKILL.md` 写明地图目录的两个位置、任务再小也建地图、阻塞以 QUES 清单为准、提交前问是否跑 spec-review 并记下拒绝、有阻塞问题时不进入 Downstream（[ARD-CH](../decision-history/spec-driven-development-decision-history.md#ard-ch)）。**判定：** Python。

## Test Execution Order

1. TST-A：MUST 清单覆盖率不到 100% 就停。
2. TST-B：检查脚本失效就停。
3. TST-O、TST-P、TST-V：design 的覆盖、证据、可读性。这一步的 TST-V 只测 SDD 自己的文档。
4. TST-C，然后 TST-D：第一次运行，或者 gold 升版时。
5. TST-G、TST-N、TST-R、TST-S、TST-T、TST-U、TST-W、TST-X、TST-Y、TST-Z、TST-AA。
6. TST-E、TST-F，然后对 TST-C、TST-E 里 spec-write 写出的文档跑 TST-V。
7. TST-H，然后 TST-I。
8. TST-Q：mock 执行。
9. TST-L，然后 TST-K（报告要带上复核结果）。
10. TST-J（可选）。
11. 有改动时跑 TST-M，再从第 1 步开始。

## Expected Pass Threshold

| 门槛 | 条件 |
|---|---|
| 测试框架可用 | TST-A 覆盖率 100%；TST-B 全部通过 |
| 设计完整 | TST-N parent 五篇齐全；TST-O 100% 对应；TST-P 全部通过 |
| 读得懂 | TST-V：每篇都通过 |
| mock 执行 | TST-Q 有调用记录，没有真实副作用 |
| 网页和 skill 正文 | TST-R 网页和重新生成的一致；TST-S 四个例子齐全；TST-U、TST-W 通过；TST-Z 每页都能从首页点到；TST-AA wayfinder 写明进度规则 |
| 检查和版本戳 | TST-X 没有 L1 内容减少；TST-Y 版本戳和 PRD 一致 |
| 外部 gold | TST-T：有问题的快照上，应该找出的都找出；修好的快照上，除了允许的以外 0 个问题；源仓库不在本机就跳过 |
| gold v1 定稿 | TST-C 每次运行都写出五篇；TST-D：范例的分数 1 满分；标注经人工认可 |
| spec-write 可以发布 | TST-E 分数 1 满分、分数 2 不退步；TST-F 四种输入全部通过；TST-L 5 次里至少 4 次通过；TST-K 报告结构齐全 |
| spec-review 可以发布 | TST-G 没有差异；TST-H 找出 100%、误报 0；TST-I 不低于上一次；TST-L 5 次里至少 4 次通过 |
| wayfinder 可以发布 | TST-AA 通过 |
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
| PRD-H | Unverified（「优先用已有的热门 skill」没法自动判定） |
| PRD-I | Unverified（本表里的 Unverified 标注本身就是这条的落实） |
| PRD-J | TST-AA（只查 wayfinder 写没写规则；执行效果 Unverified，PRD-I） |
| PRD-K | TST-S |
| PRD-L | TST-P |
| PRD-M | TST-V |
| PRD-N | TST-P；TST-F |
| PRD-O | TST-Q |
| PRD-P | TST-S；TST-AA；Expected Pass Threshold 表 |
| PRD-Q | TST-S |

document-standard 的 reader PRD：

| PRD | Covered by |
|---|---|
| PRD-A、PRD-G、PRD-J、PRD-K（内容不丢） | TST-X 查编号标题与 MUST 句数不减少；逐条比对 L1 内容仍 Unverified |
| PRD-B、PRD-H（排版、标题层级） | TST-U |
| PRD-C、PRD-D、PRD-E（覆盖、原文路径、文件位置） | TST-R 检查汇编页和它的源文件；其余页面 Unverified |
| PRD-F、PRD-I、PRD-N（流程类要求） | Unverified（流程，PRD-I） |
| PRD-L（样式统一） | 不测，是 NICE（[ARD-BY](../decision-history/spec-driven-development-decision-history.md#ard-by)） |
| PRD-M（改完提示重新生成） | TST-R |
| document-standard 的 DSGN-N-D（插图与样式） | TST-W |
| PRD-O、PRD-P（纯静态、不放密钥） | Unverified（还没有对应的检查脚本） |

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
| 2026-11-20 | 第 1 轮审查后：`eval.yaml` 的说明从一个表格单元拆成逐键的表 |
| 2026-11-20 | 第 2 轮审查后：TST-A 扫描所有 design 分篇和 parent 的 DSGN-E；TST-O 加入 reader PRD，追溯表加 reader PRD 一节；TST-V 分两次跑（先测 SDD 文档，spec-write 跑完再测它的产出）；PRD-H 改为 Unverified |
| 2026-11-20 | 第 3 轮审查后：判断依据改为三份标准文件，交付物改链 ARD-BX；TST-O 按 feature 分开比对编号，PRD-G 已延后不要求对应 |
| 2026-11-20 | TST-X：L1 内容不减少 |
| 2026-11-24 | 新增 TST-Y（ARD-CC）；DSGN-N-D 补 feature 名；eval.yaml 现状更新 |
| 2026-11-24 | TST-R 改为比较内容，不比修改时间 |
| 2026-11-24 | 新增 TST-Z：每页都能从首页点到（ARD-CD） |
| 2026-11-24 | TST-O：编号要出现在规则小节正文里才算对应 |
| 2026-11-24 | TST-A：写明 parent DSGN-A 的改动上限不收进清单 |
| 2026-11-24 | TST-X 改引 DSGN-I；TST-W 改成完整句子；TST-Y 写明四个 skill；门槛表补 TST-W 到 TST-Z，TST-R 按内容比较 |
| 2026-11-24 | TST-W 写明查的是 `data-svg="` 占位属性 |
| 2026-11-24 | 复核改为 5 次、至少 4 次通过，Claude 再核对（ARD-CJ）；TST-Y 加升版本（ARD-CK）；新增 TST-AA（ARD-CH） |
| 2026-11-24 | 第 8 轮审查后：被测对象三个 skill；checkers.repeats 改 5；TST-Y 五个 SKILL.md、升版本由单元测试判；TST-AA 加进执行顺序、门槛和追溯表 |
| 2026-11-24 | 第 9 轮审查后：TST-J 的辅助 skill 不再含 wayfinder；门槛表加 wayfinder 发布行；PRD-P 追溯加 TST-AA；改链 ARD-CH |
| 2026-11-24 | 第 10 轮审查后：分数 2 最高分写对；TST-L 先于 TST-K，报告带复核结果 |
| 2026-11-24 | 第 11 轮审查后：语义审查案例标明还没写；门槛表加 TST-N、TST-C、TST-K |
| 2026-11-24 | 第 12 轮审查后：TST-G 移到 spec-review 发布门槛 |
| 2026-11-24 | 第 13 轮审查后：TST-L 写明结论文件提交、语料 sha 过期就重跑 |
| 2026-11-24 | 第 15 轮审查后：TST-A 的输入加 DSGN-C |
| 2026-11-24 | 第 18 轮审查后：TST-I 正文写明不低于上一次；TST-V 写明等间隔抽题和按小节出题 |
