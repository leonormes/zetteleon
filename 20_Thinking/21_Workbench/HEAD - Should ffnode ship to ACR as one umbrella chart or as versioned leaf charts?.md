---
title: HEAD - Should ffnode ship to ACR as one umbrella chart or as versioned leaf
  charts?
type: question
tension: 'FTFL-1008 asks for charts to be versioned in ACR, which forces a choice
  the ticket does not acknowledge: what the deployable unit actually is. One versioned
  ffnode gives an unambiguous artefact and a one-string rollback, but makes every
  sync all-or-nothing. N versioned leaf charts keep per-component health and rollback,
  but mean the node has no single version number — the thing the ticket literally
  asks for.'
candidate_answers:
- Leaf charts published independently; ffnode stays an app-of-apps whose children
  carry pinned OCI versions
- ffnode collapsed into a real umbrella chart with dependencies and a Chart.lock;
  one Application per node
- 'Both: leaf charts now, umbrella later once change control is stronger'
related_claims: []
sources:
- '[[2026-08-27-fitfile-helm-chart-acr-publishing-audit]]'
- '[[HEAD - The Release Candidate Object]]'
tags:
- state/thinking
- prodos/head
- fitfile
- deployment
- ftfl-1008
conformant: true
prodos:
  kind: head
  lifecycle: active
status: open
AoL: Work
closing_condition: true
created: 2026-08-27 18:42:19+01:00
modified: 2026-08-27 18:42:19+01:00
permalink: llmeon/20-thinking/21-workbench/head-should-ffnode-ship-to-acr-as-one-umbrella-chart-or-as-versioned-leaf-charts
---

## The Question

FTFL-1008 wants Helm charts versioned in ACR with a clear mapping from pipeline run to deployable artefact. Delivering that forces a choice the ticket does not name: **what is the deployable unit — the node, or the component?** Either `ffnode` becomes a real umbrella chart with `dependencies:` and a `Chart.lock`, so one version number denominates everything a node runs; or the leaf charts are published independently and `ffnode` stays an app-of-apps whose children carry pinned OCI versions. The first gives the artefact the ticket asks for and loses operational granularity. The second keeps granularity and means a node has no single version.

## Why It Matters

Downstream of this sits the whole of FTFL-1008 and any future rollback story. It also decides how much of the existing estate has to change: the app-of-apps route is incremental and reuses a path already proven in production, while the umbrella route is a rewrite of `charts/ffnode` and of how every environment is synced. Getting it wrong in the direction of the umbrella is expensive to reverse, because per-component Applications — sync waves, per-app health, per-app rollback — are how a 39-app production estate is currently operated.

It is genuinely mine to decide because it is a risk-appetite judgement, not a lookup: how much blast radius is acceptable in exchange for an unambiguous version number, given a team the audit rates at level 2 on change control and level 1 on secrets.

## What I Currently Think

Leaning strongly to the leaf-chart route, and the research supports it: the OCI path is already live and proven (8 Applications, exact-pinned, Synced/Healthy; `enableOCI: true`; ACR already in the `fitfile` AppProject's `sourceRepos`), so it is incremental rather than novel. Four of six customer environments have *already* moved to ArgoCD multi-source with a separate `chart_target_revision` and `values_target_revision` — the chart/config split is half-built without anyone having framed it as a decision.

What I am less sure of is whether "no single node version" is actually acceptable to the people who will be asked to roll back under pressure, or whether that is me optimising for migration cost and calling it architecture. The umbrella route is the one that makes [[HEAD - The Release Candidate Object]]'s `is_immutable` and deterministic-`id` properties true at the node level; the leaf route only makes them true per component.

## What Would Settle It

1. Convert one non-production node (`ff-test-b` or `ff-test-c`) to pinned OCI leaf charts and **actually perform a rollback under time pressure**. If reverting one component's version string is comfortable and legible, the leaf route is settled. If the operator wants one number to move, it is not.
2. Ask the people who would run that rollback which they would rather hold at 2am — a node version, or a component version.
3. Confirm whether `ffnode` needs a node-level version for any external reason (customer contracts, assurance evidence, NHS DSPT). If a customer must be told "you are running FITFILE 1.4.2", the leaf route needs a synthetic node version anyway, which weakens its advantage considerably.

Item 1 is cheap and reversible; nothing else should be decided before it runs.

## Sources

- [[2026-08-27-fitfile-helm-chart-acr-publishing-audit]] — the evidence base: current topology, the revision graph, staging validated against the live cluster, customer pattern, six defects found.
- [[FITFILE Delivery Pipeline Audit 2026-08-27]] — parent audit; S-07 (credential expiry 2026-10-18), S-13 (no immutable pinning), S-16 (config outside version control).
- [[HEAD - The Release Candidate Object]] — the immutability properties this decision either does or does not satisfy at node level.