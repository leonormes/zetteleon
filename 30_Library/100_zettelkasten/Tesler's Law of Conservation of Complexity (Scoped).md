---
conformant: true
created: 2026-09-19T15:24:06+00:00
created_utc: 2026-09-19 00:00:00+00:00
modified: 2026-09-19T15:44:43+00:00
permalink: llmeon/00-inbox/teslers-law-of-conservation-of-complexity-scoped
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [complexity, conservation, software-architecture, tesler-law]
title: "Tesler's Law of Conservation of Complexity (Scoped)"
type: claim
upstream: '[[Data Structures vs Control Flow]]'
---

## Tesler's Law of Conservation of Complexity (Scoped)

Software has an inherent amount of complexity dictated by its problem domain that can be relocated between a system's layers (interface, code, data) but not eliminated by any single layer absorbing it.

### Scope & Conditions

Applies specifically to essential/irreducible complexity per Tesler's original postulate, not to total system complexity—Tesler's own wording concedes that reducible complexity exists and can genuinely be destroyed.

### Evidence

> "Tesler…observed that this inherent complexity behaves much like mass or energy in physics; it cannot be legislated out of existence." / "Tesler postulated that every application has an inherent amount of irreducible complexity, and the only question is who has to deal with it. That wording concedes that reducible complexity exists."

### Implications

- Simplifying one layer (e.g. UI) forces another layer (code) to absorb the corresponding complexity.
- The Law only constrains the portion of complexity that is genuinely irreducible.

### Related

- [[SoT - Conservation of Complexity]]—direct concept match: same law, same "cannot be destroyed, only relocated" framing, same balloon/waterbed analogy family.
- [[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]]—extends: generalises this exact law from software specifically to every formal system (type theory, clinical data, infrastructure, cognitive scaffolding).

### See Also

- [[SoT - Infrastructure Complexity]]—applies the same conservation law to IaC (AWS vs Azure, "pay the tax upfront or on cleanup").
