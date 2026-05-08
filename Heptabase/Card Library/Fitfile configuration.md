---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:39+00:00
title: Fitfile configuration
---

## Fitfile Configuration

We use helm charts.

They are pulled and prepared by [ArgoCD.md](ArgoCD.md) in most situations. Once argocd has processed these configurations they are nolonger helm managed resources. ArgoCD turns them into just straightforward old fashioned yaml files.

For each component of [FITFILE](https://app.heptabase.com/c16a6d60-49a6-4aec-9d1a-6161cbbe31a8/card/1c86cbaf-4e38-475a-880a-d16bb1fbc635) we need to turn on the telemetry. In most cases that mean [Prometheus.md](Prometheus.md).

We want to instrument the [Traces.md](Traces.md) for the full system.

![[This makes OpenTelemetry a cross-cutting concern - a piece of software which is mixed into many o]]
