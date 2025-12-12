---
aliases: []
confidence:
created: 2025-11-26T05:04:29Z
epistemic:
last_reviewed:
modified: 2025-12-04T13:27:53Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [nnuh]
title: Permissions to deploy AKS
type:
uid:
updated:
---

Short answer: you’re *very* close. The custom role already includes the critical `Microsoft.Authorization/roleAssignments/*`, which covers `roleAssignments/write`. For most “vanilla” private AKS deployments, this set is enough.

However, there are a few gaps I’d recommend filling to make it robust and avoid weird 403s during AKS+addon provisioning, especially around:

- Reading role definitions
- Reading/using providers and locations
- Log Analytics / Monitoring addons
- Key Vault / disk encryption (if used)
- Route tables / load balancers / NSGs (for certain network setups)

Below is an updated `permissions` block you can propose. I’ll keep your existing actions and just add commonly needed ones, with comments so you can trim if some don’t apply.

```hcl
resource "azurerm_role_definition" "private_aks" {
  name  = "private-aks-provisioner"
  scope = data.<given_subscription_id>

  permissions {
    actions = [
      # Existing: role assignments (needed for Microsoft.Authorization/roleAssignments/write)
      "Microsoft.Authorization/roleAssignments/*",

      # RECOMMENDED EXTRA: read role definitions (some flows query roles)
      "Microsoft.Authorization/roleDefinitions/read",

      # Existing: compute/VM control
      "Microsoft.Compute/disks/*",
      "Microsoft.Compute/virtualMachines/*",
      "Microsoft.Compute/virtualMachines/extensions/*",
      "Microsoft.Compute/virtualMachines/powerOff/action",

      # Existing: AKS control
      "Microsoft.ContainerService/managedClusters/*",

      # Existing: user-assigned identities
      "Microsoft.ManagedIdentity/userAssignedIdentities/*",

      # Existing: NICs & NSGs
      "Microsoft.Network/networkInterfaces/*",
      "Microsoft.Network/networkInterfaces/join/action",
      "Microsoft.Network/networkSecurityGroups/delete",
      "Microsoft.Network/networkSecurityGroups/join/action",
      "Microsoft.Network/networkSecurityGroups/*",

      # Existing: Private DNS
      "Microsoft.Network/privateDnsZones/A/*",
      "Microsoft.Network/privateDnsZones/SOA/*",
      "Microsoft.Network/privateDnsZones/*",
      "Microsoft.Network/privateDnsZones/virtualNetworkLinks/*",

      # Existing: PIP + VNETs
      "Microsoft.Network/publicIPAddresses/*",
      "Microsoft.Network/virtualNetworks/*",

      # NEW: Route tables (needed in some network setups / UDRs)
      "Microsoft.Network/routeTables/*",
      "Microsoft.Network/routes/*",

      # NEW: Load balancers (AKS SLB / outbound rules)
      "Microsoft.Network/loadBalancers/*",
      "Microsoft.Network/loadBalancers/backendAddressPools/*",
      "Microsoft.Network/loadBalancers/frontendIPConfigurations/*",
      "Microsoft.Network/loadBalancers/loadBalancingRules/*",
      "Microsoft.Network/loadBalancers/probes/*",
      "Microsoft.Network/loadBalancers/inboundNatRules/*",

      # Existing: read subscription & RGs
      "Microsoft.Resources/subscriptions/providers/read",
      "Microsoft.Resources/subscriptions/resourcegroups/*",

      # NEW: generic resource read (helps with a lot of “lookup” operations)
      "Microsoft.Resources/subscriptions/resourcegroups/read",
      "Microsoft.Resources/subscriptions/resourcegroups/resources/read",

      # NEW: Monitoring / Log Analytics (if you enable OMS/insights addon)
      "Microsoft.OperationalInsights/workspaces/*",
      "Microsoft.Insights/diagnosticSettings/*",

      # NEW: Key Vault / disk encryption (only if you use CMK, pod identity via KV, etc.)
      "Microsoft.KeyVault/vaults/read",
      "Microsoft.KeyVault/vaults/accessPolicies/*",
      "Microsoft.KeyVault/vaults/secrets/*",

      # NEW: Provider + location discovery (often used under the hood)
      "Microsoft.Resources/subscriptions/locations/read",
      "Microsoft.Resources/providers/read"
    ]

    not_actions = []
  }

  assignable_scopes = [
    data.<given_subscription_id>
  ]
}
```

## How to Justify This in an Email

You can explain it like this:

- We already grant the Terraform SP `Microsoft.Authorization/roleAssignments/*`, which covers the required `roleAssignments/write` permission for AKS-related role assignments.
- To avoid deployment failures during AKS cluster + addon provisioning, we also need it to:
    - Read role definitions and providers to validate capabilities.
    - Manage/load network resources like load balancers and route tables used by the AKS control plane and node pools.
    - Optionally manage Log Analytics and Key Vault resources if those addons/integrations are enabled.

If you tell me which AKS features you’re enabling (private cluster, Azure CNI vs kubenet, UDRs, AGIC, monitoring addon, Key Vault integration, etc.), I can trim this list down to just what you need.
