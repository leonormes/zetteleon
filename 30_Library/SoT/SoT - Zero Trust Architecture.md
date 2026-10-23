---
aliases: [Identity as Perimeter, Never Trust Always Verify, Zero Trust, ZT Architecture]
conformant: true
created: 2026-04-04T14:30:00+00:00
last-synthesis: 2026-04-04
modified: 2026-10-22T15:11:10+00:00
permalink: llmeon/30-library/so-t/so-t-zero-trust-architecture
tags: [architecture, iam, networking, security, zero-trust]
title: SoT - Zero Trust Architecture
type: sot
---

## Minimum Viable Understanding (MVU)

Zero Trust is a security model that fundamentally rejects the notion of "implicit trust" based on network location. It operates on the core principle: "Never Trust, Always Verify." In this framework, every user, device, application, and network flow is considered untrusted by default, regardless of whether it originates inside or outside the traditional network perimeter.

---

## 1. The Shift: From Perimeter to Identity

### The Flaw of Traditional Perimeters

Traditional security relies on a Perimeter-Based Model (the "Castle and Moat" or "Hard Shell, Soft Interior"). A firewall creates a boundary around a "trusted" internal network.

Vulnerabilities:

- Implicit Trust: Once an attacker breaches the shell, they can move laterally with ease.
- Blind Spots: Lack of Intra-zone traffic inspection; the system assumes internal entities are inherently safe.
- Modern Complexity: Cloud, mobile, and remote work render a static physical perimeter obsolete.

### Identity as the New Control Plane

Zero Trust shifts the point of control from physical network boundaries to the Trusted Identities of users, devices, and applications. Identity becomes the Logical Perimeter.

---

## 2. Core Principles of Zero Trust

1. Identity-Driven Security: Access decisions are primarily based on the verified identity of the requester. Every entity must have a unique set of credentials and must be rigorously authenticated.
2. Explicit Verification: Every access request, regardless of origin, must be explicitly verified based on identity and contextual factors (device health, location, time) before access is granted.
3. Least Privilege: Once authenticated, an identity is granted only the minimum necessary permissions to perform its specific task, limiting the "blast radius" of a potential compromise. [synthesizes:: [[Least Privilege Authorization with Terraform Cloud]]]
4. Assume Breach: Operate under the assumption that attackers are already present within the network. This necessitates continuous verification and strict internal access controls to block lateral movement.
5. Mutual Authentication: Trust is established in both directions; not only does the user authenticate to the resource, but the resource must also authenticate its identity to the user (e.g., via mTLS).

---

## 3. Implementation Framework

### Secure Introduction (Bootstrapping Trust)

For new entities to join the system, a secure introduction process is required.

- Humans: Robust identity creation paired with real-world verification.
- Devices: Leveraging hardware-based trust anchors (TPMs) or "known-good" images.

### Trust Anchors and Chains

Trust typically originates from a Root of Trust (e.g., a Certificate Authority in a PKI system) and is delegated through a chain of signed assertions.

### Microsegmentation

Zero Trust facilitates the isolation of workloads into granular segments. Access is granted only between specific, identified services that need to communicate, rather than broad network subnets.

---

## 4. Challenges & Maintenance

### Challenges

- Legacy Systems: Retrofitting modern cryptography and identity protocols into older systems that rely on perimeter trust.
- Heterogeneous Environments: Maintaining consistent policy across diverse devices, clouds, and operating systems.
- Control Plane Security: The system responsible for policy decisions (the "Brain") becomes the most critical target.

### Maintenance

- Continuous Monitoring: Maintaining comprehensive logs and telemetry to detect anomalies.
- Dynamic Trust Scores: Trust is not static; it fluctuates based on behavior, device health, and risk signals.
- Short-Lived Access: Using ephemeral tokens and frequent credential rotation to reduce the window of opportunity for attackers.

---

## 5. Practical Stack (HashiCorp Zero Trust)

HashiCorp provides a suite of tools that operationalize these principles:

