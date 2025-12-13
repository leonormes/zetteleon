---
aliases: []
confidence: 
created: 2025-02-11T09:15:58Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:52Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ff_deploy]
title: LZA Questions
type: 
uid: 
updated: 
version: 
---

Here are key questions to ask the LZA team to help resolve the node registration issues:

1. IAM Role Permissions:
   - Can you confirm the exact permissions attached to the `eks-cluster-role` and node group role?
   - Are there any custom policies or restrictions applied to these roles through Service Control Policies (SCPs)?
   - Do the roles have the necessary trust relationships configured for EKS and EC2 services?

2. VPC and Networking:
   - Are there any Network ACLs (NACLs) or Security Group restrictions that might prevent node-to-cluster communication?
   - Is the VPC configured with the required endpoints for EKS (eks.amazonaws.com, ec2.amazonaws.com, ecr.amazonaws.com)?
   - Are the subnets properly tagged for EKS auto-discovery (`kubernetes.io/cluster/${cluster-name}`)?

3. Cross-Account Access:
   - Are there any cross-account permissions we need to be aware of?
   - Do we need specific assume role configurations for cross-account access?

4. Security and Compliance:
   - Are there any specific security requirements or restrictions we should be aware of?
   - Are there any mandatory tags or naming conventions we need to follow?

5. Troubleshooting Access:
   - Can you provide CloudTrail logs for the IAM role access denials?
   - Can we get VPC Flow logs to analyze the network connectivity issues?
   - Do you have any specific troubleshooting procedures or tools we should use?

6. Best Practices:
   - What's the recommended approach for deploying EKS clusters in your environment?
   - Are there any reference architectures or examples we can follow?
   - Should we be using specific node instance types or configurations?

7. Operational Questions:
   - Who owns and manages the CloudWatch logs for the cluster?
   - What's the process for rotating or updating IAM roles and policies?
   - Are there any specific monitoring or alerting requirements?

These questions should help identify any misconfigurations or missing permissions that are preventing the nodes from registering with the cluster.

Based on the LZA configuration files, I can answer several of our questions:

1. IAM Role Permissions:
   - There is a specific `EKSClusterPolicy` defined for the `eoe-sde-discovery` account
   - We should ask to see the contents of `iam-policies/eks-cluster-policy.json` to verify the exact permissions

2. VPC and Networking:
   - The environment uses a Transit Gateway setup with pre and post-inspection routing
   - Network is centrally managed through the `eoe-sde-network` account
   - VPC endpoints are configured in a central VPC (`eoe-sde-nwhub-infra-vpc-endpoints`)
   - The CIDR range for the environment is `10.64.0.0/16`

3. Cross-Account Access:
   - Cross-account access is managed through Transit Gateway attachments
   - The Transit Gateway is shared with both Infrastructure and Workloads OUs

4. Security and Compliance:
   - There's a centralized network inspection setup (pre/post inspection routing)
   - Network traffic appears to be routed through a central inspection VPC

Updated Questions for the LZA Team:

1. IAM-specific:
   - Can we see the contents of `iam-policies/eks-cluster-policy.json`?
   - Are there any additional Service Control Policies (SCPs) that might affect EKS or EC2 permissions?
   - Should we be using the `EC2-Default-SSM-AD-Role` for our node groups?

2. Networking-specific:
   - Do we need to route node-to-cluster traffic through the transit gateway inspection?
   - Are there specific security group rules we need to follow for the EKS cluster and node groups?
   - Should we be using the central VPC endpoints, or can we create our own?

3. Architecture-specific:
   - Is there a reference EKS deployment in another account we can look at?
   - Should we be using specific subnet tags for EKS auto-discovery?
   - Are there any specific requirements for node group configurations (instance types, scaling policies)?

4. Process-specific:
   - What's the process for requesting new IAM policies or roles if needed?
   - Who should we contact for VPC Flow logs or CloudTrail logs if needed for troubleshooting?
   - Is there a change management process we need to follow for EKS deployments?

