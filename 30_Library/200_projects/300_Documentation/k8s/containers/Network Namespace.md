---
aliases: []
confidence: 
created: 2025-02-07T12:57:54Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:47Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [containers, namespace]
title: Network Namespace
type:
uid: 
updated: 
version:
---

A network namespace in Linux is an isolated networking environment that provides a separate set of networking resources and configurations. It is one of the namespaces available in the Linux kernel that enables containerization and the creation of lightweight, isolated environments.

## What is a Network Namespace

A network namespace is a feature that creates a virtual instance of the [[networking stack]]. Each namespace has its own isolated network devices, IP addresses, routing tables, firewall rules, sockets, and other network-related configurations. Processes running inside a network namespace cannot directly access resources of other network namespaces unless explicitly connected.

By default, the Linux kernel has a single, global network namespace, but new ones can be created and managed.

---

## Default Features of a Network Namespace

When a new network namespace is created, it is a blank slate with its own default properties:

### 1. Private Network Interfaces

- A network namespace starts without any network interfaces. You can add virtual interfaces (e.g., veth pairs) or physical interfaces to it.
- Each namespace can have its own set of network interfaces that are isolated from the interfaces in other namespaces.

### 2. Independent IP Addressing

- Each namespace can have its own IP addresses for its interfaces (both IPv4 and IPv6).
- These addresses are completely independent of the addresses in other namespaces.

### 3. Separate Routing Tables

- Each namespace maintains its own independent routing table, allowing for unique routes and policies specific to that namespace.

### 4. Unique Firewall Rules (Netfilter)

- A namespace has its own instance of Netfilter, allowing independent configuration of iptables rules for NAT, filtering, and other packet-processing tasks.

### 5. Private ARP and Neighbor Tables

- Each namespace has its own ARP (Address Resolution Protocol) table for IPv4 and neighbor table for IPv6. This means it resolves MAC-to-IP mappings independently of other namespaces.

### 6. Isolated Sockets

- Processes in a network namespace use isolated sockets. They cannot directly see or connect to sockets in other namespaces unless explicitly bridged or configured.

### 7. Own Network Devices

- A namespace can contain its own network devices, such as:
- Physical interfaces (e.g., `eth0` or `wlan0` if moved into the namespace).
- Virtual interfaces (e.g., `veth` pairs, bridges, or tunnels).
- By default, a new namespace starts without any devices, not even a loopback interface until manually enabled.

### 8. Loopback Interface

- Each namespace has its own loopback interface (`lo`). The loopback interface is not active in a new namespace by default but can be enabled using:

```bash
ip link set lo up
```

### 9. Independent DNS Configuration

- Each namespace can have its own DNS resolver settings by modifying `/etc/resolv.conf` or using tools like `systemd-resolved`.

### 10. Process Isolation

- Only processes inside the namespace can use the networking resources of that namespace. Processes from other namespaces cannot interfere with or access the network namespace unless explicitly configured.

---

## Use Cases of Network Namespaces

1. Containerization: Tools like Docker, Kubernetes, and Podman rely on network namespaces to isolate the network of containers.
2. Network Virtualization: Simulate complex network setups for testing and development.
3. Multitenancy: Provide isolated network environments for different users or applications on the same host.
4. Security: Limit network access for specific applications or processes.

---

## Limitations

- Network namespaces do not inherently share resources; explicit bridges, veth pairs, or other mechanisms are required to connect namespaces.
- Managing and monitoring multiple namespaces requires familiarity with tools like `ip netns`, `ip link`, and `nsenter`.

The `ip` tool is a powerful command-line utility used for network configuration and management in Linux. It is part of the iproute2 suite and replaces older tools like `ifconfig`, `route`, and `arp`. The `ip` tool provides a consistent and flexible way to interact with networking features in the Linux kernel.

---

## General Structure of the `ip` Command

The basic syntax for the `ip` command is:

```bash
ip [OPTIONS] OBJECT {COMMAND | help}
```

- OPTIONS: Options that modify the behavior of the `ip` command (e.g., `-s` for statistics).
- OBJECT: The networking object to interact with, such as `link`, `address`, `route`, etc.
- COMMAND: The specific action to perform on the object, such as `add`, `delete`, `show`, etc.

---

## Commonly Used Objects and Subcommands

### 1. Link

Manages network interfaces.

- Subcommands:
- `show [dev DEVICE]`: Display information about network interfaces.

```bash
ip link show
```

- `set dev DEVICE [options]`: Configure a network interface.

```bash
ip link set dev eth0 up      # Bring the interface up
ip link set dev eth0 down    # Bring the interface down
ip link set dev eth0 mtu 1500 # Set the MTU
ip link set dev eth0 promisc on # Enable promiscuous mode
```

- `add`: Add a virtual link.
- `delete`: Remove a virtual link.

---

### 2. Address

Manages IP addresses assigned to network interfaces.

- Subcommands:
- `show [dev DEVICE]`: Display IP addresses.

```bash
ip address show
ip address show dev eth0
```

- `add ADDRESS dev DEVICE`: Add an IP address.

```bash
ip address add 192.168.1.10/24 dev eth0
```

