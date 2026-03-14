---
created: 2026-03-02T12:26:20+00:00
modified: 2026-03-14T11:10:52+00:00
title: Node-Exporter-Security-Config
---

## Configuring Node Exporter Security Context

In the `FITFILE` monitoring stack, Node Exporter is deployed as a sub-dependency of the `clusterMetrics` feature. If your cluster has strict Pod Security Policies (PSP) or Admission Controllers (like Kyverno or Gatekeeper), you may need to override the default security settings to resolve "disallowed" errors.

### Configuration Path

Because of the chart's hierarchical structure, the overrides must be placed under the `clusterMetrics.node-exporter` key in your root `values.yaml`.

- Root Chart: `k8s-monitoring`
- Feature Alias: `clusterMetrics` (points to `feature-cluster-metrics`)
- Component Alias: `node-exporter` (points to `prometheus-node-exporter`)

### YAML Configuration Example

Add or update the following block in your `values.yaml` file:

```yaml
clusterMetrics:
  node-exporter:
    # 1. Pod-level Security Context
    # Applied to the entire Pod
    securityContext:
      fsGroup: 65534
      runAsGroup: 65534
      runAsNonRoot: true
      runAsUser: 65534
      # seccompProfile:
      #   type: RuntimeDefault

    # 2. Main Container Security Context
    # Applied specifically to the node-exporter container
    containerSecurityContext:
      readOnlyRootFilesystem: true
      allowPrivilegeEscalation: false
      capabilities:
        add:
          - SYS_TIME  # Required if gathering clock-related metrics
        drop:
          - ALL

    # 3. RBAC Proxy Security Context (if enabled)
    # Applied to the sidecar that protects the metrics endpoint
    kubeRBACProxy:
      containerSecurityContext:
        allowPrivilegeEscalation: false
        capabilities:
          drop:
            - ALL
        readOnlyRootFilesystem: true
        runAsNonRoot: true
        runAsUser: 65532
```

### Common Security Fixes

| Issue | Solution |
|:--- |:--- |
| Privileged container not allowed | Set `allowPrivilegeEscalation: false` in `containerSecurityContext`. |
| Must run as non-root | Set `runAsNonRoot: true` and provide a numeric `runAsUser` (e.g., `65534`). |
| Read-only root filesystem required | Set `readOnlyRootFilesystem: true`. Node Exporter uses host mounts for data, so the container's own root can usually be read-only. |
| Capabilities "ALL" disallowed | Use the `capabilities.drop: ["ALL"]` block shown above. |

### OpenShift Considerations

If you are deploying to OpenShift, the cluster typically manages UIDs automatically via Security Context Constraints (SCC). In this case, you may need to omit the `runAsUser` and `fsGroup` fields to allow the platform to assign them:

```yaml
clusterMetrics:
  node-exporter:
    securityContext:
      runAsNonRoot: true  # Still required, but let SCC handle the specific ID
    containerSecurityContext:
      allowPrivilegeEscalation: false
```

### Verification

After applying the changes, verify the Pod's effective security context using `kubectl`:

```bash
kubectl get pod -l app.kubernetes.io/name=node-exporter -o jsonpath='{.items[0].spec.containers[0].securityContext}'
```
