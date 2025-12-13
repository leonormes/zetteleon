---
aliases: [Authentication, Authorization, Credentials, Digital Identity, Identity Attributes, Identity Data]
confidence: 5/5
created: 2025-12-13T00:00:00Z
epistemic: technical
last-synthesis: 2025-12-13
last_reviewed: 2025-12-13
modified: 2025-12-13T14:08:09Z
purpose: To define digital identity from a data-centric perspective, outlining
  its core components, purpose, and abstracted properties for both human and
  machine entities.
related-soTs: '["[[SoT - PRODOS (System Architecture)]]", "[[SoT -
  Identity-Based Habit Formation]]", "[[SoT - Zero Trust Security]]", "[[SoT -
  Data-Centric IAM in Zero Trust]]", "[[SoT - Authentication Mechanisms]]",
  "[[SoT - Authorization Mechanisms]]"]'
review_interval: 6 months
see_also: []
source_of_truth: true
status: stable
tags: [authentication, authorization, data, IAM, identity, security]
title: SoT - Digital Identity
type: SoT
uid: null
updated: null
---

## 1. Definitive Statement

> [!definition] Digital Identity (Data-Centric View)
> A **digital identity** is a dynamic, context-specific collection of electronically stored and correlated **attributes** that describe an entity (person, organization, or device) within a digital environment. It serves as a **proxy** for the real-world entity, enabling trust and interaction.

---

## 2. Core Components of a Digital Identity

A digital identity is best understood through its fundamental data components:

### A. Identifiers

Unique labels used to refer to a specific identity within a system. An identifier acts as a primary key or pointer to the collection of attributes.

-   **Purpose:** To uniquely name an entity within a given context.
-   **Examples:** Username, email address, UUID, passport number (digitized). A single person has multiple identifiers across various systems.

### B. Attributes

Individual pieces of data or claims made about the subject of the identity. These are key-value pairs that describe what the entity *is* or *has*.

-   **Purpose:** To describe characteristics of the entity.
-   **Types:**
    -   **Self-asserted:** Claimed by the entity itself (e.g., "My name is John").
    -   **Verified:** Attested by a trusted authority (e.g., government digitally confirms date of birth).
-   **Examples:** `given_name: "John"`, `date_of_birth: "1990-10-26"`, `is_over_18: true`, `role: "administrator"`.

### C. Credentials

Tamper-evident, machine-readable data structures that cryptographically bind attributes to an identifier. They are issued by an authority and presented to a relying party to prove claims.

-   **Purpose:** To verifiably prove specific attributes without necessarily revealing all other attributes.
-   **Examples:** Digital equivalent of a driver's license (proves "over 18" without revealing exact DOB). Can be passwords, digital certificates, OAuth tokens.

---

## 3. Purpose of Digital Identity (Abstract View)

From an abstract viewpoint, the fundamental purpose of a digital identity is to **establish sufficient trust to enable interactions in a digital environment**. It achieves this by performing three core functions:

### A. Authentication

To answer the question, "*Are you who you claim to be?*".

-   **Mechanism:** Verifying a claimed identity (e.g., password, fingerprint, digital certificate).
-   **Outcome:** Proving to the system that the entity is the legitimate operator of that digital identity.

### B. Authorization

To answer the question, "*Are you allowed to do that?*".

-   **Mechanism:** Determining what actions an authenticated entity is permitted to perform based on its attributes (e.g., `role: "manager"`, `clearance_level: "secret"`).
-   **Outcome:** Granting or denying access to resources, data, or functionalities.

### C. Attribution & Accountability

To reliably link digital actions to a specific identity, and by extension, to the person or system it represents.

-   **Mechanism:** Creating a verifiable record of who did what and when.
-   **Outcome:** Enabling legal and commercial trust, non-repudiation (inability to deny an action), and accountability.

---

## 4. Identity Claims: Human vs. Machine

While the abstract properties are shared, the *nature* of the claims (attributes) and the *authority* that verifies them differ significantly.

### A. 🧑 Human Digital Identity

Designed to represent a natural person; its claims are tied to legal and social existence.

-   **Core Claims (Who you are):**
    -   **Personally Identifiable Information (PII):** Legal name, date of birth, government ID numbers (e.g., passport). Verified by government authorities.
    -   **Biometrics:** Fingerprints, facial scans, voice patterns (link digital identity to unique physical person).
    -   **Contact Information:** Email, phone, physical address.
-   **Entitlement & Status Claims (What you are allowed):**
    -   **Qualifications:** University degrees, professional certifications.
    -   **Status:** "Over 18", "UK Resident", "Employee", "Platinum Member".
-   **Behavioural Claims (How you act):**
    -   **History:** Purchase history, browsing activity.
    -   **Reputation:** Credit score, online reviews.

### B. ⚙️ Machine/Application/Process Digital Identity

Designed to represent a non-person entity (NPE) like software, server, IoT device, or microservice. Claims relate to its function, origin, and operational context.

-   **Core Claims (What it is):**
    -   **Unique Identifiers:** UUID, MAC address, service name, process ID (PID), cryptographic key pair.
    -   **Origin & Integrity:** Software vendor, code signature, version number, hash of the binary (proves no tampering).
    -   **Configuration:** IP address, operating system, location (e.g., `aws:region:eu-west-2`), hardware specifications.
-   **Entitlement & Status Claims (What it is allowed):**
    -   **Roles & Permissions:** "Database Reader", "Queue Writer", "Metrics Publisher" (defined within IAM).
    -   **Security Posture:** Security patch level, last vulnerability scan date, compliance status (e.g., "PCI-DSS Compliant").
-   **Behavioural Claims (How it acts):**
    -   **Operational Telemetry:** CPU usage patterns, network traffic flows, API call logs.
    -   **Reputation:** Known good or malicious process, IP address reputation.

---

## 5. Relationship to a Person & Levels of Assurance

A digital identity is a **proxy** of a natural person. The link between the data (digital identity) and the person (subject) is through **identity proofing** or **binding**.

-   **Binding:** The act of linking the digital representation to the physical person with a certain confidence level (e.g., scanning a passport and taking a selfie for a bank account).
-   **Levels of Assurance (LoA):** The strength of this binding.
    -   **Low LoA:** Email and self-asserted name (e.g., social media). Weak link.
    -   **High LoA:** Rigorous proofing against authoritative sources (government IDs, biometrics). Strong, reliable link.

A single person can have multiple digital identities, each for a different context (professional, social, citizen).

---

## 6. Minimum Viable Understanding (MVU)

1.  **Digital Identity = Data:** It's a collection of identifiers, attributes, and verifiable credentials.
2.  **Purpose = Trust:** It enables authentication ("who are you?"), authorization ("what can you do?"), and accountability ("who did it?").
3.  **Human ≠ Machine:** Claims differ significantly (personal/legal vs. operational/functional).
4.  **Identity is a Proxy:** It's a digital representation, bound to a person with varying Levels of Assurance.

---

## 7. Sources and Links
-   Original Proposal: "What is a Digital Identity? A Data-Centric View" (Archived)
-   [[SoT - PRODOS (System Architecture)]] (Foundational for system architecture)
-   [[SoT - Identity-Based Habit Formation]] (Relates to human identity and self-perception)
-   [[SoT - Zero Trust Security]] (Foundational security model for modern identity management)
-   [[SoT - Data-Centric IAM in Zero Trust]] (Details IAM within a Zero Trust framework)
-   [[SoT - Authentication Mechanisms]] (Explores different methods of verifying identity)
-   [[SoT - Authorization Mechanisms]] (Explores different methods of granting permissions)
