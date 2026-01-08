---
aliases: ["FitFile Deployment Guide", "Phase 1-4 Manual", "Setup Checklist"]
confidence: "5/5"
created: 2025-12-21T10:50:49Z
epistemic: "process"
last_reviewed: "2025-12-30"
modified: 2026-01-08T10:49:43+00:00
purpose: "The definitive operational guide for deploying a FITFILE node from scratch."
review_interval: "3 months"
see_also: ["[[SoT - FitFile Deployment - Strategy & Architecture]]", "[[SoT - FITFILE Secret Management Architecture]]"]
source_of_truth: []
status: "stable"
tags: ["deployment", "ff_deploy", "manual", "ops"]
title: SoT - FitFile Deployment - Implementation Manual
type: "SoT"
uid: 
updated: 
---

## 1. Overview

This manual details the four-phase execution of a FITFILE deployment.

---

## Phase 1: Foundation & Tooling (The Control Plane)

**Goal:** Establish the identities, secrets, and monitoring stacks.

1. **Generate Deployment Key:** Run `./short_name.sh` (e.g., `WM-Prod`).
2. **Vault Setup:** Create the path `deployments/<key>/application` in HCP Vault. Populate with initial secrets.
3. **Auth0 Setup:** Provision SPA and M2M clients in the Auth0 tenant.
4. **Grafana Setup:** Provision a new stack/datasource in Grafana Cloud.

**Checklist:**
- [ ] Vault paths exist and are populated.
- [ ] Auth0 Client IDs/Secrets are stored in Vault.
- [ ] Grafana tokens are stored in Vault.

---

## Phase 2: Core Infrastructure (The Bedrock)

**Goal:** Provision the private network and Kubernetes cluster.

1. **Repo Prep:** Create a new deployment repo from the standardized Terraform template.
2. **Cloud Credentials:** Set `ARM_` (Azure) or `AWS_` environment variables in Terraform Cloud.
3. **Apply Infrastructure:** Execute `terraform apply` to create:
    - VPC/VNet (Private subnets).
    - EKS/AKS Cluster.
    - Jumpbox/Bastion host.
4. **Vault AppRole:** Generate the AppRole JSON from `central-services/vault` and inject it into the TFC workspace for the next phase.

**Checklist:**
- [ ] `terraform output` returns Cluster Endpoint.
- [ ] `kubectl get nodes` shows healthy workers.

---

## Phase 3: Platform Services (The Cluster OS)

**Goal:** Install GitOps and Routing tools.

1. **Install ArgoCD & VSO:** Run the platform Terraform module from the **Jumpbox**.
2. **Namespace Prep:**

    ```bash
    kubectl create namespace <deployment-key>
    # Create image pull secret for Azure/AWS registry
    kubectl create secret docker-registry fitfile-image-pull-secret ...
    ```

3. **Routing:** Configure NGINX Ingress and CoreDNS rewrites for internal service discovery.

**Checklist:**
- [ ] ArgoCD UI is accessible and "Healthy."
- [ ] VSO is successfully syncing secrets from Vault.

---

## Phase 4: Application Layer (The Logic)

**Goal:** Deploy FITFILE microservices.

1. **Configure values.yaml:** Update the customer deployment repo with specific feature flags and image versions.
2. **ArgoCD Sync:** Trigger a sync of the `ffnode` umbrella chart.
3. **Initialization:**
    - Insert initial `Tenants` and `Connections` into MongoDB.
    - Setup SpiceDB relationships.

**Checklist:**
- [ ] All ArgoCD applications are "Synced."
- [ ] Frontend is reachable via the Ingress IP.
- [ ] Pods successfully mount Vault-injected secrets.
