---
aliases: []
confidence: 
created: 2025-02-22T11:31:00Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, ff_deploy, networking, peering, vpc]
title: allow the peered VPC ec2 query the private DNSv2
type: instruction
uid: f8412ceb-e64d-4def-a7e6-eb8f10b7f4c8
updated: 
version: 2
---

## Understanding The Setup

- Private EKS Cluster: Your EKS cluster is running in two private subnets (AZs) within your primary VPC (`vpc-0aabc42188b2162bf` in the screenshot).
- Peered VPC: You have another VPC that needs to access a web application running in your EKS cluster.
- EC2 Instance: The EC2 instance in the peered VPC will initiate the connection.
- Security Goal: Establish secure and reliable access, minimizing the attack surface.

## Routing Considerations

You need to explicitly set up routing for both AZ subnets to ensure high availability and fault tolerance. Here's why and how:

1. High Availability: EKS distributes pods across multiple AZs. If you only route to one AZ, you risk losing connectivity if that AZ experiences an issue.
2. Load Balancing: Even if you use an internal load balancer (which you should for EKS), the load balancer distributes traffic across the target group, which includes instances in both AZs.
3. Explicit Routing: You must explicitly define routes in the peered VPC's route table to direct traffic to both EKS subnets.

### Your VPC Details

- VPC ID: `vpc-0aabc42188b2162bf`
- VPC Name: `eoe-sde-codisc`
- IPv4 CIDR: `10.65.0.0/20`

### Peering Connection Details

- Peering Connection ID: `pcx-06524c8e180979086`
- Requester VPC ID: `vpc-0d9a8634e304211bd`

## Steps To Configure Secure Routing

### 1. Create A VPC Peering Connection
- Action: The VPC peering connection between `vpc-0aabc42188b2162bf` (your VPC) and `vpc-0d9a8634e304211bd` (the peered VPC) is already established and active (`pcx-06524c8e180979086`).
### 2. Modify Route Tables in the Peered VPC (`vpc-0d9a8634e304211bd`)

- Action: Identify the route table associated with the subnet where your EC2 instance resides in `vpc-0d9a8634e304211bd`.
- Add Two New Routes:
 - Route 1:
	  - Destination: The CIDR block of your first EKS subnet (`subnet-02b4bec3447cbbf9e`). This is the same as before.
	  - Target: `pcx-06524c8e180979086` (Your Peering Connection ID).
 - Route 2:
	  - Destination: The CIDR block of your second EKS subnet (`subnet-0c3d71c782e12d044`). This is the same as before.
	  - Target: `pcx-06524c8e180979086` (Your Peering Connection ID).
 - Important: You might also need to add a route for the entire VPC CIDR if you have resources that need to be accessed outside the EKS subnets.
	  - Route 3 (Optional):
		- Destination: `10.65.0.0/20` (Your VPC CIDR)
		- Target: `pcx-06524c8e180979086` (Your Peering Connection ID).
### 3. Modify Security Groups

- EKS Security Groups (Associated with `vpc-0aabc42188b2162bf`):
 - Action: Identify the security group(s) associated with your EKS worker nodes or the load balancer.
 - Add Inbound Rule:
	  - Source: The CIDR block of `vpc-0d9a8634e304211bd` (the peered VPC).
	  - Protocol: TCP (or the protocol your application uses).
	  - Port: The port your web application is listening on (e.g., 80 or 443).
- EC2 Security Group (Associated with `vpc-0d9a8634e304211bd`):
 - Action: Identify the security group associated with your EC2 instance in `vpc-0d9a8634e304211bd`.
 - Add Outbound Rule:
	  - Destination: The CIDR blocks of your two EKS subnets (`subnet-02b4bec3447cbbf9e` and `subnet-0c3d71c782e12d044`).
	  - Protocol: TCP (or the protocol your application uses).
	  - Port: The port your web application is listening on (e.g., 80 or 443).
 - Optional Outbound Rule:
	  - Destination: `10.65.0.0/20` (Your VPC CIDR).
	  - Protocol: TCP (or the protocol your application uses).
	  - Port: The port your web application is listening on (e.g., 80 or 443).Internal Load Balancer (Recommended):
### 4. Internal Load Balancer (Recommended)

- Use an internal Network Load Balancer (NLB) or Application Load Balancer (ALB) for your EKS service.
- This load balancer will distribute traffic across your EKS pods in both AZs, ensuring high availability and load balancing.
- Ensure the security group of the NLB or ALB allows traffic from the peered VPC.
- Action: Use an internal Network Load Balancer (NLB) or Application Load Balancer (ALB) for your EKS service.
- Security Group: Ensure the security group of the NLB or ALB allows traffic from the CIDR block of `vpc-0d9a8634e304211bd`.

### 5. DNS Resolution

- Action: If you are using a custom domain name, ensure DNS resolution is correctly configured.
- Consider: Route 53 private hosted zones or DNS forwarding.
- If you are using a custom domain name for your web application, ensure that DNS resolution is correctly configured.
- For private EKS, you might need to use Route 53 private hosted zones or configure DNS forwarding to resolve the internal load balancer's DNS name.

## Route Table Configuration (Peered VPC - `vpc-0d9a8634e304211bd`)

|                                           |                                                                          |
| ----------------------------------------- | ------------------------------------------------------------------------ |
| Destination                           | Target                                                               |
| `subnet-02b4bec3447cbbf9e` (EKS subnet 1) | `pcx-06524c8e180979086` (Peering Connection ID)                          |
| `subnet-0c3d71c782e12d044` (EKS subnet 2) | `pcx-06524c8e180979086` (Peering Connection ID)                          |
| `10.65.0.0/20` (Your VPC CIDR)            | `pcx-06524c8e180979086` (Peering Connection ID)                          |
| `0.0.0.0/0`                               | `igw-xxxxxxxxxxxxxxxxx` (Internet Gateway - if needed for other traffic) |

## Security Best Practices

- Principle of Least Privilege: Only allow the necessary traffic.
- Security Groups: Use security groups to control traffic.
- Network ACLs (Optional): Additional security layer.
- Encryption: Use HTTPS.
- Private Subnets: EKS nodes and load balancers should be in private subnets.
- IAM Roles: Use IAM roles for EC2 and EKS nodes.
- Regular Audits: Audit security configurations and logs.
- Principle of Least Privilege: Only allow the necessary traffic between the peered VPC and your EKS cluster.
- Security Groups: Use security groups to tightly control inbound and outbound traffic.
- Network ACLs (Optional): You can use Network ACLs for an additional layer of security, but security groups are usually sufficient for this scenario.
- Encryption: Use HTTPS for your web application to encrypt traffic in transit.
- Private Subnets: Ensure your EKS nodes and load balancers are in private subnets with no direct internet access.
- IAM Roles: Use IAM roles for your EC2 instance and EKS worker nodes to grant only the necessary permissions.
- Regular Audits: Regularly audit your security configurations and logs to identify and address any potential vulnerabilities.
### Key Points

- Replace Placeholders: Ensure you replace the subnet IDs (`subnet-02b4bec3447cbbf9e` and `subnet-0c3d71c782e12d044`) with your actual values.
- Test Thoroughly: Test the connection from your EC2 instance in `vpc-0d9a8634e304211bd` to your EKS web application.

### Important Notes

- Replace the example CIDR blocks and peering connection ID with your actual values.
- Adjust the security group rules based on your specific application requirements.
- Consider using AWS PrivateLink for even more secure and private connectivity if applicable.
