---
aliases: []
confidence: 
created: 2025-10-24T15:17:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:27Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [container, egress, iptables, linux, nat, topic/technology/networking, type/mechanism]
title: How a packet exits a container via NAT
type: Mechanism
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - Container Networking Model]]
- Related: [[What is iptables NAT MASQUERADE]], [[What is IP forwarding]], [[What is a Linux bridge]]

## Summary

When a container sends a packet to an external IP address, it flows through the container's veth pair, across the bridge to the host's network interface, where iptables MASQUERADE rewrites the source IP to the host's public IP, enabling the packet to traverse the internet and return via connection tracking.

## Context / Problem

Containers use private, non-routable IP addresses (e.g., 10.244.0.x) from their Pod CIDR. Internet routers would drop packets with these source IPs because they're not globally routable. Additionally, return packets wouldn't know how to reach the container. NAT (specifically MASQUERADE) solves this by making all container traffic appear to originate from the host's public IP, with connection tracking ensuring replies are correctly reverse-translated back to the original container.

## Mechanism / Details

### Prerequisites

```bash
# 1. IP forwarding MUST be enabled
sysctl -w net.ipv4.ip_forward=1

# 2. MASQUERADE iptables rule MUST exist
iptables -t nat -A POSTROUTING -s 10.244.0.0/16 ! -d 10.244.0.0/16 -j MASQUERADE

# The rule means:
# - Source (-s): Traffic from Pod CIDR (10.244.0.0/16)
# - NOT destination (! -d): Exclude same-network traffic (Pod-to-Pod)
# - Action: MASQUERADE (rewrite source IP to outgoing interface IP)
```

### Complete Packet Flow: Pod → Internet → Pod

#### Outbound Path (Pod Sends Packet to 8.8.8.8)

```sh
Step 1: Application in pod-red sends packet
┌─────────────────────────────────────────┐
│ Pod-red (10.244.0.10)                   │
│ Application: curl http://example.com    │
│ Packet created:                         │
│   src=10.244.0.10:54321                 │
│   dst=93.184.216.34:80 (example.com)    │
└─────────────────┬───────────────────────┘
                  │
Step 2: Routing decision in pod-red
│ Pod routing table:                      │
│   default via 10.244.0.1 dev veth-red   │
│ Decision: Send to gateway 10.244.0.1    │
                  │
Step 3: Packet enters veth pair
│ veth-red (pod) → veth-red-br (host)     │
│ Packet unchanged at this point          │
                  │
Step 4: Packet arrives at bridge
│ v-net-0 (cni0) bridge                   │
│ MAC lookup: dst=10.244.0.1 (bridge IP)  │
│ Forward to host routing stack           │
                  │
Step 5: Host routing decision
│ Host routing table:                     │
│   default via 192.168.1.1 dev eth0      │
│ Decision: Send via eth0 to 192.168.1.1  │
│ (IP forwarding enabled, so proceed)     │
                  │
Step 6: POSTROUTING iptables NAT chain
│ iptables -t nat -L POSTROUTING          │
│ Rule matches:                           │
│   -s 10.244.0.0/16 ! -d 10.244.0.0/16   │
│ Action: MASQUERADE                      │
│                                         │
│ *** PACKET REWRITTEN ***                │
│   OLD: src=10.244.0.10:54321            │
│   NEW: src=203.0.113.5:38472 (host IP) │
│   dst=93.184.216.34:80 (unchanged)      │
│                                         │
│ Conntrack entry created:                │
│   10.244.0.10:54321 ↔ 203.0.113.5:38472 │
                  │
Step 7: Packet exits host via eth0
│ Physical NIC transmits packet           │
│   src=203.0.113.5:38472                 │
│   dst=93.184.216.34:80                  │
└─────────────────┬───────────────────────┘
                  │
              INTERNET
                  │
Step 8: External server receives packet
│ Server sees: src=203.0.113.5:38472      │
│ (No knowledge of 10.244.0.10)           │
│ Processes request, sends reply          │
                  │
```

#### Inbound Path (Reply from Internet)

```sh
Step 9: Reply packet arrives at host
┌─────────────────────────────────────────┐
│ Packet arrives at eth0:                 │
│   src=93.184.216.34:80                  │
│   dst=203.0.113.5:38472                 │
└─────────────────┬───────────────────────┘
                  │
Step 10: Conntrack lookup
│ Kernel checks connection tracking table │
│ Finds matching entry:                   │
│   203.0.113.5:38472 ↔ 10.244.0.10:54321 │
│                                         │
│ *** REVERSE NAT APPLIED ***             │
│   OLD: dst=203.0.113.5:38472            │
│   NEW: dst=10.244.0.10:54321            │
│   src=93.184.216.34:80 (unchanged)      │
                  │
Step 11: Host routing decision
│ Routing table consulted:                │
│   10.244.0.0/24 dev v-net-0             │
│ Decision: Send to bridge v-net-0        │
                  │
Step 12: Bridge forwards to pod
│ v-net-0 MAC table lookup:               │
│   10.244.0.10 → veth-red-br             │
│ Frame forwarded to veth-red-br          │
                  │
Step 13: Packet enters veth pair
│ veth-red-br (host) → veth-red (pod)     │
                  │
Step 14: Pod receives packet
┌─────────────────▼───────────────────────┐
│ Pod-red (10.244.0.10)                   │
│ Application receives reply:             │
│   src=93.184.216.34:80                  │
│   dst=10.244.0.10:54321                 │
│ curl displays response                  │
└─────────────────────────────────────────┘
```

