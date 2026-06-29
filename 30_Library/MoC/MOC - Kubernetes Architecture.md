---
aliases:
- K8s MOC
- Kubernetes Map
created: 2025-12-16 13:52:13+00:00
last_reviewed: '2025-12-23'
modified: 2026-02-01 15:08:05+00:00
status: stable
tags:
- devops
- index
- infrastructure
- kubernetes
title: MOC - Kubernetes Architecture
type: map
updated: null
permalink: llmeon/30-library/mo-c/moc-kubernetes-architecture
---

## Kubernetes Architecture - Map of Content

> [!hint] Overview
> This map routes you through the technical layers of Kubernetes, starting with the Linux kernel primitives that enable isolation and moving up to platform-specific implementation.

---

### 1. Container Primitives (The Bedrock)

The low-level Linux mechanisms that make containers possible.

- [[SoT - Namespacing in Computing]]—_The architectural pattern of identifier isolation._
- [[SoT - Linux Container Internals]]—_The coordinated use of all six namespaces and the 'Mount Namespace' mandate._
- [[SoT - Namespace-Aware Pseudo-Filesystems]]—_How procfs and sysfs provide virtualized views of kernel state._

---

### 2. Cluster Architecture (The Mental Model)

- [[SoT - Kubernetes Cluster State Architecture]]—_The foundational model: K8s as a state-store/database. Selectors and API logic._
- [[SoT - Kubernetes Networking & DNS]]—_The flat network model, Ingress-to-Pod traffic flow, and Service discovery._
- [[SoT - AWS EKS Networking Architecture]]—_AWS-specific implementation (VPC CNI, ENIs, and Capacity Planning)._
- [[SoT - Kubernetes Secrets Management]]—_Encryption at rest and Secret consumption models._

---

### 3. Platform Implementation (FITFILE Context)

- [[SoT - FITFILE Platform Deployment]]—_Standardized deployment of the FITFILE stack._
- [[SoT - FITFILE Secret Management Architecture]]—_Implementing Vault Secrets Operator (VSO)._
- [[SOT - CI-CD Pipelines]]—_The automated delivery mechanisms._

---

### 4. Configuration & Security

- [[SoT - Software Configuration Management Patterns]]—_IaC and GitOps best practices._
- [[SoT - Data-Centric Infrastructure (Terraform)]]—_Managing state as code._
- [[Network Policies]]—_Hardening namespace boundaries._