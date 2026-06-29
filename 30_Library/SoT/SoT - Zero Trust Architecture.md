---
aliases:
- Identity as Perimeter
- Never Trust Always Verify
- Zero Trust
- ZT Architecture
created: 2026-04-04 14:30:00+00:00
last-synthesis: 2026-04-04
last_reviewed: null
modified: 2026-05-26 11:44:16+00:00
status: evergreen
synthesis-count: 1
tags:
- architecture
- iam
- networking
- security
- zero-trust
title: SoT - Zero Trust Architecture
trust-level: stable
type: SoT
permalink: llmeon/30-library/so-t/so-t-zero-trust-architecture
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
3. Least Privilege: Once authenticated, an identity is granted only the minimum necessary permissions to perform its specific task, limiting the "blast radius" of a potential compromise.
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

- Vault: Manages secrets and identity-based access for systems and applications.
- Consul: Enables service-to-service identity (mTLS) and microsegmentation (Intentions).
- Boundary: Secures remote access based on user identity and authorized targets, replacing traditional VPNs.

---

## Related Knowledge

- Identity Data Model: [[SoT - Data-Centric IAM in Zero Trust]]
- Digital Identity Fundamentals: [[SoT - Digital Identity]]
- Platform Implementation: [[SoT - Microsoft Entra Identity]]
- Industry Compliance: [[SoT - NHS Identity Compliance]]
- Network Security: [[SoT - Network Security Architecture]]
- Governance: [[SoT - NIST Cybersecurity Framework]]
- Operationalization: [[Protocol - NIST CSF Implementation via Microsegmentation]]