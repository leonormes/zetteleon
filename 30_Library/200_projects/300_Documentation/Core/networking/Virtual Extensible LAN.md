---
aliases: []
confidence: 
created: 2025-03-25T12:57:08Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [calico, k8s, networking, vxlan]
title: Virtual Extensible LAN
type: 
uid: 
updated: 
version: 
---

No worries. I'm glad to hear that the issue is solved.

VXLAN (Virtual Extensible LAN) is an encapsulation protocol that creates overlay networks, allowing pod-to-pod communication across nodes even when the underlying network doesn't understand pod IP addresses.

Purpose of VXLAN in Calico

Overlay networking: VXLAN creates a network overlay that allows pods to communicate across nodes without requiring the underlying network to be aware of pod IP addresses Overlay networking.

Cloud compatibility: VXLAN is specifically supported in environments where IP-in-IP is not, such as Azure. In fact, Azure blocks IP-in-IP packets but supports VXLAN Azure.

Cross-subnet communication: VXLAN enables pod traffic to cross subnet boundaries, which is particularly useful in cloud environments like AWS multi-AZ deployments or Azure VNETs Overlay networking.

Best Practices for VXLAN

For optimal performance, we recommends using the "cross-subnet" option with VXLAN to minimize encapsulation overhead:

```yaml
apiVersion: projectcalico.org/v3
kind: IPPool
metadata:
  name: ippool-vxlan-cross-subnet-1
spec:
  cidr: 192.168.0.0/16
  vxlanMode: CrossSubnet
  natOutgoing: true
```

This configuration ensures VXLAN encapsulation is only used when traffic crosses subnet boundaries, which provides better performance in AWS multi-AZ deployments and Azure VNETs Overlay networking.

It's also recommended to set natOutgoing: true with VXLAN to prevent asymmetric routing issues that could cause traffic to be filtered due to RPF checks IP pool definition.

The fact that you can ping pods across nodes confirms that your VXLAN setup is working correctly, allowing inter-node pod communication as expected.

Please let me know if further clarification is needed.
