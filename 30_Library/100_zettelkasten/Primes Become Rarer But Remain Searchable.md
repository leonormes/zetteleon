---
alias: ["Prime Density", "Prime Number Theorem"]
aliases: []
confidence: "5/5"
created: 2025-12-24T12:00:00Z
epistemic: "fact"
last_reviewed: 2025-12-24
modified: 2026-01-08T10:49:59+00:00
purpose: "To explain the distribution of primes and its impact on finding large primes for keys."
review_interval: "1 year"
see_also: ["[[Infinitude of Primes Guarantees a Limitless Supply for Keys]]"]
source_of_truth: ["[[SoT - Cryptography and Encryption]]"]
status: "stable"
tags: ["cryptography", "maths"]
title: Primes Become Rarer But Remain Searchable
type: "concept"
uid: 
updated: 
---

As numbers get larger, the **Density of Primes** decreases. This is because larger numbers have more opportunities to be divisible by smaller primes (the "filtering effect").

## 📐 The Prime Number Theorem

The distribution of primes is described by the Prime Number Theorem. The probability of a large random number $N$ being prime is roughly:

$$P(\text{prime}) \approx \frac{1}{\ln(N)}$$

| Digits | Range | Number of Primes | Density |
|:--- |:--- |:--- |:--- |
| **1** | 1 - 9 | 4 | 44.4% |
| **3** | 100 - 999 | 143 | 15.9% |
| **6** | 100k - 1M | 68,906 | 7.7% |

## 🔐 Impact on Cryptography

Even though the density drops (e.g., to < 0.1% for 309-digit numbers), the **absolute number** of primes remains astronomically large.

- Computers can find 1024-bit primes quickly using "Generate and Test" methods.
- The vast pool (over $10^{305}$ candidates) ensures that two people will almost never randomly pick the same prime pair.
- **Links**: [[Randomness in Computing Relies on Environmental Entropy]]
