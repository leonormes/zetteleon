---
aliases: []
created: 2025-02-07T12:57:53Z
ID: "7a5"
last_reviewed: ""
modified: 2026-02-01T15:08:15+00:00
status: ""
tags: []
title: eni_scaling_and_ip_address_limits
type: ""
updated: 
---

## ENI Scaling and IP Address Limits

### Key Points

- Each EC2 instance has limits on the number of ENIs and secondary IP addresses it can handle, based on its instance type.
- In EKS, each ENI on a worker node can be assigned multiple IP addresses for pods, but scaling is constrained by these limits.
- Monitoring ENI usage is crucial in large EKS clusters to avoid running out of IP addresses.

### Linked Zettels

- VPC CNI Plugin and ENIs
- ENI Usage Monitoring

---

[aws eni](<../Notes/aws eni.md>)
