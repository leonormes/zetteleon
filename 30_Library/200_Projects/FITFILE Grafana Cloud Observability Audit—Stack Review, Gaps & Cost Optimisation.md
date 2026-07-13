---
created: 2026-06-05T08:50:57+00:00
modified: 2026-07-13T08:44:38+00:00
permalink: llmeon/30-library/200-projects/fitfile-grafana-cloud-observability-audit-stack-review-gaps-cost-optimisation
project_category: refined_deployment
project_name: Refined Deployment
project_status: active
title: FITFILE Grafana Cloud Observability Audit—Stack Review, Gaps & Cost Optimisation
type: null
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Friday Jun 5, 2026 - 9:50 AM_
---

Now I have everything needed. Here is the full synthesis.

---

## FITFILE Grafana Cloud Observability Audit—Stack Review, Gaps & Cost Optimisation

_Based on `/Volumes/DAL/Zettelkasten/LLMeon/00_Inbox/2026-06-05-fitfile-loki-prometheus-cardinality-audit.md` and live Grafana Cloud research (June 2026)._

---

## 1. Your Current Stack (What the Audit Found)

The `fitfiletest` Grafana Cloud instance (`https://fitfiletest.grafana.net`) uses the following confirmed components:

| Layer | Tool | Status |
|---|---|---|
| Metrics | Prometheus / Mimir (via `grafana-k8s-monitoring` Helm) | ✅ Active—but high-cardinality crisis |
| Logs | Loki (via Alloy collector, k8s-events + pod logs) | ✅ Active—but index bloat severe |
| Collector | Grafana Alloy (formerly Grafana Agent) | ✅ Active |
| Kubernetes observability | `grafana-k8s-monitoring` Helm chart | ✅ Active |
| Adaptive Telemetry APIs | Adaptive Logs + Adaptive Metrics | ⚠️ Blocked—expired API token (`401 Unauthorized`) |
| Distributed Tracing | Tempo | ❌ Not mentioned—absent from audit |
| Continuous Profiling | Pyroscope / Grafana Cloud Profiles | ❌ Not mentioned—absent |
| Frontend / RUM | Faro | ❌ Not mentioned—absent |
| Synthetic Monitoring | Grafana Synthetic Monitoring | ❌ Not mentioned—absent |
| Load Testing | k6 Cloud | ❌ Not mentioned—absent |
| Incident Response | Grafana IRM / OnCall | ❌ Not mentioned—absent |
| SLOs | Grafana SLO | ❌ Not mentioned—absent |
| Alerting | Grafana-Managed Alerting (GMA) | ❓ Unknown—not mentioned |

Clusters audited: `ollie`, `testing`, `yasir` (test). `fitfileprod` was not configured in `gcx config`—prod audit is deferred and outstanding.

---

## 2. Full Grafana Cloud Product Surface (What They Offer)

### Core LGTM+P Stack

- Mimir—managed Prometheus-compatible metrics backend ($6.50 / 1k active series on Pro)
- Loki—managed log backend with Adaptive Logs ($0.05/GB process + $0.40/GB write + $0.10/GB retain)
- Tempo—managed distributed tracing backend, OpenTelemetry-native (same pricing structure as Loki)
- Pyroscope / Grafana Cloud Profiles—continuous profiling (CPU, memory, heap); Pyroscope 2.0 released April 2026 with native OTLP ingestion and dramatically improved storage cost; same pricing model as Loki/Tempo

### Frontend & Synthetic

- Faro—Real User Monitoring (RUM) for web apps: browser errors, performance, sessions ($0.75 / 1k sessions)
- Synthetic Monitoring—HTTP, DNS, TCP probes from Grafana's global probe network

### Performance Testing

- k6 Cloud—managed load testing, now integrates directly with Pyroscope for flame-graph correlation under load ($0.15 / VU hour Pro; as low as $0.05 Enterprise)

### Incident & Reliability

