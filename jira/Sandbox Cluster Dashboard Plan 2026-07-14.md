---
created: 2026-07-14T09:50:00+00:00
modified: 2026-07-14T10:12:32+00:00
permalink: llmeon/sandbox-cluster-dashboard-plan-2026-07-14
tags: [1]
title: Sandbox Cluster Dashboard Plan 2026-07-14
type: note
---

## Sandbox Cluster (`aks-ff-uks-gp-1`)—Dashboard & Stress-Test Monitoring Plan

_Follows [[FTFL-698 Monitoring Gap Report 2026-07-14]]. Triggered by Ollie's dashboard notes + confirmation this is the cluster we currently care about. All live data pulled 2026-07-14 ~09:40–09:46 UTC._

### 1. Cluster Snapshot

`aks-ff-uks-gp-1`, resource group `rg-ff-uks-gp-net`, subscription Testing (`7bbc8ae5-…`), region `uksouth`. Private cluster—no public API FQDN, not reachable by plain `kubectl` from this machine (DNS for the private FQDN doesn't resolve off-network). Reachable via `az aks command invoke` instead, which proxies commands through the Azure control plane—that's how everything below was gathered. Worth setting up proper access (VPN/private-link peering, or a jumpbox) if this cluster is going to be worked in regularly; `command invoke` is a fine stopgap but slow and non-interactive (no `kubectl exec -it`, no port-forward).

K8s 1.34.7, Free tier, `azureMonitorProfile.metrics.enabled: false` (Azure Managed Prometheus is off—matches what's actually running: a self-hosted Grafana Alloy stack, same pattern as staging/testing). `metricsProfile.costAnalysis.enabled: false`—the built-in AKS Cost Analysis add-on is off, relevant to Ollie's cost-per-node-pool ask below.

Node pools:

| Pool | VM size | Autoscale | Taint | Currently running |
|---|---|---|---|---|
| `system` | Standard_D2as_v7 | 1–1 (fixed) | `CriticalAddonsOnly=true:NoSchedule` | 1 node |
| `fitfile` | Standard_D4as_v7 | 1–1 (fixed) | none | 1 node |
| `workflows` | Standard_E4as_v7 | 0–10 | `dedicated=workflows:PreferNoSchedule` + `scalesetpriority=spot:NoSchedule` (Spot) | 2 nodes (live) |
| `omopdb` | Standard_E4as_v7 | 0–1 | `dedicated=omopdb:NoSchedule` | 0 nodes—no `omopdb` namespace exists on this cluster right now. Provisioned but unused. |

The `workflows` pool is Spot-priced and autoscales 0→10—this is the pool Ollie's cost-tracking idea is really about, and the one worth watching under stress-test load since it's where the compute actually happens (see below).

### 2. What's Actually Running Right now (Ground tRuth, not aSsumptions)

Namespace `sandbox-testing-1` holds the full FITFILE stack: `ffcloud-service`, `fitconnect-ftc`, `frontend`, `minio`, `mongodb` (+ arbiter), `postgresql`, `workflows-api`. Also present on this cluster: `thehyve-postgresql-0`, `spicedb` (+ its own Postgres), and a `terraform` namespace running TFC agents.

There is a live stress-test workflow running right now: `100k-patients-single-source-privacy-on-1-workflow-6mwvz`, `Running`, 16h old, two `custom-transformation` pods each pulling ~1 CPU and up to 4.6GB memory. A `privacy-off` sibling run already `Succeeded` 17h ago. Five other runs (`my-omop-workflow-mon-jul-13-2026-*`) all Failed, each on a `run-sql…` task step within 2–4 minutes.

Load distribution during the running stress test, from `kubectl top`:

| Node/pod | CPU | Memory |
|---|---|---|
| `aks-workflows-…001f` | 1078m (27%) | 6.2Gi (20%) |
| `aks-workflows-…001g` | 1091m (28%) | 2.9Gi (9%) |
| `sandbox-testing-1-postgresql-0` | 5m | 48Mi |

The app-level Postgres is essentially idle during this run—`pg_stat_activity` showed 1 backend, no active queries; `pg_stat_database` showed 316 commits total, 0 temp files, 0 deadlocks, cache hit ratio ~99%. The compute-heavy part of a "100k patients" run is happening inside the `custom-transformation` workflow containers, not as SQL pushed to this Postgres instance. `\l` on that instance shows only `argoworkflows`, `ffcloud`, `fitconnect`, `spicedb`—no OMOP/CDM database lives here.

Open question worth putting to Ollie/whoever owns the workflow definitions: where does the actual bulk clinical-data / "big query" load land? The failed runs died on a `run-sql` task, which implies at least some workflows do push real SQL somewhere—but not to any Postgres instance on this cluster showing meaningful load. Candidates: an external/managed OMOP CDM DB not on this cluster, MongoDB (which does show more baseline activity), or the SQL happens against files staged in MinIO via DuckDB/similar in-process rather than a server. Worth confirming before building "database load" panels aimed at the wrong instance.

### 3. Ollie's dashboards—grounded against what Exists Today

3.1 Database metrics—CPU, Memory, Storage

Standard cAdvisor panels (`container_cpu_usage_seconds_total`, `container_memory_working_set_bytes`, PVC usage via `kubelet_volume_stats_*`), filtered to Postgres/MongoDB/MinIO pods. Nothing missing—build straight away. Confirmed live per [[FTFL-698 Monitoring Gap Report 2026-07-14]] section 2 on the staging/testing clusters; same exporters/agent pattern is running here.

3.2 Workflow metrics—per-container + whole-workflow overview

Two layers:

- _Container level_: cAdvisor again, grouped by the labels Argo stamps on workflow pods (`workflows.argoproj.io/workflow`, `workflows.argoproj.io/node-name` or similar—confirm exact label set with `kubectl get pod <workflow-pod> --show-labels`, didn't verify the precise label key names in this session). This gets you per-step CPU/memory, which is what showed the `custom-transformation` steps as the actual hot spot above.
- _Whole-workflow overview_: `argo_workflows_*` controller metrics (queue depth, operation duration, pod counts)—confirmed present in FTFL-698. This is controller-level health, not business-outcome level—pairs with 3.3 below for the actual "did this run go well" answer.

3.3 Query overview—correlate Started/Completed/Failed events

This is already fully buildable, today, from existing data—and it changes a conclusion in [[FTFL-698 Monitoring Gap Report 2026-07-14]] (gap 1, "run ID / stage timings / error taxonomy—absent"). That report only checked Prometheus metrics via PromQL. It didn't check Loki. Checking Loki now:

`ffcloud-service` already emits structured JSON audit-log events for exactly this—`WorkflowInstanceStarted`, `WorkflowInstanceCompleted`, `WorkflowInstanceFailed` (source: `/app/services/events/LogAuditor.js`), confirmed live in the last 24h on this cluster. Sample fields:

- Started: `payload.instanceId`, `payload.workflowName`, `payload.userflow.stageName`, `payload.userflow.entrypointId`
- Completed: same, plus `payload.duration` (ms)—already pre-computed, no correlation math needed
- Failed: same, plus `payload.duration`, `payload.nodeId`, and `payload.error`—the full error text, e.g. `Error in workflow task "run-sql3994c593-…": main: Error (exit code 1)`, naming the exact failing step

So Ollie's "correlate Started with Completed/Failed to get duration" is actually a non-problem—`Completed`/`Failed` events already carry `duration`. A LogQL-based dashboard can:

- Table/count panel of `WorkflowInstanceStarted` vs `Completed` vs `Failed` by `payload.workflowName`, to get success rate
- Histogram/heatmap of `payload.duration` by `payload.workflowName` or `payload.userflow.stageName` (Loki supports `| json | unwrap payload_duration` style metric queries)
- Failed-run table with `payload.error` for a live error taxonomy—group by the task-name prefix inside the error string (e.g. `run-sql`) to get a taxonomy for free without new instrumentation
- `DistributedWorkflowInstance.entityId` in the `scopes` block is the correlation key (= `payload.instanceId`) if you want to trace one run end-to-end across events

This should go back into FTFL-698 as a correction, not just live here—worth a short addendum on that report noting gap 1 is a Loki/dashboard task, not a code-instrumentation task, for the workflow-level view. (Stage-level _rows scanned/returned_ isn't in these events though—that part of gap 1 still stands; these audit events cover run/stage timing and errors, not row counts.)

3.4 FITFILE system metrics—FFCloud, FITConnect, MinIO, MongoDB CPU/Mem/Storage

Same mechanism as 3.1, just a different pod filter. All four confirmed live and scraping in FTFL-698 §1/§2. No gap.

3.5 Cost of workflows node pool

Ollie's proposed method (node uptime × VM\_Size hourly cost) works, with one wrinkle: the `workflows` pool is Spot priority, so its hourly cost isn't a fixed number—Azure Spot pricing floats with capacity/region. Two options:

- Turn on the AKS Cost Analysis add-on (`metricsProfile.costAnalysis.enabled`, currently `false`)—gives a native per-node-pool cost breakdown in the Azure portal without building this by hand. Cheapest to implement, but it's an Azure Cost Management view, not a Grafana panel—decide whether "in Grafana" is a hard requirement.
- Build it as described: node uptime from `kube_node_created`/`kube_pod_start_time` (kube-state-metrics, already present), multiplied by VM\_Size rate pulled from the Azure Retail Prices API (`prices.azure.com`) filtered to Spot + `Standard_E4as_v7` + `uksouth`—that API returns current Spot price, not a static number, so the multiplier needs to be a live/periodic query too, not a hardcoded constant, or the number will silently drift wrong.

3.6 Workflows node pool total usage—CPU, Memory, local storage

Same cAdvisor/node-exporter metrics as 3.1, summed with `node=~"aks-workflows-.*"` (or a `agentpool="workflows"` label if kube-state-metrics exposes it—confirm). No gap, straightforward.

### 4. Stress-testing & "How well is the DB hAndling bIg queries"—research

The live "100k patients" run above showed the app Postgres barely moving. Before building dashboards aimed at "database load," it's worth being deliberate about _which_ system actually bears the load for a given workflow, and instrumenting that one. Below is what each engine in the stack can expose, ranked by usefulness for diagnosing big-query/bulk-load stress specifically (not general uptime monitoring, which §3.1/3.4 already covers).

Postgres—the single biggest gap is `pg_stat_statements`, confirmed not loaded anywhere (see [[FTFL-698 Monitoring Gap Report 2026-07-14]] §3a). Without it there's no per-query runtime/row-count breakdown at all, on any instance, staging or sandbox. This is the top recommendation if "big query" performance on Postgres is a real concern:

- `pg_stat_statements`—total/mean exec time, calls, rows, shared\_blks\_hit/read per normalized query. This is the thing that actually answers "which query is slow and how slow."
- `auto_explain` (log\_min\_duration threshold)—captures the real query plan for anything over the threshold, without needing to reproduce manually. Already scoped as part of the Step 3 fix in FTFL-698.
- `pg_stat_activity.wait_event_type`/`wait_event`—live, right now, no config change needed. Distinguishes lock waits from I/O waits from CPU-bound execution during a big query.
- `pg_stat_database.temp_files`/`temp_bytes`—non-zero means queries are spilling sort/hash work to disk because `work_mem` is too small for the query—a classic big-query symptom, and a single number worth alerting on.
- `pg_locks`—blocking-chain detection under concurrent load.
- `pg_stat_progress_copy` / `pg_stat_progress_create_index`—live progress bars for bulk loads and index builds, exactly the shape of operation a 100k-patient import would trigger if it does land in Postgres.
- `pg_stat_wal`—WAL bytes/records generated; spikes here confirm a genuinely write-heavy bulk operation is happening even if `pg_stat_activity` looks quiet in a point-in-time check.

MongoDB—showed more baseline activity than Postgres in the FTFL-698 pass, worth checking first if this is where the bulk data actually lands:

- `db.currentOp()` / `$currentOp`—long-running ops live.
- Profiler (`system.profile`, threshold-based)—Mongo's slow-query log equivalent; not yet confirmed enabled anywhere, worth checking (`db.getProfilingStatus()`).
- WiredTiger cache: bytes currently in cache vs configured max—cache-eviction pressure is the primary big-dataset stress signal for Mongo, more so than raw CPU.
- `$indexStats`—catches collection scans on large collections, i.e. queries that should be using an index for a 100k-patient dataset and aren't.
- Checkpoint duration—already confirmed visible in Loki per FTFL-698 §1.

MSSQL (`dev-mssql`, testing cluster—not present on this sandbox cluster, but relevant if OMOP CDM queries land there instead):

- Query Store—confirmed already ON, `AUTO` capture, per FTFL-698 §3a rerun. No setup needed, just needs a dashboard pulling from it.
- `sys.dm_os_wait_stats`—aggregate wait-type breakdown (`PAGEIOLATCH_*` = disk-bound, `CXPACKET`/`CXCONSUMER` = parallelism contention)—the standard first move for "why is this big query slow."
- `sys.dm_db_index_physical_stats`—fragmentation on large tables, relevant at 100k-patient scale.
- tempdb `PAGELATCH` contention—classic large-analytical-query symptom on SQL Server.

MinIO—worth including since the workflow does file-based staging: `minio_s3_requests_total`, `minio_bucket_usage_total_bytes`, and MinIO's request-duration histograms give a throughput ceiling for the data-extract stage—useful to rule out "object storage was the bottleneck" separately from DB or compute.

Stress-testing approach—don't bolt on synthetic benchmarks before using what's already happening:

The `100k-patients-*` Argo workflows already _are_ a real, representative stress test, running today, with real duration/error telemetry (§3.3). The highest-value next step is wiring dashboards to that existing signal rather than introducing a separate synthetic load tool first. If a DB-only benchmark is later wanted in isolation from the app layer:

- `pgbench` (Postgres-native)—supports custom `-f` scripts, can replay realistic query shapes instead of just the default TPC-B-like workload.
- HammerDB—supports Postgres, MSSQL and MongoDB, has TPC-H (analytical/big-query pattern) as well as TPC-C (OLTP)—closer to this workload's shape than pgbench's default.
- k6/Locust—app/API-level load, for driving FFCloud/workflow endpoints directly if the goal is end-to-end rather than DB-only.

One more thread worth pulling rather than rebuilding: a couple of the Loki log lines already carry `trace_id`/`span_id` (seen on the `distributed_workflow_instance_invalid` log)—meaning OTel tracing is at least partially wired up in `ffcloud-service`. If DB client calls are captured as spans too, that gives a direct pivot from "this `WorkflowInstanceCompleted` event was slow" straight to the DB span that caused it, without needing to hand-correlate timestamps across systems. Worth checking what backend those traces go to (Tempo? nothing yet?) before assuming this needs building from scratch.

### 5. Recommended next Steps, Roughly in order

1. Confirm with Ollie/workflow owners where the actual "big query" load lands for a 100k-patient run—the app Postgres on this cluster isn't it (§2). Don't build DB-load panels against the wrong instance.
2. Build the workflow Started/Completed/Failed Loki dashboard (§3.3) first—it's zero-instrumentation, data already exists, and it's the one Ollie framed as needing correlation work that turns out not to be needed.
3. Enable `pg_stat_statements` + `auto_explain` per the FTFL-698 Step 3 SQL, on whichever Postgres instance turns out to be the real target from step 1.
4. Standard cAdvisor dashboards for §3.1/3.4/3.6—no blockers, can be done in parallel with the above.
5. Decide AKS Cost Analysis add-on vs hand-rolled Spot-price panel for §3.5—the add-on is a five-minute enable if an Azure-portal view is acceptable; the Grafana-native version needs a live pricing-API pull, not a static number.
