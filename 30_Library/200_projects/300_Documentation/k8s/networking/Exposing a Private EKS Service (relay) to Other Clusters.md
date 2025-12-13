---
aliases: []
confidence: 
created: 2025-03-16T11:22:59Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:48Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ff_deploy, networking, relay]
title: Exposing a Private EKS Service (relay) to Other Clusters
type: 
uid: 
updated: 
version: 
---

You have a private AWS EKS cluster and a service called `relay` that needs to be accessible from other clusters to receive job requests and return results. Here's a comprehensive list of the components and considerations to achieve this:

## 1. Understanding the Network Topology

- Private EKS Cluster: This implies your worker nodes and potentially the control plane are in private subnets with no direct route to the public internet.
- Other Clusters: We need to consider where these "other clusters" reside. Are they in the same AWS account, different AWS accounts, or even outside of AWS? The solution might vary slightly depending on this. For this explanation, I'll primarily focus on the scenario where the other clusters are within the same or different AWS accounts within the same region.

## 2. Core Components for Exposing the Service

Given the private nature of your EKS cluster and the need for secure communication, the most suitable approach is to leverage AWS PrivateLink**. This allows you to expose your service privately without exposing it to the public internet. Here's how it works:

### 2.1. Network Load Balancer (NLB) within Your EKS Cluster's VPC

- Purpose: To distribute incoming traffic across the pods of your `relay` service.
- Type: You will need an internal Network Load Balancer (NLB). This NLB will only have private IP addresses within your VPC.
- Configuration:
    - Target Group: Configure a target group that points to the IP addresses and ports of your `relay` service pods. This requires your EKS cluster to be configured to allow the NLB to target pods directly (using IP mode for target groups). Alternatively, you can target the instance IDs of your worker nodes and the `NodePort` or `HostPort` of your `relay` service, but IP mode is generally preferred for better efficiency and scalability.
    - Listeners: Configure listeners on the NLB to listen on the appropriate ports (the ports your `relay` service uses).
    - Subnets: Ensure the NLB is deployed across the private subnets where your EKS worker nodes reside for high availability.

### 2.2. AWS PrivateLink - VPC Endpoint Service

- Purpose: To represent your internal NLB as a service that can be privately accessed by other AWS accounts and VPCs.
- Creation: You will create a VPC Endpoint Service in the VPC of your private EKS cluster.
- Association: This endpoint service will be associated with the internal NLB you created in the previous step.
- Permissions: You will need to configure the permissions for your VPC Endpoint Service to specify which AWS accounts (if the other clusters are in different accounts) are allowed to connect to it. You can also grant access to specific IAM principals within your own account.

### 2.3. AWS PrivateLink - Interface VPC Endpoints in Other Clusters' VPCs

- Purpose: To provide a private and secure connection from the other clusters' VPCs to your `relay` service.
- Creation: In each VPC where the other clusters reside, you will create an interface VPC endpoint**.
- Service Category: When creating the endpoint, you will select the "AWS services" category and then search for your VPC Endpoint Service by its name or service name (which AWS will provide after you create the endpoint service).
- Subnets: Deploy the interface VPC endpoint in private subnets within the other clusters' VPCs.
- Security Groups: Configure the security groups associated with the interface VPC endpoint to allow outbound traffic to the endpoint's private IP addresses on the ports used by your `relay` service.

### 2.4. DNS Resolution

- AWS Provided DNS: When an interface VPC endpoint is created, AWS automatically provides DNS names that can be used to reach your `relay` service. These DNS names resolve to the private IP addresses of the endpoint within the respective VPC.
- Private DNS Names (Optional but Recommended): You can enable private DNS names for your VPC Endpoint Service. This allows clients in the other VPCs to use a regional DNS name (e.g., `vpce-xxxxxxxxxxxxxxxxx.relay-service.region.vpce.amazonaws.com`) that resolves to the interface endpoint. You might also consider setting up a custom DNS record in your private DNS zone to provide a more user-friendly name.

### 2.5. Security Groups

