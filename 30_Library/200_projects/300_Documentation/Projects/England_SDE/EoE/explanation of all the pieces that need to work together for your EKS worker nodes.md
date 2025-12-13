---
aliases: []
confidence: 
created: 2025-02-10T12:38:48Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:52Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, ff_deploy, FFAPP-3638]
title: explanation of all the pieces that need to work together for your EKS worker nodes
type: 
uid: 
updated: 
version: 
---

## Overview

1. Terraform Cloud Service Principal (SP):
    This is the identity that runs your Terraform code. It has permissions to create AWS resources such as VPCs, EKS clusters, and node groups.
2. EKS Cluster (Control Plane):
    This is the managed Kubernetes cluster hosted by AWS. It runs the API server and control logic.
3. EKS Node Group:
    This is a configuration (managed by AWS) that tells EKS how to launch EC2 instances (the worker nodes) that join the cluster.
4. EC2 Worker Nodes:
    These are the actual virtual machines. They run a “kubelet” process (the Kubernetes agent) that must register itself with the EKS control plane.
5. IAM Roles and Permissions:
    - For Terraform: Your Terraform SP must have permission to create all resources.
    - For Worker Nodes: When the EC2 instances launch, they assume an IAM role (attached as an “instance profile”) that gives them the credentials they need. This role must include policies such as:
        - AmazonEKSWorkerNodePolicy (to allow the node to interact with AWS services)
        - AmazonEKS_CNI_Policy (to allow the networking plugin to work)
        - AmazonEC2ContainerRegistryReadOnly (to pull container images)
    - Mapping to Kubernetes: The EKS control plane must know which nodes are allowed to join. In older setups this was done via the aws‑auth ConfigMap, but in your case it’s done through EKS Access Entries. Your worker node role (e.g. `ff-eoe-sde-node-group`) must be registered there.

---

## Step-by-Step Process

### Step 1: Terraform Creates the EKS Cluster and Node Group

- Terraform Cloud SP Role:
    The Terraform service principal calls the AWS APIs (using its permissions) to create an EKS cluster and then to create a node group.
- What Happens:
    - The EKS cluster is set up (the control plane is created).
    - A node group is defined and configured to use a specific IAM role for the worker nodes.

### Step 2: Node Group Launches EC2 Instances

- EC2 Instances (Worker Nodes):
    When the node group is created, AWS launches EC2 instances using a launch template (either auto‑generated or one you provide).
- IAM Role for Nodes:
    Each EC2 instance is launched with an instance profile that attaches the worker node IAM role (e.g. `ff-eoe-sde-node-group`).
- What This Role Does:
    It provides the node with permissions (through its policies) to:
    - Communicate with AWS services (for example, to pull images from ECR).
    - Call EKS APIs (if needed) and interact with the VPC CNI plugin.

### Step 3: Worker Nodes Boot Up and Register with the Cluster

- Bootstrap Process:
    When an EC2 instance boots up, it runs a bootstrap script (usually part of the Amazon EKS‑optimized AMI). This script starts the kubelet process.
- Assuming the IAM Role:
    Because of the attached instance profile, the worker node “assumes” its IAM role and obtains temporary AWS credentials.
- Registering with the EKS Cluster:
    The kubelet uses these credentials to authenticate with the EKS control plane’s API.
    - Access Mapping:
        Instead of using the old `aws-auth` ConfigMap, your cluster uses EKS Access Entries to map the IAM role (e.g. `ff-eoe-sde-node-group`) to the proper Kubernetes groups (typically `system:bootstrappers` and `system:nodes`). This mapping tells the control plane “this node is allowed to join.”

### Step 4: Node is Accepted and Joins the Cluster

- Successful Registration:
    If all permissions are correct and the network configuration allows the node to reach the API server, the node registers and appears as “Ready” in your Kubernetes cluster.
- If It Fails:
    The node may not join if:
    - The worker node IAM role is missing one of the required policies.
    - The IAM trust relationship is not set to allow EC2 instances.
    - The mapping in the EKS Access Entries is missing or incorrect.
    - The node cannot reach the EKS API (due to network issues such as missing NAT Gateway or misconfigured security groups).

---

## Diagram

Here’s a simplified diagram that shows the flow:

```sh
+---------------------------------------------------+
| Terraform Cloud Service Principal (SP)            |
| (Runs Terraform with AWS permissions)             |
+--------------------------+------------------------+
                           |
                           | Creates
                           v
+---------------------------------------------------+
|              EKS Cluster (Control Plane)          |
|  - Managed by AWS EKS                             |
|  - Has an API endpoint to which nodes connect     |
|  - Uses EKS Access Entries to map node IAM roles   |
+--------------------------+------------------------+
                           |
                           | Creates node group
                           v
+---------------------------------------------------+
|                EKS Node Group                     |
|  - Configured with an IAM role for worker nodes     |
|  - Launches EC2 instances (worker nodes)           |
+--------------------------+------------------------+
                           |
                           | Launches EC2 instances with
                           | an instance profile (worker IAM role)
                           v
+---------------------------------------------------+
|               EC2 Worker Nodes                    |
|  - Assume the IAM role (e.g., ff-eoe-sde-node-group)|
|  - Run the bootstrap script and start kubelet      |
+--------------------------+------------------------+
                           |
                           | Kubelet uses IAM credentials to
                           | connect to the EKS API
                           v
+---------------------------------------------------+
|         EKS Control Plane API (Cluster)           |
|  - Verifies node’s IAM role via EKS Access Entries  |
|  - Accepts the node if mapping is correct           |
+---------------------------------------------------+
```

---

## Key Points Recap

- Terraform (Service Principal)**: Creates the cluster and node group.
- EKS Cluster**: Runs the Kubernetes control plane.
- Node Group**: Specifies the settings for EC2 worker nodes, including which IAM role they use.
- EC2 Worker Nodes**: Boot up, assume their IAM role, and run the kubelet.
- IAM Role for Nodes**: Must have the correct managed policies (WorkerNode, CNI, and ECR read-only) and a trust policy allowing EC2 to assume the role.
- EKS Access Entries**: Map the worker node IAM role to the appropriate Kubernetes groups so that the control plane will allow the node to join.
- Network Connectivity**: The worker nodes must be able to reach the EKS API endpoint (using public IPs, NAT Gateway, or VPC endpoints).

By ensuring every one of these steps is correctly configured, your nodes can successfully register with your EKS cluster.

Below is a step‐by‐step guide showing you which AWS CLI commands you can run to collect full details of your EKS deployment and its related resources. With these details, you (or someone helping you) can better diagnose why your worker nodes aren’t joining the cluster.

---

## 1. Get the EKS Cluster Details

This command returns the full configuration of your EKS cluster, including its endpoint, certificate authority, VPC configuration, and status.

```sh
aws eks describe-cluster --name <your-cluster-name> --region <your-region> --output json
```

*Example:*

```sh
aws eks describe-cluster --name ff-eoe-sde --region eu-west-2 --output json
```

What to Look For:

- Status: Should be ACTIVE.
- Endpoint and Certificate Authority: Used by worker nodes to connect.
- VPC Config: Includes the subnet IDs and security group IDs that the control plane uses.

---

## 2. List and Describe Node Groups

First, list all node groups associated with your cluster:

```sh
aws eks list-nodegroups --cluster-name <your-cluster-name> --region <your-region>
```

*Example:*

```sh
aws eks list-nodegroups --cluster-name ff-eoe-sde --region eu-west-2
```

Then, for each node group (for example, if your node group is named `ff-eoe-sde-node-group`), get detailed information:

```sh
aws eks describe-nodegroup --cluster-name <your-cluster-name> --nodegroup-name <your-nodegroup-name> --region <your-region> --output json
```

*Example:*

```sh
aws eks describe-nodegroup --cluster-name ff-eoe-sde --nodegroup-name ff-eoe-sde-node-group --region eu-west-2 --output json
```

What to Look For:

- Node Role ARN: Confirms which IAM role is assigned to the nodes.
- Subnets: Check that the subnets specified are correct.
- Status and Scaling Config: Indicates if the node group is active or in error.

---

## 3. List EKS Access Entries

Since your cluster uses EKS Access Entries to map IAM principals instead of the aws‑auth ConfigMap, list them:

```sh
aws eks list-access-entries --cluster-name <your-cluster-name> --region <your-region> --output json
```

*Example:*

```sh
aws eks list-access-entries --cluster-name ff-eoe-sde --region eu-west-2 --output json
```

What to Look For:

- Ensure your worker node IAM role (for example, `arn:aws:iam::703671921185:role/ff-eoe-sde-node-group`) is listed.
- Other mappings (for IAM users or service roles) that might affect access.

---

## 4. Get EC2 Instance Details for Your Nodes

