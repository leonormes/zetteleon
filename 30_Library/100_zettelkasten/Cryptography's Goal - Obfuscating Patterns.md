---
aliases: []
created: 2025-08-26T09:27:23+00:00
last_reviewed: ''
modified: 2026-07-04T10:51:53+00:00
permalink: llmeon/30-library/100-zettelkasten/cryptographys-goal-obfuscating-patterns
status: ''
tags: [information]
title: "Cryptography's Goal - Obfuscating Patterns"
type: ''
updated: null
---

🔑 Cryptography is a practical application that sits at the intersection of patterned and random-seeming data.

The fundamental goal of encryption is to take structured, meaningful information (which has low Shannon entropy and low Kolmogorov complexity) and apply a reversible transformation that makes the output statistically indistinguishable from random noise.

- Input (Plaintext): Possesses perceivable patterns. It is predictable and compressible. See [[Information as Perceivable Pattern]].
- Output (Ciphertext): Appears to have no patterns. It should have high Shannon entropy and high Kolmogorov complexity, resembling a random sequence to any observer without the key.

This process intentionally hides the usable information by destroying its perceivable structure, thereby validating the idea that patterns are what make data interpretable.

- Links: [[Information as Perceivable Pattern]], [[Shannon's Information Theory - Information as Uncertainty]]
