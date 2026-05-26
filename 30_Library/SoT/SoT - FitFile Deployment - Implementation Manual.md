---
aliases: [Deployment SOP, FitFile Deployment Guide, Master Deployment Checklist, Phase 1-6 Manual]
created: 2025-12-21T10:50:49Z
last_reviewed: "2026-03-28"
modified: 2026-05-26T11:44:20+00:00
status: evergreen
tags: [deployment, ff_deploy, manual, ops, sop]
title: SoT - FitFile Deployment - Implementation Manual
type: SoT
updated: 2026-03-28
---

## 1. Overview & Critical Path

This manual details the six-phase execution of a FITFILE deployment. It serves as the primary checklist for Deployment Engineers.

Critical Path Summary:

`Kernel Definition` → `Provider Gen` → `Infra Apply` → `CUE Generation` → `Jumpbox Setup` → `ArgoCD Sync` → `Smoke Tests`

---

## Phase 0: Pre-Flight & Generative Setup

Goal: Verify prerequisites and generate the dynamic provider configuration.

| Step | Action | Prerequisite | Verification |
|:---|:---|:---|:---|
| 0.1 | Edit `customer.yaml` | Allocation from NetTeam | Check `vnet_address_space` and `deployment_key`. |
| 0.2 | Generate `providers.tf` | TFC Organization access | `make generate-providers`. Verify workspace name. |
| 0.3 | Initialize Backend | Provider gen complete | `terraform init`. Should link to the new TFC workspace. |
| 0.4 | Validate CIDR | Network planning | Ensure `10.x.x.x/16` does NOT overlap with Client On-Prem. |

---

## Phase 1: Network Provisioning (The Bedrock)

Goal: Establish the network fabric and connectivity to Central Services.

1. Apply Terraform: Provision VNet and Subnets.
   - _Note_: Subnets (System, Workflows, App, Jumpbox) are sliced using deterministic `cidrsubnet` math.
2. Establish Peering: Connect Customer VNet to Central Services Hub VNet.
3. Configure DNS: Link Private DNS Zones to both VNets.
4. Client Handoff: Provide Ingress IP (System Subnet offset.203) to the client firewall team.

---

## Phase 2: Central Services Integration

Goal: Establish identities, secrets, and repositories.

1. GitLab Repo: Create the customer infrastructure repository.
2. Vault Path: Create `admin/deployments/{deployment-key}`.
3. Seed Secrets: Inject initial keys (ACR Pull, Database Credentials) into Vault.
   - _LCA Pattern_: Use `admin/central/azure/creds/acr-pull` for dynamic registry auth.

---

## Phase 3: AKS Cluster Deployment

1. Deploy AKS: Execute `terraform apply`. Ensure OIDC Issuer is enabled.
2. OIDC Propagation: Wait 15-30 mins for the OIDC discovery URL to become consistent across Azure/Vault.
3. Verify Host Network: Ensure `cert-manager` is configured for Host Network if deploying into strict Trust environments.

---

## Phase 4: Platform & Configuration Generation

Goal: Deploy the software stack via GitOps.

1. Generate Helm Values:
   - Run `make generate-values`.
   - The script extracts `infra_facts`, validates via CUE, and writes to `generated/values.yaml`.
2. Jumpbox Bootstrap:
   - Connect via Bastion: `./scripts/connect-jumpbox.sh`.
   - Extract config: `terraform output -raw jumpbox_main_content > main.tf`.
   - Run `terraform apply` from the jumpbox to deploy the ArgoCD Root App and VSO Auth.
3. ArgoCD Sync: Verify the Root Application (`ff-{deployment-key}`) is syncing.

---

## Phase 5: Certificate & Ingress Configuration

1. TLS Issuance: Verify `cert-manager` completes the DNS-01 ACME challenge.
2. Split-Horizon Validation:
   - `dig {host}` (Normal): Should return Private IP (`192.168.x.x`).
   - `dig +trace {host}` (Public): Should return Cloudflare Public IP.
3. Ingress Validation: `curl -v https://{host}/fitconnect/health`.

---

## Phase 6: Client Handoff & Validation

1. Smoke Test: Execute a sample workflow and verify data persistence in MongoDB/PostgreSQL.
2. Observability: Check Grafana for VSO sync metrics and Pod resource utilization.

---

## Automation Quick Reference

| Command | Purpose |
|:---|:---|
| `make generate-providers` | Syncs `providers.tf` with the current `customer.yaml` identity. |
| `make generate-values` | Validates facts and generates the Helm `values.yaml` manifest. |
| `make validate-cue` | Runs `cue vet` against the infrastructure contract. |
| `terraform output infra_facts` | Views the raw typed contract passed to the App layer. |
