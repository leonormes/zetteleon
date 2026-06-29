---
title: ffnode Helm Chart Review — Complexity & Library Chart Assessment
wiki_type: dossier
entity_kind: project
created: 2026-06-06
modified: 2026-06-06
tags:
- wiki
- dossier
- project
- helm
- kubernetes
- observability
sources:
- - - raw/2026-06-06-pieces-ffnode-helm-chart-review
- - - raw/2026-06-04-pieces-alloy-faro-grafana-explore
- - - raw/2026-06-04-pieces-k8s-labels-structured-metadata
permalink: llmeon/wiki/projects/ffnode-helm-chart-review
---

# ffnode Helm Chart Review — Complexity & Library Chart Assessment

## Summary

Workstream to analyse and simplify the `ffnode` umbrella Helm chart — the chart managing observability configuration across all FITFILE Kubernetes clusters (testing, staging, barts-prod, cuh-prod-1, nnuh-prod-1, hie-prod-34, mkuh-prd-4, sandbox-testing-1, ff-test-a, and others). The chart has grown complex through iterative additions, largely authored by Ollie Rushton. The goal is to assess whether Helm library charts can replace the current named-template umbrella patterns to create a type-safe, self-documenting, multi-cluster-safe process.

## Key Facts

- Work triggered by FTFL-673 (Grafana Alloy upgrade + Faro frontend observability) which added significant new templating to the ffnode umbrella chart — `_grafana.tpl`, `_certs.tpl`, `_frontend.tpl` — as part of MR !787 — [[raw/2026-06-06-pieces-ffnode-helm-chart-review]] (Pieces: 93d2d954-0552-4f79-a85f-8a1a1b2e688b)

- User collaborated with **Ollie Rushton** on the Faro/Alloy Helm deployment over several days, creating a comprehensive Claude Code prompt to analyse and review the chart's templating via git history — [[raw/2026-06-06-pieces-ffnode-helm-chart-review]] (Pieces: e0986954-c470-4e01-827d-914248b200e8)

- A Claude Code prompt was produced instructing the LLM to: (1) review all `ffnode` chart templates and cluster-specific overrides, (2) analyse git history for complexity trends, (3) assess whether library charts could replace current patterns, (4) recommend a migration sequence, (5) audit for the VSO double-evaluation bug across all 27 clusters — [[raw/2026-06-06-pieces-ffnode-helm-chart-review]]

- The library chart question was definitively answered: **library charts partially replace the umbrella patterns**, but the more important immediate win is making `secretTransformationDisableTpl: true` the **default** inside the library, preventing the VSO double-evaluation bug from recurring across clusters. Two clusters (LCA-DP, mkuh-prod-4) already required manual remediation in March 2026 — [[raw/2026-06-06-pieces-ffnode-helm-chart-review]] (Pieces: 25097810-5b9e-45cd-abad-4b192f6dcaab)

- Current templating patterns identified in the ffnode chart:
  1. **Named template as values factory** (`_grafana.tpl`, `_frontend.tpl`) — `mergeOverwrite + fromYaml + toYaml` chain risks silent key drops on type mismatch
  2. **Feature-flag gating** — `enabled: false` defaults in `values.yaml`
  3. **Vault secret injection via `tpl()`** — `generateVaultDynamicSecrets` applies `tpl()` to secret transformations; bare `{{get .Secrets "key"}}` expressions crash without `secretTransformationDisableTpl: true`

- Bugs encountered during FTFL-673: (1) `fromYaml` arity error (3 args instead of 1), (2) `$out` undefined in `_frontend.tpl`, (3) VSO double-evaluation bug, (4) type coercion in `_grafana.tpl` — [[raw/2026-06-04-pieces-alloy-faro-grafana-explore]]

- User goal: "type safe and flexible process for managing multiple k8s clusters" — wants the chart reviewable by anyone, not just Ollie — [[raw/2026-06-06-pieces-ffnode-helm-chart-review]]

## Connections

- [[wiki/projects/Grafana Alloy Monitoring — FTFL-638]] — Parent monitoring stack project; FTFL-673 is the Grafana upgrade ticket related to this helm chart work
- [[wiki/projects/FITFILE Testing Infrastructure]] — Testing cluster where the new chart patterns were first validated
- [[wiki/projects/FTFL-673 Grafana Deploy All Envs]] — The deployment ticket driving the chart changes
- [[wiki/projects/Hermes Config Production-Ready Audit]] — Config review skills may apply to the chart review prompt design
- [[wiki/projects/Helm Chart Structured Metadata — Grafana Cloud Log Enrichment]] — Structured metadata experiment that will inject metadata through the same ffnode umbrella chart
- [[wiki/projects/FITFILE Deployment — ArgoCD + Helm]] — Parent deployment architecture: FFNode umbrella chart + FFNodes overlays via ArgoCD; this page is a component of that system

## Contradictions

- None identified. The library chart analysis and the Claude Code prompt are complementary — the prompt handles the git-history-based complexity audit, while the hotfix evidence provides the concrete migration motivation.

## Open Questions

- Has the Claude Code prompt been executed, and what were its findings?
- Which clusters are still vulnerable to the `secretTransformationDisableTpl` bug (per the suggested `grep` audit)?
- Has the per-cluster CUE file audit (`grep -rn "secretTransformation" ffnodes/ | grep -v "DisableTpl"`) been run?
- Is there buy-in from Ollie on the library chart direction, or will this be a solo investigation?