---
created: 2026-05-27T00:00:00+00:00
modified: 2026-07-20T16:33:00+00:00
permalink: llmeon/raw/2026-05-27-pieces-terraform-aks-upgrade-override
pieces_ids: [2786291a-0ade-44d1-9531-2807a745b29b, 34d03caa-8e79-4696-9bcf-a0abdb38a587, 4f80d935-1bc0-44ea-b0e0-3e1c24a07f8d, 804011cd-efc2-4983-afaf-c59320dcff4b, 8aedc7fd-869c-49d7-8513-a8fffe34bf09, 9d404c67-1e0d-407a-a7ae-9a57b0109194]
source: pieces-ltm
tags: [aks, fitfile, pieces, raw, terraform]
title: 2026-05-27-pieces-terraform-aks-upgrade-override
---

## Terraform AKS upgrade_override Fix—FITFILE Testing Cluster

### Asset 1 (Pieces: 34d03caa-8e79-4696-9bcf-a0abdb38a587)

Captured: 2026-05-27T12:07:20Z

> give me a hermes prompt to fix with option 1

### Asset 2 (Pieces: 4f80d935-1bc0-44ea-b0e0-3e1c24a07f8d)

Captured: 2026-05-27T12:06:22Z

Now I have the full log. Here's the complete diagnosis.

### Terraform Apply Failure—Diagnosis & Fix

#### The Error

```
Error: `upgrade_override` cannot be unset
  on .terraform/modules/azure_public_infrastructure/main.tf, line 8, column 46
  resource "azurerm_kubernetes_cluster" "main"
```

Resource: `module.azure_public_infrastructure.azurerm_kubernetes_cluster.main`

#### What's Happening

This is a provider-state conflict, not a code bug. The AKS cluster currently has `upgrade_override` set in Azure state, but the Terraform config doesn't declare it. The Azure provider refuses to let you "unset" a value that's present in the real resource.

#### Fix Option 1—Add Explicit `upgrade_settings` Block

```text
/goal Fix `upgrade_override` Terraform azurerm_kubernetes_cluster upgrade_override error
```

### Asset 3 (Pieces: 804011cd-efc2-4983-afaf-c59320dcff4b)

Captured: 2026-05-27T12:05:17Z

AKS cluster API response:

```json
{
    "apiVersion": "2026-03-01",
    "id": "/subscriptions/249df46b-f75d-4492-8e78-b33a00473548/resourceGroups/fitfile-cloud-testing-rg/providers/Microsoft.ContainerService/managedClusters/fitfile-cloud-testing-aks-cluster",
    "name": "file-cloud-testing-aks-cluster",
    "sku": {
        "name": "Base",
        "tier": "Free"
    },
    "location": "uksouth",
    "tags": {
        "BillTo": "FITFILE"
    }
}
```

### Asset 4 (Pieces: 8aedc7fd-869c-49d7-8513-a8fffe34bf09)

Captured: 2026-05-27T12:13:23Z

Memory search confirmed: no pre-existing Hermes `/goal` prompt in LTM specifically for the `upgrade_override` Terraform fix.

Here is the Hermes `/goal` prompt to fix Terraform `upgrade_override` error (Option 1—add explicit `upgrade_settings` block):

```text
/goal Fix `upgrade_override` cannot be unset
```

### Asset 5 (Pieces: 2786291a-0ade-44d1-9531-2807a745b29b)

Captured: 2026-05-27T12:12:35Z

All memory pages confirmed consistent—no conflicting "option 1" definition. You haven't done this fix before.

### Asset 6 (Pieces: 9d404c67-1e0d-407a-a7ae-9a57b0109194)

Captured: 2026-05-27T12:11:48Z

Hermes `/goal` Prompt—Fix `upgrade_override` Terraform Error

Paste this directly into `hermes --tui` (including the leading `/goal`):

```text
/goal Fix Terraform azurerm_kubernetes_cluster upgrade_override error

# Context

A `terraform apply` against the FITFILE testing AKS
```
