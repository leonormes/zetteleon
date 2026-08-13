---
aliases: [AFM Hub, Applied Formal Methods Index, Formal Foundations Hub]
created: 2026-04-19T09:00:00+00:00
modified: 2026-08-13T10:53:35+00:00
permalink: llmeon/30-library/mo-c/moc-applied-formal-methods
see_also: ["[[MOC - Formal Logic & Philosophy (Triage)]]", "[[MOC - The Unified Systems Paradigm]]"]
supersedes: '[[MOC - Formal Logic & Philosophy (Triage)]]'
tags: [prodos/moc, topic/formal-methods, topic/knowledge-architecture, topic/mathematics, topic/software-architecture, topic/type-theory]
title: MOC - Applied Formal Methods
---

## MOC - Applied Formal Methods

> Thesis: Structure is not a representation of truth—structure _is_ truth. This MoC is the hub for all systems—software, data, infrastructure, and knowledge—that derive their correctness from the mathematical properties of their shape, not from runtime validation or narrative description.

This hub was derived from a Formal Concept Analysis of the vault's topic taxonomy. Its four levels correspond to concepts in a concept lattice, traversed from the most specific (type-theoretic foundations) to the most general (structural truth as a universal principle). See [[SoT - Formal Context (Applied Formal Methods)]] for the full derivation.

---

### The Concept Lattice (Navigation Structure)

The hierarchy below represents the _extent_ (topics covered) and _intent_ (attributes required) at each level. Moving upward adds topics by relaxing constraints; moving downward adds constraints by narrowing scope.

```
C4  (Apex)   {CI, DS, PK, DC, AM}      ←  {M4: Structural Truth, M10: Complexity Reduction}
  │           Adds: Personal OS
  │
C11          {CI, DS, DC, AM}           ←  adds M1: Deterministic/Declarative
  │           Adds: Cloud Infrastructure & IaC
  │
C12          {DS, DC, AM}              ←  adds M8: Formal Methods
  │           Adds: Data Systems & Clinical Informatics
  │
C16 (Seed)   {DS, AM}                  ←  adds ty-th: Type Theory
              Data-Centric SE + Applied Mathematics
```

Key implication derived from the lattice:

> M8 (Formal Methods) → {M1, M4, M10}
> _Any system employing formal methods is necessarily deterministic, structurally grounded, and complexity-reducing. These are not design choices—they are logical consequences._

---

### Level C16—Formal Foundations _(Seed)_

Extent: Data-Centric Software Engineering + Applied Mathematics & Formal Logic

Intent: M1 (Deterministic) · M4 (Structural Truth) · M8 (Formal Methods) · M10 (Complexity Reduction) · ty-th (Type Theory)

#### Constitutional Axioms

A note belongs at C16 if it satisfies all five of the following tests:

| # | Test | Fail signal |
|---|------|-------------|
| 1 | M1—Does this describe a system whose behaviour is _fully determined_ by its specification? | If outcomes depend on runtime state or interpretation, it belongs higher in the lattice. |
| 2 | M4—Is structure/schema the _primary carrier of truth_, not narrative or documentation? | If the truth lives in prose rather than form, it is not C16. |
| 3 | M8—Does it employ formal proof, type-theoretic reasoning, or formal verification machinery? | Informal "good practice" is C11 at best. |
| 4 | M10—Does it _demonstrate_ how formal structure absorbs or eliminates a class of complexity? | Observation without structural mechanism belongs at C12. |
| 5 | ty-th—Is Type Theory invoked as an explicit framework (not merely as a metaphor)? | Metaphorical use of types belongs at C12. |

#### Hub Notes

Satellite MoCs:

- [[MOC - Type Theory]]—The central hub. Curry-Howard, Monad pattern, HoTT, language implementations.
- [[MOC - Order Theory]]—Lattices, partial orders, subsumption. The mathematics of this hierarchy itself.
- [[MOC - The Unified Systems Paradigm]]—The synthesis: type logic governing data layout.

Core SoT Notes:

