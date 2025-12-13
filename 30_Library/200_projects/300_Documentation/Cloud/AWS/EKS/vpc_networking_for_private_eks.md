---
aliases: []
confidence: 
created: 2025-02-07T12:57:53Z
depends_on:
  - name: deployment_phases
    type: documentation
    reason: Defines the overall deployment structure
    doc_link: "[deployment_phases](deployment_phases.md)"
  - name: terraform_cloud_projects
    type: tooling
    reason: Required for infrastructure state management and deployment
    doc_link: "[terraform_cloud_projects](terraform_cloud_projects.md)"
  - name: aws_account_setup
    type: tooling
    reason: Required for AWS resource creation
    doc_link: "[aws_account_setup](aws_account_setup)"
deployment_phase: 2
description: VPC configuration for private EKS cluster
epistemic: 
iac_path:
  - repo: terraform-aws-eks-private
    path: modules/vpc2
    main_file: main.tf
last_reviewed: 
modified: 2025-12-13T11:39:52Z
name: vpc_networking_for_private_eks
phase_order:
  phase: 2
  step: 1
  next_steps:
    - vpc_endpoints
    - jumpbox
purpose: 
required_configurations:
  - name: CIDR ranges
    description: Network CIDR block allocations
  - name: AWS region
    description: Target deployment region
  - name: TFC workspace
    description: Terraform Cloud workspace configuration
required_resources:
  - type: aws_service
    name: vpc
    reason: Base networking infrastructure
  - type: aws_service
    name: ec2
    reason: Required for VPC endpoints
  - type: external_service
    name: terraform_cloud
    reason: Required for state management and deployment
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, ff_deploy, networking, vpc]
title: vpc_networking_for_private_eks
type: infrastructure
uid: 
updated: 
verification_steps:
version: 1
---

## vpc_networking_for_private_eks

Information about using the CIDR range 10.1.0.0/16 for an AWS VPC that will host a private EKS cluster.

### CIDR Range Analysis

The CIDR range 10.1.0.0/16 is a private IP address range that falls within the

- Total IP addresses: 65,536 (2^16)
- Usable IP addresses: 65,531 (AWS reserves 5 IP addresses in each subnet)
- First IP: 10.1.0.0
- Last IP: 10.1.255.255
- Subnet mask: 255.255.0.0

This range provides ample space for subnetting and allocating IP addresses to various resources within your EKS cluster.

### VPC Design for Private EKS Cluster

When designing the VPC for a private EKS cluster using this CIDR range, consider the following:

#### Subnet Distribution

1. Private Subnets: Allocate at least two private subnets across different Availability Zones (AZs) for high availability. For example:
   - 10.1.0.0/19 (8,192 IPs) in AZ-a
   - 10.1.32.0/19 (8,192 IPs) in AZ-b

2. Public Subnets: Even for a private cluster, it's recommended to have public subnets for
   - 10.1.192.0/20 (4,096 IPs) in AZ-a
   - 10.1.208.0/20 (4,096 IPs) in AZ-b

#### VPC Endpoints

For a private EKS cluster, you'll need to set up VPC endpoints to allow communication with AWS services without internet access. Some essential endpoints include:

- com.amazonaws.region.ecr.api
- com.amazonaws.region.ecr.dkr
- com.amazonaws.region.s3
- com.amazonaws.region.logs
- com.amazonaws.region.sts
- com.amazonaws.region.eks

### EKS Cluster Configuration

When creating the EKS cluster:

1. Enable private endpoint access for the Kubernetes API server.
2. Optionally, disable public endpoint access for enhanced security.
3. Place worker nodes in the private subnets.
4. Configure the cluster security group to allow necessary inbound and outbound traffic.

### Networking Considerations

