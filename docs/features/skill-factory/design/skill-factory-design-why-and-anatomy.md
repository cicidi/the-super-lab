---
feature: skill-factory
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# skill-factory — 为什么要做，一个 skill 怎么搭

本篇是 [skill-factory 设计](skill-factory-design.md) 的一个分篇（part）。
13 个必备章节只在入口文件里，本篇只回答两个问题。
第一，skill-factory 为什么存在，用户最初想要什么。
第二，在本仓库里，一个 skill 由哪些部分组成，又怎样从创建走到安装。

## 证据从哪里来

用户的原话来自本机的 opencode 会话库（`~/.local/share/opencode/opencode.db`）和 Claude Code 的输入历史（`~/.claude/history.jsonl`）。
下文用会话 id 的前 8 位加日期引用，例如 ses_14b5b4b7（2026-06-10）。
opencode 库里记的是 UTC 时间，下文日期一律换算成用户本地时间（太平洋时间）。
仓库事实引用 commit 短哈希，现状以 HEAD `b0b9be8` 为准。
旧决策引用 [decision-history](../decision-history/skill-factory-decision-history.md) 里的四位编号，例如第 0018 条。
找不到证据的地方写 UNKNOWN，不猜。

## 为什么要有 skill-factory

**DSGN-A 起点：把三类 skill 放在一处。**
skill 是一份 SKILL.md 文件，告诉 AI agent 遇到某类任务时按什么步骤做。
用户的第一句话是"我要做一个skill factory"（ses_14b5b4b7，2026-06-10）。
用户要放三类东西：自己写的好 skill；导入的别人的 skill，并且"复合版权，著名出处"；
以及只给自己用的 personal skill，放进 gitignore（git 不跟踪的文件清单）。
仓库的第一个提交是 `5d9747e`（2026-06-10），内容就是 skill-create。

**DSGN-B 开源。**
用户在同一场会话里说"我想做开源"（ses_14b5b4b7，2026-06-10），对应第 0009 条决策。

**DSGN-C 自举并迭代。**
自举的意思是：用工厂里的第一个 skill 去造工厂的其他工具。
用户说 create skill 是"最基础的一个skill"（ses_14bdec5d，2026-06-10）。
用户要求 skill-create 造出 skill-import 和 skill-edit；
产品不好时，先修 skill-create，再重新生成并复审，如此反复（ses_14aa890f，2026-06-10）。
对应第 0087、0088 条决策。具体需求见 [skill 的 PRD-I](../features/skill/prd/skill-prd.md)。

**DSGN-D 一个 skill 一个文件，只留一个版本。**
用户问过"为什么不是世界一个Skill.md 就行了，为什么做那么多层"（ses_14b5b4b7，2026-06-10）。
用户还说工厂"可以没有deploy 概念"，"就保留一个版本"，change log 放在 git 历史里（ses_14bdec5d，2026-06-10）。
"没有 deploy"后来成为质量门槛，见第 0112 条决策。

**DSGN-E 先查重，再动手。**
用户要求 skill-create 先去 GitHub 搜"至少10个热门的repo"。
然后让用户三选一：导入后再改、只吸收灵感、自己从头写（ses_14aa890f，2026-06-11）。
实现见 commit `d30f01c`，决策见第 0021、0083 条。

**DSGN-F 归属边界。**
2026-08-02 用户划了一条线：和 walter-worker 运行无关的 skill 都搬到 skill-factory，和运行有关的留在 walter-worker（b682481a，2026-08-02）。
walter-worker 是用户的另一个项目，负责安装、记忆和会话分析。
同一场会话里，用户举例说 research skill 应该放在 skill-factory。

**DSGN-G 后来加上的两个目标。**
2026-07-24 用户提出：一个本地 skill 被调用超过 10 次，就导入 skill-factory 的 personal 目录（71979623，2026-07-24）。
2026-10-30 用户提出：整个项目要有一个类似 spec 的网站，介绍 skill-factory，spec-driven 是其中一个 feature（d5833bbe，2026-10-30）。

入口 [PRD](../prd/skill-factory-prd.md) 的目标表写着"6 个月 50+ 个 skill""每月 20+ 个 fork"。
这些数字在上述会话里都找不到原话，出处是 UNKNOWN。
那份 PRD 的 Change Log 说它是从 126 条决策自动生成的。

## 目标与现状对照

下表把用户说过的目标和 HEAD `b0b9be8` 的现状并排放。
"不符"一列只陈述事实，要不要改由用户决定。

