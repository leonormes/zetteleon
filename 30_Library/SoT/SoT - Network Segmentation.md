---
created: 2026-04-01T21:47:06+00:00
last-synthesis: 2026-04-02
modified: 2026-07-13T08:52:51+00:00
permalink: llmeon/30-library/so-t/so-t-network-segmentation
source_of_truth: true
tags: [domain/networking, security/segmentation, theory/zero-trust, type/SoT]
title: SoT - Network Segmentation
---

## Minimum Viable Understanding (MVU)

Network segmentation is the practice of dividing a network into smaller, isolated zones to control traffic flow, limit access, and contain security breaches. It shifts security from an implicit trust model (flat network) to a resource-centric model where every boundary requires continuous verification. According to NIST SP 800-207, segmentation is a foundational component of Zero Trust Architecture, providing "damage limitation in space" by preventing lateral movement.

## Working Knowledge

### 1. Types of Segmentation

| Type | Mechanism | Trade-offs |
|:--- |:--- |:--- |
| Physical | Dedicated hardware (switches, firewalls, cabling). | Strongest isolation; high cost and rigidity. |
| Logical | Virtual isolation (VLANs, subnets, IEEE 802.1Q). | Flexible and cost-effective; risk of "VLAN hopping." |
| Firewall-based | Internal filtering at zone boundaries. | Fine-grained control; high rule management overhead. |
| Software-Defined (SDN) | Programmatic policy management (SDN controllers). | Dynamic and scalable; essential for cloud environments. |
| Microsegmentation | Policy at the individual workload/app level. | Most granular; requires advanced automation/visibility. |

### 2. Comparisons & Building Blocks

- Segmentation vs. VLANs: VLANs are a Layer 2 logical grouping tool. They are a _building block_ of segmentation but lack the granular access control and Layer 3+ inspection required for a complete segmentation strategy.
- Segmentation vs. Firewalling: Segmentation defines the _structural isolation_ (the zones), while firewalls act as the _gatekeepers_ enforcing rules and inspecting traffic flowing between those zones.

### 3. Multi-Dimensional Benefits

Beyond breach containment, segmentation provides:

- Performance Optimization: Reduces network congestion by localizing traffic and improving resource allocation.
- Simplified Compliance: Isolates regulated assets (PCI DSS, HIPAA, GDPR), reducing the scope of audits and reporting.
- Management Visibility: Provides clearer insight into traffic flows and user behavior, enabling more efficient troubleshooting.
- Insider Threat Mitigation: Restricts access to sensitive systems based on the principle of Least Privilege.

## Current Understanding

### The "Lateral Movement" Prevention Model

Modern segmentation rejects the "castle-and-moat" perimeter. Instead, it assumes breach (Zero Trust) and focuses on the internal blast radius.

- Incident Response Role: Segmentation accelerates containment and investigation. It allows security teams to isolate compromised segments without disrupting the entire network, potentially containing breaches in as little as 24 hours.
- Case Study (Colonial Pipeline): The lack of segmentation between IT and OT networks allowed ransomware to spread laterally, causing catastrophic operational failure.
- Strategic Value: Segmentation is not just a technical control; it is a financial imperative. IBM research indicates that organizations with mature containment capabilities reduce breach costs by millions.

## Related Knowledge

- Broad Principles: [[SoT - Cloud Networking Principles]] (`rel:: broader`)
- Privacy Patterns: [[SoT - Zero Knowledge Architecture]] (`rel:: supports`)
- Cloud Specifics: [[SoT - AWS EKS Networking Architecture]] (`rel:: example-of`)
- Complexity Theory: [[SoT - Infrastructure Complexity]] (`rel:: supports`)
