---
aliases: []
confidence:
created: 2025-11-20T11:23:03Z
epistemic:
last_reviewed:
modified: 2025-11-20T12:26:16Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [nnuh]
title: NNUH Alignment with Plan
type:
uid:
updated:
---

I'll re-analyze the current config with the updated NAT Gateway–centric requirements, then outline gaps and a clean change plan. First I'll briefly inspect the module's route table behavior and search for NAT Gateway usage so the recommendations are accurate.

## PHASE 1: CURRENT STATE ANALYSIS

### 1. Files & Structure (NNUH-DP workspace)

Terraform files:

- **Core**: [main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/main.tf:0:0-0:0), [locals.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/locals.tf:0:0-0:0), [variables.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/variables.tf:0:0-0:0), [terraform.tfvars](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/terraform.tfvars:0:0-0:0), [providers.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/providers.tf:0:0-0:0), [versions.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/versions.tf:0:0-0:0)
- **Support**: [data.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/data.tf:0:0-0:0), [outputs.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/outputs.tf:0:0-0:0), [README.md](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/README.md:0:0-0:0), [.terraform](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/.terraform:0:0-0:0) (module cache)

### 2. What the `private-infrastructure` Module is Doing

Module call (simplified):

```hcl
module "private-infrastructure" {
  source  = "app.terraform.io/FITFILE-Platforms/private-infrastructure/azure"
  version = "1.3.0"

  create_vnet              = false
  vnet_resource_group_name = "NNUHFT-SDE-Networking"
  vnet_name                = "NNUHFT-SDE-vnet1"

  deployment_key     = "nnuh-prod"
  admin_password     = var.admin_password
  vm_size            = "Standard_D2s_v3"
  kubernetes_version = var.kubernetes_version
  location           = local.location

  default_node_pool_subnet_address_prefix    = local.default_node_pool_subnet_address_prefix
  additional_node_pool_subnet_address_prefix = local.additional_node_pool_subnet_address_prefix
  vm_subnet_address_prefix                   = local.vm_subnet_address_prefix
  default_node_pool_max_count                = local.default_node_pool_max_count
  additional_node_pool_max_count             = local.additional_node_pool_max_count

  network_policy      = "calico"
  network_plugin_mode = "overlay"
  pod_cidr            = "10.244.0.0/16"

  # You have now added:
  # firewall_existing_private_ip = local.firewall_private_ip

  default_node_pool_enable_node_public_ip = false

  workload   = local.workload  # "ff"
  region     = local.region    # "uks"
  env_prefix = local.env_prefix # "gp"

  ingress_controller_ip_address = "192.168.200.36"
  private_dns_zone_enabled      = false
}
```

Local networking:

```hcl
locals {
  workload   = "ff"
  region     = "uks"
  env_prefix = "gp"

  vnet_address_space = "192.168.200.0/24"

  default_node_pool_subnet_address_prefix    = [cidrsubnet(local.vnet_address_space, 4, 2)] # 192.168.200.64/28
  additional_node_pool_subnet_address_prefix = [cidrsubnet(local.vnet_address_space, 4, 3)] # 192.168.200.80/28
  vm_subnet_address_prefix                   = [cidrsubnet(local.vnet_address_space, 5, 8)] # 192.168.200.128/29

  firewall_private_ip = "192.168.208.4" # Hub firewall
  location            = "uksouth"
}
```

#### Network Resources (via Module code)

From [terraform-azure-private-infrastructure](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/TFC-Modules/terraform-azure-private-infrastructure:0:0-0:0):

- **VNet**:
  - Uses **existing** `NNUHFT-SDE-vnet1` in RG `NNUHFT-SDE-Networking` (`create_vnet=false`).
- **Subnets created** (inside existing VNet):
  - `snet-ff-uks-gp-system` → `192.168.200.64/28`
  - `snet-ff-uks-gp-workflows` → `192.168.200.80/28`
  - `snet-ff-uks-gp-jumpbox` → `192.168.200.128/29`
