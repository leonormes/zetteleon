---
aliases: []
confidence: 
created: 2025-10-22T13:53:03Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/technology/networking]
title: explain this cli output_ip addr show
type:
uid: 
updated: 
version:
---

## Explain This Cli Output

```sh
ip addr show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
inet 127.0.0.1/8 scope host lo
valid_lft forever preferred_lft forever
inet6 ::1/128 scope host noprefixroute
valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
link/ether 52:55:55:0a:13:c6 brd ff:ff:ff:ff:ff:ff
altname enx5255550a13c6
inet 192.168.5.15/24 metric 200 brd 192.168.5.255 scope global dynamic eth0
valid_lft 3388sec preferred_lft 3388sec
inet6 fe80::5055:55ff:fe0a:13c6/64 scope link proto kernel_ll
valid_lft forever preferred_lft forever
```

The command `ip addr show` displays detailed information about all network interfaces on a Linux system, including both IPv4 and IPv6 addresses, link-layer (MAC) data, and interface states. Let’s break down your specific output line by line to explain each element.[^1][^4][^6][^7][^9]

---

### First Interface – Loopback

```sh
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
```

- `1:` — Interface index.
- `lo:` — Interface name (loopback).
- `<LOOPBACK,UP,LOWER_UP>` — Flags:
  - `LOOPBACK`: special local interface.
  - `UP`: device is enabled.
  - `LOWER_UP`: link layer is active.
- `mtu 65536` — Maximum Transmission Unit (max packet size).
- `qdisc noqueue` — No queuing discipline (since traffic doesn’t go on the wire).
- `state UNKNOWN` — There’s no physical carrier to test link state.
- `group default` / `qlen 1000` — Organizational grouping and default transmit queue length.

```sh
link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
```

- `link/loopback` — Type of link-layer interface.
- MAC address is all zeros because it’s a virtual internal interface.

```sh
inet 127.0.0.1/8 scope host lo
inet6 ::1/128 scope host noprefixroute
```

- IPv4 address `127.0.0.1/8` — Used internally for local host communication.
- IPv6 address `::1/128` — IPv6 equivalent of localhost.
- `scope host` meaning it’s only reachable from within the machine.

```sh
valid_lft forever preferred_lft forever
```

- Lease times (`lft` = lifetime). “forever” means these addresses never expire.

---

### Second Interface – Ethernet

```sh
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
```

- `eth0` — Primary ethernet NIC.
- Flags explained:
  - `BROADCAST`: can send broadcast traffic.
  - `MULTICAST`: supports multicasting.
  - `UP`: interface enabled.
  - `LOWER_UP`: physical link detected.
- `mtu 1500` — Common ethernet packet size.
- `qdisc fq_codel` — Queue discipline focusing on low latency (Fair Queue Controlled Delay).
- `state UP` — Interface active.

```sh
link/ether 52:55:55:0a:13:c6 brd ff:ff:ff:ff:ff:ff
```

- `link/ether` — Ethernet link layer.
- MAC address: `52:55:55:0a:13:c6`.
- `brd` (broadcast) address: standard ethernet broadcast FF:FF:FF:FF:FF:FF.

```sh
altname enx5255550a13c6
```

- Alternate system-generated name (predictable interface naming convention).

```sh
inet 192.168.5.15/24 metric 200 brd 192.168.5.255 scope global dynamic eth0
```

- IPv4 address: `192.168.5.15` assigned dynamically (via DHCP).
- `/24` → subnet mask 255.255.255.0.
- `scope global` → accessible on the LAN.
- `metric 200` → preference ranking for routing.
- `brd` → subnet broadcast address.

```sh
valid_lft 3388sec preferred_lft 3388sec
```

- DHCP lease lifetimes — address valid and preferred for ~56 minutes.

```sh
inet6 fe80::5055:55ff:fe0a:13c6/64 scope link proto kernel_ll
```

- IPv6 link-local address auto-generated based on the interface’s MAC.
- `scope link` → only valid within local network segment.
- `proto kernel_ll` → provided by the kernel at link-layer discovery.

---

### Summary

This `ip addr show` output reveals:

- One loopback interface used internally (`lo`).
- One active network adapter (`eth0`) with:
  - Local IPv4 address `192.168.5.15`.
  - Link-local IPv6 address `fe80::5055:55ff:fe0a:13c6`.
  - Up and connected physical link.
- DHCP manages the IPv4 lease dynamically.

The command replaces the older `ifconfig` and provides richer details for network diagnostics and configuration.
