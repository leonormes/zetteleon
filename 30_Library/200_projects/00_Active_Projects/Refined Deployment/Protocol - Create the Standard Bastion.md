---
created: 2025-12-04T12:02:41Z
last_reviewed:
modified: 2026-02-13T10:58:23+00:00
status: processing
tags:
  - bastion
  - customer/lcrca
  - ssh
title: Create the Standard Bastion
type: protocol
updated:
---

It seems we've hit a perfect storm of version-specific quirks. The `az network bastion update` command in your version is rejecting the high-level flags (`--vnet-name`, `--public-ip-address`) when combined with `--set`, and it is failing the SKU string parser.

Since the CLI is being uncooperative with the "update" command, the most reliable way to get you connected is to delete and recreate the Bastion host. Because the Developer SKU is "IP-less" and the Standard SKU requires an IP configuration, the "update" path is clearly struggling to bridge that gap in your environment.

## The Reliable 2-Step Fix

### 1. Delete the Existing Developer Bastion

This will take about 2-3 minutes.

```sh
az network bastion delete \
  --name vnet-lca-plat-uks-01-bastion \
  --resource-group rg-lca-uks-prd-net
```

### 2. Create the Standard Bastion

This uses the dedicated `create` command which is much more robust at mapping the networking requirements.


```sh
az network bastion create \
  --name vnet-lca-plat-uks-01-bastion \
  --resource-group rg-lca-uks-prd-net \
  --vnet-name vnet-lca-plat-uks-01 \
  --public-ip-address bastion-lca-plat-uks-01PublicIp \
  --sku Standard \
  --enable-tunneling
```

---

## Why This is the Best Path forward

- Fresh Config: This ensures the `ipConfigurations` are built correctly from scratch inside the `AzureBastionSubnet`.
- Enable Tunneling: I've added the `--enable-tunneling` flag directly to the creation command so you don't have to run another update later.
- Clean Slate: It bypasses the "dict vs string" parser bug that is currently blocking the `update` command.

## Verification & SSH

Once the creation completes (approx. 5-10 mins), you can immediately run your original command:


```sh
az network bastion ssh \
  --name vnet-lca-plat-uks-01-bastion \
  --resource-group rg-lca-uks-prd-net \
  --target-resource-id /subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-LCA-UKS-PRD-NET/providers/Microsoft.Compute/virtualMachines/vmlcajmp01 \
  --auth-type password \
  --username azadmin \
  -- -o PubkeyAuthentication=no -o PreferredAuthentications=password
```

One last check: Since your environment is managed by Terraform, recreating this via CLI will cause a "Plan" mismatch later. Do you want me to provide the exact `azurerm_bastion_host` block so you can update your Terraform code instead of doing this manually?
