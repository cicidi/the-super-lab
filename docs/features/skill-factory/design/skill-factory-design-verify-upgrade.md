---
feature: skill-factory
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# skill-factory — 怎么验证 skill，怎么装进 AI 工具并升级

本篇是 [skill-factory 设计](skill-factory-design.md) 的一个分篇（part）。
13 个必备章节只在入口文件里，本篇只回答两个问题。
第一，skill-factory 怎样检查一个 skill 写得对不对，包括质量门、测试、评审和评测。
第二，skill 怎样被安装、分发和升级到 Claude Code、OpenCode 和 Cursor 这三个 AI 工具里。
每个问题都先写用户要过什么，再写现在有什么，最后用一张表对照差距。
skill 的组成和生命周期见 [为什么要做，一个 skill 怎么搭](skill-factory-design-why-and-anatomy.md)，本篇不重复。

## 证据从哪里来

用户的原话来自本机 opencode 会话库和 Claude Code 输入历史（`~/.claude/history.jsonl`）。
下文用会话 id 的前 8 位加日期引用，例如 ses_14aa890f（2026-06-10）。
本仓库的现状以 HEAD `d865462` 为准。
walter-worker 是用户的另一个项目，负责安装和升级；它的现状以 HEAD `a0f4ce0` 为准，这也是它的 `origin/master`（2026-11-24 核对）。
旧决策引用 [decision-history](../decision-history/skill-factory-decision-history.md) 的四位编号，例如第 0105 条。
文中"运行结果"都是 2026-11-24 在本机实际跑出来的。
找不到证据的地方写 UNKNOWN，不猜。

几个术语先说明。
质量门（quality gate）是一条检查规则，不满足就不许提交。
CI（持续集成）是每次推送代码时由 GitHub 自动运行的检查。
评测（eval）是让 skill 真的跑一遍任务，再按标准答案打分。
harness 指运行 skill 的 AI 工具，这里是 Claude Code、OpenCode 和 Cursor。
manifest（安装清单）是安装脚本写下的"我装了哪些文件"的记录，位置是 `~/.coworker/install-manifest.json`。
prune（修剪）指删除上一次装过、这一次不再产出的文件。

## 用户在验证方面要过什么

**DSGN-P 用多个 agent 互相评审，反复迭代。**
用户要求先用一个 agent 模拟用户、在 skill-create 引导下造出 skill-edit；再用另一个 agent 自评；再来一个 subagent 审查，找出 skill-create 哪里出了问题，然后重复（ses_14aa890f，2026-06-10）。
用户还说，skill 做得不好时要修 skill-create，重新生成，再评审，"如此迭代"（同一会话）。
这件事做过一轮。
commit `1d7bb7e` 提交了 Agent-A 造出的两个 skill，`d9baa43` 提交了 Agent-B 的评估报告，结论是两个都 PASS（第 0002 条）。
commit `33e48d2` 按这轮评审改进了 skill-create 的质量门（第 0001 条）。
这些评审记录放在 `docs/superpowers/rounds/round-01/`，2026-06-23 被移出 git（commit `add4f31`）。
此后再没有第二轮的记录，也没有可以重复运行的脚本。

**DSGN-Q 先写测试计划，再由另一个 agent 执行。**
用户要一个 work-review skill：第一个 agent 只写测试计划，不写测试代码；第二个 agent 执行计划，可以写代码、跑 Playwright（浏览器自动化工具）、跑开发者自己的单元测试（ses_145b2d79，2026-06-12）。
对应第 0122、0123 条。
work-review 后来并进 doc-review（commit `6086424`），doc-review 又在 2026-11-04 从 `skills/` 删除（commit `c44e983`）。
现在承担评审的是 `spec-review`，它审的是 spec 文档，不审 SKILL.md。

**DSGN-R 改 skill 时同时写测试，跑到通过为止。**
用户在本仓库说"现在开始 impl skill 或者修改 skill 然后同时写 test 跑 test 直到 test 过了"（2891600e，2026-11-04）。
用户还要一个循环：用 spec-review 审 spec，改 spec，"重新 train skill，验证 skill 好不好，跑一遍测试"，再审，直到找不出新问题（f62ad5e2，2026-11-23；14c9ad77，2026-11-24）。
在另一个项目里，用户也要求用 subagent 把同一个 skill 跑好几次，看产出有没有问题（eb214735，2026-10-09）。
这些话都是在做 spec-driven-development（SDD）相关 skill 时说的。
它们是否也要求其他 skill 有同样的测试，没有找到原话，记为 UNKNOWN。

**DSGN-S 安装和升级也要测，要有验收。**
用户要求检查"安装 upgrade 测试是否完整"（d4853c97，2026-07-14）。
同一天用户还要求"所有的完成都必须证据，安排一个验收的 subagent，实际考察验收"（84019fa1，2026-07-14）。

