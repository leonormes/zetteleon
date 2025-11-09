---
aliases: []
confidence: 
created: 2025-10-10T09:05:47Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:12Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Log Analysis Summary & Alert Plan
type:
uid: 
updated: 
version:
---

Based on analysis of 1,000 log entries from the testing cluster, I've identified **5 critical alert categories** that should be implemented across all clusters.

## Identified Issues in Logs

### 1. **Calico Network Policy Configuration Errors** (HIGH SEVERITY)

- **Pattern**: `Error creating resource StagedNetworkPolicy ... cannot specify ports with a service selector`
- **Frequency**: Very high (100+ occurrences in 1-hour window)
- **Namespaces**: `cert-manager`, `monitoring`
- **Impact**: Network policies failing to apply, potential security gaps

### 2. **MongoDB Metrics Exporter Duplicate Metrics** (HIGH SEVERITY) ✅ *Already exists*

- **Pattern**: `collected metric ... was collected before with the same name and label values`
- **Frequency**: Extremely high (100+ errors per scrape)
- **Namespace**: `testing`
- **Impact**: Prometheus scrape failures, monitoring blind spots

### 3. **Kubernetes API Deprecation Warnings** (WARNING SEVERITY) ✅ *Already exists*

- **Pattern**: `v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice`
- **Frequency**: High (every 15-30 seconds)
- **Component**: `calico-typha`
- **Impact**: Will break on K8s v1.33+ upgrade

### 4. **Calico Felix NAT Table Inconsistencies** (MEDIUM SEVERITY)

- **Pattern**: `Chain had unexpected inserts, marking for resync ... chainName="POSTROUTING" table="nat"`
- **Frequency**: Periodic (every ~25 seconds)
- **Component**: `calico-node` (felix)
- **Impact**: Network routing instability, potential packet drops

### 5. **CoreDNS Configuration Warnings** (LOW SEVERITY)

- **Pattern**: `No files matching import glob pattern: custom/*.override`
- **Frequency**: Startup warnings
- **Component**: `coredns`
- **Impact**: Informational, expected if no custom configs

## Recommended Alert Plan

### **Priority 1: New Critical Alerts**

#### Alert 1: Calico Network Policy Validation Errors

```hcl
name: "Calico Network Policy Configuration Errors"
severity: high
condition: count_over_time({cluster=~".*"} |~ "Error creating resource StagedNetworkPolicy.*cannot specify ports" [5m]) > 10
for: 5m
description: |
  *Cluster:* {{ $labels.cluster }}
  *Namespace:* {{ $labels.namespace }}
  *Component:* Calico API Server

  Calico is repeatedly failing to create network policies due to configuration errors.
  This indicates invalid NetworkPolicy specifications that mix service selectors with port definitions.

  *Impact:*
  • Network policies not being enforced
  • Potential security policy gaps
  • Resource reconciliation loops

  *Action Required:*
  1. Review NetworkPolicy definitions in affected namespaces
  2. Remove port specifications from policies using service selectors
  3. Check for ArgoCD/Helm chart misconfigurations
  4. Verify Calico version compatibility with policy syntax
```

#### Alert 2: Calico Felix NAT Table Resync Loops

```hcl
name: "Calico Felix NAT Table Inconsistencies"
severity: medium
condition: count_over_time({cluster=~".*", container="calico-node"} |~ "Chain had unexpected inserts.*POSTROUTING.*nat" [10m]) > 20
for: 10m
description: |
  *Cluster:* {{ $labels.cluster }}
  *Node:* {{ $labels.node }}

  Calico Felix is detecting unexpected iptables NAT rules and repeatedly resyncing.
  This may indicate external modifications to iptables or conflicts with other network components.

  *Impact:*
  • Network performance degradation
  • Potential packet drops during resync
  • Increased CPU usage on nodes

  *Action Required:*
  1. Check for other network tools modifying iptables (kube-proxy, CNI plugins)
  2. Review node-level network configuration
  3. Investigate if Azure CNI overlay is conflicting with Calico
  4. Check Calico Felix logs for more details: `kubectl logs -n calico-system <pod> -c calico-node`
```

### **Priority 2: Enhanced Existing Alerts**

#### Alert 3: Pod Restart/CrashLoop Detection (NEW)

```hcl
name: "Pod Restart Loop Detected"
severity: high
condition: rate(kube_pod_container_status_restarts_total{cluster=~".*"}[15m]) > 0.5
for: 15m
description: |
  *Cluster:* {{ $labels.cluster }}
  *Namespace:* {{ $labels.namespace }}
  *Pod:* {{ $labels.pod }}
  *Container:* {{ $labels.container }}

  Container is restarting frequently, indicating instability.

  *Impact:*
  • Service disruption
  • Potential data loss
  • Resource waste

  *Action Required:*
  1. Check pod logs: `kubectl logs -n {{ $labels.namespace }} {{ $labels.pod }} --previous`
  2. Check events: `kubectl describe pod -n {{ $labels.namespace }} {{ $labels.pod }}`
  3. Review resource limits (OOMKilled?)
  4. Check liveness/readiness probe configuration
```

#### Alert 4: High Error Log Rate (NEW)

```hcl
name: "High Error Log Rate"
severity: medium
condition: sum(rate({cluster=~".*", detected_level="error"}[5m])) by (cluster, namespace, container) > 1
for: 10m
description: |
  *Cluster:* {{ $labels.cluster }}
  *Namespace:* {{ $labels.namespace }}
  *Container:* {{ $labels.container }}

  Container is producing error logs at an elevated rate (>1 error/sec sustained).

  *Action Required:*
  1. Review recent error logs in Grafana Loki
  2. Check for application-specific issues
  3. Verify external dependencies (databases, APIs)
  4. Review recent deployments or configuration changes
```

### **Priority 3: Proactive Monitoring**

#### Alert 5: Persistent Volume Issues (NEW)

```hcl
name: "Persistent Volume Mount Failures"
severity: critical
condition: count_over_time({cluster=~".*", reason="FailedMount"}[10m]) > 5
for: 5m
description: |
  *Cluster:* {{ $labels.cluster }}
  *Namespace:* {{ $labels.namespace }}
  *Pod:* {{ $labels.pod }}

  Pod cannot mount required persistent volumes.

  *Impact:*
  • Pod stuck in Pending/ContainerCreating state
  • Application unavailable
  • Data access failures

  *Action Required:*
  1. Check PVC status: `kubectl get pvc -n {{ $labels.namespace }}`
  2. Check StorageClass availability
  3. Verify CSI driver health (Calico CSI, Azure Disk CSI)
  4. Check node storage capacity
```

## Implementation Priority

| Priority | Alert                 | Severity | Reason                                    |
| -------- | --------------------- | -------- | ----------------------------------------- |
| **1**    | Network Policy Errors | HIGH     | Security impact, high frequency           |
| **2**    | Pod Restart Loops     | HIGH     | Service availability                      |
| **3**    | PV Mount Failures     | CRITICAL | Data access, blocking issue               |
| **4**    | Felix NAT Resync      | MEDIUM   | Performance, already exists but recurring |
| **5**    | High Error Rate       | MEDIUM   | General health monitoring                 |

## Next Steps

1. **Implement Priority 1 alerts** (Network Policy + Pod Restarts)
2. **Test alerts** in testing cluster to tune thresholds
3. **Roll out to all clusters** via Terraform
4. **Document runbooks** for each alert in Confluence/Wiki
5. **Review alert noise** after 1 week and adjust thresholds

Would you like me to implement these alerts in the Terraform configuration?
