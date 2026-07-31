---
created: 2026-07-31T09:22:16+00:00
modified: 2026-07-31T09:23:47+00:00
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-31-2026-10-22am
title: SRE Observability — Current State & Person-Centric Forward Plan
type: note
---

Window reviewed: ~May 2025–Jul 2026 (LTM)
Stacks: [fitfileprod](https://fitfileprod.grafana.net) · [fitfiletest](https://fitfiletest.grafana.net) (Grafana Cloud org under Gareth Hailes)
Primary ask: people on call, actually looking at alerts, and ongoing maintenance—with a realistic ownership model for this team.

---

## Top-line

You already have a working Grafana IRM + Slack alert path and a strong instrumentation engine (you + Ollie). What's missing is the team operating system: a named rotation, ack norms, runbook hygiene, and maintenance ownership that isn't silently defaulting to you. Alerts fire and frequently invite you alone; severity is split across channels; noisy `DatasourceNoData` and Argo OutOfSync events drown signal; collector/Alloy health is weak (you already flagged a ~31h blind spot to Jim).

---

## Current State (What LTM sHows yOu aCtually dO)

## Alerting & IRM Stack

| Layer | What exists | Evidence |
|---|---|---|
| Alert source | Grafana Cloud Alerting → Grafana IRM / OnCall | Slack `Grafana IRM APP` posts; Oct 2025 IRM setup workstream |
| Chat routing | `#prod-alerts`, `#non-prod-alerts`, `#ops-critical`, `#ops-warnings`, `#ops-optimisation`, `#incident-room`, `#dev-ops` | Slack sidebars across 2025–2026 |
| Actions exposed | Acknowledge · Resolve · Silence · Responders · Declare incident · Add resolution notes · Show timeline | IRM messages in Threads / ops channels |
| Telemetry stack | Alloy (ex-Agent) → Prometheus/Mimir, Loki, Tempo?, Faro RUM, OpenCost (partial), `grafana-k8s-monitoring` Helm | Your FTFL-638/673/698 work; Obsidian observability audits |
| CLI ops surface | `gcx` against fitfileprod/fitfiletest | Cardinality audit 2026-06-05; Agent investigations Jul 2026 |
| Partner | Jim Rawdon (Grafana CSM for FITFILE); OnCall/IRM workshop floated | Email 17 Jun 2026; your 13 Jul follow-up notes |

## Alert Shapes You Repeatedly See

- Argo CD: Persistent OutOfSync, Degraded Applications (staging/testing + prod)—high volumehältnis
- K8s health: `KubePodCrashLooping`, `KubePodNotReady`, `KubeContainerWaiting`, `KubeJobFailed`, `KubeDaemonSetRolloutStuck/MisScheduled`, `KubeDeploymentReplicasMismatch`
- Noise / meta: `DatasourceNoData`, `DatasourceError` (often with empty cluster/namespace/app labels)
- Calico/Tigera: API deprecation warnings, crashloops, missing monitoring StatefulSets
- App-ish: `SDE Relay Error`, Mongo metrics collection failing, compliance-benchmarker failures (historically)

## How People Actually Interact with Alerts (Observed pAttern)

| Person | Role in the alert path today | Pattern |
|---|---|---|
| You (Leon Ormes) | De facto on-call / primary IRM invitee | Grafana IRM repeatedly: _"Inviting leon.ormes@fitfile.com (@Leon Ormes) to look at the alert group."_ You join `#ops-critical`, resolve `InstanceDown`, drive Alloy/Loki/Faro fixes (`FTFL-638`, `FTFL-673`), stress-test observability (`FTFL-698`), EKS observability dashboards. Persona: Senior SRE/Platform—cloud remediation, CI/CD health, governance. |
| Ollie / Oliver Rushton | Observability co-architect & instrumentation owner | Pairing lead on Grafana Alloy upgrades, Faro DNS/certs, OpenCost, Loki structured metadata, workflow inspector, `pg_stat_statements` / `auto_explain`, stress-test dashboards. Asks you for DNS/Route53 unblockers; ships MRs you review. Highest leverage partner for _signal quality_ and _dashboards that matter_. |
| Robin Mofakham | Platform guardian / customer-node ops—not primary pager | Heavy execution on MKUH/NNUH/NWSDE, DNS/SPF/DKIM, access, Terraform. Present in ops-channel participant lists; day-to-day firefighting is node/install connectivity more than IRM rotation. Uses same Signals surface but is under-utilized as a formal on-call peer. |
| Pavlo Kotov | App + data plane escalations | Pipeline/secrets/CI (e.g. expired AAD client secrets → you rotate), OMOP/cohort, stress-test plan contributions. Good secondary responder when alerts map to app/data paths—not first-line infra page today. |
| Weronika Jastrzębska | Channel participant / occasional ops touch | Visible in `#ops-warnings` / `#ops-critical` history; useful for product/context, not primary infra ownership. |
| Gareth Hailes | Grafana Cloud org owner / commercial | Org context for stack billing & access; escaltion path for account limits / Adaptive features. |
| Jim Rawdon (Grafana) | External enablement | Hands-on Grafana support; candidate owner of IRM/OnCall workshop covering silent-failure detection (your 13 Jul note). |

## What's _not_ Evidenced (Important nEgatives)

- No documented multi-person on-call schedule/rotation in LTM (no calendar rotation, no IRM schedule screenshots as a living team artefact).
- Ack/resolution discipline is thin—many IRM messages sit on channel with auto-resolve or invite-you; "Declare incident" is available, rarely used in captured trails.
- Runbooks appear as label/fields on some prod alerts (`HE Runbook`) but ownership, freshness, and coverage of top alert classes are unclear.
- Maintenance cadence for alert hygiene (silence review, flapping rules, DatasourceNoData root-cause) is ad-hoc—mostly when you or Ollie open a ticket (`FTFL-638`, `FTFL-698`, Alloy upgrade, cardinality audit).

---

## Gaps that Hurt "People lOoking at aLerts"

1. Single-human pager concentrator—IRM defaults invite you; knowledge and burden don't fans out. Risk: leave, deep-focus day, or concurrent prod fires.
2. Severity channel sprawl without SLA—prod / non-prod / critical / warnings exist; no clear "who must ack within N minutes" matrix.
3. Noise > signal—`DatasourceNoData`, empty labels, chronic ArgoOutOfSync make ack fatigue rational. Teams learn to ignore channels.
4. Silent failure mode—when Alloy/collectors die, blind spots (you measured overnight collector drop on stress boxes; noted 31h ticker gap as a workshop topic for Jim). Meta-monitoring is weak.
5. Maintenance is project-shaped, not rota-shaped—FTFL-698 stress-test harness, FTFL-673 Alloy/Faro, FTFL-638 Loki labels ship as epics; no weekly "alert debt" ritual.
6. Incident loop incomplete—Detect works; Respond is ad-hoc; Learn (postmortems, alert-tuning tickets, runbook ROTs) is sparse in memory.

---

## Person-centric Operating Model (Forward)

Treat observability as a product with named roles, not a side hustle for whoever opens Slack first.

## Role Map (Assign in kickoff—proposed dEfaults)

| Role | Primary | Backup | Owns | Does _not_ own |
|---|---|---|---|---|
| On-call primary (page) | Rotate: Leon ↔ Ollie ↔ Robin (week-about to start) | Next-up in rota | Ack within SLA; mitigate; declare incident; hand off | Permanent solo ownership of every alert class |
| Observability product owner | Ollie | Leon | Alert taxonomy, dashboards-that-matter, Alloy/k8s-monitoring chart health, OpenCost, workflow metrics | Customer node installs |
| Platform / cluster SRE lead | Leon | Robin | Production cluster health SLOs, IRM integration-as-code, gcx/auth, multi-cluster parity, meta-alerts on collectors | Feature app bugs |
| Customer-node / edge ops | Robin | Leon | Trust/node alerts (`mkuh`, `hie`, `nnuH` patterns), NSG/DNS-related pages | Core FITFILE cloud dashboard backlog |
| App / data secondary | Pavlo | Weronika / app peers | Escalations for OMOP, pipelines, Mongo/SpiceDB app symptoms, PII tooling | First-line node OOM / DaemonSet pages |
| IRM configuration steward | Leon (+ Jude w/ Ollie) |—| Schedules, escalation chains, Slack routes, Terraform-as-code for IRM | Manual one-off UI edits without PR |
| Grafana vendor liaison | Leon (technical) + Gareth (commercial) |—| Jim workshops, Adaptive Metrics/Logs enablement, token/auth | Day-to-day pages |
| Incident commander (IC) | On-call primary | Secondary on-call | Comms in `#incident-room`, timeline, resolve note | Deepest code expert (that's SME) |
| Runbook librarian | Rotate monthly (start: Ollie) | Leon | Every pageable alert has runbook URL; dead links = P2 ticket | Writing every runbook alone—SMEs contribute |

---

## Best-practice Playbook (Fit to _this_ tEam)

## 1. Detect—make Pages Rare and Trustworthy

- Page only user-impacting or SLO-breach conditions (prod API/error budget, Kube critical for user paths, disk full, cert expiry <14d, Alloy/metrics pipeline down).
- Route everything else to `#ops-warnings` as ticket-or-watch, not IRM page.
- Kill or fix top noise first (2-week burn-down):
  - `DatasourceNoData` / empty labels → fix rule or datasource, don't silence forever
  - Argo OutOfSync who-cares vs blocking—split alert; only page on Degraded + health degraded progress stuck
- Meta-monitoring (Leon + Ollie, this sprint): alert when log/metric volume per cluster drops to ~0 for >15m during expected-on windows (except known night-off sandboxes). This is your Jim workshop silent-failure item.

## 2. Respond—person Path, not Hero Path

Proposed on-call product (start simple, 8-week pilot):

- Business hours rota (Mon–Fri 09:00–18:00 UK): Leon / Ollie / Robin weekly
- After-hours: best-effort until headcount grows; explicit "severity 1 only" page overnight so the rota doesn't become always-on.
- IRM schedule + escalation chain (IaC): Primary → Secondary (15m) → resolve-or-IC manager chat. Stop hard-coding invite-Leon.
- Ack SLA:
  - `#ops-critical` / page: ack ≤10 min business hours
  - `#prod-alerts` non-page: ack or ticket ≤1 business day
  - `#ops-warnings`: weekly hygiene, not live ack
- Every pageEvent must end in one of: Resolve + note · Silence-with-ticket · Incident declared. No orphan "firing" walls.

Livetext "looking at alerts" ritual (15 min, start of primary's day):

1. IRM "Mine + Unacked"
2. `#ops-critical` then `#prod-alerts`
3. One-liner in `#dev-ops`: _"On-call day N: X open, Y noise tickets filed"_

## 3. Maintain—continuous, Named

| Cadence | Owner | Ritual |
|---|---|---|
| Daily | On-call | Ack path + open-incident check |
| Weekly 30m "Signal Review" | Ollie (chair) + on-call + Leon | Top 10 firing rules by volume; promote/ demote/delete; runbook gaps |
| Bi-weekly | Leon | Collector health: Alloy targets down, scrape fails, Faro ingestion, cardinality spike (gcx) |
| Monthly | Robin + Leon | Customer-node alert pack review (false positives per Trust) |
| Per incident (Sev1/2) | IC | Blameless note in Confluence; one follow-up ticket max linchpin |
| Quarterly with Jim | Leon | IRM maturity: schedules, insights report, silent-failure drills |

## 4. Runbooks—minimum Viable Quality bar

For each pageable alert:

- Symptom (what user/system feels)
- 5-minute triage (`gcx` / Explore links / kubectl context)
- Blast radius (which customer/nodes)
- Mitigate vs fix
- Escalate to: _role_ (not person name only)
- Link from IRM annotation (you already half-have this)

First pack to write (owner in brackets):

1. Alloy/metrics pipeline silent (Ollie + Leon)
2. Argo Degraded/OutOfSync triage matrix (Leon)
3. KubePodCrashLooping / OOM (Ollie + Pavlo when app)
4. Ingress/DaemonSet stuck (Leon + Robin for node-local)
5. Credential/secret expiry class (service principals, Vault, GitLab)—you already live this with Pavlo/Robin

## 5. Ongoing Maintenance Themes (From oPen work—keep tHem pErson-bound)

| Workstream | Ticket / theme | Driver | On-call relevance |
|---|---|---|---|
| Stress-test observability | `FTFL-698` | Leon + Ollie | Harness metrics must not train the team on wrong dashboards |
| Alloy / Faro / OpenCost | `FTFL-673` | Ollie lead, Leon platform | Collector upgrades = change freezes + watch window |
| Loki structured metadata / labels | `FTFL-638` | Leon | Directly cuts exploration time during pages |
| Cardinality / Adaptive | gcx audits | Leon (+ Gareth for plan) | Cost + query speed for responders |
| Credential rotation toil | AAD/GitLab secrets incidents | Leon + Robin policy | Should become expiring-secret alerts + runbook, not Slack surprise |

---

## 90-day Roadmap (Person-anchored)

## Days 0–14—Stop the Bleeding

- Leon: Export current IRM escalations/invites; propose schedule mirrored in Grafana IRM; draft severity matrix doc (1 page) in Confluence.
- Ollie: Rank top 15 alert rules by 30-day volume; tag Keep / Fix / Delete; open tickets for Fix.
- Robin: Confirm willingness/capacity for one week in three; list node-specific alerts he can own triage for.
- Pavlo: List app symptoms he wants paged vs ticketed (Mongo, pipelines, SpiceDB).
- Team tone check (standup): Explicit "on-call is a role, not Leon's default".

## Days 15–45—Make the Rota Real

- IRM schedule live; Slack @oncall handles/usergroup.
- First weekly Signal Review.
- Meta-alert for telemetry blackhole—Ollie implements, Leon reviews.
- Runbook pack of five (above) linked from annotations—Ollie library; SMEs fill.
- Jim workshop: silent-failure + escalation design—Leon books.

## Days 46–90—Professionalize

- After-hours Sev1-only policy written + tested (game day with Ollie primary, Leon secondary).
- DORA/alert metrics: MTTA, % auto-resolved noise, pages per week per person (fairness).
- Alert-as-code standard (Terraform/grafanactl path you already used in late 2025 IRM work)—no UI-only alert rules.
- Customer-node playbooks under Robin; app secondary rota snippet under Pavlo.

---

## Working Agreements (Paste into Confluence / tEam cHarter)

1. If it pages, a human acks. Silence without a ticket is not done.
2. If it fires >5×/week and isn't user-impacting, it is debt—owned in Signal Review.
3. Changes to page rules go through PR (same as deploy config).
4. On-call is protected focus: no sprint commitment >70% capacity that week.
5. Leaf knowledge is written once—if you fixed it twice from memory, it becomes a runbook line.
6. Heroics are incidents, not process—if Leon is sole resolver three weeks running, the rota design failed; fix the design.

---

## Suggested Kickoff Agenda (45 Min)

1. Agree role map (names above as defaults)—10m
2. Severity × channel matrix—10m
3. First 4-week rota (Leon / Ollie / Robin)—5m
4. Noise burn-down top 5 (Ollie brings data)—10m
5. Jim workshop scope (silent failure + schedules)—5m
6. Owners for first runbook pack—5m

---

## Open Questions to Resolve in that Kickoff (LTM cOuldn't sEttle)

- Exact current IRM schedule JSON / who is secondary today beyond invite-Leon behaviour
- Whether after-hours contractual cover is expected by leadership
- Gareth's desired spend envelope for Adaptive Metrics/Logs (affects noise cut strategy)
- Formal IC list for multi-Trust incidents involving external Security (Tech Ahoy / pen-test paths)

---

## Bottom line for You

You have already built most of the machine (IRM, Slack routes, Alloy, Explore muscle, stress-test observability). The improvement is almost entirely social and ownership systems:

- Ollie = make alerts²true and dashboards useful
- You = IRM/schedules/meta-monitoring + multi-cluster SRE bar
- Robin = share the page weight + own node-edge packs
- Pavlo = expert second line so infra doesn't thrash on app symptoms
- Jim + Gareth = vendor/leverage so the stack supports the process

Do the two-week burn-down + publish a three-name business-hours rota, and "people on call actually looking at alerts" stops being aspirational and becomes observable at the next Signal Review.
