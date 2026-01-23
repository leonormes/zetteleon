---
aliases: ["CSPRNG", "Entropy", "Environmental Randomness"]
confidence: "5/5"
created: 2025-12-24T12:00:00Z
epistemic: "technical"
last_reviewed: 2025-12-24
modified: 2026-01-23T18:09:30+00:00
purpose: "To explain how deterministic computers generate truly random prime numbers."
review_interval: "1 year"
see_also: ["[[Primes Become Rarer But Remain Searchable]]"]
source_of_truth: ["[[SoT - Cryptography and Encryption]]"]
status: "stable"
tags: ["computing", "SoftwareEngineering/Security"]
title: Randomness in Computing Relies on Environmental Entropy
type: "concept"
uid: 
updated: 
---

Because computer processes are **deterministic**, they cannot generate true randomness through pure software logic. To generate cryptographic keys, they must harvest chaos from the physical world.

## 🎲 Step 1: Harvesting Entropy

Operating systems maintain an **Entropy Pool**. This is a collection of unpredictable data gathered from:

- Timing of mouse movements and keystrokes.
- Precise intervals between network packet arrivals.
- Thermal noise from fans or hardware sensors.

## 🧩 Step 2: Seeding the Generator

This entropy acts as a "seed" for a **Cryptographically Secure Pseudorandom Number Generator (CSPRNG)**. This algorithm produces a long sequence of numbers that are statistically random and impossible to predict without the original seed.

## 🧪 Step 3: Generate and Test

To pick a large prime:

1. Generate a large random candidate using the CSPRNG.
2. Run a **Probabilistic Primality Test** (e.g., Miller-Rabin).
3. If it fails, discard and try again. Because primes are reasonably common, this loop finds a prime very quickly.

This search for primes is a one-time cost performed during key generation.
