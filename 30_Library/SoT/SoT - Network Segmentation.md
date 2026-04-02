---
created: 2026-04-01T21:47:06+00:00
last-synthesis: 2026-04-01
modified: 2026-04-01T21:47:06+00:00
source_of_truth: true
status: evergreen
synthesis-count: 1
tags: [domain/networking, security/segmentation, theory/zero-trust, type/SoT]
title: SoT - Network Segmentation
trust-level: stable
---

## Minimum Viable Understanding (MVU)

Network segmentation is the practice of dividing a network into smaller, isolated zones to control traffic flow, limit access, and contain security breaches. It shifts security from an implicit trust model (flat network) to a resource-centric model where every boundary requires continuous verification. According to NIST SP 800-207, segmentation is a foundational component of Zero Trust Architecture, providing "damage limitation in space" by preventing lateral movement.

## Working Knowledge

### 1. Types of Segmentation

| Type | Mechanism | Trade-offs |
| :--- | :--- | :--- |
| **Physical** | Dedicated hardware (switches, firewalls, cabling). | Strongest isolation; high cost and rigidity. |
| **Logical** | Virtual isolation (VLANs, subnets, IEEE 802.1Q). | Flexible and cost-effective; risk of "VLAN hopping." |
| **Firewall-based** | Internal filtering at zone boundaries. | Fine-grained control; high rule management overhead. |
| **Software-Defined (SDN)** | Programmatic policy management (SDN controllers). | Dynamic and scalable; essential for cloud environments. |
| **Microsegmentation** | Policy at the individual workload/app level. | Most granular; requires advanced automation/visibility. |

### 2. Zero Trust Alignment (NIST SP 800-207)

- **Continuous Verification:** No location confers implicit trust; every session must be authenticated and authorized.
- **Micro-perimeters:** Enforcement points move as close to the resource as possible (e.g., sidecars, host firewalls).
- **Policy Engine:** Authorization decisions are made by Policy Decision Points (PDPs) based on device health, user identity, and threat intelligence.

### 3. Implementation Phases

1. **Assessment & Baseline:** Map current data flows and classify all workloads.
2. **Policy Definition:** Define least-privilege rules; implement initially in "monitoring mode."
3. **Enforcement:** Progressively activate policies, starting with high-value assets.
4. **Optimization:** Continuous testing via simulated attacks and rule refinement.

## Current Understanding

### The "Lateral Movement" Prevention Model

Modern segmentation rejects the "castle-and-moat" perimeter. Instead, it assumes breach (Zero Trust) and focuses on the internal blast radius. 

- **Case Study (Colonial Pipeline):** The lack of segmentation between IT and OT networks allowed ransomware to spread laterally, causing catastrophic operational failure.
- **Strategic Value:** Segmentation is not just a technical control; it is a financial imperative. IBM research indicates that organizations with mature containment capabilities (like segmentation) reduce breach costs by millions by dropping the average breach lifecycle.

## Related Knowledge

- **Broad Principles:** [[SoT - Cloud Networking Principles]] (`rel:: broader`)
- **Privacy Patterns:** [[SoT - Zero Knowledge Architecture]] (`rel:: supports`)
- **Cloud Specifics:** [[SoT - AWS EKS Networking Architecture]] (`rel:: example-of`)
- **Complexity Theory:** [[SoT - Infrastructure Complexity]] (`rel:: supports`)
