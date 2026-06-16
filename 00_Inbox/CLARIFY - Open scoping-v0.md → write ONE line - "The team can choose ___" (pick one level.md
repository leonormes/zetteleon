---
created: 2026-06-11T14:48:39+00:00
title: "CLARIFY - Open scoping-v0.md → write ONE line: "The team can choose ___" (pick one level from notes), then close the file"
tags: [clarify, todoist-inbox]
type: clarify
---

Imported from Todoist inbox on 2026-06-11 15:48.

## Description

**PROJECT (one-layer fog)** — not a quick prep job. The fog is *scope*, not facts: decide it at the desk, don't go dig for anything.

**"CI/CD options" sits at ONE of these levels. Picking the level = the scope. Job is to eliminate three:**
1. **Runner / platform** — GitHub Actions vs Azure DevOps vs GitLab CI vs Tekton
2. **GitOps delivery** — ArgoCD (incumbent) vs Flux; app-of-apps vs ApplicationSets; sync strategy ⚠️ *your ArgoCD auto-sync race hazard lives here — load-bearing, not academic*
3. **Pipeline architecture** — per-service vs mono; build-once-promote; promotion model
4. **Practice / policy** — trunk-based, release gating, DQ gates, in-pipeline scanning (Trivy slots here)

**Traps in the original wording:** "options" → comprehensiveness spiral; "for the team" → evaluation stakes. So bound hard, write the ONE line, then stop. "Write nothing else" is the off-switch.

**If the blank won't fill** → it's secretly two-layer (like the Trivy item). Real first leaf becomes a one-line message to whoever owns the team's CI/CD pain — not a doc.

## Next Action

Review and clarify what this means, then take action.

