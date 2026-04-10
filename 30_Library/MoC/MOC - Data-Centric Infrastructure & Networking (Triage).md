---
aliases: [Infrastructure Triage, Networking Triage]
created: 2026-04-08T00:00:00+00:00
modified: 2026-04-10T16:52:04+00:00
status: seedling
tags: [cloud, devops, infrastructure, moc, networking, triage]
title: MOC - Data-Centric Infrastructure & Networking (Triage)
type: map
---

## Navigation Hub: Data-Centric Infrastructure & Networking

This hub triages the "Domain III" (Data-Centric Systems) cluster, focusing on Infrastructure-as-Code (Terraform/CUE), Network Security Architecture, and Cloud-Native Networking. It aims to resolve the high-value seedlings identified in the global scan.

### 1. High-Priority Processing (The Logic)

- [[SoT - The Data-Centric Philosophy]] - The axiom of data-first design.
- [[SoT - The Data-Centric Theory of Networking]] - Routing as prefix-trie traversal.
- [[SoT - Data-Centric IAM in Zero Trust]] - AuthZ as a data-processing operation.
- [[SoT - Infrastructure Complexity]] - Managing entropy in distributed systems.
- [[SoT - Generative Infrastructure Configuration Framework]] - The GIC framework (Makefiles/CUE/HCL).
- [[SoT - Type-Driven Infrastructure Strategy]] - Proof-carrying logic for cloud resources.

### 2. Networking & Traffic Control

- [[SoT - AWS EKS Networking Architecture]]
- [[SoT - Azure Hybrid Networking (ExpressRoute)]]
- [[SoT - DNS Core Components and Environments]]
- [[SoT - External Ingress & SSL Architecture]]
- [[SoT - Network Security Architecture]]
- [[SoT - Network Segmentation]]
- [[SoT - Scalable Private Networking & IPAM]]

### 3. Infrastructure & Automation

- [[SoT - AKS IP Allocation & Subnet Sizing]]
- [[SoT - ArgoCD Networking Patterns]]
- [[SoT - Automated Cloud Resource Hibernation]]
- [[SoT - CUE Configuration]]
- [[SoT - FitFile Deployment - Strategy & Architecture]]
- [[SoT - GitLab CLI Authentication]]
- [[SoT - HashiCorp Vault Architecture]]
- [[SoT - State Synchronization Models]]

### 4. Unprocessed Seedlings (Triage Candidates)

- [[Data-Centric Networking Focuses on Packet Journey Through Devices]]
- [[Host-Based Routing Enables Virtual Hosting in Cloud Infrastructure]]
- [[Internet Gateway in AWS Networking]]
- [[Ephemeral Agents and Environments in Terraform Cloud]]
- [[Configuration Kernel]]
- [[Configuration Generator]]
- [[Intent-Implementation Separation]]
- [[Configuration as Generated Output]]
- [[Configuration Error Surface Area]]
- [[Naming Protocol]]

### 5. Recommended Actions

- [x] Harvest: Integrate the "Naming Protocol" and "Intent-Implementation Separation" notes into the [[SoT - Generative Infrastructure Configuration Framework]].
- [x] Consolidate: Review the "Configuration" seedlings and merge them into a single [[SoT - Software Configuration Management Patterns]]. (Integrated into GIC Framework SoT instead).
- [x] Synthesise: Map the "ArgoCD Networking Patterns" onto the [[SoT - The Data-Centric Theory of Networking]].
