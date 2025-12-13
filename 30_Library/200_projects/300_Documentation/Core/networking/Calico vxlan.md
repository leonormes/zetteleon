---
aliases: []
author: 
confidence: 
created: 2025-03-25T06:15:16Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source: https://docs.tigera.io/calico/latest/networking/configuring/vxlan-ipip
source_of_truth: []
status: 
tags: [calico, networking]
title: Calico vxlan
type: 
uid: 
updated: 
version: 
---

## Overlay Networking | Calico Documentation

## Overlay Networking

### Big picture[​](#big-picture "Direct link to Big picture")

Enable inter workload communication across networks that are not aware of workload IPs.

### Value[​](#value "Direct link to Value")

In general, we recommend running Calico without network overlay/encapsulation. This gives you the highest performance and simplest network; the packet that leaves your workload is the packet that goes on the wire.

However, selectively using overlays/encapsulation can be useful when running on top of an underlying network that cannot easily be made aware of workload IPs. A common example is if you are using Calico networking in AWS across multiple VPCs/subnets. In this case, Calico can selectively encapsulate only the traffic that is routed between the VPCs/subnets, and run without encapsulation within each VPC/subnet. You might also decide to run your entire Calico network with encapsulation as an overlay network -- as a quick way to get started without setting up BGP peering or other routing information in your underlying network.

### Concepts[​](#concepts "Direct link to Concepts")

#### Routing Workload IP addresses[​](#routing-workload-ip-addresses "Direct link to Routing workload IP addresses")

Networks become aware of workload IP addresses through layer 3 routing techniques like static routes or BGP route distribution, or layer 2 address learning. As such, they can route unencapsulated traffic to the right host for the endpoint that is the ultimate destination. However, not all networks are able to route workload IP addresses. For example, public cloud environments where you don’t own the hardware, AWS across VPC subnet boundaries, and other scenarios where you cannot peer Calico over BGP to the underlay, or easily configure static routes. This is why Calico supports encapsulation, so you can send traffic between workloads without requiring the underlying network to be aware of workload IP addresses.

#### Encapsulation types[​](#encapsulation-types "Direct link to Encapsulation types")

Calico supports two types of encapsulation: VXLAN and IP in IP. VXLAN is supported in some environments where IP in IP is not (for example, Azure). VXLAN has a slightly higher per-packet overhead because the header is larger, but unless you are running very network intensive workloads the difference is not something you would typically notice. The other small difference between the two types of encapsulation is that Calico's VXLAN implementation does not use BGP, whereas Calico's IP in IP implementation uses BGP between Calico nodes.

#### Cross-subnet[​](#cross-subnet "Direct link to Cross-subnet")

Encapsulation of workload traffic is typically required only when traffic crosses a router that is unable to route workload IP addresses on its own. Calico can perform encapsulation on: all traffic, no traffic, or only on traffic that crosses a subnet boundary.

### Before You begin[​](#before-you-begin "Direct link to Before you begin")

**Not supported**

-   Calico for OpenStack (i.e. when Calico is used as the Neutron plugin)

**Limitations**

-   IP in IP supports only IPv4 addresses
-   VXLAN in IPv6 is only supported for kernel versions ≥ 4.19.1 or redhat kernel version ≥ 4.18.0

### How to[​](#how-to "Direct link to How to")

-   [Configure default IP pools at install time](#configure-default-ip-pools-at-install-time)
-   [Configure IP in IP encapsulation for only cross-subnet traffic](#configure-ip-in-ip-encapsulation-for-only-cross-subnet-traffic)
-   [Configure IP in IP encapsulation for all inter workload traffic](#configure-ip-in-ip-encapsulation-for-all-inter-workload-traffic)
-   [Configure VXLAN encapsulation for only cross-subnet traffic](#configure-vxlan-encapsulation-for-only-cross-subnet-traffic)
-   [Configure VXLAN encapsulation for all inter workload traffic](#configure-vxlan-encapsulation-for-all-inter-workload-traffic)

#### Best practice[​](#best-practice "Direct link to Best practice")

Calico has an option to selectively encapsulate only traffic that crosses subnet boundaries. We recommend using the **cross-subnet** option with IP in IP or VXLAN to minimize encapsulation overhead. Cross-subnet mode provides better performance in AWS multi-AZ deployments, Azure VNETs, and on networks where routers are used to connect pools of nodes with L2 connectivity.

Be aware that switching encapsulation modes can cause disruption to in-progress connections. Plan accordingly.

#### Configure Default IP Pools at Install time[​](#configure-default-ip-pools-at-install-time "Direct link to Configure default IP pools at install time")

Default IP pools are configured at install-time automatically by Calico. You can configure these default IP pools based on install method.

-   Operator
-   Manifest

For operator managed clusters, you can configure encapsulation in the IP pools section of the default Installation. For example, the following installation snippet will enable VXLAN across subnets.

```sh
kind: Installation
```

For manifest installations of Calico, you can control the default IP pool encapsulation mode using the `CALICO\_IPV4POOL\_VXLAN` and `CALICO\_IPV4POOL\_IPIP` (and `CALICO\_IPV6POOL\_VXLAN` for IPv6) environment variables in the environment of the `calico-node` daemon set.

#### Configure IP in IP Encapsulation for only Cross-subnet traffic[​](#configure-ip-in-ip-encapsulation-for-only-cross-subnet-traffic "Direct link to Configure IP in IP encapsulation for only cross-subnet traffic")

IP in IP encapsulation can be performed selectively, and only for traffic crossing subnet boundaries.

To enable this feature, set `ipipMode` to `CrossSubnet`.

```sh
apiVersion: projectcalico.org/v3
```

#### Configure IP in IP Encapsulation for All Inter Workload traffic[​](#configure-ip-in-ip-encapsulation-for-all-inter-workload-traffic "Direct link to Configure IP in IP encapsulation for all inter workload traffic")

With `ipipMode` set to `Always`, Calico routes traffic using IP in IP for all traffic originating from a Calico enabled-host, to all Calico networked containers and VMs within the IP pool.

```sh
apiVersion: projectcalico.org/v3
```

#### Configure VXLAN Encapsulation for only Cross Subnet traffic[​](#configure-vxlan-encapsulation-for-only-cross-subnet-traffic "Direct link to Configure VXLAN encapsulation for only cross subnet traffic")

VXLAN encapsulation can be performed selectively, and only for traffic crossing subnet boundaries.

To enable this feature, set `vxlanMode` to `CrossSubnet`.

```sh
apiVersion: projectcalico.org/v3
```

#### Configure VXLAN Encapsulation for All Inter Workload traffic[​](#configure-vxlan-encapsulation-for-all-inter-workload-traffic "Direct link to Configure VXLAN encapsulation for all inter workload traffic")

With `vxlanMode` set to `Always`, Calico routes traffic using VXLAN for all traffic originating from a Calico enabled host, to all Calico networked containers and VMs within the IP pool.

```sh
apiVersion: projectcalico.org/v3
```

If you use only VXLAN pools, BGP networking is not required. You can disable BGP to reduce the moving parts in your cluster by [Customizing the manifests](https://docs.tigera.io/calico/latest/getting-started/kubernetes/self-managed-onprem/config-options). Set the `calico_backend` setting to `vxlan`, and disable the BGP readiness check.

### Additional resources[​](#additional-resources "Direct link to Additional resources")

For details on IP pool resource options, see [IP pool](https://docs.tigera.io/calico/latest/reference/resources/ippool).

<https://qdnqn.com/networking-on-kubernetes-calico-and-ebpf/>
