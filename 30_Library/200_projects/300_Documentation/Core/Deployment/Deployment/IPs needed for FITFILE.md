---
aliases: []
confidence: 
created: 2025-02-17T00:00:00Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:51Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, eks, ff_deploy, ip, networking]
title: IPs needed for FITFILE
type:
uid: 
updated: 
version:
---

## Key Considerations for VPC CIDR Range

### Number of EKS Nodes (EC2 Instances)

Each worker node in your EKS cluster is an EC2 instance and requires an IP address from your VPC CIDR range.

You need to estimate the maximum number of nodes you anticipate running in your cluster, considering potential scaling and future growth.

### Pods per Node

Each pod in your EKS cluster, by default, is assigned an IP address from your VPC CIDR range.

The number of pods you can run per node depends on the instance type you choose for your worker nodes and the Kubernetes configuration. You should estimate the maximum number of pods you expect to run across your entire cluster.

### Services

Kubernetes Services also consume IP addresses from your VPC CIDR range.3 While the number of Service IPs is typically smaller than the number of pods, you should still account for them. Each service gets a ClusterIP, and if you are using LoadBalancer or NodePort services, those might also consume additional IPs depending on your setup.

### Network Interfaces per Node

Each EC2 instance (worker node) in your VPC can have multiple Elastic Network Interfaces (ENIs). The number of ENIs and IP addresses per ENI is limited by the EC2 instance type.4 EKS networking relies on ENIs to provide network connectivity for pods.5 You need to ensure your VPC CIDR range is large enough to accommodate the IP addresses required by the ENIs on your worker nodes.

### Future Growth

It's crucial to overestimate your initial needs to accommodate future growth. Resizing a VPC CIDR range after deployment can be complex and disruptive. Consider potential increases in the number of nodes, pods, and services over time.

## Kubernetes Pod IPs and VPC CIDR Range

- Pods get VPC CIDR IPs: By default, in EKS, pods do receive IP addresses directly from your VPC CIDR range.6 This is achieved through the AWS VPC Container Network Interface (CNI) plugin for Kubernetes. This means each pod is directly routable within your VPC and can communicate with other resources in your VPC using standard VPC networking.7
- No Cluster-Specific IP Range (by default): In a standard EKS setup using the AWS VPC CNI, there is no separate, cluster-specific IP range for pods that is outside of your VPC CIDR range. Pods are part of your VPC network and are assigned IPs from the VPC's address space.8

## Calculating the Required CIDR Range

### 1. Estimate Total IP Addresses Needed

Nodes: Estimate the maximum number of worker nodes (e.g., `N`).

Pods per Node: Estimate the maximum number of pods per node (e.g., `P`).

Total Pods: `N  P` (approximately).

Services: Estimate the number of services (e.g., `S`).

Network Interfaces: Consider the number of ENIs per node. This is more complex and depends on the instance type and configuration. For simplicity, you can initially assume each node primarily uses one ENI for pod networking, but be aware of ENI limits for your instance types.

1. Calculate Total IPs: A rough estimate of total IPs needed would be `(N  P) + S + N` (Pods + Services + Nodes). However, it's safer to slightly overestimate, especially for pods, to account for overhead and potential density increases.
2. Choose a CIDR Block: Select a CIDR block that can accommodate the total number of IP addresses you calculated. Here's a quick reference:

 - `/24` CIDR: 256 IPs
 - `/23` CIDR: 512 IPs
 - `/22` CIDR: 1024 IPs
 - `/21` CIDR: 2048 IPs
 - `/20` CIDR: 4096 IPs
 - `/19` CIDR: 8192 IPs
 - `/18` CIDR: 16384 IPs
 - `/17` CIDR: 32768 IPs
 - `/16` CIDR: 65536 IPs

 For example, if you estimate needing around 1500 IP addresses, a `/21` CIDR block (2048 IPs) would be a suitable starting point. For larger deployments, you might consider `/20` or even larger.

Example Scenario:

Let's say you anticipate:

- Maximum 50 worker nodes.
- Maximum 20 pods per node.
- Around 50 services.

Total estimated IPs (rough): `(50 nodes  20 pods/node) + 50 services + 50 nodes = 1000 + 50 + 50 = 1100 IPs`.

In this case, a `/22` CIDR block (1024 IPs) might seem just enough, but to be safe and allow for some growth, you might choose a `/21` CIDR block (2048 IPs) for your VPC.

Important Notes:

- AWS VPC Limits: Be mindful of AWS VPC limits, including the number of CIDR blocks you can associate with a VPC and the size of those blocks.
- Overlapping CIDR Ranges: Ensure your VPC CIDR range does not overlap with any other networks your VPC needs to connect to (e.g., on-premises networks, other VPCs).
- Subnets: Once you have your VPC CIDR, you will divide it into subnets (e.g., public and private subnets) for your EKS cluster components. Make sure to plan your subnet CIDR ranges within the VPC CIDR.
- Instance Type Limits: The number of pods you can run on a node is also limited by the instance type's ENI and IP address limits, as described in [Result 2].9 For example, a `t3.medium` instance supports a maximum of 17 pods.

