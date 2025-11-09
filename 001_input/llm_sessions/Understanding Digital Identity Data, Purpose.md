---
aliases: []
author: ["[[Gemini]]"]
confidence: 
created: 2025-08-22T00:00:00Z
description: Created with Gemini
epistemic: 
last_reviewed: 
modified: 2025-10-30T11:06:55Z
published:
purpose: 
review_interval: 
see_also: []
source: https://gemini.google.com/share/2e391d97c8be
source_of_truth: []
status: 
tags: []
title: Understanding Digital Identity Data, Purpose
type:
uid: 
updated: 
version:
---

---

## What is a Digital Identity? A Data-Centric View

From a data-centric perspective, a **digital identity** is not a single, monolithic object. Instead, it is a collection of electronically stored and correlated **attributes** that describe an entity (a person, organisation, or device) within a specific digital context.

It is best understood through its core data components:

1. **Identifiers**: These are unique labels used to refer to a specific identity within a system. An identifier acts as a primary key or pointer to the collection of attributes. Examples include a username, an email address, a universally unique identifier (UUID), or a passport number. A single person will have many different identifiers across the various systems they interact with.
2. **Attributes**: These are individual pieces of data or claims made about the subject of the identity. They are key-value pairs. For example:
   - `given_name: "John"`
   - `date_of_birth: "1990-10-26"`
   - `is_over_18: true`
   - `role: "administrator"`
   - Attributes can be self-asserted (e.g., you state your name on a forum) or verified by a trusted authority (e.g., the government digitally attests to your date of birth).
3. **Credentials**: These are tamper-evident, machine-readable data structures that bind attributes to an identifier. They are issued by an authority and can be presented to a relying party to prove the attributes are valid. A credential is the digital equivalent of a physical document like a driver's licence or a passport. It allows you to prove a specific attribute (e.g., "I am over 18") without necessarily revealing all your other attributes (like your full date of birth or address).

In essence, a digital identity is the sum of all the data—the identifiers, attributes, and credentials—that represents you online. This data is often fragmented and stored in different *identity silos* controlled by various organisations (e.g., Google, your bank, the NHS, your employer).

## How is a Digital Identity Related to a Person

A digital identity is a **proxy** or a **digital representation** of a natural person. It is not the person themselves, but rather the set of data that stands in for them in digital interactions. The relationship between the data (the digital identity) and the person (the subject) is established and maintained through a critical process known as **identity proofing** or **binding**.

- **Binding**: This is the act of linking the digital representation to the physical person with a certain degree of confidence. For example, when you open a bank account online, you might scan your physical passport and take a selfie. The bank's system analyses these inputs to "bind" the digital account they are creating to you, the real person.
- **Levels of Assurance (LoA)**: The strength and trustworthiness of this binding determine the identity's Level of Assurance.
  - A **low LoA** identity might only require an email address and a self-asserted name (e.g., a social media account). The link to the actual person is weak.
  - A **high LoA** identity involves rigorous proofing against authoritative sources, like government-issued documents and biometric checks (e.g., a Gov.UK Verify identity). The link to the person is strong and reliable.

A single person can possess multiple digital identities, each tailored to a different context. You have a professional identity on LinkedIn, a social identity on Instagram, and a citizen identity with the government. These are all distinct collections of data representing different facets of you as a person.

## What is Its Purpose from an Abstract Point of View

From an abstract viewpoint, the fundamental purpose of a digital identity is to **establish sufficient trust to enable interactions in a digital environment**. It achieves this by performing three core functions:

1. **Authentication**: To answer the question, " *Are you who you claim to be?*". Authentication is the process of verifying a claimed identity. When you enter a password or use your fingerprint to log in, you are authenticating. You are proving to the system that you are the legitimate operator of that digital identity.
2. **Authorisation**: To answer the question, " *Are you allowed to do that?*". Once a user's identity has been authenticated, authorisation determines what actions they are permitted to perform. The attributes of the identity (e.g., `role: "manager"`, `clearance_level: "secret"`) are used by systems to grant or deny access to resources, data, or functionalities.
3. **Attribution & Accountability**: To reliably link digital actions to a specific identity, and by extension, to the person it represents. This creates a record of who did what and when. This function is the foundation for establishing legal and commercial trust, enabling concepts like non-repudiation (the inability to deny an action, such as signing a digital contract) and accountability.

