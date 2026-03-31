---
created: 2026-03-30T11:54:16+00:00
modified: 2026-03-30T16:55:05+00:00
title: LCRCA
---

```sh
az network bastion ssh \
  --name vnet-fflz-uks-01-bastion \
  --resource-group rg-lca-uks-prd-net \
  --target-resource-id /subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/rg-lca-uks-prd-net/providers/Microsoft.Compute/virtualMachines/vmlcajmp01 \
  --auth-type password \
  --username azadmin \
  -- -o PubkeyAuthentication=no -o PreferredAuthentications=password
```
