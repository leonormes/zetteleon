---
aliases: [FITFILE Secret Management Architecture, Secret Management SoT, VSO Implementation Guide]
created: 2025-12-15T00:00:00Z
last_reviewed: 2026-02-13
modified: 2026-02-13T10:26:57+00:00
status: evergreen
tags: ["SoftwareEngineering/Architecture", "SoftwareEngineering/Security", fitfile, kubernetes, vault]
title: SoT - FITFILE Secret Management Architecture
type: SoT
updated:
uuid: d33b2418-260e-4eba-8375-26c545e2792e
---

## 2. The Canonical Architecture

The standard implementation leverages a data-driven approach where secrets are defined in Helm values and materialized by VSO.

### Core Components

1. HashiCorp Vault: The central, encrypted source of truth for all secret data.
2. Vault Secrets Operator (VSO): The Kubernetes operator that authenticates with Vault (via AppRole or JWT) and synchronizes secrets into Kubernetes `Secret` resources.
3. VaultConnection: A cluster-wide resource (`default` in `vault-secrets-operator-system`) that defines the link to the HCP Vault instance.
4. Reflector: Mirroring operator used to distribute secrets (e.g., TLS certs) across namespaces.
5. Helm / ArgoCD: The delivery mechanism that configures VSO resources via the `ffnode` chart.

### 2.1 Dynamic Infrastructure Secrets (ACR)

Unlike application secrets (static KV), infrastructure credentials like image pull secrets are generated dynamically to ensure short-lived access.

- Mechanism: `VaultDynamicSecret` (via `charts/ffnode/_helpers.tpl`).
- Resource Example: `argocd-pull` in `argocd` namespace pointing to `creds/acr-pull`.
- Refresh: Automatically rotated every 1 hour (standard) or 10m (aggressive/testing).

---

## 3. Deployment Inventory & Status

Based on an investigation of the production cluster (Feb 2026), the following mappings are active:

### A. Active Customer Deployments (VSO Enabled)

| Deployment (NS) | Vault Path (Base) | Auth Namespace | Key Secrets |
|:--- |:--- |:--- |:--- |
| `ff-a` | `ff-a-application` | `admin/deployments/prod-1` | `ffcloud`, `fitconnect`, `mongodb`, `pg-web`, `sleuth-secret` |
| `ff-b` | `ff-b-application` | `admin/deployments/prod-1` | `ffcloud`, `fitconnect`, `fitfile-rsa-private-key` |
| `ff-c` | `ff-c-application` | `admin/deployments/prod-1` | `ffcloud`, `fitconnect`, `ude-secret` |
| `barts` | `application` | `admin/deployments/prod-1` | `frontend`, `mongodb`, `postgresql`, `workflows-secrets` |

### B. Platform & Shared Services

| Service (NS) | Vault Path | Purpose |
|:--- |:--- |:--- |
| `argocd` | `argocd` | GitOps repo credentials & SSO |
| `argo` | `argo-workflows` | Postgres & SSO for workflows |
| `monitoring` | `monitoring` | Grafana/Prometheus credentials |
| `spicedb` | `spicedb` | SpiceDB PSK & DB credentials |
| `cert-manager`| `cloudflare` | Cloudflare API Token for DNS-01 |

---

## 5. Reference Implementation: Integration Layer

Integrations (Hutch, TheHyve) often require complex secret transformations to map Vault KV pairs to specific application-expected environment variables or files.

### 5.1 Secrets Inventory (Hutch/TheHyve)

| Secret Name | NS | Source Path | Refresh | CRD Type |
|:--- |:--- |:--- |:--- |:--- |
| `bunny` | `hutch` | `hutch` | 10m | `VaultStaticSecret` |
| `bunny` | `hutch-mkuh` | `hutch-mkuh` | 10m | `VaultStaticSecret` |
| `thehyve` | `thehyve-mkuh`| `thehyve-mkuh` | 10m | `VaultStaticSecret` |

### 5.2 Transformation Example (Hutch)

The `bunny` secret in the `hutch` namespace demonstrates advanced template mapping:

```yaml
spec:
  destination:
    transformation:
      templates:
        db_password:
          text: '{{get .Secrets "bunny_postgresql_password"}}'
        db_username:
          text: '{{get .Secrets "bunny_postgresql_username"}}'
        task_api_password:
          text: '{{get .Secrets "bunny_relay_password"}}'
        task_api_username:
          text: '{{get .Secrets "bunny_relay_username"}}'
  refreshAfter: 10m
  rolloutRestartTargets:
  - kind: Deployment
    name: hutch-bunny
```

---

## 6. Future Improvements & Automation

### 6.1 Standardizing Auth Scopes

Currently, most deployments share the `admin/deployments/prod-1` Vault namespace scope. Future refactoring will transition to individual Vault namespaces per customer deployment to ensure strict isolation.

### 6.2 Refresh Policy Standardization

- Critical Secrets: `5m` (e.g., `ffcloud`, `frontend`)
- Integration Secrets: `10m` (e.g., `hutch`, `thehyve`)
- Infrastructure Secrets: `30m` or `1h`
