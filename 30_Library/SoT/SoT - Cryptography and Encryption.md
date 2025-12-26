---
aliases: ["Cryptography SoT", "Encryption SoT"]
confidence: "5/5"
created: 2025-12-24T12:00:00Z
epistemic: "technical"
last_reviewed: 2025-12-24
modified: 2025-12-25T11:40:22+00:00
purpose: "To define the stable principles of modern cryptography and encryption."
review_interval: "6 months"
see_also: ["[[Public and Private Keys Are Mathematically Asymmetric]]"]
source_of_truth: []
status: "stable"
tags: ["cryptography", "security", "SoT"]
title: SoT - Cryptography and Encryption
type: "SoT"
uid: 
updated: 
---

## 1. The Core Principle: The Trapdoor

Modern cryptography relies on **Trapdoor One-Way Functions**. These are mathematical operations that are computationally easy to perform in one direction but virtually impossible to reverse without a specific secret (the "trapdoor").

- **One-Way Direction:** Encrypting with a public key.
- **Trapdoor Direction:** Decrypting with a private key.

## 2. Primary Algorithms & Hard Problems

The security of any asymmetric system is only as strong as the mathematical "Hard Problem" it is based on.

| Algorithm | Hard Problem | Description |
|:--- |:--- |:--- |
| **RSA** | Integer Factorisation | Impossible to find large prime factors of a massive modulus. |
| **Diffie-Hellman** | Discrete Logarithm | Impossible to find the exponent in modular exponentiation. |
| **ECC** | Elliptic Curve Logarithm| A more efficient version of the discrete log problem. |

### 2.1 Modern Algorithm Standards (2025)

| Use Case | Recommended Algorithm | Notes |
|:--- |:--- |:--- |
| **Signing (JWT/Auth)** | **Ed25519** (EdDSA) | High speed, constant time, side-channel resistant. |
| **Signing (Legacy/Compat)** | **ES256** (P-256) | Widely supported (e.g., WebAuthn). |
| **Encryption (Asymmetric)** | **RSA-4096** | Robust but computationally expensive. |
| **Hashing** | **SHA-256** | The industry standard baseline. |

## 3. Confidentiality vs. Authenticity

Asymmetric keys serve two distinct purposes based on the order of operations:

### A. Encryption (Confidentiality)

- **Action:** Recipient's **Public Key** locks the data.
- **Goal:** Only the recipient can read it.

### B. Digital Signatures (Authenticity)

- **Action:** Sender's **Private Key** signs a **Hash**.
- **Goal:** Anyone can verify the sender and confirm integrity.

## 4. Practical Implementation: Hybrid Encryption

Because asymmetric encryption is computationally slow, real-world systems (TLS, SSH) use a **Hybrid** approach:

1. Use Asymmetric keys to exchange a fast **Symmetric Key** (e.g., AES).
2. Use the Symmetric key to encrypt the bulk data.

## 5. History: Parallel Paths

Public-key cryptography was discovered twice in the 1970s:

- **Secretly:** By GCHQ (James Ellis, Clifford Cocks, Malcolm Williamson).
- **Publicly:** By Academics (Whitfield Diffie, Martin Hellman, Ralph Merkle, and the RSA trio).