## 用户在安装和升级方面要过什么

**DSGN-T 同一份 skill 装进所有 AI 工具。**
2026-07-14 用户说，安装和升级都要覆盖两个 IDE，"script and skill 都要作"（6d322231，2026-07-14）。
2026-07-24 用户要求 skill 同时放进 Claude Code 和 OpenCode 的 skill 目录，并问两者能否共用一个目录（71979623，2026-07-24）。
2026-09-24 用户把规则定下来：the-super-lab 是唯一的源头，每次先改这里，再部署到 Claude Code、OpenCode 和 Cursor（ef7cf4dd，2026-09-24）。
2026-11-23 用户问 Claude Code 和 Cursor 的 skill 地址变没变，walter-worker 的安装还能不能用（00df8b66，2026-11-23）。
这一问直接引出了 walter-worker 的 commit `a3d08d7`。

**DSGN-U 升级由一个 skill 全包，修复也走升级。**
用户说 upgrade skill 要"全包"：安装 skill，更新 CLAUDE.md（7b214ca4，2026-07-17）。
用户还要求发现问题时先改 walter-worker 本身，再通过升级把修复带回来（6d322231，2026-07-14；e5b482e3，2026-07-17）。
这就是 `walter-worker-fix` 和 `walter-worker-upgrade` 两个 skill 的来历。

## 现在怎么验证

**DSGN-V 质量门只写在文字里，没有程序去执行。**
入口设计 2.3.1 节列了 MUST 门，例如正文少于 150 行、必须有 Quality Gates 一节、不许出现 deploy 目录。
MUST 门不满足就挡住提交，NICE 门只给警告（第 0096、0105、0112、0126 条）。
但现在的 `skills/skill/SKILL.md` 里，create 流程只有"起草、给用户看、确认后保存"三步，没有"运行质量门"这一步。
HEAD 的 26 个 skill 里，只有 13 个有 `## Quality Gates` 一节，有 12 个文件超过 150 行（2026-11-24 在 HEAD 上统计）。
所以这些门并没有挡住任何提交。

**DSGN-W 唯一一个通用的 skill 校验脚本已经过时。**
`tests/test_skills.sh` 是 2026-06-24 加的（commit `559834a`），2026-08-02 只做过一次改名（commit `015f3ff`）。
它检查目录、frontmatter 五个字段、必备章节、禁用写法和命名。
它默认去找 `~/project/skill-factory`，这个目录已经不存在，所以直接运行会报错退出。
它只扫描 `walter-worker-skills/`、`personal-skills/`、`import-skills/` 三个目录，从来不看 `skills/`。
设置 `SKILL_FACTORY_SOURCE` 指向本仓库后运行，只测到 9 个 skill，结果是 37 项通过、15 项失败。
15 项失败里，2 项是旧目录不存在，6 项是两个 skill 缺 frontmatter 字段，6 项是缺必备章节，1 项是正文有装饰性 emoji。
这次运行读的是工作区，其中 `personal-skills/luma-event-scout/SKILL.md` 有未提交的改动。
这个脚本不在任何 CI 里。

**DSGN-X CI 只检查 SDD。**
本仓库有两个 CI 工作流。
`.github/workflows/sdd-mechanical.yml` 运行 `tools/run_sdd_mechanical.sh`，它再调用 `skills/spec-organize/tests/run_mechanical.sh`。
那个脚本里的每一项检查，对象都是 spec 文档或 `spec-*` 系列 skill。
`.github/workflows/pages.yml` 只负责把文档构建成网站并发布。
`skills/` 下被 git 跟踪的测试文件，只在 `spec-organize/tests/`（130 个文件）和 `spec-review/tests/`（29 个文件）里。
`skills/spec-organize/tests/test_skill_examples.py` 也只检查 `spec-pipeline`、`spec-organize`、`spec-review`、`spec-write` 四个 skill。
结论是：SDD 以外的 skill，没有一个测试覆盖。

**DSGN-Y 行为评测也只覆盖 SDD。**
SDD 的 skill 有一套评测：用标准答案（gold）和裁判模型（judge）给 skill 的产出打分，配置在 `skills/spec-organize/tests/eval.yaml`。
最近一次是 commit `68c52ce`（2026-11-24），提交信息写着 54 条 MUST 全过。
这套评测的设计见 [SDD 的 test-plan](../../spec-driven-development/test-plan/spec-driven-development-test-plan.md)，本篇不重复。
其他 skill 没有类似的评测，也没有标准答案。

