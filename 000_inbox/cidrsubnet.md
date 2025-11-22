---
aliases: []
confidence: 
created: 2025-11-21T09:27:03Z
epistemic: 
last_reviewed: 
modified: 2025-11-21T09:27:09Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: cidrsubnet
type: 
uid: 
updated: 
---

I'll explain what the `cidrsubnet` parameters mean for your current jumpbox subnet and then reorganise the locals to use a clearer, hierarchical split that still yields the same CIDRs.

## What `cidrsubnet` Was Doing before

The original expression:

```hcl
vm_subnet_address_prefix = [cidrsubnet(local.vnet_address_space, 5, 16)]
```

- `local.vnet_address_space = "192.168.200.0/24"`.
- `newbits = 5` → `/24` + 5 bits = `/29`.
- Each `/29` block in a `/24` has `2^(32-29) = 8` IPs.
- `netnum = 16` → skip `16 * 8 = 128` addresses from the start of the /24.

So this yields:

- `192.168.200.(0 + 128) = 192.168.200.128`
- Result: `192.168.200.128/29` (range `–`), which matches your intended jumpbox subnet.

So **`(5, 16)` was mathematically correct**, just not very intuitive.

---

## How it’s Organised now

I changed it to a two‑step, more readable split:

```hcl
vnet_address_space = "192.168.200.0/24"

# High‑level layout notes:
# System:    192.168.200.32/27
# Workflows: 192.168.200.64/27
# Jumpbox:   192.168.200.128/29

default_node_pool_subnet_address_prefix    = [cidrsubnet(local.vnet_address_space, 3, 1)]  # 192.168.200.32/27
additional_node_pool_subnet_address_prefix = [cidrsubnet(local.vnet_address_space, 3, 2)]  # 192.168.200.64/27

# 1) Carve out a /26 block for “jumpbox area”
jumpbox_block_prefix = cidrsubnet(local.vnet_address_space, 2, 2)
# /24 + 2 bits = /26 → index 2 = 192.168.200.128/26 (128–191)

# 2) Within that /26, carve the actual /29 used by the VM subnet
vm_subnet_address_prefix = [cidrsubnet(local.jumpbox_block_prefix, 3, 0)]
# /26 + 3 bits = /29 → index 0 = 192.168.200.128/29 (128–135)

bastion_subnet_address_prefix = [cidrsubnet(local.vnet_address_space, 2, 3)]  # 192.168.200.192/26
```

So now:

- **Jumpbox block**: `192.168.200.128/26` (128–191) reserved as a “space” for jumpbox‑adjacent things.
- **Jumpbox VM subnet**: first `/29` inside that block → still `192.168.200.128/29`.
- **Bastion**: `cidrsubnet(/24, 2, 3)` → `192.168.200.192/26` (unchanged).

This keeps all actual CIDRs **identical** to before, but:

- Makes it obvious that:
  - `/24` → four `/26`s: `/26`, `/26`, `/26`, `/26`.
  - You’re using `/26` for jumpbox things, and `/26` for Bastion.
- Avoids the “magic” `5, 16` numbers by structuring the calculation in logical steps.
