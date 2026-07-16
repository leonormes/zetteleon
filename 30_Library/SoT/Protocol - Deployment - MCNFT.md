---
aliases: []
created: 2026-02-01T15:45:00+00:00
id: Protocol - Deployment - Mersey Care
modified: 2026-07-13T08:52:41+00:00
permalink: llmeon/30-library/so-t/protocol-deployment-mcnft
status: active
tags: [azure, deployment, mersey-care, protocol]
title: Protocol - Deployment - MCNFT
type: protocol
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## 1. Executive Summary

This protocol defines the specific execution path for the Mersey Care deployment, aligning the standard FITFILE Deployment Playbook with the specific infrastructure requirements (Hub-Spoke, Two Node Pools, NWSDE integration).

- Deployment Key: `mcnft-prd-01` (Provisional)
- Target Subscription: FITFILE Subscription Spoke (Peered to Customer Hub)
- Primary DNS Zone: `prod-1.fitfile.net` (Private Split-Horizon)

---

## 2. Configuration Variables (Inputs)

| Variable              | Value                | Notes                                 |
|:-------------------- |:------------------- |:------------------------------------ |
| `customer_id`         | `mersey-care`        |                                       |
| `deployment_key`      | `mersey-care-prd-01` | Used for Vault paths & TFC Workspaces |
| `hub_vnet_id`         | `[PENDING]`          | Customer Hub VNET Resource ID         |
| `hub_subscription_id` | `[PENDING]`          | Customer Subscription ID              |
| `dns_zone`            | `prod-1.fitfile.net` | Override: Standard is `{id}.internal` |
| `aks_version`         | `1.28.x`             | Confirm current LTS                   |

---

## 3. Discovery Track (Blocking Questions)

> [!danger] Resolution Required Before Phase 1
> These items correspond to the "Open Questions" in the architecture definition.

1. NWSDE Connectivity:
   - _Question:_ How will the NWSDE Node access the FITFILE Node?
   - _Action:_ Determine if peering, Private Link, or VPN is required for the "LCA FITFILE Node" inside NWSDE.
2. DNS Management Strategy:
   - _Question:_ How will DNS be managed?
   - _Action:_ Confirm if `prod-1.fitfile.net` is delegated to us or if we manage records in their existing DNS servers via forwarded requests.
3. User Access (Web App):
   - _Question:_ How will Data Managers/Analysts access the Web App?
   - _Action:_ Confirm if Ingress IP is private (VPN only) or public (Internet accessible via Allow-list). _Assumption based on Architecture: Private Access via VPN._

---

## 4. Execution Roadmap

### Phase 0: Pre-Flight & Compliance

- [ ] 0.1 NDOO Check: Verify "National Data Opt-Out" (NDOO) technical requirements. Does the `ffnode` chart need specific flags enabled?
- [ ] 0.2 CIDR de-conflict: Get the CIDR range of the Customer Hub VNET. Ensure our Spoke VNET candidate (`10.x.x.x/16`) does not overlap.
- [ ] 0.3 Vault Init: Create path `admin/central/mersey-care` in Central Vault.
- [ ] 0.4 Deployment Key: Register `mersey-care-prd-01` in Terraform Cloud.

### Phase 1: Network Fabric (Hub-Spoke)

_Reference: [[SoT - FitFile Deployment - Implementation Manual#Phase 1: Network Provisioning (The Bedrock)]]_

1.1 Provision VNET (Spoke):

- Create `vnet-mersey-care-prd-01`.
- Critical Subnets:
  - `snet-jumpbox` (Jumpbox VM)
  - `snet-workflows` (Data Pipeline Node Pool)
  - `snet-system` (Platform Node Pool)
- [ ] 1.2 Establish Peering:
  - Initiate peering from `vnet-mersey-care-prd-01` to `[Hub-VNET-ID]`.
  - Request Customer Network Team to approve/reciprocate peering.
- [ ] 1.3 Private DNS Zone:
  - Create Azure Private DNS Zone: `prod-1.fitfile.net`.
  - Link to Spoke VNET and Hub VNET (Request customer to link if cross-subscription permissions are restricted).
- [ ] 1.4 Firewall Rules (Hub):
  - Request outbound allow-list for Spoke Subnets to Central Services (Auth0, Vault, ACR, Grafana).

### Phase 2: Infrastructure (AKS & Bastion)

_Reference: [[SoT - FitFile Deployment - Implementation Manual#Phase 3: AKS Cluster Deployment]] (Note: Mersey Specifics)_

- [ ] 2.1 Jumpbox Provisioning:
  - Deploy VM in `snet-jumpbox`.
  - Enable Azure Bastion for secure Admin access (No Public IP on VM).
- [ ] 2.2 AKS Deployment:
  - Deploy Cluster: `aks-mersey-care-prd-01`.
  - Node Pool A (System):
    - Subnet: `snet-system`.
    - Label: `pool=system`.
  - Node Pool B (Workflows):
    - Subnet: `snet-workflows`.
    - Label: `pool=workflows`.
    - Taint: `workload=pipeline:NoSchedule` (Ensure pipeline jobs are targeted).
- [ ] 2.3 OIDC & Identity:
  - Enable Workload Identity.
  - federate with Central Vault.

### Phase 3: Platform Bootstrap

- [ ] 3.1 Secrets: Sync `fitfile-image-pull-secret` from Central Vault to `mersey-care-prd-01` path.
- [ ] 3.2 VSO & ArgoCD:
  - Deploy `vault-secrets-operator`.
  - Deploy `argocd` (Core GitOps engine).
- [ ] 3.3 Ingress Controller:
  - Deploy NGINX Ingress.
  - Override: Ensure annotations set LoadBalancer to Internal (`service.beta.kubernetes.io/azure-load-balancer-internal: "true"`).
  - Capture the Internal IP (e.g., `10.x.x.50`).

### Phase 4: Application Deployment

- [ ] 4.1 Deploy `ffnode`:
  - Target: `mersey-care` branch/tag in GitOps repo.
  - Feature Flags:
    - `deploy.monitoring: true` (Grafana Agent)
    - `deploy.persistence: true` (Azure Disk backed)
- [ ] 4.2 Data Pipeline Configuration:
  - Configure Workflow Engine to target `pool=workflows` Node Pool.
  - Verify NWSDE connectivity (based on Phase 0 discovery).

### Phase 5: Access & Security

- [ ] 5.1 DNS Records:
  - Create A-Record in `prod-1.fitfile.net` Private Zone: `*.prod-1` -> `[Ingress Internal IP]`.
- [ ] 5.2 Certs:
  - Configure `cert-manager` with ACME Issuer (DNS-01 challenge likely required if private, or HTTP-01 if outbound 80 is allowed).
- [ ] 5.3 Auth0:
  - Configure Mersey Care Tenant in Auth0.
  - Update `ffcloud` OIDC config.

### Phase 6: Handoff & Validation

- [ ] 6.1 User Access Test:
  - Connect via VPN (mimicking Customer User).
  - Access `https://console.prod-1.fitfile.net`.
  - Login via Auth0.
- [ ] 6.2 Data Ingress Test:
  - Upload dummy CSV (Data Analyst workflow).
  - Verify processing on `workflows` node pool.