- NLB Security Group: The security group associated with your internal NLB in the EKS cluster's VPC should allow inbound traffic on the `relay` service ports from the private IP address ranges of the VPCs where the interface VPC endpoints are created.
- EKS Worker Node Security Groups: Ensure that the security groups of your EKS worker nodes allow inbound traffic on the necessary ports from the NLB's private IP addresses.
- Interface VPC Endpoint Security Group: As mentioned earlier, this security group in the other clusters' VPCs should allow outbound traffic to the NLB's IP addresses (via the interface endpoint) on the `relay` service ports.

## 3. Alternative Approaches (Considerations)

While PrivateLink is the recommended approach for private communication, here are a couple of other options you might consider, although they might have different trade-offs:

### 3.1. AWS API Gateway with VPC Link

- Purpose: To create a managed API endpoint that acts as a front door to your `relay` service.
- Components:
    - Internal NLB (as described above): You would still likely need an internal NLB to distribute traffic within your EKS cluster.
    - VPC Link: You would create a VPC Link in API Gateway that connects to your internal NLB.
    - API Gateway Endpoint: You would create an API Gateway (either HTTP API or REST API) and configure routes to forward requests to the VPC Link.
- Pros: Offers more control over the API interface, authentication, authorization, request/response transformation, and rate limiting.
- Cons: Adds complexity and cost compared to a direct PrivateLink connection.

### 3.2. Service Mesh (e.g., Istio with Gateway)

- Purpose: To provide advanced traffic management, security, and observability across your clusters.
- Components: You could potentially use a service mesh with a gateway deployed in your private EKS cluster and expose it via an internal NLB and PrivateLink.
- Pros: Provides rich features for inter-cluster communication, including mutual TLS, traffic routing rules, and observability.
- Cons: Can be significantly more complex to set up and manage, potentially overkill for a simple job queue.

## 4. Specific Considerations for a Job Queue (`relay`)

- Statelessness: Ensure your `relay` service is designed to be stateless or handles state appropriately, as you will be load balancing across multiple instances.
- Idempotency: If the job submission process involves network communication, consider making the API calls idempotent to handle potential retries.
- Authentication and Authorization: Implement robust authentication and authorization mechanisms to ensure only authorized clusters can submit jobs to your `relay` service. This could involve IAM roles, API keys, or other security measures.
- Request/Response Format: Define a clear and consistent format for job requests and result responses.
- Monitoring and Logging: Set up comprehensive monitoring and logging for all the components involved (NLB, PrivateLink endpoints, `relay` service) to track performance, identify issues, and ensure the reliability of your job queue.

## 5. Step-by-Step Implementation Outline (Using PrivateLink)

1.  Deploy `relay` service in your private EKS cluster. Ensure it's running and accessible within the cluster's network.
2.  Create an internal Network Load Balancer (NLB) in your EKS cluster's VPC. Configure it with a target group pointing to your `relay` service pods (using IP mode if possible) and a listener on the appropriate port.
3.  Create a VPC Endpoint Service in your EKS cluster's VPC and associate it with the internal NLB.
4.  Configure permissions for the VPC Endpoint Service to allow connections from the AWS accounts (if applicable) where the other clusters reside.
5.  In each of the other clusters' VPCs, create an interface VPC endpoint. Select the "AWS services" category and find your VPC Endpoint Service. Choose the subnets where you want to deploy the endpoint.
6.  Configure security groups for the NLB, EKS worker nodes, and the interface VPC endpoints to allow the necessary traffic flow.
7.  Obtain the DNS names for the interface VPC endpoints in the other clusters' VPCs.
8.  Test connectivity from the other clusters to your `relay` service using the DNS names of the interface VPC endpoints.

By following these steps, you can securely and privately expose your `relay` service running in your private EKS cluster to other clusters using AWS PrivateLink. This approach minimizes exposure to the public internet and provides a reliable and scalable solution for inter-cluster communication. Remember to tailor the security group rules and permissions to your specific requirements.
