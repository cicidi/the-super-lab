# Spec-Driven Development — PRD

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

## Solution

**Spec-driven development**

我们不重复什么是 spec-driven。这里要做的是开发一些 skill；这些 skill 会在一起工作，而不是单个 skill。这些 skill 的目标是：通过一组 skill，把具体问题分析清楚。

**PRD、decision history、spec 是互相打磨的循环**，不是只走一遍的直线；循环收敛到「够稳」后，**impl plan** 与 **test plan** 各自独立：都从 **spec** 总结出来，彼此不串行依赖。

1. **PRD** — 我们到底要做什么、解决什么；当前的 limitation 是什么；preference 是什么；timeline、各种 resource、tool 都有什么。spec 或 decision 暴露缺口时，回到 PRD 改 requirement。
2. **Decision history** — 基于 PRD 作出 decision；任何跟产品方向相关的 decision 先 update decision history（约 50% AI、50% 人）。新 decision 可能改 PRD 范围；spec 里的 trade-off 也可能要求补 decision。
3. **Spec** — 与 PRD、decision 并行迭代：写设计（技术方案、contract、tool 等；HLD/LLD 不在此展开）。设计问清 problem、或发现 decision 不够，回到 1/2 继续磨。
4. **Impl plan** — 从 spec 总结实现：先做什么、后做什么；各个 task 的细节、准备工作等（不依赖 test plan 先写完）。
5. **Test plan** — 从 spec 总结验证：任务完成标准、可用性检查、regression guard（不依赖 impl plan 先写完）。

## Requirements

**PRD-A** — 做一个 pipeline，基于现在现有的 pipeline 做一些改进。

**PRD-B** — 做一些 skill；这些 skill 其实就是优质 prompt，或其他 popular 的 prompt，引导 AI 怎么工作：完成 spec 的书写、命名、校验、更新。

**PRD-C** — 保证每次改动都很小，不要超过 10 行、200 个字左右。改动太大，会导致崩溃。

**PRD-D** — 文档大小限制在 1000 行；太大几乎没法 maintain。

**PRD-E** — 文档的文件组织架构、folder 关系。

Additional constraints:

**PRD-F** — （open）多参与者 decision 谁为准 — deferred，见 **ARD-M**。

**PRD-G** — （open）success metric 度量与 baseline — deferred，见 **ARD-N**。

**PRD-H** — Spec-driven development 的 workflow 尽量使用 popular skill，不要自己重新发明。

**PRD-I** — 修改需要验证；没有能验证的，都需要在 spec 里面标注上。

**PRD-J** — 提供 **spec-pipeline** skill：凡写/改 feature spec 经 pipeline 进入；编排 spec-organize / spec-write，提交 committed 变更前询问 spec-review；支持 recap 与轻量 state（feature 确定前 CLAUDE.local，之后 `docs/features/<f>/raw/state/`）。
