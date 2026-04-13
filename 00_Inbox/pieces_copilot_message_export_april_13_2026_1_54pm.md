*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Monday Apr 13, 2026 - 1:54 PM*
---
## The Instruction Doesn't Make Sense — And You Were Right to Question It

Robin's instruction **"it must not be attached to our VNET"** is **incorrect** or at minimum **badly phrased**. Here's why:

---

## Why a Private DNS Zone MUST Be Linked to a VNet

An Azure Private DNS Zone only intercepts DNS queries when it's **linked to a VNet**. Without a VNet link:

1. **DNS queries bypass the private zone entirely** → they go straight to public DNS (Cloudflare)
2. **The A record you created (`10.200.80.50`) is never used** → all traffic hits the public IP
3. **The private zone becomes a useless orphan resource** → it exists but does nothing

**Your current working setup** (confirmed at **1:10 PM**):
```json
"virtualNetworkLinkState": "Completed"
"virtualNetwork": "/subscriptions/.../vnet-fflz-uks-01"
```

✅ **This is correct.** Without this link, the entire private DNS zone would be pointless.

---

## What Robin Might Have Meant

### **Theory 1: Wrong VNet Reference**
Robin might have meant *"don't link it to FITFILE's corporate office VNet"* (if one exists) but *do* link it to the customer deployment VNet (`vnet-fflz-uks-01`). 

However, I don't see evidence of a separate FITFILE corporate VNet in your context — all the infrastructure appears to be customer-scoped.

### **Theory 2: Confusion About Private Link**
The old zone was named `privatelink.fitfile.net`, which suggests confusion with [Azure Private Link](https://learn.microsoft.com/en-us/azure/private-link/). Private Link zones use a specific naming pattern (`privatelink.<service>.azure.net`) and **are automatically linked when you create private endpoints**.

Robin might have been thinking of Private Link zones (which auto-link) vs. custom private DNS zones (which require manual links).

### **Theory 3: The Ticket Was Vague**
[FTFL-550](https://fitfile.atlassian.net/browse/FTFL-550) might not have captured the full requirement. Ollie's explanation (**"inside the private network"**) confirms the zone **must** be linked — otherwise customers can't access via the private IP.

---

## What Ollie Actually Explained

From your summary (**1:39 PM**):
> "basically 'inside the private network' as cloudflare is already pointing lca-prd-2.fitfile.net to the LCA public IP"

**Ollie's point:** You need **split-horizon DNS**:
- **Inside the private network** (VNet users) → Resolve to `10.200.80.50` (private IP)
- **Outside the private network** (internet) → Resolve to LCA's public IP (via Cloudflare)

This **requires** the private DNS zone to be linked to the VNet. Without the link, "inside the private network" users would get the public IP too.

---

## TL;DR: You Did It Correctly

| **Robin's Instruction** | **What Actually Works** | **Why** |
|-------------------------|-------------------------|---------|
| *"must not be attached to our VNET"* ❌ | Must be attached to `vnet-fflz-uks-01` ✅ | Private DNS zones don't work without VNet links |
| Ambiguous ticket | Ollie clarified: split-horizon DNS | Internal users need private IP resolution |
| No VNet link = zone does nothing | VNet link = private IP for internal users | DNS interception only happens via linked VNets |

---

## Next Step: Clarify the Ticket

Update [FTFL-550](https://fitfile.atlassian.net/browse/FTFL-550) with:

> **Implemented Solution:**  
> Created Azure Private DNS zone `fitfile.net` with A record `lca-prd-2 → 10.200.80.50`.  
> **Linked to VNet:** `vnet-fflz-uks-01` (required for split-horizon DNS).  
> **Result:** Internal users resolve to private IP; external users resolve to public IP via Cloudflare.

This prevents future confusion when someone reads the ticket history. Robin's original instruction was either misstated or based on incomplete information — Ollie's clarification was the correct approach.