- **Route table behavior (module)**:

  ```hcl
  # networking.tf in module
  locals {
    create_route_table = var.firewall_existing_private_ip != null
  }

  module "routetable" {
    count    = local.create_route_table ? 1 : 0
    source   = "./modules/route_table"
    # ...
    firewall_private_ip = var.hub_deploy ? module.firewall[0].private_ip_address : var.firewall_existing_private_ip
    subnets_to_associate = { ... system/workflows/jumpbox ... }
  }
  ```

  And [modules/route_table/main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/TFC-Modules/terraform-azure-private-infrastructure/modules/route_table/main.tf:0:0-0:0):

  ```hcl
  resource "azurerm_route_table" "rt" {
    route {
      name                   = "kubenetfw_fw_r"
      address_prefix         = "0.0.0.0/0"
      next_hop_type          = "VirtualAppliance"
      next_hop_in_ip_address = var.firewall_private_ip
    }
  }
  ```

  **Implication**:  
  - When `firewall_existing_private_ip` is **non-null**, a route table with **0.0.0.0/0 → firewall (192.168.208.4)** will be created and associated to **all 3 subnets**.

#### NAT Gateway

- In this workspace and module:
  - **No** `azurerm_nat_gateway` resources.
  - **No** `azurerm_subnet_nat_gateway_association`.
  - **No data source** for NNUHFT-SDE-nat.
- NAT Gateway `NNUHFT-SDE-nat` with IP `20.162.236.86` currently exists only **outside** this Terraform configuration.

#### AKS Cluster Configuration (via [modules/aks/main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/TFC-Modules/terraform-azure-private-infrastructure/modules/aks/main.tf:0:0-0:0))

- Private AKS cluster:
  - `private_cluster_enabled = true`
  - CNI: `network_plugin = azure`
  - Overlay: `network_plugin_mode = var.network_plugin_mode` → `"overlay"`
  - Network policy: `calico`
- Node pools:
  - Default/system: size & scaling controlled by module vars (derived from locals in NNUH-DP).
  - Additional `workflows` node pool: Spot, separate subnet.
- Egress mode (from root module):

```hcl
outbound_type = var.hub_deploy || var.firewall_existing_private_ip != null
? "userDefinedRouting"
: var.aks_cluster_outbound_type
```

  Current NNUH-DP:

  - `hub_deploy` default: `false`
  - `aks_cluster_outbound_type` default: `"loadBalancer"`
  - **But** you now set `firewall_existing_private_ip = local.firewall_private_ip`, so:
    - `outbound_type` will be `"userDefinedRouting"`
    - Combined with route table 0.0.0.0/0 → firewall.

#### Compute Resources

- Jumpbox VM (module [jumpbox.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/TFC-Modules/terraform-azure-private-infrastructure/jumpbox.tf:0:0-0:0)):

```hcl
module "FITFILEJumpbox" {
source            = "./modules/virtual_machine"
name              = var.vm_name
size              = var.vm_size
public_ip         = var.vm_public_ip  # default false
subnet_id         = module.aks_network.subnet_ids["snet-ff-uks-gp-jumpbox"]
admin_password    = var.admin_password
# NSG attached at NIC level in VM module
}
```

- **No Bastion** module instantiation, though the module has a [bastion_host](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/TFC-Modules/terraform-azure-private-infrastructure/modules/bastion_host:0:0-0:0) submodule available.

#### DNS Resources

- In [main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/main.tf:0:0-0:0): `private_dns_zone_enabled = false`
- Module networking has logic for a private DNS zone, but this flag disables it.
- No additional DNS resources in NNUH-DP workspace.

#### Security & Identity

- User-assigned identity for AKS created in module.
- Role Assignment in [modules/aks/main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/TFC-Modules/terraform-azure-private-infrastructure/modules/aks/main.tf:0:0-0:0):

