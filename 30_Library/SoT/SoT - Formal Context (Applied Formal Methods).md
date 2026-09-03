---
aliases: [AFM Formal Context, FCA Matrix, Topic Concept Lattice]
conformant: false
created: 2026-04-19T09:00:00+00:00
modified: 2026-08-29T09:36:37+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-formal-context-applied-formal-methods
see_also: ["[[MOC - Applied Formal Methods]]", "[[Protocol - AFM Vault Constitutional Triage]]", "[[SoT - Order Theory & Lattices]]", "[[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]]"]
tags: [fca/attr/m10, fca/attr/m4, fca/level/c4, prodos/sot, topic/formal-methods, topic/knowledge-architecture, topic/mathematics, topic/pkm]
title: SoT - Formal Context (Applied Formal Methods)
type: sot
---

## SoT—Formal Context (Applied Formal Methods)

### Minimum Viable Understanding (MVU)

This note records the Formal Concept Analysis (FCA) of the vault's 11 core topic domains. The analysis produced the [[MOC - Applied Formal Methods]] concept lattice, the [[Protocol - AFM Vault Constitutional Triage]], and the keystone note [[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]]. It is preserved here as a canonical artefact so the lattice can be extended or revised without reconstructing the derivation from scratch.

Source data: `gemini-scribe/scripts/topics_whitelist.json` · Analysis date: 2026-04-19

---

### 1. The Formal Context: Objects

#### Objects (G)—11 Topic Domains

| ID | Topic |
|----|-------|
| CI | Cloud Infrastructure & IaC |
| PE | Platform Engineering & Containers |
| NE | Network Engineering |
| DS | Data-Centric Software Engineering |
| AL | AI Engineering & LLM Systems |
| AC | ADHD & Cognitive Scaffolding |
| PK | PKM & Personal Operating System |
| DC | Data Systems & Clinical Informatics |
| AM | Applied Mathematics & Formal Logic |
| PR | Philosophy, Meaning & Resilience |
| HE | Health & Endurance |

---

### 2. Phase 1—Original Keyword Context (Sparse)

The initial formal context was derived from the `keywords` arrays in `topics_whitelist.json`. After normalising `kubernetes` + `k8s` → single attribute, the result was:

- |G| = 11 · |M| = 81 · Density = 9.1%
- Shared attributes: 1 (`type-theory`, shared by DS and AM only)
- Singleton-extent attributes: 80 (98.8%)

Finding: The original keyword taxonomy functions as a labelling system, not a concept lattice. It returns an almost-flat structure—11 leaf concepts and one interior concept. No meaningful hierarchy can be derived.

---

### 3. Phase 2—Meta-Attribute Enrichment

To scale the context, 10 higher-order meta-attributes were synthesised from the topic _description_ fields (not keywords). Each attribute is present in at least two topics.

#### Meta-Attribute Definitions

| ID | Name | Derivation from descriptions |
|----|------|------------------------------|
| M1 | Deterministic / Declarative Systems | CI "declarative"; GitOps "declarative"; NE "systematic diagnostic"; DS "types as proofs"; AL "deterministic software systems"; DC "structural conventions"; AM "formal verification"; PR "mental models as algorithms"; HE "engineering problem" |
| M2 | Probabilistic / Stochastic Systems | AL "probabilistic AI models"; AC "biological constraints"; HE "physiological modelling" |
| M3 | External Scaffolding | PE "platform scaffolds delivery"; AC "external scaffolding required to thrive" (explicit); PK "vault as externalised prefrontal cortex" (explicit); PR "philosophical scaffolding" (explicit) |
| M4 | Structural Truth / Canonical Schema | CI "IaC as infra ground-truth"; DS "'Structure is Truth'" (explicit); PK "synthesis to canonical knowledge"; DC "OMOP CDM … structural conventions"; AM "underlying mathematical order" |
| M5 | Distributed State | CI "hybrid environments"; PE "namespaces to clusters"; NE "distributed state transport as first-class discipline" (explicit); DC "distributed data systems" (explicit) |
| M6 | Orchestration & Automation | CI "IaC automation"; PE "container orchestration, GitOps pipelines" (explicit); AL "orchestration architecture" (explicit); PK "raw capture → executable action"; DC "ETL pipelines" |
| M7 | Optimisation & Resilience | NE "systematic diagnostic methodology"; AC "thrive despite constraints"; PR "algorithms for resilience" (explicit); HE "long-term vitality optimisation" (explicit) |
| M8 | Formal Methods & Type Theory | DS "types as mathematical proofs of correctness"; DC "CDM as formal relational schema"; AM "type-theoretic foundations … formal verification" (explicit) |
| M9 | Cognitive / Context Architecture | AL "context curation … cognitive bridge" (explicit); AC "understanding the ADHD operating system"; PK "personal operating system … externalised prefrontal cortex"; PR "mental models as algorithms" |
| M10 | Complexity Reduction via Structure | CI "declarative reduces ops complexity"; PE "namespaces to clusters = abstraction ladder"; DS "structure as primary lever for complexity reduction" (explicit); PK "raw capture through synthesis to canonical knowledge"; DC "CDM reduces clinical data heterogeneity"; AM "underlying mathematical order of systems" |
| ty-th | Type Theory _(retained bridge)_ | DS + AM (original shared attribute from Phase 1) |

