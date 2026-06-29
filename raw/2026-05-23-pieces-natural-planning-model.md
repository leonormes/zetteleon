---
created: 2026-05-23 12:02:54+00:00
modified: 2026-05-26 11:43:32+00:00
pieces_ids:
- 201d6e29-282f-4295-8bf1-44282a6752d3
- 49049282-6f30-48f6-8a68-c5cc68b79bb8
source: pieces-ltm
tags:
- pieces
- raw
title: 2026-05-23-pieces-natural-planning-model
permalink: llmeon/raw/2026-05-23-pieces-natural-planning-model
---

## Complex Projects—Natural Planning Model & Execution Protocol

Captured from Gemini chat session (<https://gemini.google.com/app/18d0fc49e39be5bb>) on 2026-05-23. User applied the GTD Natural Planning Model across three complex summer engineering projects, requested a break-glass account blueprint, and designed a personal execution protocol for high-friction technical work.

### Asset 1 (Pieces: 49049282-6f30-48f6-8a68-c5cc68b79bb8)

Full structured note from Gemini chat covering:

#### Projects Clarified

1. K8s Cluster Stress Testing with OMOP Data

- Goal: Validate stability and resilience of distributed Kubernetes clusters under large OMOP data loads.
- Key phases: Purpose & Principles (data privacy, zero prod disruption, compute cost cap), Vision (comprehensive cluster behaviour report, identified breaking points, tuned config), Brainstorm (DevOps + data scientists + network specialists; K8s pod eviction thresholds; OMOP data distributions; risks: cascading crashes, data corruption, OOM), Organise (timing, hard deadlines, ownership, tooling: Grafana/Prometheus, load gen tools, node scaling), Next Action: "Draft email to DevOps lead to schedule whiteboard session on K8s load testing parameters."

2. GitOps Deployment Pipeline Optimisation

- Goal: Improve a live GitOps process—investigation first, then incremental optimisation without disrupting team delivery.
- Key phases: Purpose & Principles (reduce lead time, improve deployment frequency, eliminate manual bottlenecks; no big-bang replacements), Vision (immediate dev feedback, seamless ArgoCD reconciliation, zero config drift; Four Key Metrics), Brainstorm (current state vs documented state; queue/wait time analysis; CI/CD architecture review; trunk-based dev vs long-lived branches; secrets management in K8s), Organise (Phase A: Value stream mapping + metric baseline → Phase B: CI feedback loop → Phase C: CD sync policies & manifest management), Next Action: "Schedule 60-min value stream mapping session" or "Run query to extract average build times for last 30 days."

3. Azure Entra ID IAM → IaC + PIM Migration

- Goal: Move Entra ID configuration to Infrastructure as Code, implement PIM for privileged access, and tidy stale policies.
- Key phases: Purpose & Principles (post-audit, stop portal config drift, Zero Trust; all IAM changes via pull request, no standing human privileges), Vision (all Conditional Access, App Registrations, Enterprise Apps in Terraform/Bicep; PIM gates all elevation; standing Global Admin eradicated), Brainstorm (stale guest accounts, undocumented groups, conflicting CA policies; Terraform AzureAD provider nuances; pipeline auth to Entra), Organise (Phase A: Audit & tidy → Phase B: Break-glass + baseline alerting → Phase C: PIM rollout → Phase D: Codification), Next Action: "Run PowerShell script to export CSV of all Global Admin and Privileged Role Admin assignments" or "Create empty git repo for Entra IaC project."
- Tooling decision needed: Terraform (AzureAD provider) vs Bicep?

#### Break-Glass Account Blueprint

Phase 1—Account Architecture:

- Create exactly two emergency access accounts (redundancy mandatory)
- Use `*.onmicrosoft.com` domain only—no custom/federated domain
- Cloud-only—never sync from on-premises AD
- Standing Global Administrator—do NOT put behind PIM

Phase 2—Policy Exclusions:

- Explicitly exclude from ALL Conditional Access policies
- Exclude from standard MFA policies (use physical hardware keys instead)
- Consider an "emergency" management group exempt from standard policy scope

Phase 3—Credential Security:

- Generate 30+ character random password
- Bind a FIDO2 hardware security key (e.g. YubiKey)
- Physical storage only—printed paper + FIDO2 key in a physical safe
- Split knowledge: one password half to CTO/CISO, other half to second senior executive
- Use two separate authentication methods

Phase 4—Monitoring Tripwire:

- Azure Monitor alert rule targeting Entra ID Sign-in logs, filtered on specific Object IDs
- Route alert to highest-priority incident tool (PagerDuty/Opsgenie) AND dedicated Slack/Teams channel
- Alert must fire within seconds of any sign-in

Phase 5—Lifecycle & Maintenance:

- 90-day drill: scheduled recurring calendar event to test sign-in and validate monitoring tripwire
- Verify account still holds Global Admin role on each drill
- Immediately rotate password and FIDO2 keys after every drill or genuine use
- Document the process fully

#### Execution Protocol—Getting High-Friction Work Started

Phase 1—Pre-Flight (State Management):

- Acknowledge the overwhelm explicitly
- Use brief physical movement (brisk walk) as neurological reset

Phase 2—Walking Skeleton Initiation:

- Timebox to 15–25 minutes, executing only the single atomic next action
- Goal is overcoming inertia, not architectural perfection

Phase 3—The Unschedule:

- Schedule breaks, meals, and leisure first—then schedule work around them
- Guaranteed endpoint removes dread

Phase 4—Radical WIP Limits:

- Treat personal attention like a delivery pipeline—strictly finite throughput
- Work on one major project at a time
- Creatively neglect others until active project reaches defined milestone

#### Open Loops / Next Actions

- [ ] Decide IaC tooling: Terraform vs Bicep for Entra
- [ ] Create two break-glass accounts before any Entra/CA changes
- [ ] Establish Log Analytics alert on break-glass Object IDs
- [ ] Export current Global Admin + Privileged Role Admin CSV
- [ ] Schedule value stream mapping session (GitOps pipeline)
- [ ] Draft K8s load testing scoping email to DevOps lead
- [ ] Pick one project to start—apply WIP limit, run 25-min timebox

### Asset 2 (Pieces: 201d6e29-282f-4295-8bf1-44282a6752d3)

Raw user query and Gemini response covering the same three projects with Natural Planning Model trigger lists. Includes the user's original request for help with K8s/OMOP stress testing initiation, GitOps pipeline optimisation, and Azure Entra IAM migration. Also includes the break-glass account plan with references and the execution protocol request.