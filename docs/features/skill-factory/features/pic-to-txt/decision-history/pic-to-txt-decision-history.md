---
feature: pic-to-txt
type: decision-history
state: draft
health: active
owner: cicidi
last_verified: 2026-11-24
---

# pic-to-txt — 决策记录

本篇按时间倒序记录 `pic-to-txt` 这个 skill 的关键决策。
需求见 [PRD](../prd/pic-to-txt-prd.md)，设计见 [design](../design/pic-to-txt-design.md)。
所有决策都出自 2026-07-18 的会话 b1cdd2d6，同日由 commit 1e029ae 落地。
此后这个 skill 没有再改过（`git log --follow`）。

## Decision Log

| ID | Date | Decision |
|---|---|---|
| ARD-A | 2026-07-18 | 原始 OCR 结果存为 `_raw_ocr_output.txt`；LLM 修正必做，原始结果不交付 |
| ARD-B | 2026-07-18 | 输出文件以文件夹名命名，存回图片所在的文件夹 |
| ARD-C | 2026-07-18 | 放在 personal-skills，并附带 `ocr.py` 脚本统一调用两个引擎 |
| ARD-D | 2026-07-18 | 图片按文件名自然排序，文件顺序就是页序 |
| ARD-E | 2026-07-18 | 中文用 PaddleOCR，英文用 EasyOCR，不用 Tesseract |

## Evidence Appendix

### ARD-A

理由：用户要求"再用llm 优化"（PRD-B）。SKILL.md 写明 OCR 有错字，原始结果不能当成品。
保存原始结果、修正必做这两条由 agent 写入，用户没有逐条确认。
被否决的方案：直接交付原始 OCR 文本。出处：b1cdd2d6（2026-07-18）；commit 1e029ae。

### ARD-B

理由：用户要求结果放在当前文件夹，一个文件夹一份文档（PRD-A）。以文件夹名命名由 agent 定。
被否决的方案：UNKNOWN，对话里没有讨论别的命名方式。
出处：b1cdd2d6（2026-07-18）；当晚的产出 `slides/the-impact-of-ai-on-home-prices.md` 即按此命名。

### ARD-C

理由：agent 用选择题问放在哪里，选项是 personal-skills 和项目本地（PRD-E）。
被否决的方案：只放在当时的视频项目里。
`ocr.py` 把两个引擎的调用包成一条命令，由 agent 加入，用户没有专门要求。
出处：b1cdd2d6（2026-07-18）；commit 1e029ae。

### ARD-D

理由：agent 问是否按文件名排序，另一个选项是"自定义顺序"；复述的结论是按文件名排序（PRD-D）。
自然排序指 page2 排在 page10 前面，由 `ocr.py` 的 `natural_sort_key` 实现。
被否决的方案：自定义顺序。出处：b1cdd2d6（2026-07-18）。

### ARD-E

理由：agent 调研了三个开源引擎的中文准确率：Tesseract 约 82-85%，EasyOCR 约 88-93%，PaddleOCR 95% 以上（b1cdd2d6）。
随后 agent 复述"中文用 PaddleOCR（最强中文），英文用 EasyOCR"（PRD-C）。用户点选的原始答案没有存档。
被否决的方案：Tesseract；以及"你推荐吧"，即交给 agent 自选。
2026-07-22 用户问起百度的 Unlimited-OCR，agent 建议暂不替换；用户没有回复（会话 1de9cb65），见 design 的 QUES-D。

## Change Log

| Date | Change |
|------|--------|
| 2026-11-24 | 初版：从过去的对话和提交记录反推 pic-to-txt 的决策 |
