---
aliases: [One-Way Functions, Trapdoor One-Way Function]
conformant: false
created: 2025-12-24T12:00:00+00:00
modified: 2026-08-29T09:36:07+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/trapdoor-functions-are-the-foundation-of-public-key-cryptography
tags: [cryptography, maths]
title: Trapdoor Functions Are the Foundation of Public-Key Cryptography
type: claim
---

A Trapdoor One-Way Function is a mathematical operation that is easy to compute in one direction but extremely difficult to reverse unless you possess a secret piece of information (the "trapdoor").

## 🧩 Core Components

- One-Way Process: Easy to execute (e.g., snapping a padlock shut). Hard to reverse (e.g., picking the lock).
- The Trapdoor: The secret knowledge that makes the reverse operation trivial (e.g., the key to the padlock).

## 🎨 Analogies

- Paint Mixing: It is easy to mix two secret colours to get a unique third colour. It is virtually impossible to "un-mix" the final colour to identify the original ingredients.
- Padlock: Anyone can snap a padlock shut (Public Key action). Only the owner can open it (Private Key action).

## 📐 Implementation Examples

- RSA: Relies on the fact that multiplying two primes is easy, but factoring the result is hard.
- Diffie-Hellman: Relies on the difficulty of the Discrete Logarithm Problem.

Without these "fortunate" mathematical curiosities, secure communication over public channels would be impossible.
