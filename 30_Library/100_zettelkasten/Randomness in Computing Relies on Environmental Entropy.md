---
aliases: [CSPRNG, Entropy, Environmental Randomness]
conformant: false
created: 2025-12-24T12:00:00+00:00
modified: 2026-08-29T09:36:04+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/randomness-in-computing-relies-on-environmental-entropy
tags: [computing, SoftwareEngineering/Security]
title: Randomness in Computing Relies on Environmental Entropy
type: claim
---

Because computer processes are deterministic, they cannot generate true randomness through pure software logic. To generate cryptographic keys, they must harvest chaos from the physical world.

## 🎲 Step 1: Harvesting Entropy

Operating systems maintain an Entropy Pool. This is a collection of unpredictable data gathered from:

- Timing of mouse movements and keystrokes.
- Precise intervals between network packet arrivals.
- Thermal noise from fans or hardware sensors.

## 🧩 Step 2: Seeding the Generator

This entropy acts as a "seed" for a Cryptographically Secure Pseudorandom Number Generator (CSPRNG). This algorithm produces a long sequence of numbers that are statistically random and impossible to predict without the original seed.

## 🧪 Step 3: Generate and Test

To pick a large prime:

1. Generate a large random candidate using the CSPRNG.
2. Run a Probabilistic Primality Test (e.g., Miller-Rabin).
3. If it fails, discard and try again. Because primes are reasonably common, this loop finds a prime very quickly.

This search for primes is a one-time cost performed during key generation.
