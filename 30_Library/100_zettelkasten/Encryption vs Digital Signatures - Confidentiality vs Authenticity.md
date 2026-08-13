---
aliases: [Confidentiality vs Authenticity, Encryption vs Signatures]
conformant: false
created: 2025-12-24T12:00:00+00:00
modified: 2026-08-13T10:56:52+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/100-zettelkasten/encryption-vs-digital-signatures-confidentiality-vs-authenticity
tags: [cryptography, SoftwareEngineering/Security]
title: Encryption vs Digital Signatures - Confidentiality vs Authenticity
type: claim
---

While asymmetric keys use the same underlying modular exponentiation, the process and goal are fundamentally different based on which key is used first.

## 🔐 Comparison Table

| Feature | Encryption | Digital Signature |
|:--- |:--- |:--- |
| Primary Goal | Confidentiality (Secrecy) | Authenticity & Integrity (Identity) |
| Data Processed | The entire message | A Hash of the message |
| Initial Action | Recipient's Public Key locks | Sender's Private Key signs |
| Final Action | Recipient's Private Key unlocks | Sender's Public Key verifies |

## 🧩 Why the Difference

- Confidentiality: You want only one specific person to read the message. Therefore, you use their public key (which only they can unlock).
- Authenticity: You want everyone to know the message came from you. Therefore, you use your private key (which only your public key can verify).
- Note on Efficiency: We rarely encrypt entire large files with asymmetric keys because it is slow. Instead, we use [[Hybrid Encryption Combines Symmetric Speed with Asymmetric Security]].
