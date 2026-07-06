---
created: 2026-05-21T12:48:36+00:00
modified: 2026-07-04T10:49:57+00:00
permalink: llmeon/raw/2026-05-21-pieces-cuh-aks-backup-session-compaction
pieces_ids: [1ce0fe65-de4f-422a-9e9f-3dfbcb1985fa, 8809d6de-e144-4517-9558-1749cf2742f3, b3535217-9689-4610-a7d6-41ee8015db46, d90eaf20-0e8c-4975-96a2-6d4829e2e45b, fc65fdb8-0b73-4320-924f-9a62f9d291fe]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-05-21-pieces-cuh-aks-backup-session-compaction
---

## Context

These are context compaction summaries from a Hermes worker session (2026-05-21 12:44–12:48) on the CUH AKS Backup / Terraform project. Each represents a compaction point where the session context was summarised due to token limits. Together they trace the worker's progress in debugging CUH cluster connectivity, resolving the jumpbox VM name, and validating Azure bastion SSH access.

---

## Asset 1 (Pieces: 1ce0fe65-de4f-422a-9e9f-3dfbcb1985fa)—12:48:36 (Most Complete sUmmary)

### Summary

User corrected the worker's previous mix-up of NNUH environment details with the CUH cluster (`aks-ff-uks-gp-01`) and provided the correct Azure AKS resource JSON for CUH.

### Open Questions / Loose Ends

- What is the exact tenant ID for the CUH Foundation Trust (`cuhfoundationtrust.onmicrosoft.com` or subscription `709f3d57-b6d7-48c6-8252-6b1c1174a541`) to login cleanly via `az login`?
- Confirm the actual name of the Bastion host (implied `bas-ff-uks-gp` from the `rg-ff-uks-gp-net` configuration) used to tunnel into the CUH jumpbox.

### Confirmed Facts

- CUH Cluster ID: `/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.ContainerService/managedClusters/aks-ff-uks-gp-01`
- Client Identity (UserAssigned): `uai-ff-uks-gp-aks` (clientId: `6120d87f-85d8-4768-adfe-af8d540d4018` / principalId: `0eb04d09-5d1b-4ee9-98ae-17742560e807`)
- System Subnet ID: `/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Network/virtualNetworks/vnet-ff-uks-gp-01/subnets/snet-ff-uks-gp-system`
- Private DNS Endpoint: `aks-ff-uks-gp-01-igmjlo7k.303e6cfc-b5ff-47c7-93cc-517c8ce1a9aa.privatelink.uksouth.azmk8s.io`
- Cluster Node Resource Group: `rg-ff-uks-gp-aks`
- Local Proxy Config: `http://10.252.142.180:8080/` used heavily for cluster-wide outbound proxy exceptions.
- Jumpbox Deployment Script: `/Users/leon.ormes/Documents/LeonLM/00_Inbox/JUMPBOX_DEPLOYMENT.md`
- Bastion Configuration and Network Notes: `/Users/leon.ormes/Documents/LeonLM/20_Thinking/21_Workbench/Understanding NAT Gateways.md`

### CUH Bastion SSH Command

```sh
az network bastion ssh \
  --name bas-ff-uks-gp \
  --resource-group rg-ff-uks-gp-net \
  --target-resource-id $VM_ID \
  --auth-type password \
  --username azadmin \
  -- -o PubkeyAuthentication=no -o PreferredAuthentications=password
```

Once connected to jumpbox, fetch credentials: `az aks get-credentials --resource-group rg-ff-uks-gp-aks --name aks-ff-uks-gp-01 --subscription 709f3d57-b6d7-48c6-8252-6b1c1174a541`

### Jumpbox VM name Resolved

The virtual machine's resource name on the CUH platform is `FITFILEJumpbox` (not `vm-ff-uks-gp-jumpbox`). NIC: `FITFILEJumpboxNic`. The `az vm show` command with `vm-ff-uks-gp-jumpbox` returned ResourceNotFound; corrected to `FITFILEJumpbox`.

### Tenant ID Confirmed

Azure tenant ID: `4ae8fd93-d084-481f-ba6e-370b7d4d8d0d` / `cuhfoundationtrust.onmicrosoft.com`

### Previous Run Error

Terraform apply-run `run-VsHz6gWZmEyW3MzJ` on workspace `cuh-poc-1` errored due to overlapping subnet configurations during `azurerm_subnet private_endpoint` deployment.

---

## Asset 2 (Pieces: b3535217-9689-4610-a7d6-41ee8015db46)—12:47:38

Same session, earlier compaction. Same facts as above. No new unique information beyond Asset 1.

---

## Asset 3 (Pieces: fc65fdb8-0b73-4320-924f-9a62f9d291fe)—12:46:34

Same session, earlier compaction. Same facts. Worker had validated CUH private DNS setup and virtual network link context using naming conventions from Obsidian.

---

## Asset 4 (Pieces: 8809d6de-e144-4517-9558-1749cf2742f3)—12:45:14

Same session, earlier compaction. Same facts. Worker validated subnet allocations and resource group divisions in `cuh-poc-1` workspace.

---

## Asset 5 (Pieces: d90eaf20-0e8c-4975-96a2-6d4829e2e45b)—12:44:39

Same session, earliest compaction. Contains the initial confirmed facts before the jumpbox name resolution.
