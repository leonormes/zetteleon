---
aliases: [Internal DNS, Private TLD]
confidence:
created: 2025-07-16T17:30:03Z
epistemic:
last_reviewed:
modified: 2025-10-30T15:36:27Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [topic/technology/networking/dns]
title: Private DNS Zones Provide Internal Network Name Resolution
type:
uid:
updated:
version:
---

A private DNS zone, such as one using a private Top-Level Domain (TLD) like `privatelink.fitfile.net`, is used for name resolution exclusively within a private network (e.g., an Azure VNet). Records in a private zone are not resolvable from the public internet.

This approach ensures that internal services, like a Kubernetes application frontend at `app.privatelink.fitfile.net`, have stable, predictable DNS names without being exposed publicly. This is a common practice for securing internal application endpoints.

This concept is a key part of enabling a [[Hybrid Cloud DNS Resolution Flow]], which relies on tools like the to bridge the gap between on-premises networks and cloud resources.