These questions are more targeted based on the actual LZA configuration we can see. The main issue seems likely to be either:

1. Missing permissions in the EKS cluster policy
2. Network routing/security group issues with the transit gateway setup
3. VPC endpoint access for the EKS API

Based on the analysis of the LZA files, here's what we need to know for deploying our EKS cluster:

1. Account Structure:
   - We're deploying to the `eoe-sde-discovery` account in the `Workloads/Discovery` OU
   - The account has specific IAM policies defined in `iam-policies/eks-cluster-policy.json`

2. Network Architecture:
   - Base CIDR: `10.64.0.0/16`
   - Discovery CIDR: `10.64.76.0/24`
   - Transit Gateway routing through:
     - Pre-inspection route table: `eoe-sde-nwhub-infra-tgwrt-preinspection`
     - Post-inspection route table: `eoe-sde-nwhub-infra-tgwrt-postinspection`
   - All traffic goes through a central inspection VPC

3. Security Requirements:
   - Region restricted to eu-west-2 (London)
   - Mandatory security services enabled:
     - GuardDuty
     - Security Hub
     - AWS Config
     - Access Analyzer
   - All EBS volumes must be encrypted
   - CloudWatch logs must be encrypted

4. Required VPC Endpoints:
   - EKS requires access to:
     - eks.amazonaws.com
     - ec2.amazonaws.com
     - ecr.api.amazonaws.com
     - ecr.dkr.amazonaws.com
     - s3.amazonaws.com
     - sts.amazonaws.com
     - logs.amazonaws.com (for CloudWatch)

5. Network Flow:
   - All outbound traffic (0.0.0.0/0) routes through the transit gateway
   - Traffic goes through network firewall inspection
   - DNS resolution uses central Route53 resolver

Key Questions for LZA Team:

1. Network-specific:
   - Do we need to use the central VPC endpoints in `eoe-sde-nwhub-infra-vpc-endpoints`, or can we create our own?
   - Are there specific firewall rules we need to be aware of for EKS cluster-to-node communication?
   - Should node-to-node traffic stay local or go through the transit gateway?

2. IAM-specific:
   - Can we see the contents of `iam-policies/eks-cluster-policy.json`?
   - Do we need to add any specific trust relationships for cross-account access?
   - Are there any SCPs that might affect EKS or EC2 permissions?

3. Security-specific:
   - Are there specific encryption requirements for EKS secrets beyond KMS?
   - Do we need to enable specific Security Hub controls for EKS?
   - Are there any custom AWS Config rules for EKS we need to comply with?

4. Operational:
   - What's the process for requesting additional VPC endpoints if needed?
   - Who manages the central Route53 resolver rules?
   - What's the process for updating security group rules if needed?

Recommendations for our Deployment:

1. Networking:

   ```hcl
   # VPC Configuration
   - Use CIDR 10.64.76.0/24 (Discovery IPAM pool)
   - Create subnets in both AZs
   - Ensure Transit Gateway attachment with proper route table associations
   - Route 0.0.0.0/0 to Transit Gateway
   ```

2. Security Groups:

   ```hcl
   # Cluster Security Group
   - Allow inbound 443 from node security group
   - Allow all outbound
   
   # Node Security Group
   - Allow all traffic between nodes
   - Allow outbound to cluster security group on 443
   - Allow outbound to internet via Transit Gateway
   ```

3. IAM:

   ```hcl
   # Use existing roles
   - cluster_role_arn = "arn:aws:iam::${account_id}:role/eks-cluster-role"
   - node_role_arn = "arn:aws:iam::${account_id}:role/${cluster_name}-node-group"
   ```

4. Encryption:

   ```hcl
   # Use KMS for secrets
   - Enable envelope encryption for secrets
   - Enable EBS encryption by default
   ```

Would you like me to look into any specific aspect in more detail?
