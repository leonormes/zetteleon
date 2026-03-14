---
aliases: [Secrets Management Index, Secrets MoC, Vault MoC]
created: 2026-03-14T10:00:00Z
modified: 2026-03-14T10:29:48+00:00
status: evergreen
tags: [fitfile, kubernetes, moc, secrets, security, vault]
title: MoC - Secrets & Vault Management
type: MoC
---

## MoC - Secrets & Vault Management

### 1. Governance & Strategy

- [[SoT - FITFILE Secret Management Architecture]]: The canonical structural overview of how secrets flow from HCP Vault to Kubernetes.
- [[SoT - The Data-Centric Philosophy]]: Underlying principles of managing configuration and secrets as data.
- [[SoT - Zero Knowledge Architecture]]: Security principles for cross-cloud and hybrid deployments.

### 2. Core Infrastructure (The Stack)

- [[SoT - HashiCorp Vault Architecture]]: Deep dive into Vault's internal data structures (Tries, Merkle Trees) and path-based routing.
- [[SoT - Kubernetes Secrets Management]]: How Kubernetes handles secrets at rest and in etcd.
- [[SoT - VSO Authentication (JWT vs AppRole)]]: Comparison and rationale for authentication methods used by the operator.

### 3. Operations & Protocols (The Manual)

- [[SoT - FitFile Secrets Operations (Vault & VSO)]]: The "Golden Path" for creating, mapping, and verifying secrets.
- [[Protocol - VSO Secret Management & Troubleshooting]]: Essential playbook for fixing stuck secrets, handling rotation, and the "Overwrite" rule.
- [[Protocol - Vault Deployment Secret Management]]: Specific steps for bootstrapping Vault in new environments.

### 4. Problem Solving & Analysis

- [[ARGO_VSO_ROOT_CAUSE]]: Case study on debugging ArgoCD sync issues vs. VSO path overrides.
- [[VAULT_IAC_ASSESSMENT]]: Evaluation of Infrastructure-as-Code patterns for managing Vault resources.
- [[lca-prd-2-vault-vso-audit]]: Real-world audit of a production cluster's secret state.

---

### Quick Actions

- Need to add a secret? Follow [[SoT - FitFile Secrets Operations (Vault & VSO)#Step 3 Map in Helm]].
- Secret not updating? Check [[Protocol - VSO Secret Management & Troubleshooting#2 The Overwrite Golden Rule]].
- Auth error? See [[Protocol - VSO Secret Management & Troubleshooting#Phase 1 Diagnostics]].
