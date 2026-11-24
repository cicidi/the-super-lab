---
feature: create-video-workflow
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# create-video-workflow — 研究文档变内容

本篇说明 `create-video-workflow` 这个 skill 现在怎么工作。
源文件：`personal-skills/create-video-workflow/SKILL.md`（commit c4159a9），与 hackathon-video-gen 仓库 commit 8a9bc62 的版本完全相同。
下文把 hackathon-video-gen 简称 hvg。

## Problem Statement

旧版只能把一个想法做成 30 到 60 秒的竖屏短视频，写死了 2 个模板和 6 个场景（decision-history 的 ARD-G）。
用户做完研究后，想按听众和传播渠道，把文档变成演示、视频或网站（PRD-A、PRD-B）。

## Solution

一个 8 段的流水线，编号 Phase 0 到 Phase 7，中间有 4 个检查点（checkpoint，必须停下等用户说 continue 的地方）。
阶段对应软件工程：Phase 0-2 是需求和设计，3 是 spec，4 是实施，5 是 build，6 是验收，7 是发布（PRD-H）。
SKILL.md 自称"7-phase"，但实际编号从 0 到 7，共 8 段。

## User Stories

- 作为创作者，我说"把这篇论文做成 YouTube 视频"，走完整流程，最后上传（SKILL.md 的 Standard 例子）。
- 作为工程师，我说"把会议记录做成团队幻灯片"，走轻量流程，验收只略看（Lite 例子）。
- 作为产品负责人，我要一个发布视频、一个落地页和内部文档，三个渠道分别验收、分别发布（Full 例子）。

## Implementation Decisions

skill 目录下只有 SKILL.md 一个文件，本身不带脚本。生成视频和图片要调用 hvg 仓库里的 Python 脚本（ARD-H）。
所有中间文件都写在 `projects/<name>/` 下，一个内容项目一个目录（ARD-K）。
唯一声明的依赖是 `doc-organize`：Phase 4 生成文档时，用它决定路径和文件名（PRD-G）。

## Design

**DSGN-A Phase 0 渠道与听众。** 先问用户内容发到哪里：YouTube、抖音或公众号、公司内部文档、会议演讲、GitHub demo、网站，或多个渠道（PRD-C）。
每个渠道定下听众的专业程度、细节深度、语气和平台格式（PRD-B）。
和用户一起写一段 Goal 声明，说清核心信息；它是 Phase 6 验收的靶子（PRD-I）。
产出 `requirements.md`：渠道与听众、Goal、成功标准、范围。用户说不清目标时，用"教程、推介、深度技术、公告"几类例子帮他收窄。

**DSGN-B Phase 1 素材摄入和检查点 1。** 输入可以是 markdown、PDF、网页、YouTube 链接、GitHub 仓库或公司内部文档（PRD-A）。
每种都抽成文字，合并进 `source_material.md`。付费墙、纯音频、死链这类读不了的，记进 gaps 一节，问用户怎么办。
检查点 1：列出收了什么、跳过什么，问用户素材够不够撑起 Goal。

**DSGN-C Phase 2 内容大纲。** 大纲不套模板，不强制 6 个场景；可以是 2 张幻灯片、1 段视频或 3 节文档（PRD-E）。
每个内容单元写明类型、主题、要点和大致长度，存为 `content_plan.md`，交给用户确认。
用户反复否定时，退回"开头、主体、结尾"的线性结构，留给 Phase 3 细化。不再问用户要不要模板（PRD-N，见 QUES-C）。

**DSGN-D Phase 3 文稿与 spec，检查点 2。** `transcript.md` 是给人听和看的文稿，不是学术文章（PRD-C）。
语气按渠道分五种：YouTube 像博主聊天，抖音短而有钩子，公司内部专业清楚，会议演讲配合幻灯片，GitHub demo 偏技术演示。
`spec.json` 每个内容单元一条，是 Phase 4 的输入（PRD-H）。字段有类型、文稿片段、屏幕文字、画面描述、配音 `voiceover`（PRD-M）。
还有 `engine`，按单元类型选 seedance、gemini、chatgpt 或 ffmpeg，以及输出尺寸 `format`（PRD-D）。
检查点 2：用户逐段改文稿，检查 spec 是否覆盖每个单元。

**DSGN-E Phase 4 资源生成，检查点 3。** 按 spec.json 的类型分派：视频走 hvg 的旧脚本链，依次生成叙事、场景、图片、视频，再轮询任务（PRD-E）。
幻灯片写成带分隔符的 markdown；文档先用 doc-organize 定位置（PRD-G）；网站生成 HTML、CSS、JS；动画生成给引擎的 prompt。
能并行的都并行（PRD-F）。图片可以并行，视频按顺序生成，用上一段的尾帧接下一段（PRD-L）。
产物放在 `output/<type>/`，进度记在 `gen_status.json`。失败时重试、跳过或换简化 prompt。
检查点 3：用户逐个看视频、图片和文档，可以说"重做第 N 个场景"。

**DSGN-F Phase 5 合成。** 视频用 `concat.sh` 统一格式后拼接；幻灯片编成一个演示文件（PRD-F）。
markdown 里插入图片和视频的链接或占位符；网站把页面和资源连起来。
多格式时打成一个目录，放在 `output/final/`，并写一个 README 列出所有产物。

