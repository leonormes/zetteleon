---
aliases: []
created: 2026-09-13T00:00:00+00:00
modified: 2026-09-13T16:30:20+00:00
permalink: llmeon/30-library/100-zettelkasten/pods-communicate-across-cluster-using-cni-provided-networking
tags: [SoftwareEngineering/Containers, SoftwareEngineering/Kubernetes, SoftwareEngineering/Networking]
title: Pods communicate across cluster using CNI-provided networking
type: Fact
---

## Summary

Kubernetes gives every Pod its own IP address and expects Pods to reach each other directly, without NAT, regardless of which node they land on. The cluster itself has no built-in mechanism for this—a CNI (Container Network Interface) plugin is what actually wires up the flat, routable network that makes it work.

## Details

- Each node runs a CNI plugin (Calico, Flannel, Cilium, Azure CNI, etc.) that allocates a slice of the cluster's Pod CIDR to that node and assigns IPs to Pods scheduled there.
- On pod creation, the plugin creates a veth pair, attaches one end to the Pod's network namespace and the other to the node's bridge/overlay, then programs routes so traffic for other nodes' Pod ranges is sent to the right place (via an overlay tunnel, direct routing, or cloud-provider VPC routing depending on the plugin).
- The result is a single flat address space: any Pod can reach any other Pod's IP directly, whether they're on the same node or different ones—the plugin hides the per-node subnetting from workloads.
- This is the foundation everything else in the model builds on: [[etcd stores cluster network state and service configuration]] persists the state that drives this, [[Kube-Proxy Implements Services Using Iptables or IPVS]] and [[Kubernetes Provides NodePort and LoadBalancer for External Service Access]] build Service-level abstractions on top of it, and [[Network policies control traffic flow between pods using labels and namespaces]] restricts it after the fact.

## Related

- Up: [[MOC - Container Networking Model]]
- [[CNI plugins provide different network models and features]]—how the plugin implements this
- [[Container Runtime Configures Pod Networking Through CNI Plugins]]—who invokes the plugin and when
- [[Kubernetes networking components coordinate through a defined workflow]]—full component sequence
