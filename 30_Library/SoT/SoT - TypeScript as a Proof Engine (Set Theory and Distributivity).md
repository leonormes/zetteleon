---
aliases: ["Distributivity in Types", "Set Theory in TypeScript", "Type-Level Programming", "TypeScript Proof Engine"]
confidence: "5/5"
created: 2025-12-18T00:00:00Z
epistemic: "authoritative"
last_reviewed: "2025-12-18"
modified: 2025-12-27T20:40:55+00:00
purpose: "Defines the architectural mental model of TypeScript as a Proof Engine operating on Set Theory, specifically addressing the distributivity trap."
review_interval: "1 year"
see_also: ["[[SoT - Computational Type Theory (Meaning as Use)]]", "[[SoT - The Algebra of Types (Cardinality and Isomorphism)]]"]
source_of_truth: []
status: "stable"
tags: ["architecture", "formal_verification", "set_theory", "type_theory", "typescript"]
title: SoT - TypeScript as a Proof Engine (Set Theory and Distributivity)
type: "SoT"
uid: 
updated: 
---

## 1. Working Knowledge (Stable Foundation)

- **The Hybrid Model:** TypeScript is a practical fusion of **Set Theory** (The Data Model) and **Type Theory** (The Execution Model).
- **Types are Sets:** A type is not a shape; it is a set of allowed values. `string | number` is the union of two infinite sets. `never` is the Empty Set.
- **The Compiler is a Proof Engine:** It does not "run" code; it solves constraints. `A extends B` means "Is Set A a subset of Set B?".
- **The Distributivity Trap:** Conditional types (`T extends U`) map over unions. They do not treat the union as a single blob unless you explicitly "box" it.

## 2. Current Understanding (Coherent Narrative)

### The Core Paradigm: Structural vs. Nominal

- **Nominal Typing (The "Club" Model):** Found in Java/C#. Types are defined by identity and explicit declaration (e.g., `class A implements B`). It acts as a gatekeeper.
- **Structural Typing (The "Predicate" Model):** Found in TypeScript. A type is a set of constraints (a shape). If a value satisfies the shape, it belongs to the set. Compatibility is implicit and "predicate-based."

### The Data Model: Set Theory

Types are visualized as sets of allowed values.

- **Union (`|`)**: Logical OR (Disjunction). Represents the union of sets. A value belongs to the union if it belongs to *at least one* component set.
- **Intersection (`&`)**: Logical AND (Conjunction). Overlap of sets.
  - *Logic:* Intersection increases the *constraints* (requirements), which in turn *narrows* the set of compatible values. More requirements = fewer valid objects.
- **Subtyping (`extends`)**: Subset inclusion.
- **Control Flow Analysis:** The compiler narrows the "set" of a variable within code blocks (e.g., narrowing `string | number` to `string` inside an `if (typeof x === "string")` block).

### Pattern: Emulating Sum Types (Discriminated Unions)

Since TypeScript lacks native Algebraic Data Types (ADTs), we model them using **Literal Types**:

- **Mechanism:** Intersect an object structure with a specific literal string tag (e.g., `{ kind: "square", side: number }`).
- **Result:** A **Discriminated Union**. By switching on the `kind` property, the compiler mathematically proves which variant is active, enabling "exhaustive checking."
- **Goal:** To "make invalid states unrepresentable" at compile time.

### Meta-Layer: Type-Level Programming

The type system is a functional programming language where types are the data:

- **Generics = Functions:** They accept a Type as input and return a Type as output.
- **Mapped Types = Comprehensions:** Operators like `keyof` and mapped object syntax (`[K in keyof T]`) allow iterating over types to derive new ones (e.g., `Partial<T>`).
- **Substitutability:** Complex generic types are reasoned about via substitution, similar to lambda calculus reduction.

### The Execution Model: The Proof Engine

When you write `type F<T> =...`, you are defining a logical proposition.

- **Distributivity (The Map):** If `T` is a union (`A | B`), the compiler distributes the operation: `F<A> | F<B>`. This is often counter-intuitive to programmers expecting function-like behavior.
- **The Fix (Boxing):** To disable distributivity, wrap the types in tuples: `[T] extends [U]`. This forces the compiler to treat the union as a single, atomic set (a specific data structure) rather than a list of possibilities.

### Architectural Failure Mode

Treating types as "runtime functions" leads to bugs because:

1. **Map vs. Function:** You expect `IsNumber<string | number>` to return `false` (it's mixed). The compiler returns `boolean` (because it ran `IsNumber<string>` -> false AND `IsNumber<number>` -> true).
2. **Instantiation Depth:** Recursion is limited by an arbitrary compiler guardrail, not stack memory. Algorithms must be $O(1)$ for the compiler, not just the CPU.

## 3. Understanding Layers (Progressive Abstraction)

- **Layer 1 (The Programmer):** "Types check if my variables are correct."
- **Layer 2 (The Architect):** "Types are Sets. `extends` is Subset."
- **Layer 3 (The Type Theorist):** "Distributivity allows us to map logic over unions without loops. Boxing allows us to validate structure."

## 4. Minimum Viable Understanding (MVU)

- **Types = Sets.**
- **`extends` = Subset?**
- **Generic + Conditional = Distributive Map.**
- **Tuple Wrap `[]` = Atomic Check.**

## 5. Tensions, Gaps, and Cross-SoT Coherence

- **Structural vs. Nominal:** This model relies on **Structural Typing** (The "Predicate" model: checking shape/sets). It contrasts with the **Nominal Typing** (The "Club" model: checking names/declarations) often assumed in OOP.
- **Relation to Algebra:** The "Union" here is the **Sum Type** from [[SoT - The Algebra of Types (Cardinality and Isomorphism)]], but with the added property of being *untagged* and commutative (A | B == B | A).
- **The Logic Engine:** TypeScript frames itself not just as "JS with Types," but as a formal logic engine for hoisting runtime invariants into compile-time constraints.

## 6. Sources and Links

- **Source:** Analysis of "Programming or Proof" (Gemini/Blog Post).
- **Related:** [[SoT - Proof-Carrying Code via Simulated Dependent Types]].
