---
aliases: []
confidence: 
created: 2025-10-24T15:10:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [firewall, iptables, linux, nat, topic/technology/networking, type/fact]
title: What is iptables NAT MASQUERADE
type: Factual
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - Container Networking Model]]
- Related: [[What is IP forwarding]], [[How a packet exits a container via NAT]]

## Summary

iptables MASQUERADE is a type of Source NAT (SNAT) that dynamically rewrites the source IP address of outgoing packets to match the interface's IP address, enabling containers with private IPs to access external networks.

## Context / Problem

Containers use private IP addresses (e.g., 10.244.0.0/16) that are not routable on the internet. When a container sends packets to external destinations, routers would drop return packets because the source IP is non-routable. MASQUERADE solves this by replacing the container's source IP with the node's public IP, making return traffic possible.

## Mechanism / Details

### What Is It

MASQUERADE is an iptables target in the **NAT table, POSTROUTING chain** that:

- Rewrites the **source IP** of outgoing packets to the outgoing interface's IP
- Tracks connections in the **conntrack** table to reverse the translation for replies
- Dynamically adapts to interface IP changes (unlike static SNAT)
- Only applies to packets leaving the host

### How It Differs from SNAT

- **SNAT**: Requires specifying a fixed IP address (`--to-source 203.0.113.5`)
- **MASQUERADE**: Automatically uses the outgoing interface's current IP
- **Use case**: MASQUERADE is ideal for dynamic IPs (DHCP, NAT gateways)

### Creating a MASQUERADE Rule

```bash
# Enable IP forwarding (required for NAT)
sysctl -w net.ipv4.ip_forward=1

# MASQUERADE all traffic from Pod CIDR
iptables -t nat -A POSTROUTING -s 10.244.0.0/16 -j MASQUERADE

# List NAT rules
iptables -t nat -L POSTROUTING -n -v
```

### Packet Flow Example

1. **Pod sends packet**: `src=10.244.0.5, dst=8.8.8.8`
2. **POSTROUTING MASQUERADE**: Rewrites `src=203.0.113.10` (node IP)
3. **External server sees**: `src=203.0.113.10, dst=8.8.8.8`
4. **Reply packet**: `src=8.8.8.8, dst=203.0.113.10`
5. **Conntrack reverses NAT**: Rewrites `dst=10.244.0.5`
6. **Pod receives**: `src=8.8.8.8, dst=10.244.0.5`

## Connections / Implications

### What This Enables

- **Container internet access**: Pods can reach external services without public IPs
- **Security**: Hides internal Pod IP structure from external networks
- **Kubernetes egress**: Default behavior for Pod-to-internet traffic
- **Multi-tenant isolation**: All Pods appear to originate from the node IP

### What Breaks If This Fails

- Pods cannot reach external IPs (e.g., `curl google.com` fails)
- DNS resolution to external servers fails (if DNS is external)
- Kubernetes Services with `type: LoadBalancer` may fail health checks
- Return traffic is lost because external routers drop replies to private IPs

### How It Maps to Kubernetes

- **kube-proxy**: Does NOT create MASQUERADE rules (common misconception)
- **CNI plugins**: Responsible for MASQUERADE setup (e.g., Calico, Flannel)
- **kubelet**: May configure MASQUERADE for certain CNI plugins
- **Pod egress traffic**: Always MASQUERADE'd unless using a custom CNI policy

### Common Scenarios

```bash
# Allow only specific Pods to egress
iptables -t nat -A POSTROUTING -s 10.244.0.0/24 ! -d 10.0.0.0/8 -j MASQUERADE

# Exclude internal traffic from MASQUERADE
iptables -t nat -A POSTROUTING -s 10.244.0.0/16 ! -d 10.244.0.0/16 -j MASQUERADE
```

## Questions / To Explore

- How does conntrack maintain NAT state?
- What is the difference between SNAT, MASQUERADE, and DNAT?
- How does kube-proxy use iptables for Services?
- DEBUG - Pod can reach same-node Pods but not external IPs
- How does Calico implement MASQUERADE differently than bridge CNI?
- What happens when the NAT table is full?
