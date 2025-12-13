---
aliases: []
confidence: 
created: 2025-02-07T12:57:54Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [containers, networking]
title: network-namespace-exploration
type: instruction
uid: 
updated: 
version: 1
---

## Understanding Linux's Default Network Namespace

The default network namespace is the foundation of Linux networking. Think of it as the master blueprint that contains all your system's network interfaces, routing rules, and firewall configurations. When you create new network namespaces for containers, you're essentially making isolated copies of this blueprint.

### Examining Network Interfaces

Let's start by looking at the network interfaces in the default namespace:

```bash
# Show all network interfaces
ip link show

# The output might look like:
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 00:15:5d:01:ca:05 brd ff:ff:ff:ff:ff:ff
```

The output shows us several important things:

- The loopback interface (lo) is always present
- Physical or virtual network interfaces (like eth0)
- Each interface's state (UP/DOWN)
- MTU (Maximum Transmission Unit) settings
- MAC addresses for each interface

### Understanding IP Addresses

Let's examine how IP addresses are assigned in the default namespace:

```bash
# Show IP address configuration
ip addr show

# More detailed view of a specific interface
ip addr show dev eth0

# The output might look like:
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 00:15:5d:01:ca:05 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.100/24 brd 192.168.1.255 scope global dynamic eth0
    inet6 fe80::215:5dff:fe01:ca05/64 scope link
```

This shows us:

- IPv4 and IPv6 addresses assigned to each interface
- Network mask (/24 indicates a 255.255.255.0 subnet)
- Broadcast address
- Scope (global means reachable from anywhere)

### Routing Configuration

The routing table determines how network traffic is directed:

```bash
# Show routing table
ip route show

# The output might look like:
default via 192.168.1.1 dev eth0 
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.100
```

This tells us:

- The default gateway (where traffic goes if no other route matches)
- Direct routes to connected networks
- The source IP used for outgoing packets

### Examining Network Statistics

Let's look at how the interfaces are performing:

```bash
# Show interface statistics
ip -s link show

# More detailed statistics for specific interface
ip -s -s link show dev eth0

# The output shows:
# - Packets transmitted and received
# - Bytes transmitted and received
# - Errors and dropped packets
```

### Network Protocol Configuration

The default namespace also manages protocol-specific settings:

```bash
# Show ARP cache (IPv4 address to MAC mapping)
ip neigh show

# Show socket statistics
ss -s

# Show active connections
ss -tuln
```

### Understanding Process Network Context

Every process on your system inherits this default namespace unless specifically configured otherwise:

```bash
# Show network namespace of a process
ls -l /proc/[PID]/ns/net

# Show which processes are using which network interfaces
lsof -i

# Show listening ports and their processes
netstat -tulpn
```

### Practical Exploration Exercises

1. Watch Network Interface Changes:

```bash
# Open a terminal and run
watch -n1 'ip addr show'

# In another terminal, bring an interface down and up
sudo ip link set eth0 down
sudo ip link set eth0 up
```

2. Monitor Network Traffic:

```bash
# Watch interface statistics in real-time
watch -n1 'ip -s link show eth0'

# Generate some traffic
ping 8.8.8.8
```

3. Examine Connection States:

```bash
# Watch active connections
watch -n1 'ss -tan'

# Make some connections
curl http://example.com
```

### Common Configuration Tasks

1. Changing IP Addresses:

```bash
# Add an IP address
sudo ip addr add 192.168.1.200/24 dev eth0

# Remove an IP address
sudo ip addr del 192.168.1.200/24 dev eth0
```

2. Modifying Routes:

```bash
# Add a static route
sudo ip route add 10.0.0.0/24 via 192.168.1.1

# Delete a route
sudo ip route del 10.0.0.0/24
```

3. Changing Interface Properties:

```bash
# Change MTU
sudo ip link set eth0 mtu 9000

# Change interface state
sudo ip link set eth0 down
sudo ip link set eth0 up
```

### Debugging Tools and Techniques

1. Connectivity Testing:

```bash
# Test basic connectivity
ping 8.8.8.8

# Trace network path
traceroute 8.8.8.8

# Check DNS resolution
dig google.com
```

2. Traffic Analysis:

```bash
# Watch packets in real-time
sudo tcpdump -i eth0

# Monitor bandwidth usage
sudo iftop -i eth0
```

3. Socket Investigation:

```bash
# Show all listening ports
sudo netstat -tulpn

# Show established connections
sudo netstat -tun
```

### Understanding the Relationship with Container Networking

When you create a container or a new network namespace, it starts as a copy of this default namespace but:

- Has its own isolated set of interfaces
- Has its own routing table
- Has its own firewall rules
- Cannot see the interfaces in the default namespace unless explicitly connected

This isolation is what enables containers to have their own networking stack without interfering with the host or other containers.
