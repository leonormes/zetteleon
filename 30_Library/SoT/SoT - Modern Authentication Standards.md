---
aliases: ["AuthN Standards", "Modern Auth Protocols", "OAuth and OIDC"]
confidence: "5/5"
created: 2025-12-25T13:00:00Z
epistemic: "technical"
last_reviewed: "2025-12-30"
modified: 2026-01-23T18:09:19+00:00
purpose: "To define the canonical standards for modern, cloud-native authentication, focusing on token-based flows and cryptographic trust."
review_interval: "6 months"
see_also: ["[[MOC - Cloud-Native Authentication]]", "[[SoT - Cryptography and Encryption]]", "[[SoT - Digital Identity]]"]
source_of_truth: []
status: "stable"
tags: ["authentication", "oauth", "oidc", "SoftwareEngineering/Security", "standards"]
title: SoT - Modern Authentication Standards
type: "SoT"
uid: 
updated: 
---

## 1. The Paradigm Shift

Modern authentication moves away from **Static Credentials** (long-lived passwords/keys) towards **Dynamic, Token-Based Exchange**. Trust is established via cryptographic signatures, not secret sharing.

---

## 2. Core Protocols

### A. OAuth 2.0 & 2.1 (Authorization Framework)

- **Role:** The industry standard for **Delegated Authorization** (accessing resources on behalf of a user).
- **Evolution:**
    - _OAuth 1.0a (Legacy):_ Relied on complex cryptographic signing of every request. Deprecated for most use cases.
    - _OAuth 2.0 (Standard):_ Relies on **TLS (HTTPS)** for transport security. Uses **Bearer Tokens** (if you hold the token, you have access). Simpler but requires strict transport security.
- **Key Flows:**
    - **Authorization Code Flow (+PKCE):** The gold standard for users. Browser redirects to IdP, returns a code, code is exchanged for a token. PKCE prevents code injection attacks.
    - **Client Credentials Flow:** Machine-to-Machine (M2M). Service uses `AppID` + `Secret` to get a token. No user context.

### B. OpenID Connect (OIDC) - The Identity Layer

- **Role:** Adds **Authentication** (Who are you?) on top of OAuth 2.0 (What can you do?).
- **The ID Token:** A JWT containing user profile data (`sub`, `email`, `name`). Signed by the IdP.
- **UserInfo Endpoint:** An API endpoint to fetch more user details using the Access Token.
- **Significance:** Standardizes how Identity is shared between Google, Microsoft, and your app.

### C. Mutual TLS (mTLS) - Zero Trust Identity

- **Role:** Service-to-Service authentication where **Every Request** is verified.
- **Mechanism:** Two-way verification. The Client verifies the Server's certificate, AND the Server verifies the Client's certificate.
- **Zero Trust Principle:** "Never Trust, Always Verify." mTLS binds identity to the workload (certificate), not the network location (IP address).
- **Stack:** X.509 Certificates + TLS 1.3.

---

## 6. FIDO & Passwordless Standards

Moving beyond "shared secrets" (passwords) to public key cryptography.

### A. FIDO2 / WebAuthn

The standard for passwordless authentication on the web.

- **Mechanism:** The user unlocks a private key stored on their device using a local gesture (PIN, Fingerprint). The device signs a challenge from the server.
- **Security:** Phishing-resistant. The private key never leaves the device.

### B. UAF Vs U2F (Legacy FIDO)

- **UAF (Universal Authentication Framework):** Passwordless experience (Biometrics).
- **U2F (Universal 2nd Factor):** The "Dongle" experience (YubiKey). Requires a password first, then the key.

### C. Passkeys

- **Evolution:** Syncable FIDO credentials. Allows the private key to exist across a user's ecosystem (e.g., iCloud Keychain), solving the "lost device" recovery problem.

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
