---
feature: spec-driven-development
type: design
state: draft
final_date: 2026-10-30
health: active
owner: cicidi
last_verified: 2026-11-04
---

# Spec-Driven Development — HLD

本文件 **仅 HLD**。Requirement 见 `prd/spec-driven-development-prd.md`；LLD、规则条文、skill 契约、迁移步骤等 **全部** 在 peer / sub feature 或本 initiative 的 **aspect design 篇** 里，此处只 link。

### 术语

| 术语 | 含义 |
|---|---|
| **Feature spec** | 一个 feature 下 **全套 committed 文稿**：PRD + **design** + impl-plan + test-plan + decision-history（+ 可选 how-to）。 |
| **`design` 篇** | 其中 **技术设计** 文件：`design/<f>-design.md`。SDD 图里循环打磨的「设计」指此，不是合称。 |

## Problem Statement

问题定义、unknown、decision 变更、可读性与文件管理、非软件难题——见 PRD Problem Statement。

## Solution

一套 artifact + skill 体系：PRD、decision-history、design 篇、impl-plan、test-plan 五篇；四个 skill 编排、书写、校验、审查。

## User Stories

- 作为写 spec 的人，我希望先被 interview，把未知和盲区问出来。
- 作为 reviewer，我希望机械 MUST 和语义缺陷都能被检出。
- 作为执行者，我希望 spec 能落到 design/impl-plan，并留下可追溯的证据。

## Design

### 1. System Context

SDD 是一套 **artifact + skill** 体系：PRD 说 problem，decision history 记方向，**design 篇** 写技术方案；收敛后 impl plan、test plan **从 design 篇** 各写一份总结。文档落在 `docs/features/`。

### 2. Logical Architecture（HLD）

### 2.1 Artifact 循环与下游

```
     PRD ◄──────────────────► decision history
      ▲                              │
      │                              ▼
      └──────── design ◄─────────────┘
              │
              ▼ 收敛后（从 design 篇各写一份）
         impl plan    test plan
              └─ 独立，无先后 ─┘
```

- **循环区：** PRD、decision history、**design 篇** 互相打磨（见 PRD Solution）。
- **下游区：** impl plan、test plan 均从 **design 篇** 总结；细节见 **pipeline** sub-feature。

### 2.2 组件分解（HLD）

```
docs/features/
├── spec-driven-development/     ← 本 initiative（parent：PRD + 本 HLD + decision-history）
│   └── features/
│       ├── pipeline/
│       └── document-standard/
└── skill-factory/                 ← peer initiative
```

### 3. Peer / Sub 清单（Review）

### 3.1 Peer features（`docs/features/<name>/`）

| # | Feature | 判定 | HLD 职责（一句话） | Detail design |
|---|---------|------|-------------------|---------------|
| P0 | **spec-driven-development** | Parent | Initiative 总览、本 HLD、parent PRD/decision-history | 本文件 + `prd/spec-driven-development-prd.md` |
| P1 | **skill-factory** | Peer | Skill 生产/管理 | `docs/features/skill-factory/design/` |

**Peer 判定规则：** 可单独 PRD / feature spec / ship → 放在 `docs/features/` 下，**不要** nest 在 `spec-driven-development/features/`。

### 3.2 Sub features（`spec-driven-development/features/<name>/`）

| # | Sub feature | Detail design |
|---|-------------|---------------|
| S1 | **pipeline** | `features/pipeline/design/pipeline-design.md` |
| S2 | **document-standard** | `features/document-standard/design/document-standard-design.md` |
| S3–S6 | （延后） | — |

### 3.3 子问题归属（PIPE-L / PRD-L）

| 子问题 | 归属 | 依据 |
|---|---|---|
| 存量不合规文档是否迁移 | 人决定 | ARD-AF |
| wayfinder-import 是否作为子特性 | 人决定 | ARD-T |
| eval 跑分与报告是否入库 | AI 查完人决定 | ARD-AD |
| 四个非软件例子是否建 gold | 人决定 | ARD-AD |

## Implementation Decisions

### 4. AI 文档编辑约束（SDD 全 pipeline）

**来源：** parent PRD Requirements §3。

**适用范围：** agent 对 **`docs/` 内 Markdown**（feature spec 各篇）的单次编辑。

| 规则 | 说明 |
|---|---|
| **单次上限** | ≤ **10 行** *或* ≤ **200 字符**（满足其一） |
| **超出时** | 拆多次；或 human 授权 `restructure` |
| **与 document-standard** | cap、路径、frontmatter 见 **document-standard** design 篇 |
| **验证** | 测试验不了单次编辑大小。不作为 test plan 的通过条件 |

**Implementation：** **spec-write** 已有正文。人不读 skill 正文。本条上限看 skill 执行，不靠测试。

### 5. Decision history — 何时写（agent / 写 spec 时注意）

**原则：** decision-history 记 **已对外生效或已强迫改 reality 的方向**，不是 design 脑内迭代的日记。

