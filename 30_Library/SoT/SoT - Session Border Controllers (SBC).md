---
aliases: ["Oracle SBC", "Perimeta", "SBC", "SIP Security", "Voice Policy Enforcement"]
created: 2026-04-02T12:10:00Z
last_synthesis: 2026-04-02
modified: 2026-04-08T18:01:04+00:00
source_of_truth: true
status: evergreen
synthesis-count: 1
tags: ["networking", "security", "sip", "voice", "voip"]
title: SoT - Session Border Controllers (SBC)
trust-level: stable
type: "SoT"
---

## Minimum Viable Understanding (MVU)

A Session Border Controller (SBC) is a network device used to exert control over the signaling and media streams involved in setting up, conducting, and tearing down telephone calls or other interactive media communications. In modern architectures, they act as Application-Layer Policy Enforcement Nodes, not just simple voice gateways.

---

## 1. Core Functions

1. Security: Protects the internal voice network from SIP-based attacks, toll fraud, and unauthorized access.
2. Interoperability: Normalizes different SIP flavors and protocols to ensure different networks (e.g., carrier to enterprise) can communicate.
3. QoS (Quality of Service): Manages bandwidth and prioritizes voice/video traffic (RTP).
4. NAT Traversal: Handles the complex translation of internal IP addresses for SIP/RTP traffic across a firewall.

---

## 2. The SBC as a Security Control

Traditional firewalls are often insufficient for voice because they do not understand SIP state or the relationship between signaling (SIP) and media (RTP).

### 2.1 Application-Layer Awareness

An SBC understands that 100 SIP INVITEs are millions of times more expensive than 100 RTP frames. It can implement:

- Rate-Limiting: Throttling INVITE attempts from a specific source to prevent DoS.
- Protocol Validation: Ensuring incoming SIP messages adhere strictly to RFC standards.
- Fraud Detection: Identifying unusual calling patterns that indicate compromised accounts or toll fraud.

### 2.2 SIP Security Best Practices

- Never rely on default policies: Many SBCs ship with open access to SIP. Hardening is mandatory.
- MFA for SIP: Use client TLS certificate validation to eliminate reliance on source IP addresses for trunk authentication.
- Decryption: If the SBC isn't decrypting TLS traffic, it cannot inspect the payload. "You're already flying blind."

---

## 3. Deployment Scenarios

- Peering: Connecting one service provider's network to another's.
- Access: Connecting end-user devices or SIP-PBXs to a service provider's core.
- DDoS Sidestepping: Using IP address mobility and SBC policy to mitigate volumetric attacks targeting voice infrastructure.

---

## Related Knowledge

- Security Architecture: [[SoT - Network Security Architecture]]
- Networking: [[SoT - The Architecture of Packet Encapsulation (TCP-IP)]]
- Identity: [[SoT - Data-Centric IAM in Zero Trust]]
