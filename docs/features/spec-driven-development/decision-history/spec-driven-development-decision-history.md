---
feature: spec-driven-development
type: decision-history
state: final
final_date: 2026-09-25
health: active
owner: cicidi
last_verified: 2026-11-24
---

# Spec-Driven Development — Decision History

本文件记录这套方法里所有已经生效的决定。每条决定有一个编号，格式是 `ARD-` 加字母，例如 `ARD-A`、`ARD-BK`。编号一旦写下就不再改，也不再给别的决定用。

怎么读这份文件：

- **Decision Log** 是一张总表，一行一条决定，最新的在最上面。
- **Evidence Appendix** 按同样的顺序，逐条写这条决定的原因、放弃了哪些方案。
- 一条决定被新决定推翻时，旧行不删，而是用删除线划掉，后面链到新决定。这是整套 spec 里唯一使用删除线的地方（[ARD-BM](#ard-bm)）。

术语见 [parent design 附录：术语表](../design/spec-driven-development-design.md#glossary)。

## Decision Log

| ID | Date | Decision |
|---|------|----------|
| ARD-CL | 2026-11-24 | 划掉的 ARD 行一律保留；某篇超过行数上限要压缩时，先压缩已划掉的内容 |
| ARD-CK | 2026-11-24 | 每次运行 `build_spec_skills.py` 都把 parent PRD 的 `version` 末位加 1，再印进 `SKILL.md`；`--check` 不升版本 |
| ARD-CJ | 2026-11-24 | DeepSeek 复核跑 5 次，至少 4 次一致才算定论；Claude 再逐条核对没通过或有分歧的结论，记下同意还是不同意 |
| ARD-CI | 2026-11-24 | spec-review 除三份标准文件外，还读三份审查参考：`CONTENT-PRIORITY.md`、`AUTHORITY-BY-CONCERN.md`、`SPEC-SCOPE.md` |
| ARD-CH | 2026-11-24 | wayfinder 负责进度规则（pipeline design 的 PIPE-A-D、PIPE-A-E、PIPE-A-F、PIPE-H、PIPE-E-A），轻量改写后成为第三个交付物 |
| ARD-CG | 2026-11-24 | CLAUDE 层按顺序找：项目里有 `CLAUDE.local.md` 就写它，没有就写 `CLAUDE.md`，两个都没有就问用户要不要新建 |
| ARD-CF | 2026-11-24 | spec-write 改完 markdown 要告诉用户网页还没更新，问要不要重建；commit 前必须重建，提交的网页和 markdown 一致（TST-R） |
| ARD-CE | 2026-11-24 | 改动上限只管修改已有文件；新建一个文件不算在内 |
| ARD-CD | 2026-11-24 | 网站用 GitHub Pages 发布：推送 master 后由 GitHub Actions 从 markdown 重新生成并部署；每一页都要能从 `index.html` 点到 |
| ~~ARD-CC~~ | 2026-11-24 | ~~parent PRD 的 `version` 是 spec bundle（整套 SDD spec）的版本；`tools/build_spec_skills.py` 把它印进四个 SDD `SKILL.md`，只标来源，不做迁移~~ → [ARD-CK](#ard-ck) |
| ARD-CB | 2026-11-20 | 网页离线可读指正文与已提交的 SVG 插图；字体与 Mermaid 可联网加载（reader PRD 的 PRD-O） |
| ARD-CA | 2026-11-20 | 插图用 diagram-design 画，SVG 与 citing md 同目录；全站配色与 diagram-design 默认一致；spec-review 查图文一致 |
| ARD-BZ | 2026-11-20 | 补记两次编号迁移：parent design 的 §4 到 §8 改为 DSGN-A 到 DSGN-E；reader design 里重号的 DSGN-N-H、DSGN-N-I 改为 DSGN-N-M、DSGN-N-N |
| ARD-BY | 2026-11-20 | reader PRD 的 PRD-L（全站样式统一）降为 NICE，和 reader design 的 DSGN-N-D 一致 |
| ~~ARD-BX~~ | 2026-11-20 | ~~交付物只有 spec-write 和 spec-review 两个 skill。它们读三份标准文件：SPEC-STANDARD.md、SPEC-PRESENTATION.md，以及讲 HTML 页面的 SPEC-HTML-STANDARD.md；标准文件不算交付物~~ → [ARD-CH](#ard-ch) |
| ARD-BW | 2026-11-20 | `raw/` 里的文件可以单独作为证据，即使其他读者打不开；链接检查不把指向 `raw/` 的链接算作死链 |
| ARD-BV | 2026-11-20 | 内容改动由 spec-write 做；格式类 MUST 可以由整理工具的 Lint 模式直接修，同样受 ARD-BP 的改动上限约束 |
| ~~ARD-BU~~ | 2026-11-20 | ~~feature 目录要等人在 Map 阶段确认后才建；Create 阶段只把暂定名记在 CLAUDE.local.md~~ → [ARD-CH](#ard-ch) |
| ~~ARD-BT~~ | 2026-11-20 | ~~重申 ARD-U、ARD-V 里仍然有效的部分：Map 阶段以访谈为主；进度在 feature 名字定之前记在 CLAUDE.local.md，定了以后记在 raw/state/；非软件难题留在本 PRD，用同样五篇文档~~ → [ARD-CH](#ard-ch) |
| ARD-BS | 2026-11-20 | 正文可以中英文混合，只要读着通顺；英文术语第一次出现时要解释，或者收进术语表。Problem Statement 可以保留作者原话，包括原来的编号标题（ARD-AW 的例外，ARD-AW 在本条重述） |
| ARD-BR | 2026-11-20 | pipeline design 的子条款改用字母：PIPE-A1 改为 PIPE-A-A，PIPE-E1 改为 PIPE-E-A，依此类推；pipeline design 里留新旧对照表 |
| ARD-BQ | 2026-11-20 | 六种文档都可以拆分篇；有分篇时必须有入口文件 `<f>-<type>.md`，入口链到各分篇 |
| ~~ARD-BP~~ | 2026-11-20 | ~~AI 每次改 docs/ 下的 .md，必须同时满足：不超过 10 行，并且不超过 200 字符；更大的改动拆成多次，或经人授权后一次大改~~ → [ARD-CE](#ard-ce) |
| ARD-BO | 2026-11-20 | 可读性是通过条件：由 LLM 扮演本科程序员，只读一篇文档和术语表，回答从该篇需求和规则条目里抽出的问题；答错太多，或有第一次出现时没解释的术语，这篇就不通过 |
| ARD-BN | 2026-11-20 | 规则分两级：MUST 是违反后 spec 会出错或丢信息的规则；NICE 是格式偏好。八条纯格式规则降为 NICE |
| ARD-BM | 2026-11-20 | 删除线只用在 decision-history。正文只写现行规则，并链到推翻旧说法的 ARD；正文的旧版本交给 git |
| ARD-BL | 2026-11-20 | 用来打分的 gold 是 iPhone 购买案例。这套 SDD spec 是写法样板，由 spec-review 审查，不用来打分 |
| ~~ARD-BK~~ | 2026-11-20 | ~~本次整理是人明确授权的大改：正文统一为中文，可以大段重写，术语表放在 parent design 附录；单次改动上限在这一批暂停~~ → [ARD-BS](#ard-bs) |
| ~~ARD-BJ~~ | 2026-11-18 | ~~gold spec 就是这套 spec-driven-development，iPhone gold/v1 不是 gold~~ → [ARD-BL](#ard-bl) |
| ARD-BI | 2026-11-18 | 左侧栏显示层级和序号：1 prd、2 decision-history、3 design、4 impl plan、5 test plan、6 how to、10 sub-feature |
| ~~ARD-BH~~ | 2026-11-18 | ~~交付物只有 spec-write 和 spec-review 两个 skill。两份标准文件是这两个 skill 要读的文档，不算交付物~~ → [ARD-BX](#ard-bx) |
| ARD-BG | 2026-11-07 | 全站只有一个网站，入口是 docs/book/html/index.html。进入一个 feature 后，左边是这个 feature 的目录，右边是正文 |
| ARD-BF | 2026-11-07 | spec 的 HTML 放在 docs/book/html/，目录结构和 docs/features/ 一样；markdown 留在 feature 目录 |
| ~~ARD-BE~~ | 2026-11-07 | ~~图只用来画文字说不清的流程，一个流程一张图~~ → [ARD-CA](#ard-ca) |
| ARD-BD | 2026-11-07 | 外部仓库的 gold 只记一份清单（commit 和应找出的问题），不把别人的 spec 原文复制进本仓库 |
| ARD-BC | 2026-11-07 | 引用一个未决问题时写的状态，必须和问题清单里的状态一致 |
| ARD-BB | 2026-11-07 | 问题清单里写的总数和各状态的数量，必须等于实际行数 |
| ARD-BA | 2026-11-07 | 手工维护的 HTML 更新记录，要覆盖 markdown Change Log 里的每个日期 |
| ARD-AZ | 2026-11-07 | 写成「§N」的链接要落在第 N 节或它的上下级；同一文档里的步骤范围不能重叠 |
| ARD-AY | 2026-11-07 | 如果问题清单的每一行都写了负责人和依据，design 可以链到清单，不必再抄一张子问题归属表 |
| ARD-AX | 2026-11-07 | Decision Log 可以多加一列 Ready；Status 列和 Supersedes 列仍然禁止 |
| ~~ARD-AW~~ | 2026-11-07 | ~~必需章节的标题用英文、不编号；专门写有序步骤的章节可以编号~~ → [ARD-BS](#ard-bs) |
| ARD-AV | 2026-11-07 | design 拆成多篇时，13 个必需章节只要求写在入口文件；其他分篇链回入口，只写自己那部分 |
| ARD-AU | 2026-11-07 | 本地翻译副本不提交；副本开头写明以原文为准 |
| ARD-AT | 2026-11-07 | 每个 IMPL 任务写明完成标准；先做读的一侧，再做写的一侧；对方接口还没上线时写一个 mock |
| ARD-AS | 2026-11-07 | 正文推翻旧说法时，链到新的 ARD；删除线只留给 decision-history；错别字可以直接改 |
| ARD-AR | 2026-11-07 | 不变量写成表格，不写成口号 |
| ARD-AQ | 2026-11-07 | design 或 impl-plan 里引用「文件:行号」时，写明是哪个 commit 的 |
| ARD-AP | 2026-11-07 | 编号迁移时保留新旧对照表；标题改名时保留旧锚点 |
| ARD-AO | 2026-11-07 | 每个 feature 只有一份未决问题清单，其他文档链过去；条目编号是 QUES 加字母，写明问题、目前答案、负责人 |
| ARD-AN | 2026-11-07 | 决定的就绪程度可以写在决定正文里；同一行可以原地修订；未决事项按负责人分组 |
| ARD-AM | 2026-11-07 | 步骤编号表示位置，不是永久编号；impl 和 test 引用同一个步骤范围 |
| ARD-AL | 2026-11-07 | frontmatter 可选字段 audience 只能是 internal 或 external |
| ARD-AK | 2026-11-07 | markdown 是全文。手工维护的 HTML 记录源文件和它的 sha256，不一致就算过期；脚本生成的 HTML 直接重新生成 |
| ARD-AJ | 2026-11-07 | 入口 skill 是 spec-write 和 spec-review；标准写在 SPEC-STANDARD.md 和 SPEC-PRESENTATION.md；spec-organize 和 spec-pipeline 不再是入口 |
| ARD-AI | 2026-11-04 | 那一次的 spec 合并是人明确授权的大改，那一批允许超过 10 行的改动 |
| ~~ARD-AH~~ | 2026-11-04 | ~~给人读的 reader 是唯一的 HTML 交付物；旧的摘要 HTML 删除~~ → [ARD-BG](#ard-bg) |
| ARD-AG | 2026-11-04 | 是否收敛由规则自动判断（pipeline design 的 PIPE-E-A 到 PIPE-E-C）：每个未决事项都标明是否阻塞；AI 不能自己宣布「已经够稳」 |
| ~~ARD-AF~~ | 2026-11-04 | ~~故意不定义的事项：失败处理、skill 和 spec 的版本管理、信息来源可信度分级、数据清理；不迁移旧文档~~ → [ARD-CC](#ard-cc) |
| ARD-AE | 2026-11-04 | 非软件问题也用同样的五篇文档；design 里写子问题归属表；结论必须有依据，查不到写 UNKNOWN |
| ~~ARD-AD~~ | 2026-11-04 | ~~评测用 deepseek-flash 独立跑 3 次；gold 由案例、版本、范例、标注四部分组成；跑分结果和报告不提交；四个非软件例子写进 skill 正文，不在本仓库建 gold~~ → [ARD-CJ](#ard-cj) |
| ARD-AC | 2026-11-04 | PRD 的必需章节去掉非功能需求；编号在「feature 加文档类型」内唯一，跨 feature 引用写成 feature/编号；how-to 暂不检查 |
| ~~ARD-AB~~ | 2026-11-04 | ~~交付物是四个 skill：spec-pipeline、spec-organize、spec-review、spec-write~~ → [ARD-AJ](#ard-aj) |
| ARD-AA | 2026-11-04 | 多人的决定互相冲突时，以 decision-history 里时间较晚的为准；看不出先后就问用户；AI 不猜 |
| ARD-Z | 2026-11-04 | PRD 写清限制、偏好、时间、资源、工具五项（没有的写 not apply），并且 design 和 decision-history 都已存在，才能进入下游 |
| ARD-Y | 2026-11-04 | 拆分问题时，AI 给出几种拆法；一个人 20 小时内能搞清楚的算一个 feature spec，超过就拆；估算和判断都由 AI 做 |
| ARD-X | 2026-11-04 | 执行只做到 mock：mock MCP 客户端调用 mock 服务器，打印出调用记录就算成功；不真下单、不真订票 |
| ARD-W | 2026-11-04 | 可读性由 LLM 扮演本科程序员来判断，它读懂了才算通过 |
| ~~ARD-V~~ | 2026-11-04 | ~~非软件难题留在本 PRD，用同样五篇文档，并建四个 gold 例子~~ → [ARD-AD](#ard-ad) |
| ~~ARD-U~~ | 2026-11-03 | ~~交付物是 spec-pipeline 编排 skill；Map 阶段以访谈为主；state 先记在 CLAUDE.local，再记到 raw/state/~~ → [ARD-AJ](#ard-aj) |
| ARD-T | 2026-11-03 | wayfinder-import 不是 SDD 的 sub-feature，它在 features/wayfinder-import/ 下的目录删除 |
| ARD-S | 2026-11-03 | gold 集合可以增长，并且有版本号；分数只在同一版本内比较 |
| ARD-R | 2026-11-03 | 评测有两个分数：MUST 合规分必须满分；对标 gold 的分数不能比上一次低 |
| ARD-Q | 2026-11-03 | 测试放在 skills/<skill>/tests/；跨 skill 的检查器、gold、报告放在 spec-organize 下 |
| ARD-P | 2026-11-03 | spec-review 也要找出机械规则的违反；它只给修改建议，不直接改 |
| ~~ARD-O~~ | 2026-11-03 | ~~skill 是 spec-organize（主）、spec-review、spec-write；标准文件是 spec-organize/SPEC-STANDARD.md~~ → [ARD-AB](#ard-ab) |
| ARD-N | 2026-10-30 | 产品级成功指标的测量方法和基线延后，记在 PRD-G |
| ~~ARD-M~~ | 2026-10-30 | ~~多人决定以谁为准延后，记在 PRD-F~~ → [ARD-AA](#ard-aa) |
| ARD-L | 2026-10-30 | 盲区由现有 skill 来发现，不另造新机制 |
| ~~ARD-K~~ | 2026-10-30 | ~~AI 每次改 docs/ 下的 .md，不超过 10 行或 200 字符；更大的改动拆成多次~~ → [ARD-BP](#ard-bp) |
| ARD-J | 2026-10-30 | 五种必需的文档，外加一种可选的 how-to；how-to 不是每个 feature 都要写 |
| ARD-I | 2026-09-25 | 当时这个 feature 有两份 spec 文档，是对「每种类型一份」规则的有意例外（已成历史，见 ARD-T） |
| ARD-H | 2026-09-25 | 内容分四个优先级；L1 永远不删 |
| ARD-G | 2026-09-25 | design 分篇用名词命名，impl-plan 分篇用「序号加阶段」命名 |
| ~~ARD-F~~ | 2026-09-25 | ~~一个 feature 目录可以有多份 design 或 impl-plan~~ → [ARD-BQ](#ard-bq) |
| ARD-E | 2026-09-25 | design 和 impl-plan 最多 1,000 行；decision-history 不设上限 |
| ARD-D | 2026-09-25 | 文档健康状况的字段叫 health，不叫 status |
| ARD-C | 2026-09-25 | 细节写在 skill 目录里的其他文件，不全部塞进 SKILL.md |
| ARD-B | 2026-09-25 | 标准放在已有的 skill 里（当时叫 doc-organize，后改名 spec-organize，见 ARD-O），不新建 skill |
| ARD-A | 2026-09-25 | 按关注点分权威，取代「全局只有一个真相来源」 |

## Evidence Appendix

<a id="ard-cl"></a>

### ARD-CL — 划掉的内容保留，压缩时先压它

**原因。** 划掉的 ARD 行说明一条规则为什么变了，删掉就查不到来龙去脉。ARD-BE 划掉后剩下的两句也一样保留。

**规则。** 划掉的行和它的 Evidence Appendix 一律保留。某篇文档超过行数上限、必须压缩时，先压缩已划掉的内容（例如合成一行并链到新 ARD），再动别的；L1 内容仍不能删。

**放弃的方案。** 定期清理划掉的行：会丢掉历史。

<a id="ard-ck"></a>

### ARD-CK — 每次 build 升版本号

**原因。** ARD-CC 只说印版本号，没说什么时候升。印戳的是五个 `SKILL.md`：spec-write、spec-review、wayfinder、spec-organize、spec-pipeline。版本不升，两次不同的 build 印出同一个号，起不到标来源的作用。

**规则。** 每次运行 `build_spec_skills.py`（不带 `--check`），先把 parent PRD 的 `version` 末位加 1，例如 `1.0.0` 变成 `1.0.1`，再印进 `SKILL.md`。`--check` 只比对，不升版本。

**重述。** 本条推翻 ARD-CC 里放弃「自动升版」的部分，ARD-CC 因此划掉。其余仍有效：版本号只写在 parent PRD 的 `version`；脚本写入版本、日期、git 短 sha，拒绝重复键（TST-Y）；失败处理、信息来源可信度分级、数据清理、迁移策略故意不定义，旧文档不迁移（ARD-AF 经 ARD-CC 的重述）。

**放弃的方案。** 每次由人决定升哪一位：每次都要人判断，容易忘。

<a id="ard-cj"></a>

### ARD-CJ — 复核跑 5 次，Claude 再核对

**原因。** 2026-11-24 夜里，MUST-B 在相关内容没变的情况下出现过一次 2 比 1 的翻转，说明 3 次太少。DeepSeek 的结论本身也可能错。

**规则。** `judge_deepseek.py` 默认跑 5 次：至少 4 次通过算通过，至少 4 次不通过算不通过，其余算有分歧，按不通过计。

**规则（续）。** Claude 逐条核对不通过和有分歧的结论，把同意或不同意及理由写进 `claude_audit`。Claude 不同意时报告用户，不自己改判；Python 检查的结果仍不能推翻。

**范围。** 本条管 `judge_deepseek.py` 的复核（TST-L）。TST-V 的可读性判分另有门槛，不变。Claude 不同意的条目在用户决定前仍算没通过。

**重述。** 本条推翻 ARD-AD「复核跑 3 次」的部分，ARD-AD 因此划掉。其余仍有效：生成 gold 跑 3 次；gold 由案例、版本、范例、标注组成；跑分结果和报告不提交（复核结论文件 `judgments/` 例外，要提交，测试靠它判断结论过没过期）；四个非软件例子写进 skill 正文，不在本仓库建 gold；只有 DeepSeek 的 API，不同模型之间的偏差标为 Unverified。

**规则（补）。** 重跑时，题目、结论、票数分布和语料 sha 都没变的条目，保留上次的 `claude_audit`；有任何一项变了就清空，等 Claude 重新核对。

**放弃的方案。** 5 次都一致才通过：次数越多越容易因一次波动失败。换更贵的模型：仍是一个模型说了算。

<a id="ard-ci"></a>

### ARD-CI — spec-review 的三份审查参考

**原因。** 契约说 skill 只读三份标准文件，spec-review 的正文却还加载另外三份，两处说法不一致。

**规则。** spec-review 另读三份审查参考：`CONTENT-PRIORITY.md`（哪些是 L1 必有内容）、`AUTHORITY-BY-CONCERN.md`（每件事以哪篇为准）、`SPEC-SCOPE.md`（design 不写实现细节）。

它们支撑审查里的具体检查，不是写作标准，spec-write 不必读。

**放弃的方案。** 并进 SPEC-STANDARD.md：标准文件变长，写作时又用不到。

<a id="ard-ch"></a>

### ARD-CH — wayfinder 负责进度规则

**原因。** spec-pipeline 不再是入口 skill 以后，pipeline design 的 PIPE-A-D、PIPE-A-E、PIPE-A-F、PIPE-H、PIPE-E-A 没有 skill 负责。

另外，名字没定时进度全记在 `CLAUDE.local.md` 一处，几个 feature 同时进行就会互相覆盖。名字没定时的暂定名、粗略 PRD 和背景也一起移进地图文件。

**规则。** wayfinder 的地图目录就是进度记录：`map.md` 加 `issues/` 下每个 brief 一个文件。名字没定时放在 `docs/state/wayfinder-<暂定名>/`，定了以后整个移到 `docs/features/<f>/raw/state/wayfinder/`，都不提交。

每个 feature 一个地图目录，互不覆盖；任务再小也建地图。CLAUDE 层只记当前地图的路径（ARD-CG）。

**规则（续）。** 重新开始时读地图给出回顾。阻塞与否以 design 的问题清单（QUES-*）为准，有标「是」的没解决就不进入 Downstream；处理它的 brief 写明 QUES 编号。提交前问要不要跑 spec-review，用户说不跑就记进地图。

**重述。** 本条推翻 ARD-BX「交付物只有两个」，以及 ARD-BT、ARD-BU「进度记在 CLAUDE.local.md」的部分，三条因此划掉。

仍有效的部分：spec-write、spec-review 读三份标准文件，标准文件不算交付物；Map 以访谈为主；非软件难题留在本 PRD；人在 Map 确认名字后才建 feature 目录；spec-organize 和 spec-pipeline 不是交付物。

**放弃的方案。** 交给 spec-write：正文变重，名字没定时的冲突还要另想办法。先标 Unverified：规则一直没人执行。改写 wayfinder 会和上游 mattpocock/skills 分叉，接受这个代价。

<a id="ard-cg"></a>

### ARD-CG — CLAUDE 层写在哪个文件

**原因。** DSGN-C 要求规范也写进 CLAUDE 层，但本仓库没有 `CLAUDE.md`，只有不提交的 `CLAUDE.local.md`。

**规则。** 按顺序找：项目里有 `CLAUDE.local.md` 就写它；没有就写 `CLAUDE.md`；两个都没有，问用户要不要新建，不自己建。

**放弃的方案。** 一律新建 `CLAUDE.md`：会把个人设置提交进仓库。

<a id="ard-cf"></a>

### ARD-CF — 网页什么时候重建

**原因。** TST-R 要求提交的网页和 markdown 一致，spec-write 却规定用户要求时才重建，两条冲突。

**规则。** spec-write 改完 markdown，告诉用户哪些网页还没更新，问要不要现在重建。commit 前必须重建，让提交的网页和 markdown 一致；推送 master 后 CI 再重建并部署（ARD-CD）。

**放弃的方案。** 不再提交 HTML、只靠 CI 生成：在本地分支上就看不到网页。

<a id="ard-ce"></a>

### ARD-CE — 新建文件不受改动上限限制

**原因。** 上限是为了让每次修改都看得清（ARD-BP）。新建的文件没有旧内容可对比，拆成十几次只多出步骤。

**规则。** 上限只管修改已有文件。新建一个文件可以一次写完，但仍要符合行数上限（PRD-D）。从已有文件挪出内容另建分篇，算修改，不算新建。

**重述。** 本条推翻 ARD-BP 没区分新建和修改的部分，ARD-BP 因此划掉。其余仍有效：修改 `docs/` 下已有的 markdown，每次不超过 10 行并且不超过 200 字符；更大的改动拆开，或经人授权。

**放弃的方案。** 新建文件也按 10 行拆：步骤多，看不出好处。

<a id="ard-cd"></a>

### ARD-CD — 用 GitHub Pages 发布网站

**原因。** 网站只在本地能看；还有 6 个旧页面从首页点不到，读者找不到也不知道它们过期了。

**规则。** 只从 master 部署。CI 先运行 `build_sdd_site.py` 和 `build_sdd_reader.py`，再用 `check_site_reachable.py` 确认每页都能从首页点到（TST-Z）。从首页点不到的旧页面删掉。

**放弃的方案。** 直接发布已提交的 HTML（忘了重建就发布旧页面）；工作分支也部署（会互相覆盖线上版本）。

<a id="ard-cc"></a>

### ARD-CC — spec bundle 版本戳

**原因。** skill 正文由 spec 提炼；spec 改了以后，看不出手上的 skill 对应哪一版 spec。

**规则。** 版本号只写在 parent PRD 的 `version`。脚本把版本、日期、git 短 sha 写进 `SKILL.md`；`--check` 比对版本、拒绝重复键（TST-Y）。迁移策略仍不定义。

本条推翻 ARD-AF 里「不定义版本」的部分，ARD-AF 因此划掉，其余在此重述：失败处理、信息来源可信度分级、数据清理、迁移策略故意不定义；不迁移旧文档。

**放弃的方案。** 每个 `SKILL.md` 手写版本号；按 semver 自动升版。

<a id="ard-cb"></a>

### ARD-CB — 离线可读范围

**原因。** 插图内嵌进网页后，如果 reader PRD 的 PRD-O「直接打开就能读」要求完全不联网，字体和 Mermaid（把文字描述画成流程图的脚本）就加载不了。

**规则。** MUST：断网时正文和 SVG 插图能读；字体和 Mermaid 可以从网上加载。

**放弃的方案。** 全站严格零联网（与 Mermaid、字体策略冲突）。

<a id="ard-ca"></a>

### ARD-CA — 插图与站点样式

**原因。** 只有文字的 spec 难读；Mermaid 自动排的版不像人精心画的图；构建网页时再让 AI 画图，每次结果都不一样。

**规则。** 写 spec 时用 diagram-design 画 SVG，文件名 `<文档名>-fig-<主题>.svg`，放在引用它的 md 旁边；网页配色用 diagram-design 的默认颜色；图里有正文没有的内容或与正文矛盾，spec-review 报 severity 3。

**重述。** 本条推翻 ARD-BE「图只画流程、状态用表格不用图」的部分，SPEC-PRESENTATION 列的形状都可以画图。其余仍有效：图不能出现正文里没写的事实（MUST，见上面的规则）；步骤数和所在章节一致（NICE，ARD-BN）。另加 NICE：一张图不超过 9 个节点、12 条边。

**放弃的方案。** 仅在 build 时让 AI 重画；只把配色套在 Mermaid 上。

<a id="ard-bz"></a>

### ARD-BZ — 补记两次编号迁移

**原因。** document-standard 的 DSGN-F 规定：确实要改编号时，要记一条 ARD。2026-11-20 有两次改编号只引用了通用规则 ARD-AP，没有自己的 ARD。

**规则。** parent design 的规则小节 §4 到 §8 改为 DSGN-A 到 DSGN-E，因为编号不能用纯数字。reader design 里 Implementation Decisions 表的 DSGN-N-H、DSGN-N-I 和同名小节重号，表里的改为 DSGN-N-M、DSGN-N-N。两处的对照表都留在原文件里。

<a id="ard-by"></a>

### ARD-BY — 全站样式统一降为 NICE

**原因。** reader PRD 的 PRD-L 把全站样式统一写成功能需求，reader design 的 DSGN-N-D 却标为 NICE，两处不一致。

**规则。** 人选择降级：PRD-L 改为 NICE。样式不统一时只提醒，不算失败。页面能不能读懂由其他 MUST 保证（编号可见、标题层级可分、不在运行时读 `.md`）。

**放弃的方案。** 改回 MUST：样式统一很难用脚本判定，容易误报。

<a id="ard-bx"></a>

### ARD-BX — 标准文件是三份

**原因。** parent design、skill 契约和 PRD 只列了两份标准文件，但 reader design 和 spec-write 的 SKILL.md 还读第三份 `skills/spec-html-standard/SPEC-HTML-STANDARD.md`。spec-review 要审 HTML 页面，也需要这一份。

**规则。** 两个 skill 读三份标准文件：`SPEC-STANDARD.md` 讲路径、权限、写什么和证据；`SPEC-PRESENTATION.md` 讲文字、格式和表格；`SPEC-HTML-STANDARD.md` 讲 HTML 页面。ARD-AJ 说标准写在 SPEC-STANDARD.md 和 SPEC-PRESENTATION.md，这仍然成立，本条只是加上第三份，不推翻 ARD-AJ。推翻 ARD-BH 里「两份标准文件」的说法；ARD-BH 其余部分仍然有效，在此重述：交付物只有 spec-write 和 spec-review 两个 skill；三份标准文件是它们的输入，不算交付物；spec-organize 和 spec-pipeline 也不是交付物。

**放弃的方案。** 把 HTML 规则并进 SPEC-PRESENTATION.md：要改非 spec 文件，而且 markdown 和 HTML 的规则混在一起不好找。

<a id="ard-bw"></a>

### ARD-BW — raw/ 文件可以单独作为证据

**原因。** `raw/` 不提交，别人点开是死链；但 pipeline design 的 PIPE-L、SPEC-STANDARD 和 ARD-AE 都接受 `raw/` 路径作证据。规则互相矛盾。

**规则。** 人选择接受：结论写进正式文档，证据可以只是一个 `raw/` 路径，即使其他读者打不开。链接检查不把指向 `raw/` 的链接算作死链。

**放弃的方案。** 证据必须有 URL、ARD 或 commit，`raw/` 只能作额外指引：更严谨，但调研阶段的大量笔记就没法引用。

<a id="ard-bv"></a>

### ARD-BV — 格式修正可以由 Lint 直接做

**原因。** pipeline design 的 PIPE-A-C 说所有修改都由 spec-write 做；但 document-standard 的 DSGN-L、skill 契约和 ARD-P 都允许整理工具直接修格式问题。

**规则。** 内容的增删改由 spec-write 做。格式类 MUST（例如标题写法、frontmatter 字段）可以由整理工具的 Lint 模式直接修。两者都受 ARD-BP 的改动上限约束。

**放弃的方案。** Lint 只报告不改：每个小格式问题都要绕一次 spec-write，太慢。

<a id="ard-bu"></a>

### ARD-BU — 人确认后才建 feature 目录

**原因。** pipeline design 里，Create 阶段（PIPE-C、PIPE-G）说要用 feature create 命令建目录，但 PIPE-D 和 Implementation Decisions 说人在 Map 阶段确认后才建。Map 在 Create 之后，两者矛盾。

**规则。** Create 阶段只把暂定的 feature 名字和进度记在 `CLAUDE.local.md`（ARD-BT）。人在 Map 阶段确认拆法和名字之后，才用 feature create 命令建 `docs/features/<f>/`。

**放弃的方案。** Create 就建目录：名字还没定就建，事后改名会留下死链。

<a id="ard-bt"></a>

### ARD-BT — 重申 ARD-U、ARD-V 仍然有效的部分

**原因。** ARD-U 和 ARD-V 在日志里整行被划掉，但它们只有一部分被推翻：ARD-U 被推翻的是「spec-pipeline 是入口」，ARD-V 被推翻的是「为四个例子建 gold」。剩下的部分仍是现行规则（PRD-J、pipeline design 的 PIPE-D、PIPE-H、PRD-K），却挂在已划掉的决定上，读者会以为这些规则也作废了。

**规则。** 下面三条仍然有效，以本条为准：Map 阶段以访谈为主，产出由 AI 判断；进度在 feature 名字定之前记在 `CLAUDE.local.md`，定了以后记在 `docs/features/<f>/raw/state/`；非软件难题留在本 PRD，用同样五篇文档。

<a id="ard-bs"></a>

### ARD-BS — 可以中英文混合；Problem Statement 保留原话

**原因。** ARD-BK 要求正文统一为中文。审查时发现 PRD 的 Problem Statement 是作者原话，中英文混写，标题带 1 到 5 的编号。人决定保留原样：读着通顺比形式统一更重要。

**规则。** 正文可以中英文混合，只要读着通顺。英文术语第一次出现时要解释，或者收进术语表。Problem Statement 可以保留作者原话，包括原来的编号标题。推翻 ARD-BK 里「正文统一为中文」的说法。ARD-BK 其余部分仍然有效，在此重述：2026-11-20 这次整理是人明确授权的大改，可以大段重写；术语表放在 parent design 附录；单次改动上限在这一批暂停。

本条也给 ARD-AW 加了一个例外，ARD-AW 因此划掉，在此重述：必需章节（`##` 级）的标题用英文、不编号；其他章节只有写有序步骤时才编号；例外是 Problem Statement 下面作者原话的小标题可以保留编号。

<a id="ard-br"></a>

### ARD-BR — pipeline 子条款改用字母

**原因。** document-standard 的 DSGN-F 规定编号后面只用字母，但 pipeline design 的子条款用了数字（PIPE-A1、PIPE-E1）。人选择改名，不开例外。

**规则。** PIPE-A1 到 PIPE-A6 改为 PIPE-A-A 到 PIPE-A-F；PIPE-E1 到 PIPE-E3 改为 PIPE-E-A 到 PIPE-E-C；PIPE-F1、PIPE-F2 改为 PIPE-F-A、PIPE-F-B。新旧对照表在 pipeline design 的 Further Notes（ARD-AP）。

**放弃的方案。** 记一条例外，允许子条款用数字：改动最小，但标准里就多了一条特例。

<a id="ard-bq"></a>

### ARD-BQ — 六种文档都可以拆分篇

**原因。** ARD-F 只允许 design 和 impl-plan 拆分篇，理由是其他四种不会无限变长。但后来 document-standard 的 DSGN-B 给六种文档都定了分篇的命名规则，DSGN-J 也允许 decision-history 拆分篇，document-standard 还已经有一个 PRD 分篇（reader PRD）。规则和实际做法都已经超出了 ARD-F。

**规则。** 六种文档都可以拆分篇。有分篇时，必须有入口文件 `<f>-<type>.md`，入口文件链到各分篇。document-standard 因此补上入口文件 `document-standard-prd.md`。推翻 ARD-F。

**放弃的方案。** 维持 ARD-F、收紧 DSGN-B：reader PRD 会变成违规文件，又不能随意改名。允许只有分篇、没有入口：读者不知道从哪篇开始读。

<a id="ard-bp"></a>

### ARD-BP — 改动上限两条都要满足

**原因。** ARD-K 写的是「10 行或 200 字符，满足其一即可」。按字面理解，一行 5,000 个字符的改动也算合规，这违背了「小步改、每步能看清」的本意。

**规则。** AI 每次改 `docs/` 下的 markdown，必须同时满足两条：不超过 10 行，并且不超过 200 字符。更大的改动拆成多次；确实需要一次大改，要人明确授权并记一条 ARD。推翻 ARD-K 里「满足其一即可」的部分，ARD-K 其余内容由本条完整重述。

<a id="ard-bo"></a>

### ARD-BO — 可读性是通过条件

**原因。** PRD-M 把可读性定为硬需求，却又写「不作为通过条件」，等于没有要求。这套方法要解决的问题之一就是「人读不过来」（PRD Problem Statement 第 4 点），可读性必须能挡住交付。

**怎么判。** 一个 LLM 扮演本科程序员，只读被测的那一篇和 parent design 的术语表（本行在 2026-11-20 原地修订，加上术语表，和 PRD-M、TST-V 一致；ARD-AN 允许原地修订）。脚本从这篇的编号条目（`PRD-*`、`DSGN-*`、`PIPE-*`、`IMPL-*`、`TST-*`、`ARD-*`）各出一道题，例如「PRD-F 规定多人决定冲突时怎么办」。再出一组对照题：不给文档直接问，能答对的题说明太容易，作废。答对率不足，或者有第一次出现时没有解释、术语表里也没有的词，这篇就不通过。具体门槛写在 test-plan 的 TST-V。

**放弃的方案。** 只让 LLM 打一个「好不好读」的分：主观，同一篇文档两次打分可能差很多。用句长、词频这类可读性公式打分：看不出术语有没有解释。ISO 24495-1（简明语言标准）讲的是原则和真实读者测试，不是公式；TST-V 让模型扮演读者答题，借的正是这个思路。

**影响。** 修改 PRD-M；ARD-W 的「读懂才算通过」保留，并补上具体做法。

<a id="ard-bn"></a>

### ARD-BN — 规则分 MUST 和 NICE 两级

**原因。** 2026-11-07 一天加了二十多条格式规则。作者为了逐条满足，只好把句子压成关键词和编号，文档越来越像给机器读的。规则越多，越没人读得完。

**怎么分。** MUST 是违反后 spec 会写错、会丢信息、会互相矛盾的规则。NICE 是格式上的偏好，spec-review 可以提，但不算失败。下面八条降为 NICE：

| 决定 | 内容 | 为什么只是偏好 |
|---|---|---|
| ARD-AL 的后半句 | 每节写明哪份文档对这些事实有权威 | 「一个事实只写一处」已经是 MUST，这句是额外的标注 |
| ARD-AM | 步骤编号是位置，不是永久编号 | 只影响引用方式 |
| ARD-AN | 就绪程度、原地修订、按负责人分组 | 都是允许怎么写，不是必须怎么写 |
| ARD-AR | 不变量写成表格 | 写成清楚的句子也不会错 |
| ARD-AZ | §N 链接落点、步骤范围不重叠 | 链接打不开已经由 ARD-AP 管 |
| ARD-BA | HTML 更新记录覆盖每个日期 | HTML 是派生物 |
| ARD-BB | 问题清单的数量统计 | 数错一个数不影响规则本身 |
| ARD-BE | 图的规则 | 画法偏好 |

ARD-AX 和 ARD-AY 本来就是「允许」，不是要求，不受影响。其他规则保持 MUST。

**放弃的方案。** 全部保留、只改写法：规则数量不变，作者负担不变。全部删掉：会丢掉其中有用的写法建议。

<a id="ard-bm"></a>

### ARD-BM — 删除线只用在 decision-history

**原因。** 2026-11-18 在 document-standard 的 DSGN-F 加了一条「改正文时不删旧句，划掉后在旁边写新句」。几轮下来，test-plan 的资产表一个格子里有三处删除线，读者分不清哪句是现行规则。这条规则还和 ARD-AS（删除线只留给 decision-history）直接矛盾。

**规则。** 正文只写现行规则。推翻旧说法时，在新句后面链到对应的 ARD。旧版本可以从 git 历史和 decision-history 里找到。错别字直接改。本决定重申 ARD-AS，撤销 2026-11-18 那条规则。

**放弃的方案。** 保留正文删除线：历史已经有 decision-history 和 git 两处记录，正文再记一次是重复，而且越积越难读。

<a id="ard-bl"></a>

### ARD-BL — 打分用的 gold 是 iPhone 案例

**原因。** 评测的做法是：给 skill 同一份需求和背景资料，看它写出的 spec 和 gold 有多接近。ARD-BJ 把这套 SDD spec 定为 gold，但它没有对应的「输入需求」，skill 无从生成它，所以没法打分。如果拿 skill 去审 gold 本身，又成了自己考自己：改 gold 就能提高分数。

**规则。** 打分用的 gold 是 iPhone 购买案例 `skills/spec-organize/tests/gold/v1/`：有需求 `requirement.md`、背景资料 `context.md`、范例 `exemplar/` 和标注 `annotations.yaml`。这套 SDD spec 是写法样板：spec-review 拿它当审查对象，找出它不满足自己标准的地方，但它不参与打分。推翻 ARD-BJ。

**放弃的方案。** 保留 ARD-BJ 并补写一份输入需求：需求是事后补的，等于按答案出题。四个非软件例子各建一个 gold：ARD-AD 已决定这四个例子不在本仓库建 gold。

<a id="ard-bk"></a>

### ARD-BK — 本次整理是授权的大改

人在 2026-11-20 明确授权这一批整理：正文统一改成中文（必需章节标题和编号仍是英文，见 document-standard 的 DSGN-E；后来 [ARD-BS](#ard-bs) 放宽为允许中英文混合）；可以大段重写，但要保留原意；缩写和术语集中解释在 [parent design 附录](../design/spec-driven-development-design.md#glossary)。这一批暂停「每次不超过 10 行或 200 字符」的上限（ARD-K），这一批结束后恢复。做法和 ARD-AI 相同。

<a id="ard-bj"></a>

### ARD-BJ — gold spec 就是这套 spec（已被 ARD-BL 推翻）

当时的想法是：这套 spec 本身就是写得最好的样板，评测通过就意味着写出了这样的 spec。后来发现它没有输入需求，无法用来打分，见 [ARD-BL](#ard-bl)。

<a id="ard-bi"></a><a id="ard-bi--left-sidebar-numbers-and-hierarchy"></a>

### ARD-BI — 左侧栏的序号和层级

左侧栏按层级排列，序号可见：1 prd、2 decision-history、3 design、4 impl plan、5 test plan、6 how to。sub-feature 不放在 design 下面，而是单独一组，编号 10，每个 sub-feature 在这组下展开。design 的分篇和 reader 放在 3 design 下面。pipeline 在左侧目录里没有单独的页面，它的内容收在 reader 汇编页里。原因：读者先按顺序读 prd、决定、design，序号让顺序一眼可见。

<a id="ard-bh"></a><a id="ard-bh--deliverable-is-only-spec-write-and-spec-review"></a>

### ARD-BH — 交付物只有 spec-write 和 spec-review

对外交付的只有两个 skill：spec-write 负责写，spec-review 负责审。`SPEC-STANDARD.md` 和 `SPEC-PRESENTATION.md` 是这两个 skill 要读的文件，不单独算交付物。spec-organize 和 spec-pipeline 也不在交付物里。ARD-AJ 只说了标准写在哪里，没说它们算不算交付物；本条补上这一点。标准文件后来增加到三份，见 [ARD-BX](#ard-bx)。原因：使用者只调用 skill；标准文件单独交付没有用处。

<a id="ard-bg"></a>

### ARD-BG — 全站一个网站，左边是目录

`docs/book/html/index.html` 列出所有 feature。每篇 spec 的 HTML 是目录里的一行。打开一个 feature，左边是这个 feature 的目录，右边是正文。原因：读者要在多篇文档之间来回跳，一个网站比一堆独立的 HTML 文件好找。推翻 ARD-AH 的「reader 是唯一的 HTML 交付物」：现在 reader 是网站里的一页。ARD-AH 里「旧的摘要页删除」已经执行，仍然有效。

<a id="ard-bf"></a>

### ARD-BF — spec 的 HTML 放在 book 下

`docs/book/html/` 的目录结构和 `docs/features/` 一样。parent 的汇编页是 `docs/book/html/<parent>/<parent>-reader.html`；其他 spec 的 HTML 用相同的相对路径，只把扩展名换成 `.html`。markdown 留在 `docs/features/`。原因：HTML 和 markdown 混在一起，容易被误当成权威文件。

<a id="ard-be"></a>

### ARD-BE — 图只画流程

一个流程一张图。图里的步骤数要和它所在章节写的步骤范围一致。状态用表格写，不用图。图不能出现文字里没写的事实。原因：图里多出来的事实没人维护，很快就和文字不一致。按 [ARD-BN](#ard-bn) 降为 NICE。

<a id="ard-bd"></a>

### ARD-BD — 外部 gold 只留清单

清单记录：源仓库路径、有问题的那个 commit、修好后的 commit、应该找出的问题、允许漏掉的问题。别人的 spec 原文不复制进本仓库。原因：那些 spec 不是公开的。

<a id="ard-bc"></a>

### ARD-BC — 引用处的状态与问题清单一致

在正文里提到某个 QUES 时，旁边写的「未决」或「已决」必须和问题清单里一致。原因：清单里已经关闭的问题，正文还说它未决，读者会被误导。

<a id="ard-bb"></a>

### ARD-BB — 问题清单的数量要对得上

清单里写「共 N 个问题」，N 必须等于实际行数；按状态统计的数量也一样。按 [ARD-BN](#ard-bn) 降为 NICE。

<a id="ard-ba"></a>

### ARD-BA — HTML 更新记录覆盖每个日期

手工维护的 reader 页面，它的更新记录要包含 markdown Change Log 里的每一个日期。按 [ARD-BN](#ard-bn) 降为 NICE。

<a id="ard-az"></a>

### ARD-AZ — 章节链接和步骤范围

写成「§N」的链接要落在第 N 节，或它的上一级、下一级。同一文档里的步骤范围不能重叠。按 [ARD-BN](#ard-bn) 降为 NICE。

<a id="ard-ay"></a>

### ARD-AY — 问题清单可以代替子问题归属表

如果每个子问题都已经是问题清单里的一行，并且每行都写了负责人和依据，design 可以只放一个链接，不必再抄一张归属表。原因：同一件事记两处，迟早不一致。

<a id="ard-ax"></a>

### ARD-AX — 可以加 Ready 列

Decision Log 可以加第四列 Ready，表示这条决定是否已经可以执行。仍然不能加 Status 列和 Supersedes 列：状态写在正文里，推翻关系用删除线加链接表示。

<a id="ard-aw"></a>

### ARD-AW — 只有步骤类章节可以编号

必需章节的标题用标准规定的英文原文，不加编号。专门写一串有序步骤的章节可以编号。原因：检查脚本按标题原文找必需章节；编号会让标题对不上。

<a id="ard-av"></a>

### ARD-AV — 必需章节只写在入口文件

design 拆成多篇时，13 个必需章节只要求写在入口文件 `<f>-design.md`。其他分篇在开头链回入口，只写自己负责的那部分。原因：每个分篇都写 13 节，大部分会是空话。

<a id="ard-au"></a>

### ARD-AU — 翻译副本只放本地

`<name>.<lang>.md` 这样的翻译副本不提交。副本开头写明以 `<name>.md` 为准。副本里的标题可以翻译。原因：提交的翻译副本会和原文慢慢不一致，又没人负责同步。

<a id="ard-at"></a>

### ARD-AT — 完成标准、顺序、mock

每个 `IMPL-*` 写明完成标准。先做只读的部分，再做会写入的部分。对方的接口还没上线时，先写一个 mock 代替。原因：没有完成标准的任务不知道什么时候算做完；先写后读容易把数据写坏。

<a id="ard-as"></a>

### ARD-AS — 正文推翻旧说法时链到新 ARD

正文不再成立的句子直接改写，并链到推翻它的 ARD。删除线只留给 decision-history。错别字直接改。[ARD-BM](#ard-bm) 重申了这条。

<a id="ard-ar"></a>

### ARD-AR — 不变量写成表格

不变量是「任何时候都必须成立的事」。把它写成表格：哪些记录必须存在，或者哪些状态绝不能出现，各由谁来保证。原因：一句口号没法检查。按 [ARD-BN](#ard-bn) 降为 NICE。

<a id="ard-aq"></a>

### ARD-AQ — 引用代码时写明 commit

design 或 impl-plan 里写「某文件第几行」时，同时写明是哪个 commit 的。原因：代码会变，行号会移动；不写 commit，以后没人知道当时指的是哪一行。

<a id="ard-ap"></a>

### ARD-AP — 保留旧锚点

编号迁移时，保留一张新旧编号对照表。标题改名时，把旧的锚点留在新标题上方。原因：其他文档里的旧链接不会因此失效。

<a id="ard-ao"></a>

### ARD-AO — 每个 feature 一份问题清单

很多文档都提到同一批问题时，只在一处列出，其他文档链过去。每个条目编号是 `QUES-` 加字母，写明问题、目前答案、负责人。原因：同一个问题记在三处，关掉一处另外两处还开着。

<a id="ard-an"></a>

### ARD-AN — 就绪程度和原地修订

一条决定可以写「这边已经定了，在等另一个团队」。同一行的措辞可以原地修订。未决事项按负责人分组。按 [ARD-BN](#ard-bn) 降为 NICE。

<a id="ard-am"></a>

### ARD-AM — 步骤编号只是位置

步骤编号表示它在流程里的位置，不是永久编号。插入一步时，这一节和引用它的地方一起重新编号。按 [ARD-BN](#ard-bn) 降为 NICE。

<a id="ard-al"></a>

### ARD-AL — audience 字段

frontmatter 的 `audience` 可以是 `internal` 或 `external`。不写不算错，所以已有文档不受影响；写了其他值就算错。原来的后半句「每节写明哪份文档对这些事实有权威」按 [ARD-BN](#ard-bn) 降为 NICE。

<a id="ard-ak"></a>

### ARD-AK — markdown 是全文

脚本生成的 reader 每次从 markdown 重新生成。手工维护的 HTML 要在页面里写明源文件路径和源文件的 sha256；源文件变了而 HTML 没变，检查就会报「过期」。原因：HTML 是给人读的副本，不能比 markdown 旧。

<a id="ard-aj"></a><a id="ard-aj--entry-skills-are-spec-write-and-spec-review"></a>

### ARD-AJ — 入口 skill 是 spec-write 和 spec-review

使用者从 spec-write 和 spec-review 进入。路径、权限、写什么、证据这些规则写在 `skills/spec-organize/SPEC-STANDARD.md`；文字、格式、表格这些表达规则写在 `skills/spec-html-standard/SPEC-PRESENTATION.md`。spec-organize 和 spec-pipeline 不再是入口。推翻 ARD-AB。原因：四个 skill 让使用者不知道该从哪个开始；写和审两个动作已经覆盖全部场景。

<a id="ard-ai"></a>

### ARD-AI — 那一次合并是授权的大改

人明确授权了一次性合并 SDD 的 spec 文档。那一批允许超过 10 行或 200 字符的改动，之后恢复上限。

<a id="ard-ah"></a>

### ARD-AH — reader 是唯一的 HTML 交付物（已被 ARD-BG 推翻）

`spec-driven-development-reader.html` 是给人读的交付物。旧的摘要页 `spec-driven-development.html` 删除，原来指向它的链接改指 reader。后来改成全站一个网站，reader 是其中一页，见 [ARD-BG](#ard-bg)。

<a id="ard-ag"></a>

### ARD-AG — 收敛由规则判断

pipeline design 的 PIPE-E-A 到 PIPE-E-C（收敛条件）自动检查。每个未决事项都要标明是否阻塞（写在问题清单的「阻塞」列）。只要还有阻塞的事项，就不能进入下游。原因：让 AI 自己判断「够稳了」，它总会说够稳了。

<a id="ard-af"></a>

### ARD-AF — 故意不定义的事项

失败处理、skill 和 spec 的版本管理、信息来源可信度分级、数据清理，都故意不定义。已有的不合规 feature 不迁移，只修 SDD 自己这套文档。原因：先把核心流程做对，这些事项等有真实需求再定。

<a id="ard-ae"></a>

### ARD-AE — 非软件问题的对应关系、归属和证据

非软件问题也用同样五篇文档：调研笔记放 `raw/research/`，决定放 decision-history，方案和执行步骤放 design 和 impl-plan，验证放 test-plan。每个有子问题的 design 都有一张子问题归属表，每个子问题标明「AI 查」「人决定」或「AI 查完人决定」。每个结论都有来源；查不到的写 `UNKNOWN`。测不了的项写成 `Unverified: <原因>（<什么条件下能测>）`。

<a id="ard-ad"></a><a id="ard-ad--eval-uses-deepseek-flash-with-3-independent-runs"></a>

### ARD-AD — 评测用 deepseek-flash 跑 3 次

目前只有 DeepSeek 的 API 可用，所以生成 gold 和判分都用 `deepseek-flash` 独立跑 3 次。不同模型之间的偏差暂时测不了，标为 Unverified。gold 由四部分组成：案例、版本、范例、标注。跑分结果 `runs/` 和报告 `reports/` 不提交。四个非软件例子（盖 shed、北京旅游、数学题、股票）写进 skill 正文作说明，不在本仓库建 gold。推翻 ARD-V 里建 gold 的部分。

<a id="ard-ac"></a>

### ARD-AC — PRD 和文档标准的调整

PRD 的必需章节去掉「非功能需求」；parent PRD 补齐 Overview、Goals and Success Metrics、User Stories、Functional Requirements、Out of Scope。编号在「feature 加文档类型」内唯一，跨 feature 引用写成 `<feature>/<编号>`。HLD 的架构章节不要求 DSGN 编号。how-to 有定义，但暂不检查。

<a id="ard-ab"></a><a id="ard-ab--four-skills-including-spec-pipeline"></a>

### ARD-AB — 四个 skill（已被 ARD-AJ 推翻）

当时的交付物是四个 skill：spec-pipeline 负责编排，spec-organize 负责标准和检查，spec-review 负责找问题，spec-write 负责改文档。推翻了只列三个 skill 的 ARD-O。

<a id="ard-aa"></a><a id="ard-aa--multi-participant-decisions-use-the-latest-history-entry-otherwise-ask"></a>

### ARD-AA — 多人决定以较晚的为准，否则问

PRD-F 关闭。两个决定冲突时，decision-history 里时间较晚的那条为准；看不出先后，就问用户。AI 不猜谁说了算。推翻 ARD-M。

<a id="ard-z"></a>

### ARD-Z — PRD 写清五项，再进入下游

取代 pipeline design 的 PIPE-E-B（当时编号 PIPE-E2）里原来没定义的「六项输入」。PRD 要写清限制、偏好、时间、资源、工具五项；不适用的写 not apply，不能留空。PRD、design、decision-history 三篇都存在后，才能开始写 impl-plan 和 test-plan。放弃的方案：用「building」这个词，以及让 PIPE-E-B 指向一个并没有这个定义的 PIPE-F。

<a id="ard-y"></a>

### ARD-Y — 按 20 小时估算来拆分

暂行规则（pipeline design 的 PIPE-D 第 6 步）。AI 先给出几种拆法。一个人 20 小时内能搞清楚的，算一个 feature spec；AI 估算超过 20 小时的，拆成 peer 或 sub-feature。估算和判断都由 AI 做。建目录仍要等人确认（PIPE-D 第 5 步）。

<a id="ard-x"></a>

### ARD-X — 执行只做到 mock 调用记录

不真订票，不真交易。mock MCP 客户端调用 mock MCP 服务器，打印出调用记录就算交付成功（PRD-O）。放弃的方案：真实执行，有不可撤回的副作用。

<a id="ard-w"></a>

### ARD-W — 可读性由本科程序员判断

另一个 LLM 扮演本科程序员。它读懂了才算通过，读不懂就不算交付（PRD-M）。调研时找到过 ISO 24495-1（简明语言标准），但没有拿它来打分。[ARD-BO](#ard-bo) 补上了具体判法。

<a id="ard-v"></a>

### ARD-V — 难题用同样五篇文档（建 gold 的部分已被 ARD-AD 推翻）

盖 shed、北京旅游、一道著名数学题、分析一只股票，都留在本 PRD（PRD-K），用同样五篇文档。每个子问题写明由谁处理，每个结论引用查到的事实（PRD-L、PRD-N）。放弃的方案：为它们另开一个 feature。仍然有效的部分由 [ARD-BT](#ard-bt) 重述。

<a id="ard-u"></a>

### ARD-U — spec-pipeline 编排和 Map、state 模型（已被 ARD-AJ 推翻）

当时 SDD 加了 spec-pipeline 作为入口 skill：它调用 spec-organize 和 spec-write，并在提交前提示跑 spec-review。Map 阶段靠和人访谈，产出（怎么拆、记什么决定、草稿）由 AI 判断，没有固定模板。进度先记在 CLAUDE.local，feature 建好后记到 `docs/features/<f>/raw/state/`。放弃的方案：Map 阶段强制产出固定文件，以及 BMAD 风格的仓库根目录状态树。spec-pipeline 作为入口已被 ARD-AJ 推翻；Create、Map、Converge、Downstream 四个阶段作为参考步骤保留在 pipeline design。仍然有效的部分（访谈、进度记录的位置）由 [ARD-BT](#ard-bt) 重述。

<a id="ard-t"></a>

### ARD-T — wayfinder-import 不是 SDD 的 sub-feature

wayfinder 导入是另一项工作，属于 skill-factory，不属于 SDD 交付物。`spec-driven-development/features/wayfinder-import/` 下的目录删除；需要的话在别处继续。ARD-I 的两份 spec 例外从此只是历史。

<a id="ard-s"></a>

### ARD-S — gold 可以增长，并有版本号

每次跑分发现的新好例子、新坏例子，追加到 `annotations.yaml`，同时 gold 版本号加一。分数只在同一个版本内比较。放弃的方案：gold 冻结不变，那样评审中发现的问题就积累不下来。

<a id="ard-r"></a>

### ARD-R — 两个分数和门槛

MUST 合规分是硬底线，必须满分。对标 gold 的分数按「(加分 − 减分) × 10 / 标注总数」计算，在同一 gold 版本内不能退步。放弃的方案：给对标分设一个固定及格线，因为 gold 升版后分母会变，固定线没有意义。

<a id="ard-q"></a>

### ARD-Q — 测试放在 skill 目录下

skill 会被装到任意项目里，测试也要跟着走。跨 skill 的检查器、gold、报告放在 spec-organize 下（当时它是主 skill）。放弃的方案：放在仓库根目录 `tests/sdd/`，那样测试不会跟着 skill 一起部署。

<a id="ard-p"></a>

### ARD-P — spec-review 也查机械规则

review 输出修改建议，不直接改。机械规则的违反也必须出现在建议里，否则使用者拿到的审查不完整。负责整理的工具可以直接修；review 只找问题、给建议。放弃的方案：review 只看语义，那样就没法用同一套 MUST 来给 review 打分。

<a id="ard-o"></a><a id="ard-o--skills-are-spec-organize-main-spec-review-spec-write-the-standard-file-is-spec-organizespec-standardmd"></a>

### ARD-O — skill 是 spec-organize（主）、spec-review、spec-write（已被 ARD-AB 推翻）

交付的 skill 统一用 `spec-` 前缀，因为它们服务于 spec-driven development，而不是一般的文档编辑。标准文件放在主 skill 里，叫 `SPEC-STANDARD.md`，延续 ARD-B 的做法。放弃的方案：单独建一个 `spec-standard` skill，三个使用方多一份要同步的副本。

<a id="ard-n"></a>

### ARD-N — 产品级成功指标延后

产品级成功指标怎么量、基线是多少，目前没有数据来定，延后到 PRD-G。test-plan 里的分数是评测指标，不是产品成功指标。

<a id="ard-m"></a>

### ARD-M — 多人决定以谁为准（已被 ARD-AA 推翻）

当时还没想清楚多人决定冲突时以谁为准，先延后到 PRD-F。后来由 ARD-AA 定下规则。

<a id="ard-l"></a>

### ARD-L — 盲区由现有 skill 发现

`research` skill 已经有「发现未知」的分支，`grill-with-docs` 已经会做追问式访谈。PRD-H 要求优先用现有工具。放弃的方案：专门新建一个 skill；在现有做法够用之前不做。以后可以换成新 skill，但「这一步必须跑」的要求不变。

<a id="ard-k"></a>

### ARD-K — AI 每次只改一小段（「满足其一即可」已被 ARD-BP 推翻）

一次大改动没人细看就进去了，出了问题也难找原因。当时的上限是 10 行或 200 字符，满足其中一条即可；[ARD-BP](#ard-bp) 改为两条都要满足。更大的改动拆成多次。真要大改（restructure）需要人明确同意，ARD-AI 和 ARD-BK 就是这样的授权。放弃的方案：超出上限直接拒绝，会挡住正当的大改；只警告不拦，等于没有限制。

<a id="ard-j"></a>

### ARD-J — 五种必需文档加一种可选的 how-to

PRD 当时写的是六种必需文档，`pipeline-design.md` 和文档标准写的是五种。五种是对的：how-to 只在需要人去操作结果时才写，不是每个 feature 都要有。当时把这五种文档叫作「阶段」；现在「阶段」专指 pipeline design 里的 Create、Map、Converge、Downstream 四步，所以这里改称「文档」。放弃的方案：为了和 PRD 一致保留六种必需文档，那样会多出一种大多数 feature 用不到的文档。

<a id="ard-i"></a>

### ARD-I — 当时有两份 spec 文档（已成历史）

这是对 ARD-F 的「每种类型默认一份」的有意例外，按规则要写明原因，不能悄悄违反。当时这个 feature 以标准本身命名，所以标准的 spec 放在这里；而 `wayfinder-import-design.md` 已经占了 `spec-driven-development/design/`，它是另一项有自己生命周期的工作。两份文件按 ARD-G 用名称区分。放弃的方案：给 feature 改名（这个名字已在项目里用开了）；把标准单独放一个 feature（标准和导入当时属于同一项工作）；把两份合成一份（两件不相关的事写在一个文件里）。ARD-T 删除 wayfinder-import 后，这个例外不再存在。

<a id="ard-h"></a>

### ARD-H — 内容分四个优先级，L1 永远不删

L1 是决定性内容：行为、接口约定、不变量、约束、错误处理、安全规则、架构边界、不在范围内的事项、前提假设、兼容性约束、未决问题。L2 是理由，L3 是放弃的方案，L4 是参考资料。文档需要瘦身时，先删 L4，再删 L3，再压缩 L2，L1 永远不删。

「不在范围内」「前提假设」「兼容性约束」「未决问题」归在 L1 而不是 L2，因为丢掉其中任何一项，实现会和丢掉一条需求一样出错。如果一个事实的权威出处在别的文档，这里只能放链接（L4），不能复述一遍。

<a id="ard-g"></a>

### ARD-G — 分篇的命名

```
payment-design-authorization.md        design 分篇：名词，没有顺序
payment-impl-plan-01-schema.md         impl-plan 分篇：序号加阶段，有顺序
```

放弃的方案：两者都用序号（`payment-design-01.md`）。序号说明不了内容，插入一篇还要全部重新编号。impl-plan 本身有先后顺序，所以序号有意义；design 按业务边界拆，所以用名词。

<a id="ard-f"></a>

### ARD-F — 一个 feature 可以有多份 design 或 impl-plan（已被 ARD-BQ 推翻）

后来六种文档都允许拆分篇，见 [ARD-BQ](#ard-bq)。当时的内容：取代原来「每个 feature 每种类型只有一份文件」的规则，只对这两种类型放开，并删掉禁止第二份 spec 的反例。`prd`、`test-plan`、`decision-history`、`how-to` 仍是一份：它们不会无限变长。design 和 impl-plan 会，既然限制了 1,000 行，就必须允许拆成多份。

<a id="ard-e"></a>

### ARD-E — 行数上限

旧的指引说 feature spec 一般 500 到 1,500 行，和 1,000 行上限矛盾。以上限为准，删掉旧指引。decision-history 不设上限：它只增不减，删减它就毁掉了它存在的意义；不设上限也就不会有删旧决定的压力。

<a id="ard-d"></a>

### ARD-D — 字段叫 health，不叫 status

`state` 字段已经表示写作状态（`draft` 或 `final`）。再加一个叫 `status` 的字段，读者会以为是同一件事，而且它的取值（`draft`、`active`、`stale`、`deprecated`）和 `state` 有重叠。放弃的方案：把 `state` 的取值改成 `draft | active | stale | deprecated`，那样所有已有文档都要改。

<a id="ard-c"></a>

### ARD-C — 细节放在 skill 目录的其他文件里

标准有十七节，全部写进 `SKILL.md` 会超过 700 行，而 skill 需要一次读完。沿用已有做法，例如 `domain-modeling/ADR-FORMAT.md` 和 `domain-modeling/CONTEXT-FORMAT.md`。这些文件和 skill 放在同一目录，跟着 skill 一起走，skill 才能装到别的项目；skill 不能指向本仓库的 `docs/`，因为别的项目里没有这个目录。

<a id="ard-b"></a>

### ARD-B — 标准放在已有的 skill 里

文档的放置、检查和合并本来就由 `doc-organize`（后改名 spec-organize）负责，它的 Sync 模式也负责发现不一致。新建一个 skill 就得把文档标准再抄一份。放弃的方案：新建 `spec-driven-development` skill，`doc-organize` 只留一个指针；两者会共用类型列表、frontmatter 约定和必需章节，副本迟早会不一致。

<a id="ard-a"></a>

### ARD-A — 按关注点分权威

原来的规则是「代码是唯一真相」，在 `doc-organize` 里写了三处。它把所有冲突都判给代码，spec 就保护不了「本来想要的行为」。比如 spec 规定重试 3 次，代码重试了 5 次：按旧规则 spec 是错的，即使 3 次才是需求。

放弃的方案：

- 继续「代码是唯一真相」：spec 在最需要约束的地方失效，而且通过的测试会被当成需求。
- 改成「spec 是唯一真相」：反过来也不行，spec 回答不了代码现在实际在做什么，每次重构都得改 spec。
- 「唯一真相加例外清单」：很难维护，而且默认仍有一方说了算。

采用的做法：按关注点分。想要的行为以 spec 为准，当前实现以代码为准，接口约定以机器可读的定义文件为准，数据库结构以 migration 为准，可执行的验证以测试为准。

## Path Update — 2026-10-30

2026-10-30 这个 feature 拆成了几个 sub-feature，历史记录里的路径对应如下：

| 旧路径 | 新路径 |
|---|---|
| 2026-10-30 之前的 `design/spec-driven-development-design.md`（流程设计） | `features/pipeline/design/pipeline-design.md` |

2026-10-31 起，`design/spec-driven-development-design.md` 这个路径重新使用，现在放的是 parent 的整体设计。历史记录保持原样，这张表只是现在的指路。没有改任何决定。

## Change Log

| Date | Change |
|------|--------|
| 2026-09-25 | Initial creation; records the SDD standard's adoption and the two-spec exception |
| 2026-10-30 | Added a path-update note after the feature was split into sub-features |
| 2026-10-30 | Added decisions ARD-J–ARD-N from the PRD revision: five stages, small edits, existing-skill blind spots, two deferrals |
| 2026-11-03 | 旧数字 ID → `ARD-A`–`ARD-N`; Log 倒序；格式对齐 document-standard **DSGN-E**/**DSGN-J** |
| 2026-11-03 | ARD-O–ARD-S：skill 命名、review 边界、测试位置、eval 评分与门槛、gold 版本化 |
| 2026-11-03 | ARD-T：移除 wayfinder-import sub-feature 树 |
| 2026-11-03 | ARD-U：spec-pipeline 编排；Map interview；state 两阶段 |
| 2026-11-04 | ARD-V–ARD-X：非软件难题留在本 PRD；可读性由本科程序员 LLM 打分；执行以 mock MCP log 为交付 |
| 2026-11-04 | ARD-Y：Map 拆分以一人 20 小时为界，估算和评判由 AI 做 |
| 2026-11-04 | ARD-Z：PRD 五项写明或 not apply；design 与 decision history 都在才进 Downstream |
| 2026-11-04 | PRD-F 关闭 ARD-M 的延期：按 history 时间，否则问用户。无新 ARD（A–Z 已用完） |
| 2026-11-04 | ARD-AA–AI：PRD-F 关闭、4 skill、文档标准、eval、非软件映射、未定义项、自动收敛、reader、restructure 授权 |
| 2026-11-07 | ARD-AJ：入口改为 spec-write 与 spec-review；标准两份文档；organize 与 pipeline 不再是入口 |
| 2026-11-07 | ARD-U 划掉并链到 ARD-AJ；四阶段名称留在 pipeline-design 作参考 |
| 2026-11-07 | ARD-AK：手写 HTML 用 spec-source 与 sha256；不一致则 paired_html_stale |
| 2026-11-07 | ARD-AL：audience 只允许 internal 或 external；缺省不算失败 |
| 2026-11-07 | ARD-AM–BE：步骤号、tracker、锚点、commit、图、外部 gold（逐字稿） |
| 2026-11-07 | 保留 ARD-O 旧锚点（ARD-AP） |
| 2026-11-07 | ARD-BF：spec HTML 统一放 docs/book/html/，目录与 features 同构 |
| 2026-11-07 | ARD-BG：全站一份目录；feature 页左目录右正文 |
| 2026-11-18 | ARD-BH：交付只有 spec-write 与 spec-review |
| 2026-11-18 | ARD-BI：左侧栏 1–6 加 10 sub-feature |
| 2026-11-18 | ARD-BJ：gold spec 就是这套 spec-driven-development |
| 2026-11-20 | ARD-BK–BO：授权本次大改；gold 改回 iPhone 案例（推翻 ARD-BJ）；删除线只在 decision-history；规则分 MUST 与 NICE；可读性成为通过条件 |
| 2026-11-20 | 全文改为中文；Evidence Appendix 改为与 Log 同序，补齐 ARD-M、ARD-N 与 ARD-AM 之后各条的原因；每条加短锚点，旧英文锚点保留（ARD-AP）；Path Update 说明旧路径已重新使用（ARD-BK） |
| 2026-11-20 | 第 1 轮审查后：ARD-BP–BT（改动上限两条都要满足、六种文档都可拆分篇、PIPE 子条款改字母、允许中英文混合、重申 ARD-U/V 仍有效的部分）；划掉 ARD-AH、ARD-F、ARD-K；ARD-J 的「阶段」改称「文档」；跨 feature 的编号补上 feature 名 |
| 2026-11-24 | ARD-CC：spec bundle 版本戳（审查 F7 选方案一） |
| 2026-11-24 | Evidence Appendix 的 ARD-CB 移到 ARD-CA 前，与 Log 同序；ARD-CA、ARD-CB 改写成完整句子 |
| 2026-11-24 | 划掉 ARD-AF，由 ARD-CC 重述仍有效的部分 |
| 2026-11-24 | ARD-CD：GitHub Pages 发布，删除 6 个从首页点不到的旧页面 |
| 2026-11-24 | ARD-BO 的放弃方案改正对 ISO 24495-1 的描述（审查 F16） |
| 2026-11-24 | 补记 2026-11-20 的 Log 变化：新增 ARD-BU 到 ARD-CB；划掉 ARD-BH、ARD-BE、ARD-AW、ARD-BK（各自链到推翻它的 ARD） |
| 2026-11-24 | 新增 ARD-CE 到 ARD-CL；划掉 ARD-CC、ARD-BX、ARD-BP、ARD-BT、ARD-BU（各自链到推翻它的 ARD） |
| 2026-11-24 | 第 8 轮审查后：划掉 ARD-AD，由 ARD-CJ 重述并写明范围；ARD-CE 写明挪出内容算修改；ARD-CH 地图改为目录、阻塞以 QUES 为准；ARD-CK 写明五个 SKILL.md |
| 2026-11-24 | 第 9 轮审查后：ARD-CK、ARD-CJ、ARD-CH 补全被划掉条目里仍有效的部分；ARD-CJ 写明 claude_audit 何时保留 |
| 2026-11-24 | 第 10 轮审查后：ARD-CA 补上对 ARD-BE 的重述 |
| 2026-11-24 | 第 11 轮审查后：ARD-CA 的重述分清 MUST 和 NICE，补上节点和连线上限 |
| 2026-11-24 | 第 13 轮审查后：ARD-CJ 写明 judgments/ 是「结果不提交」的例外 |
