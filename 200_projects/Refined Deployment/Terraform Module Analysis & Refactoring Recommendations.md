---
aliases: []
confidence:
created: 2025-11-25T09:53:41Z
epistemic:
last_reviewed:
modified: 2025-11-27T08:40:23Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [nnuh]
title: Terraform Module Analysis & Refactoring Recommendations
type:
uid:
updated:
---

## Executive Summary

The [terraform-azure-private-infrastructure](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/TFC-Modules/terraform-azure-private-infrastructure:0:0-0:0) module is a comprehensive AKS deployment module that creates private Azure Kubernetes clusters with networking, security, and jumpbox infrastructure. After analyzing the codebase against Terraform best practices, I've identified several opportunities to improve flexibility, maintainability, and reusability.

## Current Architecture

### Strengths

- ✅ Clear naming conventions with `workload-region-env_prefix` pattern
- ✅ Good use of `coalesce()` for resource name overrides
- ✅ Proper module composition with child modules
- ✅ Comprehensive variable validation
- ✅ Sensitive output handling

### Key Issues Identified

1. **❌ Excessive Variable Count (665 lines)** - 100+ individual variables create maintenance burden
2. **❌ Hardcoded Assumptions** - Single additional node pool, fixed subnet structure
3. **❌ Tight Coupling** - Module creates both infrastructure AND networking
4. **❌ Limited Flexibility** - Cannot support multiple node pools or custom subnet configurations
5. **❌ Variable Explosion** - Every AKS property exposed as individual variable (lines 3-73 in main.tf)

---

## Recommended Refactors

### 1. **Use Object Variables for Node Pool Configuration**

**Current Problem:**

```hcl
# 20+ individual variables for additional node pool
variable "additional_node_pool_availability_zones" { ... }
variable "additional_node_pool_enable_auto_scaling" { ... }
variable "additional_node_pool_max_count" { ... }
# ... 17 more variables
```

**Recommended Solution:**

```hcl
variable "node_pools" {
  description = "Map of node pool configurations"
  type = map(object({
    vm_size                = string
    availability_zones     = optional(list(string))
    enable_auto_scaling    = optional(bool, true)
    min_count             = optional(number, 1)
    max_count             = optional(number, 10)
    node_count            = optional(number, 2)
    max_pods              = optional(number, 100)
    mode                  = optional(string, "User")
    node_labels           = optional(map(string), {})
    node_taints           = optional(list(string), [])
    os_disk_type          = optional(string, "Managed")
    enable_host_encryption = optional(bool, true)
    enable_node_public_ip  = optional(bool, false)
    priority              = optional(string, "Regular")
    eviction_policy       = optional(string, "Delete")
    subnet_name           = string
  }))
  default = {}
}
```

**Benefits:**

- Support unlimited node pools
- Reduce variables from 20+ to 1
- Type-safe configuration
- Clear structure in consumer code

**Consumer Example:**

```hcl
node_pools = {
  workflows = {
    vm_size    = "Standard_E4s_v5"
    min_count  = 1
    max_count  = 10
    priority   = "Spot"
    subnet_name = "workflows"
    node_taints = ["dedicated=workflows:PreferNoSchedule"]
  }
  gpu = {
    vm_size    = "Standard_NC6s_v3"
    min_count  = 0
    max_count  = 5
    subnet_name = "gpu"
  }
}
```

### 2. **Dynamic Subnet Configuration**

**Current Problem:**

- Hardcoded 3 subnets (system, workflows, jumpbox)
- Cannot add custom subnets for different purposes

**Recommended Solution:**

```hcl
variable "subnets" {
  description = "Map of subnet configurations"
  type = map(object({
    address_prefixes                          = list(string)
    private_endpoint_network_policies_enabled = optional(bool, true)
    private_link_service_network_policies_enabled = optional(bool, false)
    purpose            = optional(string, "general") # system, workflows, jumpbox, custom
  }))
  
  default = {
    system = {
      address_prefixes = ["10.0.0.0/20"]
      purpose         = "system"
    }
    workflows = {
      address_prefixes = ["10.0.16.0/20"]
      purpose         = "workflows"
    }
    jumpbox = {
      address_prefixes = ["10.0.48.0/20"]
      purpose         = "jumpbox"
    }
  }
}
```

