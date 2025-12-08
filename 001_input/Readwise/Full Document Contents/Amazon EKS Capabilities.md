---
aliases: []
confidence: 
created: 2025-12-08T07:34:19Z
epistemic: 
last_reviewed: 
modified: 2025-12-08T11:11:56Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [articles]
title: Amazon EKS Capabilities
type: 
uid: 
updated: 
---

## Amazon EKS Capabilities

![rw-book-cover](https://docs.aws.amazon.com/assets/images/favicon.ico)

### Metadata
- Author: [[Amazon EKS Document History]]
- Full Title: Amazon EKS Capabilities
- Category: #articles
- Summary: Amazon EKS now provides fully managed cluster capabilities with EKS Capabilities, with support for declarative continuous deployment with support for Argo CD, AWS resource management with support for AWS Controllers for Kubernetes, and Kubernetes resource composition and orchestration with support for Kube Resource Orchestrator.
- URL: <https://docs.aws.amazon.com/eks/latest/userguide/capabilities.html>

### Full Document
**Help improve this page**

To contribute to this user guide, choose the **Edit this page on GitHub** link that is located in the right pane of every page.

#### EKS Capabilities

Amazon EKS Capabilities is a layered set of fully managed cluster features that help accelerate developer velocity and offload the complexity of building and scaling with Kubernetes.

EKS Capabilities are Kubernetes-native features for declarative continuous deployment, AWS resource management, and Kubernetes resource authoring and orchestration-all fully managed by AWS.

With EKS Capabilities, you can focus more on building and scaling your workloads, offloading the operational burden of these foundational platform services to AWS.

These capabilities run within EKS rather than in your clusters, eliminating the need to install, maintain, and scale critical platform components on your worker nodes.

To get started, you can create one or more EKS Capabilities on a new or existing EKS cluster.

To do this, you can use the AWS CLI, the AWS Management Console, EKS APIs, eksctl, or your preferred infrastructure-as-code tools.

While EKS Capabilities are designed to work together, they are independent cloud resources that you can pick and choose based on your use case and requirements.

All Kubernetes versions supported by EKS are supported for EKS Capabilities.

EKS Capabilities are available in all AWS commercial Regions where Amazon EKS is available.

For a list of supported Regions, see [Amazon EKS endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/eks.html) in the AWS General Reference.

##### Available Capabilities

###### AWS Controllers for Kubernetes (ACK)

ACK enables the management of AWS resources using Kubernetes APIs, allowing you to create and manage S3 buckets, RDS databases, IAM roles, and other AWS resources using Kubernetes custom resources.

ACK continuously reconciles your desired state with the actual state in AWS, correcting any drift over time in order to keep your system healthy and your resources configured as specified.

You can manage AWS resources alongside your Kubernetes workloads using the same tools and workflows, with support for more than 50 AWS services including S3, RDS, DynamoDB, and Lambda.

ACK supports cross-account and cross-region resource management, enabling complex multi-account, multi-cluster system management architectures.

ACK supports read-only resources and read-only adoption, facilitating migration from other infrastructure as code tools into your Kubernetes-based systems.

[Learn more about ACK →](./ack.html)

###### Argo CD

Argo CD implements GitOps-based continuous deployment for your applications, using Git repositories as the source of truth for your workloads and system state.

Argo CD automatically syncs application resources to your clusters from your Git repositories, detecting and remdiating drift to ensure your deployed applications match your desired state.

You can deploy and manage applications across multiple clusters from a single Argo CD instance, with automated deployment from Git repositories whenever changes are committed.

Using Argo CD and ACK together provides a foundational GitOps system, simplifying workload dependency management as well as supporting whole-system designs including cluster and infrastructure management at scale.

Argo CD integrates with AWS Identity Center for authentication and authorization, and provides a hosted Argo UI for visualizing application health and deployment status.

[Learn more about Argo CD →](./argocd.html)

###### Kro (Kube Resource Orchestrator)

kro enables you to create custom Kubernetes APIs that compose multiple resources into higher-level abstractions, allowing platform teams to define reusable patterns for common resource combinations-cloud building blocks.

With kro, you can compose both Kubernetes and AWS resources together into unified abstractions, using simple syntax to enable dynamic configurations and conditional logic.

kro enables platform teams to provide self-service capabilities with appropriate guardrails, allowing developers to provision complex infrastructure using simple, purpose-built APIs while maintaining organizational standards and best practices.

kro resources are simply Kubernetes resources, and are specified in Kubernetes manifests which can be stored in Git, or pushed to OCI-compatible registries like Amazon ECR for broad organizational distribution.

[Learn more about kro →](./kro.html)

##### Benefits of EKS Capabilities

EKS Capabilities are fully managed by AWS, eliminating the need for installation, maintenance, and scaling of foundational cluster services.

AWS handles security patching, updates, and operational management, freeing your teams to focus on building with AWS rather than on cluster operations.

Unlike traditional Kubernetes add-ons that consume cluster resources, capabilities run in EKS rather than on your worker nodes.

This frees up cluster capacity and resources for your workloads while minimizing the operational burden of managing in-cluster controllers and other platform components.

With EKS Capabilities, you can manage deployments, AWS resources, custom Kubernetes resources, and compositions using native Kubernetes APIs and tools like `kubectl`.

All capabilities operate in the context of your clusters, automatically detecting and correcting configuration drift in both application and cloud infrastructure resources.

You can deploy and manage resources across multiple clusters, AWS accounts, and regions from a single control point of control, simplifying operations in complex, distributed environments.

EKS Capabilities are designed for GitOps workflows, providing declarative, version-controlled infrastructure and application management.

Changes flow from Git through the system, providing audit trails, rollback capabilities, and collaboration workflows that integrate with your existing development practices.

This Kubernetes-native approach means you don’t need to use multiple tools or manage infrastructure-as-code systems external to your clusters, and there is a single source of truth to refer to.

Your desired state, defined in version-controlled Kubernetes declarative configuration, is continuously enforced across your environment.

##### Pricing

With EKS Capabilities, there are no upfront commitments or minimum fees.

You are charged for each capability resource for each hour it is active on your Amazon EKS cluster.

Specific Kubernetes resources managed by EKS Capabilities are also billed at an hourly rate.

For current pricing information, see the [Amazon EKS pricing page](https://aws.amazon.com/eks/pricing/).

You can use AWS Cost Explorer and Cost and Usage Reports to track capability costs separately from other EKS charges.

You can tag your capabilities with cluster name, capability type, and other details for cost allocation purposes.

##### How EKS Capabilities Work

Each capability is an AWS resource that you create on your EKS cluster.

Once created, the capability runs in EKS and is fully managed by AWS.

You can create one capability resource of each type (Argo CD, ACK, and kro) for a given cluster.

You cannot create multiple capability resources of the same type on the same cluster.

You interact with capabilities in your cluster using standard Kubernetes APIs and tools:

Some capabilities have additional tools supported. For example:

Capabilities are designed to work together but are independent and fully opt-in.

You can enable one, two, or all three capabilities based on your needs, and update your configuration as your requirements evolve.

All EKS Compute types are supported for use with EKS Capabilities. For more information, see [Manage compute resources by using nodes](./eks-compute.html).

For security configuration and details on IAM roles, see [Security considerations for EKS Capabilities](./capabilities-security.html).

For multi-cluster architecture patterns, see [EKS Capabilities considerations](./capabilities-considerations.html).

##### Common Use Cases

**GitOps for Applications and Infrastructure**

Use Argo CD to deploy applications and ACK to provision infrastructure, both from Git repositories.

Your entire stack—applications, databases, storage, and networking—is defined as code and automatically deployed.

Example: A development team pushes changes to Git.

Argo CD deploys the updated application, and ACK provisions a new RDS database with the correct configuration.

All changes are auditable, reversible, and consistent across environments.

**Platform Engineering with Self-Service**

Use kro to create custom APIs that compose ACK and Kubernetes resources.

Platform teams define approved patterns with guardrails.

Application teams use simple, high-level APIs to provision complete stacks.

Example: A platform team creates a "WebApplication" API that provisions a Deployment, Service, Ingress, and S3 bucket.

Developers use this API without needing to understand the underlying complexity or AWS permissions.

**Multi-Cluster Application Management**

Use Argo CD to deploy applications across multiple EKS clusters in different regions or accounts.

Manage all deployments from a single Argo CD instance with consistent policies and workflows.

Example: Deploy the same application to development, staging, and production clusters across multiple regions.

Argo CD ensures each environment stays in sync with its corresponding Git branch.

**Multi-Cluster Management**

Use ACK to define and provision EKS clusters, kro to customize cluster configurations with organizational standards, and Argo CD to manage cluster lifecycle and configuration.

This provides end-to-end cluster management from creation through ongoing operations.

Example: Define EKS clusters using ACK and kro to provision and manage cluster infrastructure, defining organizational standards for networking, security policies, add-ons and other configuration.

Use Argo CD to create and continuously manage clusters, configuration, and Kubernetes version updates across your fleet leveraging consistent standards and automated lifecycle management.

**Migrations and Modernization**

Simplify migration to EKS with native cloud resource provisioning and GitOps workflows.

Use ACK to adopt existing AWS resources without recreating them, and Argo CD to operationalize workload deployments from Git.

Example: A team migrating from EC2 to EKS adopts their existing RDS databases and S3 buckets using ACK, then uses Argo CD to deploy containerized applications from Git.

The migration path is clear, and operations are standardized from day one.

**Account and Regional Bootstrapping**

Automate infrastructure rollout across accounts and regions using Argo CD and ACK together.

Define your infrastructure as code in Git, and let capabilities handle the deployment and management.

Example: A platform team maintains Git repositories defining standard account configurations—VPCs, IAM roles, RDS instances, and monitoring stacks.

Argo CD deploys these configurations to new accounts and regions automatically, ensuring consistency and reducing manual setup time from days to minutes.
