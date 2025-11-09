---
aliases: []
confidence: 
created: 2025-10-27T19:47:54Z
epistemic: 
last_reviewed: 
modified: 2025-10-31T09:09:16Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [networking]
title: I installed Calico cni. what is vxlan in Calico an
type:
uid: 
updated: 
version:
---

## I Installed Calico Cni. what is Vxlan in Calico and when Should I Use it

VXLAN (Virtual Extensible LAN) in Calico is an overlay networking technology that encapsulates Layer 2 traffic over Layer 3 networks. It is used to connect Kubernetes pods across nodes or subnets, particularly in environments where traditional IP routing methods like BGP or IP-in-IP are not feasible or desirable.

### When to Use VXLAN in Calico

1. **Cloud Environments with Restrictions**: VXLAN is ideal for public clouds (e.g., Azure) where IP-in-IP is unsupported or where the underlying network cannot route pod IPs[^1_1][^1_5][^1_8].
2. **Avoiding BGP Dependencies**: Unlike IP-in-IP, VXLAN does not require BGP, reducing complexity in clusters without BGP support[^1_1][^1_2].
3. **Cross-Subnet Traffic**: Use VXLAN in "CrossSubnet" mode to encapsulate traffic only when it crosses subnet boundaries, improving performance for intra-subnet communication[^1_1][^1_9][^1_11].
4. **Simplified Multi-Cluster Networking**: VXLAN can be leveraged for multi-cluster setups, allowing seamless pod-to-pod communication without complex routing configurations[^1_10].
5. **Hybrid and Multi-Region Deployments**: It supports scenarios where underlay network routing is challenging, such as hybrid cloud or multi-region Kubernetes clusters[^1_10].

### Configuration Options

- **Always Mode**: Encapsulates all inter-workload traffic using VXLAN.
- **CrossSubnet Mode**: Encapsulates only cross-subnet traffic, optimizing performance for local traffic[^1_1][^1_6].

VXLAN is particularly useful for scalable and platform-agnostic networking in modern Kubernetes environments.

<span style="display:none">[^1_3][^1_4][^1_7]</span>

<div align="center">⁂</div>

[^1_1]: <https://docs.tigera.io/calico/latest/networking/configuring/vxlan-ipip>

[^1_2]: <https://joshrosso.com/c/calico-routing-modes/>

[^1_3]: <http://platform9.com/docs/kubernetes/networking-integration-with-calico>

[^1_4]: <https://www.youtube.com/watch?v=WMLSD2y2Ig4>

[^1_5]: <https://support.tools/training/networking/kubernetes-vxlan/>

[^1_6]: <https://ubuntu.com/kubernetes/charmed-k8s/docs/cni-calico>

[^1_7]: <https://www.cisco.com/c/en/us/td/docs/dcn/whitepapers/extending-kubernetes-clusters-with-nx-os-vxlan-and-calico.html>

[^1_8]: <https://qdnqn.com/networking-on-kubernetes-calico-and-ebpf/>

[^1_9]: <https://kops.sigs.k8s.io/networking/calico/>

[^1_10]: <https://www.tigera.io/blog/deep-dive/how-to-create-a-cluster-mesh-with-calico-cni-and-vxlan/>

[^1_11]: <https://docs.tigera.io/calico/latest/networking/determine-best-networking>

---

## What Are the Main Use Cases for VXLAN in a Kubernetes Cluster

The main use cases for VXLAN in a Kubernetes cluster include:

1. **Cross-Node Pod Communication**: VXLAN enables seamless communication between pods on different nodes by encapsulating Layer 2 traffic over a Layer 3 network, making it ideal for multi-node clusters[^2_1][^2_2].
2. **Cloud Environments**: It is particularly useful in public clouds where direct pod-to-pod routing is not feasible due to network restrictions or lack of support for IP-in-IP encapsulation[^2_1][^2_2].
3. **Multi-Cluster and Hybrid Deployments**: VXLAN simplifies networking in multi-cluster setups or hybrid cloud environments by creating an overlay network that abstracts the underlying infrastructure[^2_3][^2_8].
4. **Scalability**: VXLAN supports up to 16 million virtual networks (VNIs), far exceeding the 4,000 VLAN limit, which is beneficial for large-scale Kubernetes deployments with many isolated workloads[^2_5].
5. **Simplified Network Configuration**: It eliminates the need for complex VLAN configurations by creating logical Layer 2 networks over existing Layer 3 infrastructure, reducing operational overhead[^2_1][^2_5].
6. **Cluster Meshes**: In tools like Calico, VXLAN can be used to create cluster meshes, allowing pod networks to communicate without manual routing configurations[^2_8].

These features make VXLAN a versatile choice for Kubernetes networking in complex or large-scale environments.

<span style="display:none">[^2_4][^2_6][^2_7]</span>

<div align="center">⁂</div>

[^2_1]: <https://support.tools/training/networking/kubernetes-vxlan/>

[^2_2]: <https://www.youtube.com/watch?v=WMLSD2y2Ig4>

[^2_3]: <https://www.cisco.com/c/en/us/td/docs/dcn/whitepapers/extending-kubernetes-clusters-with-nx-os-vxlan-and-calico.html>

[^2_4]: <https://www.reddit.com/r/networking/comments/17gpp0o/whats_the_only_advantage_of_vxlan_in_campus/>

[^2_5]: <https://www.yellow-bricks.com/2012/11/02/vxlan-use-cases/>

[^2_6]: <https://github.com/openvnf/kube-vxlan-controller>

[^2_7]: <https://www.eficode.com/blog/debugging-kubernetes-networking>

[^2_8]: <https://www.tigera.io/blog/deep-dive/how-to-create-a-cluster-mesh-with-calico-cni-and-vxlan/>