1. IP Address Management: The Amazon VPC CNI plugin allocates IP addresses to Pods from the node's subnet. Ensure your subnets have enough available IP addresses.
2. Maximum Pods per Node: The number of Pods per node is limited by the available IP addresses in the subnet. Plan your node and Pod density accordingly.
3. NAT Gateways: Deploy NAT Gateways in the public subnets to allow outbound internet access from private subnets if required.
4. Load Balancers: For ingress traffic, use internal load balancers placed in the private subnets.
5. VPC Peering or Transit Gateway: Consider setting up VPC peering or a transit gateway for communication with other VPCs or on-premises networks.

### Security Measures

1. Implement strict security group rules to control traffic flow.
2. Use Network ACLs as an additional layer of network security.
3. Enable VPC Flow Logs for network traffic monitoring and troubleshooting.
4. Implement AWS PrivateLink for secure access to AWS services.

### Scalability and Future Growth

The chosen CIDR range (10.1.0.0/16) provides room for future expansion. However, plan your subnet allocations carefully to accommodate potential growth in node count, Pod density, and additional services.

By following these guidelines, you can create a well-structured, secure, and scalable network architecture for your private EKS cluster using the 10.1.0.0/16 CIDR range. Remember to always adhere to AWS and Kubernetes best practices for networking and security.

When planning for node count growth and pod density in a Kubernetes cluster, it's important to consider both current needs and future scalability. Here are some key considerations and rules of thumb to help you plan effectively:

### Node Count Growth

#### Initial Sizing

Start with a conservative number of nodes based on your current workload requirements. A common starting point is 3-5 nodes across multiple availability zones for high availability.

#### Scalability Buffer

Plan for a 20-30% buffer in node capacity to accommodate sudden spikes in workload or temporary failures. This buffer allows for smoother scaling and reduces the frequency of cluster autoscaling events.

#### Node Group Strategy

Multiple Node Groups: Use multiple node groups to separate workloads with different resource requirements or to isolate specific applications. This approach provides more flexibility in scaling and resource allocation.

Limit Node Groups: While multiple node groups are useful, aim to keep the total number of node groups below 10 if possible. Too many node groups can impact the performance of the Cluster Autoscaler.

### Pod Density

#### Optimal Pod Density

A general rule of thumb is to aim for 30-50 pods per node. This range balances efficient resource utilization with manageable complexity.

#### Consider Node Capacity

Be aware of the maximum number of pods a node can support. For example, Amazon EKS limits pods per node based on instance type, ranging from 4 to 737 pods.

### Rules of Thumb for Future-Proofing

1. Overestimate Initial Capacity: Start with more capacity than you think you need. It's easier to scale down than to hurriedly scale up during a traffic spike.
2. Use Cluster Autoscaler: Implement Cluster Autoscaler to automatically adjust the number of nodes based on resource demands. This helps maintain an efficient balance between resource utilization and availability.
3. Implement Pod Disruption Budgets: Use Pod Disruption Budgets to ensure high availability during node scaling or maintenance operations.
4. Regular Capacity Reviews: Schedule quarterly reviews of your cluster capacity and adjust your scaling strategies accordingly.
5. Monitor Resource Utilization: Implement robust monitoring to track CPU, memory, and network usage across nodes and pods. This data will inform your scaling decisions.
6. Use Horizontal Pod Autoscaler: Implement Horizontal Pod Autoscaler to automatically scale the number of pods based on observed metrics, which can help optimize resource usage before scaling nodes.
7. Consider Mixed Instance Types: Use mixed instance types in your node groups to balance cost and performance, especially when using spot instances.
8. Plan for Multi-AZ Distribution: Distribute nodes across multiple Availability Zones for better fault tolerance and to avoid capacity constraints in a single AZ.
9. Implement Resource Quotas: Use namespace resource quotas to prevent a single team or application from consuming all cluster resources, which could impact scalability for others.
10. Optimize Container Images: Use smaller, optimized container images to reduce node startup time and improve scalability.

By following these guidelines and regularly reviewing your cluster's performance and capacity, you can create a scalable and efficient Kubernetes infrastructure that can grow with your needs while minimizing future rework. Remember that these are general guidelines, and you should always tailor your approach to your specific use case and workload characteristics.
