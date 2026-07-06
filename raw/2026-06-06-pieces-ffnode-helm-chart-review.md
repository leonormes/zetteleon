---
created: 2026-06-06T07:05:55+00:00
modified: 2026-07-04T10:49:24+00:00
permalink: llmeon/raw/2026-06-06-pieces-ffnode-helm-chart-review
pieces_ids: [25097810-5b9e-45cd-abad-4b192f6dcaab, 93d2d954-0552-4f79-a85f-8a1a1b2e688b, e0986954-c470-4e01-827d-914248b200e8, e80bcd4e-9cbb-4096-af77-8eb8e41ac2ec]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-06-06-pieces-ffnode-helm-chart-review
---

## Ffnode Helm Chart Review—Claude Code Prompt & Library Chart Analysis

### Asset 1—User Prompt (07:05:55)

over the passed few days ollie and I have worked on the helm deployment for the faro and alloy helm chart. Give me a llm prompt for claude code to analyse and review the helm chart tpl and config. I have a feeling it is too complicated and that only Ollie understands it. Get the llm to review all the changes via git history. Get it to summarise how the templating is working for our charts and to describe the patterns we are using. Create a md note in obsidian of the findings. My goal is to have a type safe and flexible process for managing multiple k8s clusters.

### Asset 2—Agent Synthesis: Claude Code Prompt & Obsidian Note (07:13:48)

The Obsidian directory is confirmed at `/Volumes/DAL/Zettelkasten/LLMeon/30_Library/200_projects/00_Active_Projects/Refined Deployment/` and no existing `ffnode-helm-chart-analysis.md` file was found. Here is the complete note—paste it directly into that directory as `ffnode-helm-chart-analysis.md`:

---

```markdown
---
title: "ffnode Helm Chart — Templating Analysis & Claude Code Review Prompt"
created: 2026-06-06T08:05:00+01:00
modified: 2026-06-06T08:05:00+01:00
tags: [helm, kubernetes, grafana-alloy, faro, ffnode, templating, observability, multi-cluster, FTFL-673, seedling, work]
kind: project-note
lifecycle: active
ticket: FTFL-673
branch: feature/FTFL-673-grafana-alloy-upgrade
mr: "!787"
related:
  - "[[Grafana k8s-monitoring v2]]"
  - "[[grafana_alloy_audit_report]]"
---

## Context

Over 4–5 Jun 2026 you and Ollie Rushton worked on `FTFL-673 — grafana alloy upgrade and frontend observability` ([GitLab MR !787](https://gitlab.com/fitfile/deployment/-/merge_requests/787), branch `feature/FTFL-673-grafana-alloy-upgrade`).

The work added Faro frontend observability to the `ffnode` umbrella chart — the chart that manages every FITFILE k8s cluster via ArgoCD. The chart is complex, largely Ollie's invention, and currently hard for anyone else to reason about independently.

Your goal: have a type-safe, self-documenting, multi-cluster-safe process for managing k8s observability configuration across all clusters.

### What was changed (FTFL-673 summary)

| File | Change |
|------|--------|
| `charts/ffnode/templates/grafana-alloy-application.yaml` | Renamed from `grafana-application.yaml`; bumped `targetRevision` to `4.1.4`; now references `_grafana.tpl` helper |
| `charts/ffnode/templates/_grafana.tpl` | New helper `ffnode.grafana.values` — builds the entire `k8s-monitoring` values block |
| `charts/ffnode/templates/_certs.tpl` | Conditionally appends cert-manager certificate for Faro ingress |
| `charts/ffnode/templates/_frontend.tpl` | Added `ffnode.frontend.faroSecret` helper — injects FARO_COLLECTOR_TOKEN from Vault |
| `charts/ffnode/templates/_ffcloud.tpl` / `_fitconnect.tpl` | Updated `allowedOrigin` configuration |
| `charts/ffnode/values.yaml` | Added `grafanaAlloy.frontendobservability` block |
| `ffnodes/fitfile/ff-test-a/values.yaml` | Enabled frontendobservability in staging/test |
| `infrastructure/central-services/cloudflare/locals.tf` | Added Faro DNS A-records |
| `infrastructure/production/mkuh-prd-4/generated/values.yaml` | Alloy upgrade committed on branch |

Bugs hit: fromYaml arity error, $out undefined, VSO double-evaluation bug (`secretTransformationDisableTpl` fix), type coercion in `_grafana.tpl`.

### Templating patterns used

1. Named template as values factory — `_grafana.tpl` builds YAML via `mergeOverwrite + fromYaml + toYaml` chain. Risk: type mismatches silently drop keys.
2. Feature-flag gating — `grafanaAlloy.frontendobservability.enabled: false` default in values.yaml.
3. Vault secret injection via tpl — `generateVaultDynamicSecrets` applies `tpl()` to secret transformations; bare `{{get .Secrets "key"}}` expressions crash without `secretTransformationDisableTpl: true`.

### Claude Code Review Prompt

A comprehensive prompt was produced for Claude Code to:
1. Review all `ffnode` chart templates and cluster-specific overrides
2. Analyse git history for complexity trends
3. Assess whether Helm library charts could replace the umbrella patterns
4. Recommend a migration sequence
5. Audit for the VSO double-evaluation bug across all 27 clusters
```

### Asset 3—User Follow-up Question (07:26:14)

Could library charts replace our current umbrella templating patterns?

### Asset 4—Agent Synthesis: Library Chart Verdict (07:41:26)

The March 2026 hotfix evidence is the missing piece that makes the library chart argument conclusive. The `secretTransformationDisableTpl` fix was not a one-time patch—it was a manual chase across individual cluster `render_fitfile.cue` files after each cluster hit the VSO corruption bug in production. LTM confirms at least two clusters required explicit remediation: LCA-DP and mkuh-prod-4 (March 2026 Cursor session).

Final verdict: Library charts partially replace the umbrella patterns—but the more important immediate win is making `disableTpl: true` the default inside the library, so the bug that has already hit LCA-DP and mkuh-prod-4 cannot be reintroduced by any future cluster onboarding. The App-of-Apps topology and the per-cluster override mechanism stay as-is. The library chart refactor addresses only the named template layer—and on that layer, it is the correct and sufficient answer.
