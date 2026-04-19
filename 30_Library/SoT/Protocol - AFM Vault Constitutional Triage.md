---
aliases: [AFM Triage Protocol, FCA Metadata Linter, Vault Constitutional Protocol]
created: 2026-04-19T10:30:00+01:00
modified: 2026-04-19T18:30:29+00:00
see_also: ["[[MOC - Applied Formal Methods]]", "[[SoT - Conservation of Complexity]]", "[[SoT - Order Theory & Lattices]]", "[[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]]"]
tags: [fca/constitutional, prodos/protocol, topic/formal-methods, topic/pkm, topic/prodos]
title: Protocol - AFM Vault Constitutional Triage
---

## Protocol—AFM Vault Constitutional Triage

### Logic Map

- Objective: Assign any incoming note with formal-methods content to its correct concept-lattice level (C16 → C4) and verify that its metadata satisfies the structural integrity constraints implied by that level.
- Foundation: Three FCA implications derived from the vault's topic taxonomy. Violations are _type errors_—not style violations.
- Dependency: Requires [[MOC - Applied Formal Methods]] and [[SoT - ProdOS Note Metadata (Frontmatter)]].
- Derivation: See [[SoT - Formal Context (Applied Formal Methods)]] for the full FCA analysis.

---

### Part I—Axiom Registry

The six attributes that constitute the AFM lattice. Every triage decision is reducible to the presence or absence of these.

| ID | Name | Binary Test |
|----|------|-------------|
| M1 | Deterministic / Declarative | _Does this note describe a system whose outputs are fully determined by its specification, with no runtime variance?_ |
| M2 | Probabilistic / Stochastic | _Does this note reason about systems with inherent statistical or biological variance?_ |
| M4 | Structural Truth | _Is structure / schema the primary carrier of truth—not narrative, documentation, or convention?_ |
| M8 | Formal Methods | _Does this note employ at least one formal proof technique, type-theoretic construction, or formal relational schema as its method (not merely its subject)?_ |
| M10 | Complexity Reduction via Structure | _Does this note identify a class of complexity that the formal structure eliminates—not merely organises?_ |
| ty-th | Type Theory | _Is type theory invoked as an explicit framework—Curry-Howard, dependent types, linear logic, HoTT—not as a metaphor?_ |

Derived discriminators (C16 only):

| ID | Name | Binary Test |
|----|------|-------------|
| M-sub | Computational Substrate | _Is the formal system's realization dependent on a computational or physical substrate?_ |
| M-axiom | Axiomatic Independence | _Does the formal system derive from first-principles axioms without reference to any substrate?_ |

#### The Three Governing Implications

These are logical consequences of the FCA analysis—not heuristics. Violating them in metadata is a type error.

```
I1:  ty-th      →  { M1, M4, M8, M10 }
I2:  M8         →  { M1, M4, M10 }
I3:  {M5, M6}   →  { M1, M10 }
I4:  M-sub      →  ¬M-axiom
I5:  M-axiom    →  ¬M-sub
```

---

### Part II—Triage Protocol

Pre-condition: Note has been captured in `00_Inbox/` and is ready for triage.

#### Phase A—AFM Routing Gate

- [ ] A1. Read the note's first paragraph and abstract section entirely.
- [ ] A2. Ask: _Does this note reason about structure, formal systems, types, schemas, or declarative specifications?_
  - If NO on all: STOP. Route to a different MoC. This note is not AFM.
  - If YES on any: proceed to Phase B.

---

#### Phase B—Level Assignment (deepest Valid Level first)

##### B1—Test For C16 (Type-Theoretic Core)

- [ ] B1a. Does the note invoke ty-th—type theory as an explicit framework?
  - Test: Is there reference to Curry-Howard, dependent types, affine/linear types, HoTT, Univalence, or a formal type judgement of the form `Γ ⊢ e: T`?
  - If NO: skip to B2.
  - If YES: proceed.
