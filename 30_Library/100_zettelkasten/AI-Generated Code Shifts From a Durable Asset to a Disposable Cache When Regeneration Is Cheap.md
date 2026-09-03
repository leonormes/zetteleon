---
created: 2026-07-28T10:35:28+00:00
epistemic_status: medium
modified: 2026-08-29T09:35:57+00:00
permalink: llmeon/30-library/100-zettelkasten/ai-generated-code-shifts-from-a-durable-asset-to-a-disposable-cache-when-regeneration-is-cheap
proposition: When AI makes regenerating code cheap, code stops functioning as a durable
  "asset and starts functioning as a cache — a materialized view of understanding that's"
  useful while current and disposable when stale. This extends the immutable-infrastructure
  principle (mutation accumulates entropy, replacement resets it) from infrastructure
  into application code itself, making editing-in-place the riskier choice once rewriting
  is cheap.
tags: [domain/llm, topic/code-quality, topic/software-architecture]
title: AI-Generated Code Shifts From a Durable Asset to a Disposable Cache When Regeneration Is Cheap
  Is Cheap
type: claim
---

## AI-Generated Code Shifts From a Durable Asset to a Disposable Cache When Regeneration Is Cheap

Infrastructure engineering already made this move once: immutable infrastructure treats servers and containers as disposable, replacing rather than patching them, because mutation accumulates entropy in ways that make long-lived, hand-edited systems drift into unreproducible states. Cheap AI-driven code generation pushes the same premise into application code. When regeneration is easy, code stops being an asset you protect and starts acting as a cache—"a materialized view of understanding that is useful while current, disposable when stale" (Chad Fowler). Editing in place, once the default and cheapest option, becomes the riskier one: each in-place mutation adds a little entropy that a clean regeneration would have reset.

The shift isn't about code quality dropping—it's about where durability is expected to live. If code is disposable, the thing that has to be durable instead is whatever tells you the regenerated version is still correct.

### Scope & Conditions

Applies where AI-assisted regeneration of a component is genuinely cheap and reliable enough to be a realistic alternative to patching—not yet universal, and the source explicitly ties the argument to code where evaluation criteria for correctness already exist or can be made explicit (see the companion Deletion Test claim). Doesn't apply to code whose correctness can't be externally verified; in that case regeneration just trades one unverifiable state for another.

### Evidence

Source: Chad Fowler (quoted and endorsed by Charity Majors, "AI demands more engineering discipline. Not less.", charitydotwtf.substack.com, captured 2026-06-17): "When regeneration is easy, code stops being an asset and starts acting as a cache: a materialized view of understanding that is useful while current, disposable when stale." Majors extends this explicitly beyond infrastructure: "AI pushes this premise beyond infrastructure and into application code itself. When rewriting is cheap, editing in place becomes risky. Mutation accumulates entropy. Replacement resets it."

### Implications

- It depends on solving the evaluation-gap problem first: [[The Deletion Test Reveals Resistance to Deleting Code Is an Evaluation Problem, Not a Code Problem]] identifies why teams resist treating code as disposable—because the knowledge of what "correct" means often lives only in the code itself. This note's reframing is only safe once that knowledge has somewhere else to live.
- It relocates durability rather than eliminating it: [[Production-Stage Behavioral Testing and Fast Feedback Loops Are the Engineering Discipline AI-Generated Code Demands]] describes the concrete mechanism (behavioural tests, characterization tests, observability) that has to be durable and trustworthy precisely because the code no longer is.
- It's the same entropy-vs-reset logic already established for infrastructure, applied one layer up: no existing vault note currently documents the immutable-infrastructure precedent this claim extends from—worth noting as a gap rather than assuming coverage.
- Taken to its logical endpoint, this argues for architecture becoming the durable artifact instead of code: [[Architecture as Source of Truth - Code Regenerated From Specification Rather Than Reverse-Engineered Into It]] is the aspirational, further-out version of this same premise.

### Related

- [[The Deletion Test Reveals Resistance to Deleting Code Is an Evaluation Problem, Not a Code Problem]]—depends_on: this note's disposability claim presupposes that note's diagnosis has been addressed.
- [[Architecture as Source of Truth - Code Regenerated From Specification Rather Than Reverse-Engineered Into It]]—extended-by: the speculative, further conclusion of treating code as fully disposable.
- [[Dark Factories Fail Within Months Because LLMs Lack Long-Term Architectural Intuition]]—contrast: that note's failure mode is uncontrolled _mutation_ accumulating over unsupervised runs; this note's prescription (prefer regeneration to in-place mutation) is a direct countermeasure to exactly that failure mode.
- [[Vibe Coding - Rapid AI-Assisted Code Generation Without Engineering Rigor]]—related: disposability without evaluation discipline is indistinguishable from vibe coding; the difference is entirely in whether correctness criteria exist.

### See Also

- [[Classic Engineering Discipline Is More Necessary, Not Less, as a Countermeasure to AI-Generated Slop]]

[depends_on:: [[The Deletion Test Reveals Resistance to Deleting Code Is an Evaluation Problem, Not a Code Problem]], strength=3, confidence=medium]
