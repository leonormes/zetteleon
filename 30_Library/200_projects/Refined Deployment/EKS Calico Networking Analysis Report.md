---
aliases: []
confidence: 
created: 2025-09-26T10:38:07Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [security, topic/technology/networking]
title: EKS Calico Networking Analysis Report
type:
uid: 
updated: 
version:
---

## EKS Calico Networking Analysis Report

**Cluster:** eoe-sde-codisc
**Date:** [[2025-09-26]]
**Calico Version:** v3.29.1 (Client: v3.29.3)
**Analysis Tool:** calicoctl v3.29.3

### Executive Summary

This EKS cluster is running **Calico Enterprise (Tigera Secure)** as the Container Network Interface (CNI), providing advanced networking, security, and observability capabilities. The cluster uses VXLAN overlay networking with comprehensive network policies managed through tiered security policies.

### 1. Cluster Architecture Overview

#### Nodes Configuration

| Node Name                                 | Instance Type | AZ         | Internal IP    | Pod CIDR Block           |
| ----------------------------------------- | ------------- | ---------- | -------------- | ------------------------ |
| ip-10-65-4-211.eu-west-2.compute.internal | m5.xlarge     | eu-west-2a | 10.65.4.211/23 | VXLAN Tunnel IP assigned |
| ip-10-65-5-167.eu-west-2.compute.internal | m5.xlarge     | eu-west-2b | 10.65.5.167/23 | VXLAN Tunnel IP assigned |
| ip-10-65-6-75.eu-west-2.compute.internal  | m5.xlarge     | eu-west-2c | 10.65.6.75/23  | VXLAN Tunnel IP assigned |
| ip-10-65-6-85.eu-west-2.compute.internal  | m5.xlarge     | eu-west-2c | 10.65.6.85/23  | VXLAN Tunnel IP assigned |

#### Key Architectural Facts

- **CNI Mode:** Calico VXLAN overlay (no IPIP, no native routing)
- **BGP:** Disabled/No mesh (using VXLAN for inter-node communication)
- **Typha:** Enabled for scalable datastore access (2 replicas)
- **IP Pool:** Single pool with /16 CIDR, /26 block size per node
- **NAT Outgoing:** Enabled for internet-bound traffic

### 2. IP Address Management (IPAM)

#### IP Pool Configuration

```yaml
Name: default-ipv4-ippool
CIDR: 192.168.0.0/16 # (masked for security)
Block Size: /26 (64 IPs per node)
Encapsulation: VXLAN Always
NAT Outgoing: true
Node Selector: all()
```

#### Key IPAM Facts

- **Total Available IPs:** ~65,536 IP addresses
- **IPs per Node:** 64 addresses (/26 blocks)
- **Current Node Count:** 4 nodes
- **Theoretical Max Nodes:** ~1,024 nodes
- **VXLAN VNI:** 4096 (default)

#### IP Utilization Status

Based on workload endpoint count, approximately **50-100 pods** are currently running across the cluster, representing minimal IP pool utilization.

### 3. BGP Configuration

#### BGP Status: **DISABLED**

- **BGP Configuration:** Empty/No BGP mesh
- **ASN Assignment:** Default 64512 for all nodes
- **Peering:** None configured
- **Route Reflectors:** Not applicable

**Analysis:** This cluster uses pure VXLAN overlay networking without BGP. All inter-node communication happens through VXLAN tunnels, which is appropriate for cloud environments where BGP mesh may not be necessary.

### 4. Network Security Policies

#### Policy Tiers (5 Tiers configured)

1. **allow-tigera** (Order: 100) - Tigera system components
2. **adminnetworkpolicy** (Order: 1,000) - Admin-level policies
3. **namespace-isolation** (Order: 10,000) - Namespace isolation
4. **default** (Order: 1,000,000) - Default application policies
5. **baselineadminnetworkpolicy** (Order: 10,000,000) - Baseline admin policies

#### Policy Coverage

- **Namespaces with Policies:** 10+ namespaces including system namespaces
- **Global Policies:** 2 global policies (default-allow-all, default-allow-all-dns)
- **Security Model:** Tiered security with default-allow but namespace-level controls

#### Critical Security Policies

- Default DNS resolution allowed globally
- Tigera system components have dedicated access policies
- Individual namespace policies for compliance, monitoring, and security systems

### 5. Workload Endpoints Analysis

#### Pod Distribution

- **Total Workload Endpoints:** 50+ pods across namespaces
- **System Namespaces:** calico-system, calico-cloud, tigera-\*
- **Application Namespaces:** argo, argocd, cert-manager, etc.

#### IP Allocation Pattern

