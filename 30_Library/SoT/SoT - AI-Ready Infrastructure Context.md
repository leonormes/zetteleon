---
aliases: [AI Context Builder, Droidctx Pattern, Infrastructure Snapshotting]
conformant: false
created: 2026-03-28T17:10:00+00:00
modified: 2026-08-13T10:53:40+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-ai-ready-infrastructure-context
tags: [ai, context, devops, documentation, kubernetes, monitoring]
title: SoT - AI-Ready Infrastructure Context
type: sot
---

## Minimum Viable Understanding (MVU)

When AI coding agents debug production issues, they often waste tokens fumbling across tools and hallucinating about system topology. AI-Ready Infrastructure Context is the practice of pre-generating structured, machine-readable snapshots (Markdown) of your entire environment—monitoring dashboards, K8s manifests, DB schemas—so the agent has instant, grounded context before it starts reasoning.

---

## Working Knowledge

### 1. The "Sync" Pattern (Droidctx)

Infrastructure context should be generated via a single command (e.g., `droidctx sync`) that connects to production tools and extracts metadata into `.md` files.

#### Data Sources

- Monitoring: Grafana (dashboards, alerts), DataDog (monitors, services), CloudWatch.
- Kubernetes: Namespaces, Deployments, Services, Ingresses, HPAs.
- Databases: Table schemas, relationship maps (Postgres, MongoDB).
- CI/CD: ArgoCD application status, GitHub workflow definitions.

### 2. Output Structure

Snapshots are organized by connector and cross-referenced by service name:

```sh
resources/
  overview.md                    # Summary of all connected tools
  connectors/
    k8s_production/
      _summary.md                # Counts and health status
      namespaces.md              # Topology map
      deployments.md             # Resource limits and images
    grafana_prod/
      dashboards/
        api-gateway.md           # Panels and queries in text form
  cross_references/
    services.md                  # Unified view of a service across tools
```

### 3. Integration with Agents

The context path is documented in the agent's core instructions (e.g., `CLAUDE.md` or `GEMINI.md`):

> "My production infrastructure context is in `./my-infra/resources/`. Refer to this when investigating issues, writing queries, or understanding system topology."

---

## Current Understanding

### Benefits

- Token Efficiency: Tiered summaries prevent dumping thousands of lines of YAML into the context window.
- Hypothesis Quality: The agent starts with "what is" rather than "what might be."
- Query Generation: Accurate DB schemas and monitoring queries because the agent sees the actual table names and metric identifiers.

### Requirements

- CLI Mode: Tools should ideally use local kubeconfig or cloud CLI credentials (`az`, `aws`, `gcloud`) to extract data without requiring dedicated service account tokens for the generation phase.

## Related Documentation

- [[SoT - LLM Codebase Understanding & Hierarchy]]
- [[SoT - Cloud-Native Observability]]
- [[_link_report_agent_first_workflow]]
