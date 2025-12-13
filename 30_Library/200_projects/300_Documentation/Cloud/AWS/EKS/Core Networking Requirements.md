---
aliases: []
confidence: 
created: 2025-02-07T12:57:53Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:52Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ff_deploy, networking]
title: Core Networking Requirements
type: config
uid: 
updated: 
version: 1
---

## 1. Core Networking Requirements

At the foundation of any EKS deployment is a robust and correctly configured network. Here’s what that entails:

- Virtual Private Cloud (VPC): Amazon EKS integrates with Amazon VPC, which allows you to use your own VPC security groups and network access control lists (ACLs). You must choose an existing VPC that meets EKS requirements or create one, and it's important to note that once chosen, you cannot change the VPC associated with your cluster. If you don't have a VPC, you can create one using an AWS CloudFormation template provided by Amazon EKS.
- Subnets: When you create an EKS cluster, you must specify at least two subnets that reside in different Availability Zones. All available subnets in your chosen VPC are preselected by default, but you must ensure you have at least two selected. The subnets you select must meet Amazon EKS subnet requirements, and it is advisable to familiarize yourself with these requirements before selecting your subnets.
- Public vs. Private Subnets: Subnets can be either public or private, with a public subnet having a route to an internet gateway and a private subnet not having such a route. For nodes to connect to the control plane using only the public endpoint, they must have a public IP address and a route to an internet gateway or a NAT gateway.
- VPC Endpoints: If your nodes are in private subnets and do not have a route to a NAT device, you'll need to add VPC endpoints using AWS PrivateLink. This is essential for your nodes and pods to communicate with AWS services such as Amazon ECR, Elastic Load Balancing, and Amazon S3. Not all AWS services support VPC endpoints.

## 2. Security Groups

Security groups act as virtual firewalls to control traffic to and from your EKS resources. Here's what you need to know:

- EKS Managed Security Group: Whether you specify security groups or not, Amazon EKS creates a security group that allows communication between your cluster and your VPC.
- Optional Security Groups: You can specify additional security groups that you want Amazon EKS to associate with the network interfaces it creates.
- Control Plane Security Group: If connecting to your cluster from a connected network, you must ensure that your EKS control plane security group contains rules to allow inbound traffic on port 443 from the connected network. The same applies when using a bastion host.
- Outbound Rules: Your cluster's security group needs outbound rules to allow traffic to the cluster security group on TCP port 443, TCP port 10250, and DNS traffic on TCP and UDP port 53.
- Inter-node Communication: You also need to add rules for the protocols and ports that your nodes will use for inter-node communication.

## 3. Internet Access

The level of internet access needed for your nodes depends on how you've configured your cluster:

- Public Internet Access: If your nodes have public IP addresses, they can directly access the internet. If your cluster uses the public endpoint, nodes will require a route to the internet gateway or a NAT gateway to communicate with the control plane.
- Limited Internet Access: If your cluster does not have outbound internet access, it must be configured to pull images from a container registry within your VPC. You can use Amazon Elastic Container Registry (ECR) for this.
- Private Clusters: If you're deploying a private cluster, you'll need VPC endpoints for all the AWS services your nodes and pods need to access if they do not have internet access.

## 4. Hybrid Node Networking

When incorporating hybrid nodes, there are additional networking considerations:

- Reliable Connection: Hybrid nodes require a reliable connection between your on-premises environment and AWS. They aren't suitable for disconnected or intermittent environments.
- VPC and Subnet Routing: Communication between the EKS control plane and hybrid nodes is routed through the VPC and subnets you choose when creating your cluster.
- Connectivity Options: Various methods can connect your on-premises networks to a VPC including AWS Site-to-Site VPN and AWS Direct Connect.
- IP Address Family: Hybrid nodes can only be used with Amazon EKS clusters configured with the IPv4 IP address family.
- On-premises CIDRs: Your on-premises node and pod CIDRs must be IPv4 RFC1918 CIDR blocks.
- Inbound and Outbound Access: You need to enable inbound network access from the EKS control plane to your on-premises environment and outbound access for your hybrid nodes to communicate with the EKS control plane.
- Minimum Bandwidth and Latency: AWS recommends reliable network connectivity of at least 100 Mbps with a maximum of 200ms round trip latency.
- CIDR Blocks: Your on-premises node and pod CIDR blocks must not overlap with each other, the VPC CIDR for your EKS cluster, or your Kubernetes service IPv4 CIDR.
- VPC Routing: Your VPC must have routes in its routing table for your on-premises node and pod CIDRs, and these routes should direct traffic to the gateway you're using for your hybrid network connectivity.
- Security Groups for Hybrid Nodes: When using hybrid nodes, one of the security groups must have inbound rules for your on-premises node and pod CIDRs.
- Remote Node and Pod Networks: You must provide your on-premises node and pod CIDRs during EKS cluster creation. You must use the API fields `RemoteNodeNetwork` and `RemotePodNetwork`.
- DNS Requirements: Your VPC must have DNS hostname and DNS resolution support.

## 5. Key Takeaways

- VPC and Subnets: Choose an existing VPC or create a new one, ensuring it has the necessary subnets in multiple availability zones.
- Security Groups: Ensure you have security groups configured correctly, controlling both inbound and outbound traffic to your cluster.
- Internet Access: Manage internet access depending on whether you are using a public or private cluster. Use VPC endpoints or private registries as needed.
- Hybrid Nodes: Pay special attention to hybrid node requirements, including setting up network connectivity, configuring CIDR blocks, and defining routes.

To ensure your network setup is correct, it’s crucial to have a thorough understanding of these requirements before deploying a cluster. If you're not familiar with Amazon EKS networking, it is recommended to consult the 'De-mystifying cluster networking for Amazon EKS worker nodes' resource.
