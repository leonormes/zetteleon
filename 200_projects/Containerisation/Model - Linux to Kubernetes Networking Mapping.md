---
aliases: []
confidence: 
created: 2025-10-24T15:21:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [cni, container, kubernetes, linux, mapping, topic/technology/networking, type/model]
title: Model - Linux to Kubernetes Networking Mapping
type: Model
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - Container Networking Model]]
- Related: [[What is a network namespace]], [[What is a veth pair]], [[What is a Linux bridge]], [[What is iptables NAT MASQUERADE]]

## Summary

A comprehensive mapping that translates manual Linux networking primitives (namespaces, veth pairs, bridges, iptables) into their automated Kubernetes equivalents (Pods, CNI plugins, Services, kube-proxy), revealing what CNI plugins and kubelet abstract away.

## Context / Problem

Kubernetes networking appears magical—Pods communicate seamlessly without visible configuration. This abstraction hides the fact that Kubernetes **automates the exact same Linux primitives** you would configure manually. Understanding this mapping is critical for:

- **Debugging**: "If kube-proxy uses iptables, I can inspect iptables rules to debug Services"
- **Architecture decisions**: "Choosing Calico vs Flannel means choosing L3 routing vs L2 bridging"
- **Troubleshooting**: "If a Pod can't reach others, check if the veth pair exists"

## Model

### Complete Mapping Table

| Linux Primitive | Kubernetes Equivalent | Managed By | Layer |
|-----------------|------------------------|------------|-------|
| **Network namespace** (`ip netns`) | Pod network namespace | kubelet | - |
| **Veth pair** (`ip link add type veth`) | Pod `eth0` ↔ Node veth | CNI plugin | L2 |
| **Linux bridge** (`ip link add type bridge`) | `cni0` bridge | CNI plugin (bridge, flannel) | L2 |
| **IP address assignment** | Pod IP from Pod CIDR | IPAM plugin (host-local, etc.) | L3 |
| **Default route** (`ip route add default`) | Pod default gateway | CNI plugin | L3 |
| **IP forwarding** (`sysctl ip_forward=1`) | Enabled by kubelet/CNI | kubelet, CNI plugin | L3 |
| **iptables MASQUERADE** | Pod egress SNAT | CNI plugin | L3 (NAT) |
| **iptables DNAT** (manual Service NAT) | Service ClusterIP → Pod IP | kube-proxy | L3/L4 (NAT) |
| **iptables port forwarding** | NodePort, LoadBalancer | kube-proxy | L4 |
| **Routing table entries** | Cross-node Pod routes | CNI plugin (Calico, etc.) | L3 |
| **ARP** (MAC learning) | Bridge MAC table | Automatic (kernel) | L2 |

### Detailed Component Mappings

#### 1. Network Namespace → Pod Network Namespace

**Linux:**

```bash
ip netns add pod-red
```

**Kubernetes:**

- **kubelet** creates a network namespace for each Pod
- Namespace is held open by the **pause container**
- Other containers in the Pod join this namespace (`docker run --net=container:pause`)
- View on node: `ip netns list` (may require symlink setup)

**Key Files:**

- `/var/run/netns/<pod-namespace>` (if CNI creates symlinks)
- `/proc/<pid>/ns/net` (actual namespace reference)

---

#### 2. Veth Pair → Pod `eth0` ↔ Node `vethXXXX`

**Linux:**

```bash
ip link add veth-pod type veth peer name veth-host
ip link set veth-pod netns pod-red
```

**Kubernetes:**

- **CNI plugin** creates veth pair during Pod creation
- One end (`eth0`) placed in Pod namespace
- Other end (e.g., `veth4a2b1c3`) attached to bridge or routing table on node
- Naming: Node-side veth has random suffix for uniqueness

**Inspection:**

```bash
# On node
ip link | grep veth

# Inside Pod
kubectl exec -it <pod> -- ip link show eth0
```

---

#### 3. Linux Bridge → `cni0` Bridge