```hcl
resource "azurerm_role_assignment" "cluster_network_contributor" {
scope                = var.resource_group_id
role_definition_name = "Network Contributor"
principal_id         = azurerm_user_assigned_identity.aks_identity.principal_id
}
```

- No ACR role (`AcrPull`) configured here.
- NSGs:
  - Per-VM NSG for Jumpbox (inside virtual_machine module).
  - No explicit NSGs per-subnet for AKS in this workspace.

#### Monitoring / Observability

- No explicit Log Analytics / Monitor resources in this NNUH-DP layer.  
  (Firewall module in `.terraform/modules/private-infrastructure.firewall` contains outbound rules for Azure monitor endpoints, but that’s outside your current NNUH-DP config.)

---

## PHASE 2: GAP ANALYSIS (Against NAT Gateway–centric Design)

### High-level Summary

- **VNet + subnets**: Correct (System, Workflows, Jumpbox).
- **AKS networking mode**: Correct (Azure CNI Overlay, Calico).
- **Egress**: Currently being changed towards **firewall UDR 0.0.0.0/0**, which **conflicts** with new requirement “egress via NAT Gateway”.
- **NAT Gateway & associations**: Not referenced at all.
- **Ingress via hub firewall**: VNet peering exists out-of-band, but not validated or complemented by specific on-prem routes in Terraform.
- **Bastion**: Not deployed.
- **NSGs**: No hardened subnet-level NSGs.
- **DNS**: No private DNS zones / records.

### Gap Table (condensed)

| Area | Requirement | Current | Status |
|------|-------------|---------|--------|
| VNet reuse | Use existing `NNUHFT-SDE-vnet1` | Done via `create_vnet = false` | ✅ |
| Subnets | System/Workflows/Jumpbox CIDRs | Exactly as required | ✅ |
| AzureBastionSubnet | /26 (e.g. 192.168.200.192/26) | Not defined | ❌ |
| NAT Gateway | Use existing `NNUHFT-SDE-nat` for outbound | No data source or associations | ❌ |
| Egress strategy | Outbound via NAT, NO 0.0.0.0/0 → firewall | Newly added `firewall_existing_private_ip` will create 0.0.0.0/0 UDR and `userDefinedRouting` | 🔧 **Must remove** |
| Inbound routing | Specific on-prem CIDRs → firewall | No route table under NNUH-DP | ❌ |
| AKS cluster | Private, no node public IPs, overlay, Calico | All configured | ✅ |
| AKS version | Supported 1.30.x in UK South | Hardcoded 1.33.5 | ⚠️ (needs validation/change) |
| Bastion | Azure Bastion in AzureBastionSubnet | Not present | ❌ |
| Jumpbox | No public IP, only via Bastion | Public IP disabled, but no Bastion yet | ⚠️ |
| NSGs | Hardened per subnet | Only VM-level NSG | ❌ |
| Role assignments | Network Contributor (done), AcrPull, DNS Contributor, NAT Reader | Only Network Contributor | ⚠️ |
| DNS | Private zones for nnuh-prod-1.fitfile.net, AKS API | All disabled | ❌ |

---

## PHASE 3: REQUIRED CHANGES

### Critical Changes (Must Fix)

#### 1. **Revert Firewall-based Default route**

**Issue**: The line you just added:

```hcl
firewall_existing_private_ip = local.firewall_private_ip
```

will:

- Create `0.0.0.0/0 → 192.168.208.4` on all three subnets.
- Force AKS `outbound_type = "userDefinedRouting"`.
- **Override NAT Gateway egress**, violating the design.

**Action**:

- **Remove** that line from `module "private-infrastructure"` in [main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/main.tf:0:0-0:0).

After removal:

- `firewall_existing_private_ip = null` (default).
- Module **does not** create route table or UDR.
- AKS outbound_type falls back to `aks_cluster_outbound_type` (default `"loadBalancer"`), which is compatible with NAT Gateway on the subnets.

#### 2. **Associate Existing NAT Gateway to AKS + Jumpbox subnets**

Add to [data.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/data.tf:0:0-0:0):

