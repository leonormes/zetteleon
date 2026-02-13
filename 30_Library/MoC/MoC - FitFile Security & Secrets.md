---
aliases:
  - FitFile Security Index
  - Secret Management Map
created: 2026-01-08T12:45:00Z
last_reviewed: 2026-02-13
modified: 2026-02-13T00:00:00+00:00
status: active
tags:
  - fitfile
  - moc
  - secrets
  - security
  - vault
title: MoC - FitFile Security & Secrets
type: map
---

## 1. Core Architecture

- Secret Management: [[SoT - FITFILE Secret Management Architecture]]
    - Defines the VSO implementation, "Canonical" vs. "Legacy" paths, and the "Golden Config" for rotation.
- General K8s Secrets: [[SoT - Kubernetes Secrets Management]]
    - Covers the underlying concepts (Etcd encryption, External Secrets pattern).
- Identity Management: [[SoT - FitFile Identity & Access Management (Auth0)]]
    - Covers OIDC federation, Management API security, and tenant isolation.

## 2. Operational Procedures

- Secret Operations: [[SoT - FitFile Secrets Operations (Vault & VSO)]]
    - Practical guide for managing `VaultStaticSecret` and `VaultDynamicSecret` resources.
- Rotation & Troubleshooting: [[SoT - FitFile Deployment - Troubleshooting and Known Issues]]
    - See Section 1.3 for the Rotation Policy.
    - See Section 2.1 for Stale Secret debugging.
- Audit Reports:
    - [[SoT - FITFILE Secret Management Architecture#1. Executive Summary|Audit - FITFILE Secret Management (Oct 2025)]] (Historical context for current architecture).

## 3. Hardening Standards

- Container Security: [[SoT - Container Security & Hardening]]
    - Best practices for image building (Distroless), runtime security (PSA), and supply chain.
- Infrastructure Strategy: [[SoT - DevOps & Infrastructure Architecture Strategy]]
    - Philosophy on "Shift-Left" security and immutable infrastructure.
- Zero Trust IAM: [[SoT - Data-Centric IAM in Zero Trust]]
    - Architectural framework for PDP/PEP and the Equation of Trust.

## 4. Related Maps

- [[MOC - Cloud-Native Authentication]]
- [[SoT - External Ingress & SSL Architecture]]
- [[MOC - Kubernetes Architecture]]