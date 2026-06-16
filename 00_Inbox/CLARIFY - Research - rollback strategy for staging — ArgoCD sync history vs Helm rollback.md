---
created: 2026-06-11T14:48:39+00:00
title: "CLARIFY - Research: rollback strategy for staging — ArgoCD sync history vs Helm rollback vs Git revert"
tags: [clarify, todoist-inbox]
type: clarify
---

Imported from Todoist inbox on 2026-06-11 15:48.

## Description

Current problem: can't easily roll back staging when something breaks. Goal: define a fast, reliable rollback mechanism.

Starting questions:
- Is staging managed by ArgoCD? If so, `argocd app rollback` to a previous sync revision is the obvious first move.
- If Helm-managed: `helm rollback <release> <revision>` — but what's the revision tracking story?
- Is a Git revert + re-sync a better audit trail?
- Should rollback be a manual step or a pipeline stage with a trigger?

## Next Action

Review and clarify what this means, then take action.

