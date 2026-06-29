---
title: Grafana Alloy Monitoring — FTFL-638
wiki_type: dossier
entity_kind: project
created: 2026-05-06 20:15:00+00:00
modified: 2026-06-04 20:41:52+00:00
tags:
- wiki
- dossier
sources:
- raw/2026-05-06-pieces-grafana-alloy-monitoring
- raw/2026-05-26-pieces-ftfl599-ftfl638-prodos
- raw/2026-05-26-pieces-ftfl638-antigravity-cursor-prompt
- raw/2026-05-27-pieces-alloy-image-pull-secret
- raw/2026-05-27-pieces-k8s-observability
- raw/2026-05-28-pieces-ftfl638-grafana-alloy-fix
- raw/2026-05-29-pieces-ftfl638-logs
- raw/2026-05-29-pieces-ftfl638-workflow-taints
- raw/2026-05-30-pieces-ftfl638-scheduling-regression
- raw/2026-05-30-pieces-ftfl638-cpu-saturation
- raw/2026-06-04-pieces-alloy-faro-grafana-explore
- raw/2026-06-04-pieces-k8s-labels-structured-metadata
permalink: llmeon/wiki/projects/grafana-alloy-monitoring-ftfl-638
---

## Summary

A Kubernetes monitoring stack project focused on Grafana/Alloy Helm deployment and Loki log labeling. The primary ticket is **FTFL-638** (Grafana/Alloy log labeling improvements), with related work tracked under FTFL-511/512. **As of 2026-05-29 15:54, the taint-based coverage gap for alloy-logs on workflow nodes has been fully diagnosed**: two taints block the DaemonSet from scheduling on `aks-workflows-*` nodes (`dedicated=workflows:NoSchedule` and `kubernetes.azure.com/scalesetpriority=spot:NoSchedule`). The fix is to add both tolerations to `grafana.alloy-logs.tolerations` in `ffnodes/fitfile/testing/values.yaml`. Previously fixed: (1) `alloy-metrics` pushing to wrong endpoint, (2) River config parsing error `action = keep` corrected to `action = "keep"`.

## Key Facts

- **2026-05-27**: `fitfile-image-pull-secret` missing from `monitoring` namespace — Alloy-logs DaemonSet pods (x8t45: 167, tbnz9: 212, hl9v2: 213 occurrences) all hitting `FailedToRetrieveImagePullSecret`. This is the **4th known recurrence** (Jan 22, Mar 27, May 5, May 27) — [[raw/2026-05-27-pieces-alloy-image-pull-secret]] (Pieces: 22e8d732-027b-4357-8f4a-2497823a02dd)

- **2026-05-27**: Root cause identified — wrong secret name and wrong secret type. A secret named `argocd-acr-pull-secret` (ArgoCD Helm OCI repo credential, type Opaque) was created in `monitoring`, but alloy-logs expects `fitfile-image-pull-secret` (type kubernetes.io/dockerconfigjson with .dockerconfigjson data key) — [[raw/2026-05-27-pieces-alloy-image-pull-secret]] (Pieces: 197fa585-493b-4385-b7fd-ade194efe574)

- **Secret replication chain**: (1) Terraform creates VaultDynamicSecret `fitfile-image-pull` in argocd namespace → (2) VSO reads creds/acr-pull from Vault, creates `fitfile-image-pull-secret` (kubernetes.io/dockerconfigjson) in argocd → (3) Reflector auto-replicates to namespaces listed in `namespaces_for_image_pull_secret` → (4) kubernetes_default_service_account_v1 injects imagePullSecrets — [[raw/2026-05-27-pieces-alloy-image-pull-secret]] (Pieces: 98a0aea4-ba8f-4161-b6ae-ff08d93dea69)

- The project spans Jira tickets FTFL-638 (log labeling), FTFL-511, and FTFL-512.
  > "Recent fixes and decisions documented in Jira: FTFL-638 (Grafana/Alloy log labeling improvements), and related notes about labelsToKeep (pod, namespace, container, and later job/stream/flags additions)." — [[raw/2026-05-06-pieces-grafana-alloy-monitoring]] (Pieces: cc31dc88-8370-40ed-8d2e-8ed5943921ad)

