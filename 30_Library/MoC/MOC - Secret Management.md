---
created: 2026-04-02T11:10:00+01:00
modified: 2026-05-26T11:44:22+00:00
status: active
tags: [moc, secrets, security, vault]
title: MOC - Secret Management
---

## MOC - Secret Management

### 1. Core Architectures (SoT)

- [[SoT - Vault Secrets Operator (VSO)]]: The primary bridge between Vault and Kubernetes.
- [[SoT - Vault Infrastructure Automation]]: Manifest-driven provisioning of Vault resources via Terraform.
- [[SoT - Kubernetes Secrets Management]]: Fundamental behavior of the K8s Secret API.
- [[SoT - Zero Knowledge Architecture]]: Principles of minimal-trust design.

### 2. Operational Procedures (Protocols)

- [[Protocol - VSO Secret Management & Troubleshooting]]: Playbook for rotation, refresh, and debugging.
- [[Protocol - GitLab CLI Authentication]]: Managing M2M access for CI/CD and ArgoCD.
- [[Protocol - Vault Deployment Secret Management]]: Domain-specific patterns for LCA-DP.

### 3. Related Concepts

- [[MOC - CUE Configuration]]: Using CUE to render complex secret transformations.
- [[SoT - Infrastructure Complexity]]: Addressing the fragility of string-based coupling.
- [[SoT - Modern Authentication Standards]]: OIDC, JWT, and mTLS.

---

### Integration Queue

- [ ] Implement JSON Schema validation for the Vault manifest.
- [ ] Migrate manual AppRole SecretIDs to temporary OIDC-based bootstrap.
