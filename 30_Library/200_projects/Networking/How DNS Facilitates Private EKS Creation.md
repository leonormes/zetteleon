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
title: How DNS Facilitates Private EKS Creation
type: 
uid: 
updated: 
version: 
---

- Internal Communication: DNS enables internal communication within your EKS cluster and between services within your VPC. Kubernetes relies on DNS for service discovery. Therefore, having a properly configured DNS ensures that pods can find each other within the cluster.
- Integration with AWS Services: DNS integrates with other AWS services within your VPC. For example, services like `ExternalDNS` can manage DNS records for microservices within the EKS cluster.
- Avoiding Public Exposure: Using a private hosted zone along with private subnets ensures that your cluster's resources remain private and are not directly exposed to the public internet. This significantly enhances the security posture of your EKS environment.
- Custom Networking: When creating a VPC for your EKS cluster, you can use tools like `eksctl`, which, by default, configures a VPC to address all networking requirements, including the creation of both public and private endpoints. This highlights how DNS configurations are integrated with other network aspects of setting up private EKS clusters.
- Windows Node DNS: When using Windows managed node groups, it's important to add `eks:kube-proxy-windows` to the AWS IAM Authenticator configuration map for DNS to function properly. This ensures DNS resolution works correctly within the Windows nodes.

[[300_Documentation/FITFILE/Cloud/AWS/VPC DNS Configuration]]
