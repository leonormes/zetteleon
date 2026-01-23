---
aliases: ["CoreDNS Configuration", "DNS Architecture", "Hybrid Cloud DNS", "Split-View DNS"]
confidence: "High"
created: 2026-01-06T20:15:48+00:00
epistemic: "Architecture"
last_reviewed: 
modified: 2026-01-23T18:09:20+00:00
purpose: "To define the comprehensive DNS architecture for the FITFILE hybrid deployment, specifically detailing the Split-View DNS strategy between Azure (CUH) and AWS (SDE)."
review_interval: "1 year"
see_also: ["[[SoT - Cloud Networking Core Components]]", "[[SoT - Kubernetes Networking & DNS]]", "[[SoT - The Data Architecture of DNS]]"]
source_of_truth: []
status: "Active"
tags: ["aws", "azure", "dns", "networking", "SoftwareEngineering/Architecture"]
title: SoT - DNS Core Components and Environments
type: "SoT"
uid: 
updated: 
---

> **Architectural Pattern:** This deployment utilizes a **Split-View DNS** architecture. Domain names resolve to different IP addresses depending on the origin of the query (Internal vs. External). This is achieved via reciprocal conditional forwarding between Cloud CoreDNS and On-Premise DNS servers.

## 1. Core Components

### A. SDE Hub (AWS EKS)

- **Role:** The central hub hosting the FITFILE platform.
- **DNS Mechanism:**
    - **Internal:** CoreDNS (K8s) forwards private queries to AWS Route 53 Private Zones.
    - **Hybrid:** Configured with conditional forwarders to resolve CUH on-premise names by querying the CUH DNS Server IPs.
    - **External:** AWS Route 53 Public Zones manage `*.eoe.fitfile.net`.

### B. CUH Spoke (Azure VNet / On-Premise)

- **Role:** The hospital integration node.
- **Azure CoreDNS:**
    - Authoritative for `*.cuh.local` within Azure.
    - Forwards `*.fitfile.internal` to On-Premise DNS.
- **On-Premise DNS:**
    - The "Master" for internal resolution.
    - Authoritative for `*.fitfile.internal`.
    - Forwards `*.cuh.local` back to Azure CoreDNS (`10.2.0.10`).

## 2. Domain Strategy

| Domain | Scope | Management | Purpose |
|:--- |:--- |:--- |:--- |
| `*.eoe.fitfile.net` | **Public** | Cloudflare | External access to SDE Hub. Used for ACME DNS-01 challenges. |
| `*.fitfile.internal` | **Private** | CUH On-Premise | M2M communication. Bypasses Azure's strict hostname validation. |
| `*.cuh.local` | **Hybrid** | Split Authority | Internal resolution for CUH-specific services. |
| `*.privatelink` | **Legacy** | Azure Private DNS | **Avoid.** Causes DNS-01 validation failures in Azure. Use `.internal` instead. |

## 3. Resolution Flows (The Packet Path)

### Scenario A: CUH Spoke -> SDE Hub (Private)

1. Resource in CUH queries `relay.cuh-prod-1.fitfile.internal`.
2. Query hits **Azure CoreDNS**.
3. Forwarded to **CUH On-Premise DNS**.
4. Resolved to Private IP.

### Scenario B: SDE Hub -> Public Internet

1. Pod in EKS queries `google.com`.
2. Query hits **EKS CoreDNS**.
3. Forwarded to AWS VPC Resolver -> Internet.

### Scenario C: Cert-Manager Validation (The Trap)

- **Problem:** Azure's internal resolver prioritizes Private Zones over Public DNS. If `cert-manager` tries to validate a public domain that also has a private zone (split-horizon), it fails.
- **Fix:** Force `cert-manager` to use public resolvers (e.g., `1.1.1.1`) by setting `dns01-recursive-nameservers-only=true`.

## 4. Security Constraints

1. **Firewall:** Port 53 (UDP/TCP) must be open between SDE Hub (`13.42.119.194`) and CUH On-Premise.
2. **Proxy Bypass:** DNS traffic **cannot** go through the McAfee Web Proxy. It must be exempted via `NO_PROXY` or firewall rules.
