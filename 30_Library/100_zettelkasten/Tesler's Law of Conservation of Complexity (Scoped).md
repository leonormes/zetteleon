---
conformant: true
contradicts: []
created: 2026-09-19T15:24:06+00:00
created_utc: 2026-09-19 00:00:00+00:00
epistemic_status: medium
evidence_links: []
modified: 2026-10-16T15:00:00+00:00
non_conformance_reason: ''
permalink: llmeon/00-inbox/teslers-law-of-conservation-of-complexity-scoped
proposition: Software has an inherent amount of complexity dictated by its problem domain that can be relocated between layers of a system but not eliminated by any single layer absorbing it.
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [complexity, conservation, software-architecture, tesler-law]
title: "Tesler's Law of Conservation of Complexity (Scoped)"
type: claim
upstream: '[[tmp_atoms_data-structures-vs-control-flow]]'
---

## Tesler's Law of Conservation of Complexity (Scoped)

Software has an inherent amount of complexity dictated by its problem domain that can be relocated between a system's layers (interface, code, data) but not eliminated by any single layer absorbing it. The design question is therefore never whether the complexity exists, but which layer, and which person, carries it.

### Scope & Conditions

- Applies to essential (irreducible) complexity only, not to total system complexity. Tesler's own wording concedes that reducible complexity exists and can genuinely be destroyed, so removing accidental complexity does not break the law.
- The split between the two kinds is Brooks's, see [[Essential vs Accidental Complexity (Brooks)]]. Tesler's Law adds the conservation claim on top: what remains is moved, not removed.
- The law is a heuristic about allocation, not a measured quantity. No unit of essential complexity is given, which limits what it can predict (see Tensions).
- The original Tesler source is not held in the vault (`source_url` is unknown); the evidence below is a secondary restatement.

### Evidence

> "Tesler…observed that this inherent complexity behaves much like mass or energy in physics; it cannot be legislated out of existence." / "Tesler postulated that every application has an inherent amount of irreducible complexity, and the only question is who has to deal with it. That wording concedes that reducible complexity exists."

### Implications

- Simplifying one layer (e.g. UI) forces another layer (code) to absorb the corresponding complexity.
- The Law only constrains the portion of complexity that is genuinely irreducible.
- A simplification claim should name the receiving layer. "It is simpler now" without naming where the complexity went is a prompt to look for the hidden cost.
- Placement is a design choice with consequences: complexity moved into types and schemas is checked by tooling, complexity left in control flow is checked only at run time.

### Related

- [[SoT - Conservation of Complexity]]—direct concept match: same law, same "cannot be destroyed, only relocated" framing, same balloon/waterbed analogy family.
- [[Essential vs Accidental Complexity (Brooks)]]—part of: supplies the essential/accidental split that defines this note's scope.
- [[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]]—extends: generalises this exact law from software specifically to every formal system (type theory, clinical data, infrastructure, cognitive scaffolding).

[implements:: [[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]], confidence=high]

### Tensions

- [[A Conservation Claim Becomes Unfalsifiable If Essential Complexity Is Defined Post-Hoc]]—tension, not contradiction: if "essential" means whatever survived simplification, the law is true by definition. The scope above only holds as a testable claim if essential complexity is estimated independently of the representation.
- [[Radical Simplicity - The Don't Make Me Think Rule]]—tension, not contradiction: that note targets the user-facing friction surface, this one targets where the total complexity ends up. Hiding complexity from the user is compatible with it persisting elsewhere.

### See Also

- [[SoT - Infrastructure Complexity]]—applies the same conservation law to IaC (AWS vs Azure, "pay the tax upfront or on cleanup").
