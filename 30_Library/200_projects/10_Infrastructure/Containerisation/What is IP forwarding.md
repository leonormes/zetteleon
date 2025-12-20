---
aliases: []
confidence: 
created: 2025-10-24T15:11:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [kernel, linux, routing, topic/technology/networking, type/fact]
title: What is IP forwarding
type: Factual
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - Container Networking Model]]
- Related: [[What is iptables NAT MASQUERADE]], [[How a packet exits a container via NAT]]

## Summary

IP forwarding is a Linux kernel parameter (`net.ipv4.ip_forward`) that controls whether the system routes packets between network interfaces, acting as a router rather than just an endpoint.

## Context / Problem

By default, Linux systems drop packets destined for other interfaces—they only accept packets addressed to their own IPs. Container networking requires the host to act as a router, forwarding packets from container namespaces to external networks and between containers. Without IP forwarding enabled, containers are isolated islands with no connectivity.

## Mechanism / Details

### What Is It

IP forwarding is a kernel setting that enables:

- Routing packets between network interfaces (e.g., `eth0` → `cni0`)
- Acting as a gateway for containers/VMs
- Bridging isolated network namespaces
- Multi-homed host behavior (packets arriving on one interface can exit another)

### Checking the Setting

```bash
# Check current value (0=disabled, 1=enabled)
sysctl net.ipv4.ip_forward
# or
cat /proc/sys/net/ipv4/ip_forward
```

### Enabling IP Forwarding

```bash
# Temporary (lost on reboot)
sysctl -w net.ipv4.ip_forward=1

# Permanent (survives reboot)
echo 'net.ipv4.ip_forward=1' >> /etc/sysctl.conf
sysctl -p
```

### How It Works

When a packet arrives:

1. Kernel checks if the destination IP matches a local interface
2. **If no** → Check `ip_forward` setting
   - If `ip_forward=0` → Drop packet
   - If `ip_forward=1` → Consult routing table and forward to next hop
3. **If yes** → Deliver to local application

### IPv6 Forwarding

IPv6 has a separate setting:

```bash
sysctl -w net.ipv6.conf.all.forwarding=1
```

## Connections / Implications

### What This Enables

- **Container networking**: Packets flow from Pod → veth → bridge → host interface → internet
- **Kubernetes networking**: Nodes act as routers for Pod traffic
- **Multi-node communication**: Cross-node Pod traffic is routed through nodes
- **NAT functionality**: Forwarding is prerequisite for iptables NAT to work

### What Breaks If This Fails

- **Pods cannot reach external networks**: Packets are dropped at the host
- **Pod-to-Pod cross-node fails**: Packets never leave the source node
- **Services unreachable**: kube-proxy rules ineffective without forwarding
- **NAT doesn't work**: MASQUERADE rules require forwarding to function

### How It Maps to Kubernetes

- **kubelet**: Often enables `ip_forward` during node initialization
- **CNI plugins**: Some CNI plugins check/enable this setting
- **kube-proxy**: Assumes forwarding is enabled for Service routing
- **Node readiness**: Disabled forwarding can prevent node from becoming Ready

### Security Considerations

- **Firewall bypass risk**: Forwarding can route traffic around firewall rules if misconfigured
- **Unintended routing**: Packets from untrusted interfaces may reach internal networks
- **Best practice**: Combine with iptables INPUT/FORWARD chains to control forwarding

### Example Debug Scenario

```bash
# Symptom: Pods cannot ping external IPs
# Check:
sysctl net.ipv4.ip_forward
# Output: net.ipv4.ip_forward = 0

# Fix:
sysctl -w net.ipv4.ip_forward=1

# Test:
kubectl exec -it pod-name -- ping 8.8.8.8
# Now works!
```

## Questions / To Explore

- [[How does the Linux kernel routing table work?]]
- [[What is the FORWARD iptables chain?]]
- [[How do you trace packet forwarding with tcpdump?]]
- [[DEBUG - IP forwarding enabled but Pods still cannot reach internet]]
- [[How does Docker enable IP forwarding automatically?]]
- [[What is reverse path filtering (rp_filter)?]]
