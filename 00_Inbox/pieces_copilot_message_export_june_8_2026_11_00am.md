---
created: 2026-06-08T10:00:14+00:00
modified: 2026-06-08T11:06:32+00:00
---
*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Monday Jun 8, 2026 - 11:00 AM*
---
All three cursors are now drained (two returned `sufficient`, one hit the circuit breaker as a redundancy guard — the evidence base is complete). I have rich, grounded material across 250+ candidates. Here is the full experiment guide.

---

## Structured Metadata Pilot Grafana Cloud Log Enrichment via Helm

### Background and why this matters

Your LTM carries extensive audit work from late May through early June 2026 ([Grafana Alloy Audit Report](https://fitfiletest.grafana.net/explore?schemaVersion=1&panes=%7B%227ho%22%3A%7B%22datasource%22%3A%22grafanacloud-logs%22%2C%22queries%22%3A%5B%7B%22refId%22%3A%22A%22%2C%22expr%22%3A%22%7Bcluster%3D%5C%22testing%5C%22%7D%20%7C%20json%22%2C%22queryType%22%3A%22range%22%2C%22datasource%22%3A%7B%22type%22%3A%22loki%22%2C%22uid%22%3A%22grafanacloud-logs%22%7D%2C%22editorMode%22%3A%22builder%22%2C%22direction%22%3A%22backward%22%7D%5D%2C%22range%22%3A%7B%22from%22%3A%22now-1h%22%2C%22to%22%3A%22now%22%7D%2C%22panelsState%22%3A%7B%22logs%22%3A%7B%22sortOrder%22%3A%22Descending%22%7D%7D%2C%22compact%22%3Afalse%7D%7D&orgId=1), memory IDs `ea41c74d-273d-4b5a-b204-922da0f8e821`, `0841deb8-bfdc-4862-a646-94d6fdba0d8c`). The core finding: you have high-cardinality fields (`pod`, `container`, `requestID`, `grpc.service`, `grpc.method`, `peer.address`, `component`, `logger`, `reason`, `service_name`, `namespace_name`, `application`) landing in **indexed Loki stream labels**, which inflates cost and can break selectors when fields accidentally migrate between label tiers across chart versions (the FTFL-638 war story: `pod` ending up in `structured_metadata` rather than labels, making `{pod="..."}` queries stop working).

The fix is to be **intentional**: keep a small stable set of indexed labels, and push everything else to `structuredMetadata` where it enriches log detail without ballooning cardinality.

---

## The Experiment

### Scope

**One workload, non-prod only:** `spicedb` in `fitfiletest`. It already emits `requestID`, `grpc.service`, `grpc.method`, and `peer.address` — confirmed visible in [Grafana Explore (testing cluster)](https://fitfiletest.grafana.net/explore?schemaVersion=1&panes=%7B%227ho%22%3A%7B%22datasource%22%3A%22grafanacloud-logs%22%2C%22queries%22%3A%5B%7B%22refId%22%3A%22A%22%2C%22expr%22%3A%22%7Bcluster%3D%5C%22testing%5C%22%7D%20%7C%20json%22%2C%22queryType%22%3A%22range%22%2C%22datasource%22%3A%7B%22type%22%3A%22loki%22%2C%22uid%22%3A%22grafanacloud-logs%22%7D%2C%22editorMode%22%3A%22builder%22%2C%22direction%22%3A%22backward%22%7D%5D%2C%22range%22%3A%7B%22from%22%3A%22now-1h%22%2C%22to%22%3A%22now%22%7D%2C%22panelsState%22%3A%7B%22logs%22%3A%7B%22sortOrder%22%3A%22Descending%22%7D%7D%2C%22compact%22%3Afalse%7D%7D&orgId=1). Perfect pilot candidate because the rich fields are already there in the log bodies.

### Success criteria (from your own audit doc)

- Moved fields stop inflating the indexed label set
- Log detail view in Explore still shows `requestID`, `grpc.service`, `grpc.method`, `peer.address` (just as metadata, not as selectors)
- Existing queries using `{cluster="testing", namespace="spicedb"}` continue to work
- No new labels appear in the Loki label index

---

## Step-by-step instructions

### Step 1 — Baseline snapshot (5 min)

Before touching any code, record the current state:

```bash
# In Grafana Explore, run this query and screenshot the label browser:
{cluster="testing", namespace="spicedb"} | json

# Then run in your terminal to capture the current label set:
gcx logs query --context fitfiletest '{cluster="testing", namespace="spicedb"}' \
  --since 15m --limit 10 -o json | jq '[.[].stream | keys] | flatten | unique'
```

Save the output — this is your before state.

---

### Step 2 — Add the toggle to `values.yaml`

In `deployment/charts/ffnode/values.yaml`, add a new block under `grafanaAlloy`:

```yaml
grafanaAlloy:
  # ... existing config (frontendObservability, chart, etc.) ...

  structuredMetadataPilot:
    enabled: false   # flip to true to activate the pilot
    workload: spicedb
```

This gives you a clean, reviewable toggle. Default is `false` so no clusters are affected until you explicitly opt in.

---

### Step 3 — Wire the toggle into `_grafana.tpl`

In `deployment/charts/ffnode/templates/_grafana.tpl`, inside the `{{- define "ffnode.grafana.values" -}}` block, add a conditional `extraConfig` section that only activates when the pilot flag is set:

```yaml
{{- if .Values.grafanaAlloy.structuredMetadataPilot.enabled }}
logs:
  podLogsViaLoki:
    enabled: true
    extraRelabelingRules: |
      # Keep only stable, low-cardinality fields as indexed labels
      rule {
        action        = "labeldrop"
        regex         = "pod|container|service_name|reason|stream"
      }
    extraStageBlocks: |
      stage.labels {
        values = {
          cluster   = "",
          namespace = "",
          job       = "",
        }
      }
      stage.structured_metadata {
        values = {
          pod           = "pod",
          container     = "container",
          service_name  = "service_name",
        }
      }
      # For JSON logs that include runtime fields (e.g. spicedb):
      stage.json {
        expressions = {
          requestID   = "requestID",
          grpc_svc    = "grpc.service",
          grpc_method = "grpc.method",
          peer_addr   = "peer.address",
          component   = "component",
          logger      = "logger",
        }
      }
      stage.structured_metadata {
        values = {
          requestID   = "requestID",
          grpc_svc    = "grpc_svc",
          grpc_method = "grpc_method",
          peer_addr   = "peer_addr",
          component   = "component",
          logger      = "logger",
        }
      }
{{- end }}
```

> **Important gotcha from your audit history:** Alloy does **not** have `stage.static_structured_metadata`. If you need to inject static values, use `stage.static_labels` first, then promote with `stage.structured_metadata`. Also: never write the same field to both indexed labels and structured metadata in the same pipeline — this caused FTFL-638 (`pod` appearing in both tiers).

---

### Step 4 — Render and inspect (no deploy yet)

```bash
# From deployment/ root:
helm template dev ./charts/ffnode \
  -f ./ffnodes/fitfile/ff-test-a/values.yaml \
  --set grafanaAlloy.structuredMetadataPilot.enabled=true \
  -s templates/grafana-alloy-application.yaml \
  | less
```

Check the rendered output:
- The `extraStageBlocks` appear under the correct Alloy config section
- No duplicate field definitions
- The `labels` block only contains `cluster`, `namespace`, `job`

---

### Step 5 — Deploy to `fitfiletest` only

In `ffnodes/fitfile/ff-test-a/values.yaml` (or the equivalent `fitfiletest` overlay):

```yaml
grafanaAlloy:
  structuredMetadataPilot:
    enabled: true
    workload: spicedb
```

Commit to your branch (`feature/FTFL-673-grafana-alloy-upgrade` or a new branch), push, and let ArgoCD sync to `fitfiletest` only. Watch the ArgoCD sync status:

```bash
kubectl --context fitfile-cloud-testing-aks-cluster \
  get application grafana-k8s-monitoring -n argocd -w
```

---

### Step 6 — Validate in Grafana Explore

Open [Grafana Explore (fitfiletest)](https://fitfiletest.grafana.net/explore?schemaVersion=1&panes=%7B%227ho%22%3A%7B%22datasource%22%3A%22grafanacloud-logs%22%2C%22queries%22%3A%5B%7B%22refId%22%3A%22A%22%2C%22expr%22%3A%22%7Bcluster%3D%5C%22testing%5C%22%7D%20%7C%20json%22%2C%22queryType%22%3A%22range%22%2C%22datasource%22%3A%7B%22type%22%3A%22loki%22%2C%22uid%22%3A%22grafanacloud-logs%22%7D%2C%22editorMode%22%3A%22builder%22%2C%22direction%22%3A%22backward%22%7D%5D%2C%22range%22%3A%7B%22from%22%3A%22now-1h%22%2C%22to%22%3A%22now%22%7D%2C%22panelsState%22%3A%7B%22logs%22%3A%7B%22sortOrder%22%3A%22Descending%22%7D%7D%2C%22compact%22%3Afalse%7D%7D&orgId=1) and run these checks:

| Check | Query | Expected result |
|---|---|---|
| Stream selector still works | `{cluster="testing", namespace="spicedb"}` | Returns logs |
| `pod` no longer a stream label | Label browser | `pod` absent from indexed labels |
| `requestID` visible in detail | Click a log line | `requestID`, `grpc.service`, `grpc.method` in metadata panel |
| `pod` visible in detail | Click a log line | `pod` in metadata panel (not label bar) |
| Old dashboards unaffected | Any existing spicedb dashboard | Still renders |

---

### Step 7 — Rollout decision

**Pilot passes** → repeat the pattern for `mongodb`/`ff-test-a` and then template it as the default for all new workloads by moving `structuredMetadataPilot.enabled: true` into the base `values.yaml` and removing the flag.

**Pilot fails** (e.g. a dashboard breaks) → set `structuredMetadataPilot.enabled: false` in the overlay, sync, and investigate which field was being used as a selector in a way you didn't expect.

---

### Open questions to resolve before generalising

- **`component` and `logger`**: keep as indexed labels for spicedb (useful for quick namespace-level filtering) or move to structured metadata? Your audit notes flagged them as candidates for metadata but their selectivity varies by workload.
- **`pod` during the transition**: your earlier debugging (FTFL-638) showed `pod` appearing as an indexed label despite the override — check the rendered ConfigMap directly after deploy: `kubectl --context fitfile-cloud-testing-aks-cluster get configmap -n monitoring -l app.kubernetes.io/name=alloy -o yaml | grep pod`.
- **Chart version alignment**: staging/prod still run k8s-monitoring `1.5.4` (Alloy v1.3.1) while testing runs `4.1.3` (Alloy v1.12.2). The `structuredMetadata` behaviour differs between these versions — the pilot only proves the pattern on v4; a separate migration plan is needed before promoting to prod.