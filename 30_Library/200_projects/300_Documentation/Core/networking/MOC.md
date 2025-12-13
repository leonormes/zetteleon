---
aliases: []
confidence: 
created: 2025-05-20T12:00:00Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [cloud, kubernetes, moc, networking]
title: MOC
type: map_of_content
uid: 
updated: 
version: 
---

## Cloud Networking Map of Content

This document serves as a central navigation hub for cloud networking topics, with a focus on Kubernetes networking, cross-cloud connectivity, and service exposure patterns.

### Kubernetes Gateway API

The Gateway API is a modern approach to Kubernetes service networking that provides advanced traffic routing capabilities.

#### Core Concepts

- [[Gateway API]] - Overview of the Gateway API family and its design principles
- [[Introduction - Kubernetes Gateway API]] - Introduction to the Gateway API architecture
- [[Kubernetes Gateway API Explained]] - Detailed explanation of Gateway API functionality
- [[What's Gateway API and how to deploy on AWS?]] - Practical guide for AWS deployments

#### AWS Implementation

- [[AWS Gateway API Controller]] - Details of the AWS controller for Gateway API
- [[Concepts - AWS Gateway API Controller]] - Conceptual overview of AWS Gateway API implementation
- [[Concepts - AWS Gateway API Controller 1]] - Additional AWS Gateway API controller concepts
- [[gateway controllers aws]] - AWS-specific Gateway controllers
- [[I am using k8s gateway api on aws eks]] - Practical guide for using Gateway API with EKS
- [[the K8s gateway API, and an AWS Load Balancer controller]] - Integration with AWS Load Balancer

#### Deployment Examples

- [[Create an AWS API Gateway to your EKS Cluster (with Terraform)]] - Terraform-based deployment guide
- [[Secure Cross-Cluster Service Exposure using Kubernetes Gateway API and Terraform]] - Security-focused deployment
- [[Step-by-Step Guide Creating an EKS Cluster with ALB Controller using Terraform Modules]] - Comprehensive EKS setup with ALB

### Kubernetes Networking

#### Ingress Controllers

- [[Practical Application of Nginx as an Ingress Controller in Kubernetes]] - Nginx ingress implementation guide
- [[Understanding Cloud Provider Managed Kubernetes Ingress Controllers]] - Overview of managed ingress solutions

#### Network Policies & Security

- [[Calico Cloud vs Kubernetes Network Policies in GitOps]] - Comparison of network policy approaches
- [[Firewalls expense]] - Cost considerations for network security

#### Overlay Networking

- [[Calico vxlan]] - Calico implementation of VXLAN overlay networking
- [[Virtual Extensible LAN]] - Overview of VXLAN technology
- [[when vxlan]] - Use cases for VXLAN overlay networks

#### Service Networking

- [[Service]] - Kubernetes Service resource detailed explanation

### Cross-Cloud Connectivity

#### AWS-Azure Integration

- [[Securely Exposing AWS EKS Service to Azure AKS]] - Pattern for secure cross-cloud service exposure
- [[EOE peering config]] - Enterprise-level peering configuration

### DNS & Service Discovery

#### DNS Configuration

- [[Fitfile DNS database]] - Overview of DNS configuration for Fitfile
- [[Analyze DNS from a data-centric perspective]] - Analytical approach to DNS management
- [[cloudflare]] - Cloudflare DNS and networking integration

#### Private DNS

- [[allow the peered VPC ec2 query the private DNS]] - DNS query patterns across VPC peering
- [[allow the peered VPC ec2 query the private DNSv2]] - Updated approach for cross-VPC DNS resolution

### Network Protocols & Fundamentals

- [[A Detailed Examination of the TCP Packet and the Encapsulation Process]] - Deep dive into TCP packet structure

### Implementation Patterns

#### AWS-Specific Patterns

- [[gateway API 1]] - Implementation pattern for Gateway API on AWS

#### Cross-Cloud Patterns

- [[Securely Exposing AWS EKS Service to Azure AKS]] - Pattern for secure cross-cloud service exposure

### Troubleshooting Guides

- Collection of common networking issues and their resolutions
  - VPC peering issues
  - DNS resolution problems
  - Ingress controller configuration challenges

### Best Practices

- Security patterns for cloud networking
- Performance optimization techniques
- Cost-effective network design principles

---

### Related Resources

- [Kubernetes Networking Documentation](https://kubernetes.io/docs/concepts/services-networking/)
- [Gateway API Website](https://gateway-api.sigs.k8s.io/)
- [AWS Networking Documentation](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- [Calico Documentation](https://docs.tigera.io/calico/latest/)
