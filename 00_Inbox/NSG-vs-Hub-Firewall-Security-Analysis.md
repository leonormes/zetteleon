---
created: 2026-03-11T13:18:35+00:00
modified: 2026-03-14T11:10:52+00:00
title: NSG-vs-Hub-Firewall-Security-Analysis
---

SECURITY ARCHITECTURE ANALYSIS

Network Boundary Security for Special Category Data Processing

NSG-Only vs. Hub Firewall Architecture

Azure Hub-and-Spoke—AKS Spoke Environment

| Classification: | OFFICIAL–SENSITIVE |
| ----: |:---- |
| Audience: | CISO / SIRO / Architecture Board |
| Date: | March 2026 |
| Author: | Principal Cloud Security Architect |
| Status: | FOR DECISION |

## Executive Summary

This document provides a formal analysis of an architectural deviation introduced during a Proof of Concept (PoC) for a system processing Special Category Data (medical and social care records) on behalf of a UK local government authority. The deviation consists of bypassing the approved Azure Hub Firewall (Layer 7 / WAF) and instead exposing an AKS cluster's load balancer directly to the public internet, secured solely by a Network Security Group (NSG) restricted to a single trusted source IP address.

This analysis concludes that the NSG-only approach is fundamentally inadequate for production use. It violates NCSC Cyber Essentials boundary firewall requirements, contravenes NCSC Cloud Security Principles (notably Principle 11: External Interface Protection), is incompatible with NCSC Zero Trust Architecture guidance, and exposes the local authority to material regulatory risk under UK GDPR Article 32 and PSN compliance obligations.

| Recommendation: The hub firewall must be reinstated on the inbound traffic path before any production workloads are deployed. The NSG-only configuration should be explicitly documented as a time-limited PoC exception and decommissioned. |
|:---- |

## 1\. NCSC Cyber Essentials and Boundary Firewalls

### 1.1 The Cyber Essentials Requirement

Cyber Essentials is the _minimum_ standard of cyber security recommended by the UK Government for organisations of all sizes. It is a mandatory requirement for organisations handling certain categories of government data and is referenced in the PSN Code of Connection (CoCo) compliance framework. The scheme's first technical control is Firewalls and Internet Gateways, which requires that every device and service connected to the internet be protected by a correctly configured firewall.

The NCSC Requirements for IT Infrastructure document (v3.3, current) mandates that boundary firewalls must be configured to block all inbound traffic by default ("deny by default"), permitting only explicitly approved services. Critically, it requires that firewall rules be documented and approved, and that the firewall be capable of inspecting and filtering traffic based on its source, destination, and communication protocol.

### 1.2 Why an NSG Does Not Satisfy This Requirement

An Azure Network Security Group operates exclusively at OSI Layers 3 and 4\. It evaluates traffic based on source/destination IP addresses, port numbers, and protocol (TCP/UDP). It cannot inspect the contents of network packets, cannot terminate or inspect TLS-encrypted sessions, and cannot identify malicious payloads, application-layer exploits, or data exfiltration attempts concealed within permitted traffic flows.

The following table illustrates the capability gap between an NSG and a Layer 7 firewall:

| Capability | Azure NSG (Layer 4\) | Azure Firewall / WAF (Layer 7\) |
|:---- |:---- |:---- |
| OSI Layer | 3-4 (IP/Port) | 3-7 (Full Application Stack) |
| Deep Packet Inspection | No | Yes |
| TLS Termination & Inspection | No | Yes |
| OWASP Top 10 Protection | No | Yes |
| SQL Injection / XSS Filtering | No | Yes |
| IDPS (Intrusion Detection) | No | Yes (Premium SKU) |
| Threat Intelligence Feeds | No | Yes |
| Centralised Logging & SIEM | Flow logs only (no payload) | Full application-layer logging |
| FQDN / URL Filtering | No | Yes |
| Stateful Across Spokes | Per-subnet only | Centralised hub-wide policy |

The NCSC's requirement for boundary firewalls is not merely a requirement for _any_ filtering mechanism. It is a requirement for an active, stateful boundary defence capable of identifying and blocking threats before they reach internal services. An NSG is a network access control list, not a firewall in the NCSC's doctrinal sense.

### 1.3 The "Trusted Source" Fallacy

The argument that restricting inbound traffic to a single trusted external IP address renders Layer 7 inspection unnecessary contains a critical logical flaw. It conflates network identity (an IP address) with trustworthiness of content. An IP address confirms where traffic originates; it says nothing about what the traffic contains.

Consider the following threat scenarios that an NSG alone cannot mitigate, even with a single permitted source IP:

