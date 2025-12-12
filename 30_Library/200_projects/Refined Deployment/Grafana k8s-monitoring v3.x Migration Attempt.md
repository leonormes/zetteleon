---
aliases: []
confidence: 
created: 2025-11-10T17:56:07Z
epistemic: 
last_reviewed: 
modified: 2025-11-12T14:24:27Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Grafana k8s-monitoring v3.x Migration Attempt
type: 
uid: 
updated: 
---

## Grafana k8s-monitoring v3.x Migration Attempt

**Date**: 2025-11-10
**Status**: ❌ Failed - Rolled back to v1.5.4
**Environment**: Testing cluster (fitfile-testing)

### Summary

Attempted to migrate Grafana k8s-monitoring from v1.5.4 to v3.5.6 in the testing environment. The migration was technically successful in terms of deployment, but **logs stopped flowing to Grafana Cloud**, forcing a rollback.

### What Was Completed

#### ✅ Successful Steps

1. **Added k8s-monitoring to chart-manager**
   - Modified chart-manager to support `--skip-validation` flag
   - Added chart configuration to `config.yaml`
   - Successfully imported chart v3.5.6 to fitfileregistry.azurecr.io

2. **Updated version manager**
   - Set testing environment to v3.5.6 in fitfile-version-manager
   - Commits: `6b390ff`, `cafbb5e`

3. **Migrated configuration from v1.x to v3.x**
   - Created backup: `ffnodes/fitfile/testing/values.yaml.v1.5.4.backup`
   - Converted v1.x config structure to v3.x requirements:
     - Explicitly nulled v1.x fields (externalServices, metrics, logs, traces, alloy, prometheus-operator-crds)
     - Added required `cluster.name: "fitfile-testing"`
     - Converted to `destinations` array format
     - Renamed feature sections (clusterMetrics, clusterEvents, podLogs)
     - Updated Alloy instance naming (alloy-metrics, alloy-logs, alloy-singleton)

4. **Imported missing images to ACR**
   - `prometheus/node-exporter:v1.10.2`
   - `kube-state-metrics/kube-state-metrics:v2.17.0`
   - `grafana/helm-chart-toolbox-kubectl:0.1.1`

5. **Deployed v3.5.6 successfully**
   - All Alloy Operator pods running
   - All Alloy instances created (metrics, logs, singleton)
   - node-exporter and kube-state-metrics operational
   - No errors in pod logs

#### ❌ Critical Issue: Logs Not Flowing

**Problem**: Despite all pods running without errors, logs were **not reaching Grafana Cloud Loki**.

**Root Cause Investigation**:

1. **Initial attempt** - Used simple `url` field with template variables:

   ```yaml
   destinations:
     - name: "grafana-cloud-logs"
       type: "loki"
       url: "${loki-host}/loki/api/v1/push"
   ```

   - **Failed**: Chart literally used `${loki-host}` as string, not substituted

2. **Second attempt** - Used hardcoded URLs:

   ```yaml
   destinations:
     - name: "grafana-cloud-logs"
       type: "loki"
       url: "https://logs-prod-008.grafana.net/loki/api/v1/push"
   ```

   - **Failed**: Chart still generated `${loki-host}` in Alloy config, ignoring hardcoded URL

3. **Third attempt** - Used `hostKey` field:

   ```yaml
   destinations:
     - name: "grafana-cloud-logs"
       type: "loki"
       hostKey: "loki-host"
   ```

   - **Failed**: Chart didn't recognize `hostKey`, still generated broken template

4. **Fourth attempt** - Found correct syntax using `urlFrom` with Alloy expressions:

   ```yaml
   destinations:
     - name: "grafana-cloud-logs"
       type: "loki"
       urlFrom: convert.nonsensitive(remote.kubernetes.secret.grafana_cloud_logs.data["loki-host"]) + "/loki/api/v1/push"
       auth:
         type: "basic"
         usernameKey: "loki-username"
         passwordKey: "loki-password"
       secret:
         create: false
         name: "monitoring"
         namespace: "monitoring"
   ```

   - **Deployed successfully**: Alloy config generated correctly with `remote.kubernetes.secret` references
   - **Still failed**: Logs did not reach Grafana Cloud (verified by user)

### Key Learnings

#### v3.x Chart Behavior

1. **`urlFrom` is required** for dynamic secret references, not `url`
2. **`secret.create: false`** must be set when using pre-existing secrets
3. **Hook jobs** can block deployments if images are wrong (registry doubling issue)
4. **Port conflicts** between v1.x and v3.x components during migration

#### v3.x Architecture Changes

- **v1.x**: Standalone Alloy Helm chart
- **v3.x**: Alloy Operator dynamically creates Alloy instances
- **v1.x**: Features enabled by default
- **v3.x**: All features disabled by default (must explicitly enable)
- **v1.x**: `externalServices` object
- **v3.x**: `destinations` array
- **v3.x**: Cluster name is REQUIRED field

### Unresolved Mystery

**Why logs didn't flow despite correct configuration:**

The final configuration (Attempt 4) had:

- ✅ Correct `urlFrom` syntax with `remote.kubernetes.secret` references
- ✅ All Alloy pods running without errors
- ✅ Alloy config correctly generated with proper secret references
- ✅ No error messages in logs
- ❌ **But logs were NOT reaching Grafana Cloud**

Possible theories:

1. Silent failure in Alloy's secret loading mechanism
2. Network/firewall issue specific to v3.x Alloy instances
3. Loki authentication issue not being logged
4. Secret keys mismatch (hyphenated vs underscore)
5. Timing issue - logs might have started flowing after rollback was initiated

### Current Status

- **Production**: v1.5.4 ✅
- **Staging**: v1.5.4 ✅
- **Testing**: v1.5.4 ✅ (rolled back from v3.5.6)
- **Logs**: Flowing to Grafana Cloud ✅
- **v3.x Migration**: Blocked pending investigation ⏸️

### Next Steps for Future v3.x Migration

#### Required Investigation

1. **Test v3.x in isolated environment first**
   - Deploy v3.x alongside v1.x with different release name
   - Verify logs actually reach Grafana Cloud before switching
   - Monitor for 30+ minutes to ensure sustained log delivery

2. **Debug secret loading**
   - Verify secret keys are exactly correct (hyphens vs underscores)
   - Check if Alloy is actually reading the secret values
   - Enable debug logging in Alloy if available

3. **Contact Grafana support**
   - Provide our configuration
   - Ask why `urlFrom` with correct syntax didn't work
   - Check if there are known issues with secret substitution

4. **Alternative approach - Embedded secrets**
   - Try using `secret.embed: true` with direct credential values
   - This bypasses the secret loading mechanism

#### Prerequisites Before Retry

- [ ] Understand root cause of logs not flowing
- [ ] Test in non-production cluster first
- [ ] Have confirmed working v3.x example configuration
- [ ] Ensure ArgoCD hook job images are correct
- [ ] Plan for faster rollback process
