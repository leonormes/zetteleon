---
alias: [Prime Density, Prime Number Theorem]
aliases: []
conformant: false
created: 2025-12-24T12:00:00+00:00
modified: 2026-07-28T09:12:49+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/primes-become-rarer-but-remain-searchable
tags: [cryptography, maths]
title: Primes Become Rarer But Remain Searchable
type: claim
---

As numbers get larger, the Density of Primes decreases. This is because larger numbers have more opportunities to be divisible by smaller primes (the "filtering effect").

## 📐 The Prime Number Theorem

The distribution of primes is described by the Prime Number Theorem. The probability of a large random number $N$ being prime is roughly:

$$
P(\text{prime}) \approx \frac{1}{\ln(N)}
$$

| Digits | Range | Number of Primes | Density |
|:--- |:--- |:--- |:--- |
| 1 | 1 - 9 | 4 | 44.4% |
| 3 | 100 - 999 | 143 | 15.9% |
| 6 | 100k - 1M | 68,906 | 7.7% |

## 🔐 Impact on Cryptography

Even though the density drops (e.g., to < 0.1% for 309-digit numbers), the absolute number of primes remains astronomically large.

- Computers can find 1024-bit primes quickly using "Generate and Test" methods.
- The vast pool (over $10^{305}$ candidates) ensures that two people will almost never randomly pick the same prime pair.
- Links: [[Randomness in Computing Relies on Environmental Entropy]]

## Related

- [[SoT - Scalable Private Networking & IPAM]]—mechanism isomorphism: sparse allocation strategies. Primes thin out at 1/ln(N) but remain findable via generate-and-test; IPAM deliberately leaves "enormous gaps" for summarizability and growth buffer. Both manage uncertainty in large search spaces using hierarchical uniqueness guarantees (Euler Product ↔ CIDR lattice).
- [[Connection - Prime Distribution ↔ IPAM Sparse Allocation]]—detailed cross-domain analysis
