---
aliases: []
confidence: 
created: 2025-06-30T19:38:05Z
epistemic: 
last_reviewed: 
modified: 2025-11-01T15:05:48Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Cloud Network
type:
uid: 
updated: 
version:
---

To control traffic with precision and accuracy in a cloud Kubernetes environment, you primarily need to focus on two layers of control:

1. Kubernetes-Native Abstractions: These are the built-in mechanisms within Kubernetes itself that define how applications communicate with each other internally and are exposed externally.
2. Cloud Provider Networking Services: These are the underlying network infrastructures provided by cloud vendors (like Azure, AWS, GCP) that your Kubernetes cluster leverages for broader network connectivity, security, and specialized routing.

Let's break down the key components for precision and accuracy:

[[Kubernetes-Native Abstractions for Traffic Control]]
