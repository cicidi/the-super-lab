---
feature: document-standard
type: design
state: draft
final_date: 2026-11-03
health: active
owner: cicidi
last_verified: 2026-11-20
---

# Document Standard — 给人读的 HTML 页面（Design）

本篇是 [document-standard-design.md](document-standard-design.md) 的分篇，规则编号 DSGN-N。需求见 [reader PRD](../prd/document-standard-prd-spec-reader-html.md)（PRD-A 到 PRD-P）。路径规则和 DSGN-B 一致，内容优先级和 DSGN-I 一致，编号和 DSGN-F 一致。术语见 [parent design 的术语表](../../../design/spec-driven-development-design.md#glossary)。

生成网页时要遵守的规则摘要在 `SPEC-HTML-STANDARD.md` 和 `SPEC-PRESENTATION.md`，它们是两个 skill 要读的三份标准文件中的两份（[ARD-BX](../../../decision-history/spec-driven-development-decision-history.md#ard-bx)）。markdown 是全文，HTML 只是方便阅读的视图。spec-write 只改 markdown；spec-review 检查 HTML 有没有丢内容（[ARD-AJ](../../../decision-history/spec-driven-development-decision-history.md#ard-aj)）。

## Problem Statement

1. feature spec 有很多篇、好几层，人很难一次读完。
2. 如果「好读的 HTML」被写成短摘要，审查和新人上手时就会漏掉 MUST 规则，这违反了 document-standard 的「L1 永远不删」。
3. 早期 spec-pipeline 里的 `SPEC-READER.md` 写过「概括并改写」，容易被理解成可以大幅删减。这种理解作废，以本篇的 DSGN-N 为准。

## Solution

规定一种叫「spec reader」的 HTML 产物：静态网页，排版好读，内容不丢。它从已提交的 markdown 派生出来，正式版本永远是 markdown。

---

## Design

### DSGN-N — 给人读的 HTML 页面

#### DSGN-N-A — 产物和路径

来源：reader PRD 的 PRD-E、PRD-F。

| 项 | 规则 |
|---|---|
| 文件名 | parent 的汇编页是 `<parent>/<parent>-reader.html`。其他页面和对应的 `.md` 在 `docs/features/` 下的相对路径相同，只把扩展名改成 `.html` |
| 目录 | 都放在 `docs/book/html/` 下，parent 和 sub-feature 都一样；不放在 `docs/features/` 或 `site/` 里（[ARD-BF](../../../decision-history/spec-driven-development-decision-history.md#ard-bf)） |
| 真相来源 | 每一页对应的一篇或几篇已提交的 `.md`。HTML 是派生物 |
| 现在怎么生成 | 由 `tools/build_sdd_site.py` 和 `tools/build_sdd_reader.py` 从 markdown 生成。例子：`docs/book/html/spec-driven-development/spec-driven-development-reader.html` |

#### DSGN-N-H — 单篇页面

来源：reader PRD 的 PRD-F、PRD-J。

- markdown 是源头，HTML 是派生物。
- markdown 里用 `<!-- html-skip -->` 包住的内容可以不显示，但不能用它包住 L1 内容。
- decision-history 里被划掉的句子在 HTML 里也保留。页面上有一个按钮，可以切换「显示删除线」和「隐藏删除线」。
- 脚本生成的页面每次从 markdown 重新生成，不带 `spec-paired` 标记。手工维护的页面要带三个标记：`spec-paired=hand-maintained`、`spec-source`（源 markdown 的路径）、`spec-source-sha256`（源文件的哈希）。源文件变了而页面没变，哈希就对不上，检查会报「过期」（[ARD-AK](../../../decision-history/spec-driven-development-decision-history.md#ard-ak)）。
- 手工维护的页面如果有更新记录，要覆盖 markdown Change Log 里的每个日期（[ARD-BA](../../../decision-history/spec-driven-development-decision-history.md#ard-ba)，NICE）。

#### DSGN-N-B — 内容不丢（MUST）

来源：reader PRD 的 PRD-A、PRD-G、PRD-J、PRD-K。

把 DSGN-I 的四个优先级对应到 HTML：

| 级别 | 在 HTML 里怎么处理 |
|---|---|
| L1 | 全部显示：MUST 和禁止事项、需求表的每一行、测试用例、实现任务、Decision Log 的每一行（带编号）、接口表的数据行、Out of Scope、前提假设、边界、安全规则、错误处理。不能用一段话代替整张表或整节 |
| L2 | 事实保留；可以写得更短，或者放进提示框，但不能删掉理由里的结论 |
| L3 | 放弃的方案等，可以压成要点，加一句「详见原文」 |
| L4 | 可以不显示正文，但必须在页脚或链接里指向 markdown |

**编号必须可见（MUST）。** HTML 里要原样显示编号，例如 `PRD-A`、`DSGN-B`、`ARD-C`、`IMPL-C`、`TST-A`，方便和审查结果、MUST 清单对照。

**不允许（MUST NOT）：**

- 只留「问题」「方案」各一段，删掉 Design 下面各个 DSGN 小节的正文。
- 用「见原文」代替一整页。（一节里面的 L3、L4 可以指向原文。）
- 做成 markdown 预览：整页 `<pre>`，或者没排版的 markdown 原文。

**允许：**

- 把 markdown 表格改成 HTML 表格。列可以合并显示，但行一行都不能少。
- 把长段落分段，加提示框，加小流程图，前提是 L1 的内容一条都不少。
- 一种文档有多个分篇时，按分篇分开显示。

#### DSGN-N-C — 汇编页的结构

来源：reader PRD 的 PRD-C、PRD-D。

parent 的汇编页（reader）把 parent 和各个 sub-feature 的文档放在一页里，方便从头读到尾。它是全站的一页，在左侧目录的「3 design」下面（[ARD-BI](../../../decision-history/spec-driven-development-decision-history.md#ard-bi)）。

- **页面顶部（MUST）：** 说明这是方便阅读的汇编页，要改内容去改 `.md`；写明 parent 的名字。
- **parent 部分：** 每种存在的文档一部分：PRD、Design、Impl plan、Test plan、Decision history；how-to 可选。
- **sub-feature 部分：** 每个 `docs/features/<parent>/features/<sub>/` 一部分，至少包含它的 design 入口和 design 分篇。
- **每部分底部（MUST）：** 写 `Canonical:` 加原文相对仓库根目录的路径；有多个分篇时，全部列出。

早期的汇编页用多个 Tab 切换，现在改成全站目录加汇编页（[ARD-BG](../../../decision-history/spec-driven-development-decision-history.md#ard-bg)）。

#### DSGN-N-I — 全站目录

来源：reader PRD 的 PRD-C。

全项目只有一个网站，入口是 `docs/book/html/index.html`。每篇 spec 的 HTML 是目录里的一行。先在目录里选 feature；进入后，左边是这个 feature 的目录，右边是正文（[ARD-BG](../../../decision-history/spec-driven-development-decision-history.md#ard-bg)）。

#### DSGN-N-K — 正文里的链接

来源：reader PRD 的 PRD-D、PRD-H。

- 正文里出现的编号（`PRD-`、`DSGN-`、`ARD-`、`IMPL-`、`TST-`、`PIPE-`、`QUES-`）要链到它的定义。编号前面写明了出处（例如「parent design 的 DSGN-A」或 `<feature>/<编号>`），就链到那个 feature。没写出处，才先找本 feature；本 feature 里没有，再链到 parent。
- 指向 `docs/features/` 下 `.md` 的链接，改成指向 `docs/book/html/` 下同路径的 HTML。没有单独页面的文档（例如 pipeline design，见 DSGN-N-L），链到汇编页里对应的那一节。
- 指向其他已存在文件的链接，直接链到那个文件。

#### DSGN-N-L — 左侧目录的序号和层级

来源：reader PRD 的 PRD-C。

左侧目录显示层级和序号：1 prd、2 decision-history、3 design、4 impl plan、5 test plan、6 how to、10 sub-feature。design 的分篇和汇编页放在 3 下面。sub-feature 单独成一组，在 10 下面逐个展开。pipeline 在左侧目录里没有单独的页面，它的内容收在汇编页里（[ARD-BI](../../../decision-history/spec-driven-development-decision-history.md#ard-bi)）。

#### DSGN-N-D — 视觉和技术要求

来源：reader PRD 的 PRD-B、PRD-H、PRD-L、PRD-O、PRD-P。

- 全站用同一套样式：页面布局、编号标签、卡片、提示框（NICE，[ARD-BY](../../../decision-history/spec-driven-development-decision-history.md#ard-by)）。
- 把 CSS 写在页面里，用浏览器直接打开文件也能正常显示（NICE）。
- 允许内嵌 Mermaid 流程图（Mermaid 是一种用文字描述、由浏览器画成图的格式）；没有先例时用文字画的流程图。
- 页面里不能有密钥，也不能有 `raw/` 里给机器用的评测原文；需要的话只放路径（MUST）。
- 不能在运行时读取 `.md` 文件来显示主要内容；只有调试时可以（MUST）。
- 页面标题、节、小节、条目的字号、粗细、样式各不相同；段落前面不加 a、b、c 或 1、2、3 这类序号（MUST）。

#### DSGN-N-E — 谁负责什么

来源：reader PRD 的 PRD-I、PRD-M、PRD-N。

| 角色 | 负责 |
|---|---|
| spec-write | 只改 markdown，不管 HTML 模板；改完后提示重新生成网页（PRD-M） |
| spec-review | 检查网页有没有丢 L1 内容、编号是否可见 |
| `SPEC-HTML-STANDARD.md` | `skills/spec-html-standard/` 下的规则摘要，是 DSGN-N 的可执行版本；没有对应的 SKILL.md |
| spec-organize | 负责路径和 INDEX，不负责生成网页 |

spec-pipeline 里的 `SPEC-READER.md` 如果还在，只能是指向本篇和 `SPEC-HTML-STANDARD.md` 的链接，避免出现两份规则。

#### DSGN-N-F — 什么时候重新生成

来源：reader PRD 的 PRD-M。

- parent 或任何 sub-feature 的已提交文档有实质修改（尤其是 L1、L2）之后，重新生成（NICE；网页过期由 parent test-plan 的 TST-R 检查）。
- 用户明确要求时，例如「生成 reader」「生成网页」「reader 太简略了，补全」。
- 只改了错别字的提交，不必每次都重新生成（NICE）。

#### DSGN-N-G — 以后的 markdown 转 HTML

可以再加一份机械转换的规则，例如分篇 `document-standard-design-md-to-html.md`，规定 markdown 的每种结构对应哪种网页组件。自动转换仍然必须满足 DSGN-N-B。本篇和 `SPEC-HTML-STANDARD.md` 规定的是「要达到什么效果」。

---

## User Stories

用户故事见 [reader PRD](../prd/document-standard-prd-spec-reader-html.md#user-stories) 的 PRD-G 到 PRD-I。是否做到，以 DSGN-N-B 为准。

## Implementation Decisions

| ID | 决定 |
|---|---|
| DSGN-N-M | reader 的规则挂在 document-standard 下面，不挂在 pipeline design 下面，因为它属于「文档长什么样、怎么读」，和 DSGN-A 是同一类 |
| DSGN-N-N | 最初的网页是手工维护的，所以先把「内容不丢」写进规则，防止 AI 再做出过度精简的页面。现在已改为脚本生成（DSGN-N-A） |
| DSGN-N-J | 可执行的规则放在 `skills/spec-html-standard/SPEC-HTML-STANDARD.md`；document-standard 入口文件的编号表链到本篇；不新建 reader skill |

**编号对照（[ARD-AP](../../../decision-history/spec-driven-development-decision-history.md#ard-ap)、[ARD-BZ](../../../decision-history/spec-driven-development-decision-history.md#ard-bz)）：** 本表原来的 DSGN-N-H 和 DSGN-N-I，和后来加的两个小节（单篇页面、全站目录）用了同样的编号，违反了「编号不复用」（DSGN-F）。小节保留原编号，本表改为 DSGN-N-M 和 DSGN-N-N：

| 旧 | 新 |
|---|---|
| Implementation Decisions 里的 DSGN-N-H | DSGN-N-M |
| Implementation Decisions 里的 DSGN-N-I | DSGN-N-N |

## Testing Decisions

- parent test-plan 的 TST-R：网页不能比 markdown 旧。
- parent test-plan 的 TST-U：网页有「隐藏删除线」按钮，二级标题比三级标题大。
- 可选（NICE）：spec-review 抽查网页里是否包含 markdown 中所有的 PRD、DSGN、TST 编号。

## Out of Scope

- 在 CI 里强制要求网页和 markdown 逐字一致。
- 代替 spec-organize 的检查。

## Further Notes

- 早期手工维护的汇编页，很多 design 只剩一句口号。改为脚本从 markdown 全文生成后，按 DSGN-N-B 检查。
- parent design 已经写明网页的路径。交付物只有 spec-write 和 spec-review（[ARD-BX](../../../decision-history/spec-driven-development-decision-history.md#ard-bx)）；网页的规则在 `skills/spec-html-standard/`。

## Alternatives Considered

- **直接嵌入 `.md` 做预览：** 放弃。DSGN-N 要求的是排好版的汇编，不是 markdown 查看器。
- **每个分篇单独一个 HTML，互不相连：** 放弃。读者需要在多篇文档之间来回跳，所以要有全站目录。

## Drawbacks

- 网页和 markdown 会慢慢不一致，需要 parent test-plan 的 TST-R 检查网页是否过期。

## Risks and Mitigations

| 风险 | 应对 |
|---|---|
| 网页被当成正式版本 | 每页底部写明原文路径 |
| 排版时把编号弄丢 | DSGN-N-B 要求编号原样可见 |

## Open Questions

本篇的未决问题记在 [document-standard 的问题清单](document-standard-design.md#open-questions)。和本篇有关的是 QUES-E：Mermaid 图在网页里怎么渲染，要不要统一。

## Reversibility

- 网页是派生物，删掉不影响 spec，重新生成即可。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-03 | Initial aspect design **DSGN-N**；保真规则 |
| 2026-11-03 | **spec-html-standard** 替代 spec-reader skill（**DSGN-N-E/J**） |
| 2026-11-07 | 表达标准 SPEC-PRESENTATION；write 改 md，review 查保真（ARD-AJ） |
| 2026-11-07 | 手写 HTML 须带 spec-source 与 sha256（ARD-AK） |
| 2026-11-07 | DSGN-N-H：单篇阅读视图；手写 changelog 盖住每个 md 日期（ARD-BA） |
| 2026-11-07 | part 链回 document-standard-design.md（ARD-AV） |
| 2026-11-07 | HTML 改到 docs/book/html/，目录与 features 同构（ARD-BF） |
| 2026-11-07 | DSGN-N-I：全站一份目录；feature 页左目录右正文（ARD-BG） |
| 2026-11-07 | DSGN-N-K：正文条目号与路径必须是可用链接 |
| 2026-11-07 | DSGN-N-L：左侧只列五篇；其余展开在 design 下；pipeline 无 HTML |
| 2026-11-07 | DSGN-N-L：子 feature 在 design 下一层占一行，再展开自己的页面 |
| 2026-11-18 | 页顶按钮切换显示或隐藏删除线 |
| 2026-11-18 | 层级靠字号和样式分开，段落不用 a–z 或数字序号 |
| 2026-11-18 | 交付 skill 改为 spec-write 与 spec-review（ARD-BH） |
| 2026-11-18 | 左侧栏序号 1–6 与 10 sub-feature（ARD-BI） |
| 2026-11-20 | DSGN-N-H 的生成稿与手写稿标记改为与 ARD-AK 一致；「参考」行并回 DSGN-N-A 的表；Implementation Decisions 的重复编号改为 DSGN-N-M、DSGN-N-N 并留对照表；DSGN-N-C 从 Tab 改为全站目录加汇编页（ARD-BG）；DSGN-N-D、DSGN-N-E 去掉已删除的旧 HTML 和 spec-pipeline；Testing Decisions 改指 TST-R、TST-U；全文改写为完整句子（ARD-BK） |
| 2026-11-20 | 第 1 轮审查后：DSGN-N-D、DSGN-N-F 的 SHOULD、MAY 改为 NICE 或「允许」；DSGN-N-L 写明 pipeline 没有单独页面、内容在汇编页里 |
| 2026-11-20 | 第 2 轮审查后：每个 DSGN-N 小节写明来源的 reader PRD 编号；DSGN-N-D 加上 PRD-P 的「不放密钥」，样式统一链到 ARD-BY；DSGN-N-K 先按编号前写明的出处链接；对照表链到 ARD-BZ；TST-R、TST-U 写明属于 parent test-plan |
| 2026-11-20 | 第 3 轮审查后：DSGN-N-K 写明没有单独页面的文档链到汇编页的对应一节；交付物改链 ARD-BX；其余 TST-R 写明属于 parent test-plan |
