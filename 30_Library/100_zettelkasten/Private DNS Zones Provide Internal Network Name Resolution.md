---
aliases: ["Internal DNS", "Private TLD"]
confidence: "null"
created: 2025-07-16T17:30:03Z
epistemic: "null"
last_reviewed: "null"
modified: 2026-01-03T10:19:36+00:00
purpose: "null"
review_interval: "null"
see_also: []
source_of_truth: []
status: "null"
tags: ["topic/technology/networking/dns"]
title: Private DNS Zones Provide Internal Network Name Resolution
type: "null"
uid: 
updated: 
version: "null"
---

A private DNS zone, such as one using a private Top-Level Domain (TLD) like `privatelink.fitfile.net`, is used for name resolution exclusively within a private network (e.g., an Azure VNet). Records in a private zone are not resolvable from the public internet.

This approach ensures that internal services, like a Kubernetes application frontend at `app.privatelink.fitfile.net`, have stable, predictable DNS names without being exposed publicly. This is a common practice for securing internal application endpoints.

This concept is a key part of enabling a [[Hybrid Cloud DNS Resolution Flow]], which relies on tools like the to bridge the gap between on-premises networks and cloud resources.
