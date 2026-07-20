---
created: 2026-04-29T08:34:48+00:00
modified: 2026-07-20T16:33:29+00:00
permalink: llmeon/raw/2026-04-29-pieces-security-and-maintenance-roadmap
pieces_ids: [1245dff5-c287-4131-8a0c-4825a367dda4, 2bb99982-828c-4126-9610-e25ac846b041, 2c32b6a7-9ec8-43cf-9969-c98bdec19497, 2dde824a-4759-467a-84db-100e7745db42, 4fa0276d-6dae-48a4-9f7e-8b3b8431e634, 8509d2ff-c79a-46d3-8f3f-ef0961888df3]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-04-29-pieces-security-and-maintenance-roadmap
---

Asset: `2dde824a-4759-467a-84db-100e7745db42`

Captured: 2026-04-29T07:03:09.242263Z

```
Leon wants the Security & Maintenance roadmap topic to cover both Platform Security and Application Security, with both quarterly goals and per-sprint capacity allocation. Let me build on my previous response and produce a refined, comprehensive version.
```

---

Asset: `2bb99982-828c-4126-9610-e25ac846b041`

Captured: 2026-04-29T06:59:02.037341Z

Updated: 2026-04-29T07:03:06.091561Z

```
You’ve already got a natural opening to introduce this as a roadmap-level track, because (per your Teams clipboard at 7:37 AM) “everybody has 2 topics to present for the future roadmap” and you’ve got “Planning Topics – presentation” on the calendar (organized by Weronika) visible around 7:34 AM. I’d use one of your two slots to make Security + Maintenance a first-class workstream instead of a once-a-year pen-test scramble.

## 1) How to frame it so it lands (roadmap language, not “extra chores”)
Positioning: “Move from *annual pen test* to *continuous security + maintenance*, with explicit capacity and measurable SLOs.”

One-sentence pitch (copyable):
> We currently treat security/maintenance as an annual event (pen test). We need to treat it as an always-on product quality attribute with a dedicated roadmap track, recurring capacity, and measurable outcomes (patch latency, vuln burn-down, backup/restore drills, access reviews).

Why leadership will care:
- Annual pen tests are detection, not control. Controls need cadence.
- Security and maintenance reduce *probability × blast radius* of incidents; they also reduce delivery drag (less “emergency work”).

## 2) What to put on the roadmap (a concrete “Security & Maintenance” track)
Make it a standing quarterly theme with a small number of epics that repeat.

### Roadmap Track: Security & Maintenance (Continuous)
Epic A — Vulnerability Management (continuous)
- Automated dependency scanning + upgrade cadence
- Container image scanning + base image patch cadence
- Defined patch SLOs (e.g., Critical within 7 days, High within 30)

Epic B — Platform Hardening (quarterly increments)
- Access control & least privilege reviews (IAM/RBAC)
- Secrets management standards (rotation, storage, eliminating long-lived creds)
- Network controls (ingress restrictions, allow-lists, private endpoints where appropriate)

Epic C — Backup/Restore + DR as a routine (maintenance that prevents catastrophe)
This maps directly onto work you already have in motion: your Obsidian Jira note FTFL-596 “Configure the Azure backups module for NNUH & MKUH” (seen 7:37 AM) is essentially *maintenance + resilience* becoming standardized instead of bespoke.
- Backup policy standard (frequency/retention/cost model)
- Restore drills (prove RPO/RTO, not just “we have backups”)

Epic D — Security hygiene in delivery (make the team think about it)
- “Definition of Done” adds: threat-checklist + dependency status + logging/audit basics
- Lightweight threat modeling for new externally-facing endpoints / data flows

## 3) The operating model change (this is the real fix)
If the team “doesn’t even think about it,” the roadmap item must include how it gets time and how it becomes default.

Propose these explicit mechanisms:
1. Capacity reservation: 10–20% of each sprint (or 1 day/week) is reserved for Security & Maintenance tickets.  
2. A single backlog lane + triage cadence: weekly 30-min “Sec/Maint triage” to size, prioritize, and assign.
3. Ownership: name a rotating “Security & Maintenance Champion” each sprint (not a role forever; a duty).
4. Metrics dashboard (simple):
   - # critical/high vulns open; mean time to remediate
   - patch latency vs SLO
   - backup success rate + last restore test date
   - pen test findings burn-down trend (so the yearly test becomes validation, not discovery)

## 4) What you can present in the meeting (2-slide structure)
### Slide 1 — Problem / Risk
- Current state: “Security/maintenance = yearly pen test + ad hoc fixes”
- Consequence: unknown exposure window, recurring emergency work, inconsistent standards

### Slide 2 — Proposal / Roadmap
- Create “Security & Maintenance” roadmap track
- Reserve capacity + add cadence + define metrics
- Seed epics: vuln mgmt, hardening, backups/restore drills (cite FTFL-596 as an immediate example), delivery hygiene

## 5) Two quick questions so I can help you tailor it to FITFILE reality
1) Do you want this framed primarily as platform/infrastructure security (IAM, K8s, networks, backups), or also application security (auth flows, API hardening, secure coding practices)?  
2) Are you aiming for a quarterly roadmap theme or a per-sprint fixed allocation (recommended: both—quarterly goals + per-sprint capacity)?

If you answer those, I’ll turn this into a crisp “roadmap proposal” blurb you can paste directly into Jira/Confluence (plus a small list of starter tickets that make it real immediately).
```

---

Asset: `8509d2ff-c79a-46d3-8f3f-ef0961888df3`

