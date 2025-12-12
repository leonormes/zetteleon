---
aliases: []
confidence: 
created: 2025-08-15T03:15:45Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Common Properties and Claims of a Digital Identity
type:
uid: 
updated: 
version:
---

To provide an abstracted understanding of digital identity, we can define it functionally as "how we recognise, remember, and respond to specific people and things". Digital identity systems are designed to acquire, correlate, apply, reason over, and govern information assets pertaining to subjects, identifiers, attributes, raw data, and context. These systems enable trust in the digital world.

A subject is broadly defined as a person, organisation, software program, machine, or any other entity recorded within a system. While the term "identity" can be nuanced, an "identity record" typically refers to a collection of data about a subject, encompassing attributes, preferences, and traits. For practical purposes in system design, these are often collectively referred to as "attributes".

Here are the common properties and claims of a digital identity for both humans and machines/applications/processes:

**Common Properties and Claims of a Digital Identity:**

1. **Subject/Entity**: A digital identity pertains to an 'entity,' which can generically refer to the subject of an identity record, such as people, places, things, and organisations.
   - **For a human**: People are often conceptualised as having multiple "personas" or identities, which are different perspectives on their singular identity, often tied together by correlating attributes like name, address, or Social Security number. The core identity for a human is more complex and nuanced than what can be captured in a database record. The goal for humans is "digital embodiment," allowing them to act as autonomous peers in the digital world, rather than existing solely through the grace of administrative systems.
   - **For a machine/application/process (Thing)**: Devices, software programs, and processes also have identities. Examples include a car title, a computer, a piece of land, a movie ticket identifying its holder for a seat at a specific time, an invoice identifying a payment request, or an IoT lightbulb. Identity for things is crucial for managing control, data, and interactions in the Internet of Things (IoT).

2. **Attributes/Claims**: These are pieces of information about a subject.
   - **Attributes**: Characteristics that are acquired, such as a drug allergy, purchase history, or dress size for a person. For a machine, it could be its capabilities or current state.
   - **Preferences**: Desires and defaults, like preferred airline seating or default currency.
   - **Traits**: Inherent features that change slowly, if at all, such as eye colour for a person or how a company was incorporated.
   - A 'claim' is a statement about the entity to whom an identifier refers. Verifiable Credentials (VCs) are structured documents containing claims.

3. **Identifiers**: These are names or unique strings used to refer to a specific entity within a given namespace.
   - **Types**: Omnidirectional (public) identifiers are easily resolvable by anyone and are meant for discovery (e.g., URLs, domain names, email addresses). Unidirectional (peer or private) identifiers are used with a single site or relationship, providing better privacy protection as they don't leak correlatable information (e.g., usernames unique to a single site, cryptographically generated keys for a specific relationship).
   - **Properties**: Ideally, identifiers should be unique within a namespace, memorable, and short. Zooko's Triangle suggests an identifier can have at most two of three desirable properties: decentralized, secure, and human readable. Decentralized Identifiers (DIDs) are a type of cryptographic identifier designed to be nonreassignable, resolvable, cryptographically verifiable, and decentralised, functioning outside any specific context.

4. **Relationships**: Digital identity systems are primarily built to support digital relationships between entities.
   - **Integrity**: Ensures that you are dealing with the same entity across interactions, providing security and authenticity.
   - **Life Span**: Relationships can be long-lived (e.g., with Amazon) or ephemeral and short-lived (e.g., buying bolts from a specialty store, opening a door with a digital credential).
   - **Utility**: Relationships are created to provide specific functionality or purpose (e.g., an e-commerce site selling products, a social media site showing ads).
   - **Anonymity/Pseudonymity**: In the digital world, interactions are often pseudonymous (uniquely identified but other identifying information is not shared), rather than truly anonymous, due to the need for identifiers for session continuity, convenience, and trust.