- [ ] B1b. Verify implication I1 is satisfied—check all four are present:
  - [ ] M1 present? (System deterministic by specification)
  - [ ] M4 present? (Structure is the canonical truth-bearer)
  - [ ] M8 present? (Formal proof or construction used as method)
  - [ ] M10 present? (A class of complexity is structurally eliminated)
  - If all YES: ASSIGN C16. Proceed to Phase C (SIT-C16).
  - If any NO: TYPE ERROR—I1 VIOLATION. See §VI, Resolution R-I1.

##### B2—Test For C12 (Formal Methods & Relational Logic)

- [ ] B2a. Does the note employ M8—formal methods as its primary method?
  - Test: Is there a formal schema specification (CDM, relational model), a proof by construction, a formal grammar, or formal verification claim—used as _method_, not merely as subject matter?
  - If NO: skip to B3.
  - If YES: proceed.
- [ ] B2b. Verify implication I2 is satisfied:
  - [ ] M1 present?
  - [ ] M4 present?
  - [ ] M10 present?
  - If all YES: ASSIGN C12. Proceed to Phase C (SIT-C12).
  - If any NO: TYPE ERROR—I2 VIOLATION. See §VI, Resolution R-I2.

##### B3—Test For C11 (Deterministic Structural Systems)

- [ ] B3a. Does the note satisfy M1—fully declarative/deterministic specification?
  - Test: Is the system state expressible as a specification file, schema, or formal declaration that _precedes_ any implementation?
  - If NO: skip to B4.
  - If YES: proceed.
- [ ] B3b. Does the note also satisfy M4—structure as canonical ground truth?
  - Test: Is the specification file / schema / declaration _the_ truth (not a description of truth held elsewhere)?
  - If NO: skip to B4.
  - If YES: proceed.
- [ ] B3c. Does the note satisfy M10?
  - If YES: ASSIGN C11. Proceed to Phase C (SIT-C11).
  - If NO: WARN—M10 absent. Add a "Structural Payoff" section to the note. If M10 genuinely cannot be established, fall through to B4.

##### B4—Test For C4 (Structural Truth & Complexity Reduction—Apex)

- [ ] B4a. Does the note satisfy M4 (structural truth)?
- [ ] B4b. Does the note satisfy M10 (complexity reduction)?
  - If both YES: ASSIGN C4. Proceed to Phase C (SIT-C4).
  - If M4 only (no M10): Note is incomplete. Add complexity payoff. Re-triage.
  - If neither: NOT AFM. Route to other MoC.

---

#### Phase C—Structural Integrity Test + Finalisation

- [ ] C1. Run the appropriate SIT from §V for the assigned level.
- [ ] C2. Set `prodos.fca.sit_passed: true` in frontmatter if all assertions pass.
- [ ] C3. Apply the correct YAML Linter Template from §IV.
- [ ] C4. Update the appropriate satellite MoC with a backlink to this note.
- [ ] C5. If C16 assigned, set `prodos.fca.discriminator` (computational / pure-abstract / leave unset for join).

---

### Part III—Implication Rules (Linter Specification)

Tags are either PRIMARY (manually asserted, triggers implication rules) or CALCULATED (derived and auto-inserted). Primary tags trigger rules; calculated tags must be present whenever their trigger is.

```
RULE r-ty-th  [Trigger: topic/type-theory]
  WHEN  "topic/type-theory" ∈ tags
  THEN  add: fca/attr/m1, fca/attr/m4, fca/attr/m8, fca/attr/m10
  AND   set fca.level: c16
  AND   set fca.calculated_attrs: [m1, m4, m8, m10]

RULE r-m8  [Trigger: topic/formal-methods | topic/relational-schema | topic/cdm]
  WHEN  ("topic/formal-methods" OR "topic/relational-schema" OR "topic/cdm") ∈ tags
  AND   "topic/type-theory" ∉ tags
  THEN  add: fca/attr/m1, fca/attr/m4, fca/attr/m10
  AND   set fca.level: c12
  AND   set fca.calculated_attrs: [m1, m4, m10]

RULE r-m5m6  [Trigger: topic/distributed-systems AND topic/orchestration]
  WHEN  "topic/distributed-systems" AND "topic/orchestration" ∈ tags
  AND   "topic/formal-methods" ∉ tags
  AND   "topic/type-theory" ∉ tags
  THEN  add: fca/attr/m1, fca/attr/m10
  AND   set fca.level: c11
  AND   set fca.calculated_attrs: [m1, m10]
```