#### Enriched Incidence Matrix

| Object | M1 | M2 | M3 | M4 | M5 | M6 | M7 | M8 | M9 | M10 | ty-th |
|--------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:-----:|
| CI | X |   |   | X | X | X |   |   |   | X  |      |
| PE | X |   | X |   | X | X |   |   |   | X  |      |
| NE | X |   |   |   | X |   | X |   |   |    |      |
| DS | X |   |   | X |   |   |   | X |   | X  | X    |
| AL | X | X |   |   |   | X |   |   | X |    |      |
| AC |   | X | X |   |   |   | X |   | X |    |      |
| PK |   |   | X | X |   | X |   |   | X | X  |      |
| DC | X |   |   | X | X | X |   | X |   | X  |      |
| AM | X |   |   | X |   |   |   | X |   | X  | X    |
| PR | X |   | X |   |   |   | X |   | X |    |      |
| HE | X | X |   |   |   |   | X |   |   |    |      |

Density after enrichment: 49 / 121 = 40.5%

---

### 4. The Three Governing Implications

Derived by inspecting which attributes co-occur across all objects satisfying each trigger:

```
I1:  ty-th       →  { M1, M4, M8, M10 }
I2:  M8          →  { M1, M4, M10 }
I3:  { M5, M6 }  →  { M1, M10 }
```

I1 verified: DS (M1 ✓, M4 ✓, M8 ✓, M10 ✓), AM (M1 ✓, M4 ✓, M8 ✓, M10 ✓)

I2 verified: DS ✓, DC ✓, AM ✓—all carry M1, M4, M10

I3 verified: CI ✓, PE ✓, DC ✓—all objects with both M5 and M6 carry M1 and M10

Additional implication from C16 discriminator analysis:

```
I4:  M-sub   →  ¬M-axiom    (computational substrate precludes axiomatic independence)
I5:  M-axiom →  ¬M-sub
```

---

### 5. Key Formal Concepts

Pairs (A, B) where A′ = B and B′ = A. Listed from most general to most specific.

| # | Label | Extent A | Intent B |
|---|-------|----------|----------|
| C0 | Top | {all 11} | {} |
| C1 | Deterministic Systems | {CI, PE, NE, DS, AL, DC, AM, PR, HE} | {M1} |
| C2 | Complexity Reduction | {CI, PE, DS, PK, DC, AM} | {M10} |
| C3 | Orchestration | {CI, PE, AL, PK, DC} | {M6} |
| C4 | Structural Truth + Complexity | {CI, DS, PK, DC, AM} | {M4, M10} |
| C5 | Distributed Infrastructure | {CI, PE, NE, DC} | {M1, M5} |
| C6 | Optimisation / Resilience | {NE, AC, PR, HE} | {M7} |
| C7 | External Scaffolding | {PE, AC, PK, PR} | {M3} |
| C8 | Cognitive Architecture | {AL, AC, PK, PR} | {M9} |
| C9 | Probabilistic Systems | {AL, AC, HE} | {M2} |
| C10 | Infrastructure Automation | {CI, PE, DC} | {M1, M5, M6, M10} |
| C11 | Deterministic + Structural | {CI, DS, DC, AM} | {M1, M4, M10} |
| C12 | Formal Methods Cluster | {DS, DC, AM} | {M1, M4, M8, M10} |
| C13 | Scaffolded Cognition | {AC, PK, PR} | {M3, M9} |
| C14 | Probabilistic Cognition | {AL, AC} | {M2, M9} |
| C15 | Human Resilience Systems | {AC, PR} | {M3, M7, M9} |
| C16 | Formal Foundations (Type Theory) | {DS, AM} | {M1, M4, M8, M10, ty-th} |
| C17 | Bottom | {} | {all 11 attributes} |

