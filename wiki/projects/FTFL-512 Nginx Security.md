---
title: FTFL-512 Nginx Security
wiki_type: dossier
entity_kind: project
created: 2026-06-01 22:06:18+00:00
modified: 2026-06-01 22:06:18+00:00
tags:
- wiki
- dossier
- security
- ftfl
- nginx
sources:
- raw/2026-06-01-pieces-ftfl-512-nginx-infodisclosure
permalink: llmeon/wiki/projects/ftfl-512-nginx-security
---

## Summary

FITFILE security ticket to remediate nginx information disclosure on `sandbox-testing-1.fitfile.net`. A basic `curl` to the domain returns a 302 response that exposes the nginx server banner (`<hr><center>nginx</center>`). The fix involves adding a `server-snippet` annotation with `server_tokens off` to the Helm ingress template, but this is blocked by an ingress-nginx admission webhook that forbids snippet annotations cluster-wide.

## Key Facts

- **2026-06-01T13:31** — Fix identified: add nginx.ingress.kubernetes.io/server-snippet annotation with server_tokens off
  > "Fix identified: add nginx.ingress.kubernetes.io/server-snippet annotation with server_tokens off" — [[raw/2026-06-01-pieces-ftfl-512-nginx-infodisclosure]] (Pieces: 7cafab12-f27f-4b01-bbd7-ea1087d5a86f)
- **2026-06-01T13:31** — Root cause: admission webhook blocking server-snippet annotations cluster-wide — allow-snippet-annotations is set to false in ingress-nginx
  > "Root cause: admission webhook blocking server-snippet annotations cluster-wide — allow-snippet-annotations is set to false in ingress-nginx" — [[raw/2026-06-01-pieces-ftfl-512-nginx-infodisclosure]] (Pieces: 7cafab12-f27f-4b01-bbd7-ea1087d5a86f)
- **2026-06-01T13:31** — ArgoCD shows sandbox-testing-1-frontend OutOfSync after pushing server-snippet changes to Helm ingress template
  > "ArgoCD shows sandbox-testing-1-frontend OutOfSync after pushing server-snippet changes to Helm ingress template" — [[raw/2026-06-01-pieces-ftfl-512-nginx-infodisclosure]] (Pieces: 7cafab12-f27f-4b01-bbd7-ea1087d5a86f)
- **2026-06-01T13:31** — kubectl patch application used to force ArgoCD sync instead of argocd CLI
  > "kubectl patch application used to force ArgoCD sync instead of argocd CLI" — [[raw/2026-06-01-pieces-ftfl-512-nginx-infodisclosure]] (Pieces: 7cafab12-f27f-4b01-bbd7-ea1087d5a86f)
- **2026-06-01T11:34** — curl test confirms nginx body disclosure — 302 response reveals "<hr><center>nginx</center>"
  > "curl test confirms nginx body disclosure — 302 response reveals "<hr><center>nginx</center>"" — [[raw/2026-06-01-pieces-ftfl-512-nginx-infodisclosure]] (Pieces: 1e442f42-03b5-47d2-8597-ed9956d98c52)

## Timeline

- **2026-06-01** — curl test confirms nginx body disclosure still present on sandbox-testing-1.fitfile.net
- **2026-06-01** — Identified server-snippet annotation with `server_tokens off` as the fix in Helm ingress template
- **2026-06-01** — Discovered admission webhook blocks server-snippet annotations cluster-wide (`allow-snippet-annotations: false`)
- **2026-06-01** — Pushed changes to Helm ingress template; ArgoCD shows sandbox-testing-1-frontend OutOfSync
- **2026-06-01** — Attempted kubectl patch to force ArgoCD sync; annotation still not appearing on live ingress object
- **2026-06-01** — nginx ingress controller config checked — annotation not present in nginx.conf on the controller pod

## Connections

- [[FTFL-511 Nginx HTTPS Hardening]] — companion FTFL security ticket
- [[FTFL-511-512 Security Scan]] — combined security scanning context
- [[FITFILE-Testing-Infrastructure]] — parent FITFILE infrastructure project
- [[Azure-AKS]] — AKS cluster hosting the ingress

## Contradictions

None identified.

## Open Questions

- How to resolve the admission webhook blocking — does `allow-snippet-annotations` need to be changed at the ingress-nginx ConfigMap level, or is there an alternative annotation approach?
- Should `server_tokens` be disabled at the nginx ConfigMap level globally rather than per-ingress via server-snippet?
- Is there a different annotation key (e.g., `nginx.ingress.kubernetes.io/configuration-snippet`) that is not blocked?