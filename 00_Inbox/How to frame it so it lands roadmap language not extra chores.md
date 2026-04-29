---
created: 2026-04-29T06:59:38+00:00
modified: 2026-04-29T07:01:41+00:00
title: How to frame it so it lands roadmap language not extra chores
---

You've already got a natural opening to introduce this as a roadmap-level track, because (per your Teams clipboard at 7:37 AM) "everybody has 2 topics to present for the future roadmap" and you've got "Planning Topics–presentation" on the calendar (organized by Weronika) visible around 7:34 AM. I'd use one of your two slots to make Security + Maintenance a first-class workstream instead of a once-a-year pen-test scramble.

## 1) How to Frame it so it Lands (roadmap Language, not "extra chores")

Positioning: "Move from _annual pen test_ to _continuous security + maintenance_, with explicit capacity and measurable SLOs."

One-sentence pitch (copyable):

> We currently treat security/maintenance as an annual event (pen test). We need to treat it as an always-on product quality attribute with a dedicated roadmap track, recurring capacity, and measurable outcomes (patch latency, vuln burn-down, backup/restore drills, access reviews).

Why leadership will care:

- Annual pen tests are detection, not control. Controls need cadence.
- Security and maintenance reduce _probability × blast radius_ of incidents; they also reduce delivery drag (less "emergency work").

## 2) What to Put on the Roadmap (a Concrete "Security & Maintenance" track)

Make it a standing quarterly theme with a small number of epics that repeat.

### Roadmap Track: Security & Maintenance (Continuous)

Epic A—Vulnerability Management (continuous)

- Automated dependency scanning + upgrade cadence
- Container image scanning + base image patch cadence
- Defined patch SLOs (e.g., Critical within 7 days, High within 30)

Epic B—Platform Hardening (quarterly increments)

- Access control & least privilege reviews (IAM/RBAC)
- Secrets management standards (rotation, storage, eliminating long-lived creds)
- Network controls (ingress restrictions, allow-lists, private endpoints where appropriate)

Epic C—Backup/Restore + DR as a routine (maintenance that prevents catastrophe)

This maps directly onto work you already have in motion: your Obsidian Jira note FTFL-596 "Configure the Azure backups module for NNUH & MKUH" (seen 7:37 AM) is essentially _maintenance + resilience_ becoming standardized instead of bespoke.

- Backup policy standard (frequency/retention/cost model)
- Restore drills (prove RPO/RTO, not just "we have backups")

Epic D—Security hygiene in delivery (make the team think about it)

- "Definition of Done" adds: threat-checklist + dependency status + logging/audit basics
- Lightweight threat modeling for new externally-facing endpoints / data flows

## 3) The Operating Model Change (this is the Real fix)

If the team "doesn't even think about it," the roadmap item must include how it gets time and how it becomes default.

Propose these explicit mechanisms:

1. Capacity reservation: 10–20% of each sprint (or 1 day/week) is reserved for Security & Maintenance tickets.
2. A single backlog lane + triage cadence: weekly 30-min "Sec/Maint triage" to size, prioritize, and assign.
3. Ownership: name a rotating "Security & Maintenance Champion" each sprint (not a role forever; a duty).
4. Metrics dashboard (simple):
   - critical/high vulns open; mean time to remediate
   - patch latency vs SLO
   - backup success rate + last restore test date
   - pen test findings burn-down trend (so the yearly test becomes validation, not discovery)

## 4) What You Can Present in the Meeting (2-slide structure)

### Slide 1—Problem / Risk

- Current state: "Security/maintenance = yearly pen test + ad hoc fixes"
- Consequence: unknown exposure window, recurring emergency work, inconsistent standards

### Slide 2—Proposal / Roadmap

- Create "Security & Maintenance" roadmap track
- Reserve capacity + add cadence + define metrics
- Seed epics: vuln mgmt, hardening, backups/restore drills (cite FTFL-596 as an immediate example), delivery hygiene

## 5) Two Quick Questions so I Can Help You Tailor it to FITFILE Reality

1. Do you want this framed primarily as platform/infrastructure security (IAM, K8s, networks, backups), or also application security (auth flows, API hardening, secure coding practices)?
2. Are you aiming for a quarterly roadmap theme or a per-sprint fixed allocation (recommended: both—quarterly goals + per-sprint capacity)?

If you answer those, I'll turn this into a crisp "roadmap proposal" blurb you can paste directly into Jira/Confluence (plus a small list of starter tickets that make it real immediately).
