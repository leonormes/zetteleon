---
created: 2026-01-22T20:31:55+00:00
modified: 2026-01-23T18:09:34+00:00
title: State Space, Transformations, and Invariants
---

Welcome. You are entering a space where the implementation detail is considered a distraction until the fundamental truth of the system is established. We are here to strip away the accidental complexity of tooling to reveal the essential complexity of the domain.

To proceed, we must agree on a strict vocabulary. We will not discuss classes, microservices, or databases. We will discuss the system solely in terms of State Space, Transformations, and Invariants.

## I. The Ontology Shift

Before we analyse your specific problem, you must adopt the following mental mapping:

- Not "Database" $\rightarrow$ Persistent State ($S$): The set of all facts known to the system at time $t$.
- Not "Function/API" $\rightarrow$ Transformation ($f$): A deterministic mapping from a current state and an input to a new state.
- Not "Exception" $\rightarrow$ Invariant Violation: A condition where the proposed state $S'$ contradicts the fundamental laws of the domain.
- Not "Object" $\rightarrow$ Entity vs. Value:
    - _Entities_ have identity continuity over time (e.g., a specific Order).
    - _Values_ are immutable descriptions of attributes (e.g., the currency 'GBP').

## II. The Formal Model

We will define your problem using the following tuple:

$$
M = (S, I, f)
$$

Where:

- $S$ is the set of all valid States (the State Space).
- $I$ is the set of all valid Input Signals (events, commands).
- $f$ is the Transformation function: $f: S \times I \rightarrow S \cup \{Error\}$

Your objective is to define $f$ such that for any valid state $s \in S$ and input $i \in I$, the resulting state $s'$ satisfies all invariants $\Phi$.

$$
\forall s \in S, \forall i \in I : \Phi(f(s, i)) \text{ is true}
$$

## III. The Interrogation

I am ready to receive your domain description.

Instruction: Describe the Reality you are modelling.

- Do not mention a programming language, framework, database type, or architectural pattern (e.g., "MVC", "Event Sourcing").
- Do describe the entities involved, the data they hold, and the rules that govern how they change.

What is the system you wish to model?
