---
created: 2025-12-04T12:02:41+00:00
last_reviewed: null
modified: 2026-07-13T08:53:02+00:00
permalink: llmeon/30-library/ops/protocol-az-bastion-create-standard
status: processing
tags: [bastion, customer/lcrca, ssh]
title: protocol-az-bastion-create-standard
type: protocol
updated: null
---

## 1. Create the Standard Bastion

This uses the dedicated `create` command which is much more robust at mapping the networking requirements. This is LCRCA

```sh
az logout
az login --tenant "dbb3517b-09e6-4a76-9aa9-d7d72b1073e7"
```

```sh
az network bastion create --name vnet-lca-plat-uks-01-bastion --resource-group rg-lca-uks-prd-net --vnet-name vnet-lca-plat-uks-01 --public-ip-address bastion-lca-plat-uks-01PublicIp --sku Standard --enable-tunneling
```

---

## Verification & SSH

Once the creation completes (approx. 5-10 mins), you can immediately run your original command:

```sh
az network bastion ssh \
  --name vnet-fflz-uks-01-bastion \
  --resource-group rg-lca-uks-prd-net \
  --target-resource-id /subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/rg-lca-uks-prd-net/providers/Microsoft.Compute/virtualMachines/vmlcajmp01 \
  --auth-type password \
  --username azadmin \
  -- -o PubkeyAuthentication=no -o PreferredAuthentications=password
```
