---
aliases: []
confidence: 
created: 2025-03-13T09:29:09Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [dns]
title: Private EKS Cluster Endpoints
type: 
uid: 
updated: 
version: 
---

- Private Clusters and the EKS Auth API: For private EKS clusters, the `eks-auth` endpoint in AWS PrivateLink is required to allow nodes to reach the Amazon EKS Auth API. This ensures that communication between the nodes and the EKS control plane remains within the private network and doesn't go through the public internet.
- Accessing Private API Server: To access a private EKS cluster's API server, you'd typically connect from within the cluster's VPC or from an environment like AWS Cloud9. When using an IDE in Cloud9, you need to ensure that the EKS control plane security group allows ingress traffic on port 443 from the IDE’s security group. It is also important to map the AWS credentials of your IDE to the cluster's RBAC configuration.

[[300_Documentation/FITFILE/Cloud/AWS/VPC DNS Configuration]]
