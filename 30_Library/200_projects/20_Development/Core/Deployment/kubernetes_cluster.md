---
aliases: []
confidence: 
created: 2025-02-07T12:57:55Z
depends_on:
  - name: 'deployment_phases type: documentation reason: "Defines the overall deployment structure" doc_link: "[deployment_phases](deployment_phases.md)"'
  - name: 'vpc_networking_for_private_eks type: infrastructure reason: "Required for cluster networking" doc_link: "[vpc_networking_for_private_eks](vpc_networking_for_private_eks.md)"'
  - name: 'vpc_endpoints type: infrastructure reason: "Required for private cluster communication with AWS services" doc_link: "[vpc_endpoints](vpc_endpoints)"'
  - name: 'jumpbox type: infrastructure reason: "Required for cluster access" doc_link: "[jumpbox](jumpbox)"'
deployment_phase: 3
description: EKS cluster deployment with node groups
epistemic: 
estimated_duration: 45m
iac_path:
  - repo: "terraform-aws-eks-private path: modules/eks main_file: main.tf"
id: kubernetes_cluster
last_reviewed: 
modified: 2025-12-13T11:39:45Z
name: kubernetes_cluster
phase_order:
  next_steps:
    - container_registry
    - key_management_service
    - monitoring_infrastructure
  phase: 3
  step: 1
purpose: 
required_configurations:
  - name: 'Node groups configuration description: "Worker node instance types and sizes"'
  - name: 'IAM roles description: "Cluster and node group IAM roles"'
  - name: 'Security groups description: "Cluster and node security groups"'
required_resources:
  - type: 'aws_service name: eks reason: "Core EKS service"'
  - type: 'aws_service name: ec2 reason: "For worker nodes"'
  - type: 'aws_service name: ecr reason: "For container images"'
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: kubernetes_cluster
type: infrastructure
uid: 
updated: 
version:
---

## Kubernetes Cluster

This document describes the EKS cluster deployment process and requirements.

### Prerequisites

Before deploying the EKS cluster, ensure Phase 2 (Core Infrastructure) is complete:

1. VPC and networking infrastructure is deployed and verified
2. VPC endpoints are configured and tested
3. Jumpbox is available and accessible

### Deployment Process

1. Apply the EKS module configuration
2. Wait for cluster creation (approximately 15-20 minutes)
3. Deploy node groups
4. Configure cluster access and security

### Configuration Details

The cluster uses the following node groups:

- SystemNodeGroup: For system workloads
- WorkflowsNodeGroup: For workflow-specific workloads

See the IaC path for detailed configuration.

### Next Steps

After successful cluster deployment:

1. Deploy container registry
2. Set up key management service
3. Configure monitoring and logging infrastructure
