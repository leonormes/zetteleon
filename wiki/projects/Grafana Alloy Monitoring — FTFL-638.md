---
title: Grafana Alloy Monitoring — FTFL-638
wiki_type: dossier
entity_kind: project
created: 2026-05-06T20:15:00+00:00
modified: 2026-05-26T14:30:00+00:00
tags: [wiki, dossier]
sources:
  - raw/2026-05-06-pieces-grafana-alloy-monitoring
  - raw/2026-05-26-pieces-ftfl599-ftfl638-prodos
---

## Summary

A Kubernetes monitoring stack project focused on Grafana/Alloy Helm deployment and Loki log labeling. The primary ticket is **FTFL-638** (Grafana/Alloy log labeling improvements), with related work tracked under FTFL-511/512. The goal is to define a production-ready `values.yaml` shape for the Grafana/Alloy deployment, fix YAML indentation and label consistency issues in the Alloy ConfigMap, and produce a staged plan to stabilise the testing cluster so that logs for `ffcloud-service`, `frontend`, and `spicedb` are reliably labeled and queryable in Loki.

## Key Facts

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

## Connections

- [[wiki/projects/Azure AKS Backup — FTFL]] (same FTFL program; FTFL-596/599/615)
- [[wiki/projects/Hermes Integration — Provider Adapter Setup]] (Hermes orchestration skill used to produce the research prompt)

## Contradictions

_(none identified)_

## Open Questions

- Has the `values.yaml` draft been tested against the actual Helm chart schema for Grafana Alloy v3.7.5?
- Are there additional containers beyond `ffcloud-service`, `frontend`, and `spicedb` that need log labeling verification?
- What is the current state of the `extraRelabelingRules` fallback — is it required or can the primary `labelsToKeep` config achieve `job="namespace/container"` alone?
