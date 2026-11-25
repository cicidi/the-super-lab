# Answer key (written by coordinator before the run; the runner must not see it)
Target feature for all items: pic-to-txt (existing: docs/features/skill-factory/features/pic-to-txt/)
Rejected input: the PaddleOCR URL (v1 does not support URLs)
| # | Item | Doc type | Source |
| 1 | >200 images → ask before starting | prd | 用户 2026-11-23 |
| 2 | reason: OCR takes long | decision-history (reason of item 1) | 用户 2026-11-23 |
| 3 | output name <folder>-ocr.md | prd or design (both accepted: interface contract) | 用户 2026-11-23 |
| 4 | HEIC: pillow-heif first, then heif-convert (no reason) | decision-history, reason UNKNOWN (design also accepted) | 用户 2026-11-23 |
| 5 | order: HEIC decoding before batch confirm | impl-plan | 用户 2026-11-23 |
| 6 | reason: prompt needs image count | decision-history or impl-plan note (both accepted) | 用户 2026-11-23 |
| 7 | test: 3 HEIC → 3 text sections | test-plan | 用户 2026-11-23 |
| 8 | PaddleOCR ~2s/image on CPU | design, source UNKNOWN (no attribution) | UNKNOWN（path L10） |
| 9 | vertical Chinese? | design Open Questions (QUES) | path L11 |
| 10 | keep image filename as subheading | prd (design also accepted) | 用户 2026-11-23 |
Hard rules: no committed spec file written by spec-ingest; every row has a source or UNKNOWN; no invented items; URL rejected.

## Run 2026-11-24 (fresh agent, did not see this key)
8 decided rows, all match; I-3 and I-8 marked 待定 (not counted wrong, ARD-L); URL rejected; only the
gitignored sort table written. Agreement 100% (pass ≥90%). Six ambiguities it reported were fixed in
SKILL.md the same day (URL inside a file, `<f>` for sub-features, when to use 待定, background facts,
UNKNOWN list meaning, sort-table date).
