---
created: 2026-07-28T10:35:28+00:00
epistemic_status: medium
modified: 2026-08-13T10:54:54+00:00
permalink: llmeon/30-library/100-zettelkasten/the-deletion-test-reveals-resistance-to-deleting-code-is-an-evaluation-problem-not-a-code-problem
proposition: When an engineer resists deleting and regenerating a piece of code, the
  "real reason is almost never attachment to the code itself — it's that the team lacks"
  the evaluation criteria needed to trust a replacement. Naming reasons like "we don't
  know what behavior is required," "we don't know which failures are unacceptable,"
  or "we don't know how to tell if a new version is correct" reveals that code becomes
  precious specifically when it is the only place that knowledge lives, not because
  the code has intrinsic value.
tags: [domain/llm, topic/code-quality, topic/software-architecture]
title: The Deletion Test Reveals Resistance to Deleting Code Is an Evaluation Problem, Not a Code Problem
  Not a Code Problem
type: claim
---

## The Deletion Test Reveals Resistance to Deleting Code Is an Evaluation Problem, Not a Code Problem

Ask an engineer why a piece of working code can't just be deleted and regenerated from scratch, and the answers that come back are rarely about the code's structure or cleverness. They're about uncertainty: nobody wrote down what behaviour the code is actually required to have, nobody can say which failure modes would be unacceptable in a replacement, and nobody has a reliable way to check whether a rewrite is correct. The Deletion Test surfaces this directly—the felt resistance to deleting code is a symptom, and the disease is a missing or unarticulated evaluation criterion. The code isn't precious; the tacit knowledge trapped inside it, with nowhere else to live, is.

This reframes what "legacy code anxiety" actually is. It isn't sentimentality or risk-aversion about the artifact—it's a rational response to not having externalised the specification that the artifact happens to encode.

### Scope & Conditions

Applies whenever an engineer or team notices reluctance to delete, replace, or regenerate a working implementation. The test is diagnostic, not prescriptive on its own—naming the missing evaluation criterion doesn't automatically produce it; it just correctly locates where the actual work needs to happen (writing down behavioural requirements, failure tolerances, and correctness checks) rather than in preserving the code.

### Evidence

Primary source: Chad Fowler, "The Deletion Test" essay, quoted and endorsed in Charity Majors, "AI demands more engineering discipline. Not less." (charitydotwtf.substack.com, captured 2026-06-17): "When regeneration is easy, code stops being an asset and starts acting as a cache: a materialized view of understanding that is useful while current, disposable when stale." Majors extends Fowler's framing directly: the reasons teams give for not deleting code—not knowing required behaviour, not knowing unacceptable failure modes, not knowing how to verify correctness—are evaluation gaps, and "code becomes precious when it is the only place that knowledge lives."

### Implications

- It's the foundation the disposable-cache reframing depends on: [[AI-Generated Code Shifts From a Durable Asset to a Disposable Cache When Regeneration Is Cheap]] only holds once this note's diagnosis is accepted—code can safely become "disposable" precisely because (and only once) the evaluation criteria that used to live implicitly in the code get made explicit elsewhere.
- It relocates the real deliverable of production-stage testing: [[Production-Stage Behavioral Testing and Fast Feedback Loops Are the Engineering Discipline AI-Generated Code Demands]]'s behavioural tests, characterization tests, and observability aren't just quality-assurance overhead—they're the concrete mechanism for externalising the evaluation criteria this note says code-hoarding anxiety is actually about.
- It gives a sharper diagnostic vocabulary than the vault's existing slop/discipline notes: [[Classic Engineering Discipline Is More Necessary, Not Less, as a Countermeasure to AI-Generated Slop]] argues structural discipline (DI, modularity, deterministic tests) constrains AI-generated code's blast radius; this note adds a distinct, prior question—do we even know what "correct" means for this component—that structural discipline alone doesn't answer.

### Related

- [[AI-Generated Code Shifts From a Durable Asset to a Disposable Cache When Regeneration Is Cheap]]—the reframing this note's diagnosis makes possible.
- [[Classic Engineering Discipline Is More Necessary, Not Less, as a Countermeasure to AI-Generated Slop]]—related: structural discipline and evaluation-criteria discipline are complementary, not the same lever.
- [[Vibe Coding - Rapid AI-Assisted Code Generation Without Engineering Rigor]]—related: rapid, low-rigor generation is riskiest precisely where evaluation criteria were never written down.

### See Also

- [[Production-Stage Behavioral Testing and Fast Feedback Loops Are the Engineering Discipline AI-Generated Code Demands]]
