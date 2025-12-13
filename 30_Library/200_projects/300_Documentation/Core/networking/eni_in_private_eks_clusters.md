---
aliases: []
confidence: 
created: 2025-02-07T12:57:53Z
epistemic: 
ID: 7a1a
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: eni_in_private_eks_clusters
type:
uid: 
updated: 
version:
---

## ENI In Private EKS Clusters

### Key Points

- ENIs are used by the AWS VPC CNI plugin to assign IP addresses to Kubernetes Pods in a private EKS cluster.
- Each worker node in EKS has ENIs that handle pod-level networking, allowing direct VPC integration.
- In private EKS clusters, ENIs enable secure communication between worker nodes and the private control plane.

### Linked Zettels

- Overview of ENI
- VPC CNI Plugin and ENIs
- ENIs in Load Balancing for EKS

---

[aws eni](<../Notes/aws eni.md>)
