---
aliases: []
confidence: 1.0
created: 2025-11-22T15:05:02Z
epistemic: fact
last_reviewed: 2025-11-22
modified: 2025-11-22T14:50:39Z
purpose: "Provides a reference for common CIDR implementations."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [networking/cidr]
title: Concept - CIDR Subnet Sizes
type: concept
uid: 2025-11-22T15:05:02Z
updated: 2025-11-22T15:05:02Z
---

## CIDR Subnet Sizes

**Summary:** The number of available IP addresses in a Classless Inter-Domain Routing (CIDR) block is calculated as $2^{(32 - \text{mask})}$.

**Details:**
Common subnet sizes encountered in infrastructure access control and segmentation include:
-   **/24:** 256 addresses ($2^8$).
-   **/26:** 64 addresses ($2^6$). Often used for intermediate logical blocks.
-   **/27:** 32 addresses ($2^5$).
-   **/29:** 8 addresses ($2^3$). Often used for small, dedicated subnets like jumpboxes.
Note that in many cloud environments (like Azure or AWS), roughly 5 addresses per subnet are reserved for system use, further reducing the usable count.
