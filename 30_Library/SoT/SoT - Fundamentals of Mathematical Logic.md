---
aliases: [First-Order Logic Basics, Mathematical Quantifiers, Propositional Logic]
conformant: false
created: 2026-01-12T10:05:00+00:00
modified: 2026-07-20T16:33:49+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-fundamentals-of-mathematical-logic
tags: [fundamentals, math/logic, prodos/sot]
title: SoT - Fundamentals of Mathematical Logic
type: sot
---

Logic provides the rigour, language, and inferential machinery for mathematics. It serves as the bedrock upon which mathematical structures are built.

## 1. Propositional Logic (The Grammar)

Propositional logic deals with combining simple statements (propositions) using logical connectives.

### Core Connectives

- AND ($\land$): True only if both P and Q are true.
- OR ($\lor$): True if at least one of P or Q is true.
- NOT ($\neg$): Reverses the truth value.
- IMPLIES ($\implies$): "If P, then Q". False only if P is true and Q is false.
- IF AND ONLY IF ($\iff$): True if P and Q have the same truth value.

### Truth Tables

Truth tables define the functional meaning of connectives.

| P | Q | P $\implies$ Q | $\neg$P | $\neg$P $\lor$ Q | (P $\implies$ Q) $\iff$ ($\neg$P $\lor$ Q) |
|---|---|---|---|---|---|
| T | T | T | F | T | T |
| T | F | F | F | F | T |
| F | T | T | T | T | T |
| F | F | T | T | T | T |

## 2. Predicates and Quantifiers

To generalise statements, mathematics uses predicates (statements with variables) and quantifiers.

### The Quantifiers

- Universal Quantifier ($\forall$): "For all".
    - Example: $\forall n \in \mathbb{Z}, n^2 \ge 0$ ("For every integer n, n squared is non-negative").
- Existential Quantifier ($\exists$): "There exists".
    - Example: $\exists p \in \mathbb{P}, 20 < p < 25$ ("There exists a prime number between 20 and 25").

### Translating Logic

Skill in translating between natural language and logical notation is essential.

- Logic to English: $\forall x \in \mathbb{R}, \exists y \in \mathbb{R}, y > x$ becomes "For every real number, there is another real number that is larger than it."