Check the instances launched as part of your node group. These instances usually have tags indicating their association with the EKS cluster and node group.

```sh
aws ec2 describe-instances \
  --filters "Name=tag:eks:cluster-name,Values=<your-cluster-name>" "Name=tag:eks:nodegroup-name,Values=<your-nodegroup-name>" \
  --region <your-region> --output json
```

*Example:*

```sh
aws ec2 describe-instances \
  --filters "Name=tag:eks:cluster-name,Values=ff-eoe-sde" "Name=tag:eks:nodegroup-name,Values=ff-eoe-sde-node-group" \
  --region eu-west-2 --output json
```

What to Look For:

- Instance State: Should be running.
- Private IP Addresses: Confirm that they have an IP and can route traffic.
- Tags: Ensure the instances have the expected tags (e.g., the cluster and node group name).

---

## 5. Check the IAM Role Details for the Worker Nodes

To see what policies are attached and to view the trust relationship for the worker node IAM role:

### A. Get the Role Information

```sh
aws iam get-role --role-name <Your-Worker-Node-Role> --output json
```

*Example:*

```sh
aws iam get-role --role-name ff-eoe-sde-node-group --output json
```

### B. List Attached Policies

```sh
aws iam list-attached-role-policies --role-name <Your-Worker-Node-Role> --output json
```

*Example:*

```sh
aws iam list-attached-role-policies --role-name ff-eoe-sde-node-group --output json
```

What to Look For:

- Attached Policies: Should include:
    - AmazonEKSWorkerNodePolicy
    - AmazonEKS_CNI_Policy
    - AmazonEC2ContainerRegistryReadOnly
- Trust Relationship: Verify that it allows EC2 (`"Principal": { "Service": "ec2.amazonaws.com" }`).

---

## 6. Get VPC and Subnet Details

Sometimes networking issues prevent nodes from reaching the EKS API. Check your VPC and subnets:

### A. Describe Your VPC

```sh
aws ec2 describe-vpcs --vpc-ids <your-vpc-id> --output json
```

### B. Describe Subnets in the VPC

```sh
aws ec2 describe-subnets --filters "Name=vpc-id,Values=<your-vpc-id>" --output json
```

*Example:*

```sh
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-12345678" --output json
```

What to Look For:

- Subnet Configuration: Ensure that the subnets have proper route tables (e.g., if private, a route to a NAT Gateway).
- IP Address Availability: Check if there are enough free IP addresses for new nodes.

---

## 7. (Optional) Check CloudFormation Stacks

If you used Terraform with CloudFormation (or if your resources were created by CloudFormation), you might want to check the CloudFormation stacks:

```sh
aws cloudformation describe-stacks --region <your-region> --output json
```

This command returns details of all stacks, which might give clues if there are errors in stack creation.

---

## Diagram Of the AWS CLI Data Flow

Below is a simplified diagram showing the different areas and how you collect information with the AWS CLI:

```sh
         +-------------------------------+
         |         EKS Cluster           |
         |  (Control Plane Details)      |
         |  aws eks describe-cluster     |
         +---------------+---------------+
                         |
                         v
         +-------------------------------+
         |       Node Groups             |
         |  aws eks list-nodegroups      |
         |  aws eks describe-nodegroup   |
         +---------------+---------------+
                         |
                         v
         +-------------------------------+
         |   EKS Access Entries          |
         |  aws eks list-access-entries  |
         +---------------+---------------+
                         |
                         v
         +-------------------------------+
         |   EC2 Worker Nodes            |
         |  aws ec2 describe-instances   |
         +---------------+---------------+
                         |
                         v
         +-------------------------------+
         |      IAM Role Details         |
         | aws iam get-role              |
         | aws iam list-attached-role-policies |
         +---------------+---------------+
                         |
                         v
         +-------------------------------+
         |   VPC & Subnet Configuration  |
         | aws ec2 describe-vpcs         |
         | aws ec2 describe-subnets      |
         +-------------------------------+
```

---

## Summary

By running these AWS CLI commands, you’ll gather complete information about:

- Your EKS cluster configuration,
- Node groups and their settings,
- Which EC2 instances are running as worker nodes,
- The IAM roles and policies that give these nodes permission,
- And the networking setup (VPC and subnets).

Once you have these details, you (or someone helping you) can look for discrepancies or misconfigurations that might be preventing nodes from registering with the EKS cluster.

Feel free to share any output (redacted as needed) or ask more questions if something isn’t clear. This information will help pinpoint the issue.
