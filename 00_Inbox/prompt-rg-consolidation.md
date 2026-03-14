---
created: 2026-02-23T11:18:02+00:00
modified: 2026-02-23T12:18:34+00:00
title: prompt-rg-consolidation
---

## Terraform Refactor: Consolidate Resource Groups

### Objective

Consolidate two resource groups into one. Currently the networking and workload resources are split across `rg-vnet-fflz-01` and `rg-lca-uks-prd-net` in ways that cause cross-RG friction (e.g. NSGs in one RG attached to subnets in another, Bastion needing full resource IDs to reference the VNet). Merge them into a single RG.

### Constraints

- Do NOT touch `RG-CONNECTIVITY-FFLZ-01`—this is externally managed. It contains a public load balancer (`lb-fflz-uks-public-01`) and its public IP (`pip-fflz-lb-uks-public-01`). Leave all references to it intact.
- Do NOT touch `rg-lca-uks-prd-aks`—this is the AKS-managed node resource group, created automatically by AKS. Leave all references to it intact.
- The target consolidated RG name should be `rg-lca-uks-prd-net` (the workload networking RG survives, `rg-vnet-fflz-01` is absorbed).
- All resources must remain in `uksouth`.
- Preserve all existing tags on every resource.
- The AKS cluster has a private API server endpoint. The VNet has a peering to a hub VNet in a different subscription (`698610ad-eb6f-4fe5-a182-c466a8c95250`). Ensure the peering configuration is preserved.

### Current State

#### `rg-vnet-fflz-01` (TO BE ABSORBED)

These resources currently live here and must move to `rg-lca-uks-prd-net`:

| Resource | Type |
|----------|------|
| `vnet-fflz-uks-01` | Virtual Network (`10.200.80.0/24`) |
| `nat-lca-uks-prd-01` | NAT Gateway |
| `pip-nat-lca-uks-prd-01` | Public IP (for NAT gateway) |
| `nsg-default-fflz-01` | Network Security Group |
| `rt-default-fflz` | Route Table |
| `kv-fitfile-uks-01` | Key Vault |

#### `rg-lca-uks-prd-net` (TARGET—keeps Its name)

These resources already live here and stay:

| Resource | Type |
|----------|------|
| `aks-lca-uks-prd-01` | AKS Managed Cluster |
| `vmlcajmp01` | Virtual Machine (jumpbox) |
| `vmlcajmp01Nic` | Network Interface |
| `vmlcajmp01Nsg` | Network Security Group |
| `vmlcajmp01OsDisk` | OS Disk |
| `nsg-lca-uks-prd-jumpbox` | Network Security Group |
| `nsg-lca-uks-prd-system` | Network Security Group |
| `nsg-lca-uks-prd-workflows` | Network Security Group |
| `uai-lca-uks-prd-aks` | User Assigned Managed Identity |
| `privatelink.fitfile.net` | Private DNS Zone |
| `bastion-lca-plat-uks-01PublicIp` | Public IP (for Bastion) |
| `vnet-fflz-uks-01-bastion` | Bastion Host |
| `NetworkWatcher_uksouth` | Network Watcher |

#### VNet Subnet Layout (preserve exactly)

| Subnet | CIDR | Attached NSG | Notes |
|--------|------|-------------|-------|
| `snet-lca-uks-prd-system` | `10.200.80.0/26` | `nsg-lca-uks-prd-system` | AKS system pool + API server PE |
| `snet-lca-uks-prd-workflows` | `10.200.80.64/26` | `nsg-lca-uks-prd-workflows` | AKS workflows pool |
| `snet-lca-uks-prd-jumpbox` | `10.200.80.128/27` | `nsg-lca-uks-prd-jumpbox` | Jumpbox VM |
| `AzureBastionSubnet` | `10.200.80.192/26` | _(none)_ | Azure Bastion |

#### VNet Peering (preserve exactly)

- Name: `vnet-fflz-uks-01-to-vnet-hub-uks-01`
- Remote VNet: `/subscriptions/698610ad-eb6f-4fe5-a182-c466a8c95250/resourceGroups/rg-vnet-hub-uks-01/providers/Microsoft.Network/virtualNetworks/vnet-hub-uks-01`
- Settings: `allowVirtualNetworkAccess: true`, `allowForwardedTraffic: true`, `useRemoteGateways: true`

### Instructions

1. Find every `resource_group_name` reference that currently points to `rg-vnet-fflz-01` (or its resource group resource/data source) and update it to point to `rg-lca-uks-prd-net`.
2. Remove the `rg-vnet-fflz-01` resource group resource definition (e.g. `azurerm_resource_group.vnet` or similar). Do not remove any of the resources that were inside it—just re-parent them.
3. Update all cross-references. After consolidation, resources that previously used full resource IDs to reference the VNet (because of the cross-RG split) can now use simpler same-RG references. Specifically:
   - Bastion `--vnet-name` no longer needs a full resource ID
   - NSG-to-subnet associations are now same-RG
   - NAT gateway associations are now same-RG

4. Check for `depends_on` or implicit dependencies that referenced the old RG and update them.
5. Do NOT rename any resources—only change their resource group placement. Resource names stay identical.
6. Generate a `terraform state mv` script as a separate output file. For each resource moving from `rg-vnet-fflz-01` to `rg-lca-uks-prd-net`, output the corresponding `terraform state mv` command to update the state without destroying/recreating. Format:

   ```sh
   terraform state mv 'module.or.resource.old_address' 'module.or.resource.new_address'
   ```

7. Generate an import block file as an alternative to the state mv script, using Terraform 1.5+ `import` blocks for each moved resource, in case we prefer a clean state rebuild.

### Output

- Modified Terraform files with all RG references updated
- `state-mv-commands.sh`—executable script of `terraform state mv` commands
- `imports.tf`—Terraform import blocks as an alternative migration path
- Brief summary of all changes made
