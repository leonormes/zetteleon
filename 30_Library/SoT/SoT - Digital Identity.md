---
aliases: [Digital Identity Properties, Human Identity, Identity Fundamentals, Machine Identity]
conformant: false
created: 2025-12-29T20:02:16+00:00
last_reviewed: null
modified: 2026-07-20T16:33:51+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-digital-identity
status: Active
tags: [concepts, iam, SoftwareEngineering/Architecture, SoftwareEngineering/Security, TheHuman/Identity]
title: SoT - Digital Identity
type: sot
updated: null
---

## SoT - Digital Identity

> Definition: Digital Identity is "how we recognize, remember, and respond to specific people and things." It is the set of Attributes, Identifiers, and Credentials that allow an entity to exist and act within a digital system.

### 1. The Trinity of Identity

Every digital identity consists of three core components:

1. Identifier (The Name): A unique string referring to the entity (e.g., `user-123`, `api-service-alpha`, `leon.ormes@company.com`).
2. Attributes (The Claims): Facts _about_ the entity (e.g., "Role: Admin", "Department: Engineering", "Region: EU-West").
3. Credentials (The Proof): Secrets used to prove ownership of the identity (e.g., Password, API Key, X.509 Certificate, Biometrics).

---

### 2. Human vs. Machine Identity

While the structure is shared, the nature of the claims differs fundamentally.

#### A. Human Identity

- Context: Tied to legal and social existence. High complexity, "personas," and privacy concerns.
- Core Claims: PII (Name, Email), Biometrics, Legal Status.
- Entitlements: Qualifications, Organizational Role ("Manager"), Relationships.
- Behavior: Unpredictable, adaptive.
- Lifecycle: Long-lived (Joiner, Mover, Leaver).

#### B. Machine Identity (Non-Person Entity - NPE)

- Context: Workloads, devices, containers, and services.
- Core Claims: IP Address, MAC Address, Service Name, Image Hash.
- Entitlements: Functional Permissions ("Can Write to S3", "Can Read Queue").
- Behavior: Deterministic, repetitive.
- Lifecycle: Often ephemeral (spin up, execute, destroy).

---

### 3. Properties of Identity Systems

#### A. Identifiers

- Omnidirectional: Public discovery (Email, DNS). Resolvable by anyone.
- Unidirectional: Private scope (Internal UUID). Used for privacy or internal logic.
- Zooko's Triangle: Identifiers can only be two of three: Decentralized, Secure, and Human-Readable. (e.g., DIDs are Decentralized + Secure, but not Readable).

#### B. Control Models

- Administrative (Centralized): The organization owns the identity (e.g., Active Directory). Most common in enterprise.
- Federated: The user brings an identity from a trusted provider (e.g., "Log in with Google").
- Self-Sovereign (SSI): The entity owns the identity and keys entirely (e.g., DIDs, Verifiable Credentials).

#### C. Trust & Confidence

- Trust: Based on Provenance (Who issued this? Do I trust the issuer?).
- Confidence: Based on Fidelity (How strong was the authentication? MFA vs Password).

### 4. The Identity Lifecycle

#### A. Establishing an Identity (Identity Management)

Digital identity is the foundation for establishing trust. The lifecycle includes:

- Registration/Creation: Generating an identity and securely linking it to a real-world entity.
- Provisioning: Creating, modifying, or deleting user accounts across systems (e.g., HR to IdP, IdP to Apps).
- Maintenance: Constantly updating identity information as roles change or entities leave the organization.

#### B. Verifying an Identity (Authentication)

Trust is established by computing an assertion that the entity can provide information only they possess ("Proof of Possession").

- Credential-based: Password policies (length, rotation, smart lockout).
- Challenge-Response: Protocols like CHAP for remote network access.
- Biometric Identification: Measuring physiological traits (Fingerprint, FaceID).
- MFA: Adding layers of verification (SMS, Push, Hardware tokens).
- Passwordless: Leveraging public key cryptography (FIDO2/WebAuthn) for phishing-resistant auth.

#### C. Role of Attributes

Attributes (Name, Role, Security Clearance) are crucial for Authorization decisions. Modern IAM systems enforce the principle of "Never Trust, Always Verify," using contextual attributes (device, location, behavior) for continuous authentication.

---

### 5. Federated Identity Management (FIM)

FIM allows the use of a single identity across multiple organizations, shifting verification toward a trusted Identity Provider (IdP). Technologies like SAML, OpenID Connect (OIDC), and OAuth 2.0 enable this cross-organizational trust.

---

### 6. Architectural Implications

1. Least Privilege: Identities should only possess the attributes required for their function. Machine identities should have zero access to human data unless explicitly required.
2. Lifecycle Management:
    - _Humans:_ Focus on efficient Onboarding/Offboarding (JML).
    - _Machines:_ Focus on automated rotation (Short-lived Certs, SPIFFE/SPIRE).
3. The Identity Layer: Identity is the new perimeter. Trust is no longer based on "being on the network" but on "proving who you are."
