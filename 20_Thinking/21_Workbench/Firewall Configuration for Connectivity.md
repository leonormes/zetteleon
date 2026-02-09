---
captured: 2026-02-09T10:42:12+00:00 2026-02-09T10:42:12+00:00
created: 2026-02-09T10:42:15+00:00
modified: 2026-02-09T10:47:46+00:00
source: https://gemini.google.com/share/5052758c23a0
status: processing
tags: [customer/hie, customer/nnuh, input]
title: Firewall Configuration for Connectivity
type: head
---

## Executive Summary

Status: 🔴 External Access Failed / ✅ Internal Infrastructure Healthy Root Cause: Missing Inbound DNAT and SNAT configuration on the Customer Edge Firewall (`195.171.151.154`).Owner: Customer Network Team.

The Azure AKS cluster and Internal Load Balancer are correctly configured and healthy. The failure occurs at the network boundary where the public IP (`195.171.151.154`) fails to properly translate and forward traffic to the internal backend (`192.168.200.40`).

---

## 1. Architecture & Verification

We have verified the health of the internal components to rule out Azure AKS issues.

| Component       | Detail                    | Status     | Evidence                                 |
| --------------- | ------------------------- | ---------- | ---------------------------------------- |
| Public Endpoint | `195.171.151.154`         | 🔴 Failing | External `curl` times out.               |
| Internal LB     | `192.168.200.40`          | ✅ Healthy  | `curl` from Jumpbox succeeds (HTTP 200). |
| AKS Outbound    | NAT Gateway               | ✅ Healthy  | Pods can reach Google/Internet.          |
| DNS             | `nnuh-prod-1.fitfile.net` | ✅ Healthy  | Resolves to `195.171.151.154`.           |

Conclusion: Since the internal Load Balancer responds correctly to internal traffic from the Jumpbox, the application and AKS networking are functional. The blockage is upstream at the customer firewall.

---

## 2. Technical Justification: The "Routing Paradox"

The connectivity failure is caused by a lack of Symmetric Routing, which is required when mixing an Inbound Firewall with an Outbound NAT Gateway.

### The Failure Scenario (Current State)

If the firewall performs DNAT only (Destination NAT), the traffic flow breaks due to asymmetric routing:

1. Inbound: Client (`13.42.x.x`) Firewall AKS Node.
	- _The AKS Node sees the Source IP as `13.42.x.x`._
2. Reply: AKS Node replies to `13.42.x.x`.
3. Routing Decision: The AKS subnet uses the NAT Gateway for all traffic destined to the Internet (`0.0.0.0/0`).
4. Drop: The reply packet is sent to the NAT Gateway, not the Firewall. The NAT Gateway drops the packet because it doesn't recognize the session (asymmetric path).

### The Solution (SNAT / "Hairpinning")

To fix this, the Firewall must perform SNAT (Source NAT) in addition to DNAT.

1. Inbound: Client Firewall (SNATs to `Private_FW_IP`) AKS Node.
	- _The AKS Node sees the Source IP as `Private_FW_IP` (e.g., 192.168.208.4)._
2. Reply: AKS Node replies to `Private_FW_IP`.
3. Routing Decision: The destination is a Local VNet IP. Azure routes the traffic back to the Firewall.
4. Success: The Firewall translates the packet back to the Client IP and returns it.

---

## 3. Required Actions

Please pass the following configuration request to the Customer Network Team:
Request: Configure Inbound Access for `nnuh-prod-1.fitfile.net`.
1. Firewall Configuration (Public IP: `195.171.151.154`)
- Action: Create a DNAT Rule forwarding TCP/443 to the Internal Load Balancer `192.168.200.40`.
- Critical Constraint: You MUST enable Source NAT (SNAT) on this rule.
	- _If using Azure Firewall:_ This happens automatically (no manual SNAT config needed).
	- _If using 3rd Party NVA (Palo Alto, Fortinet, etc.):_ You must explicitly configure "Source NAT" or "Masquerading" to the firewall's internal interface IP to ensure return traffic symmetry.

