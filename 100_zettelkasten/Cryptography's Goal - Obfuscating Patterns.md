---
aliases: []
confidence: 
created: 2025-08-26T09:27:23Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [information]
title: "Cryptography's Goal - Obfuscating Patterns"
type:
uid: 
updated: 
version:
---

🔑 **Cryptography** is a practical application that sits at the intersection of patterned and random-seeming data.

The fundamental goal of encryption is to take structured, meaningful information (which has low Shannon entropy and low Kolmogorov complexity) and apply a reversible transformation that makes the output statistically indistinguishable from random noise.

- **Input (Plaintext)**: Possesses perceivable patterns. It is predictable and compressible. See [[Information as Perceivable Pattern]].
- **Output (Ciphertext)**: Appears to have no patterns. It should have high Shannon entropy and high Kolmogorov complexity, resembling a random sequence to any observer without the key.

This process intentionally hides the usable information by destroying its perceivable structure, thereby validating the idea that patterns are what make data interpretable.

- **Links**: [[Information as Perceivable Pattern]], [[Shannon's Information Theory - Information as Uncertainty]]