#### Linter Error Codes

| Code | Condition | Severity |
|------|-----------|----------|
| `E-IMPL-I1` | `topic/type-theory` present but any of `{fca/attr/m1, fca/attr/m4, fca/attr/m8, fca/attr/m10}` absent | ERROR |
| `E-IMPL-I2` | `topic/formal-methods` present but any of `{fca/attr/m1, fca/attr/m4, fca/attr/m10}` absent | ERROR |
| `E-IMPL-I3` | Both distributed-systems + orchestration present but `fca/attr/m1` or `fca/attr/m10` absent | ERROR |
| `W-LEVEL-UP` | Note is filed at level X but passes tests for a more specific level | WARN |
| `W-M2-CONTAMINATION` | `fca/attr/m2` present in a note at C16 | WARN |
| `E-NO-M10` | `fca/attr/m4` present but `fca/attr/m10` absent and no `sit_notes` explaining the omission | ERROR |
| `I-MISSING-DISCRIM` | Note assigned C16 but `fca.discriminator` not set | INFO |

---

### Part IV—YAML Linter Templates

#### Template: C16—Formal Foundations

```yaml
tags:
  # PRIMARY (manually assert at least one trigger)
  - topic/type-theory          # ty-th trigger → fires r-ty-th
  # CALCULATED (auto-derived by r-ty-th; do not remove)
  - fca/attr/m1                # M1 ← implied by ty-th (I1)
  - fca/attr/m4                # M4 ← implied by ty-th (I1)
  - fca/attr/m8                # M8 ← implied by ty-th (I1)
  - fca/attr/m10               # M10 ← implied by ty-th (I1)
  - fca/level/c16
prodos:
  kind: "[atomic | sot]"
  lifecycle: "[seedling | active | stable | evergreen]"
  trust: "[low | working | stable | authoritative]"
  fca:
    level: c16
    discriminator: "[computational | pure-abstract]"  # REQUIRED at C16
    primary_attrs: [ty-th]
    calculated_attrs: [m1, m4, m8, m10]
    sit_passed: false
    sit_notes: ""
```

#### Template: C12—Formal Methods & Relational Logic

```yaml
tags:
  # PRIMARY
  - topic/formal-methods       # M8 trigger → fires r-m8
  # CALCULATED
  - fca/attr/m1                # M1 ← implied by M8 (I2)
  - fca/attr/m4                # M4 ← implied by M8 (I2)
  - fca/attr/m8
  - fca/attr/m10               # M10 ← implied by M8 (I2)
  - fca/level/c12
prodos:
  fca:
    level: c12
    primary_attrs: [m8]
    calculated_attrs: [m1, m4, m10]
    sit_passed: false
    sit_notes: ""
```

#### Template: C11—Deterministic Structural Systems

```yaml
tags:
  # PRIMARY
  - topic/iac                  # or: topic/gitops, topic/declarative-config
  - topic/distributed-systems  # M5 — if also M6 present, fires r-m5m6
  - topic/orchestration        # M6
  # CALCULATED
  - fca/attr/m1                # M1 ← from declarative framing + r-m5m6
  - fca/attr/m4                # M4 — manually confirmed in SIT
  - fca/attr/m10               # M10 ← implied by {M5+M6} via I3
  - fca/level/c11
prodos:
  fca:
    level: c11
    primary_attrs: [m1, m4]
    calculated_attrs: [m10]
    sit_passed: false
    sit_notes: ""
```

#### Template: C4—Structural Truth & Complexity Reduction (Apex)

