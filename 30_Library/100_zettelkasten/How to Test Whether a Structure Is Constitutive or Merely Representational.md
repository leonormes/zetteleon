---
conformant: true
created: 2026-10-21 14:00:00+00:00
modified: 2026-10-21 14:00:00+00:00
status: seed
steps:
- Name the structure and the system it governs in one sentence.
- Absence test. Imagine removing the structure entirely and write down whether valid
  facts remain or only noise.
- Drift test. Find a case where the structure and the running state disagree and write
  down which one is treated as the reference.
- Elimination test. Name a class of failure and write down whether it can be made
  impossible at the structural level.
- Record the three answers and state the verdict, constitutive if all three point
  to the structure.
tags:
- formal-methods
- topic/knowledge-architecture
- epistemology
- topic/software-architecture
title: How to Test Whether a Structure Is Constitutive or Merely Representational
trigger: A schema, type system, state file or scaffold is being treated as either
  the definition of valid facts or only a record of them and the view needs checking.
type: procedure
verification: All three tests have a written answer for a named structure, and the
  verdict follows from those answers.
permalink: llmeon/30-library/100-zettelkasten/how-to-test-whether-a-structure-is-constitutive-or-merely-representational
---

## How to Test Whether a Structure Is Constitutive or Merely Representational

The SoT gives three tests for deciding whether a structure defines the valid facts of a system or only records them. The procedure runs them in order and ends with a verdict. The verdict rule in the last step is this note's own and is not in the SoT.

### Scope & Conditions

- Use it before claiming that a schema or type system is "the source of truth" and when a design argument turns on whether a structure is authoritative or merely descriptive.
- The tests apply to formal systems. For a model of an independent reality, such as a map of a territory, the answer is expected to be representational.
- A structure can pass one test and fail another. The SoT says the tests confirm the constitutive reading "in each domain" but does not say what to do with a split result, so the all-three rule here is a conservative choice.

### Evidence

> "1. The Absence Test. Remove the structure entirely. What happens to the truth? If truth dissolves—if there are no longer "valid" facts, only noise—then structure was constitutive, not representational.
> 2. The Drift Test. When structure and runtime state diverge, which is treated as the reference? In every well-engineered formal system, the structure wins.
> 3. The Elimination Test. Can a class of failures be made impossible at the structural level? If yes, the structure is doing more than documenting existing facts—it is constituting the domain of possible ones."
> ([[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]], §1, abridged)

### Implications

- The Drift Test is the quickest to apply in practice. Whichever side is corrected when the two disagree shows which side the team treats as the reference.
- The tests give a way to argue about the claim in [[Structure Constitutes the Domain of Valid Facts Rather Than Representing a Pre-Existing Truth]] case by case and not as a slogan.

### Related

[implements:: [[Structure Constitutes the Domain of Valid Facts Rather Than Representing a Pre-Existing Truth]], strength=3, confidence=medium]

- [[Structure Constitutes the Domain of Valid Facts Rather Than Representing a Pre-Existing Truth]]—implements: the tests are the working method for applying the claim.
- [[The Representational Fallacy]]—depends on: the tests separate the two views this concept contrasts.
- [[A Declarative State File Is the Infrastructure and Configuration Drift Is Its Gap From Reality]]—shared mechanism: the Drift Test is most visible in infrastructure.