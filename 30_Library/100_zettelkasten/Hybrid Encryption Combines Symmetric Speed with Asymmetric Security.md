---
aliases: ["Hybrid Encryption", "Session Keys"]
confidence: "5/5"
created: 2025-12-24T12:00:00Z
epistemic: "technical"
last_reviewed: 2025-12-24
modified: 2025-12-28T09:56:31+00:00
purpose: "To explain the real-world architecture of secure communications like TLS/SSH."
review_interval: "1 year"
see_also: ["[[Encryption vs Digital Signatures - Confidentiality vs Authenticity]]"]
source_of_truth: ["[[SoT - Cryptography and Encryption]]"]
status: "stable"
tags: ["cryptography", "infrastructure"]
title: Hybrid Encryption Combines Symmetric Speed with Asymmetric Security
type: "concept"
uid: 
updated: 
---

In the real world, we rarely use RSA or ECC to encrypt large amounts of data. Asymmetric encryption is computationally slow and has data size limits. Instead, we use **Hybrid Encryption**.

## 🧩 The 3-Step Process

1. **Symmetric Key Generation:** The computer generates a fast, single-use key (e.g., for AES).
2. **Key Exchange:** The recipient's **Public Key** is used to encrypt only the small symmetric key. This is sent securely.
3. **Data Transfer:** Both parties now use the fast symmetric key to encrypt and decrypt the bulk of the communication.

## 🚀 Benefits

- **Asymmetric Layer:** Provides secure identity and key exchange without pre-shared secrets.
- **Symmetric Layer:** Provides massive speed and the ability to process gigabytes of data with minimal CPU overhead.

This architecture is the foundation of **HTTPS (TLS)**, **SSH**, and **PGP**.