**Benefits:**

- Support custom subnet layouts
- GPU node pools, database subnets, etc.
- Maintain backward compatibility with defaults

### 3. **Separate Network Module from AKS Module**

**Current Problem:**

- Module creates VNet AND AKS cluster
- Cannot reuse existing networks easily
- Violates single responsibility principle

**Recommended Solution:**

Create two separate modules:

**Module 1: `terraform-azure-network`**

```hcl
# Outputs network resources
output "vnet_id" { ... }
output "subnet_ids" { ... }
output "route_table_id" { ... }
```

**Module 2: `terraform-azure-aks` (refactored)**

```hcl
# Consumes network resources
variable "vnet_id" { ... }
variable "subnet_ids" { ... }
variable "route_table_id" { ... }
```

**Consumer Pattern:**

```hcl
module "network" {
  source = "../../terraform-azure-network"
  # network config
}

module "aks" {
  source     = "../../terraform-azure-aks"
  vnet_id    = module.network.vnet_id
  subnet_ids = module.network.subnet_ids
  # aks config
}
```

**Benefits:**

- Reuse networks across multiple clusters
- Test network and AKS independently
- Follow Terraform composition best practices

### 4. **Configuration Object Pattern**

**Current Problem:**

```hcl
# 40+ individual AKS configuration variables passed through
admin_group_object_ids = var.admin_group_object_ids
admin_username = var.admin_username
automatic_channel_upgrade = var.automatic_channel_upgrade
# ... 37 more lines
```

**Recommended Solution:**

```hcl
variable "aks_config" {
  description = "AKS cluster configuration"
  type = object({
    kubernetes_version            = string
    automatic_channel_upgrade     = optional(string, "stable")
    sku_tier                      = optional(string, "Free")
    azure_policy_enabled          = optional(bool, true)
    azure_rbac_enabled            = optional(bool, true)
    admin_group_object_ids        = optional(list(string), [])
    workload_identity_enabled     = optional(bool, false)
    oidc_issuer_enabled           = optional(bool, false)
    keda_enabled                  = optional(bool, false)
    vertical_pod_autoscaler_enabled = optional(bool, true)
    image_cleaner_enabled         = optional(bool, false)
    http_application_routing_enabled = optional(bool, false)
  })
}

variable "network_config" {
  description = "Network configuration for AKS"
  type = object({
    network_plugin      = optional(string, "azure")
    network_plugin_mode = optional(string)
    network_policy      = optional(string, "calico")
    pod_cidr            = optional(string)
    service_cidr        = string
    dns_service_ip      = string
  })
}
```

**Benefits:**

- Logical grouping of related settings
- Easier to understand module interface
- Reduce variable count by 70%

### 5. **Feature Flags with Sensible Defaults**

**Current Problem:**

- Many optional features scattered across variables
- Unclear which features are enabled

**Recommended Solution:**

```hcl
variable "features" {
  description = "Optional feature flags"
  type = object({
    bastion_host    = optional(bool, false)
    jumpbox         = optional(bool, true)
    hub_network     = optional(bool, false)
    azure_firewall  = optional(bool, false)
    private_dns     = optional(bool, true)
  })
  default = {}
}

# Usage in module
resource "azurerm_bastion_host" "this" {
  count = var.features.bastion_host ? 1 : 0
  # ...
}
```

### 6. **Naming Configuration Object**

**Current Problem:**

```hcl
# 10+ override variables for names
variable "resource_group_name" { ... }
variable "vnet_name" { ... }
variable "aks_cluster_name" { ... }
# ... 7 more
```

**Recommended Solution:**

```hcl
variable "naming" {
  description = "Naming configuration"
  type = object({
    workload   = string
    region     = string
    env_prefix = string
    overrides  = optional(object({
      resource_group = optional(string)
      vnet          = optional(string)
      aks_cluster   = optional(string)
      route_table   = optional(string)
      nsg           = optional(string)
      bastion       = optional(string)
    }), {})
  })
}

locals {
  base_name = "${var.naming.workload}-${var.naming.region}-${var.naming.env_prefix}"
  
  names = {
    resource_group = coalesce(var.naming.overrides.resource_group, "rg-${local.base_name}-net")
    vnet          = coalesce(var.naming.overrides.vnet, "vnet-${local.base_name}-01")
    aks_cluster   = coalesce(var.naming.overrides.aks_cluster, "aks-${local.base_name}-01")
    # ...
  }
}
```

