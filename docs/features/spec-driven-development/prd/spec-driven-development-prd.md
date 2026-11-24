---
feature: spec-driven-development
type: prd
state: draft
health: active
owner: cicidi
version: "1.0.7"
last_verified: 2026-11-24
---

# Spec-Driven Development — PRD

## Overview

这份 PRD 说明我们要做什么：一套「先写清楚 spec，再让 AI 去做」的方法，叫 spec-driven development（下文简称 SDD）。

SDD 用五篇文档把一个有门槛的问题分析清楚：PRD（要做什么）、decision-history（做过哪些决定）、design（怎么做）、impl-plan（按什么顺序做）、test-plan（怎么验证做对了）。写文档由 spec-write 这个 skill 负责，检查文档由 spec-review 负责（[ARD-AJ](../decision-history/spec-driven-development-decision-history.md#ard-aj)）。

文中的缩写和术语，例如 skill、ARD、gold，在 [parent design 附录：术语表](../design/spec-driven-development-design.md#glossary) 里有解释。

## Problem Statement

今天，AI 模型的能力已经非常强大。它们可以阅读、搜索最新、最前沿的技术，帮助我们解决问题。

但是，问题是什么？

### 1. Problem 经常没有被定义清楚，更何谈解决

比如这样一个问题：

> 嘿，AI，我买 iPhone 18 Duo 还是 iPhone 18 基础版？

看似是一个简单的问题，但实际上，我们并没有告诉 AI 我们的真实需求。

比如：我们买新的 iPhone 是用来做什么的？我们的 budget 是多少？我们之前是否一直使用 iPhone？我们喜欢 iPhone 的哪些优点，又有哪些缺点？

这些 context，AI 并不知道，因此 AI 的推荐肯定不会准确。

这正是很多人抱怨 AI 不好用的原因。事实上，对于我们自己来说，这看似是一个清楚的问题，但实际上，可能不是 AI 不好用，而是人没有把 problem 定义好。

### 2. AI 真正赋予我们的 superpower，是帮助我们发现 unknown

在我们把问题问清楚以后，AI 也提供了一些思路，甚至 solution。

但是，由于人的能力有限，我们可能根本没有见过某些解决方法或方案。

我们利用已知的信息，找到我们不知道自己知道的信息，同时学习我们知道自己不知道的知识，最后把我们不知道、甚至不知道自己不知道的 blind spot 发掘出来。

这才是 AI 真正赋予我们超能力的地方。

### 3. Decision 不断变化，AI 需要理解、记录并同步这些变化

经常，我们做了一段时间，或者和 team 里的其他人讨论后，会发现一些 decision 一直在改变。

比如：我们买 iPhone 的 budget，和父母、妻子商量未果。我们之前说买 iPhone 的 budget 是 2,000 美金，现在突然变成了 1,000 美金，那么 AI 整个 decision 的方向就会发生彻底的转变。

紧接着，一系列新的问题又会被引入：去哪里买？是不是能够接受二手 iPhone 18 Duo？

当然，随之而来的，去哪里买、如何找 deal 等具体实现方式都会发生改变。

今天的例子比较简单，以后可能会有更复杂的例子：多个人做出多个 decision，到底谁是真理？而这个真理，可能还需要 impact、覆盖其他一些之前的 decision。

比如：爸爸的 budget 是 1,800 美金，妈妈说 1,500 美金；爸爸说下个月可以买，妈妈说这个月可以买。

到底谁是真理？根据这个真理，我们又要如何修改之前的 decision？

这里真正的问题是：当多个参与者做出不同的 decision 时，AI 如何理解这些 decision 之间的关系，判断哪些 decision 是有效的，并根据最新的 decision 更新整个 decision-making process？

### 4. 即使 problem、solution、update、sync 都做好了，人依旧是整个 AI 世界最大的 bottleneck

首先是阅读。

怎么让文件好读、好懂？文件怎么好查找？如何清晰地知道每个文件是做什么的？如何做好 file management？

大的项目不可能只有一个 spec，那么如何切分 spec？如何让不同的 spec 之间保持清晰的关系？以后 AI 和人又该怎么读、怎么查找？

当项目越来越大，文件越来越多，spec 越来越复杂时，我们如何让人和 AI 都能够快速理解整个项目，并准确找到自己需要的信息？

这些都是 AI 真正落地到实际工作中，需要解决的问题。

### 5. 有门槛的难题不只在软件里

盖一个 shed、去北京旅游、看懂一道著名数学题、不靠猜地分析一只股票——人往往从没做过，不知道怎么拆、盲区在哪、哪些要自己拍板。

AI 要把大问题拆成小的：能查的 AI 自己查（合规、财报、交通），要选的人来选（预算、偏好、风险），人想不到的 AI 主动问。spec 既是学习笔记，也是决策记录，最后交给 AI 执行。

## Goals and Success Metrics

**目标：** 任何有门槛的难题，都能拆成三类小问题：AI 能查的、人要决定的、可以交给 AI 执行的。拆完写成一套本科生读得懂、前后一致、结论有依据的 spec。

**验收方式：** 看 test-plan 的测试结果，包括机械检查、对 iPhone 案例的评测分数、可读性测试（[test-plan](../test-plan/spec-driven-development-test-plan.md)）。这些是评测指标，用来判断 skill 好不好用。

**产品级成功指标：** 例如「用了 SDD 的人，决策是否真的更好」。怎么量、基线是多少，目前还定不下来，延后处理（PRD-G，[ARD-N](../decision-history/spec-driven-development-decision-history.md#ard-n)）。

## User Stories

- 作为写 spec 的人，我希望 AI 先追问我，把我已知的、未知的和没想到的盲区都问出来。
- 作为审 spec 的人，我希望格式错误和内容问题都能被找出来，而且每条修改建议都能直接照着做。
- 作为执行的人，我希望 spec 能一路落到 design 和 impl-plan，执行时先用 mock 演练，每个结论都能查到来源。

## Solution

我们不重新解释什么是 spec-driven。这里要做的是一组配合使用的 skill，让 AI 按固定的方法把一个具体问题分析清楚。

**PRD、decision-history、design 三篇是反复打磨的循环**，不是只写一遍的直线。三篇打磨到足够稳定之后，再从 design 分别总结出 impl-plan 和 test-plan。这两篇互不依赖，可以同时写。

1. **PRD**：要做什么、解决什么问题；有哪些限制、偏好、时间要求、可用的资源和工具。design 或某个决定暴露出缺口时，回到 PRD 修改需求。
2. **Decision-history**：根据 PRD 做出的决定。凡是影响方向的决定，先记进 decision-history。这一步大约一半靠 AI 整理、一半靠人拍板。新决定可能改变 PRD 的范围；design 里的取舍也可能需要补一条决定。
3. **Design**：和 PRD、decision-history 一起迭代，写技术方案、接口约定、要用的工具等。写 design 时发现问题没想清楚、或决定不够，就回到第 1 步或第 2 步继续打磨。
4. **Impl-plan**：从 design 总结出实现步骤，包括先做什么、后做什么、每个任务的细节和准备工作。不需要等 test-plan 写完。
5. **Test-plan**：从 design 总结出验证方法，包括每个任务怎么算完成、可用性检查、防止改坏旧功能的回归检查。不需要等 impl-plan 写完。

## Functional Requirements

**PRD-A**：写 spec 的流程沿用现有流程并加以改进，不另造一套。流程分哪几个阶段、每个阶段做什么，写在 [pipeline design](../features/pipeline/design/pipeline-design.md)。

**PRD-B**：提供一组 skill。skill 本质上是写得好的 prompt，引导 AI 完成 spec 的四件事：书写、命名、检查、更新。

**PRD-C**：AI 每次改 `docs/` 下的文档，必须同时满足两条：不超过 10 行，并且不超过 200 字符；新建一个文件不算在内（[ARD-CE](../decision-history/spec-driven-development-decision-history.md#ard-ce)）。更大的改动拆成多次；确实需要一次大改（restructure）时，必须有人明确授权，并记一条 ARD。

**PRD-D**：每篇文档有行数上限，最长不超过 1,000 行，因为太长的文档几乎没法维护。decision-history 例外，不设上限：它只增不减（[ARD-E](../decision-history/spec-driven-development-decision-history.md#ard-e)）。各类文档的具体上限见 document-standard 的 DSGN-B。

**PRD-E**：规定文档放在哪个目录、文件叫什么名字、目录之间是什么关系（parent、sub-feature、peer）。具体规则见 document-standard 的 DSGN-B。

**PRD-F**：多个人的决定互相冲突时，以 decision-history 里时间较晚的那条为准；看不出先后，就问用户。AI 不猜测谁说了算。

**PRD-G**（延后）：产品级成功指标和基线，暂时定不下来，见 [ARD-N](../decision-history/spec-driven-development-decision-history.md#ard-n)。test-plan 里的分数是评测指标，不是产品成功指标。

**PRD-H**：流程里的每一步，优先使用已经流行的 skill，不重新发明。

**PRD-I**：每项改动都要能验证。实在验证不了的，在 spec 里标为 `Unverified` 并写明原因；标了的项不作为 test-plan 的通过条件。

**PRD-J**：写或改 feature spec 时，由 spec-write 按标准判断要新建哪篇、或要改哪几篇；提交前，询问是否先跑 spec-review。写作进度记在 wayfinder 的地图目录里，目录建好前后的位置见 pipeline design 的 PIPE-H（[ARD-CH](../decision-history/spec-driven-development-decision-history.md#ard-ch)）。

**PRD-K**：适用范围不限于软件，任何有门槛的难题都用同一套 spec。四个例子：盖 shed（合规、成本、施工）、北京旅游（行程、住宿、风险、预算）、看懂一道著名数学题（零基础一步步学）、分析一只股票（基本面、财报、新闻，每个结论有依据）。这四个例子不在本仓库建 gold（[ARD-CJ](../decision-history/spec-driven-development-decision-history.md#ard-cj)）。

**PRD-L**：每个子问题都标明由谁处理：AI 查、人决定、或 AI 查完后人决定。人没有问到的盲区和风险，AI 必须主动提出来。

**PRD-M**：文档要让人读懂，这是硬需求，而且是通过条件。交付前，由一个 LLM（大语言模型）扮演本科水平的程序员，只读这一篇文档和术语表，回答从文档里抽出的问题；答错太多，或者有文档里没解释、术语表里也没有的术语，就不算交付（[ARD-BO](../decision-history/spec-driven-development-decision-history.md#ard-bo)）。具体门槛见 test-plan 的 TST-V。

**PRD-N**：正式 spec 里的每个结论，都要能追溯到查到的事实，例如法规条文、财报、新闻、定义，不靠猜。查不到的写 `UNKNOWN`。评测时，AI 回答问题只能用 context 包里给的信息。

**PRD-O**：执行阶段不真下单、不真订票。所有例子共用一个 mock MCP 服务器，提供几个固定的工具；客户端调用后打印出调用记录，就算交付成功。

**PRD-P**：最终交付物是 spec-write、spec-review，以及负责进度规则的 wayfinder 三个 skill（[ARD-CH](../decision-history/spec-driven-development-decision-history.md#ard-ch)）。用它们写出来的 spec，要满足 PRD-K 到 PRD-O。

**PRD-Q**：书写、命名、检查、更新，以及 PRD-K 到 PRD-O，都是需求；spec-write 和 spec-review 能做的事不限于这几件。两个 skill 的正文里都要写出四个例子：盖 shed、北京旅游、数学题、股票。skill 好不好用，只看测试结果。

## Out of Scope

- 真实下单、订票、交易。执行只做到 mock MCP 的调用记录。
- 多人决定的细致仲裁规则，例如两个决定时间相同怎么办。目前只按 decision-history 的先后，看不出就问用户。
- 在本仓库为四个非软件例子建 gold。例子写进 skill 正文，gold 放在别处。
- 把已有的不合规文档批量迁移到新标准。
- skill 和 spec 的迁移策略。版本只做来源标记：每次 build 把 PRD 的 `version` 末位加 1 再印进 skill（[ARD-CK](../decision-history/spec-driven-development-decision-history.md#ard-ck)）。

## Resources Needed

- spec-write、spec-review、wayfinder 三个 skill，前两个要读的三份标准文件（[ARD-CH](../decision-history/spec-driven-development-decision-history.md#ard-ch)），和一份 test-plan。不需要数据库。外部服务：评测用的 `deepseek-flash` API，以及发布网站用的 GitHub Actions 和 GitHub Pages（[ARD-CD](../decision-history/spec-driven-development-decision-history.md#ard-cd)）。
- 评测需要 `deepseek-flash` 的 API，以及生成 gold 跑 3 次、复核跑 5 次的费用。跑分结果和报告不提交（[ARD-CJ](../decision-history/spec-driven-development-decision-history.md#ard-cj)）。

进入下游前，PRD 要写清的五项（pipeline design 的 PIPE-E-B）：

| 项 | 本 PRD |
|---|---|
| 限制 | 每次改动不超过 10 行并且不超过 200 字符（PRD-C）；文档行数有上限（PRD-D） |
| 偏好 | not apply |
| 时间 | not apply |
| 资源 | 上面列出的 `deepseek-flash` API 和评测费用 |
| 工具 | spec-write、spec-review、`run_spec_checks.py` 检查脚本、mock MCP 服务器（PRD-O）、发布网站的 GitHub Actions |

## Change Log

| Date | Change |
|------|--------|
| 2026-11-04 | 新增 Problem 5：有门槛的非软件难题（shed、北京旅游、数学题、股票）要拆成可查/可决策的小问题，spec 兼学习、决策与执行 |
| 2026-11-04 | 新增 PRD-K：范围覆盖非软件难题，四个 gold example |
| 2026-11-04 | 新增 PRD-L：子问题归属（AI 查 / 人决定 / 查完再决定）；AI 主动暴露盲区与风险 |
| 2026-11-04 | 新增 PRD-M：可读性硬需求，LLM 以本科程序员真人身份按「能不能看懂」打分 |
| 2026-11-04 | 新增 PRD-N：结论必须追溯到查到的事实；查不到标未知 |
| 2026-11-04 | 新增 PRD-O：执行用 mock MCP client/server，call 打出 log 即成功 |
| 2026-11-04 | 新增 PRD-P：交付是 spec-organize / spec-review / spec-write / spec-pipeline，写出的 spec 满足 PRD-K 到 PRD-O |
| 2026-11-04 | 新增 PRD-Q：skill 不绑定具体题目，以后的新题也要能做；正文是否点名例子未定，验收只看测试 |
| 2026-11-04 | PRD-F 关闭延期：按 decision history 时间较晚者；看不出先后则问用户；AI 不猜测 |
| 2026-11-04 | 选择题：G/H/J 维持；I 验不了的不进测试；K 的 gold 放到别处；M 测不了；N 评测只用 context；O 共用一个 mock server；Q 正文写出四个例子 |
| 2026-11-04 | 补 frontmatter、Overview、Goals and Success Metrics、User Stories、Out of Scope；Requirements → Functional Requirements |
| 2026-11-04 | PRD-C 改为硬上限 10 行或 200 字符；PRD-G 区分 eval 分数与产品 metric；Solution 术语改 design 篇 |
| 2026-11-07 | PRD-J/P/Q 与 Resources：入口为 spec-write 与 spec-review（ARD-AJ） |
| 2026-11-07 | Overview 与 Goals 验收改为 spec-write 与 spec-review（ARD-AJ） |
| 2026-11-18 | PRD-P：交付只有 spec-write 与 spec-review（ARD-BH） |
| 2026-11-20 | PRD-M 改为通过条件（ARD-BO）；PRD-A、B、D、E 改写成可检查的句子，PRD-D 与 DSGN-B 的行数上限对齐；PRD-P 去掉删除线（ARD-BM）；Overview、Goals、Solution 改为完整句子并链到术语表（ARD-BK） |
| 2026-11-20 | 第 1 轮审查后：PRD-C 改为两条都要满足（ARD-BP）；PRD-D 写明 decision-history 例外；PRD-M 与 TST-V 对齐，允许查术语表；PRD-J 链到 ARD-BT；Problem Statement 保留原话（ARD-BS） |
| 2026-11-20 | 第 2、3 轮审查后：Resources 写明三份标准文件；PRD-P 改链 ARD-BX（ARD-BH 已被它取代） |
| 2026-11-20 | Resources Needed 加上 PIPE-E-B 要求的五项；偏好、时间写 not apply |
| 2026-11-24 | Out of Scope：版本只做来源标记（ARD-CC） |
| 2026-11-24 | Resources：列出外部服务 deepseek API、GitHub Actions 和 Pages（ARD-CD） |
| 2026-11-24 | PRD-C：新建文件不算在改动上限内（ARD-CE） |
| 2026-11-24 | 第 8 轮审查后：PRD-J、PRD-P、Resources 跟上 ARD-CH；复核次数跟上 ARD-CJ；改链 ARD-CE、ARD-CK |
| 2026-11-24 | 第 9 轮审查后：PRD-K 的链接改到重述它的 ARD-CJ |