```yaml
tags:
  # PRIMARY
  - topic/pkm                  # or: topic/software-architecture, topic/data-centric
  # CALCULATED
  - fca/attr/m4                # M4 — manually confirmed
  - fca/attr/m10               # M10 — manually confirmed
  - fca/level/c4
  # Add if M2 content present as subject matter:
  # - fca/m2-framed
prodos:
  fca:
    level: c4
    primary_attrs: [m4, m10]
    calculated_attrs: []
    sit_passed: false
    sit_notes: ""
```

---

### Part V—Structural Integrity Tests

#### SIT-C16

All 6 assertions must hold. Any failure is a type error.

```
ASSERT-1 [ty-th genuine]:
  The note contains at least one formal type judgement, inference rule,
  or explicit invocation of a named type-theoretic framework
  (Curry-Howard, HoTT, dependent types, linear logic, MLTT, CIC).
  FAIL → TYPE ERROR: TYPE_THEORY_COSPLAY

ASSERT-2 [M1 satisfied]:
  Every claim is derivable from a fixed, closed specification.
  No claim depends on runtime state, measurement, or empirical observation.
  FAIL → TYPE ERROR: DETERMINISM_BREACH

ASSERT-3 [M4 satisfied]:
  The note's primary truth-bearer is a structural artefact
  (type signature, formal definition, schema, axiom set) —
  not narrative prose or informal argument.
  FAIL → TYPE ERROR: DOCUMENTATION_FALLACY

ASSERT-4 [M8 satisfied]:
  The note constructs or applies at least one formal proof,
  type-theoretic derivation, or verified schema.
  Describing formal methods ≠ using formal methods.
  FAIL → TYPE ERROR: PSEUDO_FORMALISM

ASSERT-5 [M10 satisfied]:
  The note identifies at least one class of complexity or failure mode
  that the formal structure makes structurally impossible.
  FAIL → TYPE ERROR: COMPLEXITY_DEBT

ASSERT-6 [¬M2]:
  The note contains no probabilistic reasoning used as method.
  Probabilistic content may appear as quarantined subject matter
  (tagged fca/m2-framed) but must not drive any conclusion.
  FAIL → TYPE ERROR: PROBABILISTIC_CONTAMINATION
```

#### SIT-C12

```
ASSERT-1 [M8 genuine]:
  The note applies formal methods — not merely references them.
  A formal schema is normative (prescribes valid states);
  documentation is descriptive (describes existing states).
  FAIL → TYPE ERROR: DOCUMENTATION_FALLACY

ASSERT-2 [M1 satisfied]:
  The formal system's outputs are fully determined by its specification.
  FAIL → TYPE ERROR: DETERMINISM_BREACH

ASSERT-3 [M4 satisfied]:
  Schema / CDM / formal grammar is the *source* of truth,
  not a representation of truth held in code or documentation.
  FAIL → TYPE ERROR: DOCUMENTATION_FALLACY

ASSERT-4 [M10 satisfied]:
  The formal schema demonstrably reduces heterogeneity, ambiguity,
  or a class of integration errors.
  FAIL → TYPE ERROR: COMPLEXITY_DEBT

ASSERT-5 [not C16]:
  If ty-th is detected, promote to C16.
  FAIL → TYPE ERROR: UNDER_CLASSIFICATION
```

#### SIT-C11

```
ASSERT-1 [M1 satisfied]:
  The system state is expressed as a declarative specification
  that precedes any implementation.
  Procedural steps ("how to run") are OPERATIONAL, not C11.
  FAIL → TYPE ERROR: OPERATIONAL_CONTAMINATION

ASSERT-2 [M4 satisfied]:
  The specification file / state definition IS the canonical system state.
  If manual configuration is the ground truth, M4 fails.
  FAIL → TYPE ERROR: CONFIGURATION_DRIFT_PATTERN

ASSERT-3 [M10 satisfied]:
  The declarative architecture absorbs at least one class of
  operational complexity.
  FAIL → TYPE ERROR: COMPLEXITY_DEBT

ASSERT-4 [not C12, not C16]:
  If M8 or ty-th detected, promote accordingly.
  FAIL → TYPE ERROR: UNDER_CLASSIFICATION
```

