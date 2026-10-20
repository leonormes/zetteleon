---
aliases: [Hybrid Encryption, Session Keys]
conformant: true
contradicts: []
created: 2025-12-24T12:00:00+00:00
epistemic_status: high
evidence_links: []
modified: 2026-10-19T00:00:00+00:00
permalink: llmeon/30-library/100-zettelkasten/hybrid-encryption-combines-symmetric-speed-with-asymmetric-security
proposition: Real systems encrypt bulk data with a fast single-use symmetric key and use asymmetric cryptography only to protect and exchange that small key, because asymmetric encryption is slow and limited in data size.
tags: [cryptography, infrastructure]
title: Hybrid Encryption Combines Symmetric Speed with Asymmetric Security
type: claim
---

In the real world, we rarely use RSA or ECC to encrypt large amounts of data. Asymmetric encryption is computationally slow and has data size limits. Instead, we use Hybrid Encryption.

## 🧩 The 3-Step Process

1. Symmetric Key Generation: The computer generates a fast, single-use key (e.g., for AES).
2. Key Exchange: The recipient's Public Key is used to encrypt only the small symmetric key. This is sent securely.
3. Data Transfer: Both parties now use the fast symmetric key to encrypt and decrypt the bulk of the communication.

## 🚀 Benefits

- Asymmetric Layer: Provides secure identity and key exchange without pre-shared secrets.
- Symmetric Layer: Provides massive speed and the ability to process gigabytes of data with minimal CPU overhead.

This architecture is the foundation of HTTPS (TLS), SSH, and PGP.

### Related

- [[Trapdoor Functions Are the Foundation of Public-Key Cryptography]] [depends_on:: [[Trapdoor Functions Are the Foundation of Public-Key Cryptography]], confidence=medium]—*the asymmetric primitive being combined.*
- [[Public and Private Keys Are Mathematically Asymmetric]] [depends_on:: [[Public and Private Keys Are Mathematically Asymmetric]], confidence=medium]—*the key pair whose public half wraps the symmetric key (inferred).*
- [[SoT - Cryptography and Encryption]] [supports:: [[SoT - Cryptography and Encryption]], confidence=medium]—*its section 4 states the same hybrid approach for TLS and SSH.*
- [[SoT - The Data Architecture of TLS 1.3]]—*the protocol named as built on this pattern. TLS 1.3 negotiates the shared secret with an ephemeral key exchange rather than encrypting a key under the server's public key, so step 2 above is the older RSA key-transport form (inferred, worth checking).*
- [[RSA Algorithm Relies on Integer Factorisation]]—*the best-known asymmetric algorithm used for the key-wrapping step.*
- [[Encryption vs Digital Signatures - Confidentiality vs Authenticity]]—*the other use of the same asymmetric key pair: signing rather than wrapping a key.*
- [[SSL Offloading Centralises Certificate Management on the Load Balancer]]—*a deployment where the expensive TLS work is moved off backend servers.*
- [[MOC - Cryptography]]—*the map this note is filed under.*