- The testing cluster is missing logs for three key containers: `ffcloud-service`, `frontend`, and `spicedb`. ArgoCD syncs trigger re-deployments that disrupt log streams.
  > "Testing cluster issues: missing logs for ffcloud-service, frontend, spicedb; ArgoCD syncs triggering re-deployments; testing/logging verification with Loki via logcli." — [[raw/2026-05-06-pieces-grafana-alloy-monitoring]] (Pieces: cc31dc88-8370-40ed-8d2e-8ed5943921ad)

- A concrete `values.yaml` draft has been produced covering `podLogs.labelsToKeep`, `grafana.chart.targetRevision: "3.7.5"`, `loki.discovery`, `extraRelabelingRules` fallback, and `opencost` configuration.
  > "```yaml\n# Grafana/Alloy monitoring values (illustrative)\npodLogs:\n  enabled: true\n  labelsToKeep:\n    - pod\n    - namespace\n    - container\n    - job\n    - stream\n    - flags\n\ngrafana:\n  chart:\n    targetRevision: '3.7.5'\n```" — [[raw/2026-05-06-pieces-grafana-alloy-monitoring]] (Pieces: cc31dc88-8370-40ed-8d2e-8ed5943921ad)

- The `job` label target is `namespace/container` for Loki queries. Fallback `extraRelabelingRules` are defined using `source_labels = ["namespace", "container"]` with separator `/` and action `replace`.
  > "optional extra relabeling (fallback; use only if primary fix does not produce the desired label)\n```\nrule {\n  source_labels = [\"namespace\", \"container\"]\n  separator = \"/\"\n  target_label = \"job\"\n  action = \"replace\"\n}\n```" — [[raw/2026-05-06-pieces-grafana-alloy-monitoring]] (Pieces: cc31dc88-8370-40ed-8d2e-8ed5943921ad)

- Validation tooling specified: `logcli` for Loki stream label verification, `helm` for chart inspection/upgrades, `kubectl` for ConfigMap checks, `cue vet -c=false` for structural schema validation, and ArgoCD for GitOps syncs.
  > "Tooling: kubectl, helm, cue vet -c=false, logcli." — [[raw/2026-05-06-pieces-grafana-alloy-monitoring]] (Pieces: cc31dc88-8370-40ed-8d2e-8ed5943921ad)

- The execution plan is staged in four phases: (1) Discovery and Schema Stabilization, (2) Values.yaml Design, (3) Apply/Validate/Stabilize in Testing Cluster, (4) Documentation and Handover.
  > "Phase 1 — Discovery and Schema Stabilization... Phase 2 — Values.yaml Design... Phase 3 — Apply, Validate, and Stabilize in Testing Cluster... Phase 4 — Documentation and Handover." — [[raw/2026-05-06-pieces-grafana-alloy-monitoring]] (Pieces: cc31dc88-8370-40ed-8d2e-8ed5943921ad)

- Acceptance criteria include: values.yaml passes `cue vet -c=false`; Loki queries show `job="namespace/container"` for target containers; Alloy-logs DaemonSet redeployed via ArgoCD; Grafana dashboards show no gaps; rollback/runbook documented; all changes linked to FTFL tickets.
  > "Acceptance Criteria (definition of done): The values.yaml draft is complete and passes structural validation (cue vet -c=false) against the schema you’ve been using." — [[raw/2026-05-06-pieces-grafana-alloy-monitoring]] (Pieces: cc31dc88-8370-40ed-8d2e-8ed5943921ad)

- Security constraints remain in force: TLS 1.2/1.3, cipher suites, private networking; no dashboard or retention policy changes without explicit approval.
  > "Security hardening remains in force (TLS 1.2/1.3, cipher suites, private networking where applicable)." — [[raw/2026-05-06-pieces-grafana-alloy-monitoring]] (Pieces: cc31dc88-8370-40ed-8d2e-8ed5943921ad)