### Key Components

1. **IP Forwarding** (`net.ipv4.ip_forward=1`)
   - Enables kernel to route packets between interfaces
   - Without this, packets are dropped after reaching the bridge

2. **MASQUERADE Rule**
   - Operates in `nat` table, `POSTROUTING` chain
   - Triggered AFTER routing decision, just before packet exits
   - Dynamically uses outgoing interface's IP

3. **Connection Tracking (conntrack)**
   - Kernel module that tracks active connections
   - Stores bidirectional mapping: `pod-IP:port ↔ host-IP:port`
   - Enables reverse NAT for replies
   - View active connections: `conntrack -L`

### Verification Commands

```bash
# 1. Check IP forwarding
sysctl net.ipv4.ip_forward
# Should return: 1

# 2. Verify MASQUERADE rule exists
iptables -t nat -L POSTROUTING -n -v
# Look for MASQUERADE target with source 10.244.0.0/16

# 3. Test egress from pod
ip netns exec pod-red ping -c 3 8.8.8.8
# Should succeed

# 4. View conntrack entries during connection
watch -n 1 'conntrack -L | grep 10.244.0.10'
# Shows active NAT mappings

# 5. Capture outbound traffic on host interface
tcpdump -i eth0 -n src host 203.0.113.5
# Packets should show host IP as source, not pod IP

# 6. Trace packet path
ip netns exec pod-red traceroute 8.8.8.8
# First hop should be bridge IP (10.244.0.1)
```

### Common Failure Scenarios

| Issue | Symptom | Debug Command | Fix |
|-------|---------|---------------|-----|
| IP forwarding OFF | Pod cannot reach external IPs | `sysctl net.ipv4.ip_forward` | `sysctl -w net.ipv4.ip_forward=1` |
| No MASQUERADE rule | Packets leave with pod IP, replies lost | `iptables -t nat -L POSTROUTING` | Add MASQUERADE rule |
| Wrong source subnet in rule | Only some pods affected | Check `-s` range in rule | Update rule to match Pod CIDR |
| Conntrack table full | New connections fail | `conntrack -L \| wc -l` | Increase `nf_conntrack_max` |
| Firewall blocks forwarded traffic | Packets dropped at FORWARD chain | `iptables -L FORWARD -v` | Add ACCEPT rule for pod traffic |

## Connections / Implications

### What This Enables

- **Internet access for Pods**: Pods can reach public services (DNS, APIs, etc.)
- **Hide internal topology**: External servers see only node IPs, not pod IPs
- **Load balancer health checks**: ALB/NLB can reach Pods via NodePort
- **Kubernetes default behavior**: All CNI plugins implement egress NAT

### What Breaks If This Fails

- **DNS resolution fails**: If DNS servers are external (e.g., 8.8.8.8)
- **Internet connectivity lost**: `curl`, `apt-get`, API calls all fail
- **Container image pulls fail**: Cannot reach external registries
- **Outbound webhooks fail**: Pods cannot notify external services

### How It Maps to Kubernetes

**CNI Plugin Responsibilities:**

- **Bridge CNI**: Adds MASQUERADE rule during setup
- **Calico**: Uses iptables rules for egress (can disable SNAT per policy)
- **Flannel**: Adds MASQUERADE for cross-node traffic

**kube-proxy Does NOT:**

- kube-proxy manages Service → Pod DNAT
- It does NOT handle Pod → External SNAT/MASQUERADE
- That's the CNI plugin's job

**Network Policies:**

- Can block egress at Layer 3/4
- Applied BEFORE MASQUERADE (in FORWARD chain)
- Calico uses iptables rules to implement policies

### Security Implications

- **All Pods share node IP for egress**: External services see the same source IP for all Pods on a node
- **Port conflicts**: MASQUERADE uses different source ports to distinguish connections
- **Egress filtering**: Implement NetworkPolicy to restrict which Pods can reach external IPs
- **NAT traversal**: Some protocols (FTP, SIP) require ALG (Application Level Gateway) support

## Questions / To Explore

- [[How does conntrack maintain state for thousands of connections?]]
- [[What is the difference between SNAT and MASQUERADE?]]
- [[How do you troubleshoot conntrack table exhaustion?]]
- [[DEBUG - Pod can reach same-node Pods but not external IPs]]
- [[How does Calico implement per-Pod egress policies without MASQUERADE?]]
- [[What happens when MASQUERADE port pool is exhausted?]]
