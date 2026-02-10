---
created: 2026-02-09T00:00:00+00:00
modified: 2026-02-10T13:37:45+00:00
owner: Customer Network Team
tags: [customer/hie, customer/nnuh, diagnostics, networking, outage]
title: MOC - Firewall Configuration for Connectivity
---

## 🚨 Diagnostic Report: Inbound Connectivity Failure

### 📋 Executive Summary

- Target: `https://nnuh-prod-1.fitfile.net`
- Public IP: `195.171.151.154` (Customer Firewall)
- Backend IP: `192.168.200.40` (Internal AKS LB)
- Source IP: `13.42.119.194` (Our Egress IP)
- Status: 🔴 External Access Failed / ✅ Internal Infrastructure Healthy
- Root Cause: Traffic is reaching the customer's network boundary (`195.171.151.154`) but is being blackholed. This indicates a missing Inbound DNAT rule or Symmetric SNAT configuration on the firewall.

---

### 1. Architecture & Verification Status

We have verified the health of all internal components to rule out Azure/AKS issues.

| Component       | Detail                    | Status     | Evidence                                     |
|:-------------- |:------------------------ |:--------- |:------------------------------------------- |
| Public Endpoint | `195.171.151.154`         | 🔴 Failing | External `curl` and `tcptraceroute` timeout. |
| Internal LB     | `192.168.200.40`          | ✅ Healthy  | `curl` from Jumpbox succeeds (HTTP 200).     |
| AKS Outbound    | NAT Gateway               | ✅ Healthy  | Pods can reach Google/Internet.              |
| DNS             | `nnuh-prod-1.fitfile.net` | ✅ Healthy  | Resolves to `195.171.151.154`.               |

---

### 2. Technical Justification: The "Routing Paradox"

> [!INFO] Why this fails without SNAT
> The connectivity failure is caused by a lack of Symmetric Routing, which is mandatory when mixing an Inbound Firewall with an Outbound NAT Gateway.

1. The Failure (DNAT Only): The Firewall sends the packet to the AKS Node preserving the Client IP (`13.42.x.x`). The AKS Node replies, but because the destination is an external IP, it routes the reply via the NAT Gateway, which drops the packet (asymmetric path).
2. The Fix (DNAT + SNAT): The Firewall must Source NAT the packet to its own Private IP. The AKS Node then replies to the Firewall's Private IP, forcing the traffic back through the correct return path (hairpinning).

---

### 3. Diagnostic Commands & Evidence

#### A. Source Side: Verify Egress (From Netshoot)

_Run these inside a debug pod in the source cluster._

```bash
# Start Netshoot Pod
kubectl run netshoot-test -i --tty --rm --image nicolaka/netshoot -- /bin/bash

# Export Target
export TARGET_IP=195.171.151.154

# 1. Basic Egress Check (Confirm we have internet)
ping -c 4 8.8.8.8

# 2. Verify Our Public IP (For Customer Allowlist)
curl -s ifconfig.me

# 3. Test TCP Connectivity (Port 443) - The "Truth Serum"
# If this fails, traffic is blocked.
nc -vz -w 5 ${TARGET_IP} 443

# 4. Detailed HTTPS Handshake
curl -v --connect-timeout 5 https://nnuh-prod-1.fitfile.net
````

#### B. The "Smoking Gun": MTR Traceroute

_Standard traceroute uses ICMP/UDP which is often blocked. We use TCP SYN packets on port 443 to prove the traffic reaches the edge._

```sh
# Run MTR using TCP SYN on port 443
mtr -n -T -P 443 -r -c 10 195.171.151.154
```

Result Analysis:

| Hop | IP Range | Status | Interpretation |
|:--- |:--- |:--- |:--- |
| 1-9 | `10.65.x.x` $\to$ `Public Internet` | ✅ 0% Loss | Traffic successfully traverses internal network and public internet. |
| 10 | `208.127.198.30` | ✅ 0% Loss | Final successful hop before Customer Gateway. |
| 11 | `???` | 🔴 100% Loss | Blackhole: Traffic reached the firewall boundary but was dropped. |

#### C. Internal Validation (From Jumpbox)

_Run from a VM inside the destination VNet to prove the backend is working._

```sh
# 1. Hit Internal Load Balancer directly
curl -v -k https://192.168.200.40

# 2. Spoof Host Header (Validates App Logic without DNS)
curl -v -k --resolve nnuh-prod-1.fitfile.net:443:192.168.200.40 https://nnuh-prod-1.fitfile.net
```

---

### 4. Action Plan

#### Request to Customer Network Team

Please configure Inbound Access for `nnuh-prod-1.fitfile.net` on Firewall `195.171.151.154`:

1. DNAT Rule: Forward TCP/443 to Internal LB `192.168.200.40`.
2. SNAT Configuration (CRITICAL): Enable Source NAT (Masquerading) on the inbound rule to ensure the return traffic goes back to the firewall interface, preventing asymmetric routing drops.
3. ACL: Allow Source IP `13.42.119.194`.

#### Log Verification Request (Template)

"Could you please share the actual traffic logs (hit counts) for the last 24 hours regarding the HIE connectivity?

We need to distinguish between the Firewall Rule (which may show as 'Allowed') and the Actual Packet Flow. specifically:

- Source: `13.42.119.194`
- Destination: `195.171.151.154` (NATs to `192.168.200.40`)
- Port: `443`

Do your logs show packets successfully traversing the firewall and completing the NAT translation, or are they being dropped by subsequent inspection rules?"

#### Manager Justification (Template)

Subject: Diagnostic Results: Inbound Connectivity Failure

Key Findings:

- Path Validation: The `mtr` (TCP/443) trace successfully completes 10 hops, reaching the final provider edge before the customer's firewall.
- The Blocker: The connection fails with 100% packet loss exactly at the destination IP (`195.171.151.154`).
- Conclusion: The traffic is being "blackholed" at the customer's edge. This confirms a missing Inbound DNAT rule or blocked Security Policy, as the internal backend is proven healthy.
