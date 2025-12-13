---
aliases: []
confidence: 
created: 2025-04-15T12:34:28Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:52Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Performance and Latency
type: 
uid: 
updated: 
---

Even with ExpressRoute, querying a database across a network connection (on-premises to Azure, then peered to the FITFILE cluster) will likely introduce higher latency and potentially lower throughput compared to querying a database residing within the same Azure subscription and potentially the same region as the FITFILE cluster. For performance-sensitive SQL queries, this could be a significant factor.

[[Stronger Reasons for Considering Moving the Data to the Shared Subscription]]