- [[SoT - The Curry-Howard Correspondence (Propositions as Types)]]—The bedrock isomorphism: _A program is a proof._
- [[SoT - Order Theory & Lattices]]—Formal definitions: posets, meet/join, Hasse diagrams.
- [[SoT - Equality in Type Theory (Intensional vs Extensional)]]—The architectural tension between semantic truth and decidability.
- [[SoT - Conservation of Complexity]]—Tesler's Law. The physical law underpinning M10.
- [[SoT - Cubical Type Theory (Computational Univalence)]]—Making the Univalence Axiom computable.
- [[SoT - Type-Driven Development (The Torvalds Loop)]]—The practical protocol: Shape → Access → Invariants → Logic.

Atomic Notes:

- [[Intuitionism Rejects the Law of the Excluded Middle]]—The constructive logic foundation.
- [[Deductive Reasoning Underwrites Mathematical Proof]]
- [[Axiomatic Set Theory Is a Foundational Framework for Mathematics]]

Planned gaps:

- `SoT - The Algebra of Types (Cardinality and Isomorphism)`
- `SoT - The Trinity of Isomorphism (Logic, Computation, Categories)`
- `SoT - Algebraic Data Types (ADTs)`

#### C16 Dataview Query

```dataview
TABLE prodos.lifecycle AS Lifecycle, prodos.trust AS Trust
FROM "30_Library"
WHERE (
  contains(tags, "type_theory") OR
  contains(tags, "type-theory") OR
  contains(tags, "formal-methods") OR
  contains(tags, "order-theory") OR
  contains(tags, "logic")
) AND prodos.kind != "moc"
SORT modified DESC
LIMIT 20
```

---

### Level C12—Formal Methods & Relational Logic

Extent: Data-Centric SE + Data Systems & Clinical Informatics + Applied Mathematics

Intent: M1 · M4 · M8 · M10 _(drops ty-th—formal methods need not be type-theoretic)_

#### Constitutional Axioms (Delta from C16)

C12 relaxes the ty-th requirement. Formal methods here may be relational (SQL, CDM schema, formal data modelling) rather than type-theoretic. The key test: is the schema _normative_ (defines valid states) rather than _descriptive_ (annotates existing ones)?

#### Hub Notes

Satellite MoCs:

- [[MOC - OHDSI & OMOP Architecture]]—Relational formal methods in practice: CDM as canonical schema.
- [[MOC - CUE Configuration]]—Lattice-based configuration: structural truth in infrastructure config.
- [[MOC - Software Architecture Principles]]—Architectural invariants as formal constraints.

Core SoT Notes:

- [[SoT - OHDSI Standardized Vocabularies]]—A large-scale ontology using subsumption (Order Theory in production).
- [[SoT - Database Internals for Systems Programmers]]—Storage as formal structure: B-Trees, MVCC, pages.
- [[SoT - High-Performance Data Structures]]—Data layout as formal specification.
- [[SoT - Core Fields of Mathematical Logic]]—The formal landscape connecting all sub-fields.
- [[SoT - Fundamentals of Mathematical Logic]]—Core axioms and proof theory.

#### C12 Dataview Query

```dataview
TABLE prodos.lifecycle AS Lifecycle
FROM "30_Library"
WHERE (
  contains(tags, "type_theory") OR
  contains(tags, "logic") OR
  contains(tags, "mathematics") OR
  contains(tags, "omop") OR
  contains(tags, "ohdsi") OR
  contains(tags, "relational-database") OR
  contains(tags, "data-modelling")
) AND prodos.kind != "moc"
SORT modified DESC
LIMIT 20
```

---

### Level C11—Deterministic Structural Systems

Extent: C12 + Cloud Infrastructure & IaC

Intent: M1 · M4 · M10 _(drops M8—formal proof machinery not required)_

#### Constitutional Axioms (Delta from C12)

C11 relaxes M8. Notes here govern systems that are _declarative and structurally grounded_ but do not require formal proof machinery. The key test: is the state file / specification the _canonical_ truth, such that divergence from it is definitionally a failure (not just unexpected behaviour)?

#### Hub Notes

Satellite MoCs:

- [[MOC - Data-Centric Infrastructure]]—Infrastructure as data: GitOps, secrets, Merkle integrity.
- [[MOC - Generative Infrastructure Configuration]]—CUE + Terraform: types governing IaC.
- [[MOC - Identity & Access Management]]—IAM as a data-processing operation; policies as formal predicates.

