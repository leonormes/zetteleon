---
created: 2026-02-13T10:21:27+00:00
modified: 2026-02-13T18:52:47+00:00
title: Kubernetes Namespaces and Secret Mapping
---

## Overview

This document outlines the mapping of Kubernetes namespaces to the secrets they require, specifically focusing on the integration with HCP Vault via Vault Secrets Operator (VSO) and Reflector.

### Secret Management Architecture

- HCP Vault: Central store for secrets.
- Vault Secrets Operator (VSO): Synchronizes secrets from HCP Vault to Kubernetes `Secret` resources using `VaultStaticSecret` and `VaultDynamicSecret` CRDs.
- Reflector: Used to mirror secrets (e.g., TLS certificates) across namespaces (Assumed based on user context, though explicit configuration was not found in the inspected charts).

## Deployment: EoE (hie-prod-34)

### Namespace: `hie-prod-34`

The primary application namespace.

| Secret Name | Source (Vault Path) | Destination K8s Secret | CRD Type | Notes |
|:--- |:--- |:--- |:--- |:--- |
| relay | `hutch-prod` | `relay` | `VaultStaticSecret` | Contains DB, RabbitMQ, and Upstream API credentials. |
| hutch-postgresql | `hutch-prod` | `hutch-postgresql` | `VaultStaticSecret` | Postgres admin password. |
| hutch-rabbitmq | `hutch-prod` | `hutch-rabbitmq` | `VaultStaticSecret` | RabbitMQ admin password and Erlang cookie. |
| relay-downstream-users | `hutch-prod` | `relay-downstream-users` | `VaultStaticSecret` | Passwords for downstream users (e.g., cuhbunny1). |
| s3-export-secret | `application` | `s3-export-secret` | `VaultStaticSecret` | S3 credentials for workflows (export). |
| fitfile-eoe-tls | Vault PKI (`pki_int_hie-prod-34`) | `fitfile-eoe-tls` | `Certificate` | TLS certificate for ingress. |

### Namespace: `ohdsi`

Used for OHDSI tools.

| Secret Name | Source | Destination K8s Secret | CRD Type | Notes |
|:--- |:--- |:--- |:--- |:--- |
| ohdsi-eoe-tls | Vault PKI | `ohdsi-eoe-tls` | `Certificate` | TLS certificate for OHDSI ingress. |

### Namespace: `workflows` (implied)

Used for Argo Workflows execution (if separate from app namespace).

_Note: Secrets like `s3-export-secret` are defined in the main values but might be used by workflow pods._

---

## Deployment: Fitfile Prod 1 (ff-a)

### Namespace: `ff-a`

The primary application namespace.

| Secret Name | Source (Vault Path) | Destination K8s Secret | CRD Type | Notes |
|:--- |:--- |:--- |:--- |:--- |
| pg-web | `ff-a-application` | `pg-web` | `VaultStaticSecret` | Credentials for PGWeb UI (Demo). |
| sleuth-secret | `ff-a-application` | `sleuth-secret` | `VaultStaticSecret` | API key for Sleuth deployment tracking. |
| s3-export-secret | `ff-a-application` | `s3-export-secret` | `VaultStaticSecret` | S3 credentials for export. |
| frontend | `application` | `frontend` | `VaultStaticSecret` (Templated) | Frontend specific secrets. |
| fitconnect | `application` | `fitconnect` | `VaultStaticSecret` (Templated) | FitConnect specific secrets. |
| ffcloud | `application` | `ffcloud` | `VaultStaticSecret` (Templated) | FFCloud specific secrets. |
| mongodb | `application` | `mongodb` | `VaultStaticSecret` (Templated) | MongoDB credentials. |
| postgresql | `application` | `postgresql` | `VaultStaticSecret` (Templated) | PostgreSQL credentials. |
| fitfile-ff-a | `cloudflare-issuer-api-token` | `cloudflare-tls` | `Certificate` | TLS certificate. |

### Namespace: `argocd` / `argo`

Management namespaces.

| Secret Name | Source | Destination K8s Secret | CRD Type | Notes |
|:--- |:--- |:--- |:--- |:--- |
| cloudflare-tls | Let's Encrypt / Cloudflare | `cloudflare-tls` | `Certificate` | TLS certificate for ArgoCD/Workflows UI. |

### Namespace: `ff-b`, `ff-c`, `barts`

Other customer namespaces managed by this cluster.

| Secret Name | Source | Destination K8s Secret | CRD Type | Notes |
|:--- |:--- |:--- |:--- |:--- |
| cloudflare-tls | Let's Encrypt / Cloudflare | `cloudflare-tls` | `Certificate` | TLS certificate. |

---

## Templating Mechanism

Secrets are dynamically generated using the `_helpers.tpl` file in the `ffnode` chart.

- Key Function: `generateVaultDynamicSecrets` and `VaultStaticSecret` template.
- Configuration: Defined in `values.yaml` under `vaultSecrets` lists.
- Source: Look for `charts/ffnode/templates/_helpers.tpl` for the logic and `values.yaml` for the secret definitions.

## Templating Mechanism

---

### Related Knowledge

- [[SoT - FITFILE Secret Management Architecture]] (Canonical Reference)
- [[Protocol - Vault Deployment Secret Management]] (Onboarding)
- [[SoT - FitFile Secrets Operations (Vault & VSO)]] (Operations)
