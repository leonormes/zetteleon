---
aliases: []
confidence: 
created: 2024-03-19T12:00:00Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:43Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, azure, ff_deploy, k8s, networking]
title: Cross-Cloud Kubernetes Networking Documentation Index
type: index
uid: 
updated: 
version: 
---

This index provides links to documentation related to networking between AWS EKS and Azure AKS Kubernetes clusters.

## Core Implementation Documents

### Secure Network Plan

- [[Secure Network Plan Azure AKS (Bunny) to AWS EKS (Relay) Communication]] - Comprehensive guide for establishing secure communication between public AKS and private EKS clusters
  - Includes VPN tunnel setup
  - Security configurations
  - Implementation steps
  - Architecture diagrams

### Cross-Cloud Networking Overview

- [[cross_cloud_networking]] - High-level overview of networking Kubernetes clusters across cloud providers
  - Cluster federation concepts
  - Infrastructure requirements
  - General networking considerations

## Private Cluster Configuration

### Ingress and Security

- [[Secure Cross-Cloud Communication Between AWS EKS and Azure AKS for Task Distribution]] - Configuration details for private cluster ingress
  - TLS setup
  - Certificate management
  - Security best practices

### Work Plan

- [[Work Plan Secure Cross-Cloud Communication between Private EKS and AKS Clusters]] - Detailed implementation plan
  - Credential management
  - Security considerations
  - Step-by-step implementation guide

## Related Documentation

### General Kubernetes Networking

- [[Learn Me That Network]] - Foundational Kubernetes networking concepts
- [[Why And How Of Kubernetes Ingress (And Networking)]] - Ingress controller and networking basics

### Cloud-Specific Documentation

- [[Why kubernetes is a good choice]] - Overview of Kubernetes benefits across cloud providers
- [[QU - What is the difference between AWS and Azure IP management on K8s clusters]] - IP management differences between cloud providers

## Implementation Components

### Network Architecture

- VPN Gateway setup
- VPC/VNet configuration
- Subnet management
- Security groups and NSGs

### Security

- Network policies
- Service-level security
- Monitoring and logging
- Certificate management

### DNS Configuration

- Private DNS zones
- Service discovery
- DNS forwarding

## Best Practices

- Network segmentation
- Least privilege access
- Regular security audits
- Monitoring and alerting
- Backup and recovery procedures

## Alternatives

- AWS Direct Connect
- Azure ExpressRoute
- Cloud-native interconnect options
