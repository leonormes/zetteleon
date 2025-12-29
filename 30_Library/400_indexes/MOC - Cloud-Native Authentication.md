---
aliases: ["AuthN MOC", "Identity Map", "Cloud Security Map"]
confidence: "5/5"
created: 2025-12-25T13:05:00Z
epistemic: "index"
last_reviewed: 2025-12-25"
modified: 2025-12-25T21:04:19+00:00
purpose: "Map of Content connecting Identity, Cryptography, and Authentication standards for cloud-native systems."
review_interval: "6 months"
see_also: ["[[SoT - Modern Authentication Standards]]", "[[SoT - Digital Identity]]"]
source_of_truth: []
status: "stable"
tags: ["authentication", "moc", "security", "map"]
title: MOC - Cloud-Native Authentication
type: "MOC"
uid: 
updated: 
---

## 1. The Core Trinity

Authentication is the intersection of Identity (Who), Cryptography (Proof), and Standards (How).

- **[[SoT - Digital Identity]]** - The abstract concepts (Subject, Credential, Identifier).
- **[[SoT - Cryptography and Encryption]]** - The mathematical foundation (RSA, ECC, Signatures).
- **[[SoT - Modern Authentication Standards]]** - The protocols (OIDC, OAuth, mTLS).

## 2. Workload Identity (Machine-to-Machine)

How code proves its identity to other code.

- **[[SoT - Secure Cross-Cloud Data Transport]]** - Applying mTLS and encryption in transit.
- **[[SoT - Container Security & Hardening]]** - Preventing identity theft (Non-Root, RO Filesystem).
- **Protocols:**
    - **OIDC Federation:** Eliminating static keys for GitHub/AWS connectivity.
    - **SPIFFE/SPIRE:** (Planned) Identity bootstrapping for dynamic workloads.

## 3. Authorization & Zero Trust

Authentication proves identity; Authorization defines the boundaries.

- **[[SoT - Data-Centric IAM in Zero Trust]]** - The PDP/PEP architecture and trust equation.
- **[[SoT - Role-Based Access Control (RBAC)]]** - (Planned) Traditional static permissions.
- **[[SoT - Attribute-Based Access Control (ABAC)]]** - Dynamic, fine-grained control.

## 4. User Identity (Human-to-Machine)

- **FIDO2 / Passkeys:** Phishing-resistant authentication.
- **SSO (Single Sign-On):** Centralizing trust via OIDC.

## 5. Key Algorithms

- **Signing:** `RS256`, `ES256`, `EdDSA` (Ed25519).
- **Hashing:** `SHA-256`.
- **Encryption:** `AES-GCM` (Symmetric), `RSA-OAEP` (Asymmetric).
