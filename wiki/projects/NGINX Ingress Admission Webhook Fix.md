---
title: NGINX Ingress Admission Webhook Fix
wiki_type: dossier
entity_kind: project
created: 2026-06-01T17:58:23+00:00
modified: 2026-06-01T17:58:23+00:00
tags: [wiki, dossier]
sources: [raw/2026-06-01-pieces-nginx-ingress-webhook-fix]
---

## Summary

Investigation and fix for a failing ArgoCD sync caused by an NGINX Ingress admission webhook rejection. The cluster's NGINX Ingress Controller has snippet annotations disabled (`allowSnippetAnnotation: false`), causing Ingress manifests with `server-snippet` annotations to be rejected. Work is scoped to IaC-only changes (Helm charts, Kustomize overlays, or raw YAML in Git), since the target cluster is on a private network with no direct `kubectl` access.

## Key Facts

> "Good constraint to lock in. The prompt needs to drop all `kubectl` live-cluster operations and pivot entirely to **IaC-only changes** — find the files in the repo, rewrite them, and let ArgoCD's own sync verify the fix.  ---  ## Revised Hermes Prompt…" — [[raw/2026-06-01-pieces-nginx-ingress-webhook-fix]] (Pieces: 24a8b712-f922-40e9-a6b6-06e57e2445ee)
> "The user is clarifying that Hermes (the LLM agent) cannot directly interact with the cluster (since it's on a private network), so it can only modify the Infrastructure as Code (IaC) — likely Helm charts, Kustomize overlays, or raw YAML manifests in…" — [[raw/2026-06-01-pieces-nginx-ingress-webhook-fix]] (Pieces: 212a7336-2663-4126-bf24-4d95d7bd9a0e)
> "the cluster is on a private network so hermes can only update the IaC rather than directly the cluster.…" — [[raw/2026-06-01-pieces-nginx-ingress-webhook-fix]] (Pieces: 1c378604-c5d5-4d62-92b3-1fb8df02a019)
> "## Hermes Prompt — NGINX Ingress Snippet Webhook Fix  Copy-paste ready. Works with Nous-Hermes 2, OpenHermes, or any ChatML-compatible model (Cursor, LM Studio, Ollama, etc.).  ---  ````text <|im_start|>system You are an expert Kubernetes and NGINX I…" — [[raw/2026-06-01-pieces-nginx-ingress-webhook-fix]] (Pieces: d01de85a-1e3f-4049-9b89-7db7ae06f70d)
> "The user wants me to create a "Hermes prompt" to investigate and fix the NGINX Ingress admission webhook issue described. A "Hermes prompt" typically refers to a prompt formatted for use with the Hermes/Nous-Hermes model family, or more generally, a…" — [[raw/2026-06-01-pieces-nginx-ingress-webhook-fix]] (Pieces: e5500e50-e1fb-47e8-b6b2-9a37ce280806)
> "give me a hermes prompt to investigate and fix this This is coming from the **NGINX Ingress admission webhook**, not ArgoCD itself. Argo is just surfacing the failure during the sync.  ### What the error means  ``` admission webhook "validate.nginx.i…" — [[raw/2026-06-01-pieces-nginx-ingress-webhook-fix]] (Pieces: 43a78b56-55a4-4e96-a5f6-b615de3f741f)

## Timeline

- 2026-06-01 — User began designing a Hermes-formatted prompt to investigate and fix the NGINX Ingress admission webhook rejection, scoped to IaC-only operations on a private network cluster.

## Connections

- [[FTFL-511 Nginx HTTPS Hardening]] — related NGINX Ingress hardening workstream
- [[Azure AKS Backup — FTFL]] — same FTFL project family, ArgoCD-based deployment
- [[ArgoCD]] — deployment tool surfacing the webhook rejection

## Contradictions

None identified.

## Open Questions

- Which specific Ingress manifest(s) contain the snippet annotations that need removing or replacing?
- Is the fix to remove snippet annotations, replace them with whitelist-safe alternatives, or reconfigure the Ingress Controller to allow snippets?
- What is the exact FTFL ticket reference for this piece of work?
