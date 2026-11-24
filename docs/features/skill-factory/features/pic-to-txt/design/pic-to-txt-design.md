---
feature: pic-to-txt
type: design
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# pic-to-txt — 截图转文字文档

本篇说明 `pic-to-txt` 这个 skill 现在怎么工作。
源文件：`personal-skills/pic-to-txt/SKILL.md` 和 `ocr.py`，都由 commit 1e029ae（2026-07-18）加入，之后没有改过。

## Problem Statement

做视频研究时，资料常是一组幻灯片或屏幕截图，文字锁在图片里（PRD-A）。
OCR 能认出文字，但会有错字、断词和丢标点，不能直接用（PRD-B）。

## Solution

一个 skill 加一个 Python 脚本。脚本按语言选引擎，对整个文件夹做 OCR（PRD-C）。
然后 agent 用 LLM 修正错字，把文档存回同一文件夹（PRD-A、PRD-B）。

## User Stories

- 作为做视频研究的人，我给出一个截图文件夹，拿回一份按页序排好的文字稿。
- 作为用户，我想知道用了哪个引擎、修了哪些错，好判断结果可不可信。

## Implementation Decisions

两个引擎都是 Python 库，脚本只在用到时才导入，没装的那个不影响另一个（`ocr.py`）。
EasyOCR 固定 `gpu=True`；PaddleOCR 打开方向分类，能处理旋转的文字（`ocr.py`）。
LLM 修正没有单独的脚本，由运行 skill 的 agent 自己完成（b1cdd2d6 当晚的运行）。

## Design

**DSGN-A 触发。** 触发词有 extract text from images、ocr these images、图片转文字、提取图片文字等（PRD-F）。
2026-07-26 漏触发过一次（a2dcb9ad）。现在加了照片转文字、OCR these photos、HEIC、pic 2 txt、把图片导成文档（ARD-G）。

**DSGN-B 检查依赖。** 第 0 步分别试着导入 paddleocr 和 easyocr，至少一个可用才继续，否则先安装（PRD-C）。

**DSGN-C 扫描和排序。** 第 1 步用 `ls -1v` 列出图片；它按自然顺序排，01 在 02 前，10 在 100 前（PRD-D）。
跑 OCR 前，必须让用户确认图片数量和顺序，并确认这些图片属于同一份文档（PRD-A）。

**DSGN-D 选引擎。** 中文用 PaddleOCR（`lang='ch'`），英文用 EasyOCR；中英混排优先 PaddleOCR（PRD-C）。
语言说不清时先问用户。

**DSGN-E 脚本 `ocr.py`。** 用法是 `ocr.py <folder> [--lang zh|en|auto]`，默认 auto（PRD-C）。
auto 的规则：文件名或文件夹名里有汉字就判为中文，否则判为英文。
SKILL.md 照此描述，并提醒 `IMG_1234.HEIC` 这类名字总被判为英文，中文要传 `--lang zh`（ARD-H）。
每张图的结果前加一行 `--- 文件名 ---`，合起来存为 `_raw_ocr_output.txt`，同时打到标准输出（PRD-A）。
HEIC/HEIF 照片先转成临时 JPEG：依次试 pillow-heif、`heif-convert`、ImageMagick；都不行就报错并列出安装方法（ARD-F）。
临时文件放在系统临时目录，跑完自动删除；结果里仍用原文件名。
文件夹不存在或里面没有图片时，报错退出。

**DSGN-F LLM 修正。** 第 3 步把原始 OCR 文本交给 LLM，只修错字、补标点和分段，保留标题和列表（PRD-B）。
不许增删内容，也不许总结；拿不准处标 `[sic?]` 或 `[unclear]`。

**DSGN-G 保存和报告。** 结果存为 `<文件夹>/<文件夹名>.md` 或 `.txt`，放在图片旁边（PRD-A）。
最后报告输出路径、图片张数、所用引擎、修正前后字数和主要修正。

**DSGN-H 存放位置。** skill 在本仓库的 `personal-skills/pic-to-txt/`（PRD-E）。
由 install.sh 装到各个 AI 工具，本机 `~/.claude/skills/pic-to-txt` 就是装好的副本。

