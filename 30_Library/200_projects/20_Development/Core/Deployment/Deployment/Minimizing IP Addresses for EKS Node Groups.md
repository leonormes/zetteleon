---
aliases: []
confidence: 
created: 2025-02-17T12:17:19Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:51Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ff_deploy, networking]
title: Minimizing IP Addresses for EKS Node Groups
type:
uid: 
updated: 
version: 1
---

You have a running EKS cluster and want to minimize the number of IPs assigned to its node groups. This is a great way to optimize IP address utilization and improve the efficiency of your cluster! Here's how you can determine the appropriate number of IPs and adjust your node group configuration:

## Analyzing Your Existing Cluster

1. **Current Node Group Configuration:**

    - Use the following `kubectl` command to get details about your node groups, including their subnet and IP address assignments:Bash

        ```sh
        kubectl get nodes -o wide
        ```

    - Pay attention to the `INTERNAL-IP` and `EXTERNAL-IP` columns to understand how IP addresses are assigned to your nodes.
    - Also, check the subnet configuration for each node group using the AWS Management Console or the AWS CLI:Bash

        ```sh
        aws ec2 describe-subnets --filters "Name=subnet-id,Values=<subnet-id>"
        ```

        Replace `<subnet-id>` with the actual subnet ID of your node group.

2. **IP Address Utilization:**

    - Analyze the output of the following command to see how many IP addresses are currently assigned to pods and services in your cluster:Bash

        ```sh
        kubectl get pods -A -o wide
        kubectl get services -A -o wide
        ```

    - Count the number of unique IP addresses in the `IP` column for pods and the `CLUSTER-IP` and `EXTERNAL-IP` columns for services.
3. **Network Requirements:**

    - Consider the network requirements of your applications running in the cluster. Do they need any specific IP address ranges or configurations?
    - Are there any external services or dependencies that need to be accessed from your nodes?

## Determining the Minimum Number of IPs

Based on the analysis above, you can estimate the minimum number of IP addresses required for your node groups. Here are some factors to consider:

- **Number of Nodes:** Each node in a node group needs at least one IP address.
- **Pods and Services:** Allocate enough IP addresses to accommodate the current and anticipated number of pods and services in your cluster.
- **Headroom for Growth:** Leave some room for future growth in the number of nodes, pods, and services.
- **High Availability:** If you need high availability for your nodes, you might need additional IP addresses for load balancing or failover configurations.
- **External Services:** If your nodes need to access external services or be accessed from outside the cluster, you might need additional IP addresses for those purposes.

## Adjusting Node Group Configuration

Once you've determined the minimum number of IP addresses, you can adjust your node group configuration. Here are some options:

- **Reduce Subnet Size:** If your current subnets are larger than necessary, you can reduce their size by editing their CIDR blocks in the AWS Management Console or using the AWS CLI. However, exercise caution when doing this, as it might impact existing resources or future scaling needs.
- **Create Smaller Subnets:** Instead of modifying existing subnets, you can create new, smaller subnets with more restrictive IP ranges and migrate your nodes to the new subnets. This approach minimizes disruption but requires careful planning and execution.
- **Use IPAM:** For more advanced IP management and optimization, consider using Amazon VPC IP Address Manager (IPAM). IPAM provides tools for planning, tracking, and monitoring IP addresses in your VPCs, helping you identify and reclaim unused IP addresses.

## Obsidian Markdown

Markdown

```sh
## Minimizing IP Addresses for EKS Node Groups

**Analysis Steps:**

1. **Node Group Configuration:** Use `kubectl get nodes -o wide` and `aws ec2 describe-subnets`.
2. **IP Address Utilization:** Use `kubectl get pods -A -o wide` and `kubectl get services -A -o wide`.
3. **Network Requirements:** Consider application needs and external dependencies.

**Factors to Consider:**

- Number of nodes
- Pods and services
- Headroom for growth
- High availability
- External services

**Adjustment Options:**

- Reduce subnet size
- Create smaller subnets
- Use IPAM
```

By carefully analyzing your cluster's IP address utilization and network requirements, you can effectively minimize the number of IPs assigned to your node groups, optimizing resource usage and improving the efficiency of your EKS cluster.
