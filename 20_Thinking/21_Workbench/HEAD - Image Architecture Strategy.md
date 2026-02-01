---
aliases: []
AoL: Work
created: 2025-12-08T00:00:00Z
last_reviewed:
modified: 2026-02-01T15:09:11+00:00
status: someday
tags: ["SoftwareEngineering/Architecture", docker, head, kubernetes, thinking]
title: HEAD - Image Architecture Strategy
type: head
updated:
---

## The Spark

> [!abstract] The Spark (Contextual Wrapper)
Task: "research image arch differences and how to choose" and "Image arch on import repaired".
We are facing issues where the wrong image architecture (e.g., amd64 vs arm64) might be pulled or imported, causing failures in our K8s clusters.

## My Current Model

- Images are often multi-arch manifests.
- When importing to ACR or pulling to a node, we need to be explicit if the runtime environment is specific.
- Hypothesis: We need a mechanism in our import pipelines to pin the architecture or ensure the multi-arch manifest is preserved correctly.

## The Tension

- Ambiguity: Why is it failing now? Is it the import tool (skopeo/crane?) or the runtime?
- Standard: We need a rule: "Always use multi-arch" OR "Always pin to linux/amd64".

## The Next Test

- [ ] Reproduction: Try to import a known multi-arch image (e.g., alpine) and inspect what actually lands in ACR.
- [ ] Check the flags of our current import tool for architecture selection.