**DSGN-G Phase 6 听众 agent 验收，检查点 4。** 听众 agent 是另起的一个 AI 实例，按 Phase 0 的听众画像设定（PRD-I）。
它要能读文字、看视频、听音频，写出观后感和一句话总结，存为 `audience_review.md`。
总结和 Goal 不一致时，按原因回退：目标不清回 Phase 0，缺例证回 1，结构问题回 2，语气问题回 3，画面不对回 4。
检查点 4：把观后感、总结和 Goal 并排给用户，用户选通过或修改。

**DSGN-H Phase 7 发布。** 按渠道发布：YouTube 和抖音走平台 API，内部文档推到 Confluence 或 Notion，GitHub 推代码并建 release，网站部署到托管平台（PRD-J）。
写 `release_notes.md` 记录发了什么、发到哪、何时、链接，并逐个确认链接能打开。
没有 API 时导出文件并附手动上传说明；API 失败重试一次，再转人工。

**DSGN-I 检查点、错误和质量门。** 4 个检查点都写着 STOP，用户说 continue 才往下走（PRD-G）。
任何阶段出错就停在原地，记进 `errors.md`，让用户选重试、跳过、改需求或放弃。
每个阶段有一条质量门，例如 Phase 0 的 Goal 必须明确可衡量，Phase 6 的总结必须对上 Goal。

**DSGN-J 存放和入口。** 一份在 hvg 的 `.claude/skills/`，hvg 的 CLAUDE.md 把它定为主入口；另一份在本仓库 `personal-skills/`（PRD-K）。
两份目前内容相同，但没有写明谁是正本，见 QUES-F。

## Testing Decisions

SKILL.md 列了 3 个测试场景：论文做 YouTube 视频、内部文档做团队演示、GitHub 仓库做落地页。它们只写了期望行为，没有自动测试或评测集。
analytics.db 里没有找到调用 v3 的记录；2026-07-23 的 omnigent vlog 会话（d1bc3211）也没有用它。v3 是否完整跑通过，属于 UNKNOWN。

## Out of Scope

已有成稿、只拼 30 到 60 秒短视频的，走 git 历史里的旧 5 步流程或直接调脚本；只要文字摘要的，交给摘要类 skill。
单个 PDF 且没有演示意图的，用更简单的抽取流程（SKILL.md 的 When NOT to Use 一节）。

## Further Notes

需求见 [PRD](../prd/create-video-workflow-prd.md)，决策见 [decision-history](../decision-history/create-video-workflow-decision-history.md)。
旧版可在 hvg 仓库用 `git show c440a27:.claude/skills/create-video-workflow/SKILL.md` 查看，含模板和 tasks.json 格式。
音频素材可交给 `transcribe-audio` 转文字，它的描述里写了服务于本 skill 的 Phase 1（hvg commit ca6bb23，2026-07-22）。

## Alternatives Considered

另建一个叫 research-to-content 的编排 skill、旧 skill 当子程序：被否决，直接改写旧的（ARD-G）。
所有渠道用同一种口语化语气：被否决，改为按渠道定语气（ARD-F）。
合成完就结束、由用户手动发布：被否决，加了听众验收和发布两个阶段（ARD-C、ARD-B）。

## Drawbacks

8 段加 4 个检查点，对"会议记录做几张幻灯片"这类小请求偏重；SKILL.md 只靠 Lite 例子示意可以简化。
听众 agent 由 AI 扮演，SKILL.md 自评这一步信心为 medium，取决于模拟听众的 prompt 质量。
skill 依赖 hvg 仓库的脚本，换到别的项目里用时，Phase 4 和 Phase 5 的视频部分跑不起来。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| SKILL.md 写的是 `tools/`，但 hvg 在 v3 之前已把它改名为 `scripts/`（commit b805482） | 暂无；见 QUES-A |
| `projects/` 已从 hvg 移到 video-gen-initiative 仓库（hvg commit cb2d6d4），SKILL.md 仍写 `projects/<name>/` | 暂无；见 QUES-B |
| 发布到公开平台后难以撤回 | 检查点 4 由用户决定通过与否；没有 API 时只导出文件（DSGN-H） |
| 视频 API 贵且排队久，用户问过"seedance 的api 这么贵"（18d4bf16，2026-04-19） | 检查点 3 逐个审阅，坏场景单独重做 |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 脚本路径改成 `scripts/` 吗？ | SKILL.md 写 `tools/`，hvg 已没有这个目录 | cicidi | no |
| QUES-B | 项目文件写在哪个仓库？ | SKILL.md 写 `projects/<name>/`；实际数据在 video-gen-initiative | cicidi | no |
| QUES-C | 要不要恢复"问是否要模板"（PRD-N）？ | v3 不提模板，也不问 | cicidi | no |
| QUES-D | Phase 1 遇到音频，要不要调 transcribe-audio？ | SKILL.md 把纯音频记为 gap；transcribe-audio 却说服务于这一步 | cicidi | no |
| QUES-E | 听众 agent 用什么工具"看"视频、"听"音频（PRD-I）？ | SKILL.md 只要求能做到，没写怎么做 | cicidi | no |
| QUES-F | hvg 和 `personal-skills/` 两份，哪份是正本？ | 目前内容相同，没有同步规则 | cicidi | no |

## Reversibility

skill 本身是 git 跟踪的一个文件，用 `git revert` 即可撤回；旧的短视频版可从 hvg commit c440a27 取回。
已发布到 YouTube、抖音等平台的内容，只能到平台上手动删除。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 写出 create-video-workflow 的 design，引用 PRD-A 到 PRD-N |
