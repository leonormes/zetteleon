---
aliases: [K8s Secrets MOC, Kubernetes Secrets Map]
confidence: "null"
created: 2025-12-15T12:00:00Z
epistemic: "null"
last_reviewed: "null"
modified: 2026-01-08T10:49:46+00:00
purpose: ""
review_interval: "null"
see_also: []
source_of_truth: []
status: active
tags: ["SoftwareEngineering/Security", kubernetes, secrets, vault]
title: MOC - Kubernetes Secrets Management
type: map
uid:
updated:
---

## MOC - Kubernetes Secrets Management

### 1. Core Concepts (Native Primitives)

Understanding the baseline mechanisms provided by Kubernetes.

- [[kubernetes_secrets]] - **Primary Reference.** Covers the distinction between ConfigMaps and Secrets, base64 encoding vs. encryption, and best practices like in-memory mounting (`tmpfs`).
  - _Key Insight:_ Native secrets are base64 encoded, not encrypted by default. True security requires "Encryption at Rest" and external KMS integration.

### 2. Advanced Management (HashiCorp Vault)

The preferred "Production" pattern using external secret managers.

- [[Vault to Kubernetes Secrets Management Guide]] - **The Architecture Guide.** Detailed walkthrough of the Vault + Vault Secrets Operator (VSO) pattern.
  - _Components:_ Vault AppRole, Vault Policy, VSO Controller.
  - _Flow:_ Auth -> Token -> Fetch -> Sync to K8s Secret.
- Secrets Management Report - hie-prod-34 - **Implementation Case Study.** A live report of this architecture in the `hie-prod-34` deployment.
  - _Pattern:_ `VaultStaticSecret` CRDs -> VSO -> Native K8s Secrets.
  - _Diagram:_ Includes a Mermaid object diagram of the dependency flow.

### 3. Related Security Context

Broader security topics touching on secrets.

- [[Is Whitelisting Cloudflare IPs Enough for Maximum Kubernetes Security]] - Contextualizes secrets within a "Defence-in-Depth" strategy (Node Hardening, Audit Logging).
- [[Secure Cross-Cloud Communication Between AWS EKS and Azure AKS for Task Distribution]] - Mentions secure secrets management for cross-cloud connectivity.

### 4. Key Workflows & Snippets

- **Debug VSO:** `kubectl get vaultstaticsecret <name> -o yaml` (from Secrets Management Report - hie-prod-34)
- **Vault Auth:** Using AppRoles for machine-to-machine authentication (from [[Vault to Kubernetes Secrets Management Guide]]).
- **Terraform:** How to define secrets in `locals.tf` to auto-provision Vault (from [[Vault to Kubernetes Secrets Management Guide]]).
