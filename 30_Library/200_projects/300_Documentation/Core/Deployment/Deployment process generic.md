---
aliases: []
confidence: 
created: 2025-02-07T12:57:55Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:45Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ff_deploy]
title: Deployment process generic
type: 
uid: 
updated: 
version: 
---

Let me break down the deployment process described in these documents. The deployment follows a structured approach across multiple cloud services and tools.

The overall deployment process consists of four main phases:

First Phase - Tooling Configuration

The process begins with setting up central services tooling. This involves configuring HashiCorp Vault, Auth0, and Grafana. A deployment key (a short, consistent name like "WM-Prod") is used to identify the customer deployment across all infrastructure components. The tooling phase includes creating necessary secrets in Vault, setting up authentication mechanisms in Auth0, and configuring monitoring through Grafana.

Second Phase - Infrastructure Deployment

The infrastructure deployment varies depending on whether you're using AWS or Azure. For AWS, the process involves:

Creating a Terraform Cloud workspace with the deployment key and configuring AWS credentials. A private GitLab repository is created to store the infrastructure code, using terraform-aws-eks-private as a template. The deployment creates an EKS cluster, networking components, and a jumpbox for secure access.

For Azure, there's a similar process but with Azure-specific components:

Setting up a Terraform Cloud workspace, configuring Azure credentials (ARM keys), and creating an Azure Kubernetes Service (AKS) cluster. The infrastructure includes private networking, managed identities, and necessary resource providers.

Third Phase - Platform Configuration

After infrastructure deployment, the platform configuration involves setting up the Kubernetes cluster with necessary components. This includes:

Setting up storage classes, configuring CoreDNS for internal routing, deploying an ingress controller, and establishing secure communications. ArgoCD is deployed for GitOps-based management of the cluster. The platform configuration also involves setting up role-based access control and connecting to the previously configured Vault instance for secrets management.

Fourth Phase - Application Deployment

The final phase involves deploying the actual application components. This is managed through ArgoCD, which pulls configuration from the deployment repository. The application deployment uses secrets stored in Vault and authentication configured in Auth0.

Throughout all phases, security is a key consideration:

- Private networking is used for cluster communication
- Jumpboxes provide secure access to the clusters
- Secrets are managed centrally through Vault
- Authentication is handled through Auth0
- All sensitive credentials are marked as sensitive in Terraform

The process is designed to be reproducible and consistent across different customer deployments, with the deployment key serving as a unique identifier throughout the system. The documentation emphasizes the importance of maintaining consistency in naming and configuration across all components of the infrastructure.

A notable aspect is the flexibility built into the system to accommodate different customer requirements, such as various types of network configurations (loadBalancer, userDefinedRouting, or NATGateway) and different VM sizes for the compute resources.

Would you like me to elaborate on any particular phase or component of this deployment process?