#### SIT-C4

```
ASSERT-1 [M4 satisfied]:
  Structure / schema / note-kind is the primary carrier of truth.
  FAIL → TYPE ERROR: STRUCTURAL_NOMINALISM

ASSERT-2 [M10 satisfied]:
  The structural choice demonstrably absorbs cognitive, epistemic,
  or operational complexity.
  FAIL → TYPE ERROR: STRUCTURE_WITHOUT_PAYOFF

ASSERT-3 [M2 framing — advisory]:
  If M2 content is present, it must be tagged fca/m2-framed
  and used as subject matter only — not as explanatory method.
  FAIL → WARN: STOCHASTIC_OVERRIDE

ASSERT-4 [C4 not trivially satisfied]:
  The note makes a specific structural claim, not a meta-commentary
  about the value of structure.
  FAIL → TYPE ERROR: STRUCTURAL_NOMINALISM
```

---

### Part VI—Type Error Taxonomy & Resolution

| Code | Description | Resolution |
|------|-------------|------------|
| TYPE_THEORY_COSPLAY | ty-th claimed but no formal construction present | Demote to C12. Replace metaphorical references with formal constructions, or accept M8 without ty-th. |
| DETERMINISM_BREACH | M1 claimed but probabilistic or empirical content is load-bearing | Quarantine stochastic content to a companion note linked via `see_also`. Demote level to wherever M1 is no longer required. |
| PROBABILISTIC_CONTAMINATION | M2 content drives conclusions at C16 | Extract M2 reasoning to a note tagged `fca/m2-quarantined`. C16 note retains only deterministic structure. Cross-link the pair. |
| DOCUMENTATION_FALLACY | Schema described as annotation of truth held elsewhere | Rewrite schema as normative: it must _define_ valid states, not _describe_ existing ones. If impossible, demote to C4. |
| PSEUDO_FORMALISM | M8 claimed but only informal best-practice reasoning | Demote to C11. If formal proof is the genuine intent, add the missing construction before re-triaging. |
| COMPLEXITY_DEBT | Formal structure present but M10 payoff undemonstrated | Add a "Structural Payoff" section: "This structure makes the following class of error structurally impossible: …" |
| UNDER_CLASSIFICATION | Note filed at X but passes tests for a more specific level | Promote. Re-run SIT at higher level. Update `fca.level` and hub MoC backlinks. |
| OPERATIONAL_CONTAMINATION | Procedural steps mixed with declarative specification at C11 | Extract procedural steps to an `ops` note. C11 note retains only the declarative state description. |
| CONFIGURATION_DRIFT_PATTERN | IaC described but manual configuration remains ground truth | Structural fix: enforce IaC-as-truth in the system. If aspirational, demote to C4 and note in `sit_notes`. |
| STRUCTURAL_NOMINALISM | Note talks _about_ structure without instantiating a structural claim | Rewrite to make a specific structural invariant, not a general claim about structure's value. |
| STOCHASTIC_OVERRIDE | M2 content at C4 drives conclusions | Add `fca/m2-framed` tag. Ensure M4 structural claim is the note's _conclusion_, not a framing device. |

---

### Part VII—Collision Resolution: DS ↔ AM at C16

#### The Problem

DS (Data-Centric SE) and AM (Applied Mathematics) originally had identical intents at C16—making them formally indistinguishable. A note cannot be unambiguously classified as computational type theory vs pure formal logic without additional discriminating attributes.

#### Discriminating Attributes

M-sub—Computational Substrate Dependency

> A formal system has M-sub if its realization requires a computational or physical substrate.

- DS = YES. Rust ownership rules are enforced by the _compiler_. Data-Oriented Design is grounded in _cache line physics_. The formal system cannot exist without a substrate.
- AM = NO. Category theory, order theory, and set theory are substrate-independent. A lattice is a lattice in Haskell, SQL, chalk on a board, or nowhere.

M-axiom—Axiomatic Independence

