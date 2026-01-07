---
aliases: ["Identity Fundamentals", "Machine Identity", "Human Identity", "Digital Identity Properties"]
confidence: "High"
created: 2026-01-06
epistemic: "Foundation"
last_reviewed: 
modified: 
purpose: "To define the abstract properties of Digital Identity for both humans and machines, serving as the foundational model for all IAM and authentication architectures."
review_interval: "1 year"
see_also: 
  - "[[SoT - Public Key Infrastructure (PKI) and Trust]]"
  - "[[SoT - Modern Authentication Standards]]"
  - "[[SoT - Zero Trust Architecture]]"
source_of_truth: []
status: "Active"
tags: ["identity", "iam", "security", "architecture", "concepts"]
title: SoT - Digital Identity
type: "SoT"
uid: 
updated: 
---

# SoT - Digital Identity

> **Definition:** Digital Identity is "how we recognize, remember, and respond to specific people and things." It is the set of **Attributes**, **Identifiers**, and **Credentials** that allow an entity to exist and act within a digital system.

## 1. The Trinity of Identity

Every digital identity consists of three core components:

1.  **Identifier (The Name):** A unique string referring to the entity (e.g., `user-123`, `api-service-alpha`, `leon.ormes@company.com`).
2.  **Attributes (The Claims):** Facts *about* the entity (e.g., "Role: Admin", "Department: Engineering", "Region: EU-West").
3.  **Credentials (The Proof):** Secrets used to prove ownership of the identity (e.g., Password, API Key, X.509 Certificate, Biometrics).

---

## 2. Human vs. Machine Identity

While the structure is shared, the nature of the claims differs fundamentally.

### A. Human Identity
*   **Context:** Tied to legal and social existence. High complexity, "personas," and privacy concerns.
*   **Core Claims:** PII (Name, Email), Biometrics, Legal Status.
*   **Entitlements:** Qualifications, Organizational Role ("Manager"), Relationships.
*   **Behavior:** Unpredictable, adaptive.
*   **Lifecycle:** Long-lived (Joiner, Mover, Leaver).

### B. Machine Identity (Non-Person Entity - NPE)
*   **Context:** Workloads, devices, containers, and services.
*   **Core Claims:** IP Address, MAC Address, Service Name, Image Hash.
*   **Entitlements:** Functional Permissions ("Can Write to S3", "Can Read Queue").
*   **Behavior:** Deterministic, repetitive.
*   **Lifecycle:** Often ephemeral (spin up, execute, destroy).

---

## 3. Properties of Identity Systems

### A. Identifiers
*   **Omnidirectional:** Public discovery (Email, DNS). Resolvable by anyone.
*   **Unidirectional:** Private scope (Internal UUID). Used for privacy or internal logic.
*   **Zooko's Triangle:** Identifiers can only be two of three: **Decentralized**, **Secure**, and **Human-Readable**. (e.g., DIDs are Decentralized + Secure, but not Readable).

### B. Control Models
*   **Administrative (Centralized):** The organization owns the identity (e.g., Active Directory). Most common in enterprise.
*   **Federated:** The user brings an identity from a trusted provider (e.g., "Log in with Google").
*   **Self-Sovereign (SSI):** The entity owns the identity and keys entirely (e.g., DIDs, Verifiable Credentials).

### C. Trust & Confidence
*   **Trust:** Based on **Provenance** (Who issued this? Do I trust the issuer?).
*   **Confidence:** Based on **Fidelity** (How strong was the authentication? MFA vs Password).

---

## 4. Architectural Implications

1.  **Least Privilege:** Identities should only possess the attributes required for their function. Machine identities should have zero access to human data unless explicitly required.
2.  **Lifecycle Management:**
    *   *Humans:* Focus on efficient Onboarding/Offboarding (JML).
    *   *Machines:* Focus on automated rotation (Short-lived Certs, SPIFFE/SPIRE).
3.  **The Identity Layer:** Identity is the new perimeter. Trust is no longer based on "being on the network" but on "proving who you are."