Core SoT Notes:

- [[SoT - Type-Driven Infrastructure Strategy]]—Terraform modules as Types: preventing configuration explosion.
- [[SoT - Data-Centric IAM in Zero Trust]]—Trust as a calculated intersection of identity, context, and resource data.
- [[SoT - The Infrastructure Witness Pattern]]—Proof-carrying code for infrastructure dependencies (IP → DNS → Cert).
- [[SoT - GitOps for IAM and Permissions]]—Permissions as temporal types (leases).
- [[SoT - Vault KV Data Structure]]—Vault as a versioned prefix trie: secrets management as structural truth.

#### C11 Dataview Query

```dataview
TABLE prodos.lifecycle AS Lifecycle
FROM "30_Library"
WHERE (
  contains(tags, "iac") OR
  contains(tags, "terraform") OR
  contains(tags, "gitops") OR
  contains(tags, "architecture") OR
  contains(tags, "data-centric")
) AND prodos.kind != "moc"
SORT modified DESC
LIMIT 20
```

---

### Level C4—Structural Truth & Complexity Reduction _(Apex)_

Extent: C11 + PKM & Personal Operating System

Intent: M4 · M10 _(only the two universal axioms remain)_

#### Constitutional Axioms

| Axiom | Statement |
|-------|-----------|
| M4—Structural Truth | The structure of a system _is_ its canonical state. Changing the structure changes the truth. |
| M10—Complexity Reduction via Structure | Structure is the _primary mechanism_ by which complexity is made manageable. Procedure follows structure; never the reverse. |

---

#### The Prefrontal Cortex Bridge

> This is where the AFM paradigm folds back on itself.

The inclusion of PK (Personal OS) at C4 is not a category error—it is the lattice _proving_ something important: the same mathematical principles that make software correct make a PKM system functional.

