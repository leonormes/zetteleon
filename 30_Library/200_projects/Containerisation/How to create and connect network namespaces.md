---
aliases: []
confidence: 
created: 2025-10-24T15:18:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [container, linux, namespace, topic/technology/networking, type/mechanism]
title: How to create and connect network namespaces
type: Mechanism
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - Container Networking Model]]
- Related: [[What is a network namespace]], [[How a veth pair connects two network namespaces]], [[How to set up a Linux bridge for container networking]]

## Summary

Creating and connecting network namespaces involves using `ip netns add` to create isolated network stacks, then bridging them with veth pairs or attaching them to Linux bridges to enable controlled communication between isolated environments.

## Context / Problem

Containers need network isolation for security and multi-tenancy, but they also need connectivity for communication. Linux network namespaces provide the isolation, but must be explicitly connected using virtual network devices. This is the foundation of all container networking—understanding this manual process reveals what CNI plugins automate.

## Mechanism / Details

### Step-by-Step: Complete Namespace Setup

#### 1. Create Network Namespaces

```bash
# Create two namespaces (simulating two Pods)
ip netns add pod-red
ip netns add pod-blue

# Verify creation
ip netns list
# Output:
# pod-blue
# pod-red

# Check namespace details
ls -l /var/run/netns/
# Shows namespace mount points
```

**What Happens:**

- Kernel creates isolated network stack
- New namespace starts with only loopback interface (down)
- Namespace is "mounted" in `/var/run/netns/`

#### 2. Inspect Initial Namespace State

```bash
# Check interfaces in new namespace
ip netns exec pod-red ip link show
# Output:
# 1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN

# Check routing table (empty)
ip netns exec pod-red ip route
# No routes

# Check iptables (clean slate)
ip netns exec pod-red iptables -L
# Empty chains
```

**Initial State:**

- Only `lo` interface exists (DOWN)
- No IP addresses assigned
- No routes configured
- No iptables rules

#### 3. Bring Up Loopback

```bash
# Loopback must be enabled for local processes
ip -n pod-red link set lo up
ip -n pod-blue link set lo up

# Assign loopback IP
ip -n pod-red addr add 127.0.0.1/8 dev lo
ip -n pod-blue addr add 127.0.0.1/8 dev lo

# Test loopback
ip netns exec pod-red ping -c 2 127.0.0.1
# Should work
```

### Connection Method 1: Point-to-Point (Veth Pair)

For **two namespaces** that need direct connectivity:

```bash
# 1. Create veth pair
ip link add veth-red type veth peer name veth-blue

# 2. Move ends to namespaces
ip link set veth-red netns pod-red
ip link set veth-blue netns pod-blue

# 3. Assign IPs (same subnet)
ip -n pod-red addr add 10.0.1.1/24 dev veth-red
ip -n pod-blue addr add 10.0.1.2/24 dev veth-blue

# 4. Bring interfaces up
ip -n pod-red link set veth-red up
ip -n pod-blue link set veth-blue up

# 5. Verify connectivity
ip netns exec pod-red ping -c 2 10.0.1.2
# SUCCESS: Direct path via veth pair

# 6. Check routes (automatically added)
ip -n pod-red route
# Output:
# 10.0.1.0/24 dev veth-red scope link
```

**Result:** Two namespaces connected directly, no bridge needed.

### Connection Method 2: Multi-Namespace (Bridge)

For **multiple namespaces** that all need to communicate:

```bash
# 1. Create a bridge on the host
ip link add v-net-0 type bridge
ip link set v-net-0 up
ip addr add 10.244.0.1/24 dev v-net-0

# 2. Create veth pairs (one per namespace)
ip link add veth-red type veth peer name veth-red-br
ip link add veth-blue type veth peer name veth-blue-br

# 3. Move namespace ends
ip link set veth-red netns pod-red
ip link set veth-blue netns pod-blue

# 4. Attach bridge ends to bridge
ip link set veth-red-br master v-net-0
ip link set veth-blue-br master v-net-0

# 5. Bring everything up
ip link set veth-red-br up
ip link set veth-blue-br up
ip -n pod-red link set veth-red up
ip -n pod-blue link set veth-blue up

# 6. Assign IPs to namespaces
ip -n pod-red addr add 10.244.0.10/24 dev veth-red
ip -n pod-blue addr add 10.244.0.20/24 dev veth-blue

# 7. Add default routes via bridge
ip -n pod-red route add default via 10.244.0.1
ip -n pod-blue route add default via 10.244.0.1

# 8. Test connectivity
ip netns exec pod-red ping -c 2 10.244.0.20  # pod-to-pod
ip netns exec pod-red ping -c 2 10.244.0.1   # pod-to-gateway
```