> A formal system has M-axiom if its validity is derivable from first-principles axioms without reference to any substrate.

- AM = YES. Order Theory's axioms (reflexivity, antisymmetry, transitivity) are formally closed.
- DS = NO. Data-Oriented Design is empirically grounded in hardware behaviour.

#### Evolved Lattice Structure

```
Before: C16 = ({DS, AM}, {M1, M4, M8, M10, ty-th})   ← DS and AM indistinguishable

After:
C16      ({DS, AM},  {M1, M4, M8, M10, ty-th})         ← shared abstract core, unchanged
  ├── C16-DS  ({DS}, {M1, M4, M8, M10, ty-th, M-sub})  ← Computational TT leaf
  └── C16-AM  ({AM}, {M1, M4, M8, M10, ty-th, M-axiom}) ← Pure Formal Logic leaf
```

New implications: I4: M-sub → ¬M-axiom and I5: M-axiom → ¬M-sub. No note can hold both.

#### Discriminator Field Values

| Value | Meaning | Example notes |
|-------|---------|---------------|
| `computational` | M-sub: substrate-dependent | [[SoT - Rust's Ownership Model]], [[SoT - Type-Driven Development (The Torvalds Loop)]], [[SoT - Data-Oriented Design]] |
| `pure-abstract` | M-axiom: substrate-independent | [[SoT - Order Theory & Lattices]], [[SoT - The Curry-Howard Correspondence (Propositions as Types)]] |
| _(unset)_ | Sits at C16 join—bridges both | [[MOC - Type Theory]], [[SoT - Conservation of Complexity]] |

---

### Part VIII—CUE Schema Extension

Add to `gemini-scribe/cue/prodos_frontmatter.cue`:

```cue
// ── FCA Lattice Extension ──────────────────────────────────────────────
// Implements the Applied Formal Methods concept lattice.
// Spec: 30_Library/SoT/Protocol - AFM Vault Constitutional Triage.md

#FcaLevel: "c16" | "c12" | "c11" | "c4"

#FcaAttr: "ty-th" | "m1" | "m2" | "m3" | "m4" | "m5" | "m6" |
          "m7" | "m8" | "m9" | "m10" | "m-sub" | "m-axiom"

#FcaDiscriminator: "computational" | "pure-abstract" | "relational" |
                   "declarative" | "meta"

#FcaBlock: close({
    level!:            #FcaLevel
    discriminator?:    #FcaDiscriminator
    primary_attrs?:    [...#FcaAttr]
    calculated_attrs?: [...#FcaAttr]
    sit_passed?:       bool
    sit_notes?:        string
})
```

Add `fca?: #FcaBlock` to the universal `prodos` object in the existing schema.

---

### Quick Reference Card

```
TRIAGE PATH (fastest route):

  topic/type-theory?   ──YES──▶  C16  (I1: M1+M4+M8+M10 must follow)
       │
       NO
       │
  formal schema/proof? ──YES──▶  C12  (I2: M1+M4+M10 must follow)
       │
       NO
       │
  declarative + M4?   ──YES──▶  C11  (check M10; I3 if M5+M6 present)
       │
       NO
       │
  M4 + M10 alone?     ──YES──▶  C4   (SIT-C4; flag M2 if present)
       │
       NO
       │
  NOT AFM — route elsewhere.

─────────────────────────────────────────────────────────────
IMPLICATIONS:

  ty-th  ──▶  M1, M4, M8, M10    (I1 — C16)
  M8     ──▶  M1, M4, M10        (I2 — C12)
  M5+M6  ──▶  M1, M10            (I3 — C11)

─────────────────────────────────────────────────────────────
C16 DISCRIMINATOR:

  M-sub   → computational  (DS notes: Rust, DOD, TDD loop)
  M-axiom → pure-abstract  (AM notes: Category/Order/Set Theory)
  both absent → unset      (sits at C16 join)

  CONSTRAINT: M-sub ∧ M-axiom = ⊥  (I4/I5)
─────────────────────────────────────────────────────────────
```
