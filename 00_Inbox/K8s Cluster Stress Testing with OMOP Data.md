---
captured: "2026-05-23T13:00:10+01:00"
created: 2026-05-23T12:03:25+00:00
modified: 2026-05-23T12:16:15+00:00
related: ["[[Azure Entra IAM Overhaul]]", "[[DevOps Projects MOC]]", "[[GTD — Natural Planning Model]]", "[[K8s Stress Testing]]"]
source: "https://gemini.google.com/app/18d0fc49e39be5bb"
status: "processed"
tags: ["azure-entra", "break-glass", "devops", "execution-protocol", "gitops", "gtd", "iac", "kubernetes", "natural-planning-model", "omop", "pim"]
title: pieces_copilot_message_export_may_23_2026_1_03pm
type: "note"
---

## Summary

A working session applying the GTD Natural Planning Model across three complex summer engineering projects, followed by a deep-dive blueprint for a best-in-class Entra ID break-glass account, and a personal execution protocol to overcome initiation difficulty on high-friction technical work.

---

## Projects Clarified

### 1. K8s Cluster Stress Testing with OMOP Data

Goal: Validate stability and resilience of distributed Kubernetes clusters under large OMOP data loads.

| Phase | Key Questions / Actions |
|---|---|
| Purpose & Principles | Why now? Peak clinical data loads? Data pipeline resilience? Non-negotiables: data privacy, zero prod disruption, compute cost cap |
| Vision | Comprehensive cluster behaviour report, identified breaking points, tuned config |
| Brainstorm | DevOps + data scientists + network specialists; K8s pod eviction thresholds; OMOP data distributions; risks: cascading crashes, data corruption, OOM |
| Organise | Timing, hard deadlines, ownership, tooling (Grafana/Prometheus, load gen tools, node scaling) |
| Next Action | _"Draft email to DevOps lead to schedule whiteboard session on K8s load testing parameters."_ |

---

### 2. GitOps Deployment Pipeline Optimisation

Goal: Improve a live GitOps process—investigation first, then incremental optimisation without disrupting team delivery.

| Phase | Key Questions / Actions |
|---|---|
| Purpose & Principles | Reduce lead time? Improve deployment frequency? Eliminate manual bottlenecks? No big-bang replacements—incremental only |
| Vision | Immediate dev feedback, seamless ArgoCD reconciliation, zero config drift. Measure via Four Key Metrics (deployment frequency, lead time, MTTR, change fail rate) |
| Brainstorm | Current state vs. documented state; queue/wait time analysis; CI/CD architecture review; trunk-based dev vs. long-lived branches; secrets management in K8s |
| Organise | Phase A: Value stream mapping + metric baseline → Phase B: CI feedback loop (parallelise test suites) → Phase C: CD sync policies & manifest management |
| Next Action | _"Schedule 60-min value stream mapping session to trace a single commit from workstation to production."_ or _"Run query to extract average build times for last 30 days."_ |

---

### 3. Azure Entra ID IAM → IaC + PIM Migration

Goal: Move Entra ID configuration to Infrastructure as Code, implement PIM for privileged access, and tidy stale policies.

| Phase | Key Questions / Actions |
|---|---|
| Purpose & Principles | Post-audit? Stop portal config drift? Zero Trust architecture? Non-negotiable: all IAM changes via pull request, no standing human privileges |
| Vision | All Conditional Access, App Registrations, Enterprise Apps in Terraform/Bicep. PIM gates all elevation. Standing Global Admin eradicated |
| Brainstorm | Stale guest accounts, undocumented groups, conflicting CA policies; Terraform AzureAD provider nuances; pipeline auth to Entra without creating a security risk |
| Organise | Phase A: Audit & tidy (delete dead weight manually first) → Phase B: Break-glass + baseline alerting → Phase C: PIM rollout (eligible roles, approval workflows) → Phase D: Codification (import existing state) |
| Next Action | _"Run PowerShell script to export CSV of all Global Admin and Privileged Role Admin assignments."_ or _"Create empty git repo for Entra IaC project."_ |

> Tooling decision needed: Terraform (AzureAD provider) vs. Bicep?

---

## Break-Glass Account Blueprint

> Prerequisite: Complete this before making any IaC or Conditional Access changes.

### Phase 1—Account Architecture

- Create exactly two emergency access accounts (redundancy is mandatory)
- Use `*.onmicrosoft.com` domain only—no custom/federated domain
- Cloud-only—never sync from on-premises AD
- Standing Global Administrator—do NOT put behind PIM (if PIM breaks, you cannot elevate)

### Phase 2—Policy Exclusions

- Explicitly exclude from ALL Conditional Access policies
- Exclude from standard MFA policies (use physical hardware keys instead—see below)
- Consider an "emergency" management group exempt from standard policy scope

### Phase 3—Credential Security

- Generate a 30+ character random password (upper, lower, numbers, symbols)
- Bind a FIDO2 hardware security key (e.g. YubiKey)—not Authenticator App
- Physical storage only—printed paper + FIDO2 key in a physical safe
- Split knowledge: give one password half to CTO/CISO, other half to a second senior executive or architect, stored in separate physical locations
- Use two separate authentication methods—do not rely on a single method for both accounts

### Phase 4—Monitoring Tripwire

- Azure Monitor alert rule targeting Entra ID Sign-in logs, filtered on the specific Object IDs of the break-glass accounts
- Route alert to highest-priority incident tool (PagerDuty / Opsgenie) AND a dedicated Slack/Teams channel
- Alert must fire within seconds of any sign-in

### Phase 5—Lifecycle & Maintenance

- 90-day drill: scheduled recurring calendar event to test sign-in and validate the monitoring tripwire fires
- Verify account still holds Global Admin role on each drill
- Immediately rotate password and FIDO2 keys after every drill or genuine use; return new credentials to the physical safe
- Document the process fully so the team can execute under pressure

---

## Execution Protocol—Getting High-Friction Work Started

Designed for initiating large, ambiguous engineering projects when task-start resistance is high.

### Phase 1—Pre-Flight (State Management)

- Acknowledge the overwhelm explicitly—don't suppress it
- Use brief physical movement (e.g. a brisk walk) as a neurological reset before beginning

### Phase 2—Walking Skeleton Initiation

- Timebox to 15–25 minutes, executing only the single atomic next action identified in planning
- Goal is overcoming inertia, not architectural perfection
- _Start now, get perfect later_

### Phase 3—The Unschedule

- Schedule breaks, meals, and leisure first—then schedule work around them
- The guaranteed endpoint removes dread; replaces open-ended grind with bounded, purposeful effort

### Phase 4—Radical WIP Limits

- Treat personal attention like a delivery pipeline—strictly finite throughput
- Work on one major project at a time
- Creatively neglect the others until the active project reaches a defined, testable milestone

---

## Open Loops / Next Actions

- [ ] Decide IaC tooling: Terraform vs. Bicep for Entra
- [ ] Create two break-glass accounts before any Entra/CA changes
- [ ] Establish Log Analytics alert on break-glass Object IDs
- [ ] Export current Global Admin + Privileged Role Admin CSV
- [ ] Schedule value stream mapping session (GitOps pipeline)
- [ ] Draft K8s load testing scoping email to DevOps lead
- [ ] Pick one project to start—apply WIP limit, run 25-min timebox

---

_Captured from Gemini chat · 2026-05-23 · Processed by Pieces_

```
