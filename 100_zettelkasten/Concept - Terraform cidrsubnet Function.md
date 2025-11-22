---
aliases: [cidrsubnet]
confidence: 1.0
created: 2025-11-22T15:05:00Z
epistemic: fact
last_reviewed: 2025-11-22
modified: 2025-11-22T14:50:43Z
purpose: "Defines the Terraform function for calculating subnets."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [HCL, networking, terraform]
title: Concept - Terraform cidrsubnet Function
type: concept
uid: 2025-11-22T15:05:00Z
updated: 2025-11-22T15:05:00Z
---

## Terraform Cidrsubnet Function

**Summary:** The `cidrsubnet` function in Terraform calculates a subnet address within a given IP network address prefix.

**Details:**
The function signature is `cidrsubnet(prefix, newbits, netnum)`.
-   **prefix:** The routing prefix to subnet (e.g., `"10.0.0.0/16"`).
-   **newbits:** The number of additional bits to extend the prefix by. The new subnet mask will be `old_mask + newbits`.
-   **netnum:** A whole number acting as the index (0-based) to select which subnet to return.
It enables the mathematical calculation of subnets directly within Infrastructure as Code configurations.
