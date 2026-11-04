---
feature: document-standard
type: design
state: draft
final_date: 2026-10-30
health: active
owner: cicidi
last_verified: 2026-10-30
---

# Document Standard — 文档标准（待 Review）

本文件定义 **`docs/features/` 下 feature 文档** 的类型、路径、命名、体量、格式、authority、health 与 enforcement。**不** 规定 agent skill 拆几个文件、如何加载 — 那是 **implementation** 另文对齐。

相关：**pipeline** 见 `../pipeline/design/pipeline-design.md`；**测试** 见 parent `../../../test-plan/spec-driven-development-test-plan.md`（被测 = spec-organize / spec-review；本篇 MUST 进其 registry）。

### 术语（避免与 SDD「spec-driven」混淆）

| 术语 | 含义 |
|---|---|
| **Feature spec** | 一个 feature 的 **committed 文稿合称**：`prd` + **`design`** + `impl-plan` + `test-plan` + `decision-history`（+ 可选 `how-to`）。口语「维护 spec」常指 **这一套**，不是单指某一文件。 |
| **`design`（type）** | 合称中的 **技术设计篇**：目录 `design/`，文件 `<f>-design.md`，frontmatter `type: design`。SDD 循环里与 PRD、decision-history 互磨的 **设计正文** 指此。 |
| **SDD** | Spec-driven development — 方法名不变；与 **`type: design`** 文件夹无关。 |

**DSGN 索引**

| 节 | 内容 |
|---|---|
| DSGN-A | Contract（类型、路径、size、non-commit、INDEX/book、格式、条目 ID） |
| DSGN-G | Authority by concern |
| DSGN-H | `design` 篇写什么 / agent context |
| DSGN-I | Content priority（L1–L4） |
| DSGN-J | Decision history 语义 |
| DSGN-K | 命名冲突处置 |
| DSGN-L | Enforcement modes |
| DSGN-M | Quality gates（MUST / NICE） |
| DSGN-N | Spec reader HTML（aspect 篇 + **SPEC-HTML-STANDARD**） |

## Problem Statement

Feature 文档多时，缺少统一 standard 会导致：无 authoritative artifact 时的 silent overwrite、路径混乱、stale 与 wrong 不分、同一 fact 多处 drift。

## Solution

**DSGN-A = 契约**（MUST 主要来自 **DSGN-A**（含 **DSGN-B–F**）与 **DSGN-M**）。**DSGN-G–DSGN-L** = 语义与流程补充。

---

## Design

### DSGN-A — Document Contract

#### DSGN-B — 类型 · 目录 · 文件名 · size · split（一表）

`<f>` = kebab-case slug，**与 committed 文件名中的 feature 段一致**。

| 形态 | 根目录 | 表内 `<f>` / frontmatter `feature` |
|---|---|---|
| Flat | `docs/features/<f>/` | `<f>` |
| Sub-feature | `docs/features/<parent>/features/<sub>/` | **`<sub>`** |

**Sub 示例**（parent `spec-driven-development`，sub `document-standard`）：  
`.../document-standard/design/document-standard-design.md`；part `document-standard-design-<aspect>.md`；  
`.../document-standard/raw/research/<topic>.md`；`.../raw/state/state-<YYYY-MM-DD>.md`。  
Sibling：`.../pipeline/design/pipeline-design.md`。**待 review：** tooling 是否完全支持 sub 树与 `raw/`。

Committed：**目录 + 文件名**；文件名 **必须** `<f>-<type>…`（`raw/` 除外）。Supporting：`docs/features/<f>/<type>/<source-name>.md`（硬 cap 同 parent type）。**禁止** 单独 `reference/` type（外链材料放在 supporting 或 `raw/`）。

**Split / size：** 六种 type 均可 part；`行数 > 硬 cap` → MUST fail；按 bounded context / domain / ownership / lifecycle / 时间线 拆（不机械切行数）。可先 **DSGN-I** trim（`decision-history` 不 trim entry，只拆 part）。Entry 文件可链 part。**Collision** → **DSGN-K**。硬 cap 含 frontmatter 与 Change Log；**删 L1 凑 cap = defect**。

