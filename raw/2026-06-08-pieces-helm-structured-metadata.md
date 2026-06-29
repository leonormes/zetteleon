---
title: Helm Chart Structured Metadata Experiment
created: 2026-06-08 11:00:00+00:00
source: pieces-ltm
pieces_ids:
- f220d2f8-0c00-4239-95c8-602328fcb022
- c0470216-6d54-486b-8481-2e67e2bbab2c
- 4fb49ed6-54b6-482d-ade0-8111a2afb146
- aba394bc-3ca8-4995-a8cb-ec622b4fee7c
- 80120449-7b3f-4ebc-8ae5-341e0bce4a46
- 1879599e-0642-4337-b40f-0e2eebfa61e2
- 205e2486-a55f-48bb-996a-6fe0f9ad12c3
- e7af65bf-8a96-4f6f-8834-a03f1031f8e5
- f0c51431-bd39-4155-b09d-d2e03d61fb0a
- ccf9ac96-54bf-4c04-b676-56882a94e5da
tags:
- raw
- pieces
permalink: llmeon/raw/2026-06-08-pieces-helm-structured-metadata
---

# Helm Chart Structured Metadata Experiment — 2026-06-08

Work session investigating structured metadata enrichment for Helm chart deployments to improve Grafana Cloud log context.

## Asset 1 (Pieces: f220d2f8) — 2026-06-08T08:48:25.001Z

User request: "I need a llm prompt with the full and accurate context of how we deploy via argocd and helm"

The user requested a comprehensive context-packaging prompt covering the FITFILE ArgoCD + Helm deployment process to use with another agent (Cursor/Claude Code).

## Asset 2 (Pieces: c0470216) — 2026-06-08T08:59:21.001Z

Copilot synthesised a comprehensive wiki page prompt covering:
- FITFILE Deployment architecture (27 clusters across AKS)
- `ffnode` umbrella chart structure and library chart patterns
- Cluster-specific overlay pattern in `ffnodes/<cluster>/` directories
- ArgoCD ApplicationSets, PR generators, and sync strategies
- Component templates: `_grafana.tpl`, `_certs.tpl`, `_frontend.tpl`
- VSO double-evaluation bug and `secretTransformationDisableTpl: true` fix

## Asset 3 (Pieces: 4fb49ed6, aba394bc) — 2026-06-08T09:17-09:56

User request: "I want to experiment with adding useful structured metadata to our helm charts for all applications so that our grafana cloud logs are richer in context. Give me a small experiment to do and instructions on how"

## Asset 4 (Pieces: 80120449) — 2026-06-08T09:33:20.001Z

Copilot experiment plan — Phase 1: Small Pilot

> ## Small pilot: move one log-context field from label to structured metadata
>
> Use a single, low-risk application (e.g. `spicedb` on testing cluster).
>
> **Current state:** Labels like `app`, `namespace`, `cluster` are used as Loki stream labels (indexed, high-cardinality risk)
>
> **Target state:** Relocate low-cardinality context fields (e.g., `app_version`, `deployment_strategy`, `git_sha`) from labels to structured metadata (non-indexed, per-line)
>
> Steps:
> 1. Pick one app (`spicedb` in `fitfiletest`)
> 2. Add `structuredMetadata` block to its Helm values
> 3. Update Alloy pipeline to promote `app_version` to structured metadata
> 4. Verify with `gcx logs query`

## Asset 5 (Pieces: 1879599e) — 2026-06-08T09:43:42.001Z

Phase 2: reusable helper and safety rails

- Define a shared `structuredMetadata` block in Helm values
- Use a library chart template to inject metadata consistently
- Verify that the Alloy pipeline can consume structured metadata

## Asset 6 (Pieces: 205e2486) — 2026-06-08T09:45:17.001Z

Phase 2: pilot execution in `fitfiletest`

- Put the canary in one overlay only
- Validate with `helm template` before deploying
- Use `gcx logs query` to verify metadata appears

## Asset 7 (Pieces: e7af65bf) — 2026-06-08T09:46:26.001Z

Phase 2: measurement plan

- Record baseline (existing stream labels for the target app)
- After deployment, verify structured metadata fields appear in Loki logs
- Compare cardinality impact

## Asset 8 (Pieces: f0c51431, ccf9ac96) — 2026-06-08T10:01-10:02

User ran loki query to inspect stream labels:

```
gcx logs query --context fitfiletest '{cluster="testing", namespace="spicedb"}' \
  --since 15m --limit 10 -o json | jq '[.[].stream | keys] | flatten | unique'
```

Hit jq error `Cannot index string with string "stream"` — the top-level JSON is not a plain array of stream objects. Analysis indicates element 12 of the `.[]` iteration is a string, not an object with `.stream`.