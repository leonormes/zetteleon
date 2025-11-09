---
aliases: []
confidence: 
created: 2025-08-19T23:32:29Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:47Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Public and Private Keys Are Mathematically Asymmetric
type:
uid: 
updated: 
version:
---

While they work as a pair, public and private keys are not interchangeable. They are created with distinct mathematical properties for different roles.

- Public Key: Contains the modulus n and a small, standard public exponent e (usually 65537). It's designed for "locking" (encryption).
- Private Key: Contains the same modulus n and a massive, unique private exponent d. It is the "trapdoor" for "unlocking" (decryption).
  The value d is calculated from the secret prime factors of n and is the mathematical inverse of e. This asymmetry is fundamental to the security of the system.
  Links to: [[Prime Numbers Create a Mathematical Trapdoor]], [[Modular Arithmetic Creates a Cyclical System]]

[[prime atoms]]
