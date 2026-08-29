---
aliases: [Debugging Toolkit, Netshoot Tools, Network Tools SoT, Tcpdump Guide]
created: 2026-02-04T00:00:00+00:00
modified: 2026-08-29T09:36:50+00:00
permalink: llmeon/30-library/ops/sot-network-tools-patterns
tags: [debugging, linux, networking, sot, tools]
title: sot-network-tools-patterns
type: sot
---

## 1. The Strategy: Divide and Conquer (OSI Model)

Effective network debugging moves up the stack. Do not debug HTTP (L7) if you cannot ping the Gateway (L3).

| Layer          | Focus         | Key Tools                                    | Typical Issues                                        |
|:------------- |:------------ |:------------------------------------------- |:---------------------------------------------------- |
| L7 (App)       | HTTP/DNS/TLS  | `curl`, `dig`, `drill`, `openssl`, `grpcurl` | DNS resolution, TLS Handshake, HTTP 500/403.          |
| L4 (Transport) | TCP/UDP Ports | `nc`, `nmap`, `ss`, `iperf3`                 | Connection Refused (Port closed), Timeout (Firewall). |
| L3 (Network)   | IP Routing    | `ping`, `mtr`, `ip route`                    | Packet Loss, Routing Loops, Blackholes.               |
| L2 (Link)      | Interfaces    | `ip link`, `ethtool`                         | MTU Mismatches, Interface Down, Physical errors.      |

---

## 2. Layer 3: Reachability & Routing (The Roads)

### `ping` & `mtr` (My Traceroute)

- Goal: Verify basic connectivity and path integrity.
- Protocol: ICMP.
- Warning: ICMP is often deprioritized or blocked by cloud firewalls. A failed ping does _not_ prove the host is down.

```bash
# Basic check (fast fail)
ping -c 4 -W 1 8.8.8.8

# Path analysis (Packet loss per hop)
mtr -rw -c 10 google.com
```

### `ip route` (Routing Table)

- Goal: Where does the packet _go_ next?
- Key Check: Ensure you have a default route (`default via …`) and specific routes for internal subnets.

```bash
# Show route to specific IP (Validation)
ip route get 1.1.1.1
```

---

## 3. Layer 4: Ports & Sockets (The Doors)

### `nc` (Netcat) - The Swiss Army Knife

- Goal: Test TCP/UDP port availability without protocol overhead.
- Why use it: It distinguishes between "Host Down" (Timeout) and "Port Closed" (Refused).

```bash
# Test TCP Port 443 (Verbose, Zero-IO, Timeout 2s)
nc -vz -w 2 $TARGET_IP 443

# Test UDP Port 53
nc -vzu -w 2 $TARGET_IP 53
```

### `ss` (Socket Statistics)

- Goal: Inspect local connections. Replacement for `netstat`.

```bash
# Show all Listening TCP/UDP ports with Process names
ss -tulnp
```

### `nmap` (Network Mapper)

- Goal: Discovery and Firewall profiling.
- Key Flags: `-Pn` (Skip ping), `-p` (Port range), `--reason` (Why is it closed?).

```bash
# Scan specific ports, skipping ping check
nmap -Pn -p 80,443 --reason $TARGET_IP
```

---

## 4. Layer 7: Application & DNS (The Conversation)

### `curl` (Client URL)

- Goal: Debug HTTP/HTTPS and TLS.
- Key Pattern: The `resolve` flag allows testing ingress/virtual hosts without DNS changes.

```bash
# Test connection timing
curl -w "@curl-format.txt" -o /dev/null -s https://example.com

# Bypass DNS (Force Host to IP)
curl -v --resolve example.com:443:10.0.0.1 https://example.com
```

### `dig` (Domain Information Groper)

- Goal: DNS troubleshooting.
- Key Check: Compare internal (K8s CoreDNS) vs External (8.8.8.8).

```bash
# Short answer (IP only)
dig +short google.com

# Trace the recursion
dig +trace google.com
```

---

## 5. Packet Capture (The Truth Serum)

### `tcpdump`

- Goal: See what is actually on the wire.
- Philosophy: "Packets don't lie."

```bash
# Capture standard web traffic (ASCII output)
tcpdump -n -i any -A port 80

# The "Handshake Check" (SYN sent, no SYN-ACK received?)
tcpdump -n -i any "tcp[tcpflags] & (tcp-syn|tcp-ack) != 0" and host $TARGET_IP
```

---

## 6. Linux Host Deep-Dive (When Tools Lie)

Sometimes the issue isn't the network, but the Linux Kernel on the Node.

- IP Forwarding: Ensure the node can route between interfaces (required for CNI).
    - `sysctl net.ipv4.ip_forward`
- IPTables Chains: Check if `KUBE-SERVICES` or `DOCKER` chains are dropping packets.
    - `iptables -L -n -v | grep DROP`
- Bridge FDB: Check the Forwarding Database for MAC learning issues on overlay networks.
    - `bridge fdb show`

---

## 7. Cloud & Kubernetes Specifics

- Netshoot: The container image that contains all the above.
    - `kubectl run netshoot -it --rm --image nicolaka/netshoot -- /bin/bash`
- AWS Reachability Analyzer: Static analysis of AWS Network configuration (Security Groups, ACLs, Routes). Use this _before_ tcpdump if you have console access.
- Azure Network Watcher: Equivalent for Azure. "IP Flow Verify" checks NSGs.

## Related Protocols

- [[Protocol - HIE--NNUH Network Debugging]]—_The step-by-step diagnostic workflow._
