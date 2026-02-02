---
aliases: [Complexity Budget, Law of Conservation of Complexity, Tesler's Law]
created: 2026-01-31T00:00:00+00:00
last_reviewed: 
modified: 2026-02-02T07:31:26+00:00
status: evergreen
tags: [architecture, complexity, mental-model, system-design]
title: SoT - Conservation of Complexity
type: SoT
updated: 
---

## The Core Insight

> Software complexity is conserved: it must reside either in control flow (code), in representation (data structures), or in the user's cognitive load. Systems become simpler, safer, and more scalable when complexity is pushed into Structure (Data) rather than Process (Code).

## 1. Tesler's Law (The Balloon Metaphor)

Every application has an inherent amount of complexity that cannot be removed or hidden. It can only be moved.

- The User Trade-off: If the _User_ experiences simplicity (e.g., a one-button interface), the _System_ must carry the burden of interpreting intent.
- The Engineer Trade-off: If the _Code_ is simpler (generic lists), the _Logic_ must be complex to handle it. If the _Data Structure_ is complex (rich types), the _Code_ becomes trivial.

## 2. The Choice of Container: Code vs. Data

Linus Torvalds: _"Bad programmers worry about the code. Good programmers worry about data structures and their relationships."_

| Feature | Complexity in Code (Logic) | Complexity in Data (Structure) |
|:--- |:--- |:--- |
| Nature | Dynamic / Temporal | Static / Topological |
| Cognitive Load | High (must simulate execution) | Low (can inspect schema) |
| Constraints | Implicit (hidden in `if` checks) | Explicit (Enums, Types, Schemas) |
| Scalability | Combinatorial Explosion | Linear / Graph expansion |

Sustainability Heuristic: Complexity belongs where it can be named, constrained, and inspected. That place is almost always Data.

## 3. Dimensions of Complexity

### A. Objective (The System)

- Kolmogorov Complexity: The length of the shortest possible description of the system. This defines the "Irreducible Floor."
- Cyclomatic Complexity: The number of linearly independent paths through code. High scores indicate logic that has bypassed structural containment.

### B. Subjective (The Observer)

- Essential Complexity: Difficulty inherent in the problem itself (e.g., UK Tax Law). Cannot be reduced, only managed.
- Accidental Complexity: Difficulty created by poor tools, "spaghetti code," or tech debt. Must be eliminated.
- Cognitive Chunking: A specialist perceives a car engine as 4 subsystems; a novice sees 200 parts. Complexity is "reduced" via Abstraction (internal mental models), but the objective complexity remains.

### C. Business Complexity (Semantic Density)

How do we measure the complexity of a domain?

1. Cynefin Framework: Is the problem Simple (Categorize), Complicated (Analyze), or Complex (Probe)? >50% Complex = Core Domain.
2. Semantic Density: High vocabulary size + High ambiguity (e.g., "Customer" means different things to Sales vs. Support) = High Complexity.
3. Invariant Count: The number of rules that _must always be true_ for an entity. High invariant count requires State Machines (Structure), not boolean flags (Logic).

## 4. Physics vs. Systems Context

Unlike Physics, where "Conservation" is a fundamental law of the universe, Tesler's Law is an empirical heuristic.

| Concept | Physics (Thermodynamics) | Systems (Tesler's Law) |
|:--- |:--- |:--- |
| Principle | Unitarity / 2nd Law: Information is conserved; Entropy (disorder) increases. | Conservation: Complexity is fixed; it only shifts location. |
| Mechanism | Energy flow. | Trade-off between Developer effort vs. User effort. |
| Goal | Describe the universe. | Minimize cognitive load / Maximize maintainability. |

## 5. Diagnostic Heuristic

> "Is this logic compensating for missing structure?"

If yes, you are paying interest on Schema Debt.

Common Smells:

- Large `if/elif` ladders → missing tables/polymorphism.
- Boolean flags tracking state → missing state machine.
- Defensive null checks everywhere → invalid states allowed by schema.
- "Special cases" → broken representation.

See Also: [[SoT - Data-Oriented Design]], [[SoT - Infrastructure Complexity Management]]

## Validating the Tesler–Torvalds Synthesis

Your statement is logically sound and represents a genuine insight, but it benefits from some refinement to make the connection between the two thinkers more precise.

---

### The Core Claim, Restated

You're arguing:

1. Tesler's Law establishes that complexity in a problem domain is _conserved_—it can be moved but not destroyed
2. Torvalds' dictum ("Bad programmers worry about the code. Good programmers worry about data structures and their relationships.") is a _heuristic for where to allocate_ that conserved complexity
3. Therefore, Torvalds is giving tactical advice within the strategic constraint Tesler identified

This synthesis is valid. Let me show you why, and where the nuance lies.

---

### Where the Logic Holds

#### Tesler's Law as a Conservation Principle

Tesler (from his work at Xerox PARC and Apple) observed that every application has an inherent amount of complexity that cannot be removed—only _relocated_. The classic formulation concerns the user/system boundary: you can hide complexity from users, but the system must absorb it.

Your extension—that this conservation applies _within_ the system itself—is legitimate and widely accepted in software architecture discourse. Fred Brooks made a similar distinction between _essential complexity_ (inherent to the problem) and _accidental complexity_ (introduced by our tools/choices).

#### Torvalds as an Allocation Strategy

Torvalds' statement _does_ function as guidance on where to place essential complexity. The argument runs:

|Complexity in Code|Complexity in Data Structures|
|---|---|
|Scattered, imperative, hard to verify|Centralised, declarative, easier to reason about|
|Changes require understanding control flow|Changes require understanding relationships|
|Bugs hide in branches|Constraints surface errors at boundaries|

By "worrying about data structures," you're choosing to encode domain rules _structurally_ rather than _procedurally_—which often makes the system more robust.

---

### Where Refinement Helps

#### 1. Tesler's Original Scope Was Narrower

Tesler was primarily discussing the user-facing complexity threshold—the point at which simplifying the interface further would remove essential functionality. Your application to _internal_ system design is a reasonable generalisation, but it's worth acknowledging you're extending the principle.

#### 2. The Buckets Aren't Fully Disjoint

Your framing of "Code" vs "Data Structures" is useful but slightly leaky:

- Data structures encode algorithms implicitly. A B-tree _is_ an algorithm for maintaining sorted access. A graph _is_ a decision about traversal complexity.
- Schema design is code. SQL constraints, foreign keys, and indices are declarative logic that _executes_.

A more precise framing might be:

> Imperative/Procedural allocation vs Declarative/Structural allocation of the same essential complexity.

#### 3. Torvalds' Heuristic Has Limits

There are domains where algorithmic complexity genuinely cannot be "pushed into" data structures—cryptography, certain numerical methods, real-time scheduling. In these cases, the _algorithm is the essential complexity_, and no amount of clever structuring removes it.

---

### Verdict

|Aspect|Assessment|
|---|---|
|Tesler as conservation law|✅ Valid application|
|Torvalds as allocation strategy|✅ Valid interpretation|
|Buckets A & B as exhaustive|⚠️ Useful heuristic, but boundaries blur|
|Synthesis as actionable principle|✅ Yes—it guides architectural decisions|

---

### The Principle, Sharpened

> Essential domain complexity is conserved. The architect's choice is whether to express it through control flow (imperative logic) or through structure (data relationships and constraints). Torvalds argues—correctly, in most cases—that structural expression yields more maintainable systems.

---

### Your Next Action

Write a single concrete example from your own domain (Kubernetes configs, GitOps pipelines) where you've seen this trade-off play out. Describe: _what complexity existed, and where did you (or someone else) choose to allocate it?_

This will test whether the abstraction actually predicts real architectural decisions you've encountered.