By carefully considering these factors and making reasonable estimations, you can choose an appropriate VPC CIDR range for your EKS deployment that provides enough IP addresses for your current and future needs. Remember to always err on the side of slightly over-provisioning to avoid potential IP address exhaustion issues later.

In EKS, pods can get their IPs in two different ways, depending on your networking mode:

First, let's look at the default mode called "AWS VPC CNI":

In this mode, every pod does indeed get an IP address from your VPC CIDR range. The CNI plugin assigns each pod a real VPC IP address. This means you need to carefully plan your CIDR range to accommodate all potential pods, nodes, and other AWS resources.

For example, if you expect to run 1000 pods across your cluster, you'll need at least that many free IP addresses in your VPC, plus additional IPs for your worker nodes, load balancers, and other AWS services. A good practice is to allocate significantly more than your immediate needs to allow for growth.

The alternative mode is "custom networking":

If IP address conservation is a concern, you can configure EKS to use custom networking solutions like Calico or Cilium. These CNI plugins can assign pod IPs from a separate address space that doesn't use your VPC IPs. This can be particularly useful if you have VPC CIDR constraints.

For your VPC CIDR planning, you'll need to consider:

The number of worker nodes you plan to deploy. Each node needs its own VPC IP.

The maximum number of pods you expect to run if using AWS VPC CNI. Each pod needs a VPC IP.

Any AWS services you'll use that need IPs (like load balancers, NAT gateways, etc.).

Future growth and scaling requirements.

Subnet distribution across Availability Zones for high availability.

A practical example:

If you're using AWS VPC CNI and planning for:

- 10 worker nodes
- Up to 100 pods per node (1000 total pods)
- A few load balancers and NAT gateways

You might want to allocate a /20 CIDR block (4,096 IPs) to give yourself room for growth. This could be divided into multiple subnets across AZs.

Would you like me to explain more about any particular aspect of this, such as subnet distribution or how to calculate the exact CIDR block size you need for your specific use case?

Here's a structured breakdown of CIDR planning for AWS EKS, including key considerations and how pod IPs work:

---

## Key Considerations for EKS VPC CIDR Planning

When designing your VPC CIDR for EKS, you must account for:

1. Pod IP Allocation (Default Behavior):
   - Pods use VPC CIDR IPs: By default, AWS EKS uses the VPC CNI plugin, which assigns pods IPs directly from your VPC subnets.
   - No cluster-specific CIDR: Unlike some Kubernetes setups (e.g., Calico with overlay networks), pods share the same IP space as EC2 instances, load balancers, and other AWS resources.

2. IP Requirements:
   - Nodes: Each EC2 worker node requires 1 IP.
   - Pods: Each pod requires 1 IP. The max pods per node depends on the instance type (e.g., `t3.large` supports ~35 pods).
   - AWS Services: Load balancers (ALB/NLB), NAT gateways, RDS proxies, etc., consume additional IPs.
   - Reserved IPs: AWS reserves 5 IPs per subnet (e.g., 172.31.0.0/24 has 251 usable IPs).

3. Subnet Sizing:
   - Use the formula:

```plaintext
Total IPs Needed = (Number of Nodes × Pods per Node) + Nodes + Buffer (for AWS services)
```

   - Example: For 10 nodes (35 pods each) + 2 load balancers:

```plaintext
(10 × 35) + 10 + 2 = 362 IPs → Minimum subnet size: /23 (512 IPs)
```

---

## Solutions For IP Exhaustion

If your current VPC CIDR is insufficient:

1. Expand Subnet Size:
   - Use larger subnets (e.g., /22 instead of /24).
   - Example: A /22 subnet provides 1021 usable IPs.

2. Secondary CIDR Blocks:
   - Assign a secondary CIDR to your VPC (e.g., `10.0.0.0/16` for pods).
   - Configure the VPC CNI plugin to use this CIDR for pods:

```bash
kubectl set env daemonset aws-node -n kube-system AWS_VPC_K8S_CNI_CUSTOM_NETWORK_CFG=true
kubectl set env daemonset aws-node -n kube-system ENI_CONFIG_LABEL_DEF=failure-domain.beta.kubernetes.io/zone
```

1. Use Smaller Pod Ranges:
   - Reduce the number of pods per node (adjust `--max-pods` in the EKS worker node bootstrap script).

---

## Example CIDR Plan

Assume:

- 50 nodes (m5.xlarge, 58 pods/node)
- 5 load balancers
- 10 RDS proxies

Calculation:

```plaintext
Total IPs = (50 × 58) + 50 + 5 + 10 = 2,965 IPs
```

