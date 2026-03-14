---
aliases: [FitFile Security Index, Secret Management Map]
created: 2026-01-08T12:45:00Z
last_reviewed: 2026-02-13
modified: 2026-02-16T09:40:27+00:00
status: active
tags: [fitfile, moc, secrets, security, vault]
title: MoC - FitFile Security & Secrets
type: map
---

## 1. Core Architecture

- Secret Management: [[SoT - FitFile VSO Secrets Management]] — Single source of truth for VSO, Vault, and all secret types.
    - Full index: [[MoC - FitFile Secrets Management]]
- General K8s Secrets: [[SoT - Kubernetes Secrets Management]]
    - Covers the underlying concepts (Etcd encryption, External Secrets pattern).
- Identity Management: [[SoT - FitFile Identity & Access Management (Auth0)]]
    - Covers OIDC federation, Management API security, and tenant isolation.

## 2. Operational Procedures

- Secret Operations: [[SoT - FitFile VSO Secrets Management]] (Golden Path, protocols)
    - Practical guide for managing `VaultStaticSecret` and `VaultDynamicSecret` resources.
- Rotation & Troubleshooting: [[SoT - FitFile Deployment - Troubleshooting and Known Issues]]
    - See Section 1.3 for the Rotation Policy.
    - See Section 2.1 for Stale Secret debugging.
- Audit Reports:
    - [[lca-prd-2-vault-vso-audit]] (Production cluster audit; cleanup checklist).

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
