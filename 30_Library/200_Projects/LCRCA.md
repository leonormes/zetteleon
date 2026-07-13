---
created: 2026-03-30T11:54:16+00:00
modified: 2026-07-13T08:52:11+00:00
permalink: llmeon/30-library/200-projects/lcrca
project_category: deployments
project_name: Deployments
project_status: active
title: LCRCA
type: null
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

open tunnel for rdp app on mac

```sh
az network bastion tunnel \
  --name vnet-fflz-uks-01-bastion \
  --resource-group rg-lca-uks-prd-net \
  --target-resource-id /subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/rg-lca-uks-prd-net/providers/Microsoft.Compute/virtualMachines/vmlcajmp01 \
  --resource-port 3389 \
  --port 50022
```
