---
aliases: []
confidence: 
created: 2025-11-22T15:05:03Z
epistemic: NA
last_reviewed: 2025-11-22
modified: 2025-11-22T14:49:26Z
purpose: "Explains the refactoring of subnet logic for clarity."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [networking, terraform]
title: MOC - Refactoring Subnet Definitions for Readability
type: map
uid: 2025-11-22T15:05:03Z
updated: 2025-11-22T15:05:03Z
---

## MOC - Refactoring Subnet Definitions for Readability

**Summary:** This note details a refactoring of Terraform subnet definitions, moving from opaque, direct indexing to a clearer, hierarchical approach.

### The Problem: Opaque Indexing

The original implementation calculated a specific jumpbox subnet (`/29`) directly from the main VNet address space (`/24`) using the [[Concept - Terraform cidrsubnet Function]]:

```hcl
vm_subnet_address_prefix = [cidrsubnet(local.vnet_address_space, 5, 16)]
```

While mathematically correct (`/24` + 5 bits = `/29`; index 16 starts at `.128`), the "magic numbers" `5` and `16` are not intuitive. They require mental math to visualize where the subnet sits in the address space.

### The Solution: Hierarchical Subnetting

The improved approach uses [[Strategy - Hierarchical Subnetting]] to break the calculation into logical steps:

1.  **Carve a generic block:** First, define a larger "Jumpbox Area" (`/26`) from the main VNet.

    ```hcl
    jumpbox_block_prefix = cidrsubnet(local.vnet_address_space, 2, 2) # Result: 192.168.200.128/26
    ```

2.  **Carve the specific subnet:** Then, define the specific VM subnet (`/29`) from *that* intermediate block.

    ```hcl
    vm_subnet_address_prefix = [cidrsubnet(local.jumpbox_block_prefix, 3, 0)] # Result: 192.168.200.128/29
    ```

This method yields the exact same [[Concept - CIDR Subnet Sizes|CIDR ranges]] but makes the layout explicit: the generic block covers the range `.128-.191`, and the specific VM subnet occupies the first slice of that block.
