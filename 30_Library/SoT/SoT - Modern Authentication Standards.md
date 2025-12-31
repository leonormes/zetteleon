---
aliases: ["AuthN Standards", "OAuth and OIDC", "Modern Auth Protocols"]
confidence: "5/5"
created: 2025-12-25T13:00:00Z
epistemic: "technical"
last_reviewed: "2025-12-30"
modified: 2025-12-31T23:08:34+00:00
purpose: "To define the canonical standards for modern, cloud-native authentication, focusing on token-based flows and cryptographic trust."
review_interval: "6 months"
see_also: ["[[SoT - Digital Identity]]", "[[SoT - Cryptography and Encryption]]", "[[MOC - Cloud-Native Authentication]]"]
source_of_truth: []
status: "stable"
tags: ["authentication", "oauth", "oidc", "security", "standards"]
title: SoT - Modern Authentication Standards
type: "SoT"
uid: 
updated: 
---

## 1. The Paradigm Shift

Modern authentication moves away from **Static Credentials** (long-lived passwords/keys) towards **Dynamic, Token-Based Exchange**. Trust is established via cryptographic signatures, not secret sharing.

---

## 2. Core Protocols

### A. OAuth 2.1 / OIDC (Identity Layer)

- **Role:** The standard for User and Workload identity.
- **Mechanism:** Delegated authorization. An Identity Provider (IdP) issues tokens to a Client.
- **Key Flows:**
    - **Authorization Code Flow (+PKCE):** Standard for users/browsers.
    - **Client Credentials Flow:** Standard for machine-to-machine (M2M) auth where no user is present (Service-to-Service).
    - **OIDC Workload Identity:** Federation that allows cloud workloads (e.g., GitHub Actions, K8s Pods) to trade their native tokens for cloud provider access tokens (AWS/Azure) without stored secrets.

### B. JWT (JSON Web Token)

- **Role:** The container for identity claims.
- **Structure:** `Header.Payload.Signature`.
- **Trust:** The recipient validates the **Signature** using the issuer's public keys (JWKS endpoint).
- **Algorithms:**
    - **RS256:** RSA Signature with SHA-256 (Legacy/Standard).
    - **ES256:** ECDSA with P-256 and SHA-256 (Modern/Efficient).

### C. Mutual TLS (mTLS)

- **Role:** Service-to-Service authentication (Zero Trust).
- **Mechanism:** Two-way verification. The Client verifies the Server's certificate, AND the Server verifies the Client's certificate.
- **Stack:** X.509 Certificates + TLS 1.3.
- **Use Case:** Service Meshes (Istio, Linkerd) where sidecars handle identity transparently.

---

## 3. M2M Authentication Patterns

Strategies for Machine-to-Machine communication where traditional MFA (OTP) is not feasible.

| Method | Mechanism | Use Case | Security Level |
|:--- |:--- |:--- |:--- |
| **Client Credentials (OAuth)** | App ID + Secret exchange for Token. | Service-to-Service, Daemons. | High (if secrets managed). |
| **Mutual TLS (mTLS)** | Certificate-based mutual auth. | Zero Trust Networks, Financial/Healthcare. | Very High (Hardware-bound). |
| **JWT Assertion** | Signed JWT used as credential. | Distributed Systems, Microservices. | High. |
| **API Keys** | Static string in header. | Public APIs, Simple Integrations. | Low (Hard to rotate). |
| **Cloud IAM Roles** | Identity federation / metadata service. | Cloud-native workloads (AWS/Azure). | Very High (Short-lived). |

---

## 4. Cloud-Native Identity Primitives

Cloud providers implement these standards as managed services to eliminate credential management.

| Provider | Mechanism | Underlying Protocol |
|:--- |:--- |:--- |
| **AWS** | IAM Roles for Service Accounts (IRSA) | OIDC + STS |
| **Azure** | Managed Identity (MSI) | OAuth 2.0 / OIDC |
| **GCP** | Workload Identity | OIDC Federation |
| **K8s** | Service Account Tokens | Projected Service Account Volumes (JWT) |

---

## 5. User Authentication Evolution

Moving beyond passwords to cryptographic proof of possession.

- **FIDO2 / WebAuthn:** Standard for passwordless auth. The "password" is a private key stored in a hardware authenticator (YubiKey) or platform module (TouchID/FaceID).
- **Passkeys:** Syncable FIDO2 credentials. Allows the private key to exist across devices (e.g., iCloud Keychain), balancing security with recovery.
