---
created: 2026-07-14T09:12:51+00:00
modified: 2026-07-20T16:33:31+00:00
permalink: llmeon/ftfl-698-monitoring-gap-report-2026-07-14
tags: [1]
title: FTFL-698 Monitoring Gap Report 2026-07-14
type: note
---

## FTFL-698—Monitoring & Harness Readiness Verification: Gap Report

_Jira: [FTFL-698](https://fitfile.atlassian.net/browse/FTFL-698)_

_Endpoint: `fitfiletest.grafana.net` (context `fitfiletest`, datasources `grafanacloud-prom`/`grafanacloud-logs`). All queries run 2026‑07‑14, ~09:00–09:15 UTC (unix ts ≈1784019848–1784020165)._

### 1. Dashboards—live/scraping Status

| Dashboard (ticket's known list) | Found? | Live/scraping evidence |
|---|---|---|
| ArgoCD | Yes (2 copies: `LCAgc9rWz`, `qPkgGHg7k`) | `up{job=~"argocd-.*"}`: server/repo-server/appset/application-controller = 1. `argocd-dex-server` = 0 on both staging and testing (sustained, not a blip) |
| FF Data Audit | Yes (`bdbhaonrk3c3ke`) | Backed by live Postgres/Mongo series (below) |
| FF Data Audit Copy | Yes (`bdbzle30qtcsgd`) | Same as above—appears to be a duplicate, cleanup candidate |
| Incident Insights | Yes (`da459d5e-…`) | Grafana IRM built-in, not Prometheus-scrape dependent |
| Kubernetes CPU and Memory Rightsizing | Yes (`olwtxsd`) | `container_cpu_usage_seconds_total`/`container_memory_working_set_bytes` = 457 series each, current |
| MinIO Dashboard | Yes (`TgmJnqnnk`) | `up{job=~".*minio.*"}` = 1 (dev, ff-test-a, sandbox-testing-1) |
| MongoDB | Yes (`ddyabd43znsowa`) | `up{job=~".*mongodb.*"}` = 1; live WiredTiger checkpoint logs in Loki |
| MongoDBa | Yes (`AyWQt9jWk`) | Same backing series |
| OnCall Insights | Yes (`f9fe4233-…`) | Grafana IRM built-in |
| Platform Metrics for Invoicing | Yes (`ol8wjsv`) | Not independently spot-checked panel-by-panel; underlying container/DB series it would draw on are live |
| Platform Monitoring (old - to be deleted) | Yes (`ya6wtdr`) | Still exists—matches ticket's own note that it's a deprecated dashboard; no scrape gap, just needs deleting |
| Simple Streaming Example | Yes (`TXSTREZ`) | Grafana demo dashboard, not scrape-dependent |
| Trivy Operator - Vulnerabilities | Yes (`security_trivy_operator`) | `up{job="trivy-operator"}` = 1 |
| Alloy / Cluster Overview | Yes (`3a6b7020…`) | No data: `cluster_node_info` and `cluster_node_peers` (the two series its panels query) return empty result sets |
| Integration - Alloy Health | Partial | No dashboard with this exact title; folder `integration---alloy-health` holds 7 Alloy dashboards (Cluster Overview, Cluster Node, Logs Overview, OpenTelemetry, Controller, Resources, Prometheus Components). `alloy_component_controller_running_components` and all `alloy_*` series return empty |

Extra dashboards found, not in the ticket's known list: `ArgoWorkflow Metrics` (`Qcsy6bx7z`), Kubescape, Argo CD - Essential Monitoring, Kubernetes Monitoring Cardinality, Kubernetes Pod Health Dashboard (Simple), (Home) Kubernetes Integration, standard `kubernetes-mixin` dashboards (Compute Resources / Node / Pod / Namespace / Workload / Cluster / Persistent Volumes), and Grafana Cloud's own Usage Insights / Cardinality Management / Billing dashboards.

Down-target sweep—`up == 0` (instant, whole org): 5 series down, all in two jobs, sustained over the last 2h (not transient):

- `argo-workflows-workflow-controller`, endpoint `telemetry` (port 8081)—down on all 3 clusters (staging, testing, sandbox-testing-1). The `metrics` endpoint (port 9090) on the same pods is up=1 throughout—this is the actual Prometheus metrics port and it's healthy. Port 8081 looks like a stray/misconfigured OTel scrape target, not a loss of controller observability.
- `argocd-dex-server`—down on staging and testing.

Alloy component health: cannot be confirmed via `Integration - Alloy Health` or `alloy_component_controller_running_components`—see gap above. Indirect evidence Alloy itself is functioning: it is clearly the agent shipping cadvisor/kubelet/kube-state-metrics, postgres/mssql/mongo/minio exporter metrics, and container logs to Loki (all confirmed live below)—Alloy's own self-telemetry just isn't wired up.

### 2. Metrics Coverage Matrix

| Family | Metric | Status | Evidence (PromQL) |
|---|---|---|---|
| System/container | CPU usage | Present | `container_cpu_usage_seconds_total` → 457 series |
| | CPU throttling | Absent | `container_cpu_cfs_throttled_seconds_total` → 0 series |
| | Memory working set | Present | `container_memory_working_set_bytes` → 457 series |
| | OOM kills | Present | `kube_pod_container_status_last_terminated_reason{reason="OOMKilled"}` → 3 series (`container_oom_events_total` absent, but not needed) |
| | Disk IOPS | Present | `container_fs_reads_total` / `container_fs_writes_total` → 352 series each |
| | Disk I/O time/latency | Absent | `container_fs_io_time_seconds_total` → 0 series |
| | Network throughput | Present | `container_network_receive/transmit_bytes_total` → 337 series each, carries both `node` and `pod` labels |
| | Cross-node bandwidth | Partial | No CNI flow metric (`hubble_*`/`cilium_*` → 0 series). Can approximate via `sum by (node) (container_network_*_bytes_total)`, but there's no true node-pair flow metric |
| Database (Postgres) | Exporter present | Present (contradicts prior-memory assumption) | `pg_up` on 4 jobs: `dev-`, `thehyve-`, `sandbox-testing-1-`, `ff-test-a-databases-postgresql-metrics`, all =1 |
| | Active connections | Present | `pg_stat_activity_count` |
| | Query runtime (p50/95/99) | Absent | No `pg_stat_statements_*` series—extension not exposed by the exporter |
| | Long-running-tx proxy | Present (partial) | `pg_stat_activity_max_tx_duration` (proxy only, not a real percentile histogram) |
| | Lock waits | Present (partial) | `pg_locks_count` (lock counts by mode; no explicit wait-time histogram) |
| | Buffer-cache hit ratio | Present (computable) | `pg_stat_database_blks_hit` / `(blks_hit + blks_read)` |
| | Slow-query log | Absent currently | `pg_settings_log_min_duration_statement_seconds` = ‑1 (disabled) on dev/sandbox-testing-1/ff-test-a; = 5s on thehyve (not the 500ms target); no `duration:` lines seen in Loki over 1h |
| Database (MSSQL) | Exporter present | Present | `mssql_up` = 1, job `dev-mssql` (testing cluster) |
| | Connections/batch reqs | Present | `mssql_connections`, `mssql_batch_requests` |
| | Deadlocks | Present | `mssql_deadlocks` |
| | I/O latency proxy | Present | `mssql_io_stall`, `mssql_io_stall_total` |
| | Query Store / query-level runtime | Absent from Prometheus | Not exporter-visible; must be checked via T‑SQL directly (Step 3) |
| Workflow (FITFILE-specific) | Argo controller operational health | Present | `argo_workflows_*` (queue depth/latency, operation duration, workflow_condition, pod counts)—generic controller instrumentation only |
| | Run ID / scenario coordinates (C,S,E,P,X,L) | Absent | No matching series (`.*scenario.*|.*run_id.*` matched only an unrelated MongoDB internal metric) |
| | Stage timings | Absent | No matching series |
| | Rows scanned/returned | Absent | No matching series |
| | Error taxonomy | Absent | No matching series beyond generic `argo_workflows_error_count` (controller errors, not workflow business-logic errors) |

### 3. Slow-query Logging Status

Could not be verified or applied directly—this environment has no working DB access: `psql`/`sqlcmd` aren't installed, and `kubectl` (context `fitfile-cloud-staging-aks-cluster`) is unauthenticated (`the server has asked for the client to provide credentials`). Documented rather than escalated to get credentials, per decision made during this investigation.

Before-state, inferred from Prometheus/Loki (not a substitute for the actual `SHOW`/`sys.database_query_store_options` checks):

| Target | Setting | Inferred value | Evidence |
|---|---|---|---|
| Postgres—dev, sandbox-testing-1, ff-test-a (staging) | `log_min_duration_statement` | Disabled (‑1) | `pg_settings_log_min_duration_statement_seconds` |
| Postgres—thehyve | `log_min_duration_statement` | 5000ms (not 500ms target) | same metric = 5 |
| Postgres—all | `shared_preload_libraries` (pg_stat_statements, auto_explain) | Unknown—not exporter-visible | No `pg_stat_statements_*` series exist, which is consistent with it not being loaded, but this isn't conclusive without `SHOW shared_preload_libraries` |
| Postgres—all | Corroborating signal | Consistent with disabled | No `duration:` log lines in Loki over the last hour; postgres stdout logging pipeline itself is confirmed working (checkpoint logs present) |
| MSSQL—dev-mssql (testing) | Query Store state | ~~Unknown~~ Confirmed ON (`READ_WRITE`, `AUTO` capture)—see §3a | No Prometheus-visible proxy for this; verified via direct `sqlcmd` 2026-07-14 |

After-state: not applied. The verify/apply SQL from the ticket is unchanged and ready to hand off:

```sql
-- Postgres verify
SHOW shared_preload_libraries;
SHOW log_min_duration_statement;
-- Postgres apply (requires restart)
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements,auto_explain';
ALTER SYSTEM SET log_min_duration_statement = 500;
ALTER SYSTEM SET auto_explain.log_min_duration = 500;
ALTER SYSTEM SET auto_explain.log_analyze = true;

-- MSSQL verify
SELECT actual_state, actual_state_desc, query_capture_mode_desc FROM sys.database_query_store_options;
-- MSSQL apply
ALTER DATABASE CURRENT SET QUERY_STORE = ON;
ALTER DATABASE CURRENT SET QUERY_STORE (QUERY_CAPTURE_MODE = AUTO);
```

Note `shared_preload_libraries` changes require a Postgres restart—whoever runs this should treat it as a change-managed, restart-incurring action, not a live reload.

### 3a. Rerun—Direct DB Verification 2026-07-14 (~09:15–09:29 UTC)

Staging cluster login (`fitfile-cloud-staging-aks-cluster`) is now authenticated; `fitfile-cloud-testing-aks-cluster` turned out to be authenticated too (same Azure session). `az aks list` confirms only these two clusters exist under the current subscription (`FITCloud Non-Production`)—`dev` and `sandbox-testing-1` are separate `k8s_cluster_name` values in Prometheus that do not correspond to AKS clusters reachable from this session (not in `az aks list`, not in other subscriptions checked: Production, Shared Services, Management, Identity, Testing, FitFile, NNUHFT-SDE—did not exhaustively search all of these for a third cluster, stopped once staging+testing access answered the ticket's actual ask). Ran `psql`/`sqlcmd` directly via `kubectl exec`, superseding the Prometheus-inference in section 3 for the instances actually reached.

Postgres—directly verified (3 of 5 instances):

| Instance | Cluster | `log_min_duration_statement` | `shared_preload_libraries` | `pg_stat_statements` installed? |
|---|---|---|---|---|
| `ff-test-a-databases-postgresql-0` | staging | -1 (disabled) | `pgaudit` only | No |
| `dev-postgresql-0` | testing | -1 (disabled) | `pgaudit` only | No |
| `thehyve-postgresql-0` (ns `thehyve-test`) | staging | -1 (disabled) | `pgaudit` only | No |

All three confirm the report's inference exactly—disabled, no `pg_stat_statements`/`auto_explain` loaded. This upgrades those cells from "inferred" to "confirmed."

Note on `thehyve-postgresql-0`, ns `thehyve-test` (staging) vs the `thehyve` job in section 3: these are different pods. Re-querying Prometheus live confirms the `thehyve` job showing `5` (not `-1`) is `thehyve-postgresql-0` in `namespace=thehyve`, `k8s_cluster_name=sandbox-testing-1`—a third, distinct cluster this session cannot reach. The `thehyve-test` pod I _could_ reach (staging cluster) is an unrelated instance that happens to share a name pattern; it was not the one section 3 was inferring about. So the "5000ms, not 500ms target" finding for the real `thehyve` job is still unverified directly—inference stands, cluster still unreachable.

Also unreachable directly for the same reason: `sandbox-testing-1-postgresql-0` (cluster `sandbox-testing-1`)—Prometheus still shows `-1`, consistent with the original inference, but not confirmed via `SHOW`.

MSSQL—directly verified, and this changes the recommendation:

`dev-mssql-0` (testing cluster, namespace `testing`) reached via `sqlcmd` (`/opt/mssql-tools18/bin/sqlcmd`, present in the image). Only user database is `OMOP`.

```
SELECT actual_state, actual_state_desc, query_capture_mode_desc FROM sys.database_query_store_options;

actual_state  actual_state_desc   query_capture_mode_desc
2             READ_WRITE          AUTO
```

Query Store is already ON and capturing (AUTO mode) on `dev-mssql`/`OMOP`. This was previously "Unknown—needs `sys.database_query_store_options`" in section 3—it's now confirmed good, not a gap. No apply action needed on the MSSQL side.

Not applied: the Postgres `ALTER SYSTEM` fix from section 3 was not run against `ff-test-a` or `dev` in this session—confirming state, not changing it, was the ask. Flagging it as ready to run since DB access now exists; say the word and I'll run it (staging `ff-test-a` and testing `dev` are both writable from here), but it's a restart-incurring change so I'd want explicit go-ahead per instance rather than doing it opportunistically.

### 3b. Addendum—gap 1 Partially Revised (2026-07-14, via [[Sandbox Cluster Dashboard Plan 2026-07-14]])

Follow-up work on the `sandbox-testing-1` cluster (`aks-ff-uks-gp-1`) found that `ffcloud-service` already emits structured `WorkflowInstanceStarted`/`Completed`/`Failed` audit events to Loki, with `instanceId`, `workflowName`, `stageName`, pre-computed `duration`, and (on `Failed`) the full error text naming the failing task step. This was missed in section 2 because that pass only checked Prometheus/PromQL (`.*run_id.*`/`.*scenario.*` series), not Loki/LogQL.

Net effect on gap 1: run ID, stage timings, and error taxonomy are not absent—they exist today as logs and just need a Loki-backed dashboard, not new instrumentation. What's still genuinely missing: rows scanned/returned isn't in these events, and none of it is in Prometheus as metrics (so PromQL-only tooling, alerting on numeric thresholds, etc. still can't see it without a log-to-metric bridge). See the linked plan doc §3.3 for detail. Downgrades gap 1 from "blocks Phase 2, needs code instrumentation" to "partially covered by a dashboard build; rows-scanned/returned is the remaining real gap."

### 4. Gaps Found

| # | Gap | Blocks Phase 2? | Bespoke panel justified? |
|---|---|---|---|
| 1 | No FITFILE workflow-run metrics (run ID, C/S/E/P/X/L, stage timings, rows scanned/returned, error taxonomy) | Yes—this is the core observability the harness needs to judge scenario runs | Not a panel problem—the metrics don't exist yet. Needs instrumentation added to the workflow/harness code (emit custom Prometheus metrics or structured logs with these fields), then a panel. Panel work is downstream of instrumentation, not a substitute for it. |
| 2 | Postgres slow-query logging disabled (or set too high on thehyve) and `pg_stat_statements`/`auto_explain` unconfirmed; MSSQL Query Store unconfirmed | Yes—Step 3 deliverable is unmet, and without this you have no query-level diagnostic trail for slow scenarios | No—this is a DB config change, not a dashboard gap |
| 3 | No dedicated Postgres/MSSQL dashboard, despite exporters existing and exposing good data | No | Deferred—existing `pg_*`/`mssql_*` series can be explored ad hoc via Explore in the interim; a proper dashboard is a nice-to-have, not a blocker |
| 4 | CPU throttling (`container_cfs_throttled_seconds_total`) and disk I/O time/latency metrics absent | No | No—flag as a monitoring config gap (cAdvisor should expose these; likely a metric-relabel/keep-list drop in the Alloy config), fix at the collector config level |
| 5 | No true cross-node bandwidth (node-pair) metric, only per-node aggregate | No | No—would need CNI-level flow metrics (Hubble/Cilium), out of scope for Phase 2 |
| 6 | Alloy self-observability (`Alloy / Cluster Overview` and the whole `integration---alloy-health` folder) has zero data | No—everything Alloy ships downstream (k8s, DB, log data) is confirmed live by other means | No—this is an Alloy self-monitoring config gap, not something a bespoke panel fixes |
| 7 | `argo-workflows-workflow-controller` `telemetry` endpoint (8081) and `argocd-dex-server` down org-wide | No | No—likely a stray/misconfigured scrape target; worth a ticket to clean up, doesn't affect the metrics you actually need |
| 8 | Duplicate dashboards (ArgoCD ×2, FF Data Audit + Copy, MongoDB/MongoDBa) and a marked-deprecated dashboard still present | No | No—housekeeping |

### 5. Recommendation (Updated after 3a rErun)

No-go on Phase 2 from a monitoring-readiness standpoint, but now only on gap 1, plus a narrowed version of gap 2:

1. There is no workflow-run-level telemetry (run ID, scenario coordinates, stage timings, rows scanned/returned, error taxonomy) anywhere in Prometheus. Without this, you can't actually judge scenario runs from the monitoring stack—this needs to be instrumented in the harness/workflow code before Phase 2 starts generating runs you'd want to analyse. Unchanged by this rerun.
2. Slow-query logging—MSSQL side is now resolved: Query Store is confirmed ON (`READ_WRITE`, `AUTO` capture) on `dev-mssql`/`OMOP`, verified directly via `sqlcmd`. Postgres side is still open: `log_min_duration_statement` is confirmed disabled (`-1`) via direct `psql` on `ff-test-a` (staging) and `dev` (testing); `pg_stat_statements`/`auto_explain` are confirmed not loaded on either. The `thehyve` (5000ms) and `sandbox-testing-1` (-1) instances live on a cluster (`sandbox-testing-1`) not reachable from this Azure session—still inference-only, not directly confirmed. The verify/apply SQL from section 3 is unchanged and is now runnable against `ff-test-a` and `dev`—not run yet, pending go-ahead since it's restart-incurring.

Everything else—system/container CPU/memory/disk/network, both DB exporters, dashboard scrape health, and the log pipeline—is confirmed live and adequate for Phase 2. None of gaps 3–8 should block a go decision; they're either deferred nice-to-haves or unrelated hygiene items.

Next steps: (a) decide whether to apply the Postgres `ALTER SYSTEM` fix to `ff-test-a` and `dev` now that write access exists (restart required—needs a go/no-go, not just DB creds), (b) get access to the `sandbox-testing-1` cluster (or someone who has it) to verify/fix `thehyve` and `sandbox-testing-1` Postgres instances the same way, (c) scope the workflow-run metrics instrumentation as its own piece of work—that's a code change in the harness, not something Grafana/Prometheus config can supply.
