---
created: 2026-02-05T17:15:00Z
modified: 2026-02-05T17:21:47+00:00
status: permanent
tags:
  - aks
  - azure
  - log
  - networking
  - troubleshooting
  - customer/nnuh
title: 2026-02-05 - Azure AKS Inbound DNAT and IP Sizing
type: head
---

## Context

Troubleshooting connectivity issues between a customer's private AKS cluster and our Azure AKS deployment, followed by an IP capacity planning exercise for a new deployment.

## 1. Inbound Connectivity (The "Routing Paradox")

### Problem

- Source: Customer Pod (`192.168.59.91`) -> Target Public IP (`195.171.151.154`).
- Symptom: `SYN` packets sent, no `SYN-ACK` received. Connection timeout.
- Architecture: The Public IP `195.171.151.154` belongs to the _Customer's_ firewall, configured to DNAT traffic to our internal Load Balancer (`192.168.200.40`).

### Root Cause: Asymmetric Routing

1. Inbound: Firewall DNATs packet: `Src: 192.168.59.91` -> `Dst: 192.168.200.40`.
2. Processing: Our server receives it.
3. Reply: Our server replies to `192.168.59.91`.
4. Routing Failure: Since `192.168.59.91` is a private IP but not in our VNet, our router sends it to the default gateway (NAT Gateway) or drops it. It does _not_ send it back to the inbound Firewall because it doesn't know the Firewall was the previous hop.
5. Result: The Firewall never sees the reply, so the stateful session breaks.

### Solution: SNAT (Source NAT)

- The Fix: Configure the Customer Firewall to SNAT the traffic in addition to DNAT.
- Flow: `Src: Firewall_Private_IP` -> `Dst: 192.168.200.40`.
- Return: Our server replies to `Firewall_Private_IP`, forcing traffic back through the symmetric path.
- Note: Azure Firewall does this automatically for DNAT rules.

## 2. IP Capacity Planning (Calico Overlay)

### Requirement

Determine the minimum CIDR size for a new private AKS deployment in a customer tenant.

### Investigation

- Architecture: AKS with Azure CNI Overlay (Calico).
- Key Insight: Pods use an overlay network (`10.244.0.0/16`) and DO NOT consume VNet IP addresses. Only Nodes and Internal Load Balancers consume VNet IPs.

### Audit Results

- Nodes: 3
- Internal LBs: 1 (`ingress-nginx`)
- Azure Reserved: 5
- Private Endpoint: 1
- Total Required: 11 IPs

### Recommendation

- Selected Size: `/27` (32 IPs).
- Justification: A `/28` (16 IPs) leaves only ~5 spare IPs, which is too risky for upgrades (surge nodes) or HA scaling. A `/27` provides ample headroom without wasting customer address space.

## 3. Artifacts

### IP Audit Script

```bash
#!/bin/bash
# AKS IP Usage & CIDR Sizing Calculator (Calico/Overlay Mode)

BOLD='\033[1m'; NC='\033[0m'
CLUSTER_JSON=$(az aks list --query "[0]" -o json)
CLUSTER_NAME=$(echo $CLUSTER_JSON | jq -r '.name')
RESOURCE_GROUP=$(echo $CLUSTER_JSON | jq -r '.resourceGroup')

# Counts
NODE_COUNT=$(kubectl get nodes --no-headers | wc -l)
ILB_COUNT=$(kubectl get svc --all-namespaces -o json | jq '[.items[] | select(.spec.type=="LoadBalancer") | select(.metadata.annotations."service.beta.kubernetes.io/azure-load-balancer-internal"=="true")] | length')
AZURE_RESERVED=5; PRIVATE_ENDPOINT_IP=1; MAX_SURGE=1

TOTAL_REQUIRED=$((NODE_COUNT + ILB_COUNT + PRIVATE_ENDPOINT_IP + MAX_SURGE + AZURE_RESERVED))

echo -e "${BOLD}Minimum IPs Required:${NC} $TOTAL_REQUIRED"
if [ "$TOTAL_REQUIRED" -le 27 ]; then echo "/27 is SUFFICIENT"; else echo "/27 is TOO SMALL"; fi
```

## Related Knowledge

- [[30_Library/SoT/Cheatsheet - Azure AKS Networking]]
- [[30_Library/SoT/SoT - Azure Hybrid Networking (ExpressRoute)]]
- [[30_Library/200_projects/10_Infrastructure/Networking/Calico Cloud vs Kubernetes Network Policies in GitOps]]
