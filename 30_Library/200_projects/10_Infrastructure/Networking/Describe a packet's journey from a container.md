---
aliases: []
confidence: 
created: 2025-10-25T17:49:24Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:22Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: "Describe a packet's journey from a container"
type:
uid: 
updated: 
version:
---

The journey of a packet leaving a container within a pod in a private AWS EKS Kubernetes cluster and heading out to the public internet. It's a multi-stage trip involving several AWS and Kubernetes networking components.

1. **Container to Pod Network Namespace:**  
   - The application within the container generates a packet destined for a public IP address.  
   - This packet first travels through the container's network interface (eth0, for example) and into the pod's network namespace. Containers within the same pod share this network namespace.  
   - The pod has its own private IP address within the EKS cluster's internal network.  
2. **Pod Egress Traffic Handling (kube-proxy/CNI):**  
   - Kubernetes uses a network proxy (typically kube-proxy) and a Container Network Interface (CNI) plugin (like Calico, Cilium, or Weave Net) to handle networking within the cluster.  
   - For egress traffic, kube-proxy (in iptables or ipvs mode) or the CNI plugin will intercept the packet.  
   - **SNAT (Source Network Address Translation):** Since the pod's private IP address is not routable on the public internet, the source IP address of the packet needs to be translated to a public IP address. This is typically done using Source Network Address Translation (SNAT).  
3. **Node Network Namespace:**  
   - The packet, now likely with its source IP address translated, leaves the pod's network namespace and travels to the network namespace of the worker node where the pod is running.  
4. **AWS Elastic Network Interface (ENI) of the Worker Node:**  
   - The worker node has one or more Elastic Network Interfaces (ENIs) attached to it. These ENIs have private IP addresses within the VPC subnet where the node resides.  
   - The packet is routed through the node's network stack and out through one of its ENIs.  
5. **NAT Gateway or Public Subnet with Public IP:**  
   - This is where the route to the public internet is established. There are two main ways this can happen in AWS:  
     - **NAT Gateway:** If the worker node resides in a private subnet (which is typical for security reasons), the subnet will have a route to a NAT (Network Address Translation) Gateway. The NAT Gateway has a public IP address and handles the SNAT for instances in the private subnet, allowing them to initiate outbound traffic to the internet without being directly reachable from the internet. The NAT Gateway will replace the source IP address of the packet with its own public IP address.  
     - **Public Subnet with Public IP:** If the worker node is in a public subnet and has a public IP address directly associated with its ENI, the SNAT might occur at the instance level or be handled by AWS's infrastructure. In this less common scenario for EKS worker nodes, the instance's public IP would be used as the source IP.  
6. **Internet Gateway (IGW):**  
   - The NAT Gateway (or the public subnet's routing) will have a route to an Internet Gateway (IGW) attached to the VPC.  
   - The IGW is a highly available, horizontally scalable VPC component that allows communication between instances in your VPC and the internet.  
   - The packet travels from the NAT Gateway (or the public subnet) to the IGW.  
7. **Out to the Public Internet:**  
   - The Internet Gateway forwards the packet out onto the public internet, using standard internet routing protocols.  
   - The destination server on the public internet receives the packet, appearing to originate from the public IP address of the NAT Gateway (or the worker node's public IP, if configured that way).  
8. **Return Traffic:**  
   - When the destination server sends a response, the packet is routed back to the public IP address of the NAT Gateway (or the worker node).  
   - The NAT Gateway maintains state and knows which internal IP address originated the request. It will then forward the response packet back to the correct private IP address of the worker node.  
   - The worker node's network stack then routes the packet back to the pod's network namespace.  
   - Finally, the Kubernetes networking (CNI/kube-proxy) ensures the packet is delivered to the correct container within the pod.

In essence, for a packet to leave a container in a private EKS cluster and reach the public internet, it undergoes several layers of network address translation and routing managed by Kubernetes and AWS networking services like VPCs, subnets, NAT Gateways, and Internet Gateways. This ensures that the internal, private IP addresses of the pods are not exposed directly to the public internet while still allowing outbound communication.
