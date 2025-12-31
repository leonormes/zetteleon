---
aliases: ["Euclid's Theorem on Primes", "Infinite Primes"]
confidence: "5/5"
created: 2025-08-19T23:32:29Z
epistemic: "fact"
last_reviewed: 2025-12-24
modified: 2025-12-30T17:49:51+00:00
purpose: "To explain why there is no largest prime number and its impact on key generation."
review_interval: "1 year"
see_also: ["[[Fundamental Theorem of Arithmetic]]", "[[Primes Become Rarer But Remain Searchable]]"]
source_of_truth: ["[[SoT - Cryptography and Encryption]]"]
status: "stable"
tags: ["cryptography", "maths"]
title: Infinitude of Primes Guarantees a Limitless Supply for Keys
type: "concept"
uid: 
updated: 
---

There is an infinite number of prime numbers. As proven by Euclid over 2,000 years ago, no matter how large a prime you find, there is always a larger one.

## 📐 Euclid's Logic (Simplified)

1. Imagine you have a complete list of all the prime numbers that exist.
2. Multiply all of them together and add 1 ($P = p_1 * p_2 *... * p_n + 1$).
3. This new number $P$, when divided by any of the primes on your list, will always leave a remainder of 1.
4. Therefore, $P$ is either a new prime itself or has a prime factor not on the original list.
5. In either case, the original list was incomplete.

## 🔐 Impact on Cryptography

This property ensures a **limitless supply** of unique large primes. We can generate unique key pairs for every person and device on the planet without ever running out of the necessary atomic building blocks.

- **Links**: [[Prime Numbers Are the Atomic Elements of All Numbers]], [[Primes Become Rarer But Remain Searchable]]