| Type | 内容 | Commit | 目录 | 文件名（entry） | 文件名（part） | 目标行 | 硬 cap |
|---|---|---|---|---|---|---|---|
| `prd` | 做什么、为什么 | yes | `docs/features/<f>/prd/` | `<f>-prd.md` | `<f>-prd-<aspect>.md` | 150–400 | 800 |
| `design` | 技术设计（怎么做） | yes | `docs/features/<f>/design/` | `<f>-design.md` | `<f>-design-<aspect>.md` | 200–500；架构 500–900 | 1,000 |
| `impl-plan` | task 分解 | yes | `docs/features/<f>/impl-plan/` | `<f>-impl-plan.md` | `<f>-impl-plan-<NN>-<phase>.md` | 100–500 | 1,000 |
| `test-plan` | 验证 | yes | `docs/features/<f>/test-plan/` | `<f>-test-plan.md` | `<f>-test-plan-<area>.md` | 200–600 | 800 |
| `decision-history` | 全部 decision | yes | `docs/features/<f>/decision-history/` | `<f>-decision-history.md` | `<f>-decision-history-<NN>-<period>.md` | 单 part 宜 ≤600 | 1,000 |
| `how-to` | 使用/运维 | yes | `docs/features/<f>/how-to/` | `<f>-how-to.md` | `<f>-how-to-<scenario>.md` | 100–350 | 600 |
| `raw` | 非 commit 原始区 | no | `docs/features/<f>/raw/<subdir>/` | 见下表 | — | 宜 ≤2,000 | — |

**`raw/`**（gitignore `docs/features/*/raw/`；无 frontmatter / Change Log / INDEX；升格事实 **link** 不 restate）：

| Subdir | 放什么 | 文件名 |
|---|---|---|
| `raw/research/` | 调研原始输出 | `<topic>.md` |
| `raw/review/` | agent 短时 review | `<YYYY-MM-DD>-<reviewer>-<subject>.md` |
| `raw/design/` | 未并入 **`design/` 正文** 的草稿（≠ committed `design/` 目录） | `<YYYY-MM-DD>-<subject>.md` |
| `raw/evidence/` | evidence / 工具输出 | `<YYYY-MM-DD>-<slug>.md` |
| `raw/discussion/` | 讨论串（可选） | `<topic>.md` |
| `raw/state/` | compaction 快照 | `state-<YYYY-MM-DD>.md`（硬 cap 400） |

Part 命名：`prd`/`design`/`test-plan`/`how-to` 用名词；`impl-plan`/`decision-history` 用 `<NN>`+phase/period。Legacy 顶层 `state/`、`research/`、`discussion/` → 迁入 `raw/`。Ticket：`.scratch/<feature-slug>/`（同样 **不得 commit**）。

**Commit 列：** `yes` = 纳入版本库的标准 feature 文档；`no` = **不得** 进入 git（本地可存在）。`no` 路径须 `.gitignore` 或等价策略；误 commit 视为 **DSGN-M MUST** 违规。

#### DSGN-C — 不得 commit（`Commit = no`）

| 路径 | 说明 |
|---|---|
| `docs/features/<f>/raw/**` | 原始区全树（含 `raw/state/`） |
| `.scratch/<feature-slug>/` | ticket 等 ephemeral（不在 `docs/features/` 但同属 non-commit） |

不得要求 frontmatter、Change Log、INDEX 条目。升格进 committed type 时 **link**，不把 raw 当 authoritative home。

#### DSGN-D — INDEX 与 book（派生层）

`docs/features/` 里的 committed 文档是 **source of truth**。INDEX 与 book 都是 **派生层**，不用 **DSGN-E** frontmatter / Change Log，**不写** 新 decision：

| | **INDEX** | **book** |
|---|---|---|
| 回答的问题 | **在哪**（路径、type、initiative 结构） | **干了什么**（短摘要，便于 AI/人决定要不要打开全文） |
| 典型粒度 | 一行链接 + 标题（可带一句 summary） | 每篇或每组 source 文档一段 **组装摘要**，链回 canonical 路径 |

---

**`docs/INDEX.md` — 干什么**

| | |
|---|---|
| **目的** | 全库 **feature spec** 各篇的 **地图**：哪个 initiative 下有哪些 PRD、design、plan，路径是什么。 |
| **给谁用** | 人、agent、脚本 **发现文档** 时先查 INDEX，再打开 `docs/features/...` 里的正文。 |
| **不是什么** | 不是 design 正文；在 INDEX 里改标题/链接 **不等于** 改 requirement；INDEX 里 **不写** 设计结论。 |
| **与 feature 树** | 每个 listed 链接必须指向 **Commit = yes** 的标准路径；tree 变了 INDEX 必须跟着变。 |

**INDEX 怎么维护**

