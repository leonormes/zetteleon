---
aliases: ["Asymmetric Keys", "Key Pair Asymmetry"]
confidence: "5/5"
created: 2025-08-19T23:32:29Z
epistemic: "technical"
last_reviewed: 2025-12-24
modified: 2026-01-03T10:19:36+00:00
purpose: "To define the mathematical distinction between public and private keys in RSA."
review_interval: "1 year"
see_also: ["[[Modular Arithmetic Creates a Cyclical System]]", "[[RSA Algorithm Relies on Integer Factorisation]]"]
source_of_truth: ["[[SoT - Cryptography and Encryption]]"]
status: "stable"
tags: ["cryptography", "maths", "SoftwareEngineering/Security"]
title: Public and Private Keys Are Mathematically Asymmetric
type: "concept"
uid: 
updated: 
---

While they work as a pair, public and private keys are not interchangeable. They are created with distinct mathematical properties for different roles.

## 🧩 The RSA Anatomy

- **Public Key**: Contains the modulus `n` and a small, standard public exponent `e` (overwhelmingly **65537**). It is designed for "locking" (encryption).
- **Private Key**: Contains the same modulus `n` and a massive, unique private exponent `d`. It is the "trapdoor" for "unlocking" (decryption).

## 🔄 The Inverse Relationship

The value `d` is specifically calculated to be the modular multiplicative inverse of `e`. Mathematically:

$$(e * d) \pmod{\lambda(n)} = 1$$

Where $\lambda(n)$ is the secret totient derived from the original prime factors. This ensures that:

- **For Encryption**: $(m^e)^d \pmod{n} = m$
- **For Signing**: $(h^d)^e \pmod{n} = h$

This symmetry allows the same maths to serve both **Confidentiality** and **Authenticity** depending on the order of operations.

- **Links**: [[Prime Numbers Create a Mathematical Trapdoor]], [[Modular Arithmetic Creates a Cyclical System]]
