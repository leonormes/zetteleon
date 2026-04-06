---
aliases: ["AuthN Standards", "Modern Auth Protocols", "OAuth and OIDC"]
created: 2025-12-25T13:00:00Z
last_reviewed: "2025-12-30"
modified: 2026-02-01T15:07:55+00:00
status: "stable"
tags: ["authentication", "oauth", "oidc", "SoftwareEngineering/Security", "standards"]
title: SoT - Modern Authentication Standards
type: "SoT"
updated: 
---

## 1. The Paradigm Shift

Modern authentication moves away from Static Credentials (long-lived passwords/keys) towards Dynamic, Token-Based Exchange. Trust is established via cryptographic signatures, not secret sharing.

---

## 2. Core Protocols

### A. OAuth 2.0 & 2.1 (Authorization Framework)

- **Role:** The industry standard for **Delegated Authorization** (accessing resources on behalf of a user).
- **Core Components:**
    - *Resource Owner:* The user whose data is being accessed.
    - *Client Application:* The app requesting the data.
    - *Resource Server:* Where the user data resides (the API).
    - *Authorization Server:* The trusted authority that issues tokens (e.g., Entra ID, Auth0).
- **Key Flows:**
    - **Authorization Code Flow (+PKCE):** The gold standard for web and mobile apps. Browser redirects to IdP, returns a code, which the client exchanges for an access token. **PKCE** (Proof Key for Code Exchange) adds a code challenge/verifier to mitigate interception risks on public clients.
    - **Device Code Flow:** Designed for devices with limited input (TVs, CLI tools). The user enters a code on a separate device (laptop/phone) while the app polls for completion.
    - **Token Refresh Flow:** Addresses short access token lifetimes. The app exchanges a long-lived **Refresh Token** for a new access token, minimizing repeated user logins.
    - **Client Credentials Flow:** Machine-to-Machine (M2M). The service uses `AppID` + `Secret` to get a token. No user context; used for admin/service tasks.
- **Security Note:** Avoid **Implicit Flow** and **Resource Owner Password Credentials**—they are outdated, insecure, and deprecated in OAuth 2.1.

### B. OpenID Connect (OIDC) - The Identity Layer

- **Role:** Adds **Authentication** (Who are you?) on top of OAuth 2.0 (What can you do?).
- **The ID Token:** A JWT containing user profile data (`sub`, `email`, `name`). Signed by the IdP.
- **UserInfo Endpoint:** An API endpoint to fetch more user details using the Access Token.
- **Significance:** Standardizes how Identity is shared between providers (Google, Microsoft) and applications.

### C. SAML 2.0 (Security Assertion Markup Language)

- **Role:** An XML-based standard used primarily for **Enterprise Single Sign-On (SSO)**.
- **Mechanism:** The Identity Provider (IdP) sends a signed XML assertion to the Service Provider (SP) to notify it that the user is verified.
- **Comparison:** While OIDC is JSON/REST-friendly and dominant in modern apps, SAML remains the backbone of many corporate and legacy enterprise integrations.

---

## 3. Identity Verification Methods (Authentication)

Trust is established by providing information that only the entity being authenticated can possess ("Proof of Possession").

- **Credential-based:** Traditional username/password. Weak against modern threats; requires strict complexity and rotation policies.
- **Challenge-Handshake Authentication Protocol (CHAP):** Used in network communications (remote access). Uses cryptographic challenge-response messages to prevent eavesdropping and replay attacks.
- **Biometric Identification:** Measures unique physiological traits (Fingerprint, Facial Recognition). Highly resistant to spoofing when implemented correctly.
- **Multi-Factor Authentication (MFA):** Adds a critical second layer of security via phone calls, SMS, mobile app push notifications, or hardware tokens.
- **Passwordless (FIDO2/WebAuthn):** Shifting to public key cryptography where the "password" is a private key stored in a hardware module (TPM, Secure Enclave).

### C. Mutual TLS (mTLS) - Zero Trust Identity

- Role: Service-to-Service authentication where Every Request is verified.
- Mechanism: Two-way verification. The Client verifies the Server's certificate, AND the Server verifies the Client's certificate.
- Zero Trust Principle: "Never Trust, Always Verify." mTLS binds identity to the workload (certificate), not the network location (IP address).
- Stack: X.509 Certificates + TLS 1.3.

---

## 6. FIDO & Passwordless Standards

Moving beyond "shared secrets" (passwords) to public key cryptography.

### A. FIDO2 / WebAuthn

The standard for passwordless authentication on the web.

- Mechanism: The user unlocks a private key stored on their device using a local gesture (PIN, Fingerprint). The device signs a challenge from the server.
- Security: Phishing-resistant. The private key never leaves the device.

### B. UAF Vs U2F (Legacy FIDO)

- UAF (Universal Authentication Framework): Passwordless experience (Biometrics).
- U2F (Universal 2nd Factor): The "Dongle" experience (YubiKey). Requires a password first, then the key.

### C. Passkeys

- Evolution: Syncable FIDO credentials. Allows the private key to exist across a user's ecosystem (e.g., iCloud Keychain), solving the "lost device" recovery problem.

---

## 3. M2M Authentication Patterns

Strategies for Machine-to-Machine communication where traditional MFA (OTP) is not feasible.

| Method | Mechanism | Use Case | Security Level |
|:--- |:--- |:--- |:--- |
| Client Credentials (OAuth) | App ID + Secret exchange for Token. | Service-to-Service, Daemons. | High (if secrets managed). |
| Mutual TLS (mTLS) | Certificate-based mutual auth. | Zero Trust Networks, Financial/Healthcare. | Very High (Hardware-bound). |
| JWT Assertion | Signed JWT used as credential. | Distributed Systems, Microservices. | High. |
| API Keys | Static string in header. | Public APIs, Simple Integrations. | Low (Hard to rotate). |
| Cloud IAM Roles | Identity federation / metadata service. | Cloud-native workloads (AWS/Azure). | Very High (Short-lived). |

---

## 4. Cloud-Native Identity Primitives

Cloud providers implement these standards as managed services to eliminate credential management.

| Provider | Mechanism | Underlying Protocol |
|:--- |:--- |:--- |
| AWS | IAM Roles for Service Accounts (IRSA) | OIDC + STS |
| Azure | Managed Identity (MSI) | OAuth 2.0 / OIDC |
| GCP | Workload Identity | OIDC Federation |
| K8s | Service Account Tokens | Projected Service Account Volumes (JWT) |

---

## 5. User Authentication Evolution

Moving beyond passwords to cryptographic proof of possession.

- FIDO2 / WebAuthn: Standard for passwordless auth. The "password" is a private key stored in a hardware authenticator (YubiKey) or platform module (TouchID/FaceID).
- Passkeys: Syncable FIDO2 credentials. Allows the private key to exist across devices (e.g., iCloud Keychain), balancing security with recovery.