- **生成物**：整文件 **regenerate**（改 generator/template，不长期手改一行行条目）。
- **何时 regenerate**：任一 committed 文档 **create / move / rename / delete** 之后；与 book 一样，**push 到 GitHub 前/时** 应与 `docs/features/` 变更 **同批同步**（见 book 应然）。
- **收录范围**：只列 committed 文档（含 sub-feature）；**不**列 `raw/`、`.scratch/`。
- **结构**：按 **feature（initiative）** 分块，块内按 **type** 顺序（`prd` → `design` → … → `decision-history`）；链接相对 `docs/`。
- **质量（DSGN-M MUST）**：disk 有文件但未 listed → **orphan**；listed 但文件不存在 → **dead link**。

---

**`docs/book/**` — 干什么**

（与历史 **doc-organize** 一致：*Assembled output, built from documents that are already `final`。* — 此处 **final** 指 feature 侧已接受的 committed 正文，不是 book 自己定稿。）

| | |
|---|---|
| **目的** | 由 feature spec 各篇 **组装** 的 **摘要层**：用短说明写清每份 PRD/design/plan **覆盖什么、得出什么、该去哪读全文** — 主要给 **AI 检索与选篇**。 |
| **给谁用** | Agent / 人 **先扫 book 再打开** `docs/features/...`；不是在此写第一版 design 或新 decision。 |
| **不是什么** | **不是** source of truth；**不是** design 全文拷贝；**不能** 与 feature 正文 **手维护两份相同 fact**。 |
| **与 INDEX** | INDEX = 目录；book = **内容摘要**。二者互补，通常 **一起** 更新。 |

**book 写什么（摘要契约）**

- 每条摘要 **必须** 链到对应 **canonical 路径**（`docs/features/...`）。
- 写 **scope + 主要结论/状态**（例如：document-standard 的 design 篇定 DSGN-A 契约；pending review 项），**不** 展开 L1 全文。
- 新增/变更 decision 只改 feature / `decision-history`，再 **重生成** book 摘要，禁止只在 book 改口径。

**book 什么时候更新（应然）**

- 凡 **`docs/features/` 下 committed 文档** 有变更并 **push 到 GitHub**，**同一 push（或紧邻的前序 commit）中应已 regenerate 对应的 book**（及 INDEX）。  
  *实现*（pre-push hook、CI、bot、手动）属 **impl**；本 standard 要求 **远端可见的 docs 与 book/INDEX 同步**，避免 AI 在 GitHub 上读到新 spec 却仍是旧摘要。
- 源文档 **`state: draft`** 时可暂不更新对应摘要；**`final` 或已 merge 的 committed 变更** 必须反映到 book。

**其它**

- 路径：`docs/book/**`；无 **DSGN-E** frontmatter；Lint 查 **link 有效**、摘要指向的文件存在。
- 可 **额外** 用于 MkDocs / Pages 发布；发布 nav 属 impl，不得与 feature 树、INDEX 矛盾。

---

**其它豁免路径**（同样不是 feature 文档，无 **DSGN-E** frontmatter；Lint 只查 link）：`CONTEXT.md`（domain glossary）、`README.md`（repo 导向）。

#### DSGN-E — 格式（committed 文档）

```yaml
---
feature: <feature-name>
type: prd | design | impl-plan | test-plan | decision-history | how-to
state: draft | final
final_date: YYYY-MM-DD   # final 时必填
---
```

可选（NICE）：`spec_id`, `version`, `health`（`active`|`stale`|`deprecated`），`owner`, `last_verified` — 用 **`health`** 不用 `status`。

| Type | Required sections（可 add，不可 rename/drop） |
|---|---|
| `prd` | Overview, Goals and Success Metrics, User Stories, Functional Requirements, Non-Functional Requirements, Out of Scope |
| `design` | Problem Statement, Solution, User Stories, Implementation Decisions, Design, Testing Decisions, Out of Scope, Further Notes |
| `impl-plan` | Global Constraints, numbered Tasks |
| `test-plan` | Test Cases, Test Execution Order, Expected Pass Threshold |
| `decision-history` | Decision Log, Evidence Appendix |
| `how-to` | Overview, Prerequisites, Steps, Verification |

`design` 可选 `Alternatives Considered`（L3）。Decision Log 表头：`ID \| Date \| Decision`（**无** `Status` / `Supersedes` 列）。**倒序**：新 entry 在表顶。Change Log：**最后一节**，只 append。PROTECTED 块任何 mode 不改。INDEX：文档增删移后 regenerate。

#### DSGN-F — 条目 ID（type 前缀 + 字母）

各 type 内可追溯条目用 **`{前缀}-{字母}`**，字母序同 Excel 列（`A`–`Z` → `AA`–`AZ` → `BA`–…）。可在已有条目之间 **插入** 新 ID（大方向顺序，见 **DSGN-J**）。

