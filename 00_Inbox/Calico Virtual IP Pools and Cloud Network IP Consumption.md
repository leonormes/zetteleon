---
created: 2026-01-20T08:54:54+00:00
modified: 2026-01-20T20:23:26+00:00
title: Calico Virtual IP Pools and Cloud Network IP Consumption
---

# Calico Virtual IP Pools and Cloud Network IP Consumption

You are correct: **using Calico IP pools for Kubernetes pod networking** (as opposed to the default cloud CNI) is a strategic way to avoid consuming precious Azure or AWS VNet/Subnet IPs for every pod. This is especially important in environments where subnet space is limited or tightly managed.

## How Calico Virtual IP Pools Work

- **Calico CNI** allows you to define custom IP pools (e.g., 192.168.x.x/16, 172.16.x.x/16) that are **not part of your cloud VNet/subnet**.
- **Pods** are assigned IPs from these Calico pools, not from the underlying Azure/AWS subnet.
- **Only nodes and infra components** (e.g., VM NICs, load balancers, NAT gateways, etc.) consume IPs from the cloud VNet/subnet.
- **Pod-to-pod traffic** is routed via Calico's overlay network (using encapsulation like VXLAN or IP-in-IP), not directly on the VNet.

## Benefits

| Feature                        | Calico IP Pools (Overlay)         | Azure/AWS CNI (VNet IPs)         |
|------------------------------- |-----------------------------------|----------------------------------|
| Pod IPs consume VNet IPs?      | **No**                            | **Yes**                          |
| Node/Infra IPs consume VNet?   | Yes (nodes, LB, NAT, etc.)        | Yes (nodes, pods, LB, NAT, etc.) |
| Pod scaling limited by subnet? | No (limited by Calico pool size)  | Yes (limited by subnet size)     |
| Network visibility             | Overlay (encapsulated)            | Native VNet routing              |

## Azure Example

Your [AKS cluster configuration](https://gemini.google.com/app/9eb055683ea75339) shows:

- **Network configuration:** Azure CNI Overlay
- **Pod CIDR:** 10.244.0.0/16 (not part of VNet)
- **Service CIDR:** 10.2.0.0/24 (not part of VNet)
- **Network policy engine:** Calico

This means:

- **Pods** get IPs from 10.244.0.0/16 (Calico overlay), not from the VNet (e.g., 10.0.0.0/16).
- **Only nodes, load balancers, and other infra** consume VNet IPs.

## AWS Example

- With **Calico overlay** on EKS, you can similarly define non-VPC IP pools for pods.
- Only nodes and infra (ENIs, NAT, etc.) consume VPC subnet IPs.

## Practical Guidance

- **Subnet Sizing:** You only need to size your Azure/AWS subnets for the number of nodes and infra, not for all pods.
- **Pod Scaling:** You can scale pods far beyond the VNet subnet size, limited only by your Calico pool and node resources.
- **IP Pool Management:** Make sure your Calico IP pools do not overlap with any VNet/subnet or on-prem ranges to avoid routing conflicts.

## Reference

- [AKS Network Concepts - Azure CNI Overlay](https://learn.microsoft.com/en-us/azure/aks/azure-cni-overlay)
- [Calico IP Pool Documentation](https://docs.tigera.io/calico/latest/networking/ip-pools)
- [EKS Calico Networking Analysis Report](file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Tools/FF%20Deployment%20Docs/EKS%20Calico%20Networking%20Analysis%20Report)

---

**Summary:**
By using Calico virtual IP pools, your cluster only consumes Azure/AWS network IPs for infrastructure (nodes, LB, NAT, etc.), not for every pod. This enables much higher pod density and avoids subnet exhaustion issues common with cloud-native CNI plugins.

If you need a sample Calico IP pool manifest or want to review your current pool configuration, let me know!