_Concepts in bold are the four levels of [[MOC - Applied Formal Methods]]._

---

### 6. The Three Civilisations

The lattice reveals three structurally distinct clusters identified by dominant attribute co-occurrence:

| Civilisation | Topics | Key Attributes | Hub concepts |
|--------------|--------|---------------|--------------|
| Deterministic / Engineering | CI, PE, NE, DS, DC, AM | M1, M4, M8, M10 | C11, C12, C16 |
| Human / Cognitive | AC, PK, PR, AL | M3, M9 | C7, C8, C13 |
| Probabilistic / Embodied | AL, AC, HE | M2 | C9 |

AL bridges all three. It holds M1 (deterministic software), M2 (probabilistic AI), M6 (orchestration), and M9 (cognitive architecture).

PK bridges Deterministic and Cognitive. It shares M4, M10 with the Engineering cluster (C4) while sharing M3, M9 with the Cognitive cluster (C13).

---

### 7. C16 Collision Resolution: DS Vs AM

DS and AM had identical intents at C16, making them formally indistinguishable without additional attributes.

Discriminating attributes proposed:

| Attribute | Definition | DS | AM |
|-----------|------------|:--:|:--:|
| M-sub (Computational Substrate) | Realization requires a computational or physical substrate | YES | NO |
| M-axiom (Axiomatic Independence) | Derivable from first-principles axioms without substrate reference | NO | YES |

Evolved C16 sub-concepts:

```
C16      ({DS, AM},  {M1, M4, M8, M10, ty-th})             ← join — unchanged
  ├── C16-DS  ({DS},  {M1, M4, M8, M10, ty-th, M-sub})     ← Computational TT
  └── C16-AM  ({AM},  {M1, M4, M8, M10, ty-th, M-axiom})   ← Pure Formal Logic
```

In practice: DS notes (Rust ownership, DOD, Torvalds Loop) carry `discriminator: computational`; AM notes (category theory, order theory, set theory) carry `discriminator: pure-abstract`. Notes at the join (Type Theory as a subject bridging both) leave the discriminator unset.

---

### 8. Concept Lattice Sketch (AFM Path)

```
       ⊤  (all 11 objects, empty intent)
       │
    C1 {M1}          C2 {M10}       C6 {M7}    C7 {M3}   C8 {M9}   C9 {M2}
   (9 objs)          (6 objs)       (4 objs)   (4 objs)  (4 objs)  (3 objs)
       │                 │                          \      /             │
    C5 {M1,M5}     C4 {M4,M10}  ◄── AFM APEX    C13 {M3,M9}       C14 {M2,M9}
    (4 objs)       (5 objs)                      (3 objs)           (2 objs)
       │                 │                            │                  │
    C10 {M1,M5,M6,M10}  C11 {M1,M4,M10}         C15 {M3,M7,M9}      (AL,AC)
    (CI,PE,DC)          (CI,DS,DC,AM)             (AC,PR)
                             │
                        C12 {M1,M4,M8,M10}
                         (DS,DC,AM)
                             │
                        C16 {M1,M4,M8,M10,ty-th}
                          (DS,AM)  ◄── deepest shared concept
                         /         \
                    C16-DS         C16-AM
                  (DS, +M-sub)   (AM, +M-axiom)
                         │
                         ⊥
```

[supports:: [[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]], strength=5, confidence=high]
