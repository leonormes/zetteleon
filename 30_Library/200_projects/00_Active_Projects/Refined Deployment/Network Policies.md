---
aliases: []
created: 2025-07-10T13:05:05Z
last_reviewed: "null"
modified: 2026-02-01T15:08:20+00:00
tags: ["SoftwareEngineering/Kubernetes", "SoftwareEngineering/Networking"]
title: Network Policies
type: "head"
updated: 
---

- Purpose: Network Policies act as pod-level firewalls, allowing you to specify how groups of pods are permitted to communicate with each other. By default, Kubernetes allows any traffic to or from any pod in the cluster, which is generally undesirable for security in production environments. Network Policies enable you to restrict connections based on labels applied to pods, rather than relying on ephemeral IP addresses.
- Precision/Accuracy: They provide granular control over ingress (traffic entering a pod) and egress (traffic leaving a pod) traffic. For instance, you can create a default Egress policy to suppress all outbound traffic from pods in a specific namespace. They are implemented by the Container Network Interface (CNI) plugin you choose, and not all CNI plugins support Network Policies.
- Example: Cilium, a popular CNI plugin, uses eBPF programs to enforce Network Policies at layers 3/4 and even layer 7 (for protocols like HTTP and gRPC), dropping packets that do not match the defined rules.
- Strategic Recommendation: Implement Network Policies from the outset to establish strong security boundaries between application components and prevent unauthorized lateral movement within the cluster. This is crucial for compliance and reducing the attack surface.

[[Kubernetes-Native Abstractions for Traffic Control]]
