---
aliases: []
confidence: "null"
created: 2025-10-26T17:19:00Z
epistemic: "null"
last_reviewed: "null"
modified: 2026-01-03T10:19:26+00:00
purpose: "null"
review_interval: "null"
see_also: []
source_of_truth: []
status: "null"
tags: ["labels", "network-policy", "security", "topic/technology/containers", "topic/technology/kubernetes", "traffic-control"]
title: Network policies control traffic flow between pods using labels and namespaces
type: "Fact"
uid: 
updated: 
version: "1"
---

## Summary

Kubernetes Network Policies provide fine-grained traffic control between pods by defining rules based on pod labels, namespaces, and ports, enhancing cluster security through isolation and access control.

## Details

### Policy Mechanism

- **Rule-Based Control**: Define which pods can communicate with each other
- **Label-Based Selection**: Use pod labels and namespaces to target specific workloads
- **Port-Level Control**: Restrict communication to specific ports
- **Default Deny**: When policies exist, traffic is denied by default unless explicitly allowed

### Common Use Cases

**Workload Isolation:**

- Isolate sensitive workloads from rest of cluster
- Create security zones within the cluster
- Implement defense-in-depth strategy

**Access Control:**

- Allow only specific pods to access databases
- Restrict frontend to backend communication
- Block traffic from certain namespaces

**Compliance Requirements:**

- Meet regulatory security requirements
- Implement network segmentation
- Audit traffic patterns

### Policy Components

- **Pod Selector**: Target pods for the policy
- **Ingress Rules**: Control incoming traffic
- **Egress Rules**: Control outgoing traffic
- **Peer Selection**: Define source/destination pods using labels

## Implementation

- **CNI Plugin Required**: Network policies require a CNI plugin that supports them (Calico, Cilium, etc.)
- **iptables/eBPF**: Policies are implemented using kernel networking features
- **Performance Impact**: Minimal overhead when properly implemented

## Related

- [[MOC - Container Runtime & Orchestration]] - How policies are implemented by CNI plugins
- [[Kube-Proxy Implements Services Using Iptables or IPVS]] - Related iptables usage
- What are iptables chains and tables? - Underlying mechanism for policy enforcement
