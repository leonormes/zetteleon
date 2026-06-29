---
created: 2026-02-17 08:49:16+00:00
incident_type: connectivity_failure
modified: 2026-03-14 11:10:10+00:00
tags:
- cross-cluster
- customer/hie
- customer/nnuh
- network
- playbook
target_service: network
title: pb-cross-cluster-connectivity-triage
type: playbook
permalink: llmeon/30-library/ops/pb-cross-cluster-connectivity-triage
---

## Playbook: Cross-Cluster Connectivity Triage

### 🧭 Trigger Condition

- Pod in Cluster A cannot reach service in Cluster B.
- Symptom: Connection Timeout (not Connection Refused).
- Error: `curl: (28) Connection timed out`.

---

### Decision Context

- Origin: Netshoot pod inside the source cluster.
- Goal: Prove where the packet dies to provide evidence for allowlisting.

---

### 🧱 Execution Flow

#### Phase 1: Establish Baseline

1. Set target IP:

   ```bash
   export TARGET_IP=<target_ip_address>
   ```

2. Spin up the diagnostic shell:
   ![[cmd-k8s-run-netshoot#⚡ Action]]

3. Identify your Source IP (what the destination sees):
   ![[cmd-net-get-egress-ip#⚡ Action]]

4. Verify outbound internet access:

   ```bash
   ping -c 4 8.8.8.8
   ```

#### Phase 2: Probe the Destination

1. Test DNS Resolution:

   ```bash
   nslookup <target_hostname>
   ```

2. Check if the port is `filtered` (Silent Drop) vs `closed` (Rejected):
   ![[cmd-net-nmap-check-filtered#⚡ Action]]

#### Phase 3: Pinpoint the Drop

1. Run a TCP-mode trace to see exactly where the packets stop responding:
   ![[cmd-net-mtr-tcp#⚡ Action]]

2. (Optional) Watch for SYN retransmissions in a second terminal:
   ![[cmd-net-tcpdump-syn-watch#⚡ Action]]

---

### 🔎 Analysis: Success vs. Failure

| Symptom | Meaning | Probable Action |
| --- | --- | --- |
| Nmap: `open` | Success | Issue is likely at L7 (Auth/Application). |
| Nmap: `closed` | Reachable, but no listener | Verify service is running on target and listening on correct IP/Port. |
| Nmap: `filtered` | Silent Drop | Ingress Firewall/ACL at destination is blocking your Source IP. |
| MTR dies at last hop | Destination edge drop | provide egress IP to destination admin. |

---

### ✉️ Communication Template (For Firewall Admins)

If diagnostics confirm a silent drop at the edge:

> "Please allowlist inbound TCP on port \<port> from source IP \<your_egress_ip>.
>
> Evidence:
> - MTR (TCP mode) confirms traffic reaches your network edge but is silently dropped at the final hop.
> - Nmap shows port \<port> as `filtered` (no-response).
> - Packet capture shows outgoing SYNs with no returning SYN/ACK or RST."

---

### 🧠 End State

Success =

- `nc -vz  <port>` returns `succeeded!`.
- Traffic flows from Cluster A to Cluster B.