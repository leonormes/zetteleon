---
aliases: []
confidence: 
created: 2025-04-15T12:30:40Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:52Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: One-Off or Infrequent Use Case
type:
uid: 
updated: 
version:
---

If FITFILE's need for this curated data is infrequent or for a very specific, limited purpose, the overhead of migrating and maintaining the data in Azure might not be justified.

In conclusion, given that the data is already traversing the network for querying, the arguments for moving the curated dataset to the Shared Services Subscription become significantly stronger from a technical and operational perspective. The primary benefits would likely be improved performance, reduced network dependency, better scalability, and potentially simplified security management within the Azure environment. The remaining reasons for not moving it would likely be rooted in stringent data governance policies or very specific compliance requirements about the physical location of the authoritative data source, rather than the act of querying it remotely.

[[why not move data to the shared sub]]

[[Remaining Potential (But Weaker) Reasons for Not Moving]]
