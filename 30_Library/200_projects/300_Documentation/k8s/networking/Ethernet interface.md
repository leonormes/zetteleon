---
aliases: []
confidence: 
created: 2025-02-07T12:57:54Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:48Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [containers, networking]
title: Ethernet interface
type: documentation
uid: 
updated: 
version: 1
---

An Ethernet interface is a network interface that enables devices to communicate using the Ethernet protocol, which is widely used in local area networks (LANs) and wide area networks (WANs). Ethernet interfaces are physical or logical components that provide connectivity for sending and receiving data packets over Ethernet networks.

## Key Characteristics of Ethernet Interfaces

- Operate at the data link layer (Layer 2) of the OSI model
- Use MAC addresses for identifying devices on the network
- Support various transmission speeds, from 10 Mbps to multiple Gbps
- Typically use twisted pair cables (e.g., Cat5, Cat6) or fiber optic cables for connections
- Follow IEEE 802.3 standards for protocols and specifications

## Other Types of Network Interfaces

1. Serial Interfaces:
   - Use serial transmission, sending one bit at a time
   - Examples include RS-232, RS-485, and UART[8]
   - Typically used for short-distance, low-speed communications

2. Wireless Interfaces:
   - Utilize radio waves for data transmission
   - Include Wi-Fi (IEEE 802.11 standards)[12]
   - Offer mobility and convenience

3. Fiber Channel (FC) Interfaces:
   - Designed for high-speed data transfer in storage area networks (SANs)[14]
   - Use fiber optic cables for transmission

4. InfiniBand (IB) Interfaces:
   - High-performance computing interconnect technology[14]
   - Used in data centers and supercomputers

5. Virtual Interfaces:
   - Software-defined interfaces without physical hardware
   - Examples include TUN (network layer) and TAP (data link layer) interfaces[15]

6. Loopback Interfaces:
   - Virtual network interfaces used for internal communication within a device[2]

7. Tunnel Interfaces:
   - Used for creating virtual private networks (VPNs) or other encapsulated connections[6]

8. Bridge Interfaces:
   - Connect multiple network segments at the data link layer[15]

9. Aggregate Interfaces:
   - Combine multiple physical interfaces into a single logical interface for increased bandwidth and redundancy[6]

These various interface types cater to different networking requirements, from high-speed data center connections to virtual private networks and specialized industrial applications.

To create and manage veth devices using the ip command-line interface on Linux, follow these best practices:

## Creating Veth Pairs

To create a veth pair:

```bash
ip link add <veth1> type veth peer name <veth2>
```

For example:

```bash
ip link add veth0 type veth peer name veth1
```

This creates two connected virtual Ethernet interfaces named veth0 and veth1.

## Configuring Veth Interfaces

After creating the veth pair, configure and activate the interfaces:

1. Assign IP addresses:

```bash
ip addr add 192.168.1.1/24 dev veth0
ip addr add 192.168.1.2/24 dev veth1
```

2. Bring up the interfaces:

```bash
ip link set veth0 up
ip link set veth1 up
```

## Best Practices

1. Use descriptive names for veth interfaces to indicate their purpose or connection.
2. When connecting veth interfaces to network namespaces:

```bash
ip link set veth1 netns <namespace>
```

3. For connecting containers or namespaces, create one veth in the host namespace and move the peer to the target namespace.
4. When using veth pairs with bridges:

```bash
ip link add br0 type bridge
ip link set veth0 master br0
```

5. Set appropriate MTU size if needed:

```bash
ip link set veth0 mtu 9000
```

6. Use the `ip link show` command to verify the status and configuration of veth devices.
7. Clean up unused veth pairs to avoid clutter:

```bash
ip link delete veth0
```

This will automatically remove both ends of the veth pair.

8. When troubleshooting, use `tcpdump` on veth interfaces to capture and analyze traffic.
9. Consider using network namespaces to isolate veth pairs for different applications or services.
10. Document your veth configurations, especially in complex setups involving multiple namespaces or containers.