| 用户的目标 | 现状 | 符合吗 | 证据 |
|---|---|---|---|
| personal skill 不进 git（DSGN-A） | `personal-skills/` 下 9 个 skill 都被 git 跟踪；`.gitignore` 只写了 `personal/` | 不符 | ses_14b5b4b7；第 0018 条；commit `a2e4724` 起跟踪 |
| 导入的 skill 单独放一个目录 | 2026-08-02 起和自写的 skill 混在 `skills/` 里，只靠 README 的 🔗 标记和 `metadata.source_author` 区分 | 部分符合 | ses_14aa890f；commit `8d451059`、`93d4a4a` |
| 安装后名字带前缀 | 前缀已去掉 | 不符 | ses_14b5b4b7、ses_14aa890f；commit `bc4d6cc`、`6086424` |
| 格式规则只有一个出处 `CONVENTIONS.md` | 文件还在工作区，但 2026-08-02 起被 gitignore 并移出 git，新克隆的仓库里没有它 | 不符 | commit `226ef65`；[skill 的 PRD-C](../features/skill/prd/skill-prd.md) |
| 导入时保留作者和出处 | 7 个导入的 skill 的 frontmatter 都有 `source_author` 和 `source_url`；但 `/skill import` 的步骤里没有写这一步 | 部分符合 | 第 0085 条；[skill 的 QUES-C](../features/skill/design/skill-design.md) |
| 查重至少搜 10 个 repo（DSGN-E） | `/skill create` 保留了搜索，但没有写下限 | 部分符合 | [skill 的 PRD-B](../features/skill/prd/skill-prd.md) |
| 修 create 再重新生成，反复迭代（DSGN-C） | 没有自动测试来判断"产品好不好" | 不符 | [skill 的 QUES-A](../features/skill/design/skill-design.md) |
| 调用超过 10 次就导入 personal 目录（DSGN-G） | 没找到按次数导入的代码；walter-worker 的 pending 队列把批准的 skill 放到 `~/.coworker/skills`，不是本仓库 | 未找到实现 | walter-worker `src/coworker/memory/pending.py`（commit `1096d01`） |

2026-08-02 的合并（commit `6086424`，38 个 skill 合成 11 个）还删掉了用户在 06-23 要过的改动。
例子见 [bug 的 design](../features/bug/design/bug-design.md) 和 [auto-tdd 的 design](../features/auto-tdd/design/auto-tdd-design.md) 的 Open Questions。

## 一个 skill 由什么组成

**DSGN-H 目录。**
每个 skill 是一个文件夹，里面必须有一份大写的 `SKILL.md`（`CONVENTIONS.md` 的 File Structure 一节）。
仓库只有两个放 skill 的目录。
`skills/` 放在本仓库写的 skill 和导入的 skill，HEAD 有 17 个。
`personal-skills/` 放用户自己用的 skill，HEAD 有 9 个。
早期的 `import-skills/` 和 `walter-worker-skills/` 已经不存在（commit `8d451059`、`93d4a4a`）。

**DSGN-I frontmatter。**
frontmatter 是 SKILL.md 开头两行 `---` 之间的 YAML 元数据，agent 靠它决定何时调用这个 skill。
规定的字段有五个：`name`、`description`、`license`、`compatibility`、`metadata`（`CONVENTIONS.md` 的 Frontmatter 一节）。
`description` 以 "Use when" 开头，写触发条件，不写流程。
`metadata` 是一个自由的键值表，本仓库常用 `triggers`；导入的 skill 还用 `when_to_use`、`source_author`、`source_url`（例如 `skills/wayfinder/SKILL.md`）。
HEAD 的 26 个 skill 里，24 个五个字段齐全。
`personal-skills/create-video-workflow` 和 `personal-skills/transcribe-audio` 只有 `name` 和 `description`。
入口设计里的"带 `trigger` 字符串的五字段格式"已过时，见入口的 Known Drift 表。

**DSGN-J 正文章节。**
`CONVENTIONS.md` 的 Body Structure 一节规定了正文章节，必备的是标题加概述、`## When to Use`、`## When NOT to Use`、`## Process`。
HEAD 有 10 个 skill 至少缺一个必备章节。
7 个从 mattpocock/skills 导入的 skill 都在其中，它们把 when_to_use 写进了 `metadata`，而不是正文章节。
[skill 的 DSGN-C](../features/skill/design/skill-design.md) 说导入时要补齐这两节，但这 7 个没有补。
另外 3 个是 `personal-skills/` 下的 `luma-event-scout`、`video-production-pip-style` 和 `create-video-workflow`。
禁止的写法（如正文里写 Changelog、TBD 占位）也在 `CONVENTIONS.md` 的 Prohibited 一节。

**DSGN-K 附属文件。**
一个 skill 可以在 `SKILL.md` 旁边放别的文件，例如 `skills/domain-modeling/ADR-FORMAT.md`、`personal-skills/pic-to-txt/ocr.py`、`skills/spec-review/tests/`。
安装时复制的是文件夹顶层的文件，所以附属文件会跟着 skill 走；`tests/` 这样的子目录不会被复制（walter-worker `setup/install.sh` 的 Step 11b，commit `a3d08d7`）。