5. **Control/Sovereignty**: Refers to who or what controls the relationship, including who initiates it, owns the identifier, sets rules, and determines attribute sharing.
   - **Administrative Control**: The majority of current identity systems are administrative, built and operated by an organisation that determines the rules, allowed attributes, and sharing. This leads to limited autonomy for the subject.
   - **User-Centred/Federated**: Offers a higher degree of autonomy where the person chooses the account to use, but the underlying account is still administrative.
   - **Self-Sovereign Identity (SSI)**: A model where parties exchange cryptographically mutually authenticated identifiers (like DIDs), providing trustworthy channels and reciprocal autonomy. The entity (person or organisation) has complete control over attributes they share.

6. **Trust and Confidence**: Essential for digital relationships to have utility.
   - **Trust**: Depends on personal vulnerability and risk-taking, often linked to provenance (reputation, institutional context, governance).
   - **Confidence**: Depends on internalised expectations derived from knowledge or past experiences, often linked to fidelity (cryptographic strength, protocols, authentication factors).

7. **Authenticity and Confidentiality**:
   - **Authenticity**: Allows parties in a conversation to know whom they are talking to. It is a foundational requirement for relationship integrity.
   - **Confidentiality**: Ensures that only authorised parties can view the content of a message or transaction.
   - There is a trade-off between privacy, authenticity, and confidentiality, where achieving strong authenticity often reduces privacy and vice versa.

In essence, digital identity, whether for a human or a machine, is an abstract construct of data, identifiers, and rules that enables entities to recognise, remember, and interact with each other in a controlled and verifiable manner across diverse digital contexts. It is not a single, universal solution but a polymorphic foundation for building interconnected identity systems that can adapt to varying needs for trust, privacy, and utility. The emergent "identity layer" or "identity metasystem" aims to provide common infrastructure and protocols for building these systems, much like the internet provides infrastructure for messaging systems.

Next step: We can explore how specific identity architectures (administrative, algorithmic, autonomic) differ in their implementation of these properties and claims, particularly regarding their trust bases and locus of control.

From an abstract perspective, the properties and claims of a digital identity are fundamentally the same for both a human and a machine They both serve to establish trust and enable secure interactions in a digital environment. The primary differences lie in the *nature* of the attributes and the *authority* that issues and verifies them.

A digital identity for any entity can be broken down into three core components: identifiers, attributes, and credentials.

---

## Common Abstracted Properties

At a high level, all digital identities, whether for a person or a process, share these fundamental properties:

- **Identifier**: A unique label used to refer to the entity. This is the "name" of the identity within a system (e.g., `user-123`, `api-service-alpha`).
- **Attributes**: A collection of **claims** or facts about the identifier. These describe what the entity *is* or *has*
- **Credentials**: A verifiable, tamper-evident way to present attributes This is how the identity proves its claims.
- **Lifecycle**: All identities have a lifecycle: they are created (provisioning), used, sometimes modified, and eventually deleted (de-provisioning).
- **Authorisation**: Based on its authenticated attributes, every identity is granted a set of permissions or entitlements detailing what it is allowed to do

---

## Identity Claims: Human vs. Machine

The key distinction between human and machine identities becomes clear when looking at the specific **claims** (attributes) they possess.

### 🧑 Human Digital Identity

A human's digital identity is designed to represent a person Its claims are tied to their legal and social existence.

- **Core Claims (Who you are):**
  - **Personally Identifiable Information (PII):** Legal name, date of birth, government ID numbers (e.g., National Insurance number, passport number) These are typically issued and verified by a government authority
  - **Biometrics:** Fingerprints, facial scans, voice patterns These claims link the digital identity to a unique physical person
  - **Contact Information:** Email address, phone number, physical address
- **Entitlement & Status Claims (What you are allowed):**
  - **Qualifications:** University degrees, professional certifications
  - **Status:** "Over 18", "UK Resident", "Employee", "Platinum Member".
  - **Relationships:** "Parent of [Child's ID]", "Spouse of [Spouse's ID]".
