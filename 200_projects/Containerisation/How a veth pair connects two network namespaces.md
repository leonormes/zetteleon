---
aliases: []
confidence: 
created: 2025-10-24T15:15:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:27Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [container, linux, namespace, topic/technology/networking, type/mechanism, veth]
title: How a veth pair connects two network namespaces
type: Mechanism
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - Container Networking Model]]
- Related: [[What is a veth pair]], [[What is a network namespace]], [[How to create and connect network namespaces]]

## Summary

A veth pair creates a bidirectional pipe between two network namespaces by placing each end in a different namespace, enabling point-to-point packet forwarding as if connected by a virtual cable.

## Context / Problem

Network namespaces are completely isolated—they cannot communicate by default. To enable communication between two namespaces (e.g., a Pod and the host, or two Pods), you need a mechanism that bridges the isolation boundary. A veth pair solves this by acting as a virtual Ethernet cable where packets entering one end immediately exit the other, even across namespace boundaries.

## Mechanism / Details

### Step-by-Step Packet Flow

#### Setup Phase

```bash
# 1. Create two namespaces (simulating two Pods)
ip netns add pod-red
ip netns add pod-blue

# 2. Create a veth pair
ip link add veth-red type veth peer name veth-blue
# At this point, both ends exist in the root namespace

# 3. Move each end to its respective namespace
ip link set veth-red netns pod-red
ip link set veth-blue netns pod-blue

# 4. Assign IP addresses
ip -n pod-red addr add 10.0.1.1/24 dev veth-red
ip -n pod-blue addr add 10.0.1.2/24 dev veth-blue

# 5. Bring interfaces up
ip -n pod-red link set veth-red up
ip -n pod-blue link set veth-blue up
ip -n pod-red link set lo up  # Enable loopback
ip -n pod-blue link set lo up
```

#### Packet Transmission: Pod-red → Pod-blue

1. **Application sends data**

   ```bash
   ip netns exec pod-red ping 10.0.1.2
   ```

2. **Pod-red namespace routing**
   - Kernel checks routing table: `ip -n pod-red route`
   - Destination `10.0.1.2` matches `10.0.1.0/24` → Use `veth-red`

3. **Packet enters veth-red**
   - IP packet constructed: `src=10.0.1.1, dst=10.0.1.2`
   - Ethernet frame: `src=veth-red MAC, dst=veth-blue MAC`
   - Packet written to `veth-red` interface

4. **Kernel forwards through veth pair**
   - Kernel recognizes `veth-red` is paired with `veth-blue`
   - Packet is **immediately transferred** to `veth-blue`
   - No intermediate network devices or routers involved

5. **Packet exits veth-blue**
   - Packet appears on `veth-blue` in `pod-blue` namespace
   - Kernel delivers to `pod-blue`'s network stack

6. **Pod-blue processes packet**
   - Destination IP matches local interface (10.0.1.2)
   - ICMP echo request processed
   - Reply sent back through the same path in reverse

### Key Characteristics

**Speed**: No actual network traversal—just kernel memory copy  
**Directionality**: Fully bidirectional (duplex)  
**Layer**: Operates at Layer 2 (Ethernet frames)  
**Isolation**: Each namespace sees only its end of the pair  
**Discovery**: Ends can be identified using `ethtool -S veth-red` (shows peer index)

### Debugging Commands

```bash
# Verify veth pair connectivity
ip netns exec pod-red ip link show veth-red
ip netns exec pod-blue ip link show veth-blue

# Check if interfaces are UP
ip netns exec pod-red ip link | grep veth-red
# Should show: state UP

# Verify routing
ip netns exec pod-red ip route
# Should show: 10.0.1.0/24 dev veth-red scope link

# Test connectivity
ip netns exec pod-red ping -c 3 10.0.1.2

# Capture traffic on one end
ip netns exec pod-red tcpdump -i veth-red -n
```

### Common Failure Modes

| Issue | Symptom | Fix |
|-------|---------|-----|
| Interface DOWN | `ping: Network is unreachable` | `ip -n pod-red link set veth-red up` |
| No IP assigned | `ping: connect: Network is unreachable` | `ip -n pod-red addr add 10.0.1.1/24 dev veth-red` |
| Wrong subnet | Packets sent but no reply | Ensure both IPs in same /24 subnet |
| One end deleted | Both ends disappear | Recreate the veth pair |
| Namespace deleted | Veth pair destroyed | Namespace lifecycle owns veth ends |

## Connections / Implications

### What This Enables

- **Pod isolation with connectivity**: Namespaces remain isolated but can selectively communicate
- **Container networking foundation**: Every CNI plugin uses veth pairs for Pod connectivity
- **Kubernetes Pod `eth0`**: The Pod's primary interface is always one end of a veth pair
- **Host-side networking**: The other veth end is attached to a bridge or routing table on the host

### What Breaks If This Fails

- **Pod cannot start**: CNI ADD operation fails if veth creation fails
- **Pod loses connectivity**: If the host-side veth is deleted, Pod is unreachable
- **Performance degradation**: MTU mismatch on veth pair causes fragmentation
- **Network policies broken**: Firewall rules applied to veth interfaces become ineffective

### How It Maps to Kubernetes

```sh
┌─────────────────────────────────────┐
│         Pod Network Namespace       │
│                                     │
│   ┌──────────────────┐              │
│   │ Container eth0   │              │
│   │ (veth end 1)     │              │
│   │ IP: 10.244.1.5   │              │
│   └────────┬─────────┘              │
└────────────┼──────────────────────────┘
             │ veth pair
             │ (bidirectional)
┌────────────▼──────────────────────────┐
│       Host Network Namespace         │
│                                      │
│   ┌──────────────────┐               │
│   │ vethXXXXXX       │               │
│   │ (veth end 2)     │               │
│   │ Attached to cni0 │               │
│   └────────┬─────────┘               │
│            │                         │
│   ┌────────▼─────────┐               │
│   │   cni0 bridge    │               │
│   └──────────────────┘               │
└──────────────────────────────────────┘
```

- **kubelet**: Invokes CNI plugin to create veth pair during Pod creation
- **CNI plugin**: Creates veth, moves one end into Pod namespace, assigns IP
- **Pod `eth0`**: Always the namespace-internal end of a veth pair
- **Host `vethXXXXX`**: Randomly named, attached to bridge or routing table

### Real-World Example

```bash
# On Kubernetes node, find a Pod's veth
kubectl get pod nginx-pod -o jsonpath='{.status.containerStatuses[0].containerID}'
# Extract container ID: abc123...

# Find the veth on the host
ip link | grep veth
# Output: veth4f2a1b2@if3: <BROADCAST,MULTICAST,UP,LOWER_UP>

# Trace the pair
ip link show veth4f2a1b2
# Shows: link/ether ... with peer index (e.g., if3)

# Inside Pod
kubectl exec -it nginx-pod -- ip link show eth0
# Shows: eth0@if12 (index 3, paired with host veth)
```

## Questions / To Explore

- [[How does kubelet invoke CNI to create veth pairs?]]
- [[How do you identify which veth belongs to which Pod?]]
- [[What happens if veth MTU mismatches the bridge MTU?]]
- [[DEBUG - Veth pair exists but ping fails]]
- [[How does Calico use veth pairs differently than bridge CNI?]]
- [[Can you have multiple veth pairs in one namespace?]]
