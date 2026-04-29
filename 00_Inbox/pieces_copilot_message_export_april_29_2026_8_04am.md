---
created: 2026-04-29T07:04:13+00:00
modified: 2026-04-29T07:40:24+00:00
title: pieces_copilot_message_export_april_29_2026_8_04am
---

## Security & Maintenance Roadmap Track: Platform + Application Security

Building on our earlier discussion—here's the full version scoped to both platform and application security, with quarterly themes and per-sprint allocation so it's immediately actionable in Weronika's planning session.

---

### 1) Quarterly Roadmap Themes (Rolling 4-Quarter View)

Each quarter has a platform security and an application security focus area that run in parallel.

| Quarter | Platform Security Theme | Application Security Theme | Exit Criteria |
|---|---|---|---|
| Q1 (Current / Next) | Pen-test remediation burn-down + IAM least-privilege—CORS allow-lists, rate-limiting, JWT secret rotation, production backup account lockdown, EBS CSI `AmazonEBSCSIDriverPolicyV2` migration | Auth & API hardening—review all auth flows (JWT validation, session handling), API input validation, error-message leakage audit | 0 Critical / 0 High pen-test findings open; IAM audit clean; OWASP Top 10 baseline checklist green |
| Q2 | Network & secrets posture—private endpoints rollout (ref: FTFL-615g Azure Backups subnet), ingress restrictions, secrets rotation automation (HashiCorp Vault / Azure Key Vault) | Dependency & supply-chain security—automated SCA scanning in CI, container base-image policy, SBOM generation | All secrets < 90-day rotation; no public endpoints for internal services; SCA gates blocking Critical in CI |
| Q3 | Backup/Restore + DR drills—standardized backup policy across providers (ref: FTFL-596 for NNUH & MKUH), prove RPO/RTO with live restore drills | Secure SDLC integration—threat modeling for new features, security "Definition of Done," lightweight security reviews in PR process | Restore drill passed for every data provider; threat model template adopted for all new epics |
| Q4 | Observability & audit—security-event dashboards (Grafana), audit-log completeness, anomaly alerting | Penetration re-test & validation—annual pen test becomes _validation_ of continuous work, not _discovery_ | Pen test confirms ≤ 2 Medium findings; audit trail covers all admin actions; dashboard live |

---

### 2) Per-Sprint Allocation (The Operating Model)

This is the part that actually changes behavior. Without explicit sprint capacity, it stays aspirational.

#### Recommended Split: 20% of Sprint Capacity Reserved for Security & Maintenance

For a typical 2-week sprint with ~80 story points of capacity:

| Allocation | Points | What Goes Here |
|---|---|---|
| Platform Security | ~8 pts (10%) | IAM reviews, network hardening, secrets rotation, backup config, infra patching, K8s RBAC |
| Application Security | ~8 pts (10%) | Auth flow fixes, API hardening, dependency upgrades, secure coding fixes, threat model actions |
| Feature / Delivery | ~64 pts (80%) | Normal product backlog |

#### Sprint Ceremonies to Support This

1. Security & Maintenance Triage—30 min, weekly (Tuesday or Wednesday)
   - Review new vulns from scanning tools
   - Prioritize against quarterly theme
   - Size and assign into current/next sprint
   - Attendees: you + Ollie (as the "Security Hardening" unit) + rotating team member

2. Sprint Planning—Security tickets are pre-loaded into the sprint before feature negotiation begins. They are not "stretch goals"—they are committed capacity.
3. Sprint Review—Security work is demoed/reported alongside features. This normalizes it as "real work."

#### Backlog Structure (Jira)

Create two epics that persist across sprints:

```
Epic: Platform Security (Continuous)
  ├── Label: sec-platform
  ├── Quarterly sub-epic: Q1 - Pen Test Remediation & IAM
  └── Stories: CORS fix, rate-limiting, JWT rotation, EBS CSI policy, etc.

Epic: Application Security (Continuous)  
  ├── Label: sec-application
  ├── Quarterly sub-epic: Q1 - Auth & API Hardening
  └── Stories: JWT validation audit, input sanitization, error-message review, etc.
```

Filter: `label in (sec-platform, sec-application)` gives you instant visibility of all security work.

---

### 3) Metrics Dashboard (How You Prove It's Working)

#### Platform Security Metrics

- Patch latency vs SLO (Critical ≤ 7 days, High ≤ 30 days)
- # open infrastructure vulns by severity (trend line)
- Secrets age—% of secrets within rotation policy
- Backup success rate + last restore drill date per provider
- IAM policy drift—# of over-privileged roles

#### Application Security Metrics

- # open application vulns by severity (from SCA + DAST)
- Dependency freshness—% of deps within 1 major version
- CI gate pass rate—% of pipelines passing security gates without override
- Threat models completed—ratio of new features with vs without

---

### 4) Presentation-Ready: 2 Slides for the Meeting

#### Slide 1—The Problem

Title: _Security is an afterthought—and it's our biggest risk_

- Current state: security = annual pen test + ad-hoc emergency fixes
- No dedicated capacity → findings languish → risk accumulates
- Both layers are exposed:
  - Platform: IAM over-privilege, inconsistent backup posture, unpatched infra (you and Ollie are already firefighting CORS, JWT, rate-limiting from the latest pen test)
  - Application: no systematic auth/API review, no dependency scanning gates in CI, no threat modeling

#### Slide 2—The Proposal

Title: _Continuous Security & Maintenance—quarterly themes + 20% sprint allocation_

- Quarterly goals set the direction (see table above)
- 20% per sprint (10% platform, 10% application) makes it real
- Weekly triage keeps it prioritized
- Metrics dashboard proves ROI and makes the annual pen test a _validation_, not a _discovery_
- Immediate wins already in flight: FTFL-596 (Azure backups for NNUH/MKUH), pen-test remediation with Ollie, EBS CSI least-privilege migration

---

### 5) One-Paragraph Blurb (Pasteable into Confluence / Jira)

> Roadmap Track: Platform & Application Security (Continuous)
> We propose establishing security and maintenance as a permanent roadmap track with two parallel streams—_Platform Security_ (IAM, networking, secrets, backups, infrastructure patching) and _Application Security_ (auth flows, API hardening, dependency scanning, secure SDLC). Each quarter defines a theme and exit criteria for both streams. Sprint capacity is reserved at 20% (10% platform, 10% application) with a weekly triage to prioritize work. Success is measured via patch-latency SLOs, vulnerability burn-down, backup/restore drill results, and CI security-gate pass rates. The goal: the annual pen test validates our posture rather than revealing it.

---

Want me to generate the starter Jira tickets (broken into platform vs application) so you can seed both epics before the meeting?
