---
aliases: [BGP Hub and Spoke Architecture, Private IPAM Strategy, Scalable Network Connectivity]
created: 2026-02-11T08:15:00+00:00
last-synthesis: 2026-02-11
modified: 2026-07-13T08:52:53+00:00
permalink: llmeon/30-library/so-t/so-t-scalable-private-networking-ipam
source_of_truth: true
tags: [architecture, domain/infrastructure, ipam, networking, sot]
title: SoT - Scalable Private Networking & IPAM
type: sot
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## Minimum Viable Understanding (MVU)

Scalable private networking requires a shift from "addressing by coincidence" to Hierarchical Aggregation with Sparse Allocation. In environments where final topology is indeterminate (e.g., greenfield growth or M&A), connectivity is maintained through BGP-based dynamic routing (The Control Plane) and centralized transit hubs (The Data Plane). The goal is to enforce non-overlap by construction, allowing any-to-any connectivity without the "NAT tax" of cost and complexity.

## Working Knowledge

### 1. The Governing Standards (RFCs)

| RFC | Designation | Role in IPAM |
| --- | --- | --- |
| RFC 1918 | Private Address Space | Defines 10/8, 172.16/12, and 192.168/16. 10/8 is the only block sufficient for enterprise scale. |
| RFC 6598 | CGN Shared Space | `100.64.0.0/10`—useful as a "transit range" or buffer when RFC 1918 collisions occur. |
| RFC 4632 | CIDR | Enables hierarchical, variable-length allocation (The Lattice Mechanism). |
| RFC 4271 | BGP | The standard for advertising reachability between autonomous private networks. |
| RFC 4193 | IPv6 ULA | Unique Local Addresses; randomly generated /48s to prevent collisions by probability. |

### 2. Architectural Frameworks

#### A. The Hierarchical Tiered Model (Greenfield Standard)

Allocate from large blocks, assign in small ones, and leave enormous gaps.

- Top-Down Delegation: Org (`/8`) $\to$ Region (`/16`) $\to$ Environment (`/20`) $\to$ VPC/Cluster (`/24`).
- Structural Guarantee: If each branch is a strict subset of its parent and siblings don't overlap, non-collision is guaranteed by the tree structure.
- Summarizability: Any tier can be described by a single CIDR prefix, keeping routing tables and firewall rules compact.

#### B. "Carrier-Style" Transit (Indeterminate Scale)

Treat the central Hub as a Transit Provider rather than a server farm.

- Control Plane (eBGP): Each spoke acts as its own Autonomous System (AS). New spokes advertise CIDR blocks; the Hub learns and propagates routes automatically.
- Data Plane (Centralized Hub): Managed services like AWS Transit Gateway or Azure vWAN centralize policy and enable spoke-to-spoke flows without re-IPing.

#### C. Overlay & Intermediation (Brownfield/Conflict)

When overlap is unavoidable (e.g., acquisitions):

- Private Link (L4-7): Expose services via local IPs in the consumer network. Decouples connectivity from network topology.
- Twice NAT: Both source and destination IPs are translated through an intermediary CIDR block.
- VXLAN/GENEVE: Decouple "Underlay" (physical IP) from "Overlay" (tenant IP) using encapsulation.

## Current Understanding

### The "Configuration Management" Analogy

Network IPAM is the physical manifestation of the Lattice Problem found in configuration tools like CUE:

- CIDR Hierarchy: Maps to Type Hierarchy (`top` $\to$ `struct` $\to$ `concrete`).
- Non-overlap: Maps to Constraint Satisfaction (Unification).
- BGP Advertising: Maps to Service Discovery/Registries.
- Overlay Networking: Maps to Adapters/Anti-Corruption Layers.

Both domains are about making composition safe when the final system shape is unknown at design time.

### Cloud-Native Validation

- AWS: Well-Architected Framework (REL02-BP05) explicitly mandates non-overlapping ranges to avoid "Private NAT Gateway" remediation.
- Azure: Architecture Center specifies that a non-overlapping scheme is the "bedrock" of hub-and-spoke, positioning Azure Route Server (BGP) as the solution to static route maintenance.

## Integration Queue & Related

- rel:: broader [[SoT - Cloud Networking Principles]]
- rel:: supports [[Strategy - Hierarchical Subnetting]]
- rel:: practical-reference [[Cheatsheet - Azure AKS Networking]]
- rel:: mechanism-isomorphism [[Primes Become Rarer But Remain Searchable]]—prime distribution follows 1/ln(N) density law; IPAM sparse allocation could model optimal gap sizing on Prime Number Theorem. Both use multiplicative structure (prime factorisation / CIDR hierarchy) to guarantee uniqueness across infinite spaces.
- rel:: error-term-analogy [[HEAD What is the Riemann Hypothesis]]—Riemann zeros describe prime distribution fluctuations; IPAM surge buffers describe IP consumption variance. Both are uncertainty management in sparse systems.
- rel:: [[Connection - Prime Distribution ↔ IPAM Sparse Allocation]]—detailed cross-domain analysis
