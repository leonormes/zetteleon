---
aliases: []
created: 2025-02-07T12:57:56Z
last_reviewed: ""
modified: 2026-04-09T07:46:45+00:00
prodos: {kind: atomic, lifecycle: seedling, trust: working, id: "", review: {interval: "", last_reviewed: ""}, chronos: {last_synthesis: "", synthesis_count: 0}, atomic: {form: concept}, protocol: {applies_to: [], binary_checklist: true}, moc: {hub_for: [], entry_points: []}, ops: {tool: "", target_service: "", hop_level: "", requires_tunnel: false, prerequisites: []}, prompt: {description: "", inject_as: "", model_hints: ""}, project: {area: "", status: "", owner: ""}}
see_also: []
status: ""
superseded_by: ""
supersedes: ""
tags: []
title: kubernetes_dashboard_security
type: ""
updated: 
---

## Kubernetes Dashboard Security

Content: The Kubernetes dashboard should not be publicly exposed without additional authentication. RBAC should be used to restrict access, and the dashboard's service account should not have excessive privileges.

Context: From the provided text on securing the Kubernetes API.

---

Connections: ->

---

[kubernetes_security](kubernetes_security.md)
