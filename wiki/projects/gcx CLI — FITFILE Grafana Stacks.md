---
title: gcx CLI — FITFILE Grafana Stacks
wiki_type: dossier
entity_kind: project
created: 2026-05-19T22:20:00+00:00
modified: 2026-05-19T22:20:00+00:00
tags: [wiki, dossier, project]
sources:
  - raw/2026-05-19-pieces-gcx-cli-grafana-setup
---

## Summary

Setting up and authenticating the `gcx` CLI tool (Grafana CLI) to manage resources across both FITFILE Grafana Cloud stacks — production (`fitfileprod`) and testing (`fitfiletest`). The goal is to enable the LLM to read details from both stacks via the CLI.

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

## Timeline

- **2026-05-19** — User requested help setting up and authenticating `gcx` CLI for both FITFILE Grafana stacks; setup guide produced from memory.

## Connections

- [[Grafana-Monitoring]]
- [[Grafana Alloy Monitoring — FTFL-638]]

## Contradictions

*None identified.*

## Open Questions

- Has the `gcx login` been completed for both stacks?
- Are API keys or service account tokens being used for authentication?