**ID immutable（MUST）：** 某 ID **一旦写入** feature spec（表、标题、正文、外链），该字符串 **终身固定** — **禁止** 改字母、改前缀、拼写「修正」、重编号、把 `PRD-A` 合并进 `PRD-B`。**禁止复用** 已出现过的 ID（即使 entry 被 strike / 整段作废）。口径变了 → **新 ID** + 旧处 strike / link（**DSGN-J**）；**不得** 改旧 ID 本身。

| Type | 前缀 | 例 |
|---|---|---|
| `prd` | `PRD` | `PRD-A`, `PRD-B`, `PRD-AA` |
| `design` | `DSGN` | `DSGN-A`, `DSGN-B` |
| `decision-history` | `ARD` | `ARD-A`, `ARD-AA` |
| `impl-plan` | `IMPL` | `IMPL-A`, `IMPL-B` |
| `test-plan` | `TST` | `TST-A`, `TST-B` |

跨文档引用 **写全 ID**（如 `PRD-A`、`ARD-F`）。`how-to` 无强制 letter ID。

**凡有序号即 ID（MUST）：** ADR、requirement、design 规则小节、impl task、test case、defer/open question 等 **一切** 可追溯条目 — **必须** 用上表 `{前缀}-{字母}`。**禁止** 裸数字（`0001`）、`PRD-1`/`DH-1`/`FR-3`/`OQ-1`/`D1` 等作永久 ID。本 design 篇小节即 **DSGN-A** 起（见索引）。

**AI 单次 edit 粒度**（≤10 行 / ≤200 字）属 SDD parent HLD **§4**，不在本 document-standard；impl 目标：**spec-write** 等书写 skill。

---

### DSGN-G — Authority by Concern

不要 global single source of truth — **按 concern 各认一个 authoritative artifact**；不一致时 **Detect → Report → Ask**（禁止 silent 改一侧；禁止默认 `design` 篇 > code）。

| Concern | Authoritative artifact |
|---|---|
| Intended behavior | feature **`design` 文档** |
| API contract | OpenAPI / protobuf / GraphQL / JSON Schema 等 |
| Database structure | migrations / schema |
| Current implementation | code |
| Executable verification | tests |

**`design` 篇** 权威 intended behavior；code 权威当前实现与内部结构。Machine-readable contract **不要**在 Markdown 里手抄全文 — link 或 generate。Tests 是 verification，不是 requirement 替身。`final` 后 maintain，不整篇 rewrite。

---

### DSGN-H — Design 文档 Scope（`type: design` 正文）

**写：** behavior、contract、invariant、constraint、error、state transition、外部交互、架构边界（含 diagram 类）。  
**不写：** class 结构、private method、framework 内部细节（见 **DSGN-I** trim 时也应 absent）。  
**测试句：** 可改 implementation 而不改 externally observable behavior → 不应改 **design 篇**。

**Agent 加载顺序：** Global rules → Domain **design** → Architecture → Contract → Examples/tests → Code。窄问题却要整篇 design → re-cut boundary。

体量与 split：**DSGN-B**。篇内设计决策 / 小节锚点用 **`DSGN-A`** 等（**DSGN-F**）。

---

### DSGN-I — Content Priority

Trim 顺序 L4 → L3 → 压 L2；**L1 永不删**。仍 `> 硬 cap` → **DSGN-B** split。

| Level | Trim |
|---|---|
| **L1** | behavior、contract、invariant、error、security、boundary、out of scope、assumption、compatibility、open question — **never** |
| **L2** | rationale — 压缩 |
| **L3** | alternatives — 先删 |
| **L4** | 引用、raw output — 先删；重复 fact 只能是 **link** |

---

### DSGN-J — Decision History — 语义

**文件角色：** 决策 **索引 + 正文**（Decision Log / `### <ID>` 小节，格式 **DSGN-E**）。**不是** PRD / **design 篇** 的摘要。

**书写顺序：** **倒序** — 每加一条，写在 Decision Log **最上面**（最新在上，越往下越早）。

**Decision ID：** 格式 **`ARD-{字母}`**（**DSGN-F**，分配后 **不可改**）。Log 表 / `### ARD-A — …` 与 ID 一致。

**推翻旧 decision：** 旧 entry **不删行**；正文 ~~删除线~~；旁 **link 到新 ID**（如 `→ [ARD-F](#ard-f--…)`）。新口径用 **新 ARD ID** 写满一条，倒序 **插 Log 顶**。旧 entry 仅 strike + 指链（**DSGN-I** 不 trim 被 strike 字句）。