1. Access Control List (ACL)
- Source: Allow `13.42.119.19` (HIE Client).
- Destination:`192.168.200.40` (Internal LB).
- Port: TCP 443.

1. Verification Command (to be run from HIE/External):

I want to ask the customer about the fw logs. I have written this. "Did you seem fw logs that say the traffic from hie was allowed through the fw? "

Make it clearer for me and include the relevant details

Here is a more professional and specific version of your question. It includes the exact IPs to make it easy for them to search their logs.

"Could you please check your firewall logs to confirm if traffic from 13.42.119.19 (HIE) destined for 195.171.151.154 (Public IP) is being allowed? Specifically, do you see the packets being forwarded to our internal load balancer at 192.168.200.40?"

I am trying to distinguish between the fw rule that says the traffic is allowed and the logs that show the packets are _actually_ being allowed. There is a difference between 1 rule saying allowed and the traffic actually getting through. If we are only looking at the fw in one rule which says allowed but there are other rules blocking the traffic

To help you get the clarity you need, you should ask the customer's network team for specific traffic logs (hit counts) rather than just a confirmation of the rule's existence. In complex firewall environments, a "permit" rule can be shadowed by a "deny" rule with higher priority, or a packet might be dropped by an inspection engine (like IPS) even if the rule matches.

Here is a refined version of your question that distinguishes between the policy and the actual packet flow:

---

## Suggested Message to the Customer

"Could you please share the actual traffic logs (hit counts) for the last 24 hours regarding the HIE connectivity?

We want to distinguish between the Firewall Rule (which may show as 'Allowed' in the policy) and the Actual Packet Flow. Specifically, can you confirm if your logs show packets successfully traversing the firewall for this flow?

- Source IP:`13.42.119.19` (HIE)
- Destination Public IP:`195.171.151.154`
- Translated Backend IP:`192.168.200.40`
- Port:`443` (HTTPS)

We are looking for confirmation that the firewall is not only matching the permit rule but is also successfully completing the NAT translation and forwarding the packets to our internal load balancer without being dropped by other subsequent rules or security profiles."

---

## Why This Distinction Matters

A firewall policy is just a list of instructions; the logs are the evidence of what actually happened to the data. By asking for this, you are checking for three common "invisible" blockers:

- Rule Shadowing: A "Deny All" rule or a more specific restriction might be sitting above your "Allow" rule in the priority list.
- Asymmetric Return Path: The packet might get _in_, but if the firewall doesn't see the return traffic (because of the SNAT issue we discussed), it will eventually time out the session and show a "TCP Reset" or "Teardown" in the logs.
- Security Inspection: Even if the rule is "Allowed," features like Deep Packet Inspection (DPI) or an Intrusion Prevention System (IPS) might be dropping the packets silently if it thinks the handshake looks suspicious.

Would you like me to draft a list of specific "log status codes" (like _TCP:Sync-Received_ or _TCP:Reset_) they should look for to prove the connection is working?

I have done this

## Logic Map

- Objective: Systematically diagnose connectivity issues between clusters (e.g., EKS $to$ AKS) or from public internet to ingress.
- Strategy: Divide and Conquer. Test from the _Source_ (Egress), then the _Destination Infrastructure_ (Cloud Network), then the _Destination Cluster_ (Kubernetes/Ingress).
- Prerequisites:
- `kubectl` access to both clusters.
- A `netshoot` pod running in the source cluster.
- SSH access to a Jumpbox in the destination network (optional but recommended).
- Reference: [[SoT - Network Debugging Tools & Patterns]]

---

## 1. Source Side: Verify Egress (From Netshoot)

_Run these inside a debug pod in the source cluster._

`kubectl run netshoot-test -i --tty --rm --image nicolaka/netshoot -- /bin/bash`

### A. Basic Connectivity

```bash
kubectl run netshoot-test -i --tty --rm --image nicolaka/netshoot -- /bin/bash
export TARGET_IP=195.171.151.154
# 1. Is ping actually sending? (Short timeout to detect hang vs packet loss)
ping -c 4 -W 1 ${TARGET_IP}
# 2. Do we have internet access? (Check NAT/Egress)
ping -c 4 8.8.8.8
# 3. What is my public egress IP? (For allowlisting)
curl -s ifconfig.me
```