- Key file reference: `ffnodes/fitfile/testing/values.yaml` on local filesystem (`file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/deployment/ffnodes/fitfile/testing/values.yaml`).
  > "File references you've touched or reviewed: ffnodes/fitfile/testing/values.yaml and related Alloy config/configMap sections." — [[raw/2026-05-06-pieces-grafana-alloy-monitoring]] (Pieces: cc31dc88-8370-40ed-8d2e-8ed5943921ad)

- **2026-05-26**: User provided a detailed FTFL-638 spec document (YAML frontmatter + markdown) with a structured task list covering Phase 0 verification (kubectl/gcx checks), values.yaml fixes (extraRelabelingRules, KSM cluster label, discoveryType), and a complete Cursor context prompt was produced and delivered — [[raw/2026-05-26-pieces-ftfl599-ftfl638-prodos]] (Pieces: 79586e03-fc44-4bcd-84ba-be79547e60ab)
- **2026-05-26**: Live values.yaml (16,966 bytes, modified 14:00 BST) was read directly; specific problems identified in the `grafana:` block including wrong `extraRelabelingRules` structure, missing KSM cluster label, and incorrect `discoveryType` key — [[raw/2026-05-26-pieces-ftfl599-ftfl638-prodos]] (Pieces: 01c62afd-9f7d-444f-825c-1213baddc4cb)
- **2026-05-26**: A complete, grounded Cursor context prompt for FTFL-638 was produced covering all 7 checklist items, backed by real file reads and corroborated LTM evidence — [[raw/2026-05-26-pieces-ftfl599-ftfl638-prodos]] (Pieces: acbc5946-0a34-4b46-bc44-2fe5e6a0823e)

- **2026-05-26 (17:16)**: A complete antigravity-cli prompt was produced for FTFL-638, instructing the LLM to use MCP file analysis tools to diff Grafana Helm override files across all FITFILE ffnodes clusters and use kubectl+gcx to investigate live cluster state — [[raw/2026-05-26-pieces-ftfl638-antigravity-cursor-prompt]] (Pieces: 59181fac-0d3a-4176-8071-58cec7e668b8)
- **2026-05-26 (16:48)**: A comprehensive Cursor context prompt was produced with full history of all remediation attempts; key environment details: AKS cluster `fitfile-cloud-testing-aks-cluster` runs Kubernetes v1.34.7 (UK South), subscription `249df46b-f75d-4492-8e78-b33a00473548`, gcx v0.2.16 (v0.3.0 available), active branch `feature/FTFL-638-add-labels-for-logs` — [[raw/2026-05-26-pieces-ftfl638-antigravity-cursor-prompt]] (Pieces: 4c73b9cb-71e6-481b-bbbf-8e6db1ac904b)

- **2026-05-27**: Grafana config fix requested — `labelsToKeep` contains label names with dots and slashes (`app.kubernetes.io/name`, `k8s.namespace.name`, `k8s.node.name`) that are invalid as Loki stream labels; dots and slashes must be replaced with underscores — [[raw/2026-05-27-pieces-k8s-observability]] (Pieces: 5ffdfcc3-392a-4cc3-89ba-bac507176ede)

- **2026-05-27**: Alloy-logs DaemonSet secret issue resolved — user created `fitfile-image-pull-secret` in `monitoring` namespace by copying from `argocd`; next step is rolling the alloy-logs pods and verifying log flow — [[raw/2026-05-27-pieces-k8s-observability]] (Pieces: 05295732-afd3-4c33-86c8-bdef43a4e9d7)

- **2026-05-27**: A complete Hermes `/goal` prompt was produced to analyse the FITFILE k8s deployment codebase at `https://gitlab.com/fitfile/deployment` and generate a report covering ArgoCD sync status, Alloy config, and Helm values — [[raw/2026-05-27-pieces-k8s-observability]] (Pieces: 093e4abc-4d0a-4446-9325-d52f187f87eb)

