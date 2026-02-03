---
created: 2025-12-04T12:02:41Z
last_reviewed: null
modified: 2026-02-03T16:11:50+00:00
status: processing
tags: [state/thinking]
title: HEAD - Azure Bastion Deletion
type: head
updated: null
---

Yep—in your case, you can delete the Bastion and reuse the same Public IP when you recreate it.

From what you pasted, your Public IP is already exactly what Bastion needs:

- Public IP SKU: `Standard` ✅
- Allocation: `Static` ✅
- Version: `IPv4` ✅
- Region: `uksouth` ✅
- Same RG/subscription as Bastion: ✅
- It's currently attached via `ipConfiguration`, but once you delete Bastion it should become unattached and eligible to reuse ✅

So the workflow you're aiming for is valid.

---

## The only Gotchas to Watch for

1. Deletion order
    
    - Delete the Bastion host first.
    - Keep the Public IP resource.
        
2. Wait for detachment
    
    - After Bastion deletion completes, open the Public IP and confirm it no longer shows an attached `ipConfiguration` (or "Associated to …").
    - Sometimes Azure takes a short moment to fully detach.
        
3. Recreate Bastion pointing at that IP
    
    - During Bastion creation (portal or Terraform), select / reference the existing Public IP:
        - `/Microsoft.Network/publicIPAddresses/bastion-lca-plat-uks-01PublicIp`

---

## Terraform Note (since Your Tags Say CreatedWith=Terraform)

If you manage this with Terraform, you typically want:

- Bastion resource can be destroyed/recreated safely
- Public IP persists (don't destroy it)

That usually means:

- Keep the `azurerm_public_ip` resource in state
- Allow destroying `azurerm_bastion_host` without touching the IP
- On recreate, Bastion references the existing `public_ip_address_id`

If you want, paste your Bastion + Public IP Terraform snippet and I'll show the cleanest way to structure it so "remove bastion, keep IP" is a one-liner and doesn't cause replacement surprises.

---

## Cost Reality Check (important)

This will remove Bastion hourly costs, but you'll still pay a smaller ongoing charge for the Standard Public IP while it exists. If you need zero cost, you'd delete the IP too (but then you lose that fixed address).

If your goal is mainly "Bastion is expensive, but I want to keep the IP stable for allowlists," your plan is spot on.
