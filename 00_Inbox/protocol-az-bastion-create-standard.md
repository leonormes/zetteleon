---
created: 2025-12-04T12:02:41Z
last_reviewed:
modified: 2026-02-23T12:18:36+00:00
status: processing
tags: [bastion, customer/lcrca, ssh]
title: protocol-az-bastion-create-standard
type: protocol
updated:
---

## Context

- VNet: `vnet-fflz-uks-01` in `rg-vnet-fflz-01` (`10.200.80.0/24`)
- Jumpbox: `vmlcajmp01` in `rg-lca-uks-prd-net` (subnet `snet-lca-uks-prd-jumpbox`, `10.200.80.128/27`)
- Bastion requirement: A subnet named exactly `AzureBastionSubnet` (minimum `/26`) must exist in the target VNet.
- Cross-RG note: The Bastion host lives in `rg-lca-uks-prd-net` but the VNet is in `rg-vnet-fflz-01`, so the full resource ID is required for `--vnet-name`.

### Address Space Map

| Subnet                       | CIDR                 | Purpose                    |
|------------------------------|----------------------|----------------------------|
| `snet-lca-uks-prd-system`   | `10.200.80.0/26`     | AKS system + API server PE |
| `snet-lca-uks-prd-workflows`| `10.200.80.64/26`    | AKS workflows              |
| `snet-lca-uks-prd-jumpbox`  | `10.200.80.128/27`   | Jumpbox VM                 |
| _(unused)_                   | `10.200.80.160/27`   | Available                  |
| `AzureBastionSubnet`         | `10.200.80.192/26`   | Bastion (this protocol)|

---

## 1. Create the Public IP for Bastion

Azure Bastion requires a Standard SKU public IP with static allocation.

```sh
az network public-ip create \
  --name bastion-lca-plat-uks-01PublicIp \
  --resource-group rg-lca-uks-prd-net \
  --location uksouth \
  --sku Standard \
  --allocation-method Static
```

---

## 2. Create the AzureBastionSubnet

The subnet must be named exactly `AzureBastionSubnet`—Azure will reject any other name. Minimum size is `/26`.

```sh
az network vnet subnet create \
  --name AzureBastionSubnet \
  --resource-group rg-vnet-fflz-01 \
  --vnet-name vnet-fflz-uks-01 \
  --address-prefixes 10.200.80.192/26
```

---

## 3. Create the Standard Bastion

Uses the full VNet resource ID because the Bastion host (`rg-lca-uks-prd-net`) and VNet (`rg-vnet-fflz-01`) are in different resource groups.

```sh
az network bastion create \
  --name vnet-fflz-uks-01-bastion \
  --resource-group rg-lca-uks-prd-net \
  --vnet-name /subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/rg-vnet-fflz-01/providers/Microsoft.Network/virtualNetworks/vnet-fflz-uks-01 \
  --public-ip-address bastion-lca-plat-uks-01PublicIp \
  --sku Standard \
  --enable-tunneling
```

Approx. 5–10 minutes to provision.

---

## 4. Verification & SSH

Once the creation completes, connect to the jumpbox:

```sh
az network bastion ssh \
  --name vnet-fflz-uks-01-bastion \
  --resource-group rg-lca-uks-prd-net \
  --target-resource-id /subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-LCA-UKS-PRD-NET/providers/Microsoft.Compute/virtualMachines/vmlcajmp01 \
  --auth-type password \
  --username azadmin \
  -- -o PubkeyAuthentication=no -o PreferredAuthentications=password
```

---

## Teardown

To remove the Bastion (e.g. to save costs when not in use):

```sh
az network bastion delete \
  --name vnet-fflz-uks-01-bastion \
  --resource-group rg-lca-uks-prd-net

az network public-ip delete \
  --name bastion-lca-plat-uks-01PublicIp \
  --resource-group rg-lca-uks-prd-net
```

Note: The `AzureBastionSubnet` can be left in place—it costs nothing without a Bastion host attached.