Ultimately, digital identity is the core mechanism that allows us to recreate the concepts of recognition, trust, permission, and accountability from the physical world within the digital realm.

What are the common properties and claims of a digital identity for a human and for a machine/application/process? I want the abstracted understanding of digital identity.

From an abstract perspective, the properties and claims of a digital identity are fundamentally the same for both a human and a machine. They both serve to establish trust and enable secure interactions in a digital environment. The primary differences lie in the *nature* of the attributes and the *authority* that issues and verifies them.

A digital identity for any entity can be broken down into three core components: identifiers, attributes, and credentials.

---

## Common Abstracted Properties

At a high level, all digital identities, whether for a person or a process, share these fundamental properties:

- **Identifier**: A unique label used to refer to the entity. This is the "name" of the identity within a system (e.g., `user-123`, `api-service-alpha`).
- **Attributes**: A collection of **claims** or facts about the identifier. These describe what the entity *is* or *has*.
- **Credentials**: A verifiable, tamper-evident way to present attributes. This is how the identity proves its claims.
- **Lifecycle**: All identities have a lifecycle: they are created (provisioning), used, sometimes modified, and eventually deleted (de-provisioning).
- **Authorisation**: Based on its authenticated attributes, every identity is granted a set of permissions or entitlements detailing what it is allowed to do.

---

## Identity Claims: Human vs. Machine

The key distinction between human and machine identities becomes clear when looking at the specific **claims** (attributes) they possess.

### 🧑 Human Digital Identity

A human's digital identity is designed to represent a person. Its claims are tied to their legal and social existence.

- **Core Claims (Who you are):**
  - **Personally Identifiable Information (PII):** Legal name, date of birth, government ID numbers (e.g., National Insurance number, passport number).These are typically issued and verified by a government authority.
  - **Biometrics:** Fingerprints, facial scans, voice patterns.These claims link the digital identity to a unique physical person.
  - **Contact Information:** Email address, phone number, physical address.
- **Entitlement & Status Claims (What you are allowed):**
  - **Qualifications:** University degrees, professional certifications.
  - **Status:** "Over 18", "UK Resident", "Employee", "Platinum Member".
  - **Relationships:** "Parent of \[Child's ID\]", "Spouse of \[Spouse's ID\]".
- **Behavioural Claims (How you act):**
  - **History:** Purchase history, browsing activity, search queries.
  - **Reputation:** Credit score, online reviews, social media activity.

### ⚙️ Machine/Application/Process Digital Identity

A machine identity is designed to represent a non-person entity (NPE) like a piece of software, a server, an IoT device, or a microservice. Its claims relate to its function, origin, and operational context.

- **Core Claims (What it is):**
  - **Unique Identifiers:** Universally Unique Identifier (UUID), MAC address, service name, process ID (PID), cryptographic key pair.
  - **Origin & Integrity:** Software vendor, code signature, version number, hash of the binary. These claims prove it hasn't been tampered with.
  - **Configuration:** IP address, operating system, location (e.g., `aws:region:eu-west-2`), hardware specifications.
- **Entitlement & Status Claims (What it is allowed):**
  - **Roles & Permissions:** "Database Reader", "Queue Writer", "Metrics Publisher". These are often defined within an Identity and Access Management (IAM) system.
  - **Security Posture:** Security patch level, last vulnerability scan date, compliance status (e.g., "PCI-DSS Compliant").
- **Behavioural Claims (How it acts):**
  - **Operational Telemetry:** CPU usage patterns, network traffic flows, API call logs.
  - **Reputation:** Known good or malicious process, IP address reputation.

In summary, while the abstract structure is the same, human identity claims focus on **personal and legal characteristics**, whereas machine identity claims focus on **operational and functional characteristics**. Both use these verified claims to authenticate themselves and gain authorised access to resources.
