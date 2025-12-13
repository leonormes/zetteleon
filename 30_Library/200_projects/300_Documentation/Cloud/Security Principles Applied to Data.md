---
aliases: []
confidence: 
created: 2025-03-15T07:39:41Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:43Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Security Principles Applied to Data
type:
uid: 
updated: 
version:
---

To summarize, the fundamental security principles applied to the data in this cross-cloud communication are:

**Data in Transit Encryption**: Protecting confidentiality using encryption algorithms.

**Data Integrity Protection**: Ensuring data is not modified using integrity checks.

**Endpoint Authentication**: Verifying the identity of communicating services to prevent impersonation.

**Access Control (Authorization)**: Restricting data exchange to authorized services only.

**Network Isolation**: Creating a private and isolated network path to minimize exposure.

By focusing on these data-centric principles and the abstract network components that fulfil these functions, you can understand the core requirements for secure cross-cloud communication, regardless of the specific cloud provider products or terminology used. When you then look at vendor-specific solutions (like VPN Gateways, Direct Connect, etc.), you can map these products back to these fundamental functions and understand how they implement these data security principles in practice.

[[Data-Centric Perspective Secure Cross-Cloud Communication (AWS EKS to Azure AKS)]]