- Compromised source host: If the trusted external system is compromised (via malware, supply chain attack, or credential theft), every packet it sends will pass the NSG unimpeded. The attacker inherits the trust conferred by the IP allow-list.
- Application-layer attacks: SQL injection, cross-site scripting, command injection, and SSRF attacks arrive as syntactically valid HTTP/HTTPS requests from the permitted IP. An NSG has no capability to detect or block these.
- Data exfiltration: If AKS is compromised through any vector (container escape, vulnerable dependency, misconfigured RBAC), an NSG cannot detect sensitive data leaving the cluster within permitted outbound flows.
- Encrypted payload blindness: Without TLS termination, the NSG cannot inspect the contents of HTTPS traffic at all. Malicious payloads are invisible to it.

Trusting an IP address as a proxy for security is a perimeter-era assumption that the NCSC has explicitly moved away from. As we address in Section 3, the NCSC's Zero Trust guidance treats all networks—including nominally trusted ones—as potentially hostile.

## 2\. Defence in Depth (NCSC Cloud Security Principles)

### 2.1 Principle 11: External Interface Protection

NCSC Cloud Security Principle 11 states: _"All external or less-trusted interfaces of the service should be identified and appropriately defended."_ The NCSC elaborates that internet-facing and public interfaces are inherently more susceptible to attack and require robust security measures including protection against authentication attacks, DDoS, and application-level exploits such as SQL injection.

By attaching a public IP directly to the AKS load balancer and defending it with only an NSG, the architecture fails to appropriately defend an external interface. The NSG provides no protection against the application-level attacks explicitly named in Principle 11\. It is equivalent to installing a lock on a front door whilst leaving every window open.

### 2.2 The Hub Firewall as a Defence-in-Depth Layer

The original hub-and-spoke design with a centralised Azure Firewall implements a layered security model consistent with NCSC guidance. Traffic from the public internet first traverses the hub firewall (providing Layer 7 inspection, IDPS, threat intelligence filtering, and centralised logging), then is forwarded via VNet peering to the spoke, where the NSG provides an additional layer of network-level access control at the subnet boundary.

This gives the architecture two independent security boundaries:

- Layer 7 (Hub Firewall): Inspects payloads, terminates TLS, applies WAF rulesets, blocks known threat indicators, and feeds telemetry to the SIEM.
- Layer 4 (Spoke NSG): Enforces network segmentation, restricts permitted source IPs and ports, and provides a secondary boundary in case the firewall is misconfigured or bypassed.

Removing the hub firewall collapses two independent security layers into one. The architecture now depends entirely on the NSG—a control that, as demonstrated in Section 1, has no application-layer visibility. This is the _antithesis_ of defence in depth.

### 2.3 Single Point of Failure in Security Controls

With the hub firewall bypassed, the NSG becomes the single point of failure for all inbound security enforcement. If the NSG rule is misconfigured (a broader CIDR is accidentally permitted, a rule priority conflict arises, or the NSG is temporarily disassociated during an infrastructure change), there is no secondary control to prevent direct public access to the AKS cluster.

In a system processing Special Category Data under UK GDPR, the consequence of such a failure is not a minor operational incident. It is a potential reportable data breach involving the medical and social care records of citizens, with all the regulatory, reputational, and legal consequences that entails.

## 3\. The Zero Trust Architecture Imperative

### 3.1 NCSC Zero Trust Principles

The NCSC defines Zero Trust as _"an architectural approach where inherent trust in the network is removed, the network is assumed hostile, and each request is verified based on an access policy."_ The NCSC's eight Zero Trust Architecture Design Principles establish that:

- The network is hostile: Communications should use secure transport protocols regardless of network location. No network segment—including VNet-peered spokes—should be inherently trusted.
- Every request must be verified: Authentication and authorisation decisions should consider multiple signals (device health, user identity, behavioural context), not simply network location or source IP address.
- Don't trust any network: The NCSC explicitly states that you should not trust any network between the device and the service, including the local network. This principle directly invalidates the argument that a "trusted IP" is a sufficient security control.

### 3.2 IP Trust vs. Zero Trust: A Fundamental Incompatibility

The NSG-only approach is architecturally predicated on a model of network trust that the NCSC has formally deprecated. It assumes that because traffic arrives from a known IP address, it is safe. This assumption violates every tenet of Zero Trust:

- An IP address is not an identity. It can be spoofed, reassigned, or associated with a compromised host.
- An IP address carries no information about the intent, content, or legitimacy of the traffic it labels.
- Granting access based solely on source IP is the definition of "inherent network trust"—the very thing Zero Trust architecture is designed to eliminate.

A Layer 7 firewall, by contrast, aligns with Zero Trust by inspecting the _content_ of every request, validating it against application-layer policies, and making a trust decision based on the payload itself—not merely its origin.

### 3.3 Relevance to Special Category Data

