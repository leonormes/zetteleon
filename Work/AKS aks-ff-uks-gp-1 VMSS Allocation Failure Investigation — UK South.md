---
author: Claude (read-only investigation)
created: 2026-07-09T10:17:37+00:00
date: 2026-07-09
modified: 2026-07-09T10:17:37+00:00
permalink: llmeon/work/aks-ff-uks-gp-1-vmss-allocation-failure-uk-south
related_ticket:
status: Investigation complete — no fix applied
tags: [azure, aks, vmss, allocation-failure, uksouth, capacity, incident]
title: AKS aks-ff-uks-gp-1 VMSS Allocation Failure Investigation — UK South
---

## AKS `aks-ff-uks-gp-1` — VMSS Allocation Failure Investigation (UK South)

> Scope: read-only investigation into why all 4 node pools on `aks-ff-uks-gp-1` (subscription `7bbc8ae5-1710-48ab-ab83-59b52bd0de1a`, resource group `rg-ff-uks-gp-net`) are stuck in Failed provisioning state with `OverconstrainedAllocationRequest`. No fixes, SKU changes, or config edits were made — investigation and reporting only, per instruction.

### Verdict

Root cause is **(b) genuine capacity constraint**, not quota, not a subscription restriction, and not a zone-pinning conflict. Every "hard gate" checked came back clean — quota usage across the relevant families sits at 0–20% of limit (2.2% of total regional vCPU quota), all four affected SKUs report zero restriction entries, and there is no subscription-level block. What's left is Azure's own `OverconstrainedAllocationRequest` signal — the control plane's language for "no physical hosts currently match this combination of VM size + accelerated networking in the target region/zones." Two corroborating signals: the AMD "as"/"ads" (premium-storage-capable) family only exists at **v7 generation** in UK South for this subscription — there's no v5/v6 AMD fallback offered here at all, consistent with a newly-released hardware generation still ramping capacity — and all four affected SKUs are stocked in only 2 of the 3 UK South zones (1 and 3), narrowing the physical rack pool further.

---

### 1. Quota Check

| Family | SKUs covered | Current | Limit | Usage % |
|---|---|---|---|---|
| Standard Dasv7 | D2as_v7, D4as_v7 | 0 | 10 | 0% |
| Standard Dadsv7 | D4ads_v7 | 2 | 10 | 20% |
| Standard Easv7 | E4as_v7 | 0 | 40 | 0% |
| Total Regional vCPUs | (all) | 2 | 90 | 2.2% |

**Verdict:** Quota is not the constraint — nowhere close to any limit.

### 2. SKU Availability

| SKU | Location | Zones | Restrictions |
|---|---|---|---|
| Standard_D2as_v7 | uksouth | 1, 3 | None |
| Standard_D4as_v7 | uksouth | 1, 3 | None |
| Standard_E4as_v7 | uksouth | 1, 3 | None |
| Standard_D4ads_v7 | uksouth | 1, 3 | None |

All four SKUs are listed as available for this subscription, no restriction flags.

### 3. Zone-Level Availability

All four SKUs are available **only in zones 1 and 3** in UK South (not zone 2) — consistent across the whole family, not SKU-specific.

### 4. Restrictions

`az vm list-skus ... --query "[].restrictions"` returned `[]` (empty) for all four SKUs — no `NotAvailableForSubscription`, no `SubscriptionCapacity` reason codes.

### 5. Activity Log (last 48h)

One failure recorded:

| Field | Value |
|---|---|
| Time | 2026-07-09T07:30:24.68Z |
| Operation | `Microsoft.ContainerService/managedClusters/write` |
| Correlation ID | `22386bc4-6bf4-4def-9be1-48de4dcce141` |
| Target VMSS | `aks-system-22181708-vmss` |
| Node resource group | `rg-ff-uks-gp-aks` — *differs from `rg-ff-uks-gp-net`, which only holds the AKS control-plane object; the actual VMSS lives in the AKS-managed node RG* |
| Error code | `OverconstrainedAllocationRequest` |
| Message | "Allocation failed. VM(s) with the following constraints cannot be allocated... Constraints applied are: Networking Constraints (such as Accelerated Networking or IPv6); VM Size." |

Only the `system` pool's VMSS write is captured in this window — consistent with it being the first pool AKS attempts to reconcile.

### 6. AKS Node Pools

| Pool | VM Size | Count | Max | Availability Zones |
|---|---|---|---|---|
| system | Standard_D2as_v7 | 1 | 1 | null (regional, not zone-pinned) |
| omopdb | Standard_D4ads_v7 | 1 | 1 | null |
| workflows | Standard_E4as_v7 | 0 | 10 | null |
| fitfile | Standard_D4as_v7 | 0 | 1 | null |

None of the pools are zone-pinned, so there's no explicit zone-mismatch conflict — but since the SKU family itself is only stocked in 2 of 3 zones, the effective allocation pool is already narrower than a fully-available SKU would offer.

---

### Verified alternative SKUs (same class, Intel v6 generation, zero restrictions, all 3 zones)

Not a recommended fix — listed as data-verified options for a future decision (AZ retry, SKU swap, or a capacity ticket with Microsoft citing correlation ID `22386bc4-6bf4-4def-9be1-48de4dcce141`).

| Original (constrained) | Alternative | Zones | Restrictions |
|---|---|---|---|
| Standard_D2as_v7 (system) | Standard_D2ns_v6 | 1, 2, 3 | None |
| Standard_D4as_v7 (fitfile) | Standard_D4ns_v6 | 1, 2, 3 | None |
| Standard_E4as_v7 (workflows) | Standard_E4ns_v6 | 1, 2, 3 | None |
| Standard_D4ads_v7 (omopdb, local disk) | Standard_D4nls_v6 | 1, 2, 3 | None |

---

### Commands run (read-only)

```sh
az account set --subscription 7bbc8ae5-1710-48ab-ab83-59b52bd0de1a
az vm list-usage --location uksouth --output table
az vm list-skus --location uksouth --size <SKU> --output table
az vm list-skus --location uksouth --size <SKU> --output json --query "[].locationInfo[].zones"
az vm list-skus --location uksouth --size <SKU> --output json --query "[].restrictions"
az monitor activity-log list --resource-group rg-ff-uks-gp-net --offset 48h \
  --query "[?contains(operationName.value, 'deployments') || contains(status.value, 'Failed')]"
az aks nodepool show --resource-group rg-ff-uks-gp-net --cluster-name aks-ff-uks-gp-1 \
  --name <pool> --query "{vmSize:vmSize, count:count, maxCount:maxCount, availabilityZones:availabilityZones}"
```

No cluster, VMSS, or subscription state was modified as part of this investigation.