## Testing Decisions

本 skill 没有自动测试或评测集。
创建当天，agent 用项目里的英文幻灯片跑过 `ocr.py`，EasyOCR 正常出字（b1cdd2d6）。
随后完整跑了 26 张幻灯片，原始约 2806 词，修正后约 3065 词（同一会话）。
PaddleOCR 当天还没安装，那条路径创建时没有测过（同一会话）。

## Out of Scope

手写字、单张图片、PDF、讲究版面的表格和表单、重水印或艺术字图片，都不用本 skill（SKILL.md 的 When NOT to Use 一节）。

## Further Notes

需求见 [PRD](../prd/pic-to-txt-prd.md)，决策见 [decision-history](../decision-history/pic-to-txt-decision-history.md)。
youtube-research-pipeline 第 0 步调用本 skill 的 `ocr.py`，但写的是旧路径 `~/project/skill-factory/...`。
这个目录本机已不存在，见 QUES-F。

## Alternatives Considered

Tesseract：中文准确率最低，被否决（ARD-E）。自定义页序：被否决，改为按文件名排序（ARD-D）。
Unlimited-OCR（百度的视觉大模型 OCR）：2026-07-22 讨论过，没有接入，见 QUES-D。

## Drawbacks

HEIC（苹果手机照片格式）只有 `ocr.py` 能读；转换要装 pillow-heif、`heif-convert` 或 ImageMagick 之一（ARD-F）。
SKILL.md 第 2 步的内联命令只匹配 `*.png`，HEIC 照片要改用 `ocr.py`（ARD-F）。
一个文件夹只出一份 md 或 txt。2026-08-03 用户要过 md 加 Excel，还要按图片拆成多份（会话 8be9c74b），见 QUES-E。

## Risks and Mitigations

| 风险 | 缓解 |
|---|---|
| 用户的说法不在触发词里，agent 自己编内容 | 2026-07-26 发生过（a2dcb9ad）；已补触发词（ARD-G） |
| auto 判断语言不准，选错引擎 | 语言说不清时先问用户（DSGN-D）；照片名里没有语言线索时传 `--lang`（ARD-H） |
| 原始 OCR 文件一直留在图片旁边 | SKILL.md 要求保留它，没有清理选项；是否需要属于 UNKNOWN |

## Open Questions

| ID | 问题 | 目前答案 | Owner | Blocking |
|---|---|---|---|---|
| QUES-A | 要不要支持 HEIC 照片（PRD-A）？ | 支持，`ocr.py` 先转成 JPEG（ARD-F） | cicidi | no |
| QUES-B | 触发词要不要加上"导成文档""转文字稿"等说法（PRD-F）？ | 已加照片转文字、pic 2 txt、把图片导成文档等（ARD-G） | cicidi | no |
| QUES-C | auto 语言检测以哪个为准（PRD-C）？ | 以 `ocr.py` 为准：看名字里的汉字（ARD-H） | cicidi | no |
| QUES-D | 要不要把 Unlimited-OCR 加为可选引擎（PRD-C）？ | agent 2026-07-22 建议暂不；用户未回复（1de9cb65） | cicidi | no |
| QUES-E | 要不要支持 Excel 等输出，或把一个文件夹拆成多份文档（PRD-A）？ | 当前只出一份 md 或 txt | cicidi | no |
| QUES-F | youtube-research-pipeline 里 `ocr.py` 的旧路径要不要改（PRD-E）？ | 仍指向已不存在的 `~/project/skill-factory/` | cicidi | no |
| QUES-G | 2026-07-18 用户选引擎的原始答案是什么（PRD-C、PRD-D）？ | 只有 agent 的复述，答案没有存档 | cicidi | no |

## Reversibility

所有改动都在 git 跟踪的 `personal-skills/pic-to-txt/` 里，用 `git revert` 即可撤回。
已安装的副本要重跑 `install.sh` 才会同步。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：按 SKILL.md 和 ocr.py 写出 pic-to-txt 的 design，引用 PRD-A 到 PRD-F |
| 2026-11-24 | 按 ARD-F、G、H 改写 DSGN-A、E，Drawbacks，QUES-A、B、C |