**DSGN-Z walter-worker 那一侧有安装测试。**
walter-worker 的 `tests/setup/test_install.bats` 用 bats（一个 shell 测试框架）测 `setup/install.sh`，共 40 个用例。
用例覆盖部署到三个 harness、跳过指回源目录的符号链接、按 manifest 修剪旧文件等。
2026-11-24 本机运行，40 个全部通过。
walter-worker 的 `.github/workflows/ci.yml` 有一个 bats 任务运行这些用例。
`tests/python/test_skill_factory_integration.py` 检查本仓库的 skill 和部署副本是否一致。
它需要本机有本仓库的检出，所以在 CI 里会被跳过。
本机运行结果是 10 个通过、1 个失败。
失败原因是 `skills/spec-html-standard/` 没有 SKILL.md，这个目录在 2026-11-04 加入（commit `c44e983`）。
它对 frontmatter 只检查有没有 `name` 和 `description`。
`walter-worker-upgrade` 这个 skill 本身没有测试。

## 现在怎么安装和升级

**DSGN-AA 安装入口是 walter-worker 的 `setup/install.sh`。**
Step 3 先对本仓库做一次 `git pull --ff-only`，失败只警告、继续用本地版本；本仓库默认位置是 `~/project/the-super-lab`。
Step 11b 把 `skills/` 和 `personal-skills/` 下每个带 SKILL.md 的目录部署出去。
Claude Code 和 Cursor 各得到一份目录副本，位置是 `~/.claude/skills/<name>/` 和 `~/.cursor/skills/<name>/`。
OpenCode 得到指回源目录的符号链接，`skills/` 进 `~/.config/opencode/skills/the-super-lab/`，`personal-skills/` 进同级的 `the-super-lab-personal/`。
写 Cursor、部署 personal-skills、遇到指回源目录的目标就跳过，这三点来自 commit `a3d08d7`（2026-11-23，PR #14，合并提交 `2b5da57`）。
Step 10 不再把本仓库的 skill 另写一份 `~/.claude/commands/<name>.md`，内容和源文件一致的旧副本会被删掉，这来自 commit `893e17c`（2026-11-24，PR #15，合并提交 `a0f4ce0`）。
2026-11-24 本机状态：`~/.cursor/skills/` 有 26 个 skill，OpenCode 两个目录分别有 17 个和 9 个链接，`~/.cursor/rules/` 是空的。

**DSGN-AB 修剪只删自己装过的东西。**
Step 16 写 manifest 时，把上一次 manifest 记过、这一次不再产出的路径删掉。
这段修剪逻辑最早出现在 commit `c7fbf3c`（2026-09-25）。
记忆笔记 `coworker-skill-mirror-drift.md` 的标题仍写着"从不 prune"，这已过时；笔记正文 2026-11-23 的更新段落写的是现状。
从没被 manifest 记过的文件不会被删。
本机还留着 `~/.claude/commands/doc-review.md` 和 `doc-organize.md`，两个文件的日期都是 2026-09-25。
它们的源在 2026-11-04 已经从 `skills/` 删除（commit `c44e983`），但在本会话里仍然可以被调用。
其中 `doc-organize.md` 至今仍被 manifest 记着，所以不会被修剪；为什么还被记着，UNKNOWN。

**DSGN-AC `walter-worker-upgrade` 和 `install.sh` 各装一遍，而且做法不同。**
`skills/walter-worker-upgrade/SKILL.md` 最后一次修改是 commit `5a1b951`（2026-09-25）。
它的 Phase 4 自己装 skill，Anti-Patterns 第 6 条说 Phase 4 是唯一权威的安装者。
Phase 5 再运行 `install.sh`，并输入 `0` 来"跳过选择 skill"。
但 `install.sh` 的 Step 11b 不看这个选择，照样部署全部 skill（Step 7 的注释写明了这一点）。
所以一次升级会用两套逻辑各装一遍。
两套逻辑有四处不一致。
第一，Phase 4 去 `~/.config/opencode/skills/the-super-lab` 拉取本仓库，但那里现在只是一个放符号链接的普通目录，不是 git 仓库，拉取会失败。
第二，Phase 4 把整个目录用符号链接装进 `~/.claude/skills/` 和 `~/.opencode/skills/`，而 `install.sh` 用的是目录副本和 `~/.config/opencode/skills/` 下的两个目录。
指回源目录的符号链接，正是 commit `a3d08d7` 修过的"same file"中断的起因（见 `install.sh` Step 11b 的注释）。
第三，Phase 4 完全没有 Cursor。
第四，Phase 1 拉取 `origin/main`，但 walter-worker 只有 `master` 分支。
Phase 4 判断"要不要更新"用的是文件修改时间（`-nt`），不比较内容。

**DSGN-AD `walter-worker-fix` 的验证步骤有两处跑不通。**
它的 Verify 一步运行 `bash setup/install.sh --dry-run 2>&1 || true`。
`install.sh` 不认识 `--dry-run`，会报"Unknown argument"并退出；`|| true` 把失败吞掉了，所以这一步永远显示成功。
它的提交一步运行 `git push origin main`，而分支名是 `master`。
这个 skill 只修 walter-worker 自己。
本仓库的 skill 出错时没有对应的"修完再分发"流程；记录纠正的路径见 [bug 的 design](../features/bug/design/bug-design.md) 的 Heal 分支。