For a system processing Special Category Data (Article 9 UK GDPR), the bar for demonstrating appropriate technical measures is significantly higher than for ordinary personal data. The NCSC's Zero Trust guidance is particularly pertinent here: if the NCSC advises treating all networks as hostile even for routine enterprise traffic, then a system handling the most sensitive categories of personal data has an even stronger obligation to implement payload inspection and multi-signal verification at every boundary.

## 4\. Compliance Risk for Local Authorities

### 4.1 UK GDPR Article 32: Security of Processing

Article 32 of the UK GDPR requires data controllers and processors to implement _"appropriate technical and organisational measures"_ to ensure a level of security appropriate to the risk, taking into account the state of the art, the costs of implementation, and the nature, scope, context, and purposes of processing, as well as the risk of varying likelihood and severity for the rights and freedoms of natural persons.

For a system processing Special Category Data (medical and social care records), the "risk of varying likelihood and severity" is manifestly at the upper end of the spectrum. Stripping away application-layer inspection from the network boundary of such a system, when the technology is readily available and already deployed in the hub, is difficult to characterise as implementing measures "appropriate to the risk". The ICO would likely view this as a failure to implement state-of-the-art protections that were both available and previously in place.

### 4.2 PSN Code of Connection

Local authorities connecting to the Public Services Network are required to demonstrate that their infrastructure meets a baseline standard of information assurance, verified through the PSN compliance process. The PSN uses a "walled garden" approach predicated on every connected organisation maintaining sufficient security to avoid presenting an unacceptable risk to the wider network. The CoCo requires organisations to evidence effective boundary security controls.

An architecture that exposes an internet-facing load balancer with only Layer 4 filtering, processing data that may transit to or from PSN-connected services, would be a significant finding in any compliance review. Even as the public sector transitions towards the Future Network for Government (FN4G) and internet-first connectivity models, the underlying security assurance requirements remain, and in many cases reference Cyber Essentials and NCSC Cloud Security Principles as their baseline.

### 4.3 Accountability: The SIRO's Position

The Senior Information Risk Owner (SIRO) of the local authority is personally accountable for ensuring that information risks are managed appropriately. If a data breach were to occur through an application-layer exploit that a hub firewall would have blocked, the SIRO would need to explain to the ICO, the affected data subjects, and potentially the courts why an existing Layer 7 inspection capability was deliberately removed from the architecture. The fact that this was done to accommodate a PoC convenience, rather than in response to a documented risk assessment, substantially weakens the authority's defensibility position.

## 5\. Conclusion and Recommendations

This analysis has demonstrated that relying solely on a Layer 4 NSG for public boundary security of a system processing Special Category Data is not a matter of professional preference or architectural style. It is a departure from established NCSC doctrine, a violation of the defence-in-depth principle, and a material compliance risk for the local authority.

The following actions are recommended:

1. Immediate: Reinstate the Azure Hub Firewall (Layer 7 / WAF) on the inbound traffic path to the AKS spoke. All public inbound traffic must traverse this inspection point before reaching the AKS load balancer.
2. Short-term: Document the PoC deviation as a formal exception with a defined expiry date. Record the risk acceptance decision (if any was made) and the identity of the risk owner who approved it.
3. Ongoing: Ensure that any future architectural changes affecting the network security boundary undergo a formal Architecture Decision Record (ADR) process, with explicit sign-off from the SIRO and alignment to NCSC Cloud Security Principles.
4. Assurance: Commission a penetration test of the AKS environment with the hub firewall in place, to validate the effectiveness of the layered security model and provide evidence for the next PSN compliance review.

| In summary: An NSG is a necessary but insufficient security control. It is a component within a defence-in-depth architecture, not a replacement for it. For Special Category Data processing, Layer 7 inspection at the network boundary is not optional—it is a baseline expectation of NCSC guidance, UK GDPR, and public sector compliance frameworks. |
|:---- |

## References

- NCSC, Cloud Security Principles (2025)—ncsc.gov.uk/collection/cloud/the-cloud-security-principles
- NCSC, Zero Trust Architecture Design Principles—ncsc.gov.uk/collection/zero-trust/architecture-design-principles
- NCSC, Cyber Essentials: Requirements for IT Infrastructure v3.3—ncsc.gov.uk/files/cyber-essentials-requirements-for-it-infrastructure-v3-3.pdf
- NCSC, Network Architectures Guidance—ncsc.gov.uk/collection/device-security-guidance/infrastructure/network-architectures
- UK GDPR, Article 32—Security of Processing
- UK GDPR, Article 9—Processing of Special Categories of Personal Data
- Cabinet Office, PSN Compliance Guidance—gov.uk/guidance/public-services-network-psn-compliance
- Cabinet Office, PSN Code of Connection Application—gov.uk/guidance/apply-for-a-public-services-network-psn-connection-compliance-certificate