All pods receive IPs from the default-ipv4-ippool with proper VXLAN interface assignments (cali\* interfaces).

### 6. Component Health Assessment

#### Calico System Components Status

| Component               | Replicas | Status  | Health     |
| ----------------------- | -------- | ------- | ---------- |
| calico-node (DaemonSet) | 4/4      | Running | ✅ Healthy |
| calico-typha            | 2/2      | Running | ✅ Healthy |
| calico-kube-controllers | 1/1      | Running | ✅ Healthy |
| calico-csi-node-driver  | 4/4      | Running | ✅ Healthy |

#### Felix Configuration Highlights

- **BPF Mode:** Disabled (traditional iptables mode)
- **Flow Logs:** Configured (flush interval set)
- **Health Port:** 9099
- **Log Level:** Info
- **VXLAN VNI:** 4096

### 7. Security Posture Evaluation

#### Strengths

✅ **Tigera Secure/Calico Enterprise** deployment with advanced security features

✅ **Tiered Network Policies** providing defense-in-depth

✅ **Namespace Isolation** configured

✅ **Compliance and Runtime Security** components deployed

✅ **Intrusion Detection** system active

✅ **Policy Recommendation** engine available

#### Areas for Attention

⚠️ **Encryption:** WireGuard/IPSec encryption not detected

⚠️ **BPF Mode:** Not enabled (could improve performance)

⚠️ **Flow Logs:** Monitor for excessive log volume

### 8. Monitoring & Troubleshooting Readiness

#### Available Observability

- **Prometheus Integration:** Tigera prometheus system active
- **Flow Logs:** Configured and available
- **Policy Recommendations:** System deployed
- **Compliance Reporting:** Active components

#### Diagnostic Commands Reference

```bash
# Node status (requires node access)
./calicoctl node status --allow-version-mismatch

# Flow logs
./calicoctl get flowlog --allow-version-mismatch

# Policy troubleshooting
./calicoctl get networkpolicy --all-namespaces --allow-version-mismatch

# IPAM status
./calicoctl ipam show --show-blocks --allow-version-mismatch
```

### 9. Recommendations

#### Immediate Actions

1. **Monitor IP Pool Utilization** - Set up alerts when pools exceed 80% utilization
2. **Review Global Policies** - Assess if default-allow-all policies align with security requirements
3. **Enable Flow Log Analysis** - Ensure flow logs are being processed and analyzed
4. **Performance Monitoring** - Monitor VXLAN overhead and inter-node communication

#### Future Considerations

1. **WireGuard Encryption** - Consider enabling for encryption in transit
2. **BPF Dataplane** - Evaluate enabling eBPF mode for better performance
3. **Network Segmentation** - Implement stricter default-deny policies
4. **Multi-tenancy** - Further namespace isolation if required

### 10. Architecture Diagram

```sh
┌─────────────────────────────────────────────────────────────────┐
│                        EKS Cluster                             │
│                   eoe-sde-codisc                               │
└─────────────────────────────────────────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │     AWS VPC           │
                    │   10.65.0.0/16        │
                    └───────────┬───────────┘
                                │
        ┌───────────┬───────────┼───────────┬───────────┐
        │           │           │           │           │
   ┌────▼───┐  ┌───▼───┐   ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
   │eu-west │  │eu-west│   │eu-west│   │eu-west│   │eu-west│
   │  -2a   │  │  -2b  │   │  -2c  │   │  -2c  │   │  ...  │
   └────┬───┘  └───┬───┘   └───┬───┘   └───┬───┘   └───┬───┘
        │          │           │           │           │
   ┌────▼───┐  ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
   │ Node 1 │  │ Node 2│   │ Node 3│   │ Node 4│
   │m5.xlge │  │m5.xlge│   │m5.xlge│   │m5.xlge│
   └────────┘  └───────┘   └───────┘   └───────┘
        │          │           │           │
   ┌────▼───┐  ┌───▼───┐   ┌───▼───┐   ┌───▼───┐
   │Calico  │  │Calico │   │Calico │   │Calico │
   │ Node   │  │ Node  │   │ Node  │   │ Node  │
   │(VXLAN) │  │(VXLAN)│   │(VXLAN)│   │(VXLAN)│
   └────────┘  └───────┘   └───────┘   └───────┘
```

### Conclusion

Your EKS cluster is running a sophisticated **Calico Enterprise** setup with comprehensive security, monitoring, and policy management capabilities. The VXLAN overlay networking approach is well-suited for AWS environments, and the tiered policy system provides enterprise-grade network security.

The cluster is currently healthy with good resource utilization patterns. Key focus areas should be monitoring and leveraging the advanced Tigera Secure features for enhanced security posture.
