---
feature: spec-driven-development
type: impl-plan
state: draft
final_date: 2026-11-03
health: active
owner: cicidi
last_verified: 2026-11-24
---

# Spec-Driven Development — 实现计划

本篇列出把 SDD 做出来的任务和先后顺序。每个任务写明依赖哪个任务、挡住了哪个任务、做到什么程度算完成（document-standard 的 DSGN-E）。术语见 [parent design 的术语表](../design/spec-driven-development-design.md#glossary)。

## Global Constraints

- **先改 spec，再改 skill：** 做任务时发现 spec 有错，先问人，改好 spec，再改 skill 和测试。
- **skill 的写法：** `SKILL.md` 用 `skill create` 或 `skill edit`（见 `skills/skill/SKILL.md`）来写。本篇只规定顺序。
- **测试：** 测什么见 [test-plan](../test-plan/spec-driven-development-test-plan.md)，测试文件放在 `skills/spec-organize/tests/`。
- **不做 wayfinder-import sub-feature**（[ARD-T](../decision-history/spec-driven-development-decision-history.md#ard-t)）。
- **评测：** 用 `deepseek-flash` 生成 gold 跑 3 次、复核跑 5 次；跑分结果和报告不提交（[ARD-CJ](../decision-history/spec-driven-development-decision-history.md#ard-cj)）。打分用 iPhone 案例（[ARD-BL](../decision-history/spec-driven-development-decision-history.md#ard-bl)）。
- **不迁移旧文档**，只修 SDD 自己这套（[ARD-CK](../decision-history/spec-driven-development-decision-history.md#ard-ck)，重述 ARD-AF）。

## IMPL-A — skill 目录改名

**目标：** `doc-organize` 改名为 `spec-organize`，`doc-review` 改名为 `spec-review`。

**步骤：** 用 `git mv` 移动目录；改 `SKILL.md` 里的 `name:` 和互相引用；部署时更新 `~/.coworker/project.yaml`（作者本机记录各项目装了哪些 skill 的配置文件）里的 skill 列表。

**依赖：** 无。**挡住：** IMPL-B、IMPL-C。

**Verify:** `ls skills/spec-organize skills/spec-review` 两个目录都在；触发词能找到对应的 skill。这一项已经完成。

## IMPL-B — spec-write 和 spec-review 的 SKILL.md

**目标：** spec-write、spec-review 的 `SKILL.md` 和 [skill 契约](../design/spec-driven-development-design-skill-contracts.md)一致（[ARD-AJ](../decision-history/spec-driven-development-decision-history.md#ard-aj)、[ARD-CH](../decision-history/spec-driven-development-decision-history.md#ard-ch)）。

**步骤：** 契约或标准改了，就用 `skill edit` 同步修改两份 `SKILL.md`。

**依赖：** IMPL-A、IMPL-C。**挡住：** IMPL-E、IMPL-I、IMPL-N。

**Verify:** `SKILL.md` 开头的 description（一句话说明什么时候用这个 skill）以「Use when」开头；`SKILL.md` 里有 MUST 门槛；职责和契约表一致。

## IMPL-C — 三份标准摘要

**目标：** `skills/spec-organize/SPEC-STANDARD.md`、`skills/spec-html-standard/SPEC-PRESENTATION.md` 和 `skills/spec-html-standard/SPEC-HTML-STANDARD.md` 是可执行的规则摘要；完整规则仍在 document-standard design 和 reader design（[ARD-CH](../decision-history/spec-driven-development-decision-history.md#ard-ch) 重述 ARD-BX）。

**步骤：** 每次 DSGN 规则改动，同一批修改摘要。

**依赖：** IMPL-A。**挡住：** IMPL-B、IMPL-F、IMPL-M、IMPL-R。

**Verify:** 摘要里的每条 MUST 都能在 document-standard design 里找到出处；没有和 design 矛盾的说法。

## IMPL-D — 测试骨架和 iPhone gold 的输入

**目标：** 按 test-plan 在 `skills/spec-organize/tests/` 下建好测试骨架。

**要产出的文件：**

- `eval.yaml`；`must_registry.yaml`（通过 TST-A 扫描生成）
- `gold/v1/requirement.md` 和 `gold/v1/context.md`：iPhone 购买案例的输入（[ARD-BL](../decision-history/spec-driven-development-decision-history.md#ard-bl)）
- `fixtures/neg/` 和 `fixtures/pos/`，随 TST-B 增加
- `checks/` 下的 Python 检查模块，实现 TST-B

**依赖：** 无。**挡住：** IMPL-J、IMPL-K、IMPL-L、IMPL-E。

**Verify:** 有检查模块时 TST-B 能跑；gold 的输入文件都在。

## IMPL-E — 自己跑一遍评测

**目标：** 跑基线评测：`grill.skills: []`，输入是 iPhone 案例的需求和背景资料（[ARD-BL](../decision-history/spec-driven-development-decision-history.md#ard-bl)）。

**步骤：** 新开分支 `eval/v1/<run_id>`；用 spec-write 写出一套 feature spec；跑 TST-E、TST-F、TST-K；失败时先改 spec。

**依赖：** IMPL-B、IMPL-D、IMPL-J、IMPL-P；报告部分还依赖 IMPL-L，可读性部分还依赖 IMPL-Q。**挡住：** IMPL-I。

**Verify:** 生成了 HTML 报告；分数按 test-plan 的 Scoring 计算。

## IMPL-F — 给人读的网页

**目标：** 全站一个网站，入口 `docs/book/html/index.html`；feature 页左边是目录，右边是正文；parent 的汇编页 `spec-driven-development-reader.html` 在其中（[ARD-BG](../decision-history/spec-driven-development-decision-history.md#ard-bg)、[reader design](../features/document-standard/design/document-standard-design-spec-reader-html.md)）。

**步骤：** markdown 改了之后，用 `tools/build_sdd_site.py` 和 `tools/build_sdd_reader.py` 重新生成；每页底部链到原文路径。

**依赖：** IMPL-C。**挡住：** IMPL-O、IMPL-S。

**Verify:** 用浏览器直接打开页面能看；页面里列出的原文路径都存在。

## IMPL-G — CLAUDE 层里的 SDD 段落

**目标：** CLAUDE 层只记当前 wayfinder 地图目录的路径，进度本身在地图里（pipeline design 的 PIPE-H；[ARD-CG](../decision-history/spec-driven-development-decision-history.md#ard-cg)、[ARD-CH](../decision-history/spec-driven-development-decision-history.md#ard-ch)）。

**步骤：** 在项目的 CLAUDE 层（ARD-CG）里加一段 SDD：当前地图目录的路径、reader 网页的链接。

**依赖：** 无。**挡住：** 无。

**Verify:** spec-write 开始工作时能读到这一段。

## IMPL-H — 文档整理

**目标：** INDEX 列出 parent 的 impl-plan 和新增的 design 分篇；删除旧的摘要网页。

**步骤：** 重新生成 `docs/INDEX.md`；删除 `spec-driven-development.html`，只保留 reader。

**依赖：** 无。**挡住：** IMPL-O、IMPL-V。

**Verify:** 没有链接指向已删除的摘要网页，也没有指向 wayfinder-import 的路径。

## IMPL-I — spec-review 报告机械 MUST

**目标：** spec-review 能找出机械 MUST 的违反，并给出修改建议（[ARD-P](../decision-history/spec-driven-development-decision-history.md#ard-p)）。

**步骤：** document-standard 和 test-plan 里关于 review 的部分稳定后，修改 `skills/spec-review/SKILL.md`。

**依赖：** IMPL-B、IMPL-K、IMPL-E。**挡住：** 无。

**Verify:** TST-H 的案例全部检出。

## IMPL-J — 评测配置和配置测试

**目标：** `eval.yaml` 能用 `deepseek-flash` 生成 gold 跑 3 次、复核跑 5 次；目标仓库可以用环境变量覆盖；`test_eval_config.py` 在配置缺项时报错。

**依赖：** IMPL-D。**挡住：** IMPL-E、IMPL-Q。

**Verify:** `pytest test_eval_config.py` 通过；`eval.yaml` 包含所有必需的键。

## IMPL-K — 反例、正例和审查案例

**目标：** 每个检查至少一个反例和一个正例；spec-review 的 16 个审查案例（11 个机械，5 个语义）。

**依赖：** IMPL-D。**挡住：** IMPL-I。

**Verify:** TST-B 全部通过；TST-H 和 TST-I 需要的文件都在。

## IMPL-L — 评测报告脚本

**目标：** `tools/render_eval_report.py` 生成一个 HTML 报告，包含分数 1、分数 2 和这次运行的信息。

**依赖：** IMPL-D。**挡住：** IMPL-E 的报告部分。

**Verify:** 对一次样例运行跑 TST-K 通过。

## IMPL-M — 检查脚本更新

**目标：** `sections.py` 检查五种文档的必需章节；`ids.py` 检查编号格式；去掉不该有的豁免。

**依赖：** IMPL-C。**挡住：** IMPL-P、IMPL-T。

**Verify:** TST-B 通过；`run_spec_checks.py` 跑 SDD 目录。

## IMPL-N — skill 契约和四个例子

**目标：** [skill 契约](../design/spec-driven-development-design-skill-contracts.md)写好；两个 skill 的正文都提到盖 shed、北京旅游、数学题、股票（PRD-Q）。

**依赖：** IMPL-B。**挡住：** 无。

**Verify:** TST-S 通过；spec-review 会读契约。

## IMPL-O — 网页新鲜度

**目标：** spec 改了之后重新生成网页；旧的 `spec-driven-development.html` 已删除。

**依赖：** IMPL-F、IMPL-H。**挡住：** 无。

**Verify:** TST-R 通过；没有死链。

## IMPL-P — 让代码和数据跟上 2026-11-20 的决定

**目标：** 2026-11-20 那批整理（[ARD-BS](../decision-history/spec-driven-development-decision-history.md#ard-bs)，它重述了 ARD-BK）只改了 spec 的 markdown，下面这些 markdown 以外的文件当时还按旧规则写，需要同步修改。这一项已于 2026-11-24 完成：

| 文件 | 要改什么 | 依据 |
|---|---|---|
| `skills/spec-organize/tests/eval.yaml` | `gold.cases` 改回 iPhone 案例 `gold/v1`，不再指向 SDD 目录 | [ARD-BL](../decision-history/spec-driven-development-decision-history.md#ard-bl) |
| `skills/spec-organize/tests/must_registry.yaml` | 重新扫描（TST-A）。document-standard design 已改写，原来按行号记的出处都错位了。已于 2026-11-24 重新扫描，`registry_provenance` 报 0 个问题；把 reader design 的 MUST 也收进来（TST-A）；去掉「正文改动要留删除线」这条 MUST；标出改为 NICE 的规则 | TST-A、TST-M、[ARD-BM](../decision-history/spec-driven-development-decision-history.md#ard-bm)、[ARD-BN](../decision-history/spec-driven-development-decision-history.md#ard-bn) |
| `skills/spec-organize/tests/checks/sections.py` | 这个脚本检查必需章节。去掉一条旧豁免：以前 design 只要有「System Context」标题，就不检查必需章节；parent design 现在已有 13 个必需章节，不再需要这条豁免 | document-standard 的 DSGN-E |
| `.gitignore` | `docs/features/*/raw/` 改为 `docs/features/**/raw/`，把 sub-feature 下的 `raw/` 也排除 | document-standard 的 DSGN-B |
| `skills/spec-organize/tests/checks/` 里检查链接的脚本 | 指向 `raw/` 的链接不算死链 | [ARD-BW](../decision-history/spec-driven-development-decision-history.md#ard-bw) |
| `checks/section_refs.py`、`counts.py`、`diagram_steps.py` | 对应的规则已改为 NICE，报出的问题改为提醒，不算失败 | [ARD-BN](../decision-history/spec-driven-development-decision-history.md#ard-bn) |
| `skills/spec-organize/tests/gold/v1/annotations.yaml` | 去掉「改旧句没划线」这条坏例子，改为「正文里出现删除线」 | [ARD-BM](../decision-history/spec-driven-development-decision-history.md#ard-bm) |
| `docs/book/html/` 下的网页 | 用 `tools/build_sdd_site.py` 重新生成 | TST-R |

**依赖：** 本批 spec 修改完成；IMPL-M。**挡住：** IMPL-E、IMPL-Q。

**Verify:** `run_spec_checks.py` 跑 `docs/features/spec-driven-development/` 报 0 个问题（旧文档不迁移，不检查别的 feature）（包括 `registry_provenance`）；TST-A 覆盖率 100%；TST-R 通过。

## IMPL-Q — 可读性测试

**目标：** 实现 TST-V：让一个 LLM 扮演本科程序员，只读一篇文档，回答从这篇的编号条目里抽出的问题；再找出第一次出现时没解释、术语表里也没有的词（[ARD-BO](../decision-history/spec-driven-development-decision-history.md#ard-bo)）。

**步骤：** 在 `skills/spec-organize/tests/` 下写出题、答题、判分的脚本；对照题不给文档，答对的题作废；结果写进评测报告。

**依赖：** IMPL-J、IMPL-P。**挡住：** IMPL-E 的可读性部分。

**Verify:** 对 SDD 的每篇已提交文档跑 TST-V，并在报告里列出每篇的答对率和没解释的术语。

## IMPL-R — CLAUDE 层和 skill 的规则同步

**目标：** parent design 的 DSGN-C 要求 CLAUDE 层（`CLAUDE.md`、`CLAUDE.local.md`）和 skill 里的规则一致。DSGN-A 的改动上限和 DSGN-B 的「什么时候记 ARD」要同时写进两处。

**步骤：** 标准文件改了之后，检查 CLAUDE 层里有没有对应的旧说法，一起改掉。2026-11-20 已改：`CLAUDE.local.md` 的改动上限从「10 行或 200 字符」改为「10 行并且 200 字符」，需求编号从不存在的 FR-12 改为 PRD-C（[ARD-BP](../decision-history/spec-driven-development-decision-history.md#ard-bp)）。

**依赖：** IMPL-C。**挡住：** 无。

**Verify:** CLAUDE 层里：改动上限写的是「并且」，并引用 PRD-C；没有 `FR-` 这类已禁止的编号；进度路径是 wayfinder 的地图目录（PRD-J、ARD-CH）；文档目录是 `docs/features/<f>/<类型>/`（document-standard 的 DSGN-B）；列出的 skill 是 spec-write、spec-review 和 wayfinder（ARD-CH）。2026-11-20 已按这几条改过 `CLAUDE.local.md`。

## IMPL-S — 插图与网页样式

**目标：** 网页里的插图用 diagram-design 的默认配色，SVG 文件在生成网页时嵌进页面；插图规则分清 MUST 和 NICE（[ARD-CA](../decision-history/spec-driven-development-decision-history.md#ard-ca)）。

**依赖：** IMPL-F。**挡住：** 无。

**Verify:** TST-W 通过。

## IMPL-T — L1 不减少的检查

**目标：** 实现 TST-X：`tools/check_l1_delta.py --base <git ref>`，默认和上一个 commit 比。

**依赖：** IMPL-M。**挡住：** 无。

**Verify:** `test_tst_x_l1_delta.py` 通过；对当前分支运行报 0 个问题。

## IMPL-U — spec bundle 版本戳

**目标：** `tools/build_spec_skills.py` 按 [ARD-CC](../decision-history/spec-driven-development-decision-history.md#ard-cc) 给五个 SDD `SKILL.md`（交付的 spec-write、spec-review、wayfinder，以及也引用标准文件的 spec-organize、spec-pipeline）打版本戳；每次 build 版本末位加 1（[ARD-CK](../decision-history/spec-driven-development-decision-history.md#ard-ck)）。

**依赖：** 无。**挡住：** 无。

**Verify:** TST-Y 通过。

## IMPL-V — GitHub Pages 发布

**目标：** `.github/workflows/pages.yml` 按 [ARD-CD](../decision-history/spec-driven-development-decision-history.md#ard-cd) 在 master 推送后重新生成并部署网站；删除从首页点不到的旧页面。

**依赖：** IMPL-H。**挡住：** 无。

**Verify:** TST-Z 通过；workflow 在 master 上成功部署。

## IMPL-W — wayfinder 轻量改写

**目标：** 按 [ARD-CH](../decision-history/spec-driven-development-decision-history.md#ard-ch) 改 `skills/wayfinder/SKILL.md`：地图文件当进度记录，审查关口用 spec-review，重新开始时给回顾。

**依赖：** 无。**挡住：** 无。

**Verify:** TST-AA 通过。

## IMPL-X — 复核 5 次加 Claude 核对

**目标：** `tools/judge_deepseek.py` 按 [ARD-CJ](../decision-history/spec-driven-development-decision-history.md#ard-cj) 默认跑 5 次、4 次一致才算定论，输出里留 `claude_audit` 给 Claude 填。

**依赖：** 无。**挡住：** 无。

**Verify:** TST-L 按 5 次判定。

## Execution order

先做不依赖别人的任务，被挡住的后做：

1. IMPL-A、IMPL-D、IMPL-G、IMPL-H、IMPL-U、IMPL-W、IMPL-X（互不依赖，可以同时做）
2. IMPL-C
3. IMPL-B、IMPL-F、IMPL-J、IMPL-K、IMPL-L、IMPL-M、IMPL-R
4. IMPL-N、IMPL-O、IMPL-P、IMPL-S（等 IMPL-F）、IMPL-T（等 IMPL-M）、IMPL-V（等 IMPL-H）
5. IMPL-Q
6. IMPL-E（评测要等 spec 可读、测试骨架齐全、gold 改回 iPhone 之后再跑）
7. IMPL-I

## Acceptance Criteria

- 分数 1 满分，并且 5 次独立复核里至少 4 次通过（ARD-CJ）。
- 分数 2 不低于同一 gold 版本的上一次运行（[ARD-R](../decision-history/spec-driven-development-decision-history.md#ard-r)：不设固定及格线）。
- 能执行的 TST-A 到 TST-AA 全部通过；`run_spec_checks.py` 跑 `docs/features/spec-driven-development/` 报 0 个问题。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-03 | Initial parent impl-plan; tasks 1–9 |
| 2026-11-03 | Task 6：Reader 改为富格式汇编，非 MD fetch |
| 2026-11-04 | Task 1–9 → IMPL-A–I；新增 IMPL-J–O：eval 配置、fixtures/cases、报告、检查器、skill 契约、reader |
| 2026-11-04 | Global Constraints 加 eval/no-migration；IMPL-D gold 路径改 iphone/v1 |
| 2026-11-18 | IMPL-D / IMPL-E：gold spec 改为这套 spec-driven-development（ARD-BJ） |
| 2026-11-20 | 每个 IMPL 写明依赖和挡住谁，执行顺序改为分组；IMPL-B 改为 spec-write 和 spec-review；IMPL-D、IMPL-E 改回 iPhone gold（ARD-BL）；IMPL-F 改为全站网页（ARD-BG）；验收的分数 2 从「不低于 6」改为「不低于上一次」，和 ARD-R、test-plan 一致；新增 IMPL-P（markdown 以外的欠账）和 IMPL-Q（可读性测试）；全文改为中文（ARD-BK） |
| 2026-11-20 | 第 1 轮审查后：依赖和挡住两头对齐（C 挡住 F；D 挡住 L；J 挡住 Q；E 依赖 J、L、Q；I 依赖 E） |
| 2026-11-20 | 第 2 轮审查后：IMPL-C 改为三份标准摘要（ARD-BX）；IMPL-P 加上 `.gitignore` 和 raw/ 链接两项，数字改为 15/32，解释 System Context 豁免；新增 IMPL-R（CLAUDE 层同步）；IMPL-G 写明暂定名也记在 CLAUDE.local.md（ARD-BU） |
| 2026-11-20 | 第 3 轮审查后：IMPL-A 解释 `~/.coworker/project.yaml`；IMPL-R 的检查加上进度路径、文档目录和 skill 列表 |
| 2026-11-20 | IMPL-P 除 MUST 清单出处外已完成；IMPL-Q 脚本就绪（未跑 API）；新增 IMPL-T |
| 2026-11-24 | IMPL-S、IMPL-T 移到依赖之后的批次；新增 IMPL-U；不迁移旧文档改链 ARD-CC |
| 2026-11-24 | 新增 IMPL-V：GitHub Pages 发布（ARD-CD） |
| 2026-11-24 | IMPL-K 进度：11 个机械审查案例已齐；5 个语义案例待 judge 执行器 |
| 2026-11-24 | IMPL-U 写明四个 skill；IMPL-P 现状更新；Verify 和验收只查 SDD 目录、覆盖到 TST-Z；IMPL-F、IMPL-H、IMPL-M 补上挡住的任务；IMPL-S 改成完整句子 |
| 2026-11-24 | IMPL-P 标为已完成，改引 ARD-BS |
| 2026-11-24 | 新增 IMPL-W、IMPL-X；IMPL-R 进度路径改为地图文件（ARD-CH）；IMPL-U 加升版本（ARD-CK） |
| 2026-11-24 | 第 8 轮审查后：IMPL-G 改为 CLAUDE 层只记地图路径；评测次数跟上 ARD-CJ；IMPL-U 五个 SKILL.md；验收改到 TST-AA |
