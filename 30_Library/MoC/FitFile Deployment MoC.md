---
tags: ["ff_deploy", "MoC", "deployment"]
type: MOC
status: active
---

# FitFile Deployment MoC

## Context
This Map of Content centralizes all knowledge, procedures, and standards related to the deployment of the FitFile Platform. It serves as the entry point for engineers configuring, deploying, or troubleshooting the stack.

## 1. The Core Standard (Source of Truth)
*   [[SoT - FitFile Deployment]] - **The Canonical Guide.** Read this first. Covers Architecture, Module Usage (v2.0.0+), and Security.

## 2. Infrastructure & Environment
*   **Infrastructure (Terraform Cloud):** Handles base Azure/AWS resources (AKS, VNet).
*   **Platform (Jumpbox):** Deploys the Kubernetes runtime using the `terraform-helm-fitfile-platform` module.
*   **Application (ArgoCD):** Deploys the actual FitFile workloads (`ffnode`, etc.).

## 3. Operational Guides & Workflows
*(Links to be populated as specific procedural notes are identified or created)*
*   [[FITFILE Customer Onboarding Prompt]] - *Check location*
*   [[Azure Jumpbox Preflight Check - Customer One-Pager]] - Pre-deployment verification.
*   [[How to Backup and Restore Kubernetes Clusters Using Velero]] - Disaster Recovery.
*   [[How to Reduce Grafana Cloud Costs]] - Observability tuning.

## 4. Key Components
*   **Ingress:** NGINX Controller (Internal LB).
*   **Secrets:** HashiCorp Vault + VSO + Reflector.
*   **GitOps:** ArgoCD.

## 5. Troubleshooting
*   See "Troubleshooting & Operations" in [[SoT - FitFile Deployment]].
*   For Network issues: [[Network Policies]]
*   For Cloud connectivity: [[Cloud Network]]

## 6. Deprecated / Archived
*   *Old Wikis and processed analysis notes have been consolidated into the SoT.*