By following these practices, you can effectively create and manage veth devices for various networking scenarios in Linux[1][2][5].

The command `ip link add veth0 type veth peer name veth1` is used in Linux to create a virtual Ethernet (veth) pair, which consists of two connected virtual network interfaces. These interfaces are commonly used for network namespaces, container networking, and virtualized network setups.

### Command Syntax Breakdown

Here is a breakdown of the command, with each argument explained:

1. `ip`

    - The main command for managing networking in Linux. It provides utilities for network interfaces, addresses, routes, and more.
2. `link`

    - Specifies that you are managing a network link (interface). This is part of the `ip` subcommands for interacting with physical and virtual interfaces.
3. `add`

    - Indicates you want to create (add) a new network link or interface.
4. `veth0`

    - The name of the first interface in the veth pair. You can choose any valid interface name (e.g., `veth0`, `veth-peer0`, etc.).
5. `type veth`

    - Specifies the type of network interface to create.
    - `veth` stands for virtual Ethernet and represents a pair of connected virtual interfaces. Data sent on one end (e.g., `veth0`) appears on the other end (e.g., `veth1`), mimicking an Ethernet cable.
6. `peer name veth1`

    - `peer`: Designates that you are creating the other end of the veth pair.
    - `name veth1`: Assigns the name of the peer interface connected to the first (`veth0`). This name can also be arbitrary.

---

### Why Is It Structured This Way

The syntax is structured to be modular and extendable, reflecting the flexibility of Linux's networking tools. Here’s why:

- Declarative: The command specifies exactly what you want to do (add a link of type `veth`) and its parameters (names and peers).
- Consistency: The `ip` utility follows a consistent format across subcommands, with `object (link/address/route)` followed by `operation (add/del/show)` and then configuration options.
- Flexibility: This design allows users to interact with various network objects (interfaces, routes, addresses, etc.) using a unified command structure.

---

### Other Options for `ip link add`

The `ip link add` command supports several other types and configurations. Here are some commonly used options:

#### Types of Links

- `bridge`: Creates a software bridge device for connecting multiple interfaces.
    - Example: `ip link add br0 type bridge`
- `dummy`: Creates a dummy interface for testing or administrative purposes.
    - Example: `ip link add dummy0 type dummy`
- `bond`: Creates a bonded interface for combining multiple physical links into one (e.g., for redundancy or performance).
    - Example: `ip link add bond0 type bond`
- `vxlan`: Creates a VXLAN interface for overlay networking.
    - Example: `ip link add vxlan0 type vxlan id 42 dev eth0`
- `macvlan`: Creates a MACVLAN interface to assign a separate MAC address for containers or virtual machines.
    - Example: `ip link add macvlan0 link eth0 type macvlan mode bridge`

#### Additional Options

- `mtu <size>`: Set the maximum transmission unit for the interface.
    - Example: `ip link add veth0 type veth mtu 1400 peer name veth1`
- `netns <namespace>`: Assign one of the veth pair interfaces to a specific network namespace.
    - Example: `ip link add veth0 type veth peer name veth1 netns ns1`
- `txqueuelen <number>`: Set the transmit queue length for the interface.
    - Example: `ip link add veth0 type veth txqueuelen 1000 peer name veth1`

---

### Use Case Example

A common scenario is setting up a pair of veth interfaces, where one end is inside a network namespace (e.g., for container networking):

```bash
ip link add veth0 type veth peer name veth1
ip link set veth1 netns mynamespace
```

- This creates a veth pair (`veth0` and `veth1`).
- `veth1` is moved into the `mynamespace` network namespace.
- `veth0` remains in the default namespace, acting as a bridge between the two namespaces.

---

### Summary

- Purpose: Creates a veth pair, which is vital for linking network namespaces, containers, or virtualized environments.
- Syntax: Modular and extensible, following a consistent `ip` utility structure.
- Options: Flexible, supporting different link types and configurations, allowing diverse network setups.

This design enables precise, declarative network configurations, making it a powerful tool for both simple and complex networking tasks.
