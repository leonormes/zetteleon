---
tags: [confluence, ffnode, stress-testing, review, ollie-rushton, weronika-jastrzebska]
source: confluence/doc/2839871490
created: 2026-06-11
author: Leon Ormes
status: draft
---

# FFNode Stress Testing — Design Document v4: Review Comment Changes

**Source:** Confluence page "FFNode Stress Testing—Design Document v3" ([link](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2839871490))
**Current version:** v3 / v5 (restructured + review comments addressed)  
**Reviewers who commented:** Ollie Rushton (67 comments), Weronika Jastrzebska (12 comments)  
**Next version:** v4 (this plan → to be drafted as Obsidian note → uploaded to Confluence)

---

## Route Map

This plan maps 71 review comments to 10 thematic change blocks. Each block lists the comment(s), the required change, and the target section(s) in the Confluence doc.

---

## Block 1: Infrastructure — 5 New Synthetic Nodes Only (§7)

**Context:** Ollie repeatedly states existing production nodes must not be used for stress testing — 5 brand new nodes are required, communicating solely via public endpoints with no intra-cluster routing or vVPN/IPsec.

| # | Comment | Change |
|---|---|---|
| 1 | "We need 5 brand new nodes - cannot use our existing nodes" | **Rewrite §7.1.** Remove all production node references (ff-a, ff-b, ff-c, barts, cuh-prod-1, mkuh-prd-4, nwsde-prod-1). Replace with 5 new synthetic-only nodes. Update §7.2 accordingly. |
| 2 | "no intra-cluster - all of it via public endpoints" | **Update §7.4 (networking).** Remove intra-cluster routing. All inter-node traffic traverses public endpoints. |
| 3 | "None use this" (re: vVPN / IPsec) | **Remove vVPN/IPsec from D2.** Decision D2 becomes moot with no production nodes in test bed. |
| 4 | "No, don't touch mkuh-prd-4 - No production nodes will be used within this stress tests!" | **Remove all prod node references from dependencies.** Drop FTFL-638 (mkuh-prd-4 Alloy sync) as a pre-condition. |

**Blocker impact:** This fundamentally changes the environment topology. All references to specific prod nodes throughout the document must be purged or replaced.

---

## Block 2: Test Scope & Permutation Grid (§6, §8)

**Context:** Ollie wants an additional permutation dimension (Export) added to the grid, and several scope clarifications.

| # | Comment | Change |
|---|---|---|
| 5 | "Also, we need to add 'export' to the permutation list" | **Add Export as a 6th dimension in §8.1.** The grid goes from 216 to 432 cases (or simplifies elsewhere to keep it manageable). |
| 6 | "Add export in the same way you have done privacy treatment" | **Export dimension (X):** Binary — X=On (S3 export stage enabled) / X=Off (no export). Follows same pattern as Privacy treatment. |
| 7 | "Add a note that private networking solutions (Express Route, site-to-site VPN) are out of scope" | **Add to §6.2 Out of Scope list.** |
| 8 | "do you mean PII" | **Edit text.** Check every instance — likely "PHI" (Protected Health Information) was intended, not "PII" (Personally Identifiable Information). The clinical context uses PHI. |
| 9 | "concurrent" | **Fix typo or clarify usage.** Likely refers to concurrent query terminology. |
| 10 | "We don't necessarily have time to carry on forever beyond the requirement" | **Add explicit scope boundary.** The test stops at the defined customer requirement limit, not indefinite limit-seeking. §4.4 "limit-finding" language needs tempering. |

---

## Block 3: Privacy Treatment — No K-Anonymity (§5, §8, §11)

**Context:** Ollie clarifies that only the default privacy treatment template is in scope — k-anonymity is not applied in this programme.

| # | Comment | Change |
|---|---|---|
| 11 | "We are only applying the default privacy treatment template - no k-anonymity" | **Remove all k-anonymity references throughout.** Replace with "default privacy treatment template" in §5 (Axis C success criteria), §8.2 (Wave A purpose), §11 (risk 3). |
| 12 | "Out of scope - included in F3 using default privacy treatment template" | **Update F5 dimension description.** F5 is exercised by F3 when P=On; no separate k-anonymity benchmark. |

---

## Block 4: Data Quality Gates — Simpler (§9)

**Context:** Ollie significantly simplifies the pre-flight gates — WhiteRabbit and DQD are out; only Achilles + schema integrity remain.

| # | Comment | Change |
|---|---|---|
| 13 | "Not white rabbit, just Achilles" | **Remove §9.3 (WhiteRabbit).** |
| 14 | "You can get all this from the Achilles reports" | **Remove §9.3 entirely.** Gate is: OMOP schema + FK integrity + Achilles profiles only. |
| 15 | "Remove this" (re: DQD) | **Remove §9.5 (DQD).** |

---

## Block 5: HDRUK SLA & Success Criteria — Reframe (§4, §5, §15)

**Context:** Both Ollie and Weronika challenge the HDRUK 5-minute timeout as primary success criterion. SDE primarily uses the FITFILE application, not HDRUK directly. Weronika adds AS05/AS06 milestone traceability requirements.

| # | Comment | Change |
|---|---|---|
| 16 | "HDRUK is low importance for the SDE... they use FITFILE application solely" | **Reprioritise.** Add FITFILE application internal SLA as primary; HDRUK timeout becomes a secondary external constraint. |
| 17 | "Need to link to AS05/AS06 contractual requirements" | **Add milestone mapping matrix.** Map each axis and success criterion to AS05/AS06 deliverable requirement. |
| 18 | "Cost-per-query is a required AS05 output metric" | **Add cost-per-query metric to Axis A/B/C success criteria tables in §5.** |
| 19 | "We can't force this to happen, but we can observe it if it happens" (re: silent failure reproduction) | **Change §8.3.** From deliberate throttle test to observed-behaviour-only — document that we watch for it, not force it. |