Recommended CIDR:

- Use /20 subnet (4,096 IPs) or /19 subnet (8,192 IPs) for future scaling.

---

## Critical Best Practices
1. Avoid Overlap: Ensure VPC CIDR does not conflict with on-premises networks or peered VPCs.
2. Multi-AZ Subnets: Deploy nodes across multiple subnets/AZs for high availability.
3. Monitor IP Usage:

```bash
# Check remaining IPs in a subnet
aws ec2 describe-subnets --subnet-ids <subnet-id> --query "Subnets[].AvailableIpAddressCount"
```

---

## Default Vs. Custom Networking

| Aspect               | Default VPC CNI           | Custom Networking (Secondary CIDR)       |
|--------------------------|-------------------------------|----------------------------------------------|
| Pod IP Source         | VPC Subnet CIDR               | Dedicated CIDR (e.g., 100.64.0.0/16)         |
| IP Management         | Tied to EC2 Capacity          | Decoupled from EC2 IP limits                 |
| Complexity            | Simple (AWS-managed)          | Requires ENI configurations                  |
| Use Case              | Small/Medium Clusters         | Large clusters with strict IP isolation      |

---

By planning for pods, nodes, and AWS services upfront, you can avoid IP exhaustion and ensure smooth EKS operations. Use secondary CIDRs for large-scale deployments.

When planning the CIDR range for your Amazon Elastic Kubernetes Service (EKS) deployment, it's crucial to account for all components that will consume IP addresses within your Virtual Private Cloud (VPC). Here's what you need to consider:

1. Kubernetes Pods:

By default, each pod in an EKS cluster is assigned a unique private IPv4 address from the VPC's CIDR block. These addresses are allocated to the elastic network interfaces (ENIs) attached to your worker nodes. The number of IP addresses available for pods on a node depends on the instance type and the number of ENIs it supports. For detailed information, refer to the [Amazon EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/cni-increase-ip-addresses.html).

1. Worker Nodes:

Each worker node (EC2 instance) requires one primary IP address for each ENI. The number of ENIs and secondary IP addresses per ENI varies by instance type. Ensure your VPC has enough IP addresses to accommodate the maximum number of nodes you plan to deploy.

1. Load Balancers and Other Services:

Services like load balancers, NAT gateways, and other AWS resources will also consume IP addresses from your VPC. Account for these when planning your CIDR range.

Calculating the CIDR Range:

To determine the appropriate CIDR block size:

1. Estimate the Maximum Number of Pods:

    - Decide on the maximum number of pods you expect to run simultaneously.
2. Determine IP Addresses per Pod:

    - Each pod requires one IP address.
3. Calculate Total IP Addresses Needed:

    - Total IPs = (Number of Pods) + (Number of Nodes) + (Additional Services and Buffers)
4. Choose an Appropriate CIDR Block:

    - Based on the total IPs calculated, select a CIDR block that provides sufficient addresses. For example, a /16 CIDR block offers 65,536 IP addresses, while a /20 provides 4,096.

Alternative IP Allocation Strategies:

If conserving VPC IP addresses is a priority, consider implementing custom networking with the Amazon VPC CNI plugin. This allows you to assign pod IP addresses from secondary CIDR blocks, including those outside the VPC's primary CIDR range, such as the 100.64.0.0/10 range. This approach helps prevent exhaustion of IP addresses in your primary CIDR block. For more details, see the [Amazon EKS Best Practices Guide for Networking](https://docs.aws.amazon.com/eks/latest/best-practices/custom-networking.html).

Key Takeaway:

Each pod in your EKS cluster requires an IP address from your VPC's CIDR range by default. Therefore, it's essential to plan a sufficiently large CIDR block to accommodate all pods, nodes, and additional services, or to explore alternative IP allocation methods to optimize IP address usage within your VPC.

To set up Calico CNI in AWS to reduce the number of IPs needed from the VPC CIDR, you can follow these steps:

1. Install Calico on your existing EKS cluster using Helm[5]:

```bash
helm repo add projectcalico https://docs.tigera.io/calico/charts
helm install calico projectcalico/tigera-operator --version v3.29.0
```

1. Configure Calico to use VXLAN overlay networking mode[5][6]. This encapsulates pod traffic, allowing pods to use a separate IP range from the VPC CIDR:

```yaml
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  calicoNetwork:
    ipPools:
    - cidr: 192.168.0.0/16
      encapsulation: VXLAN
```

1. Use Calico's IPAM (IP Address Management) instead of AWS VPC CNI[1][6]. This allows for more efficient IP address allocation:

```yaml
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  cni:
    type: Calico
  ipam:
    type: Calico
```

By implementing these configurations, you can significantly reduce the number of IPs needed from the VPC CIDR, as Calico will manage pod IP allocation independently of the VPC IP range[1][6].
