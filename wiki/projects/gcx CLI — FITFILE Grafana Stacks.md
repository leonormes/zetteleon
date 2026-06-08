---
title: gcx CLI — FITFILE Grafana Stacks
wiki_type: dossier
entity_kind: project
created: 2026-05-19T22:20:00+00:00
modified: 2026-06-05T09:50:00+00:00
tags: [wiki, dossier, project]
sources:
  - raw/2026-05-19-pieces-gcx-cli-grafana-setup
  - raw/2026-06-05-fitfile-loki-prometheus-cardinality-audit
---

## Summary

Setting up and authenticating the `gcx` CLI tool (Grafana CLI) to manage resources across both FITFILE Grafana Cloud stacks — production (`fitfileprod`) and testing (`fitfiletest`). The gcx CLI is now actively used for observability audits — a full Loki & Prometheus label cardinality audit was completed on the `fitfiletest` stack on 2026-06-05.

## Key Facts

- The `gcx` CLI is a unified tool for managing Grafana resources, dashboards, datasources, alerting, and Cloud product APIs (SLO, IRM, Synthetic Monitoring, Fleet, k6, and more).
  > "gcx is a unified CLI for managing Grafana resources, dashboards, datasources, alerting, and Cloud product APIs (SLO, IRM, Synthetic Monitoring, Fleet, k6, and more)." — [[raw/2026-05-19-pieces-gcx-cli-grafana-setup]] (Pieces: a4bd5558-c9be-4226-bb84-1db404eea34f)

- Two Grafana Cloud stacks exist under the FITFILE org (`garethhailes`):
  | Context name | Stack URL | Purpose |
  |---|---|---|
  | `fitfileprod` | `https://fitfileprod.grafana.net` | Production |
  | `fitfiletest` | `https://fitfiletest.grafana.net` | Testing / Non-prod |
  > "You have two Grafana Cloud stacks under the FITFILE org (garethhailes): fitfileprod (Production) and fitfiletest (Testing)" — [[raw/2026-05-19-pieces-gcx-cli-grafana-setup]] (Pieces: 6b5a24ff-c41d-43f8-b0af-6cde6f90ae79)

- The org is on **Grafana Cloud Pro**, cluster `prod`.
  > "Your org is FITFILE (garethhailes), on Grafana Cloud Pro, cluster prod" — [[raw/2026-05-19-pieces-gcx-cli-grafana-setup]] (Pieces: ab317018-890b-47e2-ae7b-7ca195f6118a)

- Access policies are managed at `grafana.com/orgs/garethhailes/access-policies`. Relevant existing policies include `terraform` and `hermes-agent`.
  > "Your access policies are managed at grafana.com/orgs/garethhailes/access-policies. Relevant policies that already exist include: terraform, hermes-agent" — [[raw/2026-05-19-pieces-gcx-cli-grafana-setup]] (Pieces: 2474c2e1-ac86-4e73-b774-e3a8d6619e6d)

- **2026-06-05:** A full Loki & Prometheus label cardinality audit was executed on `fitfiletest` via `gcx logs label-names`, `gcx logs label-values`, `gcx logs query`, and `gcx metrics labels` commands.
  > "FITFILE—Loki & Prometheus Cardinality Audit... Scope: fitfiletest Grafana Cloud Stack" — [[raw/2026-06-05-fitfile-loki-prometheus-cardinality-audit]]

- **Cardinality crisis identified:** Prometheus has 65K-series `name` label, 47K-series `container_id`, 24K `uid` — estimated 60-70% of active series bill is wasted on unbounded labels from kube-state-metrics.
  > "These are all covered by the values.yaml snippets already in your audit file (§6). Apply them now." — [[raw/2026-06-05-fitfile-loki-prometheus-cardinality-audit]]

- **Loki index bloat:** 562 unique `pod` values (still indexed despite expected SM override), 308 `container` values (58% UUIDs), 323 `service_name` values (55% UUIDs).
  > "pod: null structured metadata override is not working on the testing cluster" — [[raw/2026-06-05-fitfile-loki-prometheus-cardinality-audit]]

- **Adaptive Telemetry blocked:** Both Adaptive Logs and Adaptive Metrics APIs returned `401 Unauthorized` due to expired Grafana Cloud API token. Re-authentication is needed via `gcx login`.
  > "Adaptive Telemetry APIs returned 401 Unauthorized—the Grafana Cloud API token has expired." — [[raw/2026-06-05-fitfile-loki-prometheus-cardinality-audit]]

- **Prod audit deferred:** `fitfileprod` context was not found in `gcx config`. Prod must be added and audited separately.

## Timeline

- **2026-05-19** — User requested help setting up and authenticating `gcx` CLI for both FITFILE Grafana stacks; setup guide produced from memory.
- **2026-06-05** — gcx CLI used to run full Loki & Prometheus label cardinality audit on `fitfiletest`. Comprehensive report with drop/move/SM recommendations produced. Adaptive telemetry found to be blocked by expired token.

## Connections

- [[Grafana-Monitoring]]
- [[Grafana Alloy Monitoring — FTFL-638]]
- [[FTFL-673 Grafana Deploy All Envs]]

## Contradictions

*None identified.*

## Open Questions

- ✅ **2026-06-05: RESOLVED** — `gcx login` was completed for the `fitfiletest` stack. CLI is actively working for label audit queries. The `fitfileprod` context is NOT yet configured — blocked by `gcx login` requiring re-auth. The Grafana Cloud API token has expired, preventing access to Adaptive Telemetry APIs.
- Are API keys or service account tokens being used for authentication? (Still unknown — the `gcx` stack authentication model hasn't been investigated.)
- Why is `pod` still showing as an indexed label (562 values) on the testing cluster despite the expected `pod: null` structured metadata override? Needs Alloy/values.yaml verification.
