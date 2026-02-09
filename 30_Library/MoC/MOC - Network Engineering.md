---
aliases: ["NetEng", "Network Engineering Map", "Networking MOC"]
created: 2026-02-04T00:00:00+00:00
modified: 2026-02-06T20:02:08+00:00
tags: ["engineering", "infrastructure", "moc", "networking"]
title: MOC - Network Engineering
type: map
---

## The Nervous System of Distributed Computing

Network Engineering is not just about connecting cables; it is the discipline of managing Latency, Throughput, and Reliability across distributed systems.

### 1. Core Sources of Truth (SoT)

- [[SoT - The Data-Centric Theory of Networking]]—_The fundamental philosophy: Data gravity vs. Speed of Light._
- [[SoT - Cloud Networking Principles]]—_Latency, Bandwidth, and the CAP theorem applied to pipes._
- [[SoT - Kubernetes Networking & DNS]]—_The specific implementation of networking in K8s (CNI, CoreDNS, Ingress)._
- [[SoT - The Universal Speed of Causality]]—_The hard physics limit of latency ($c$)._

### 2. Operational Protocols (The "How-To")

- Diagnostics: [[Protocol - HIE--NNUH Network Debugging]]—_A step-by-step checklist for isolating connectivity faults._
- Hybrid Cloud: [[SoT - Network Debugging - Cross-Cloud & Hybrid]]—_ExpressRoute, DirectConnect, and VNET peering failure modes._
- Tooling: [[SoT - Network Debugging Tools & Patterns]]—_The armory: tcpdump, netshoot, mtr, and nc._

### 3. Architecture & Hardware

- [[MOC - Cloud Hardware Architecture]]—_Physical constraints: NICs, NUMA, and SR-IOV._
- [[SoT - Azure Hybrid Networking (ExpressRoute)]]—_Connecting On-Prem to Cloud._

### 4. Key Concepts

- Latency: The time cost of distance. See [[SoT - Mechanical Sympathy]].
- DNS: The phonebook. See [[The Domain Name System]].
- Sockets: The interface. See [[MOC - How Sockets Actually Work]].