### B. Protocol Specifics (TCP Vs ICMP)

_ICMP is often blocked. TCP is the source of truth._

```bash
# 4. Test TCP Connectivity (Port 443/80)
nc -vz -w 5 ${TARGET_IP} 443
# 5. Test HTTPS Handshake (Detailed verbose output)
curl -v --connect-timeout 5 https://${TARGET_IP}
# 6. Deep Dive: Why is it failing? (Filtered vs Closed)
# -Pn skips ping discovery. --reason shows why port is marked state.
nmap -Pn -p 80,443 --reason ${TARGET_IP}
```

### C. Packet Inspection (The "Truth Serum")

_Run this while executing the curl/nc command in another terminal._

```bash
# 7. Check if packets are actually leaving the pod
tcpdump -n -i any host ${TARGET_IP}
# Look for: Flags [S] (SYN sent).
# No Reply = Dropped downstream.
# Reply [R.] = Rejected (Closed port).
```

---

## 2. Destination Infrastructure: Azure/Cloud (From Jumpbox)

_Run these from a VM inside the destination VNet._

### A. Identify the Target

```bash
# 1. Who owns this Public IP? (Is it even ours?)
az network public-ip list --query "[?ipAddress=='${TARGET_IP}']"
# 2. List Load Balancers
az network lb list --output table
```

### B. Cloud Firewall/NSG Checks

```bash

# 3. Check Effective NSG Rules (Requires VM name)
az network nsg rule list --nsg-name ${AZ_NSG_NAME} --resource-group ${AZ_RESOURCE_GROUP} --output table
# 4. Check Azure Firewall Rules (If applicable)
az network firewall network-rule list --firewall-name ${AZ_FIREWALL_NAME} --resource-group ${AZ_RESOURCE_GROUP} --collection-name ${AZ_FW_RULE_COLLECTION}
```

---

## 3. Destination Cluster: Kubernetes Ingress (From Jumpbox/Local)

### A. Bypass Public Path (Test Internal Ingress)

_Confirm the app is healthy inside the VNet, ignoring public firewalls._

```bash
# 1. Hit the Internal Ingress Controller IP directly
# (Get IP from: kubectl get svc -n ${K8S_INGRESS_NAMESPACE})
nc -vz ${K8S_INTERNAL_INGRESS_IP} 443
# 2. Test TLS Handshake (Ignore cert errors)
curl -v -k https://${K8S_INTERNAL_INGRESS_IP}
# 3. Spoof the Host Header (The "Gold Standard" Test)
# Simulates real traffic without DNS/Public IP issues.
curl -v -k --resolve ${TARGET_HOSTNAME}:443:${K8S_INTERNAL_INGRESS_IP} https://${TARGET_HOSTNAME}
```

### B. Kubernetes Configuration (kubectl)

```bash
# 4. List all LoadBalancer services (Is it Public or Internal?)
kubectl get svc -A -o wide | grep -i loadbalancer
# 5. Check Service Annotations (Look for "service.beta.kubernetes.io/azure-load-balancer-internal")
kubectl get svc -n ${K8S_NAMESPACE} ${K8S_SERVICE_NAME} -o yaml
# 6. Map Ingress Rules to Backends (Machine Readable)
kubectl get ingress -A -o jsonpath='{range.items[*]}{.metadata.namespace}/{.metadata.name}{":n"}{range.spec.rules[*]}{" "}{.host}{"n"}{range.http.paths[*]}{" "}{.path}{" -> "}{.backend.service.name}{":"}{.backend.service.port.number}{"n"}{end}{end}{"n"}{end}'
# 7. Check Backend Pods (Are they actually running?)
kubectl get endpoints -n ${K8S_NAMESPACE} ${K8S_SERVICE_NAME}
```

---

## 4. Decision Matrix (Interpretation)