**DSGN-L 命名。**
名字用 kebab-case，即全小写、用连字符连接，格式是"动词-对象"或"领域-动作"（`CONVENTIONS.md` 的 Skill Naming 一节）。
`name` 字段必须和文件夹名一致，用户原话是"name 和文件夹必须匹配"（ses_14aa890f，2026-06-11）。
HEAD 的 26 个 skill 都满足这一条。
导入的 skill 保留原名，见 [skill 的 PRD-E](../features/skill/prd/skill-prd.md)。

## 生命周期：创建、修改、导入、安装

**DSGN-M 创建、修改、导入。**
这三件事都通过一个 `/skill` 命令完成，用子命令区分（commit `6086424` 把原来四个 skill 合成一个）。
每一步做什么，见 [skill 的 design](../features/skill/design/skill-design.md) 的 DSGN-A 到 DSGN-C，本篇不重复。
三者共同的规则是：只在源仓库 `~/project/the-super-lab/` 里改，草稿或 diff 给用户确认后才写入文件。

**DSGN-N 安装。**
改动提交并推送后，由 walter-worker 的 `setup/install.sh` 把 skill 部署到三个 harness（运行 skill 的 AI 工具）。
Claude Code 和 Cursor 各得到一份文件夹副本，分别在 `~/.claude/skills/<name>/` 和 `~/.cursor/skills/<name>/`。
OpenCode 得到一个指回源目录的符号链接（symlink），`skills/` 进 `the-super-lab`，`personal-skills/` 进 `the-super-lab-personal`。
以上见 `setup/install.sh` Step 11b 的注释（commit `a3d08d7`，2026-11-23）。
`CONVENTIONS.md` 还写着 Cursor 得到 `~/.cursor/rules/<name>.md` 的扁平副本，这已过时。
不要直接改部署出去的副本，下次安装会覆盖（`CONVENTIONS.md` 的 Source Repo vs Deployed Copies 一节）。
改名后旧副本可能残留，见 [skill 的 design](../features/skill/design/skill-design.md) 的 Risks and Mitigations。

**DSGN-O 列出。**
`/skill list` 运行 `coworker skill list`，列出每个 skill 的名字、路径和是否启用（`skills/skill/SKILL.md`）。

## 各个 skill 的规格

每个 skill 自己的需求、设计和决策写在子 feature 里，本篇只链接。
目录是 `docs/features/skill-factory/features/<skill>/`，每个下面有 prd、design、decision-history 三份。
入口：
[auto-tdd](../features/auto-tdd/prd/auto-tdd-prd.md)、
[bug](../features/bug/prd/bug-prd.md)、
[create-video-workflow](../features/create-video-workflow/prd/create-video-workflow-prd.md)、
[doc-protect](../features/doc-protect/prd/doc-protect-prd.md)、
[domain-modeling](../features/domain-modeling/prd/domain-modeling-prd.md)、
[english-grammar-fix](../features/english-grammar-fix/prd/english-grammar-fix-prd.md)、
[grill-with-docs](../features/grill-with-docs/prd/grill-with-docs-prd.md)、
[implement](../features/implement/prd/implement-prd.md)、
[luma-event-scout](../features/luma-event-scout/prd/luma-event-scout-prd.md)、
[multi-model-team](../features/multi-model-team/prd/multi-model-team-prd.md)、
[pic-to-txt](../features/pic-to-txt/prd/pic-to-txt-prd.md)、
[prototype](../features/prototype/prd/prototype-prd.md)、
[skill](../features/skill/prd/skill-prd.md)、
[tmux-status-bar](../features/tmux-status-bar/prd/tmux-status-bar-prd.md)、
[to-spec](../features/to-spec/prd/to-spec-prd.md)、
[to-tickets](../features/to-tickets/prd/to-tickets-prd.md)、
[transcribe-audio](../features/transcribe-audio/prd/transcribe-audio-prd.md)、
[video-production-pip-style](../features/video-production-pip-style/prd/video-production-pip-style-prd.md)、
[wayfinder](../features/wayfinder/prd/wayfinder-prd.md)、
[youtube-summarize](../features/youtube-summarize/prd/youtube-summarize-prd.md)。
`research`、`youtube-research-pipeline` 和 `spec-*` 系列还没有子 feature 规格。

## 未知项

- 入口 PRD 里的量化目标（50+ 个 skill、20+ 个 fork 等）出自哪里：UNKNOWN。
- `CONVENTIONS.md` 被 gitignore 是否是有意的：commit `226ef65` 的那次请求里，用户贴的文本内容看不到（b682481a，2026-08-02），所以 UNKNOWN。
- `personal-skills/` 被 git 跟踪是否已经改了主意：没找到用户改口的原话，UNKNOWN。
- 本仓库是否仍是公开仓库：本篇没有核实，UNKNOWN。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从会话和 git 历史整理 skill-factory 的动机、目标与现状对照、skill 的组成和生命周期 |
