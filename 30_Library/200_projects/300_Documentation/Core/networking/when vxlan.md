---
aliases: []
confidence: 
created: 2025-03-25T06:21:56Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [calico, networking]
title: when vxlan
type: 
uid: 
updated: 
version: 
---

I installed Calico cni. what is vxlan in Calico and when should I use it

VXLAN (Virtual Extensible LAN) in Calico is an overlay networking technology that encapsulates Layer 2 traffic over Layer 3 networks. It is used to connect Kubernetes pods across nodes or subnets, particularly in environments where traditional IP routing methods like BGP or IP-in-IP are not feasible or desirable.

## When to Use VXLAN in Calico
1. **Cloud Environments with Restrictions**: VXLAN is ideal for public clouds (e.g., Azure) where IP-in-IP is unsupported or where the underlying network cannot route pod IPs[1][5][8].
2. **Avoiding BGP Dependencies**: Unlike IP-in-IP, VXLAN does not require BGP, reducing complexity in clusters without BGP support[1][2].
3. **Cross-Subnet Traffic**: Use VXLAN in "CrossSubnet" mode to encapsulate traffic only when it crosses subnet boundaries, improving performance for intra-subnet communication[1][9][11].
4. **Simplified Multi-Cluster Networking**: VXLAN can be leveraged for multi-cluster setups, allowing seamless pod-to-pod communication without complex routing configurations[10].
5. **Hybrid and Multi-Region Deployments**: It supports scenarios where underlay network routing is challenging, such as hybrid cloud or multi-region Kubernetes clusters[10].

## Configuration Options
- **Always Mode**: Encapsulates all inter-workload traffic using VXLAN.
- **CrossSubnet Mode**: Encapsulates only cross-subnet traffic, optimizing performance for local traffic[1][6].

VXLAN is particularly useful for scalable and platform-agnostic networking in modern Kubernetes environments.

Citations:

[1] Overlay networking - Calico Documentation - Tigera <https://docs.tigera.io/calico/latest/networking/configuring/vxlan-ipip>

[2] Calico Routing Modes - joshrosso <https://joshrosso.com/c/calico-routing-modes/>

[3] Calico CNI - Platform9 Docs <http://platform9.com/docs/kubernetes/networking-integration-with-calico>

[4] What is VXLAN and How It is Used as an Overlay Network in ... <https://www.youtube.com/watch?v=WMLSD2y2Ig4>

[5] How Kubernetes Uses VXLAN for Overlay Networking - Support Tools <https://support.tools/training/networking/kubernetes-vxlan/>

[6] CNI with Calico - Ubuntu <https://ubuntu.com/kubernetes/charmed-k8s/docs/cni-calico>

[7] Extending Kubernetes Clusters with Cisco NX-OS VxLAN and Calico <https://www.cisco.com/c/en/us/td/docs/dcn/whitepapers/extending-kubernetes-clusters-with-nx-os-vxlan-and-calico.html>

[8] Kubernetes Calico: Networking explained - qdnqn <https://qdnqn.com/networking-on-kubernetes-calico-and-ebpf/>

[9] Calico - kOps - Kubernetes Operations <https://kops.sigs.k8s.io/networking/calico/>

[10] How to create a cluster mesh with Calico CNI and VXLAN - Tigera <https://www.tigera.io/blog/deep-dive/how-to-create-a-cluster-mesh-with-calico-cni-and-vxlan/>

[11] Determine best networking option - Calico Documentation - Tigera <https://docs.tigera.io/calico/latest/networking/determine-best-networking>

What are the main use cases for VXLAN in a Kubernetes cluster

The main use cases for VXLAN in a Kubernetes cluster include:

1. **Cross-Node Pod Communication**: VXLAN enables seamless communication between pods on different nodes by encapsulating Layer 2 traffic over a Layer 3 network, making it ideal for multi-node clusters[1][2].
2. **Cloud Environments**: It is particularly useful in public clouds where direct pod-to-pod routing is not feasible due to network restrictions or lack of support for IP-in-IP encapsulation[1][2].
3. **Multi-Cluster and Hybrid Deployments**: VXLAN simplifies networking in multi-cluster setups or hybrid cloud environments by creating an overlay network that abstracts the underlying infrastructure[3][8].
4. **Scalability**: VXLAN supports up to 16 million virtual networks (VNIs), far exceeding the 4,000 VLAN limit, which is beneficial for large-scale Kubernetes deployments with many isolated workloads[5].
5. **Simplified Network Configuration**: It eliminates the need for complex VLAN configurations by creating logical Layer 2 networks over existing Layer 3 infrastructure, reducing operational overhead[1][5].
6. **Cluster Meshes**: In tools like Calico, VXLAN can be used to create cluster meshes, allowing pod networks to communicate without manual routing configurations[8].

These features make VXLAN a versatile choice for Kubernetes networking in complex or large-scale environments.

Citations:

[1] How Kubernetes Uses VXLAN for Overlay Networking - Support Tools <https://support.tools/training/networking/kubernetes-vxlan/>

[2] What is VXLAN and How It is Used as an Overlay Network in ... <https://www.youtube.com/watch?v=WMLSD2y2Ig4>

[3] Extending Kubernetes Clusters with Cisco NX-OS VxLAN and Calico <https://www.cisco.com/c/en/us/td/docs/dcn/whitepapers/extending-kubernetes-clusters-with-nx-os-vxlan-and-calico.html>

[4] What's the only advantage of VXLAN in campus environment? - Reddit <https://www.reddit.com/r/networking/comments/17gpp0o/whats_the_only_advantage_of_vxlan_in_campus/>

[5] VXLAN basics and use cases (when / when not to use it) <https://www.yellow-bricks.com/2012/11/02/vxlan-use-cases/>

[6] openvnf/kube-vxlan-controller - GitHub <https://github.com/openvnf/kube-vxlan-controller>

[7] Debugging Kubernetes Networking - Eficode.com <https://www.eficode.com/blog/debugging-kubernetes-networking>

[8] How to create a cluster mesh with Calico CNI and VXLAN - Tigera <https://www.tigera.io/blog/deep-dive/how-to-create-a-cluster-mesh-with-calico-cni-and-vxlan/>
