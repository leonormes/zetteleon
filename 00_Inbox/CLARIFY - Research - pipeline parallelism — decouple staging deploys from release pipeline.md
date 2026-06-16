---
created: 2026-06-11T14:48:39+00:00
title: "CLARIFY - Research: pipeline parallelism — decouple staging deploys from release pipeline"
tags: [clarify, todoist-inbox]
type: clarify
---

Imported from Todoist inbox on 2026-06-11 15:48.

## Description

Current problem: a broken staging environment blocks all releases. Goal: understand patterns for making staging a non-blocking path (e.g. separate ArgoCD AppProjects, independent pipeline triggers, environment-scoped gates).

Starting questions:
- Are staging and prod sharing the same ArgoCD App or pipeline gate?
- Can a staging failure be isolated so it doesn't lock the release pipeline?
- What's the right model: branch-based? label-based? separate repo sync?

## Next Action

Review and clarify what this means, then take action.

