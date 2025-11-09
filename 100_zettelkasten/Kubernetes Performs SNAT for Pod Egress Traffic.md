---
aliases: []
confidence: 0.9
created: 2025-10-31T11:51:00Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T10:42:03Z
purpose: "Explain Kubernetes egress traffic handling."
review_interval: 90
see_also: ["Containers Within a Pod Share Network Namespace and IP Address.md", "NAT Gateways Enable Private Resources to Access Internet.md"]
source_of_truth: []
status: seedling
tags: [kubernetes, networking]
title: Kubernetes Performs SNAT for Pod Egress Traffic
type: concept
uid: 
updated: 
---

## Kubernetes Performs SNAT for Pod Egress Traffic

**Summary:** Kubernetes translates private pod IPs to node IPs for outbound traffic using:
- kube-proxy (iptables/ipvs)
- CNI plugins
- Node network namespace

**Process:**
1. Pod generates packet with private source IP
2. kube-proxy/CNI applies SNAT rules
3. Packet continues with node IP as source

**Purpose:**
- Hide pod IPs from external networks
- Enable return traffic routing
