---
aliases: ["Central Services Index", "FitFile Deployment Phase 1"]
confidence: "5/5"
created: 2025-12-21T10:50:49Z
epistemic: "process"
last_reviewed: "2025-12-23"
modified: 2025-12-25T18:34:55Z
purpose: "The definitive guide and index for establishing the FitFile control plane and central services."
review_interval: "3 months"
see_also: ["[[Auth0 Object Architecture - FITFILE Deployments]]", "[[Grafana IaC Report]]", "[[MOC - FitFile Deployment]]", "[[SoT - FITFILE Platform Deployment]]"]
source_of_truth: []
status: "stable"
tags: ["central_services", "ff_deploy", "foundation", "phase1", "tooling"]
title: SoT - FitFile Deployment - Phase 1 - Foundation and Tooling
type: "SoT"
uid: 
updated: 
---

## 1. Goal: Establishing the Control Plane

Phase 1 establishes the foundational components needed for authentication, secret management, and monitoring. This is the **"Key to the Castle"**—all subsequent infrastructure and application layers depend on these central services being healthy and correctly configured.

### 1.1 The Central Services Model

FitFile uses a **Hybrid Architecture** for its control plane:

- **Shared Resources:** One instance per Org (e.g., Auth0 Tenant settings, Vault root, Grafana Cloud org). Managed in the `central-services` repository.
- **Distributed Resources:** One instance per customer deployment (e.g., Auth0 Clients, Vault Namespaces, Grafana Stacks).

---

## 2. The Tooling Inventory

Ensure your local workstation is equipped with the following "Compiled Binaries":

| Tool | Role | Purpose |
|:--- |:--- |:--- |
| **Terraform** | IaC Engine | Provisioning all cloud and service resources. |
| **tfenv** | Version Manager | Managing multiple Terraform versions (v1.9.0+ required). |
| **aws/az CLI**| Cloud Interface | Authenticating with AWS/Azure providers. |
| **kubectl** | Cluster Interface| Managing Kubernetes resources once the cluster is live. |
| **UDE CLI** | Secret Generator | Generating the Unique Data Encryption (UDE) keys. |

---

## 3. Central Services Connectivity

For private clusters (SDE/HIE), the following FQDNs must be present in the **Outbound Allow List** to enable the control plane to communicate with the cluster.

| Service | URL | Protocol |
|:--- |:--- |:--- |
| **HashiCorp Vault** | `vault-public-vault-*.hashicorp.cloud:8200` | HTTPS |
| **Auth0 Tenant** | `fitfile-prod.eu.auth0.com` | HTTPS |
| **Grafana (Metrics)** | `prometheus-prod-05-gb-south-0.grafana.net` | HTTPS |
| **Grafana (Logs)** | `logs-prod-008.grafana.net` | HTTPS |
| **Azure Registry** | `fitfileregistry.azurecr.io` | HTTPS |

---

## 4. Execution Protocols

### A. Deployment Key Generation

The `deployment_key` is the primary identifier for all resources.

1. Run `./short_name.sh` in the `central-services` repo.
2. Save the key (e.g., `WM-Prod`) and record it in the [Deployment Database](https://fitfile.atlassian.net/wiki/spaces/FITFILE/database/1839071273). This key will be used consistently across Vault, Auth0, TFC, and Cloud Providers.

### B. Vault Configuration

Establish the **Secrets Path** before provisioning infrastructure.

> [!warning] Security Audit (Oct 2025)
> **Do not use `shared-secrets` charts.** The 2025 Audit found hardcoded credentials in legacy deployments. All secrets must be provisioned via VSO as defined in the [[SoT - FITFILE Secret Management Architecture]].

- **Pattern:** `deployments/<deployment-key>/application`
- **Mechanism:** Add the key to `locals.tf` in `central-services/hcp/vault`.
- **Goal:** Create all necessary credentials for databases, monitoring, and application services.
- **See Also:** [[SoT - FITFILE Secret Management Architecture]]

### C. Auth0 Configuration

Create the **Logical Identity** for the new node.

- **Pattern:** Create unique SPA and M2M clients; link to the shared "Username-Password-Authentication" connection.
- **Mechanism:** Update `locals.tf` in `central-services/auth0/prod`.
- **Goal:** Establish the authentication mechanism for the application stack.
- **Reference:** [[Auth0 Object Architecture - FITFILE Deployments]]

### D. Monitoring (Grafana)

Setup the **Observability Stack**.

- **Pattern:** Provision a new stack and associated data sources (Loki, Prometheus).
- **Mechanism:** Update `grafana/locals.tf` in `central-services`.
- **Goal:** Configure monitoring through Grafana for full-stack visibility.
- **Reference:** [[Grafana IaC Report]]

---

## 5. Verification Checklist

- [ ] **TFC Connectivity:** Workspace can pull from GitLab.
- [ ] **Vault Paths:** `secret/fig/<deployment-key>/application` exists and is populated.
- [ ] **Auth0 Tenants:** New API and Application visible in Auth0 dashboard.
- [ ] **Grafana Stack:** Data sources provisioned and reachable via the tokens stored in Vault.
