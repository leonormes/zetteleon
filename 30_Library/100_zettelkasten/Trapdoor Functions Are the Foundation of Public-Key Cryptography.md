---
aliases: ["One-Way Functions", "Trapdoor One-Way Function"]
confidence: "5/5"
created: 2025-12-24T12:00:00Z
epistemic: "technical"
last_reviewed: 2025-12-24
modified: 2025-12-30T14:11:50+00:00
purpose: "To explain the fundamental mathematical concept that makes asymmetric encryption possible."
review_interval: "1 year"
see_also: ["[[Public and Private Keys Are Mathematically Asymmetric]]"]
source_of_truth: ["[[SoT - Cryptography and Encryption]]"]
status: "stable"
tags: ["cryptography", "maths"]
title: Trapdoor Functions Are the Foundation of Public-Key Cryptography
type: "concept"
uid: 
updated: 
---

A **Trapdoor One-Way Function** is a mathematical operation that is easy to compute in one direction but extremely difficult to reverse unless you possess a secret piece of information (the "trapdoor").

## 🧩 Core Components

- **One-Way Process:** Easy to execute (e.g., snapping a padlock shut). Hard to reverse (e.g., picking the lock).
- **The Trapdoor:** The secret knowledge that makes the reverse operation trivial (e.g., the key to the padlock).

## 🎨 Analogies

- **Paint Mixing:** It is easy to mix two secret colours to get a unique third colour. It is virtually impossible to "un-mix" the final colour to identify the original ingredients.
- **Padlock:** Anyone can snap a padlock shut (Public Key action). Only the owner can open it (Private Key action).

## 📐 Implementation Examples

- **RSA**: Relies on the fact that multiplying two primes is easy, but factoring the result is hard.
- **Diffie-Hellman**: Relies on the difficulty of the **Discrete Logarithm Problem**.

Without these "fortunate" mathematical curiosities, secure communication over public channels would be impossible.
