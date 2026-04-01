---
created: 2026-03-30T08:34:15+00:00
modified: 2026-04-01T10:09:02+00:00
title: NWSDE
---

tenant ID: `eae2146b-01ed-4b70-8a27-caa5804ab9ca`

```sh
az logout
az login --tenant "eae2146b-01ed-4b70-8a27-caa5804ab9ca"
```
Tunnel
```sh
az network bastion tunnel --name bas-ff-ukw-gp --resource-group DSC-RLZ-RG-Services-FITFILE --target-resource-id /subscriptions/bd15b86f-5159-4021-8ba0-f912e79a0085/resourceGroups/DSC-RLZ-RG-Services-FITFILE/providers/Microsoft.Compute/virtualMachines/vm-ff-ukw-gp-jumpbox --resource-port 3389 --port 50022
```
ssh
```sh
az network bastion ssh --name bas-ff-ukw-gp --resource-group DSC-RLZ-RG-Services-FITFILE --target-resource-id /subscriptions/bd15b86f-5159-4021-8ba0-f912e79a0085/resourceGroups/DSC-RLZ-RG-Services-FITFILE/providers/Microsoft.Compute/virtualMachines/vm-ff-ukw-gp-jumpbox --auth-type password --username azadmin -- -o PubkeyAuthentication=no -o PreferredAuthentications=password
```