- **2026-05-28**: Grafana Alloy config parse error identified — `action = keep` (bare identifier) at line 248 of `/etc/alloy/config.alloy` causes fatal startup crash; in River config language, `keep` is parsed as a component reference where a string is expected; fix is `action = "keep"` — [[raw/2026-05-28-pieces-ftfl638-grafana-alloy-fix]] (Pieces: 48031f32-a7d5-4191-bddf-347b19528d81, 63742416-0040-428f-bd13-f3206bc8b8b1)

- **2026-05-28**: ArgoCD sync `01345-xeYhP` for `grafana-k8s-monitoring` app (project: `default`, namespace: `monitoring`) ran successfully — mid-sync snapshot showed Sync/0 wave largely complete with one resource still rolling and PostSync hooks pending — [[raw/2026-05-28-pieces-ftfl638-grafana-alloy-fix]] (Pieces: df1054fe-1f65-494d-861b-8f159a442533, eb033a66-71a3-45d9-81ac-4287575901b1, eaaa7158-e26f-49de-8989-0fb3a85f0cf1)

- **2026-05-28**: A complete Claude Code debug prompt was produced for FTFL-638 covering the full stack (ArgoCD + testing cluster monitoring charts deployment failure), with instructions to use `kubectl` CLI for live cluster investigation — [[raw/2026-05-28-pieces-ftfl638-grafana-alloy-fix]] (Pieces: 8f08c302-94ef-440d-8afa-1009449f6973)

- **2026-05-28**: Per user confirmation, the Grafana Monitoring issue in the testing cluster is **now fixed**; a Jira update was drafted for FTFL-628 covering the two resolved root causes: (1) `alloy-metrics` was pushing Prometheus metrics to the wrong endpoint, and (2) a config parsing error in `/etc/alloy/config.alloy` — [[raw/2026-05-28-pieces-ftfl638-grafana-alloy-fix]] (Pieces: cb801a1a-0bca-4d3a-9893-10389e501fa8, d766dadf-20b8-4ab6-9b5e-fe81d3e8fde1, 0dc6aa22-eb8b-49cf-bab0-bb7f2c2d0774)
- **2026-05-30 (15:42)**: Confirmed tolerations are permissive, not restrictive — adding workflow node tolerations to alloy-logs does NOT restrict scheduling on system nodes (`aks-system-*`), which have no taints. The fix adds coverage for both taints on `aks-workflows-*` nodes (`dedicated=workflows:NoSchedule` and `spot:NoSchedule`) while preserving existing system node coverage — [[raw/2026-05-30-pieces-ftfl638-tolerations-permissive.md]] (Pieces: fd75ff76-e61c-4d32-a5b1-f53c8679c090)