- `delete ADDRESS dev DEVICE`: Remove an IP address.

```bash
ip address delete 192.168.1.10/24 dev eth0
```

---

### 3. Route

Manages routing tables.

- Subcommands:
- `show [table TABLE]`: Display the routing table.

```bash
ip route show
```

- `add ROUTE`: Add a route.

```bash
ip route add 192.168.2.0/24 via 192.168.1.1 dev eth0
```

- `delete ROUTE`: Remove a route.

```bash
ip route delete 192.168.2.0/24
```

---

### 4. Rule

Manages policy routing rules.

- Subcommands:
- `show`: Display routing rules.

```bash
ip rule show
```

- `add`: Add a new rule.

```bash
ip rule add from 192.168.1.0/24 lookup 100
```

- `delete`: Remove a rule.

```bash
ip rule delete from 192.168.1.0/24
```

---

### 5. Netns

Manages network namespaces.

- Subcommands:
- `list`: List all network namespaces.

```bash
ip netns list
```

- `add NAME`: Create a new network namespace.

```bash
ip netns add mynamespace
```

- `delete NAME`: Delete a network namespace.

```bash
ip netns delete mynamespace
```

- `exec NAME COMMAND`: Execute a command in a namespace.

```bash
ip netns exec mynamespace ip addr show
```

---

### 6. Tunnel

Manages tunnels (GRE, IP-in-IP, etc.).

- Subcommands:
- `add NAME mode MODE [options]`: Add a tunnel.

```bash
ip tunnel add mytun mode gre local 192.168.1.1 remote 192.168.1.2
```

- `delete NAME`: Remove a tunnel.

```bash
ip tunnel delete mytun
```

- `show`: Display tunnel information.

```bash
ip tunnel show
```

---

### 7. Neighbor

Manages ARP/ND (Neighbor Discovery Protocol) entries.

- Subcommands:
- `show`: Display neighbor entries.

```bash
ip neighbor show
```

- `add`: Add a neighbor entry.

```bash
ip neighbor add 192.168.1.2 lladdr 00:11:22:33:44:55 dev eth0
```

- `delete`: Remove a neighbor entry.

```bash
ip neighbor delete 192.168.1.2 dev eth0
```

---

### 8. Monitor

Monitors changes to the network configuration in real-time.

- Command:

```bash
ip monitor [object]
```

Example:

```bash
ip monitor all
```

---

## Common Options

- `-s`: Show additional statistics.
- `-4`: Use IPv4 only.
- `-6`: Use IPv6 only.
- `-c`: Show colorized output (where supported).

---

## Examples

1. Add an IP address to an interface:

```bash
ip address add 192.168.1.100/24 dev eth0
```

2. View the routing table:

```bash
ip route show
```

3. Create and view a network namespace:

```bash
ip netns add testns
ip netns exec testns ip address show
```

The `ip` tool is versatile and essential for managing Linux networking tasks. Let me know if you need more examples or details on a specific subcommand!

The behavior you're observing is a consequence of how Linux network namespaces (netns) are implemented and how visibility of namespaces is handled.

## Understanding the Behavior

1. Isolated Interfaces (`ip a`):

- When you create a new network namespace, it starts with only the loopback interface (`lo`). This ensures that the processes in this namespace cannot directly access or see the network interfaces from the host or other namespaces, which is the desired isolation.
2. Namespace Visibility (`ip netns show`):

- The `ip netns` command operates in the global namespace context. It lists all the network namespaces that are present on the host system. This includes namespaces that you or other processes have created, regardless of which namespace you're currently operating in.
- This visibility is not scoped to your current namespace but reflects the global namespace where `ip netns` maintains its state.

---

## Why This Happens

- Netns Management in User Space:
- Network namespaces are kernel-level constructs. Tools like `ip netns` are user-space utilities provided by `iproute2`.
- The `ip netns` command does not query the namespaces from within your current namespace. Instead, it looks at the `/var/run/netns` directory on the host, which acts as a user-space registry of named namespaces.
- As a result, even from within an isolated namespace, you can still see all network namespaces listed by `ip netns` because the command interacts with the global namespace.
- Security Considerations:
- This visibility does not compromise isolation. Even though you can see the names of all network namespaces, you cannot interact with or access them unless explicitly granted permission.

---

## How to Fix or Hide This

If you want the `ip netns` command to respect namespace isolation:

1. Create a Separate Environment for `/var/run/netns`:

- Use a mount namespace (`unshare --mount`) to isolate `/var/run/netns`.
- Remount an empty directory as `/var/run/netns` in the new namespace:

```bash
mkdir /tmp/netns
mount --bind /tmp/netns /var/run/netns
```

- After this, `ip netns show` will no longer list the global namespaces because the directory is now isolated.
2. Leverage User Privileges:

- Ensure the processes in the isolated namespace do not have elevated privileges that allow them to query the global `/var/run/netns`.

---

## Key Takeaways

- The behavior is expected and stems from `ip netns` being a user-space utility that operates in the global context.
- While it lists all namespaces, this does not break network isolation.
- Use mount namespaces or other techniques to mask global visibility if required for your use case.
