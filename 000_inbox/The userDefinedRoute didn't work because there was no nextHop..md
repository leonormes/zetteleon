---
aliases: []
confidence: 
created: 2025-11-24T14:00:26Z
epistemic: 
last_reviewed: 
modified: 2025-11-24T14:00:51Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: "The userDefinedRoute didn't work because there was no nextHop."
type: 
uid: 
updated: 
---

```sh
╷
│ Error: creating Kubernetes Cluster (Subscription: "4ae8fd93-d084-481f-ba6e-370b7d4d8d0d"
│ Resource Group Name: "rg-ff-uks-gp-net"
│ Kubernetes Cluster Name: "aks-ff-uks-gp-01"): performing CreateOrUpdate: unexpected status 400 (400 Bad Request) with response: {
│   "code": "ExistingRouteTableNotAssociatedWithSubnet",
│   "details": null,
│   "message": "An existing route table has not been associated with subnet /subscriptions/4ae8fd93-d084-481f-ba6e-370b7d4d8d0d/resourceGroups/NNUHFT-SDE-Networking/providers/Microsoft.Network/virtualNetworks/NNUHFT-SDE-vnet1/subnets/snet-ff-uks-gp-system. Please update the route table association",
│   "subcode": ""
│  }
│
│   with module.private-infrastructure.module.aks_cluster.azurerm_kubernetes_cluster.aks_cluster,
│   on .terraform/modules/private-infrastructure/modules/aks/main.tf line 27, in resource "azurerm_kubernetes_cluster" "aks_cluster":
│   27: resource "azurerm_kubernetes_cluster" "aks_cluster" {
│
╵
```

You want to keep `userDefinedRouting` and apply Terraform in pieces. I’ll check the `terraform-azure-private-infrastructure` module to see where the route table and its association are defined and how `private-infrastructure` wires into it. Then I’ll outline which targets must be applied (and in what order) so the route table is created/associated before `aks_cluster`, and confirm whether the RT code is already present.

I’ll check the private-infrastructure module to see how the route table and subnet association are defined, then explain what you need to apply (and in what order) so userDefinedRouting works when you target resources.

## What’s Going on

- **Yes, the route table (RT) code is already in the module.**
  - [terraform-azure-private-infrastructure/networking.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/TFC-Modules/terraform-azure-private-infrastructure/networking.tf:0:0-0:0) defines `module "routetable"` and associates it to the AKS subnets.
  - [main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/main.tf:0:0-0:0) for the module sets `depends_on = [module.routetable]` on `module "aks_cluster"`.
- But in your NNUH-DP usage, that RT code is **not being run** because:
  - `local.create_route_table = var.firewall_existing_private_ip != null`
  - In NNUH-DP you don’t pass `firewall_existing_private_ip`, so it’s `null`.
  - Therefore `module "routetable"` has `count = 0` → **no route table** and **no association**.
  - At the same time, you’ve forced `outbound_type = "userDefinedRouting"`, so AKS expects a UDR on `snet-ff-uks-gp-system` and complains.

Additionally, for existing VNets (`create_vnet = false`) there was a subtle bug: the RT association used the module’s RG instead of the VNet RG. I’ve updated the module code so the association now uses `vnet_resource_group_name` when provided, which matches your NNUHFT-SDE-Networking layout.

---

## Making Option 1 Work (userDefinedRouting with Existing network)

You’re reusing an existing VNet `NNUHFT-SDE-vnet1` in RG `NNUHFT-SDE-Networking`. To have proper forced tunneling:

1. **Provide the existing firewall’s private IP to the module**

   In your NNUH-DP [main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/main.tf:0:0-0:0) `module "private-infrastructure"` block, add:

   ```hcl
   firewall_existing_private_ip = "<PRIVATE_IP_OF_YOUR_FIREWALL>"
   ```

   Replace `<PRIVATE_IP_OF_YOUR_FIREWALL>` with the actual private IP of the NNUH firewall / virtual appliance that should handle internet egress.

   Effects:

   - `firewall_existing_private_ip != null` → `local.create_route_table = true`
   - `module "routetable"` will be created.
   - The RT will route `0.0.0.0/0` to `VirtualAppliance` at that IP.

2. **Route table association behaviour (now fixed for existing VNets)**

   In the module:

   - The RT is created in `rg-ff-uks-gp-net` (the module’s RG).
   - The subnets to associate are built with:
     - `subscription_id      = current subscription`
     - `resource_group_name  = coalesce(var.vnet_resource_group_name, azurerm_resource_group.rg.name)`
     - `virtual_network_name = module.aks_network.name` (your existing VNet name)

   For NNUH-DP, this means:

   - RT in `rg-ff-uks-gp-net`.
   - Associations to subnets in `NNUHFT-SDE-Networking` / `NNUHFT-SDE-vnet1` (cross-RG association is supported).

   That satisfies AKS’s requirement for `userDefinedRouting`.

3. **How to apply when using `--target`**

   Once `firewall_existing_private_ip` is set:

   - `module "aks_cluster"` has `depends_on = [module.routetable]`.
   - So even if you run:

     ```bash
     terraform apply --target module.private-infrastructure.module.aks_cluster
     ```

     Terraform will automatically create `module.private-infrastructure.module.routetable` first (because it’s a dependency) **as long as its `count` is 1**, which now it is.

   You don’t strictly need to target `routetable` separately, but if you want to be explicit:

   ```bash
   # Ensure VNet/subnets wiring is in place (if not already applied)
   terraform apply --target module.private-infrastructure.module.aks_network

   # Create route table + associations
   terraform apply --target module.private-infrastructure.module.routetable

   # Then create the AKS cluster
   terraform apply --target module.private-infrastructure.module.aks_cluster
   ```

   After the RT is associated, the AKS API will accept `outbound_type = "userDefinedRouting"` and the 400 error should disappear.

---

## Summary

- **RT code is present**, but with your current inputs it was effectively disabled (`count = 0`).
- For **Option 1** (keep `userDefinedRouting`):
  - Set `firewall_existing_private_ip` in the NNUH-DP `private-infrastructure` module call.
  - Re-run `terraform apply` (with or without `--target`), letting Terraform create the route table and associate it to `snet-ff-uks-gp-system` before/with the AKS cluster.
- The module code has been adjusted so RT associations work correctly when using an **existing VNet in another RG**, matching your `NNUHFT-SDE-Networking` setup.

If you tell me the firewall’s private IP and confirm whether hub is managed elsewhere, I can show you the exact snippet to add in your NNUH-DP [main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/NNUH-DP/main.tf:0:0-0:0) block.