Captured: 2026-04-29T06:58:51.431092Z

```
Planning security improvements

I’m looking to address Reliability Maintenance by rolling out a backups module, conducting DR tests, and practicing restore drills. I also want to enhance observability for security through audit logging and alerts. For pen test readiness, I'll focus on reducing issues, implementing quarterly internal tests, and tracking metrics like patch latency and critical vulnerabilities. I plan to suggest this as one of two presentation topics, along with a mini-outline, while asking about the scope and timeframe. Training and threat modeling sessions would also be beneficial.
```

---

Asset: `1245dff5-c287-4131-8a0c-4825a367dda4`

Captured: 2026-04-29T06:58:49.366292Z

```
Creating a security roadmap pitch

I should propose a "Security & Maintenance as First-Class Roadmap Track" by emphasizing "continuous security" instead of just annual penetration tests. I want to structure a 30-second pitch with a couple of slides. I need to avoid referencing any file paths in the context of Obsidian notes. Formatting time as AM/PM is also vital. The roadmap will include quarterly goals like baseline hardening and continuous vulnerability scanning, as well as new rituals like monthly security sprints and defining value for done.
```

---

Asset: `4fa0276d-6dae-48a4-9f7e-8b3b8431e634`

Captured: 2026-04-29T06:57:24.212446Z

Updated: 2026-04-29T07:03:06.084996Z

```
I want to put the topic of security and maintance on the roadmap. currently it is not something the team even thinks about. They leave it up to a yearly pen test. It is the single most important part and it gets the least focus time.
```

---

Asset: `2c32b6a7-9ec8-43cf-9969-c98bdec19497`

Captured: 2026-04-29T06:39:25.046195Z

Updated: 2026-04-29T07:03:06.078054Z

```
### What was the Obsidian note?
From the long-term memories I can see two Obsidian notes you had open this morning, but neither one is clearly the “platform poset” note:

1) “2026-04-28-pieces-omop-stress-testing-plan” (seen at 7:32 AM)  
2) “Stress Test Execution Plan” (seen at 7:36 AM) — this one contains the synthesized plan text and references the Miro board + Jira anchors.

I don’t have a captured memory snippet showing the note that contains “platform poset” specifically, so I can’t name it with certainty from the current context.

#### Fastest way to locate it in Obsidian (30–60 seconds)
1) Quick Switcher: `Cmd+O` → type “poset”  
2) If that fails: `Cmd+Shift+F` (Search) → search for:
   - `poset`
   - `"platform poset"`
   - `partial order`
   - `roadmap`
   - `Planning Topics`
3) If you remember it was created “today”: open File Explorer in Obsidian → sort by Modified time → look for the most recent note around when you created the topic list.

If you paste me the top 10 lines (or the note title list from search results), I can tell you which one matches and help tighten the two topics.

---

### Meeting context (so we prep the right thing)
- Teams calendar shows “Planning Topics - presentation” (organized by Weronika Jastrzebska) visible at 7:34 AM.
- Your clipboard note at 7:37 AM says: “Everybody has 2 topics to present for the future roadmap.”

---

## Two solid topics you can bring (based on what you’ve been working on)
Below are two options that are strongly supported by your recent notes/threads—pick these unless your “platform poset” note suggests different priorities.

### Topic A — OMOP Stress Testing: proving capacity + federation behavior
Why it’s roadmap-worthy: it converts “we think it scales” into measurable platform guarantees.  
Your supporting material: the Obsidian notes above + Oliver’s suggestion to use [omock](https://ohdsi.github.io/omock/) for easier mock generation (Teams chat seen 7:16–7:33 AM) + your Miro link (shared in the same chat): [NHS Synthetic Data & OMOP Pipeline](https://miro.com/app/board/uXjVGh4h0_g=/?share_linkid=49586236545)

30-second structure to present
- Problem: we don’t yet have hard numbers/curves for p50/p95/p99 latency + resource usage as data/node count grows.
- Proposal: run a phased stress plan: single-node → 2/3/5-node federation; record latency/CPU/mem/IO/error rate.
- Output: a “capacity envelope” and a repeatable benchmark harness.
- Decision needed: realistic synthetic data vs “good enough” mocks (omock) depending on what we’re validating.

### Topic B — Azure Backups module rollout for data providers (NNUH & MKUH)
Why it’s roadmap-worthy: it’s core resilience/compliance work that needs standardization across providers (not one-off fixes).  
Your supporting material: your Obsidian Jira note FTFL-596: Configure the Azure backups module for NNUH & MKUH (seen 7:37 AM).

30-second structure to present
- Problem: backups module not enabled for some EoE data providers; need consistent backup posture for app PVCs + Hyve OMOP DB.
- Proposal: define backup policy (frequency, retention, cost model, PVC classes), then enable module + private endpoint dependency.
- Dependencies/risks: private endpoint subnet prerequisite; service principal permissions/roles per provider.
- Outcome: repeatable provider onboarding standard (less ad-hoc infra variance).

---

### If your “platform poset” note is important: quick way to map it into a topic
If “platform poset” was you describing dependency ordering / what must precede what, you can convert it into a roadmap topic like:
- “Platform dependency ordering (‘poset’) → a formalized delivery sequence + gating criteria”
  - outputs: dependency map, gates (security, backup, observability), “allowed parallelism,” and a canonical rollout order.

Send me the note title once you find it (or paste the section headings), and I’ll help you select the best 2 topics and turn them into 2 clean slides each.
```

---