```hcl
data "azurerm_nat_gateway" "sde_nat" {
  name                = "NNUHFT-SDE-nat"
  resource_group_name = "NNUHFT-SDE-Networking"
}

data "azurerm_subnet" "system" {
  name                 = "snet-ff-uks-gp-system"
  virtual_network_name = "NNUHFT-SDE-vnet1"
  resource_group_name  = "NNUHFT-SDE-Networking"
}

data "azurerm_subnet" "workflows" {
  name                 = "snet-ff-uks-gp-workflows"
  virtual_network_name = "NNUHFT-SDE-vnet1"
  resource_group_name  = "NNUHFT-SDE-Networking"
}

data "azurerm_subnet" "jumpbox" {
  name                 = "snet-ff-uks-gp-jumpbox"
  virtual_network_name = "NNUHFT-SDE-vnet1"
  resource_group_name  = "NNUHFT-SDE-Networking"
}
```

Add a new file `nat_gateway.tf` (or similar):

```hcl
resource "azurerm_subnet_nat_gateway_association" "system" {
  subnet_id      = data.azurerm_subnet.system.id
  nat_gateway_id = data.azurerm_nat_gateway.sde_nat.id
}

resource "azurerm_subnet_nat_gateway_association" "workflows" {
  subnet_id      = data.azurerm_subnet.workflows.id
  nat_gateway_id = data.azurerm_nat_gateway.sde_nat.id
}

resource "azurerm_subnet_nat_gateway_association" "jumpbox" {
  subnet_id      = data.azurerm_subnet.jumpbox.id
  nat_gateway_id = data.azurerm_nat_gateway.sde_nat.id
}
```

**Result**:

- Outbound Internet from all three subnets uses NAT Gateway.
- Static public IP: **20.162.236.86** for allowlisting.

#### 3. **Add Route Table for Inbound On-prem Traffic only**

Create `routing.tf`:

```hcl
variable "onprem_cidrs" {
  description = "On-prem CIDRs that should route via NNUH hub firewall"
  type        = list(string)
  default     = [] # e.g. ["10.0.0.0/8"] – to be provided by NNUH
}

resource "azurerm_route_table" "aks_inbound" {
  name                = "rt-ff-uks-gp-aks"
  location            = local.location
  resource_group_name = "NNUHFT-SDE-Networking"

  dynamic "route" {
    for_each = var.onprem_cidrs
    content {
      name                   = "onprem-${replace(route.value, "/", "-")}"
      address_prefix         = route.value
      next_hop_type          = "VirtualAppliance"
      next_hop_in_ip_address = local.firewall_private_ip # 192.168.208.4
    }
  }
}

resource "azurerm_subnet_route_table_association" "system" {
  subnet_id      = data.azurerm_subnet.system.id
  route_table_id = azurerm_route_table.aks_inbound.id
}

resource "azurerm_subnet_route_table_association" "workflows" {
  subnet_id      = data.azurerm_subnet.workflows.id
  route_table_id = azurerm_route_table.aks_inbound.id
}

resource "azurerm_subnet_route_table_association" "jumpbox" {
  subnet_id      = data.azurerm_subnet.jumpbox.id
  route_table_id = azurerm_route_table.aks_inbound.id
}
```

**Key point**:  
- **No 0.0.0.0/0 route** is created here.  
- Only specific on-prem CIDRs go via firewall; everything else uses system routes + NAT Gateway.

#### 4. **AKS version**

In [terraform.tfvars](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/terraform.tfvars:0:0-0:0):

- Replace `1.33.5` with a supported version (after checking via `az aks get-versions`):

```hcl
kubernetes_version = "1.30.x" # e.g. "1.30.7" – pick supported value for uksouth
```

---

### Important Changes (Should Fix)

#### 5. Azure Bastion

- Create **AzureBastionSubnet** in `NNUHFT-SDE-vnet1` (data plane RG).
- Deploy `azurerm_bastion_host` in a **FITFILE RG** (module’s RG or a shared RG).

