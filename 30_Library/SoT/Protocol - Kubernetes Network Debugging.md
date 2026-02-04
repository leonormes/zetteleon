---
created: 2026-02-01T15:35:00+00:00
modified: 2026-02-04T07:27:25+00:00
status: "evergreen"
tags: ["kubernetes", "networking", "protocol", "troubleshooting", 100]
title: Protocol - Kubernetes Network Debugging
type: "protocol"
---

## 1. Logic Map

- Objective: Diagnose and prove packet loss between a Kubernetes Cluster (Source) and an external Endpoint (Destination).
- Dependencies: `kubectl` access, `netshoot` container image, AWS CLI (optional but recommended).
- Success Criteria: Definitive proof of where the packet is dropping (Source Egress vs. Destination Ingress).

## 2. The Algorithm (Netshoot)

### Step 1: Deploy Ephemeral Diagnostic Pod

Spin up a `netshoot` pod in the source namespace. This bypasses distroless limitations of application containers.

```bash
kubectl run netshoot --rm -i --tty --image nicolaka/netshoot -- /bin/bash
```

### Step 2: Validate Basic Reachability (ICMP/DNS)

Inside the pod, verify name resolution and basic routing.

```bash
# Check DNS
nslookup <destination-domain>

# Check Routing (ICMP)
ping -c 3 <destination-ip>
```

### Step 3: Trace the Path (MTU & Hops)

Use `tracepath` (no sudo required) to identify routing hops and MTU issues.

```bash
tracepath -n <destination-ip>
```

### Step 4: The "Smoking Gun" Test (TCP Dump)

If the connection times out, use `tcpdump` to prove if packets are leaving the source.

Terminal 1 (Inside Netshoot): Start Listener

```bash
# Capture packets for the specific host
tcpdump -i any host <destination-ip> -n
```

Terminal 2 (Inside Netshoot): Trigger Traffic

```bash
# Attempt connection (e.g., HTTPS)
curl -v https://<destination-ip>
```

Interpretation:

- [S] (SYN) sent, nothing received: The packet left the source but was "black-holed" by the destination or an intermediate firewall.
- [R] (RST) received: The destination (or a firewall) actively rejected the connection.
- No Output: The packet is being dropped internally (CNI, NetworkPolicy, or local Egress rule).

## 3. The Algorithm (AWS Infrastructure)

If `tcpdump` shows no output, checking the cloud infrastructure is required.

1. Routing: Ensure Route Table has `0.0.0.0/0` -> `nat-gateway` (Private Subnet) or `igw` (Public Subnet).
2. Security Groups (Stateful): Ensure Outbound Rule allows `0.0.0.0/0` (or specific IP).
3. NACLs (Stateless): Ensure Outbound Rule 100 allows `0.0.0.0/0`.
4. NAT Gateway IP: Find the public source IP to provide to the destination admin.

```bash
# Get NAT Gateway Public IP
aws ec2 describe-nat-gateways --nat-gateway-ids <nat-id> --query "NatGateways[0].NatGatewayAddresses[0].PublicIp" --output text
```