- **Behavioural Claims (How you act):**
  - **History:** Purchase history, browsing activity, search queries
  - **Reputation:** Credit score, online reviews, social media activity

### ⚙️ Machine/Application/Process Digital Identity

A machine identity is designed to represent a non-person entity (NPE) like a piece of software, a server, an IoT device, or a microservice Its claims relate to its function, origin, and operational context.

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

In summary, while the abstract structure is the same, human identity claims focus on **personal and legal characteristics**, whereas machine identity claims focus on **operational and functional characteristics**. Both use these verified claims to authenticate themselves and gain authorised access to resources

When considering Machine-to-Machine Two-Factor Authentication (2MFA), it is essential to adapt the principles of multi-factor authentication (MFA) from human-centric scenarios to the unique context of automated systems and devices. While the goal remains to enhance security by requiring more than one form of verification, the "factors" for machines manifest differently than for humans.

Here are best practices for Machine-to-Machine 2MFA, drawing upon concepts of digital identity, secure protocols, and robust cryptographic practices:

**1. Establish a Strong Digital Identity for Each Machine Entity:** Just as humans have digital identities, so too do machines, applications, and processes. This identity is "how we recognise, remember, and respond to specific people and things". For machines, this involves:

- **Unique Identifiers:** Each machine, device, or process should have a unique, non-reassignable, and non-guessable identifier. Decentralized Identifiers (DIDs) are an example of cryptographic identifiers designed to be non-reassignable, resolvable, cryptographically verifiable, and decentralised, functioning outside any specific context.
- **Cryptographic Keys as Core Identity:** Rely on public/private key pairs as the foundational "something you have" for machine identities. The private key remains secure on the machine, while the public key is used for verification. This forms a strong basis for mutual authentication, where each party can authenticate the other without sharing secrets.

**2. Implement Multi-Factor Verification for Machine Interactions:** Adapt the traditional MFA factors ("something you know," "something you have," "something you are") for machine contexts:

- **"Something you know" (Credentials/Secrets):** This translates to securely managed API keys, client secrets, or other shared cryptographic secrets. However, relying solely on shared secrets can introduce vulnerabilities if compromised.
- **"Something you have" (Possession Factor):** For machines, this is typically a dynamically generated, cryptographically strong token or credential.
  - **Access Tokens:** OAuth 2.0 uses Access Tokens for granting access to protected resources, which can be short-lived.
  - **Refresh Tokens:** For long-lived sessions, Refresh Tokens can be used to obtain new Access Tokens without re-authentication. Securely handling these, including setting appropriate lifecycles, is critical.
  - **Verifiable Credentials (VCs):** Machines can hold and present VCs to prove specific attributes about themselves (e.g., capabilities, current state, firmware version, ownership) in a cryptographically verifiable manner. This acts as a powerful "something you have" that can be selectively disclosed.
- **"Something you are/do/where you are" (Inherence/Behavior/Location for machines):**
  - **Device Fingerprinting:** Unique characteristics of a device's hardware, software configuration, or network environment can act as an implicit factor. This can include browser configuration, hardware, device information, location (IP address, GPS), and even Bluetooth-paired devices.
  - **Contextual Information:** Similar to human "trust zones," machine interactions can be evaluated based on expected operational context, such as usual network segments, time of day, or specific interaction patterns.

**3. Employ Secure Protocols and Architectures:**

