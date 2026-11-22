---
conformant: true
contradicts: []
created: 2026-09-19T15:26:00+00:00
created_utc: 2026-09-19 00:00:00+00:00
epistemic_status: medium
evidence_links: []
modified: 2026-11-22T20:00:00+00:00
non_conformance_reason: ''
permalink: llmeon/30-library/100-zettelkasten/conservation-of-complexity-is-testable-only-if-essential-complexity-is-measured-before-the-design-is-chosen
proposition: The law that software complexity is conserved is testable only if essential complexity is measured independently of the design, not defined as whatever survives simplification
source_title: The Conservation of Software Complexity - The Dichotomy of Data Structures and Control Flow (plus epistemic review and fact-check)
source_url: unknown
status: seed
tags: [conservation-of-complexity, epistemics, falsifiability, unfalsifiable-claims]
title: Conservation of Complexity Is Testable Only If Essential Complexity Is Measured Before the Design Is Chosen
type: claim
upstream: '[[tmp_atoms_data-structures-vs-control-flow]]'
---

## Conservation of Complexity Is Testable Only If Essential Complexity Is Measured Before the Design Is Chosen

The law that software complexity is conserved, only moved and never destroyed, can be tested only if essential complexity is measured independently of the design, for example by counting the domain's states or business rules before any representation is chosen. If essential complexity is instead defined as whatever remains after simplification, every reduction can be redescribed as accidental complexity removed, so the law is true by definition and predicts nothing. ^claim

### Scope & Conditions

Applies to conservation-of-complexity claims in software (Tesler's law, and the version that complexity moves between control flow and representation), and more widely to any "conservation of X" claim whose conserved quantity is identified after the change it is meant to explain. It does not say the law is false: it says what the law needs in order to be a test and not a definition. Brooks's own definition of essential complexity is tied to the problem, so the circularity arises only when "essential" is worked out afterwards. Counts of states or rules are proxies, and different independent counts might disagree.

### Evidence

The core is the author's own logical argument. It came from an AI epistemic review (source not kept), and the paraphrased quotation that stood here was never a book passage, so it has been removed. Brooks defines the term at the level of the problem, before any representation, which is what makes an independent measure conceivable. His text does not show that such a measure is easy:

> "The essence of a software entity is a construct of interlocking concepts"
> (Brooks 1995, ch. 16) · [open in Calibre](calibre://view-book/GCcalibreBooks/1634/EPUB?open_at=toc:Chapter%2016.%20No%20Silver%20Bullet%E2%80%94Essence%20and%20Accident%20in%20Software%20Engineering)

> "I believe the hard part of building software to be the specification, design, and testing of this conceptual construct, not the labor of representing it and testing the fidelity of the representation."
> (Brooks 1995, ch. 16) · [open in Calibre](calibre://view-book/GCcalibreBooks/1634/EPUB?open_at=toc:Chapter%2016.%20No%20Silver%20Bullet%E2%80%94Essence%20and%20Accident%20in%20Software%20Engineering)

### Implications

- To use the law as a test, fix the measure first: count states or business rules before comparing designs, so no leftover complexity can be relabelled essential afterwards.
- A conservation claim with no measure fixed in advance is a design heuristic about where complexity lives, not a tested law.
- Ask of any such claim: what was counted before the change?

### Falsifier

- A post-hoc definition of essential complexity that still yields a prediction which could fail, or independent measures such as counts of states or rules that do not track the complexity engineers observe.

### Related

- [[Falsifiability Distinguishes Science from Dogma]]—standard applied: a claim must say in advance what would show it wrong.
- [[Essential vs Accidental Complexity (Brooks)]]—definition: Brooks's split between essential and accidental complexity, which this card asks to be measured independently.
- [[Tesler's Law of Conservation of Complexity (Scoped)]]—partial answer: it already calls the law a heuristic with no unit, and this card says what a unit would have to be.

[implements:: [[Falsifiability Distinguishes Science from Dogma]], confidence=high]
[depends_on:: [[Essential vs Accidental Complexity (Brooks)]], strength=4, confidence=high]

### Tensions

- [[Software Complexity is Conserved Between Control Flow and Representation]]—tension, not contradiction: states the law as settled fact without saying its test needs an independent measure of essential complexity.
- [[SoT - Conservation of Complexity]]—tension, not contradiction: gives the same unqualified statement, and its pointer to a note on whether the law generalises is currently dangling.

### Further Reading

- Brooks, Frederick P., Jr. 1995. *The Mythical Man-Month, Anniversary Edition: Essays on Software Engineering*. Pearson Education. [Open in Calibre](calibre://view-book/GCcalibreBooks/1634/EPUB)—_corroborates: essence is defined by the problem's concepts, not their representation._
