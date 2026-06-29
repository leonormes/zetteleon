---
alias:
- Fundamental Theorem of Arithmetic
- Prime Factorisation Uniqueness
aliases: []
created: 2025-12-24 12:00:00+00:00
last_reviewed: 2025-12-24
modified: 2026-02-01 15:08:33+00:00
status: stable
tags:
- maths
title: Fundamental Theorem of Arithmetic Guarantees Unique Prime Products
type: concept
updated: null
permalink: llmeon/30-library/100-zettelkasten/fundamental-theorem-of-arithmetic-guarantees-unique-prime-products
---

The Fundamental Theorem of Arithmetic states that every whole number greater than 1 is either a prime number itself or can be written as a unique product of prime numbers.

## 🧱 Prime "Atoms"

Prime numbers are the atoms of the numerical world. No matter how you break a composite number down, you will always end up with the same set of prime building blocks.

- Example: 12 can only be $2 \times 2 \times 3$.
- Example: 50 can only be $2 \times 5 \times 5$.

## 🔐 Application in Cryptography

In RSA, the public key modulus $n$ is the product of two massive primes $p$ and $q$. The Fundamental Theorem guarantees that there is only one pair of primes that can create that specific modulus. If an attacker factors $n$, they are guaranteed to find the exact primes used to create the private key.

The security of the system relies on the fact that while this product is unique, finding it among the infinite pool of candidates is computationally impossible.