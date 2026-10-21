---
conformant: true
contradicts: []
created: 2026-10-21 14:00:00+00:00
epistemic_status: low
evidence_links: []
modified: 2026-10-21 14:00:00+00:00
proposition: The SoT claims one pattern operates identically in type theory, clinical
  data, declarative infrastructure and cognitive scaffolding, where a constitutive
  schema removes a class of runtime failure by making it structurally undefined.
status: seed
tags:
- formal-methods
- topic/knowledge-architecture
- topic/software-architecture
- TheHuman/Health/ADHD
title: The Same Constitutive Schema Removes a Class of Runtime Failure in Type Theory,
  Clinical Data, Infrastructure and Cognitive Scaffolding
type: claim
permalink: llmeon/30-library/100-zettelkasten/the-same-constitutive-schema-removes-a-class-of-runtime-failure-in-type-theory-clinical-data-infrastructure-and-cognitive-scaffolding
---

## The Same Constitutive Schema Removes a Class of Runtime Failure in Type Theory, Clinical Data, Infrastructure and Cognitive Scaffolding

The SoT claims that one pattern operates in four domains: a constitutive schema removes a class of runtime failure by making it structurally undefined, and where the schema is absent the runtime pays. It states that this is an isomorphism and not an analogy. This note records the claim as the SoT makes it, with its evidence status marked as low because two challenges to it are open.

### Scope & Conditions

- The four domains are type theory, clinical data (the OMOP CDM), declarative infrastructure and cognitive scaffolding for ADHD. A fifth case, Git's object store, is argued separately in [[Git's Content-Addressed Object Store Absorbs Distributed-Trust Complexity Into Structure]].
- The strongest support is the SoT's own table of what each structure constitutes and what the runtime pays when it is absent. The weakest part is the cognitive row, which has no formal machinery behind it.
- The word "isomorphism" is a mathematical claim and needs a mapping between structures. The SoT supplies a concept lattice as the mapping, and the reading of that lattice is contested.

### Evidence

> "The isomorphism is not an analogy. The same abstract structure—constitutive schema eliminates a class of runtime failure by making it structurally undefined—operates identically in all four rows."
> ([[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]], §2 The Isomorphism of Order)

> "Runtime exceptions. Defensive validation code multiplies. Invalid states become representable and must be caught or missed at execution time."
> (same section, the type theory row, "Runtime Pays When Absent")

### Implications

- If it holds, a design lesson from one domain should transfer to the others, such as treating drift as a signal in infrastructure and in a personal task system alike.
- If it holds only as a family resemblance, transfer is a source of hypotheses and not a guarantee, which is the reading in [[Shared Formal Attributes Across Domains May Be a Family Resemblance and Not an Ontological Equivalence]].

### Related

[depends_on:: [[Structure Constitutes the Domain of Valid Facts Rather Than Representing a Pre-Existing Truth]], strength=5, confidence=high]

- [[Structure Constitutes the Domain of Valid Facts Rather Than Representing a Pre-Existing Truth]]—depends on: the cross-domain claim presupposes the constitutive reading.
- [[A Declarative State File Is the Infrastructure and Configuration Drift Is Its Gap From Reality]]—elaborates: the infrastructure row worked out.
- [[A Clinical Observation Outside the Common Data Model Is Undefined in That Domain Rather Than Poorly Captured]]—elaborates: the clinical data row worked out.
- [[An External Scaffold Is the Executive Function for an ADHD System and Not an Aid to It]]—elaborates: the cognitive row worked out.
- [[SoT - The Curry-Howard Correspondence (Propositions as Types)]]—elaborates: the type theory row, where a type is a proposition.

### Tensions

- [[Shared Formal Attributes Across Domains May Be a Family Resemblance and Not an Ontological Equivalence]]—tension, not contradiction: the lattice shows shared attributes and does not by itself establish equivalence.
- [[Cognitive Scaffolds Are Constitutive but Lack Formal Closure]]—tension, not contradiction: the fourth row has no proof, algebra or reconciliation engine behind it.