| Test Result                             | Diagnosis             | Next Action                              |
|:-------------------------------------- |:-------------------- |:--------------------------------------- |
| `ping` fails, `nc` works                | ICMP Blocked (Normal) | Ignore ping. Focus on TCP.               |
| `nc` fails (Timeout)                    | Traffic Blackholed    | Check NSGs, Firewalls, and Route Tables. |
| `nc` fails (Connection Refused)         | Port Closed           | Check Pod Health, Service Port mapping.  |
| `curl --resolve` works, Public IP fails | Public Edge Issue     | Check WAF, Public LB, or NAT rules.      |
| `kubectl get endpoints` is empty        | Service has no Pods   | Check Pod Labels and Deployment status.  |

Can you give me the traceroute command from netshoot pod to give the results to my manager

To provide your manager with a clear picture of where the connection is dropping, you should run a Traceroute that specifically targets the service port (TCP 443). Standard traceroute uses UDP or ICMP, which are almost always blocked by Azure Firewalls, leading to a misleading row of asterisks (`* * *`).

Use the following commands inside your netshoot pod:

### 1. The TCP Traceroute (The Manager's "Proof")

This is the most important command because it mimics the actual application traffic.

### 2. The "MTR" Report (High-Level Summary)

If you want to provide a professional report that shows packet loss and latency at every hop over time, use `mtr`. Managers generally prefer this as it is easier to read.

---

### How to Interpret and Report the Results

When you send these results to your manager, include a brief interpretation to justify why the issue is at the firewall:

- If the trace stops at a Private IP (e.g., 10.x.x.x or 192.168.x.x): > "The traffic is being dropped internally within the customer's network before it even reaches the public gateway."
- If the trace reaches the Public IP but shows no response on the final hop: > "Packets are reaching the firewall boundary at `195.171.151.154`, but the firewall is not responding or forwarding the traffic to our backend. This confirms a missing Inbound DNAT/Allow rule."
- If you see `!X` or `!A` at a specific hop: > "The traceroute explicitly returned a 'Communication Administratively Prohibited' flag, confirming an active block by a Firewall/ACL."

### A Quick Note on "Dead" Hops

If you see rows of `* * *`, it does not always mean the network is down; it often means that specific intermediate routers are configured to ignore traceroute requests for security. However, if the very last hop is `* * *` and the application is failing, it is a definitive sign that the packet reached the destination gateway but was dropped there.

traceroute -n -T -p 443 195.171.151.154

traceroute: unrecognized option: T

BusyBox v1.37.0 (2025-12-16 14:19:28 UTC) multi-call binary.

Usage: traceroute [-46IFlnrv] [-f 1ST_TTL] [-m MAXTTL] [-q PROBES] [-p PORT]

[-t TOS] [-w WAIT_SEC] [-s SRC_IP] [-i IFACE]

[-z PAUSE_MSEC] HOST [BYTES]

Trace the route to HOST

-4,-6 Force IP or IPv6 name resolution

-F Set don't fragment bit

-I Use ICMP ECHO instead of UDP datagrams

-l Display TTL value of the returned packet

-n Print numeric addresses

-r Bypass routing tables, send directly to HOST

-v Verbose

-f N First number of hops (default 1)

-m N Max number of hops

-q N Number of probes per hop (default 3)

-p N Base UDP port number used in probes

(default 33434)

-s IP Source address

-i IFACE Source interface

-t N Type-of-service in probe packets (default 0)

-w SEC Wait for a response (default 3)

-z MSEC Wait before each send

It looks like you are running the BusyBox version of `traceroute` (common in lightweight Docker images like Alpine), which is more limited than the standard GNU/Linux version. It does not support the `-T` (TCP) flag directly.

Since we need to prove TCP 443 connectivity to your manager, we have to use a different tool available in `netshoot` or a different approach with the tools you have.

---

## 1. The Better Alternative: Tcptraceroute

Since you are in a `netshoot` pod, you have access to `tcptraceroute`. This tool is designed specifically for what you are trying to do—bypass firewalls that block UDP/ICMP by using TCP SYN packets.

Run this command:

## 2. If You Must Use BusyBox Traceroute

If you are restricted to the BusyBox binary you showed, your only option is to use ICMP (Ping-style) packets. Note that if the customer firewall blocks ICMP, this will just show asterisks after the first few hops.

