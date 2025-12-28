---
aliases: ["K8s MOC", "Kubernetes Map"]
confidence: "5/5"
created: 2025-12-16T13:52:13Z
epistemic: "reference"
last_reviewed: "2025-12-23"
modified: 2025-12-28T18:49:32+00:00
purpose: "The central entry point for navigating Kubernetes architecture, from low-level container primitives to high-level platform deployment."
review_interval: "6 months"
see_also: ["[[MOC - Networking & DNS]]", "[[MOC - ProdOS]]"]
source_of_truth: []
status: "stable"
tags: ["devops", "index", "infrastructure", "kubernetes"]
title: MOC - Kubernetes Architecture
type: "map"
uid: 
updated: 
---

## Kubernetes Architecture - Map of Content

> [!hint] Overview
> This map routes you through the technical layers of Kubernetes, starting with the Linux kernel primitives that enable isolation and moving up to platform-specific implementation.

---

### 1. Container Primitives (The Bedrock)

The low-level Linux mechanisms that make containers possible.

- **[[SoT - Namespacing in Computing]]**—*The architectural pattern of identifier isolation.*
- **[[SoT - Container Isolation (The Namespace Security Model)]]**—*The coordinated use of all six namespaces and the 'Mount Namespace' mandate.*
- **[[SoT - Namespace-Aware Pseudo-Filesystems]]**—*How procfs and sysfs provide virtualized views of kernel state.*

---

### 2. Cluster Architecture (The Mental Model)

- **[[SoT - Kubernetes Cluster State Architecture]]**—*The foundational model: K8s as a state-store/database. Selectors and API logic.*
- **[[SoT - Kubernetes Networking & DNS]]**—*The flat network model, Ingress-to-Pod traffic flow, and Service discovery.*
- **[[SoT - Kubernetes Secrets Management]]**—*Encryption at rest and Secret consumption models.*

---

### 3. Platform Implementation (FITFILE Context)

- **[[SoT - FITFILE Platform Deployment]]**—*Standardized deployment of the FITFILE stack.*
- **[[SoT - FITFILE Secret Management Architecture]]**—*Implementing Vault Secrets Operator (VSO).*
- **[[SOT - CI-CD Pipelines]]**—*The automated delivery mechanisms.*

---

### 4. Configuration & Security

- **[[SoT - Software Configuration Management Patterns]]**—*IaC and GitOps best practices.*
- **[[SoT - Data-Centric Infrastructure (Terraform)]]**—*Managing state as code.*
- **[[Network Policies]]**—*Hardening namespace boundaries.*