| 应该写 | 不应写 |
|---|---|
| **他人** 的 decision（review、配对、stakeholder 口径）需团队可见 | 仍在本人脑中、**未** 写入 **design 篇** 且 **未** 改 existing code 的探索性微调 |
| **本人** 重大转向且 **已改或必须改 existing code**（contract、路径、rename、authority 换边、breaking behavior） | 为「想过又改主意」每条 append；design 篇里改一句能表达的不单独开 entry |
| Pipeline 要求的 **rename / collision / supersede** 等（见 document-standard **DSGN-J**–**DSGN-K**） | 仅 enrich **design 篇** 正文、尚未收敛的 rationale |

未 commit 的 scratch 与 `raw/design/` **不** 替代 decision-history；升格 committed fact 时按上表判断。**Agents** 补写 feature spec 时 **默认不** 自动堆 decision-history；有疑问时 human 定夺。

### 6. Agent 规范落地：CLAUDE.md + skill

§4（小步编辑）、§5（decision-history 取舍）、feature spec 各篇职责等，须在 **harness 全局** 留下印象，不能只在 repo 内 skill 正文里写一遍（PRD-H：复用既有 skill，不另造）。

| 通道 | 作用 |
|---|---|
| **`~/.claude/CLAUDE.md`** + 项目 **`CLAUDE.md` / `CLAUDE.local.md`** | 跨 session、跨 feature 的 **默认 agent 行为**（含 walter-worker **managed block**） |
| **Skills**（**spec-organize** 主 skill、**spec-review**、**spec-write**） | 任务级 procedure、机械检查 |

Implement SDD / document-standard 时：**plan 必须含 skill 变更与 CLAUDE 层条目**（managed block 或等价），二者对齐同一 norm；条文细节在 sub **design 篇**，本 HLD 只定双通道原则。

## Testing Decisions

### 7. Deliverable 与测试

| 项 | 约定 |
|---|---|
| **Deliverable** | 四个 skill（可装任意项目）：**spec-pipeline**（编排入口，PRD-J）、**spec-organize**（主/标准）、**spec-review**、**spec-write** |
| **Standard 文件** | `skills/spec-organize/SPEC-STANDARD.md`（自 document-standard design 产出；见 **ARD-AB**） |
| **测试位置** | `skills/<skill>/tests/`；跨 skill 检查器、gold、报告在 `skills/spec-organize/tests/`（**ARD-Q**） |
| **Test plan** | parent `test-plan/spec-driven-development-test-plan.md`；sub-feature 不另写 |
| **Pipeline design** | `features/pipeline/design/pipeline-design.md`（spec-pipeline 行为） |
| **Skill contracts** | `design/spec-driven-development-design-skill-contracts.md`（四个 skill 的输入/输出/边界） |
| **Spec reader HTML** | `<parent>-reader.html`；规范 **`skills/spec-html-standard/SPEC-HTML-STANDARD.md`**（**DSGN-N**，非独立 skill） |

## Out of Scope

- **PRD-G**：产品级 success metric 与 baseline 延后（**ARD-N**）；test-plan 的分数是 eval 指标，不是产品 metric。
- 真实下单、订票、交易；执行只到 mock MCP log。
- 更细的多人 decision 仲裁（例如同时间的 tie-breaker）；主规则按 decision-history 时间，仍看不出则问用户。
- 存量不合规文档的批量迁移。
- skill / spec 的版本与迁移策略。

## Further Notes

### 8. Parent vs sub-feature — review 齐备度

**Parent（本 initiative 根 `docs/features/spec-driven-development/`，不含 `features/<sub>/`）：** **spec-review** 须核对 **feature spec 五篇** 均在：`prd`、`design`、`decision-history`、`impl-plan`、`test-plan`（`how-to` 可选；类型见 document-standard **DSGN-B**）。缺任一篇 → severity ≥3 finding。

**Sub-feature（`features/<sub>/`）：** **不** 要求五篇齐全；可以只有 `design` 等。review 只查**已有**文稿；**不得**因未计划的 type 缺失而 fail。

## Change Log

| Date | Change |
|------|--------|
| 2026-10-31 | 收窄为 HLD only；peer/sub review 表 |
| 2026-11-03 | §4 AI 编辑约束 |
| 2026-11-03 | 术语 feature spec 合称；技术设计目录 `design/`；循环图改为 design |
| 2026-11-03 | §5 decision-history 何时写；§6 CLAUDE.md + skill 双通道 |
| 2026-11-03 | §7 Deliverable 与测试；skill 名 spec-organize / spec-review / spec-write |
| 2026-11-03 | 移除 wayfinder-import sub-feature（§2.2、§3.2） |
| 2026-11-03 | §8 parent review 须五篇齐备；sub-feature 不要求 |
| 2026-11-03 | §7 增加 spec-pipeline deliverable 与 pipeline design 指针 |
| 2026-11-03 | §7 Spec reader HTML；parent impl-plan 路径 |
| 2026-11-03 | §7 reader 规范 → **spec-html-standard**（无 spec-reader skill） |
| 2026-11-04 | §4：spec-write 已有正文；人不读 skill，靠 test plan 验收 |
| 2026-11-04 | §4：单次编辑大小测试验不了，不作为 test plan 的通过条件 |
| 2026-11-04 | 补齐 design 八章节；§7 增加 skill-contracts aspect design 指针 |
| 2026-11-04 | Intro 允许 aspect design；§7 Standard 引用 ARD-AB |
| 2026-11-04 | Out of Scope 收窄多人 decision 条款 |