**拆 part（超 **DSGN-B** 硬 cap）：** ID **全 feature 唯一**；新 entry 写入 **当前 part** Log 顶部；旧 part 保留；part 间 link 即可。

**什么时候加一条（agent 写 spec 时）：** 细则表见 parent HLD **§5**。简记：

| 加 | 不加 |
|---|---|
| 别人定下来的口径（review、结对、stakeholder），团队要能看到 | 仅在你脑子里、还没写进 **design 篇**、也 **没动代码** 的试探 |
| 你的转向会 **改已有代码或对外契约**（breaking behavior、路径/rename、谁才是 authority） | 只在 **design 篇** 改几句就能说清的推敲；「想过又改主意」不必每条都 log |
| rename / 撞名等流程要求记入的（**DSGN-K**） | agent **默认不** 自动批量 append；不确定问 human |

---

### DSGN-K — Paths and Names — 冲突处置

新 feature / 新文件名 **必须** 对照已有名称；命中任一 **collision signal** 即视为冲突：

| Signal | 例 |
|---|---|
| normalize 后相同 | `Payment` vs `payment` |
| token 子集 | `auth` vs `auth-service` |
| 单复数 / 常见缩写 | `doc` vs `docs` |
| edit distance ≤ 2 | `payment-api` vs `payments-api` |

处置：同一 bounded context → **merge** 再按 aspect split **`design`**。不同 context 易混 → **rename** 双方并记入 `decision-history`。同 feature 内文件撞名 → 拉开 aspect 或 rename feature。**Rename = decision**，更新 inbound link，禁止 silent。

---

### DSGN-L — Enforcement Modes

| Mode | 行为 |
|---|---|
| **Organize** | feature/type → collision → 路径/文件名 → frontmatter + sections → Change Log → INDEX |
| **Lint** | walk `docs/features/`；MUST 机械 fix；semantic **report** |
| **Consolidate** | propose → 批准；decision 全保留；`raw/` legacy  cite 或删 |
| **Sync** | drift；按 **DSGN-G** authority；semantic conflict **report** |
| **Review**（spec-review） | 同 Lint 的 detect（机械 MUST + semantic）；**不** fix，输出带 severity 的修改建议 |

内容质量（设计是否成立）由 **Review** 的 semantic 部分处理，不属本 standard 的 MUST。

---

### DSGN-M — Quality Gates

**MUST：** **DSGN-A** 全满足（含 **DSGN-F** ID 不可改、不可复用）；**DSGN-G** 冲突不 silent；**DSGN-I** 不删 L1；consolidation 不丢 decision；**Commit = no** 路径未 commit；INDEX 无 orphan/dead link；含 `docs/features/` 变更的 **push** 时 INDEX/book 已与源同步；collision 已查。

**NICE：** heading 不跳级；link 有效；CONTEXT 术语一致；`last_verified` 新鲜；context boundary 合理。

---

## Testing Decisions

验证见 parent **`../../../test-plan/spec-driven-development-test-plan.md`**：被测对象是 **spec-organize / spec-review**，不是本篇；本篇全部 **MUST / 禁止** 由 **TST-A** 扫入 `must_registry.yaml`，机械项 Python 判、其余 LLM judge 判。

## Out of Scope

- Pipeline 阶段编排（见 pipeline spec）。
- 存量 tree 一次性 migrate（incremental 合规即可）。
- CI / skill **如何实现** enforcement（文件数、prompt、hook）。
- 自动 drift detection 产品化。

## Further Notes

- 已知历史偏离例：`skill-factory/design/` 等 — migrate 时按 DSGN-M 逐项清。
- **待一起 review：** **DSGN-B** 硬 cap 数字、sub-feature 是否正式 MUST、`raw/` 子目录是否够用。AI edit 上限见 parent HLD §4；agent 全局 norm（含 §5 decision-history、§6 CLAUDE+skill）见 parent HLD。

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
| 2026-11-03 | 本篇 `D1`–`D8`/`D1-*` 重命名为 **DSGN-A**–**DSGN-M** |
| 2026-11-03 | Testing Decisions → `../test-plan/document-standard-test-plan.md` |
| 2026-11-03 | Feature 级 test plan（parent 仅 harness） |
| 2026-11-03 | Testing Decisions → parent test plan（被测 = skill）；DSGN-L 加 Review 行；doc-write → spec-write |
| 2026-11-03 | **DSGN-N** spec reader HTML → aspect design + `skills/spec-html-standard/` |
