---
alias: ["FFNode Deployment", "Helm Chart Deployment Guide"]
aliases: []
confidence: "5/5"
created: 2025-02-07T12:57:55Z
epistemic: "guide"
last_reviewed: "2025-12-26"
modified: 2026-01-23T18:09:20+00:00
purpose: "To provide the standard operating procedure for deploying FitFile applications using Helm, specifically focusing on the FFNode umbrella chart and configuration overrides."
review_interval: "6 months"
see_also: ["[[SOT - CI-CD Pipelines]]", "[[SoT - FitFile Deployment - Release Process]]", "[[SoT - FITFILE Platform Deployment]]", "[[SoT - Kubernetes Networking & DNS]]"]
source_of_truth: []
status: "stable"
tags: ["deployment", "fitfile", "helm", "kubernetes", "sop"]
title: SoT - FitFile Deployment - Helm Configuration & Operations
type: "SoT"
uid: 
updated: 
---

## 1. Overview

FITFILE deployments utilize a **GitOps-compatible Helm architecture**. The core principle is "Configuration as Code," where a generic chart (`ffnode`) is specialized for each environment (e.g., `ff-a`, `prod-1`) via specific `values.yaml` overrides.

---

## 2. Chart Architecture

### 2.1 The Umbrella Pattern

We utilize an **Umbrella Chart** approach to deploy the entire stack as a single unit.

- **Root Chart:** `charts/ffnode`
- **Subcharts:** `frontend`, `fitconnect`, `mongodb`, `keycloak` (legacy), `auth0-config`.

### 2.2 Directory Structure

```sh
charts/
├── ffnode/                  # The Umbrella Chart
│   ├── Chart.yaml           # Metadata & Dependencies
│   ├── values.yaml          # Default Configuration
│   └── templates/           # K8s Manifests
└── [component]/             # Individual Service Charts (e.g., frontend)
    ├── Chart.yaml
    └── templates/
```

---

## 3. Configuration Management

### 3.1 The Values Hierarchy

Configuration is layered to ensure stability while allowing specificity:

1. **Chart Defaults:** `charts/ffnode/values.yaml` (Base configuration).
2. **Environment Overrides:** `environments/<env>/values.yaml` (Specific to `ff-a`, `prod`, etc.).
3. **Secrets:** Injected at runtime via Vault (See [[SoT - FITFILE Secret Management Architecture]]).

### 3.2 Key Configuration Parameters

| Parameter | Description | Example |
|:--- |:--- |:--- |
| `namespace` | Target K8s namespace. | `ff-a` |
| `deploymentKey` | Unique ID for resource tagging. | `prod-1` |
| `host` | Public ingress domain. | `app.fitfile.net` |
| `applicationVaultPath` | Path to secrets in Vault. | `deployments/prod-1/application` |
| `global.sleuth` | Distributed tracing config. | `enabled: true` |

---

## 4. Operational Workflows

### 4.1 Modifying a Chart

1. **Edit:** Modify `charts/<component>/templates/*.yaml`.
2. **Bump:** Increment `version` in `Chart.yaml` (Semantic Versioning).
3. **Test:** Run `helm template.` locally to verify manifest generation.

### 4.2 Manual Deployment (Testing)

For local testing or manual overrides (outside ArgoCD):

```bash
# Syntax
helm upgrade --install <release-name> ./charts/ffnode \
  --namespace <namespace> \
  --values environments/<env>/values.yaml

# Example (FF-A Demo)
helm upgrade --install ff-a ./charts/ffnode \
  --namespace ff-a \
  --values ffnodes/fitfile/ff-a/values.yaml
```

---

## 5. Troubleshooting & Invariants

- **Immutable Tags:** Never redeploy a chart with the same image tag if the code changed. Always use a new SHA or semantic version.
- **Secret Absence:** If pods fail to start, check if the `applicationVaultPath` exists in Vault and contains the expected keys.
- **Ingress Validation:** Ensure `host` matches the DNS record created in Cloudflare.
