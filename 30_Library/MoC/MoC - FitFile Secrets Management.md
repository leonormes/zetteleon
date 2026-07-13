---
aliases: [FitFile Secrets Index, Secrets MoC, Vault Secrets Index, VSO Secrets Map]
created: 2026-03-14T12:00:00+00:00
modified: 2026-07-13T08:45:07+00:00
permalink: llmeon/30-library/mo-c/mo-c-fit-file-secrets-management
tags: [fitfile, moc, secrets, security, vault, vso]
title: MoC - FitFile Secrets Management
---

## MoC - FitFile Secrets Management

Single source of truth: [[SoT - FitFile VSO Secrets Management]]

---

### 1. Core Architecture & Strategy

- [[SoT - FitFile VSO Secrets Management]]—Canonical deep dive: secret types, auth, Vault structure, operations, troubleshooting
- [[SoT - VSO Authentication (JWT vs AppRole)]]—Auth method comparison; why JWT for HCP Vault + private AKS
- [[SoT - Kubernetes Secrets Management]]—Underlying K8s concepts (etcd, RBAC, consumption patterns)
- [[fitfile-vault-vso-argocd-architecture]]—Mermaid diagram: HCP Vault → VSO → ArgoCD → Pods

---

### 2. Operations & Protocols

| Document | Purpose |
|:---|:---|
| [[Protocol - VSO Secret Management & Troubleshooting]] | Overwrite rule, force refresh, ArgoCD repo-creds priority |
| [[Protocol - Vault Deployment Secret Management]] | Bootstrap new deployment: Terraform scaffolding, Vault population |
| [[SoT - FitFile Secrets Operations (Vault & VSO)]] | Golden path: create, map, verify (legacy SOP; superseded by main SoT) |

---

### 3. Troubleshooting & Playbooks

| Document | Trigger |
|:---|:---|
| [[playbook_vso_secret_debugging]] | VSO-managed secret stale, 401/403, misconfigured |
| [[playbook_argocd_vso_oci_registry_auth_failure]] | ArgoCD sync fails with 401 against Helm OCI registry |
| [[kb_vso_metadata_identifiers]] | Trace secret → Vault path (ownerReferences, mount, path) |
| [[kb_vso_stale_credentials_logic]] | Overwrite block; stale credential root cause |

---

### 4. Case Studies & Audits

| Document | Content |
|:---|:---|
| [[ARGO_VSO_ROOT_CAUSE]] | ArgoCD deploying wrong VaultStaticSecret path; inline values override |
| [[lca-prd-2-vault-vso-audit]] | Production cluster audit: Vault structure, VSO resources, cleanup checklist |

---

### 5. Related Maps & Domains

- [[MoC - FitFile Security & Secrets]]—Broader security (IAM, container hardening)
- [[SoT - FitFile Identity & Access Management (Auth0)]]
- [[SoT - External Ingress & SSL Architecture]]

---

### Quick Actions

| Task | Action |
|:---|:---|
| Add a secret | [[SoT - FitFile VSO Secrets Management#10. Golden Path: Adding a New Secret]] |
| Secret not updating | [[Protocol - VSO Secret Management & Troubleshooting#2. The Overwrite Golden Rule]] |
| Auth error | [[Protocol - VSO Secret Management & Troubleshooting#4. Troubleshooting Playbook]] |
| ArgoCD 401 on registry | [[playbook_argocd_vso_oci_registry_auth_failure]] |
