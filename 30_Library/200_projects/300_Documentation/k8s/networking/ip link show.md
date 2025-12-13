---
aliases: []
confidence: 
created: 2025-02-21T05:15:57Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:48Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [networking]
title: ip link show
type: info
uid: 
updated: 
version: 1
---

## Network Devices on macOS

Here's a breakdown of the network devices listed in your `ip` output, categorized and explained:

### Loopback Interfaces

-   lo0: The loopback interface. This is a virtual interface used for internal communication within the system. It's how your computer talks to itself (e.g., when you access `localhost` or `127.0.0.1`). It's always present and essential for networking functionality.

### Tunnel Interfaces

-   gif0: Generic tunnel interface. Often used for encapsulating IPv6 traffic within IPv4. Not commonly seen on typical home networks.
-   stf0: 6to4 tunnel interface. Another tunneling technology, primarily for IPv6 transition. Less common now.
-   utun0, utun1, utun2, utun3: Universal Tunnel interfaces. These are commonly used by VPN software or other applications that create virtual network interfaces. Each `utun` interface represents a separate tunnel.

### Physical Network Interfaces (Ethernet/Wi-Fi)

-   en0: Ethernet interface. This is likely your primary wired network connection. It's currently UP, meaning it's active and connected.
-   en1, en2, en3: Other Ethernet interfaces. These are likely additional physical Ethernet ports on your Mac. They are currently DOWN, meaning they are not active.
-   en4, en5, en7: More Ethernet interfaces. Likely additional physical Ethernet ports. All are currently DOWN.
-   anpi0, anpi1, anpi2: Apple Network Processor Interface. These interfaces are related to Wi-Fi. They are currently DOWN. It's possible these relate to different Wi-Fi adapters or configurations.
-   ap1: Likely another Wi-Fi interface. It is currently DOWN.

### Other Interfaces

-   bridge0: Bridge interface. This is used for network bridging, where multiple network interfaces are combined into a single network. Often used for virtualization or sharing a network connection. It is currently DOWN.
-   awdl0: Apple Wireless Direct Link. Used for peer-to-peer communication between Apple devices (e.g., AirDrop, Continuity). It's UP.
-   llw0: Low-Level Wireless. This is related to the Wi-Fi hardware and is used for low-level communication. It is currently UNKNOWN.
-   pktap0: Packet Tap interface. This is a special interface used for capturing network traffic. It's used by network monitoring tools (like Wireshark). It is currently UNKNOWN.

### Key Observations

-   You have multiple Ethernet ports (`en0` through `en7`), but only `en0` is currently active.
-   You have multiple Wi-Fi related interfaces (`anpi0` through `anpi2`, and `ap1`), but all are currently DOWN. This suggests Wi-Fi is not currently active or configured.
-   The `utun` interfaces indicate the use of VPNs or other tunneling software.
-   `awdl0` is active, meaning features like AirDrop are likely available.
