---
name: grilling
description: |
  Use when the user wants to stress-test a plan or design before building,
  or uses any 'grill' trigger phrase. Interviews the user relentlessly, one
  question at a time, each with a recommended answer.
license: MIT
compatibility: claude-code,opencode
metadata:
  triggers:
    - grill
    - grill me
    - stress-test a plan
    - interview me
  when_to_use: |
    When a plan or design has open decisions that only the user can make.
    When another skill (wayfinder, grill-with-docs) names /grilling.
  when_not_to_use: |
    When the answer is a fact that can be found by exploring the codebase.
    When the user wants synthesis of an existing conversation, not an
    interview.
  audience:
    - developers
    - designers
  source_author: mattpocock
  source_url: https://github.com/mattpocock/skills/blob/fa460cb/skills/productivity/grilling/SKILL.md
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time, waiting for feedback on each question before continuing. Asking multiple questions at once is bewildering.

If a *fact* can be found by exploring the codebase, look it up rather than asking me. The *decisions*, though, are mine — put each one to me and wait for my answer.

Do not enact the plan until I confirm we have reached a shared understanding.