- Grafana IRM (OnCall)—alert routing, on-call schedules with working hours, maintenance windows (silence/group/disable modes), Slack-native incident workflows ($20 / active IRM user / month)
- Grafana SLO—burn-rate alerting that feeds into IRM; tightly coupled with GMA
- Grafana-Managed Alerting (GMA)—now the default on new stacks; routes into IRM

### Platform & Intelligence

- Kubernetes Monitoring—turnkey K8s observability solution ($0.01 / host hour + $0.0007 / container hour)
- Application Observability—APM-style service maps, RED metrics, OTel-native ($0.025 / host hour)
- Database Observability—deep DB query analysis ($0.07 / host hour)
- Adaptive Telemetry suite—Adaptive Metrics, Adaptive Logs, Adaptive Traces, Adaptive Profiles (usage-based intelligence across all pillars)
- Fleet Management—Alloy pipeline management with no-code component editor
- Grafana AI Assistant + Investigations—AI assistant with agentic incident investigation ($20 / active AI user / month, 40M tokens included)
- Grafana Cloud Cost Management Hub—cost attribution by team/service, DPM dashboards

---

## 3. Stack Gaps—What You're Missing

### 🔴 Critical Gaps

Distributed Tracing (Tempo)

Tempo is completely absent. You have no request-level visibility across services (ArgoCD, SpiceDB, MongoDB, Tigera are all visible in your logs—none of their traces are correlated). For a Kubernetes-native stack with gRPC services (SpiceDB's `grpc.service` / `grpc.method` fields are in your log body, suggesting active RPC traffic), this is a major blind spot. Without traces:

- You cannot distinguish a slow downstream call from a local processing bottleneck
- Distributed root-cause analysis requires manual log correlation instead of trace-driven drilling

Continuous Profiling (Pyroscope)

No profiling instrumentation is present. Combined with the k6 integration (if you adopt load testing), Pyroscope 2.0's OTLP support means you could correlate load-test runs → flame graphs → code-level hotspots in a single workflow. With Pyroscope 2.0's reduced storage cost, this is increasingly cost-justifiable.

### 🟡 Significant Gaps

Grafana IRM / OnCall

There's no incident management layer. Alerts presumably route to some external system (PagerDuty, email?), but there's no evidence of GMA → IRM integration. Without IRM, you're missing: working-hours-aware on-call, burn-rate SLO → page escalation, and incident timeline correlation with telemetry.

SLOs

No SLO definitions are present. Given the multi-cluster Kubernetes setup (`ollie`, `testing`, `staging`, `sandbox-testing-1`, `yasir` visible in `cluster` labels), this means there's no formal reliability target tracking and no burn-rate alerting—you only know something broke when someone notices.

Frontend / RUM (Faro)

If fitfile has any web frontend (reasonable assumption for a fitness file service), Faro is absent. Browser-side errors, Core Web Vitals, and session performance data are completely invisible.

Synthetic Monitoring

No probe-based availability checks are configured. You have no outside-in view of service health—only inside-out Kubernetes metrics and logs.

### 🟢 Minor / Optional Gaps

- k6 Cloud—not configured. Relevant if load testing is part of your dev cycle
- Application Observability—would provide automated RED metrics + service maps without manual instrumentation, but requires Tempo to be useful
- Database Observability—MongoDB is visible in your logs; DB query observability may be worth evaluating
- Grafana AI Assistant—useful for incident triage once you have fuller telemetry

---

## 4. Do You Have a Full Stack?

No. You have approximately 40% of a production-grade observability stack. Specifically:

- ✅ Metrics—instrumented but cardinality-degraded (see §5)
- ✅ Logs—instrumented but index-bloated (see §5)
- ❌ Traces—entirely absent
- ❌ Profiles—entirely absent
- ❌ Frontend / RUM—entirely absent
- ❌ Reliability (SLO + IRM)—entirely absent
- ⚠️ Adaptive Telemetry—present but blocked by expired auth token

The two pillars you have (metrics + logs) are also significantly under-optimised, driving costs that could partially fund the missing pillars.

---

## 5. Cost Optimisation—Concrete Recommendations

The audit's findings map directly to Grafana's pricing model. Here's the priority-ordered plan:

### 🔴 Immediate (This Week)—Fix the Auth & Apply Quick Wins

Re-authenticate adaptive telemetry first. Every other cost action is harder without it:

```bash
gcx login
gcx stacks list
gcx config set-context fitfileprod --stack fitfileprod
```

This unblocks Adaptive Metrics (average 35% metrics cost reduction across 1,500+ orgs) and Adaptive Logs without any collector redeployment.

Prometheus—eliminate the three biggest cost drivers (these alone likely represent 60–70% of your active series bill):

| Drop target | Cardinality eliminated | Mechanism |
|---|---|---|
| `name` label from ksm | 65,145 series | `metric_relabel_configs` → `labeldrop` |
| `container_id` | 47,016 series | `metric_relabel_configs` → `labeldrop` |
| `uid` | 24,057 series | `metric_relabel_configs` → `labeldrop` |
| `pod` from ksm + `k8s_pod_name` / `k8s_pod_uid` / `k8s_pod_ip` / `pod_ip` | ~26,000+ series | `labeldrop` / `labeldrop` |

These are all covered by the `values.yaml` snippets already in your audit file (§6). Apply them now.

Loki—single-line highest-impact fix:

The `pod: null` structured metadata override is not working on the testing cluster despite being expected—`pod` still shows 562 indexed values. Fix this first; it's a single `values.yaml` line that eliminates the biggest single source of Loki index growth.

Then drop zero-cardinality labels (`app_id`, `app_key`, `flags`, `source`, `k8s_cluster_name`)—these add index cost with zero query value.

### 🟡 Short Term (2–4 Weeks)—Use Adaptive Telemetry & Label Pruning

Once auth is restored:

1. Adaptive Metrics—open `Administration → Cost management → Metrics cost management → Adaptive Metrics`. Apply top recommendations iteratively, starting with any rule touching `name`, `workload`, `image_id`, `system_uuid`, `machine_id`. Review before applying—dropped cardinality is not historically recoverable.
2. Adaptive Logs—enable to auto-identify low-value log streams (UUID `service_name` values, 179 distinct—ideal pattern-aggregation candidates).
3. Move high-cardinality Loki labels to Structured Metadata: `container` (308, 58% UUIDs), `service_name` (323, 55% UUIDs), `reason` (64), `stream` (2). SM is stored but not indexed—you keep query-time access without paying for index cardinality.
4. Scrape interval tuning: For any non-alerting metrics (informational dashboards, capacity planning), increase scrape interval from 15s to 60s—reduces DPM by 75% on those series at zero loss of SLO-relevant resolution.

### 🟢 Medium Term (1–3 Months)—Add Missing Pillars Efficiently

Add Tempo (traces) cost-effectively:

- Tempo's pricing ($0.05/GB process, $0.40/GB write, $0.10/GB retain) rewards aggressive tail-based sampling
- Instrument only: error traces (100% sample), slow traces (>P95 latency, 100%), and normal traces (1–5% head sample)
- With SpiceDB gRPC traffic already producing `grpc.service` / `grpc.method` log fields, Tempo instrumentation will immediately produce actionable service maps—likely the highest ROI addition

Add Pyroscope (profiles) selectively:

- Pyroscope 2.0 (OTLP-native, reduced storage) makes the per-GB cost much more predictable
- Start with a single high-CPU service (visible via `container` metrics from cadvisor), not all services at once
- The k6 + Pyroscope integration is immediately useful if you run load tests against fitfile's API

Defer / evaluate last:

- Faro RUM ($0.75/1k sessions)—only if fitfile has a web frontend with real users
- k6 Cloud—only if performance regression testing is part of your release pipeline
- IRM ($20/user/month)—evaluate vs. existing incident tooling; free tier supports limited users
- Database Observability ($0.07/host hour ≈ $51/host/month)—expensive; only justify for MongoDB if query performance is a known issue

### Cost-as-Code Discipline (Ongoing)

- Store all dashboards, alerts, and SLOs in Git. Adaptive Metrics' recommendations are based on observed query usage—dashboards only in the UI are invisible to it, leading to false "unused" signals
- Run a monthly cost attribution review via Grafana Cloud's Cost Management Hub once available
- Audit prod (`fitfileprod`) with the same `gcx` process—the audit notes the prod context was missing; prod cardinality patterns are likely similar or worse

---

## 6. Summary Verdict

| Dimension | Status | Priority |
|---|---|---|
| Metrics | Present, severely cardinality-bloated | Fix now—60–70% cost reduction possible |
| Logs | Present, index-bloated | Fix now—label moves + drops + Adaptive Logs |
| Adaptive Telemetry | Blocked by expired token | Unblock immediately (`gcx login`) |
| Traces | Missing | Add next—highest ROI missing pillar |
| Profiles | Missing | Add after traces |
| Frontend/RUM | Missing | Evaluate—depends on product type |
| Synthetic Monitoring | Missing | Low cost, high value for SLA evidence |
| IRM / OnCall | Missing | Evaluate vs. existing tooling |
| SLOs | Missing | Define at least 2–3 key SLOs once GMA is confirmed |
| Prod audit | Deferred | Schedule immediately after test fixes validated |

The fastest cost improvement is applying the Prometheus `labeldrop` rules from your audit file and fixing the `pod: null` SM override—these require no new tooling, no auth, and could cut your metrics and logs bills materially before end of this sprint.

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Monday Jun 8, 2026 - 10:46 AM_
---

## Phase 2: Make the Canary Measurable

### Record the Baseline You Will Compare against

Before you turn the pilot on, capture a single representative log entry from `spicedb` in `fitfiletest` and write down these three things:

- the selector you used
- the indexed labels you saw
- the fields visible in the log detail panel

Keep that snapshot small. One log line is enough if it clearly contains `requestID`, `grpc.service`, `grpc.method`, and `peer.address`.

### Define the Success Metric up front

For this phase, the experiment succeeds if all of the following are true after rollout:

- the same selector still finds the workload
- the request fields still appear in log details
- the indexed label set is smaller or unchanged
- no saved query or dashboard breaks

If the label set grows, the pilot failed even if the detail panel still looks nice.

### Use a Strict before/after Compare

After deployment, re-run the exact same Grafana Explore query you used for the baseline and compare only the following:

| Check | Baseline | Pilot |
|---|---|---|
| Stream selector | working | working |
| Indexed labels | recorded | no larger |
| Detail fields | recorded | still visible |
| Query behavior | recorded | unchanged |

If one of those changes unexpectedly, stop and roll the pilot back before touching any other workload.

### Keep the Rollback Path Trivial

Make rollback a one-line values change in the same overlay:

- `enabled: true` for the pilot
- `enabled: false` to revert

Do not introduce a second toggle for this phase. One flag is easier to reason about, easier to revert, and easier to expand later.

### Decide what to Do with `component` and `logger` after the Canary

For the pilot, treat `component` and `logger` as conditional:

- keep them only if they are stable and useful for filtering in that workload
- move them to structured metadata if they vary a lot or are just debugging context

That lets you avoid over-indexing fields that look convenient but do not help with actual query patterns.

### Phase 2 Exit Criteria

You are ready to move on when:

- the pilot is isolated to one workload in `fitfiletest`
- the Helm render has a clean label/metadata split
- the same log line still shows the request context after rollout
- the indexed label footprint does not increase
- rollback works with a single values edit

If you want, I can continue with Phase 3 and turn this into the reusable helper pattern for the shared chart.