- **2026-05-30 (12:56)**
- **2026-06-04** — Alloy Faro logs debugging: SessionInstrumentation fix identified; K8s labels & structured metadata guidance produced; Grafana Explore UI filtering workflow clarified
: New root cause identified — **CPU request saturation** on workflow node: one node reported at **99% request saturation** (`3852m/3860m`, only **8m free`), while `alloy-logs` was requesting **10m CPU**. Kubernetes returned `Warning FailedScheduling ... 0/3 nodes are available: 1 Insufficient cpu, 2 node(s) didn't satisfy plugin(s) [NodeAffinity]`. **Proposed fix:** reduce `alloy-logs` CPU request from `10m` → `5m` in `ffnodes/fitfile/testing/values.yaml`, keep workflow/spot tolerations, then redeploy and verify DaemonSet reschedules. See [FTFL-638 MR !783](https://gitlab.com/fitfile/deployment/-/merge_requests/783). **Related:** same change set also removed `pod: null` from `structuredMetadata`, pushing `pod` out of Loki stream labels — restoring that keeps pod-based querying working — [[raw/2026-05-30-pieces-ftfl638-cpu-saturation]] (Pieces: 14aa82dd-ea33-4b05-b981-95ad9aa151ea)

## Connections

- [[wiki/projects/Azure AKS Backup — FTFL]] (same FTFL program; FTFL-596/599/615)
- [[wiki/projects/gcx CLI — FITFILE Grafana Stacks]] (gcx tool used for Grafana Cloud investigation)
- [[wiki/projects/Hermes-Agent]] (Hermes orchestration used to produce the antigravity-cli prompt)
- [[wiki/projects/FITFILE Testing Infrastructure]] (same testing cluster; Terraform AKS and secrets management)
- [[FTFL-673 Grafana Deploy All Envs]] (successor: deploy fixed Grafana across all environments)
- [[wiki/projects/Helm Chart Structured Metadata — Grafana Cloud Log Enrichment]] (structured metadata experiment feeding into Alloy's log processing pipeline)

- **2026-05-29 (15:34–15:54)**: Root Cause #2 for missing workflow logs fully diagnosed — the `aks-workflows-32842669-vmss*` node pool has **two taints** (`dedicated=workflows:NoSchedule` and `kubernetes.azure.com/scalesetpriority=spot:NoSchedule`), and the alloy-logs DaemonSet tolerates neither. Result: the second alloy-logs pod stays `Pending` whenever the workflow pool scales up, and workflow pod logs are never collected — [[raw/2026-05-29-pieces-ftfl638-workflow-taints]] (Pieces: d8922edc-675e-44aa-a03b-b719fcf7780a)

- **2026-05-29 (15:39)**: Workflow node taint details confirmed via `kubectl get nodes -o json | jq ...` — only the `aks-workflows-*` pool carries the `dedicated=workflows:NoSchedule` taint; system nodes (`aks-system-*`) have zero taints — [[raw/2026-05-29-pieces-ftfl638-workflow-taints]] (Pieces: cf74bae5-299f-4da9-86f3-c94740c77269)

- **2026-05-29 (15:54)**: Complete values.yaml toleration fix produced — both taints must be tolerated for alloy-logs to schedule on workflow nodes. The Spot VM taint (`kubernetes.azure.com/scalesetpriority=spot:NoSchedule`) is AKS-standard on all Spot node pools and must be explicitly tolerated by any DaemonSet needing coverage — [[raw/2026-05-29-pieces-ftfl638-workflow-taints]] (Pieces: 7c6fcf68-3c0e-4f47-ac18-c8d348f377e4)

- **2026-05-29 (15:42)**: User confirmed tolerations are permissive, not restrictive — adding workflow node tolerations to alloy-logs does NOT affect scheduling on system nodes (`aks-system-*`), which have no taints. Result: alloy-logs continues on system nodes (unchanged) + newly covers workflow nodes — [[raw/2026-05-29-pieces-ftfl638-workflow-taints]] (Pieces: 6c429e3c-2cb5-49dc-900a-79d52e9c56f7)

- **2026-05-30 (04:17–08:17)**: Commit `d3c292` (MR !779 / !781) re-broke pod labels on workflow nodes ~21 minutes before detection — the `grafana-k8s-monitoring-alloy-logs-f54v9` pod is failing to schedule on 2 of 3 nodes due to NodeAffinity mismatch; the `agentpool=workflows` and `kubernetes.azure.com/priority=spot` labels conflict with the DaemonSet's affinity rules — [[raw/2026-05-30-pieces-ftfl638-scheduling-regression]] (Pieces: ec7ab7b2-48ac-4fdf-9bd8-9b1274d43af5)

- **2026-05-30**: Hermes `/goal` prompt was requested to investigate the current state of testing and gcx logging — the user needs an automated investigation of the DaemonSet scheduling failure and CPU exhaustion on the third node — [[raw/2026-05-30-pieces-ftfl638-scheduling-regression]] (Pieces: 9e20bac1-90d5-4a57-8745-d31f459ba2e7)

- **2026-06-04**: **Alloy Faro logs not reaching Grafana Cloud** — root cause: missing `X-Faro-Session-Id` header. The Grafana Cloud Faro collector requires every inbound payload to carry a `X-Faro-Session-Id` header, which is injected by the Faro Web SDK's `SessionInstrumentation` plugin. The InsightFILE frontend (branch `feature/TT-138-configure-faro-sdk`, file `getAppConfigEnv.ts`) was missing `new SessionInstrumentation()` in the `initializeFaro` call.

  > "I now have sufficient context to deliver the full answer. ## Root cause: missing `X-Faro-Session-Id` header. The Alloy error is unambiguous: `HTTP Status Code 400, Message=missing X-Faro-Session-Id header, activate the SessionInstrumentation`" — [[raw/2026-06-04-pieces-alloy-faro-grafana-explore]] (Pieces: 5678461a-fc77-4c5b-8b3e-c9754a0bbbe2)

- **2026-06-04**: **Fix identified** — add `new SessionInstrumentation()` to the `instrumentations` array in `initializeFaro()`. The session header flows: Browser (Faro Web SDK with `SessionInstrumentation`) → `otelcol.receiver.faro "default"` on port 12347 (exposed via Ingress) → Grafana Cloud Faro collector.

  > "Your `initializeFaro` call needs to look like this. The key addition is `new SessionInstrumentation()` in `instrumentations`: ... `instrumentations: [...getWebInstrumentations(), new SessionInstrumentation()],`" — [[raw/2026-06-04-pieces-alloy-faro-grafana-explore]] (Pieces: 5678461a-fc77-4c5b-8b3e-c9754a0bbbe2)

- **2026-06-04**: **K8s labels vs Structured Metadata guidance produced** — clarified that labels are low-cardinality indexed stream identifiers (`env`, `app`, `namespace`), while structured metadata are high-cardinality non-indexed per-line attributes (`traceID`, `userID`, `requestID`). Recommended K8s standard labels: `app.kubernetes.io/name`, `app.kubernetes.io/instance`, `app.kubernetes.io/component`, `app.kubernetes.io/part-of`, `app.kubernetes.io/managed-by`. AKS operational labels: `environment`, `team`, `owner`, `cost-center`, `criticality`.

  > "Labels are indexed key-value pairs that define and identify a log stream... Structured metadata are non-indexed key-value pairs attached to individual log lines, not to streams." — [[raw/2026-06-04-pieces-k8s-labels-structured-metadata]] (Pieces: c1023742-62e5-425d-a9ca-7ff8aad2a4b2)


## Timeline

- **2026-05-06** — Project page created; initial values.yaml draft produced
- **2026-05-26** — FTFL-638 spec document provided; Cursor and antigravity-cli prompts generated
- **2026-05-27** — Alloy image pull secret issue identified and resolved (4th recurrence); labelsToKeep dots/slashes issue flagged
- **2026-05-28** — River config parse error fixed (`action = keep` → `action = "keep"`); Argo CD sync successful; issue declared fixed
- **2026-05-29** — Ollie reports Workflows logs still invisible; investigation identifies two root causes: (1) `pod: null` in structuredMetadata suppresses stream label, (2) alloy-logs DaemonSet can't schedule on workflow nodes due to missing taint tolerations
- **2026-05-29 15:54** — Full taint investigation complete: workflow nodes have two taints; complete values.yaml fix produced; tolerations confirmed as permissive (system node coverage unaffected)
- **2026-05-30** — Commit `d3c292` (MR !779/!781) re-broke pod labels on workflow nodes; NodeAffinity mismatch blocks scheduling on 2 of 3 nodes; Hermes `/goal` prompt requested for automated investigation
- **2026-05-30 (12:56)**
- **2026-06-04** — Alloy Faro logs debugging: SessionInstrumentation fix identified; K8s labels & structured metadata guidance produced; Grafana Explore UI filtering workflow clarified
 — CPU request saturation root cause identified: workflow node at 3852m/3860m (99%), Alloy requesting 10m; fix proposed: reduce to 5m

## Contradictions

_(none identified)_

## Open Questions

- Has the `values.yaml` draft been tested against the actual Helm chart schema for Grafana Alloy v3.7.5?
- After applying both tolerations to alloy-logs, have workflow pod logs appeared in Grafana for the `argo` namespace?
- What is the current state of the `extraRelabelingRules` fallback — is it required or can the primary `labelsToKeep` config achieve `job="namespace/container"` alone?
- After reducing alloy-logs CPU request to 5m, does the DaemonSet successfully reschedule on the saturated workflow node?