**Linux:**

```bash
ip link add cni0 type bridge
ip link set cni0 up
ip addr add 10.244.0.1/24 dev cni0
ip link set veth-host master cni0
```

**Kubernetes:**

- **Bridge CNI plugin** creates `cni0` bridge on each node
- All node-side veth ends attach to this bridge
- Bridge IP becomes default gateway for Pods
- **Note**: Calico CNI skips the bridge, using pure L3 routing

**Verification:**

```bash
ip link show cni0
bridge link show | grep cni0
```

---

#### 4. IP Address Assignment → Pod CIDR / IPAM

**Linux:**

```bash
ip -n pod-red addr add 10.244.0.10/24 dev veth-pod
```

**Kubernetes:**

- Each node gets a **Pod CIDR** subnet (e.g., node1: `10.244.0.0/24`, node2: `10.244.1.0/24`)
- **IPAM plugin** (host-local, DHCP, Calico IPAM) assigns IPs from this range
- IP stored in Pod status: `kubectl get pod <pod> -o jsonpath='{.status.podIP}'`

**CNI IPAM Config:**

```json
{
  "ipam": {
    "type": "host-local",
    "subnet": "10.244.0.0/16",
    "rangeStart": "10.244.0.10",
    "rangeEnd": "10.244.0.254"
  }
}
```

---

#### 5. Default Route → Pod Gateway

**Linux:**

```bash
ip -n pod-red route add default via 10.244.0.1
```

**Kubernetes:**

- CNI plugin configures default route in Pod namespace
- Gateway is usually the bridge IP (`cni0`) or a virtual IP
- Enables Pods to reach external IPs and other nodes

**Inspection:**

```bash
kubectl exec -it <pod> -- ip route
# Output:
# default via 10.244.0.1 dev eth0
# 10.244.0.0/24 dev eth0 scope link
```

---

#### 6. IP Forwarding → Kernel Routing

**Linux:**

```bash
sysctl -w net.ipv4.ip_forward=1
```

**Kubernetes:**

- **kubelet** or **CNI plugin** enables IP forwarding during node setup
- Required for packets to flow from Pod → Node NIC → Internet
- Check on node:

```bash
sysctl net.ipv4.ip_forward
# Should return: 1
```

---

#### 7. Iptables MASQUERADE → Pod Egress SNAT

**Linux:**

```bash
iptables -t nat -A POSTROUTING -s 10.244.0.0/16 ! -d 10.244.0.0/16 -j MASQUERADE
```

**Kubernetes:**

- **CNI plugin** (bridge, Flannel, Calico) adds MASQUERADE rules
- Allows Pods with private IPs to reach internet
- Source IP rewritten to node's public IP

**Inspection:**

```bash
iptables -t nat -L POSTROUTING -n -v | grep MASQUERADE
```

---

#### 8. Iptables DNAT → Service ClusterIP

**Linux (manual Service):**

```bash
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 10.244.0.10:8080
```

**Kubernetes:**

- **kube-proxy** creates iptables DNAT rules for each Service
- Traffic to ClusterIP:port → DNAT to Pod IP:targetPort
- Multiple Pods → random or round-robin via iptables statistic module

**Inspection:**

```bash
iptables -t nat -L KUBE-SERVICES -n | grep <clusterIP>
```

---

### Architecture Diagram: Linux Primitives in Kubernetes

