---
aliases: [Defense in Depth, Layered Defense, Network Security Components, Security Architecture]
created: 2026-04-02T12:00:00+00:00
modified: 2026-07-13T08:52:51+00:00
permalink: llmeon/30-library/so-t/so-t-network-security-architecture
source_of_truth: true
tags: [architecture, infrastructure, networking, security]
title: SoT - Network Security Architecture
type: sot
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## Minimum Viable Understanding (MVU)

Network Security Architecture is a framework of policies, technologies, and controls designed to protect an organization's network infrastructure. It prioritizes Layered Defense (Defense in Depth) to ensure that if one control fails, others are in place to mitigate the threat. The goal is not absolute protection, but reducing risk to an acceptable level while ensuring confidentiality, integrity, and availability.

---

## 1. Core Objectives (The 6 Goals)

1. Acceptable Risk: Align security spend with asset exposure and threat surface, not just revenue.
2. Confidentiality: Ensure only authorized entities see sensitive data (IAM, Least Privilege).
3. Integrity: Prevent silent or unauthorized changes to data/systems (Version Control, Audit).
4. Availability: Ensure services work when needed (Redundancy, DDoS mitigation).
5. Enforceable Controls: Use policies that can be programmatically verified and enforced (Security as Code).
6. Measurable Observability: Prove security works through testing, reporting, and logs.

---

## 2. Essential Security Components

### 2.1 Perimeter & Internal Firewalls

- Stateful Inspection: Essential for tracking active connections; stateless packet filtering is largely legacy for modern security.
- WAF (Web Application Firewall): A secondary layer for API protection. Heuristic: Fix input validation in code first; use a WAF as a shield, not a savior.
- Cloud Security Groups: Dynamically generated ACLs that act as distributed firewalls within AWS/Azure.

### 2.2 Application-Layer Enforcement

- Session Border Controllers (SBC): Critical for voice/SIP security. They act as policy enforcement nodes at the application layer, not just gateways.
- Identity-Aware Proxies: Shifting from "Network Trust" to "Identity Trust."

### 2.3 Detection & Prevention (IDPS)

- IDPS: Must be linked to automated routing or ACL management to be effective. "Passive dashboards are not defenses."
- Egress Monitoring: Critical for preventing data exfiltration via DNS, HTTPS, or messaging APIs.

---

## 3. Best Practices for Secure Design

### 3.1 Layered Defense (Defense in Depth)

- Combine Firewalls/VPNs, Internal Segmentation, Encryption, and Endpoint Security (EDR/MDM).
- Redundancy: Ensure no single security control is a single point of failure.

### 3.2 Strong IAM & Zero Trust

- Eliminate IP Trust: Use MFA (avoiding SMS/Email) and client TLS certificates to verify identity regardless of source IP.
- ZTNA (Zero Trust Network Access): Replace traditional VPNs with application-layer encryption and continuous validation.
- Foundational Model: See [[SoT - Zero Trust Architecture]] for the core principles of shifting from perimeter trust to identity-centric security.

### 3.3 Automate & Patch

- 32% of attacks target unpatched vulnerabilities. Automate patching and vulnerability scanning.
- Regression Testing: Ensure patches don't break system behavior (e.g., the 2024 CrowdStrike outage).

---

## 4. Modern Challenges

- Tool Sprawl: Consolidate policy and telemetry into unified engines (SASE/SSE).
- Security vs. Agility: Shift from manual tickets to Infrastructure as Code (IaC) and versioned security policies.
- Legacy Systems: Isolate legacy gear via aggressive segmentation and proxies with explicit retirement timelines.

---

## Related Knowledge

- Governance: [[SoT - NIST Cybersecurity Framework]]
- Segmentation: [[SoT - Network Segmentation]]
- Identity: [[SoT - Data-Centric IAM in Zero Trust]]
- Voice Security: [[SoT - Session Border Controllers (SBC)]]
- Networking: [[SoT - The Data-Centric Theory of Networking]]
