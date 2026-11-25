---
feature: create-video-workflow
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# create-video-workflow — 决策记录

本篇按时间倒序记录 `create-video-workflow` 这个 skill 的关键决策。
需求见 [PRD](../prd/create-video-workflow-prd.md)，设计见 [design](../design/create-video-workflow-design.md)。
2026-07-22 之前的决策发生在 hackathon-video-gen 仓库，那里的 commit 号前标"hvg"。会话按 id 前 8 位引用。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-Q | 2026-11-24 | 已不存在的 doc-organize 换成 spec-write |
| ARD-P | 2026-11-24 | Phase 1 遇到音频或带声音的视频，交给 transcribe-audio 转文字 |
| ARD-O | 2026-11-24 | 脚本路径改为 hvg 的 `scripts/`，项目目录改为 video-gen-initiative 的 `projects/` |
| ARD-A | 2026-07-22 | 把 v3 版复制一份到 skill factory 的 `personal-skills/`，项目里的那份照旧 |
| ARD-B | 2026-07-22 | 加 Phase 7 Deploy：验收通过后像 CI/CD 一样发布到各渠道，并写 release notes |
| ARD-C | 2026-07-22 | Phase 0 产出带 Goal 的需求文档；加 Phase 6 听众 agent 验收和第 4 个检查点 |
| ARD-D | 2026-07-22 | 阶段按软件工程划分；Phase 3 产出 transcript 和 spec.json，spec.json 是 Phase 4 的输入 |
| ARD-E | 2026-07-22 | 文档类产出用 doc-organize 定路径和命名；每个检查点都停下等用户说 continue |
| ARD-F | 2026-07-22 | transcript 的语气由发布渠道决定，渠道列表加入公司内部文档 |
| ARD-G | 2026-07-22 | 直接重写已有的 create-video-workflow，不另建一个编排 skill |
| ARD-H | 2026-07-22 | 旧的 Python 生成脚本全部保留，在 Phase 4 和 Phase 5 里调用 |
| ARD-I | 2026-07-22 | 先增强 skill-create，再用它写 v3；v3 因此带三档例子谱 |
| ARD-J | 2026-05-01 | 视频按顺序逐段生成，上一段的尾帧作为下一段的起始图 |
| ARD-K | 2026-04-19 | 视频生成改成后台脚本加 tasks.json 轮询；每个视频一个独立的 project 目录 |
| ARD-L | 2026-04-18 | 视频带配音，不做无声视频 |
| ~~ARD-M~~ | ~~2026-04-18~~ | ~~提供创业故事和搞笑反转两个模板，开头让用户选~~ 已被 [ARD-G](#ard-g) 取代 |
| ~~ARD-N~~ | ~~2026-04-18~~ | ~~5 步加 3 个检查点，把创业故事想法做成 60 秒短视频~~ 已被 [ARD-G](#ard-g) 取代 |

## Evidence Appendix

### ARD-Q

理由：commit c44e983 把 doc-organize 换成 spec-organize 和 spec-write；spec-organize 不是入口 skill。
本条修改了 ARD-E 里 doc-organize 的部分；检查点的规则不变。
被否决的方案：指向 spec-organize。出处：用户 2026-11-24 审阅回复；commit c44e983。

### ARD-P

理由：hvg commit ca6bb23 给 hvg 那份 SKILL.md 加了这段分流，本仓库这份一直没有，音频被记为 gap。
本次照搬 ca6bb23 的写法：音频直接转，视频先用 ffmpeg 抽音轨，没有字幕的 YouTube 先下载音频。
被否决的方案：继续把纯音频记为 gap。出处：用户 2026-11-24 审阅回复；hvg commit ca6bb23。

### ARD-O

理由：hvg commit b805482 把 `tools/` 改名为 `scripts/`；video-gen-initiative commit d000be2 把 `projects/` 从 hvg 移了过去。
hvg 脚本仍按 `<hvg>/projects/<name>/` 拼路径，SKILL.md 要求跑脚本前先问用户怎么接上（QUES-G）。
被否决的方案：保留旧路径；不问用户直接建软链接。出处：用户 2026-11-24 审阅回复；用 ls 和 git log 核对。

### ARD-A

理由：用户看完 v3 后说"直接改claude.md ， skill 也要放到skill factory"（PRD-K）。
被否决的方案：只放在 hackathon-video-gen 项目里。
出处：1de9cb65（2026-07-22）；本仓库 commit c4159a9 与 hvg 8a9bc62 的 SKILL.md 内容完全相同。

### ARD-B

理由：用户说验收成功后"应该有一个cicd pipeline"，部署目标是 YouTube 或抖音的 API（PRD-J）。
被否决的方案：验收后停下，由用户手动发布。出处：1de9cb65（2026-07-22）。
没有 API 时导出文件加手动上传说明，这条兜底由 agent 写入，用户没有逐条确认。

### ARD-C

理由：用户要求"后面还得有一个验收"，模拟第一步的听众写观后感和总结，并和 goal 对照（PRD-I）。
用户同时补充：一开始设计时要有需求文档，里面要有 goal。
被否决的方案：Phase 5 合成完就结束。出处：1de9cb65（2026-07-22）。
偏差时回到哪个阶段的对照表由 agent 写入，用户没有逐条确认。

### ARD-D

理由：用户先要求核对"前面的生成的spec 文档就是phase 4 的输入"，又把阶段对到需求、design、spec、实施、build（PRD-H）。
被否决的方案：沿用旧版的 metadata.json，只描述视频场景。
出处：1de9cb65（2026-07-22）。spec.json 的字段名（unit_id、engine 等）由 agent 写入，用户没有逐条确认。

### ARD-E

理由：用户说生成文档"要使用doc organize skill"，每个文档都要人参与讨论和 review（PRD-G）。
被否决的方案：一路自动生成，最后一次性交给用户。出处：1de9cb65（2026-07-22）。

### ARD-F

理由：agent 起初写成"口语化，结合 YouTube、自媒体等素材"。用户纠正为结合"以后传播的地方"，风格不一样（PRD-C）。
被否决的方案：所有渠道用同一种口语化语气。出处：1de9cb65（2026-07-22）。

### ARD-G

理由：旧版写死了 2 个模板、6 个场景和 30 到 60 秒竖屏，用户要的是"不要定的太死"（PRD-E）。
agent 推荐新建一个叫 research-to-content 的编排 skill，旧 skill 当子程序；用户选择直接改写旧的。
被否决的方案：新建编排 skill；放进 skill factory 而不放在视频项目。出处：1de9cb65（2026-07-22），hvg commit 8a9bc62。
用户在选项框里的原始回答没有存档，只有 agent 的复述，属于 UNKNOWN。

### ARD-H

理由：用户问"原来的 py 是干什么的"，确认"并不是扔掉了"（PRD-E）。
旧脚本负责"怎么做"：生成叙事、场景、图片、视频，轮询任务，拼接视频；新阶段负责"做什么"。
被否决的方案：重写全部生成脚本。出处：1de9cb65（2026-07-22）。

### ARD-I

理由：同一条消息里，用户先要 skill-create 帮作者加例子，写得像法律文书，"不能太宽，也不能太松"。
agent 提议先做这件事，再拿它来写 v3，用户同意；例子谱分轻量、标准、完整三档。
被否决的方案：两件事并行做。出处：1de9cb65（2026-07-22）；v3 的 Example Spectrum 一节。

### ARD-J

理由：用户要求视频一个个生成，前一段最后一个镜头的截图作为下一段的开始，转场写进剧本（PRD-L）。
被否决的方案：各段并行生成，彼此不衔接。出处：会话 5cf6decf（2026-05-01）。
v3 保留了这条：Phase 4 说视频按顺序生成，用尾帧衔接。

### ARD-K

理由：Seedance 是离线任务，用户要求触发后台脚本，把 task id 记进 json 再轮询（PRD-L）。
用户还要求每个视频有单独的 project 目录，每个场景有自己的 metadata（会话 18d4bf16，2026-04-19）。
被否决的方案：让 Claude Code 会话一直等着视频生成。出处：hvg commit c440a27 的 SKILL.md（tasks.json、`projects/<name>/`）。

### ARD-L

理由：hvg commit 49a7aff 的 SKILL.md 写着"this workflow produces silent clips"。用户要求"生成要背景说话的"（PRD-M）。
被否决的方案：只出无声片段。出处：会话 18d4bf16（2026-04-18）；v3 的 spec.json 有 `voiceover` 字段。

### ARD-M

理由：用户说不要绑定在创业者叙事上，把它分析成一个故事模板，再加一个模仿网络节奏的搞笑模板（PRD-N）。
出处：会话 18d4bf16（2026-04-18）；hvg c440a27 的 Step 0 "Pick template"。
被 ARD-G 取代：v3 用灵活大纲代替模板，也不再问用户要不要模板，见 design 的 QUES-C。

### ARD-N

理由：第一版面向不懂技术的创业者，从一个想法做出 60 秒短视频，有 3 个人工审阅点（hvg commit 35b8eda 的说明）。
发起这一版的对话没有找到，属于 UNKNOWN。
被 ARD-G 取代；v3 的 When NOT to Use 仍让已有成稿的短视频走"git 历史里的旧 5 步流程"。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 create-video-workflow 的决策 |
| 2026-11-24 | 新增 ARD-O（路径）、ARD-P（音频分流）、ARD-Q（spec-write） |
