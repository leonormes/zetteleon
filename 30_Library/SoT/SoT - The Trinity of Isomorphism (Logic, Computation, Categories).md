---
aliases: [Curry-Howard-Lambek Isomorphism, Propositions as Types as Objects, The Computational Trinity]
created: 2026-04-19T14:00:00+01:00
modified: 2026-04-19T19:54:49+00:00
see_also: ["[[MOC - Applied Formal Methods]]", "[[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]]", "[[SoT - The Curry-Howard Correspondence (Propositions as Types)]]"]
tags: [fca/attr/m1, fca/attr/m10, fca/attr/m4, fca/attr/m8, fca/level/c16, topic/category-theory, topic/formal-methods, topic/logic, topic/type-theory]
title: SoT - The Trinity of Isomorphism (Logic, Computation, Categories)
---

## SoT—The Trinity of Isomorphism (Logic, Computation, Categories)

### Minimum Viable Understanding (MVU)

The Curry-Howard-Lambek Isomorphism is the foundational observation that three major branches of mathematics are different syntaxes for the same underlying structure. A Proposition in logic is exactly a Type in computation, which is exactly an Object in a Cartesian Closed Category (CCC). This trinity provides the "Formal Closure" for Level C16: it ensures that when we write code that type-checks, we are actually performing a mathematical proof whose truth is guaranteed by the structure of the category it inhabits.

---

### 1. The Three Languages of the Trinity

The isomorphism identifies a precise mapping between Logic, Computation, and Category Theory. If a statement is true in one, a corresponding statement must be true in the others.

|Logic (Propositions)|Computation (Types)|Category Theory (Objects)|
|---|---|---|
|Proposition $A$|Type $A$|Object $A$|
|Proof of $A$|Program/Term $e$ of type $A$|Morphism $1 \to A$|
|Implication $A \implies B$|Function Type $A \to B$|Exponential Object $B^A$|
|Conjunction $A \land B$|Product Type $(A, B)$|Categorical Product $A \times B$|
|Disjunction $A \lor B$|Sum Type $A + B$|Categorical Coproduct $A \sqcup B$|
|Tautology (True)|Unit Type `()`|Terminal Object $1$|
|Absurdity (False)|Empty Type `Void`|Initial Object $0$|

---

### 2. Formal Judgement: The Syntax of Truth

In the Trinity, the Type Judgement is the universal syntax. It states that under a certain context ($\Gamma$), an expression ($e$) is an inhabitant of a type ($T$):

$$
\Gamma \vdash e : T
$$

- Logic interpretation: Under the set of assumptions $\Gamma$, $e$ is a proof of the proposition $T$.
- Computation interpretation: In the environment $\Gamma$, $e$ is a program that evaluates to a value of type $T$.
- Categorical interpretation: In the category $\mathcal{C}$, $e$ is a morphism from the product of objects in $\Gamma$ to the object $T$.

This is the instantiation of M4 (Structural Truth): the truth of the expression is not verified at "runtime" but is encoded in the formal relationship between the term and its type.

---

### 3. Why the Trinity Matters for Complexity ($M10$)

The Trinity is the ultimate absorber of Complexity ($M10$). It moves the burden of correctness from the "Runtime" (human debugging or execution-time testing) into the "Static Structure" of the system.

1. Elimination of Null/Undefined: By identifying "False" with the categorical Initial Object (an empty set), we make it structurally impossible to have a "value" of an empty type.
2. Verified Composition: Because morphisms in a category must compose ($g \circ f$), we can guarantee that if two programs type-check individually, their composition is logically sound.
3. Substrate Independence ($M-axiom$): The Trinity proves that these laws hold whether you are using a whiteboard, a Rust compiler, or a quantum circuit. The logic is prior to the implementation.

---

### 4. Current Understanding: The "Rosetta Stone" Table

|Phenomenon|Logical View|Computational View|Categorical View|
|---|---|---|---|
|Simplification|Proof Normalisation|Program Execution (Evaluation)|Morphism Composition|
|Abstraction|Universal Quantification|Generics / Parametricity|Limits and Colimits|
|Transformation|Natural Deduction|Functional Programming|Functors|

---

### Related Knowledge

- [[SoT - The Curry-Howard Correspondence (Propositions as Types)]]—Focuses on the Logic-Computation bridge.
- [[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]]—The philosophical anchor for why this isomorphism is the vault's "Ground Truth".
- [[MOC - Applied Formal Methods]]—This note sits at the deepest level (C16) of this MOC.
- [[Protocol - AFM Vault Constitutional Triage]]—Provides the SIT-C16 tests used to validate this note.