Skeleton (as discussed earlier; you can keep it light and we can refine later):

- [locals.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/locals.tf:0:0-0:0): add `bastion_subnet_address_prefix = ["192.168.200.192/26"]` (or via `cidrsubnet`).
- `bastion.tf`: create `azurerm_subnet` + `azurerm_public_ip` + `azurerm_bastion_host`.

#### 6. Hardened NSGs

- New NSGs for:
  - system subnet
  - workflows subnet
  - jumpbox subnet
- Rules:
  - Inbound:
    - Allow from Bastion subnet → Jumpbox (3389/22).
    - Allow from on-prem CIDRs (via hub firewall IP ranges) as required.
    - Allow Azure LB probes.
    - Deny all other inbound.
  - Outbound:
    - Allow all (egress control handled by firewall + NAT), or refine further later.

#### 7. RBAC

- Add ACR `AcrPull` when ACR ID known.
- Add Private DNS Zone Contributor if you manage private DNS.
- Reader on NAT Gateway if desired (not strictly required).

---

### Recommended Enhancements (Nice to Have)

- Data sources for:
  - VNet peering to hub (for validation only).
  - Existing public IP of NAT Gateway (useful in outputs).
- Private DNS zones for:
  - `nnuh-prod-1.fitfile.net` (or a private subdomain).
  - AKS private FQDN zone if you choose BYO DNS instead of AKS-managed.

---

## PHASE 4: IMPLEMENTATION PLAN

1. **Undo firewall UDR**  
   - Remove `firewall_existing_private_ip` line from [main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/main.tf:0:0-0:0).
   - `terraform plan` and confirm the module’s route table is **removed or not created**.

2. **Introduce NAT Gateway associations**  
   - Add data sources for NAT & subnets ([data.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/data.tf:0:0-0:0)).
   - Add `nat_gateway.tf` with `azurerm_subnet_nat_gateway_association` resources.
   - `terraform plan` and confirm associations only (no NAT creation).

3. **Add inbound route table**  
   - Add `routing.tf` with `azurerm_route_table` and `azurerm_subnet_route_table_association`.
   - Start with placeholder `onprem_cidrs = []` until NNUH supplies ranges.
   - `terraform plan` – ensure no 0.0.0.0/0 route.

4. **Update Kubernetes version**  
   - Check supported versions, update [terraform.tfvars](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/terraform.tfvars:0:0-0:0).

5. **Add Bastion**  
   - Add Bastion subnet & host.
   - Plan carefully – check if AzureBastionSubnet already exists before applying.

6. **Add NSGs**  
   - Introduce NSGs and associations.
   - Validate they don’t break required traffic (plan + small tests).

7. **Add RBAC & DNS** later once core networking is stable.

---

## PHASE 5: VALIDATION CHECKLIST

**Terraform Plan**

- No creation of `azurerm_route_table` with `address_prefix = "0.0.0.0/0"` in this workspace.
- New `azurerm_subnet_nat_gateway_association` for:
  - `snet-ff-uks-gp-system`
  - `snet-ff-uks-gp-workflows`
  - `snet-ff-uks-gp-jumpbox`
- New `azurerm_route_table` with **only** on-prem CIDR routes (when configured).
- No replacement of existing critical resources (AKS, VNet).

**Runtime / Connectivity**

- From Jumpbox (via Bastion):
  - `curl ifconfig.me` → should return `20.162.236.86`.
- From on-prem (once routes configured):
  - Can reach AKS ingress IP `192.168.200.36`.
- AKS:
  - Can pull images from ACR.
  - Can reach Auth0, Cloudflare, Vault, Grafana via outbound NAT.

---

If you’d like, next step I can generate **full updated files** ([main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/main.tf:0:0-0:0), [data.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/data.tf:0:0-0:0), `nat_gateway.tf`, `routing.tf`, etc.) following your “follow-up prompt” format, with comments explaining NAT vs firewall routing.