- **OAuth 2.0 and OpenID Connect:** OAuth 2.0 is designed to accommodate various scenarios, including "interfaceless Consumers such as Internet of Things devices". The **Client Credentials Grant** is particularly suitable for machine-to-machine authentication where the client itself is the resource owner. OpenID Connect can be layered on top of OAuth 2.0 to provide richer identity information (claims) for machines if needed.
- **DIDComm for Self-Sovereign Machine Interactions:** DIDComm provides a "secure, private communication methodology built atop the decentralized design of DIDs". It allows machines (via "agents") to establish mutually authenticated peer relationships and exchange messages and verifiable credentials. This is especially relevant for a Self-Sovereign Internet of Things (SSIoT) where devices can have direct relationships with each other and their owners without manufacturer intermediation.
- **TLS/SSL for Data in Transit:** All machine-to-machine communications, especially those carrying sensitive data, must use secure channels like SSL/TLS. OAuth 2.0 relies on TLS for secure token transmission.
- **Secure Hashing and Key Stretching:** While more common for human passwords, the principle of using strong, slow hashing algorithms (like bcrypt, PBKDF2, scrypt) and key stretching is applicable to any machine-stored secrets to increase resistance to offline cracking.
- **Asynchronous Cryptography (Public/Private Keys):** Ideal for scenarios where channels might not be secure or parties do not trust each other, enabling encrypted communication and signature verification without sharing a secret key.
- **Synchronous Cryptography (Shared Secrets):** Suitable for trusted environments where a shared secret can be securely exchanged and maintained, offering faster encryption/decryption. Authenticated encryption modes like GCM are industry-accepted standards for providing both confidentiality and authenticity.
- **FIDO Protocols (U2F/UAF):** While often tied to physical user actions, the underlying public-key cryptography and the concept of a "platform authenticator" that creates, stores, and uses authentication keys securely and resists phishing attacks can inform secure hardware-backed machine identities.

**4. Implement Robust Key Management and Lifecycle:**

- **Automated Key Generation and Rotation:** Keys should be generated securely, preferably by the machine itself or a trusted hardware component (e.g., TPM). Implement automated key rotation and secure key updates for DIDs without changing the identifier.
- **Secure Storage of Keys:** Private keys must be stored in secure enclaves or hardware security modules (HSMs) where possible, ensuring they cannot be easily extracted or compromised.
- **Revocation Mechanisms:** Implement mechanisms to revoke compromised machine identities or credentials, immediately invalidating them across the system.

**5. Prioritize Security by Design and Minimal Disclosure:**

- **Zero Trust Architecture:** Implement access control based on the "zero trust" principle, where no machine or process is inherently trusted; access is granted dynamically based on verified identity and attributes.
- **Attribute-Based Access Control (ABAC):** For machines, ABAC is highly flexible, allowing authorization based on various attributes of the machine, the resource, and the context, enabling fine-grained control and reducing over-privileging.
- **Minimal Disclosure:** Design M2M communication to share only the absolute minimum amount of information required for a transaction or authorization. VCs with Zero-Knowledge Proofs (ZKPs) can be leveraged for this, allowing a machine to prove a characteristic without revealing underlying sensitive data.
- **Functional Privacy:** While privacy for machines might seem less critical than for humans, limiting data collection and ensuring confidentiality of M2M communications (e.g., operational data, sensitive process information) is crucial to prevent leakage and misuse.

**6. Ensure Auditability and Monitoring:**

- **Comprehensive Logging:** All authentication and authorization attempts, key rotations, and credential issuances/presentations should be logged. These logs must be tamper-resistant to ensure auditability.
- **Anomaly Detection:** Continuously monitor M2M interaction patterns for unusual or suspicious activities, which could indicate a compromise.

**7. Implement Layered Security (Defense in Depth):**

- No single security measure is foolproof. Combine multiple practices to create a robust defense. This includes securing data at rest (database encryption) and in motion (TLS, authenticated encryption), along with strong authentication and authorization protocols.

By integrating these practices, organisations can build a robust 2MFA framework for their machine and IoT ecosystems, mitigating risks and enabling secure, autonomous interactions.

Next step: We can delve into specific technical implementations of these practices, such as how DIDs and VCs might be architected for IoT devices with limited processing power, or how to manage the lifecycle of machine-specific cryptographic keys.
