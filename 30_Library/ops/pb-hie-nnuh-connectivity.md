---
created: 2026-02-05T10:40:21+00:00
customer: nnuh
incident_type: connectivity_failure
modified: 2026-07-04T10:50:39+00:00
permalink: llmeon/30-library/ops/pb-hie-nnuh-connectivity
status: active
tags: [hie, network, nnuh, playbook]
target_service: network
title: pb-hie-nnuh-connectivity
type: playbook
---

## Playbook: HIE -> NNUH Connectivity Triage (Live Run)

### 🧭 Trigger Condition

- HIE Source Cluster `hie-prod-34` cannot reach NNUH Ingress.
- Symptom: 100% packet loss to `$TARGET_IP`.

---

### 🗺️ NNUH Network Topology (Context)

- Destination Public IP: `195.171.151.154` (nnuh-prod-1.fitfile.net)
- VNet Address Space: `192.168.200.0/24`
- Private Firewall IP: `192.168.208.4` (NNUH-HUB)
- NNUH Jumpbox: `192.168.200.132`

---

### 🧱 Execution Flow

#### Phase 1: Source Side (EKS Cluster A)

_Run inside a netshoot pod in `hie-prod-34`._

1. Set target IP:

   ```bash
   export TARGET_IP=195.171.151.154
   ```

2. Identify the Source Egress IP (The "What they see" check):
   ![[cmd-net-get-egress-ip#⚡ Action]]
   _Current known egress:_ `13.42.119.194`

3. Run the "Smoking Gun" trace to locate the drop:
   ![[cmd-net-mtr-tcp#⚡ Action]]
   _Expected:_ Dies at Hop 11 if Firewall is blocking.

4. Confirm SILENT drop vs REJECT:
   ![[cmd-net-nmap-check-filtered#⚡ Action]]

---

#### Phase 2: Destination Infrastructure (Azure Edge)

_Run from local machine or Jumpbox._

1. Verify Azure IP Ownership:
   ![[cmd-az-get-public-ip-owner#⚡ Action]]

2. Check Effective NSG Rules for the NNUH Jumpbox/Nodes:

   ```bash
   az network nic show-effective-route-table --resource-group RG-NNUH-PROD-NET --name <NIC_NAME> --output table
   ```

---

#### Phase 3: Cluster Internal (AKS Cluster B)

_Confirm the app is alive, bypassing the public firewall._

1. Map Ingress hostnames to backend services:
   ![[cmd-k8s-get-ingress-map#⚡ Action]]

2. Spoof the Host Header (The "Gold Standard" internal test):
   ![[cmd-net-curl-spoof-host#⚡ Action]]
   _Target IP:_ Use the internal Ingress Controller IP.

---

### 🔎 Analysis Matrix

| Result | Diagnosis | Action |
| --- | --- | --- |
| `MTR` dies at last hop | Ingress Filtering | Send Communication Template to NNUH Cyber Team. |
| `Spoof Header` works | Edge Problem | Firewall/WAF is blocking; Kubernetes is fine. |
| `Spoof Header` fails | Cluster Problem | Check Backend Pods and Service Endpoints. |

---

### ✉️ Ready-to-Send Evidence

> "Traffic from HIE (`13.42.119.194`) is reaching the NNUH edge but being silently dropped. Nmap reports port 443 as `filtered` (no-response). Please allowlist source IP `13.42.119.194` on the NNUH-HUB firewall."

---

### 🔗 Related

- [[pb-cross-cluster-connectivity-triage]]
- [[SoT - network-hybrid-debugging]]
