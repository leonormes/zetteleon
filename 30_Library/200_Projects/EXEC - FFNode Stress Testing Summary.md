---
aliases: []
created: 2026-06-17T11:45:00+00:00
modified: 2026-07-13T08:44:37+00:00
permalink: llmeon/30-library/200-projects/exec-ffnode-stress-testing-summary
project_name: Stress Testing
tags: [as05-milestone, fitfile, infrastructure, management, testing]
title: EXEC - FFNode Stress Testing Summary
---

## FFNode Stress Testing—Executive Summary

Status: Draft | Author: Leon Ormes | Audience: Leadership / Stakeholders

---

### The Problem (In Plain English)

In April 2026, our FITFILE federated data system experienced a query timeout that we only learned about because a customer complained. We fixed the immediate symptom but discovered two underlying gaps:

1. No predictability—we cannot forecast when performance will break under realistic clinical load
2. No visibility—failures are silent at our end; we depend on customers to tell us about them

This programme defines a structured testing plan to solve both.

---

### What We're Testing (Three Layers)

| Layer | What matters | Success =? |
|-------|-------------|-----------|
| Single-node capacity | Can one data node handle a realistic patient cohort? | Query latency stays predictable up to 5M patients; cost per query is documented |
| Multi-node federation | What's the penalty when we query across multiple NHS trusts? | Querying 2, 3, and 5 nodes together completes reliably; overhead is quantified |
| Workflow permutations | How do privacy, export, and data scope interact? | Export to S3 works; privacy doesn't break data links; cost scales linearly |

---

### Key Deliverables (By 31 July 2026)

#### For Management

- Known working limit—"FITFILE can reliably federate X patients across Y nodes"
- Cost-per-query baseline—£X to run a 1M-patient cohort discovery
- Top-3 risks identified—with reproducible test coordinates so engineering can fix them

#### For SDE (Secure Data Environment)

- Proof that FITFILE scales to the contracted 5-node requirement
- Architecture recommendations for the next 2 years
- Candidate improvements for follow-on work (AS06)

---

### How We'll Do It (5 Phases)

| Phase | What | Duration | By date |
|-------|------|----------|---------|
| 0 | Register datasets, verify they meet size threshold | 0.5 day | Sprint 16 |
| 1 | Pre-flight quality gates (data integrity checks) | 1–2 days | Sprint 17 |
| 2 | Single-node baseline testing | 1–2 days | Sprint 17 |
| 3 | Multi-node federation + complexity testing (4 waves) | 5–9 days | ~Sprint 18 |
| 4 | Final report + recommendations | 0.5–1 day | 31 July 2026 |

Total programme duration: ~4 weeks (concurrent with standard sprint work)

---

### Why This Timeline Is Tight (Position B)

We agreed to stop testing once we hit the contractual requirement (AS05), not continue beyond it. This means:

- ✅ Do: Prove 5-node federation works at scale
- ✅ Do: Document cost and identify risks
- ❌ Skip: Exhaustive permutation testing, chaos engineering, cross-cloud scenarios

This scope gives us 4 weeks to deliver proof of contractual compliance.

---

### Critical Dependencies (Blockers Before We Start)

| Blocker | Status | Impact if missed |
|---------|--------|-----------------|
| 5 new test nodes provisioned | TBC | Cannot run any tests |
| Datasets finalised & verified | TBC | Cannot start Phase 0 |
| Internal latency SLA defined | 🔴 NOT YET | Cannot grade Phase 2 results (currently using vague 5-min HDRUK target) |
| Data overlap computed | TBC | Cannot design multi-node tests |

Action: Leon + Ollie + Robin must resolve these before Sprint 16 ends.

---

### What Success Looks Like

✅ All 5 nodes pass data integrity gates

✅ Single-node queries complete within our internal SLA at 5M-patient scale

✅ Querying 5 nodes together is possible (even if slow)

✅ Cost-per-query is documented with clear methodology

✅ Top 3 performance risks are identified and can be reproduced on demand

Stretch goal: Architecture recommendations credible enough for EoE SDE to commit to follow-on work (AS06).

---

### Key Risks We're Watching

| Risk | Likelihood | Mitigation |
|------|------------|-----------|
| Network bandwidth saturates when querying 5 nodes | High | Monitor cross-node bytes; cap if needed |
| Privacy rules break referential integrity | High | Validate after every privacy-ON test |
| Database runs out of memory under load | Medium | Right-size nodes before Phase 2 |
| A node fails silently (like April incident) | High | Ensure monitoring surfaces this |
| Cost burn exceeds budget | Medium | Set daily ceiling; abort if breached |

---

### Who Needs to Do What

| Role | Responsibility | Timeline |
|------|-----------------|----------|
| Leon Ormes (Platform) | Programme lead; Phase 0–4 execution; infrastructure | Ongoing |
| Oliver Rushton (Query strategy) | Query design; SLA definition; wave sign-off | ASAP (SLA needed for Phase 2) |
| Ollie/Robin (Infra) | Node provisioning; networking; monitoring setup | Sprint 16 |
| Weronika Jastrzębska (SDE) | Stakeholder alignment; final report audience | Ongoing |
| Jakub Jaworski (CUH) | DB indexing strategy reference | As-needed |

---

### Questions for Leadership

1. Is the 31 July deadline realistic? (Depends on blockers being resolved in Sprint 16)
2. Are we comfortable with "Position B" scope, or should we allocate more time for deeper testing?
3. If we find showstoppers in Phase 3, do we pivot scope or add time?
4. Who owns the SDE follow-on (AS06) if we identify high-impact findings?

---

### Next Steps

- [ ] This week: Resolve blockers B1–B5 (data, nodes, SLA)
- [ ] Sprint 16: Raise 11 new Jira tickets; confirm Phase 0 can start
- [ ] Sprint 17: Phase 1–2 (pre-flight checks + single-node baseline)
- [ ] Sprint 18: Phase 3 (federation waves); daily reporting
- [ ] By 31 July: Phase 4 (dual-audience report)

---