Run this command:

- -n: Disables DNS lookups for speed.
- -I: Uses ICMP ECHO instead of the default UDP.

---

## 3. How to Present the "Proof" to Your Manager

When you get the output, the most important part is the last successful hop.

### Use This Template for Your Report

Network Diagnostic: Inbound Connectivity to 195.171.151.154

- Test Tool:`tcptraceroute` (TCP SYN on port 443)
- Result: [Paste your output here]
- Manager Summary: > * The trace successfully leaves our cluster and traverses the internet.
- It stops/times out exactly at the Public IP (195.171.151.154).
- Conclusion: This confirms the traffic is reaching the customer's network boundary but is being dropped by their Firewall. No SYN-ACK is returned, indicating the Inbound DNAT rule is likely missing or incorrectly configured.

---

Would you like me to help you interpret the specific IP addresses that appear in your trace once you run it?

```sh
mtr -n -T -P 443 -r -c 10 195.171.151.154
Start: 2026-02-09T09:52:06+0000
HOST: netshoot-tt-2 Loss% Snt Last Avg Best Wrst StDev
1.|-- 10.65.7.187 0.0% 10 0.1 0.2 0.1 0.3 0.1
2.|-- 10.65.12.115 0.0% 10 1.3 1.3 1.2 1.5 0.1
3.|-- 240.2.96.36 0.0% 10 4.8 3.8 3.5 4.8 0.4
240.2.96.10
240.2.96.38
240.2.96.9
240.2.96.42
240.2.96.43
240.2.96.47
240.2.96.8
4.|-- 242.5.253.5 0.0% 10 3.7 4.4 3.0 9.3 2.0
242.5.253.3
242.5.252.135
242.5.252.7
242.5.252.5
242.5.253.131
242.5.253.133
5.|-- 109.159.253.121 0.0% 10 3.9 3.8 3.5 4.7 0.3
109.159.253.131
6.|-- 109.159.253.130 0.0% 10 3.0 3.1 2.8 3.3 0.1
109.159.253.120
7.|-- 62.6.200.8 0.0% 10 4.3 4.4 4.1 4.5 0.1
194.74.16.244
8.|-- 213.121.193.119 0.0% 10 4.0 4.0 3.8 4.2 0.1
213.121.193.121
9.|-- 62.7.52.109 0.0% 10 9.1 9.2 9.0 9.4 0.1
10.|--??? 100.0 10 0.0 0.0 0.0 0.0 0.0
```

This `mtr` report is the "smoking gun" you need for your manager. It clearly shows that your traffic successfully traverses the internal network and the public internet, only to be killed at the very last step.

### Analysis of the MTR Report

- Hops 1–2: These are your internal cluster and Azure virtual network gateways. Latency is sub-2ms, showing a healthy internal start.
- Hops 3–9: These represent the transit through major internet service providers (BT/Openreach IPs like `109.159.x.x` and `62.6.x.x`). The traffic is moving normally across the UK backbone.
- Hop 10 (`???` with 100% Loss): This is the destination gateway at `195.171.151.154`. The fact that hop 9 responds but hop 10 is a total blackout (100% packet loss) proves that the packets are reaching the customer's front door but are being dropped by a firewall policy.

---

### Justification Report for Your Manager

You can send this summary to your manager to justify the outcome:

Subject: Diagnostic Results: Inbound Connectivity Failure to `195.171.151.154`

Key Findings:

- Path Validation: The `mtr` (TCP/443) trace successfully completes 9 hops, reaching the final provider edge before the customer's firewall. This confirms our egress and the public internet path are fully functional.
- The Blocker: The connection fails with 100% packet loss at the final destination (`195.171.151.154`). Because we are using TCP SYN packets (the actual protocol for HTTPS), this result is definitive.
- Technical Conclusion: The traffic is being "blackholed" at the customer's edge. This typically indicates that while a DNS record exists, there is no corresponding Inbound DNAT rule or Security Policy on the firewall to allow and translate the traffic to our internal backend (`192.168.200.40`).
