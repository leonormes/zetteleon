---
aliases: ["Rivest-Shamir-Adleman", "RSA"]
confidence: "5/5"
created: 2025-12-24T12:00:00Z
epistemic: "technical"
last_reviewed: 2025-12-24
modified: 2025-12-30T14:11:51+00:00
purpose: "To define the RSA algorithm and its reliance on prime factorisation."
review_interval: "1 year"
see_also: ["[[Public and Private Keys Are Mathematically Asymmetric]]"]
source_of_truth: ["[[SoT - Cryptography and Encryption]]"]
status: "stable"
tags: ["cryptography", "rsa"]
title: RSA Algorithm Relies on Integer Factorisation
type: "concept"
uid: 
updated: 
---

The **RSA Algorithm** (named after Rivest, Shamir, and Adleman) is the most widely used system for encryption and digital signatures. Its security rests on the **Integer Factorisation Problem**.

## 📐 The Mathematical Trapdoor

1. **The Easy Part:** Multiplying two massive prime numbers (`p` and `q`) to get a modulus (`n`). A computer does this instantly.
2. **The Hard Part:** Taking the modulus (`n`) and figuring out the original primes (`p` and `q`). For 2048-bit numbers, this would take thousands of years for the world's most powerful computers.
3. **The Trapdoor:** Knowing the original primes allows the owner to calculate the **Totient** ($\lambda(n)$), which is required to derive the private key.

## 🔄 The Cycle of Powers

RSA uses **Modular Exponentiation**. The totient determines the "length" of the exponentiation cycle. The private key `d` is designed to complete several full "laps" around the modulus and land exactly one step past the start, returning the original message.

- **Links**: [[Infinitude of Primes Guarantees a Limitless Supply for Keys]], [[Modular Arithmetic Creates a Cyclical System]]
