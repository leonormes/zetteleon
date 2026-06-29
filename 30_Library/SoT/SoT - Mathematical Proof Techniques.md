---
aliases:
- Direct Proof
- How to Prove It
- Proof by Contradiction
- Proof Methods
created: 2026-01-12 10:10:00+00:00
modified: 2026-02-01 15:07:55+00:00
status: stable
tags:
- logic
- math/proofs
- prodos/sot
title: SoT - Mathematical Proof Techniques
type: SoT
permalink: llmeon/30-library/so-t/so-t-mathematical-proof-techniques
---

## Mathematical Proof Techniques

Proof theory analyses the structure of mathematical arguments. Mastering these standard techniques is the core skill of mathematical reasoning.

### 1. Standard Techniques

#### A. Direct Proof

- Logic: Assume Hypothesis $P$ is true. Deduce a chain of implications to show Conclusion $Q$ is true.
- Use Case: "Prove that the sum of two even integers is even."

#### B. Proof by Contrapositive

- Logic: To prove $P \implies Q$, prove the logically equivalent $\neg Q \implies \neg P$.
- Mechanism: Assume the conclusion is false, and show the hypothesis must therefore be false.
- Use Case: "Prove that if $n^2$ is even, then $n$ is even."

#### C. Proof by Contradiction (Reductio Ad Absurdum)

- Logic: To prove $P$, assume $\neg P$ and derive a logical absurdity (e.g., $1=0$ or $Q \land \neg Q$).
- Use Case: "Prove that $\sqrt{2}$ is irrational."

#### D. Proof by Induction

- Logic: Prove a base case (e.g., $n=1$). Then prove that if true for $k$, it must be true for $k+1$.
- Use Case: Proving properties for all natural numbers (e.g., summation formulas).

---

### 2. Worked Example: Contrapositive

Statement: For any integer $n$, if $n^2$ is even, then $n$ is even.

1. Identify $P \implies Q$:
    - $P$: $n^2$ is even.
    - $Q$: $n$ is even.
2. Form Contrapositive ($\neg Q \implies \neg P$):
    - If $n$ is odd, then $n^2$ is odd.
3. Proof:
    - Assume $n$ is odd: $n = 2k + 1$.
    - Square it: $n^2 = (2k+1)^2 = 4k^2 + 4k + 1$.
    - Factor: $n^2 = 2(2k^2 + 2k) + 1$.
    - Result: $n^2 = 2m + 1$, which is the definition of an odd number.
4. Conclusion: Since the contrapositive is true, the original statement is true.

### 3. Recommended Resources

- Books: _How to Prove It_ (Velleman), _Book of Proof_ (Hammack).
- Practice: Brilliant.org (Logic courses), Project Euler (Computational logic).