```sh
┌──────────────────────────────────────────────────────┐
│                  Kubernetes Node                     │
│                                                      │
│  ┌────────────────────────────────────────┐          │
│  │         cni0 Bridge (10.244.0.1)       │          │
│  │  (Linux bridge created by CNI)         │          │
│  └──────┬──────────────┬──────────────┬───┘          │
│         │              │              │              │
│    ┌────▼─────┐   ┌───▼─────┐   ┌───▼─────┐         │
│    │veth123abc│   │veth456def│  │veth789ghi│         │
│    │(Node side)│  │(Node side)│ │(Node side)│        │
│    └────┬─────┘   └───┬─────┘   └───┬─────┘         │
└─────────┼─────────────┼─────────────┼───────────────┘
   (veth pairs cross namespace boundary)
          │             │             │
┌─────────▼──┐   ┌──────▼───┐   ┌────▼──────┐
│  Pod A NS  │   │ Pod B NS │   │ Pod C NS  │
│  eth0      │   │ eth0     │   │ eth0      │
│ 10.244.0.10│   │10.244.0.11│  │10.244.0.12│
│ (Network   │   │ (Network │   │ (Network  │
│ namespace) │   │namespace)│   │namespace) │
└────────────┘   └──────────┘   └───────────┘
```

### CNI Plugin Responsibilities

When kubelet invokes CNI `ADD` command, the CNI plugin must:

1. **Create veth pair**
2. **Move one end into Pod namespace**
3. **Attach other end** to bridge or configure routing
4. **Assign IP** from IPAM
5. **Configure default route** in Pod
6. **Add iptables rules** (MASQUERADE for egress)
7. **Return result** to kubelet (IP, gateway, routes)

Example: [Bridge CNI plugin source](https://github.com/containernetworking/plugins/tree/main/plugins/main/bridge)

### Kube-proxy Modes and Iptables

| Mode | How It Works | Linux Equivalent |
|------|--------------|------------------|
| **iptables** | DNAT rules per Service | Manual `iptables -t nat -A PREROUTING` rules |
| **IPVS** | Kernel load balancing | `ipvsadm` commands |
| **userspace** (deprecated) | Proxy daemon | `socat` or `nginx` proxy |

**iptables Mode Example:**

```bash
# Service: nginx-service (ClusterIP 10.96.0.10:80)
# Backend Pods: 10.244.0.5:8080, 10.244.0.6:8080

iptables -t nat -A KUBE-SERVICES -d 10.96.0.10/32 -p tcp --dport 80 -j KUBE-SVC-NGINX
iptables -t nat -A KUBE-SVC-NGINX -m statistic --mode random --probability 0.5 -j KUBE-SEP-POD1
iptables -t nat -A KUBE-SVC-NGINX -j KUBE-SEP-POD2
iptables -t nat -A KUBE-SEP-POD1 -j DNAT --to-destination 10.244.0.5:8080
iptables -t nat -A KUBE-SEP-POD2 -j DNAT --to-destination 10.244.0.6:8080
```

## Connections / Implications

### What This Mapping Enables

- **Troubleshooting**: "Service not working? Check kube-proxy iptables rules"
- **CNI selection**: "Need pure L3? Use Calico. Need simple L2? Use bridge CNI."
- **Performance tuning**: "iptables slow at scale? Switch to IPVS mode."
- **Learning path**: Master Linux networking → understand Kubernetes networking

### What Breaks If Automation Fails

- **CNI plugin crash**: Pods created but no veth pair → no connectivity
- **kube-proxy down**: New Services created but no iptables rules → unreachable
- **IPAM exhaustion**: No IPs available → Pods stuck in Pending
- **IP forwarding disabled**: Pods isolated on node, cannot reach external IPs

## Questions / To Explore

### Factual Gaps

- [[What is the CNI specification and ADD/DEL commands?]]
- [[What is the pause container and why does Kubernetes use it?]]
- [[What is IPAM and how do different IPAM plugins work?]]
- [[What is kube-proxy and how does it differ from CNI?]]

### Mechanism Gaps

- [[How does kubelet invoke CNI plugins during Pod creation?]]
- [[How does kube-proxy generate iptables rules for Services?]]
- [[How does Calico implement network policies with iptables?]]
- [[How does Flannel VXLAN work for cross-node traffic?]]

### Debugging Scenarios

- [[DEBUG - Pod created but no eth0 interface]]
- [[DEBUG - Service ClusterIP unreachable from Pods]]
- [[DEBUG - Pods can communicate same-node but not cross-node]]
