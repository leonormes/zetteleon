---
created: 2026-07-28T10:35:28+00:00
epistemic_status: low
modified: 2026-08-29T09:35:58+00:00
permalink: llmeon/30-library/100-zettelkasten/architecture-as-source-of-truth-code-regenerated-from-specification-rather-than-reverse-engineered-into-it
proposition: If code becomes fully disposable, the source of truth for a system should
  invert — instead of architecture being inferred after the fact from existing code,
  engineers converge on an architecture specification directly, and code is regenerated
  whenever that specification changes. This is explicitly aspirational; the source
  'acknowledges the tools and shared vocabulary needed to make "specification" expressive'
  "and precise enough don't yet exist."
tags: [domain/llm, topic/software-architecture, topic/speculative]
title: Architecture as Source of Truth - Code Regenerated From Specification Rather Than Reverse-Engineered Into It
  Than Reverse-Engineered Into It
type: claim
---

## Architecture as Source of Truth - Code Regenerated From Specification Rather Than Reverse-Engineered Into It

Today, architecture is usually something read out of code after the fact—diagrams and design docs are approximations that drift from what the code actually does the moment either one changes without the other. If code truly becomes a disposable, regenerable cache rather than a durable asset, the natural next step is to invert that relationship: engineers discuss and converge on an architecture specification directly, and code becomes the regenerated output of that specification rather than the thing architecture is inferred from. Changing the architecture would mean regenerating the code, not editing it and hoping the diagram gets updated to match.

This is presented as a genuinely open question rather than an available practice. What counts as a sufficiently expressive, precise "specification"—one detailed enough to regenerate correct code from, rather than just a rough sketch—isn't solved yet, and no current tooling supports this workflow end to end.

### Scope & Conditions

Speculative and forward-looking; the source explicitly says "the tools to do this don't exist yet." Treat as a direction implied by the disposable-code premise taken to its logical conclusion, not a documented or validated practice. Depends on solving what a machineand human-legible "specification" actually consists of—an unsolved problem, not a detail.

### Evidence

Source: Charity Majors, "AI demands more engineering discipline. Not less." (charitydotwtf.substack.com, captured 2026-06-17). Raises the possibility of converging on an architecture diagram and regenerating code from changes to it, while explicitly hedging that the necessary tooling doesn't yet exist.

### Implications

- It's the aspirational endpoint of the disposable-cache reframing: [[AI-Generated Code Shifts From a Durable Asset to a Disposable Cache When Regeneration Is Cheap]] argues code is disposable once regeneration is cheap; this note follows that premise to its conclusion—if code is fully disposable, durability has to live somewhere, and architecture specification is the candidate.
- It runs in the opposite direction from the vault's existing legacy-modernization pattern: [[AI Reverse-Engineers Legacy Codebases to Enable Modernization Without Original Developers]] describes AI inferring architecture _from_ existing code, for systems where no other source of truth survives. This note describes the reverse and more aspirational flow—architecture specified first, code generated _from_ it—which only becomes viable once specification tooling exists; today's reverse-engineering pattern is arguably the necessary bridge until then.
- It's distinct from the vault's review-speed tactics: [[Interactive Visual Artifacts Speed Human Review of Complex AI-Generated Designs]] uses visual artifacts to make existing AI-generated designs easier for humans to review quickly; this note is about the source of truth for generation itself, not about reviewing what's already been generated.

### Related

- [[AI-Generated Code Shifts From a Durable Asset to a Disposable Cache When Regeneration Is Cheap]]—extends: the further, speculative conclusion of treating code as fully disposable.
- [[AI Reverse-Engineers Legacy Codebases to Enable Modernization Without Original Developers]]—contrast: inverse direction (code→architecture vs. this note's architecture→code), and today's necessary workaround in the absence of the tooling this note calls for.
- [[Interactive Visual Artifacts Speed Human Review of Complex AI-Generated Designs]]—related: both concern architecture-level artifacts in AI-assisted development, but one speeds review of existing output, the other proposes replacing code as the source of truth entirely.

### See Also

- [[The Deletion Test Reveals Resistance to Deleting Code Is an Evaluation Problem, Not a Code Problem]]

[extends:: [[AI-Generated Code Shifts From a Durable Asset to a Disposable Cache When Regeneration Is Cheap]], strength=2, confidence=low]
