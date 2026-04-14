---
created: 2026-04-13T13:01:40+00:00
modified: 2026-04-13T13:18:28+00:00
title: pieces_copilot_message_export_april_13_2026_2_01pm
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Monday Apr 13, 2026 - 2:01 PM_

## Yes—You'd Link to BOTH VNets (Not "Either/Or")

You're hitting on the key insight here. If the customer is on a different VNet, you need to link the private DNS zone to the customer's VNet as well (not instead of yours).

---

## How Private DNS Zone Links Work

A single private DNS zone can be linked to up to 1,000 VNets (from your zone properties at 1:10 PM):

```json
"maxNumberOfVirtualNetworkLinks": 1000
```

Each VNet that needs private IP resolution requires its own link. Think of it like access control: any VNet that should resolve `lca-prd-2.fitfile.net` to `10.200.80.50` needs to be explicitly linked.

---

## Typical Topology Scenarios

### Scenario A: Customer Has Their Own VNet

If the customer VMs are in `vnet-customer-uks-01` (separate from `vnet-fflz-uks-01`), you'd have two VNet links:

```bash
# Link 1: Your VNet (already created at 1:10 PM)
az network private-dns link vnet create \
  --resource-group "rg-lca-uks-prd-net" \
  --zone-name "fitfile.net" \
  --name "link_to_vnet-fflz-uks-01" \
  --virtual-network "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/rg-vnet-fflz-01/providers/Microsoft.Network/virtualNetworks/vnet-fflz-uks-01" \
  --registration-enabled false

# Link 2: Customer VNet (new)
az network private-dns link vnet create \
  --resource-group "rg-lca-uks-prd-net" \
  --zone-name "fitfile.net" \
  --name "link_to_vnet-customer-uks-01" \
  --virtual-network "/subscriptions/<sub-id>/resourceGroups/<customer-rg>/providers/Microsoft.Network/virtualNetworks/vnet-customer-uks-01" \
  --registration-enabled false
```

Result: VMs in both VNets resolve `lca-prd-2.fitfile.net` to `10.200.80.50`.

---

### Scenario B: Customer Uses Peered VNet with DNS Forwarding

From your VNet JSON (1:08 PM), you have a peering to `vnet-hub-uks-01`:

```json
"allowForwardedTraffic": true
"useRemoteGateways": true
```

If the customer VNet peers with `vnet-hub-uks-01` and that hub uses Azure DNS (`168.63.129.16`), DNS queries automatically propagate. In this case:

- ✅ Link to `vnet-fflz-uks-01` (your VNet)
- ✅ Customer VNet gets DNS via peering (no additional link needed)

Verify peering settings:

```bash
az network vnet peering show \
  --resource-group <customer-rg> \
  --name <peering-name> \
  --vnet-name <customer-vnet> \
  --query "{allowVirtualNetworkAccess: allowVirtualNetworkAccess, useRemoteGateways: useRemoteGateways, allowForwardedTraffic: allowForwardedTraffic}"
```

If `allowForwardedTraffic: true`, DNS queries should work via peering.

---

## Re-Interpreting Robin's Instruction

Now Robin's comment "it must not be attached to our VNET" makes more sense if interpreted as:

> _"It must not be attached only to our VNET—the customer's VNet needs access too."_

But the phrasing was ambiguous. The correct approach:

1. Link to your VNet (`vnet-fflz-uks-01`) ✅ Done
2. Also link to customer VNet OR ensure peering allows DNS forwarding

---

## TL;DR

| If Customer VNet is… | Action Required |
|----------------------------|---------------------|
| Directly peered with `vnet-fflz-uks-01` (with DNS forwarding) | Nothing—existing link works via peering |
| Peered via hub (`vnet-hub-uks-01`) with Azure DNS | Nothing—existing link works via hub |
| Isolated/separate (no peering) | Create second VNet link to customer VNet |
| In a different subscription (managed by customer) | Coordinate with customer to create link (requires permissions) |

---

Next step: Identify the customer's VNet name/resource ID and check if it's peered with `vnet-fflz-uks-01` or `vnet-hub-uks-01`. If yes, test DNS resolution from a customer VM. If no, create the second VNet link.