- Vault: Manages secrets and identity-based access for systems and applications. [synthesizes:: [[SoT - HashiCorp Vault Architecture]]]
- Consul: Enables service-to-service identity (mTLS) and microsegmentation (Intentions).
- Boundary: Secures remote access based on user identity and authorized targets, replacing traditional VPNs.

---

## 6. Applied Controls (Atomic Notes)

How the principles in section 2 show up as concrete, checkable controls in the vault.

- Explicit Verification: [[Phishing-Resistant MFA]] makes the verification step resistant to credential theft. [synthesizes:: [[Phishing-Resistant MFA]], confidence=high]
- Explicit Verification: [[Legacy Authentication Blocking]] closes the protocols that cannot be challenged for MFA, so no request skips verification.
- Least Privilege and Short-Lived Access: [[Just-In-Time (JIT) Admin Access]] grants privileged roles only when needed and only for a time-bound window. [synthesizes:: [[Just-In-Time (JIT) Admin Access]], confidence=high]
- Identity-Driven Security for Workloads: [[Workload Identity Governance]] applies the same rigour to service principals and AI agents as to people. [synthesizes:: [[Workload Identity Governance]], confidence=high]
- Assume Breach: [[Shared Account Interactive Access Restriction]] and [[Directory Creation Restrictions]] limit what a compromised identity can use to move laterally.
- Secure Introduction for Devices: [[Trusted Launch for Critical Infrastructure]] supplies the hardware trust anchor (Secure Boot, vTPM) described under Bootstrapping Trust. [synthesizes:: [[Trusted Launch for Critical Infrastructure]], confidence=medium]

---

## Related Knowledge

- Identity Data Model: [[SoT - Data-Centric IAM in Zero Trust]] [depends_on:: [[SoT - Data-Centric IAM in Zero Trust]]]
- Digital Identity Fundamentals: [[SoT - Digital Identity]] [depends_on:: [[SoT - Digital Identity]]]
- Platform Implementation: [[SoT - Microsoft Entra Identity]] [depends_on:: [[SoT - Microsoft Entra Identity]]]
- Industry Compliance: [[SoT - NHS Identity Compliance]] [depends_on:: [[SoT - NHS Identity Compliance]]]
- Network Security: [[SoT - Network Security Architecture]] [depends_on:: [[SoT - Network Security Architecture]]]
- Governance: [[SoT - NIST Cybersecurity Framework]] [depends_on:: [[SoT - NIST Cybersecurity Framework]]]
- Operationalization: [[Protocol - NIST CSF Implementation via Microsegmentation]] [depends_on:: [[Protocol - NIST CSF Implementation via Microsegmentation]]]
- Protocols and Tokens: [[SoT - Modern Authentication Standards]] covers the OIDC, OAuth 2.0 and mTLS mechanisms that carry identity in this model.
- Segmentation Detail: [[SoT - Network Segmentation]] expands the microsegmentation approach in section 3.
- Transport Security: [[SoT - The Data Architecture of TLS 1.3]] describes the handshake data that mTLS builds on.

### Further Reading (Personal Library)

- [Zero Trust Networks — "Evolution of the Threat Landscape", p. 27](calibre://view-book/GCcalibreBooks/750/EPUB) - _Describes how a single compromised host becomes a stepping stone, which is the lateral-movement flaw of perimeter models in section 1._
- [Zero Trust Networks — "Trust Signals", p. 24](calibre://view-book/GCcalibreBooks/750/EPUB) - _Covers mining historical user activity to judge current trustworthiness, matching the Dynamic Trust Scores point in section 4._
- [Distributed Services With Go — "Authenticate the Server with TLS"](calibre://view-book/GCcalibreBooks/321/EPUB) - _A worked mTLS example of the two-way verification in Core Principle 5._
- [Learning Helm — "Client certificates"](calibre://view-book/GCcalibreBooks/234/EPUB) - _Shows a server verifying the client certificate during the TLS handshake, the mTLS mechanism in practice._