**Result:** Multiple namespaces connected via bridge, scalable architecture.

### Connection Method 3: Namespace-to-Host

For namespace connectivity to the **host namespace**:

```bash
# 1. Create veth pair (one end stays in host namespace)
ip link add veth-pod type veth peer name veth-host

# 2. Move only one end to namespace
ip link set veth-pod netns pod-red

# 3. Configure IPs (different subnets)
ip addr add 10.1.1.1/24 dev veth-host      # Host end
ip -n pod-red addr add 10.1.1.2/24 dev veth-pod

# 4. Bring up
ip link set veth-host up
ip -n pod-red link set veth-pod up

# 5. Test
ping 10.1.1.2  # Host to pod
ip netns exec pod-red ping 10.1.1.1  # Pod to host
```

**Result:** Namespace can communicate with host processes.

### Advanced: Executing Commands in Namespaces

```bash
# Run single command
ip netns exec pod-red ping 8.8.8.8

# Start interactive shell
ip netns exec pod-red /bin/bash
# Now in pod-red namespace context

# Run daemon in namespace (stays running)
ip netns exec pod-red nohup nc -l 8080 &

# Alternative: nsenter (by PID)
# Find namespace PID
ip netns pids pod-red
# Enter namespace
nsenter --net=/var/run/netns/pod-red /bin/bash
```

### Cleanup

```bash
# Delete namespace (automatically removes all interfaces)
ip netns del pod-red

# Veth pairs attached to the namespace are also destroyed
# Bridge-side veth (veth-red-br) is removed automatically
```

## Connections / Implications

### What This Enables

- **Container isolation**: Each container gets its own network stack
- **Kubernetes Pod networking**: Kubelet creates namespaces for each Pod
- **Testing and debugging**: Manually replicate container networking for learning
- **Custom network topologies**: Build complex multi-namespace scenarios

### What Breaks If This Fails

- **Pod creation fails**: If namespace creation fails, Pod enters CrashLoopBackOff
- **Network isolation lost**: Without namespaces, containers share host network
- **IP conflicts**: Containers without namespaces cannot bind to same ports
- **CNI plugin failures**: If CNI cannot create/access namespaces

### How It Maps to Kubernetes

**kubelet's Role:**

1. Creates network namespace for Pod
2. Invokes CNI plugin via `CNI ADD` command
3. CNI plugin:
   - Creates veth pair
   - Moves one end into Pod namespace
   - Attaches other end to bridge
   - Assigns IP via IPAM
   - Configures routes
4. Returns network config to kubelet

**Pause Container:**

- Kubernetes creates a "pause" container first
- Pause container holds the network namespace open
- Other containers in the Pod join this namespace
- When pause dies, entire Pod networking collapses

### Debugging Techniques

```bash
# List all namespaces
ip netns list

# Find which namespace a process is in
ps -ef | grep <process>
ls -l /proc/<PID>/ns/net

# Compare namespaces
ip netns exec pod-red ip addr
ip addr  # Host namespace

# Monitor namespace creation
watch -n 1 'ip netns list'

# Check namespace mount points
ls -l /var/run/netns/

# Capture traffic in namespace
ip netns exec pod-red tcpdump -i veth-red
```

## Questions / To Explore

- [[How does kubelet create network namespaces for Pods?]]
- [[What is the pause container and why does it exist?]]
- [[How do multiple containers share a Pod's network namespace?]]
- [[DEBUG - Namespace creation succeeds but Pod has no connectivity]]
- [[How does Docker create network namespaces?]]
- [[What are the performance implications of network namespaces?]]
