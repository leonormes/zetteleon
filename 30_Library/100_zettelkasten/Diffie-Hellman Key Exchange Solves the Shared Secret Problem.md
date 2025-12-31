---
aliases: ["DH", "Diffie-Hellman", "Discrete Logarithm Problem"]
confidence: "5/5"
created: 2025-12-24T12:00:00Z
epistemic: "technical"
last_reviewed: 2025-12-24
modified: 2025-12-30T17:49:53+00:00
purpose: "To explain how two parties can agree on a secret key over an insecure channel."
review_interval: "1 year"
see_also: ["[[Trapdoor Functions Are the Foundation of Public-Key Cryptography]]"]
source_of_truth: ["[[SoT - Cryptography and Encryption]]"]
status: "stable"
tags: ["cryptography", "diffie-hellman"]
title: Diffie-Hellman Key Exchange Solves the Shared Secret Problem
type: "concept"
uid: 
updated: 
---

**Diffie-Hellman (DH)** is a method for two parties to agree on a shared secret key over a public, insecure channel. Unlike RSA, it is not used for encrypting messages themselves, but for establishing the session key for symmetric encryption.

## 🎨 The Paint Mixing Analogy

1. **Public Agreement:** Alice and Bob agree on a base color (Public Base).
2. **Secret Choice:** Alice picks red; Bob picks blue (Private Keys). They never share these.
3. **The Exchange:** Alice mixes her red with the base; Bob mixes his blue. They exchange the results.
4. **Final Secret:** Alice adds her red to Bob's mix; Bob adds his blue to Alice's mix. Both arrive at the same final "muddy brown" color. An eavesdropper cannot create this color because they lack the original secret red or blue.

## 📐 The Hard Problem

DH relies on the **Discrete Logarithm Problem**.

- It is easy to calculate $g^x \pmod{p}$.
- It is computationally impossible to find $x$ if you only know the result, $g$, and $p$.

This ensures that even if an attacker sees the exchange, they cannot derive the final shared secret.