**DSGN-AE 列表看不到工厂里的 skill，旧的 marketplace 方案没有落地。**
`/skill list` 运行 `coworker skill list`。
2026-11-24 本机运行，列出 15 个：13 个来自 `~/.coworker/coworker.yaml`，2 个来自本仓库的 `.coworker/` 配置（`spec-write`、`spec-review`）。
本仓库其余 24 个 skill 都不在列表里。
第 0012 条决定用 Claude Code 的 `extraKnownMarketplaces`（本地插件市场）安装。
但本仓库从未提交过 marketplace 文件，`.claude-plugin/` 是一个未被跟踪的空目录。
本机 `~/.claude/settings.json` 的 `extraKnownMarketplaces` 里也只有一个无关的条目。
现在实际在用的是 DSGN-AA 的复制加链接方案。

## 目标与现状对照

下表把用户要过的东西和现状并排放。
"差距"一列只陈述事实，要不要改由用户决定。

| 用户要什么 | 现在有什么 | 差距 | 证据 |
|---|---|---|---|
| 多 agent 评审、反复迭代 skill-create（DSGN-P） | 2026-06-10 做过一轮，记录已移出 git | 只做过一次，没有可重复的流程 | ses_14aa890f；`d9baa43`；`add4f31` |
| MUST 质量门挡住提交（DSGN-V） | 门只写在文字里；`/skill create` 没有运行门的步骤 | 26 个里 13 个缺 Quality Gates 一节，12 个超过 150 行 | 第 0096、0105、0126 条；`skills/skill/SKILL.md` |
| 合并前跑格式校验（入口 PRD 的 F11、F15；test-plan 的 CI-01 到 CI-03） | `tests/test_skills.sh` 只扫旧目录，不进 CI | `skills/` 下的 17 个 skill 从未被这个脚本校验过 | [PRD](../prd/skill-factory-prd.md)；[test-plan](../test-plan/skill-factory-test-plan.md)；`559834a` |
| 改 skill 同时写测试、跑到通过（DSGN-R） | 只有 `spec-*` 有测试和评测 | SDD 以外的 skill 没有测试 | 2891600e；`68c52ce`；`.github/workflows/sdd-mechanical.yml` |
| 导入时审查内容安全（入口 PRD 的 N2） | 导入只补格式 | 没有内容审查 | [skill 的 QUES-B](../features/skill/design/skill-design.md) |
| 装进 Claude Code、OpenCode、Cursor（DSGN-T） | `install.sh` Step 11b 部署全部 26 个 | 符合 | ef7cf4dd；`a3d08d7` |
| 改名或删除后不留旧副本 | manifest 修剪已有 | 没被记过的文件仍残留，例如 `doc-review.md` | `c7fbf3c`；`c44e983` |
| 升级由一个 skill 全包（DSGN-U） | `walter-worker-upgrade` 的路径和分支过时，没有 Cursor，和 `install.sh` 重复安装 | 不符 | 7b214ca4；`5a1b951` |
| 安装和升级要测（DSGN-S） | 40 个 bats 用例在 CI 里全过；集成测试 1 个失败 | 升级 skill 本身没有测试 | d4853c97；walter-worker `tests/setup/test_install.bats` |
| 先修 walter-worker 再升级分发（DSGN-U） | `walter-worker-fix` 存在 | `--dry-run` 和 `main` 两处跑不通 | 6d322231；walter-worker `skills/walter-worker-fix/SKILL.md` |
| 用本地 marketplace 安装（第 0012 条） | 没有 marketplace 文件 | 决策已被实际做法取代，但没有新的决策记录 | 第 0012 条；`.claude-plugin/` 为空 |

## 未知项

- `~/.claude/commands/doc-organize.md` 的源已删除，为什么仍被 manifest 记着：UNKNOWN。
- 本仓库 `sdd-mechanical` CI 在最近一次推送上是否通过：本篇没有查 GitHub，UNKNOWN。
- OpenCode 是否能识别 `~/.config/opencode/skills/the-super-lab/<name>/` 这种多一层的目录：`install.sh` 的注释只说 OpenCode 从 `<config>/skills` 取 skill，没有说支持多深，UNKNOWN。
- 用户要的"写 skill 同时写测试"是否适用于 SDD 以外的 skill：UNKNOWN，见 DSGN-R。
- 第 0012 条的 marketplace 方案是何时、为何放弃的：没有找到记录，UNKNOWN。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从会话、两个仓库的代码和本机运行结果整理 skill 的验证方式、安装与升级流程，以及目标与现状对照 |