---

## Block 6: Ticket Plan — Major Reduction (§16)

**Context:** Ollie marks 7+ tickets for removal, questions duplication, and wants simplification.

| # | Comment | Change |
|---|---|---|
| 20 | "remove" (on NEW10, NEW11, NEW3, NEW6, NEW9, NEW7, NEW8) | **Remove 7 tickets from §16.1.** Keep only: NEW1 (dataset manifest), NEW2 (Person_ID overlap), NEW4 (query harness), NEW5 (Phase 2 harness), NEW12 (final report). |
| 21 | "Might as well make this a 1million pointer" (on NEW1 dataset size) | **Bump NEW1 spec to 1M patients/node.** |
| 22 | "split it out into separate tickets" | **Restructure remaining tickets** — split Phase 3 execution tickets by wave. |
| 23 | "What does this mean? You already have the test runner above?" | **Merge or remove NEW5.** Phase 2 baseline test harness may be the same work as NEW4 (query harness). |
| 24 | "Analyse the current Azure deployment... Improve terraform... Migrate Nginx to Gateway API" | **Add separate deployment-improvement tickets** outside the stress-test ticket set. Create a companion epic for infrastructure improvements. |

---

## Block 7: Monitoring — Simplify to Existing (§10)

**Context:** Ollie wants to use existing Grafana/k8s observability dashboards, not build bespoke panels.

| # | Comment | Change |
|---|---|---|
| 25 | "Is the Kubernetes Observability dashboards enough to monitor all the things we need to?" | **Simplify §10.** Default to existing k8s observability dashboards first; only build bespoke panels if gaps are found. |
| 26 | "We cannot use these" (re: specific metrics from cloud providers) | **Remove inaccessible metrics.** |
| 27 | "Let's just see what we have available from the prometheus metrics of PostgreSQL and MS SQL charts" | **Adopt pragmatic approach.** §10.2 three required dashboard panels become nice-to-have, not must-have. |

---

## Block 8: Hyve / ETL — De-Scope (§12, §9)

**Context:** Ollie clarifies that the OMOP nodes are not Hyve-generated, and Hyve pipeline testing is The Hyve's responsibility.

| # | Comment | Change |
|---|---|---|
| 28 | "These are OMOP - so there will be no hyve work" | **Reduce §12.** The nodes use Synthea → OMOP directly; no Hyve ETL involved. |
| 29 | "The Hyve responsibility - not us" (multiple) | **De-scope Axis D / Phase 4.** Remove or drastically shrink the Hyve section. Document as external dependency. |

---

## Block 9: Reporting — Dual-Audience Phase 5 (§5, Phase 5)

**Context:** Weronika adds detailed requirements for Phase 5 reporting to serve both internal FITFILE and external SDE audiences.

| # | Comment | Change |
|---|---|---|
| 30 | "Phase 5 report needs to serve two audiences: internal + SDE" | **Restructure Phase 5 deliverables.** Internal section: infra spec, ticket recommendations, run manifests. SDE section: AS05 evidence, top-3 issues for AS06, baseline metrics for comparative re-testing. |
| 31 | "NEW12 acceptance criteria should include: AS05 milestone evidence, top-3 issues, baseline exports" | **Expand NEW12.** Add explicit AC for SDE delivery confirmation, cost-per-query methodology doc, and baseline metric exports. |
| 32 | "SDE project area delivery confirmation as explicit acceptance criteria" | **Add to §5 success criteria.** Confirmed delivery to correct SDE area with evidence in Phase 5 report. |

---

## Block 10: Federation Behaviour — Document Current State (§8.3, OQ-4)

**Context:** Ollie clarifies that fitConnect currently has no node-unavailability resilience, and this is Hutch team's domain.

| # | Comment | Change |
|---|---|---|
| 33 | "Currently no - the behaviour is not resilient to a node not being available. But the user can just unselect it and run again" | **Update §8.3.** Document current known behaviour (no resilience, manual node deselection) rather than treating it as a test target. |
| 34 | "We do not own this system - the hutch team should do this" | **Move OQ-4 to external dependency.** Assign to Hutch team; remove from FITFILE open items. |

---

## Summary: Change Matrix

| Block | Section | Impact | Changes | Priority |
|---|---|---|---|---|
| 1. Infrastructure | §7 | **High** — rewrite environment topology | 4 | P0 |
| 2. Scope & Permutation | §6, §8 | **High** — add new dimension, re-scope | 6 | P0 |
| 3. Privacy Treatment | §5, §8, §11 | Medium — terminology sweep | 2 | P0 |
| 4. Data Quality Gates | §9 | Medium — remove 2 sections | 3 | P0 |
| 5. HDRUK SLA & Success Criteria | §4, §5, §15 | **High** — reframe primary metric | 4 | P0 |
| 6. Ticket Plan | §16 | **High** — major reduction | 5 | P1 |
| 7. Monitoring | §10 | Medium — simplify | 3 | P1 |
| 8. Hyve / ETL | §12 | **High** — de-scope | 2 | P1 |
| 9. Reporting | §5, Phase 5 | Medium — expand | 3 | P1 |
| 10. Federation Behaviour | §8.3 | Medium — document only | 2 | P1 |

**Next step:** Draft v4 in full as an Obsidian note, then upload to Confluence as a replacement page.