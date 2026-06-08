---
title: Helm Chart Structured Metadata — Grafana Cloud Log Enrichment
wiki_type: dossier
entity_kind: project
created: 2026-06-08T11:00:00+00:00
modified: 2026-06-08T11:00:00+00:00
tags: [wiki, dossier]
sources:
  - raw/2026-06-08-pieces-helm-structured-metadata
  - raw/2026-06-04-pieces-k8s-labels-structured-metadata
---

## Summary

Experiment initiative to enrich FITFILE Helm chart deployments with structured metadata, improving Grafana Cloud log context beyond what stream labels alone provide. The work builds on the labels-vs-structured-metadata understanding developed in early June and targets a phased rollout: starting with a small pilot on `spicedb` (testing cluster) as a canary, then generalising to a reusable Helm library helper pattern across all applications.

## Key Facts

- **2026-06-04** — Discussed the distinction between Kubernetes labels (indexed, high-cardinality risk) vs Loki structured metadata (non-indexed, per-line context fields) — [[raw/2026-06-04-pieces-k8s-labels-structured-metadata]] (Pieces: c1023742-62e5-425d-a9ca-7ff8aad2a4b2)

- **2026-06-08T08:48** — User requested a comprehensive context-packaging prompt covering the FITFILE ArgoCD + Helm deployment process (27 clusters, ffnode umbrella chart, overlay patterns) to use with an external agent — [[raw/2026-06-08-pieces-helm-structured-metadata]] (Pieces: f220d2f8-0c00-4239-95c8-602328fcb022)

- **2026-06-08T08:59** — Copilot synthesised the deployment context prompt covering: `ffnode` umbrella chart structure, cluster-specific overlay pattern (`ffnodes/<cluster>/`), ArgoCD ApplicationSets with PR generators, component templates (`_grafana.tpl`, `_certs.tpl`, `_frontend.tpl`), and VSO double-evaluation bug fix — [[raw/2026-06-08-pieces-helm-structured-metadata]] (Pieces: c0470216-6d54-486b-8481-2e67e2bbab2c)

- **2026-06-08T09:33** — Experiment plan defined: Phase 1 — small pilot moving one log-context field (e.g., `app_version`) from label to structured metadata on `spicedb` (fitfiletest cluster). Steps: pick app → add `structuredMetadata` to values → update Alloy pipeline → verify — [[raw/2026-06-08-pieces-helm-structured-metadata]] (Pieces: 80120449-7b3f-4ebc-8ae5-341e0bce4a46)

- **2026-06-08T09:43** — Phase 2 design: reusable helper and safety rails — define a shared `structuredMetadata` block in Helm values, use library chart template for consistent injection, verify Alloy pipeline consumption — [[raw/2026-06-08-pieces-helm-structured-metadata]] (Pieces: 1879599e-0642-4337-b40f-0e2eebfa61e2)

- **2026-06-08T10:01** — User ran Loki query to inspect stream labels on spicedb: `gcx logs query --context fitfiletest '{cluster="testing", namespace="spicedb"}' --since 15m --limit 10 -o json | jq '[.[].stream | keys] | flatten | unique'`. Hit jq error (element 12 is a string, not a stream object) — [[raw/2026-06-08-pieces-helm-structured-metadata]] (Pieces: f0c51431-bd39-4155-b09d-d2e03d61fb0a)

## Timeline

| Date | Event |
|------|-------|
| 2026-06-04 | Labels vs structured metadata discussion (theoretical groundwork) |
| 2026-06-08T08:48 | Context prompt request — ArgoCD/Helm deployment architecture |
| 2026-06-08T09:17 | Experiment request — structured metadata for Helm charts |
| 2026-06-08T09:33 | Phase 1 pilot plan defined (spicedb → fitfiletest) |
| 2026-06-08T09:43 | Phase 2 reusable helper design |
| 2026-06-08T10:01 | Loki stream label inspection (jq error encountered) |

## Connections

- [[wiki/projects/ffnode Helm Chart Review]] — ongoing ffnode umbrella chart simplification; structured metadata will be injected through the same chart
- [[wiki/projects/Grafana Alloy Monitoring — FTFL-638]] — the Alloy pipeline that consumes structured metadata in Grafana Cloud; the metadata enrichment directly feeds into Alloy's log processing
- [[wiki/projects/GitOps Deployment Pipeline Optimisation]] — ArgoCD/Helm deployment pipeline used to roll out structured metadata changes

## Contradictions

None identified yet.

## Open Questions

- What is the exact response format from `gcx logs query -o json` — is it a JSON array or NDJSON? The jq error on element 12 suggests mixed types in the top-level array.
- Is `spicedb` on `fitfiletest` the right canary target, or should the pilot start on a different low-traffic namespace?
- Which specific fields should be promoted from labels to structured metadata first? `app_version` is proposed but the full list needs specification.
- Does the Alloy pipeline on `fitfiletest` already support structured metadata, or does the River config need updating first?