### 7. **Validation Functions**

Add comprehensive validation:

```hcl
variable "node_pools" {
  # ...
  
  validation {
    condition = alltrue([
      for name, pool in var.node_pools :
      pool.min_count <= pool.max_count
    ])
    error_message = "Node pool min_count must be <= max_count for all pools."
  }
  
  validation {
    condition = alltrue([
      for name, pool in var.node_pools :
      contains(["User", "System"], pool.mode)
    ])
    error_message = "Node pool mode must be 'User' or 'System'."
  }
}
```

---

## Migration Strategy

### Phase 1: Add New Variables (Non-Breaking)

1. Add `node_pools` variable alongside existing variables
2. Add `subnets` variable with current defaults
3. Add `aks_config`, `network_config`, `naming` objects
4. Update locals to use new variables when provided

### Phase 2: Update Documentation

1. Mark old variables as deprecated
2. Provide migration examples
3. Update README with new patterns

### Phase 3: Deprecation (Breaking Change)

1. Remove individual variables in next major version
2. Require object-based configuration
3. Publish migration guide

---

## Example: Before Vs After

### Before (Current)

```hcl
module "private-infrastructure" {
  source = "..."
  
  # 50+ individual variables
  workload   = "ff"
  region     = "uks"
  env_prefix = "prod"
  
  additional_node_pool_name = "workflows"
  additional_node_pool_vm_size = "Standard_E4s_v5"
  additional_node_pool_min_count = 1
  additional_node_pool_max_count = 10
  additional_node_pool_enable_auto_scaling = true
  additional_node_pool_priority = "Spot"
  # ... 45 more variables
}
```

### After (Proposed)

```hcl
module "private-infrastructure" {
  source = "..."
  
  naming = {
    workload   = "ff"
    region     = "uks"
    env_prefix = "prod"
  }
  
  aks_config = {
    kubernetes_version = "1.30.0"
    sku_tier          = "Standard"
  }
  
  network_config = {
    service_cidr   = "10.2.0.0/24"
    dns_service_ip = "10.2.0.10"
  }
  
  node_pools = {
    workflows = {
      vm_size    = "Standard_E4s_v5"
      min_count  = 1
      max_count  = 10
      priority   = "Spot"
      subnet_name = "workflows"
    }
  }
  
  features = {
    jumpbox      = true
    bastion_host = false
  }
}
```

---

## Terraform Best Practices Applied

1. **✅ Module Composition** - Separate network and compute concerns
2. **✅ Object Variables** - Group related configuration
3. **✅ Optional Attributes** - Sensible defaults with override capability
4. **✅ Validation** - Type safety and business rule enforcement
5. **✅ Flat Module Hierarchy** - Avoid deep nesting
6. **✅ Clear Interfaces** - Reduced cognitive load
7. **✅ Backward Compatibility** - Phased migration approach

---

## Priority Recommendations

### High Priority (Do First)

1. **Node Pools Object Variable** - Biggest flexibility gain
2. **Naming Configuration Object** - Simplifies interface
3. **Subnet Configuration Map** - Enables custom layouts

### Medium Priority

4. **AKS/Network Config Objects** - Better organization
5. **Feature Flags Object** - Clearer feature management

### Low Priority (Future)

6. **Separate Network Module** - Architectural improvement
7. **Advanced Validation** - Enhanced safety

---

## Conclusion

These refactors will transform the module from a rigid, variable-heavy implementation into a flexible, composable infrastructure module that follows Terraform best practices. The phased approach ensures backward compatibility while enabling gradual migration to the improved interface.

**Estimated Impact:**

- **Variables:** 100+ → ~15-20 (80% reduction)
- **Flexibility:** Single node pool → Unlimited node pools
- **Maintainability:** High → Very High
- **Reusability:** Medium → High
