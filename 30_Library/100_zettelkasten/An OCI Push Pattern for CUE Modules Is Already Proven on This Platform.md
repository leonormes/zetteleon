---
conformant: true
created: 2026-09-23T14:49:38+00:00
created_utc: '2026-09-23T00:00:00Z'
modified: 2026-09-23T14:56:28+00:00
permalink: llmeon/00-inbox/an-oci-push-pattern-for-cue-modules-is-already-proven-on-this-platform
source_title: Multi-customer Deployment Review, and an Assessment of CUE
source_url: N/A — internal engineering assessment
status: seed
tags: [ci-cd, cue, oci]
title: An OCI Push Pattern for CUE Modules Is Already Proven on This Platform
type: claim
upstream: '[[CUE-ASSESSMENT]]'
---

## An OCI Push Pattern for CUE Modules Is Already Proven on This Platform

The registry credentials and immutability pattern needed to publish a versioned CUE module already exist on this platform, because a prior initiative demonstrated pushing OCI Helm artefacts to the same Azure Container Registry with immutability enforced.

### Scope & Conditions

Refers specifically to a prior CI initiative (`FTFL-1008 Phase 1`).

### Evidence

> "`cue mod publish` pushes a CUE module to an OCI registry, and `FTFL-1008 Phase 1` … has already demonstrated that `AZ_CLIENT_ID` can push OCI Helm artefacts to `fitfileregistry.azurecr.io` with immutability enforced. Same registry, same credentials, same pattern."

### Implications

- Publishing a CUE module as an OCI artefact requires no new infrastructure, only reuse of an existing pattern.

### Related

- [[Unversioned CUE Included Per-Repo Has Already Forked Between Two Copies]]—extends: this proven pattern is the specific fix for that fork.
- [[SoT - Generative Infrastructure Configuration Framework]]—extends: supports the module-publishing route to the "One Home" principle for shared logic, not just shared data.