| Formal Methods principle | PKM equivalent |
|--------------------------|----------------|
| Types as specifications | `prodos.kind` is a type. A note's kind governs routing, lifecycle, and valid content structure. |
| Make Illegal States Unrepresentable | A HEAD note cannot be cited as a stable source. The ProdOS schema _physically encodes_ epistemic validity. |
| Conservation of Complexity (Tesler's Law) | Skipping frontmatter moves complexity into working memory. The vault is the type system for your thoughts. |
| Structural Truth (M4) | The vault's frontmatter schema IS the canonical description of a note's state. The prose is secondary. |
| Parse, Don't Validate | Capture goes to `00_Inbox/` (raw, untyped). Triage converts it to a typed note. |

The bridge axiom: _The vault is a formal system. The ProdOS schema is its type system. The Chronos Synthesis protocol is its type-driven development loop. The zettelkasten is its canonical data model._

See [[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]] for the full philosophical argument.

#### Hub Notes

Satellite MoCs:

- [[MOC - ProdOS]]—The operational specification of the vault as a formal system.
- [[MOC - PKM as Process vs Product]]—The meta-reflection on knowledge architecture.
- [[MOC - From Information to Knowledge]]—The transformation pipeline (capture → structure → synthesis).
- [[MOC - Data-Centric Software Engineering]]—The mother MoC for the "Structure is Truth" paradigm.

Core SoT Notes:

- [[SoT - The Data-Centric Philosophy]]—"Data Dominates Code." The axiom that grounds all C4 content.
- [[SoT - Conservation of Complexity]]—The universal law. Applies to software _and_ cognition.
- [[SoT - Knowledge Architecture (Associative Ontology)]]—Tags as lattice values; the vault's ontology as a partial order.
- [[SoT - ProdOS Frontmatter Contract (Note Type Schemas)]]—The type specification for vault notes.
- [[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]]—The keystone note for this entire MoC.

#### C4 Dataview Query

```dataview
TABLE prodos.kind AS Kind, prodos.lifecycle AS Lifecycle, prodos.trust AS Trust
FROM "30_Library"
WHERE (
  prodos.lifecycle = "evergreen" OR prodos.trust = "authoritative"
) AND (
  contains(tags, "architecture") OR
  contains(tags, "pkm") OR
  contains(tags, "prodos") OR
  contains(tags, "data-centric")
)
SORT prodos.trust DESC, modified DESC
LIMIT 20
```

---

### Cross-Links: The Human/Cognitive Civilisation

The FCA lattice identified two bridge concepts connecting the AFM "Deterministic/Engineering" civilisation to the "Human/Cognitive" civilisation. These are structurally derived, not thematic.

#### Bridge Point 1—C4 ↔ C13 via PK

C13 = ({AC, PK, PR} | {M3 External Scaffolding, M9 Cognitive Architecture})

PK sits in both C4 and C13. The vault is simultaneously a formal system (M4, M10) and an external cognitive scaffold (M3, M9).

Cross-link: [[MOC - ADHD Functional Neurology & Scaffolding]]

#### Bridge Point 2—Conservation of Complexity

C15 = ({AC, PR} | {M3, M7, M9})—Human Resilience Systems

| Domain | Complexity source | Structure that absorbs it |
|--------|------------------|---------------------------|
| Software (C16) | Runtime validation failure | Type system |
| IaC (C11) | Manual configuration drift | Declarative state file |
| Clinical data (C12) | Heterogeneous source schemas | OMOP CDM |
| PKM (C4) | Cognitive overload / context loss | ProdOS schema + zettelkasten |
| ADHD (C13/C15) | Executive function failure | External scaffolding |

Cross-link notes:

- [[MOC - ADHD Functional Neurology & Scaffolding]]
- [[MOC - Project Continuity]]
- [[MOC - The One Degree Change Framework for ADHD]]

---

### Planned Notes (Gaps Identified by This Analysis)

| Note                                                                       | Level  | Type   | Rationale                                                                      |
| -------------------------------------------------------------------------- | ------ | ------ | ------------------------------------------------------------------------------ |
| `SoT - The Algebra of Types (Cardinality and Isomorphism)`                 | C16    | SoT    | Arithmetic of data shapes; flagged in [[MOC - The Unified Systems Paradigm]]   |
| `SoT - The Trinity of Isomorphism (Logic, Computation, Categories)`        | C16    | SoT    | The Rosetta Stone note; flagged in [[MOC - The Unified Systems Paradigm]]      |
| `SoT - Infrastructure as Formal Specification`                             | C11    | SoT    | Unifying thesis for IaC at the AFM level                                       |
| `Complexity Conservation Applies to Cognitive Systems as Well as Software` | Bridge | Atomic | The bridge claim between AFM and Human/Cognitive civilisations                 |
| `The Vault's Frontmatter Schema is a Type System for Knowledge`            | C4     | Atomic | The Prefrontal Cortex Bridge as a standalone vault-specific claim              |
| `Cognitive Scaffolds Are Constitutive but Lack Formal Closure`             | C13    | Atomic | T2 from [[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]] |

---

### Related MoCs

| MoC | Lattice Level | Relationship |
|-----|--------------|--------------|
| [[MOC - Type Theory]] | C16 | Satellite hub—type-theoretic core |
| [[MOC - Order Theory]] | C16 | Satellite hub—the mathematics of this hierarchy |
| [[MOC - The Unified Systems Paradigm]] | C16–C11 | Peer hub—synthesis of type logic and data physics |
| [[MOC - Data-Centric Software Engineering]] | C16–C4 | Peer hub—"Structure is Truth" paradigm hub |
| [[MOC - Data-Centric Infrastructure]] | C11 | Satellite hub—IaC and declarative infrastructure |
| [[MOC - OHDSI & OMOP Architecture]] | C12 | Satellite hub—relational formal methods in practice |
| [[MOC - CUE Configuration]] | C12–C11 | Satellite hub—lattice-based config language |
| [[MOC - ProdOS]] | C4 | Satellite hub—vault as formal system |
| [[MOC - Formal Logic & Philosophy (Triage)]] | C16 | Partially superseded (technical arm); philosophy arm retained |
| [[MOC - ADHD Functional Neurology & Scaffolding]] | Bridge (C13) | Cross-civilisation bridge—cognitive scaffolding equivalent |

%%[depends_on:: [[SoT - Formal Context (Applied Formal Methods)]], strength=5, confidence=high]%%
